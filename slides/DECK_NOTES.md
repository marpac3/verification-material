# Deck build notes

Accumulated the hard way across four decks. Read before building a fifth.

## The toolchain

Build **only** through the environment:

```
micromamba run -n gvsoc_env_3_12 weasyprint slides/<deck>.html slides/<deck>.pdf
```

The bare `weasyprint` on `PATH` is a broken py3.6 build. It writes nothing, exits
without an obvious error, and **leaves any stale PDF in place** — so the build appears
to succeed and you verify the previous version. Always check the PDF's mtime is later
than the HTML's.

## WeasyPrint 52.5 limitations

- **No inline SVG layout** — it silently emits the text content as prose. Do not use it.
- **`display:flex` breaks `target-counter()`.** Do not combine them.
- **`var()` is ignored for `background` and `border-color`.** Write literal colours for
  those two properties only.
- **`grid` and `gap` are ignored entirely.**
- A nested `width:100%` table inside a flex container **inflates the parent column**.
- `td` padding **adds to** 100% widths and clips.
- **Under `table-layout: fixed`, a per-cell width default ADDS to an inline width.**
  `table.cols td { width: 50% }` plus an inline `width:57%` on the first cell totals
  107%, and the last column runs past the page edge and is clipped. Scope the default to
  `td:first-child` and let fixed layout divide the remainder. Found on Part IV, where it
  clipped the final line of the last slide.
- **A nested table inside a `table.cols` cell misallocates its first column under auto
  layout.** Distinct from the trap above: here the nested table hands its first column
  far more than the declared percentage, leaving a large gap. Purely horizontal, so the
  checker is blind to it. Fix: `table-layout: fixed` on the *nested* table.
- **A three-column nested table inside a half-width column explodes vertically.** Four
  Part V slides rendered at two pages each on only ~2,100 characters. Promoting the table
  to full width fixed all four. This is why *characters per slide* is useless as a
  budget: **structure dominates word count**.
- `<sup>` and `<sub>` render correctly (10¹², log₂). Confirmed in 52.5.
- **Analytical width formulas run optimistic for monospace columns.** A predicted 71-character
  fit wrapped at 68 in the render. Set code blocks to **≤60 characters** and verify by
  rendering, never by calculation. Trust the render over your own model — the Part VI build
  found two wrapping `pre` blocks this way that no formula and no script would have caught.

## The footer defect — HOUSE-WIDE, PRE-EXISTING, UNFIXED

`.brand` and `.pagenum` sit at `bottom: 15px` of a `.slide` that **grows past its
`min-height`** once content exceeds 124.5 mm. Any slide rendering taller than **421 pt**
therefore silently loses or clips its footer chrome.

Measured maxima on shipped decks: **Part IV +29.8 pt, Part V +29.2, Part VI +28.5.**

**No gate catches it**, because the page count still comes out 1:1 — which is precisely why
it survived five decks. It is a production defect, not a content defect, and fixing it means
touching the shared CSS and rebuilding every deck at once. Deliberately left alone during the
Part VI build rather than deviating from house precedent on 14 slides; **fix it in one pass
across all seven decks, or not at all** — a half-fixed set is worse than a consistent flaw.

## What the checker cannot see, and what to use instead

`check_deck.py` measures **vertical height only**. Two stronger instruments:

- **`pdfinfo` page count is the better ground truth for overflow**: 43 pages for 43 slides
  means zero overflow, full stop. The height measurement is a proxy for this.
- **`pdftoppm` rasterisation is the ONLY way** to catch wrapping inside `pre` blocks and
  table cells. Every horizontal defect this project has hit was invisible to every script and
  visible immediately in a rendered page.

Tooling trap: `pgrep -f 'python check_deck'` **self-matches the polling command's own shell
wrapper**, so an `until ! pgrep …` loop never exits. The `[c]heck_deck` bracket trick fixes
the process match but still self-matches on any echo string containing the literal name.

## What the checker cannot see

`check_deck.py` measures **height**. It is therefore blind to every horizontal defect:
text clipped at the page edge, `<pre>` blocks wrapping and orphaning a line, a table
running past the margin. On Part IV, **three of the four real defects were invisible to
it** and were caught only by looking at rendered pages.

A clean `check_deck.py` run is necessary and nowhere near sufficient.

## The verification sequence

1. `check_deck.py` — catches vertical overflow.
2. **Slide count must equal PDF page count.** Check on *every* rebuild, not just the
   first — it earned its keep three times on Part V alone. A caption that grows by a few
   characters has pushed a deck from 32 pages to 33 here.

   ```
   grep -c '<section class="slide' slides/<deck>.html   # NOT 'class="slide"'
   pdfinfo slides/<deck>.pdf | grep Pages
   ```

   **`grep -c 'class="slide"'` is wrong and undercounts every deck in this set**, because
   it misses every slide carrying a modifier class. Measured: it reports 30/18/17/6/6
   where the true counts are 37/32/49/44/46. The form above agrees with `pdfinfo` on all
   five. (`check_deck.py`'s own regex was always correct; only this instruction was broken.)
3. **Rasterise and look** — `pdftoppm -png -r 80 -f N -l N`. Sample by *category*, not by
   position: **every page carrying a code block**, and the widest table. Enumerate the
   defect classes the checker cannot see before deciding what to inspect.
4. Extract any SystemVerilog back out of the finished HTML and lint it with `slang`.
   Sweep `-G` over mode parameters for generate branches. Delete the harness.
5. Banned names, including the documented false positives: the ordinary English
   "chips it", and `idma` inside the cited surname **Davidmann**.

## Making the trim converge

**Micro-trimming prose returns exactly zero.** If a shortened paragraph still occupies
the same number of lines, the page is unchanged — roughly eight of fourteen trim batches
on Part V moved nothing at all. Only **whole-line, whole-bullet, whole-row, whole-element**
removals change the page count.

To turn a binary pass/fail into a gradient, render each slide alone on an oversized page
(`@page { size: 264mm 1200mm }`), read the maximum `yMax` from `pdftotext -bbox`, and
compare against 421 pt. Calibration from Part V: a slide measuring **41.9 pt over** did
spill to a second page, while small positives fitted — so treat **~40 pt+ as real** and
small positives as noise, with `check_deck.py` as the oracle. An 8-thread parallel
version of that measurement runs in ~2 minutes against >20 serial, which is what makes
the iteration loop practical; `check_deck.py` itself exceeds a 120 s foreground timeout.

**Never build while a checker run is in flight.** A foreground `micromamba run … weasyprint`
contends with a background run on the mamba lock. The failure mode is exactly the stale-PDF
symptom above — a warning prints, the old PDF stays, and the page count you read belongs to
the previous version. The mtime check catches it either way.

## What no tool checks at all

Every gate here is mechanical, and **none of them can see a sentence that is true,
well-written, and not in the book.** Part V shipped a slide note asserting what a lab
does when selecting trace signals — plausible, useful, and absent from the chapter. It
survived overflow, lint, name and count checks because no tool checks provenance.

Give every slide a `<!-- src: chNN:lines (what was abridged) -->` comment above its
banner, and **diff each slide's assertions against its own source range before the first
build**, not after. Abridge code by whole declaration, never with an ellipsis inside a
construct.

## Settling a CSS question

"Does this deviation from the house sheet earn its place?" is answerable empirically in
one run: revert to the house CSS, rebuild, run the checker, count the failures. On Part
IV the revert produced five overflows, which settled it in minutes and produced better
evidence than any amount of reasoning about it.

## Size

40–48 slides. Part III ran 49 and that was judged one too many. Four chapters of
material is a lot to compress: **cut a topic whole rather than thinning every topic**.
A deck that teaches five things well beats one that mentions twelve. State what you cut
and why, so the next editor knows it was a decision.

## Built so far

| Part | Deck | Slides |
|---|---|---|
| I Foundations | `part1_foundations` | 37 |
| II Planning and Measurement | `part2_planning_measurement` | 32 |
| III Dynamic Verification | `part3_dynamic_verification` | 49 |
| IV Static and Formal | `part4_static_formal` | 44 |
| V Beyond RTL Simulation | `part5_beyond_rtl` | 46 |
