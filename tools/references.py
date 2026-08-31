"""Bibliography resolution: references.md with a corpus_index.md fallback.

Three tiers, per the build contract:
  1. ID present in meta/references.md          -> use the bibliographic string
  2. ID absent there but present in corpus_index -> warn, use a fallback string
  3. ID present in neither                      -> hard failure at end of build
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

# `S1 | Author, "Title," Venue, Year.` — the documented references.md contract.
_PIPE_ROW = re.compile(r"^\s*([A-Z]{1,3}\d{1,3})\s*\|\s*(.+?)\s*$")
# `| ID | anything |` — a markdown table row whose first cell is a bare ID.
_TABLE_ROW = re.compile(r"^\|\s*([A-Z]{1,3}\d{1,3})\s*\|(.*)\|\s*$")
# The section that holds the entries, when references.md is sectioned.
_SECTION = re.compile(r"^##+\s+(.*?)\s*$")
_ENTRY_SECTION_WORDS = ("entries", "entry", "references", "bibliography")
# `- **S1** — text`, `* [S1] text`, `S1. text`, `S1: text`, `S1 — text`
_LIST_ROW = re.compile(
    r"^\s*(?:[-*+]\s+)?"
    r"(?:\*\*|\[|`)?\s*([A-Z]{1,3}\d{1,3})\s*(?:\*\*|\]|`)?"
    r"\s*(?:[—–:.)\-]|\s)\s*(.+?)\s*$"
)
# `### S1` / `#### S1 — title`
_HEADING_ROW = re.compile(r"^#{2,6}\s+([A-Z]{1,3}\d{1,3})\b\s*[—–:.\-]?\s*(.*)$")

_SEPARATOR_ROW = re.compile(r"^\|[\s:|-]+\|$")


@dataclass
class Bibliography:
    """ID -> bibliographic string, with provenance tracking."""

    entries: dict[str, str] = field(default_factory=dict)
    fallback_ids: set[str] = field(default_factory=set)
    missing_ids: set[str] = field(default_factory=set)
    references_path: Path | None = None
    references_found: bool = False

    def resolve(self, cit_id: str) -> str:
        """Return a bibliographic string for `cit_id`, recording its tier."""
        text = self.entries.get(cit_id)
        if text is None:
            self.missing_ids.add(cit_id)
            return f"{cit_id} — [NO REFERENCE ENTRY]"
        if cit_id in self.fallback_ids:
            pass  # already recorded when the fallback was installed
        return text


def _clean_cell(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _entry_region(text: str) -> str:
    """Narrow to the '## Entries' section when one exists.

    references.md also carries a provenance table whose rows start with `| ID |`;
    parsing the whole file would let those shadow the real entries.
    """
    lines = text.splitlines()
    starts: list[tuple[int, str]] = [
        (i, m.group(1).lower())
        for i, line in enumerate(lines)
        if (m := _SECTION.match(line))
    ]
    for index, (line_no, title) in enumerate(starts):
        if any(word in title for word in _ENTRY_SECTION_WORDS):
            end = starts[index + 1][0] if index + 1 < len(starts) else len(lines)
            region = "\n".join(lines[line_no + 1 : end])
            if re.search(r"^\s*[A-Z]{1,3}\d{1,3}\s*[|—–:.]", region, re.M):
                return region
    return text


def parse_references(path: Path) -> dict[str, str]:
    """Tolerantly parse meta/references.md.

    Accepts the documented `ID | text` contract plus markdown tables,
    bullet/numbered lists and per-ID headings, since the file is produced by a
    separate agent and its exact shape is not guaranteed.
    """
    out: dict[str, str] = {}
    if not path.is_file():
        return out

    in_fence = False
    pending_heading: str | None = None
    heading_buffer: list[str] = []

    def flush_heading() -> None:
        nonlocal pending_heading, heading_buffer
        if pending_heading is not None:
            text = _clean_cell(" ".join(heading_buffer))
            if text and pending_heading not in out:
                out[pending_heading] = text
        pending_heading, heading_buffer = None, []

    for raw in _entry_region(path.read_text(encoding="utf-8")).splitlines():
        line = raw.rstrip()
        if line.lstrip().startswith(("```", "~~~")):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if _SEPARATOR_ROW.match(line.strip()):
            continue

        pipe = _PIPE_ROW.match(line)
        if pipe and not line.lstrip().startswith("|"):
            flush_heading()
            cid, text = pipe.group(1), _clean_cell(pipe.group(2))
            if text and cid not in out:
                out[cid] = text
            continue

        heading = _HEADING_ROW.match(line)
        if heading:
            flush_heading()
            cid, tail = heading.group(1), _clean_cell(heading.group(2))
            pending_heading = cid
            heading_buffer = [tail] if tail else []
            continue

        if pending_heading is not None:
            if line.strip():
                heading_buffer.append(line.strip())
                continue
            if heading_buffer:
                flush_heading()
            continue

        table = _TABLE_ROW.match(line.strip())
        if table:
            cid = table.group(1)
            cells = [_clean_cell(c) for c in table.group(2).split("|")]
            text = " — ".join(c for c in cells if c)
            if text and cid not in out:
                out[cid] = text
            continue

        listed = _LIST_ROW.match(line)
        if listed and line.strip():
            cid = listed.group(1)
            text = _clean_cell(listed.group(2)).lstrip("|").strip()
            if text and cid not in out:
                out[cid] = text

    flush_heading()
    return out


def parse_corpus_index(path: Path) -> dict[str, dict[str, str]]:
    """Parse meta/corpus_index.md rows: `| ID | file | pages | internal title |`."""
    out: dict[str, dict[str, str]] = {}
    if not path.is_file():
        return out
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line.startswith("|") or _SEPARATOR_ROW.match(line):
            continue
        cells = [_clean_cell(c) for c in line.strip("|").split("|")]
        if len(cells) < 2 or not re.fullmatch(r"[A-Z]{1,3}\d{1,3}", cells[0]):
            continue
        out[cells[0]] = {
            "file": cells[1],
            "pages": cells[2] if len(cells) > 2 else "",
            "title": cells[3] if len(cells) > 3 else "",
        }
    return out


_JUNK_TITLES = {
    "untitled",
    "",
    "paper title (use style: paper title)",
}


def fallback_string(cit_id: str, entry: dict[str, str]) -> str:
    """Compose a usable citation string from a corpus_index row.

    The file path is the informative part: several internal titles are blank
    or junk ("untitled", "PSS.book", "0-387-31275-7.pdf").
    """
    parts = [cit_id, entry.get("file", "").strip()]
    title = entry.get("title", "").strip()
    if title.lower() not in _JUNK_TITLES and not title.lower().endswith(
        (".pdf", ".book", ".doc")
    ):
        parts.append(f"“{title}”")
    pages = entry.get("pages", "").strip()
    if pages:
        parts.append(f"{pages} pp.")
    parts.append("[no references.md entry — corpus fallback]")
    return " — ".join(p for p in parts if p)


def load_bibliography(references_path: Path, corpus_path: Path) -> Bibliography:
    """Build the merged bibliography (tier 1 over tier 2)."""
    bib = Bibliography(references_path=references_path)
    refs = parse_references(references_path)
    bib.references_found = references_path.is_file()
    bib.entries.update(refs)

    corpus = parse_corpus_index(corpus_path)
    for cid, entry in corpus.items():
        if cid not in bib.entries:
            bib.entries[cid] = fallback_string(cid, entry)
            bib.fallback_ids.add(cid)
    return bib
