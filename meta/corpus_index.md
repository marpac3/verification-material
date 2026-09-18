# Corpus Index — citation IDs for 'Hardware Verification: A Holistic Guide'

Only these sources may be cited as [cit:ID]. Path is relative to ~/docs/verification_corpus/.
Verify every claim against the actual PDF (Read with targeted pages) before citing.

## Policy — what this file is, and what `references.md` is

The two registry files answer two different questions and are not two copies of one list.

- **`corpus_index.md` (this file) is the whole corpus.** Every PDF held under
  `~/docs/verification_corpus/` has exactly one row here, whether or not the book cites it.
  It is the file that decides what *may* be cited.
- **`meta/references.md` is the active bibliography: only what the book actually cites.**
  An ID earns an entry there when it appears as `[cit:ID]` somewhere in `book/*.md` — which
  includes each chapter's `### Further reading`, since that section cites with `[cit:]` like
  any other prose. `book/appendix_c.md` names sources in prose without `[cit:]` markers and
  therefore does **not** make an ID cited. IDs held but not cited live in that file's
  `## Held, not cited` section, outside the parsed `## Entries` region.

**IDs are stable and this file is append-only.** An ID is never renumbered, never reused and
never deleted, because published chapters, `meta/research/anchors_industrial.md` and the
audits under `meta/audits/` all point at it by number. Empty cells in an existing row may be
completed; the ID column may not be touched. A new source gets the next free number in its
group.

Measured 2026-09-02 (`grep -oh '\[cit:[A-Z][0-9]*' book/*.md | sort -u`): **83** IDs cited by
the book, **92** rows here, **84** entries in `references.md` `## Entries` (the 83 cited, plus
D4 pre-registered for ch19 in W1) and **3** in its `## Held, not cited`. The five corpus rows
with no entry either side — D8, P1, P2, P3, P6 — are held and uncited, which is the normal
state for this file. That the anchor register's routing and the book's citations agree is
enforced by `tools/check_anchors_join.py`.

## standards (11)

| ID | file | pages | internal title |
|---|---|---|---|
| S1 | standards/Portable_Test_Stimulus_Standard_v3.0.pdf | 485 | PSS.book |
| S2 | standards/SystemRDL_2.0_Jan2018.pdf | 146 | SystemRDL.book |
| S3 | standards/UCIS_Version_1.0_Final_June-2012.pdf | 362 | untitled |
| S4 | standards/UVM_Class_Reference_Manual_1.2.pdf | 938 | June 2014 final draft -> release |
| S5 | standards/VAMS-LRM-2023.pdf | 442 | untitled |
| S6 | standards/ieee_1076_2019_vhdl_lrm.pdf | 673 | IEEE Std 1076-2019 (Revision of IEEE Std 1076-2008)  IEEE Standard for |
| S7 | standards/ieee_1685_2022_ipxact.pdf | 750 | IEEE Std 1685-2022, IEEE Standard for IP-XACT, Standard Structure for  |
| S8 | standards/ieee_1800_2023_systemverilog_lrm.pdf | 1354 | IEEE Std 1800™-2023 IEEE Standard for SystemVerilog—Unified Hardware D |
| S9 | standards/ieee_1800_2_2020_uvm.pdf | 458 | IEEE Std 1800.2™-2020, IEEE Standard for Universal Verification Method |
| S10 | standards/ieee_1801_2024_upf.pdf | 614 | IEEE Std 1801™-2024 (Revision of IEEE Std 1801-2018),  IEEE Standard f |
| S11 | standards/uvm_users_guide_1.2.pdf | 190 | uvm_guide.book |

## books (6)

| ID | file | pages | internal title |
|---|---|---|---|
| B1 | books/bergeron_2005_vmm_systemverilog.pdf | 514 |  |
| B2 | books/bergeron_2006_writing_testbenches_sv.pdf | 433 | 0-387-31275-7.pdf |
| B3 | books/bertacco_2006_scalable_hw_verification.pdf | 193 |  |
| B4 | books/cerny_2015_sva_power_of_assertions.pdf | 589 |  |
| B5 | books/piziali_2004_functional_verification_coverage.pdf | 222 |  |
| B6 | books/yuan_2006_constraint_based_verification.pdf | 258 |  |

## reports (2)

| ID | file | pages | internal title |
|---|---|---|---|
| R1 | reports/wrg_2024_fpga_trend_report.pdf | 13 | 2024 Wilson Research Group FPGA functional verification trend report |
| R2 | reports/wrg_2024_ic_asic_trend_report.pdf | 14 | 2024 Wilson Research Group IC/ASIC functional verification trend repor |

## theses (2)

| ID | file | pages | internal title |
|---|---|---|---|
| T1 | theses/Schwarz_-_Formal_Co-Verification_of_Optimized_Embedded_Systems.pdf | 118 | Formal Hardware/Firmware Co-Verification of Optimized Embedded Systems |
| T2 | theses/diss_english_joerg_bormann.pdf | 126 | Jörg Bormann – Vollständige funktionale Verifikation |

## papers (21)

| ID | file | pages | internal title |
|---|---|---|---|
| P1 | papers/1280.pdf | 19 |  |
| P2 | papers/1707.07671.pdf | 21 |  |
| P3 | papers/2102.13460.pdf | 12 |  |
| P4 | papers/2205.08524.pdf | 7 |  |
| P5 | papers/2207.00445.pdf | 8 |  |
| P6 | papers/2308.07757.pdf | 14 |  |
| P7 | papers/2405.17481.pdf | 9 | Paper Title (use style: paper title) |
| P8 | papers/2503.11687.pdf | 40 |  |
| P9 | papers/LSB_.pdf | 10 | Microsoft Word - itc2015.sqed.final.v15.docx |
| P10 | papers/acm_csur_2024_directed_test_generation_survey.pdf | 36 |  |
| P11 | papers/arxiv_2402_00386_assertllm.pdf | 9 | AssertLLM: Generating and Evaluating Hardware Verification Assertions  |
| P12 | papers/arxiv_2504_17226_flag_formal_llm.pdf | 9 |  |
| P13 | papers/arxiv_2604_01572_ai_hw_security_verif.pdf | 7 | AI-Assisted Hardware Security Verification: A Survey and AI Accelerato |
| P14 | papers/arxiv_2604_15073_emulation_soc_security.pdf | 32 | Emulation-based System-on-Chip Security Verification: Challenges and O |
| P15 | papers/dac21_marcelo.pdf | 6 |  |
| P16 | papers/fine_ziv_2003_cdg_bayesian_networks.pdf | 6 | p18-2-ziv.dvi |
| P17 | papers/foster_dac2015_trends.pdf | 6 | Microsoft Word - Foster-DAC-Submission.doc |
| P18 | papers/hollander_2001_e_language.pdf | 10 | The e language: a fresh separation of concerns - Technology of Object- |
| P19 | papers/ioannides_eder_2012_cdg_machine_learning_review.pdf | 21 | Coverage-Directed Test Generation Automated by Machine Learning -- A R |
| P20 | papers/kern_greenstreet_1999_formal_verification_survey.pdf | 71 | Formal verification in hardware design: a survey |
| P21 | papers/mishra_2017_post_silicon_validation_soc_era.pdf | 25 | Post-Silicon Validation in the SoC Era: A Tutorial Introduction |

## dvcon (35)

| ID | file | pages | internal title |
|---|---|---|---|
| D1 | dvcon/1046-Closing-Functional-Coverage-With-Deep-Reinforcement-Learning-A-Compression-Encoder-Example.pdf | 11 | Paper Title (use style: paper title) |
| D2 | dvcon/Fault-Injection-Analysis-for-Automotive-Safety-and-Security.pdf | 57 | PowerPoint Presentation |
| D3 | dvcon/Never-too-late-with-formal-Stepwise-guide-for-applying-formal-verification-in-post-silicon-phase-to-avoid-re-spins.pdf | 11 |  |
| D4 | dvcon/P18-DVConIndia25_Final_PPT_5976.pdf | 1 | [no PDF Title metadata] Novel and optimized solution to accelerate gate level simulation for complex SOC — DVCon India 2025 poster, one A0 page, © Accellera. NO author affiliation printed on the page or in the archive listing; see the D4 row in references.md "Provenance notes" |
| D5 | dvcon/PSS-In-The-Real-World.pdf | 98 | PowerPoint Presentation |
| D6 | dvcon/Planning-for-RISC-V-Success-Verification-Planning-and-Functional-Coverage-lead-to-quality-RISC-V-processo.pdf | 16 | PowerPoint Presentation |
| D7 | dvcon/Proven-Strategies-for-Better-Verification-Planning.pdf | 43 |  |
| D8 | dvcon/SW_4A_1_CDC_RDC_Format_Update.pdf | 63 |  |
| D9 | dvcon/best-practices-in-verification-planning.pdf | 10 | Microsoft Word - Best Practices in Verification Planning - Final Revie |
| D10 | dvcon/coverage-driven-distribution-of-constrained-random-stimuli.pdf | 8 | Preparation of Papers in Two-Column Format for the Proceedings of the  |
| D11 | dvcon/coverage-models-for-formal-verification.pdf | 9 | Preparation of Papers in Two-Column Format for the Proceedings of the  |
| D12 | dvcon/formal-assisted-fault-campaign-for-iso26262-certification.pdf | 8 | Paper Title (use style: paper title) |
| D13 | dvcon/formal-verification-in-the-real-world.pdf | 62 |  |
| D14 | dvcon/full-flow-clock-domain-crossing-from-source-to-si.pdf | 12 | litterick_cdc_paper |
| D15 | dvcon/fully-automated-functional-coverage-closure.pdf | 8 | Preparation of Papers in Two-Column Format for the Proceedings of the  |
| D16 | dvcon/i-created-the-verification-gap-presentation.pdf | 16 |  |
| D17 | dvcon/low-power-verification-with-upf-principle-and-practice.pdf | 8 | DVCON2010_108-PY527 |
| D18 | dvcon/making-formal-property-verification-mainstream-an-intel-graphics-experience.pdf | 9 |  |
| D19 | dvcon/metric-driven-verification-of-mixed-signal-designs.pdf | 6 | DVCon_uvm_ms_v011311.1 |
| D20 | dvcon/metrics-in-soc-verification.pdf | 9 | Paper Title (use style: paper title) |
| D21 | dvcon/montesano_verification_mind_games.pdf | 7 | Paper Title (use style: paper title) |
| D22 | dvcon/no-country-for-old-men-a-modern-take-on-metrics-driven-verification-paper.pdf | 8 | Microsoft Word - dvcon_europe_no_country_for_old_men.docx |
| D23 | dvcon/practical-approach-using-a-formal-app-to-detect-x-optimism-related-rtl-bugs.pdf | 9 | Paper Title (use style: paper title) |
| D24 | dvcon/qed-symbolic-qed-pre-silicon-verification-post-silicon-validation-industrial-results-presentation.pdf | 79 |  |
| D25 | dvcon/saarthi_infineon_dvcon2025.pdf | 13 |  |
| D26 | dvcon/smarter-verification-management.pdf | 40 |  |
| D27 | dvcon/specification-driven-analog-and-mixed-signal-verification.pdf | 14 | Preparation of Papers in Two-Column Format for the Proceedings of the  |
| D28 | dvcon/system-level-security-verification-starts-with-the-hardware-root-of-trust-presentation.pdf | 34 |  |
| D29 | dvcon/test-driving-portable-stimulus-at-amd.pdf | 17 |  |
| D30 | dvcon/the-how-tosof-advanced-mixed-signal-verification.pdf | 51 |  |
| D31 | dvcon/the-process-and-proof-for-formal-sign-off-a-live-case-study.pdf | 10 | Microsoft Word - DVCon_paper_pa012716.docx |
| D32 | dvcon/unified-functional-safety-verification-platform-for-iso-26262-compliant-automotive-presentation.pdf | 54 |  |
| D33 | dvcon/uvm-hardware-assisted-acceleration-with-fpga-co-emulation.pdf | 44 |  |
| D34 | dvcon/verification-of-clock-domain-crossing-jitter-and-metastability-tolerance-using-emulation.pdf | 7 | Proceedings Template - WORD |
| D35 | dvcon/yu_foster_dvcon2023_ml_survey.pdf | 9 |  |

## additions 2026-08-26 (IDs are STABLE/append-only — never regenerate positionally)

| ID | file | pages | note |
|---|---|---|---|
| D36 | dvcon/dvcon_us2026_cdc_rdc_standard_tutorial.pdf | 93 | Accellera CDC/RDC standard tutorial deck, DVCon US 2026 (supersedes D8) |
| S12 | standards/accellera_cdc_rdc_standard_v1_0_2026.pdf | 120 | Accellera CDC/RDC IP Abstraction Standard v1.0, March 2026 |
| S13 | standards/accellera_uvm_ms_standard_v1_0_2025.pdf | 53 | Accellera UVM Mixed-Signal Standard v1.0, Feb 2025 |
| P22 | papers/arxiv_2510_15906_fvdebug_llm_formal_rca.pdf | 28 | FVDebug (NVIDIA): LLM root-cause analysis of formal failures, DVCon US 2026 3rd best paper |
| P23 | papers/arxiv_2512_23189_agentic_eda_survey.pdf | 9 | Agentic EDA survey, L1-L4 autonomy taxonomy (2026) |
| P24 | papers/arxiv_2501_09655_llm_for_eda_survey.pdf | 21 | Survey of LLMs for EDA (Jan 2025) |
| P25 | papers/arxiv_2604_27013_bzl_riscv_vv_in_the_loop.pdf | 7 | BZL V&V-in-the-loop for RISC-V, holistic methodology (2026) |

NOTE: D8 and D36 are two DVCon editions of the same recurring Accellera CDC WG deck, NOT two
revisions of one document — D8 is the DVCon India 2025 edition (63 pp, Chalana/Soni/Vijai/Parashar),
D36 the DVCon U.S. 2026 edition (93 pp, Mills/Gascoyne/Choppali Sudarshan/Olopade/Gupta); the
archive holds a third at Europe 2024. Author lists do not overlap at all. Cite D36, never both.
NOTE: new 2026 industry data (first-silicon, effort) announced for DVCon India keynote Sept 1-3 2026 — re-check early Sept before freezing ch. 1/7 statistics; until then WRG 2024 [R1,R2] remains the latest published study.

## additions 2026-08-27 — protocol and ISA specifications (IDs are STABLE/append-only)

Until this block the corpus held no protocol specification and no ISA specification: all of
S1-S13 are language and methodology standards. Every AXI, RISC-V and cache-coherence claim in
the book was therefore unauditable. These eight close that gap. Acquisition audit, with the
official source URL, page count, MD5 and printed licence terms of each file:
`meta/audits/spec_acquisition.md`.

| ID | file | pages | note |
|---|---|---|---|
| S14 | standards/riscv_isa_unprivileged_20250508.pdf | 727 | RISC-V ISA Manual Vol I Unprivileged, Version 20250508, printed state "ratified". CC-BY-4.0 |
| S15 | standards/riscv_isa_privileged_20250508.pdf | 221 | RISC-V ISA Manual Vol II Privileged, Version 20250508, printed state "Ratified" — privilege levels, CSR map, traps. CC-BY-4.0 |
| S16 | standards/riscv_debug_spec_v1_0_20250221.pdf | 119 | RISC-V Debug Specification v1.0, revised 2025-02-21, Ratified — Debug Module, DMI, triggers. CC-BY-4.0 |
| S17 | standards/arm_ihi0022_issue_l_amba_axi_2025.pdf | 320 | AMBA AXI, ARM IHI 0022 Issue L, 27 Aug 2025, Released, Non-confidential. AXI5 / AXI5-Lite / ACE5-Lite ONLY |
| S18 | standards/arm_ihi0022_issue_hc_amba_axi_ace_2021.pdf | 500 | AMBA AXI and ACE, ARM IHI 0022H.c, 26 Jan 2021, Non-Confidential. Last issue specifying AXI3 / AXI4 / AXI4-Lite / ACE / ACE-Lite |
| S19 | standards/arm_ihi0024_issue_e_amba_apb_2023.pdf | 48 | AMBA APB, ARM IHI 0024 Issue E, 28 Feb 2023, Non-Confidential. APB5 |
| S20 | standards/arm_ihi0033_issue_c_amba_ahb_2021.pdf | 104 | AMBA AHB, ARM IHI 0033 Issue C, 15 Sep 2021, Non-confidential. AHB5 |
| S21 | standards/usb_if_usb_3_2_revision_1_1_2022.pdf | 569 | Universal Serial Bus 3.2 Specification, Revision 1.1, June 2022, USB 3.0 Promoter Group |

NOTE: S17 and S18 are two SCOPES of ARM IHI 0022, not two revisions of one. Issue J (01 Mar
2023) removed AXI3, AXI4, AXI4-Lite, ACE and ACE5 from the document; Issue L, which supersedes
it, specifies only AXI5, AXI5-Lite, ACE5-Lite, ACE5-LiteDVM and ACE5-LiteACP. The book's
running example is an AXI4 crossbar, so **AXI4 and ACE claims cite S18; AXI5 and ACE5-Lite
claims cite S17.** Citing S17 for an AXI4 rule is a false citation — the text is not in it.
Both print the 4 KB burst-boundary constraint, S18 as "A burst must not cross a 4KB address
boundary." and S17 as "A transaction must not cross a 4KB address boundary." The ARM issue
letters are newest-evidenced, not confirmed-current: they were read from each document's own
release table, which cannot list a successor, and ARM's documentation site exposes no version
list to check against. Re-check before freezing — see `meta/audits/spec_acquisition.md`.

NOTE: cache coherence is now auditable, but only in ACE terms. S18 chapters D1-D5 specify the
ACE five-state cache model — UniqueClean, UniqueDirty, SharedClean, SharedDirty and Invalid —
with per-state rules and a Snoop Transactions chapter, so coherent-transaction and cache-state
claims have a real authority. What S18 does NOT do is specify MESI, ESI, MEI or MOESI: it names
them once, as protocols an ACE system can interoperate with, and no more. A textbook MESI or
MOESI state machine therefore still has no corpus authority, and neither does ARM CHI
(IHI 0050), the current authority for full hardware coherency, which was not acquired. Cite S18
for ACE states and snoops; cite nothing in this corpus for MESI/MOESI as such, or for CHI.

## additions 2026-09-02 — the open-source layer (IDs are STABLE/append-only)

Acquisition audit, with pinned commit SHAs, licences, MD5 and null results:
`meta/research/acquisition_20260902.md`. New class **O** = open project documentation
(GitHub markdown / rst / xlsx), admitted by `tools/references.py` and `tools/chapter.py`
without any code change.

| ID | file | pages | note |
|---|---|---|---|
| O1 | open/openhw/VerificationPlanning101.md |  | 14 427 B. OpenHW "How to Write a Verification Plan (Testplan)". core-v-verif @ f3b1f97. Solderpad 2.0 |
| O2 | open/openhw/VerifStrat_planning_requirements.rst |  | 1 645 B. CORE-V Verification Strategy, ch. "Verification Planning and Requirements". Thin — cite only for the strategy/vplan distinction |
| O3 | open/openhw/CodingStyleGuidelines.md |  | 51 819 B. CORE-V-VERIF coding style guidelines |
| O4 | open/openhw/CV32E40P_interrupts_vplan.xlsx |  | 3 sheets / 105 rows. A real filled CV32E40P interrupt vplan. NOT a PDF — no page count |
| O5 | open/openhw/CV32E40Pv2_waiver_list.xlsx |  | 8 sheets / 1 573 rows. CV32E40Pv2 RTL v1.8.3 waiver list, each waiver with a written reason |
| O6 | open/openhw/CV32E40Pv2_uncovered_coverage_explanation.xlsx |  | 2 sheets / 27 rows. Uncovered coverage with Cause, Future Action and a Risk (no/low/medium/high) column |
| O7 | open/openhw/OpenHWGroup_TRL5_checklist_CV32E40P.xlsx |  | 9 sheets / 9 008 rows. TRL-5 sign-off checklist: Category / Item / Sign-off Criteria / Exceptions-Waivers |
| O8 | open/opentitan/dv_methodology.md |  | 46 381 B. Design Verification Methodology within OpenTitan. opentitan @ 4e5c99d. Apache-2.0 |
| O9 | open/opentitan/DVCodingStyle.md |  | 55 843 B. lowRISC SystemVerilog DV Coding Style Guide. style-guides @ 9c15ff5. CC-BY-4.0 |
| O10 | open/opentitan/project_governance_checklist.md |  | 30 023 B. OpenTitan Signoff Checklist — generic D/V/S stage items |
| O11 | open/opentitan/development_stages.md |  | 23 352 B. OpenTitan Hardware Development Stages |
| O12 | open/opentitan/hw_ip_aes_checklist.md |  | 20 205 B. AES Checklist — one filled instance of O10 |
| O13 | open/opentitan/sec_cm_dv_framework.md |  | 9 338 B. Security Countermeasure Verification Framework |
| O14 | open/opentitan/security_impl_guidelines_hardware.md |  | 23 577 B. Secure Hardware Design Guidelines |
| O15 | open/opentitan/threat_model.md |  | 3 546 B. Lightweight Threat Model — scoping, not depth |
| S22 | standards/accellera_scemi_v24_2016.pdf | 199 | SCE-MI Reference Manual v2.4, November 2016, Accellera. Open download |
| S23 | standards/accellera_sa_edi_v10_2021.pdf | 44 | Accellera SA-EDI Standard Rev 1.0, July 2021. Open download |
| S24 | standards/arm_ihi0050d_amba5_chi_2019.pdf | 412 | AMBA 5 CHI Architecture Specification, ARM IHI 0050D (ID082919), Non-Confidential. Issue D, NOT current — G and H exist and were not obtainable |
| D37 | dvcon/dvcon_us2017_fp_sequential_equivalence_checking.pdf | 13 | Pouarz, Agrawal, DVCon US 2017, Paper — sequential equivalence checking on a floating-point datapath |
| D38 | dvcon/dvcon_india2019_bringing_datapath_formal_to_designers.pdf | 5 | Achutha KiranKumar V et al., DVCon India 2019, Paper — datapath formal (C vs RTL) at Intel |
| D39 | dvcon/dvcon_india2019_automation_of_waiver_and_design_collateral.pdf | 6 | Sridhar et al., DVCon India 2019, Paper — waiver and design-collateral automation |
| D40 | dvcon/dvcon_europe2023_testbench_linting_open_source_way.pdf | 9 | Venkataramanan et al., DVCon Europe 2023, Paper — testbench linting with slang/pyslang/PySlint |
| D41 | dvcon/dvcon_us2015_versatile_uvm_scoreboarding.pdf | 11 | Andersen, Jensen, Steffensen (SyoSil), DVCon US 2015, Paper — scoreboard architecture |
| D42 | dvcon/dvcon_taiwan2023_uvm_scoreboards_checkers_memory_tlb_cache.pdf | 28 | Edelman, Liu (Siemens EDA), DVCon Taiwan 2023 — scoreboards and checkers for memory, TLB, cache. **A slide deck, not a paper**: 960x540 pts landscape, 36 words/page. The archive record mislabels it `Paper` — cite it as a presentation |
| D43 | dvcon/dvcon_us2016_analysis_of_tlm_2_0_non_memory_mapped.pdf | 12 | Delbergue, Burton, Le Gal, Jego, DVCon US 2016, Paper — the corpus's only TLM-2.0 authority (IEEE 1666 is not held) |
| D44 | dvcon/dvcon_us2018_optimal_regression_farm_infrastructure.pdf | 13 | Lacey, Powell, DVCon US 2018, Paper — regression-farm sizing, the compute-economics side |
| D45 | dvcon/dvcon_us2025_gray_box_reachability_regression_scheduling.pdf | 9 | Ferretti et al., DVCon US 2025, Paper — reachability predictor for regression scheduling. Carries a residual MSIP "Confidential" Word label; published openly by Accellera — see the audit |
| P26 | papers/arxiv_2105_09169_pdr_proof_obligation_generalization.pdf | 16 | Seufert et al., IEEE TCAD 42(4):1351-1364, April 2023, DOI 10.1109/TCAD.2022.3198260. Year is 2023, NOT the arXiv 2105 identifier's 2021 |
| P27 | papers/arxiv_2410_15908_formalising_cxl_cache_coherence.pdf | 14 | Tan, Donaldson, Wickerson, ASPLOS 2025, pp. 437-450, DOI 10.1145/3676641.3715999. Year is 2025, NOT 2024. CXL coherence — does NOT close the CHI gap |

NOTE: the `pages` column is deliberately EMPTY for O1-O15, and this is a parser constraint rather
than a style choice. `tools/references.py:196-198` reads the cell as a string and appends a
hard-coded suffix — `if pages: parts.append(f"{pages} pp.")` — so a cell reading `3 sheets / 105
rows` would render as "3 sheets / 105 rows pp." in the citation string a reader sees whenever an ID
has no `references.md` entry. The size measure therefore lives in the note column. The nineteen PDF
rows keep a real integer page count.

NOTE: DVCon PDF CreationDate contradicts the conference year in 3 of the 9 files registered here
(D37, D44, D45): camera-ready precedes a February conference. The authority for year, venue, author
list is the archive record at dvcon-proceedings.org/document/<slug>/, never pdfinfo. Slugs are in
meta/research/acquisition_20260902.md §5. For paper-vs-presentation the archive is NOT authoritative
either: it labels all nine `Paper`, but D42 is a 960x540 landscape deck. Page geometry decides —
`pdfinfo | grep "Page size"`; page count does not (D42's 28 pp. is inside paper range, and the
corpus's real decks run to 79 pp.).

NOTE: openhwgroup/core-v-docs no longer exists under that name — the GitHub API 301-redirects it to
openhwgroup/programs (repo id 224904153). O5-O7 are pinned there; O1-O4 in openhwgroup/core-v-verif.
Any citation naming `core-v-docs` is naming a redirect.

NOTE — this supersedes one clause of the 2026-08-27 cache-coherence note above. That note ends
"cite nothing in this corpus for MESI/MOESI as such, or for CHI." The **CHI half is now false**:
S24, ARM IHI 0050D, 412 pp., is in the corpus, and its cache-state model — Valid/Invalid ×
Unique/Shared × Clean/Dirty × Full/Partial/Empty, seven states, per-state rules at *Cache line
states*, p. 4-142 — gives CHI claims an authority. The standing caveat is that **Issue D (2019) is
not the current issue**: Issues G and H exist and were not obtainable, so S24 is
newest-evidenced-obtainable, the same status the corpus assigns S17-S20. The **MESI/MOESI half stays
true, for the same reason as S18**: S24 names MESI and MOESI exactly once each, in a feature list
("Both MESI and MOESI cache models with forwarding of data from any cache state"), and specifies
neither. Cite S24 for CHI's own state names, never for a textbook MESI/MOESI state machine.
Routing detail: `meta/research/anchors_normative.md` §1.1 and §4.10.

NOTE: IEEE 1497-2001 is Inactive-Reserved and NOT in the IEEE GET programme, so it cannot enter this
corpus for free; it stays nominated without a clause. IEEE's own record for it
(`https://standards.ieee.org/ieee/1497/2235/`) prints that IEC 61523-3:2004 replaces it and is now
where SDF is defined — a correction ch19 and appendix_c can make from the publisher's own record,
with no new source. IEC 61523-3 is itself NOT held: it may be named, never `[cit:]`.
`meta/research/anchors_normative.md` §4.11 carries the recommended wording.

## Additions 2026-09-03 (author downloads, W1b) — IDs are STABLE/append-only

Nine documents the author downloaded himself, from the list handed to him as
`meta/DA_SCARICARE_2.md`. Every identity below was verified against the artifact's own front
matter, and every page number quoted anywhere for these IDs was opened with `pdftotext -f N -l N`.
Acquisition audit, with MD5, per-document page findings and the falsified claims elsewhere in the
repo: `meta/research/acquisition_20260903.md`.

| ID | file | pages | note |
|---|---|---|---|
| R3 | reports/wrg_2020_ic_asic_trend_report.pdf | 13 | MD5 `364d946465c2a80370c038f25eac532d`. 2020 Wilson Research Group IC/ASIC functional verification trend report, Harry Foster, Siemens EDA. Study year **2020**; the PDF is a 22 Oct 2021 re-export (`Subject` prints "v10.22.21") — cite the study year. Downloaded by the author from Siemens Verification Academy, registered account |
| R4 | reports/wrg_2020_fpga_trend_report.pdf | 13 | MD5 `5f0743a90468ce88b0deb076764a61fd`. 2020 WRG FPGA trend report, Harry Foster, Siemens EDA (the PDF `Author` field misspells it "Seimens"). Same study and same sample as R3, n=1492. Downloaded by the author from Siemens Verification Academy, registered account |
| R5 | reports/wrg_2022_ic_asic_trend_report.pdf | 26 | MD5 `a7005e81f15b85ad0bd1b137901bf42f`. *White Paper — 2022 Wilson Research Group IC/ASIC functional verification trends*, Siemens EDA, 2022. A **white paper**, 26 pp., not the 13-pp. report layout of R1-R4. Downloaded by the author from Siemens Verification Academy, registered account |
| R6 | reports/wrg_2022_fpga_trend_report.pdf | 26 | MD5 `457860ae3959dfbfdd004cf6488625ea`. *White Paper — 2022 Wilson Research Group FPGA functional verification trends*, Siemens EDA, 2022. Same study and sample as R5, n=980. Downloaded by the author from Siemens Verification Academy, registered account |
| B7 | books/siemens_va_coverage_cookbook_2013.pdf | 95 | MD5 `573ae3c26b45e2f332da152038047aae`. *Coverage Cookbook*, Verification Methodology Team, Mentor Graphics / Siemens EDA Verification Academy. **Two dates, both in the file**: `CreationDate` 21 Aug 2013 and `ModDate` 26 Apr 2019, and the `Subject` field prints "Verification Academy - Coverage Cookbook (**April 26, 2019**)". Cite year 2013 (creation), with 2019 as the revision the document names for itself. **Printed page = PDF page**, no offset. Downloaded by the author from Siemens Verification Academy, registered account |
| B8 | books/siemens_va_uvm_cookbook_2021.pdf | 547 | MD5 `e97599d3f5d556199f3d3f5fd03e1fd5`. *UVM Cookbook*, Functional Verification Methodology Team, Siemens EDA Verification Academy. Same two-date shape as B7: `CreationDate` 9 Sep 2021, `ModDate` 31 Jan 2022, `Subject` "(1.31.2022)". Cite year 2021. ⚠️ **Page offset +6**: `PDF page = printed page + 6` (verified at `-f 119`, `-f 120`, `-f 371`), and the book's own contents list the *printed* numbers. Downloaded by the author from Siemens Verification Academy, registered account |
| S25 | standards/ieee_1666_2023_systemc_lrm.pdf | 618 | MD5 `f636aa213c91d0aa61f3bcfd4620d7f6`. IEEE Std 1666-2023, *IEEE Standard for Standard SystemC Language Reference Manual*, Design Automation Standards Committee, IEEE Computer Society. Title page prints "**(Revision of IEEE Std 1666-2011)**" and "**Approved 5 June 2023**, IEEE SA Standards Board". Contains **TLM-2.0** (Clauses 9-16). ⚠️ **Page offset +2**: `PDF page = printed page + 2`. **Provenance as the artifact prints it, on every page**: "Authorized licensed use limited to: Politecnico di Milano. Downloaded on September 03,2026 at 10:13:52 UTC from **IEEE Xplore**. Restrictions apply." — an institutional Xplore download under the author's access, **not** an IEEE GET download, although 1666-2023 is in the GET list. Citable; **not redistributable** |
| S26 | standards/arm_ihi0050h_amba5_chi_2025.pdf | 716 | MD5 `6d9f67974982ff3b0b10ee5f8be56f2b`. *AMBA CHI Architecture Specification*, Arm Limited. Cover prints `Document number ARM IHI 0050` / `Document quality Released` / `Document version **Issue H**` / `Document confidentiality **Non-confidential**` / `Date of issue **17 Sep 2025**`. **Printed page = PDF page**, plain arabic — **not** the chapter-prefixed form S24 uses. Downloaded by the author from the Arm developer site in his own browser |
| D46 | dvcon/dvcon_europe2024_who_checks_the_checkers_c_to_rtl_equivalence.pdf | 6 | MD5 `29fa420efaecb4bf7fae1093885e37fe`. Pardalos, Donaldson, Morini, Pozzi, Wickerson, "Who checks the checkers? Automatically finding bugs in C-to-RTL formal equivalence checkers", **DVCon Europe 2024**, Munich, 15-16 Oct 2024, Paper. Affiliations are printed on p. 1: Imperial College London, Intel, Università della Svizzera italiana. Same Xplore stamp as S25 ("Politecnico di Milano … Downloaded on … from IEEE Xplore"), so the held copy came from **IEEE Xplore, author's institutional access**, not from the open DVCon archive |

**Note 2026-09-03 — S26 supersedes S24 for currency; S24 is kept, not replaced.** This supersedes
the standing clause in the 2026-09-02 note above that reads "**Issue D (2019) is not the current
issue**: Issues G and H exist and were not obtainable". Issue H *was* obtained: S26, ARM IHI 0050
Issue H, 17 Sep 2025, 716 pp. **CHI claims about the current issue cite S26.** S24 stays in the
corpus as the 2019 edition and stays citable *as that edition* — it is the right citation for a
statement about what Issue D said, and nothing else. Two facts read from S26 itself:
- The *Release information* table (p. 2) is a real change history and lists eleven public
  releases, D being the third (28 Aug 2019) and H the eleventh (17 Sep 2025) — **eight public
  releases apart**. The table's `Changes` column records **only the release ordinal**, never a
  content delta, so **no claim about what changed between D and H may be made from this document.**
- The MESI/MOESI caveat carried by the 2026-08-27 note and by `anchors_normative.md` §1.6 was
  **re-measured on Issue H and holds**: across all 716 pages, `MESI` occurs **once** and `MOESI`
  occurs **once**, in the same feature bullet on **p. 29** — "Both MESI and MOESI cache models
  with forwarding of data from any cache state." Neither is specified. Cite S26 for CHI's own
  seven-state model (B1.5.2, pp. 39-40; per-state rules at B4.1 *Cache line states*, p. 192),
  never for a textbook MESI/MOESI state machine.

**Note 2026-09-03 — the corpus now holds IEEE 1666, which falsifies the D43 row above.** The D43
row calls D43 "the corpus's only TLM-2.0 authority (**IEEE 1666 is not held**)". The parenthesis is
now false: **S25 is IEEE Std 1666-2023 and contains TLM-2.0.** D43's own value is unchanged and is
narrower than the row implied — it is a *published analysis* of where TLM-2.0's interoperability
guarantee stops, which the standard does not say about itself. Normative TLM-2.0 claims (generic
payload, base protocol, blocking and non-blocking transport, loosely-timed and approximately-timed
coding styles, sockets, the interoperability layer) now cite **S25 with a clause number**; D43 stays
the citation for the limits argument. Routing: `meta/research/anchors_normative.md` §1.7.

**Note 2026-09-03 — WRG 2016 and 2018 were not obtained, and what the series therefore is.** The
author retrieved what was reachable; the 2016 and 2018 editions were not. `meta/DA_SCARICARE_2.md`
says that with 2016, 2018, 2020 and 2022 the trends would have "**cinque punti datati**". That
sentence is now superseded by the outcome: the corpus holds **three editions of the report series —
2020 (R3/R4), 2022 (R5/R6) and 2024 (R1/R2) — plus the 2014 study point in P17**
(`papers/foster_dac2015_trends.pdf`, registered and cited as IND-36). Write it that way: *three
editions plus the 2014 point*, never "five dated points". ⚠️ And note what does **not** form a
series: the verification-engineer demand **CAGR** is quoted on a different window in every edition
(R3 p. 6 gives 2007-2020; R5 p. 10 gives 2007-2014; R2 pp. 6-7 gives 2007-2016 *and* 2016-2024), so
those percentages are not comparable across editions. Detail in `anchors_industrial.md` IND-59.

**Note 2026-09-03 — counts in the header paragraph of this file are a dated measurement and are
now stale.** The measurement dated 2026-09-02 near the top reads "**92** rows here … **84** entries
in `references.md` `## Entries` … and **3** in its `## Held, not cited`". It was already superseded
before this block: `meta/references.md` records that as of 2026-09-02 this file held **121 rows**
and that file held **33** held-not-cited lines. After the 2026-09-03 anchoring pass and this block,
the state is **130 rows here** and **15** lines under `## Held, not cited`. The header paragraph is
left as written because this file is append-only and its sentence carries its own date; this note
is the current figure.

**Note 2026-09-03 on D4 (author decision).** The D4 row (`dvcon/P18-DVConIndia25_Final_PPT_5976.pdf`) records, correctly, that the poster prints no author affiliation. On 2026-09-03 the author decided to attribute the work to **Samsung** on the strength of dvcon-india.org's own 2025 award page (identification basis in `meta/references.md` "Provenance notes", D4 row); ch19 and IND-27 say so from that date. The row is left as written because it describes the document, and the document has not changed.
