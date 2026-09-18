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

  Pass A1 (structural sub-pass of A: chapter maps, problem statements)
      identical to A, except that `§N.M` / `Section N.M` pointers into the
      chapter's OWN sections may be added — reported, and each target heading
      verified to exist. Every other cross-reference addition stays fatal.

  Pass B (industrial anchoring, additive only)
      citations   : no REMOVALS (additions expected, each carrying a source)
      numbers     : no REMOVALS
      code blocks : no removals; additions allowed
      cross-refs  : no REMOVALS
      vocabulary  : `validation` count must not change
      diff shape  : every hunk an insertion (G3, mechanical)

  Pass C (float captions / apparatus, strictly additive)
      same table as B. Its contract (`meta/passes/pass_c_captions.md`) says it
      "adds caption lines and nothing else", so it takes the same additive
      branch, G3 included. Until 2026-09-02 the docstring promised C and
      `POLICY` had no C entry, so `--policy C` was rejected by argparse and the
      pass ran ungated; the entry below is the fix.

  Pass D (consolidation: rewriting a sentence that asserts a false absence,
          folding a "pointer" bullet into the citation that now exists)
      same table as A, except that citations are held at the level of the SET
      of IDs the chapter cites: an ID that vanishes from the chapter is fatal,
      a duplicate occurrence that goes (the pointer bullet repeating a marker
      the paragraph above already carries) is a note. Added 2026-09-03, when
      W1 showed that A's per-occurrence count and B's additive diff between
      them left no policy under which "Not in the corpus: X — this edition
      holds X, see [cit:X] above" could become a true sentence.

  Pass G (voice and slimming, W2)
      A1's table — rule 2 of style-guide revision 4 replaces a re-explanation
      with a pointer into the chapter's own sections — except that a hedge
      REMOVED is a note naming the terms, not a block. G2 asks that something
      show the claim became unconditional; under G that something is the claim
      ledger the coordinator reads, because the two legitimate cases W2
      measured are invisible to a count: a sentence deleted that duplicated a
      claim still hedged in the surviving copy, and a `HEDGE_RE` false positive
      ("about" as a preposition). Hedge additions stay non-fatal, and every
      other class keeps A's asymmetry. G7 is relaxed the same way and for the
      same reason: a contiguous deletion above the block threshold is a note
      naming the figure, because fusing two paragraphs or dropping a
      re-derivation another chapter owns exceeds 120 words as a matter of
      routine, and whether the content survives elsewhere is a fact about the
      book rather than about this chapter's word list.

  Pass H (didactic apparatus, W3: exercises, figures, code, glossary, index)
      citations   : no additions, no removals. The pass carries no source, and
                    `meta/passes/pass_h_didactic_apparatus.md` §1 says so.
      numbers     : no REMOVALS. Additions are free and are NOT judged here: an
                    exercise states quantities, and whether each one comes from
                    the example bank or from the chapter's own body is
                    `check_exercises.py`'s question (pass H §3), measured
                    against a source this tool does not read.
      code blocks : existing blocks byte-identical and in the same relative
                    order; a NEW block may appear ANYWHERE. This is the third
                    code shape (`code_new_blocks`): the pass adds a covergroup
                    inside ch06 and a block inside an exercise, and neither is
                    an append, so B's prefix rule rejects both.
      cross-refs  : no REMOVALS; an addition is free, and an own-chapter `§N.M`
                    has its target heading verified — a solution pointing at a
                    section that does not exist is the failure `unresolved_refs`
                    exists for.
      hedges      : no REMOVALS.
      diff shape  : every hunk an insertion (B's rule), with one exception the
                    caller declares. `--allow-edits FILE` lists exact
                    old -> new substitutions, chapter by chapter, and a hunk
                    that is one of them is not a violation: the pass adds a
                    `{ref:}` to a float that nothing referenced, and that means
                    one existing sentence gains the clause carrying it. The
                    exception is scoped to the diff SHAPE. Every token class
                    above is still measured against the real before, so a
                    declared edit that also drops a hedge, a number or a
                    cross-reference is fatal on that class.
      length      : growth is what the pass is for, so G4's block becomes a
                    note and the band is measured where the contract puts it:
                    `check_register.py --band 0 0.15` (pass H §5.3). Without
                    this the two gates of one contract contradict each other,
                    G4 blocking at +5 % what §5.3 admits to +15 %.

Every difference between passes lives in the `POLICY` table and nowhere else:
no branch below tests a policy name, except `frozen_g_units` under G.

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


# A polarity word, screened for inside the text an additive pass inserts.
#
# One contiguous insertion is still enough to invert a sentence, and no
# byte-additivity rule can see it, because nothing was removed: "the rule
# applies" -> "the rule no longer applies" inserts ten characters at one offset
# and reverses the claim. So the inserted chunk is screened lexically and a
# chunk carrying one of these words is fatal with the chunk quoted. This is a
# tripwire on a closed word list, not a semantic check: it fires on these words
# and on nothing else, and it is the reason the byte rule alone is not the whole
# of the T2 fix.
POLARITY_RE = re.compile(
    r"\bno longer\b|\bnot\b|\bnever\b|\bnor\b|\bneither\b|\bcannot\b"
    r"|\bwithout\b|\bunlike\b|\bunless\b|\binstead of\b|\brather than\b"
    r"|\bfails? to\b|\bcontrary to\b|\bno\b|n't",
    re.IGNORECASE,
)


def single_insertion(before: str, after: str) -> str | None:
    """The one contiguous chunk inserted into `before` to give `after`.

    Returns the inserted text (possibly `""` when the lines are identical), or
    None when `after` cannot be produced from `before` by inserting one
    contiguous run of characters at one offset — which is what deletion,
    reordering and interleaved rewording all look like.

    This replaces a **subsequence** test, and the difference is the whole of
    defect T2. "Every character of the old line reappears, in order, somewhere
    in the new one" reads like byte-additivity and is not: interleaved rewording
    preserves the old characters in order and merely threads new ones between
    them. Both of these passed the old predicate and are fatal now:

        "the rule applies"                 -> "the rule no longer applies"
        "the scoreboard compares txns"     -> "the scoreboard, when enabled,
                                               compares committed txns"

    The stricter form `before in after` — insertion at the head or the tail
    only — was considered and rejected: it fails a `[cit:ID]` marker dropped at
    an offset inside an existing sentence, which the style guide names as a
    negative control that must PASS. One insertion point is the tightest rule
    that keeps that case legal.

    The cost, recorded rather than hidden: two markers inserted into the *same
    line* in one pass are two insertion points and now fail. An additive pass
    that needs both must add them in separate hunks or declare the line.

    The negation case is deliberately NOT handled here. It is a legal single
    insertion, so this predicate returns the chunk; `POLARITY_RE` above is what
    catches it, at the call site.
    """
    if after == before:
        return ""
    if len(after) <= len(before):
        return None
    i = 0
    while i < len(before) and before[i] == after[i]:
        i += 1
    # Bounded by `len(before) - i` so the common prefix and the common suffix
    # cannot overlap and claim the same characters twice.
    j = 0
    while j < len(before) - i and before[-1 - j] == after[-1 - j]:
        j += 1
    if i + j != len(before):
        return None
    return after[i : len(after) - j]


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

    Which passes it runs for is decided by `POLICY[...]["additive_diff"]`, not
    by a policy name tested here: the earlier `policy == "B"` made this
    docstring's second sentence false for C, which had no policy entry at all.
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
            chunk = single_insertion(ob, oa)
            if chunk is None:
                out.append(
                    f"line {i1 + k + 1}: reworded, not extended by one "
                    f"insertion — “{ob.strip()[:50]}” -> “{oa.strip()[:50]}”"
                )
            elif POLARITY_RE.search(chunk):
                out.append(
                    f"line {i1 + k + 1}: inserted text changes polarity — "
                    f"“{chunk.strip()[:50]}” into “{ob.strip()[:50]}”"
                )
        if len(out) >= limit:
            break
    return out[:limit]


def code_insertions_only(before: list[str], after: list[str], limit: int = 6) -> list[str]:
    """Pass H's code shape: existing blocks byte-exact and in order, new ones anywhere.

    Neither branch that existed could express it. `code_byte_exact` compares the
    two lists whole, so any insertion is a block-count change; the additive
    branch compares a PREFIX, so an insertion is legal only after the last
    existing block. Pass H adds a covergroup inside ch06's own sections and a
    fenced block inside an exercise, and both sit between existing blocks — the
    probe of 2026-09-08 ran a mid-file block into ch06 and policies B and C
    reported "existing blocks modified or reordered", which is the wrong
    finding for a correct edit.

    The rule here is the exact one: the opcodes of the two block lists must all
    be `equal` or `insert`. That says every block of the before survives, byte
    for byte, in its relative order, and says nothing about where a new one
    lands. A reordering shows up as a delete plus an insert and is reported.
    """
    sm = difflib.SequenceMatcher(a=before, b=after, autojunk=False)
    out: list[str] = []
    for tag, i1, i2, _j1, _j2 in sm.get_opcodes():
        if tag in ("equal", "insert"):
            continue
        verb = "removed" if tag == "delete" else "modified or reordered"
        out.append(f"existing block(s) {list(range(i1, i2))} {verb}")
        if len(out) >= limit:
            break
    return out[:limit]


# `--allow-edits`: the declared exception to the additive diff.
#
# Pass H adds a `{ref:}` to each float that nothing referenced (§1, F3/F4), and
# a reference needs a sentence to carry it: the one sentence that gains the
# clause is a rewording, which is exactly what `additive_violations` blocks. The
# alternative to declaring it is switching G3 off for the whole pass, which
# would let any rewording through. So the caller writes the substitutions down,
# chapter by chapter, and only those exact spans may change.
ALLOW_EDIT_REQUIRED = ("chapter", "old", "new")
ALLOW_EDIT_OPTIONAL = ("reason",)


def load_allow_edits(path: Path) -> list[dict]:
    """Read and validate the declaration file, or exit naming the entry.

    The file is written permission to change bytes, so an entry this tool cannot
    apply exactly is an error and never an entry quietly ignored: ignoring one
    turns "the declaration was malformed" into "the gate passed".
    """
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        sys.exit(f"error: --allow-edits {path}: {exc}")
    if not isinstance(payload, list):
        sys.exit(f"error: --allow-edits {path}: expected a JSON list of "
                 '{"chapter": …, "old": …, "new": …} objects')
    for i, entry in enumerate(payload):
        where = f"--allow-edits[{i}]"
        if not isinstance(entry, dict):
            sys.exit(f"error: {where}: expected an object, got {type(entry).__name__}")
        missing = [k for k in ALLOW_EDIT_REQUIRED if k not in entry]
        unknown = [k for k in entry
                   if k not in ALLOW_EDIT_REQUIRED and k not in ALLOW_EDIT_OPTIONAL]
        if missing or unknown:
            sys.exit(f"error: {where}: missing {missing}, unknown {unknown}")
        if any(not isinstance(entry[k], str) or not entry[k] for k in ALLOW_EDIT_REQUIRED):
            sys.exit(f"error: {where}: chapter, old and new must be non-empty strings")
        if entry["old"] == entry["new"]:
            sys.exit(f"error: {where}: old and new are identical")
    return payload


def declared_edits(before_text: str, edits: list[dict]) -> tuple[str, list[str], int]:
    """Pre-apply the declared substitutions to the before text.

    Returns the patched text, the problems to report, and how many were applied.
    A declaration that matches exactly one span is applied and the hunk it
    describes then reads as no change at all; every other hunk still has to be
    an insertion. A declaration that matches none, or more than one, is reported
    and NOT applied, so the hunk it was meant to license fails the additive
    check: a declaration that does not name one sentence licenses nothing.

    Every span is located in the ORIGINAL text and the text is rebuilt in one
    pass. Sequential `str.replace` would depend on the order of the file
    whenever one substitution's `new` contains another's `old`, and would
    rewrite every occurrence of an `old` that is not unique.
    """
    problems: list[str] = []
    spans: list[tuple[int, int, str, str]] = []
    for entry in edits:
        found = before_text.count(entry["old"])
        if found != 1:
            problems.append(
                f"declared edit matches {found} span(s) of the before text, must "
                f"match exactly 1, so it licenses nothing — “{entry['old'][:60]}”"
            )
            continue
        start = before_text.index(entry["old"])
        spans.append((start, start + len(entry["old"]), entry["new"], entry["old"]))
    spans.sort()
    out: list[str] = []
    cursor = applied = 0
    for start, end, new, old in spans:
        if start < cursor:
            problems.append(
                f"declared edit overlaps another declaration, so neither is "
                f"applied — “{old[:60]}”"
            )
            continue
        out.append(before_text[cursor:start])
        out.append(new)
        cursor = end
        applied += 1
    out.append(before_text[cursor:])
    return "".join(out), problems, applied


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

# Token classes map to (additions_fatal, removals_fatal). Three further keys
# carry a policy's STRUCTURAL permissions, so that no check below tests a policy
# name and adding a pass means adding a row here and nothing else:
#
#   own_section_refs  §N / §N.M / Section N pointers into the chapter's own
#                     sections may be added (reported, targets verified)
#   code_byte_exact   fenced blocks must be byte-identical and in the same
#                     order; False means the additive branch (append only)
#   code_new_blocks   read with `code_byte_exact` True: the existing blocks are
#                     byte-identical and keep their relative order, and a NEW
#                     block may appear anywhere between them. The third code
#                     shape, for pass H, which inserts a covergroup mid-chapter
#                     and a block inside an exercise: neither is an append, so
#                     the `append only` branch rejects both.
#   additive_diff     G3's mechanical form runs: every hunk an insertion
#   g4_declared       growth past GROWTH_BLOCK is a note rather than a block,
#                     because the pass declares growth and its band is measured
#                     elsewhere (pass H: `check_register.py --band 0 0.15`)
#
# T4: `A` and `A1` were byte-identical tables whose one real difference was
# hard-coded in `check_chapter` as `policy == "A1"`, so the table lied about
# being the place where passes differ. It is now true.
POLICY = {
    "A": {
        "citations": (True, True),
        "numbers": (True, False),
        "crossrefs": (True, False),
        # A hedge added is conservative and safe; a hedge lost is a claim
        # strengthened, which is the measured, asymmetric failure.
        "hedges": (False, True),
        "spelled": (False, False),
        "own_section_refs": False,
        "code_byte_exact": True,
        "code_new_blocks": False,
        "additive_diff": False,
        "citations_set_level": False,
        "hedge_ledger": False,
        "g7_declared": False,
        "g4_declared": False,
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
        "own_section_refs": True,
        "code_byte_exact": True,
        "code_new_blocks": False,
        "additive_diff": False,
        "citations_set_level": False,
        "hedge_ledger": False,
        "g7_declared": False,
        "g4_declared": False,
    },
    "B": {
        "citations": (False, True),
        "numbers": (False, True),
        "crossrefs": (False, True),
        "hedges": (False, True),
        "spelled": (False, False),
        "own_section_refs": False,
        "code_byte_exact": False,
        "code_new_blocks": False,
        "additive_diff": True,
        "citations_set_level": False,
        "hedge_ledger": False,
        "g7_declared": False,
        "g4_declared": False,
    },
    # C — float captions and apparatus. Its contract says the pass "adds
    # caption lines and nothing else", which is B's shape exactly, so it takes
    # B's table including G3. T3: the module docstring and the style guide both
    # named C as a mechanically additive pass while `POLICY` had no C entry, so
    # `--policy C` was rejected by argparse and the pass ran with no gate at
    # all. A caption line inserted above a table is an `insert` hunk and passes;
    # rewording the sentence above it does not.
    "C": {
        "citations": (False, True),
        "numbers": (False, True),
        "crossrefs": (False, True),
        "hedges": (False, True),
        "spelled": (False, False),
        "own_section_refs": False,
        "code_byte_exact": False,
        "code_new_blocks": False,
        "additive_diff": True,
        "citations_set_level": False,
        "hedge_ledger": False,
        "g7_declared": False,
        "g4_declared": False,
    },
    # D — consolidation. A's table; the one difference is the level at which
    # citation removals are judged (see the docstring). The per-occurrence
    # tuple stays (True, True) so that the table still reads as "no citation
    # may go", and `citations_set_level` names the exception precisely: a
    # removal is fatal when the ID no longer appears anywhere in the chapter.
    "D": {
        "citations": (True, True),
        "numbers": (True, False),
        "crossrefs": (True, False),
        "hedges": (False, True),
        "spelled": (False, False),
        "own_section_refs": False,
        "code_byte_exact": True,
        "code_new_blocks": False,
        "additive_diff": False,
        "citations_set_level": True,
        "hedge_ledger": False,
        "g7_declared": False,
        "g4_declared": False,
    },
    # G — voice and slimming (W2). A1's table, because rule 2 of revision 4
    # ("explained once") replaces a re-explanation with a pointer into the
    # chapter's own sections and rule 1 reopens chapters on their object, so
    # "the opening scenario" becomes "the DMA bug of §1.4": an own-chapter
    # pointer is the shape of the pass and a pointer to another chapter is
    # still a claim about material the pass cannot see. Two cells differ from
    # A1. `hedges`: under A a hedge removed is fatal, and W2 measured two
    # legitimate edits that trip it: a sentence deleted because it duplicated a
    # claim still hedged in the surviving copy, and a `HEDGE_RE` false positive
    # ("about" as a preposition in "honest about this"). G2 asks that
    # "something must show" the claim became unconditional; under G that
    # something is the claim ledger the coordinator reads, which is why the
    # removal is a note naming the terms rather than a block. `crossrefs`: the
    # pass contract (G1d) forbids adding *or removing* a cross-reference, and
    # the table shipped with removals as a note, inherited from A1, where an
    # anecdotal opening may take its pointer with it. The Codex meta-review of
    # 2026-09-06 (S3) ran the probe — "Chapter 4 placed planning" became
    # "Earlier text placed planning" and passed with a note — so under G a
    # removed pointer to another chapter is fatal, like an added one.
    "G": {
        "citations": (True, True),
        "numbers": (True, False),
        "crossrefs": (True, True),
        "hedges": (False, False),
        "spelled": (False, False),
        "own_section_refs": True,
        "code_byte_exact": True,
        "code_new_blocks": False,
        "additive_diff": False,
        "citations_set_level": False,
        "hedge_ledger": True,
        "g7_declared": True,
        "g4_declared": False,
    },
    # I — clarity of sentence and lexicon (W6, `meta/passes/pass_i_clarity.md`
    # §7). G's frozen shape with one relaxation: a recall clause may carry a
    # pointer ("Chapter 11 defines assertions in full"), so cross-references
    # may be ADDED (target verified as for own-section pointers) and never
    # removed. Numbers stay (True, False): a gloss that brings a new figure is
    # a claim, not a clarification. No word band in either direction
    # (`g4_declared` True: growth is reported, not blocked); hedges and G7
    # remain ledger notes the coordinator answers line by line. Numbers are
    # (False, True): the lexicon of revision 6 repeats "2D row" and "4 KB
    # boundary" wherever a recall clause lands, and the tool reads those digits
    # as new quantities; so an ADDED number is a note the coordinator answers
    # (each must be a repetition of 2D, 4 KB or 256 already in the chapter),
    # while a REMOVED number stays fatal.
    "I": {
        "citations": (True, True),
        "numbers": (False, True),
        "crossrefs": (False, True),
        "hedges": (False, False),
        "spelled": (False, False),
        "own_section_refs": True,
        "code_byte_exact": True,
        "code_new_blocks": False,
        "additive_diff": False,
        "citations_set_level": False,
        "hedge_ledger": True,
        "g7_declared": True,
        "g4_declared": True,
    },
    # H — didactic apparatus (W3). B's additive shape with A's citation cell:
    # the pass adds exercises, figures, three code blocks, glossary rows and an
    # index, and `meta/passes/pass_h_didactic_apparatus.md` §1 forbids it any
    # source, so a citation may neither arrive nor go. `numbers` is (False,
    # True) and the addition is not even a note worth blocking on, because an
    # exercise statement is made of quantities and their provenance is
    # `check_exercises.py`'s subject (pass H §3): this tool cannot read the
    # example bank, so a number gate here would either block the pass or
    # pretend to check what it cannot see. `crossrefs` is (False, True) with
    # `own_section_refs`, so a solution may point into its chapter and the
    # heading is verified; the two cells that are H's own are `code_new_blocks`
    # (a covergroup lands inside §6.4, which is neither byte-identical nor an
    # append) and `g4_declared` (the pass grows the chapter by 5-12 % by
    # design, and §5.3 puts that band in `check_register.py --band 0 0.15`).
    "H": {
        "citations": (True, True),
        "numbers": (False, True),
        "crossrefs": (False, True),
        "hedges": (False, True),
        "spelled": (False, False),
        "own_section_refs": True,
        "code_byte_exact": True,
        "code_new_blocks": True,
        "additive_diff": True,
        "citations_set_level": False,
        "hedge_ledger": False,
        "g7_declared": False,
        "g4_declared": True,
    },
}

TOKEN_CLASSES = ("citations", "numbers", "crossrefs", "hedges", "spelled")

CHAPTER_NUM_RE = re.compile(r"ch0*(\d+)")


SECTION_HEADING_RE = re.compile(r"^#{2,4}\s+(\d+(?:\.\d+)+)\b", re.MULTILINE)

# The chapter's own top-level number — "# 3. The Verification Problem". A bare
# `§3` points at the chapter itself, and `SECTION_HEADING_RE` requires at least
# one dot, so without this the heading set never contains a dotless number and
# every bare own-chapter pointer would be reported as dangling for ever.
CHAPTER_HEADING_RE = re.compile(r"^#\s+(\d+)(?=[.\s])", re.MULTILINE)

# A section pointer in either of the two forms the manuscript uses: `§7`,
# `§7.4`, `§ 7.4`, `Section 7`, `Sections 7.4`.
#
# T5, twice over. The dot was mandatory — `(?:\.\d+)+` — so a bare `§7` was
# classified as a permitted own-chapter pointer under A1 and then skipped by the
# resolver, which reported "each target heading verified to exist" having
# verified nothing. And the `§` was mandatory, so `Section 7.4` inside ch07
# could never reach the resolver at all: it was classified foreign and failed
# for the wrong reason. The two spellings are the same pointer, and which one
# an editor types is not a policy question — so both are recognised, both are
# permitted under A1 only when they point into the chapter's own number, and
# both have their target heading checked. Fatality for a DANGLING pointer is
# unchanged; what changed is that a resolving `Section 7.4` in ch07 is now a
# note rather than a fatal foreign reference.
SECTION_REF_RE = re.compile(r"(?:§\s?|Sections?\s+)(\d+(?:\.\d+)*)")


def section_ref_number(token: str) -> str | None:
    """The section number a `§N[.M…]` / `Section N[.M…]` token points at."""
    m = SECTION_REF_RE.fullmatch(token.strip())
    return m.group(1) if m else None


def own_section_ref(token: str, chapter_name: str) -> bool:
    """True if `token` is a section pointer into `chapter_name`'s own sections."""
    m = CHAPTER_NUM_RE.fullmatch(chapter_name)
    num = section_ref_number(token)
    return bool(m and num and num.split(".")[0] == m.group(1))


def section_headings(path: Path) -> set[str]:
    """The section numbers that actually have a heading in this file.

    Includes the chapter's own number, from its `# N.` heading, so that a bare
    `§N` resolves to the chapter itself instead of dangling.
    """
    text = path.read_text(encoding="utf-8")
    return set(SECTION_HEADING_RE.findall(text)) | set(
        CHAPTER_HEADING_RE.findall(text)
    )


def unresolved_refs(tokens, headings: set[str]) -> list[str]:
    """Own-chapter section pointers with no matching heading.

    Checking the *form* of a permitted addition is not checking the addition.
    Without this, a chapter map full of pointers to sections that do not exist
    passes policy A1 with a reassuring "permitted for a chapter map" note — the
    exact shape of a gate that looks like it is working and is not.
    """
    bad: list[str] = []
    for tok in tokens:
        num = section_ref_number(tok)
        if num and num not in headings:
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


def frozen_g_units(text: str) -> list[tuple[str, str]]:
    """The apparatus pass G promises to leave byte-identical, as an ordered list.

    The pass contract says "tables, code, captions and diagrams stay
    byte-identical by construction" (G1c) and the brief repeats the promise,
    but until 2026-09-06 the gate compared only the *bodies* of fenced blocks:
    `split_code_blocks` drops the fence lines and their info string, and no
    check read a table row or a caption at all. The Codex meta-review (S1)
    mutated a table cell ("enabled" -> "disabled"), a caption ("Five DMA
    features" -> "Five GPU features") and a fence tag (systemverilog -> python)
    in copies of ch05 and policy G passed each one with no note. Every unit
    below is compared whole, line endings included:

    * ("fence", block)      the fenced block with its delimiters and info string
    * ("table_row", line)   any line starting with `|`
    * ("caption", line)     a float caption, `{table: id} ...`, single or double
                            braces, one physical line by the manuscript's rule
    * ("ref", token)        every `{ref: id}` token in prose, in order

    A leading `> ` is stripped before classifying, so the same table inside a
    scenario box is still a table. An unterminated fence raises ValueError,
    because a chapter that does not parse cannot be certified unchanged. The
    binding of a ref token to its claim stays a human obligation.
    """
    units: list[tuple[str, str]] = []
    marker = ""
    block: list[str] = []
    for raw in text.splitlines(keepends=True):
        visible = re.sub(r"^\s*> ?", "", raw)
        fence = FENCE_RE.match(visible)
        if marker:
            block.append(raw)
            if (fence and fence.group(2)[0] == marker[0]
                    and len(fence.group(2)) >= len(marker)
                    and not fence.group(3).strip()):
                units.append(("fence", "".join(block)))
                marker, block = "", []
            continue
        if fence and "`" not in fence.group(3):
            marker, block = fence.group(2), [raw]
        elif re.match(r"^\s*\|", visible):
            units.append(("table_row", raw))
        elif re.match(r"^\s*\{\{?(?:table|figure|listing):", visible):
            units.append(("caption", raw))
        else:
            for match in re.finditer(r"\{\{?ref:[^{}\n]+\}\}?", raw):
                units.append(("ref", match.group()))
    if marker:
        raise ValueError("unterminated frozen fence")
    return units


def check_chapter(name: str, before: Path, after: Path, policy: str,
                  allow_edits: list[dict] | None = None) -> dict:
    b, a = extract(before), extract(after)
    findings: list[str] = []
    notes: list[str] = []
    rules = POLICY[policy]
    if policy == "G":
        # G1c/G1d as bytes, not as token counts: see `frozen_g_units`.
        try:
            frozen_b = frozen_g_units(before.read_text(encoding="utf-8"))
            frozen_a = frozen_g_units(after.read_text(encoding="utf-8"))
        except ValueError as exc:
            findings.append(f"G1c: {exc}")
        else:
            if frozen_b != frozen_a:
                changed = [
                    kind for (kind, _), (kind_a, _) in zip(frozen_b, frozen_a) if kind != kind_a
                ] or sorted({k for k, _ in set(frozen_b) ^ set(frozen_a)})
                findings.append(
                    "G1c/G1d: frozen apparatus or ref tokens changed "
                    f"({len(frozen_b)} -> {len(frozen_a)} unit(s); kinds: {', '.join(changed) or 'same kinds, different bytes'})"
                )

    for cls in TOKEN_CLASSES:
        added, removed = counter_delta(b[cls], a[cls])
        add_fatal, rem_fatal = rules[cls]
        if added:
            if cls == "crossrefs" and rules["own_section_refs"]:
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
                    # Fatality follows the table's `crossrefs` addition cell, as
                    # it does in the branch below. Under A1 and G that cell is
                    # True and the finding is unchanged; under H, which may add
                    # a pointer, it is a note. The message is the same either
                    # way: what changed is where it is routed.
                    line = (f"crossrefs: +{sum(foreign.values())} added outside this "
                            f"chapter [{fmt_counter(foreign)}]")
                    (findings if add_fatal else notes).append(line)
                added = foreign
            else:
                line = f"{cls}: +{sum(added.values())} added [{fmt_counter(added)}]"
                (findings if add_fatal else notes).append(line)
        if removed and cls == "hedges" and rules["hedge_ledger"]:
            # Pass G: the removal is reported with the terms and routed to the
            # ledger, because what makes it legitimate — the claim is still
            # hedged in a surviving copy, or the match was a false positive —
            # is not visible to a count over the chapter.
            notes.append(
                f"hedges: -{sum(removed.values())} removed "
                f"[{fmt_counter(removed)}] — declare in the claim ledger: for "
                "each term, the claim it qualified is still hedged elsewhere, "
                "the match was a false positive, or the claim is now unconditional"
            )
        elif removed and cls == "citations" and rules["citations_set_level"]:
            # Pass D: judge the removal on the set of IDs, not on occurrences.
            vanished = Counter({k: v for k, v in removed.items() if a[cls][k] == 0})
            duplicates = removed - vanished
            if vanished:
                findings.append(
                    f"citations: {len(vanished)} ID(s) vanished from the chapter "
                    f"[{fmt_counter(vanished)}]"
                )
            if duplicates:
                notes.append(
                    f"citations: -{sum(duplicates.values())} duplicate occurrence(s) "
                    f"removed, every ID still cited [{fmt_counter(duplicates)}]"
                )
        elif removed:
            line = f"{cls}: -{sum(removed.values())} removed [{fmt_counter(removed)}]"
            (findings if rem_fatal else notes).append(line)

    # Code blocks: order-sensitive and byte-exact. Passes B and C may append
    # blocks. A1 is a Pass A variant and takes Pass A's strict branch: its
    # contract says code blocks are byte-identical, and an `in ("A",)` test
    # silently gave A1 the additive branch, where an appended block was only a
    # note. Which branch applies is now a column of the policy table.
    if rules["code_new_blocks"]:
        # H — the third shape: every existing block byte-identical and in its
        # relative order, a new block anywhere between them.
        touched = code_insertions_only(b["code"], a["code"])
        if touched:
            findings.append(
                f"code: {'; '.join(touched)} "
                f"(Pass {policy} may add a block, not change one)"
            )
        elif len(a["code"]) > len(b["code"]):
            notes.append(f"code: +{len(a['code']) - len(b['code'])} block(s) added")
    elif rules["code_byte_exact"]:
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
            findings.append(
                f"code: existing blocks modified or reordered "
                f"(Pass {policy} is additive)"
            )
        elif len(a["code"]) > len(b["code"]):
            notes.append(f"code: +{len(a['code']) - len(b['code'])} block(s) appended")

    for term in WATCH_VOCAB:
        d = a["vocab"][term] - b["vocab"][term]
        if d:
            line = f"vocab '{term}': {b['vocab'][term]} -> {a['vocab'][term]} ({d:+d})"
            (findings if term in STRICT_VOCAB else notes).append(line)

    # G3 — additive-only diff. Applies to the byte-additive passes only (B, C);
    # a rewriting pass needs an approved span list this tool does not hold.
    if rules["additive_diff"]:
        before_text = before.read_text(encoding="utf-8")
        declared = [e for e in (allow_edits or []) if e["chapter"] == name]
        if declared:
            before_text, problems, applied = declared_edits(before_text, declared)
            findings.extend(f"G3 declaration: {problem}" for problem in problems)
            if applied:
                notes.append(
                    f"G3: {applied} declared substitution(s) applied to the before "
                    "text; every other hunk still has to be an insertion"
                )
        viol = additive_violations(before_text, after.read_text(encoding="utf-8"))
        for v in viol:
            findings.append(f"G3 not additive: {v}")

    # G4 — length delta.
    ratio = (a["words"] / b["words"]) if b["words"] else 1.0
    growth = ratio - 1.0
    if growth >= GROWTH_BLOCK and rules["g4_declared"]:
        # Pass H: growth is the pass. Four to six exercises, a figure caption
        # and a solution pointer are 5-12 % of a chapter, and the contract puts
        # that band in the register gate (§5.3), one tool with one number,
        # rather than in a 5 % block here that would fail every chapter.
        notes.append(
            f"G4 length: {b['words']} -> {a['words']} words ({growth:+.1%}); "
            f"Pass {policy} declares growth — the band is measured by "
            "`check_register.py --before … --band 0 0.15`"
        )
    elif growth >= GROWTH_BLOCK:
        findings.append(
            f"G4 length: {b['words']} -> {a['words']} words ({growth:+.1%}); "
            f"Pass {policy} must not pad — growth above {GROWTH_BLOCK:.0%} blocks"
        )
    elif growth >= GROWTH_ALARM:
        notes.append(f"G4 length: {b['words']} -> {a['words']} words ({growth:+.1%})")

    # G7 — largest single contiguous deletion.
    lost, excerpt = largest_deletion(b["prose_words"], a["prose_words"])
    if lost >= DELETION_BLOCK and rules["g7_declared"]:
        # Pass G: merging two paragraphs, or dropping a re-derivation another
        # chapter owns, passes 120 contiguous words as a matter of routine.
        # Whether the content survives elsewhere is not a property of the
        # chapter's word list, so the figure is reported and the justification
        # is owed to the ledger rather than to this tool.
        notes.append(
            f"G7 deletion: largest single deletion is {lost} words, at "
            f"“{excerpt} …” — above {DELETION_BLOCK}: declare in the claim "
            "ledger: what the deleted passage carried and where it survives"
        )
    elif lost >= DELETION_BLOCK:
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
    # T6 — a snapshot written into a directory that already holds one silently
    # mixes two pre-pass states: `shutil.copy2` overwrites the chapters named on
    # this invocation and leaves every other file from the older snapshot in
    # place, so a `--chapters ch04` snapshot taken into last week's full
    # snapshot yields a "before" that is 27 chapters old and one chapter new,
    # and every later check compares against the mixture without complaint.
    # The failure is invisible because the copy succeeds.
    if dest.exists() and not dest.is_dir():
        sys.exit(f"error: snapshot destination exists and is not a directory: {dest}")
    if dest.is_dir() and any(dest.iterdir()) and not args.force:
        sys.exit(
            f"error: snapshot destination is not empty: {dest}\n"
            "       Writing here would mix two pre-pass states and every later\n"
            "       check would compare against the mixture. Use a new directory,\n"
            "       or pass --force to overwrite this one deliberately."
        )
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
    # Resolved against ROOT, like --before and --after and unlike --json.
    allow_edits = load_allow_edits(ROOT / args.allow_edits) if args.allow_edits else []
    if allow_edits and not POLICY[args.policy]["additive_diff"]:
        # The declaration licenses hunks inside the additive diff and nothing
        # else, so under a policy that does not run one it is inert — and an
        # inert declaration read as permission is how a rewriting pass ships
        # with a file that says it was allowed.
        sys.exit(f"error: --allow-edits licenses hunks in the additive diff, "
                 f"which policy {args.policy} does not run")
    results = []
    for f in chapter_files(before_dir, args.chapters):
        after = after_dir / f.name
        if not after.exists():
            results.append(
                {"chapter": f.stem, "status": "FAIL", "findings": ["file missing in after/"],
                 "notes": [], "words_before": 0, "words_after": 0}
            )
            continue
        results.append(check_chapter(f.stem, f, after, args.policy, allow_edits))

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
    s.add_argument(
        "--force",
        action="store_true",
        help="write into a non-empty destination (mixes two pre-pass states)",
    )
    s.set_defaults(func=cmd_snapshot)

    c = sub.add_parser("check", help="diff a snapshot against the working tree")
    c.add_argument("--before", required=True)
    c.add_argument("--after", default="book")
    c.add_argument("--policy", required=True, choices=sorted(POLICY))
    c.add_argument("--chapters", nargs="*")
    c.add_argument("--json")
    c.add_argument(
        "--allow-edits",
        help='JSON list of declared substitutions, [{"chapter": "ch12", "old": '
             '"…exact sentence…", "new": "…sentence with {ref: label}…"}], each '
             "the one hunk of that chapter the additive diff may see as a change "
             "(path relative to the repository root, like --before)",
    )
    c.set_defaults(func=cmd_check)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
