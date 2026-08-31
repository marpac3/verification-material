"""Mermaid extraction, rendering (via mermaid-cli) and print-safe SVG cleanup.

Rendered SVGs are cached under <build>/mermaid_cache/ keyed by a hash of the
diagram source *plus* the renderer configuration *plus* a post-processing
version, so a theme or cleanup change invalidates stale artefacts.
"""

from __future__ import annotations

import base64
import hashlib
import json
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
POSTPROC_VERSION = "postproc-v2"

# A diagram wider than this ratio is scaled so far down to fit the text column
# that its labels stop being comfortable; those bleed into the page margins.
WIDE_RATIO = 6.0

# htmlLabels must be false at BOTH levels: mermaid 11 otherwise emits
# <foreignObject>, which CairoSVG (WeasyPrint 52 backend) cannot render.
MMDC_CONFIG: dict = {
    "theme": "neutral",
    "htmlLabels": False,
    "flowchart": {
        "htmlLabels": False,
        "curve": "basis",
        "useMaxWidth": False,
        # Tighter spacing keeps the diagram narrower, so fitting it to the text
        # column scales the labels down less.
        "nodeSpacing": 34,
        "rankSpacing": 34,
        "padding": 8,
    },
    "sequence": {"useMaxWidth": False},
    "themeVariables": {
        "fontFamily": "Liberation Sans, DejaVu Sans, sans-serif",
        "fontSize": "16px",
        "lineColor": "#5b6672",
        "primaryTextColor": "#1b1f24",
    },
}

PUPPETEER_CONFIG: dict = {
    "args": ["--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage"]
}

MERMAID_FENCE = re.compile(
    r"^[ \t]*```[ \t]*mermaid[ \t]*\n(.*?)^[ \t]*```[ \t]*$",
    re.S | re.M,
)

PLACEHOLDER = "@@MERMAID:{key}@@"
_PLACEHOLDER_RE = re.compile(r"@@MERMAID:([0-9a-f]+)@@")
_FIGURE_RE = re.compile(
    r'<figure class="diagram">@@MERMAID:([0-9a-f]+)@@</figure>'
)
_VIEWBOX_RE = re.compile(r'viewBox="([\d.eE+\- ,]+)"')
# With htmlLabels disabled (required for CairoSVG) mermaid prints <i>/<b> in
# labels literally.  <br/> is honoured and must survive.
_INLINE_MARKUP = re.compile(r"</?\s*(?:i|b|em|strong|u|span)\s*>", re.I)

_STYLE_BLOCK = re.compile(r"(<style[^>]*>)(.*?)(</style>)", re.S)


class MermaidError(RuntimeError):
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


def sanitise_source(source: str) -> str:
    """Drop inline emphasis tags mermaid would otherwise print verbatim.

    Done before layout (not on the rendered SVG) so node boxes are sized for
    the text that is actually drawn.
    """
    return _INLINE_MARKUP.sub("", source)


def diagram_key(source: str) -> str:
    payload = "\n".join(
        [
            source.strip(),
            json.dumps(MMDC_CONFIG, sort_keys=True),
            POSTPROC_VERSION,
        ]
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def extract(markdown_text: str) -> tuple[str, dict[str, Diagram]]:
    """Replace every ```mermaid fence with a <figure> carrying a placeholder."""
    found: dict[str, Diagram] = {}

    def sub(match: re.Match[str]) -> str:
        source = sanitise_source(match.group(1))
        key = diagram_key(source)
        found.setdefault(key, Diagram(key=key, source=source))
        token = PLACEHOLDER.format(key=key)
        # Block-level raw HTML: python-markdown passes it through untouched.
        replacement = f'\n<figure class="diagram">{token}</figure>\n'
        # Pad to the fence's original line count so that every line number
        # after a diagram still refers to the same line of the source file.
        # A fifteen-line fence collapsing to three silently shifted every
        # downstream line number, which made the float checker's "line N"
        # warnings point at the wrong place — and those warnings are the work
        # list a captioning pass reads. Extra blank lines are inert in
        # markdown: consecutive blanks are one paragraph break, and the raw
        # HTML block already needs a blank line either side.
        deficit = match.group(0).count("\n") - replacement.count("\n")
        if deficit > 0:
            replacement += "\n" * deficit
        return replacement

    return MERMAID_FENCE.sub(sub, markdown_text), found


# --- rendering -------------------------------------------------------------


def _mmdc_available() -> bool:
    return shutil.which("npx") is not None


def _run_mmdc(input_path: Path, output_path: Path, workdir: Path) -> None:
    conf = workdir / "mermaid.json"
    pconf = workdir / "puppeteer.json"
    conf.write_text(json.dumps(MMDC_CONFIG), encoding="utf-8")
    pconf.write_text(json.dumps(PUPPETEER_CONFIG), encoding="utf-8")
    cmd = [
        "npx", "-y", "@mermaid-js/mermaid-cli",
        "-i", str(input_path),
        "-o", str(output_path),
        "-b", "transparent",
        "-c", str(conf),
        "-p", str(pconf),
    ]
    proc = subprocess.run(
        cmd, cwd=workdir, capture_output=True, text=True, timeout=600
    )
    if proc.returncode != 0:
        raise MermaidError(
            f"mermaid-cli failed (exit {proc.returncode}):\n"
            f"{proc.stdout[-2000:]}\n{proc.stderr[-2000:]}"
        )


def _render_batch(diagrams: list[Diagram], workdir: Path) -> list[str] | None:
    """Render every diagram in one mmdc call (one browser launch). None on doubt."""
    doc = "\n\n".join(f"```mermaid\n{d.source.rstrip()}\n```" for d in diagrams)
    src = workdir / "batch.md"
    src.write_text(doc + "\n", encoding="utf-8")
    _run_mmdc(src, workdir / "batch.svg", workdir)
    produced = [workdir / f"batch-{i + 1}.svg" for i in range(len(diagrams))]
    if not all(p.is_file() for p in produced):
        return None
    return [p.read_text(encoding="utf-8") for p in produced]


def _render_single(diagram: Diagram, workdir: Path) -> str:
    src = workdir / "single.mmd"
    out = workdir / "single.svg"
    src.write_text(diagram.source.rstrip() + "\n", encoding="utf-8")
    if out.exists():
        out.unlink()
    _run_mmdc(src, out, workdir)
    if not out.is_file():
        raise MermaidError("mermaid-cli produced no SVG")
    return out.read_text(encoding="utf-8")


def render_all(
    diagrams: dict[str, Diagram], cache_dir: Path, warn
) -> dict[str, Diagram]:
    """Populate .svg on every diagram, using (and filling) the on-disk cache."""
    cache_dir.mkdir(parents=True, exist_ok=True)
    pending: list[Diagram] = []
    for diagram in diagrams.values():
        cached = cache_dir / f"{diagram.key}.svg"
        if cached.is_file():
            diagram.svg = cached.read_text(encoding="utf-8")
        else:
            pending.append(diagram)

    if not pending:
        return diagrams
    if not _mmdc_available():
        raise MermaidError(
            "npx not found on PATH; cannot render "
            f"{len(pending)} uncached mermaid diagram(s)"
        )

    with tempfile.TemporaryDirectory(prefix="mmdc-") as tmp:
        workdir = Path(tmp)
        raw: list[str] | None = None
        if len(pending) > 1:
            try:
                raw = _render_batch(pending, workdir)
            except MermaidError as exc:
                warn(f"mermaid batch render failed, falling back one by one: {exc}")
                raw = None
        if raw is None:
            raw = [_render_single(d, workdir) for d in pending]

    for diagram, svg in zip(pending, raw):
        diagram.svg = _postprocess_svg(svg, diagram.key)
        (cache_dir / f"{diagram.key}.svg").write_text(
            diagram.svg, encoding="utf-8"
        )
    return diagrams


# --- SVG clean-up ----------------------------------------------------------


def _merge_label_tspans(root: ET.Element) -> int:
    """Collapse per-word <tspan>s into one.

    Mermaid splits a label into one <tspan class="text-inner-tspan"> per word,
    relying on browser text-advance semantics that CairoSVG does not implement
    (every word would be drawn at the same x, overlapping).
    """
    merged = 0
    for element in root.iter(f"{{{SVG_NS}}}tspan"):
        if "text-outer-tspan" not in element.get("class", "") or not len(element):
            continue
        words = [t.strip() for t in element.itertext() if t and t.strip()]
        for child in list(element):
            element.remove(child)
        element.text = " ".join(words)
        merged += 1
    return merged


def _postprocess_svg(svg_text: str, key: str) -> str:
    """Make one mermaid SVG safe to inline and safe for CairoSVG."""
    ET.register_namespace("", SVG_NS)
    ET.register_namespace("xlink", XLINK_NS)
    try:
        root = ET.fromstring(svg_text)
    except ET.ParseError as exc:  # pragma: no cover - defensive
        raise MermaidError(f"mermaid produced unparseable SVG: {exc}") from exc

    _merge_label_tspans(root)

    view_box = root.get("viewBox")
    if view_box:
        parts = view_box.replace(",", " ").split()
        if len(parts) == 4:
            width, height = float(parts[2]), float(parts[3])
            root.set("width", f"{width:.0f}")
            root.set("height", f"{height:.0f}")
    # `width:100%` / `max-width` on the root fights our own CSS sizing.
    root.attrib.pop("style", None)
    root.set("preserveAspectRatio", "xMidYMid meet")

    out = ET.tostring(root, encoding="unicode")
    # mermaid hardcodes id "my-svg"; several diagrams inline in one document
    # would collide (ids *and* the CSS scoped to them).
    out = out.replace("my-svg", f"mmd-{key}")
    out = _STYLE_BLOCK.sub(_unescape_style, out)
    return out


def _unescape_style(match: re.Match[str]) -> str:
    """Keep CSS literal: an HTML parser will not unescape entities in <style>."""
    css = match.group(2)
    css = css.replace("&gt;", ">").replace("&lt;", "<").replace("&amp;", "&")
    return match.group(1) + css + match.group(3)


# --- substitution into the assembled document ------------------------------


def _render_one(diagram: Diagram | None, *, inline: bool) -> str:
    if diagram is None or not diagram.svg:  # pragma: no cover - defensive
        return '<span class="diagram-missing">[diagram unavailable]</span>'
    if inline:
        return diagram.svg
    return (
        f'<img class="diagram-img" src="{diagram.data_uri}" '
        f'alt="Diagram {diagram.key}"/>'
    )


def substitute(html: str, diagrams: dict[str, Diagram], *, inline: bool) -> str:
    """Replace placeholders with inline <svg> (HTML) or a data-URI <img> (PDF).

    WeasyPrint 52.5 cannot lay out inline SVG, so the PDF pass uses an <img>
    whose source is embedded as a data URI (no external file either way).
    """

    def whole_figure(match: re.Match[str]) -> str:
        diagram = diagrams.get(match.group(1))
        classes = "diagram wide" if diagram and diagram.is_wide else "diagram"
        return (
            f'<figure class="{classes}">'
            f"{_render_one(diagram, inline=inline)}</figure>"
        )

    def bare_placeholder(match: re.Match[str]) -> str:
        return _render_one(diagrams.get(match.group(1)), inline=inline)

    html = _FIGURE_RE.sub(whole_figure, html)
    return _PLACEHOLDER_RE.sub(bare_placeholder, html)
