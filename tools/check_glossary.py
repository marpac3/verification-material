#!/usr/bin/env python3
"""The glossary gate: Appendix A must be a table a reader can trust.

    python3 tools/check_glossary.py                       # meta/glossary.md
    python3 tools/check_glossary.py --min-rows 200         # the W3 transition
    python3 tools/check_glossary.py --json -               # machine-readable
    python3 tools/check_glossary.py --no-gate              # report, always exit 0

`tools/build_book.py` (`render_glossary`) takes the first pipe-delimited block
of `meta/glossary.md` and ships it as Appendix A. It does not read the table: a
term entered twice, a row with a cell missing, an `Introduced` column naming a
chapter that does not exist — all three render, and all three are visible only
to the reader who goes looking. This gate reads it, and it is the gate of
`meta/passes/pass_h_didactic_apparatus.md` §5.7 («unique terms, four columns
filled, ≥ 300 rows, "Introduced" names an existing chapter»).

Severities
----------
`FATAL` fails the gate (exit 1). Five defects earn it:

* **duplicate** — a term repeated, compared without case. Two rows for the same
  word is not a richer glossary, it is two definitions the reader must choose
  between with nothing to choose on.
* **cells** — a row whose cell count differs from the header's. Markdown renders
  such a row by silently dropping or padding, so the defect reaches the page as
  a shifted column rather than as an error.
* **introduced** — a value that is not `chNN` naming an existing `book/chNN.md`.
  A glossary whose provenance column points at nothing has stopped being a
  cross-reference.
* **italian-empty** — the Italian column exists and a cell of it is empty. The
  column is the preparation of the translation (`meta/IMPROVEMENT_PLAN.md` §W3),
  and a half-filled column is worse than an absent one: it looks done.
* **min-rows** — fewer than `MIN_ROWS` rows. The threshold is the pass's exit
  criterion, not a property of the table, which is why it is a constant here and
  overridable on the command line: during W3 the coordinator runs
  `--min-rows 200` on a glossary that is still growing.

`REVIEW` is printed and counted and does not fail the gate. One defect earns it:

* **subject** — the term's head (the text before the first « (», so
  `DUT (design under test)` is looked up as `DUT`) does not occur as a whole
  word in any chapter its `Introduced` column names. This cannot be FATAL. Many
  entries are labels the book coins for a contrast it draws without ever writing
  the label as a phrase — `operational vs observational communication` (ch08),
  `front-door vs back-door access` (ch10) — and those are the entries a glossary
  exists for. A human reads the list and decides whether the chapter really owns
  the term.

The three columns of today, the four of tomorrow
-----------------------------------------------
The header is the authority on the shape of the table. With three columns there
is no Italian column and no Italian check; with four, the fourth is looked up by
name (`Italian`, or `ITA`) and every cell of it must be filled. The distinction
between «no Italian column» and «an Italian cell is empty» is the point: the
first is the state of the file before `G3` adds the column, the second is a
defect. The summary line always says which shape it read, so a run that found
three columns cannot be mistaken for a run that found four full ones.

`Introduced` is looked up by name too, so a four-column header that puts
Italian third and `Introduced` last reads correctly. A header that names
neither falls back to the third column, the position `Introduced` holds today.

`Introduced` and the one row that made it a list
------------------------------------------------
§5.7 says the column «names an existing chapter», and 219 of the 220 rows of
2026-09-08 name exactly one. One row — `irritator` — names two, `ch07, ch20`.
A comma-separated list of `chNN`, every one of which must exist, is therefore
admitted, and the subject check is satisfied by an occurrence in any of them.
This is a widening of §5.7 and the coordinator can reverse it: drop
`INTRODUCED_LIST` from `parse_introduced` and the single value regex is the
whole rule again.

What this gate does not check
-----------------------------
Alphabetical order. The file of 2026-09-08 is in the order the book introduces
its terms (its own preamble says so, and Appendix A prints that preamble), and
the alphabetical ordering W3 asks for is applied by the coordinator's own script
when the Italian column lands. A gate that failed on order today would fail on
the released file for a reason that is not a defect.

Exit codes
----------
0   no FATAL (REVIEW findings may have been printed), or `--no-gate`.
1   at least one FATAL.
2   the gate could not run: a glossary file it could not read, no table in it, a
    malformed `--min-rows`. A gate that did not run must not report PASS.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

FATAL = "FATAL"
REVIEW = "REVIEW"
PASS = "PASS"

# The pass's exit criterion (§5.7, «≥ 300 rows»), not a property of the file.
MIN_ROWS = 300

CHAPTER_RE = re.compile(r"^ch\d\d$")
# `Introduced` may name more than one chapter; see the docstring.
INTRODUCED_LIST = re.compile(r"\s*,\s*")

# Header names that mean «the Italian translation of the term». Matched without
# case and without surrounding punctuation, so `| Italian |` and `| ITA |` and
# `| Italian (draft) |` all name the column.
ITALIAN_NAMES = ("italian", "ita", "italiano", "traduzione")
INTRODUCED_NAMES = ("introduced",)
# A pipe that is not escaped, so `\\|` inside a cell is not a cell border.
UNESCAPED_PIPE = re.compile(r"(?<!\\)\|")
INTRODUCED_FALLBACK = 2

# Emphasis markers to drop from a term before looking it up in a chapter. `_` is
# deliberately absent: `ignore_bins vs illegal_bins` is an identifier, and
# stripping underscores as markdown emphasis turned it into `ignorebins`, a
# string that occurs in no chapter of any book.
EMPHASIS_RE = re.compile(r"[*`]")


class InputError(RuntimeError):
    """Something that makes the verdict unearnable -> exit 2."""


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    line: int | None
    message: str

    def render(self) -> str:
        where = f"glossary:{self.line}" if self.line else "glossary"
        return f"{self.severity:<6} {self.code:<14} {where:<16} {self.message}"

    def as_dict(self) -> dict:
        return {
            "severity": self.severity,
            "code": self.code,
            "line": self.line,
            "message": self.message,
        }


@dataclass(frozen=True)
class Row:
    line: int
    cells: tuple[str, ...]


@dataclass
class Table:
    header: tuple[str, ...]
    header_line: int
    separator: Row
    rows: list[Row]

    def _column(self, names: tuple[str, ...]) -> int | None:
        """Index of the first header cell whose bare name is in `names`."""
        for index, name in enumerate(self.header):
            bare = EMPHASIS_RE.sub("", name).strip().lower()
            bare = bare.split("(")[0].strip()
            if bare in names:
                return index
        return None

    @property
    def italian_column(self) -> int | None:
        """Index of the Italian column, or None when the table has none."""
        return self._column(ITALIAN_NAMES)

    @property
    def introduced_column(self) -> int:
        """Index of the `Introduced` column.

        Read by name, like the Italian one, because `G3` is reshaping this
        table and a four-column header may well put Italian third. A header
        that does not name the column at all falls back to the position it
        holds today, which is what the whole gate assumed before.
        """
        found = self._column(INTRODUCED_NAMES)
        return INTRODUCED_FALLBACK if found is None else found


# --- parsing ----------------------------------------------------------------


def split_cells(line: str) -> tuple[str, ...]:
    """The cells of a markdown table row.

    Exactly one border pipe is removed per side, and the split is on unescaped
    pipes. Both matter, and `.strip("|")` on a bare split gets both wrong:

    * `.strip()` removes a *run*, so `| a | b ||` reads as two cells where the
      row has three (a trailing empty one) and `|| a | b |` reads as two where
      the renderer sees four. A row whose columns are shifted by one is exactly
      what the `cells` finding exists to catch, and it passed silently.
    * a `|` inside a cell is written `\\|`, and splitting on the bare character
      would report a spurious `cells` defect for a row that renders correctly.

    A pipe inside a backtick span is still split on, as the renderer may not:
    the glossary of 2026-09-08 has none, and one would show up as a `cells`
    finding for a human to read rather than as a silent miscount.
    """
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|") and not body.endswith("\\|"):
        body = body[:-1]
    return tuple(cell.strip() for cell in UNESCAPED_PIPE.split(body))


def parse_table(text: str) -> Table:
    """The first pipe-delimited block of the file, as `render_glossary` reads it.

    `build_book.render_glossary` starts at the first line whose first non-blank
    character is `|` and hands everything from there to the markdown converter.
    This finds the same first line, so a defect this gate reports is a defect in
    the block that ships, and stops at the first line that is not a table row —
    prose after the table is not the gate's business.
    """
    lines = text.splitlines()
    start = next(
        (i for i, line in enumerate(lines) if line.lstrip().startswith("|")), None
    )
    if start is None:
        raise InputError("no table found: no line begins with '|'")
    block: list[Row] = []
    for offset, line in enumerate(lines[start:], start=start):
        if not line.lstrip().startswith("|"):
            break
        block.append(Row(line=offset + 1, cells=split_cells(line)))
    if len(block) < 2:
        raise InputError(
            f"the table at line {start + 1} has a header and no separator row"
        )
    header, separator = block[0], block[1]
    if not all(set(cell) <= set("-: ") and "-" in cell for cell in separator.cells):
        raise InputError(
            f"glossary:{separator.line}: expected a markdown separator row "
            f"(|---|---|…), got {separator.cells}"
        )
    # `render_glossary` joins everything from `start` to EOF, so anything
    # pipe-delimited after this block ships as Appendix A unchecked. Refuse to
    # give a verdict on a file the gate and the builder would read differently.
    tail = [
        offset + 1
        for offset, line in enumerate(lines[start + len(block) :], start=start + len(block))
        if line.lstrip().startswith("|")
    ]
    if tail:
        raise InputError(
            f"glossary:{tail[0]}: a second pipe-delimited block follows the "
            f"table; the builder ships everything to the end of the file, so "
            f"this gate would check less than what ships"
        )
    return Table(
        header=header.cells,
        header_line=header.line,
        separator=separator,
        rows=block[2:],
    )


def parse_introduced(value: str) -> list[str]:
    """The chapter stems an `Introduced` cell names, or [] if it names none."""
    stems = [part for part in INTRODUCED_LIST.split(value.strip()) if part]
    if not stems or not all(CHAPTER_RE.match(stem) for stem in stems):
        return []
    return stems


def term_head(term: str) -> str:
    """The part of a term looked up in a chapter: the text before the first « (».

    `DUT (design under test)` is looked up as `DUT`, because that is the string
    the chapter writes. The parenthesis must be preceded by a space, so
    `(test, seed) matrix` — an entry that opens with one — keeps its head whole.
    """
    bare = EMPHASIS_RE.sub("", term).strip()
    return bare.split(" (")[0].strip()


def occurrence_pattern(head: str) -> re.Pattern[str]:
    """`head` as a whole word, without case, tolerating a plural on the last word.

    The tolerance is not laxity: a chapter that writes «equivalence classes» has
    written the term, and refusing the inflection put ten entries of the real
    glossary on the REVIEW list for a reason no human would uphold. Internal
    whitespace matches any run of whitespace, so a term broken across a line of
    the markdown source still matches.
    """
    escaped = re.escape(head)
    escaped = re.sub(r"(?:\\[ ])+", r"\\s+", escaped)
    pattern = escaped + r"(?:e?s)?" if head[-1:].isalnum() else escaped
    prefix = r"\b" if head[:1].isalnum() else ""
    suffix = r"\b" if head[-1:].isalnum() else ""
    return re.compile(prefix + pattern + suffix, re.IGNORECASE)


# --- the checks -------------------------------------------------------------


def check_table(
    table: Table,
    chapter_text: dict[str, str],
    *,
    min_rows: int,
    glossary_name: str,
) -> list[Finding]:
    """Every finding of the gate, in the order a reader of the ledger wants them.

    `chapter_text` maps a stem to the chapter's source, or omits the stem when
    `book/<stem>.md` does not exist; that is how a bad `Introduced` value is
    told from a term the chapter never writes.
    """
    findings: list[Finding] = []
    width = len(table.header)

    if len(table.separator.cells) != width:
        findings.append(
            Finding(
                FATAL,
                "cells",
                table.separator.line,
                f"separator row has {len(table.separator.cells)} cell(s), "
                f"header has {width}",
            )
        )

    if len(table.rows) < min_rows:
        findings.append(
            Finding(
                FATAL,
                "min-rows",
                None,
                f"{len(table.rows)} row(s) in {glossary_name}, {min_rows} required",
            )
        )

    italian = table.italian_column
    # A fourth column called anything else — `Traduzione` is the obvious one —
    # would leave `italian` None and the emptiness check unarmed, and the gate
    # would report §5.7 met without having tested it. `release.py` prints a
    # gate's output only when it fails, so the summary line saying «no Italian
    # column» would not be read either. Refuse to be silent about it.
    if italian is None and width > 3:
        findings.append(
            Finding(
                FATAL,
                "italian-column",
                table.header_line,
                f"{width} columns but none named {' / '.join(ITALIAN_NAMES)}: "
                f"{list(table.header)}; the Italian check cannot run",
            )
        )
    seen: dict[str, Row] = {}

    for row in table.rows:
        if len(row.cells) != width:
            findings.append(
                Finding(
                    FATAL,
                    "cells",
                    row.line,
                    f"{len(row.cells)} cell(s), header has {width}: "
                    f"{row.cells[0][:48]!r}",
                )
            )
            # Every check below indexes into the row by column, and a row of the
            # wrong width would have them report the wrong cell.
            continue

        term = row.cells[0]
        key = EMPHASIS_RE.sub("", term).strip().lower()
        if key in seen:
            findings.append(
                Finding(
                    FATAL,
                    "duplicate",
                    row.line,
                    f"{term!r} already defined at line {seen[key].line}",
                )
            )
        else:
            seen[key] = row

        if italian is not None and not row.cells[italian].strip():
            findings.append(
                Finding(
                    FATAL,
                    "italian-empty",
                    row.line,
                    f"{term!r}: the {table.header[italian]!r} cell is empty",
                )
            )

        introduced_col = table.introduced_column
        introduced = (
            row.cells[introduced_col] if width > introduced_col else ""
        )
        stems = parse_introduced(introduced)
        if not stems:
            findings.append(
                Finding(
                    FATAL,
                    "introduced",
                    row.line,
                    f"{term!r}: Introduced is {introduced!r}, expected chNN "
                    f"(or a comma-separated list of chNN)",
                )
            )
            continue
        absent = [stem for stem in stems if stem not in chapter_text]
        if absent:
            findings.append(
                Finding(
                    FATAL,
                    "introduced",
                    row.line,
                    f"{term!r}: Introduced names {', '.join(absent)}, "
                    f"and no such file exists under the book directory",
                )
            )
            continue

        head = term_head(term)
        if not head:
            findings.append(
                Finding(
                    FATAL,
                    "cells",
                    row.line,
                    "the Term cell is empty",
                )
            )
            continue
        pattern = occurrence_pattern(head)
        if not any(pattern.search(chapter_text[stem]) for stem in stems):
            findings.append(
                Finding(
                    REVIEW,
                    "subject",
                    row.line,
                    f"{head!r} does not occur as a whole word in "
                    f"{', '.join(stems)}",
                )
            )

    return findings


# --- CLI --------------------------------------------------------------------


def load_chapters(book_dir: Path) -> dict[str, str]:
    """Every `book/chNN.md` there is, by stem.

    Read once and kept, because the subject check looks up 300 terms in 26
    chapters and re-reading a chapter per term made the gate take longer than
    the build it guards.
    """
    if not book_dir.is_dir():
        raise InputError(f"book directory not found: {book_dir}")
    text: dict[str, str] = {}
    for path in sorted(book_dir.glob("ch*.md")):
        if CHAPTER_RE.match(path.stem):
            try:
                text[path.stem] = path.read_text(encoding="utf-8")
            except OSError as error:
                raise InputError(f"cannot read {path}: {error}") from error
    if not text:
        raise InputError(f"no chNN.md files under {book_dir}")
    return text


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(__doc__ or "").split("\n\n")[0],
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--glossary",
        default=str(ROOT / "meta" / "glossary.md"),
        help="the glossary table (default: meta/glossary.md)",
    )
    parser.add_argument(
        "--book",
        default=str(ROOT / "book"),
        help="directory of chNN.md files, for the Introduced column",
    )
    parser.add_argument(
        "--min-rows",
        type=int,
        default=MIN_ROWS,
        metavar="N",
        help=f"rows required (default {MIN_ROWS}, the §5.7 exit criterion; the "
        f"W3 transition runs --min-rows 200)",
    )
    parser.add_argument("--json", metavar="FILE", help="write the report as JSON ('-' for stdout)")
    parser.add_argument(
        "--no-gate", action="store_true", help="report only; always exit 0"
    )
    return parser


def run(args: argparse.Namespace) -> tuple[Table, list[Finding]]:
    if args.min_rows < 0:
        raise InputError(f"--min-rows must not be negative, got {args.min_rows}")
    path = Path(args.glossary)
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as error:
        raise InputError(f"cannot read {path}: {error}") from error
    table = parse_table(text)
    chapters = load_chapters(Path(args.book))
    findings = check_table(
        table,
        chapters,
        min_rows=args.min_rows,
        glossary_name=path.name,
    )
    return table, findings


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        table, findings = run(args)
    except InputError as error:
        print(f"[unusable] {error}", file=sys.stderr)
        return 2

    fatal = [f for f in findings if f.severity == FATAL]
    review = [f for f in findings if f.severity == REVIEW]
    verdict = FATAL if fatal else (REVIEW if review else PASS)

    italian = table.italian_column
    shape = (
        f"{len(table.header)} columns, Italian column {table.header[italian]!r}"
        if italian is not None
        else f"{len(table.header)} columns, no Italian column"
    )
    print(f"glossary: {len(table.rows)} rows, {shape}")
    # REVIEW first, FATAL last, so the findings that fail the gate sit directly
    # above the verdict. `tools/release.py` reports a failing gate by printing
    # the *tail* of its output, and with the natural order — the row-count FATAL
    # first, then two dozen review lines — the release said the glossary had
    # failed and showed only the findings that had not failed it.
    order = {REVIEW: 0, FATAL: 1}
    for finding in sorted(findings, key=lambda f: (order[f.severity], f.line or 0)):
        print(f"  {finding.render()}")
    print(f"glossary: {verdict} ({len(fatal)} fatal, {len(review)} review)")

    code = 1 if fatal else 0
    if args.json:
        payload = {
            "exit": code,
            "rows": len(table.rows),
            "header": list(table.header),
            "italian_column": italian,
            "min_rows": args.min_rows,
            "verdict": verdict,
            "findings": [f.as_dict() for f in findings],
        }
        blob = json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True)
        if args.json == "-":
            print(blob)
        else:
            Path(args.json).write_text(blob + "\n", encoding="utf-8")
    return 0 if args.no_gate else code


if __name__ == "__main__":
    raise SystemExit(main())
