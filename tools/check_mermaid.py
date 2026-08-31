"""Detect mermaid nodes hoisted out of their subgraph by a premature edge.

Mermaid creates a node at the point of first mention. If an edge names a node
before the `subgraph` block that declares it, the node is created at the root
graph and renders OUTSIDE the box. In a figure whose claim is which side of a
boundary a component sits on, that silently inverts the claim.

Reports, per mermaid block: nodes referenced by an edge at a line earlier than
the `subgraph` that contains their declaration.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

FENCE_OPEN = re.compile(r"^\s*```mermaid\s*$")
FENCE_CLOSE = re.compile(r"^\s*```\s*$")
SUBGRAPH_OPEN = re.compile(r"^\s*subgraph\s+(\S+)")
BLOCK_END = re.compile(r"^\s*end\s*$")
# Any mermaid link form: -->, ---, -.->, ==>, --text-->, etc.
EDGE = re.compile(r"(-{2,3}>|-{2,3}|-\.-+>|={2,}>)")
# A bare identifier, excluding mermaid keywords and quoted label text.
IDENT = re.compile(r"\b([A-Za-z_][A-Za-z0-9_]*)\b")

KEYWORDS = frozenset(
    {
        "graph", "flowchart", "subgraph", "end", "direction",
        "TB", "TD", "BT", "RL", "LR", "classDef", "class", "style",
        "linkStyle", "click", "note", "of",
    }
)


@dataclass(frozen=True)
class Finding:
    """One node created outside the subgraph that was meant to contain it."""

    node: str
    edge_line: int
    subgraph_line: int
    subgraph_name: str
    edge_text: str


def _strip_labels(line: str) -> str:
    """Remove bracketed/quoted label text so prose words are not read as IDs."""
    line = re.sub(r"\[[^\]]*\]", " ", line)
    line = re.sub(r"\([^)]*\)", " ", line)
    line = re.sub(r"\{[^}]*\}", " ", line)
    line = re.sub(r"\|[^|]*\|", " ", line)
    line = re.sub(r'"[^"]*"', " ", line)
    return line


def _identifiers(line: str) -> list[str]:
    return [m for m in IDENT.findall(_strip_labels(line)) if m not in KEYWORDS]


def scan_block(lines: list[tuple[int, str]]) -> list[Finding]:
    """lines: (absolute_line_number, text) for one mermaid block."""
    # Pass 1: map each subgraph region and the nodes declared inside it.
    owner: dict[str, tuple[int, str]] = {}  # node -> (subgraph line, name)
    depth = 0
    stack: list[tuple[int, str]] = []
    inside: set[int] = set()  # absolute line numbers inside any subgraph

    for lineno, text in lines:
        opened = SUBGRAPH_OPEN.match(text)
        if opened:
            depth += 1
            stack.append((lineno, opened.group(1)))
            continue
        if BLOCK_END.match(text) and depth > 0:
            depth -= 1
            if stack:
                stack.pop()
            continue
        if depth > 0:
            inside.add(lineno)
            if stack:
                for ident in _identifiers(text):
                    owner.setdefault(ident, stack[-1])

    # Pass 2: edges at root level that name an owned node too early.
    findings: list[Finding] = []
    for lineno, text in lines:
        if lineno in inside or not EDGE.search(text):
            continue
        for ident in _identifiers(text):
            if ident not in owner:
                continue
            sub_line, sub_name = owner[ident]
            if lineno < sub_line:
                findings.append(
                    Finding(ident, lineno, sub_line, sub_name, text.strip())
                )
    return findings


def scan_file(path: Path) -> list[Finding]:
    findings: list[Finding] = []
    block: list[tuple[int, str]] = []
    in_block = False

    for lineno, text in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not in_block:
            if FENCE_OPEN.match(text):
                in_block, block = True, []
            continue
        if FENCE_CLOSE.match(text):
            findings.extend(scan_block(block))
            in_block = False
            continue
        block.append((lineno, text))

    if in_block:
        print(f"  [warn] unterminated mermaid block in {path.name}", file=sys.stderr)
    return findings


def main(argv: list[str]) -> int:
    paths = [Path(a) for a in argv[1:]]
    if not paths:
        print("usage: mermaid_containment.py <file.md> [...]", file=sys.stderr)
        return 2

    total = 0
    for path in sorted(paths):
        if not path.is_file():
            print(f"[skip] {path} — not a file", file=sys.stderr)
            continue
        findings = scan_file(path)
        if not findings:
            print(f"[ok]   {path.name}")
            continue
        total += len(findings)
        print(f"[FAIL] {path.name}: {len(findings)} hoisted node(s)")
        for f in findings:
            print(
                f"       '{f.node}' used at line {f.edge_line} but declared in "
                f"subgraph '{f.subgraph_name}' opening at line {f.subgraph_line}"
            )
            print(f"         edge: {f.edge_text}")
    return 1 if total else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
