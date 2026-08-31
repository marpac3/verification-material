#!/usr/bin/env python3
"""Report paragraphs carrying more than one marker for the same source.

Why this exists as a tool rather than a habit
---------------------------------------------
The density rule was checked ad hoc, by a fresh throwaway script, on every
chapter.  Two of those scripts were wrong in the same way: they split the text
on blank lines only, so a bulleted list became one "paragraph" and every list
with a marker per bullet was reported as a dense run-on.  One writer noticed and
re-ran by hand; the others may not have.  A gate reimplemented per chapter is
not a gate, so it is written down once here.

What a hit means
----------------
NOT a violation.  The rule targets *redundancy*, and two markers to one source
in one unit are correct when they carry two claims the source treats separately
-- the style guide's surviving-marker test.  This tool narrows a chapter to the
handful of places where that test must be applied by a human; it cannot apply
it.  Reporting "0 candidates" is meaningful; reporting "3 candidates" is a
reading list, not a verdict.

Claim units
-----------
A list item is its own claim by construction, so each counts separately -- that
is the bug the ad hoc scripts had.  Table rows likewise.  Fenced code and its
blockquoted form are skipped: markers do not appear there, and brackets in code
would produce noise.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

MARKER = re.compile(r"\[cit:([^\]]+)\]")
FENCE = re.compile(r"^\s*(?:>\s*)?```")
LIST_ITEM = re.compile(r"^\s*(?:[-*+]\s|\d+[.)]\s)")
TABLE_ROW = re.compile(r"^\s*\|")
HEADING = re.compile(r"^\s*#")


@dataclass(frozen=True)
class Unit:
    """One claim unit: a prose paragraph, a list item, or a table row."""

    start_line: int
    kind: str
    text: str


@dataclass(frozen=True)
class Candidate:
    unit: Unit
    source: str
    count: int


def split_units(lines: tuple[str, ...]) -> tuple[Unit, ...]:
    """Split markdown into claim units, skipping fenced code."""
    units: list[Unit] = []
    buffer: list[str] = []
    buffer_start = 0
    in_fence = False

    def flush() -> None:
        if buffer:
            units.append(Unit(buffer_start, "paragraph", " ".join(buffer)))
        buffer.clear()

    for number, raw in enumerate(lines, 1):
        line = raw.rstrip("\n")
        stripped = line.strip().lstrip("> ").strip()

        if FENCE.match(line):
            flush()
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        if not stripped or HEADING.match(stripped):
            flush()
            continue

        # A list item or table row ends the previous unit and is its own.
        if LIST_ITEM.match(stripped) or TABLE_ROW.match(stripped):
            flush()
            kind = "list item" if LIST_ITEM.match(stripped) else "table row"
            units.append(Unit(number, kind, stripped))
            continue

        if not buffer:
            buffer_start = number
        buffer.append(stripped)

    flush()
    return tuple(units)


def sources_in(text: str) -> tuple[str, ...]:
    """Every source ID cited in the text, including multi-ID markers."""
    return tuple(
        part.strip()
        for marker in MARKER.findall(text)
        for part in marker.split(",")
        if part.strip()
    )


def candidates_in(units: tuple[Unit, ...]) -> tuple[Candidate, ...]:
    found: list[Candidate] = []
    for unit in units:
        for source, count in Counter(sources_in(unit.text)).items():
            if count > 1:
                found.append(Candidate(unit, source, count))
    return tuple(found)


def check(path: Path) -> tuple[Candidate, ...]:
    lines = tuple(path.read_text(encoding="utf-8").splitlines(keepends=True))
    return candidates_in(split_units(lines))


def excerpt(text: str, source: str, width: int = 96) -> str:
    """The text around the first marker for this source, for eyeballing."""
    hit = re.search(rf"\[cit:[^\]]*\b{re.escape(source)}\b[^\]]*\]", text)
    if hit is None:
        return text[:width]
    start = max(0, hit.start() - width // 2)
    return ("…" if start else "") + text[start : start + width] + "…"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()

    total = 0
    for path in args.paths:
        if not path.is_file():
            print(f"[err ] {path}: not a file", file=sys.stderr)
            return 2
        found = check(path)
        total += len(found)
        if not found:
            print(f"[ok  ] {path.name}: 0 density candidates")
            continue
        print(f"[chk ] {path.name}: {len(found)} candidate(s) — apply the "
              f"surviving-marker test to each; two claims one source treats "
              f"separately are CORRECT")
        for candidate in found:
            print(
                f"       {path.name}:{candidate.unit.start_line} "
                f"({candidate.unit.kind}) {candidate.source}×{candidate.count}"
            )
            print(f"         {excerpt(candidate.unit.text, candidate.source)}")

    return 0 if total == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
