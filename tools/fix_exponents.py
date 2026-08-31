import re, sys
from pathlib import Path

APPLY = "--apply" in sys.argv

# A caret exponent in prose is a plain-text convention; this book already sets
# ≈, ×, – and a Unicode subscript ₂, so the caret is the one place its typography
# falls back to ASCII. Exponents inside code — fenced or four-space indented —
# and inside inline code spans are correct as they are and must not be touched:
# ch13's MTBF formula is a monospace expression where `e^(Ts/Tc)` is the notation.
EXP = re.compile(r"(?<=[0-9A-Za-z\)])\^(-?\d+|n)\b")
CODE_SPAN = re.compile(r"`[^`]*`")

def convert_line(line: str) -> tuple[str, list[str]]:
    """Rewrite caret exponents outside inline code spans."""
    spans = [(m.start(), m.end()) for m in CODE_SPAN.finditer(line)]
    hits: list[str] = []

    def in_code(pos: int) -> bool:
        return any(a <= pos < b for a, b in spans)

    out, last = [], 0
    for m in EXP.finditer(line):
        if in_code(m.start()):
            continue
        out.append(line[last:m.start()])
        out.append(f"<sup>{m.group(1)}</sup>")
        hits.append(line[max(0, m.start() - 12):m.end() + 4])
        last = m.end()
    out.append(line[last:])
    return "".join(out), hits

total = 0
for path in sorted(Path("book").glob("*.md")) + sorted(Path("front").glob("*.md")):
    lines = path.read_text(encoding="utf-8").split("\n")
    fenced = False
    changed = False
    for i, line in enumerate(lines):
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if fenced or line.startswith("    "):
            continue
        new, hits = convert_line(line)
        if hits:
            total += len(hits)
            changed = True
            print(f"{path}:{i+1}  " + " | ".join(h.strip() for h in hits))
            lines[i] = new
    if changed and APPLY:
        path.write_text("\n".join(lines), encoding="utf-8")

print(f"\n{'applied' if APPLY else 'would convert'}: {total} exponent(s)")
