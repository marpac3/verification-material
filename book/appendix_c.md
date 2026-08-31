# Appendix C — The literature: what to read and what it will tell you

The reference list at the end of each chapter tells you what a claim rests on. It is useless for the question you will have six months from now — *where do I go to learn this properly* — because it is ordered by where sentences fell, and your question is by topic.

Worse, titles lie about contents. The best account here of how a technique gets adopted across a large organisation — a named local expert per team, escalation to a central group, continuity across projects, scaffolding for novices — is a paper about formal property verification, and until Chapter 24 was written it was cited only in formal chapters. Nobody with a process question would have found it. Section C.10 names every case of that kind.

What follows is a reader's guide, not a second bibliography: per cluster, which sources carry weight, what each gives that the others do not, and what is not covered.

## C.1 The industry's picture of itself

**Start here: the 2024 Wilson Research Group IC/ASIC trend report** (Foster, Siemens EDA). Short, current, and the source of most quantitative framing in Chapters 1, 4, 7 and 26. Its FPGA companion is a separate report with a different population, not a subset; Chapter 26's escape figure comes from it, not from the IC/ASIC one.

Foster's DAC 2015 paper, *Trends in Functional Verification: A 2014 Industry Study*, supplies what the reports do not: the methodology behind the series, the sample design, and the decade-earlier baseline the 2024 numbers are read against. Chapter 1 takes from it the participant counts and confidence interval, and the fact that the "70 percent of effort" figure has honest roots but was called unsubstantiated in the literature.

Two counterweights: Mishra, Ray, Morad and Ziv's post-silicon tutorial on what a bug costs as it moves right, and Narayan and Symons' *I Created the Verification Gap*, a taxonomy of self-inflicted shortfall behind the management vocabulary of Chapters 1, 2, 4, 7 and 24.

**Not covered.** Any measured cost-per-stage series — see Section C.12.

## C.2 Methodology, testbench architecture and stimulus

**Start here: Bergeron's *Writing Testbenches using SystemVerilog*.** The backbone of this book — seventeen of twenty-six chapters draw on it — and the only source running from the reconvergence model through bus-functional models, self-checking taxonomy and regression management in one voice.

The *Verification Methodology Manual for SystemVerilog* (Bergeron, Cerny, Hunter, Nightingale) is not a duplicate: where the testbench book explains, the manual *rules* — encapsulation of self-checking structures, scoreboard recommendations, stimulus layering, seed discipline, coverage-guideline hierarchy. Chapters 8 and 9 lean on it for the parts that read like a standard.

Hollander, Morley and Noy's 2001 *The e Language: A Fresh Separation of Concerns* is the historical source for why a modern testbench is shaped as it is — decomposition, transaction-level framing, extension-as-configuration (Section C.10).

For stimulus: Yuan, Pixley and Aziz's *Constraint-Based Verification* on solvers and over-constraint diagnosis, and the Portable Test and Stimulus Standard, the working group's *PSS in the Real World*, and Gupta and Vax's *Test driving Portable Stimulus at AMD* for its industrial limits.

**Not covered.** Environment architecture as software design at book length, and the idiom catalogue the community maintains outside the corpus.

## C.3 Coverage, metrics and sign-off

**Start here: Piziali's *Functional Verification Coverage Measurement and Analysis*.** Taxonomy, model design method, fidelity and hole analysis in one place; Chapters 5, 6, 7 and 26 route through it.

Clause 19 of the SystemVerilog standard is definitive for covergroup, bin, cross and option semantics; Accellera's Unified Coverage Interoperability Standard carries everything Chapter 16 says about merging results across engines, including its own caution against automatic merging.

On metrics as a management instrument, Meyer and Foster's *Metrics in SoC Verification* is the foundation of Chapter 7; Hristozkov, Pallister and Porter's *No Country For Old Men* is its modern industrial counterpart, with an in-house stack and measurements; Zhang shows what a management platform automates. For planning, Ehlers, Vargas and Carzola cover executable plans and assumption reviews, Marriott, Vance and McNeal deliverables and definitions of done, and Graham et al.'s *Planning for RISC-V Success* contributes the only published plan-row format here.

On closure automation, four papers form a spectrum of ambition: Kodi, Patil and Nair (constraint regeneration), Teplitsky et al. (solver level), Ohana (deep reinforcement learning) and Feng, Chen and Muchandikar (coverage models for formal).

**Not covered.** Whether a coverage model was any good: fidelity is discussed and never quantified.

## C.4 Formal verification and its industrialisation

**Start here: Kern and Greenstreet's 1999 survey, *Formal Verification in Hardware Design*.** The map: foundations, limits, and what a verification claim must state to mean anything. Chapter 15 also calls it the corpus's closest thing to a treatment of equivalence-checking algorithms.

Cerny, Dudani, Havlicek and Korchemny's *SVA: The Power of Assertions in SystemVerilog* is the reference for assertion semantics and for Chapter 14's working vocabulary. Bormann's dissertation is the corpus's most serious answer to "have I written enough properties?"; Schwarz's is the clearest account of bounded versus unbounded proof, sequential depth and spurious counterexamples from arbitrary starting states, and it extends the machinery across the hardware/firmware boundary for Chapter 18.

For practice: Tripathi, Saxena, Verma and Aggarwal work a formal sign-off end to end on a crossbar, with a required-proof-depth derivation and a mutation experiment; Bromley and Sprott's *Formal Verification in the Real World* tours complexity management and the traps around waivers; Achutha Kiran Kumar, Seligman et al.'s *Making Formal Property Verification Mainstream* is the deployment report, with a bug taxonomy by difficulty gathered on already-simulated designs.

**Not covered.** Model-checking algorithms, and the industrial C-to-RTL equivalence flow — see Section C.12.

## C.5 The standards, and which ones this book opened

Three categories, and it is easy to imply more than is true.

**Worked from directly.** IEEE 1800-2023 is the workhorse, cited across eight chapters. IEEE 1800.2-2020 is the normative UVM statement, with Accellera's UVM 1.2 *User's Guide* as the readable companion and the *Class Reference* for access policies and arbitration modes. Then IEEE 1801-2024 (UPF) for Chapter 19, Accellera's UCIS, the Portable Test and Stimulus Standard, SystemRDL, IEEE 1685-2022 (IP-XACT), the Verilog-AMS reference manual and the UVM Mixed-Signal standard for Chapter 21, and Accellera's CDC/RDC IP Abstraction standard for Chapter 13.

**Named but not held.** Accellera's co-emulation modelling interface, which defines the boundary Chapter 17 lives on, and IEEE 1497 (the Standard Delay Format), referenced but not reproduced by the SystemVerilog standard. Both are recommended in chapter notes; neither was read.

**Deliberately never paraphrased as if opened.** ISO 26262 and DO-254/ED-80. Everything Chapter 22 states about the automotive standard arrives through Richter's platform overview, Ahuja, Agarwal and Jana's fault campaign, and the fault-injection deck of Section C.7; its DO-254 characterisation is attributed to engineers who have worked under both regimes, not to the document. IEC 61508 is named only through the 2024 survey. Chapter 22 says these should be read directly rather than paraphrased — inherit that stance.

One practical warning: the CDC/RDC working-group tutorial recurs at successive conferences with different presenters, and the archive holds at least three editions; the one cited here is the 2026 U.S. edition, not a revision of the others.

**Not covered.** The corpus holds the VHDL reference manual, but this book works in SystemVerilog throughout — VHDL is mentioned twice in twenty-six chapters.

## C.6 Emulation, prototyping and post-silicon

**Start here: Mishra, Ray, Morad and Ziv's post-silicon tutorial.** The anchor for the right-hand side of the flow: the observability ladder from simulator to fabric to silicon, the pre-sighting vocabulary, and trace signal selection.

Rahman et al.'s *Emulation-based System-on-Chip Security Verification* is the platform taxonomy — prototyping, ASIC-class emulation, hybrid co-emulation, the compile-versus-execute distinction, trace-buffer constraints and the environment-divergence problem.

Grove converts a conventional environment into an acceleration-ready one; Hari, Krishnamurthy, Jain and Badaya are clearest on what a virtual environment offers over an in-circuit one. On localisation, Lin, Singh, Barrett and Mitra's symbolic quick-error-detection paper carries the error-detection-latency argument and the trace-length data, with Mitra, Singh and Devarajegowda's deck adding effort comparisons. Jain et al.'s *Never too late with formal* gives the method for reproducing a silicon bug in a proof environment.

**Not covered.** How emulation capacity is allocated across a program, and any lab bring-up narrative beyond the tutorial's.

## C.7 The domain obligations: safety, security, mixed-signal, power and timing

**Safety — start with Richter's *Unified Functional Safety Verification Platform*.** It gives the structure: systematic-versus-random split, the FMEDA process, the fault classification tree, the metric formulas and their failure-rate weighting. Ahuja, Agarwal and Jana supply the worked campaign and its fault-list reduction chain; Sesha Sai Kumar, Mouallem and Mazzawi's *Fault Injection Analysis for Automotive Safety and Security* covers fault models, strobes and cone-of-influence pruning in more detail, and extends into adversarial territory in Chapter 23.

**Security — start with Rahman et al.**, then Hasan et al.'s survey, which organises the same territory by workflow stage. Oberg's root-of-trust talk is the clearest statement of confidentiality and integrity as information-flow relations.

**Mixed-signal — start with Khan, Kashai and Fang**, who apply metric-driven verification end to end to an analog block. Chang and Kundert supply the trust problem and the effort economics (caveat in Section C.11); Brennan, Ziller, Fotouhi and Osman give real-versus-analog modelling and the runtime comparisons.

**Power and timing — start with Liu et al.'s *Low Power Verification with UPF***: a power-intent qualification checklist, an eleven-item isolation checklist and the sequencing rules, read alongside the UPF standard. Litterick's *Full Flow Clock Domain Crossing* covers what happens to a synchronizer between RTL sign-off and silicon.

**Not covered.** Side-channel measurement, the airborne regime in its own words, and any account of combining functional, safety and security positions.

## C.8 People, process and adoption

**Start here: Montesano and Litterick's *Verification Mind Games*.** Seven pages of concrete mindset calls; Chapter 2's backbone, and the source of most of Chapter 24's reflexes for engineers converting from design.

*Making Formal Property Verification Mainstream* is this corpus's only account of taking a technique mainstream inside a large organisation, and its only one with named people-structures: a champion per cluster, escalation to a central expertise team, champions who own the activity across projects, cookie-cutter property templates instead of a blank file, novice-facing self-help material, and the observation that a practice absent from mainstream deliverables does not get exercised. Bromley and Sprott's planning slides are the companion, and candid about people (Section C.10).

Section C.3's planning workshops carry the review mechanics; the 2024 IC/ASIC report the talent-gap data.

**Not covered.** Almost everything: Chapter 24 marks three of its four review mechanics as the author's read, and Chapter 12 does the same for the social layer of a regression gate.

## C.9 Machine learning and language models

**Start here: Yu, Foster and Fitzpatrick's survey of machine learning applications in functional verification**, then Bennett and Eder's 2025 review — the first for what has been tried, the second for why so little reached deployment, including the decay modes and the retraining obligation.

For coverage-directed generation, Fine and Ziv's 2003 Bayesian-network paper is the founding result and still the clearest statement of the cost side; behind few citation markers, it carries a whole section of Chapter 25. Ioannides and Eder review the field at its 2012 maturity; Jayasena and Mishra survey directed test generation in 2024 and refer readers back to them.

On generated properties, read Fang et al.'s *AssertLLM* and Shih, Lin, Gupta and Malik's *FLAG* together and in that order, watching how each defines success. Bai et al.'s *FVDebug* is the model for how such results should be reported, with a model-judged metric and a mechanically checked one side by side. Kumar, Gadde, Radhakrishna and Lettnin's *Saarthi* is the corpus's one industrial agentic-formal deployment report, unusually candid about its failure modes. For landscape, Zang et al.'s agentic-EDA survey supplies the autonomy scale and governance vocabulary; Pan et al. survey the wider field.

**Three provenance caveats, which belong with the recommendation rather than a footnote.** *Saarthi* is the one entry in this book's reference file whose conference edition was never resolved against the proceedings archive: it is cited without an edition, and its year comes from the file's creation timestamp. The agentic-EDA survey's year rests on one signal, its preprint version stamp — which is why Chapter 26 reads it as its authors' expectation rather than a finding. *AssertLLM* and the BZL paper are cited as preprints deliberately, because their published records diverge from the artifacts read: the published *AssertLLM* drops two words from its title, and the published BZL paper has a different title and an extra author.

**Not covered.** Most of it — see Section C.12; Chapter 25 says so in its own text.

## C.10 Sources filed under the wrong heading

Seven cases where a title or citation pattern hides a source from readers who need it.

- **Achutha Kiran Kumar, Seligman et al., *Making Formal Property Verification Mainstream*.** Titled and cited as formal verification; it is the corpus's only technique-adoption programme with named people-structures, and supplies most of Chapter 24's mentoring and process-integration material.
- **Rahman et al., *Emulation-based System-on-Chip Security Verification*.** Titled as security; it is the platform-and-workflow taxonomy for Chapters 17 and 18, which use it more heavily than Chapter 23 — as Chapter 23's own note concedes.
- **Kern and Greenstreet, *Formal Verification in Hardware Design: A Survey*.** Titled as a formal survey; it is where the book's equivalence-checking theory lives, and Chapter 15 calls it the closest thing the corpus has to a treatment. A misindex and a gap in one.
- **Foster, *Trends in Functional Verification: A 2014 Industry Study*.** Titled as survey data; Chapter 15 calls it the origin point for the automatic-formal-application category.
- **Hollander, Morley and Noy, *The e Language*.** Titled as a 2001 language paper; it is the historical rationale behind Chapter 8's decomposition, Chapter 9's constraint-oriented stimulus and Chapter 10's extension-as-configuration.
- **Ahmed et al., *(V&V)-in-the-Loop for RISC-V Design*.** Titled as a methodology vision for one instruction-set family; it is the corpus's only concrete account of hardware continuous-integration tiering (Chapter 12), of a multi-level environment with instruction-set-simulator co-simulation (Chapter 8), and of an FPGA validation flow (Chapter 18).
- **Bromley and Sprott, *Formal Verification in the Real World*.** A formal title carrying some of Chapter 24's best people material: experimentation time, teamwork against stalling, and internal expertise that has to be reachable.

## C.11 Reading this literature critically

These habits are not general scepticism; each was forced by something in this corpus.

**Find the denominator before you read the fraction.** *FLAG* reports covering 53 of 58 manually derived target properties across six open-source protocols — for every protocol but one, which is excluded from that count. Honestly stated in the paper; silently wrong in any summary that drops the exclusion.

**Ask what the pass criterion counts.** *Saarthi*'s primary indicator is a success rate defined as runs that completed end-to-end verification out of total runs: it measures whether the pipeline finished, not whether the properties were right — and vacuous passes are among the failure modes its authors observed. *AssertLLM*'s 89% means "passed a formal proof against known-good RTL", after human engineers removed generations referencing unmappable signals.

**Separate the model-judged metric from the mechanically checked one.** *FVDebug* reports both, which is why its own baseline table exposes the problem: one configuration scored 0.783 on best-hypothesis quality and resolved 65.8% of failures within five attempts; another scored 0.474 — the worst in the table — and resolved 81.6%. Opposite orderings. A paper reporting only the first has told you how plausible its output reads.

**Check what the baseline was.** Bennett and Eder note that random is the most common baseline in this literature, and that beating random says nothing about generalisation. Fine and Ziv's founding result matters precisely because its baseline was an expert's tuned directive file.

**Resolving a paper's year does not date its numbers.** Chang and Kundert's mixed-signal effort figures — model creation at up to 80% of the effort of getting analog blocks into chip-level verification — cite the authors' own consulting experience, undated. The paper resolves to 2015; the figures carry no year, and Chapter 21 says so.

**A container property is not an editorial fact.** Narayan and Symons' talk stood at 2022 in this book's own reference file, on the strength of a date printed in every slide footer — an auto-date field re-rendered during a bulk re-export. The archive puts it at 2015: wrong by seven years. A second entry's metadata prints `Author: DVCon Europe` while the archive records it as DVCon India; that field belongs to the Word template. Timestamps, filenames and metadata authors corroborate at best.

**Two sources that seem to contradict each other usually answer different questions.** Chapter 19 opens on one: the survey reports a metastability class needing a gate-level model with timing, while Litterick says back-end interference is answered by structural and timing analysis, not simulation. Exhibiting a failure and signing off its absence are different jobs.

## C.12 What the corpus does not have

Collected from the chapters that state each gap — the half of a reading guide a bibliography never carries, and the honest answer when someone asks for evidence that is not there.

- **No measured cost-per-stage series.** Chapter 1 says so, and refuses to treat the "cost grows tenfold per stage" rule as data.
- **Nothing on the social layer of a regression gate.** Chapter 12 marks its revert-window and ownership-by-commit guidance as practitioner judgment; no measurements exist here.
- **Equivalence checking is doubly thin.** Chapter 15 records that the literature covers the algorithms lightly relative to their industrial importance, with a 1999 survey as the nearest treatment; it also describes the industrial C-to-RTL flow and states that no source here is being stretched to cover it.
- **No security denominator.** Chapter 23: no enumeration of what an attacker might try, therefore no denominator, therefore no percentage — and no settled definition of security coverage.
- **No study scoring generated testbenches or verification plans.** Chapter 25 states this directly: the one corpus flow that drafts a plan is graded only by whether the downstream proof completed. The nearest adjacent evidence is negative: a 2023 survey found code summarisation in verification not reported at all.
- **Every language-model capability figure was measured on a block, a protocol or a curated benchmark**, none on a system-on-chip. Chapter 25 names the unit-test fallacy for reading module-level pass rates as system-level capability.
- **Review mechanics are largely uncited.** Of Chapter 24's four mechanics for a productive review, only the last comes from the corpus.
- **No survey quantifies the shrinking gate-level tier.** Chapter 19 marks it as a trajectory nothing measures.
- **Four standing failures of the field, from Chapter 26**: it does not learn from its escapes; it cannot estimate, and estimates anyway; it rarely measures whether its own environments could still fail; and it has no common language for combining functional, safety and security positions at one review.

A named gap is reviewable; an unnamed one is a surprise. That is Chapter 26's advice about verification plans, and it applies to the evidence a plan is argued from.
