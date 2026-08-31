#!/usr/bin/env python3
"""Register triage scanner: find CANDIDATE spans, per section, for Pass A.

    python3 tools/register_scan.py --book book --out meta/audits/register_candidates

This is a **triage instrument, not a gate and not an authority**.  Its property
is high recall and unknown precision.  A hit is a place worth a reader's
attention; it is not a violation.  Every pattern here matches a *string*, while
the defect is a *use*, and the two come apart badly in this book: `manager` is
AMBA AXI terminology (manager/subordinate replaced master/slave), `always` is
normative specification language, and a question the text answers with evidence
is legitimate monograph prose.

Consequences, which the calling protocol must honour:

  * A candidate never authorises an edit.  It enters a LOCALISE agent's input as
    a hint that must be confirmed or rejected with a reason.
  * A class whose hand-verified precision is below ~0.8 on its first 30 hits is
    demoted to hint-only and may not narrow anyone's reading.
  * Zero candidates in a section is the useful signal: it routes the section to
    the cheap "untouched, two rules named" verdict path instead of the expensive
    three-vote pipeline.

Fenced code blocks are excluded from scanning.  A hit whose sentence also
carries a `[cit:ID]` marker is flagged `near_citation`, because the wording may
be a source's rather than the book's.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# --------------------------------------------------------------------------
# Pattern classes.
#
# Authored from the register defects actually measured in this manuscript, not
# from generic style-guide class names.  Each entry is
# (class_name, compiled_regex, note_on_expected_false_positives).
# --------------------------------------------------------------------------

CLASSES: dict[str, tuple[re.Pattern[str], str]] = {
    # The defect the author actually reacted to: verification argued in the
    # register of a business case rather than of an engineering result.
    "business-register": (
        re.compile(
            r"\b(?:"
            r"schedule return|return on (?:the )?(?:verification |investment|effort)"
            r"|business case|cost[- ]benefit|headcount|budget(?:ary)?"
            r"|stakeholder|executive|the VP\b|C-level|management (?:buy-in|attention)"
            r"|bang for|pays for itself|justif(?:y|ies|ying) the (?:cost|spend|investment)"
            r")\b",
            re.IGNORECASE,
        ),
        "low false-positive rate expected; 'budget' is also a legitimate "
        "engineering word (power budget, error budget, deletion budget)",
    ),
    # Narrated scenes standing in for an argument.
    "meeting-vignette": (
        re.compile(
            r"\b(?:"
            r"in the (?:review|meeting|room)|the room (?:goes|falls|is)"
            r"|someone (?:asks|says|points out|objects)"
            r"|walks? (?:the team )?through|on the call|around the table"
            r"|the (?:review|meeting) (?:opens|begins|starts|ends)"
            r")\b",
            re.IGNORECASE,
        ),
        "expected clean; 'in the review' may also name a process step",
    ),
    # Second-person coaching and exhortation.
    "second-person-coaching": (
        re.compile(
            r"\b(?:"
            r"you (?:will |should |must |need to |want to |can )?(?:learn|remember|see that)"
            r"|your team|your (?:job|task) is|let(?:'|’)s\b"
            r"|don(?:'|’)t be|do not be tempted|resist the urge"
            r"|keep in mind|bear in mind"
            r")\b",
            re.IGNORECASE,
        ),
        "the book uses 'you' legitimately in some procedural passages; "
        "hits need reading",
    ),
    # Textbook scaffolding.  Split after hand-classification: the header block
    # is a systematic defect at precision ~1.0, while `in this chapter` used as
    # a referring phrase is legitimate and measured ~0.2.
    "learn-header": (
        re.compile(
            r"^\*\*What you will learn.*?:\*\*\s*$"
            r"|\bwhat you will learn\b"
            r"|\bby the end of this (?:chapter|section)\b",
            re.IGNORECASE,
        ),
        "MEASURED ~1.0. Systematic: the style guide's revision-2 skeleton "
        "replaces this block with an opening problem statement plus a chapter map",
    ),
    "chapter-reference": (
        re.compile(
            r"\b(?:"
            r"in this (?:chapter|section)|this (?:chapter|section) will"
            r"|we will (?:see|examine|look at|cover)|as we (?:shall |will )?see"
            r")\b",
            re.IGNORECASE,
        ),
        "MEASURED ~0.2 -> hint-only. A chapter map is legitimate; a promise "
        "of future reading is not, and the regex cannot tell them apart",
    ),
    # Intensifiers doing the work a quantity should do.  Two refinements after
    # hand-classification: `the very X` is an intensive determiner and is
    # precise, not vague, so it is excluded; `as a matter of course` is an idiom
    # and is not the `of course` defect.
    "vague-intensifier": (
        re.compile(
            r"(?<!the )\b(?:"
            r"very|extremely|hugely|dramatically|massively|incredibly|enormously"
            r"|vastly|tremendously|wildly|astonishingly"
            r"|obviously|clearly|needless to say|quite simply"
            r")\b"
            r"|(?<!as a matter )\bof course\b",
            re.IGNORECASE,
        ),
        "MEASURED 4/16 -> hint-only. Survivors are dominated by intensifiers "
        "belonging to cited sources, which may not be tightened",
    ),
    # Folklore standing in for evidence.
    "folklore": (
        re.compile(
            r"\b(?:"
            r"the (?:hard )?(?:reality|truth) is|in the real world|war stor(?:y|ies)"
            r"|rule of thumb|conventional wisdom|folklore|old hands"
            r"|everyone knows|it is well known"
            r")\b",
            re.IGNORECASE,
        ),
        "'rule of thumb' may be attributed to a source, in which case it is "
        "reported not asserted",
    ),
    # Reported speech.
    "dialogue": (
        re.compile(
            r"(?:”|\")\s*,?\s*(?:said|asks|asked|replies|replied|answers|answered)\b"
            r"|\b(?:said|asks|asked|replies|replied)\s*,?\s*(?:“|\")",
        ),
        "expected clean",
    ),
    # Imperative openers.
    "hortatory-opener": (
        re.compile(
            r"^(?:Remember|Never|Always|Do not|Don(?:'|’)t|Beware|Note)\b",
        ),
        "HIGH false-positive risk: 'Never'/'Always' are normative "
        "specification language and appear inside quoted clauses",
    ),
    # Questions in body prose.
    "rhetorical-question": (
        re.compile(r"\?(?:\s|$)"),
        "HIGH false-positive risk: a question the text then answers with "
        "evidence is legitimate monograph prose; expected to fail precision",
    ),
}

CITATION_RE = re.compile(r"\[cit:[A-Za-z0-9_.-]+\]")
HEADING_RE = re.compile(r"^(#{2,4})\s+(.*?)\s*$")
FENCE_RE = re.compile(r"^\s*(?:```|~~~)")

# --------------------------------------------------------------------------
# Structural detector: the chapter opening.
#
# The defect the author named — "you keep referring to managers, the tone is
# simplistic" — is not a string that appears throughout the prose.  It is a
# *structure*: the chapter opens with a narrated scene in which a person, often
# a manager, asks a question.  No line-level regex finds this, because each
# individual sentence is unobjectionable.  So this detector works on the first
# body paragraph of a chapter and reports the scene markers it carries.
#
# It reports markers, not a verdict.  "Is this opening a scene or a problem
# statement?" is a judgement, and the routing protocol requires that judgement
# to be made and recorded by a named human or agent, not inferred from a count.
# --------------------------------------------------------------------------

OPENING_MARKERS: dict[str, re.Pattern[str]] = {
    # A scene needs a time and a place.  A problem statement does not.
    "clock-or-calendar": re.compile(
        r"^(?:Month|Week|Day)\s+\w+|^(?:Monday|Tuesday|Wednesday|Thursday|Friday"
        r"|Saturday|Sunday)\b|\b\d{1,2}:\d{2}\b"
        r"|^(?:Eleven|Ten|Nine|Eight|Seven|Six|Five|Four|Three|Two|One|A few)\s+"
        r"(?:days?|weeks?|months?|hours?)\b",
        re.IGNORECASE,
    ),
    # A job title used as a narrative device rather than as a role in a process.
    "job-title-as-actor": re.compile(
        r"\b(?:project|program|programme|engineering)\s+manager\b"
        r"|\bthe (?:verification|design|project) lead\b"
        r"|\bassessor\b|\bthe room\b|\baround the table\b",
        re.IGNORECASE,
    ),
    # Reported speech in an opening is theatre by construction.
    "quoted-speech": re.compile(r"[“\"][^”\"]{8,}[”\"]"),
    # Interior states: the tell of a vignette.
    "interior-state": re.compile(
        r"\b(?:her|his|their) gut\b|\bis confident\b|\bsounds reasonable\b"
        r"|\bknows every corner\b|\bnobody had imagined\b|\bwith a highlighter\b"
        r"|\beveryone has been waiting\b|\bhallway confidence\b",
        re.IGNORECASE,
    ),
}


@dataclass
class Opening:
    chapter: str
    line: int
    markers: dict[str, list[str]]
    excerpt: str

    @property
    def marker_count(self) -> int:
        return len(self.markers)


def find_opening(path: Path) -> Opening | None:
    """Return the chapter's first body paragraph and the scene markers in it."""
    lines = path.read_text(encoding="utf-8").splitlines()
    in_fence = False
    for lineno, raw in enumerate(lines, start=1):
        if FENCE_RE.match(raw):
            in_fence = not in_fence
            continue
        if in_fence or not raw.strip():
            continue
        if raw.startswith("#") or raw.startswith(">"):
            continue
        if raw.lstrip().startswith(("-", "*", "|")):
            continue
        markers = {
            name: sorted({m.group(0).strip() for m in pat.finditer(raw)})
            for name, pat in OPENING_MARKERS.items()
            if pat.search(raw)
        }
        return Opening(
            chapter=path.stem,
            line=lineno,
            markers=markers,
            excerpt=raw[:180],
        )
    return None


@dataclass
class Hit:
    chapter: str
    section: str
    line: int
    cls: str
    matched: str
    context: str
    near_citation: bool

    def as_dict(self) -> dict[str, object]:
        return {
            "chapter": self.chapter,
            "section": self.section,
            "line": self.line,
            "class": self.cls,
            "matched": self.matched,
            "context": self.context,
            "near_citation": self.near_citation,
        }


@dataclass
class SectionStat:
    chapter: str
    section: str
    start_line: int
    words: int = 0
    hits: list[Hit] = field(default_factory=list)

    @property
    def density(self) -> float:
        return 1000.0 * len(self.hits) / self.words if self.words else 0.0


def scan_chapter(path: Path) -> tuple[list[Hit], list[SectionStat]]:
    """Scan one chapter, returning hits and per-section statistics."""
    lines = path.read_text(encoding="utf-8").splitlines()
    chapter = path.stem

    hits: list[Hit] = []
    sections: list[SectionStat] = []
    current = SectionStat(chapter=chapter, section="(front)", start_line=1)
    in_fence = False

    for lineno, raw in enumerate(lines, start=1):
        if FENCE_RE.match(raw):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        heading = HEADING_RE.match(raw)
        if heading:
            if current.words or current.hits:
                sections.append(current)
            current = SectionStat(
                chapter=chapter, section=heading.group(2), start_line=lineno
            )
            # Headings are not prose and are not scanned for register defects —
            # with one exception.  `learn-header` is a defect *of the skeleton*,
            # and this manuscript expresses it two ways: as a bold paragraph in
            # five chapters and as an `##` heading in twenty-one.  Skipping
            # headings hid four fifths of it.
            for cls in ("learn-header",):
                pattern, _ = CLASSES[cls]
                for m in pattern.finditer(heading.group(2)):
                    hit = Hit(
                        chapter=chapter,
                        section=heading.group(2),
                        line=lineno,
                        cls=cls,
                        matched=m.group(0).strip(),
                        context=raw.strip() + "   [as a heading]",
                        near_citation=False,
                    )
                    hits.append(hit)
                    current.hits.append(hit)
            continue

        current.words += len(raw.split())
        if not raw.strip():
            continue

        near_cit = bool(CITATION_RE.search(raw))
        for cls, (pattern, _note) in CLASSES.items():
            for m in pattern.finditer(raw):
                start = max(0, m.start() - 60)
                end = min(len(raw), m.end() + 60)
                hit = Hit(
                    chapter=chapter,
                    section=current.section,
                    line=lineno,
                    cls=cls,
                    matched=m.group(0).strip(),
                    context=raw[start:end].strip(),
                    near_citation=near_cit,
                )
                hits.append(hit)
                current.hits.append(hit)

    if current.words or current.hits:
        sections.append(current)
    return hits, sections


def render_openings(openings: list[Opening]) -> list[str]:
    out: list[str] = []
    out.append("## Chapter openings: scene markers")
    out.append("")
    out.append(
        "Structural detector, not a line pattern. Reports markers, never a "
        "verdict: whether an opening is a narrated scene or a problem "
        "statement is a judgement that must be made and recorded by a named "
        "reviewer. Chapters are ordered by marker count, so the queue is "
        "read top-down."
    )
    out.append("")
    out.append("| chapter | line | markers | evidence |")
    out.append("|---|---|---|---|")
    for op in sorted(openings, key=lambda o: (-o.marker_count, o.chapter)):
        if not op.markers:
            continue
        names = ", ".join(f"`{k}`" for k in op.markers)
        ev = "; ".join(
            f"{k}: " + ", ".join(f'"{v}"' for v in vals)
            for k, vals in op.markers.items()
        ).replace("|", "\\|")
        out.append(f"| {op.chapter} | {op.line} | {names} | {ev} |")
    out.append("")
    zero = [o.chapter for o in sorted(openings, key=lambda o: o.chapter) if not o.markers]
    out.append(
        f"Openings with no scene marker (**{len(zero)}**): "
        + (", ".join(f"`{c}`" for c in zero) if zero else "—")
    )
    out.append("")
    return out


def render_report(
    all_hits: list[Hit], all_sections: list[SectionStat],
    openings: list[Opening] | None = None,
) -> str:
    out: list[str] = []
    out.append("# Register triage: candidate spans")
    out.append("")
    out.append(
        "Produced by `tools/register_scan.py`. **Candidates, not violations.** "
        "A hit matches a string; the defect is a use. No hit authorises an "
        "edit; each enters a LOCALISE agent's input as a hint to confirm or "
        "reject with a reason."
    )
    out.append("")

    if openings:
        out.extend(render_openings(openings))

    out.append("## Hits per class")
    out.append("")
    out.append("| class | hits | near citation | expected false positives |")
    out.append("|---|---|---|---|")
    for cls, (_pattern, note) in CLASSES.items():
        cls_hits = [h for h in all_hits if h.cls == cls]
        near = sum(1 for h in cls_hits if h.near_citation)
        out.append(f"| `{cls}` | {len(cls_hits)} | {near} | {note} |")
    out.append("")

    clean = [s for s in all_sections if not s.hits and s.words >= 50]
    dirty = sorted(all_sections, key=lambda s: -len(s.hits))
    out.append("## Routing")
    out.append("")
    out.append(
        f"- sections scanned: **{len(all_sections)}**  \n"
        f"- zero-candidate sections (>= 50 words): **{len(clean)}** "
        "-> cheap verdict path (untouched, two rules named), with fresh-agent "
        "re-inventory of a fixed fraction  \n"
        f"- sections with candidates: **{len([s for s in all_sections if s.hits])}** "
        "-> three-vote LOCALISE pipeline"
    )
    out.append("")

    out.append("## Densest sections (candidates per 1000 words)")
    out.append("")
    out.append("| chapter | section | words | hits | per 1k |")
    out.append("|---|---|---|---|---|")
    for s in dirty[:40]:
        if not s.hits:
            break
        out.append(
            f"| {s.chapter} | {s.section} | {s.words} | {len(s.hits)} | "
            f"{s.density:.1f} |"
        )
    out.append("")

    out.append("## All candidates, by chapter")
    out.append("")
    for chapter in sorted({h.chapter for h in all_hits}):
        out.append(f"### {chapter}")
        out.append("")
        out.append("| line | class | matched | cit? | context |")
        out.append("|---|---|---|---|---|")
        for h in [x for x in all_hits if x.chapter == chapter]:
            ctx = h.context.replace("|", "\\|")
            out.append(
                f"| {h.line} | `{h.cls}` | `{h.matched}` | "
                f"{'yes' if h.near_citation else ''} | {ctx} |"
            )
        out.append("")
    return "\n".join(out) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--book", default=str(ROOT / "book"))
    ap.add_argument("--out", default=str(ROOT / "meta/audits/register_candidates"))
    ap.add_argument("--chapters", nargs="*", default=None)
    args = ap.parse_args()

    book = Path(args.book)
    paths = sorted(book.glob("*.md"))
    if args.chapters:
        wanted = set(args.chapters)
        paths = [p for p in paths if p.stem in wanted]

    all_hits: list[Hit] = []
    all_sections: list[SectionStat] = []
    openings: list[Opening] = []
    for path in paths:
        hits, sections = scan_chapter(path)
        all_hits.extend(hits)
        all_sections.extend(sections)
        opening = find_opening(path)
        if opening is not None:
            openings.append(opening)

    out_base = Path(args.out)
    out_base.parent.mkdir(parents=True, exist_ok=True)
    out_base.with_suffix(".json").write_text(
        json.dumps([h.as_dict() for h in all_hits], indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    out_base.with_suffix(".md").write_text(
        render_report(all_hits, all_sections, openings), encoding="utf-8"
    )

    print(f"[scan] {len(paths)} chapter(s), {len(all_sections)} section(s)")
    print(f"[scan] {len(all_hits)} candidate(s)")
    for cls in CLASSES:
        n = sum(1 for h in all_hits if h.cls == cls)
        near = sum(1 for h in all_hits if h.cls == cls and h.near_citation)
        print(f"         {cls:26s} {n:5d}  ({near} near a citation)")
    print(f"[scan] wrote {out_base.with_suffix('.md')}")
    print(f"[scan] wrote {out_base.with_suffix('.json')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
