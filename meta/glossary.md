# Glossary (ENG, with the Italian column of W3)

Consolidated from writer-agent GLOSSARY CANDIDATES after each chapter. This file
becomes Appendix A and constrains the Italian translation.

| Term | Definition (one line) | Introduced | Italian |
|---|---|---|---|
| (test, seed) matrix | What a random regression actually runs — tests as rows, seeds as columns, each cell a run with its own outcome. | ch12 | matrice (test, seed) |
| action (PSS) | Unit of behaviour: atomic when it maps to one operation of the system, compound when it encapsulates a flow of others. | ch09 | action (unità di comportamento in PSS) |
| activation condition | The part of a flow rule saying when tracking starts, such as the cycle a key is loaded. Without it a rule can forbid the design's intended behavior. | ch23 | condizione di attivazione |
| active vs passive agent | Active instantiation emulates a device and drives it; passive builds only the monitor and observes — the switch that carries a block environment into a system one. | ch10 | agent attivo e agent passivo |
| activity (PSS) | The flow of sub-actions a compound action encapsulates, stating scheduling relations rather than a schedule. | ch09 | activity (flusso di sotto-azioni in PSS) |
| ADC (analog-to-digital converter) | Block turning a continuous input into numbers; its behavioral model has to agree with the schematic inside a band fixed before any run. | ch21 | ADC (convertitore analogico-digitale) |
| adversarial stimulus | Traffic whose purpose is to be refused or to drive a design somewhere unspecified. A cooperative environment never emits it, so a security campaign run on one checks nothing. | ch23 | stimolo ostile |
| adversary capability | What an opponent is granted, stated as an enumerable list rather than as attacks, which form an open set. Every security property names one. | ch23 | capacità dell'avversario |
| agent | The reusable unit of an environment: sequencer, driver and monitor for exactly one interface. | ch10 | agent (unità riusabile per una sola interfaccia) |
| agentic formal flow | Pipeline in which one agent drafts a plan, others generate and criticize properties, an engine proves them and coverage is assessed; its published indicator counts finished runs. | ch25 | flusso formale agentico |
| always-on cell | Cell powered from the permanent supply. A route that starts and ends in permanent logic must be built from these, and an ordinary buffer inserted later breaks it. | ch19 | cella sempre alimentata |
| AMBA (advanced microcontroller bus architecture) | Published family of on-chip bus protocols; the interfaces of the example systems, among them AXI and APB, are members of it. | ch01 | AMBA (famiglia di protocolli di bus on-chip) |
| AMS (analog and mixed-signal) | Said of a design or a flow in which analog blocks and digital logic have to be verified together instead of apart. | ch21 | AMS (analogico e a segnali misti) |
| AMS co-simulation (analog and mixed-signal) | Coupling the event-driven engine to a time-domain analog solver so both advance in one simulation, restoring loading and transients at a runtime cost that forbids nightly use. | ch21 | co-simulazione AMS (analogico-digitale) |
| analog solver | Engine that finds node voltages and branch currents by iterating on a matrix, choosing each timestep for accuracy. It can fail to converge; a real-valued model cannot. | ch21 | risolutore analogico |
| analysis port | Broadcast, non-blocking publication of an observed transaction to any number of subscribers, none of which may block the producer or modify what it receives. | ch08 | analysis port (porta di pubblicazione delle osservazioni) |
| APB (advanced peripheral bus) | The simple low-bandwidth member of the AMBA family, carrying configuration registers and slow peripherals. | ch01 | APB (bus AMBA per le periferiche) |
| approximately timed model | Model that adds latency estimates, arbitration policies and bus delays: fast enough for architectural questions about ratios and trends, and unable to return a verdict. | ch18 | modello a tempificazione approssimata |
| arbitration mode | Policy by which a sequencer chooses among pending requests; only the strict modes grant the highest-priority one first. | ch10 | modalità di arbitraggio |
| artifact ownership | Answering for an environment, a model or a plan rather than for a claim about the design. Discharged by the artifact being good, it leaves everyone blameless after an escape. | ch24 | titolarità di un artefatto |
| ASIC (application-specific integrated circuit) | Chip fabricated for one purpose, whose masks cost enough that a functional flaw found afterwards forces another fabrication cycle. | ch01 | ASIC (circuito integrato dedicato) |
| ASIL | Automotive safety integrity level, A to D with D most demanding. Assigned from a hazard's severity, exposure and controllability — **a property of the hazard, never of your block**. | ch22 | ASIL (livello di integrità della sicurezza automobilistica) |
| ASIL decomposition | Assigning different integrity targets to regions of one design; the boundary is itself an obligation, since a fault in the lower region must not defeat the higher one's mechanisms. | ch22 | decomposizione ASIL |
| assertion | A declarative statement of a property the design must hold, evaluated by a tool, whose falsehood indicates an error. | ch11 | assertion (asserzione) |
| asset (security sense) | Something worth protecting, named before any property is written: a key, an entropy source, a boot measurement, or the configuration enforcing every other protection. | ch23 | asset (bene da proteggere) |
| assumption (assume) | A property claimed of the environment rather than of the design: checked like an assertion in simulation, never checked in formal, where it deletes traces instead. | ch11 | assunzione (assume) |
| assumption register | Reviewed table listing every assumption with an identifier, its wording, the party accountable for the behavior it names, and the evidence that discharges it. | ch14 | registro delle assunzioni |
| asynchronous FIFO | Streaming crossing whose gray-coded pointers travel each way while the payload sits in dual-port memory, never entering a synchronizer. | ch13 | FIFO asincrona |
| attribute | A parameter or dimension of a behavior whose value set defines its verifiable space. | ch05 | attributo |
| autonomous monitor | Monitor whose observing thread starts at construction and runs continuously, so a late testbench never back-pressures the design. | ch08 | monitor autonomo |
| AXI (advanced extensible interface) | The high-throughput AMBA interface: separate address, data and response channels, responses allowed out of order, identifiers separating concurrent streams. | ch01 | AXI (interfaccia AMBA a canali indipendenti) |
| base failure rate | Rate carried by each failure mode of each element, computed from design and technology data. Architectural metrics combine these rates, so a detected fraction weights them. | ch22 | tasso di guasto di base |
| batching | Covering many design cycles per host interaction so the link is crossed once per transaction; the speedup ceiling that follows is fixed by the interaction's own cost. | ch17 | batching (raggruppamento delle transazioni) |
| bind | Construct instantiating a checker into a design scope without modifying the design's source. | ch11 | bind |
| binding constraint | The activity a doubled budget would be spent on. For verification it has migrated over decades toward deciding what to check, and it differs per level rather than globally. | ch26 | vincolo dominante |
| bins | Counters over value sets — executable equivalence classes. | ch06 | bins (contenitori di conteggio) |
| blended percentage | Single coverage figure mixing simulation hits with proof results, numerically valid but with no defined denominator, so a review cannot say what fraction it names. | ch16 | percentuale mista |
| block verifier | The person answering for one block's features from extraction through sign-off, and the side of the block-to-system seam where a design's internals are actually understood. | ch24 | verificatore di blocco |
| bound checker | Module carrying its own model of an interface — counters, queues — bound to a port when the rules outgrow what a single property can state. | ch11 | bound checker (modulo legato con bind) |
| boundary cover | Cover on the condition an assumption restricts; when it reads zero, the assumption has never been approached and its simulation corroboration is empty. | ch16 | boundary cover (cover sul limite dell'assunzione) |
| bounded model checking | Proof method that copies the combinational logic once per cycle of a fixed interval and asks a satisfiability solver for a violation inside it. | ch14 | bounded model checking (verifica limitata di modello) |
| bounded proof | Result stating only that no violation exists within a stated number of cycles; a guarantee about the near future, not a proof. | ch14 | prova limitata |
| bring-up | The phase in which environment and DUT first exchange checked transactions. | ch04 | bring-up (avvio dell'ambiente sul DUT) |
| bug curve | Bug discoveries (or open/closed counts) plotted over time; the discipline's main convergence instrument. | ch07 | curva dei bug |
| bug escape | Design flaw surviving verification into a later stage. | ch01 | bug sfuggito alla verifica |
| bug footprint | Region of the coverage space a bug occupies. | ch06 | impronta del bug |
| campaign | Purpose-built run on no clock: launched for a stated reason, owned by someone, producing a written result, then stopping. | ch12 | campagna |
| capability tier | One level of a graded adversary list, from unprivileged software up to invasive physical access. Exposing a physical mechanism to software moves a claim between tiers. | ch23 | livello di capacità |
| CDC (clock-domain crossing) | Signal whose producing and consuming flip-flops run on clocks with no fixed phase relationship, so the sampling instant is unpredictable. | ch13 | CDC (attraversamento di dominio di clock) |
| CDG | Coverage-directed test generation via feedback from coverage results to stimulus. | ch06 | CDG (generazione dei test guidata dalla copertura) |
| champion | A named local expert for a technique inside one team: first point of contact, with an escalation path to central expertise and continuity across projects. Borrowed from the adoption-programme literature. | ch24 | champion (referente locale della tecnica) |
| checking contract | The written list of verdicts an environment will produce, each with a named owner — and the list of verdicts it will not. | ch08 | contratto di verifica (elenco dei verdetti dovuti) |
| CI (continuous integration) | Practice of merging changes often and running an automated tier of checks on each merge, so a break surfaces in minutes. | ch12 | CI (integrazione continua) |
| clock domain | Every flip-flop taking its edge from one clock source, or from clocks derived from it; three clock sources need not give three domains. | ch13 | dominio di clock |
| clock snooping | Taking a clock from inside the design instead of generating one in the environment. It yields fewer failing tests, a faster bring-up, and hidden clocking bugs. | ch24 | clock snooping (clock prelevato dal design) |
| clocking block | Declaration fixing the moment interface signals are sampled or driven, so the testbench cannot race the design it watches. | ch08 | clocking block |
| coarse-grained checking | What an abstract model of a hardware and software interface supports: the basic function is kept, everything finer is discarded, so only use cases at that granularity are checkable. | ch18 | controllo a grana grossa |
| common timestamp source | Free-running counter software can read and monitors can sample, finer than the events to be ordered; without one, separate records of a failure cannot be merged. | ch18 | sorgente comune di marca temporale |
| common-mode error | The same specification misreading encoded in both design and oracle, making a bug structurally invisible. | ch03 | errore di modo comune |
| concurrent assertion | Clocked, temporal assertion evaluated at clock ticks over sampled values, checked on every run that executes it. | ch11 | assertion concorrente |
| condition set | The supply, temperature, corner, frequency and load under which a stated band holds. A tolerance quoted without them is not a specification. | ch21 | insieme delle condizioni |
| conditional sign-off | Sign-off taken now but contingent on named evidence arriving by a named date. | ch07 | sign-off condizionato |
| cone of influence (COI) | The netlist region that can reach an observation point. A fault outside it cannot reach one under any workload whatsoever. | ch22 | cono di influenza (COI) |
| confidentiality (information-flow sense) | Violated when an unauthorized reader can obtain protected state. The claim quantifies over pairs of executions, which is why one sampled execution cannot settle it. | ch23 | riservatezza |
| configuration database | Store of typed values set against hierarchical path patterns, letting an integrator configure an environment without knowing its implementation. | ch10 | database di configurazione |
| connect module | Element a simulator inserts automatically where a continuous port meets a discrete one, chosen from the disciplines and the directions involved. | ch21 | connect module (modulo di conversione) |
| connectivity checking | Proof that every row of an integration table is implemented: named source to named destination, at the declared latency, under the declared enabling condition. | ch15 | verifica di connettività |
| constrained-random | Automatic generation of legal-but-unlikely stimulus under constraints. | ch01 | constrained-random (stimolo casuale vincolato) |
| controllability | The ability to steer a design into a given internal condition using only drivable interfaces. | ch03 | controllabilità |
| corner (engine-selection sense) | Several individually rare conditions holding at once; simulation cost follows the product of their probabilities, while a proof engine is indifferent to that rarity. | ch16 | corner (congiunzione di condizioni rare) |
| correlated errors | One misreading of one recurring pattern, reproduced identically across a generated batch. Sampling estimates nothing about them, so a batch is reviewed whole or rejected whole. | ch25 | errori correlati |
| correlation expiry trigger | Named event that voids a correlation result: a schematic or specification revision, a new operating condition, a retuned parameter, or a model edited during debug. | ch21 | evento di scadenza della correlazione |
| correlation tolerance | The per-port band, part of the specification and declared before any run, within which a model and the schematic must agree. | ch21 | tolleranza di correlazione |
| corruption (power-aware sense) | Simulator behavior when a domain loses its supply: every node inside goes unknown until power returns, which turns an unprotected crossing into a visible failure. | ch19 | corruzione (dei nodi di un dominio spento) |
| counterexample (CEX) | Input sequence a proof engine returns to exhibit a failure, carrying no history the failure does not need, unlike a regression trace. | ch14 | controesempio (CEX) |
| counterparty rule | An assumption naming another team is not closed until someone from that team has read it in review and named the row that discharges it. | ch24 | regola della controparte |
| cover property | Directive asking whether a scenario occurred: a count of matches in simulation, a reachability question answered with a witness in formal. | ch11 | cover property |
| coverage closure | Converging every plan item to covered-or-consciously-excluded status. | ch04 | chiusura della copertura |
| coverage differential | Bin-level comparison of two regressions, used to fail a commit that quietly made the suite ask less. | ch12 | differenziale di copertura |
| coverage hole | Required stimulus/behavior not yet observed. | ch06 | buco di copertura |
| coverage model | Multi-dimensional region defined by attributes and their values. | ch06 | modello di copertura |
| covergroup | SystemVerilog container encapsulating a coverage model specification. | ch06 | covergroup |
| coverpoint | One observed variable/expression partitioned into bins. | ch06 | coverpoint |
| cross coverage | Cartesian combinations of coverpoints. | ch06 | cross coverage (copertura incrociata) |
| the crunch | The end-of-project concentration of the hardest verification work against an immovable date. | ch04 | la stretta finale |
| cutpoint | Signal cut from its fan-in so it may take any value; an over-approximation that keeps proofs valid and can invent failures. | ch14 | cutpoint (segnale liberato) |
| dangerous-undetected fault | Fault that corrupted an output while the mechanism stayed silent: the class a campaign exists to find, and the one that must be fixed or argued away. | ch22 | guasto pericoloso non rilevato |
| data coherency (crossing sense) | The requirement that several bits crossing together be observed as a value the source actually drove; separate from resolving metastability on each bit. | ch13 | coerenza dei dati (nell'attraversamento) |
| data tagging | Encoding the expected destination and transformation inside the payload, so each output monitor can decide correctness on its own. | ch08 | marcatura dei dati |
| datapath equivalence | Word-level proof that an arithmetic block returns the same result as a bit-exact algorithmic reference for every operand, under a declared operand and result mapping. | ch15 | equivalenza del datapath |
| deadlooping | Two automated stages oscillating between states without converging. A cap on iterations is what turns that into a hand-off to a person. | ch25 | deadlooping (oscillazione senza convergenza) |
| debug-time share | Fraction of engineering time spent in debug, tracked as a project health metric. | ch07 | quota di tempo speso in debug |
| decay (of a directed test) | A test that keeps passing while no longer exercising what it was written for, because the design grew past it. | ch09 | decadimento (di un test diretto) |
| defeaturing | Reducing a part to a minimal bootable configuration without power management, security or complex firmware, then restoring features one at a time once it powers on reliably. | ch20 | defeaturing (riduzione a configurazione minima) |
| definition of done | Per-deliverable exit criterion stated as an action ("passes in regression"), never a percentage. | ch04 | definition of done (criterio di completamento) |
| delayed-lockstep | Redundant pair in which the second copy runs some cycles behind, so one disturbance reaches the two at different points and produces a mismatch instead of matching wrong answers. | ch22 | lockstep sfasato |
| dependent failure analysis | Analysis of what a single physical event could do to both halves of a redundant pair at once. | ch22 | analisi dei guasti dipendenti |
| design-for-debug (DfD) | On-die instrumentation for post-silicon observability. | ch01 | design-for-debug (progettazione orientata al debug) |
| detection distance | The time and state between a mistake and the check that catches it; what an end-to-end oracle pays and an assertion does not. | ch08 | distanza di rilevamento |
| detection point | Where the safety mechanism raises its alarm. A fault seen here is *detected* — which is not the same as observed. | ch22 | punto di rilevamento |
| diagnostic coverage | The fraction of a failure mode's faults a mechanism is claimed to catch — estimated in the FMEDA, measured by fault injection. | ch22 | copertura diagnostica |
| directed test | Stimulus whose content and order are written out by hand, doing the same thing on every run. | ch09 | test diretto |
| disable iff | Reset guard discarding any attempt in flight while its expression is true, ending it as neither pass nor failure; at most one per assertion, guarding the whole property. | ch11 | disable iff |
| disposition | The recorded decision on an open item (fix / waive-as-errata / defer with justification). | ch07 | disposizione (decisione registrata sul punto aperto) |
| distribution constraint (dist) | Weights over values and ranges that move probability mass without changing the legal set — and silently forbid whatever the list omits. | ch09 | vincolo di distribuzione (dist) |
| DMA (direct memory access) | Engine moving data between memories on its own, without the processor copying it; the recurring example block of the book. | ch01 | DMA (accesso diretto alla memoria) |
| double assignment | Deliberately giving one feature two plan rows with two metrics, one closed by proof and one by coverage, because the engines fail differently. | ch16 | doppia assegnazione |
| DPI (direct programming interface) | The SystemVerilog mechanism for calling C from the language and being called back, over a restricted set of argument types. | ch17 | DPI (interfaccia di programmazione diretta) |
| drain time | Grace period after the last objection drops, so transactions still in flight reach the checkers. | ch10 | drain time (tempo di svuotamento) |
| DSP (digital signal processor) | Processor specialized for signal arithmetic; in the example systems, a block clock gated off between bursts of work. | ch13 | DSP (processore per segnali digitali) |
| durability audit | Reading a plan row twice: once for what would still be true if every engine improved a thousandfold, and once for what today's tooling contributed to it. | ch26 | audit di durabilità |
| durable property | A statement about the verification problem rather than about a tool, such as exponential state growth or the partiality of every practical oracle. Better engines do not retire it. | ch26 | proprietà durevole |
| DUT (design under test) | The design being verified by the testbench. | ch02 | DUT (progetto in verifica) |
| DVFS (dynamic voltage and frequency scaling) | Trading supply voltage and clock frequency at run time to save energy, which multiplies the operating points a plan has to cover. | ch19 | DVFS (regolazione dinamica di tensione e frequenza) |
| ECC (error-correcting code) | Redundant bits kept with the data so a corrupted word can be spotted and, within the strength of the code, repaired. | ch22 | ECC (codice a correzione d'errore) |
| EDA (electronic design automation) | The tool industry supplying simulators, proof engines and coverage databases; its license count is often what caps a regression. | ch08 | EDA (automazione della progettazione elettronica) |
| emulation | Compiling a design onto a hardware execution fabric, synthesized and partitioned, where it runs under stimulus a host supplies; a model runs, so the work stays pre-silicon. | ch17 | emulazione |
| emulator | Purpose-built machine with its own compiler, transactors and debug infrastructure, offering roughly a billion gates of capacity and observability through triggers and state saving. | ch17 | emulatore |
| engine selection | Deciding per plan row rather than per block which engine discharges it, weighing quantification, rarity against volume, the cost of a witness, and observability. | ch16 | scelta del motore di verifica |
| environment vs directive constraint | Constraints stating what the interface makes legal, which must be obeyed, versus constraints layered above them to steer a run toward chosen scenarios. | ch09 | vincolo d'ambiente e vincolo direttivo |
| equivalence class | A set of input values assumed to exercise identical design behavior, used to shrink the test space. | ch03 | classe di equivalenza |
| errata sheet | Published catalog of post-silicon bugs with workarounds. | ch01 | errata (elenco pubblicato dei bug del silicio) |
| error detection latency | Cycles separating a fault's activation from the point where it becomes observable. For hard bugs the figure reaches millions, against trace windows a few thousand cycles deep. | ch20 | latenza di rilevamento dell'errore |
| error injection | Deliberately driving erroneous stimulus to verify detection/recovery behavior. | ch02 | iniezione di errori |
| errors re-found | Count of failures that re-discover an already-known open bug — the measure of how much of a night was spent learning nothing. | ch12 | errori ritrovati |
| escape | A bug that crosses a sign-off boundary undetected — found on the wrong side of the boundary that was supposed to catch it. Ordinary-English uses of "escape" ("the obvious escape", "escape routes") collide with this term of art and must be reworded. | ch01 | escape (bug che oltrepassa un confine di sign-off) |
| escape analysis | Blameless structured post-mortem of an escape that feeds changes into the next plan and checklist. | ch07 | analisi degli escape |
| evaluation attempt | One evaluation of a property, started afresh at every tick of its clock and running to its own verdict, overlapping the others in flight. | ch11 | tentativo di valutazione |
| exception clause | The part of a flow rule permitting one flow, such as a cipher's output. A rule is only as strong as the clause is narrow, so each needs an expiry. | ch23 | clausola di eccezione |
| executable verification plan | Machine-readable plan whose items link to the coverage/checks/results that discharge them. | ch04 | piano di verifica eseguibile |
| factory | Indirection through which components and objects are constructed, so a type can be replaced without editing the code that instantiates it. | ch10 | factory (indirezione per la costruzione dei componenti) |
| failure signature | Deduplication key built from the first error with everything run-to-run stripped out; over-generic it swallows real finds, over-specific it reduces nothing. | ch12 | firma del fallimento |
| fault injection | **Safety sense**: forcing a fault into internal design state to see whether a safety mechanism detects it. NOT ch02's *error injection*, which perturbs stimulus at the interface. The Italian must keep the two apart. | ch22 | iniezione di guasti |
| fault reaction time interval | The budgeted time a mechanism has to act once it has detected, paired with the interval it has to detect in. Late detection counts as undetected. | ch22 | intervallo di tempo di reazione al guasto |
| fault-tolerant time interval | The budgeted interval, measured from the moment a fault occurs, within which a mechanism must detect and react. Paired with the *fault reaction time interval*. | ch22 | intervallo di tolleranza al guasto |
| feature extraction | Enumerating from spec, interviews and architecture everything that must be shown to work. | ch05 | estrazione delle funzionalità |
| fidelity | Degree to which a coverage model captures actual behavioral requirements. | ch06 | fedeltà (del modello di copertura) |
| field access policy | Declared behaviour of a register field on read and write (read-only, write-one-to-clear, and the rest), from which the model predicts the mirror. | ch10 | politica di accesso del campo |
| FIFO (first-in first-out) | Queue returning entries in the order they arrived; its depth and its fill level are ordinary sources of verification state. | ch03 | FIFO (coda a ordine di ingresso) |
| firmware-driven verification | Using the shipping boot sequence and driver as stimulus: deep along the single trajectory software takes, and silent about legal traffic no driver has reason to emit. | ch18 | verifica guidata dal firmware |
| first-silicon success | First fabricated silicon is production-worthy. | ch01 | successo al primo silicio |
| first-time success | The plan-defined set of features that must work in first silicon. | ch04 | successo al primo colpo |
| first/second/third-order reuse | One environment across many testcases; its components in a system-level environment; those components in a different environment for a different design. | ch10 | riuso di primo, secondo e terzo ordine |
| flaky test (flake) | Test whose outcome varies between runs with identical manifests; it has stopped being evidence, and it teaches the team to ignore red. | ch12 | test instabile (flaky) |
| flow qualification | Evidence that the verification *environment* can fail: systematic faults are injected and what the environment detects is measured. | ch22 | qualifica del flusso |
| FMEDA | Failure mode, effects and diagnostic analysis: element-by-element analysis asking how each element can fail, with what consequence and likelihood, and which safety mechanism handles it. | ch22 | FMEDA (analisi dei modi di guasto, degli effetti e della diagnosi) |
| formal app | Packaged check whose properties the tool supplies, so a team provides only the design and a configuration; the intent lives in a machine-readable source. | ch15 | formal app (applicazione formale) |
| formal property verification | Deciding by mathematical reasoning whether a design can violate a stated property, rather than sampling behavior with stimulus. | ch14 | verifica formale di proprietà |
| FPGA (field-programmable gate array) | Device configured after manufacture, used to run a design orders of magnitude faster than simulation and with far less visibility. | ch01 | FPGA (dispositivo logico programmabile) |
| FPGA prototype | A design's logic mapped onto commodity reconfigurable devices, running at megahertz with real peripherals attached: pre-silicon in time, and a check on hardware in kind. | ch18 | prototipo FPGA |
| fresh-seed yield | Failures per unit of newly-seeded stimulus; discriminates a clean flat bug curve from a saturated one. | ch07 | resa dei seed nuovi |
| front-door vs back-door access | Access driving real bus cycles over the real path, versus one reaching the simulation constructs directly by hierarchical path. | ch10 | accesso front-door e accesso back-door |
| FSM (finite state machine) | Logic written as a set of states plus the transitions among them, the shape that state and transition coverage aim at. | ch06 | FSM (macchina a stati finiti) |
| functional verification | Pre-fabrication establishment that a design implements its specification. | ch01 | verifica funzionale |
| generator/monitor duality | One constraint used three ways: to generate legal traffic, to check a neighbour's output, and to assume in formal. | ch09 | dualità generatore/monitor |
| GLS (gate-level simulation) | Running a testbench on the synthesized netlist. It exhibits phenomena nothing else produces and cannot sign off their absence, since it samples what a test happens to sensitize. | ch19 | GLS (simulazione a livello di porte) |
| golden model | Model trusted by construction because it is the specification, stated at the specification's own level of abstraction; golden is not the same as complete. | ch08 | golden model (modello preso come specifica) |
| good machine / faulty machine | The unmodified design and a copy carrying one hypothetical injected fault, compared at designated strobe times. **ch22 deliberately writes "good", never "golden"** — do not normalise it to ch08's bound *golden model* sense. | ch22 | macchina buona / macchina guasta |
| gray-coded parallel synchronizer | One two-flop chain per bit of a bus, safe only when a single bit changes per transfer so any unresolved bit lands on a legal code. | ch13 | sincronizzatore parallelo con codifica Gray |
| grey-box verification | Black-box verification augmented with design hooks for controllability/observability. | ch03 | verifica grey-box |
| handshake synchronizer | Crossing that synchronizes only request and acknowledge while the source holds the data steady until the acknowledge returns, at the price of round-trip latency. | ch13 | sincronizzatore a handshake |
| hardware redundancy | Replicated hardware whose outputs are compared or voted. NOT ch02's *redundancy*, which is two independent readings of a specification. Same word, unrelated mechanisms. | ch22 | ridondanza hardware |
| hardware-assisted verification | Running a design on hardware instead of in an event-driven simulator, buying throughput and capacity while surrendering visibility, build turnaround and debug ergonomics. | ch17 | verifica assistita da hardware |
| heterogeneous merge | Combining coverage from different verification processes; the interchange standard warns that such items are rarely equivalent and requires the result to be tagged as derived. | ch16 | merge eterogeneo |
| hybrid co-emulation | Split in which host models run the mature parts of a system while selected register-transfer logic runs on the machine, joined by transaction-level channels. | ch17 | co-emulazione ibrida |
| hybrid co-simulation | Partition running components outside the verification target as fast host models and the target itself as register-transfer logic, joined where the architecture already has transaction semantics. | ch18 | co-simulazione ibrida |
| hybrid flow | One campaign running proof and simulation against a single plan, with work assigned by problem structure and one shared definition of legal traffic. | ch16 | flusso ibrido |
| hypothesis quality | Score a language model awards for how closely a proposed cause resembles a known one. It does not order configurations the way an applied fix and a rerun do. | ch25 | qualità dell'ipotesi |
| ICE (in-circuit emulation) | Use model in which real peripherals, hosts or instruments drive the emulated design, at the cost of replay, unattended running and state saving. | ch17 | ICE (emulazione in circuito) |
| IEC 61508 (functional safety of programmable systems) | General industrial safety standard from which several sector standards descend; it fixes integrity levels and the evidence each level demands. | ch22 | IEC 61508 (norma generale di sicurezza funzionale) |
| IEEE 1666 (SystemC standard) | Standard behind SystemC and its transaction-level interfaces, which supply an interoperability layer for models written above the level of signals. | ch08 | IEEE 1666 (norma del linguaggio SystemC) |
| IEEE 1800 (SystemVerilog standard) | Language standard holding design constructs, testbench classes, constrained randomization, functional coverage and assertions in one document. | ch06 | IEEE 1800 (norma del linguaggio SystemVerilog) |
| IEEE 1801 (power intent standard) | Standard notation for stating power intent apart from the design: domains, supply states, isolation, retention, and the legal combinations. | ch19 | IEEE 1801 (norma per l'intento di potenza) |
| ignore_bins vs illegal_bins | "Not my job" exclusion vs "must never happen" (runtime error). | ch06 | ignore_bins e illegal_bins (esclusione contro divieto) |
| image (emulation build) | One compiled build of a design on the platform; it is the unit that gets scheduled, so plan rows are grouped by it rather than by priority. | ch17 | immagine (build compilata sulla piattaforma) |
| immediate assertion | Procedural assertion testing a non-temporal expression when control flow reaches it, where x or z counts as failure. | ch11 | assertion immediata |
| implication (overlapping, non-overlapping) | Property operator making an obligation conditional, starting the consequent in the same tick or the next; an attempt whose antecedent is false succeeds having checked nothing. | ch11 | implicazione (sovrapposta e non sovrapposta) |
| implicit vs explicit prediction | Updating the mirror only from accesses the model itself issued, versus updating it from a predictor fed by the bus monitor, which sees every access. | ch10 | predizione implicita ed esplicita |
| in-fabric monitor | Check reimplemented as logic that latches its verdict into a register software can read, because the platform offers no assertion engine and no waveform to inspect. | ch18 | monitor nel fabric (realizzato in logica) |
| induction | Route to an unbounded result: prove a predicate holds after reset and is preserved by every interval, then it holds for all time. | ch14 | induzione |
| inference (PSS) | The tool completing a partial statement of intent with the actions it requires — and nothing it does not. | ch09 | inferenza (completamento automatico dell'intento in PSS) |
| information-flow tracking | Labeling data as secret or untrusted and following where the label goes, reporting when a protected value reaches an observable place or an untrusted input steers control. | ch23 | tracciamento del flusso di informazione |
| instruction-accurate model | Core model that executes the target instruction set and updates architectural state correctly while promising nothing about how many cycles any operation takes. | ch18 | modello accurato all'istruzione |
| instrumentation manifest | Per-build record of which probes and monitors a bitstream actually contains, so a later investigation knows what remains connected from the previous one. | ch18 | manifesto della strumentazione |
| integration verifier | The person answering for what only appears after assembly, to whom each delivered block arrives as a black box that cannot be learned in the time available. | ch24 | verificatore di integrazione |
| intent curation | Creating and maintaining the machine-readable source an app reads; the real cost of a flow whose properties are otherwise free. | ch15 | intent curation (cura della fonte di intento) |
| intent gate | The first human decision on a generated artifact: does it mean what the specification means. Its owner owns the plan row, and a passing proof is not evidence here. | ch25 | gate di intento |
| IP (intellectual property) | Design block licensed or reused rather than written for this project; how much of a chip is reused governs its verification cost. | ch01 | IP (blocco di proprietà intellettuale) |
| irritator | Background traffic generator run concurrently with the main test, whose only job is to perturb the DUT. Two senses: the testbench component (ch07) and the on-die version running on real silicon (ch20). Both translate the same way, but the Italian text must not imply a testbench when the subject is a fabricated part. | ch07, ch20 | irritator (generatore di traffico di disturbo) |
| ISO 26262 (road vehicle functional safety) | Automotive safety standard fixing integrity levels, architectural metrics, and the assessments a hardware element has to undergo. | ch22 | ISO 26262 (norma di sicurezza funzionale per autoveicoli) |
| isolation | Defined behaviour for a signal whose driving logic is not active. | ch19 | isolamento |
| isolation cell | The cell implementing isolation: it passes values normally and clamps its output to a specified value when its control asserts. Its own cell stays powered — that is what lets it clamp. | ch19 | cella di isolamento |
| ISS (instruction-set simulator) | Fast software model of a processor architecture, run beside the design so architectural state can be compared instruction by instruction. | ch01 | ISS (simulatore del set di istruzioni) |
| JTAG (joint test action group) | The standard serial test and debug port; in the lab, the narrow window through which a fabricated part is driven and watched. | ch18 | JTAG (porta standard di test e debug) |
| known-bad variant | Deliberately broken copy of the design kept in the repository and run regularly, to prove the environment can still fail. | ch08 | variante deliberatamente difettosa |
| latent fault | A fault that cannot violate the safety goal alone and is neither detected nor perceived; it waits for a second fault. | ch22 | guasto latente |
| LEC (logic equivalence checking) | Combinational equivalence between two closely related models, typically RTL and the netlist synthesized from it, proven cone by cone after state points are paired. | ch15 | LEC (verifica di equivalenza logica) |
| leftover | An expectation still queued at end of test, never answered — the failure that produces no mismatch, only a queue that never empties. | ch08 | residuo (attesa mai soddisfatta a fine test) |
| lemma | Auxiliary fact about internal state, proven on its own and then handed to a harder proof as an assumption needing no further discharge. | ch14 | lemma |
| level-shifter | A cell translating a signal from one voltage swing to another. | ch19 | level-shifter (cella di traslazione di livello) |
| lint | Structural check on the design description that reports questionable constructs a compiler accepts, such as inferred latches, width mismatches and unconnected ports. | ch13 | lint |
| liveness property | A claim that something must eventually happen: it can never fail in simulation, where the attempt merely stays open, but a proof engine decides it. | ch11 | proprietà di liveness (di vivacità) |
| localization | Naming the activating input sequence and the block holding the bug. Detection is cheap; this step dominates lab cost and can take weeks for one difficult bug. | ch20 | localizzazione |
| lockstep | **Safety sense**: a pair of hardware cores executing identically with a comparator between them. NOT ch03's sense of stepping an instruction-set simulator against RTL. | ch22 | lockstep (coppia di core in passo con comparatore) |
| LSB (least significant bit) | Lowest-weight bit of a word, and in analog work the unit in which the error budget of a converter is written. | ch21 | LSB (bit meno significativo) |
| MAC (media access control / multiply-accumulate) | Two unrelated senses: the block terminating an Ethernet link, and the multiply-and-add lane of an arithmetic datapath. Context decides which. | ch01 | MAC (controllo di accesso al mezzo / moltiplicazione-accumulo) |
| maturity stage | One of a small set of named, checklist-audited levels of verification maturity shared across blocks. | ch04 | stadio di maturità |
| mechanical gate | Check a machine settles alone on a generated artifact: it compiles, its signals resolve, its antecedent is reachable, it is not a duplicate. All precede any human reading. | ch25 | gate meccanico |
| metastability | The unstable condition of a flip-flop sampled too near a change, which resolves to a legal value only after an unpredictable delay. | ch13 | metastabilità |
| metastability injection | Simulation instrumentation that randomly advances, delays or passes each synchronizer sample, so receiving logic is tested against all three legitimate arrival times. | ch13 | iniezione di metastabilità |
| methodology owner | The person owning the base environment, the register generator flow, the regression infrastructure and the coverage merge on behalf of the other verifiers. | ch24 | titolare della metodologia |
| metrics-driven verification (MDV) | Managing verification on quantitative measurements collected continuously from the process rather than on status estimates from people. | ch07 | verifica guidata dalle metriche (MDV) |
| middle of the flow | Block-level work on register-transfer logic, the one stage with full visibility and a real design. Earlier claims and later debug both press on it; neither replaces it. | ch26 | centro del flusso |
| milestone | A phase-gating event defined as a checkable demonstration, not a state estimate. | ch04 | milestone (traguardo dimostrabile) |
| mined property | Property extracted from the design's own behavior, true by construction, so it detects later changes but finds no bug in the code it came from. | ch15 | proprietà estratta dall'RTL |
| mirror vs desired value | What the model believes the design currently holds, versus a value set in the model alone and pushed to the design later. | ch10 | valore del mirror e valore desiderato |
| model checking | Building the design's finite transition system, computing the states reachable from reset, and deciding a property against that set with a trace when it fails. | ch14 | model checking (verifica di modello) |
| model correlation | Checking a behavioural model against the schematic it abstracts: one self-checking testbench run against both, compared per port against tolerances declared in advance. Two words deliberately — bare "correlation" appears across ten chapters in the ordinary English sense. | ch21 | correlazione del modello |
| model register | The table of every behavioural model a project regresses against: abstraction, circuit revision correlated against, tolerances, conditions covered, date, owner, and what breaks if it is wrong. Sibling of ch14's assumption register. | ch21 | registro dei modelli |
| modport | Restricted view of an interface; an inputs-only clocking modport makes a monitor's passivity a compile-time property rather than a review item. | ch08 | modport |
| MTBF (mean time between failures) | Expected interval between synchronizer failures; its exponent is the available settling window over the flop's time constant, so small window losses cost disproportionately. | ch13 | MTBF (tempo medio tra i guasti) |
| multi-point fault | A combination of faults that together violate the safety goal, classified by whether the mechanism detects it, merely perceives it, or misses it. | ch22 | guasto multiplo |
| multi-stream (virtual) generator | One randomized object holding a sub-descriptor per stream, because constraints cannot be expressed across separate generators. | ch09 | generatore multi-flusso (virtuale) |
| must-not-happen feature | Negative requirement enumerating an error the environment must be able to detect. | ch05 | funzionalità in negativo (ciò che non deve accadere) |
| mutation-based generation | Producing hostile input by perturbing well-formed input. It suits a structured stream that stays almost legal, and not an interface that rejects malformed traffic outright. | ch23 | generazione per mutazione |
| no-connection check | Structural test that no path exists in the cone between two points, discharging a forbidden-connection row more cheaply than a proof engine would. | ch15 | verifica di assenza di collegamento |
| NoC (network-on-chip) | On-chip packet network taking the place of a bus once the number of communicating blocks makes one shared path untenable. | ch01 | NoC (rete su chip) |
| non-convergence fallback | The plan's stated answer, agreed before the work starts, to what happens when a proof does not converge; usually the row moves to simulation. | ch16 | piano di ripiego per la non convergenza |
| notifier | The mechanism that makes a timing violation *functional* rather than merely printed: a timing check drives a notifier signal, which the cell model uses to corrupt its output. | ch19 | notifier (segnale che rende funzionale una violazione di timing) |
| NRE | Non-recurring engineering cost. | ch01 | NRE (costo di ingegneria non ricorrente) |
| objection | A raised claim that an activity must finish before its phase may end; a task phase lasts only while at least one is raised. | ch10 | objection (impegno che tiene aperta la fase) |
| observability | How much internal design state is visible during debug. | ch01 | osservabilità |
| observation point | Where a fault becomes visible to the outside world. A fault seen here is *observed*. Distinct from ch01's *observability*, which is the general property. | ch22 | punto di osservazione |
| one-row-one-metric rule | Each vplan row carries exactly one measurable closure criterion; two evidences = two rows. | ch05 | regola una riga una metrica |
| operational vs observational communication | Point-to-point blocking hand-off, where back-pressure is meaningful, versus broadcast non-blocking publication, where it must never be. | ch08 | comunicazione operativa e comunicazione osservativa |
| oracle | The mechanism that decides whether an observed response is correct. | ch03 | oracolo |
| orphan response | A response from the design that matches no outstanding expectation. | ch08 | risposta orfana |
| over-approximation | Reduction that adds behaviors: a proof on the reduced model still holds on the original, while a failure may be impossible in the real design. | ch14 | sovra-approssimazione |
| over-constraining | Narrowing stimulus below what the design must accept; the quiet form stays satisfiable and silently deletes the feature under test. | ch09 | over-constraining (eccesso di vincoli) |
| own an outcome | Accountability stated as a claim about the design rather than about an artifact. Contrast *artifact ownership*, and note it is **not** a *definition of done*, which is an exit criterion rather than a unit of accountability. | ch24 | farsi carico di un esito |
| partial oracle | A checker that verifies one projection of correctness rather than correctness itself. | ch03 | oracolo parziale |
| path coverage | Coverage of decision sequences, not single branches. | ch06 | path coverage (copertura dei cammini) |
| peek / poke | Back-door sample or deposit that bypasses a field's behaviour entirely, unlike back-door read and write, which mimic the front door's side effects. | ch10 | peek / poke (lettura e deposito diretti in back-door) |
| phasing | The standard ordered steps every component runs together — build top-down, connect bottom-up, run concurrently — so independently written environments can be combined. | ch10 | phasing (successione ordinata delle fasi) |
| PHY (physical layer) | Block driving and receiving the electrical signaling of a link, usually analog, hence modeled rather than simulated at gate level. | ch18 | PHY (blocco di livello fisico) |
| plausible by construction | The property of an artifact from a system whose objective is a convincing continuation of its input: correctness is a frequent by-product rather than the target. | ch25 | plausibile per costruzione |
| PLL (phase-locked loop) | Analog block synthesizing an on-chip clock from a reference; in the lab nothing digital runs before it has locked. | ch20 | PLL (anello ad aggancio di fase) |
| poka-yoke | Mistake-proofing a human process by reducing it to foolproof steps. | ch02 | poka-yoke |
| pool (PSS) | Sized store of resources or objects that actions claim; its depth is a rule the generator must satisfy, not a queue to wait in. | ch09 | pool (deposito di risorse in PSS) |
| portable stimulus | Stimulus described once as a scenario space and retargeted to simulation, emulation, prototype and silicon. | ch09 | portable stimulus (stimolo portabile) |
| power domain | A collection of instances treated as a group for power-management purposes, typically sharing a primary supply set. | ch19 | dominio di potenza |
| power intent | Description of domains, isolation, retention and legal supply states, held outside the design description because the same logic is integrated into different power architectures. | ch19 | intento di alimentazione |
| power state table (PST) | A statement of the legal combinations of supply states. | ch19 | tabella degli stati di potenza (PST) |
| pre-silicon reproducer | What a lab investigation owes the design team: a failing stimulus brief enough for a simulator and narrow enough for a block-level environment. A narrative explanation does not qualify. | ch20 | riproduttore pre-silicio |
| predicted-unreachable | Database flag recording that a coverage item was proven unreachable, so a warning is raised if a later change, constraint or test ever covers it. | ch16 | predicted-unreachable (marcato come irraggiungibile) |
| predictor | Component computing the expected response from a monitored request — never from what the driver intended to send. | ch08 | predictor (predittore della risposta attesa) |
| prime fault / collapsed fault | A prime fault represents an equivalence class; a collapsed fault produces the same observable behaviour as its prime, so only primes are simulated. | ch22 | guasto primo / guasto collassato |
| product machine | Construction running two designs side by side on one input stream and reporting whether their outputs ever differ; the object a sequential equivalence proof explores. | ch15 | macchina prodotto |
| proof core | The logic an engine actually used to establish a result, often smaller than the cone, so a bug inside the cone but outside it escapes. | ch14 | proof core (nucleo della prova) |
| proof-carrying | Arriving with a mechanically checkable argument for itself. A generated property shipped with a cover on its antecedent and the sentence it came from is a small instance. | ch25 | che porta con sé la propria prova |
| property-guided monitor generation | Proving a rule where an engine converges, then compiling the same rule into a synthesizable checker for long firmware runs, since a proof says nothing about software reachability. | ch23 | generazione di monitor guidata dalle proprietà |
| protocol check (CDC sense) | Assertion check that a recognized synchronizer's preconditions really hold: pulse width, source-side stability, request-acknowledge sequencing, one changing bit at a time. | ch13 | verifica di protocollo (per gli attraversamenti) |
| protocol monitor vs functional monitor | Passive component judging whether traffic on an interface is legal, versus one that only reconstructs and publishes what the design did. | ch08 | monitor di protocollo e monitor funzionale |
| prototypability | Design property: the logic can be synthesized for a reconfigurable fabric at all, which rules out vendor memory macros, hand-gated clocks, latch structures and analog content. | ch18 | prototipabilità |
| prototype-scope exclusion | Plan entry naming what a board cannot carry, such as an analog interface replaced by the platform's own, together with the named alternative that discharges it. | ch18 | esclusione di perimetro del prototipo |
| provenance record | Repository entry for a generated artifact: the system and model under it, the exact document revision, the sampling settings, the checks passed, who accepted it, any later edit. | ch25 | registro di provenienza |
| pseudo-static signal | Input declared to change only while its receiver is held in reset or disabled, so the setup may exempt it from crossing analysis. | ch13 | segnale pseudo-statico |
| PSS (Portable Test and Stimulus Standard) | The standard defining that single declarative representation of scenario spaces, taking SystemVerilog as its constraint and coverage reference. | ch09 | PSS (standard per test e stimoli portabili) |
| QED (quick error detection) | Software-only transformation of a test that shortens the interval between activation and failure, for instance by reading a location back immediately after every write. | ch20 | QED (rilevamento rapido dell'errore) |
| quarantine | Named list of confirmed flaky tests, still run and reported but not gating, each with an owner and a date. | ch12 | quarantena |
| radius (formal result) | Number recorded beside a formal verdict in the interchange database: how deep a bounded proof went, or how long its failure trace was, plus the clock. | ch16 | radius (raggio del risultato formale) |
| RAL (register abstraction layer) | Object model of the design's memory-mapped registers and memories — blocks, registers, fields — commonly called the register model. | ch10 | RAL (livello di astrazione dei registri) |
| random hardware fault | A physical defect arising during manufacturing or in operation, permanent or transient. It cannot be verified away — only detected and handled. | ch22 | guasto hardware casuale |
| random stability | Localization of random generation per object and thread, so existing work keeps its sequence — provided new objects, threads and draws are appended, never inserted. | ch09 | stabilità della generazione casuale |
| ranking | Selecting the (test, seed) pairs that contribute coverage and dropping the rest — a compressed suite at equal coverage, exploring nothing new. | ch12 | ranking (selezione delle coppie che portano copertura) |
| RDC (reset-domain crossing) | Path where a register cleared by one asynchronous reset is sampled by a register in another reset domain, possibly under the same clock. | ch13 | RDC (attraversamento di dominio di reset) |
| real I/O | Connecting a prototype to a physical console, network device or storage part, so the shipping driver runs against hardware rather than against a testbench substitute. | ch18 | I/O reale |
| real number modeling (RNM) | Describing a block with real-valued signals updated on events in the ordinary simulator: no matrix to solve, no convergence failure, and no electrical relationship unless written in. | ch21 | RNM (modellazione a numeri reali) |
| reasoning trace | Record linking the intent an agent was given to the action it took, so a reviewer audits the decision rather than only the output. | ch25 | traccia del ragionamento |
| recipe (post-silicon sense) | The tuned combination of temperature, supply, part, elapsed time and feature set that brings a failure back on demand. Lacking one is not a property of the bug. | ch20 | ricetta (condizioni che riproducono il guasto) |
| reconvergence model | Verification as reconciliation of a transformation and an independent second path sharing a common origin. | ch02 | modello di riconvergenza |
| redundancy (verification sense) | Independent second interpretation of the specification by a different person, used as the error-catching mechanism. | ch02 | ridondanza (nel senso della verifica) |
| redundant-state invariant | Assertion that two independently maintained representations of one fact agree — where silent corruption is most often caught. | ch11 | invariante fra stati ridondanti |
| reference model | An independent executable of the specification, taken as golden, run on the same stimulus and compared with the design. | ch03 | modello di riferimento |
| register app | Check proving RTL against a machine-readable register description: reset values, decode, and each field's read and write behavior for every value written. | ch15 | register app (applicazione sui registri) |
| register description language | Machine-readable single source for a register map — addresses, fields and their behaviour — from which model, decode logic and headers are generated. | ch10 | linguaggio di descrizione dei registri |
| regression suite | The test set re-run at fixed cadence to guarantee backward compatibility. | ch04 | suite di regressione |
| repeat-N stability check | Running a test N times unchanged before admitting it to a gating tier, to establish that it is stable. | ch12 | verifica di stabilità con N ripetizioni |
| required proof depth | The bound a bounded result must reach, derived from latency, micro-architecture and corner cases plus margin, and recomputable by a reviewer. | ch14 | profondità di prova richiesta |
| reset synchronizer | Structure asserting reset asynchronously and releasing it on a clock edge, so that no flop meets the release inside its recovery window. | ch13 | sincronizzatore di reset |
| residual fault | A fault that violates the safety goal where a mechanism *is* present, but which falls outside what that mechanism covers. | ch22 | guasto residuo |
| respin | New fabrication cycle with corrected masks forced by an escape. | ch01 | respin (nuovo giro di fabbricazione) |
| responder | Agent that answers requests the design initiates; because its reply is under testbench control it is a driver, not a monitor. | ch08 | responder (agente che risponde alle richieste del progetto) |
| restore-period condition | Predicate a retention strategy requires throughout its restore window. When it lapses the restore fails and the retained value is lost: the canonical wake-race escape. | ch19 | condizione del periodo di ripristino |
| restrict | Directive constraining formal computation only; simulators ignore it. | ch11 | restrict |
| retention | Enhanced functionality on selected sequential elements so their values survive the power-down of the primary supply. | ch19 | retention (mantenimento dello stato) |
| retiming | Moving a register across combinational logic without changing the function; the mapping breaks, so equivalence needs a sequential proof with a declared latency relation. | ch15 | retiming (ricollocazione dei registri) |
| retirement argument | The per-row reason for removing verification work, naming the evidence that replaces it. Cutting a regression by a percentage supplies none. | ch26 | argomento di dismissione |
| reuse gap | Organizational shortfall named by a published taxonomy: knowledge about a block developed at one level and never applied at another, plus missing familiarity with the block itself. | ch24 | lacuna di riuso |
| risk-driven verification | Allocating verification effort by bug likelihood × escape cost instead of pursuing completeness. | ch03 | verifica guidata dal rischio |
| round-trip cost | What a single host interaction costs, counted in the design cycles that could have run instead: the call, the link crossing, host scheduling, the return. Largely fixed by the platform. | ch17 | costo di andata e ritorno |
| RTL (register-transfer level) | The abstraction synthesizable design is written at: registers, the combinational logic between them, and clocks stated explicitly. | ch01 | RTL (livello di trasferimento tra registri) |
| run | The unit of work: one execution with a specific seed and a specific set of source and tool revisions, producing its own messages and coverage. | ch09 | run (singola esecuzione) |
| run manifest | Per-run record of everything needed to repeat it: seed, design and testbench revisions, exact tool build, configuration, host and result. | ch12 | manifest della run |
| S1/S2/S3 | Bug severity classes: S1 blocks tape-out; S2 fix-or-waive with an argument; S3 documentation or cosmetic. | ch07 | S1/S2/S3 (classi di gravità dei bug) |
| safe fault | A fault that cannot violate the safety goal, either because it cannot reach safety-related logic or because its effect is tolerated. | ch22 | guasto sicuro |
| safe state | The state a mechanism takes the system to when it fires: in a vehicle, a warning lamp, a limp mode, or a trip to the dealership. | ch22 | stato sicuro |
| safety case | The written argument shipped as a deliverable, whose claims the evidence supports and whose gaps are argued explicitly. | ch22 | safety case (argomentazione documentata di sicurezza) |
| safety mechanism | The design element that handles a failure mode — and itself a design, with bugs of its own. | ch22 | meccanismo di sicurezza |
| sampled value | The value a concurrent assertion sees: the one held before the clock edge, which is why an assertion cannot race the design it watches. | ch11 | valore campionato |
| sampling temperature | Setting governing how varied a model's output is. It is not a seed: identical input can give different output, so the artifact is versioned rather than the recipe. | ch25 | temperatura di campionamento |
| SAT (Boolean satisfiability) | The decision problem under both constraint solving and proof engines: does an assignment exist that makes a Boolean formula true. | ch09 | SAT (soddisfacibilità booleana) |
| satisfiable narrowing | The quiet over-constraint: assumptions remain consistent and most proofs stand, yet one clause has removed precisely the behavior the difficult property targets. | ch14 | restringimento soddisfacibile |
| SCE-MI (Standard Co-Emulation Modeling Interface) | Published interface for driving an emulated design from untimed host code across vendors; the platform generates clocks and tracks model time, which is what allows replay. | ch17 | SCE-MI (interfaccia standard di modellazione per la co-emulazione) |
| scenario (stimulus) | A sequence of stimulus interesting to the design and unlikely to arise from individually constrained-random items. | ch09 | scenario (di stimolo) |
| scoreboard | The data structure holding the data expected to be received, filled by a predictor and consulted when an output is observed; loosely, the whole self-checking structure around it. | ch02 | scoreboard (registro dei risultati attesi) |
| SDF back-annotation | Loading implementation delays into a simulation from a Standard Delay Format file. SystemVerilog takes only the timing constructs from that file and ignores the rest. | ch19 | retroannotazione SDF |
| SEC (sequential equivalence checking) | Proof that two designs emit the same output sequence for every input sequence, dropping the matched-state assumption and paying a model-checking cost. | ch15 | SEC (verifica di equivalenza sequenziale) |
| seed | The value fixing a run's random draws; replaying it reproduces the stimulus only while generator, sources and tool build are unchanged. | ch09 | seed (seme del generatore casuale) |
| self-checking testbench | An environment that computes pass/fail itself instead of relying on human waveform inspection. | ch03 | testbench autoverificante |
| self-help material | Answers reachable without asking a person: recurring questions, one sheet per application, worked exercises. It is where a local expert's answers go to survive reorganization. | ch24 | materiale di autoconsultazione |
| sequence | Transient object generating stimulus, deliberately outside the component hierarchy so scenarios are not welded into the environment. | ch10 | sequence (sequenza di stimolo) |
| sequence item | The transaction object a sequence produces and a driver consumes. | ch10 | sequence item (transazione prodotta dalla sequence) |
| sequencer | Component holding pending sequence requests and choosing which one the driver receives each time the driver asks. | ch10 | sequencer |
| sequential depth | The number of cycles needed to reach the farthest reachable state from reset; beyond it, a bounded safety result becomes a genuine proof. | ch14 | profondità sequenziale |
| shaped cross | Cross with the reachable space stated via justified exclusions. | ch06 | cross sagomato (con le esclusioni dichiarate) |
| shift-left | Moving a check earlier than the stage that traditionally performed it, so a defect is found before the artifact it would have damaged exists. | ch26 | shift-left (anticipazione dei controlli) |
| shift-right | Moving a check **after tape-out**, onto the fabricated part — the lab and the field, not a pre-silicon platform. An emulator runs a model, so emulation is never shift-right however late it happens. | ch26 | shift-right (controlli spostati dopo il tape-out) |
| side channel | Route by which a protected value can be inferred from an observable physical quantity rather than read. Verifiability depends on whether that quantity exists in the model. | ch23 | canale laterale |
| sighting | A lab failure made repeatable under a stated set of conditions. It precedes assigning a debug team, and both precede any statement about a root cause. | ch20 | sighting (avvistamento ripetibile del guasto) |
| sign-off review | The formal review that judges evidence against the plan and accepts residual risk. | ch04 | revisione di sign-off |
| signal-level acceleration | Putting only the design on the platform while protocol behavior stays in host classes, so every pin event crosses the link. The canonical way to waste a fast machine. | ch17 | accelerazione a livello di segnale |
| silent drift | Divergence among an interface rule's three forms that leaves both reports green, because an assumption tighter than the stimulus permits produces no failure and no hole. | ch16 | deriva silenziosa |
| simstate | The operational capability a supply state supports, from `NORMAL` (full switching with characterised timing) down to `CORRUPT` (the supply cannot even hold existing state). Makes the level of corruption a declared property rather than a fixed behaviour. | ch19 | simstate (capacità operativa dichiarata di uno stato) |
| single event upset (SEU) | The transient fault model: one bit flipped once, then left to propagate or die out. | ch22 | single event upset (SEU, inversione di un bit per evento singolo) |
| single-point fault | A fault that violates the safety goal with no safety mechanism present to catch it. | ch22 | guasto a punto singolo |
| smoke tier | The per-commit tier: fixed seeds, bounded runtime and zero tolerance for a known-failing member, proving only that the build is alive. | ch12 | smoke tier (fascia per ogni commit) |
| SoC (system on chip) | Whole system integrated on one die, processors and accelerators and interconnect and memory and peripherals, verified at three levels. | ch01 | SoC (sistema su chip) |
| soft constraint | Preference rather than requirement: discarded when it cannot hold alongside the active hard constraints, so a default can be overridden instead of fought. | ch09 | soft constraint (vincolo preferenziale) |
| source cover | Evidence that a run actually placed a protected value into the tracked signals. Without one, a flow rule reports green over runs where nothing was ever tracked. | ch23 | cover sulla sorgente |
| spatial merge | Combining coverage taken from different parts of one design; a mechanical operation, unlike a merge across verification processes. | ch16 | merge spaziale |
| spec-hole log | Tracked list of questions extraction raised that the specification cannot answer, filed as spec defects. | ch05 | registro dei buchi di specifica |
| speed adapter | Element between a slowly running emulated design and a real link running at its specified rate: it buffers, throttles and retimes, so content is real and timing is not. | ch17 | adattatore di velocità |
| SPFM / LFM / PMHF | Single-point fault metric, latent fault metric, probabilistic metric for random hardware failures: the architectural metrics, each carrying a threshold per integrity level. | ch22 | SPFM / LFM / PMHF (metriche architetturali della sicurezza) |
| spurious counterexample | Failure trace that the real design cannot produce, arising from a missing assumption or an over-approximated starting state, and cured by stronger invariants. | ch14 | controesempio spurio |
| STA (static timing analysis) | Structural analysis establishing that every path meets its timing constraints, with no stimulus, and silent about what the design computes. | ch19 | STA (analisi statica dei tempi) |
| stage inflation | A maturity stage claimed without its exit checklist, turning a demonstrable state into an assignable status word. | ch24 | inflazione degli stadi |
| stale model | A learner whose training data no longer describes its subject. A stimulus model going stale shows in the coverage report; a generated checker going stale announces nothing. | ch25 | modello obsoleto |
| state point | A register of a model, which a combinational equivalence run must pair with its counterpart before any comparison; unpaired ones yield a mapping report. | ch15 | state point (punto di stato) |
| state restoration ratio | Restored plus traced states over traced states, the research measure of a trace signal set. No industrial report of its use in selecting signals exists. | ch20 | rapporto di ripristino dello stato |
| state space | The set of all possible configurations of a design's state elements; 2^n for n state bits. | ch03 | spazio degli stati |
| state-space explosion | The exponential growth of state count with design size that makes exhaustive analysis intractable. | ch03 | esplosione dello spazio degli stati |
| static timing analysis (STA) | Structural examination of every timing arc against a constraints file across process, voltage, temperature and variation. It is the authority on timing; simulation is one sample. | ch19 | analisi statica dei tempi (STA) |
| static verification | Analysis of the design description alone, needing no stimulus and no stated expectation, exhaustive over structure and silent about what the design computes. | ch13 | verifica statica |
| stepping | A fabrication cycle with corrected masks — what Chapter 1 calls a **respin**, in the vocabulary of the lab. The two words denote the same event; *stepping* is how a bring-up team names it. | ch20 | stepping (nuova maschera, nel lessico del laboratorio) |
| stream key | The tuple naming one ordered stream in a scoreboard: one dimension per independent source of concurrency, and computable from what the observer sees. | ch08 | chiave di flusso |
| strobe time | Instant at which two copies of a design are compared during injection. It fixes what a campaign measures, alongside the choice of compared signals. | ch22 | istante di confronto (strobe) |
| structural pruning | Removing from a fault list every site outside the cone of any observation point: an argument that holds under any stimulus, and cheaper than asking an engine. | ch22 | potatura strutturale |
| stuck-at fault | The conventional model of a permanent defect: a node held at zero or at one. | ch22 | guasto stuck-at |
| SVA (SystemVerilog Assertions) | The four-layer notation — Boolean, sequence, property, statement — in which temporal design rules are written once and read by simulator and proof engine alike. | ch11 | SVA (assertion di SystemVerilog) |
| symbolic checking | Replacing enumerated port indices with constrained arbitrary ones, so one property covers every combination and the argument stays the same size as the design grows. | ch15 | verifica simbolica |
| system slowdown factor | The divisor applied to a system clock so timing closes in fabric. Ratios to a board crystal that does not scale change with it, and crossing behavior with them. | ch18 | fattore di rallentamento del sistema |
| systematic fault | A design bug: a mistake made during development, present in every part ever manufactured, and always permanent. Contrast *random hardware fault*. | ch22 | guasto sistematico |
| tape-out | Freezing and releasing the design database for fabrication. | ch01 | tape-out (rilascio del database per la fabbricazione) |
| temporal merge | Combining repeated executions of one process against one unchanged design; with the spatial case, one of the two merges the standard treats as mechanical. | ch16 | merge temporale |
| test realization | Mapping abstract actions onto target code for one platform: portable describes the model, not the effort. | ch09 | realizzazione del test |
| test selection | Filtering tests before simulating them, on the hypothesis that dissimilar tests hit dissimilar coverage. | ch12 | selezione dei test |
| thousandfold test | Asking whether a claim would survive engines a thousand times better. It separates a property of the problem from a limit of the tooling of the day. | ch26 | test del fattore mille |
| threat model | Versioned document of assets, adversary capabilities and trust boundaries whose rows become checkable claims. A functional specification alone gives no reason to ask its questions. | ch23 | modello delle minacce |
| tier | An admission policy with a runtime budget attached — what earns a place in a given regression run, not when that run is scheduled. | ch12 | tier (fascia di ammissione con budget di tempo) |
| time bomb | Timeout ending a run that waits for something that never comes; useful only as an abnormal ending, since a suite routinely ending on it cannot tell success from deadlock. | ch12 | time bomb (timeout che chiude una run bloccata) |
| timing exception | A human claim in the constraints file that some path need not be analyzed, false or multicycle. An annotated netlist run is what checks that claim. | ch19 | eccezione di timing |
| timing side channel | Dependence of an operation's completion time on protected state. Cycles exist in the model, so this one is verifiable: a fixed-latency claim, or a rule ending at the done signal. | ch23 | canale laterale temporale |
| TLM (transaction-level modelling) | Communication between components in whole transactions over standard interface handles, rather than through signals. | ch10 | TLM (modellazione a livello di transazione) |
| toggle coverage | Per-bit 0↔1 activity metric. | ch06 | toggle coverage (copertura delle commutazioni) |
| tolerance token | Language construct attaching a band to a single real value, so that a coverage bin on a measured quantity can be hit at all despite finite precision. | ch21 | token di tolleranza |
| tool qualification | The argument that a tool's output can be trusted as evidence, scoped to a version, a set of use cases, and often a configuration. | ch22 | qualifica dello strumento |
| traceability | Permanent-ID linkage spec ↔ feature ↔ test/property/coverage ↔ result. | ch05 | tracciabilità |
| transaction level | Abstraction whose unit is a whole operation — injected into the running simulation, terminated later by an observed result — rather than the design's clock cycles. | ch08 | livello di transazione |
| transactor (bus-functional model) | Component converting between pins and transactions: every physical-level operation of one interface encapsulated in one place, so everything above it speaks transactions. | ch08 | transactor (modello funzionale del bus) |
| transactor boundary | The cut between untimed host code and timed synthesized logic. Where it falls, rather than the platform's clock rate, decides the throughput actually obtained. | ch17 | confine del transactor |
| transfer function | Testbench model reproducing the design's data transformation to predict its output: written by you, not golden, and as capable of misreading the specification as the design is. | ch08 | funzione di trasferimento |
| triage | Turning failures into facts before debugging any: deduplicate by signature, classify as design bug, testbench bug or environment failure, then assign. | ch12 | triage (classificazione dei fallimenti) |
| trigger-based debug | Debug built on state machines compiled into the platform that recognize an event sequence and start or stop capture, replacing waveform dumping bounded by a finite buffer. | ch17 | debug a trigger |
| trust boundary | Surface where the capability tier changes. It makes assets and capabilities checkable, since every property reads as one asset not crossing one boundary under one capability. | ch23 | confine di fiducia |
| two-flop synchronizer | Two chained destination flip-flops that give a metastable first stage time to settle before the second samples it; the building block of larger crossing structures. | ch13 | sincronizzatore a due flip-flop |
| type vs instance override | Replacing a requested type everywhere, or only at one instance path; instance wins over type, and both must be registered before the parent builds its children. | ch10 | override di tipo e override di istanza |
| UCIS | Unified Coverage Interoperability Standard — cross-tool coverage interchange. | ch06 | UCIS (standard di interscambio dei dati di copertura) |
| under-approximation | Reduction that removes behaviors: a failure it reports is real, while a clean result proves nothing beyond the reduced model. | ch14 | sotto-approssimazione |
| undetermined | Result in which the engine gave up, through timeout, memory exhaustion or an incomplete algorithm; neither a pass nor a failure. | ch14 | indeterminato |
| unification layer | The verification plan, where each row closes on its own declared evidence, which is what makes a cross-engine report have a denominator. | ch16 | livello di unificazione |
| unit-test fallacy | Reading a high pass rate on block-scale benchmarks as evidence about a system. Every published figure in this area concerns a block, a protocol or a curated benchmark. | ch25 | fallacia del test unitario |
| unreachability app | Check submitting coverage targets to a model checker so an exclusion rests on a proof instead of an argument; the verdict inherits every environment constraint. | ch15 | unreachability app (verifica di irraggiungibilità) |
| UPF (unified power format) | Machine-readable statement of a design's power intent, held outside the design source and read by simulation, synthesis and equivalence tools. | ch01 | UPF (formato standard dell'intento di potenza) |
| UVM (Universal Verification Methodology) | The standardized base class library and API set for building modular, reusable, configurable verification components. | ch10 | UVM (metodologia di verifica universale) |
| vacuous pass | Success of an implication whose antecedent never became true, so nothing was checked — neither a pass nor a failure. | ch06 | successo vacuo |
| valid/invalid hole | Genuine stimulus gap vs a coverage-model bug. | ch06 | buco valido / buco invalido |
| validation | Checking a design on real hardware rather than on a model — post-silicon on fabricated parts, or in the lab on a prototype. The load-bearing contrast is hardware vs model, not fabricated vs FPGA. NOT the Boehm "did we build the right thing?" sense, and not the umbrella term covering pre-silicon work. | ch20 | validazione (prova su hardware reale, non su un modello) |
| validity pruning | Discarding stimulus as "can't happen" before checking whether the interface can express it (anti-pattern). | ch02 | potatura di validità (scarto dello stimolo ritenuto impossibile) |
| variable ordering (solve ... before) | Ordering the solver's choices so a corner case becomes frequent, changing probabilities without changing the legal set. | ch09 | ordinamento delle variabili (solve ... before) |
| verification component (VC) | Reusable testbench-side model of an interface, with a driver to stimulate and a monitor to observe. | ch02 | verification component (componente di verifica) |
| verification gap | Shortfall between what must be verified and what can be (inherent/transient/self-induced). | ch01 | divario di verifica |
| verification IP (VIP) | A verification component supplied ready-made for a standard protocol, typically purchased rather than written. | ch10 | verification IP (VIP, componente di verifica acquistato) |
| verification lifecycle | The phased process from plan to sign-off, with feedback loops, run once per verification level. | ch04 | ciclo di vita della verifica |
| virtual emulation | Use model with no physical target: clocks come from the platform and model time is tracked there, giving deterministic reruns, injection at a chosen cycle and simulator-like debug. | ch17 | emulazione virtuale |
| virtual platform | Software model of a whole system, fast enough to run a real firmware binary long before stable logic exists, and without arbitration, back-pressure, latency or coherence. | ch18 | piattaforma virtuale |
| virtual sequence / virtual sequencer | Sequence coordinating several interfaces at once, through a sequencer that only holds references to sub-sequencers and drives nothing itself. | ch10 | virtual sequence / virtual sequencer |
| volatile (register field) | A field the design can change unobserved, so its mirrored value may not be trusted without a fresh read. | ch10 | volatile (campo di registro) |
| volume criterion | A plan row about aggregate behavior over many transactions, such as throughput, occupancy or fairness; no proof discharges a statistical claim. | ch16 | criterio di volume |
| waiver | Written record accepting a specific evidence hole: hole, reason, risk argument, owner, expiry. | ch07 | waiver (deroga scritta) |
| weakness analysis | Row-by-row review challenge on correctness, precision, completeness. | ch05 | analisi delle debolezze |
| white-box assertion | Assertion checking internal design signals rather than interface behavior. | ch02 | assertion white-box (sui segnali interni) |
| witness | Stimulus sequence a proof engine returns to show that a cover target is reachable while every stated assumption still holds. | ch14 | witness (traccia testimone) |
| witness cost | What a result costs to read: a counterexample arrives short and history-free, a simulation failure arrives with everything that preceded it. | ch16 | witness cost (costo di ottenere la traccia) |
| word-level reasoning | Treating operands and results as numbers rather than bit vectors, which with decomposition is what makes an arithmetic proof converge. | ch15 | ragionamento a livello di parola |
| X-dependent check | Check that needs an unknown value to reach an output. It stays in simulation, because a fabric of real gates has only two values to offer. | ch17 | controllo dipendente da X |
| X-optimism | Simulation propagating a definite 0 or 1 where silicon would hold an unknown, which can mask design bugs — though asynchronous reset works because of it. | ch12 | ottimismo sulle X |
| X-pessimism | Simulation returning an unknown where silicon would produce a definite value, filling waveforms with artifacts that cost tracing time but rarely hide design bugs. | ch13 | pessimismo sulle X |
| X-propagation | The question of whether an unknown can reach a decision or an output, answered at gate level, by a simulator mode, or by proof. | ch13 | propagazione delle X |
| zero-delay netlist | Netlist simulated with no annotated delays and no power intent: the configuration a first gate-level run should use, so each later addition has exactly one suspect. | ch19 | netlist a ritardo nullo |
| zoom-out thinking | Periodic step back from task-level work to reassess project-level verification priorities. | ch02 | sguardo d'insieme (rivalutazione periodica delle priorità) |
