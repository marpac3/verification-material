#!/usr/bin/env python3
"""The analytical index: terms to printed pages, from the first build pass.

    python3 tools/make_index.py --pdf build/hardware_verification_guide.pdf \
        --terms meta/index_terms.md --out build/index.md
    python3 tools/make_index.py --pdf … --terms … --json -

`meta/IMPROVEMENT_PLAN.md` §W3 asks for a two-pass build: a list of terms, a
`pdftotext` scan for the page each occurs on, a generated Index section, a
second build. This is the middle step. `tools/build_book.py --with-index` drives
both passes; this module is also a command, because the scan is the part a human
wants to run and read on its own while tuning `meta/index_terms.md`.

The term list is `meta/index_terms.md` and its format is documented there. This
module carries no list of terms: an index whose vocabulary lived in a tool would
be a vocabulary nobody could review.

Where the page text comes from
------------------------------
`pdftotext` (poppler), one call for the whole document, split on the form feeds
it writes between pages. `pdftotext` is what §W3 names, and the alternative in
this environment — PyMuPDF's own extractor — is used here only for the outline,
below. If `pdftotext` is not on the path the tool exits 2 rather than falling
back to something untested.

Two kinds of furniture are removed from each page before matching:

* **the running head.** WeasyPrint sets it from the section's title
  (`tools/book_style.css`, `string-set: runhead`), so «6. Coverage: Theory and
  Practice» is the first line of every page of chapter 6 — and the word
  «coverage» would then occur on all seventeen of them whatever the pages say.
  It is stripped only when the first non-blank line *equals* the section title
  the outline gives for that page, which is true of 547 of the 573 pages of the
  build of 2026-09-08; the other 26 are the part dividers, the two-line chapter
  titles and the front matter, where nothing is stripped and nothing is lost.
* **the folio**, the last line when it is exactly the page's own number. True of
  558 of those 573 pages, the rest being pages that print no folio (the title
  page, the part dividers, the blank versos).

How the boundaries are recognised
---------------------------------
From the PDF outline. WeasyPrint 52.5 emits bookmarks — 619 of them for the
build of 2026-09-08 — and its level-1 entries are exactly the front-matter
pages, the 26 chapters and the appendices, each with the page it starts on. So
the section in force on any page is known exactly, and:

* **front matter** is every page before the first chapter, the first level-1
  entry whose title begins with a number and a period (`1. Why Verification
  Exists`);
* **the glossary, the solutions and the index** are the runs of the level-1
  entries whose titles begin with one of `--exclude-prefix` (by default
  `Appendix A`, `Appendix D` and `Index`). The prefix, not the whole title,
  because the separator is not uniform in the book: `Appendix A — Glossary`
  takes an em dash and `Appendix D: Solutions to the exercises` a colon.

A run ends where the next level-1 entry starts, or at the end of the document.

There is no fallback. If the PDF carries no outline the tool exits 2 and says
so: guessing the boundaries from the running heads alone gets page 5 wrong — its
first line is `5.4 The plan review as a rite`, a line of the table of contents
and not a running head — and an index that quietly indexes the solutions is
worse than an index that refuses to be built.

Matching
--------
Whole word, without regard to case, literal otherwise. Internal whitespace
matches any run of whitespace, so a term broken across a line of the PDF still
matches. Word boundaries are asserted only at an edge that is alphanumeric, so
`(test, seed) matrix` is not required to be preceded by a word character.

There is deliberately **no** plural tolerance, unlike `check_glossary.py`'s
subject check: there the tolerance keeps a human's review list short, here the
index's own format has aliases for exactly this, and an index that silently
matched more than the entry says would be an index nobody could predict.

Output
------
Markdown: a level-1 `Index` heading, a note, and one list item per entry in
alphabetical order — `**term** 12, 45-47`, or `**term** *see* other term`.
`build_book.py` converts it with the same machinery as the glossary, so the
index has whatever the book's markdown gives a list. Its typographic design —
two columns, no bullets — is a matter for `tools/book_style.css` and is left to
the coordinator: Pass H does not retune page geometry, and a change to the CSS
would move every page number this index just measured.

Entries found on no page are **not** put in the index. They are returned in the
review list and printed, because a term the book never writes is a defect of the
term list and an entry with no pages is a defect of the page.

Exit codes
----------
0   the index was built (a review list may have been printed).
1   the term list has a malformed line: no index can be built from it.
2   the tool could not run: no `pdftotext`, no readable PDF, no outline, no
    term list.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

FATAL = "FATAL"
REVIEW = "REVIEW"
PASS = "PASS"

# The level-1 outline titles whose pages the index does not cover. Prefixes, not
# whole titles: see the docstring on the separator.
DEFAULT_EXCLUDE_PREFIXES = ("Appendix A", "Appendix D", "Index")

# A level-1 entry that opens a numbered chapter: `1. Why Verification Exists`.
# The first one ends the front matter.
CHAPTER_TITLE_RE = re.compile(r"^\d+\.\s")

ALIAS_SEP = re.compile(r"\s*;\s*")
SEE_SEP = "->"
ALIAS_MARK = "="
# The separators, as the format spells them: whitespace on both sides. A bare
# `->` or `=` matched anywhere in the line would read `|-> (implication)` as an
# entry named `|`, and `a==b` as `a` with the alias `=b`.
SEE_PATTERN = re.compile(r"\s" + re.escape(SEE_SEP) + r"\s")
ALIAS_PATTERN = re.compile(r"\s" + re.escape(ALIAS_MARK) + r"\s")
# Markdown emphasis around a term, as `check_glossary` strips it: the glossary
# writes `*golden model*` and `` `ignore_bins` ``, the PDF text carries no
# markers, and a term copied across with them matches nothing.
# `_` is not in the class: `ignore_bins` is an identifier, not emphasis.
EMPHASIS_RE = re.compile(r"[*`]")

# A trailing comment: whitespace, then `#`, to the end of the line. The
# whitespace is required so that a `#` inside a term is not a comment marker,
# and the whole-line form (`#` in the first column) is the same rule applied to
# a line whose entry is empty.
TRAILING_COMMENT_RE = re.compile(r"\s+#.*$")

# The heading and the note of the generated section. The note says what a page
# number means in a document that has no pages: the HTML keeps the numbers of
# the printed edition, because an HTML reader has a search box and a paper
# reader has nothing else.
INDEX_TITLE = "Index"
INDEX_NOTE = (
    "Page numbers are those of the printed edition. They are kept in the "
    "web version as a reference to it; a reader of the web version has the "
    "browser's own search, which no index can improve on. The index covers "
    "the chapters: it does not list the pages of the glossary, of the "
    "solutions or of this index, so a term is listed where the book discusses "
    "it and not where it is defined in a table or repeated in an answer."
)


class InputError(RuntimeError):
    """Something that makes the index unbuildable -> exit 2."""


@dataclass(frozen=True)
class Entry:
    """One line of the term list."""

    term: str
    line: int
    aliases: tuple[str, ...] = ()
    see: str | None = None

    @property
    def spellings(self) -> tuple[str, ...]:
        return (self.term, *self.aliases)

    @property
    def sort_key(self) -> tuple[str, str]:
        # Case-insensitive, and the term itself as the tie-break so `SVA` and
        # `sva` cannot swap places between two runs of the tool.
        return (self.term.lower(), self.term)


@dataclass
class IndexResult:
    located: list[tuple[Entry, list[int]]] = field(default_factory=list)
    cross_refs: list[Entry] = field(default_factory=list)
    review: list[tuple[Entry, str]] = field(default_factory=list)
    fatal: list[str] = field(default_factory=list)
    pages_scanned: int = 0
    pages_excluded: int = 0

    @property
    def verdict(self) -> str:
        if self.fatal:
            return FATAL
        return REVIEW if self.review else PASS


# --- the term list ----------------------------------------------------------


def parse_terms(text: str) -> tuple[list[Entry], list[str]]:
    """The entries of `meta/index_terms.md`, and one message per malformed line.

    A line is a comment (`#`), blank, a cross-reference (`a -> b`), a term with
    aliases (`a = b; c`), or a term, and may end in a trailing comment. A line
    carrying both marks is malformed rather than resolved by precedence: a
    silent precedence rule is how a term list starts meaning something other
    than what it says.
    """
    entries: list[Entry] = []
    errors: list[str] = []
    seen: dict[str, int] = {}
    for number, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        line = TRAILING_COMMENT_RE.sub("", line).strip()
        if not line:
            continue
        # The separators are spelled with spaces around them, and must be:
        # `|-> (implication)` is SVA vocabulary this book uses, and matching a
        # bare `->` anywhere in the line turns it into an entry named `|`.
        has_see = SEE_PATTERN.search(line) is not None
        has_alias = ALIAS_PATTERN.search(line) is not None
        if has_see and has_alias:
            errors.append(
                f"line {number}: both '{ALIAS_MARK}' and '{SEE_SEP}' in "
                f"{line!r}; a line is either a cross-reference or a term "
                f"with aliases"
            )
            continue
        if has_see:
            head, target = SEE_PATTERN.split(line, maxsplit=1)
            term, target = head.strip(), target.strip()
            if not term or not target:
                errors.append(
                    f"line {number}: {line!r} needs a term on each side of "
                    f"'{SEE_SEP}'"
                )
                continue
            entry = Entry(term=term, line=number, see=target)
        elif has_alias:
            head, tail = ALIAS_PATTERN.split(line, maxsplit=1)
            term = head.strip()
            aliases = tuple(a for a in ALIAS_SEP.split(tail.strip()) if a)
            if not term or not aliases:
                errors.append(
                    f"line {number}: {line!r} needs a term before "
                    f"'{ALIAS_MARK}' and at least one alias after it"
                )
                continue
            entry = Entry(term=term, line=number, aliases=aliases)
        elif line.startswith(SEE_SEP) or line.endswith(SEE_SEP):
            # A separator with nothing on one side of it. Requiring whitespace
            # around `->` keeps `|-> (implication)` a term, and this keeps a
            # half-written cross-reference an error rather than a term named
            # `-> assertion` that would quietly match nothing.
            errors.append(
                f"line {number}: {line!r} needs a term on each side of "
                f"'{SEE_SEP}'"
            )
            continue
        elif line.startswith(ALIAS_MARK) or line.endswith(ALIAS_MARK):
            errors.append(
                f"line {number}: {line!r} needs a term before "
                f"'{ALIAS_MARK}' and at least one alias after it"
            )
            continue
        else:
            entry = Entry(term=line, line=number)
        key = entry.term.lower()
        if key in seen:
            errors.append(
                f"line {number}: {entry.term!r} already listed at line {seen[key]}"
            )
            continue
        seen[key] = number
        entries.append(entry)
    return entries, errors


def bare_spelling(spelling: str) -> str:
    """`spelling` without markdown emphasis and with whitespace normalised.

    The PDF text has no `*` or backtick in it, and a tab in the term list must
    match the single space the typesetter produced.
    """
    return " ".join(EMPHASIS_RE.sub("", spelling).split())


def occurrence_pattern(spelling: str) -> re.Pattern[str]:
    """`spelling` as a whole word, without case, literal otherwise.

    No plural tolerance; see the module docstring on why this differs from
    `check_glossary.occurrence_pattern`.
    """
    spelling = bare_spelling(spelling)
    if not spelling:
        return re.compile(r"(?!)")
    escaped = re.escape(spelling)
    escaped = re.sub(r"(?:\\[ ])+", r"\\s+", escaped)
    prefix = r"\b" if spelling[:1].isalnum() else ""
    suffix = r"\b" if spelling[-1:].isalnum() else ""
    return re.compile(prefix + escaped + suffix, re.IGNORECASE)


# --- the PDF ----------------------------------------------------------------

# WeasyPrint hyphenates with U+2010 HYPHEN, 3275 times in the build of
# 2026-09-08 against 5 line-final U+002D. So a soft hyphen at a line end is
# dropped and the word rejoined, while a hard one is kept: `de‐\nliberate`
# becomes `deliberate` and `shift-\nright` stays `shift-right`.
SOFT_HYPHEN_BREAK = re.compile(r"‐\n")
HARD_HYPHEN_BREAK = re.compile(r"-\n")


def dehyphenate(text: str) -> str:
    text = SOFT_HYPHEN_BREAK.sub("", text)
    return HARD_HYPHEN_BREAK.sub("-", text)


def page_texts(pdf: Path) -> list[str]:
    """One string per page, in order, de-hyphenated. 1-based by position + 1."""
    if not pdf.is_file():
        raise InputError(f"PDF not found: {pdf}")
    if shutil.which("pdftotext") is None:
        raise InputError(
            "pdftotext (poppler-utils) is not on the PATH; the page scan of "
            "meta/IMPROVEMENT_PLAN.md §W3 cannot run"
        )
    try:
        proc = subprocess.run(
            ["pdftotext", str(pdf), "-"],
            capture_output=True,
            text=True,
        encoding="utf-8",
            check=True,
        )
    except subprocess.CalledProcessError as error:
        raise InputError(
            f"pdftotext exited {error.returncode} on {pdf}: "
            f"{(error.stderr or '').strip()[:200]}"
        ) from error
    pages = proc.stdout.split("\f")
    # pdftotext writes a form feed after the last page as well.
    if pages and not pages[-1].strip():
        pages.pop()
    if not pages:
        raise InputError(f"pdftotext extracted no page from {pdf}")
    return [dehyphenate(page) for page in pages]


def outline_starts(pdf: Path) -> list[tuple[str, int]]:
    """Every level-1 outline entry as (title, first page), in document order.

    Also the page-shift guard of `build_book.py --with-index`: comparing this
    list between the two passes is how the second pass proves it did not move
    the pages the index just measured.
    """
    try:
        import fitz  # PyMuPDF
    except ImportError as error:  # pragma: no cover - environment-dependent
        raise InputError(
            "PyMuPDF (fitz) is not installed; the PDF outline is the only "
            "source of the section boundaries"
        ) from error
    if not pdf.is_file():
        raise InputError(f"PDF not found: {pdf}")
    try:
        document = fitz.open(str(pdf))
    except Exception as error:  # pragma: no cover - corrupt file
        raise InputError(f"cannot open {pdf}: {error}") from error
    with document:
        toc = document.get_toc()
    starts = [
        (title.strip(), page) for level, title, page in toc if level == 1 and page >= 1
    ]
    if not starts:
        raise InputError(
            f"{pdf} carries no level-1 outline entry; WeasyPrint emits "
            f"bookmarks for the book's headings, so a PDF without them was "
            f"not produced by tools/build_book.py"
        )
    return starts


def outline_sections(pdf: Path, page_count: int) -> list[str | None]:
    """The level-1 outline title in force on each page, 1-based, index 0 unused.

    Raises `InputError` when the PDF carries no outline: the boundaries are not
    guessable, and the docstring says why nothing is guessed.
    """
    starts: dict[int, str] = {}
    for title, page in outline_starts(pdf):
        if page <= page_count:
            starts.setdefault(page, title)
    if not starts:
        raise InputError(
            f"{pdf}: no level-1 outline entry falls inside its {page_count} pages"
        )
    sections: list[str | None] = [None] * (page_count + 1)
    current: str | None = None
    for page in range(1, page_count + 1):
        if page in starts:
            current = starts[page]
        sections[page] = current
    return sections


def excluded_pages(
    sections: list[str | None], exclude_prefixes: tuple[str, ...]
) -> set[int]:
    """The pages the index does not cover: front matter and the named sections."""
    page_count = len(sections) - 1
    first_chapter = next(
        (
            page
            for page in range(1, page_count + 1)
            if sections[page] and CHAPTER_TITLE_RE.match(sections[page] or "")
        ),
        None,
    )
    if first_chapter is None:
        raise InputError(
            "no level-1 outline entry looks like a numbered chapter "
            "('1. …'); the end of the front matter cannot be located"
        )
    excluded = set(range(1, first_chapter))
    for page in range(first_chapter, page_count + 1):
        title = sections[page] or ""
        if any(title.startswith(prefix) for prefix in exclude_prefixes):
            excluded.add(page)
    return excluded


def strip_furniture(pages: list[str], sections: list[str | None]) -> list[str]:
    """Each page without its running head and its folio. See the docstring."""
    out: list[str] = []
    for position, body in enumerate(pages):
        page = position + 1
        lines = body.splitlines()
        title = sections[page] if page < len(sections) else None
        head = next((i for i, line in enumerate(lines) if line.strip()), None)
        if head is not None and title and lines[head].strip() == title:
            lines[head] = ""
        tail = next(
            (i for i in range(len(lines) - 1, -1, -1) if lines[i].strip()), None
        )
        if tail is not None and lines[tail].strip() == str(page):
            lines[tail] = ""
        out.append("\n".join(lines))
    return out


# --- locating ---------------------------------------------------------------


def locate(
    entries: list[Entry], pages: list[str], excluded: set[int]
) -> IndexResult:
    """Every entry's pages, the cross-references, and what needs a human.

    `pages` is a list of page texts; page numbers are positions + 1. Taking the
    texts rather than a path is what lets the tests state a four-page book in
    four strings.
    """
    result = IndexResult(
        pages_scanned=len(pages) - len(excluded & set(range(1, len(pages) + 1))),
        pages_excluded=len(excluded & set(range(1, len(pages) + 1))),
    )
    known = {entry.term.lower() for entry in entries}
    for entry in sorted(entries, key=lambda e: e.sort_key):
        if entry.see is not None:
            result.cross_refs.append(entry)
            if entry.see.lower() not in known:
                result.review.append(
                    (entry, f"'see {entry.see}' names no entry of the term list")
                )
            continue
        patterns = [occurrence_pattern(s) for s in entry.spellings]
        found = [
            position + 1
            for position, body in enumerate(pages)
            if (position + 1) not in excluded
            and any(pattern.search(body) for pattern in patterns)
        ]
        if found:
            result.located.append((entry, found))
        else:
            result.review.append((entry, "found on no page the index covers"))
    # Two guards, on two different facts, because an index with no rows is not
    # a small index: it is a heading and a note that a reader would take for a
    # production defect.
    #
    # The first is about the term list. `meta/index_terms.md` ships as format
    # documentation with no entry in it, so this is the state of the repo
    # today and the first thing a `--with-index` build would hit.
    if not entries:
        result.fatal.append(
            "the term list carries no entry; there is nothing to index"
        )
        return result
    # The second is about the scan, so only entries that can be located count.
    # A cross-reference is evidence about the term list and never about the
    # PDF, so it must not be allowed to disarm this: a list aimed at the wrong
    # PDF locates nothing, and would otherwise ship one `see` row and no pages.
    locatable = [entry for entry in entries if not entry.see]
    if locatable and not result.located:
        result.fatal.append(
            f"all {len(locatable)} locatable entr(ies) were found on no page "
            f"the index covers; the term list and the PDF do not belong to "
            f"each other"
        )
    return result


def format_pages(numbers: list[int]) -> str:
    """`[12, 45, 46, 47]` -> `12, 45-47`. Runs of two or more are collapsed."""
    if not numbers:
        return ""
    runs: list[list[int]] = [[numbers[0]]]
    for number in numbers[1:]:
        if number == runs[-1][-1] + 1:
            runs[-1].append(number)
        else:
            runs.append([number])
    return ", ".join(
        str(run[0]) if len(run) == 1 else f"{run[0]}-{run[-1]}" for run in runs
    )


# --- rendering --------------------------------------------------------------


def render_markdown(result: IndexResult, *, title: str = INDEX_TITLE) -> str:
    """The Index section, as markdown. Alphabetical, cross-references in place."""
    rows: list[tuple[tuple[str, str], str]] = []
    # The printed term is the bare spelling: emphasis markers copied over from
    # the glossary would render as `****bold****` inside the bold of the row.
    for entry, numbers in result.located:
        term = bare_spelling(entry.term)
        rows.append((entry.sort_key, f"- **{term}** {format_pages(numbers)}"))
    for entry in result.cross_refs:
        term = bare_spelling(entry.term)
        rows.append(
            (entry.sort_key, f"- **{term}** *see* {bare_spelling(entry.see or '')}")
        )
    body = "\n".join(text for _, text in sorted(rows, key=lambda row: row[0]))
    return f"# {title}\n\n{INDEX_NOTE}\n\n{body}\n"


def report_lines(result: IndexResult) -> list[str]:
    lines = [
        f"index: {len(result.located)} entr(ies) with pages, "
        f"{len(result.cross_refs)} cross-reference(s), "
        f"{len(result.review)} for review; "
        f"{result.pages_scanned} page(s) scanned, "
        f"{result.pages_excluded} excluded"
    ]
    for message in result.fatal:
        lines.append(f"  {FATAL:<6} terms          {message}")
    for entry, why in result.review:
        lines.append(
            f"  {REVIEW:<6} entry          "
            f"index_terms:{entry.line:<5} {entry.term!r}: {why}"
        )
    lines.append(
        f"index: {result.verdict} ({len(result.fatal)} fatal, "
        f"{len(result.review)} review)"
    )
    return lines


def build_index(
    pdf: Path,
    terms_text: str,
    *,
    exclude_prefixes: tuple[str, ...] = DEFAULT_EXCLUDE_PREFIXES,
) -> IndexResult:
    """The whole scan: term list plus first-pass PDF -> located entries."""
    entries, errors = parse_terms(terms_text)
    if errors:
        result = IndexResult(fatal=errors)
        return result
    pages = page_texts(pdf)
    sections = outline_sections(pdf, len(pages))
    excluded = excluded_pages(sections, exclude_prefixes)
    stripped = strip_furniture(pages, sections)
    return locate(entries, stripped, excluded)


# --- CLI --------------------------------------------------------------------


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(__doc__ or "").split("\n\n")[0],
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--pdf",
        required=True,
        help="the PDF of the first build pass, the one without an index",
    )
    parser.add_argument(
        "--terms",
        default=str(ROOT / "meta" / "index_terms.md"),
        help="the term list (default: meta/index_terms.md)",
    )
    parser.add_argument("--out", help="write the Index section here (default: stdout)")
    parser.add_argument(
        "--exclude-prefix",
        action="append",
        metavar="PREFIX",
        help="a level-1 outline title prefix whose pages the index skips "
        f"(default: {', '.join(DEFAULT_EXCLUDE_PREFIXES)})",
    )
    parser.add_argument("--json", metavar="FILE", help="report as JSON ('-' for stdout)")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    prefixes = tuple(args.exclude_prefix) if args.exclude_prefix else DEFAULT_EXCLUDE_PREFIXES
    try:
        terms_text = Path(args.terms).read_text(encoding="utf-8")
    except OSError as error:
        print(f"[unusable] cannot read {args.terms}: {error}", file=sys.stderr)
        return 2
    try:
        result = build_index(Path(args.pdf), terms_text, exclude_prefixes=prefixes)
    except InputError as error:
        print(f"[unusable] {error}", file=sys.stderr)
        return 2

    for line in report_lines(result):
        print(line, file=sys.stderr)

    if result.fatal:
        return 1

    markdown = render_markdown(result)
    if args.out:
        Path(args.out).write_text(markdown, encoding="utf-8")
        print(f"[info] wrote {args.out}", file=sys.stderr)
    else:
        print(markdown)

    if args.json:
        payload = {
            "verdict": result.verdict,
            "pages_scanned": result.pages_scanned,
            "pages_excluded": result.pages_excluded,
            "entries": [
                {"term": entry.term, "pages": numbers, "line": entry.line}
                for entry, numbers in result.located
            ],
            "cross_references": [
                {"term": entry.term, "see": entry.see, "line": entry.line}
                for entry in result.cross_refs
            ],
            "review": [
                {"term": entry.term, "line": entry.line, "why": why}
                for entry, why in result.review
            ],
        }
        blob = json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True)
        if args.json == "-":
            print(blob)
        else:
            Path(args.json).write_text(blob + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
