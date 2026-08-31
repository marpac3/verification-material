# Glossary — working draft (ENG; ITA column added at translation time)

Consolidated from writer-agent GLOSSARY CANDIDATES after each chapter. This file
becomes Appendix A and constrains the Italian translation.

| Term | Definition (one line) | Introduced |
|---|---|---|
| DUT (design under test) | The design being verified by the testbench. | ch02 |
| reconvergence model | Verification as reconciliation of a transformation and an independent second path sharing a common origin. | ch02 |
| verification component (VC) | Reusable testbench-side model of an interface, with a driver to stimulate and a monitor to observe. | ch02 |
| scoreboard | The data structure holding the data expected to be received, filled by a predictor and consulted when an output is observed; loosely, the whole self-checking structure around it. | ch02 |
| redundancy (verification sense) | Independent second interpretation of the specification by a different person, used as the error-catching mechanism. | ch02 |
| poka-yoke | Mistake-proofing a human process by reducing it to foolproof steps. | ch02 |
| validity pruning | Discarding stimulus as "can't happen" before checking whether the interface can express it (anti-pattern). | ch02 |
| white-box assertion | Assertion checking internal design signals rather than interface behavior. | ch02 |
| zoom-out thinking | Periodic step back from task-level work to reassess project-level verification priorities. | ch02 |
| error injection | Deliberately driving erroneous stimulus to verify detection/recovery behavior. | ch02 |
| functional verification | Pre-fabrication establishment that a design implements its specification. | ch01 |
| validation | Checking a design on real hardware rather than on a model — post-silicon on fabricated parts, or in the lab on a prototype. The load-bearing contrast is hardware vs model, not fabricated vs FPGA. NOT the Boehm "did we build the right thing?" sense, and not the umbrella term covering pre-silicon work. | ch20 |
| bug escape | Design flaw surviving verification into a later stage. | ch01 |
| respin | New fabrication cycle with corrected masks forced by an escape. | ch01 |
| first-silicon success | First fabricated silicon is production-worthy. | ch01 |
| tape-out | Freezing and releasing the design database for fabrication. | ch01 |
| constrained-random | Automatic generation of legal-but-unlikely stimulus under constraints. | ch01 |
| observability | How much internal design state is visible during debug. | ch01 |
| design-for-debug (DfD) | On-die instrumentation for post-silicon observability. | ch01 |
| verification gap | Shortfall between what must be verified and what can be (inherent/transient/self-induced). | ch01 |
| errata sheet | Published catalog of post-silicon bugs with workarounds. | ch01 |
| NRE | Non-recurring engineering cost. | ch01 |
| verification lifecycle | The phased process from plan to sign-off, with feedback loops, run once per verification level. | ch04 |
| milestone | A phase-gating event defined as a checkable demonstration, not a state estimate. | ch04 |
| definition of done | Per-deliverable exit criterion stated as an action ("passes in regression"), never a percentage. | ch04 |
| maturity stage | One of a small set of named, checklist-audited levels of verification maturity shared across blocks. | ch04 |
| bring-up | The phase in which environment and DUT first exchange checked transactions. | ch04 |
| coverage closure | Converging every plan item to covered-or-consciously-excluded status. | ch04 |
| sign-off review | The formal review that judges evidence against the plan and accepts residual risk. | ch04 |
| first-time success | The plan-defined set of features that must work in first silicon. | ch04 |
| executable verification plan | Machine-readable plan whose items link to the coverage/checks/results that discharge them. | ch04 |
| regression suite | The test set re-run at fixed cadence to guarantee backward compatibility. | ch04 |
| the crunch | The end-of-project concentration of the hardest verification work against an immovable date. | ch04 |
| escape | A bug that crosses a sign-off boundary undetected — found on the wrong side of the boundary that was supposed to catch it. Ordinary-English uses of "escape" ("the obvious escape", "escape routes") collide with this term of art and must be reworded. | ch01 |
| state space | The set of all possible configurations of a design's state elements; 2^n for n state bits. | ch03 |
| state-space explosion | The exponential growth of state count with design size that makes exhaustive analysis intractable. | ch03 |
| controllability | The ability to steer a design into a given internal condition using only drivable interfaces. | ch03 |
| oracle | The mechanism that decides whether an observed response is correct. | ch03 |
| partial oracle | A checker that verifies one projection of correctness rather than correctness itself. | ch03 |
| reference model | An independent executable of the specification, taken as golden, run on the same stimulus and compared with the design. | ch03 |
| self-checking testbench | An environment that computes pass/fail itself instead of relying on human waveform inspection. | ch03 |
| common-mode error | The same specification misreading encoded in both design and oracle, making a bug structurally invisible. | ch03 |
| equivalence class | A set of input values assumed to exercise identical design behavior, used to shrink the test space. | ch03 |
| risk-driven verification | Allocating verification effort by bug likelihood × escape cost instead of pursuing completeness. | ch03 |
| grey-box verification | Black-box verification augmented with design hooks for controllability/observability. | ch03 |
| feature extraction | Enumerating from spec, interviews and architecture everything that must be shown to work. | ch05 |
| must-not-happen feature | Negative requirement enumerating an error the environment must be able to detect. | ch05 |
| attribute | A parameter or dimension of a behavior whose value set defines its verifiable space. | ch05 |
| one-row-one-metric rule | Each vplan row carries exactly one measurable closure criterion; two evidences = two rows. | ch05 |
| traceability | Permanent-ID linkage spec ↔ feature ↔ test/property/coverage ↔ result. | ch05 |
| weakness analysis | Row-by-row review challenge on correctness, precision, completeness. | ch05 |
| spec-hole log | Tracked list of questions extraction raised that the specification cannot answer, filed as spec defects. | ch05 |
| metrics-driven verification (MDV) | Managing verification on quantitative measurements collected continuously from the process rather than on status estimates from people. | ch07 |
| bug curve | Bug discoveries (or open/closed counts) plotted over time; the discipline's main convergence instrument. | ch07 |
| waiver | Written record accepting a specific evidence hole: hole, reason, risk argument, owner, expiry. | ch07 |
| irritator | Background traffic generator run concurrently with the main test, whose only job is to perturb the DUT. Two senses: the testbench component (ch07) and the on-die version running on real silicon (ch20). Both translate the same way, but the Italian text must not imply a testbench when the subject is a fabricated part. | ch07, ch20 |
| S1/S2/S3 | Bug severity classes: S1 blocks tape-out; S2 fix-or-waive with an argument; S3 documentation or cosmetic. | ch07 |
| disposition | The recorded decision on an open item (fix / waive-as-errata / defer with justification). | ch07 |
| conditional sign-off | Sign-off taken now but contingent on named evidence arriving by a named date. | ch07 |
| escape analysis | Blameless structured post-mortem of an escape that feeds changes into the next plan and checklist. | ch07 |
| fresh-seed yield | Failures per unit of newly-seeded stimulus; discriminates a clean flat bug curve from a saturated one. | ch07 |
| debug-time share | Fraction of engineering time spent in debug, tracked as a project health metric. | ch07 |
| covergroup | SystemVerilog container encapsulating a coverage model specification. | ch06 |
| coverpoint | One observed variable/expression partitioned into bins. | ch06 |
| bins | Counters over value sets — executable equivalence classes. | ch06 |
| cross coverage | Cartesian combinations of coverpoints. | ch06 |
| shaped cross | Cross with the reachable space stated via justified exclusions. | ch06 |
| toggle coverage | Per-bit 0↔1 activity metric. | ch06 |
| path coverage | Coverage of decision sequences, not single branches. | ch06 |
| coverage model | Multi-dimensional region defined by attributes and their values. | ch06 |
| fidelity | Degree to which a coverage model captures actual behavioral requirements. | ch06 |
| bug footprint | Region of the coverage space a bug occupies. | ch06 |
| coverage hole | Required stimulus/behavior not yet observed. | ch06 |
| valid/invalid hole | Genuine stimulus gap vs a coverage-model bug. | ch06 |
| CDG | Coverage-directed test generation via feedback from coverage results to stimulus. | ch06 |
| ignore_bins vs illegal_bins | "Not my job" exclusion vs "must never happen" (runtime error). | ch06 |
| UCIS | Unified Coverage Interoperability Standard — cross-tool coverage interchange. | ch06 |
| vacuous pass | Success of an implication whose antecedent never became true, so nothing was checked — neither a pass nor a failure. | ch06 |
| transactor (bus-functional model) | Component converting between pins and transactions: every physical-level operation of one interface encapsulated in one place, so everything above it speaks transactions. | ch08 |
| transaction level | Abstraction whose unit is a whole operation — injected into the running simulation, terminated later by an observed result — rather than the design's clock cycles. | ch08 |
| operational vs observational communication | Point-to-point blocking hand-off, where back-pressure is meaningful, versus broadcast non-blocking publication, where it must never be. | ch08 |
| analysis port | Broadcast, non-blocking publication of an observed transaction to any number of subscribers, none of which may block the producer or modify what it receives. | ch08 |
| predictor | Component computing the expected response from a monitored request — never from what the driver intended to send. | ch08 |
| transfer function | Testbench model reproducing the design's data transformation to predict its output: written by you, not golden, and as capable of misreading the specification as the design is. | ch08 |
| golden model | Model trusted by construction because it is the specification, stated at the specification's own level of abstraction; golden is not the same as complete. | ch08 |
| autonomous monitor | Monitor whose observing thread starts at construction and runs continuously, so a late testbench never back-pressures the design. | ch08 |
| protocol monitor vs functional monitor | Passive component judging whether traffic on an interface is legal, versus one that only reconstructs and publishes what the design did. | ch08 |
| responder | Agent that answers requests the design initiates; because its reply is under testbench control it is a driver, not a monitor. | ch08 |
| stream key | The tuple naming one ordered stream in a scoreboard: one dimension per independent source of concurrency, and computable from what the observer sees. | ch08 |
| orphan response | A response from the design that matches no outstanding expectation. | ch08 |
| leftover | An expectation still queued at end of test, never answered — the failure that produces no mismatch, only a queue that never empties. | ch08 |
| data tagging | Encoding the expected destination and transformation inside the payload, so each output monitor can decide correctness on its own. | ch08 |
| detection distance | The time and state between a mistake and the check that catches it; what an end-to-end oracle pays and an assertion does not. | ch08 |
| clocking block | Declaration fixing the moment interface signals are sampled or driven, so the testbench cannot race the design it watches. | ch08 |
| modport | Restricted view of an interface; an inputs-only clocking modport makes a monitor's passivity a compile-time property rather than a review item. | ch08 |
| checking contract | The written list of verdicts an environment will produce, each with a named owner — and the list of verdicts it will not. | ch08 |
| known-bad variant | Deliberately broken copy of the design kept in the repository and run regularly, to prove the environment can still fail. | ch08 |
| directed test | Stimulus whose content and order are written out by hand, doing the same thing on every run. | ch09 |
| decay (of a directed test) | A test that keeps passing while no longer exercising what it was written for, because the design grew past it. | ch09 |
| environment vs directive constraint | Constraints stating what the interface makes legal, which must be obeyed, versus constraints layered above them to steer a run toward chosen scenarios. | ch09 |
| over-constraining | Narrowing stimulus below what the design must accept; the quiet form stays satisfiable and silently deletes the feature under test. | ch09 |
| soft constraint | Preference rather than requirement: discarded when it cannot hold alongside the active hard constraints, so a default can be overridden instead of fought. | ch09 |
| distribution constraint (dist) | Weights over values and ranges that move probability mass without changing the legal set — and silently forbid whatever the list omits. | ch09 |
| variable ordering (solve ... before) | Ordering the solver's choices so a corner case becomes frequent, changing probabilities without changing the legal set. | ch09 |
| seed | The value fixing a run's random draws; replaying it reproduces the stimulus only while generator, sources and tool build are unchanged. | ch09 |
| run | The unit of work: one execution with a specific seed and a specific set of source and tool revisions, producing its own messages and coverage. | ch09 |
| random stability | Localization of random generation per object and thread, so existing work keeps its sequence — provided new objects, threads and draws are appended, never inserted. | ch09 |
| scenario (stimulus) | A sequence of stimulus interesting to the design and unlikely to arise from individually constrained-random items. | ch09 |
| multi-stream (virtual) generator | One randomized object holding a sub-descriptor per stream, because constraints cannot be expressed across separate generators. | ch09 |
| generator/monitor duality | One constraint used three ways: to generate legal traffic, to check a neighbour's output, and to assume in formal. | ch09 |
| portable stimulus | Stimulus described once as a scenario space and retargeted to simulation, emulation, prototype and silicon. | ch09 |
| PSS (Portable Test and Stimulus Standard) | The standard defining that single declarative representation of scenario spaces, taking SystemVerilog as its constraint and coverage reference. | ch09 |
| action (PSS) | Unit of behaviour: atomic when it maps to one operation of the system, compound when it encapsulates a flow of others. | ch09 |
| activity (PSS) | The flow of sub-actions a compound action encapsulates, stating scheduling relations rather than a schedule. | ch09 |
| pool (PSS) | Sized store of resources or objects that actions claim; its depth is a rule the generator must satisfy, not a queue to wait in. | ch09 |
| inference (PSS) | The tool completing a partial statement of intent with the actions it requires — and nothing it does not. | ch09 |
| test realization | Mapping abstract actions onto target code for one platform: portable describes the model, not the effort. | ch09 |
| UVM (Universal Verification Methodology) | The standardized base class library and API set for building modular, reusable, configurable verification components. | ch10 |
| agent | The reusable unit of an environment: sequencer, driver and monitor for exactly one interface. | ch10 |
| active vs passive agent | Active instantiation emulates a device and drives it; passive builds only the monitor and observes — the switch that carries a block environment into a system one. | ch10 |
| factory | Indirection through which components and objects are constructed, so a type can be replaced without editing the code that instantiates it. | ch10 |
| type vs instance override | Replacing a requested type everywhere, or only at one instance path; instance wins over type, and both must be registered before the parent builds its children. | ch10 |
| configuration database | Store of typed values set against hierarchical path patterns, letting an integrator configure an environment without knowing its implementation. | ch10 |
| phasing | The standard ordered steps every component runs together — build top-down, connect bottom-up, run concurrently — so independently written environments can be combined. | ch10 |
| objection | A raised claim that an activity must finish before its phase may end; a task phase lasts only while at least one is raised. | ch10 |
| drain time | Grace period after the last objection drops, so transactions still in flight reach the checkers. | ch10 |
| sequence | Transient object generating stimulus, deliberately outside the component hierarchy so scenarios are not welded into the environment. | ch10 |
| sequence item | The transaction object a sequence produces and a driver consumes. | ch10 |
| sequencer | Component holding pending sequence requests and choosing which one the driver receives each time the driver asks. | ch10 |
| arbitration mode | Policy by which a sequencer chooses among pending requests; only the strict modes grant the highest-priority one first. | ch10 |
| virtual sequence / virtual sequencer | Sequence coordinating several interfaces at once, through a sequencer that only holds references to sub-sequencers and drives nothing itself. | ch10 |
| TLM (transaction-level modelling) | Communication between components in whole transactions over standard interface handles, rather than through signals. | ch10 |
| RAL (register abstraction layer) | Object model of the design's memory-mapped registers and memories — blocks, registers, fields — commonly called the register model. | ch10 |
| mirror vs desired value | What the model believes the design currently holds, versus a value set in the model alone and pushed to the design later. | ch10 |
| front-door vs back-door access | Access driving real bus cycles over the real path, versus one reaching the simulation constructs directly by hierarchical path. | ch10 |
| peek / poke | Back-door sample or deposit that bypasses a field's behaviour entirely, unlike back-door read and write, which mimic the front door's side effects. | ch10 |
| field access policy | Declared behaviour of a register field on read and write (read-only, write-one-to-clear, and the rest), from which the model predicts the mirror. | ch10 |
| volatile (register field) | A field the design can change unobserved, so its mirrored value may not be trusted without a fresh read. | ch10 |
| implicit vs explicit prediction | Updating the mirror only from accesses the model itself issued, versus updating it from a predictor fed by the bus monitor, which sees every access. | ch10 |
| register description language | Machine-readable single source for a register map — addresses, fields and their behaviour — from which model, decode logic and headers are generated. | ch10 |
| first/second/third-order reuse | One environment across many testcases; its components in a system-level environment; those components in a different environment for a different design. | ch10 |
| verification IP (VIP) | A verification component supplied ready-made for a standard protocol, typically purchased rather than written. | ch10 |
| assertion | A declarative statement of a property the design must hold, evaluated by a tool, whose falsehood indicates an error. | ch11 |
| SVA (SystemVerilog Assertions) | The four-layer notation — Boolean, sequence, property, statement — in which temporal design rules are written once and read by simulator and proof engine alike. | ch11 |
| concurrent assertion | Clocked, temporal assertion evaluated at clock ticks over sampled values, checked on every run that executes it. | ch11 |
| immediate assertion | Procedural assertion testing a non-temporal expression when control flow reaches it, where x or z counts as failure. | ch11 |
| sampled value | The value a concurrent assertion sees: the one held before the clock edge, which is why an assertion cannot race the design it watches. | ch11 |
| evaluation attempt | One evaluation of a property, started afresh at every tick of its clock and running to its own verdict, overlapping the others in flight. | ch11 |
| implication (overlapping, non-overlapping) | Property operator making an obligation conditional, starting the consequent in the same tick or the next; an attempt whose antecedent is false succeeds having checked nothing. | ch11 |
| disable iff | Reset guard discarding any attempt in flight while its expression is true, ending it as neither pass nor failure; at most one per assertion, guarding the whole property. | ch11 |
| assumption (assume) | A property claimed of the environment rather than of the design: checked like an assertion in simulation, never checked in formal, where it deletes traces instead. | ch11 |
| cover property | Directive asking whether a scenario occurred: a count of matches in simulation, a reachability question answered with a witness in formal. | ch11 |
| restrict | Directive constraining formal computation only; simulators ignore it. | ch11 |
| bind | Construct instantiating a checker into a design scope without modifying the design's source. | ch11 |
| bound checker | Module carrying its own model of an interface — counters, queues — bound to a port when the rules outgrow what a single property can state. | ch11 |
| liveness property | A claim that something must eventually happen: it can never fail in simulation, where the attempt merely stays open, but a proof engine decides it. | ch11 |
| redundant-state invariant | Assertion that two independently maintained representations of one fact agree — where silent corruption is most often caught. | ch11 |
| tier | An admission policy with a runtime budget attached — what earns a place in a given regression run, not when that run is scheduled. | ch12 |
| smoke tier | The per-commit tier: fixed seeds, bounded runtime and zero tolerance for a known-failing member, proving only that the build is alive. | ch12 |
| campaign | Purpose-built run on no clock: launched for a stated reason, owned by someone, producing a written result, then stopping. | ch12 |
| (test, seed) matrix | What a random regression actually runs — tests as rows, seeds as columns, each cell a run with its own outcome. | ch12 |
| run manifest | Per-run record of everything needed to repeat it: seed, design and testbench revisions, exact tool build, configuration, host and result. | ch12 |
| failure signature | Deduplication key built from the first error with everything run-to-run stripped out; over-generic it swallows real finds, over-specific it reduces nothing. | ch12 |
| triage | Turning failures into facts before debugging any: deduplicate by signature, classify as design bug, testbench bug or environment failure, then assign. | ch12 |
| errors re-found | Count of failures that re-discover an already-known open bug — the measure of how much of a night was spent learning nothing. | ch12 |
| flaky test (flake) | Test whose outcome varies between runs with identical manifests; it has stopped being evidence, and it teaches the team to ignore red. | ch12 |
| quarantine | Named list of confirmed flaky tests, still run and reported but not gating, each with an owner and a date. | ch12 |
| repeat-N stability check | Running a test N times unchanged before admitting it to a gating tier, to establish that it is stable. | ch12 |
| X-optimism | Simulation propagating a definite 0 or 1 where silicon would hold an unknown, which can mask design bugs — though asynchronous reset works because of it. | ch12 |
| time bomb | Timeout ending a run that waits for something that never comes; useful only as an abnormal ending, since a suite routinely ending on it cannot tell success from deadlock. | ch12 |
| ranking | Selecting the (test, seed) pairs that contribute coverage and dropping the rest — a compressed suite at equal coverage, exploring nothing new. | ch12 |
| test selection | Filtering tests before simulating them, on the hypothesis that dissimilar tests hit dissimilar coverage. | ch12 |
| power domain | A collection of instances treated as a group for power-management purposes, typically sharing a primary supply set. | ch19 |
| isolation | Defined behaviour for a signal whose driving logic is not active. | ch19 |
| isolation cell | The cell implementing isolation: it passes values normally and clamps its output to a specified value when its control asserts. Its own cell stays powered — that is what lets it clamp. | ch19 |
| level-shifter | A cell translating a signal from one voltage swing to another. | ch19 |
| retention | Enhanced functionality on selected sequential elements so their values survive the power-down of the primary supply. | ch19 |
| power state table (PST) | A statement of the legal combinations of supply states. | ch19 |
| simstate | The operational capability a supply state supports, from `NORMAL` (full switching with characterised timing) down to `CORRUPT` (the supply cannot even hold existing state). Makes the level of corruption a declared property rather than a fixed behaviour. | ch19 |
| notifier | The mechanism that makes a timing violation *functional* rather than merely printed: a timing check drives a notifier signal, which the cell model uses to corrupt its output. | ch19 |
| SDF back-annotation | Loading implementation delays into a simulation from a Standard Delay Format file. SystemVerilog takes only the timing constructs from that file and ignores the rest. | ch19 |
| model correlation | Checking a behavioural model against the schematic it abstracts: one self-checking testbench run against both, compared per port against tolerances declared in advance. Two words deliberately — bare "correlation" appears across ten chapters in the ordinary English sense. | ch21 |
| correlation tolerance | The per-port band, part of the specification and declared before any run, within which a model and the schematic must agree. | ch21 |
| model register | The table of every behavioural model a project regresses against: abstraction, circuit revision correlated against, tolerances, conditions covered, date, owner, and what breaks if it is wrong. Sibling of ch14's assumption register. | ch21 |
| fault injection | **Safety sense**: forcing a fault into internal design state to see whether a safety mechanism detects it. NOT ch02's *error injection*, which perturbs stimulus at the interface. The Italian must keep the two apart. | ch22 |
| hardware redundancy | Replicated hardware whose outputs are compared or voted. NOT ch02's *redundancy*, which is two independent readings of a specification. Same word, unrelated mechanisms. | ch22 |
| lockstep | **Safety sense**: a pair of hardware cores executing identically with a comparator between them. NOT ch03's sense of stepping an instruction-set simulator against RTL. | ch22 |
| stepping | A fabrication cycle with corrected masks — what Chapter 1 calls a **respin**, in the vocabulary of the lab. The two words denote the same event; *stepping* is how a bring-up team names it. | ch20 |
| coverage differential | Bin-level comparison of two regressions, used to fail a commit that quietly made the suite ask less. | ch12 |
| systematic fault | A design bug: a mistake made during development, present in every part ever manufactured, and always permanent. Contrast *random hardware fault*. | ch22 |
| random hardware fault | A physical defect arising during manufacturing or in operation, permanent or transient. It cannot be verified away — only detected and handled. | ch22 |
| FMEDA | Failure mode, effects and diagnostic analysis: element-by-element analysis asking how each element can fail, with what consequence and likelihood, and which safety mechanism handles it. | ch22 |
| diagnostic coverage | The fraction of a failure mode's faults a mechanism is claimed to catch — estimated in the FMEDA, measured by fault injection. | ch22 |
| safe fault | A fault that cannot violate the safety goal, either because it cannot reach safety-related logic or because its effect is tolerated. | ch22 |
| single-point fault | A fault that violates the safety goal with no safety mechanism present to catch it. | ch22 |
| residual fault | A fault that violates the safety goal where a mechanism *is* present, but which falls outside what that mechanism covers. | ch22 |
| latent fault | A fault that cannot violate the safety goal alone and is neither detected nor perceived; it waits for a second fault. | ch22 |
| multi-point fault | A combination of faults that together violate the safety goal, classified by whether the mechanism detects it, merely perceives it, or misses it. | ch22 |
| ASIL | Automotive safety integrity level, A to D with D most demanding. Assigned from a hazard's severity, exposure and controllability — **a property of the hazard, never of your block**. | ch22 |
| SPFM / LFM / PMHF | Single-point fault metric, latent fault metric, probabilistic metric for random hardware failures: the architectural metrics, each carrying a threshold per integrity level. | ch22 |
| observation point | Where a fault becomes visible to the outside world. A fault seen here is *observed*. Distinct from ch01's *observability*, which is the general property. | ch22 |
| detection point | Where the safety mechanism raises its alarm. A fault seen here is *detected* — which is not the same as observed. | ch22 |
| good machine / faulty machine | The unmodified design and a copy carrying one hypothetical injected fault, compared at designated strobe times. **ch22 deliberately writes "good", never "golden"** — do not normalise it to ch08's bound *golden model* sense. | ch22 |
| stuck-at fault | The conventional model of a permanent defect: a node held at zero or at one. | ch22 |
| single event upset (SEU) | The transient fault model: one bit flipped once, then left to propagate or die out. | ch22 |
| prime fault / collapsed fault | A prime fault represents an equivalence class; a collapsed fault produces the same observable behaviour as its prime, so only primes are simulated. | ch22 |
| cone of influence (COI) | The netlist region that can reach an observation point. A fault outside it cannot reach one under any workload whatsoever. | ch22 |
| fault-tolerant time interval | The budgeted interval, measured from the moment a fault occurs, within which a mechanism must detect and react. Paired with the *fault reaction time interval*. | ch22 |
| safety mechanism | The design element that handles a failure mode — and itself a design, with bugs of its own. | ch22 |
| safe state | The state a mechanism takes the system to when it fires: in a vehicle, a warning lamp, a limp mode, or a trip to the dealership. | ch22 |
| safety case | The written argument shipped as a deliverable, whose claims the evidence supports and whose gaps are argued explicitly. | ch22 |
| tool qualification | The argument that a tool's output can be trusted as evidence, scoped to a version, a set of use cases, and often a configuration. | ch22 |
| flow qualification | Evidence that the verification *environment* can fail: systematic faults are injected and what the environment detects is measured. | ch22 |
| dependent failure analysis | Analysis of what a single physical event could do to both halves of a redundant pair at once. | ch22 |
| shift-left | Moving a check earlier than the stage that traditionally performed it, so a defect is found before the artifact it would have damaged exists. | ch26 |
| shift-right | Moving a check **after tape-out**, onto the fabricated part — the lab and the field, not a pre-silicon platform. An emulator runs a model, so emulation is never shift-right however late it happens. | ch26 |
| stage inflation | A maturity stage claimed without its exit checklist, turning a demonstrable state into an assignable status word. | ch24 |
| counterparty rule | An assumption naming another team is not closed until someone from that team has read it in review and named the row that discharges it. | ch24 |
| champion | A named local expert for a technique inside one team: first point of contact, with an escalation path to central expertise and continuity across projects. Borrowed from the adoption-programme literature. | ch24 |
| own an outcome | Accountability stated as a claim about the design rather than about an artifact. Contrast *artifact ownership*, and note it is **not** a *definition of done*, which is an exit criterion rather than a unit of accountability. | ch24 |
