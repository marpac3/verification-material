#!/usr/bin/env python3
"""Build the book: markdown chapters -> one professional HTML + PDF.

    python3 tools/build_book.py                 # the whole book, as shipped

With no arguments it builds every file listed in meta/book_manifest.txt into
build/hardware_verification_guide.{html,pdf}.  That default is the point: the
appendices used to be left out of the published PDF because they were left out
of a command line, and nothing could tell that build from a deliberate one.

For a partial build while iterating on a chapter, both defaults can be
overridden:

    python3 tools/build_book.py --chapters ch13 ch14 --out-base build/prova

Structural diagrams (```mermaid) and timing diagrams (```wavedrom) are rendered
to SVG by their own pipelines, `tools/mermaid.py` and `tools/wavedrom.py`.

    python3 tools/build_book.py --with-index    # the shipped book, indexed

`--with-index` builds twice: the first pass is scanned page by page for the
terms of `meta/index_terms.md` (`tools/make_index.py`), the second carries the
Index section that scan produced, appended after the last appendix so that no
page the index cites can move. It costs one extra full build.

Produces <out-base>.html (inline SVG diagrams, browser-readable) and
<out-base>.pdf (WeasyPrint; diagrams as data-URI SVG because WeasyPrint 52.5
cannot lay out inline <svg>).  Idempotent within a day: the title page and the
PDF's CreationDate carry the build date (see book_meta.DATE).
"""

from __future__ import annotations

import argparse
import html as html_mod
import re
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import book_meta  # noqa: E402
import chapter as chapter_mod  # noqa: E402
import make_index  # noqa: E402
import mermaid  # noqa: E402
import wavedrom  # noqa: E402
from references import Bibliography, load_bibliography  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
TOOLS = Path(__file__).resolve().parent

# The anchor of the generated Index section, set the way the glossary's is
# (`book_meta.GLOSSARY_ID`) rather than taken from the markdown converter, whose
# slugs are prefixed with the converter's own name.
INDEX_ID = "book-index"

DEFAULT_MANIFEST = ROOT / "meta" / "book_manifest.txt"
DEFAULT_OUT_BASE = ROOT / "build" / "hardware_verification_guide"

# Tokens that belong to the source and never to a reader: an unconverted
# citation marker means the bibliography machinery never saw it, and an
# [UNVERIFIED] tag means a claim shipped with nothing behind it.  Both used to
# be warnings, and a warning printed among sixty lines of build information is
# a thing you scroll past -- these now fail the build.
AUTHOR_TOKENS = (
    ("[cit:...]", re.compile(r"\[cit:[^\]]*\]")),
    ("[UNVERIFIED]", re.compile(r"\[UNVERIFIED[^\]]*\]")),
)


def load_manifest(path: Path) -> list[str]:
    """The file stems of the book, in order, from meta/book_manifest.txt.

    Blank lines and everything after a '#' are ignored, so the manifest can say
    why it is what it is.  A missing, empty or repeated entry raises instead of
    degrading quietly: this list is the default for the command that publishes,
    so its failure mode has to be loud.
    """
    if not path.is_file():
        raise FileNotFoundError(f"manifest not found: {path}")
    stems = [
        line.split("#", 1)[0].strip()
        for line in path.read_text(encoding="utf-8").splitlines()
    ]
    stems = [stem for stem in stems if stem]
    if not stems:
        raise ValueError(f"manifest {path} lists no chapters")
    duplicates = sorted({stem for stem in stems if stems.count(stem) > 1})
    if duplicates:
        raise ValueError(f"manifest {path} repeats: {', '.join(duplicates)}")
    return stems


def scan_author_tokens(
    sources: list[tuple[str, str]], document: str
) -> list[str]:
    """One report line per source that still carries an author token.

    `sources` is (label, html) for every piece the document is assembled from,
    so the message names the file to open rather than a count to worry about.
    The whole document is scanned as well: whatever the labelled pieces do not
    account for came from the builder's own furniture, and saying so is better
    than hiding it behind a total that happens to match.
    """
    lines: list[str] = []
    attributed = {name: 0 for name, _ in AUTHOR_TOKENS}
    for label, html in sources:
        for name, pattern in AUTHOR_TOKENS:
            found = pattern.findall(html)
            if not found:
                continue
            attributed[name] += len(found)
            distinct = sorted(set(found))
            shown = ", ".join(distinct[:5])
            more = "" if len(distinct) <= 5 else ", ..."
            lines.append(f"{label}: {len(found)} {name} token(s) - {shown}{more}")
    for name, pattern in AUTHOR_TOKENS:
        stray = len(pattern.findall(document)) - attributed[name]
        if stray > 0:
            lines.append(
                f"(document, outside any chapter or front-matter page): "
                f"{stray} {name} token(s)"
            )
    return lines


@dataclass
class BuildReport:
    warnings: list[str] = field(default_factory=list)
    fallback_ids: set[str] = field(default_factory=set)
    missing_ids: set[str] = field(default_factory=set)

    def warn(self, message: str) -> None:
        self.warnings.append(message)
        print(f"[warn] {message}", file=sys.stderr)


# --------------------------------------------------------------------------
# document fragments
# --------------------------------------------------------------------------


def render_title_page(subtitle: str) -> str:
    esc = html_mod.escape
    return f"""<section class="title-page">
  <div class="band"></div>
  <div class="tp-body">
    <h1 class="tp-title">{esc(book_meta.BOOK_TITLE_MAIN)}</h1>
    <p class="tp-title-sub">{esc(book_meta.BOOK_TITLE_SUB)}</p>
    <div class="tp-rule"></div>
    <p class="tp-subtitle">{esc(subtitle)}</p>
    <div class="tp-meta">
      <p class="tp-author">{esc(book_meta.AUTHOR)}</p>
      <p class="tp-date">{esc(book_meta.DATE)}</p>
      <div class="tp-note">{esc(book_meta.CORPUS_NOTE)}</div>
    </div>
  </div>
</section>"""


def render_part_divider(part: dict) -> str:
    esc = html_mod.escape
    label, _, name = part["title"].partition(" — ")
    return f"""<section class="part-divider" id="{part['id']}">
  <p class="part-kicker">{esc(label)}</p>
  <h2>{esc(name or part['title'])}</h2>
  <div class="part-rule"></div>
  <p class="part-desc">{esc(part['description'])}</p>
</section>"""


def render_toc(items: list[tuple[str, str, str]]) -> str:
    """items: (css class, anchor, label) in document order."""
    rows = []
    for css_class, anchor, label in items:
        rows.append(
            f'    <li class="{css_class}">'
            f'<a href="#{anchor}">{html_mod.escape(label)}</a></li>'
        )
    body = "\n".join(rows)
    return (
        f'<nav class="toc" id="contents">\n'
        f"  <h2>{html_mod.escape(book_meta.TOC_TITLE)}</h2>\n"
        f"  <ul>\n{body}\n  </ul>\n</nav>"
    )


_LIST_TITLE_BREAK = re.compile(r"^(.{20,130}?)(?:\s+—\s|:\s|\.\s|,\s)")


def list_title(caption: str) -> str:
    """The caption's opening clause, for the list of figures or tables.

    A caption and a list entry do different jobs. A caption must let a reader
    understand the float without the surrounding paragraph, which is why the
    ones in this book run to eighty or a hundred words. A list entry must let a
    reader *find* the float, which wants a line. Printing the whole caption in
    the list did not merely read badly: the page number is set with `float:
    right`, so it lands at the end of the entry's block, and an entry six lines
    tall put the page number six lines below the title it belonged to — in the
    extracted text of the last build it fell inside a hyphenated word.

    The captions carry the break already. Each opens by naming what the reader
    is looking at and then turns, at an em dash or a colon, to what matters
    about it. That first clause is the title. Where a caption has no such turn
    within a line's worth of text, the first comma serves; where it has neither,
    the text is cut at a word boundary and marked with an ellipsis, which is
    honest about being a truncation rather than pretending to be a title.
    """
    m = _LIST_TITLE_BREAK.search(caption)
    if m:
        return m.group(1)
    if len(caption) <= 130:
        return caption.rstrip(".")
    return caption[:130].rsplit(" ", 1)[0] + "…"


def render_float_lists(chapters: list) -> list[tuple[str, str, str]]:
    """A list of figures and a list of tables, in document order.

    Returns (html, anchor, title) triples so the caller can add them to the
    table of contents. An empty list is omitted rather than printed empty: a
    heading over nothing reads as a production defect, not as an absence.
    """
    out: list[tuple[str, str, str]] = []
    for kind, title, anchor in (
        ("figure", book_meta.LIST_OF_FIGURES_TITLE, "list-of-figures"),
        ("table", book_meta.LIST_OF_TABLES_TITLE, "list-of-tables"),
    ):
        items: list[str] = []
        for processed in chapters:
            for item in processed.floats:
                if item.kind != kind:
                    continue
                word = "Figure" if kind == "figure" else "Table"
                title_text = list_title(re.sub(r"[*`_]", "", item.caption))
                items.append(
                    f'    <li><a href="#{item.anchor}">'
                    f'<span class="fl-num">{word} {item.number}</span> '
                    f"{html_mod.escape(title_text)}</a></li>"
                )
        if not items:
            continue
        body = "\n".join(items)
        out.append(
            (
                f'<section class="frontmatter" id="{anchor}">\n'
                f"  <h1>{html_mod.escape(title)}</h1>\n"
                f'  <ul class="float-list">\n{body}\n  </ul>\n</section>',
                anchor,
                title,
            )
        )
    return out


def render_front_matter(
    front_dir: Path, name: str, css_class: str, report: BuildReport
) -> tuple[str, str, str] | None:
    """Render front/<name>.md into a front-matter section.

    The file's own level-1 heading supplies the title and the anchor, so the
    prose and the table of contents cannot disagree about what the page is
    called.
    """
    path = front_dir / f"{name}.md"
    if not path.is_file():
        report.warn(f"front matter {path.name} not found; page omitted")
        return None

    source = path.read_text(encoding="utf-8")
    converter = chapter_mod._make_converter(f"fm-{name}")
    body = converter.convert(source)
    heads = [t for t in getattr(converter, "toc_tokens", []) if t["level"] == 1]
    if not heads:
        report.warn(f"front matter {path.name}: no level-1 heading; page omitted")
        return None
    title = html_mod.unescape(re.sub(r"<[^>]+>", "", heads[0]["name"])).strip()
    anchor = heads[0]["id"]
    html = f'<section class="{css_class}" id="fm-{name}">\n{body}\n</section>'
    return html, anchor, title


def render_glossary(path: Path, report: BuildReport) -> tuple[str, str] | None:
    """Convert meta/glossary.md into Appendix A."""
    if not path.is_file():
        report.warn(f"glossary not found at {path}; Appendix A omitted")
        return None

    lines = path.read_text(encoding="utf-8").splitlines()
    start = next((i for i, ln in enumerate(lines) if ln.lstrip().startswith("|")), None)
    if start is None:
        report.warn(f"no table found in {path}; Appendix A omitted")
        return None

    table = "\n".join(lines[start:]).strip()
    source = (
        f"# {book_meta.GLOSSARY_TITLE}\n\n"
        f"{book_meta.GLOSSARY_NOTE}\n{{: .glossary-note }}\n\n"
        f"{table}\n"
    )
    converter = chapter_mod._make_converter("gloss")
    body = converter.convert(source)
    title = book_meta.GLOSSARY_TITLE
    body = re.sub(
        r"<h1[^>]*>",
        f'<h1 class="chapter-title" id="{book_meta.GLOSSARY_ID}">',
        body,
        count=1,
    )
    body = body.replace(
        "</h1>",
        f'</h1>\n<p class="runhead-marker">{html_mod.escape(title)}</p>',
        1,
    )
    html = f'<section class="chapter appendix" id="appendix-glossary">\n{body}\n</section>'
    return html, book_meta.GLOSSARY_TITLE


def render_index(markdown_source: str) -> tuple[str, str, str]:
    """Convert a generated Index section into the last page of the book.

    `tools/make_index.py` writes markdown so that the index goes through the
    same converter as every other page: a heading, a note, a list. The heading
    is given the anchor by hand and followed by the running-head marker, exactly
    as `render_glossary` does, so the index gets a running head and a page break
    without a second set of rules for one section.

    Returns (html, anchor, title) like the front-matter renderers.
    """
    converter = chapter_mod._make_converter("index")
    body = converter.convert(markdown_source)
    heads = [t for t in getattr(converter, "toc_tokens", []) if t["level"] == 1]
    title = (
        html_mod.unescape(re.sub(r"<[^>]+>", "", heads[0]["name"])).strip()
        if heads
        else make_index.INDEX_TITLE
    )
    body = re.sub(
        r"<h1[^>]*>", f'<h1 class="chapter-title" id="{INDEX_ID}">', body, count=1
    )
    body = body.replace(
        "</h1>",
        f'</h1>\n<p class="runhead-marker">{html_mod.escape(title)}</p>',
        1,
    )
    html = f'<section class="chapter appendix" id="section-index">\n{body}\n</section>'
    return html, INDEX_ID, title


def render_document(body: str, css: str, subtitle: str) -> str:
    esc = html_mod.escape
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>{esc(book_meta.BOOK_TITLE_FULL)}</title>
<meta name="author" content="{esc(book_meta.AUTHOR)}"/>
<meta name="description" content="{esc(subtitle)} — {esc(book_meta.CORPUS_NOTE)}"/>
<meta name="dcterms.created" content="{esc(book_meta.DATE)}"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<style>
{css}
</style>
</head>
<body>
{body}
</body>
</html>
"""


def pygments_css() -> str:
    from pygments.formatters import HtmlFormatter

    return HtmlFormatter(style="friendly").get_style_defs("div.codehilite")


# --------------------------------------------------------------------------
# pipeline
# --------------------------------------------------------------------------


def build(args: argparse.Namespace, index_markdown: str | None = None) -> int:
    """One pass of the build. With `index_markdown`, the second one.

    `index_markdown` is the only way the assembly differs between the two
    passes, and it is None everywhere except in `build_with_index`'s second
    call: a build without an index must produce the bytes it produced before
    this parameter existed.
    """
    report = BuildReport()

    book_dir = Path(args.book_dir).resolve()
    manifest_path = Path(args.manifest).resolve()

    # A stem passed by hand is a deliberate experiment, so a file that is not
    # there stays a warning; a stem read from the manifest is a claim about
    # what the book *is*, so a file that is not there is fatal.  Without that
    # asymmetry a typo in the manifest would ship a book with a chapter
    # missing and a clean exit status.
    if args.chapters:
        chapter_ids = list(args.chapters)
    else:
        try:
            chapter_ids = load_manifest(manifest_path)
        except (FileNotFoundError, ValueError) as exc:
            print(f"[error] {exc}", file=sys.stderr)
            return 2
        absent = [c for c in chapter_ids if not (book_dir / f"{c}.md").is_file()]
        if absent:
            print(
                f"[error] {manifest_path} lists {len(absent)} file(s) absent "
                f"from {book_dir}: {', '.join(absent)}",
                file=sys.stderr,
            )
            return 2
        print(
            f"[info] chapters from {manifest_path.name} ({len(chapter_ids)})",
            file=sys.stderr,
        )

    meta_dir = Path(args.meta_dir).resolve()
    out_base = Path(args.out_base).resolve()
    out_base.parent.mkdir(parents=True, exist_ok=True)
    cache_dir = out_base.parent / "mermaid_cache"
    wave_cache_dir = out_base.parent / "wavedrom_cache"

    if args.refresh_mermaid and cache_dir.exists():
        shutil.rmtree(cache_dir)
    if args.refresh_wavedrom and wave_cache_dir.exists():
        shutil.rmtree(wave_cache_dir)

    bib: Bibliography = load_bibliography(
        meta_dir / "references.md", meta_dir / "corpus_index.md"
    )
    if not bib.references_found:
        report.warn(
            f"{meta_dir / 'references.md'} not found — every citation will use "
            "the corpus_index.md fallback string"
        )

    chapters: list[chapter_mod.Chapter] = []
    diagrams: dict[str, mermaid.Diagram] = {}
    waveforms: dict[str, wavedrom.Diagram] = {}

    for chapter_id in chapter_ids:
        path = book_dir / f"{chapter_id}.md"
        if not path.is_file():
            report.warn(f"{path} not found — chapter skipped")
            continue
        raw = path.read_text(encoding="utf-8")
        raw, found = mermaid.extract(raw)
        diagrams.update(found)
        # Two extractors over the same text, each with its own placeholder
        # namespace: a structural diagram and a timing diagram are the same kind
        # of float to everything downstream, and different kinds of source.
        raw, found_waves = wavedrom.extract(raw)
        waveforms.update(found_waves)
        processed = chapter_mod.process(chapter_id, raw, bib)
        for message in processed.warnings:
            report.warn(message)
        chapters.append(processed)

    if not chapters:
        print("[error] no chapters to build", file=sys.stderr)
        return 2

    print(
        f"[info] {len(chapters)} chapter(s), {len(diagrams)} unique diagram(s)"
        + (f", {len(waveforms)} timing diagram(s)" if waveforms else ""),
        file=sys.stderr,
    )
    try:
        mermaid.render_all(diagrams, cache_dir, report.warn)
    except mermaid.MermaidError as exc:
        report.warn(f"mermaid rendering failed: {exc}")
    try:
        wavedrom.render_all(waveforms, wave_cache_dir, report.warn)
    except wavedrom.WavedromError as exc:
        report.warn(f"wavedrom rendering failed: {exc}")

    glossary = render_glossary(meta_dir / "glossary.md", report)

    # (label, html) for every piece the document is assembled from, so a
    # residual author token can be reported against the file that carries it.
    token_sources: list[tuple[str, str]] = [
        (f"book/{processed.chapter_id}.md", processed.html) for processed in chapters
    ]
    if glossary is not None:
        token_sources.append(("meta/glossary.md (Appendix A)", glossary[0]))

    # --- assemble -----------------------------------------------------
    toc_items: list[tuple[str, str, str]] = []
    flow: list[str] = []
    seen_parts: set[int] = set()

    # Back matter is collected separately so the glossary can sit at Appendix A,
    # ahead of the other appendices, regardless of the order they were passed in.
    # Sorted by id, so B follows A and C follows B however they were passed on
    # the command line: half-automatic ordering (glossary forced, the rest by
    # argument order) is worse than either, because it looks deliberate.
    back_matter: list[tuple[str, str, str, str]] = []

    for processed in chapters:
        if book_meta.is_appendix(processed.chapter_id):
            back_matter.append(
                (
                    processed.chapter_id,
                    processed.anchor,
                    processed.title,
                    processed.html,
                )
            )
            continue

        part_no = book_meta.CHAPTER_PART.get(processed.chapter_id)
        if part_no is not None and part_no not in seen_parts:
            seen_parts.add(part_no)
            part = book_meta.PARTS[part_no]
            flow.append(render_part_divider(part))
            toc_items.append(("toc-part", part["id"], part["title"]))
        elif part_no is None:
            report.warn(
                f"{processed.chapter_id}: no entry in CHAPTER_PART; no part divider"
            )
        toc_items.append(("toc-chapter", processed.anchor, processed.title))
        for entry in processed.toc:
            if entry.level == 2:
                toc_items.append(("toc-section", entry.anchor, entry.text))
        flow.append(processed.html)

    if glossary is not None:
        glossary_html, glossary_title = glossary
        toc_items.append(("toc-appendix", book_meta.GLOSSARY_ID, glossary_title))
        flow.append(glossary_html)

    for _, anchor, title, html in sorted(back_matter):
        toc_items.append(("toc-appendix", anchor, title))
        flow.append(html)

    # The index is the last section of the book, after the last appendix. Not a
    # preference: its page numbers were measured on the first pass, and only a
    # section added after everything else leaves those pages where they were.
    if index_markdown is not None:
        index_html, index_anchor, index_title = render_index(index_markdown)
        toc_items.append(("toc-appendix", index_anchor, index_title))
        flow.append(index_html)
        token_sources.append(("the generated index", index_html))

    subtitle = book_meta.subtitle_for(chapter_ids)

    # --- front matter -------------------------------------------------
    # Set in the order a monograph sets it: copyright verso, contents, lists of
    # floats, then the prose front matter. The copyright page is deliberately
    # absent from the contents, as it is in a printed book.
    front_dir = ROOT / "front"
    copyright_page = render_front_matter(
        front_dir, "copyright", "copyright-page", report
    )
    front_toc: list[tuple[str, str, str]] = []
    front_flow: list[str] = []
    for html, anchor, title in render_float_lists(chapters):
        front_toc.append(("toc-front", anchor, title))
        front_flow.append(html)
    if copyright_page is not None:
        token_sources.append(("front/copyright.md", copyright_page[0]))
    for name in book_meta.FRONT_MATTER_AFTER_LISTS:
        entry = render_front_matter(front_dir, name, "frontmatter", report)
        if entry is None:
            continue
        html, anchor, title = entry
        front_toc.append(("toc-front", anchor, title))
        front_flow.append(html)
        token_sources.append((f"front/{name}.md", html))

    body = "\n\n".join(
        [
            render_title_page(subtitle),
            '<div class="book">',
            *([copyright_page[0]] if copyright_page else []),
            render_toc(front_toc + toc_items),
            *front_flow,
            *flow,
            "</div>",
        ]
    )

    css = pygments_css() + "\n\n" + (TOOLS / "book_style.css").read_text(
        encoding="utf-8"
    )

    html_inline = render_document(
        wavedrom.substitute(
            mermaid.substitute(body, diagrams, inline=True), waveforms, inline=True
        ),
        css,
        subtitle,
    )
    html_path = out_base.with_suffix(".html")
    html_path.write_text(html_inline, encoding="utf-8")
    print(f"[info] wrote {html_path}", file=sys.stderr)

    # An unconverted [cit:...] marker or an [UNVERIFIED] tag is a note to the
    # author that a reader should never meet: the first means the bibliography
    # machinery did not see the citation, the second that a claim has nothing
    # behind it yet.  Both were warnings until the September 2026 build, and a
    # warning is what you scroll past -- they are now fatal, and the message
    # names the file to open.
    leaked = scan_author_tokens(token_sources, html_inline)

    if not args.no_pdf:
        html_for_pdf = render_document(
            wavedrom.substitute(
                mermaid.substitute(body, diagrams, inline=False),
                waveforms,
                inline=False,
            ),
            css,
            subtitle,
        )
        pdf_source = out_base.parent / f"{out_base.name}.pdf-source.html"
        pdf_source.write_text(html_for_pdf, encoding="utf-8")
        from weasyprint import HTML as WeasyHTML

        pdf_path = out_base.with_suffix(".pdf")
        WeasyHTML(filename=str(pdf_source), base_url=str(out_base.parent)).write_pdf(
            str(pdf_path)
        )
        if not args.keep_pdf_source:
            pdf_source.unlink()
        print(f"[info] wrote {pdf_path}", file=sys.stderr)

    # --- report -------------------------------------------------------
    used_fallback = sorted(
        {
            cit_id
            for processed in chapters
            for cit_id in processed.cited_ids
            if cit_id in bib.fallback_ids
        }
    )
    missing = sorted(bib.missing_ids)

    print("\n=== build summary ===", file=sys.stderr)
    print(f"chapters : {', '.join(c.chapter_id for c in chapters)}", file=sys.stderr)
    print(f"diagrams : {len(diagrams)}", file=sys.stderr)
    if used_fallback:
        # A corpus fallback is not a cosmetic gap. The References section a reader
        # opens prints "[no references.md entry — corpus fallback]" in place of the
        # source, so the defect is invisible to the build's own exit status and
        # perfectly visible on the page. Two of these shipped through several clean
        # builds before anyone read the rendered bibliography.
        #
        # Registering it as a warning is what makes "zero warnings" mean what every
        # editorial brief in this project claims it means.
        for cid in used_fallback:
            report.warn(
                f"citation {cid} has no references.md entry; the rendered "
                f"bibliography will print a corpus-fallback placeholder"
            )
        print(
            f"corpus-fallback citations ({len(used_fallback)}): "
            f"{', '.join(used_fallback)}",
            file=sys.stderr,
        )
    if report.warnings:
        print(f"warnings : {len(report.warnings)}", file=sys.stderr)

    if leaked:
        print(
            "\n[FAIL] author tokens survived into the built HTML, where a "
            f"reader would meet them ({len(leaked)} source(s)):",
            file=sys.stderr,
        )
        for line in leaked:
            print(f"  {line}", file=sys.stderr)

    if missing:
        print(
            "\n[FAIL] citation IDs with no entry in references.md and none in "
            f"corpus_index.md ({len(missing)}): {', '.join(missing)}",
            file=sys.stderr,
        )

    return 1 if (leaked or missing) else 0


def build_with_index(args: argparse.Namespace) -> int:
    """The two-pass build of `meta/IMPROVEMENT_PLAN.md` §W3.

    Pass one is an ordinary build, whose PDF is the document the page scan
    measures. `tools/make_index.py` reads it and `meta/index_terms.md` and
    returns the Index section. Pass two rebuilds HTML and PDF with that section
    appended after the last appendix.

    The guard is the point of the ordering. The index's page numbers describe
    the first pass; the second pass adds pages at the end, which moves nothing
    before them — unless the one extra line in the table of contents overflows
    it onto a further page, which would shift every page of the book by one and
    leave an index that is uniformly, invisibly wrong. So the level-1 outline of
    the two PDFs is compared entry by entry, and a single moved page fails the
    build rather than warning about it: the index that was just written would be
    a document nobody could tell from a correct one.

    Exit codes: 0 both passes clean; 1 a pass failed, the term list is
    malformed, or a page moved between the passes; 2 the index could not be
    built (no `pdftotext`, no outline, no term list).
    """
    if args.no_pdf:
        print(
            "[error] --with-index needs the PDF of the first pass to scan; "
            "it cannot be combined with --no-pdf",
            file=sys.stderr,
        )
        return 2
    terms_path = Path(args.index_terms)
    try:
        terms_text = terms_path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"[error] cannot read {terms_path}: {exc}", file=sys.stderr)
        return 2

    print("[info] index pass 1 of 2: the book without an index", file=sys.stderr)
    code = build(args)
    if code != 0:
        print(
            "[error] the first pass failed; no index was built from it",
            file=sys.stderr,
        )
        return code

    pdf_path = Path(args.out_base).resolve().with_suffix(".pdf")
    try:
        before = make_index.outline_starts(pdf_path)
        result = make_index.build_index(pdf_path, terms_text)
    except make_index.InputError as exc:
        print(f"[error] index: {exc}", file=sys.stderr)
        return 2
    for line in make_index.report_lines(result):
        print(line, file=sys.stderr)
    if result.fatal:
        return 1

    print("[info] index pass 2 of 2: the book with the index", file=sys.stderr)
    code = build(args, index_markdown=make_index.render_markdown(result))
    if code != 0:
        return code

    try:
        after = make_index.outline_starts(pdf_path)
    except make_index.InputError as exc:
        print(f"[error] index: {exc}", file=sys.stderr)
        return 2
    # Compared by position, not by title. The index is appended last, so the
    # first `len(before)` entries of `after` are the same sections in the same
    # order; a dict keyed on the title would collapse two level-1 sections that
    # share a name and skip any section whose title the second pass changed,
    # which is exactly when a page is most likely to have moved.
    if len(after) < len(before):
        print(
            f"\n[FAIL] the second pass has {len(after)} level-1 section(s) "
            f"against {len(before)} in the first; the two passes did not build "
            f"the same book",
            file=sys.stderr,
        )
        return 1
    moved = [
        (title, page, after[position][1])
        for position, (title, page) in enumerate(before)
        if after[position][1] != page
    ]
    if moved:
        print(
            f"\n[FAIL] the second pass moved {len(moved)} section(s), so every "
            f"page number in the index it just wrote is wrong:",
            file=sys.stderr,
        )
        for title, was, now in moved[:10]:
            print(f"  {title!r}: page {was} -> {now}", file=sys.stderr)
        print(
            "  The extra table-of-contents line overflowed a page. Shorten the "
            "index's title or note, or set the index's own entry aside, and run "
            "again. The HTML and the PDF on disk are the second pass, so they "
            f"carry that wrong index: rebuild without --with-index before "
            f"anything reads {pdf_path.name}.",
            file=sys.stderr,
        )
        return 1
    print(
        f"[info] index: {len(before)} section(s) unmoved between the passes; "
        f"the page numbers hold",
        file=sys.stderr,
    )
    return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build the Hardware Verification guide (HTML + PDF)."
    )
    parser.add_argument(
        "--chapters",
        nargs="+",
        help="chapter stems, e.g. ch01 ch02 (default: every stem in --manifest)",
    )
    parser.add_argument(
        "--out-base",
        default=str(DEFAULT_OUT_BASE),
        help="output path without extension "
        "(default: build/hardware_verification_guide)",
    )
    parser.add_argument(
        "--manifest",
        default=str(DEFAULT_MANIFEST),
        help="the book's file stems, in order (default: meta/book_manifest.txt)",
    )
    parser.add_argument("--book-dir", default=str(ROOT / "book"))
    parser.add_argument("--meta-dir", default=str(ROOT / "meta"))
    parser.add_argument("--no-pdf", action="store_true", help="HTML only (fast)")
    parser.add_argument(
        "--refresh-mermaid", action="store_true", help="drop the diagram cache first"
    )
    parser.add_argument(
        "--refresh-wavedrom",
        action="store_true",
        help="drop the timing-diagram cache first",
    )
    parser.add_argument(
        "--keep-pdf-source",
        action="store_true",
        help="keep the intermediate <out>.pdf-source.html",
    )
    parser.add_argument(
        "--with-index",
        action="store_true",
        help="build twice and ship an analytical index: pass one is scanned "
        "page by page for the terms of --index-terms, pass two carries the "
        "Index section that scan produced (adds one full build to the run)",
    )
    parser.add_argument(
        "--index-terms",
        default=str(ROOT / "meta" / "index_terms.md"),
        help="the index's term list (default: meta/index_terms.md)",
    )
    return parser.parse_args(argv)


if __name__ == "__main__":
    _args = parse_args()
    sys.exit(build_with_index(_args) if _args.with_index else build(_args))
