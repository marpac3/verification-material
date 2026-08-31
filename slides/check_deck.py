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
from html.parser import HTMLParser
from pathlib import Path

WEASY = ["micromamba", "run", "-n", "gvsoc_env_3_12", "weasyprint"]
SLIDE_RE = re.compile(r'<section class="slide[^"]*">.*?</section>', re.S)
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
            if pages > 1:
                flags.append(f"OVERFLOW({pages}pp)")
            if words > 40:
                flags.append(f"WORDS({words})")
            if flags:
                problems += 1
                print(f"  slide {i:>2}  {' '.join(flags):<24} {title_of(slide)}")
    if not problems:
        print("  clean: every slide fits one page, every slide <= 40 prose words")
    return problems


if __name__ == "__main__":
    rc = 0
    for arg in sys.argv[1:]:
        rc += check(Path(arg))
    sys.exit(1 if rc else 0)
