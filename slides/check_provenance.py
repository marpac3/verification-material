#!/usr/bin/env python3
"""Check precise book-source ranges and numerical claims in W4 projection.

This checks presence, not semantic entailment; the authored notes and review
remain responsible for the claim's subject. Timing and curriculum locators are
declared separately from technical claims. Changing a chapter invalidates its
recorded range hash until the deck is deliberately rebuilt.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from decimal import Decimal
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
NUM = re.compile(r'(?<![\w.])\d+(?:[.,]\d+)*(?:%|\b)')


def numbers(text: str) -> set[str]:
    """Compare numeric values across 1,024/1024, 05/5 and 14%/14 percent.

    Units and subjects still require the semantic review described above.
    Do not treat arXiv identifiers with multiple dots as decimal quantities.
    """
    result = set()
    for raw in NUM.findall(text):
        value = raw.rstrip('%').replace(',', '')
        try: value = str(Decimal(value).normalize())
        except Exception: pass
        result.add(value)
    return result


def check(html_path: Path, manifest_path: Path) -> list[str]:
    report = json.loads(manifest_path.read_text())
    slides = BeautifulSoup(html_path.read_text(), 'html.parser').select('section.slide')
    issues = []
    if len(slides) != len(report['provenance']):
        return ['slide/source-record count mismatch']
    for i, (slide, record) in enumerate(zip(slides, report['provenance']), 1):
        texts = []
        original_hash = hashlib.sha256(slide.get_text().encode()).hexdigest()
        if not record['sources']: issues.append(f'slide {i}: no source')
        for src in record['sources']:
            lines = (ROOT / 'book' / (src['chapter'] + '.md')).read_text().splitlines()
            if not 1 <= src['start'] <= src['end'] <= len(lines):
                issues.append(f'slide {i}: invalid source range'); continue
            text = '\n'.join(lines[src['start'] - 1:src['end']])
            if hashlib.sha256(text.encode()).hexdigest() != src['sha256']:
                issues.append(f'slide {i}: stale source hash')
            comment = f'src: {src["chapter"]}:{src["start"]}-{src["end"]}'
            if comment not in str(slide): issues.append(f'slide {i}: missing source comment')
            texts.append(text)
        for hidden in slide.select('aside.notes,.brand,.pagenum,.kicker'): hidden.decompose()
        # Curriculum slides contain course routing, not quantitative hardware claims.
        if record['kind'] == 'curriculum': continue
        source_numbers = numbers(' '.join(texts))
        missing = numbers(slide.get_text(' ', strip=True)) - source_numbers
        annotation = record.get('numeric_annotation')
        if annotation:
            if record['kind'] != 'retained_handout' or record.get('text_sha256') != original_hash or not annotation.get('reason'):
                issues.append(f'slide {i}: invalid historical numeric annotation')
            else:
                missing -= numbers(' '.join(annotation['numbers']))
        if missing: issues.append(f'slide {i}: numbers absent from source: {sorted(missing)}')
    return issues


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('html', type=Path); parser.add_argument('provenance', type=Path)
    args = parser.parse_args(); issues = check(args.html, args.provenance)
    print('\n'.join(issues) if issues else 'Source ranges, hashes, comments and numerical claims verified.')
    raise SystemExit(bool(issues))
