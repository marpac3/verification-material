#!/usr/bin/env python3
"""Pre/post invariant checker for the editorial passes.

Purpose
-------
Pass A (register) rewrites prose framing across ~205k words with many parallel
agents. Pass B (industrial anchoring) adds sourced material. Both can silently
damage the things the book's whole audit machinery rests on: citation markers,
numbers, code, cross-references, glossary-controlled vocabulary.

This tool makes "nothing load-bearing moved" mechanical. It extracts five token
classes per chapter, diffs a before-snapshot against the working tree, and
applies a per-pass asymmetric policy, because the dangerous DIRECTION differs:

  Pass A (register, prose framing only)
      citations   : no additions, no removals
      numbers     : no ADDITIONS (a new number is an invented claim).
                    Removals are reported and must be declared by the agent
                    (rewriting an anecdotal opening legitimately drops
                    anecdote-local figures).
      code blocks : byte-identical, same order
      cross-refs  : no ADDITIONS; removals reported
      vocabulary  : `validation` count must not change (the live trap)

  Pass B (industrial anchoring, additive only)
      citations   : no REMOVALS (additions expected, each carrying a source)
      numbers     : no REMOVALS
      code blocks : no removals; additions allowed
      cross-refs  : no REMOVALS
      vocabulary  : `validation` count must not change

Usage
-----
    python3 tools/check_invariants.py snapshot --dest meta/snapshots/preA
    python3 tools/check_invariants.py check --before meta/snapshots/preA \\
            --after book --policy A [--chapters ch04 ch05] [--json out.json]

Exit code is non-zero if any chapter FAILs, so it can gate a build.
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import shutil
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# --- token classes -----------------------------------------------------------

FENCE_RE = re.compile(r"^([ \t]*)(`{3,}|~{3,})(.*)$")

# The comma matters. Without it the character class stops at the first source
# and the closing `]` never matches, so a marker like `[cit:S8,B4]` is not a
# partial match — it is *no* match at all. Seventy-two markers in the manuscript
# carry two or three sources, and every one of them was invisible to this
# counter: an editorial pass could delete `[cit:P17,R2]` outright and the gate
# would report no citation change in either direction, on a class whose whole
# point is that removals are fatal under every policy. Found by probing the
# extractor with a marker present and absent and getting identical output.
#
# Splitting the captured group on commas is what makes the count mean what it
# says: `[cit:S8,B4]` contributes S8 and B4 individually, so dropping one source
# from a two-source marker is caught as well as dropping the marker.
CITATION_RE = re.compile(r"\[cit:([A-Za-z0-9_.,-]+)\]")

# Digit runs, with decimal separators kept attached so "10.4" is one token and
# not two. Unicode superscripts are a separate class of digit and are captured
# as their own runs (the book writes 10^12 as 10¹²).
NUMBER_RE = re.compile(r"\d+(?:[.,]\d+)*|[⁰-⁹²³¹]+")

CROSSREF_RE = re.compile(
    r"Chapters?\s+\d+"
    r"|Appendix\s+[A-Z]\b"
    r"|§\s?\d+(?:\.\d+)*"
    r"|Sections?\s+\d+(?:\.\d+)*"
    r"|Table\s+\d+(?:\.\d+)?"
    r"|Figure\s+\d+(?:\.\d+)?"
)

# A numbered heading's own number — "## 2.1 Designer and verifier". It is the
# section's name, not a quantity claimed in the prose, and CROSSREF_RE does not
# reach it because it carries no "§" and no "Section". Numbering the headings of
# a chapter that had none previously therefore read as four fabricated
# quantities and failed the chapter.
HEADING_NUM_RE = re.compile(r"^(#{1,6})\s+\d+(?:\.\d+)*", re.MULTILINE)

# A digit run glued to a letter stem is an identifier: DMA-F01, XB-07, S13,
# AXI4, IHI0022, ch04. Extracting "01" from "DMA-F01" and calling it a quantity
# means a caption that names the plan row it captions fails the number gate.
IDENT_NUM_RE = re.compile(r"\b[A-Za-z]+(?:[-_][A-Za-z]+)*[-_]?\d+[A-Za-z0-9_-]*")

# G2 — hedges and epistemic markers.
#
# Belem et al. (2026) measure that rewriting distorts certainty in up to 75% of
# outputs, biased 1.5-2x toward *more* certainty, and that this happens "when
# semantic content is preserved" — so it is invisible, by construction, to the
# citation, number, code, cross-reference and vocabulary classes above. The
# style guide already forbids it in prose ("hedges are load-bearing and must
# survive editing"); the same paper measures that prose instructions reduce the
# defect without eliminating it. Hence a mechanical class.
#
# Shipped as a **multiset with declared removals**, deliberately, not as the
# sentence-aligned superset rule the research proposes. The aligned version
# needs a similarity floor plus merge/split declarations plus three carve-outs,
# and a gate that blocks correct edits is a gate that gets switched off. The
# multiset has the same shape as the number class, and it catches net hedge
# loss, which is the asymmetric direction actually measured. Upgrade only if
# this version starts passing something visibly wrong.
#
# Word-boundary anchored and lowercased. Multiword entries come first so the
# longest match wins.
HEDGE_TERMS = (
    "in the cases reported",
    "on the designs measured",
    "on the order of",
    "as far as",
    "to a first approximation",
    "in most cases",
    "in many cases",
    "in some cases",
    "at least",
    "at most",
    "up to",
    "tends to",
    "tend to",
    "can be",
    "may be",
    "approximately",
    "roughly",
    "typically",
    "usually",
    "generally",
    "commonly",
    "frequently",
    "often",
    "rarely",
    "seldom",
    "largely",
    "partly",
    "partially",
    "mostly",
    "broadly",
    "nearly",
    "almost",
    "about",
    "around",
    "may",
    "might",
    "could",
    "appears",
    "appear",
    "seems",
    "suggests",
    "suggest",
    "indicates",
    "indicate",
    "reported",
    "reportedly",
    "some",
    "many",
    "most",
    "several",
)

HEDGE_RE = re.compile(
    r"\b(?:" + "|".join(re.escape(t) for t in HEDGE_TERMS) + r")\b",
    re.IGNORECASE,
)

# Spelled-out quantities.
#
# `NUMBER_RE` captures digit runs only, so "five managers against four
# subordinates", "six weeks to sign-off" and "two ordering properties" are
# invisible to the number class — and the Pass A1 contract's rule that *every*
# quantity must survive an opening rewrite therefore had no mechanical backing
# for half the quantities in the openings it governs.
#
# Reported as notes, never fatal, in both directions. Spelled numbers occur
# constantly in ordinary prose ("one of the two", "a second look"), so a fatal
# gate here would fire on correct edits and would be switched off. Its job is to
# put "spelled: -1 removed ['five']" in front of the editor's eyes.
SPELLED_TERMS = (
    "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
    "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
    "seventeen", "eighteen", "nineteen", "twenty", "thirty", "forty", "fifty",
    "sixty", "seventy", "eighty", "ninety",
    "hundred", "thousand", "million", "billion", "trillion",
    "dozen", "half", "third", "quarter", "twice", "double", "triple",
)

SPELLED_RE = re.compile(
    r"\b(?:" + "|".join(SPELLED_TERMS) + r")\b", re.IGNORECASE
)

STRICT_VOCAB = ("validation",)
WATCH_VOCAB = (
    "validation",
    "verification",
    "scoreboard",
    "reference model",
    "transfer function",
    "vacuous",
    "waiver",
    "irritator",
    "sign-off",
)


def split_code_blocks(text: str) -> tuple[str, list[str]]:
    """Return (prose_with_code_removed, list_of_code_block_bodies).

    Tracks fence length and marker so a ```` ``` ```` inside a ```` ~~~~ ````
    block does not close it.
    """
    prose_lines: list[str] = []
    blocks: list[str] = []
    current: list[str] | None = None
    marker = ""
    for line in text.splitlines():
        m = FENCE_RE.match(line)
        if current is None:
            if m and m.group(3).strip().find("`") == -1:
                current = []
                marker = m.group(2)
                continue
            prose_lines.append(line)
        else:
            if m and m.group(2)[0] == marker[0] and len(m.group(2)) >= len(marker):
                blocks.append("\n".join(current))
                current = None
                continue
            current.append(line)
    if current is not None:  # unterminated fence: keep what we have
        blocks.append("\n".join(current))
    return "\n".join(prose_lines), blocks


def extract(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    prose, blocks = split_code_blocks(text)
    lower = prose.lower()
    # Citation IDs carry digits ([cit:B2] -> "2"). They are identifiers, not
    # claims, and the citation class already tracks them, so keep them out of
    # the number multiset.
    # Citation IDs and cross-references carry digits ([cit:B2] -> "2",
    # "§16.1" -> "16.1", "Chapter 14" -> "14"). Both are *identifiers*, not
    # claims, and both already have their own class above. Counting them as
    # numbers too means any legitimate change to signposting trips the number
    # gate — and a gate that fires on correct edits is a gate that gets
    # switched off.
    # Strip, in order: citation ids, cross-references, a numbered heading's own
    # number, and alphanumeric identifiers. What survives is meant to be a
    # quantity a reader could check.
    prose_no_cit = CROSSREF_RE.sub(" ", CITATION_RE.sub("", prose))
    prose_no_cit = HEADING_NUM_RE.sub(r"\1 ", prose_no_cit)
    prose_no_cit = IDENT_NUM_RE.sub(" ", prose_no_cit)
    return {
        "citations": Counter(
            src
            for group in CITATION_RE.findall(prose)
            for src in (s.strip() for s in group.split(","))
            if src
        ),
        "numbers": Counter(NUMBER_RE.findall(prose_no_cit)),
        "crossrefs": Counter(re.sub(r"\s+", " ", m) for m in CROSSREF_RE.findall(prose)),
        "code": blocks,
        "hedges": Counter(m.group(0).lower() for m in HEDGE_RE.finditer(prose)),
        "spelled": Counter(m.group(0).lower() for m in SPELLED_RE.finditer(prose)),
        "vocab": {t: lower.count(t) for t in WATCH_VOCAB},
        "words": len(prose.split()),
        "prose_words": prose.split(),
    }


def _chars_only_added(before: str, after: str) -> bool:
    """True if `before` can be obtained from `after` by deleting characters.

    That is exactly "bytes were added to this line and none were removed" — the
    shape of a permitted Pass B edit, which may insert a `[cit:ID]` marker at an
    offset inside an existing sentence but may not reword it.
    """
    it = iter(after)
    return all(ch in it for ch in before)


def additive_violations(before: str, after: str, limit: int = 6) -> list[str]:
    """G3 for the additive passes: report every non-insertion change.

    The style guide names G3 — "every changed byte falls inside an approved
    span" — as mechanically enforced. For a *rewriting* pass that needs an
    approved span list the tool does not have. But for a **byte-additive** pass
    the same intent has an exact mechanical form and no span list is required:
    every hunk must be an insertion, and a modified line is legitimate only if
    characters were added to it and none removed. Pass B and Pass C both claim
    byte-additivity as their central constraint and, until this check existed,
    nothing verified it.
    """
    b, a = before.split("\n"), after.split("\n")
    sm = difflib.SequenceMatcher(a=b, b=a, autojunk=False)
    out: list[str] = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag in ("equal", "insert"):
            continue
        if tag == "delete":
            out.append(
                f"line {i1 + 1}: {i2 - i1} line(s) deleted — "
                f"“{b[i1].strip()[:60]}”"
            )
            continue
        # replace: permitted only as a within-line insertion, pairwise.
        if (i2 - i1) != (j2 - j1):
            out.append(
                f"line {i1 + 1}: {i2 - i1} line(s) replaced by {j2 - j1} — "
                f"not an insertion"
            )
            continue
        for k in range(i2 - i1):
            ob, oa = b[i1 + k], a[j1 + k]
            if not _chars_only_added(ob, oa):
                out.append(
                    f"line {i1 + k + 1}: reworded, not extended — "
                    f"“{ob.strip()[:50]}” -> “{oa.strip()[:50]}”"
                )
        if len(out) >= limit:
            break
    return out[:limit]


def largest_deletion(before_words: list[str], after_words: list[str]) -> tuple[int, str]:
    """G7 — the largest single contiguous deletion, in words, and its opening.

    A chapter-total word delta cannot distinguish "trimmed theatre in twenty
    places" from "deleted a paragraph", and the second is the failure mode:
    deleting a non-compliant paragraph is the cheapest possible way to satisfy a
    register mandate, and it is fully compliant with a declared-removal report.
    This is the Pass A isomorph of RARR's measured preservation trap.

    Read the figure as an alarm, not as a measurement of content lost. The
    metric is alignment-sensitive: an unrelated few-word change elsewhere in
    the same paragraph can change how difflib fragments one `replace` opcode
    and so move the reported number substantially with no additional content
    deleted. Observed 2026-08-27: a one-clause grammar fix moved ch04's
    reported largest deletion from 70 words to 35.
    """
    sm = difflib.SequenceMatcher(a=before_words, b=after_words, autojunk=False)
    worst = 0
    excerpt = ""
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag not in ("delete", "replace"):
            continue
        lost = (i2 - i1) - (j2 - j1)
        if lost > worst:
            worst = lost
            excerpt = " ".join(before_words[i1 : min(i1 + 12, i2)])
    return worst, excerpt


def counter_delta(before: Counter, after: Counter) -> tuple[Counter, Counter]:
    """Return (added, removed) as positive-count Counters."""
    return (after - before), (before - after)


def fmt_counter(c: Counter, limit: int = 12) -> str:
    items = sorted(c.items(), key=lambda kv: (-kv[1], str(kv[0])))
    shown = ", ".join(f"{k!r}×{v}" if v > 1 else f"{k!r}" for k, v in items[:limit])
    if len(items) > limit:
        shown += f", … (+{len(items) - limit} more)"
    return shown or "—"


# --- policy ------------------------------------------------------------------

# class -> (additions_fatal, removals_fatal)
POLICY = {
    "A": {
        "citations": (True, True),
        "numbers": (True, False),
        "crossrefs": (True, False),
        # A hedge added is conservative and safe; a hedge lost is a claim
        # strengthened, which is the measured, asymmetric failure.
        "hedges": (False, True),
        "spelled": (False, False),
    },
    # A1 — the structural sub-pass: `What you will learn` blocks become chapter
    # maps, and narrated openings become problem statements. Identical to A
    # except that a chapter map needs numbered signposting into the chapter's
    # own sections, and under policy A that reads as a forbidden
    # cross-reference addition. A1 permits `§N.M` additions **where N is the
    # chapter's own number** and reports them; every other cross-reference
    # addition stays fatal, because a pointer to another chapter, an appendix,
    # a table or a figure is a claim about material the agent cannot see.
    "A1": {
        "citations": (True, True),
        "numbers": (True, False),
        "crossrefs": (True, False),
        "hedges": (False, True),
        "spelled": (False, False),
    },
    "B": {
        "citations": (False, True),
        "numbers": (False, True),
        "crossrefs": (False, True),
        "hedges": (False, True),
        "spelled": (False, False),
    },
}

CHAPTER_NUM_RE = re.compile(r"ch0*(\d+)")


SECTION_HEADING_RE = re.compile(r"^#{2,4}\s+(\d+(?:\.\d+)+)\b", re.MULTILINE)


def own_section_ref(token: str, chapter_name: str) -> bool:
    """True if `token` is a §N.M pointer into `chapter_name`'s own sections."""
    m = CHAPTER_NUM_RE.fullmatch(chapter_name)
    if not m:
        return False
    own = m.group(1)
    sec = re.fullmatch(r"§\s?(\d+)(?:\.\d+)*", token)
    return bool(sec and sec.group(1) == own)


def section_headings(path: Path) -> set[str]:
    """The section numbers that actually have a heading in this file."""
    return set(SECTION_HEADING_RE.findall(path.read_text(encoding="utf-8")))


def unresolved_refs(tokens, headings: set[str]) -> list[str]:
    """Own-chapter §N.M pointers with no matching heading.

    Checking the *form* of a permitted addition is not checking the addition.
    Without this, a chapter map full of pointers to sections that do not exist
    passes policy A1 with a reassuring "permitted for a chapter map" note — the
    exact shape of a gate that looks like it is working and is not.
    """
    bad: list[str] = []
    for tok in tokens:
        num = re.fullmatch(r"§\s?(\d+(?:\.\d+)+)", tok)
        if num and num.group(1) not in headings:
            bad.append(tok)
    return sorted(set(bad))

# G4 — length delta. Pass A removes theatre and replaces it with scope
# statements, so it should be length-neutral to shrinking; growth is the
# signature of rigour-flavoured padding. Marked ASSERTED in the research base:
# the supporting measurement (verbosity compensation) is from question
# answering, not from editing. The check costs nothing.
GROWTH_ALARM = 0.02   # report
GROWTH_BLOCK = 0.05   # fail

# G7 — deletion budget, in words, for a single contiguous deletion.
DELETION_ALARM = 25
DELETION_BLOCK = 120


def check_chapter(name: str, before: Path, after: Path, policy: str) -> dict:
    b, a = extract(before), extract(after)
    findings: list[str] = []
    notes: list[str] = []
    rules = POLICY[policy]

    for cls in ("citations", "numbers", "crossrefs", "hedges", "spelled"):
        added, removed = counter_delta(b[cls], a[cls])
        add_fatal, rem_fatal = rules[cls]
        if added:
            if cls == "crossrefs" and policy == "A1":
                own = Counter(
                    {k: v for k, v in added.items() if own_section_ref(k, name)}
                )
                foreign = added - own
                if own:
                    dangling = unresolved_refs(own, section_headings(after))
                    if dangling:
                        findings.append(
                            f"crossrefs: {len(dangling)} own-chapter pointer(s) "
                            f"resolve to no heading in this chapter: "
                            f"{', '.join(dangling)}"
                        )
                    resolved = sum(own.values()) - len(dangling)
                    if resolved > 0:
                        notes.append(
                            f"crossrefs: +{resolved} own-chapter section "
                            f"pointer(s) [{fmt_counter(own)}] — permitted for a "
                            "chapter map; each target heading verified to exist"
                        )
                if foreign:
                    findings.append(
                        f"crossrefs: +{sum(foreign.values())} added outside this "
                        f"chapter [{fmt_counter(foreign)}]"
                    )
                added = foreign
            else:
                line = f"{cls}: +{sum(added.values())} added [{fmt_counter(added)}]"
                (findings if add_fatal else notes).append(line)
        if removed:
            line = f"{cls}: -{sum(removed.values())} removed [{fmt_counter(removed)}]"
            (findings if rem_fatal else notes).append(line)

    # Code blocks: order-sensitive and byte-exact. Pass B may append blocks.
    # A1 is a Pass A variant and takes Pass A's strict branch: its contract says
    # code blocks are byte-identical, and an `in ("A",)` test silently gave A1
    # the additive branch, where an appended block was only a note.
    if policy in ("A", "A1"):
        if b["code"] != a["code"]:
            if len(b["code"]) != len(a["code"]):
                findings.append(
                    f"code: block count {len(b['code'])} -> {len(a['code'])}"
                )
            else:
                changed = [i for i, (x, y) in enumerate(zip(b["code"], a["code"])) if x != y]
                findings.append(f"code: block(s) {changed} modified (must be byte-identical)")
    else:
        if a["code"][: len(b["code"])] != b["code"]:
            findings.append("code: existing blocks modified or reordered (Pass B is additive)")
        elif len(a["code"]) > len(b["code"]):
            notes.append(f"code: +{len(a['code']) - len(b['code'])} block(s) appended")

    for term in WATCH_VOCAB:
        d = a["vocab"][term] - b["vocab"][term]
        if d:
            line = f"vocab '{term}': {b['vocab'][term]} -> {a['vocab'][term]} ({d:+d})"
            (findings if term in STRICT_VOCAB else notes).append(line)

    # G3 — additive-only diff. Applies to the byte-additive passes only; a
    # rewriting pass needs an approved span list this tool does not hold.
    if policy == "B":
        viol = additive_violations(
            before.read_text(encoding="utf-8"), after.read_text(encoding="utf-8")
        )
        for v in viol:
            findings.append(f"G3 not additive: {v}")

    # G4 — length delta.
    ratio = (a["words"] / b["words"]) if b["words"] else 1.0
    growth = ratio - 1.0
    if growth >= GROWTH_BLOCK:
        findings.append(
            f"G4 length: {b['words']} -> {a['words']} words ({growth:+.1%}); "
            f"Pass {policy} must not pad — growth above {GROWTH_BLOCK:.0%} blocks"
        )
    elif growth >= GROWTH_ALARM:
        notes.append(f"G4 length: {b['words']} -> {a['words']} words ({growth:+.1%})")

    # G7 — largest single contiguous deletion.
    lost, excerpt = largest_deletion(b["prose_words"], a["prose_words"])
    if lost >= DELETION_BLOCK:
        findings.append(
            f"G7 deletion: largest single deletion is {lost} words, at "
            f"“{excerpt} …” — above {DELETION_BLOCK}, must be justified "
            "as theatre with a statement of what content survives and where"
        )
    elif lost >= DELETION_ALARM:
        notes.append(
            f"G7 deletion: largest single deletion is {lost} words, at "
            f"“{excerpt} …”"
        )

    return {
        "chapter": name,
        "status": "FAIL" if findings else "PASS",
        "findings": findings,
        "notes": notes,
        "words_before": b["words"],
        "words_after": a["words"],
        "largest_deletion": lost,
    }


# --- commands ----------------------------------------------------------------

def chapter_files(directory: Path, names: list[str] | None) -> list[Path]:
    files = sorted(directory.glob("*.md"))
    if names:
        wanted = set(names)
        files = [f for f in files if f.stem in wanted]
        missing = wanted - {f.stem for f in files}
        if missing:
            sys.exit(f"error: not found in {directory}: {', '.join(sorted(missing))}")
    if not files:
        sys.exit(f"error: no .md files in {directory}")
    return files


def cmd_snapshot(args) -> int:
    src = ROOT / args.src
    dest = ROOT / args.dest
    dest.mkdir(parents=True, exist_ok=True)
    files = chapter_files(src, args.chapters)
    for f in files:
        shutil.copy2(f, dest / f.name)
    print(f"[snapshot] {len(files)} file(s) {src} -> {dest}")
    return 0


def cmd_check(args) -> int:
    before_dir, after_dir = ROOT / args.before, ROOT / args.after
    if not before_dir.is_dir():
        sys.exit(f"error: snapshot dir missing: {before_dir}")
    results = []
    for f in chapter_files(before_dir, args.chapters):
        after = after_dir / f.name
        if not after.exists():
            results.append(
                {"chapter": f.stem, "status": "FAIL", "findings": ["file missing in after/"],
                 "notes": [], "words_before": 0, "words_after": 0}
            )
            continue
        results.append(check_chapter(f.stem, f, after, args.policy))

    failed = [r for r in results if r["status"] == "FAIL"]
    print(f"=== invariant check, policy {args.policy} "
          f"({before_dir.name} -> {after_dir.name}) ===")
    for r in results:
        delta = r["words_after"] - r["words_before"]
        head = f"{r['status']:4} {r['chapter']}  {r['words_before']}->{r['words_after']} w ({delta:+d})"
        if r["findings"] or r["notes"]:
            print(head)
            for x in r["findings"]:
                print(f"       FATAL  {x}")
            for x in r["notes"]:
                print(f"       note   {x}")
        else:
            print(head)
    print(f"\n{len(results) - len(failed)}/{len(results)} PASS"
          + (f", {len(failed)} FAIL: {', '.join(r['chapter'] for r in failed)}" if failed else ""))

    if args.json:
        Path(args.json).write_text(json.dumps(results, indent=2), encoding="utf-8")
        print(f"[json] {args.json}")
    return 1 if failed else 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("snapshot", help="copy chapters to a snapshot directory")
    s.add_argument("--src", default="book")
    s.add_argument("--dest", required=True)
    s.add_argument("--chapters", nargs="*")
    s.set_defaults(func=cmd_snapshot)

    c = sub.add_parser("check", help="diff a snapshot against the working tree")
    c.add_argument("--before", required=True)
    c.add_argument("--after", default="book")
    c.add_argument("--policy", required=True, choices=sorted(POLICY))
    c.add_argument("--chapters", nargs="*")
    c.add_argument("--json")
    c.set_defaults(func=cmd_check)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
