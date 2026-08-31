#!/usr/bin/env python3
"""Variety check: count non-backbone example IPs per chapter.

Why this exists
---------------
Every other mechanical check in this pipeline is a CORRECTNESS check -- banned
names, [UNVERIFIED] claims, citation IDs, marker density, slang, mermaid.  None
of them can see the author's first requirement: that each chapter grounds its
concepts in 2-3 IPs beyond the reference SoC backbone.

A chapter that drifts back to backbone-only passes every existing check.  That
is not hypothetical: ch08's video-codec example was cut to a bare cross-reference
during a length-compression pass and nothing flagged it.

What this can and cannot decide
-------------------------------
It counts mentions and weighs them by their surroundings.  It CANNOT reliably
distinguish a substantive worked example from a passing mention -- that judgment
stays human (or reviewer-agent).  What it does is surface the two shapes that
precede a real regression:

  * a chapter below the distinct-IP floor, and
  * an IP mentioned so thinly it has probably decayed into a cross-reference.

Treat a WARN as "go look", never as "fix the count".  Padding a chapter with the
name of an IP to clear this check defeats its whole purpose.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

# Extended cast, from meta/example_bank.md.  Each entry maps a canonical name to
# the regex alternatives chapters actually use in prose.
EXTENDED_CAST: dict[str, str] = {
    "GPU": r"\bGPU\b|\bshader\b",
    "video codec": r"video codec|H\.265|\bcodec\b",
    # Deliberately NOT matching bare "MAC": the reference SoC's canonical
    # "16-lane MAC datapath" (multiply-accumulate) is not an Ethernet MAC, and
    # matching it made every chapter quoting the bank inherit a phantom hit.
    "Ethernet MAC": r"Ethernet|\bTSN\b",
    "crypto engine": r"crypto engine|AES-GCM|\bAES\b|key ladder|key slot",
    "HBM controller": r"\bHBM\b",
    "coherent hub": r"coherent hub|\bMESI\b|directory-based",
    "USB controller": r"\bUSB\b",
    "flash controller": r"flash controller|\bNAND\b|\bLDPC\b",
    "sensor hub": r"sensor hub|sensor-fusion",
    "radar front-end": r"\bradar\b|\bCFAR\b|\bFMCW\b",
}

# A mention inside one of these is structural weight, not colour: the IP is
# carrying a worked example rather than being named in passing.
SUBSTANTIVE_CONTEXT = (
    re.compile(r"^>\s", re.M),            # scenario blockquote
    re.compile(r"^```", re.M),            # code artifact
    re.compile(r"^\|", re.M),             # table row
)

DISTINCT_IP_FLOOR = 3      # style guide asks 2-3; 3 keeps a margin above the ask
THIN_MENTION_MAX = 1       # a single mention in a whole chapter smells like a stub


@dataclass(frozen=True)
class IPUsage:
    name: str
    mentions: int
    substantive_hits: int

    @property
    def looks_thin(self) -> bool:
        return self.mentions <= THIN_MENTION_MAX and self.substantive_hits == 0


def block_spans(text: str) -> list[tuple[int, int]]:
    """Character spans of scenario boxes, code fences and tables."""
    spans: list[tuple[int, int]] = []
    for line_pat in SUBSTANTIVE_CONTEXT:
        for m in line_pat.finditer(text):
            line_start = text.rfind("\n", 0, m.start()) + 1
            line_end = text.find("\n", m.start())
            spans.append((line_start, line_end if line_end != -1 else len(text)))
    # Code fences: take the whole fenced region, not just the fence line.
    for m in re.finditer(r"^```.*?^```", text, re.S | re.M):
        spans.append((m.start(), m.end()))
    return spans


def in_any_span(pos: int, spans: list[tuple[int, int]]) -> bool:
    return any(lo <= pos <= hi for lo, hi in spans)


def analyse(path: Path) -> list[IPUsage]:
    text = path.read_text(encoding="utf-8")
    spans = block_spans(text)
    usages: list[IPUsage] = []
    for name, pattern in EXTENDED_CAST.items():
        hits = list(re.finditer(pattern, text, re.I))
        if not hits:
            continue
        substantive = sum(1 for h in hits if in_any_span(h.start(), spans))
        usages.append(IPUsage(name, len(hits), substantive))
    return sorted(usages, key=lambda u: -u.mentions)


def main() -> int:
    ap = argparse.ArgumentParser(description=(__doc__ or "variety check").splitlines()[0])
    ap.add_argument("chapters", nargs="+", type=Path)
    ap.add_argument("--floor", type=int, default=DISTINCT_IP_FLOOR,
                    help=f"minimum distinct extended-cast IPs (default {DISTINCT_IP_FLOOR})")
    args = ap.parse_args()

    warnings = 0
    totals: dict[str, int] = {name: 0 for name in EXTENDED_CAST}

    for path in args.chapters:
        if not path.is_file():
            print(f"[error] not a file: {path}", file=sys.stderr)
            return 2
        usages = analyse(path)
        for u in usages:
            totals[u.name] += 1

        label = path.stem
        names = ", ".join(f"{u.name}({u.mentions}"
                          f"{'*' if u.substantive_hits else ''})" for u in usages)
        status = "ok  " if len(usages) >= args.floor else "WARN"
        if len(usages) < args.floor:
            warnings += 1
        print(f"[{status}] {label}: {len(usages)} distinct | {names or '(none)'}")

        for u in usages:
            if u.looks_thin:
                warnings += 1
                print(f"         ^ '{u.name}' mentioned {u.mentions}x, never inside a "
                      f"scenario/artifact/table -- likely decayed to a cross-reference")

    print("\n=== distribution across chapters (how many chapters use each) ===")
    for name, count in sorted(totals.items(), key=lambda kv: -kv[1]):
        bar = "#" * count
        flag = "  <- unused" if count == 0 else ""
        print(f"  {name:<18} {count:>2} {bar}{flag}")

    used = [c for c in totals.values() if c]
    if used:
        top = sorted(totals.values(), reverse=True)[:4]
        share = sum(top) / sum(used) * 100
        print(f"\ntop-4 IPs carry {share:.0f}% of chapter-level usage "
              f"({'concentrated' if share > 60 else 'balanced'})")

    print(f"\n{warnings} warning(s). "
          "* = appears inside a scenario box, code block or table.")
    print("A WARN means go and look -- never pad a chapter with a name to clear it.")
    return 1 if warnings else 0


if __name__ == "__main__":
    raise SystemExit(main())
