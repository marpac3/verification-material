"""Static book metadata: title page, parts, chapter->part map, apparatus headings.

Everything a human may want to retune without touching build logic lives here.
"""

from __future__ import annotations

import datetime as _dt

# --- Title page ------------------------------------------------------------

BOOK_TITLE_MAIN = "Hardware Verification"
BOOK_TITLE_SUB = "A Holistic Guide"
BOOK_TITLE_FULL = f"{BOOK_TITLE_MAIN}: {BOOK_TITLE_SUB}"
AUTHOR = "Marco Paci · Fondazione Chips-IT"

# The date on the title page and in the PDF's CreationDate is the date of the
# build, not a constant someone remembers to bump.  It was a constant, and it
# said 2026-08-27 on a book rebuilt in September: a hand-maintained date is a
# claim about the artefact that nothing checks.  The cost is that two builds on
# different days differ by these bytes; the docstring's "same inputs -> same
# bytes" is therefore a statement about a single day.
DATE = _dt.date.today().isoformat()

# The edition statement.  It belongs to the subtitle, which is where a title
# page names what this printing is (see subtitle_for below), and it is written
# once so the cover, the copyright verso and the PDF's Subject cannot drift
# apart.  A build that does not cover every part is a working draft and does
# not carry it.
EDITION = "First edition, September 2026"

# The line under the date on the title page, and the tail of the PDF's Subject.
# It used to read "Draft for internal review — citations verified against
# full-text corpus": the first half outlived the decision it described, since
# the book is released under CC BY-NC-SA 4.0 (see LICENSE and
# front/copyright.md) and nothing about it is internal any more.  The second
# half is the claim worth making on a cover, so it is what remains.
CORPUS_NOTE = "Citations verified against the full-text corpus"

# --- Design ----------------------------------------------------------------

ACCENT = "#2c4f8c"

# --- Parts -----------------------------------------------------------------
# Descriptions are quoted verbatim from meta/outline_master.md (Italian in the
# source outline; kept unchanged rather than silently translated).

PARTS = {
    1: {
        "id": "part-1",
        "title": "Part I — Foundations",
        "description": (
            "Why verification exists, how a verifier thinks, and why the "
            "problem is formally impossible — so it is managed as risk."
        ),
    },
    2: {
        "id": "part-2",
        "title": "Part II — Planning and Measurement",
        "description": (
            "The plan as a contract and measurement as ground truth: "
            "without these two, verification is opinion."
        ),
    },
    3: {
        "id": "part-3",
        "title": "Part III — Dynamic Verification",
        "description": (
            "The simulation core: testbench architecture, stimulus, UVM as a "
            "methodology rather than an API, assertions, and the engineering "
            "of regression."
        ),
    },
    4: {
        "id": "part-4",
        "title": "Part IV — Static and Formal",
        "description": (
            "Proving instead of sampling: from the static entry gate to model "
            "checking, the industrialised formal applications, and the hybrid "
            "flows that make one campaign of both."
        ),
    },
    5: {
        "id": "part-5",
        "title": "Part V — Beyond RTL Simulation",
        "description": (
            "What to do when the simulator runs out of cycles: acceleration "
            "and emulation, prototypes running real firmware, verification "
            "after synthesis, and the first encounter with real silicon."
        ),
    },
    6: {
        "id": "part-6",
        "title": "Part VI — Specialized Domains",
        "description": (
            "The obligations a market imposes: where the digital abstraction "
            "meets the continuous world, what changes when a standard is "
            "watching, and how to verify against an adversary."
        ),
    },
    7: {
        "id": "part-7",
        "title": "Part VII — The Human and the Machine",
        "description": (
            "The people, the process, and the machine: how verification teams "
            "are built, what automation is actually delivering, and where the "
            "discipline is going."
        ),
    },
}

CHAPTER_PART = {
    "ch01": 1,
    "ch02": 1,
    "ch03": 1,
    "ch04": 1,
    "ch05": 2,
    "ch06": 2,
    "ch07": 2,
    "ch08": 3,
    "ch09": 3,
    "ch10": 3,
    "ch11": 3,
    "ch12": 3,
    "ch13": 4,
    "ch14": 4,
    "ch15": 4,
    "ch16": 4,
    "ch17": 5,
    "ch18": 5,
    "ch19": 5,
    "ch20": 5,
    "ch21": 6,
    "ch22": 6,
    "ch23": 6,
    "ch24": 7,
    "ch25": 7,
    "ch26": 7,
}

# --- Chapter apparatus -----------------------------------------------------
# Headings normalised to level 3 so that: # = chapter, ## = numbered section,
# ### = apparatus.  Matching is case-insensitive on the stripped heading text.
# NOTE: "What you will learn" is deliberately NOT in this list -- it is a `##`
# section in ch02/ch06/ch07 and absent elsewhere; promoting it would change the
# author-visible structure of three chapters.  One-line change if wanted.

APPARATUS_HEADINGS = (
    # The chapter map is navigation, not a section of the argument, so it is
    # apparatus like the closing summary: forced to level 3 and kept out of the
    # table of contents, where 26 "Chapter map" entries would be pure noise.
    "chapter map",
    "in practice",
    "pitfalls",
    # "key takeaways" is the pre-revision-2 name; "summary" is the monograph
    # word the style guide now specifies. Both are listed so a build during the
    # rename does not silently drop a chapter's closing heading to level 2.
    "key takeaways",
    "summary",
    # Pass H (W3) adds one "### Exercises" section per chapter, between the
    # summary and the further reading. It is apparatus for the same reason the
    # summary is: it closes the chapter rather than advancing its argument, and
    # 26 "Exercises" rows would double the table of contents' apparatus noise.
    # Listing it here is also what makes the heading's level *stable*: a chapter
    # that wrote "## Exercises" by hand would otherwise ship a level-2 heading
    # that build_book.py's `entry.level == 2` filter puts straight into the
    # contents, so the omission would not fail — it would silently publish.
    "exercises",
    "further reading",
    "references",
)

REFERENCES_HEADING = "References"
FURTHER_READING_HEADING = "further reading"

# --- Appendix --------------------------------------------------------------

GLOSSARY_TITLE = "Appendix A — Glossary"
GLOSSARY_ID = "appendix-a"
GLOSSARY_NOTE = (
    "Terms appear broadly in the order the book introduces them, except that "
    "entries the book deliberately contrasts are kept side by side — the pairs "
    "where one word carries a different sense in design and in verification are "
    "the reason this glossary exists, and separating them would hide exactly "
    "what the reader came to check. The *Introduced* column names the chapter "
    "that owns the definition, which is not always the chapter of first mention: "
    "a term is often used in passing well before the chapter that pins it down."
)

TOC_TITLE = "Contents"
LIST_OF_FIGURES_TITLE = "Figures"
LIST_OF_TABLES_TITLE = "Tables"

# Front-matter pages, in the order a monograph sets them: the verso copyright
# page, then contents and the lists of floats (inserted by the builder), then
# the preface, then the notation and conventions the reader needs before
# Chapter 1. Each is a markdown file in front/, whose own level-1 heading
# supplies its title.
FRONT_MATTER_AFTER_LISTS = ("preface", "notation")

# --- Derived subtitle ------------------------------------------------------
# The subtitle used to be a hand-written constant, and it drifted: a build
# covering Parts I-V shipped a title page reading "Parts I-IV".  Nothing could
# catch that, because nothing tied the string to the chapters actually built.
# It is now derived from them, so the cover cannot disagree with the contents.

_ROMAN = ("I", "II", "III", "IV", "V", "VI", "VII")

APPENDIX_PREFIX = "appendix_"


def is_appendix(chapter_id: str) -> bool:
    """True for back-matter files (appendix_b, appendix_c, ...).

    Appendices are apparatus, not chapters: they belong to no Part, and they
    cite the book rather than the corpus.  Both facts would otherwise be
    reported as warnings on every build, and four standing false warnings are
    an excellent way to stop noticing a real one.
    """
    return chapter_id.startswith(APPENDIX_PREFIX)


def subtitle_for(chapter_ids: "tuple[str, ...] | list[str]") -> str:
    """Describe the parts these chapters cover, e.g. 'Parts I-V - Working Draft'.

    A build that covers every part carries the edition statement; anything
    less is a working draft, which is what a partial build honestly is.
    """
    parts = sorted({CHAPTER_PART[c] for c in chapter_ids if c in CHAPTER_PART})
    if not parts:
        return "Working Draft"

    complete = parts == sorted(PARTS)
    if complete:
        span = f"Parts {_ROMAN[parts[0] - 1]}–{_ROMAN[parts[-1] - 1]}"
        return f"{span} — {EDITION}"

    contiguous = parts == list(range(parts[0], parts[-1] + 1))
    if len(parts) == 1:
        span = f"Part {_ROMAN[parts[0] - 1]}"
    elif contiguous:
        span = f"Parts {_ROMAN[parts[0] - 1]}–{_ROMAN[parts[-1] - 1]}"
    else:
        span = "Parts " + ", ".join(_ROMAN[p - 1] for p in parts)
    return f"{span} — Working Draft"
