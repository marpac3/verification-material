"""Figure and table apparatus: numbering, captions, symbolic cross-references.

A monograph numbers every float, captions it, and refers to it by number. This
module supplies that apparatus without letting a number be written by hand
anywhere, because a hand-written float number is a claim that silently falsifies
the moment a float is inserted above it.

Authoring syntax, in the chapter markdown
-----------------------------------------
Figure caption — on its own line, immediately BELOW the figure (mermaid block or
image), which is where a monograph puts it:

    {figure: driver_split} The layered environment of the DMA testbench.

Table caption — on its own line, immediately ABOVE the table, which is where a
monograph puts a table caption:

    {table: exclusion_kinds} Exclusion kinds, their owners and their expiry.

Cross-reference — inline, anywhere, including before the caption itself:

    ... the split shown in {ref: driver_split} ...

The label is symbolic and arbitrary; the number is assigned at build time in
document order, per chapter, with separate counters for figures and tables.
Chapter 4's third figure is "Figure 4.3"; appendix B's first table is "Table B.1".

What this module refuses to do
------------------------------
It fails the build on a duplicate label and on a reference to a label that does
not exist, because both would otherwise ship as a plausible-looking number.
It reports — as warnings, not errors — floats with no caption, so a pass can
find them without the build becoming unusable while that pass is under way.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

import book_meta

FENCE_RE = re.compile(r"^[ \t]*(```|~~~)")

CAPTION_RE = re.compile(r"^\{(figure|table):\s*([A-Za-z0-9_-]+)\}\s*(.*)$")
REF_RE = re.compile(r"\{ref:\s*([A-Za-z0-9_-]+)\}")

# A markdown table row is the cheapest reliable tell: a line starting with "|".
TABLE_ROW_RE = re.compile(r"^[ \t]*\|")

# By the time this module runs, the build has already replaced every ```mermaid
# fence with a placeholder figure (see mermaid.extract), so that — not the fence
# — is what a diagram looks like here. Both forms are recognised, because the
# module is also used directly on raw chapter text by the checker.
DIAGRAM_RE = re.compile(r'<figure class="diagram">@@MERMAID:')

FIGURE_WORD = "Figure"
TABLE_WORD = "Table"


@dataclass(frozen=True)
class Float:
    kind: str          # "figure" | "table"
    label: str
    number: str        # "4.3" or "B.1"
    caption: str
    anchor: str
    line: int


@dataclass
class FloatResult:
    text: str
    floats: list[Float] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


def chapter_prefix(chapter_id: str) -> str:
    """'ch04' -> '4'; 'appendix_b' -> 'B'."""
    if book_meta.is_appendix(chapter_id):
        return chapter_id.rsplit("_", 1)[-1].upper()
    digits = chapter_id.lstrip("ch").lstrip("0") or "0"
    return digits


def _uncaptioned_floats(lines: list[str], captioned: set[int]) -> list[str]:
    """Report mermaid blocks and tables that no caption line accompanies.

    A figure's caption is the first non-blank line after its closing fence; a
    table's is the first non-blank line above its first row. `captioned` holds
    the indices of lines that were recognised as captions, so this only has to
    decide whether the neighbour of each float is one of them.
    """
    notes: list[str] = []
    in_fence = False
    fence_is_figure = False
    index = 0
    while index < len(lines):
        line = lines[index]
        if FENCE_RE.match(line):
            if not in_fence:
                in_fence = True
                fence_is_figure = "mermaid" in line.lower()
            else:
                in_fence = False
                if fence_is_figure:
                    probe = index + 1
                    while probe < len(lines) and not lines[probe].strip():
                        probe += 1
                    if probe not in captioned:
                        notes.append(f"line {index + 1}: mermaid figure has no {{figure: …}} caption")
            index += 1
            continue
        if in_fence:
            index += 1
            continue
        if DIAGRAM_RE.search(line):
            probe = index + 1
            while probe < len(lines) and not lines[probe].strip():
                probe += 1
            if probe not in captioned:
                # `mermaid.extract` replaces a ```mermaid fence with a padded
                # region whose first line is blank, so the <figure> placeholder
                # always sits one line below the fence opener. Report the fence
                # itself: that is what a reader greps for, and the caption goes
                # on the line after the *closing* fence.
                notes.append(
                    f"line {index}: diagram has no {{figure: …}} caption "
                    "(caption goes below the closing fence)"
                )
            index += 1
            continue
        if TABLE_ROW_RE.match(line):
            probe = index - 1
            while probe >= 0 and not lines[probe].strip():
                probe -= 1
            if probe not in captioned:
                notes.append(f"line {index + 1}: table has no {{table: …}} caption")
            while index < len(lines) and TABLE_ROW_RE.match(lines[index]):
                index += 1
            continue
        index += 1
    return notes


def process(text: str, chapter_id: str) -> FloatResult:
    """Assign numbers, rewrite captions to markdown, resolve {ref: …}."""
    lines = text.split("\n")
    prefix = chapter_prefix(chapter_id)
    counters = {"figure": 0, "table": 0}
    floats: dict[str, Float] = {}
    caption_lines: set[int] = set()
    errors: list[str] = []

    # Pass 1 — collect, in document order, so numbers follow the page and a
    # forward reference still resolves.
    in_fence = False
    for index, line in enumerate(lines):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = CAPTION_RE.match(line)
        if not match:
            continue
        kind, label, caption = match.group(1), match.group(2), match.group(3).strip()
        caption_lines.add(index)
        if label in floats:
            errors.append(
                f"duplicate float label {label!r} at line {index + 1} "
                f"(first used at line {floats[label].line})"
            )
            continue
        if not caption:
            errors.append(f"line {index + 1}: float {label!r} has an empty caption")
        counters[kind] += 1
        floats[label] = Float(
            kind=kind,
            label=label,
            number=f"{prefix}.{counters[kind]}",
            caption=caption,
            anchor=f"{chapter_id}-{'fig' if kind == 'figure' else 'tab'}-{label}",
            line=index + 1,
        )

    # Pass 2 — rewrite caption lines into captioned paragraphs carrying an id.
    out: list[str] = []
    in_fence = False
    for index, line in enumerate(lines):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence or index not in caption_lines:
            out.append(line)
            continue
        match = CAPTION_RE.match(line)
        assert match is not None
        item = floats.get(match.group(2))
        if item is None:  # duplicate label: already reported, drop the marker
            out.append(match.group(3).strip())
            continue
        word = FIGURE_WORD if item.kind == "figure" else TABLE_WORD
        css = "float-caption" + ("" if item.kind == "figure" else " caption-above")
        # Python-Markdown applies a block-level attribute list only when it sits
        # on a line of its own; appended to the paragraph's last line it is
        # emitted as literal text, which is how this was first written.
        out.append(f"**{word} {item.number}** — {item.caption}")
        out.append(f"{{: #{item.anchor} .{css.replace(' ', ' .')} }}")
    text = "\n".join(out)

    # Pass 3 — resolve references, including inside blockquotes; skip fences.
    def resolve_line(line: str) -> str:
        def one(match: re.Match[str]) -> str:
            label = match.group(1)
            item = floats.get(label)
            if item is None:
                errors.append(f"reference to unknown float label {label!r}")
                return match.group(0)
            word = FIGURE_WORD if item.kind == "figure" else TABLE_WORD
            return f"[{word} {item.number}](#{item.anchor})"

        return REF_RE.sub(one, line)

    resolved: list[str] = []
    in_fence = False
    for line in text.split("\n"):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            resolved.append(line)
            continue
        resolved.append(line if in_fence else resolve_line(line))

    warnings = _uncaptioned_floats(lines, caption_lines)
    return FloatResult(
        text="\n".join(resolved),
        floats=sorted(floats.values(), key=lambda f: (f.kind, f.number)),
        warnings=[f"{chapter_id}: {w}" for w in warnings],
        errors=[f"{chapter_id}: {e}" for e in errors],
    )
