# Style Guide — "Hardware Verification: A Holistic Guide"

Master language: **English**. (Italian translation happens later, chapter by chapter,
against the approved bilingual glossary.)

## Voice and register

> **Contract revision 2 — 2026-08-27.** Revision 1 specified "a professor-practitioner:
> authoritative, warm, direct; second person welcome" and a chapter skeleton opening on a
> narrated scenario. Measured against the finished text, that contract produced what the
> author rejected: three chapters (ch03, ch04, ch07) opening on the same workplace vignette
> — a manager asking when verification will finish — plus aphoristic closers and
> course-handout apparatus. The defect was in this file, not in the chapters. Revision 2
> replaces the register and the skeleton. Any agent reading this must use revision 2 and
> must re-stat this file before concluding a review.

The register is that of a **scientific and editorial manual**: a monograph an engineer
consults at a desk and a technical publisher would be willing to set. It is not a trade
book, not a course handout, not a consultant's deck. Four rules follow, and each overrides
a habit that reads as competent writing elsewhere.

- **Assert; do not narrate.** A chapter or section opens by naming its subject and its
  scope, then develops it. It does not open on a scene, a meeting, a dialogue, a character,
  or a job title used as a narrative device. Anecdote is not evidence, and a book whose
  chapters open on the same vignette has a formula rather than a voice.
  **Concreteness is not what goes.** The concrete system, its parameters and its numbers
  stay — they are the author's first requirement. What goes is the theatre around them.
  Convert "the program manager asks the verification lead when they will be done" into the
  engineering problem itself: what quantity must be reported at month four, which candidate
  answers are not checkable, and why.
- **Precision carries the register.** Prefer the number to the adjective, the mechanism to
  the metaphor, the named artifact to "industry practice". A quantitative claim states its
  quantity and its date; a normative claim names the document, its issue and its clause; a
  contested claim names who contests it. Vague intensifiers ("dramatically", "hugely",
  "the only question that matters") are not emphasis — they are the absence of a number.
- **No aphorism, no rhetorical question, no hortatory close.** Sentences of the form
  "One of these teams can be managed. The others can only be hoped for." are trade-book
  cadence: they compress an argument into a slogan and put it beyond checking. State the
  argument. A section ends when its subject is finished, not on a beat.
- **Hedges are load-bearing and must survive editing.** "may", "typically", "in the cases
  reported", "on the designs measured" are precision, not timidity. Deleting them to sound
  more authoritative converts a measured claim into a false one — a documented failure mode
  of register rewriting (certainty inflation). If a hedge is removed, the claim behind it
  must have become unconditional, and something must show that it did.

Mechanics: present tense; active voice; third person and the impersonal as the default.
Second person is permitted only in genuinely procedural passages — a checklist, a step a
reader performs — never as the subject of an argument, and never as "we" standing for the
reader. Explain *why* before *how*: the book teaches judgment, not tool operation.
**Well written, never needlessly verbose** (explicit author requirement): each paragraph
earns its place, one sharp example beats three vague ones, no marketing language and no
filler transitions.

- **Vendor-neutral in prescription, industrially specific in evidence.** These pull in
  opposite directions and both hold. *Prescription*: the book never tells a reader to buy
  or run a named commercial product; it names tool **categories** (simulator, formal tool,
  emulator, linter). That is the vendor-agnostic mandate and it stands. *Evidence*: the
  book names the real artifact, always. A protocol is defined by a document with an issuing
  body, a designation, an issue and a clause — "AMBA AXI (Arm IHI 0022, Issue H.c) §A5.2.2"
  — and the book says so rather than referring to "the bus protocol". An industrial
  practice is something a named organisation published about itself, and the book names the
  organisation and cites the paper. "Industry practice shows…" with no artifact behind it is
  not evidence, it is filler.
  **The bar for naming a real company, product or silicon:** a full-text source in the
  corpus, opened, supporting *that specific claim*. Parametric recall about a real company
  is never sufficient and never ships. Where the corpus cannot support an anchor, the
  example stays on the reference SoC — an honest fictional example is far better than a
  real-sounding claim nobody can check.
- Define every term of art at first use, in one clause, then keep using it.
- **`meta/glossary.md` is binding vocabulary, not a summary.** Where it defines a term,
  the book means that and nothing else. The live trap: this book defines **validation**
  as *checking a design on real hardware rather than on a model — post-silicon on
  fabricated parts, or in the lab on a prototype* (glossary; ch20 owns the term and
  states it in full at §20.1). The load-bearing contrast is **hardware versus model**,
  not fabricated versus FPGA: everything before tape-out is *verification*. Using it in
  the Boehm "did we build the right thing?" sense contradicts the glossary and would
  mistranslate into Italian; so does narrowing it to fabricated silicon, which would
  put ch18's lab work outside a word ch20 explicitly extends to it. Before leaning on a
  term's "well-known" sense, grep the glossary for it.
  **Attributing a definition is itself a claim.** ch18 glossed the term and credited
  ch01 with wording ch01 does not contain — the *usage* was compliant, the *attribution*
  false, and no check catches that because the sentence is true and the pointer is to a
  real chapter. Cite the artifact that actually carries the definition, and open it.
  **The carrier is paraphrase, and the check is on the SUBJECT, not the presence.**
  Paraphrasing close to a source preserves the source's vocabulary along with its
  claim, so a banned *sense* of an allowed word walks in behind an accurate citation.
  P21 (the post-silicon anchor) uses *validation* in the industry's umbrella sense
  throughout; ch18 imported it three times before a sweep caught it. Nothing mechanical
  sees this — the word is allowed, only its subject is wrong. So after drafting, grep
  each glossary-controlled term in the finished text and interrogate **what each
  occurrence is about**: every use of *validation* must take real hardware as its
  subject. A count of occurrences proves nothing.
  **The fix is word-level and citation-preserving**: keep the claim, keep the marker,
  swap the term ("checking" is usually right). Rewriting the claim to dodge the word
  loses the grounding for no gain.
- **A cross-reference is a claim.** "As Chapter 3 showed…" asserts that Chapter 3 showed
  it. Open the chapter and confirm before writing the pointer — a false cross-reference
  is indistinguishable to the reader from a real one, and survives every mechanical check.

## Chapter structure (mandatory skeleton)

1. **Opening problem statement** (~half page, no heading — it IS the chapter opening):
   the chapter's problem posed on a concrete system, in engineering terms. Name the
   system and the parameters that matter (reference SoC or flagship, from
   example_bank.md), state the question that must be answered and what makes it hard,
   and say what a wrong answer costs. **Keep the numbers; drop the theatre.** No
   characters, no dialogue, no meeting room, no job title as a narrative device, no
   "month four of the project". A worked quantity in the first paragraph is worth more
   than any scene.
2. **Chapter map**: one short paragraph of numbered signposting — "§8.1 defines the
   layered testbench; §8.2 develops the driver–monitor split; §8.5 treats the failure
   modes." Replaces the former "What you will learn" bullet list, which is
   course-handout apparatus and reads as such.
3. **Body sections** as per outline_master.md, each with at least one concrete
   example (Scenario box / worked example — formats in example_bank.md).
4. **In practice** box(es): what teams actually do, including the messy parts —
   **each anchored to a named source**. An "in practice" claim with no artifact behind
   it is folklore presented as reporting: either cite the corpus source, attribute it to
   the reference SoC as a constructed example, or cut it.
5. **Pitfalls**: 3-6 numbered common mistakes, each one line of symptom + one of cure.
6. **Summary**: 4-7 bullets, heading level `##`. (Renamed from "Key takeaways", which is
   handout vocabulary; the rename also settles the pre-existing `###`/`##` split that
   left the heading at two different levels across the book.)
7. **Further reading**: corpus sources first (by [cit:ID]), then non-corpus
   references (books not in corpus) clearly marked as such.

## Examples (the author's #1 requirement)

- Every central concept must be grounded in "in this scenario you use this,
  because…". Use the casts and canonical parameters from `example_bank.md` —
  never invent conflicting parameters, never name the real IPs.
- **Variety (author requirement)**: the reference SoC is the backbone, NOT the whole
  world. Every chapter must ALSO include 2-3 examples drawn from other IPs — the
  supporting/extended cast in example_bank.md (GPU, video codec, Ethernet TSN,
  crypto engine, HBM controller, coherent hub, USB, flash controller, …) or a
  fitting new one (add it to the bank if recurring). Pick the IP whose failure
  modes best illustrate the concept, not always the same three blocks.
  Run `tools/check_variety.py book/chNN.md` after writing or fixing a chapter. It
  counts distinct extended-cast IPs and flags any mentioned once and never inside a
  scenario box, code block or table — the shape an example takes as it decays into a
  bare cross-reference. It cannot judge whether an example is substantive; that stays
  human. **A warning means go and look. Never pad a chapter with an IP's name to
  clear it** — that defeats the check's entire purpose.
  Watch concentration too: widening from three backbone blocks to ten cast members
  and then leaning on four of them satisfies the letter of this rule and misses its
  point.
- At least one **worked example** per chapter with a real artifact sketch
  (a coverpoint, an SVA property, a vplan row, a bug report, a checklist excerpt).
  Code snippets in SystemVerilog where natural, minimal and correct, in fenced blocks.
- **Verify claims about your OWN code as rigorously as claims about sources.** Every
  behavioural statement the prose makes about a snippet ("this can never fail",
  "this bin is unreachable", "these counts always agree") must be re-derived from
  the code as if reading it cold — the most common defect in code-bearing chapters
  is prose that the accompanying artifact contradicts. Lint the snippets extracted
  back out of the finished chapter, never the scratch harness.
- **Lint traps.** (1) `slang --lint-only` does NOT elaborate `bind` directives: a
  bind whose `.*` ports cannot resolve passes lint silently. Check bind-based checkers
  with full elaboration (`--top`).
  **(1b) The obvious sanity check is unsound — read this before trusting a bind gate.**
  Breaking a signal name **in the bind target** does *not* error: implicit-net rules
  silently materialise the missing signal as a wire, visible only under `-Weverything`
  as `-Wunused-implicit-net`. Breaking a port name **on the checker** does error. So the
  two directions are not symmetric, and the target-side one — the direction that catches
  a real mis-wiring — fails to fail. Working recipe: a leading harness file containing
  `` `default_nettype none ``, compiled with `--single-unit --top <target>`. (slang
  10.0.138 has no `--default-net-type` flag.) Any bind-bearing chapter verified without
  this was verified by a gate that could not fail.
  **(1c) The trap is form-specific, and knowing which form you have tells you how much
  the harness is doing.** With a *named-port* bind — `u_chk (.wake_req(wake_req))` — the
  connection expression is exactly what an implicit net can materialise, so the naive
  gate reports `0 errors, 0 warnings` on a broken target name: the harness is doing all
  the work. With a `.*` bind there is no connection expression to materialise, so slang
  errors on its own (`could not find connection for implicit named port`), and the
  harness is belt-and-braces. Never infer from a clean `.*` result that the gate is
  sound — the next chapter may use the named form. `.*` also enforces type equivalence
  as an *error*, not a warning, which is what makes a mis-parameterised bind fail loudly
  instead of connecting a 4-bit port to a 7-bit signal.
  (2) `--top` alone is still not sufficient: a directive inside a parameterized
  `generate` branch is invisible unless that branch elaborates. Sweep the mode
  parameters (`-G MODE=0`, `-G MODE=1`, …) with a deliberate break in each branch.
  (3) For any BOUND checker, resolve "which agent does this instance check?" before
  writing a single claim about its covers — a claim that is true at the interconnect
  level often inverts at the port level. (4) A `bind` with no parameter override takes
  the checker's *defaults*: `bind … u_chk (.*)` silently used a 4-bit ID where the
  design needs 7, because `.*` connects only when types are equivalent (LRM §23.3.2.3).
- **Lint and md5 verify the artifact, never the prose about it.** A declaration can
  compile cleanly and still not be what the sentence claims: an unbounded `[$]` queue
  is legal SystemVerilog and unusable in a proof model. The gap between "it compiles"
  and "it is what the sentence says it is" has to be closed by re-deriving from the
  declarations by hand.
- **A DERIVED number beside a MEASURED one inherits its authority without its evidence.**
  This guide's own length calibration read "12 chapters = 106,800 words = 207 pp". The page
  count was measured and right; the word count was back-computed from it at an assumed 516
  words per page against a true 419, so it was 25% high — and it sat in the sentence that
  every length verdict in the book was decided by, for months. The two numbers looked
  equally solid because they were printed the same way. **Say which is which, and make any
  figure a chapter is judged against reproducible by a one-line command.**
- **A pipe hides a failing exit status.** `python3 tools/build_book.py … | tail` returns 0
  even when the build raises `ModuleNotFoundError` — verified: direct status 1, through a
  pipe 0, with `set -o pipefail` 1 again. Any agent reading the result through a pipe saw a
  green build that never happened. Same family as the unsound negative control: **the
  reporting channel manufactured a pass.** Check the status directly, or `set -o pipefail`.
  And always invoke the build through `micromamba run -n gvsoc_env_3_12` — the system
  `python3` has no `markdown` module. **Under parallel-agent load `micromamba run` serialises
  on `~/.cache/mamba/proc` and can block indefinitely**; the environment's own interpreter,
  `/home/marco.paci/.local/share/mamba/envs/gvsoc_env_3_12/bin/python`, is the identical
  environment with no lock. Two agents lost time to this today. The same applies to
  `weasyprint`: run it as `… /bin/python -m weasyprint`, never as a bare `weasyprint`, which
  resolves to a broken build that writes nothing and silently leaves the stale PDF in place.
- **A review's PRESCRIPTION must never contain an unsourced number of the same shape as the
  defect.** When the diagnosis is "this value has no source", a fix that supplies a
  plausible substitute value reproduces the defect while appearing to close it — and it is
  the most common way a correct finding gets refused. **Name the sourcing procedure, not a
  number.**
- **A gate reimplemented per chapter is not a gate.** Density was checked by a fresh
  throwaway script every time, and the scripts disagreed — some counted a bulleted list as
  one paragraph, some did not. Every one of them reported a clean verdict in the same
  words, so the reports were indistinguishable while the checks were not. Same shape as the
  unsound negative control below: **an ad hoc check produces a uniform-looking verdict from
  a non-uniform procedure.** If a rule is worth enforcing on every chapter, write it down
  as a tool and make it *failable* — then prove it fails on a constructed case before
  trusting any pass it reports.
- **A control counts as fired only when an ERROR LINE NAMES THE MUTATED TOKEN.** Two
  conditions are not enough — pristine clean, mutant errors — because a broken *declaration*
  also produces errors, and they get banked as proof the gate works. The third condition is
  what separates the two. With it, the book-wide sweep classified 1,262 mutations into 753
  fired, 319 correctly rejected as declaration-site breaks, and 190 non-firing names that
  are declaration-only by nature (assertion and generate labels, coverage bin names, enum
  members, DPI formal-argument names). Without it, all 1,262 would have read as success.
  **Exception — and it splits by MUTATION SITE, not by construct.** Measured on one chapter's
  own `bind`, both directions confirmed:
  - **Target-side *declaration*** — can never satisfy the third condition. The bind's own text
    stays intact, so the error names the stale *reference* (`wake_req`), not the mutated
    declaration (`wake_reqQQ`). A sound probe that the gate is live; **not** a fired control.
    Label it separately so it cannot borrow a real control's authority.
  - **Named-port *connection expression*** — **does** satisfy it: the expression is a
    reference the elaborator resolves directly under `` `default_nettype none ``, and the
    error reads `use of undeclared identifier 'wake_reqZZ'`. This is a genuine fired control.

  Both directions still return `0 errors` **without** the leading `` `default_nettype none ``,
  so the underlying trap is unchanged — the harness is what makes either one able to fail.
- **If the harness regenerates around the mutation, the gate can never fail.** Build the
  declarations ONCE from the pristine text, hash them, and re-verify the hash after every
  mutation. The natural implementation — regenerate the harness for each mutant — quietly
  declares the broken name into existence and reports a clean compile forever. This is the
  general form of the unsound-control family: **a checker that adapts to the defect cannot
  detect it.**
- **slang does not deeply elaborate a class that is never instantiated.** A class inside a
  module, extending an entirely unknown base, containing undeclared references, compiles
  with `0 errors`. Any class-bearing snippet must sit at `$unit` scope with a real base and
  be exercised (`new()` plus `randomize()`) or the gate is hollow — one chapter's block
  initially scored 0 fired out of 9 mutations for exactly this reason.
- **A negative control must break a REFERENCE, never a declaration.** A global rename
  (`sed 's/sig/sigXY/g'`) rewrites the port declaration along with every use, leaving the
  snippet internally consistent: the compiler returns `0 errors` and the gate reports a pass
  it could never have withheld. Worse, it yields the sentence *"the control fired"* from a
  run that could not have failed — a **fabricated proof of verification**, and the most
  expensive kind of false confidence in this project, because everything downstream trusts it.
  Same family as the unsound `bind` check above. **Break one use site and confirm the error**;
  if no break can make the gate fire, the snippet is not being checked at all — report that,
  never a pass.
- **"This IS a deviation, but I'll keep it" is a STOP SIGNAL, not a decision.** A deck agent
  genericised a domain's indexing vocabulary, noticed mid-task that it was deviating from the
  chapter, and then argued itself back into the deviation — which had detached a table of
  thresholds from the very term that indexes them. It caught this only on a second pass. **The
  moment that sentence forms, the answer is already no**: an author who has to justify a
  deviation to themselves has established that it is one, and the justification is being
  written by the party that wants it.
- **Deleting a noun phrase ORPHANS the pronouns that pointed at it — three sentences away.**
  Removing a scoping clause stripped the antecedent for "the other model" further down the
  paragraph, and **the defect surfaces nowhere near the edit**, which is why a diff review
  cannot see it. After deleting any noun phrase, **grep the rest of the paragraph for
  pronouns and definite descriptions** ("the other", "that one", "the same") and check each
  still resolves.
- **The corpus can contradict ITSELF, and then the claim is unsupportable from it.** Two
  sources in this corpus name different underlying models for the same system. Neither is
  checkable against the other, so any claim resting on that identity must be dropped rather
  than adjudicated — **record the conflict and stop asserting the point**, keeping whatever
  the argument still stands on without it.
- **Deleting a clause silently RE-POINTS its citation.** Remove one half of a compound
  sentence and the marker stays put while what it asserts changes — it now vouches for the
  surviving clause, which nobody checked. After any clause-level deletion inside a marked
  sentence, **re-confirm the marker against the surviving proposition** by opening a page,
  not by inferring from the page you opened for the deleted half. That inference is the very
  move that produces this defect class.
- **When a review's diagnosis is "this universal is false of member N", DELETE the universal
  rather than repair it.** Two successive drafts — the reviewer's and the fix agent's own —
  restated it in fresh words and both failed on the same member. The preceding sentence
  almost always already carries the argumentative work the universal was doing. If you do
  repair it, **re-test the new wording against member N specifically**, by name.
- **Prove an edit inventory COMPLETE by reversing it.** Reconstruct the pre-edit file by
  undoing every recorded anchor, asserting each appears exactly once, and check the word
  count returns to the original. Two files came back at exactly 5,994 and 7,519 — which
  proves the reported edits are the *only* changes, something no diff of the final state can
  establish about a report.
- **A source's INDEX answers "does it state this at all" faster than reading.** One book's
  back matter is a word concordance; intersecting three content words across their page lists
  localised a proposition to a single page in two image reads, after three pages of reading
  had failed. Also: **a PDF-to-printed page offset is not constant across a book** — it moved
  by three pages between regions of the same volume. Recompute it from a footer in each
  region rather than carrying one offset across.
- **When a hand-rolled check FIRES, verify the checker before the artifact — and a MIXED
  result is the tell.** One ID checker manufactured two failures out of twelve: its pattern
  missed the bibliography's actual entry format, and one ID passed for the wrong reason by
  matching an unrelated table elsewhere in the file. **A real gap would not clear ten IDs and
  fail two adjacent ones**; that asymmetry is evidence about the procedure, not the data.
  Three separate agents wrote a wrong grep today, and every one of them was caught by the
  result looking implausible rather than by inspecting the pattern.
- **Cost an edit `wc -w` on the FILE, before and after — never on the excised string.** A
  leading comma counts as its own token when isolated but attaches to the preceding word in
  place, so `", debugging in waveforms"` measures −4 standalone and costs −3 in the file.
  Four of seven delta corrections in one pass traced to that single effect.
- **Over a word cap, delete WHOLE UNITS — never rephrase.** Nine compression passes of
  20–40 words each were mostly cosmetic, and three of them silently damaged accuracy: a
  truncated list, a deleted evidence clause, and a dropped source the text still described
  elsewhere. **Compressing a sentence edits away the qualifiers that carry its evidence**,
  and the damage is invisible afterwards because a shorter true-sounding sentence leaves no
  trace of what it dropped. At 700 words over, cut a bullet, a source entry, a whole
  paragraph — then re-verify what remains.
- **Citation COUNT misindexes source weight.** A source can sit behind two markers and carry
  a whole section, or behind twenty with its heaviest use outside the chapter its title
  implies. **Read weight from where the substance lands**, not from marker frequency — and
  when a title and a usage pattern disagree, the title is what will hide the source from the
  reader who needs it. Seven sources in this corpus are misindexed that way.
- **Each chapter's "From the corpus" / "Not in the corpus" further-reading block is a
  pre-existing, chapter-authored index of source weight and of the corpus's own gaps.**
  Extract those first for any work spanning the whole corpus — it turns an inference from
  titles into a checkable claim.
- **"Never date from an arXiv ID" runs in BOTH directions — it cannot refute a date either.**
  A reviewer challenged two bibliography dates on the strength of their identifiers (`2510`
  reading as October against a stamp of 16 Sep; `2402` reading as 2024 against a v4 stamped
  25 Feb 2026). Both entries were right and the challenge was wrong: **the identifier encodes
  the announcement of one version, not the date of the version in hand.** The printed stamp on
  page 1 is the primary evidence. Note the trap in the second case — v1 and v4 fell in the
  *same month two years apart*, which reads as agreement to a quick glance and as a
  contradiction to a careful one, and is neither.
- **Old results get LESS scrutiny because they feel settled.** In a chapter split between
  two-decade-old classical work and brand-new results, the new material — the part everyone
  expected to be shaky, and where the checking effort went — came back near-flawless, while
  **three of seven HIGH findings landed on the settled classics**: a static model described as
  dynamic, a figure that was the chapter's own arithmetic presented as a stated cost, and a
  "could not be approached" where the source reports 28 successes. **Budget scrutiny by how
  familiar a claim feels, inversely.**
- **Two concepts sharing a NUMERAL defeat every phrase-grep.** ch14's one section holds "two
  symbolic addresses" for one design and "two caches, one address" for another; a grep on the
  shared numeral matches both and distinguishes nothing, which is how a chapter came to
  describe the first abstraction with the second's parameters — and to transplant the
  justification of one onto the other. **When a search term is a number, the search has not
  disambiguated anything**: read the surrounding sentence for the noun the number counts.
- **A REVIEW's own assertions fall under the review's own taxonomy.** One review wrote "all
  29 glossary terms clean" *before* checking them; the check then produced a finding and
  cleared a separate suspicion, so the promise was wrong in both directions. Another costed
  its fix list wrong twice and caught it on a closing self-check. **Audit your own report
  before shipping it** — a fabricated verification inside a review is worse than a missed
  defect, because everything downstream treats it as evidence.
- **A prescription is DRAFT PROSE and can simply be ungrammatical.** Three proposed fixes in
  one review were broken as English — a participle governing a second conjunct, a deletion
  stranding a parenthetical behind a comma, an insertion landing inside a closing bold. The
  reviewer caught its own. **Never paste a prescription: read the resulting sentence whole.**
- **Lead a finding with SOURCE-EXTERNAL evidence; put the elegant in-chapter proof last.**
  A reviewer's prettiest support is often an in-chapter counterexample — and if it turns out
  soft on a full reading, a fix pass that checks the boldest bullet first may dismiss a sound
  finding on the strength of its weakest leg. **Order the evidence by robustness, not by
  elegance, and label each leg's scope.** Corollary for fix agents: **judge a finding on its
  strongest support, not its first bullet.**
- **A heading is seductive evidence — treat "I read the heading" as UNVERIFIED.** Section
  titles routinely appear to contain the claim verbatim, and three appendix claims rested on
  headings alone; opening the sections confirmed two and destroyed the third, which had
  attributed to a chapter a term of art that chapter never uses. **Open the section.** Same
  family as verifying a stated location by grepping the load-bearing noun rather than the
  shared phrase.
- **When a word cap collides with a required element, pay out of the least-compressed prose
  — never delete the requirement.** Trading a required element for a word count is a net
  defect, and it is invisible afterwards because the deletion leaves nothing behind. **Record
  the trade in the report**, so the caller sees a judgment instead of discovering a gap.
  (Also: `wc -w` counts a spaced em dash as a token, so em-dash-heavy prose costs more
  against a cap than it looks — budget trims accordingly.)
- **The same misattribution in two chapters means the SOURCE was misread once and the
  reading travelled.** A page saying three separable things had the wrong one attached in
  ch26 and, independently, in ch06 — in opposite directions. Treat every such pair as a
  propagation event, not two coincidences: **grep the source ID across all chapters and read
  each hit's proposition**, because the misreading is in the shared understanding of the
  page, not in either sentence. The tell is a page cited repeatedly on a subject it only
  partly addresses.
- **A word can contradict the clause it modifies.** "Traded off against one another
  *independently*" is self-refuting — being traded off against one another *is* the
  dependency. No source check is needed to see it, and no source check found it. **Read the
  sentence as a sentence before reading it against the source**: the citation audit and the
  sense audit catch disjoint defect sets.
- **A "protected passages" list handed to a fix agent is a COMPRESSION, and compressions
  lose carve-outs.** A brief protected one chapter's handling of a standard wholesale; the
  source review's own CLEAN table had explicitly excepted one line of it. The fix agent
  recovered it only by re-reading the review instead of trusting the summary — and noticed
  that the brief's own wording ("do not add specificity") permitted the fix, since a hedge
  *removes* assertive force. **Give the fix agent the review, not your reading of it**, and
  when you do summarise, say the summary is lossy and name the source to re-read.
- **Check for declared EQUIVALENCE before checking for a carve-out.** An apparent rule
  violation dissolved outright because the owning chapter states that `ok |-> !err` and
  `err |-> !ok` are *logically equivalent* and tells you which phrasing to prefer: once two
  forms are equivalent there is no privileged polarity left to invert, so the obligation
  attaches to the preferred phrasing's antecedent. That is a **stronger refusal** than an
  exception, which merely excuses the case rather than dismantling it.
- **A finding's PREMISE is auditable separately from its prescriptions — audit it first.**
  One finding offered two fixes, both defective; arguing them one at a time would have cost
  twice as much as checking the premise, which turned out to misstate the rule it invoked.
  **Refuting the premise kills the finding once.**
- **Audit prose-to-code universals in BOTH directions.** ch21 said "every band lives in one
  package — every checker and every coverage bin quotes it", and a bare literal sat in the
  covergroup twelve lines below: the precise shape that chapter's own Pitfall 1 forbids. The
  reviewer had checked the artifact's arithmetic and its enumeration, but never checked the
  artifact against **the sentence introducing it**. Reading code→prose finds a wrong count;
  only reading prose→code finds a violated universal.
- **When a finding names both an artifact defect and the prose defending it, the PROSE is the
  primary edit.** Swapping the value is mechanical; the justification is where the defect
  actually lives. ch21's first draft fixed the constant and left the circular sentence that
  justified it by pointing at the artifact's own value — the same defect in new costume.
- **Before sourcing a new number, try RE-ANCHORING the existing one.** When a review forbids
  inventing a value, the fix is often not an external source at all: ch21's tolerance was
  wrong because of *what the percentage was taken of* — a band computed on the measured
  signal shrinks to nothing as the signal does. Referencing it to the fixed full-scale value
  instead cured it with **zero new magnitude introduced**, which no external number could
  have matched for safety.
- **State a rule's carve-outs WHERE THE RULE IS STATED.** ch11 gave the cover rule
  unqualified in one section and practised two documented exceptions in an earlier one,
  twenty to forty lines away. That gap is the whole causal chain: it is why ch23 paraphrased
  the rule narrowly, why the narrow paraphrase then excused a real violation, and why a
  book-wide audit against the unqualified wording generated findings on *compliant* code.
  A reader copying the rule's line as their reference gets the absolute version. **A rule
  and its exceptions are one artifact; separating them manufactures both false positives
  and false negatives.**
- **Match a rule by IMPLICATION, not by text.** One cover, `(level == DEPTH) && push && pop`,
  discharges the vacuity obligation of two assertions whose antecedents are `push` and `pop`,
  because it implies both. Any checker comparing antecedent *text* against cover *text*
  false-positives on that shape forever — and a fix agent acting on the false positive would
  add two covers that are true in nearly every cycle, which demonstrates nothing.
- **A chapter's paraphrase of a house rule can be NARROWER than the rule it cites.** ch23's
  Pitfall 1 restates ch11's "every implication ships with a `cover` on its antecedent" as
  "every *denial* property needs a cover" — so a positive obligation slips through, and an
  audit conducted against the local wording clears a genuine violation. **Audit against the
  owning chapter's rule, not the citing chapter's summary**, and treat a narrowed restatement
  as a defect in its own right: it will be read as the rule by anyone who meets it first.
- **After an edit that LENGTHENS a set, the stale sites are not only the numerals.** Adding a
  sixth property to a list of five refreshes every universal about that set ("all of them read
  always-on signals", "none looks back more than one cycle") into a new claim about the new
  member — and prose the reviewer verified against the *shorter* list can acquire ambiguity
  no count-grep sees. ch23's fix created an adjacent two-sense collision in a line that had
  been verified CLEAN before the edit: **a prior clean verdict expires when the environment
  around it changes.**
- **A stated ORDERING is a machine-checkable claim, and correcting a provenance breaks it
  silently.** The glossary note promised entries "in the order the book introduces them";
  six rows violated it, and **three were created by today's own owner corrections** — moving
  `validation` from ch01 to ch20 changes where the row *belongs* without moving the row. The
  other three predated them, so the note had been false for a while and nothing noticed,
  because a claim about a table's *shape* is invisible to every check that reads its *cells*.
  When ordering and grouping conflict, ask which one the reader came for: here the
  deliberately adjacent collision pairs are the glossary's whole point, so the **note** was
  wrong, not the table. Beware the obvious script: grepping the row instead of the column
  manufactures false positives out of the cross-references in the definitions themselves.
- **A hand-written metadata constant either derives from the content or diverges from it.**
  The title page carried `SUBTITLE = "Parts I–IV"` while the delivered PDF contained Parts
  I–V — a wrong claim on the *cover*, past every check, because no check tied that string
  to the chapters actually built. Every mechanical guard we own reads the chapter *bodies*;
  the apparatus around them (cover, running heads, TOC labels, deck titles) is unguarded by
  construction. **Derive it, or it will drift the moment the scope grows** — and scope grows
  by default in a book written Part by Part.
- **Grep the PROPOSITION before the label.** ch23's sweep over every `TM-0` row ID was
  internally consistent and returned a clean verdict; the contradiction surfaced only from
  grepping what a row was *about* (working key + debug port), because the offending line
  named no row ID at all. **A contradiction hides precisely where the label is absent** —
  an ID-grep can only find sites that remembered to cite the ID.
- **When two findings touch one line, the review must state an apply order.** Otherwise a
  numeral-only edit lands on text the second finding was about to change, and that finding
  goes silently unreviewed. Same family as the transposed-location class: after applying
  the first fix, **re-read the whole sentence** rather than substituting into it.
- **Byte-identity proves FILE identity, never ENTRY identity.** A DVCon slug derived from
  a filename returned 200 at an entry with the *same title, same edition, same year* —
  and the wrong record: the archive held both a Paper and a Presentation, and the corpus
  file belonged to the `-2` sibling. A 200 at a plausible slug is not a match. **Only the
  candidate entry's own Download href proves which entry serves the file**, and author
  *order* on the title page is a cheap independent confirmation. (Slugs fail three ways:
  a `-presentation` qualifier must be dropped; a filename that lost a space 301-redirects
  rather than 404ing; and a derived slug can return 200 at the wrong record. `urllib` gets
  403 from that host — use `curl`.)
- **A conference name in a PDF `Author` field is template lineage, not a venue.** One paper
  carries `Author: DVCon Europe` and is a DVCon **India** paper — the field belongs to the
  Word template, inherited by anything written for any edition, exactly like the stale
  symposium strings on four other entries. Contrast a **submission ID** (`DVCON2010_108-PY527`):
  it names one conference *and* one submission, so it is genuinely editorial. The test is
  specificity, not which metadata field it sits in.
- **The strongest in-document year evidence in a slide deck is a reproduced dated
  third-party artifact** — a press-release headline date, a dated article URL path segment.
  It is static content about an *external* event, so no re-export can regenerate it. That
  is precisely what a PowerPoint auto-date field is not, and the auto-date is what produced
  this project's seven-year error.
- **Measure a gap before sizing the work to close it.** A handed-over list of ~24 missing
  bibliography entries measured out at 8: the rest were corpus entries mistaken for
  citations. `comm -23 <cited> <entries>` settles it in one command. Same rule as any other
  handoff claim — the notes are not the evidence.
- **A stated corpus gap is a HYPOTHESIS to test, never a finding to inherit.** ch21 was
  briefed that the corpus was thin on mixed-signal and to expect a judgment-heavy chapter.
  Checking `corpus_index.md` first overturned that: 26 markers, every one resolved to an
  opened page, from six sources. **A warning about a gap reads as a licence to stop
  looking** — which is exactly how a gap becomes self-fulfilling. Check before planning
  citations, and **report the correction**, because the acquisition list is downstream of it.
- **Two speedup figures from different baselines never chain into a ladder.** D19's 24×
  (RNM vs SPICE, 2011) and D30's 90× / 230× (SV-RNM vs Verilog-AMS, 2015) measure
  different things. Multiplying them, or presenting them as a progression, invents a
  figure neither source supports — the same shape as treating two independent anchors as
  a quotient. State each with its baseline, and say they do not compose.
- **A paper's year does not date a datum the paper inherited.** D27's headline effort
  figures trace to its own reference "Based on … Consulting, Inc. experience" — an
  *undated experiential assertion* sitting inside a 2015 paper. Stamping 2015 on them
  dates the datum from its container, one level further out than the usual trap. Cite
  such figures undated with the basis named in prose.
- **Glossary collisions arrive most often through DESIGN-side vocabulary, not testbench
  vocabulary.** "read-retry sequencer" is natural hardware English and silently imports
  the UVM component's bound meaning. The term sweep must interrogate the **subject** of
  each occurrence; a count proves nothing.
- **A marker governing a LIST must be asked separately of every item.** Attaching a
  citation to a list's lead-in, then adding bullets under it, silently extends the
  source's authority over claims it never made. **The density check passes on both the
  right and the wrong attachment**, so nothing mechanical distinguishes them. Audit every
  list-governing marker item by item *before* the density pass — ch22 caught two
  near-misses of exactly this shape.
- **A table ROW can be one claim, not N independent fields.** ch23's threat-model rows
  pair an obligation with the column saying how it is discharged: writing the *verifiable*
  half of a channel into a row marked "argued, not verified" makes the table assert the
  opposite of the section that explains it. Both cells are individually true; the row is
  wrong. Read each row as a single proposition before checking it against the prose — and
  when a row carries two claims of different kinds, **split it into two rows** rather than
  softening either. Related: **"always-on" and "a power domain that goes down" are
  mutually exclusive assertions about the same block**, and the conflict is **not confined to
  proof-tractability arguments** — it first appeared in one, then turned up in a code comment,
  then inside a scenario box's checklist line with no proof argument anywhere near. Treat it
  as a property of the *block name*: **grep the block across all 26 chapters and the bank
  whenever any text puts a domain down.** Name the switchable sub-block instead — but note
  the trap that follows: **naming a different domain is itself a sourcing claim.** If no
  chapter states what that block retains, or across whose power-down, the fix is to use an
  existing sourced seam, not to substitute a domain name that sounds right. Supplying an
  unsourced *name* is the same defect as supplying an unsourced *number*.
  When you edit a row, **grep its ID and read every hit in full** — ch23 had five sites
  for one row ID and the writer had read three.
- **A handoff summary is a claim, and it can be fabricated.** A context-compaction
  summary written by this project asserted an edit to ch01 — a word count, a line, a
  rationale — that had never happened. It was caught only by verifying against **file
  state** rather than against the notes. Notes about work are not evidence of work.
  Before building on any summary of your own or another agent's — a compaction summary,
  a review's "already fixed" list, a status report — **stat and grep the artifact**.
- **A review's DIAGNOSIS and its PRESCRIPTION are separately auditable.** The diagnosis
  is usually sound because it is evidence-backed; the prescription is drafting, and
  drafting carries no evidence. ch19's reviewer correctly identified an uncited "10×"
  floor — and proposed replacement wording containing *another* uncited floor of the
  same shape, which would have produced a chapter that looked fixed and was not. **Fix
  the finding; do not adopt the wording.** This is where defects re-enter a corrected text.
- **A hedged claim and its unhedged restatement are ONE defect, not two.** ch19 stated
  the same unsupported proportion three times and only one instance carried the
  `[UNVERIFIED]` tag. Reframing the tagged line alone would have left the Key takeaway
  asserting it flatly — in the most quotable position in the chapter, stripped of
  context. **When resolving an `[UNVERIFIED]` tag, grep the PROPOSITION across the whole
  chapter before editing the tagged line.**
- **A review's word-costing is unreliable in exactly one direction.** A fix that *removes*
  an item from a list is costed at the deletion alone, because the reviewer does not
  re-read the downstream text against the shortened list. One ch19 fix was costed at −3
  words and actually cost +13, because the next sentence's example lost its antecedent
  when the list shrank. **After any list-shortening edit, re-read the following two
  sentences for referents that just went missing.**
- **When restoring a dropped clause, the CONSUMER settles its polarity.** ch20 had
  compressed ch07's question "why did no checker catch it — *or could none have seen
  it?*" down to its first half, and the first restoration attempt wrote "or could have
  seen it" — the opposite claim. Compressing a clause into apposition silently drops a
  negation, and both readings *sound* fine in isolation. What disambiguates is the later
  paragraph or table row that runs on the clause: ch20's *Propagation* row is about the
  platform gap, which only the negative form supports. **Read the consumer before
  choosing the wording**; the source sentence alone will not settle it.
- **Fixing an underivable figure at its ROOT can expose precision the text never had —
  do not then paste that precision beside a rounded derivation.** ch20's "of order 10¹²
  cycles" was underivable because no clock rate existed anywhere in the project. Adding
  the clock band to the bank fixed the root, and re-deriving showed the chapter's
  dependent figures were *conservative* rather than merely unchecked. The right move was
  to name the clock and leave the round-number chain the chapter shows its own working
  for. Inserting the precise range next to figures computed from the round one would
  have manufactured a non-composability defect while curing an underivability one.
- **Two figures from one source may be independent anchors, not a quotient.** P21 p. 71
  gives both "several years on an RTL simulator" for an OS boot *and* that same boot "in
  a few hours" on an accelerated platform. They are separate measurements, not two ends
  of a ratio: dividing "several years" by the 100–1000× band yields about eleven days,
  which composes with neither. That gap is precisely what tempts a writer to quietly
  soften the cited "years" into "months to years" — a citation-fidelity defect born from
  trying to make two sound anchors agree. **Quote both, and let the section's stated
  order-of-magnitude disclaimers carry the non-composability.** Deriving one cited figure
  from another is a new claim, and it needs its own grounding.
- **For an inverted enumeration, reorder the list rather than re-index the sentence.**
  ch17 said "Four things… **Three** of them restate the guidelines; **the fourth** is…"
  with items 3 and 4 swapped. Re-indexing to "the third" reads as an index *into* the
  three and creates a fresh ambiguity; moving the item leaves the sentence true and
  unambiguous. Reordering is safe only after grepping for positional references to that
  list from other chapters — cheap to check, and it is what licenses the better fix.
- **A chapter can carry the disproof of its own advice, hundreds of lines away.** ch18
  recommended a free-running counter "in the always-on domain" as the shared timestamp
  for correlating firmware logs, in-fabric monitors and the trace buffer — while the same
  chapter, 220 lines earlier, had established that the always-on 32 kHz reference does
  not scale with the prototype and therefore cannot separate bus-level events. Both
  statements are individually sound and every mechanical check passes; only the pair is
  wrong. **Advice is a claim about the chapter's own established facts** — before
  recommending a mechanism, grep the chapter for what it has already said about that
  mechanism's limits.
- **Verify a stated LOCATION by grepping the load-bearing noun, not the shared phrase.**
  Two sites in ch18 both read "a lower bound with an unknown gap"; one was about
  *performance* (correct — a partitioned prototype under-states it) and one about
  *latency* (inverted — cross-device links and reduced clocks over-state it). A grep for
  the shared phrase matches both and distinguishes nothing. Applying a correct fix at a
  transposed line number introduces a defect while preserving the original one, so a
  location is a claim to check, not a coordinate to trust. (`sed -n 'Np;Mp'` prints in
  file order, not argument order — an easy way to transpose two sites while reading.)
- **A defensive edit is a claim too.** A review proposed "115 seconds" → "115 seconds per
  run" as insurance, "faithful under either reading". It was false under exactly the
  reading it was meant to insure against. Hedging wording is not automatically safe;
  re-derive it like any other claim, and prefer the original when the review's own
  primary verdict was "no change required".
- **Adding to a provenance-bearing file silently falsifies its ENUMERATED prose.** Counts
  ("twenty-one such entries"), superlatives ("the first arXiv entry"), exception tallies
  ("the second author-list exception"), registry lists — these are auditable assertions,
  not decoration, and **no build step checks any of them**. The build validates that
  every ID resolves; it cannot see that a sentence about how many IDs there are has gone
  stale. After any insertion into `references.md`, `corpus_index.md` or `glossary.md`,
  **grep for number-words and superlatives** and re-check each against the new state.
  Five such claims went stale in one five-entry addition.
- **Corroboration between two artifacts a single event generates jointly is not
  corroboration.** A bulk re-export makes a PDF timestamp agree with a slide footer; an
  arXiv v1 makes the printed stamp agree with the ID prefix. Both agreements are
  manufactured, and the first shape produced this project's seven-year error. Demand a
  signal of a *different kind*: a conference submission ID or a printed copyright block
  (editorial facts a re-export cannot forge), or an in-document bound — the newest work
  the document itself cites, since nothing can cite the future. **Classify the artifact,
  not its content**: that is what separates a submission ID from a creation timestamp
  when both present as "PDF metadata".
- **DVCon slugs are not derivable from filenames.** `dvcon-proceedings.org` resolves
  entries at `/document/<slug>/`, but the slug may drop trailing filename qualifiers —
  one paper serves as `…-industrial-results-presentation.pdf` while its entry lives at
  `…-industrial-results/`. When a derived slug 404s, `wp-content/uploads/<filename>`
  still fetches the file, and MD5-comparing it against the local corpus copy proves
  entry identity outright. `-2`/`-3` siblings are different conference *editions*, never
  duplicates. Never resolve via `?s=`.
- Reuse the **canonical recurring bugs** so the book feels like one coherent project.
- Reuse **canonical artifacts** (example_bank.md "Canonical artifacts") by copying them
  VERBATIM — never re-derive a recurring property/covergroup from memory. Before
  introducing a named artifact, grep the other chapters for that name and match the
  canonical version exactly.
- **A right number can carry a wrong reason, and only the reason is wrong.** A count is
  auditable by recomputation; a *reason* is auditable only by re-deriving it from the
  artifact it claims to describe. The book stated that 6 coverage cells were "dead by
  geometry, before any constraint" — the count was right, the mechanism was not: the
  load-bearing premise ("a row is at most 256 beats") is a line in `c_solver_budget`,
  an engineering choice about solve time. **When a derivation cites a bound, find where
  that bound is written**: if it lives in a constraint block, the exclusion is policy —
  revisitable, and owed a waiver — not structure. This class survives every mechanical
  check, because the number it decorates is correct.
- **When propagating a fix, grep the PREMISE, not the conclusion.** Searching for the
  conclusion's wording ("by geometry") missed 3 of 9 sites; searching the load-bearing
  premise ("256 beats", "shorter than the row") found all of them. A site that states
  the premise without the conclusion is exactly the one a conclusion-grep cannot see —
  and it is often the source, since the premise is where the reasoning starts.
- **A convention is a premise in portable form — and it outlives the fix.** The same
  wrong premise had been compressed into a phrase the book *teaches*: ch05's "100%
  means 100% of what the geometry can reach". Nine direct sites were corrected and
  that one survived, because it reads as a principle rather than as a claim about the
  six cells — and ch09 then quoted it verbatim, re-importing the refuted premise into
  a chapter that had just refuted it. Worse, ch05 contradicted itself two paragraphs
  apart: the earlier paragraph correctly called the exclusion a chosen budget. **After
  correcting a premise, search for the slogans, conventions and italicised maxims that
  encode it**, and check the chapters that quote them. A maxim is the most durable
  carrier a bad premise has: it is short, it sounds like wisdom, and it gets cited.
- **Never re-derive a count about a canonical artifact — quote the bank.** Cell counts,
  unreachable-bin counts, port indices, field offsets and ID widths live in
  example_bank.md "Canonical numbers", each with its derivation. Copying code but
  recomputing the numbers about it in your head is how "three of the 72 cells"
  reached four files before anyone checked it (the answer is two). Where the bank
  supplies a derivation, restate the bank's derivation; do not construct your own.
  If the bank looks wrong, fix the bank and propagate — never write a divergent
  number in a chapter.

## Citations (rigor contract)

- Only sources listed in `meta/corpus_index.md` may be cited, as `[cit:ID]`
  (e.g. `[cit:B2]`, `[cit:D14]`). Multiple: `[cit:B2,D14]`.
- **Before citing, verify**: open the PDF (Read with targeted pages / grep) and
  confirm it actually supports the claim. Never cite from memory.
- Every quantitative claim (percentages, effort data, trends) MUST carry a citation —
  industry numbers come from the WRG 2024 reports [cit:R1,R2] or Foster's DAC study.
- A claim you believe true but cannot support from the corpus: either reframe as
  practitioner judgment ("in practice, teams observe…") or tag `[UNVERIFIED]` for
  the review pass. Never fabricate a source.
- Books/papers NOT in the corpus may appear ONLY in Further reading, never as [cit:].
- **Audit propositions, not phrases.** A citation audit that greps the claim's English
  wording produces false negatives at a high rate: a source states an idea in its own
  words, and books index by mechanism, not by your sentence. Before concluding "the
  corpus does not support this", search the claim's mechanism terms (for a peer-review
  claim: `peer review`, `bug in the testbench`, `skipped`, `bypass`) and read the
  surrounding pages. A marker on the WRONG source looks identical to an unsupported
  claim — the fix is often re-marking, not reframing. Three successive audits cleared
  ch04:216 as unsupported by phrase-matching; the claim is stated outright in B2 pp. 98-99.
- **Split the claim class finely enough before suspecting a source.** "Review practice"
  is two classes, not one: **peer/code review** → B2 pp. 29, 98-99 (B1 contains zero
  occurrences of either phrase), while **planning and requirements-gate review** → B1
  ch. 2 (rule set 2-x, printed pp. 17-34) and the testcase-status-table passage at p. 263.
  A sweep run on the coarse class would have "corrected" 94 sound markers. Coherence
  auditing is only as good as the granularity of its claim classes — when a whole class
  looks misattributed, suspect the class boundary first.
- **The arXiv-ID trap runs in BOTH directions.** It over-dates (`2405` on a 2022 study)
  and it under-dates (`2207` on a 2023 AITest paper). The reliable tell is not direction
  but **agreement**: when the ID year is the only signal producing the prose's year —
  metadata, the source's own newest reference, and CrossRef all disagreeing — the year
  came from the ID. `api.crossref.org/works?query.bibliographic=<title>&rows=3` resolves
  a preprint to its real venue and year with no DOI in hand.
- **Before adding a year, name the artifact it comes from and check it is data-bearing.**
  A book's publication year, a PDF's creation timestamp and an archive's re-export date
  are container properties, not the date of the datum. "Date the data" never licenses
  stamping a container year on an undated statistic — that IS the defect. Where no year
  can be substantiated (B2's undated "about 70% of the design effort"), leave it undated
  and let the prose qualify it as the commonplace it is.
- **Re-marking is a two-edit operation.** Before adding a marker, check whether the
  paragraph already carries one for that source: marker density (≤1 per source per
  paragraph) means the existing marker moves rather than a second one appearing.

### Citation RENDERING — unobtrusive, numbered (author requirement)

- `[cit:ID]` markers are converted at build time to per-chapter numbered references
  `[1] [2] …` (order of first appearance) with a numbered References list at the
  chapter end. Write `[cit:ID]` immediately after the claim, nothing else.
- **Do NOT narrate sources in the prose.** The default form is claim + marker:
  "Verification consumes about 57% of project time [cit:P17]." — NOT "Foster's
  2015 DAC industry study, based on the Wilson Research survey, shows that…".
- Naming an author/work in the body is allowed ONLY when the source's identity is
  part of the argument (a famous formulation, a school of thought, a historical
  episode) — budget: 1-2 naming instances per chapter. Everything else: numbers.
- Never put a work's full title in the body; titles live in References/Further reading.
- **Marker density: at most ONE marker per source per paragraph**, placed at the last
  claim drawn from it. Verifying every sentence against a source naturally produces a
  marker per sentence, which renders as "[3]. … [3]. … [3]" and is exactly the
  obtrusive citation style this book rejects. Verify every sentence; mark once.
  **The rule targets redundancy, not distinct claims — apply the surviving-marker test.**
  Before deleting a marker, ask whether the one you are keeping still covers the claim
  the deleted one carried. Two markers to the same source in one paragraph are correct
  when they carry two claims the source treats separately — two different statistics,
  say — because a reader chasing the second one must not be sent to a marker that was
  placed for the first. Collapsing those strips a claim of its support, which is a
  worse defect than the density it cures.
  **Sibling list items are not one paragraph.** A Pitfalls or Takeaways list with one
  marker per bullet renders as a single `[n]` per item, not as a run-on, and each bullet
  is a distinct claim by construction. Counting them as a dense paragraph is a unit
  error; when a stated count disagrees with the measured one, reconstruct the unit
  definition before assuming either number is wrong.
  **Book-wide result, 2026-08-27**: 19 of 27 files clean; the rest carry candidates, densest
  in the chapters built on survey statistics. **Sampled, not exhausted** — the two densest
  paragraphs were checked by hand and both are *correct*: three markers to one source
  carrying a statistic, a cultural diagnosis, and a replacement cost, where deleting any one
  would send a reader chasing that datum to a marker placed for a different claim. Expect
  statistics-heavy chapters to show many legitimate candidates; a high count is not a defect
  signal on its own.
  **Run `tools/check_markers.py <chapter>` — do not hand-roll this check.** It was
  hand-rolled once per chapter, and at least two of those throwaway scripts split on
  blank lines only, turning every bulleted list into one dense "paragraph" and reporting
  violations that were not there. The tool reports *candidates*, never verdicts: a hit
  means the surviving-marker test above must be applied by a human, and two markers to
  one source are correct when they carry two claims that source treats separately.
- **Never date a statistic from an arXiv ID.** The digits encode the UPLOAD month, not
  the study year: `2405.17481` is a September 2022 manuscript. Date from the PDF's own
  metadata (`pdfinfo` CreationDate) plus the newest reference the paper itself cites.
  The same caution applies to DVCon PDFs, whose venue year lives at the volume level.
- **Date the data**: every statistic carries its year in the prose ("14% in 2024"),
  and when multiple corpus sources cover the same quantity, the most recent one wins
  (older figures may appear only as explicit historical contrast).
- **A quoted figure is not yours to tighten. DO NOT REGRESS: ch17 §17.1 says
  "several years", and that wording is P21's own.** The source states, verbatim
  (p. 3 of the tutorial): *"an activity that would take a few seconds of execution
  time on the target silicon (e.g., booting an operating system) would take several
  years on an RTL simulator"*. An arithmetic audit will notice that the chapter's own
  billion-to-one ratio makes a few seconds of silicon nearer a century than "several
  years", conclude the phrase is loose, and shorten it to "years". That audit is
  wrong, and it has already been run once and acted on before the deck for Part V —
  built earlier, from the same source, and carrying a slide headed *"Do not divide
  these"* — showed that the two figures are independent anchors quoted from one
  source rather than a ratio and its quotient. The chapter already discloses the
  imprecision two paragraphs later. **The rule generalises: before adjusting a
  quantity, establish whether it is the book's derivation or the source's word. If it
  is the source's word, the only permitted change is to the surrounding prose.**

## Formatting

- Markdown. Chapter file starts with `# N. Chapter Title` (N = chapter number).
  Sections `##`, subsections `###`. No deeper nesting.
- Scenario boxes as blockquotes: `> **Scenario.** … **Approach.** … **Why.** …`
- "In practice" and "Pitfalls" as `### In practice` / `### Pitfalls` near the end.
- Diagrams: Mermaid fenced blocks (```mermaid) where a picture genuinely helps
  (flows, architectures, lifecycles); keep them simple, label in English.
- Tables for enumerable comparisons only; prose carries the argument.
- Cross-references to other chapters as "(see Chapter N)" — plain text, no links.

## Length targets — RECALIBRATED against 12 measured chapters

`outline_master.md`'s page targets were estimated before any chapter existed and are
**systematically ~50% low**. Measured against the built PDF: Parts I-II estimated
~86 pp, delivered 114; Part III estimated ~58 pp, delivered ~93.

**Corrected 2026-08-27 — the earlier word figure here was derived, not measured.** It
read "12 chapters = 106,800 words = 207 pp, i.e. ~8,900 words per chapter". The page
count was real; the word count was back-computed from it at an assumed **516 words per
page**. The true density, measured on the delivered 364-page PDF, is **419 words per
page**, so the word figure was inflated by ~25% while the page figure was right. Actual
counts on disk: **12 chapters = 85,242 words; all 26 = 199,022 words, mean 7,655**
(≈18 pp) including apparatus.

Two lessons, both already general rules below: a **derived** number sitting beside a
**measured** one inherits its authority without its evidence, and any figure a chapter
can be judged against must be reproducible from the artifacts by a one-line command.
Recompute before citing this block: `for f in book/ch*.md; do wc -w < $f; done`.

**Use these as the real targets**, and read `outline_master.md`'s numbers as *relative
weights* (a "16 pp" chapter is the heavy one of its part; a "8 pp" chapter is the light
one) rather than as absolute counts:

| outline says | write to | why |
|---|---|---|
| ~8 pp | 5,000-6,000 words | the part's light chapter |
| ~10 pp | 6,500-7,500 words | the house's actual practice at this nominal target |
| ~13 pp | 7,500-8,500 words | |
| ~16 pp | 8,500-9,500 words | the part's centre of gravity |

**These are targets, not thresholds.** Measured dispersion around them is wide and always
has been — the delivered chapters run from 4,617 to 10,946 words — so a band is a signal
to look for padding, never a reason to cut on its own. Within roughly ±10% of a band, the
correct verdict is usually *earned*, and a review should say so plainly rather than
proposing cuts. **Never pay for length with a grounded scenario, a worked artifact, an
extended-cast grounding, or a citation**: those are requirements, and trading a
requirement for a word count is a net defect. If a chapter is genuinely long, the cut is
hedging, transitions, and re-derivation of material another chapter owns — and if a grep
for filler returns nothing, the length is the chapter's real size. Report it and move on.

The cause is not padding: it is that the estimate never priced the mandatory skeleton
(opening scenario, objectives, In practice, 3-6 Pitfalls, Key takeaways, Further
reading) plus 2-3 extended-cast groundings plus a worked artifact per chapter. Those
are all requirements, so the target — not the chapter — was wrong.

A false target does not restrain anything; it just makes every writer spend a paragraph
justifying an overshoot that is not one. Density is still the real constraint: **cut
before padding**, and cut redundancy and re-derivation of other chapters first — never
a worked example or an extended-cast grounding.

Projection at this rate: 26 chapters ≈ 450 pp. That is within the author's stated
mandate ("anche più di 300 se necessario, basta che sia ben scritto e non prolisso
inutilmente") — but it is a fact to state, not to discover at the end.

## Note for reviewer agents

**Re-stat the contract files before finalising.** Writers, fixers and reviewers run in
parallel against shared `meta/` files, so `style_guide.md` and `example_bank.md` can be
rewritten *during* your review — the length targets were, mid-review, on 2026-08-27.
A verdict quoting a superseded rule is worse than no verdict. Record the mtime you
judged against in your review's method note.

**Every table cell holding a number is a claim.** A cycle count, a proof depth, a bound,
a bit index, a percentage — check each against the rule the surrounding section teaches.
This class survives lint, variety, citation and banned-name checks, because none of them
reasons about the content of an example. Two instances found so far: a 64-cycle window
proved at depth 64 with its antecedent at cycle 12 (needs 76), and a connectivity
property asserting bit 6 for a signal the same chapter's scenario puts on bit 5.

**A diagram is a claim too — read its edges as a graph against the prose.** Readers
reproduce figures, so a diagram is operational advice whatever the surrounding text
says. Found live: a ch13 mermaid figure routed protocol checks and X-propagation into
the per-commit gate that the same chapter's prose excludes from it *twice*. Nothing
mechanical can catch this: the diagram renders, the prose reads correctly, and only
someone tracing the arrows against the sentences sees the disagreement.

**Containment is a claim too, and mermaid gets it wrong silently.** Mermaid creates a
node at its point of *first mention*, so an edge naming a node before the `subgraph`
that declares it hoists that node to the root graph — and it renders **outside** the
box. In a figure whose whole point is which side of a boundary a component sits on,
that inverts the assertion while the diagram still renders cleanly. Found live in ch08,
where `SEQ --> DRV` preceded the manager-agent subgraph and so drew the drivers outside
the agent that contains them — the opposite of what the chapter teaches, and in the very
figure another chapter had cited as the house pattern to copy. **Rule: declare then
connect** — close every `subgraph` before writing any edge that crosses one. `tools/check_mermaid.py`
enforces this across the book; run it on any chapter with a figure. It is a detector,
not a proof: it sees hoisting, not whether the boxes say what the prose says.

**"A diagram is a claim" generalises to any ORDERED table.** A power-up sequence, a
bring-up order, a tiering schedule: the table asserts an ordering, and the prose around
it asserts a second one, independently. They can disagree while each is internally
consistent — which is why checking the table's rows against each other proves nothing
about the paragraphs that reference it. ch19 hit this live: all four assertions checked
out against its power-up table, while the narrative described a bypass firing on
supply-good, which against that same table would have made the assertion fail on
*every* wake rather than on a rare race — destroying the escape's character while every
individual artifact stayed sound. **After any ordered table, re-read every paragraph
that references it and map each temporal claim onto a numbered step.** For an escape or
a bug scenario, the specific thing to verify is *rarity*: a mechanism that fires on
every pass is not an escape, it is a broken check, and that difference is the whole
pedagogical point of the example.

**A real marker on the wrong claim passes every automated check.** ID validity, density,
count, corpus membership: all of them pass, because the ID *is* real and the source *does*
exist. What fails is the attachment. ch20 caught this in its own draft: `[cit:D24]`'s
"six person-months → two person-days" is a **pre-silicon** effort comparison, and it had
been written up as a post-silicon localisation result — same source, same real ID, wrong
claim. The only check that sees it is re-opening the page and asking not "does this source
support something like this?" but **"does it support THIS claim, about THIS subject?"**
A lone marker deserves *more* scrutiny than a repeated one, not less: it gets less
attention from the writer, and it is where an attachment error hides.

**The claim just past the citation.** A marker can sit correctly on a supported claim
while the *next* clause — the one the author added as connective tissue — is false.
ch13 quoted the MTBF relation accurately, then said "everything else is linear"; the
source names two exponential terms three paragraphs on. When verifying a marker, read
far enough into the source to cover the sentence that follows it in the book.

## Output contract for writer AND fixer agents

- Write the chapter to `book/chNN.md` (two-digit N). Write it section by section
  (2-4k words per writing step) — do not attempt the whole chapter in one pass.
- End your report (not the chapter file) with:
  - `EXTENDED CAST USED:` every non-backbone IP you drew on, with its section number
    and one clause on what it illustrates. **This is a hard deliverable, not a
    courtesy.** Variety is the author's first requirement and it is the only one no
    mechanical check can see: banned names, unverified claims, citation IDs, marker
    density, lint and mermaid are all correctness checks. A chapter that drifts back
    to backbone-only passes every one of them.
  - `GLOSSARY CANDIDATES:` list of term → one-line definition for new terms of art
  - `[UNVERIFIED] COUNT:` how many unverified claims remain and where
  - `[REFLECTION]` / `[FINDING]` tags per the learning protocol

### Length is a tradeoff to state, not a target to hit silently

Reviewers must cost their **fix list** in words and reconcile it against the length
target **in the same report** as their cut plan. Costing the two independently is how
chapters inflate: in ch08 the cuts yielded ~480 words against ~1,200 words of mandated
additions, and the target was unreachable by construction. The author's constraint is
"ben scritto e non prolisso inutilmente" — well written, never needlessly verbose — not
a page count. An honest tradeoff statement is the deliverable; silent compression is not.

**Never pay for length with variety.** When a fix pass must cut, the second and third
examples look expendable and are not — that is exactly how ch08 lost its video-codec
clause. Cut redundancy, re-derivation of other chapters, and hedging prose first.

---

# The editorial passes (contract revision 3, 2026-08-27)

The book is complete and audited for correctness. What remains is to raise it from a very
good internal document to a manual of editorial standard. That work is split into two
passes with **opposite risk profiles**, and they must not be combined in one edit — a
combined pass has no cheap gate, because every check that would catch a bad rewrite is
also triggered by a legitimate addition. There is now a measured reason as well: document
damage compounds with both the scope of a mandate and the number of interactions, with no
plateau, and a combined pass enlarges the mandate on both axes.

**Revision 3 exists because revision 2 was written before the evidence base.** Three
measured results govern the design of this pass, and all three describe a defect that
revision 2's gates could not see:

1. **Frontier models corrupt what they were not asked to touch** — sparsely, severely and
   silently, with the great majority of damage arriving in a few catastrophic events, and
   the failure mode is *alteration* rather than deletion. Token counts survive it intact.
2. **Rewriting inflates certainty** in a large fraction of outputs, biased toward *more*
   certainty, and it does so *while semantic content is preserved* — so it is invisible, by
   construction, to every class revision 2 watched.
3. **Models cannot leave good text alone.** On the cleanest corpus measured, single-pass
   edit precision collapses to about a fifth of its value on error-dense text. This book is
   a clean corpus. Per-edit agreement voting roughly doubles that precision.

Full evidence, source by source, with the preprints and the gaps flagged:
`meta/research/revision_and_style_transfer.md`. The corrections it makes to revision 2 are
listed there in §8.

**The consequence for this manuscript, stated plainly: the correct Pass A output is a
small, high-precision diff, not a rewritten book.** A large diff is the failure mode, not
the deliverable. `meta/audits/register_precision.md` measures how small: of 502 sections,
the register defect is structural and concentrated, and most mechanical candidates are
cited industry data, protocol terminology, table cells or publication titles.

## The gates

Mechanically enforced by `tools/check_invariants.py`, which diffs a pre-pass snapshot
against the working tree. Every gate is a discrete token or byte check and none is a graded
similarity score — deliberately, because content-preservation similarity metrics are
measured to be unable to separate the style change we want from the content loss we forbid,
so a threshold on one would be a gate that does not measure what it claims.

| Gate | Mechanism | The failure it catches |
|---|---|---|
| **G1a** citations | `[cit:ID]` multiset unchanged | citation loss during rewriting |
| **G1b** numbers | numeric-literal multiset; no additions under Pass A; removals declared | invented or dropped quantities |
| **G1c** code | fenced blocks byte-identical, same order | code mangling |
| **G1d** cross-refs | no additions; removals declared | a false pointer introduced |
| **G1e** glossary | **per-occurrence subject check inside edited spans.** The count is a tripwire for gross change, not the gate — this guide says elsewhere, of `validation`, that "a count of occurrences proves nothing", and that judgement governs here too | the banned sense of an allowed word |
| **G2** hedges | hedge/epistemic multiset; **removals are fatal**, additions are not | **certainty inflation** — the measured, asymmetric defect that G1a–G1e cannot see |
| **G3** additivity / out-of-span | **Additive passes (B, C): mechanical.** Every diff hunk must be an insertion; a modified line passes only if characters were added and none removed, which is what permits a `[cit:ID]` marker at an offset inside an existing sentence and forbids rewording it. **Pass A: not mechanical** — an approved-span check needs a span list the tool does not hold, so it is enforced by reading the diff against the pre-pass snapshot and declaring the hunk count. | **silent corruption of untouched passages**: the frontier failure mode |
| **G4** length | words after ÷ words before; growth is the alarm direction | rigour-flavoured padding |
| **G5** span agreement | independent LOCALISE runs; a span acts only if agreed | over-correction of already-good text |
| **G6** coverage / anti-copy | every section carries a verdict; a fraction of "untouched" sections is re-inventoried by a fresh agent | **the do-nothing pass** — a byte-identical output passes every other gate perfectly |
| **G7** deletion budget | largest single contiguous deletion, in words | **passing the register gate by deletion**, which is this pass's form of the preservation trap recorded under Citations |
| **G8** anchor verification | Pass B only: 100% coverage, per anchor open the page and confirm the quote and that the claim is unchanged | a false anchor; a claim weakened to fit its source |

G2, G3 and G4 are the three that cover the frontier failure mode, and revision 2 had none
of them. Each gate was shown to fail against a deliberate defect before first use: a gate
that has not been seen to fire is not a gate.

**A correction to this contract, recorded rather than quietly fixed.** Revision 3 first
described G3 as mechanically enforced for every pass. It was not implemented at all, and
three separate agents reported the discrepancy from three chapters. Claiming a check that
does not run is the same defect this book criticises elsewhere — evidence asserted rather
than held — so the row above now states exactly which passes the mechanical form covers.
For the additive passes it is now real and negative-controlled: a caption inserted above a
table passes, a `[cit:ID]` marker inserted inside a sentence passes, rewording that
sentence fails with the before-and-after quoted, and deleting a line fails. For Pass A the
honest statement is that G3 is a reading obligation, not a tool, and the evidence for it is
a declared hunk count against the snapshot.

**Self-declaration is a cross-check, not a gate.** Models identify *that* a span needs
editing at roughly human-ceiling-minus-a-little, but identify *which defect it is* at
about 0.20 precision. So every removal and every hedge shortfall is derived **mechanically
from the diff**; the agent's declared report is used only to detect disagreement between
the two. A declared report that matches the mechanical diff is evidence. A declared report
alone is not.

## Pass A — register

**Mandate.** Bring the prose to the register defined in "Voice and register": remove
narrated openings, dialogue, job titles used as narrative devices, "What you will learn"
blocks, aphoristic closers, rhetorical questions and hortatory advice. Replace with scope
statement, numbered signposting, and assertion.

**Hard constraint: Pass A introduces no claims.** It is a framing edit.

**The writable unit is one section. The chapter is read-only context.** One agent per
chapter, for cross-reference resolution and consistency; but a section at a time, and each
section in **a single turn**. There is no self-review loop and Pass A is never run twice
over the same text: self-correction from self-generated feedback has no demonstrated
success on tasks like this one, degrades output in the nearest controlled study, and
compounds certainty inflation with each iteration. Any critique step must read an
**external** artifact — the snapshot, this contract, the checker's diff, a cited page —
never the agent's own prose about its own work.

**Pass A runs in two stages, and the span inventory is a first-class artifact.**

*Stage 1, LOCALISE.* Produce a span inventory: for each candidate, the verbatim span, its
line range, the clause of this contract it violates, its defect class from a closed list,
and every token at risk inside it — each `[cit:ID]`, numeric literal, cross-reference,
code fence, glossary-controlled term **and hedge**, listed individually. Output a direction
for the replacement, not the replacement text. **"NO SPANS" is a correct and expected
answer for a section already in the target register, and it is scored as a success** — an
inventory that manufactures work is the measured failure of this stage.

*Stage 2, EDIT.* Change bytes only inside approved spans. For each hedge in a span's
tokens-at-risk list, the hedge or its exact equivalent must appear in the replacement: a
claim that was conditional stays conditional, and dropping a hedge requires naming the
evidence that made the claim unconditional. Output the full section, a hedge ledger, and a
declared-removal list.

**The objective is every span that needs it and no others — not a minimal diff.** This
matters because the preservation language in this contract will otherwise select for
under-editing, and editing too few spans is measured to under-transfer badly. Restraint
is correct only where the text is already compliant.

**Span identification by pattern is not permitted to pre-approve an edit.** A pattern
matches a string; a defect is a use. In this book `manager` is AMBA AXI terminology,
`always` is normative specification language, and a question the text answers with evidence
is legitimate monograph prose. `tools/register_scan.py` produces **candidates**, and its
per-class measured precision is recorded in `meta/audits/register_precision.md`; a
candidate enters LOCALISE as a hint to confirm or reject with a stated reason, and only
`learn-header` has measured precision high enough to narrow a reader's attention. The one
exception is a span whose boundaries are **structural rather than a judgement** — a
`What you will learn` block, a chapter's opening paragraph — where the span is identified
by position and the reviewer's recorded verdict, not by a regex.

**Zero candidates does not mean clean.** The scanner's classes have low measured precision
*and unmeasured recall*. Narrated openings, aphoristic closers, and explanations that are
simplistic rather than wrong are not detectable by pattern at all. A section with no
candidates gets a cheaper check, not no check.

**Declared-removal report** is part of the output contract, not an afterthought:

```
PASS A REPORT — chNN
sections edited    : §N.M (span ids acted on), …
sections untouched : §N.M (verdict: no rule violation found; rules checked: …), …
numbers removed    : '340' (§4.0, seed count inside deleted vignette), …
crossrefs removed  : …
hedge ledger       : <hedge> | <span id> | present after: yes/no | if no, why
largest deletion   : <words>, and what content survives and where
invariant check    : PASS   (paste the tool's summary line)
```

## Where the human gate goes

**On the diff, after the pass, before it is accepted** — not on the output, and not as a
sample. Three reasons, each measured. Machine editorial judgement is least aligned with
human judgement precisely on strong material, which is what this manuscript is. Damage is
sparse and severe rather than diffuse, so the diff is small enough to read in full while an
aggregate score would average the damage away. And the agent's own account of its edits is
the least reliable part of its output, so the human must read the change, not the report.

Verification is **100% of loci, never sampled** — the profile of the damage (a few large
events) is the worst possible case for sampling. Order the reading queue by alarm: G2 hedge
shortfalls first, because a lost hedge is a false claim; then G3 out-of-span changes; then
G4 growth; then G7 large deletions. Sections that pass every gate with a small diff are
read last.

**Cross-chapter reconciliation** (glossary-term subjects, cross-reference resolution,
heading-level uniformity, designation/issue/clause strings) is worth running because its
targets are directly checkable artifacts. It is justified on checkability and cost only:
no study measures the effect of a reconciliation pass, and the nearest measured mechanism
predicts homogenisation rather than divergence. Do not claim a measured coherence benefit
for it.

## Pass B — industrial anchoring

**Mandate.** Attach real, publicly documented industrial artifacts to material currently
anchored only to the fictional reference SoC. Two classes, and they are not equally cheap:

1. **Normative identification (backbone; do this first).** Naming the document that
   defines something the book already uses is a fact about a document we hold. It carries
   near-zero factual exposure and it is the single highest-yield fix available: the book
   uses "AXI" 61 times and never names Arm, AMBA, or the specification. Source of truth:
   `meta/research/anchors_normative.md` and `meta/audits/spec_acquisition.md`.
   **Live hazard, from the acquisition audit:** the current issue of Arm IHI 0022
   (Issue L) **does not contain AXI4** — Issue J removed AXI3, AXI4, AXI4-Lite and ACE.
   The book's running example is an AXI4 crossbar, so every AXI4 and ACE claim must cite
   **Issue H.c**. Citing the current issue for an AXI4 rule is a false citation: the text
   is not in the document.
2. **Industrial cases (corpus-gated).** A claim about what a named organisation did ships
   **only** if it resolves to a full-text source in the corpus, opened, supporting that
   specific claim, at a stated page. Menu: `meta/research/anchors_industrial.md`. Nothing
   outside that register may be used. Distinguish self-reported practice from third-party
   description, and never dress a qualitative claim as data.

**Hard constraint: Pass B is byte-additive on existing sentences.**

Not merely "additive". As revision 2 wrote it, Pass B constrained citations,
numbers, code and cross-references but left the surrounding prose free — so an
anchoring agent could reword the very claim it was anchoring, which is both the
preservation trap named below and the frontier corruption mode. Tightened:

You **may**
- insert a new sentence, or a new bracketed clause, between existing sentences;
- insert a `[cit:ID]` marker at a declared character offset inside an existing sentence;
- append a new fenced code block, or a new "In practice" box.

You **may not** reword, reorder, shorten or re-punctuate any existing sentence.
If a claim cannot be anchored as written, the output is a **finding** — "this
claim needs a different source, or must be qualified by the author" — and never
a smaller claim. Byte identity of existing sentences is what gives the gate a
way to detect the violation; the principle alone gave it none.

| Class | Rule |
|---|---|
| Existing sentences | **Byte-identical**, except for an inserted `[cit:ID]` marker at a declared offset. |
| `[cit:ID]` markers | **No removals.** Additions expected — each must carry a source and page. |
| Numbers | **No removals.** Additions must be transcribed from the source, never computed to fit. |
| Code blocks | Existing blocks unchanged and in order; new blocks may be appended. |
| Cross-references | No removals. |
| Hedges | **No removals.** An anchor that drops a source's *up to* or *typically* has strengthened the claim past what the anchor supports. |
| Glossary vocabulary | `validation` used only in the sense the glossary fixes. |

**Per anchor, output:** the claim verbatim as it currently stands; the artifact
(for a normative one: issuing body, designation, issue, clause; for an industrial
one: corpus ID, page, and whether the result is self-reported or third-party);
the source's own words on that page supporting **this** claim; the exact bytes
being inserted and where; and `claim_unchanged: yes`. If that last line would be
`no`, the row is invalid and the correct output is a finding.

**Verification is at 100% coverage, not sampled.** The project's own factuality analysis
settles this: a clean 14-citation sample bounds the true defect rate only at 19.3%, and
below a ~5% true rate sampling is closer to a coin flip than to a gate. Every anchor added
by Pass B is checked, individually, against the page it cites.

**The preservation trap.** Any gate that asks "does the source support this claim?" can be
passed the cheap way — by weakening the claim until the source trivially supports it, or by
restating the source in its own words. This is measured, not hypothetical: in the RARR
experiments an editor optimising attribution alone scored *higher* attribution than the
balanced system while destroying the text (preservation 10.4 against 83.1). So an anchor
must not soften the claim it anchors. If the source will not support the book's claim,
the finding is "this claim needs a different source or must be qualified" — not "rewrite
the claim smaller".

## Verification: give the verifier a locus list, not a chapter

Do not ask a reviewer to "review the chapter". The relevant evidence on automated review
says that grounding a judge in sources improves how it *adjudicates a claim put in front of
it*, and barely improves *where it looks*; the residual failure is therefore **misses** in
passages that read fluently and trigger no lookup. Two instances of the same model share
that blind spot by construction, because the shared prior is in the weights and not in the
conversation.

The mitigation is to convert judgement into coverage. Enumerate the loci mechanically and
require a verdict **per locus**, with the evidence consulted named:

- every number introduced or retained in an edited span;
- every claim naming a real organisation, product or silicon — with the corpus ID and page;
- every normative identification — body, designation, issue, clause;
- every cross-reference, opened and confirmed;
- every code block in an edited section;
- every glossary-controlled term in an edited span, checked on its **subject** rather than
  its presence.

A verifier that returns prose without a per-locus table has not done the task.
