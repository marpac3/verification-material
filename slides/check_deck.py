#!/usr/bin/env python3
"""Deck QA for the lecture decks.

Two checks, both cheap and objective:

1. OVERFLOW ORACLE -- each slide is rendered on its own into a one-page
   @page box. Any slide that needs more than one page overflows the 16:9
   frame and will be clipped/split in the printed deck.
2. PROSE WORD COUNT -- counts words in prose nodes only (paragraphs and
   list items), excluding tables, <pre> blocks, speaker notes and source
   lines. The house rule is ~40 words of prose per content slide.

Usage:  python check_deck.py <deck.html> [more.html ...]
"""

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
import argparse
import json
from html.parser import HTMLParser
from pathlib import Path

# The env binary by absolute path. The bare `weasyprint` on PATH is a broken
# py3.6 build that writes nothing and leaves a stale PDF in place, and
# `micromamba run` adds a lock this script has no reason to contend for.
WEASY = ["/home/marco.paci/.local/share/mamba/envs/gvsoc_env_3_12/bin/weasyprint"]
SLIDE_RE = re.compile(r'<section\b[^>]*\bclass="slide\b[^"]*"[^>]*>.*?</section>', re.S)
STYLE_RE = re.compile(r"<style>.*?</style>", re.S)
# The font <link> must be carried into the single-slide probe: without it the
# probe renders in a fallback font with different metrics and silently
# under-reports overflow.
LINK_RE = re.compile(r"<link\b[^>]*>", re.I)
PROSE_RE = re.compile(r"<(p|li)\b[^>]*>(.*?)</\1>", re.S)
TAG_RE = re.compile(r"<[^>]+>")
PRE_RE = re.compile(r"<pre\b.*?</pre>", re.S)
TABLE_RE = re.compile(r"<table\b.*?</table>", re.S)
SKIP_CLASS_RE = re.compile(r'class="[^"]*\b(note|src|pagenum|brand|kicker)\b')


def title_of(slide: str) -> str:
    m = re.search(r"<h[12][^>]*>(.*?)</h[12]>", slide, re.S)
    if not m:
        return "(no heading)"
    return re.sub(r"\s+", " ", TAG_RE.sub("", m.group(1))).strip()[:58]


def prose_words(slide: str) -> int:
    """Words in <p>/<li> nodes outside tables and <pre>, excluding chrome."""
    body = TABLE_RE.sub(" ", PRE_RE.sub(" ", slide))
    total = 0
    for m in PROSE_RE.finditer(body):
        opening = body[m.start(): m.start() + 120]
        if SKIP_CLASS_RE.search(opening):
            continue
        text = TAG_RE.sub(" ", m.group(2))
        text = re.sub(r"&[a-zA-Z]+;|&#\d+;", " ", text)
        total += len(text.split())
    return total


def page_count(pdf: Path) -> int:
    out = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
    m = re.search(r"^Pages:\s+(\d+)", out, re.M)
    return int(m.group(1)) if m else -1


def check(path: Path) -> int:
    html = path.read_text()
    style = STYLE_RE.search(html)
    style = style.group(0) if style else ""
    head = "\n".join(LINK_RE.findall(html)) + "\n" + style
    slides = SLIDE_RE.findall(html)
    print(f"\n=== {path.name}: {len(slides)} slides ===")

    problems = 0
    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        for i, slide in enumerate(slides, 1):
            one = tmpdir / f"s{i}.html"
            one.write_text(head + "\n" + slide)
            pdf = tmpdir / f"s{i}.pdf"
            subprocess.run(WEASY + [str(one), str(pdf)],
                           capture_output=True, text=True)
            pages = page_count(pdf)
            words = prose_words(slide)
            flags = []
            # Positive proof of a render. Without this a failed build gives
            # page_count() == -1, `pages > 1` is False, and the slide is
            # reported clean -- absence of evidence read as evidence.
            if pages < 1:
                flags.append("NO RENDER")
            elif pages > 1:
                flags.append(f"OVERFLOW({pages}pp)")
            if words > 40:
                flags.append(f"WORDS({words})")
            if flags:
                problems += 1
                print(f"  slide {i:>2}  {' '.join(flags):<24} {title_of(slide)}")
    if not problems:
        print("  clean: every slide fits one page, every slide <= 40 prose words")
    return problems


def check_rendered(path: Path, pdf: Path, report_path: Path | None = None) -> int:
    """W4 gate: count every rendered word, including tables and source lines.

    Retained study handouts are not subject to the projection word/font budget.
    The existing fidelity gate independently checks every visible HTML block.
    """
    import fitz
    from bs4 import BeautifulSoup
    source = BeautifulSoup(path.read_text(), 'html.parser')
    slides = source.select('section.slide')
    document = fitz.open(pdf)
    projection = path.name.startswith('lesson')
    errors = []
    if not slides or len(slides) != len(document): errors.append('slide/page mismatch')
    if projection and len(slides) > 28: errors.append('more than 28 projection slides')
    if pdf.stat().st_mtime <= path.stat().st_mtime: errors.append('stale PDF')
    # pdftotext is the required independent word-count oracle, not HTML selectors.
    proc = subprocess.run(['pdftotext', '-layout', str(pdf), '-'], capture_output=True, text=True, check=True)
    texts = proc.stdout.split('\f')
    # Poppler's independent bounding boxes also catch long preformatted lines.
    import xml.etree.ElementTree as ET
    bbox = subprocess.run(['pdftotext', '-bbox', str(pdf), '-'], capture_output=True, text=True, check=True)
    xml = ET.fromstring(bbox.stdout)
    bbox_pages = [e for e in xml.iter() if e.tag.endswith('}page')]
    if len(bbox_pages) != len(document): errors.append('bbox/page mismatch')
    for i, bp in enumerate(bbox_pages, 1):
        width = float(bp.attrib['width']); height = float(bp.attrib['height'])
        for word in bp.iter():
            if not word.tag.endswith('}word'): continue
            x0, x1 = float(word.attrib['xMin']), float(word.attrib['xMax'])
            y0, y1 = float(word.attrib['yMin']), float(word.attrib['yMax'])
            margin = 42 if projection and 60 <= y0 < height - 35 else 0
            if x0 < margin - .5 or x1 > width - margin + .5 or y0 < -.5 or y1 > height + .5:
                errors.append(f'page {i}: Poppler bbox outside content width/page')
    # All projection foregrounds must contrast with every content background.
    # These are the small, fixed palette in lesson_style.css, not arbitrary CSS.
    contrast = []
    if projection:
        def lum(rgb):
            c = [int(rgb[j:j+2],16)/255 for j in (0,2,4)]
            c = [v/12.92 if v <= .04045 else ((v+.055)/1.055)**2.4 for v in c]
            return sum(a*b for a,b in zip(c,[.2126,.7152,.0722]))
        style = ' '.join(e.get_text() for e in source.select('style'))
        colors = set(re.findall(r'(?<![-\w])color:\s*#([0-9a-fA-F]{6})',style))
        backgrounds = {'ffffff','edf3f8','fff5ea'}
        if not colors: errors.append('projection foreground palette missing')
        for color in colors:
            for background in backgrounds:
                a,b = sorted([lum(color),lum(background)])
                ratio = (b+.05)/(a+.05);contrast.append(round(ratio,3))
                if ratio < 4.5: errors.append(f'contrast below 4.5: #{color}/#{background}')
    pages = []
    for i, page in enumerate(document):
        words = len(texts[i].split())
        if projection and words > 60: errors.append(f'page {i+1}: {words} rendered words')
        for w in page.get_text('words'):
            if w[0] < -0.5 or w[1] < -0.5 or w[2] > page.rect.width + 0.5 or w[3] > page.rect.height + 0.5:
                errors.append(f'page {i+1}: text outside page')
        if projection:
            for block in page.get_text('dict')['blocks']:
                for line in block.get('lines', []):
                    for span in line['spans']:
                        # Kicker and footer are navigation chrome, not slide body.
                        if 60 <= span['bbox'][1] < page.rect.height - 35 and span['text'].strip() and span['size'] < 17.9:
                            errors.append(f'page {i+1}: body text below 18pt')
        raster = False
        if i < len(slides) and slides[i].select('pre,table'):
            folder = pdf.parent / 'raster' / pdf.stem; folder.mkdir(parents=True, exist_ok=True)
            page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5)).save(folder / f'{i+1:02}.png')
            raster = True
        pages.append({'page': i+1, 'rendered_words': words, 'rasterized': raster})
    report = {'html': str(path), 'pdf': str(pdf), 'projection': projection, 'minimum_contrast': min(contrast) if contrast else None, 'pages': pages, 'errors': sorted(set(errors))}
    if report_path: report_path.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
    return bool(errors)


if __name__ == "__main__":
    if '--pdf' in sys.argv:
        parser = argparse.ArgumentParser(description='W4 rendered-page gate')
        parser.add_argument('html', type=Path)
        parser.add_argument('--pdf', type=Path, required=True)
        parser.add_argument('--json', type=Path)
        args = parser.parse_args()
        raise SystemExit(check_rendered(args.html, args.pdf, args.json))
    rc = 0
    for arg in sys.argv[1:]:
        rc += check(Path(arg))
    sys.exit(1 if rc else 0)
