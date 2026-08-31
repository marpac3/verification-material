# Preface

## Why this book exists

Hardware functional verification is taught in pieces. There are good books on
simulation-based methodology, good books on formal property verification, good
papers on coverage, and standards documents for each of the languages involved.
What there is very little of is an account of how the pieces bear on one
another — of how a decision made in a verification plan determines what a proof
can discharge, of what a coverage number means once formal results are merged
into it, of which questions survive every instrument a project can afford. Those
are the decisions a verification lead actually makes, and they fall in the gaps
between the existing literature.

A second reason is narrower and more uncomfortable. Several of the figures this
field repeats about itself — where verification effort goes, how often first
silicon succeeds, what a bug costs at each stage — are older than the people
repeating them realise, and some trace back to no primary measurement at all.
A book that argues from evidence has to say which numbers survive being looked
up. This one does, and it names the ones that do not.

## What this book is

It is an account of hardware functional verification as a single discipline.
It covers planning and measurement; simulation-based verification and the
methodologies built on it; assertions; formal property verification and
equivalence checking; static analysis, clock- and reset-domain crossing;
gate-level and power-aware verification; acceleration, emulation and FPGA
prototyping; hardware-software co-verification; analog-mixed-signal, safety and
security verification; post-silicon validation; and the economics and metrics by
which all of it is judged. It treats these as one subject because a project does
not get to choose one of them, and because the interesting decisions are the ones
about where the boundary between two of them should fall.

The organising claim is that verification is an argument about evidence, not a
sequence of activities. A verification plan is a set of claims; coverage is a
sample of a model somebody wrote; a proof holds under assumptions somebody
discharged or did not. Every technique in this book is presented as an instrument
that produces a particular kind of evidence, with a stated reach and stated blind
spots, and the recurring question is which instrument answers which question, at
what cost, and what remains unanswered when it has.

## What it is not

It is not a manual for a methodology library, and not a tool tutorial. It names
tool categories — simulator, formal tool, emulator, linter — and does not
recommend products. Where a technique is inseparable from a standard, the
standard is named precisely, with its issue and its clause, because that is the
document a reader has to open to check the claim.

It is also not a survey. A survey reports what has been published; this book
takes positions, and marks them as positions. Where the literature is divided,
the division is described rather than averaged away. Where the published evidence
is thin — and in several areas of this field it is remarkably thin — the book
says so instead of filling the gap with confident prose.

## Who it is for

Two readers, with different needs and one book.

The first is an engineer who does verification and wants the parts of the
discipline they have not had occasion to use: a simulation-based verification
engineer meeting formal property verification, or a formal engineer being asked
about coverage closure. For that reader the chapters are self-contained enough to
be entered directly, and Appendix B gives reading paths that name what each path
equips you to do and what it leaves out.

The second is an engineer moving into verification from design. That reader is
the reason the book develops its arguments from first principles rather than
assuming a methodology background, and the reason a single worked example system
recurs from beginning to end.

## The example systems, and why they are constructed

Almost every example in this book runs on one of two constructed systems: a
modest reference SoC, and a later, larger flagship SoC from the same fictional
lineage. Their parameters are fixed and published, they do not change between
chapters, and a bug found in Chapter 1 is still the same bug in Chapter 26.

The choice is deliberate and it has a cost worth stating. A constructed example
cannot be looked up, and no reader can check it against a datasheet. What it buys
is that the example can be complete: every parameter that an argument needs is
available, the same crossbar can be examined from six different techniques'
points of view, and a coverage model can be given cell by cell rather than
gestured at. Examples drawn from real silicon are complete only where the owner
chose to publish, which is rarely where a teaching argument needs them.

Claims about real organisations are a different kind of claim, and the book keeps
the two apart. Where it reports what a named company did, that report comes from
a published source — usually that company's own conference paper — and is cited
to it. Where it reports what the industry does in aggregate, it names the study
and its year.

## The evidence discipline

The book was written against a closed corpus of documents held in full text:
papers, conference proceedings, standards and books. The rule was that a claim
either carries a reference into that corpus, or is presented as the author's
position, or does not appear. Nothing is cited from memory of a paper.

Three habits follow from that rule and are worth naming, because they show up in
the prose:

**Statistics are dated.** A figure about first-silicon success or about where
verification effort goes is a measurement of a particular year, and the year is
given. Several widely-repeated numbers in this field are older than the people
repeating them realise.

**Quantities are derived where they can be.** Where a number in an example can be
computed from the example's own parameters, the derivation is shown, so that a
reader who disagrees can find the step they disagree with.

**Absent evidence is reported as absent.** There is no industry-wide data on
several questions this book has to address. Saying so is more useful than a
plausible estimate, and it tells a reader where their own measurements would be
worth more than any citation.

## How this book was made

It was written with substantial help from large language models — specifically
Anthropic's Claude, using models in the Claude Opus family for drafting,
adversarial review and citation checking, and Claude Fable and Opus models to
coordinate work across chapters. The method is described here rather than buried, because a
reader is entitled to weigh it.

Chapters were drafted against the corpus and the style contract, then reviewed by
an independent adversarial pass whose task was to find unsupported claims,
misattributed citations, arithmetic that does not hold, and internal
contradictions; findings were then applied by a third pass empowered to refuse a
finding it judged wrong. Citation checks were done at page level against the
source document. Mechanical gates guard the classes of defect that reading does
not catch: that every citation marker resolves; that no number, code block or
cross-reference moves during an editorial pass without a stated reason; that no
hedge is lost, because a rewrite that drops *typically* or *up to* has
strengthened a claim its source does not support; that every figure and table is
captioned and every reference to one resolves; and that the one term this book
redefines against common industry usage — *validation* — never drifts in either
direction. Eight neighbouring terms are counted rather than enforced, on the
reasoning that a gate can compare occurrences but cannot read a sense, and that a
count which moves deserves a person's attention rather than a build failure. Each
gate was tested against a deliberate defect before being trusted, on the
principle that a check nobody has seen fail is not a check.

The editorial passes were designed against the published measurements of what
goes wrong when a language model edits a long document — that damage is sparse,
severe and silent; that rewriting inflates certainty while appearing to preserve
meaning; and that on already-clean text a model's precision at deciding what
needs changing collapses. The mitigations chosen follow from those measurements
rather than from intuition about them, and where the literature offers no
measurement, this book's method says so rather than borrowing confidence from an
adjacent result.

That procedure has a known ceiling, and the honest statement of it is this: an
automated reviewer sharing an author's blind spots will not see what the author
did not see, and grounding a reviewer in sources improves how it judges a claim
put in front of it far more than it improves what it thinks to check. The defects
this method catches are misattribution, contradiction and arithmetic. The defect
it catches least well is the fluent passage that is simply wrong and that nobody
thought to question. Readers who find one have found something the process could
not, and the author would like to know.

## Acknowledgements

**Use of generative artificial intelligence.** Anthropic's Claude was used in
preparing this book, as described in "How this book was made" above: models in
the Claude Opus family for drafting text, for adversarial review of drafts, and
for verifying citations against the cited pages, and Claude Fable and Opus models
for coordination across chapters. No text was published without being read. The
systems are tools and not authors, they are not credited as authors, and the
author accepts full responsibility for the whole of the content, including any
error the review passes failed to catch.

*Personal acknowledgements to be written by the author.*
{: .cp-note }
