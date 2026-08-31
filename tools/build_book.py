#!/usr/bin/env python3
"""Build the book: markdown chapters -> one professional HTML + PDF.

    micromamba run -n gvsoc_env_3_12 python3 tools/build_book.py \
        --chapters ch01 ch02 ch03 ch04 ch05 ch06 ch07 \
        --out-base build/hw_verification_guide_parts_1_2

Produces <out-base>.html (inline SVG diagrams, browser-readable) and
<out-base>.pdf (WeasyPrint; diagrams as data-URI SVG because WeasyPrint 52.5
cannot lay out inline <svg>).  Idempotent: same inputs -> same bytes.
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
import mermaid  # noqa: E402
from references import Bibliography, load_bibliography  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
TOOLS = Path(__file__).resolve().parent


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
      <div class="tp-note">{esc(book_meta.DRAFT_NOTE)}</div>
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


def render_document(body: str, css: str, subtitle: str) -> str:
    esc = html_mod.escape
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>{esc(book_meta.BOOK_TITLE_FULL)}</title>
<meta name="author" content="{esc(book_meta.AUTHOR)}"/>
<meta name="description" content="{esc(subtitle)} — {esc(book_meta.DRAFT_NOTE)}"/>
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


def build(args: argparse.Namespace) -> int:
    report = BuildReport()

    book_dir = Path(args.book_dir).resolve()
    meta_dir = Path(args.meta_dir).resolve()
    out_base = Path(args.out_base).resolve()
    out_base.parent.mkdir(parents=True, exist_ok=True)
    cache_dir = out_base.parent / "mermaid_cache"

    if args.refresh_mermaid and cache_dir.exists():
        shutil.rmtree(cache_dir)

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

    for chapter_id in args.chapters:
        path = book_dir / f"{chapter_id}.md"
        if not path.is_file():
            report.warn(f"{path} not found — chapter skipped")
            continue
        raw = path.read_text(encoding="utf-8")
        raw, found = mermaid.extract(raw)
        diagrams.update(found)
        processed = chapter_mod.process(chapter_id, raw, bib)
        for message in processed.warnings:
            report.warn(message)
        chapters.append(processed)

    if not chapters:
        print("[error] no chapters to build", file=sys.stderr)
        return 2

    print(
        f"[info] {len(chapters)} chapter(s), {len(diagrams)} unique diagram(s)",
        file=sys.stderr,
    )
    try:
        mermaid.render_all(diagrams, cache_dir, report.warn)
    except mermaid.MermaidError as exc:
        report.warn(f"mermaid rendering failed: {exc}")

    glossary = render_glossary(meta_dir / "glossary.md", report)

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

    subtitle = book_meta.subtitle_for(args.chapters)

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
    for name in book_meta.FRONT_MATTER_AFTER_LISTS:
        entry = render_front_matter(front_dir, name, "frontmatter", report)
        if entry is None:
            continue
        html, anchor, title = entry
        front_toc.append(("toc-front", anchor, title))
        front_flow.append(html)

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
        mermaid.substitute(body, diagrams, inline=True), css, subtitle
    )
    html_path = out_base.with_suffix(".html")
    html_path.write_text(html_inline, encoding="utf-8")
    print(f"[info] wrote {html_path}", file=sys.stderr)

    leaked = re.findall(r"\[cit:[^\]]*\]", html_inline)
    if leaked:
        report.warn(
            f"{len(leaked)} unconverted [cit:...] token(s) survived into the HTML: "
            f"{sorted(set(leaked))[:5]}"
        )

    # An [UNVERIFIED] tag is an internal note to the author, never something a
    # reader should meet. Every shipped chapter so far carries zero, so a tag
    # reaching the HTML means a chapter went out with a claim still unsourced.
    unverified = re.findall(r"\[UNVERIFIED[^\]]*\]", html_inline)
    if unverified:
        report.warn(
            f"{len(unverified)} [UNVERIFIED] tag(s) survived into the HTML — "
            f"reframe as practitioner judgment or ground the claim: "
            f"{sorted(set(unverified))[:5]}"
        )

    if not args.no_pdf:
        html_for_pdf = render_document(
            mermaid.substitute(body, diagrams, inline=False), css, subtitle
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

    if missing:
        print(
            "\n[FAIL] citation IDs with no entry in references.md and none in "
            f"corpus_index.md ({len(missing)}): {', '.join(missing)}",
            file=sys.stderr,
        )
        return 1
    return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build the Hardware Verification guide (HTML + PDF)."
    )
    parser.add_argument(
        "--chapters", nargs="+", required=True, help="chapter stems, e.g. ch01 ch02"
    )
    parser.add_argument(
        "--out-base", required=True, help="output path without extension"
    )
    parser.add_argument("--book-dir", default=str(ROOT / "book"))
    parser.add_argument("--meta-dir", default=str(ROOT / "meta"))
    parser.add_argument("--no-pdf", action="store_true", help="HTML only (fast)")
    parser.add_argument(
        "--refresh-mermaid", action="store_true", help="drop the diagram cache first"
    )
    parser.add_argument(
        "--keep-pdf-source",
        action="store_true",
        help="keep the intermediate <out>.pdf-source.html",
    )
    return parser.parse_args(argv)


if __name__ == "__main__":
    sys.exit(build(parse_args()))
