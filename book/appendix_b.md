# Appendix B — Reading paths

This book runs to about 500 pages, and almost nobody reads a book that size front to back. So this appendix inverts the table of contents: rather than describe what each chapter contains, it claims that *reading these chapters, in this order, equips you to do this specific thing.*

That makes every path falsifiable. Each names a situation rather than a seniority, says what you can do at the end, and — the part reading guides skip — names what it leaves out and what that costs. A path claiming no cost has not chosen anything.

Where only part of a chapter is needed the section number is given; Chapters 1–3 have unnumbered sections and are cited whole.

## Read these three if you read nothing else

The criterion is *maximum change in what you do next Monday, per page*, not logical completeness — and it assumes a reader whose work touches verification without being verification: a designer, a lead, an architect, a manager.

- **Chapter 2, *The Verifier's Mindset*** — because its opening scenario is the commonest way competent people ship bugs: a designer verifying her own block, whose stimulus exercised it the way it was meant to be used. Recognise yourself there and the rest of the book has a reason.
- **Chapter 3, *The Verification Problem*** — because without it, coverage models, risk ranking and waivers read as bureaucracy. It explains why the discipline manages risk instead of pursuing completeness, and its oracle problem — every practical oracle is partial — is what most practitioners were never told.
- **Chapter 7, *Metrics-Driven Sign-off*** — because "are we done?" is the decision you will actually be in the room for, and §7.4 is the evidence to demand when you are.

Chapter 1 is absent: it argues that verification matters, and anyone holding this book agrees. Chapter 5 is absent for a harder reason — 8,000 words of instrument for a reader who may never own a plan.

## You are starting your first verification job

You can write SystemVerilog and have been dropped into an existing environment with a backlog of failing seeds. At the end: read an unfamiliar testbench and say which part is lying, write stimulus somebody else can reproduce, triage a regression without escalating all of it.

- **Chapter 2** — because your training rewarded making things work, and this job asks the opposite posture first.
- **Chapter 3** — because someone will tell you in week one that you cannot test everything, and without this you hear it as an excuse rather than the premise the method is built on.
- **Chapter 8, *Testbench Architecture*** — because the environment you inherited separates five responsibilities (§8.1), and knowing which one owns a symptom is your fastest localisation.
- **Chapter 10, *UVM as a Methodology*** — because the code you type will be UVM code, and §10.2 gives the argument behind the class taxonomy, not the API.
- **Chapter 9, *Stimulus: Directed to Random to Portable*** — because most of your first year is constraints (§9.3), and §9.4 is what makes a failure reproducible enough for anyone senior to look at.
- **Chapter 12, *Regression Engineering*** — because your mornings are triage, and §12.5 tells you when the answer is "this test has stopped being evidence" rather than "the design is broken".

**Omits Part II entirely** — planning, coverage theory, sign-off. You will execute plan rows without knowing where they came from and read a coverage report as a score, not an argument. Come back when someone hands you a row with your name on it. Come back for **Chapter 24 §24.1** when someone gives you a block of your own: it restates ownership as an outcome.

## You designed the block and there is nobody else to verify it

No verification engineer; the block is yours to verify and defend. At the end: the cheapest defensible checks, starting with ones needing no testbench, plus a list of your own reflexes that make an environment look healthier than it is.

- **Chapter 2** — because it was written about you: its *Independence of judgment* section gives three disciplines that survive a team of one, the load-bearing one being *predict from the specification, never from what your RTL does*.
- **Chapter 13, *Static Verification*** — because you have no testbench yet, and §13.1 is the analysis needing none: no stimulus, no statement of expected output, running the first day the RTL compiles.
- **Chapter 11, *Assertion-Based Verification*** — because §11.4 names the split you can exploit alone: you are better placed than any verifier to write the internal invariants, since they state the micro-architecture's assumptions, which no specification mentions.
- **Chapter 5, *Verification Planning*** — because even a one-person plan must say what closes each row, and §5.2's five fields are the smallest honest form. §5.4 assumes a review audience you lack; take its three blades — correctness, precision, completeness — and turn them on your own rows.
- **Chapter 10 §10.10** — the permission slip: a small block with one interface does not repay a UVM environment, and the alternative it names is a module testbench with bound assertions and one covergroup.
- **Chapter 15 §§15.2–15.3** — because connectivity and register checks are proofs you can run against your own block without owning a formal methodology.

Come back for **Chapter 24 §24.4**, whose designer reflexes — explaining a failure instead of reproducing it, building a testbench that recovers, debugging in waveforms — read as a checklist against yourself.

**Omits coverage modelling (Chapter 6) and stimulus at scale.** Your evidence will be "checks that fired", not "space that was covered" — the weaker claim, and the first thing a reviewer pushes on.

## You have a decade of simulation and the next block is going to formal

The next block is an arbiter or a protocol converter — something whose specification is a set of properties. At the end: read a formal result with its three qualifiers attached, recognise the green that is not one, work an undetermined property in the order costing an afternoon rather than a fortnight.

- **Chapter 11** — start here even though you already write assertions. §11.3 is the asymmetry everything rests on: in simulation `assert` and `assume` are effectively synonyms; in formal an assumption is never checked and deletes traces instead. §11.8 names the other two shifts — covers stop counting and start searching, liveness becomes decidable.
- **Chapter 14, *Formal Property Verification*** — the chapter. §14.2 carries the hazard your simulation instincts do not: a *missing* assumption announces itself in red, an *extra* one only makes the report greener.
- **Chapter 15, *Formal Apps and Equivalence*** — because it is what you can run next month with no formal methodology behind you: connectivity, register maps, and §15.4's unreachability, which turns a coverage waiver into a result.
- **Chapter 16, *Hybrid Flows*** — because you are not leaving simulation, and §16.4 is a per-row decision procedure you can apply in a plan review.

**Omits your vendor's engine.** §14.5's convergence tactics are generic; option names are your tool documentation's job. It also omits equivalence checking as a flow you would own — §15.6 puts it in the implementation flow, which is where it usually sits.

## You must produce a verification plan and answer for it

Somebody senior will review it and quote it back at sign-off. At the end: rows with one measurable exit each, a method field you can defend, a plan that survives a specification with holes in it.

- **Chapter 4 §§4.2, 4.6** — because a plan's value is set by when it is written and who sits in the review — both calendar facts to negotiate before you write a line.
- **Chapter 5** — the chapter. §5.2's five fields, §5.5 for choosing depth feature by feature, §5.6 for the situation you actually have.
- **Chapter 6, *Coverage: Theory and Practice*** — because most of your closure metrics are coverage, and §§6.3 and 6.5 stop you writing a model that certifies your stimulus instead of the design.
- **Chapter 16 §16.4** — because the method field is where plans turn optimistic. Its question 6 — what happens if it does not converge — is otherwise answered in week nine.
- **Chapter 7 §7.4** — because the sign-off checklist is your plan's last column, and reading it now tells you which fields you are about to leave blank.

**Omits the engines themselves.** You will write "formal" in a method field without knowing what makes a property converge, and "emulation" without §17.5's queue for the machine. Survivable for a first plan, not a second; the formal path above is the fix.

## You own sign-off and the evidence was produced by other people

Block or SoC, your signature. At the end: know what to demand, in what form, and which green results cannot turn red.

- **Chapter 7** — §7.4's seven items are the demand list; §7.3 distinguishes a bug curve flat because clean from one flat because the stimulus stopped asking.
- **Chapter 6 §6.9** — because most of your hard calls are other people's waivers, and the three kinds have different owners and expiries. A risk-accepted waiver taken to make a date needs your signature, not the model owner's.
- **Chapter 14 §14.6** — because a proof arrives as a tick, and you must ask the three reviewer-side questions: complete checker list, no unintentional over-constraints, required depth reached.
- **Chapter 12 §§12.2, 12.5** — because "the regression passes" is a claim about a (test, seed) matrix, and a quarantine list nobody empties is the same disease with better manners.
- **Chapter 19 §19.5** — because somebody will propose running the whole suite at gate level and somebody else will propose skipping the tier. The arithmetic kills the first; the five criteria pick which handful answers the second.
- **Chapter 20 §20.5** — read it *before* you sign. It classifies every escape by which link broke first — activation, propagation or checking — and each owes a different upstream change.

**Omits how any of that evidence was produced.** You will audit work you could not have generated: adequate for a block, thin at SoC scale, where §20.2's design-for-debug budget was fixed at RTL freeze by people who did not consult you.

## You are arriving from software test or QA

You have written test frameworks, run continuous integration, chased flaky tests. Your instincts transfer; several of your words do not. At the end: the vocabulary held correctly, and a list of habits that were already right.

- **Chapter 3** — start here, because the oracle problem is the bridge. You know test oracles; what is new is that here every practical oracle is *partial*, and the craft is combining ones whose blind spots do not overlap.
- **Chapter 1, *Why Verification Exists*** — for the cost curve, because your instincts are calibrated against a world with patches in it.
- **Chapter 8** — because §8.1's five responsibilities map almost one-to-one onto separations you already build — the cheapest chapter here for you.
- **Chapter 12** — your home ground, with two corrections: §12.3 on why "run everything on every commit" does not transfer when a unit costs minutes not milliseconds, and §12.5 on flakiness with its hardware-specific sources.
- **Chapter 6** — because "coverage" is narrower here: §6.2's code coverage is free and structurally blind, and §6.3's functional coverage is a model a human writes from the specification.
- **Chapter 18 §18.4** — because firmware-driven verification is the closest thing here to what you used to do, and its lesson is that the interface contract was incomplete rather than either side wrong.

One vocabulary warning, the one that trips people in meetings: **validation** here does not mean "did we build the right thing?". Chapter 20 owns the term and states it at §20.1 — checking a design on real hardware rather than on a model. Everything before tape-out is *verification*.

**Omits Part IV.** Formal will keep being mentioned around you and you will have no model for it. Take the formal path later.

## A standard, not curiosity, put this on your desk

A market requires it, and someone external will read what you produce.

**Common spine, all three branches: Chapter 5, then Chapter 7.** Not because planning and metrics are generally good, but because each regime converts ordinary practice into a retained, traceable artifact — and these two are what gets converted.

**Safety.** **Chapter 22, *Safety Verification*** — §22.1 gives the three obligations (process, evidence, traceability) and the consequence outranking them: the argument itself becomes a deliverable. §22.5 changes your week: qualification is scoped to a tool *version* and *use cases*, so a mid-project upgrade is a re-argument, not an IT ticket. Then **Chapter 12 §12.2**, which defines the run manifest that §22.5 promotes to the atom of the evidence trail. Then **Chapter 19**: §22.3's fault-injection campaigns and §19.5's netlist tiers compete for the same machine hours.

**Security.** **Chapter 23, *Security Verification*** — §23.2 is where the work starts, and it is a planning act: assets, adversary capabilities as an enumerable list rather than an open set of attacks, and trust boundaries. §23.6's table routes each question to the engine that can answer it. Then **Chapter 11**, because §23.3's central caveat — a confidentiality claim quantifies over *pairs* of executions, which one assertion cannot express — lands only once you can read an ordinary property. Then **Chapter 15 §15.2**, because a connectivity check carrying negative rows, in the build from day one, is the cheapest security artifact here.

**Mixed-signal.** Deliberately short: read **Chapter 21 §21.5** and stop. It draws the boundary — you own the interface contract, the calibration sequences, the failure handling and the provenance of the tolerances, not the analog block. It omits analog verification itself: noise, linearity, corner behaviour. That belongs to the analog team, and Chapter 21 says so.

## You arrived with a specific failure in hand

An entry ramp, not a path: two chapters and a handoff.

- **A bug escaped.** Chapter 7 §7.6 — the five written questions, blameless — then Chapter 20 §20.5, which names the link that broke first and what each break owes upstream. *Handoff*: if your honest answer to question 4 is "the metrics were fine and the plan was blind", the problem is upstream. Take the plan path.
- **The regression is not trustworthy.** Chapter 12 §12.5 — flakiness, its recurring sources, quarantine with a named owner and a date — then Chapter 9 §9.4, on what a run actually is: a seed *and* a specific set of sources, which is where reproducibility is usually lost. *Handoff*: if your manifest cannot name the exact tool build, this is infrastructure, and §12.3 is the gate to build.
- **Coverage will not close.** Chapter 6 §6.8 — the loop from holes to done, including the invalid-hole branch most teams skip — then Chapter 15 §15.4, a proof instead of a waiver — its first catch being that the verdict inherits every assumption in your setup, including ones in a script written by someone who has left. *Handoff*: if the same holes recur every project, the model is downstream of a planning problem.

## What genuinely presupposes what

Chapter order is not dependency. The useful facts are the ones that license a skip.

- **Chapter 13 presupposes nothing.** §13.1 says it outright: static analysis requires no stimulus and no statement of expected output. Readable on a project's first day, by someone with no testbench and no plan.
- **Chapter 11 is readable before Part III.** Its argument runs from the specification and the RTL, not from an environment: §11.4 on who writes which assertion and where it lives, §11.8 on two engines reading one text. Neither needs Chapter 8 or Chapter 10 first.
- **Chapter 21 §21.5 stands alone** as a boundary statement, which is why the mixed-signal branch above is one section long.

The real dependencies, established by reading rather than inferred from numbering:

- **Chapter 14 → Chapter 11 §11.3.** §14.2's whole hazard is the assert/assume asymmetry, and §11.3 establishes it — Chapter 11 says so on the page.
- **Chapter 10 → Chapter 8 §8.1.** §10.2 opens by taking Chapter 8's "the reusable unit is one interface" as given and encoding it as a base class plus a flag.
- **Chapter 7 → Chapters 5 and 6.** §7.4 computes over artifacts the other two define: plan rows, closure metrics, waiver kinds. Alone it is a checklist; after them it is auditable.
- **Chapter 16 → Chapter 14.** §16.2 is assumption and constraint duality as a flow, and §16.4's question 4 prices §14.4's abstraction bill.
- **Chapter 20 §20.5 → Chapter 7 §7.6 and Chapter 3.** It reuses the five questions and Chapter 3's activation–propagation–checking chain as its classifier.
- **Chapter 24 §24.3 → Chapter 4 §4.4.** Chapter 4 defines the maturity stages; §24.3 takes them as given and asks a narrower question about the conversations they change.

## The chapters no path here reaches

Naming them is more honest than routing everyone through everything.

**Chapter 17, *Acceleration and Emulation*** turns on one triage question (§17.1): *is my problem the number of runs, or the length of one run?* A wider farm answers the first and does nothing for the second, because cycle *n* of a boot depends on cycle *n*−1. Read it when the answer is length.

**Chapter 25, *AI and ML in Verification*** is for the day somebody proposes a tool that generates artifacts — properties, testbenches, plan rows. §25.4 names the four decision points a human must occupy and the damage of leaving each unowned.

**Chapter 26, *The Road Ahead*** is an argument rather than an instruction. Read it last or not at all; it changes nothing you do tomorrow, which is exactly why it is not in the three-chapter set.
