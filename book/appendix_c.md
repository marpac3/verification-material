# Appendix C: The literature and its scope

This guide groups sources by topic, assessing their weight, distinctive contributions and gaps; each chapter's reference list instead identifies the support for its claims. That list follows sentence order, so it cannot answer a topic-based reading question six months later.

Titles also obscure relevant content: the recommended account here of adoption across a large organization is a formal property verification paper, covering a named local expert per team, escalation to a central group, continuity across projects and support for novices; until Chapter 24 was written it was cited only in formal chapters. Its title and citation pattern obscured it from readers with process questions. Section C.10 names every case of that kind.

## C.1 Industry survey data

**Initial reading: the 2024 Wilson Research Group IC/ASIC trend report** (Foster, Siemens EDA). This short, current report supplies most quantitative framing in Chapters 1, 4, 7 and 26. Its separate FPGA companion covers a different population, no subset of IC/ASIC; it supplies Chapter 26's escape figure.

Foster's DAC 2015 paper, *Trends in Functional Verification: A 2014 Industry Study*, adds the series methodology, sample design and decade-earlier baseline for the 2024 numbers. Chapter 1 draws its participant counts and confidence interval from it, along with the documented origins of the "70 percent of effort" figure, called unsubstantiated in the literature.

Two counterweights: Mishra, Ray, Morad and Ziv's post-silicon tutorial on what a bug costs as it moves right, and Narayan and Symons' *I Created the Verification Gap*, a taxonomy of self-inflicted shortfall behind the management vocabulary of Chapters 1, 2, 4, 7 and 24.

**Not covered.** Any measured cost-per-stage series (Section C.12).

## C.2 Methodology, testbench architecture and stimulus

**Initial reading: Bergeron's *Writing Testbenches using SystemVerilog*.** Used in seventeen of twenty-six chapters, it alone covers the reconvergence model through bus-functional models, self-checking taxonomy and regression management in a unified treatment.

The *Verification Methodology Manual for SystemVerilog* (Bergeron, Cerny, Hunter, Nightingale) complements the explanatory testbench book with rules for encapsulating self-checking structures, scoreboard recommendations, stimulus layering, seed discipline and the coverage-guideline hierarchy. Chapters 8 and 9 use it for prescriptions resembling a standard.

Hollander, Morley and Noy's 2001 *The e Language: A Fresh Separation of Concerns* explains modern testbench architecture historically through decomposition, transaction-level framing and extension-as-configuration (Section C.10).

For stimulus: Yuan, Pixley and Aziz's *Constraint-Based Verification* on solvers and over-constraint diagnosis, and the Portable Test and Stimulus Standard, the working group's *PSS in the Real World*, and Gupta and Vax's *Test driving Portable Stimulus at AMD* for its industrial limits.

Now included in this list, the *UVM Cookbook* idiom catalog is held; published by Siemens EDA's Verification Academy and not maintained by a community, it supports Chapters 8, 10, 11 and 17.

**Not covered.** Environment architecture as software design at book length.

## C.3 Coverage, metrics and sign-off

**Initial reading: Piziali's *Functional Verification Coverage Measurement and Analysis*.** It covers taxonomy, model design method, fidelity and hole analysis for Chapters 5, 6, 7 and 26.

Clause 19 of the SystemVerilog standard is definitive for covergroup, bin, cross and option semantics; Accellera's Unified Coverage Interoperability Standard carries everything Chapter 16 says about merging results across engines, including its own caution against automatic merging.

On metrics as a management instrument, Meyer and Foster's *Metrics in SoC Verification* is the foundation of Chapter 7; Hristozkov, Pallister and Porter's *No Country For Old Men* is its modern industrial counterpart, with an in-house stack and measurements; Zhang shows what a management platform automates. For planning, Ehlers, Vargas and Carzola cover executable plans and assumption reviews, Marriott, Vance and McNeal deliverables and definitions of done, and Graham et al.'s *Planning for RISC-V Success* contributes the only published plan-row format here.

Four papers address closure automation at different levels: Kodi, Patil and Nair (constraint regeneration), Teplitsky et al. (solver level), Ohana (deep reinforcement learning) and Feng, Chen and Muchandikar (coverage models for formal).

**Not covered.** Coverage model quality: fidelity is discussed but never quantified.

## C.4 Formal verification and its industrialisation

**Initial reading: Kern and Greenstreet's 1999 survey, *Formal Verification in Hardware Design*.** It covers foundations, limits and the required content of a meaningful verification claim. Chapter 15 also calls it the corpus's closest thing to a treatment of equivalence-checking algorithms.

Cerny, Dudani, Havlicek and Korchemny's *SVA: The Power of Assertions in SystemVerilog* is the reference for assertion semantics and for Chapter 14's working vocabulary. Bormann's dissertation is the principal reading here on property completeness; Schwarz's treats bounded versus unbounded proof, sequential depth and spurious counterexamples from arbitrary starting states, extending the machinery across the hardware/firmware boundary for Chapter 18.

For practice, Tripathi, Saxena, Verma and Aggarwal demonstrate crossbar formal sign-off end to end, deriving required proof depth and running a mutation experiment; Bromley and Sprott's *Formal Verification in the Real World* covers complexity management and waiver traps; Achutha Kiran Kumar, Seligman et al.'s *Making Formal Property Verification Mainstream* reports deployment, with a bug taxonomy by difficulty from already-simulated designs.

**Not covered.** Model-checking algorithms and the industrial C-to-RTL equivalence flow (Section C.12).

## C.5 Standards consulted and limits of access

Three categories distinguish access from mention.

**Worked from directly.** IEEE 1800-2023 is cited across eight chapters. IEEE 1800.2-2020 is the normative UVM statement, with Accellera's UVM 1.2 *User's Guide* as the readable companion and the *Class Reference* for access policies and arbitration modes. Then IEEE 1801-2024 (UPF) for Chapter 19, Accellera's UCIS, the Portable Test and Stimulus Standard, SystemRDL, IEEE 1685-2022 (IP-XACT), the Verilog-AMS reference manual and the UVM Mixed-Signal standard for Chapter 21, and Accellera's CDC/RDC IP Abstraction standard for Chapter 13. Accellera's Standard Co-Emulation Modeling Interface reference manual covers Chapter 17's boundary.
IEEE 1666-2023 supports Chapter 8: Clause 9 names the transaction-level interoperability layer. The copy worked from is an institutional licensed download, citable here but not redistributable.

**Named but not held.** IEEE 1497 (the Standard Delay Format), referenced but not reproduced by the SystemVerilog standard. It is recommended in a chapter note and was never read. IEEE's product record lists 1497-2001 as inactive-reserved and names the dual-logo IEC 61523-3:2004 as its replacement, now defining the Standard Delay Format; the book's claims about IEC 61523-3, whose text remains unopened, are limited to that record.

**Unopened; never paraphrased as direct reading.** ISO 26262 and DO-254/ED-80. Everything Chapter 22 states about the automotive standard comes through Richter's platform overview, Ahuja, Agarwal and Jana's fault campaign, and Section C.7's fault-injection deck; its DO-254 characterization is attributed to engineers experienced under both regimes, not the document. IEC 61508 is named only through the 2024 survey. Chapter 22 recommends reading these directly rather than paraphrasing them.

One caveat: the CDC/RDC working-group tutorial recurs at successive conferences with different presenters; the archive holds at least three editions, and the one cited is the 2026 U.S. edition, not a revision of the others.

**Not covered.** The corpus holds the VHDL reference manual, but the book uses SystemVerilog throughout; VHDL is mentioned twice in twenty-six chapters.

## C.6 Emulation, prototyping and post-silicon

**Initial reading: Mishra, Ray, Morad and Ziv's post-silicon tutorial.** For the later flow stages, it covers observability from simulator to fabric to silicon, pre-sighting vocabulary and trace signal selection.

Rahman et al.'s *Emulation-based System-on-Chip Security Verification* classifies platforms: prototyping, ASIC-class emulation and hybrid co-emulation, with the compile-versus-execute distinction, trace-buffer constraints and environment divergence.

Grove converts a conventional environment for acceleration; Hari, Krishnamurthy, Jain and Badaya explain the advantages of a virtual environment over an in-circuit one. On localisation, Lin, Singh, Barrett and Mitra's symbolic quick-error-detection paper carries the error-detection-latency argument and the trace-length data, with Mitra, Singh and Devarajegowda's deck adding effort comparisons. Jain et al.'s *Never too late with formal* gives the method for reproducing a silicon bug in a proof environment.

**Not covered.** How emulation capacity is allocated across a program, and any lab bring-up narrative beyond the tutorial's.

## C.7 The domain obligations: safety, security, mixed-signal, power and timing

**Initial safety reading: Richter's *Unified Functional Safety Verification Platform*.** It covers the systematic-versus-random split, FMEDA process, fault classification tree, metric formulas and their failure-rate weighting. Ahuja, Agarwal and Jana supply the worked campaign and its fault-list reduction chain; Sesha Sai Kumar, Mouallem and Mazzawi's *Fault Injection Analysis for Automotive Safety and Security* covers fault models, strobes and cone-of-influence pruning in more detail, and extends into adversarial territory in Chapter 23.

**Initial security reading: Rahman et al.**, followed by Hasan et al.'s survey, which organizes the same territory by workflow stage. Oberg's root-of-trust talk states confidentiality and integrity as information-flow relations.

**Initial mixed-signal reading: Khan, Kashai and Fang**, who apply metric-driven verification end to end to an analog block. Chang and Kundert supply the trust problem and the effort economics (caveat in Section C.11); Brennan, Ziller, Fotouhi and Osman give real-versus-analog modelling and the runtime comparisons.

**Initial power and timing reading: Liu et al.'s *Low Power Verification with UPF***, alongside the UPF standard: a power-intent qualification checklist, an eleven-item isolation checklist and sequencing rules. Litterick's *Full Flow Clock Domain Crossing* covers what happens to a synchronizer between RTL sign-off and silicon.

**Not covered.** Side-channel measurement, the airborne regime in its own words, and any account of combining functional, safety and security positions.

## C.8 People, process and adoption

**Initial reading: Montesano and Litterick's *Verification Mind Games*.** Seven pages of concrete mindset guidance underpin Chapter 2 and most of Chapter 24's guidance for engineers converting from design.

*Making Formal Property Verification Mainstream* is the corpus's only account of making a technique mainstream in a large organization, and its only one naming roles and support structures: a champion per cluster, escalation to a central expertise team, champions owning the activity across projects, ready-made property templates instead of a blank file, novice self-help material, and the observation that practices absent from mainstream deliverables go unexercised. Bromley and Sprott's companion planning slides discuss people explicitly (Section C.10).

Section C.3's planning workshops carry the review mechanics; the 2024 IC/ASIC report the talent-gap data.

**Not covered.** Almost everything: Chapter 24 identifies three of its four review mechanics as the author's judgment, as Chapter 12 does for a regression gate's social layer.

## C.9 Machine learning and language models

**Initial reading: Yu, Foster and Fitzpatrick's survey of machine learning applications in functional verification**, then Bennett and Eder's 2025 review: the first covers attempts, the second explains limited deployment, including decay modes and the retraining obligation.

For coverage-directed generation, Fine and Ziv's 2003 Bayesian-network paper supplies the founding result and explains costs; despite few citation markers, it supports a whole section of Chapter 25. Ioannides and Eder review the field at its 2012 maturity; Jayasena and Mishra survey directed test generation in 2024 and refer readers back to them.

For generated properties, Fang et al.'s *AssertLLM* and Shih, Lin, Gupta and Malik's *FLAG* should be read together, in that order, comparing their success definitions. Bai et al.'s *FVDebug* shows how results should be reported: a model-judged metric alongside a mechanically checked one. Kumar, Gadde, Radhakrishna and Lettnin's *Saarthi* is the corpus's one industrial agentic-formal deployment report, explicitly detailing failure modes. For landscape, Zang et al.'s agentic-EDA survey supplies the autonomy scale and governance vocabulary; Pan et al. survey the wider field.

**Three provenance caveats, which belong with the recommendation rather than a footnote.** *Saarthi* is the one entry in this book's reference file whose conference edition remains unresolved against the proceedings archive; cited without an edition, it takes its year from the file's creation timestamp. The agentic-EDA survey's year rests on one signal, its preprint version stamp, so Chapter 26 reads it as its authors' expectation rather than a finding. *AssertLLM* and the BZL paper are cited as preprints deliberately, because their published records diverge from the artifacts read: the published *AssertLLM* drops two words from its title, and the published BZL paper has a different title and an extra author.

**Not covered.** Most of it (Section C.12), as Chapter 25 acknowledges.

## C.10 Sources filed under the wrong heading

Seven cases of titles or citation patterns obscuring relevant content.

- **Achutha Kiran Kumar, Seligman et al., *Making Formal Property Verification Mainstream*.** Titled and cited as formal verification, it alone in this corpus describes a technique-adoption program with named roles and support structures, supplying most of Chapter 24's mentoring and process-integration material.
- **Rahman et al., *Emulation-based System-on-Chip Security Verification*.** Titled as security, it supplies the platform-and-workflow taxonomy for Chapters 17 and 18, which use it more than Chapter 23, as Chapter 23's own note acknowledges.
- **Kern and Greenstreet, *Formal Verification in Hardware Design: A Survey*.** Titled as a formal survey, it supplies the book's equivalence-checking theory; Chapter 15 calls it the corpus's nearest treatment.
- **Foster, *Trends in Functional Verification: A 2014 Industry Study*.** Titled as survey data; Chapter 15 calls it the origin point for the automatic-formal-application category.
- **Hollander, Morley and Noy, *The e Language*.** Titled as a 2001 language paper; it is the historical rationale behind Chapter 8's decomposition, Chapter 9's constraint-oriented stimulus and Chapter 10's extension-as-configuration.
- **Ahmed et al., *(V&V)-in-the-Loop for RISC-V Design*.** Titled as a methodology vision for one instruction-set family; it is the corpus's only concrete account of hardware continuous-integration tiering (Chapter 12), of a multi-level environment with instruction-set-simulator co-simulation (Chapter 8), and of an FPGA validation flow (Chapter 18).
- **Bromley and Sprott, *Formal Verification in the Real World*.** A formal title carrying some of Chapter 24's people material: time for experimentation, teamwork to prevent stalling, and accessible internal expertise.

## C.11 Reading this literature critically

Each reading criterion below responds to a specific problem in this corpus.

**Denominators and exclusions.** *FLAG* reports coverage of 53 of 58 manually derived target properties across six open-source protocols, excluding one protocol from that count. The paper states the exclusion; summaries omitting it misreport the result.

**Pass criteria and success rates.** *Saarthi*'s primary success rate divides runs completing end-to-end verification by total runs, measuring pipeline completion rather than property correctness; its authors observed vacuous passes among the failure modes. *AssertLLM*'s 89% means "passed a formal proof against known-good RTL", after human engineers removed generations referencing unmappable signals.

**Model-judged and mechanically checked metrics.** *FVDebug*'s baseline table reports both with opposite orderings: one configuration scored 0.783 on best-hypothesis quality and resolved 65.8% of failures within five attempts; another scored 0.474, the table's worst, and resolved 81.6%. Reporting only the first measures output plausibility.

**Baseline selection.** Bennett and Eder note that random is the most common baseline here, and beating it says nothing about generalization. Fine and Ziv's founding result is significant because it used an expert's tuned directive file as baseline.

**Publication years and measurement dates.** Chang and Kundert's mixed-signal model-creation figure, up to 80% of the effort of getting analog blocks into chip-level verification, comes from their own undated consulting experience. The paper resolves to 2015; the figures carry no year, and Chapter 21 says so.

**Container metadata and bibliographic evidence.** The book's reference file dated Narayan and Symons' talk to 2022 from every slide's footer, an auto-date field re-rendered during bulk re-export. The archive puts it at 2015: wrong by seven years. A second entry's metadata prints `Author: DVCon Europe` while the archive records it as DVCon India; that field belongs to the Word template. Timestamps, filenames and metadata authors corroborate at best.

**Differences in source scope.** Chapter 19 opens on one apparent conflict between two sources: the survey reports a metastability class needing a gate-level model with timing, while Litterick says back-end interference is answered by structural and timing analysis, not simulation. The comparison distinguishes exhibiting a failure from signing off its absence.

## C.12 Corpus gaps

The following gaps are collected from the chapters that identify missing evidence.

- **No measured cost-per-stage series.** Chapter 1 says so, and refuses to treat the "cost grows tenfold per stage" rule as data.
- **Nothing on the social layer of a regression gate.** Chapter 12 marks its revert-window and ownership-by-commit guidance as practitioner judgment; no measurements exist here.
- **Equivalence-checking gaps concern algorithms and industrial flow.** Chapter 15 records limited algorithm coverage relative to industrial importance, with a 1999 survey the nearest treatment; it describes the industrial C-to-RTL flow without claiming source support here.
- **No security denominator.** Chapter 23: no enumeration of what an attacker might try, hence no denominator from which to calculate a percentage, and no settled definition of security coverage.
- **No study scoring generated testbenches or verification plans.** Chapter 25 states that the one corpus flow drafting a plan is graded only by downstream proof completion. The nearest adjacent evidence is negative: a 2023 survey found no reported code summarization in verification.
- **Every language-model capability figure was measured on a block, a protocol or a curated benchmark**, none on a system-on-chip. Chapter 25 names the unit-test fallacy for reading module-level pass rates as system-level capability.
- **Review mechanics are largely uncited.** Of Chapter 24's four mechanics for a productive review, only the last comes from the corpus.
- **No survey quantifies the shrinking gate-level tier.** Chapter 19 marks it as a trajectory nothing measures.
- **Four standing failures of the field, from Chapter 26**: it does not learn from its escapes; it continues to produce estimates despite its inability to estimate; it rarely measures whether its own environments could still fail; and it has no common language for combining functional, safety and security positions at one review.

Chapter 26 recommends making gaps in verification plans explicit so they can be examined during review; the same recommendation applies to the supporting evidence.
