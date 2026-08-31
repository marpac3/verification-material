"""Per-chapter markdown transforms: heading normalisation, citations, HTML."""

from __future__ import annotations

import html as html_mod
import re
from dataclasses import dataclass, field

import markdown
from markdown.extensions.toc import slugify as toc_slugify

import book_meta
import floats as floats_mod
from references import Bibliography

_FENCE = re.compile(r"^[ \t]*(```|~~~)")
_ATX = re.compile(r"^(#{1,6})[ \t]+(.*?)[ \t]*#*[ \t]*$")
_CITE = re.compile(r"\[cit:\s*([A-Za-z]{1,3}\d{1,3}(?:\s*,\s*[A-Za-z]{1,3}\d{1,3})*)\s*\]")
# Inline code spans, so that a citation-looking token inside `code` is left alone.
_INLINE_CODE = re.compile(r"(?<!`)(`+)(?!`)(.+?)(?<!`)\1(?!`)", re.S)

MD_EXTENSIONS = ["extra", "codehilite", "sane_lists", "smarty", "toc"]


@dataclass
class TocEntry:
    level: int
    anchor: str
    text: str


@dataclass
class Chapter:
    chapter_id: str
    title: str = ""
    anchor: str = ""
    html: str = ""
    toc: list[TocEntry] = field(default_factory=list)
    cited_ids: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    floats: list[floats_mod.Float] = field(default_factory=list)


# --- heading normalisation -------------------------------------------------


def normalise_headings(text: str) -> str:
    """Force the chapter apparatus to level 3 (# chapter / ## section / ### apparatus)."""
    out: list[str] = []
    in_fence = False
    for line in text.split("\n"):
        if _FENCE.match(line):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue
        match = _ATX.match(line)
        if match and len(match.group(1)) >= 2:
            title = match.group(2).strip()
            if title.lower() in book_meta.APPARATUS_HEADINGS:
                out.append(f"### {title} {{: .apparatus }}")
                continue
        out.append(line)
    return "\n".join(out)


# --- citations -------------------------------------------------------------


class CitationNumbering:
    """Per-chapter numbering by order of first appearance."""

    def __init__(self, chapter_id: str) -> None:
        self.chapter_id = chapter_id
        self.order: list[str] = []

    def number(self, cit_id: str) -> int:
        if cit_id not in self.order:
            self.order.append(cit_id)
        return self.order.index(cit_id) + 1

    def render(self, ids: list[str]) -> str:
        numbers = sorted({self.number(i) for i in ids})
        links = ", ".join(
            f'<a href="#{self.chapter_id}-ref-{n}">{n}</a>' for n in numbers
        )
        return f'<sup class="cit">[{links}]</sup>'


def substitute_citations(text: str, numbering: CitationNumbering) -> str:
    """Rewrite [cit:ID[,ID...]] outside fenced blocks and inline code spans."""

    def replace_in_prose(segment: str) -> str:
        def one(match: re.Match[str]) -> str:
            ids = [i.strip() for i in match.group(1).split(",") if i.strip()]
            return numbering.render(ids)

        return _CITE.sub(one, segment)

    out: list[str] = []
    in_fence = False
    for line in text.split("\n"):
        if _FENCE.match(line):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence or "[cit:" not in line:
            out.append(line)
            continue

        pieces: list[str] = []
        cursor = 0
        for code in _INLINE_CODE.finditer(line):
            pieces.append(replace_in_prose(line[cursor : code.start()]))
            pieces.append(code.group(0))
            cursor = code.end()
        pieces.append(replace_in_prose(line[cursor:]))
        out.append("".join(pieces))
    return "\n".join(out)


def build_reference_block(
    chapter_id: str, numbering: CitationNumbering, bib: Bibliography
) -> str:
    items = []
    for index, cit_id in enumerate(numbering.order, start=1):
        text = html_mod.escape(bib.resolve(cit_id), quote=False)
        items.append(
            f'<li id="{chapter_id}-ref-{index}">'
            f'<span class="ref-id">{html_mod.escape(cit_id)}</span> {text}</li>'
        )
    body = "\n".join(items)
    return (
        f"\n\n### {book_meta.REFERENCES_HEADING} {{: .apparatus }}\n\n"
        f'<ol class="reflist">\n{body}\n</ol>\n'
    )


def insert_reference_section(text: str, block: str) -> str:
    """Place References after 'Further reading', else at the end of the chapter."""
    lines = text.split("\n")
    anchor = None
    in_fence = False
    for index, line in enumerate(lines):
        if _FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = _ATX.match(line)
        if match and match.group(2).strip().split("{")[0].strip().lower() == (
            book_meta.FURTHER_READING_HEADING
        ):
            anchor = index
            break
    if anchor is None:
        return text.rstrip() + block

    in_fence = False
    for index in range(anchor + 1, len(lines)):
        if _FENCE.match(lines[index]):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = _ATX.match(lines[index])
        if match and len(match.group(1)) <= 3:
            head = "\n".join(lines[:index]).rstrip()
            tail = "\n".join(lines[index:])
            return f"{head}{block}\n{tail}"
    return text.rstrip() + block


# --- conversion ------------------------------------------------------------


def _make_converter(chapter_id: str) -> markdown.Markdown:
    def slug(value: str, separator: str) -> str:
        return f"{chapter_id}-{toc_slugify(value, separator)}"

    return markdown.Markdown(
        extensions=MD_EXTENSIONS,
        extension_configs={
            "codehilite": {
                "guess_lang": False,
                "linenums": False,
                "css_class": "codehilite",
            },
            "toc": {"permalink": False, "slugify": slug, "toc_depth": "1-2"},
        },
        output_format="html",
    )


def _flatten_toc(tokens: list[dict], out: list[TocEntry]) -> None:
    for token in tokens:
        # toc_tokens carry rendered HTML (smarty emits &rsquo; &amp; ...);
        # unescape so downstream escaping does not double-encode.
        plain = html_mod.unescape(re.sub(r"<[^>]+>", "", token["name"])).strip()
        out.append(
            TocEntry(level=token["level"], anchor=token["id"], text=plain)
        )
        _flatten_toc(token.get("children", []), out)


def process(chapter_id: str, raw: str, bib: Bibliography) -> Chapter:
    """Full per-chapter pipeline: normalise -> cite -> references -> HTML."""
    chapter = Chapter(chapter_id=chapter_id)

    text = normalise_headings(raw)

    # Float apparatus before citations: a caption may carry its own [cit:] marker,
    # and numbering must see the document in source order.
    float_result = floats_mod.process(text, chapter_id)
    text = float_result.text
    chapter.floats = float_result.floats
    chapter.warnings.extend(float_result.warnings)
    if float_result.errors:
        raise ValueError("; ".join(float_result.errors))

    numbering = CitationNumbering(chapter_id)
    text = substitute_citations(text, numbering)
    chapter.cited_ids = list(numbering.order)
    if numbering.order:
        text = insert_reference_section(
            text, build_reference_block(chapter_id, numbering, bib)
        )
    elif not book_meta.is_appendix(chapter_id):
        # Appendices cite the book, not the corpus, so having no markers is
        # their normal state rather than a defect.
        chapter.warnings.append(f"{chapter_id}: no [cit:...] found")

    converter = _make_converter(chapter_id)
    body = converter.convert(text)
    _flatten_toc(getattr(converter, "toc_tokens", []), chapter.toc)

    heads = [entry for entry in chapter.toc if entry.level == 1]
    if not heads:
        raise ValueError(f"{chapter_id}: no level-1 chapter heading found")
    chapter.title = heads[0].text
    chapter.anchor = heads[0].anchor
    if len(heads) > 1:
        chapter.warnings.append(
            f"{chapter_id}: {len(heads)} level-1 headings; using the first"
        )

    # Tag the opening <h1> so CSS can start the chapter on a new page, and
    # follow it with the marker that arms the running head from page 2 on.
    marker = (
        f'<p class="runhead-marker">{html_mod.escape(chapter.title)}</p>'
    )
    body = body.replace(
        f'<h1 id="{chapter.anchor}">',
        f'<h1 class="chapter-title" id="{chapter.anchor}">',
        1,
    ).replace(
        f"</h1>", f"</h1>\n{marker}", 1
    )
    chapter.html = f'<section class="chapter" id="{chapter_id}">\n{body}\n</section>'
    return chapter
