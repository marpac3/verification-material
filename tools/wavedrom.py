"""WaveDrom extraction, rendering (via wavedrom-cli) and print-safe SVG cleanup.

The mirror of `tools/mermaid.py`, for the other kind of figure this book needs:
a structural diagram says what is connected to what, and a timing diagram says
what happens in which cycle. Where the argument *is* a waveform — a handshake
that must not drop, a stall that must propagate, a beat order — prose and a
flowchart both paraphrase it, and the paraphrase is what a reader has to undo.

Authoring, in the chapter markdown: a ```wavedrom fence holding WaveJSON, with
the caption below it and a `{ref: label}` from the text, exactly as for mermaid
(see `tools/floats.py`).

    ```wavedrom
    {"signal": [
      {"name": "clk", "wave": "p......"},
      {"name": "req", "wave": "01..0.."}
    ]}
    ```

    {figure: req_handshake} The request handshake, cycle by cycle.

Rendered SVGs are cached under <build>/wavedrom_cache/ keyed by a hash of the
diagram source *plus* the renderer identity *plus* a post-processing version, so
a cleanup change invalidates stale artefacts. The namespace of the placeholder
(`@@WAVEDROM:`) is its own: the two pipelines run over the same document, and a
shared token would let one substitute the other's figures.

Why the SVG is post-processed at all
------------------------------------
Two defects, both of which only appear once a *second* diagram, or the rest of
the book, is in the same document:

1. WaveDrom names its elements generically — `svgcontent_0`, `000`, `111`,
   `socket`, `pclk`, `nclk`, `arrowhead`, `tee` — and refers to them with
   `xlink:href="#000"` and `marker-end:url(#arrowhead)`. Inline two diagrams in
   one HTML page and the second one's references resolve against the first one's
   elements, because a document-wide id lookup returns the first match. So every
   id is prefixed with the diagram's own key, and every reference to it with it.
2. Its internal `<style>` uses unscoped selectors: `text{…}`, `.s1{…}` …
   `.s16{…}`, `.info`, `.error`, `.success`, `.warning`. Inline in HTML, a
   `<style>` inside an `<svg>` applies to the whole document, so `text{…}` would
   restyle every mermaid label on the page — and `.s1`/`.s2` collide by name
   with Pygments' own string-literal classes, which `build_book.pygments_css()`
   concatenates into the same stylesheet (verified 2026-09-08: Pygments emits
   `.s`, `.s1`, `.s2`). Every selector is therefore scoped to `#wd-<key>`.

Both rewrites survive CairoSVG, which is what renders the PDF's data-URI copy
(WeasyPrint 52.5 cannot lay out inline `<svg>`; see `mermaid.substitute`). The
negative control for the scoping is a deliberately wrong scope: with `#nope`
prefixed instead, CairoSVG draws the waveform as filled black blocks, so the
correct render is evidence the scoped CSS is being applied and not ignored.
"""

from __future__ import annotations

import base64
import hashlib
import re
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path

SVG_NS = "http://www.w3.org/2000/svg"
XLINK_NS = "http://www.w3.org/1999/xlink"

# Bumped whenever _postprocess_svg changes shape -> invalidates the cache.
POSTPROC_VERSION = "wd-postproc-v1"

# Part of the cache key: a different renderer draws a different picture from the
# same WaveJSON, and a cache that cannot tell would serve the old one.
RENDERER = "wavedrom-cli"

# One process per diagram. wavedrom-cli is a plain node script (no browser, no
# batch mode), and a single diagram of this book's size renders in ~2 s; 120 s
# is the ceiling at which a hung npx is a failure rather than slow work.
RENDER_TIMEOUT = 120

# Same policy as mermaid: past this ratio, fitting the figure into the 164 mm
# text column scales its labels below comfortable, so it bleeds into the margins
# instead (`figure.diagram.wide` in tools/book_style.css).
#
# A waveform's ratio grows with cycles and shrinks with signals. Measured on
# 2026-09-08: 4 signals over 4 cycles is 2.0:1, 2 signals over 4 cycles 4.0:1,
# 6 signals over 33 cycles 8.3:1, 2 signals over 33 cycles 23.3:1. So the long
# ones do trip this, and the wide path was checked in print at 8.3:1 — the 32
# data labels stay legible, the signal names land near 4 pt. Past roughly 10:1
# even the bleed cannot save the names: split the diagram instead.
WIDE_RATIO = 6.0

# `^ {0,3}` and not `^[ \t]*`: four spaces (or a tab) open an indented code
# block, and the ``` inside one is content. A chapter that documents how to
# author a waveform shows the fence itself, indented — extracting it rendered a
# diagram where the text promised an example.
WAVEDROM_FENCE = re.compile(
    r"^ {0,3}```[ \t]*wavedrom[ \t]*\n(.*?)^ {0,3}```[ \t]*$",
    re.S | re.M,
)
# Any fence, for the protection scan below: `(marker, info string)`.
_ANY_FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$", re.M)

PLACEHOLDER = "@@WAVEDROM:{key}@@"
_PLACEHOLDER_RE = re.compile(r"@@WAVEDROM:([0-9a-f]+)@@")
_FIGURE_RE = re.compile(
    r'<figure class="diagram">@@WAVEDROM:([0-9a-f]+)@@</figure>'
)
_VIEWBOX_RE = re.compile(r'viewBox="([\d.eE+\- ,]+)"')

_STYLE_BLOCK = re.compile(r"(<style[^>]*>)(.*?)(</style>)", re.S)
_URL_REF_RE = re.compile(r"url\(\s*#([^)\s]+)\s*\)")
# The scoper below is flat: it prefixes every selector at depth zero. An at-rule
# nests a block, so its presence means the scoper would mangle the CSS — that is
# an error rather than a silent miss. Only an `@` in *selector* position counts:
# an `@` inside a declaration value (a font family that contains one, say) is not
# an at-rule, and refusing it would turn a renderable diagram into a build stop.
# Measured 2026-09-08 on wavedrom-cli: the default, `narrow` and `lowkey` skins
# and a `config.hscale` all emit one flat <style> with no `@` at all.
_AT_RULE_RE = re.compile(r"(?:\A|\})\s*@[a-zA-Z-]")

# A missing package is the one failure worth retrying with `-y`; a WaveJSON
# error is not, and retrying it would report the second error as if the first
# attempt had never happened. npm's own diagnostics are the tell: an E404 or any
# `npm error` line means the CLI never ran.
_NPM_ERROR_RE = re.compile(r"npm (?:error|ERR!)")


class WavedromError(RuntimeError):
    pass


@dataclass
class Diagram:
    key: str
    source: str
    svg: str = ""

    @property
    def data_uri(self) -> str:
        b64 = base64.b64encode(self.svg.encode("utf-8")).decode("ascii")
        return f"data:image/svg+xml;base64,{b64}"

    @property
    def aspect_ratio(self) -> float:
        match = _VIEWBOX_RE.search(self.svg or "")
        if not match:
            return 1.0
        parts = match.group(1).replace(",", " ").split()
        if len(parts) != 4:
            return 1.0
        try:
            width, height = float(parts[2]), float(parts[3])
        except ValueError:  # pragma: no cover - defensive
            return 1.0
        return width / height if height else 1.0

    @property
    def is_wide(self) -> bool:
        return self.aspect_ratio > WIDE_RATIO


def diagram_key(source: str) -> str:
    payload = "\n".join([source.strip(), RENDERER, POSTPROC_VERSION])
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def _quoted_regions(markdown_text: str) -> list[tuple[int, int]]:
    """Character spans that sit inside a fenced block, openers excluded.

    A markdown fence is closed by a marker of the same character and at least
    the same length, so ```` ```` ```` quotes a ``` and everything between them
    is the outer block's content. The opener's own line is left outside the span
    on purpose: a top-level `` ```wavedrom `` is a fence, and if its own line
    counted as quoted it would filter itself.
    """
    regions: list[tuple[int, int]] = []
    marker = ""
    start = 0
    for match in _ANY_FENCE_RE.finditer(markdown_text):
        end_of_line = match.end() + 1
        if marker:
            if (match.group(1)[0] == marker[0]
                    and len(match.group(1)) >= len(marker)
                    and not match.group(2).strip()):
                regions.append((start, min(end_of_line, len(markdown_text))))
                marker = ""
            continue
        if "`" in match.group(2):  # an inline-code run, not a fence opener
            continue
        marker = match.group(1)
        start = end_of_line
    if marker:  # an unterminated fence quotes the rest of the file
        regions.append((start, len(markdown_text)))
    return regions


def extract(markdown_text: str) -> tuple[str, dict[str, Diagram]]:
    """Replace every ```wavedrom fence with a <figure> carrying a placeholder.

    The fence body is passed through verbatim. WaveJSON is parsed by wavedrom-cli
    with JSON5, which admits unquoted keys, trailing commas and comments, so a
    `json.loads` check here would reject sources the renderer accepts.

    A fence that is *quoted* — indented into a code block, or nested inside a
    longer fence — is an example of the syntax and not a diagram, and is left
    exactly as written. The indentation rule is in `WAVEDROM_FENCE`; the nesting
    rule is `_quoted_regions`, whose spans a match is filtered against.
    """
    found: dict[str, Diagram] = {}
    quoted = _quoted_regions(markdown_text)

    def sub(match: re.Match[str]) -> str:
        if any(start <= match.start() < end for start, end in quoted):
            return match.group(0)
        source = match.group(1)
        key = diagram_key(source)
        found.setdefault(key, Diagram(key=key, source=source))
        token = PLACEHOLDER.format(key=key)
        # Block-level raw HTML: python-markdown passes it through untouched.
        replacement = f'\n<figure class="diagram">{token}</figure>\n'
        # Pad to the fence's original line count so that every line number
        # after a diagram still refers to the same line of the source file:
        # the float checker's "line N" warnings are the work list a captioning
        # pass reads, and a collapsed fence silently shifts all of them.
        deficit = match.group(0).count("\n") - replacement.count("\n")
        if deficit > 0:
            replacement += "\n" * deficit
        return replacement

    return WAVEDROM_FENCE.sub(sub, markdown_text), found


# --- rendering -------------------------------------------------------------


def _npx_available() -> bool:
    return shutil.which("npx") is not None


def _attempt(argv: list[str], src: Path, out: Path, workdir: Path):
    cmd = [*argv, "-i", str(src), "-s", str(out)]
    return subprocess.run(
        cmd, cwd=workdir, capture_output=True, text=True, timeout=RENDER_TIMEOUT
    )


def _run_wavedrom(src: Path, out: Path, workdir: Path) -> None:
    """Render one WaveJSON file to `out`, retrying only a missing package."""
    attempts: list[str] = []
    for argv in (
        ["npx", "--no-install", "wavedrom-cli"],
        ["npx", "-y", "wavedrom-cli"],
    ):
        if out.exists():
            out.unlink()
        proc = _attempt(argv, src, out, workdir)
        if proc.returncode == 0 and out.is_file() and out.stat().st_size:
            return
        combined = f"{proc.stdout}\n{proc.stderr}"
        attempts.append(
            f"$ {' '.join(argv)} (exit {proc.returncode})\n"
            f"{proc.stdout[-1000:]}\n{proc.stderr[-1000:]}"
        )
        if not _NPM_ERROR_RE.search(combined):
            # The CLI ran and rejected the source: retrying installs nothing
            # and would report the same defect twice.
            break
    raise WavedromError(
        "wavedrom-cli produced no SVG:\n" + "\n---\n".join(attempts)
    )


def _render_single(diagram: Diagram, workdir: Path) -> str:
    src = workdir / f"{diagram.key}.json"
    out = workdir / f"{diagram.key}.svg"
    src.write_text(diagram.source.rstrip() + "\n", encoding="utf-8")
    _run_wavedrom(src, out, workdir)
    return out.read_text(encoding="utf-8")


def render_all(
    diagrams: dict[str, Diagram], cache_dir: Path, warn
) -> dict[str, Diagram]:
    """Populate .svg on every diagram, using (and filling) the on-disk cache.

    Creates `cache_dir` only when there is something to put in it, so a build of
    chapters that carry no waveform leaves no trace of this pipeline at all.
    """
    pending: list[Diagram] = []
    for diagram in diagrams.values():
        cached = cache_dir / f"{diagram.key}.svg"
        if cached.is_file():
            diagram.svg = cached.read_text(encoding="utf-8")
        else:
            pending.append(diagram)

    if not pending:
        return diagrams
    if not _npx_available():
        raise WavedromError(
            "npx not found on PATH; cannot render "
            f"{len(pending)} uncached wavedrom diagram(s)"
        )

    cache_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="wavedrom-") as tmp:
        workdir = Path(tmp)
        for diagram in pending:
            diagram.svg = _postprocess_svg(
                _render_single(diagram, workdir), diagram.key
            )
            (cache_dir / f"{diagram.key}.svg").write_text(
                diagram.svg, encoding="utf-8"
            )
    return diagrams


# --- SVG clean-up ----------------------------------------------------------


def scope_id(key: str) -> str:
    """The id the diagram's root <svg> carries, and the CSS scope for it."""
    return f"wd-{key}"


def _rewrite_refs(value: str, mapping: dict[str, str]) -> str:
    if value.startswith("#") and value[1:] in mapping:
        value = "#" + mapping[value[1:]]
    return _URL_REF_RE.sub(
        lambda m: f"url(#{mapping.get(m.group(1), m.group(1))})", value
    )


def _prefix_ids(root: ET.Element, scope: str) -> int:
    """Give every id — and every reference to one — this diagram's namespace."""
    mapping: dict[str, str] = {}
    for element in root.iter():
        old = element.get("id")
        if old is None:
            continue
        mapping[old] = scope if element is root else f"{scope}-{old}"
    for element in root.iter():
        old = element.get("id")
        if old is not None:
            element.set("id", mapping[old])
        for name, value in list(element.attrib.items()):
            if name == "id" or not value:
                continue
            rewritten = _rewrite_refs(value, mapping)
            if rewritten != value:
                element.set(name, rewritten)
    return len(mapping)


def _scope_selectors(selectors: str, scope: str) -> str:
    parts = [part.strip() for part in selectors.split(",")]
    return ", ".join(f"#{scope} {part}" for part in parts if part)


def scope_css(css: str, scope: str) -> str:
    """Confine a flat stylesheet to the subtree of `#<scope>`."""
    if _AT_RULE_RE.search(css):
        raise WavedromError(
            "wavedrom CSS contains an at-rule; the flat scoper would mangle it"
        )

    def one(match: re.Match[str]) -> str:
        return _scope_selectors(match.group(1), scope) + "{"

    return re.sub(r"([^{}]+)\{", one, css)


def _rewrite_style(match: re.Match[str], scope: str) -> str:
    """Scope the block, and keep its CSS literal.

    An HTML parser does not unescape entities inside `<style>`, so the `&gt;`
    ElementTree writes for a `>` would ship as three characters of CSS.
    """
    css = match.group(2)
    css = css.replace("&gt;", ">").replace("&lt;", "<").replace("&amp;", "&")
    return match.group(1) + scope_css(css, scope) + match.group(3)


def _postprocess_svg(svg_text: str, key: str) -> str:
    """Make one WaveDrom SVG safe to inline beside others, and safe for CairoSVG."""
    ET.register_namespace("", SVG_NS)
    ET.register_namespace("xlink", XLINK_NS)
    try:
        root = ET.fromstring(svg_text)
    except ET.ParseError as exc:  # pragma: no cover - defensive
        raise WavedromError(f"wavedrom produced unparseable SVG: {exc}") from exc

    scope = scope_id(key)
    # `_prefix_ids` maps the root's own id — whatever WaveDrom called it — onto
    # the scope, so a self-reference is rewritten too; the `set` after it is for
    # the case of a root with no id at all, where the scoped CSS below would
    # otherwise select nothing and the diagram would render unstyled.
    _prefix_ids(root, scope)
    root.set("id", scope)

    view_box = root.get("viewBox")
    if not view_box:
        raise WavedromError(f"wavedrom SVG for {key} has no viewBox")
    parts = view_box.replace(",", " ").split()
    if len(parts) == 4:
        width, height = float(parts[2]), float(parts[3])
        # Kept, not dropped: these are the intrinsic size CairoSVG needs for the
        # PDF's <img>, and in HTML `figure.diagram svg { max-width: 100%;
        # height: auto }` overrides them, so they do not block resizing.
        root.set("width", f"{width:.0f}")
        root.set("height", f"{height:.0f}")
    # `width:100%` / `max-width` on the root would fight our own CSS sizing.
    root.attrib.pop("style", None)
    root.set("preserveAspectRatio", "xMidYMid meet")

    out = ET.tostring(root, encoding="unicode")
    return _STYLE_BLOCK.sub(lambda m: _rewrite_style(m, scope), out)


# --- substitution into the assembled document ------------------------------


def _render_one(diagram: Diagram | None, *, inline: bool, occurrence: int = 1) -> str:
    """One figure's markup. `occurrence` is which use of this diagram it is.

    Two identical fences share one key, one cache entry and one post-processed
    SVG — but ids are document-wide. Inlining the same SVG twice shipped two
    elements with `id="wd-<key>"`, two with `id="wd-<key>-000"`, and a second
    `<style>` scoped to the same `#wd-<key>`. `_prefix_ids` made every internal
    id and every reference to one start with the scope, and `scope_css` made
    every selector start with `#`+scope, so suffixing the scope in the text
    renames all of them together. The key is untouched: the cache is keyed by
    the source, and the same source must not render twice.
    """
    if diagram is None or not diagram.svg:  # pragma: no cover - defensive
        return '<span class="diagram-missing">[timing diagram unavailable]</span>'
    if inline:
        if occurrence <= 1:
            return diagram.svg
        scope = scope_id(diagram.key)
        return diagram.svg.replace(scope, f"{scope}-o{occurrence}")
    return (
        f'<img class="diagram-img" src="{diagram.data_uri}" '
        f'alt="Timing diagram {diagram.key}"/>'
    )


def substitute(html: str, diagrams: dict[str, Diagram], *, inline: bool) -> str:
    """Replace placeholders with inline <svg> (HTML) or a data-URI <img> (PDF).

    The `<figure class="diagram">` wrapper is the same one mermaid emits, so
    `tools/floats.py` and `tools/book_style.css` treat both kinds of figure
    alike and a caption sits under a waveform exactly as under a flowchart.
    """

    seen: dict[str, int] = {}

    def nth(key: str) -> int:
        seen[key] = seen.get(key, 0) + 1
        return seen[key]

    def whole_figure(match: re.Match[str]) -> str:
        diagram = diagrams.get(match.group(1))
        classes = "diagram wide" if diagram and diagram.is_wide else "diagram"
        return (
            f'<figure class="{classes}">'
            f"{_render_one(diagram, inline=inline, occurrence=nth(match.group(1)))}"
            "</figure>"
        )

    def bare_placeholder(match: re.Match[str]) -> str:
        return _render_one(diagrams.get(match.group(1)), inline=inline,
                           occurrence=nth(match.group(1)))

    html = _FIGURE_RE.sub(whole_figure, html)
    return _PLACEHOLDER_RE.sub(bare_placeholder, html)
