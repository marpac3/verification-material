# Appendix B: Reading paths

This appendix provides reading paths through a book of about 500 pages. It reverses the table of contents: each ordered sequence of chapters claims to equip the reader for a specific task.

Every path is therefore falsifiable. Each one names the situation it addresses rather than the seniority of its reader, then the expected capability, then the omissions and what they cost.

Where only part of a chapter is needed the section number is given; Chapters 1–3 have unnumbered sections and are cited whole.

## Three chapters for a minimal reading path

This selection aims to maximize immediate practical change per page rather than logical completeness, for readers whose work touches verification: designers, leads, architects, and managers, rather than verification engineers.

- **Chapter 2, *The Verifier's Mindset***: its opening scenario concerns a designer verifying her own block with stimulus limited to intended use, letting bugs escape.
- **Chapter 3, *The Verification Problem*** explains the rationale for coverage models, risk ranking, and waivers. It explains risk management rather than completeness, and it explains that every practical oracle is partial. This path assumes that most practitioners have been taught neither point.
- **Chapter 7, *Metrics-Driven Sign-off*** addresses the completion decision these readers will attend and the evidence to require (§7.4).

Chapter 1 is absent because this path assumes agreement that verification matters, and that agreement is the argument that Chapter 1 develops. Chapter 5 is absent: 8,000 words on planning for a reader who may never own a plan.

## A first verification job

This path assumes SystemVerilog proficiency and an inherited environment with failing seeds to resolve. The intended outcomes are locating faults in an unfamiliar testbench, writing reproducible stimulus, and triaging a regression without escalating every failure.

- **Chapter 2** addresses the initial change from training rewarded for making things work to the opposite verification posture.
- **Chapter 3** explains why the impossibility of testing everything, raised in week one in this scenario, is a methodological premise rather than an excuse.
- **Chapter 8, *Testbench Architecture*** separates the inherited environment into five responsibilities (§8.1); identifying which one owns a symptom directs fault localization.
- **Chapter 10, *UVM as a Methodology*** explains the rationale for the class taxonomy used in the UVM code this job requires (§10.2), rather than the API.
- **Chapter 9, *Stimulus: Directed to Random to Portable*** covers constraints (§9.3), assumed to occupy most of the first year, and the reproducibility needed for senior review (§9.4).
- **Chapter 12, *Regression Engineering*** supports morning triage: §12.5 distinguishes a test that has stopped providing evidence from a broken design.

**Omits Part II entirely** (planning, coverage theory, and sign-off). The reader will execute plan rows without knowing their origins and interpret coverage reports as scores rather than arguments. That material becomes necessary when a plan row is assigned to the reader. **Chapter 24 §24.1** follows when the reader takes ownership of a block; it restates ownership as an outcome.

## A designer verifying a block alone

Without a verification engineer, the designer must verify and defend the block. The outcomes are the cheapest defensible checks, which begin without a testbench, and a list of designer reflexes that make an environment seem healthier than it is.

- **Chapter 2** addresses this designer: *Independence of judgment* gives three disciplines for a team of one. The essential discipline is prediction from the specification, never from RTL behavior.
- **Chapter 13, *Static Verification*** addresses the absence of a testbench: §13.1 describes analysis needing no stimulus or statement of expected output, running the first day RTL compiles.
- **Chapter 11, *Assertion-Based Verification***: §11.4 explains why the designer is better placed than any verifier to write internal invariants expressing micro-architectural assumptions absent from every specification.
- **Chapter 5, *Verification Planning***: even a one-person plan must specify each row's closure; §5.2's five fields give the minimum adequate form. §5.4 assumes an unavailable review audience, but its three criteria (correctness, precision, and completeness) also apply to the designer's own rows.
- **Chapter 10 §10.10** explains why a small block with one interface does not repay a UVM environment; its alternative is a module testbench with bound assertions and one covergroup.
- **Chapter 15 §§15.2–15.3** provides connectivity and register proofs the designer can run on the block without owning a formal methodology.

**Chapter 24 §24.4** provides a later checklist of designer reflexes: explaining failures instead of reproducing them, building a recovering testbench, and debugging in waveforms.

**Omits coverage modeling (Chapter 6) and stimulus at scale:** the evidence establishes checks that fired rather than space covered, a weaker claim; this path treats that limitation as the first issue for review.

## Formal verification after a decade of simulation

The next block is an arbiter or protocol converter whose specification is a set of properties. The first outcome is interpreting a formal result with the three qualifiers that Chapter 14 defines. The second is recognizing invalid passes, and the third is working an undetermined property in the order that costs an afternoon rather than a fortnight in this scenario. An undetermined property is one on which the engine gave up, through timeout, memory exhaustion, or an incomplete algorithm, and its result is neither a pass nor a failure.

- **Chapter 11** comes first even for readers who already write assertions. §11.3 is the asymmetry everything rests on: in simulation `assert` and `assume` are effectively synonyms; in formal an assumption is never checked and deletes traces instead. §11.8 names the other two shifts: covers ask whether a scenario is reachable rather than count how many times it occurs, and liveness properties become decidable.
- **Chapter 14, *Formal Property Verification*** covers the transition. §14.2 explains the hazard absent from simulation instincts: a *missing* assumption causes failures, while an *extra* one only produces more passes.
- **Chapter 15, *Formal Apps and Equivalence*** offers checks for next month without a formal methodology: connectivity and register maps, plus §15.4's unreachability proofs that replace coverage waivers with results.
- **Chapter 16, *Hybrid Flows*** retains simulation and supplies a decision procedure for each plan row, applicable in review (§16.4).

**Omits the vendor's engine.** §14.5's convergence tactics are generic; tool documentation supplies option names. It also omits ownership of an equivalence-checking flow; §15.6 places it in implementation, where it usually sits.

## Producing and defending a verification plan

This path assumes senior review of the plan and accountability against it at sign-off. The outcomes are rows with one measurable exit each, defensible method fields, and a plan that accommodates specification gaps.

- **Chapter 4 §§4.2, 4.6** explains how timing and review membership determine a plan's value; both calendar commitments need negotiation before writing begins.
- **Chapter 5** supplies the planning method: §5.2's five fields, §5.5's depth selection for each feature, and §5.6's treatment of the reader's situation.
- **Chapter 6, *Coverage: Theory and Practice*** addresses coverage, and this path assumes that coverage will supply most of the closure metrics. §§6.3 and 6.5 prevent models that give evidence for the stimulus rather than for the design.
- **Chapter 16 §16.4** addresses optimism in method selection. Its question 6 addresses nonconvergence, otherwise left until week nine in this scenario.
- **Chapter 7 §7.4** supplies the sign-off checklist for the plan's last column; reading it during planning exposes fields otherwise left blank.

**Omits the engines themselves.** The reader will specify "formal" without knowing what makes a property converge and "emulation" without understanding the machine queue (§17.5). For a first plan, this path accepts the gap; a second plan requires the engine knowledge addressed by the path *Formal verification after a decade of simulation* above.

## Signing off evidence produced by others

This path addresses responsibility for signing off a block or SoC. The outcomes are knowing which evidence to require, its form, and which passing results cannot fail.

- **Chapter 7**: §7.4 lists seven required items; §7.3 distinguishes a clean flat bug curve from one flattened because stimulus stopped probing for bugs.
- **Chapter 6 §6.9** addresses others' waivers, assumed to account for most difficult decisions; the three kinds differ in ownership and expiry. A risk-accepted waiver for a deadline needs the sign-off owner's signature rather than the model owner's.
- **Chapter 14 §14.6** goes beyond a proof tick with three required review questions: checker-list completeness, absence of unintentional over-constraints, and achievement of required depth.
- **Chapter 12 §§12.2, 12.5** explains that a passing regression describes a (test, seed) matrix; leaving quarantine lists uncleared similarly undermines the evidence.
- **Chapter 19 §19.5** addresses proposals to run the whole suite at gate level or skip the tier entirely. The arithmetic rules out the first; five criteria select the handful of tests that answers the second.
- **Chapter 20 §20.5** belongs before sign-off. It classifies every escape by the first broken link in the chain that Chapter 3 defines (activation, propagation, or checking), and each break requires a different upstream change.

**Omits how any of that evidence was produced.** The reader audits work they could not have produced: adequate for a block, limited at SoC scale, where others fixed §20.2's design-for-debug budget at RTL freeze without consulting them.

## Transition from software test or QA

This path assumes experience writing test frameworks, running continuous integration, and investigating flaky tests, the ones whose outcome varies between identically configured runs and that have therefore stopped being evidence. Those instincts transfer, but several terms do not. The outcomes are correct vocabulary and a list of existing habits that already apply.

- **Chapter 3** comes first because of the familiar oracle problem. The new distinction is that every practical hardware oracle is *partial*, requiring combinations whose blind spots do not overlap.
- **Chapter 1, *Why Verification Exists*** supplies the cost curve for readers accustomed to patchable systems.
- **Chapter 8** builds on familiar software separations: its five responsibilities (§8.1) map almost one-to-one onto them.
- **Chapter 12** covers familiar work with two corrections: §12.3 explains why running everything on every commit does not transfer when a unit costs minutes rather than milliseconds; §12.5 covers hardware-specific sources of flakiness.
- **Chapter 6** narrows "coverage": §6.2 treats free but structurally blind code coverage; §6.3 treats functional coverage as a model a person writes from the specification.
- **Chapter 18 §18.4** covers firmware-driven verification, the closest match to prior software work, and attributes the problem to an incomplete interface contract rather than fault on either side.

One vocabulary distinction concerns **validation**: the meaning used here excludes the one expressed by "did we build the right thing?". Chapter 20 defines it at §20.1 as checking a design on real hardware rather than on a model; everything before tape-out is *verification*.

**Omits Part IV.** The reader will continue encountering formal verification without a model for it; the path *Formal verification after a decade of simulation* is a later step.

## Verification required by a standard

This path addresses a market requirement and external review of the resulting artifacts.

**Common spine, all three branches: Chapter 5, then Chapter 7.** Each regime converts ordinary planning and metrics into retained, traceable artifacts; these two practices explain the selection.

**Safety.** **Chapter 22, *Safety Verification***: §22.1 gives the three obligations (process, evidence, traceability) and their overriding consequence: the argument itself becomes a deliverable. §22.5 scopes qualification to a tool *version* and *use cases*, so a mid-project upgrade requires a new argument rather than merely an IT ticket. Then **Chapter 12 §12.2** defines the run manifest that §22.5 makes the unit of the evidence trail. Then **Chapter 19**: §22.3's fault-injection campaigns and §19.5's netlist tiers compete for the same machine hours.

**Security.** **Chapter 23, *Security Verification*** starts with planning (§23.2): assets and trust boundaries, with adversary capabilities enumerated rather than an open set of attacks. §23.6's table routes each question to the engine that can answer it. Then **Chapter 11** prepares the reader to understand §23.3. A confidentiality claim quantifies over *pairs* of executions, and one assertion cannot express it. Reaching that understanding requires the ability to read an ordinary property. Then **Chapter 15 §15.2** supplies a security artifact for this path: a connectivity check with negative rows, in the build from day one.

**Mixed-signal.** This short branch ends with **Chapter 21 §21.5**. It assigns responsibility for the interface contract, for calibration sequences, for failure handling, and for the provenance of each tolerance, while excluding ownership of the analog block. It omits analog verification itself, including noise, linearity, and corner behavior. That belongs to the analog team, and Chapter 21 says so.

## Entry points for a specific failure

Each entry is limited to two chapters and a handoff.

- **A bug escaped.** Chapter 7 §7.6 supplies five written, blameless questions; then Chapter 20 §20.5 identifies the first broken link and the upstream change each break requires. *Handoff*: if the answer to question 4 is "the metrics were fine and the plan was blind", the problem lies upstream. The path *Producing and defending a verification plan* follows.
- **The regression is not trustworthy.** Chapter 12 §12.5 covers the recurring causes of flakiness and covers quarantine with a named owner and date; then Chapter 9 §9.4 defines a run as a seed *and* specific source files, and the source files are where reproducibility is usually lost. *Handoff*: a manifest missing the exact tool build is an infrastructure problem, requiring the gate in §12.3.
- **Coverage will not close.** Chapter 6 §6.8 covers the closure loop, including the invalid-hole branch this path assumes most teams skip; then Chapter 15 §15.4 replaces a waiver with proof, whose first limitation is inheriting every setup assumption, including those in scripts written by departed staff. *Handoff*: if the same holes recur every project, the model is downstream of a planning problem.

## Reading dependencies

Chapter order differs from dependency, which determines what can be skipped.

- **Chapter 13 presupposes nothing.** §13.1 states that static analysis needs no stimulus or statement of expected output. It is readable on a project's first day without a testbench or plan.
- **Chapter 11 is readable before Part III.** Its argument starts from the specification and the RTL rather than from an environment: §11.4 covers assertion authorship and placement, and §11.8 covers what happens when two engines read the same property text. Neither needs Chapter 8 or Chapter 10 first.
- **Chapter 21 §21.5 stands alone** as a boundary statement, which is why the mixed-signal branch above is one section long.

The following dependencies come from reading the chapters rather than their numbering:

- **Chapter 14 → Chapter 11 §11.3.** §14.2 depends entirely on the assert/assume asymmetry established in §11.3, as Chapter 11 explicitly states.
- **Chapter 10 → Chapter 8 §8.1.** §10.2 opens by taking Chapter 8's "the reusable unit is one interface" as given and encoding it as a base class plus a flag.
- **Chapter 7 → Chapters 5 and 6.** §7.4 computes over artifacts the other two define: plan rows, closure metrics, waiver kinds. The checklist becomes auditable after the definitions in those chapters have been established.
- **Chapter 16 → Chapter 14.** §16.2 presents assumption and constraint duality as a flow; §16.4's question 4 evaluates the cost of §14.4's abstraction.
- **Chapter 20 §20.5 → Chapter 7 §7.6 and Chapter 3.** It reuses the five questions and Chapter 3's activation–propagation–checking chain as its classifier.
- **Chapter 24 §24.3 → Chapter 4 §4.4.** Chapter 4 defines the maturity stages; §24.3 takes them as given and asks a narrower question about the conversations they change.

## The chapters no path here reaches

**Chapter 17, *Acceleration and Emulation*** centers on one triage distinction (§17.1): the number of runs versus the length of one run. A wider farm answers the first and does nothing for the second, because cycle *n* of a boot depends on cycle *n*−1. It is relevant when run length is the problem.

**Chapter 25, *AI and ML in Verification*** addresses proposed tools that generate properties, testbenches, or plan rows. §25.4 names the four decision points a human must occupy and the damage of leaving each unowned.

**Chapter 26, *The Road Ahead*** is an argument rather than an instruction. It can be read last or omitted; it has no immediate operational effect, which excludes it from the three-chapter set.
