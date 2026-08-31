"""Turn the built book into a page that can be published as an Artifact.

    python3 tools/make_artifact_html.py        # run from the repository root

The Artifact runtime supplies its own doctype, head and body, so what gets
published is the built document's parts and not its wrapper: the title, the
stylesheet, and the body. The book's stylesheet is reused unchanged — it already
carries `@media screen` blocks that paint a ground, hold the measure to a page
width and suppress the `target-counter()` page numbers in the contents and the
float lists, which resolve only in a paginated formatter and would otherwise
render as gaps. A short screen layer is appended for the three things a hosted
page needs and a printed one does not; it is documented where it is written.

Run this after `tools/build_book.py`, never instead of it: the input is the built
HTML, so a stale build produces a stale page silently.
"""

from pathlib import Path

SRC = Path("build/hardware_verification_guide.html")
DST = Path("build/artifact_book.html")

lines = SRC.read_text(encoding="utf-8").split("\n")

# The built document is a complete HTML file; the Artifact runtime supplies its
# own doctype, head and body, so publish the parts and not the wrapper. The
# boundaries are read from the file rather than assumed: an off-by-one here
# would silently drop a rule or a section of the book.
style_open  = next(i for i, l in enumerate(lines) if l.strip() == "<style>")
style_close = next(i for i, l in enumerate(lines) if l.strip() == "</style>")
body_open   = next(i for i, l in enumerate(lines) if l.strip() == "<body>")
body_close  = next(i for i, l in enumerate(lines) if l.strip() == "</body>")

book_css = "\n".join(lines[style_open + 1 : style_close])
book_body = "\n".join(lines[body_open + 1 : body_close])

assert "@page" in book_css, "book stylesheet not captured"
assert 'class="title-page"' in book_body, "book body not captured"
assert len(book_body) > 2_000_000, f"body suspiciously short: {len(book_body)}"

SCREEN_LAYER = """
/* ------------------------------------------------------------------
   Screen layer for the published edition.

   The stylesheet above is the book's own, written for paged media, and it
   already carries `@media screen` blocks that paint the ground, constrain the
   measure to a page width and suppress the `target-counter()` page numbers in
   the contents and the float lists — those resolve only in a paginated
   formatter and would otherwise render as gaps. Nothing here overrides it. What
   follows fills the three gaps a hosted page has and a printed one does not.
   ------------------------------------------------------------------ */

/* 1. The host composites this page over a ground it paints in the viewer's
      theme, and a book is a single visual world: ink on paper, deliberately
      one look rather than two. So the ground and the ink are painted
      unconditionally here as well as inside `@media screen`, and the UA is told
      which world it is in, so scrollbars and focus rings resolve to match. */
:root { color-scheme: light; }
body {
  background: #fbfbfc;
  color: #1b1f24;
}

/* 2. Keyboard focus. A 500-page document is navigated by its contents, and the
      book's own rules give links no focus state because paper has no keyboard. */
a:focus-visible {
  outline: 2px solid #1e3663;
  outline-offset: 2px;
  border-radius: 1px;
}

/* 3. Narrow viewports. The page-width card is 210mm; below roughly that the
      measure has to give. Tables are the only content that cannot simply
      reflow — several run to five and six columns — so they get their own
      scroll container rather than forcing the whole page sideways. */
@media (max-width: 860px) {
  body { padding: 14px 8px 48px 8px; }
  .book { padding: 0 14px; }
  .book, .title-page { max-width: 100%; }
  figure.diagram { overflow-x: auto; }
  table {
    display: block;
    overflow-x: auto;
    max-width: 100%;
  }
}

/* A way back to the contents, which is the one affordance a scroll of this
   length needs and a bound volume does not: paper has a thumb. Set in the
   book's own sans face and its own blue, sized to be findable and not to
   compete with the text. */
.to-contents {
  position: fixed;
  right: 18px;
  bottom: 18px;
  z-index: 10;
  font-family: "Liberation Sans", "DejaVu Sans", "FreeSans", sans-serif;
  font-size: 12.5px;
  letter-spacing: 0.02em;
  color: #1e3663;
  background: rgba(255, 255, 255, 0.94);
  border: 1px solid #d5dbe4;
  border-radius: 3px;
  padding: 7px 12px;
  text-decoration: none;
  box-shadow: 0 1px 3px rgba(27, 31, 36, 0.10);
}
.to-contents:hover {
  background: #fff;
  border-color: #1e3663;
  text-decoration: none;
}
@media (max-width: 520px) {
  .to-contents { right: 10px; bottom: 10px; }
}
"""

NAV = '<a class="to-contents" href="#contents">Contents</a>\n'

DST.write_text(
    "<title>Hardware Verification: A Holistic Guide</title>\n"
    "<style>\n" + book_css + "\n</style>\n"
    "<style>\n" + SCREEN_LAYER + "\n</style>\n"
    + NAV
    + book_body
    + "\n",
    encoding="utf-8",
)
print(f"wrote {DST} ({DST.stat().st_size/1024/1024:.2f} MB)")
