# Preface

## Purpose

Hardware functional verification is taught in pieces. There are good books on simulation-based methodology and formal property verification, good coverage papers, and standards documents for each language involved.
Very little literature explains how these subjects bear on one another. Little of it explains how a decision in a verification plan determines what a proof can discharge, that is, which of the plan's claims a proof can settle on its own. Nor does it explain what a coverage number means once formal results are merged into it, or which questions survive every instrument a project can afford. These are decisions verification leads make, but the existing literature leaves gaps between its subjects.

In the author's assessment, several figures repeated in this field are older than their use suggests, and some trace to no primary measurement. Among them are the figures for where verification effort goes, how often first silicon succeeds, and what a bug costs at each stage.
The book's evidence policy requires it to identify which numbers withstand scrutiny and name those that do not; this book does so.

## Scope

It is an account of hardware functional verification as a single discipline.
It covers planning and measurement; simulation-based verification and the methodologies built on it; and assertions. It takes up formal property verification and equivalence checking; static analysis, clock- and reset-domain crossing; and gate-level and power-aware verification. Its subjects include acceleration, emulation and FPGA prototyping; hardware-software co-verification; and analog-mixed-signal, safety and security verification. It covers post-silicon validation, and the economics and metrics by which all of it is judged. It treats these as one subject because a project cannot choose just one, and the decisions concern where the boundary between two techniques should fall.

The book treats verification as an argument about evidence rather than a sequence of activities. An argument here is a case built from evidence, not a disagreement. A verification plan is a set of claims; coverage is a
sample of a model somebody wrote; a proof holds under assumptions somebody
discharged or did not. Every technique in this book is presented as an instrument producing a particular kind of evidence, with a stated reach and stated blind spots. An instrument here is a means of measurement, and its reach is the range of behavior it can make a statement about. The recurring question is which instrument answers which question, at what cost, and what remains unanswered.

## Limits

It is not a manual for a methodology library, and not a tool tutorial. It names tool categories (simulator, formal tool, emulator, linter) and does not recommend products. Where a technique is inseparable from a standard, the standard is named precisely, because that is the document a reader has to open to check the claim. The name gives the standard's issue and its clause. The issue is the edition of the document, which matters because a specification's requirements change from one issue to the next.

Unlike a survey of published work, this book takes positions and labels them as such. Where the literature is divided,
the division is described rather than averaged away. Where published evidence is thin, as it is in several areas of this field, the book states the gap without substituting confident prose.

## Intended readers

The book serves two readers with different needs.

The first is a verification engineer seeking unfamiliar parts of the discipline: a simulation-based verification engineer encountering formal property verification, or a formal engineer asked about coverage closure. Coverage closure is the point at which every item of a verification plan has been either covered or consciously excluded. Chapters are sufficiently self-contained for direct entry, and Appendix B gives reading paths stating what each equips readers to do and leaves out.

The second is an engineer moving into verification from design. That reader is
the reason the book develops its arguments from first principles rather than
assuming a methodology background, and the reason a single worked example system
recurs from beginning to end.

## Constructed example systems

Almost every example in this book runs on one of two constructed systems: a
modest reference SoC, and a later, larger flagship SoC from the same fictional
lineage. Their parameters are fixed and published, they do not change between
chapters, and a bug found in Chapter 1 is still the same bug in Chapter 26.

The choice of constructed examples is deliberate: it gives up lookup and checking against a datasheet, and what it buys is completeness. An example can be complete: every parameter the argument needs is available, the same crossbar can be examined through six different techniques, and a coverage model can be given cell by cell. A coverage model is the set of situations a project has decided to count, one cell for each combination of values. Examples drawn from real silicon are complete only where the owner
chose to publish, which is rarely where a teaching argument needs them.

The book distinguishes these examples from claims about real organizations. Reports of what a named company did come from and cite a published source, usually that company's own conference paper. Where it reports what the industry does in aggregate, it names the study
and its year.

## The evidence discipline

The book was written against a closed corpus of documents held in full text:
papers, conference proceedings, standards and books. The rule was that a claim
either carries a reference into that corpus, or is presented as the author's
position, or does not appear. Nothing is cited from memory of a paper.

Three practices in the prose follow from this rule.

**Statistics are dated.** A figure about first-silicon success or about where verification effort goes is a measurement of a particular year, and the year is given. First-silicon success is the outcome in which the first fabricated parts are already production-worthy. The author considers several widely repeated numbers in this field older than their use suggests.

**Quantities are derived where they can be.** When a number can be computed from an example's own parameters, the book shows the derivation so readers can identify any step they dispute.

**Absent evidence is reported as absent.** There is no industry-wide data on
several questions this book has to address. The author considers reporting this absence more useful than a plausible estimate, because it identifies questions for which readers' own measurements would be worth more than any citation.

## Production and review

The book was written with substantial help from large language models, specifically Anthropic's Claude: models in the Claude Opus family for drafting, adversarial review and citation checking, and Claude Fable and Opus models for coordination across chapters. The method is disclosed here because readers are entitled to assess it.

Chapters were drafted against the corpus and the style contract. The style contract is the set of rules this book's prose was written and checked against. An independent adversarial pass then reviewed each chapter, tasked with finding unsupported claims, misattributed citations, incorrect arithmetic and internal contradictions. After the drafting and that review, a third pass applied the findings, with authority to reject the findings it judged wrong. Citation checks were done at page level against the
source document. Mechanical gates address the defects that reading misses. A mechanical gate is a check a program settles alone, before anyone reads the text. The gates catch unresolved citation markers. They catch numbers, code blocks or cross-references moved during editing without a stated reason. They catch lost hedges, since dropping *typically* or *up to* strengthens claims beyond their sources. They also catch a caption missing from a figure or a table, and a reference that never resolves to the figure or the table it names. A single term in this book is redefined against common industry usage, and that term is *validation*. In this book the word means checking a design on real hardware, and everything done on a model is verification. A further gate watches that redefined term for drift in either direction. Eight terms neighboring the redefined one are counted rather than enforced, because a gate can compare occurrences but cannot read a sense. A count that changes deserves a person's attention rather than a build failure. Each gate was tested against a deliberate defect, and trust in it depended on observing its failure on that defect.

The author's position on language models editing long documents has three parts. The first is that severe and silent damage is sparsely distributed through a document. The second is that rewriting inflates certainty while appearing to preserve meaning. The third is that on already-clean text, precision in deciding what needs changing collapses. That position rests on the author's reading of the field and on the editing of this book itself. Each rewritten chapter was checked, independently, against an inventory of its propositions. An inventory of propositions is the list of the claims the chapter made before the rewriting, and each claim is quoted from the sentence that carried it. The check against the inventory kept finding a few serious losses among many propositions preserved, typically a dropped condition or a reservation turned into a certainty. The editorial passes and their mitigations follow from that experience rather than from intuition. Where neither that experience nor the literature offers a measurement, the method reports the absence without borrowing confidence from an adjacent result.

In the author's assessment, the procedure is limited in two ways. The first is that automated reviewers that share an author's blind spots miss what the author missed. The second is that source grounding improves an automated reviewer's judgment of the claims presented to that reviewer far more than it improves the same reviewer's choice of what to check. Source grounding is putting the cited source in front of the reviewer, so that a claim is judged against an opened page and not from memory. The defects that this method catches are misattribution, contradiction and arithmetic. The method is least effective at catching fluent but wrong passages that nobody thought to question. Readers who find such a passage have found something the process could not find, and the author would like to know.

## Acknowledgements

**Use of generative artificial intelligence.** Anthropic's Claude was used in
preparing this book, as described in "Production and review" above: models in
the Claude Opus family for drafting text, for adversarial review of drafts, and
for verifying citations against the cited pages, and Claude Fable and Opus models
for coordination across chapters. No text was published without being read. The systems are tools, have no authorship and receive no author credit; the author accepts full responsibility for all content, including errors missed by review.

*Personal acknowledgements to be written by the author.*
{: .cp-note }
