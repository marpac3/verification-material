#!/usr/bin/env python3
"""Gate all W4 artifacts: PDF fidelity, layout, provenance and retained text.

Generated provenance records are checked against current book sources. Historical
handout numerical exceptions are separately inventoried; they are not silently
accepted as projection claims. Notes are compared page-by-page including the
complete assigned book exercise. Reports live with the generated artifacts.
"""
from __future__ import annotations
import argparse
import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
from bs4 import BeautifulSoup
import fitz

ROOT = Path(__file__).resolve().parent.parent


def gate(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'slides' / (name + '.py'))
    result = importlib.util.module_from_spec(spec); spec.loader.exec_module(result)
    return result


def check(folder: Path) -> list[str]:
    deck, text, provenance = [gate(n) for n in ('check_deck','check_text','check_provenance')]
    issues = []; report = []; manifests = sorted((ROOT / 'slides/lessons').glob('lesson*.json'))
    if len(manifests) != 7: issues.append('expected exactly seven lesson manifests')
    for manifest in manifests:
        data = json.loads(manifest.read_text()); n = data['number']; slug = data['slug']
        if len(data['slides']) > 28 or sum(s['minutes'] for s in data['slides']) != 90:
            issues.append(f'lesson {n}: slide/timing budget')
        if sum(s.get('kind') == 'question' for s in data['slides']) < 3:
            issues.append(f'lesson {n}: fewer than three discussion questions')
        if sum(s.get('kind') == 'exercise' for s in data['slides']) != 1:
            issues.append(f'lesson {n}: expected one assigned exercise')
        for kind in ('lesson','handout','notes'):
            path = folder / f'{kind}{n}_{slug}.html'; pdf = path.with_suffix('.pdf')
            if not path.is_file() or not pdf.is_file():
                issues.append(f'{path.stem}: missing HTML/PDF'); continue
            if pdf.stat().st_mtime <= path.stat().st_mtime: issues.append(f'{path.stem}: stale PDF')
            if kind != 'notes':
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    r1 = deck.check_rendered(path, pdf, folder / f'{path.stem}.pages.json')
                    r2 = text.check(path, pdf)
                (folder / f'{path.stem}.checks.log').write_text(output.getvalue())
                if r1 or r2: issues.append(f'{path.stem}: rendered-page/text gate; see checks.log')
                # Footer failures/collisions are advisory in the old tool, mandatory in W4.
                if 'FOOTER' in output.getvalue() or 'COLLISION' in output.getvalue():
                    issues.append(f'{path.stem}: footer placement; see checks.log')
                source_issues = provenance.check(path, path.with_suffix('.provenance.json'))
                if source_issues: issues.extend(f'{path.stem}: {e}' for e in source_issues)
            soup = BeautifulSoup(path.read_text(), 'html.parser')
            if kind == 'handout':
                original = ROOT / data['handout_source']
                expected = BeautifulSoup(original.read_text(),'html.parser').select('section.slide')
                actual = soup.select('section.slide')
                if len(expected) != len(actual) or any(a.get_text() != b.get_text() for a,b in zip(expected,actual)):
                    issues.append(f'{path.stem}: original handout text changed')
                if data.get('handout_sha256') != hashlib.sha256(original.read_bytes()).hexdigest():
                    issues.append(f'{path.stem}: historical source changed from pinned manifest')
            if kind == 'notes':
                sections = soup.select('section.teacher-page'); pages = fitz.open(pdf)
                if len(sections) != len(pages): issues.append(f'{path.stem}: note/page mismatch')
                for i,(section,page) in enumerate(zip(sections,pages),1):
                    available = text.norm(page.get_text()).replace(' ','')
                    for block in text.blocks_of(str(section)):
                        for window in text.windows(block.split()):
                            if window.replace(' ','') not in available:
                                issues.append(f'{path.stem}: note page {i} loses {window!r}'); break
                    if any(w[0] < 0 or w[2] > page.rect.width or w[3] > page.rect.height for w in page.get_text('words')):
                        issues.append(f'{path.stem}: text outside page {i}')
            report.append({'artifact': pdf.name, 'pages': len(fitz.open(pdf)),
                           'sha256': hashlib.sha256(pdf.read_bytes()).hexdigest(),
                           'md5': hashlib.md5(pdf.read_bytes()).hexdigest()})
        print(f'Lesson {n}: checked projection, retained handout and teacher notes.')
    (folder / 'release_artifacts.json').write_text(json.dumps({'artifacts':report,'issues':issues},indent=2)+'\n')
    return issues


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder',type=Path); args=parser.parse_args()
    issues=check(args.folder)
    print('\n'.join(issues) if issues else 'All 21 artifacts checked; no lost text or unresolved gates.')
    raise SystemExit(bool(issues))
