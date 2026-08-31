# Outline master (estratto dall'HTML approvato 2026-08-26)

Titolo approvato: Hardware Verification: A Holistic Guide

NOTA (2026-08-26, post-download): le marcature "da procurare" qui sotto sono SUPERATE —
la disponibilità reale delle fonti è in meta/corpus_index.md (77 full-text; sono entrati
tra gli altri WRG 2024, Bergeron, Piziali, Cerny SVA, VMM, Yuan, Bertacco, Mishra D&T 2017,
Kern&Greenstreet, Ioannides&Eder, IEEE 1800/1800.2/1801). Wile, Seligman, Foster ABV,
Carter, Rashinkar, Meyer restano NON disponibili → solo further reading.

Outline Guida Verifica

 
 
ChipsIT · Guida olistica alla verifica · Outline master v0.1
 
Outline Guida Verifica
 
La struttura completa della guida — 7 parti, 26 capitoli, ~300 pagine — con le sezioni, le fonti assegnate e lo stato del corpus per capitolo. Questo è il documento da approvare prima che inizi la scrittura: la coerenza del libro si gioca qui.
 

 Lingua ENG master → ITA
 Target ORIGINALE (proposta iniziale) ~300 pp / ~85k parole — **SUPERATO E NON PIÙ VINCOLANTE**.
 Misura reale al 2026-08-27, 20 capitoli su 26: **152.445 parole, 363 pagine**.
 Proiezione a 26 capitoli: ~450 pp / ~190k parole.
 Autorizzazione esplicita: «anche più di 300 [pagine] se necessario, basta che sia
 ben scritto e non prolisso inutilmente».
 Densità misurata: ~610 parole/pagina nominale nelle Parti I-III, ~825 nella Parte V.
 **Non usare il vecchio target come argomento per tagliare un capitolo.** Le bande di
 lunghezza vincolanti sono quelle di `style_guide.md`, ricalibrate su 12 capitoli
 misurati; il numero qui sopra è storico e serve solo a datare la proposta iniziale.
 Rigore claim citati dal corpus o [UNVERIFIED]
 Titolo (proposta) «Hardware Verification: A Holistic Guide»
 

 

 
Cosa devi rivedere tu: (1) il titolo — tre proposte: Hardware Verification: A Holistic Guide · Proving Silicon: The Discipline of Hardware Verification · The Verification Handbook: From Mindset to Sign-off; (2) capitoli da tagliare/aggiungere/spostare; (3) il peso delle parti (le pagine stimate sono ridistribuibili).
 
Legenda fonti: corpus = full-text già disponibile, citabile puntualmente · da procurare = riferimento verificato ma testo non ancora nel corpus (tuo download istituzionale, o resta further-reading).
 

 

## Part I — Foundations ~48 pp
 
Perché la verifica esiste, come pensa un verifier, e perché il problema è formalmente impossibile — quindi si gestisce col rischio.
 

 
Cap. | Titolo e sezioni | Fonti principali | Pp. | 
 
1 | Why Verification ExistsIl problema, i numeri, il costoBug escape e respin · first-silicon success al 14% · 60–70% dell'effort · economia della verifica · casi storici (Pentium FDIV) | corpus Foster DAC 2015 · da procurare WRG 2024 (IC/ASIC + FPGA) · Collett via Foster | 12 | 
 
2 | The Verifier's MindsetDal «far funzionare» al «dimostrare che non si rompe»Designer vs verifier · pensare per rotture · l'indipendenza di giudizio · il valore del dubbio | corpus Verification Mind Games (Verilab) | 8 | 
 
3 | The Verification ProblemPerché la completezza è impossibileSpazio degli stati · controllabilità/osservabilità · l'oracle problem · da esaustivo a risk-driven | da procurare Meyer · Wile/Goss/Roesner cap. 1 · lecture notes (ricerca in corso) | 12 | 
 
4 | The Verification LifecycleDal piano al sign-off: il ciclo interoFasi e milestone · stage di maturità · ruoli e review · schedule reality | da procurare Wile/Goss/Roesner · corpus Foster DAC 2015 (effort data) | 16 | 
 

 

## Part II — Planning and Measurement ~40 pp
 
Il piano come contratto e la misura come verità: senza queste due cose la verifica è opinione.
 

 
Cap. | Titolo e sezioni | Fonti principali | Pp. | 
 
5 | Verification PlanningFeature extraction, vplan, tracciabilitàDalla spec alla feature list · struttura del vplan · pass/fail misurabili · review del piano · risk assessment | corpus Mind Games · OpenHW VerificationPlanning101 (open) · da procurare Piziali | 14 | 
 
6 | Coverage: Theory and PracticeLa teoria della copertura e la sua praticaCode vs functional vs assertion coverage · tassonomia dei metric · coverage model design · closure · esclusioni oneste | da procurare Piziali · Coverage Cookbook (open) · corpus Ioannides/Eder (se scaricato ACM) | 14 | 
 
7 | Metrics-Driven Sign-offDashboard, bug curve, criteri di chiusuraMDV · bug rate curves · sign-off checklist · escape analysis post-mortem | da procurare Carter/Hemmady · WRG 2024 · DVCon papers (ricerca in corso) | 12 | 
 

 

## Part III — Dynamic Verification ~58 pp
 
Il cuore simulativo: architettura del testbench, stimolo, UVM come metodologia (non come API), assertion, ingegneria della regressione.
 

 
Cap. | Titolo e sezioni | Fonti principali | Pp. | 
 
8 | Testbench ArchitectureSelf-checking, scoreboard, reference modelStimulus/checker/coverage separati · scoreboard patterns · reference model · TLM e astrazione | da procurare Bergeron · UVM Cookbook (open) | 14 | 
 
9 | Stimulus: Directed to Random to PortableLa storia e la pratica dello stimoloDirected · constrained-random e la nascita in e/Vera · sequenze · Portable Stimulus (PSS) | corpus Hollander e-language 2001 · PSS LRM Accellera (open) | 12 | 
 
10 | UVM as a MethodologyPerché UVM è fatta così — vendor-neutralFactory e configurabilità · agent/env/test · sequences · RAL · cosa UVM non risolve | UVM Cookbook + Accellera UVM guide (open) · lowRISC DVCodingStyle (open) | 12 | 
 
11 | Assertion-Based VerificationL'assertion come specifica eseguibileSVA concettuale · protocolli · bind e separazione · assertion per sim e formal · densità e qualità | da procurare Foster/Krolnik/Lacey · corpus AssertLLM (per il ponte AI) | 10 | 
 
12 | Regression EngineeringLa fabbrica dei test: seed, triage, CIMulti-seed · flakiness · triage e bug tracking · CI per hardware · compute economics | DVCon papers (ricerca in corso) · corpus Foster DAC 2015 (dati) | 10 | 
 

 

## Part IV — Static and Formal ~44 pp
 
Dimostrare invece di campionare: dallo static signoff al model checking, fino ai flussi ibridi.
 

 
Cap. | Titolo e sezioni | Fonti principali | Pp. | 
 
13 | Static VerificationLint, CDC, RDC, X-propagationPerché lo static è il gate d'ingresso · CDC/RDC theory · X-optimism/pessimism | DVCon papers CDC (ricerca in corso) · vendor whitepaper open | 10 | 
 
14 | Formal Property VerificationModel checking per ingegneriProprietà e assunzioni · bounded vs unbounded · abstrazioni · convergenza · formal signoff | da procurare Seligman 2023 · Kern/Greenstreet · corpus FLAG, Saarthi · Fix (Intel), Reid (Arm) da procurare | 16 | 
 
15 | Formal Apps and EquivalenceIl formal industrializzatoConnectivity · register checks · unreachability · LEC/SEC · datapath C-vs-RTL | da procurare Seligman 2023 · DVCon papers (ricerca in corso) | 10 | 
 
16 | Hybrid FlowsSim+formal insieme, coverage unificataDivisione del lavoro sim/formal · coverage unification (UCIS) · quando l'uno e quando l'altro | UCIS Accellera (open) · DVCon (ricerca in corso) | 8 | 
 

 

## Part V — Beyond RTL Simulation ~44 pp
 
Il resto del ciclo che i corsi UVM non raccontano: emulazione, prototipazione, gate-level, power e il post-silicio.
 

 
Cap. | Titolo e sezioni | Fonti principali | Pp. | 
 
17 | Acceleration and EmulationQuando la simulazione non bastaEmulation vs simulation · ICE vs virtual · use model · economics | corpus arXiv emulation security 2026 (parti) · DVCon (ricerca in corso) | 10 | 
 
18 | FPGA Prototyping and HW/SW Co-verificationIl software incontra l'hardware prima del silicioPrototyping · virtual platforms · co-sim ibrida · firmware-driven verification | da procurare Rashinkar (cap.) · WRG 2024 FPGA report | 10 | 
 
19 | Gate-Level, Timing and Power-AwareGLS, SDF, UPF: la verifica vicino al silicioPerché GLS ancora esiste · timing annotation · UPF/low-power verification (domini, retention, isolamento) | DVCon UPF papers (ricerca in corso) — area gap dichiarata | 10 | 
 
20 | Post-Silicon ValidationDopo il tape-out: bring-up e debugPre vs post silicon · osservabilità · bug reproduction · il loop verso il pre-silicio | da procurare Mishra IEEE D&T 2017 + libro 2019 | 14 | 
 

 

## Part VI — Specialized Domains ~34 pp
 
I domini che diventano obbligatori a seconda del mercato: analog, safety, security.
 

 
Cap. | Titolo e sezioni | Fonti principali | Pp. | 
 
21 | Analog and Mixed-SignalDove il digitale incontra il continuoReal number modeling · AMS co-sim · behavioural models — capitolo breve, gap bibliografico dichiarato | da procurare Rashinkar (cap. AMS) · arXiv formal AMS | 8 | 
 
22 | Safety VerificationISO 26262 / DO-254: verificare per certificareFMEDA · fault injection e fault simulation · diagnostic coverage · tool qualification | DVCon safety papers (ricerca in corso) | 13 | 
 
23 | Security VerificationVerificare contro un avversarioThreat model · security properties · side channels · information flow | corpus AI HW security survey VTS 2026 · emulation SoC security 2026 | 13 | 
 

 

## Part VII — The Human and the Machine ~30 pp
 
Le persone, il processo, e l'AI: come la disciplina sta cambiando e come governarla.
 

 
Cap. | Titolo e sezioni | Fonti principali | Pp. | 
 
24 | Teams, Process and Ramp-upRuoli, review, come si formano i verifierRuoli e riti di review · maturity stages come linguaggio comune · onboarding designer→verifier · qualità del processo | OpenTitan checklists (open) · OpenHW process (open) · Mind Games | 10 | 
 
25 | AI and ML in VerificationDallo stato dell'arte alla governanceML classico (CDG, triage, compressione) · LLM (SVA, TB, vplan) con evidenza · i gate umani · governance | corpus Yu/Foster DVCon 2023 · AssertLLM · FLAG · Saarthi + ricerca Fase 1 ChipsIT | 12 | 
 
26 | The Road AheadConclusioni: dove va la disciplinaIl collo di bottiglia che si sposta · shift-left e shift-right · la verifica come professione | Foster blog 2025-26 (open) · DVCon panel 2026 | 8 | 
 

 

## Appendici ~12 pp
 
 
- A. Glossary — bilingue ENG/ITA (è anche il glossario che vincola la traduzione)
 
- B. Reading paths — percorsi di lettura per profilo (designer in conversione, manager, studente)
 
- C. Bibliography — riferimenti numerati, con marcatura esplicita [corpus] vs [riferimento]
 

 

 
Metodo (sezione dichiarata nel libro): ogni claim importante cita una fonte del corpus a full-text, verificata automaticamente; le opere non accessibili compaiono solo come further reading, mai come evidenza puntuale; i punti senza fonte adeguata sono marcati come opinione dell'autore. Scrittura per sezioni con review indipendente e passata di coerenza globale; traduzione italiana con glossario bilingue approvato.
 

 
Outline master v0.1 — 2026-08-26 · ~302 pp stimate · Sorgente: ~/docs/hw_verification_guide_outline.html · Alla tua approvazione parte la scrittura: Parte I+II come prima ondata.