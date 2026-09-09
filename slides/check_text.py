#!/usr/bin/env python3
"""Text-fidelity gate for the lecture decks: nothing that is in the HTML may
be missing from the PDF.

WeasyPrint can drop, clip or push content off the page without changing the
page count, so `slides == pages` is not enough. This gate compares, slide by
slide, the visible text of the HTML against the text of the matching PDF page.

Four checks. The first three are fatal, the fourth is a measured warning.

1. FRESHNESS -- the PDF must be newer than the HTML. Every deck shipped in
   August 2026 was missing 44 of its 55 `<p class="src">` lines for exactly
   this reason: the provenance pass edited the HTML on 28 August and the PDFs
   were left at their 27 August build. A stale PDF makes every other check
   meaningless, so it is tested first.
2. PAGINATION -- one `<section class="slide">` must produce exactly one page.
3. TEXT -- every window of WINDOW consecutive words of every block element of
   slide i must appear in the text of PDF page i, and every distinct word of
   that element must appear on that page.
4. FOOTER -- `.brand` and `.pagenum` must be on the page, in the footer band,
   on the correct side. Content that reaches into the footer band is reported
   with the overshoot in points; that is a layout residual, not text loss, so
   it does not fail the run.

Normalisation: entities decoded, NBSP folded, lowercased, anything that is
not a letter or a digit turned into a space, runs of space collapsed.

Reading a PDF back is the hard part, and no single rendering of a page is
reliable: `pdftotext -layout` interleaves the columns of a two-column slide,
plain reading order splits a paragraph that overlaps the footer, and a
four-word window is routinely broken in two or three by wrapping inside a
narrow table cell. So a window is accepted if ANY of these finds it:

  * `pdftotext` reading order, or `pdftotext -layout`;
  * a reading order rebuilt from `-bbox` -- whole page, footer removed, and
    split into columns two ways (detected gutters, and down the middle);
  * a chain of horizontal text runs, each below the previous and sharing its
    left edge or its columns -- which is what a wrap looks like, and needs no
    page-wide reading order at all.

Each of those is tried with spaces kept and with spaces removed, because
`.note b` and the kickers are letter-spaced small caps that pdftotext hands
back one letter at a time ("SAY" -> "s a y"), and because `<sup>`/`<sub>`
join differently in the render than in the source.

Calibrated against two known points: the 28 August PDFs, where the gate must
report the source lines the audit found missing, and the 2 September rebuild,
where it must report nothing. See slides/DECK_NOTES.md.

Usage:  python check_text.py <deck.html> <deck.pdf> [more pairs ...]
        python check_text.py --window 5 <deck.html> <deck.pdf>
Exit status: 0 clean, 1 any fatal check failed.
"""

from __future__ import annotations

import html as htmlmod
import re
import subprocess
import sys
from pathlib import Path

WINDOW = 4            # words per compared segment
MAX_REPORT = 10       # missing segments printed per slide
# The footer is anchored to the page: `.brand` and `.pagenum` sit at
# `bottom: 15px` of a `.slide` of definite height, which puts the top of their
# ink box 21.0 pt above the bottom of the 420 pt page box that `pdftotext
# -bbox` reports. The band is deliberately narrow: a source line one line too
# low lands ~2 pt above the footer, and it must be read as content, not as
# chrome, or the two get interleaved and every check on that line fails.
FOOTER_OFFSET = 21.0  # pt from the page bottom to the top of the footer line
FOOTER_TOL = 0.6      # pt

SLIDE_RE = re.compile(r'<section\b[^>]*\bclass="slide\b[^"]*"[^>]*>.*?</section>', re.S)
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
# Tags across which text may not be compared: the renderer is free to put the
# two sides on different lines, in different cells or in different columns.
# `span` is here because the deck stylesheet makes several spans block-level
# (`.ex .tag`, `.cbox .q`, `tr.stem i`) and because an inline-block `.pill`
# breaks a line just as effectively.
BLOCK_TAGS = ("p", "li", "ul", "ol", "h1", "h2", "h3", "h4", "div", "pre",
              "table", "thead", "tbody", "tr", "td", "th", "section", "span",
              "blockquote", "figure", "figcaption", "br", "hr")
BLOCK_RE = re.compile(r"</?(?:%s)\b[^>]*>" % "|".join(BLOCK_TAGS), re.I)
TAG_RE = re.compile(r"<[^>]+>")
CHROME_RE = re.compile(r'<span class="(brand|pagenum)">(.*?)</span>', re.S)
CLASS_RE = re.compile(r'class="([^"]*)"')
WORD_RE = re.compile(
    r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>')
PAGE_RE = re.compile(
    r'<page width="([\d.]+)" height="([\d.]+)">(.*?)</page>', re.S)


def norm(text: str) -> str:
    text = htmlmod.unescape(text)
    text = text.replace(" ", " ").replace(" ", " ").replace(" ", " ")
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return " ".join(text.split())


def run(cmd: list[str]) -> str:
    return subprocess.run(cmd, capture_output=True, text=True).stdout


def pdf_pages_text(pdf: Path, layout: bool) -> list[str]:
    cmd = ["pdftotext"] + (["-layout"] if layout else []) + [str(pdf), "-"]
    return run(cmd).split("\f")


def pdf_pages_words(pdf: Path):
    """[(page_width, page_height, [(x0, y0, x1, y1, word), ...]), ...]"""
    xml = run(["pdftotext", "-bbox", str(pdf), "-"])
    out = []
    for w, h, body in PAGE_RE.findall(xml):
        words = [(float(a), float(b), float(c), float(d), htmlmod.unescape(e))
                 for a, b, c, d, e in WORD_RE.findall(body)]
        out.append((float(w), float(h), words))
    return out


SEP = " qqzsepzqq "     # column separator: survives norm(), matches no text


def footer_band(height: float, words) -> tuple[list, float]:
    """(words sitting on the footer's baseline, that baseline's top)."""
    band_top = height - FOOTER_OFFSET
    return [w for w in words if abs(w[1] - band_top) <= FOOTER_TOL], band_top


def chrome_of(slide: str, band):
    """Pick the footer's own words out of the footer band.

    Geometry alone cannot do it. `.src` is 10.5 px, the same size as the
    footer, so a source line one line too low lands on the footer's baseline
    with the same ink height and starts 26 pt to its right, straight through
    `A HOLISTIC GUIDE`. So the footer is identified by its text: the brand's
    words are matched in order from the left edge of the band and the page
    number from the right, and anything not matched stays content. Reading a
    colliding line as chrome interleaves it with the brand and fails every
    check on that line; reading the brand as content reports the footer
    missing when it is there.

    Returns (chrome words, [(kind, wanted, what the band holds)]).
    """
    ordered = sorted(band, key=lambda w: w[0])
    chrome, bad = [], []
    for kind, raw in CHROME_RE.findall(slide):
        want = norm(raw).split()
        if not want:
            continue
        seq = ordered if kind == "brand" else list(reversed(ordered))
        need = want if kind == "brand" else list(reversed(want))
        got, walk, ok = [], iter(seq), True
        for token in need:
            for w in walk:
                if norm(w[4]) == token:
                    got.append(w)
                    break
            else:
                ok = False
                break
        if ok:
            chrome.extend(got)
        else:
            bad.append((kind, " ".join(want),
                        " ".join(norm(w[4]) for w in ordered) or "(band empty)"))
    return chrome, bad


def lines_of(words) -> list[list]:
    """Group words into text lines by vertical overlap, then order each line
    left to right.

    Overlap, not a fixed y band: a line often mixes font sizes -- `.note`
    opens with a 9.5 px letter-spaced `<b>` label in front of 12 px text, and
    the small glyphs have a lower yMin on the same baseline. Bucketing on yMin
    put that label in the next band and sent it to the end of the page.
    """
    out: list[list] = []
    cur: list = []
    lo = hi = 0.0
    for w in sorted(words, key=lambda w: (w[1], w[0])):
        h = max(w[3] - w[1], 0.1)
        if cur and min(hi, w[3]) - max(lo, w[1]) >= 0.5 * min(h, hi - lo):
            cur.append(w)
            lo, hi = min(lo, w[1]), max(hi, w[3])
        else:
            if cur:
                out.append(sorted(cur, key=lambda w: w[0]))
            cur, lo, hi = [w], w[1], w[3]
    if cur:
        out.append(sorted(cur, key=lambda w: w[0]))
    return out


def flow(words) -> str:
    """Words in reading order: line by line, then left to right."""
    return norm(" ".join(w[4] for line in lines_of(words) for w in line))


def gutters(width: float, content) -> list[float]:
    """x positions of the vertical whitespace strips that separate columns.

    A strip counts when it is at least MIN_GUTTER pt wide and free of words on
    at least half of the page's text lines. Half, not all, because a
    full-width kicker and heading sit above the columns on almost every slide
    and would otherwise hide every gutter on the page.
    """
    min_gutter, step, margin = 12.0, 2.0, 40.0
    lines = lines_of(content)
    if len(lines) < 4:
        return []
    free_x, xs = [], []
    x = margin
    while x <= width - margin:
        xs.append(x)
        busy = sum(1 for ws in lines
                   if any(w[0] - 3 <= x <= w[2] + 3 for w in ws))
        free_x.append(busy <= len(lines) * 0.5)
        x += step
    out, run = [], []
    for x, free in zip(xs, free_x):
        if free:
            run.append(x)
        else:
            if run and run[-1] - run[0] >= min_gutter:
                out.append((run[0] + run[-1]) / 2.0)
            run = []
    if run and run[-1] - run[0] >= min_gutter:
        out.append((run[0] + run[-1]) / 2.0)
    return out


def by_columns(width: float, content, bounds: list[float]) -> str:
    """Reading order column by column, columns joined by an unmatchable token."""
    if not bounds:
        return ""
    edges = [0.0] + sorted(bounds) + [width]
    parts = []
    for lo, hi in zip(edges, edges[1:]):
        col = [w for w in content if lo <= (w[0] + w[2]) / 2.0 < hi]
        if col:
            parts.append(flow(col))
    return SEP.join(parts)


def runs_of(words):
    """Split each text line into runs: neighbouring words with a small gap.
    A table gutter or a column gutter always exceeds the gap."""
    out = []
    for row in lines_of(words):
        cur = [row[0]]
        for prev, nxt in zip(row, row[1:]):
            if nxt[0] - prev[2] < 15.0:
                cur.append(nxt)
            else:
                out.append(cur)
                cur = [nxt]
        out.append(cur)
    return out


def by_start_x(words) -> str:
    """Reading order built by grouping runs on their left edge.

    Every line of a wrapped table cell, and every cell of the same table
    column, starts at the same x. Grouping on that x and then ordering by y
    reconstructs each column's text without having to find the gutters, which
    is what a five-column plan table needs.
    """
    groups: dict[int, list] = {}
    for r in runs_of(words):
        groups.setdefault(round(r[0][0] / 4.0), []).append(r)
    parts = []
    for key in sorted(groups):
        rows = sorted(groups[key], key=lambda r: r[0][1])
        parts.append(norm(" ".join(w[4] for r in rows for w in r)))
    return SEP.join(p for p in parts if p)


GAPS = (4.0, 6.0, 12.0, 25.0)
MAX_WRAP = 30.0   # pt: the furthest a wrapped continuation can sit below its line


def runs_pool(words):
    """Every horizontal text segment on the page, at three gutter widths.

    A run is what a reader sees as one uninterrupted piece of text on one
    line. Three thresholds because the deck mixes `table.compact` (6 pt
    between cells) with `table.cols` (12 pt) and free two-column layouts: at
    one threshold two neighbouring cells merge into a single run, at another a
    single cell splits, and a segment only has to survive one of them.
    Returns [(y, x0, x1, spaced text, packed text)].
    """
    out = []
    for gap in GAPS:
        for row in lines_of(words):
            cur = [row[0]]
            for prev, nxt in zip(row, row[1:]):
                if nxt[0] - prev[2] < gap:
                    cur.append(nxt)
                else:
                    out.append(cur)
                    cur = [nxt]
            out.append(cur)
    pool = []
    for r in out:
        text = norm(" ".join(w[4] for w in r))
        if text:
            pool.append((r[0][1], r[0][0], r[-1][2], text, text.replace(" ", "")))
    return pool


def _aligned(a, b) -> bool:
    """Is run b a plausible continuation of run a?

    b has to be lower on the page, no more than MAX_WRAP pt below (a wrap goes
    to the next line, not across the slide), and has to share horizontal space
    with a -- either starting at the same left edge, or overlapping its
    columns. Both tests are needed: at one gutter threshold a wrapped table
    cell's first line splits at an inner gap and loses its left edge, at
    another it merges with the neighbouring cell and loses its right end.
    """
    dy = b[0] - a[0]
    if dy <= 0 or dy > MAX_WRAP:
        return False
    if abs(b[1] - a[1]) < 8.0:
        return True
    return min(a[2], b[2]) - max(a[1], b[1]) > 1.0


def _chain(ws: list[str], pool, prev) -> bool:
    if not ws:
        return True
    last_piece = True
    for k in range(len(ws), 0, -1):
        piece = " ".join(ws[:k])
        pk = piece.replace(" ", "")
        last_piece = k == len(ws)
        for r in pool:
            if prev is None:
                ok = ((piece in r[3] or pk in r[4]) if last_piece
                      else (r[3].endswith(piece) or r[4].endswith(pk)))
            elif not _aligned(prev, r):
                continue
            elif last_piece:
                ok = r[3].startswith(piece) or r[4].startswith(pk)
            else:
                ok = r[3] == piece or r[4] == pk
            if ok and _chain(ws[k:], pool, r):
                return True
    return False


def wrapped(seg: str, pool) -> bool:
    """Is this segment on the page, allowing for line wrapping?

    A four-word window is regularly broken by the renderer wrapping a cell or
    a paragraph, sometimes twice inside four words in a narrow table column.
    It counts as present when it sits inside one run, or when it splits into
    the tail of one run followed by whole runs and finally the head of a run,
    each below the last and starting at the same left edge -- which is exactly
    what a wrap looks like. This check needs no page-wide reading order, and
    is therefore the one that does not misfire on a five-column table.
    """
    return _chain(seg.split(), pool, None)


def variants_of(spaced: list[str]) -> tuple[str, ...]:
    out = []
    for s in spaced:
        out.append(s)
        out.append(s.replace(" ", ""))
    return tuple(out)


def present(seg: str, variants: tuple[str, ...]) -> bool:
    packed = seg.replace(" ", "")
    for i, v in enumerate(variants):
        if (packed if i % 2 else seg) in v:
            return True
    return False


PRE_RE = re.compile(r"<pre\b[^>]*>(.*?)</pre>", re.S)


def blocks_of(slide: str) -> list[str]:
    # W4 projection carries an oral script which CSS deliberately hides.
    # Only the explicit speaker-note container is excluded; visible notes and
    # all other blocks retain the original deletion-sensitive comparison.
    slide = re.sub(r'<aside\b[^>]*class="notes"[^>]*>.*?</aside>', '', slide, flags=re.S)
    body = CHROME_RE.sub(" ", COMMENT_RE.sub(" ", slide))
    # `pre` is white-space: pre-wrap, so a newline in the source is a line
    # break on the slide; each line is its own block.
    body = PRE_RE.sub(lambda m: "<pre>" + m.group(1).replace("\n", "<br>") + "</pre>",
                      body)
    return [t for t in (norm(TAG_RE.sub(" ", p)) for p in BLOCK_RE.split(body)) if t]


def label_map(slide: str) -> dict[str, str]:
    """Map the first WINDOW words of an element to a printable name for it."""
    body = COMMENT_RE.sub(" ", slide)
    out: dict[str, str] = {}
    for m in re.finditer(r"<(p|div|li|h1|h2|h3|td|th|pre|span)\b([^>]*)>(.*?)</\1>",
                         body, re.S):
        cls = CLASS_RE.search(m.group(2))
        text = norm(TAG_RE.sub(" ", m.group(3)))
        if text:
            key = " ".join(text.split()[:WINDOW])
            name = "<%s%s>" % (m.group(1), "." + cls.group(1).split()[0] if cls else "")
            out.setdefault(key, name)
    return out


def windows(words: list[str]) -> list[str]:
    if len(words) <= WINDOW:
        return [" ".join(words)] if words else []
    return [" ".join(words[i:i + WINDOW]) for i in range(len(words) - WINDOW + 1)]


def merge(segs: list[str]) -> list[str]:
    out: list[list[str]] = []
    for s in segs:
        w = s.split()
        if out and out[-1][-(WINDOW - 1):] == w[:WINDOW - 1]:
            out[-1].append(w[-1])
        else:
            out.append(list(w))
    return [" ".join(r) for r in out]


def check(html_path: Path, pdf_path: Path) -> int:
    print("\n=== %s vs %s ===" % (html_path.name, pdf_path.name))
    fatal = 0

    if not pdf_path.exists():
        print("  FATAL   no PDF at %s" % pdf_path)
        return 1
    h_m, p_m = html_path.stat().st_mtime, pdf_path.stat().st_mtime
    if p_m <= h_m:
        print("  STALE   the PDF is not newer than the HTML -- rebuild first")
        fatal += 1
    else:
        print("  fresh   PDF built %.0f s after the HTML was last written" % (p_m - h_m))

    slides = SLIDE_RE.findall(html_path.read_text())
    info = run(["pdfinfo", str(pdf_path)])
    m = re.search(r"^Pages:\s+(\d+)", info, re.M)
    pages = int(m.group(1)) if m else -1
    if pages != len(slides):
        print("  PAGINATION  %d slides but %d pages" % (len(slides), pages))
        fatal += 1
    else:
        print("  paginated   %d slides = %d pages" % (len(slides), pages))

    plain = pdf_pages_text(pdf_path, layout=False)
    laid = pdf_pages_text(pdf_path, layout=True)
    boxed = pdf_pages_words(pdf_path)

    lost, chrome_bad, collisions = [], [], []
    for i, slide in enumerate(slides, 1):
        if i > pages or i > len(boxed):
            break
        width, height, words = boxed[i - 1]
        band, band_top = footer_band(height, words)
        footer, bad_chrome = chrome_of(slide, band)
        ids = {id(w) for w in footer}
        content = [w for w in words if id(w) not in ids]
        everything = flow(words)
        variants = variants_of([
            norm(plain[i - 1]) if i - 1 < len(plain) else "",
            norm(laid[i - 1]) if i - 1 < len(laid) else "",
            everything,
            flow(content),
            by_columns(width, content, gutters(width, content)),
            by_columns(width, content, [width / 2.0]),
            by_start_x(content),
        ])
        page_words = set(everything.split())
        # `.note b` and the kicker are letter-spaced small caps, and pdftotext
        # splits a letter-spaced word into single letters ("SAY" -> "s a y"),
        # so a word also counts as present when it is in the space-stripped
        # rendering of the page.
        packed_page = everything.replace(" ", "")
        pool = runs_pool(content) + runs_pool(words)
        labels = label_map(slide)
        missing = []
        for text in blocks_of(slide):
            ws = text.split()
            absent = sorted(w for w in set(ws)
                            if w not in page_words and w not in packed_page)
            miss = [w for w in windows(ws)
                    if not present(w, variants) and not wrapped(w, pool)]
            if absent or miss:
                tag = labels.get(" ".join(ws[:WINDOW]), "<block>")
                if absent:
                    missing.append((tag, "WORDS NOT ON PAGE: " + " ".join(absent[:12])))
                for runseg in merge(miss):
                    missing.append((tag, runseg))
        chrome_bad += [(i,) + b for b in bad_chrome]
        if content:
            bottom = max(w[3] for w in content)
            if bottom > band_top:
                collisions.append((i, round(bottom - band_top, 1)))
        if missing:
            lost.append(i)
            print("  slide %-3d page %-3d %d lost segment(s)" % (i, i, len(missing)))
            for tag, runseg in missing[:MAX_REPORT]:
                print("      %-18s %s" % (tag, runseg))
            if len(missing) > MAX_REPORT:
                print("      ... and %d more" % (len(missing) - MAX_REPORT))

    if lost:
        fatal += len(lost)
        print("  TEXT LOSS on %d slide(s): %s" % (len(lost), lost))
    else:
        print("  text        every block of every slide is on its page")
    if chrome_bad:
        fatal += len(chrome_bad)
        print("  FOOTER missing or misplaced on %d page(s):" % len(chrome_bad))
        for i, kind, want, got in chrome_bad[:MAX_REPORT]:
            print("      page %-3d %-8s want %r, footer band has %r" % (i, kind, want, got))
        if len(chrome_bad) > MAX_REPORT:
            print("      ... and %d more" % (len(chrome_bad) - MAX_REPORT))
    else:
        print("  footer      .brand and .pagenum on %d/%d pages" % (pages, pages))
    if collisions:
        print("  warning     content reaches into the footer band on %d page(s) "
              "(page, pt past the band top):" % len(collisions))
        print("              %s" % collisions)
    else:
        print("  clearance   no page has content inside the footer band")
    return fatal


def main(argv: list[str]) -> int:
    global WINDOW
    args = list(argv)
    if args[:1] == ["--window"]:
        WINDOW = int(args[1])
        args = args[2:]
    if len(args) < 2 or len(args) % 2:
        print(__doc__)
        return 2
    rc = 0
    for j in range(0, len(args), 2):
        rc += check(Path(args[j]), Path(args[j + 1]))
    print("\n%s" % ("FAIL" if rc else "PASS"))
    return 1 if rc else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
