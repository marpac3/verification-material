#!/usr/bin/env python3
"""Build projection, retained study handout and teacher notes from a lesson manifest.

The manifest owns the projection/notes and names the retained historical handout
source. Book sections are resolved to exact line ranges and hashes at build time.
No network resources are needed. Heavy output belongs in --out-dir on /data2.
"""
from __future__ import annotations
import argparse
import hashlib
import html
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup, Comment
from weasyprint import HTML

ROOT = Path(__file__).resolve().parent.parent


def resolve_source(ref: str) -> dict:
    chapter, section = ref.split(':', 1)
    path = ROOT / 'book' / (chapter + '.md')
    lines = path.read_text().splitlines()
    start = next(i for i, line in enumerate(lines) if re.match(r'^## ' + re.escape(section) + r'(?:\s|$)', line))
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith('## ')), len(lines))
    text = '\n'.join(lines[start:end])
    return {'chapter': chapter, 'start': start + 1, 'end': end, 'sha256': hashlib.sha256(text.encode()).hexdigest()}


def chapter_source(chapter: int) -> dict:
    name = f'ch{chapter:02d}'
    lines = (ROOT / 'book' / (name + '.md')).read_text().splitlines()
    return {'chapter': name, 'start': 1, 'end': len(lines),
            'sha256': hashlib.sha256('\n'.join(lines).encode()).hexdigest()}


def assigned_exercise(identifier: str) -> str:
    chapter = int(identifier.split('.')[0])
    text = (ROOT / 'book' / f'ch{chapter:02d}.md').read_text()
    match = re.search(r'\*\*Exercise ' + re.escape(identifier) + r'\b.*?(?=\n\n|\Z)', text, re.S)
    if not match:
        raise ValueError(f'book exercise {identifier} is missing')
    return match.group(0).replace('**', '').replace('`', '')


def document(title: str, css: str, body: str) -> str:
    return '<!doctype html><html lang="en"><head><meta charset="utf-8"><title>' + html.escape(title) + '</title><style>' + css + '</style></head><body>' + body + '</body></html>'


def slide_body(slide: dict) -> str:
    body = '<h2>' + html.escape(slide['title']) + '</h2><p class="thesis">' + html.escape(slide['thesis']) + '</p><div class="content">'
    if slide.get('flow'):
        cells = []
        for label in slide['flow']:
            if cells: cells.append('<td class="arrow">→</td>')
            cells.append('<td>' + html.escape(label) + '</td>')
        body += '<table class="flow"><tr>' + ''.join(cells) + '</tr></table>'
    body += '<ul>' + ''.join('<li>' + html.escape(x) + '</li>' for x in slide.get('bullets', [])) + '</ul></div>'
    return body


def build(manifest: Path, out: Path, pdf: bool = True) -> dict:
    data = json.loads(manifest.read_text()); number = data['number']; slug = data['slug']
    assert len(data['slides']) <= 28
    assert sum(s['minutes'] for s in data['slides']) == 90
    out.mkdir(parents=True, exist_ok=True)
    css = (ROOT / 'slides/lesson_style.css').read_text()
    projection = []; teacher = []; provenance = []
    elapsed = 0
    for i, slide in enumerate(data['slides'], 1):
        sources = [resolve_source(ref) for ref in slide['sources']]
        provenance.append({'slide': i, 'kind': slide.get('kind', 'content'), 'sources': sources})
        comments = ''.join(f'<!-- src: {s["chapter"]}:{s["start"]}-{s["end"]} -->' for s in sources)
        body = slide_body(slide)
        footer = f'<span class="brand">HARDWARE VERIFICATION LESSON {number}</span><span class="pagenum">{i}</span>'
        script = list(slide['notes'])
        if slide.get('exercise_id'):
            script.insert(0, assigned_exercise(slide['exercise_id']))
        note = '<aside class="notes">' + ''.join('<p>' + html.escape(p) + '</p>' for p in script) + '</aside>'
        projection.append(f'<section class="slide {slide.get("kind", "content")}" id="slide-{i}">' + comments + '<p class="kicker">' + html.escape(data['title']) + '</p>' + body + footer + note + '</section>')
        teacher.append('<section class="teacher-page"><div class="teacher-title">' + html.escape(slide['title']) + f'</div><p class="timing">Slide {i} · {elapsed}–{elapsed + slide["minutes"]} min</p><div class="slide-summary">' + body + '</div><h3>Teaching script</h3>' + ''.join('<p>' + html.escape(p) + '</p>' for p in script) + '<p class="source">Source: ' + ', '.join(f'{s["chapter"]}:{s["start"]}–{s["end"]}' for s in sources) + '</p></section>')
        elapsed += slide['minutes']
    nav = '<nav class="nav">' + ''.join(f'<a href="#slide-{i}">{i}. {html.escape(s["title"])}</a>' for i, s in enumerate(data['slides'], 1)) + '</nav>'
    lesson_html = document(data['title'], css, nav + ''.join(projection))
    notes_css = '''@page {size:A4; margin:17mm} *{box-sizing:border-box} body{font:11pt/1.45 'DejaVu Sans';color:#172b45} .teacher-page{page-break-after:always}.teacher-page:last-child{page-break-after:auto}.teacher-title{font-size:22pt;font-weight:bold}.timing,.source{font-size:9pt;color:#38516a}.slide-summary{background:#edf3f8;padding:12px;margin:14px 0}h2{font-size:16pt;margin:4px 0}.thesis{font-size:12pt}h3{font-size:13pt}.flow{width:100%;font-size:10pt}.flow td{padding:6px}.arrow{width:5%}'''
    notes_html = document(data['title'] + ' — teaching notes', notes_css, ''.join(teacher))
    old = ROOT / data['handout_source']; old_text = old.read_text()
    soup = BeautifulSoup(old_text, 'html.parser')
    # Network font links are optional decoration, never a dependency of a build.
    for link in soup.select('link[href^="http"]'): link.decompose()
    override = soup.new_tag('style'); override.string = '''@page{size:297mm 210mm;margin:0}@media print{.slide{width:297mm;height:210mm;min-height:0;margin:0;padding:11mm 15mm 22mm;overflow:visible}.brand,.pagenum{bottom:15px}}'''
    if soup.head:
        soup.head.append(override)
    else:
        # The historical Artifact decks are HTML fragments without a head.
        soup.append(override)
    legacy_slides = soup.select('section.slide')
    legacy_provenance = []
    current = data.get('chapters', [number])[0]
    for i, legacy in enumerate(legacy_slides, 1):
        # Original prose is retained, including references and worked artifacts.
        # The inventory hash lets the gate reject even a one-word deletion.
        legacy['data-legacy-slide'] = str(i)
        kicker = legacy.select_one('.kicker')
        match = re.search(r'Chapter (\d+)', kicker.get_text() if kicker else '')
        if match:
            current = int(match.group(1))
        # Historical handouts summarize whole chapters; their range is deliberately
        # chapter-wide. Projection sources above are narrowed to exact sections.
        sources = [chapter_source(current)]
        if not match:
            sources = [chapter_source(n) for n in data.get('chapters', [current])]
        sources.extend(resolve_source(ref) for ref in data.get('handout_supplemental_sources', {}).get(str(i), []))
        for src in sources:
            legacy.insert(0, Comment(f' src: {src["chapter"]}:{src["start"]}-{src["end"]} '))
        legacy_provenance.append({'slide': i, 'kind': 'retained_handout', 'sources': sources,
                                  'text_sha256': hashlib.sha256(legacy.get_text().encode()).hexdigest(),
                                  'numeric_annotation': data.get('handout_numeric_annotations', {}).get(str(i))})
    handout_html = str(soup)
    outputs = {}
    for kind, source in [('lesson', lesson_html), ('handout', handout_html), ('notes', notes_html)]:
        stem = f'{kind}{number}_{slug}'; path = out / (stem + '.html'); path.write_text(source)
        if pdf: HTML(filename=str(path), base_url=str(ROOT / 'slides')).write_pdf(out / (stem + '.pdf'))
        outputs[kind] = str(path)
    report = {'manifest': str(manifest), 'number': number, 'minutes': elapsed, 'projection_slides': len(projection), 'retained_handout_slides': len(legacy_slides), 'legacy_source_sha256': hashlib.sha256(old.read_bytes()).hexdigest(), 'provenance': provenance, 'outputs': outputs}
    (out / f'lesson{number}_{slug}.provenance.json').write_text(json.dumps(report, indent=2) + '\n')
    (out / f'handout{number}_{slug}.provenance.json').write_text(json.dumps({'provenance': legacy_provenance}, indent=2) + '\n')
    print(json.dumps({'lesson': number, 'slides': len(projection), 'handout_slides': len(legacy_slides), 'minutes': elapsed}))
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lesson', nargs='+', type=int)
    parser.add_argument('--out-dir', type=Path, required=True)
    parser.add_argument('--no-pdf', action='store_true')
    args = parser.parse_args()
    manifests = sorted((ROOT / 'slides/lessons').glob('lesson*.json'))
    selected = [p for p in manifests if not args.lesson or json.loads(p.read_text())['number'] in args.lesson]
    if not selected: parser.error('no matching lesson manifest')
    for manifest in selected: build(manifest, args.out_dir, not args.no_pdf)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
