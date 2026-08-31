# Example Bank — the running example system and the supporting cast

This file defines the concrete systems used for examples throughout the book.
Every writer MUST use these, with these exact parameters, so examples stay
consistent across chapters.

## Golden rules (NON-NEGOTIABLE)

1. **Never name real internal IPs or their origin.** The words *PULP, PULPissimo,
   CV32E40P, CVA6, iDMA, uDMA, axi_xbar, NE16, FlooNoC, ChipsIT, ETH Zürich* must
   NOT appear anywhere in the book. The systems below are technically faithful but
   anonymous. Public literature (OpenTitan, lowRISC, Arm/Intel published papers,
   IBM POWER4) MAY be cited normally — the ban covers only the internal/PULP family.
2. **Every central concept gets a concrete scenario.** The reader must repeatedly
   see the pattern: *"In this scenario → you use this technique → because…"*.
   Abstract explanation alone is never enough.
3. **Same parameters everywhere.** If chapter 5 says the crossbar has 5 managers,
   chapter 14 must too. The canonical parameters are below; do not invent variants.
4. **Generic but deeply real.** Examples must feel like they come from someone who
   has actually verified these blocks: real signals, real corner cases, real bugs.
5. **Names are scoped to a generation.** Bare *the core, the crossbar, the DMA
   engine, the memory, clocking, power, debug* ALWAYS mean the reference SoC's —
   chapters 1, 3, 4 and 6 pin those parameters (2 DMA channels, 512 KB SRAM,
   5×4 crossbar, 3 clock domains, 2 power domains). Second-generation elements are
   ALWAYS qualified: *the flagship's DMA, the LPDDR4 subsystem, the host cluster,
   the flagship's clocking*. Never reuse a first-generation name for a
   second-generation part.

## The reference SoC (primary cast — used in most chapters)

A microcontroller-class, single-core RISC-V SoC for low-power edge applications.
Introduce it in ch. 1 front matter as "the reference SoC used throughout this book".

| Element | Canonical description | Canonical parameters |
|---|---|---|
| **the core** | 4-stage, in-order, single-issue RV32IMC core with optional custom DSP/SIMD extensions | ~50k gates; OBI-like instr/data interfaces; M/U modes; CLINT-style interrupts + fast IRQ extension |
| **the crossbar** | full AXI4 crossbar interconnect | 5 managers (core-I, core-D, DMA×2, debug) × 4 subordinates (SRAM, boot ROM, APB bridge, neural accelerator); 32-bit address, 64-bit data; ID width 4 |
| **the DMA engine** | modular multi-channel DMA with decoupled frontend (register IF), midend (transfer legalizer/splitter) and backend (AXI4 manager) | 2 channels; 1D/2D transfers; max burst 256 beats; 16-entry × 64-bit datapath FIFO in the backend; per-channel error reporting |
| **the I/O subsystem** | autonomous I/O engine moving data between peripherals and memory without core intervention | dedicated lightweight DMA per peripheral; UART, SPI, I2S, camera interface |
| **the neural accelerator** | fixed-point convolution engine for quantized neural networks | configurable 2/4/8-bit weights; 16-lane MAC datapath; streams weights from memory; register-programmed jobs |
| **the memory** | multi-banked tightly-coupled SRAM, word-interleaved, single-cycle | 512 KB in 4 banks; logarithmic interconnect toward core/DMA |
| **the peripherals** | APB subsystem | UART, SPI, I²C, GPIO, timer, event/interrupt unit |
| **clocking** | 3 domains | system @ 200 MHz, peripheral @ 50 MHz, always-on RTC @ 32 kHz → CDC examples |
| **power** | 2 UPF power domains | always-on (RTC, wake-up logic) + switchable **system** domain (core, memory, peripherals, accelerator); retention on event unit → low-power examples. **Never call this a "compute" domain** — that name belongs to the flagship's compute island, and ch19 contrasts the two generations side by side, where the collision would read as the same block at two scales. It is also inaccurate: the domain holds the whole system, not just the compute |
| **debug** | RISC-V debug module over JTAG | run-control + abstract memory access |

*Port index map (pin this — chapters index these ports).* Crossbar manager ports
0-4 = core-I, core-D, DMA channel 0, DMA channel 1, debug; subordinate ports 0-3 =
SRAM, boot ROM, APB bridge, neural accelerator. This is the manager order of the
row above, read as indices; any chapter writing `mgr_seqr[n]`, `sub_seqr[n]` or
"manager port n" must agree with it.

Typical example seams this SoC offers (use them!):
- protocol verification on the crossbar (AXI handshakes, ordering, ID routing)
- data-mover verification on the DMA (address legalization, 4 KB boundary, error responses, descriptor corner cases)
- control/status register verification everywhere (RAL-style)
- ISA/core verification on the core (privileged state, interrupts, custom extensions → co-simulation with a golden ISS)
- accelerator verification on the neural engine (quantization corner cases, memory contention with the DMA)
- CDC between the three clock domains; UPF power sequencing between the two domains

## The flagship SoC (second generation — scale-up chapters)

**The family narrative — write it once, then just refer to it.** The reference SoC
and the flagship SoC are two generations of one fictional company's product line.
The flagship is the scale-up successor: it reuses the first generation's IP — the
DMA architecture, the register discipline, the peripheral set — and reuses the
*verification assets* that came with it. Vplans extend rather than restart (the
flagship's DMA plan is the reference SoC's plan plus the rows that eight channels
and a coherent memory system add), regression suites carry forward, and the
canonical bugs of the first generation have descendants in the second — which is
why "we already found that one" is a claim the second-generation team must earn,
not assume. The sharpest lineage line sits in the first generation's own plan:
chapter 4's out-of-scope row reads *"cache-coherent extensions (not implemented)"*.
The flagship implements them, so the reference SoC's last out-of-scope entry is the
flagship's first plan row.

**Which generation carries which chapter.** Fundamentals and block-level technique
(ch. 1-16) stay on the reference SoC — small enough to hold in your head is the
entire point. The flagship carries what only scale can teach: regression economics
(ch. 12), coherence and deadlock formal (ch. 14, 16), emulation (ch. 17), FPGA
prototyping and HW/SW co-verification (ch. 18), multi-domain power and DVFS (ch. 19,
alongside the reference SoC's two-domain teaching case), post-silicon bring-up and
observability (ch. 20), in-SoC security (ch. 23), and large-scale safety through the
flagship-A (ch. 22). Contrast pairs across the two generations — same problem, two
scales — are the preferred format for showing why technique choice changes with size.

| Element | Canonical description and parameters | Role in the flagship / seams |
|---|---|---|
| **the host cluster** | 4 × *the application core* (6-stage, single-issue RV64GC core with MMU, caches, running an OS); private 32 KB L1 I/D per core; shared 2 MB L2 in 4 slices; directory-based MESI across the four L1s; IO-coherent (snoop-in only) ports for the accelerators and the DMA | the host: boots and runs the OS. Coherence protocol → formal (ch. 14, 16); HW/SW co-verification (ch. 18) |
| **the compute cluster** | 8 identical RV32 cores sharing the multi-banked TCDM through a single-cycle logarithmic interconnect, HW synchronizer, cluster DMA | accelerator island behind an IO-coherent port; regression scale, coverage closure, performance verification |
| **the mesh NoC** | 4×4 mesh network-on-chip; wide 512-bit channels for burst data + narrow 64-bit channels for control; virtual channels; XY routing; end-to-end ordering guarantees | the system interconnect; interconnect verification at scale, emulation, formal deadlock examples |
| **the LPDDR4 subsystem** | LPDDR4 controller + PHY; one 32-bit LPDDR4-3200 channel; out-of-order per-bank scheduling; PHY training state machine | main memory; GLS/timing, emulation, performance, AMS boundary at the PHY (ch. 19, 21) |
| **the root of trust** | secure boot ROM, OTP key fuses, TRNG, inline AES-GCM on the memory path (the extended cast's crypto engine, instantiated in-SoC); measured boot; authenticated debug unlock | ch. 23 in-SoC security: threat model over real traffic, key isolation, debug unlock as an attack surface |
| **the DfD infrastructure** | per-core processor trace, 8 bus monitors with programmable trigger/capture into a 64 KB on-chip trace buffer, JTAG-reachable debug fabric with one debug access port per power domain | ch. 20 post-silicon observability; ch. 17 what an emulator sees that silicon cannot |
| **the flagship's DMA** | 8 channels; same frontend / midend / backend architecture and the same 4 KB legalization discipline as the reference SoC's DMA engine; 40-bit physical addressing; **512-bit data path** — the same width as the NoC's wide burst-data channels, pinned here from ch17's transactor artifact, whose code declares `DATA_W = 512` and whose prose says "512-bit channel" and "512-bit beat" (the reference SoC's DMA engine stays on the 64-bit path); descriptor chaining. *Any chapter turning this width into bytes per burst must state the beat count it used and check the product against the 4 KB rule.* | inherits the reference SoC's verification plan and its canonical bugs' descendants; new seam: a DMA write that must invalidate a line the host cluster holds Modified |
| **the flagship's clocking** | 5 asynchronous domains (host cluster, compute island, NoC, LPDDR PHY, always-on); DVFS with 3 operating points on host cluster and compute island — **0.6 / 1.1 / 1.5 GHz**; NoC at 800 MHz; always-on at 32 kHz (as on the reference SoC, whose system domain runs at 200 MHz) | CDC at scale, DVFS transitions (ch. 13, 19) |
| **the flagship's power intent** | 6 UPF power domains (always-on, root of trust, host cluster, compute island, NoC + memory, peripherals); retention on the L2 slices; power-gated compute island | ch. 19 UPF sequencing at scale, contrasted with the reference SoC's two domains |
| **the flagship-A** | automotive derivative: dual-core delayed-lockstep safety island, SECDED ECC on L2, LPDDR and TCDM, monitored reset and clock; ASIL-D safety island inside an ASIL-B system | ch. 22 large-scale safety: FMEDA over a full SoC, fault campaigns on a lockstep pair |

*Lineage of the missing elements.* The flagship has no crossbar row: the crossbar's
verification story scales into the NoC's, and the crossbar itself stays a
first-generation, block-level example. The DMA is the explicit reuse case — same
three-stage architecture, same 4 KB discipline, eight channels instead of two. The
neural accelerator returns too, scaled and sitting behind its own IO-coherent port:
same quantization corner cases, now contending with a coherent DMA instead of a
crossbar — which is what "the accelerators" in the host cluster row means (the
compute cluster and the neural accelerator).

*Absorption is additive.* The compute cluster, the mesh NoC and **the application
core** (still the name for the RV64GC core itself, still carrying HW/SW
co-verification and hybrid platforms) keep every standalone use they already have —
chapter 6 shapes coverage crosses on the cluster's 8-core interconnect; the NoC's
deadlock is a block-level formal example.
They are now *also* the flagship's subsystems. Standalone framing for block-level
technique, flagship framing for system-level.

The same licence extends, narrowly, to two lightweight IPs that chapters
*instantiate* rather than merely cite. **The video codec** keeps every standalone
use it has — chapter 14 splits it down the middle for formal, chapters 8 and 24
hang the bit-exact golden model on it — and is *also* a flagship media subsystem,
which is what licenses *the flagship's video codec* in chapter 20. **The sensor
hub** keeps its standalone always-on-island framing everywhere it appears, and is
*also* deliverable as a block integrated into the reference SoC's always-on domain,
which is what chapter 24's partner-delivery scenario needs. So absorption runs in
both generations: qualify a second-generation instantiation (*the flagship's* video
codec) and let a bare name mean the reference SoC's, exactly as golden rule 5
already requires. These two are the whole extension: the crypto engine's in-SoC
role is already recorded in its own row, and any *further* in-SoC role for an
extended-cast entry needs a line here before a chapter may assume it.

*The flagship-A does not break golden rule 3.* It is a separate named product with
its own fixed parameters, not an alternative parameterization of the flagship.
Nobody may write "the flagship, in its ECC configuration".

## Supporting cast (specialized chapters — "all the other cases")

| Element | Description | Used in |
|---|---|---|
| **the brake controller MCU** | automotive ASIL-D lockstep MCU with ECC memories and safety island | ch. 22 safety, **small-scale**: FMEDA on a part you can enumerate, fault injection (kept — chapter 1 names it; the flagship-A is the large-scale counterpart) |
| **the secure element** | boot ROM + AES/SHA engines + key vault + TRNG | ch. 23 security, **discrete part**: threat model, info flow, side channels (the flagship's root of trust is the in-SoC counterpart) |
| **the PCIe endpoint** | Gen4 ×4 endpoint with DMA bridge | emulation/ICE, protocol compliance at scale |
| **the SerDes** | 112G PAM4 transceiver | GLS + AMS boundary, lab bring-up |
| **the analog front-end** | 12-bit SAR ADC + PLL + temperature sensor | ch. 21 AMS (RNM, co-simulation). **It sits on the reference SoC**, its register interface in the peripheral domain the digital team owns — the placement that the ADC reference voltage in "Canonical numbers" (labelled a *reference SoC* number) and ch21's own "the reference SoC's PLL" both already assume. It is in the supporting cast because ch21 is the only chapter that calls it in, not because it is off-die: ch01 lists it among the parts specialized chapters call in, and that stays true. **There is no third product** — never write "the reference SoC's next revision" or otherwise date the front-end into a later revision |
| **the chiplet package** | 2.5D two-die system with die-to-die link | post-silicon, system-level examples |
| **a server-class OoO core** | wide out-of-order superscalar (contrast case) | to show how verification scales with complexity (cite POWER4 literature for the industrial reference) |

*Merged:* the former standalone "DDR subsystem" row is now the flagship's LPDDR4
subsystem — use that for controller/PHY examples. The HBM controller (extended cast)
remains the separate high-bandwidth-memory case.

## Extended cast (variety pool — author requirement: 2-3 non-backbone examples per chapter)

Lightweight IPs to diversify examples beyond the reference SoC. Keep parameters
consistent once used; add new entries here if an IP recurs across chapters.

| Element | Description | Example seams |
|---|---|---|
| **the GPU** | tile-based mobile GPU, 4 shader clusters, unified memory | massive-parallelism coverage, long-latency pipelines, memory-ordering bugs |
| **the video codec** | H.265-class encoder/decoder, line buffers, DDR traffic bursts | data-dependent control flow, golden-model (bit-exact reference) checking |
| **the Ethernet MAC** | 10G MAC with TSN (time-sensitive networking) queues | protocol compliance, timestamp precision, QoS arbitration corner cases |
| **the crypto engine** | inline AES-GCM on the memory path + key ladder | security properties, constant-time behavior, negative testing (the flagship's inline memory encryption is this IP instantiated in-SoC) |
| **the HBM controller** | HBM3 controller + PHY training state machine | initialization sequences, refresh/thermal corner cases, GLS |
| **the coherent hub** | directory-based cache-coherent interconnect (MESI) | protocol state explosion → formal, livelock/starvation, witness coverage. **Kept as the standalone-IP framing** — chapters 3 and 6 already use it that way; the flagship's L2 is the same protocol family in-SoC, and the hub's "two caches, one address" abstraction is the canonical proof abstraction for both |
| **the USB controller** | USB 3.x dual-role device/host controller | spec-mandated compliance suites, power states (U0-U3), CDC |
| **the flash controller** | NAND controller with LDPC ECC pipeline | error-injection verification, data-integrity oracles, performance under wear |
| **the sensor hub** | always-on sensor-fusion block, 32 kHz island + DSP | ultra-low-power modes, retention, asynchronous wake events. **Its safety derivative** (ch22) is the hub plus one added mechanism — a clock monitor watching the system clock against the always-on reference — and obeys the flagship-A discipline stated above: a derivative with its own fixed content, never an alternative parameterization, so nobody may write "the sensor hub, in its monitored configuration". For the hub as a block integrated in-SoC, see *Absorption is additive* above |
| **the radar front-end** | FMCW radar DSP chain (FFT pipelines, CFAR) | fixed-point precision verification, throughput corner cases, AMS boundary |

## Example formats (pick per situation)

1. **Scenario box** (most common): *Scenario* (2-4 lines of concrete situation on a
   cast element) → *Approach* (what a competent team does) → *Why* (the rationale,
   with trade-offs). Use markdown blockquote with bold labels.
2. **Worked example** (1-2 per chapter): longer walk-through with actual artifacts —
   a coverpoint sketch, an SVA property, a vplan row, a bug report — on the cast.
3. **War story** (sparingly): a realistic bug narrative (e.g., "a 2D transfer whose
   inner stride crossed the 4 KB boundary only when…"). Must be plausible and
   pedagogical, presented as illustrative, never as a cited fact.
4. **Contrast pair**: same problem on the reference SoC vs the server-class core or
   the NoC — shows how technique choice scales.

## Canonical artifacts (copy VERBATIM — never re-derive from memory)

Recurring code artifacts drift when re-derived: chapter 3 once reproduced the 4 KB
property without the fixes chapter 2's review had imposed. Any chapter reusing an
artifact below MUST copy this exact text (adaptation allowed only in surrounding
prose). Reviewers: grep other chapters for these names and diff against this file.

The 4 KB-boundary property (post-review canonical version — the INCR qualifier and
the 16-bit arithmetic are load-bearing: without them the property false-fires on
FIXED/WRAP bursts and silently PASSES illegal awsize>3 bursts that wrap modulo 2^13):

```systemverilog
property p_no_4kb_crossing;
  @(posedge clk) disable iff (!rst_n)
  (awvalid && awready && (awburst == 2'b01)) |->
    (16'(awaddr[11:0]) + ((16'(awlen) + 16'd1) << awsize)) <= 16'd4096;
endproperty
a_no_4kb_crossing : assert property (p_no_4kb_crossing);
```

The DMA 2D/4 KB coverage model — **the canonical coverage model for this feature**,
promoted verbatim from chapter 5, where it is named as the closure metric of vplan
row `DMA-F06a`. Any chapter modelling coverage of 2D legalization at the 4 KB
boundary MUST use these axes and bin names. Per-axis bin counts: `cp_stride_sign`
3 · `cp_boundary_dist` 4 · `cp_len` 3 · `cp_other_ch` 2 (one-bit flag, automatic
bins) → the cross `x_worst` has **72** combinations. The canonical DMA bug sits in
`neg` × `straddle` × other-channel-active — **two** reachable cells of the 72, not
three: under the generator's `c_solver_budget` a row is at most 256 beats, so a
straddling row splits into pieces none of which can itself be 256 — no burst out of
a straddling row lands in `cp_len`'s `max` bin. That exclusion follows from a
budget the team chose, not from the model's geometry (see "The solver-budget
argument" below). The bug's cells are `one` and `max_m1`.

*Resolved in the global consistency pass — do NOT harmonize these.* Chapter 2's
`cg_legalizer_stress` (`cp_stride` 2 · `cp_bnd` 3 · `cp_len` 3 · `cp_ch1` 2 = 36)
models the same feature with a narrower, mindset-stage set of axes. They differ on
the stride axis (2 vs 3 bins: `cg_2d_4kb` adds zero stride) and, more deeply, on the
boundary axis — chapter 2 bins headroom in **absolute bytes against fixed thresholds**,
`cg_2d_4kb` bins it **relative to what one burst of that row would move**. Making the
two identical was considered and rejected: the difference is a real refinement and is
now taught as one in ch05, where the model is introduced. `cg_2d_4kb` remains the
canonical artifact; `cg_legalizer_stress` is the earlier, coarser version by design.
ch05 cites both, where the model is introduced, and that is correct: any chapter
referencing the ch02 version must say which model it means — never present 36 and 72
as competing counts of one model.

*Sampling-scope note (pin this when harmonizing):* the two axes of `cg_2d_4kb`
sample at different scopes — `cp_len` samples the emitted burst length after the
midend splits a row, while `cp_boundary_dist` is a per-row relation computed by the
monitor. Every burst emitted from a straddling row carries that row's `straddle`
value. That scoping is what makes a `straddle` × `max` exclusion *statable* at all;
what actually excludes those cells is the generator's `c_solver_budget`, which caps
a row at 2048 bytes — 256 beats on the 64-bit path — so a straddling row splits into
pieces that sum to at most 256 and none of which can be 256 itself. Both halves are
load-bearing: drop the scoping and the argument does not apply, drop the budget and
the cells come back. Any reachability or cell-count argument in a chapter must
respect this scoping **and** name the budget as the exclusion's real premise — never
present these cells as dead by geometry.

```systemverilog
covergroup cg_2d_4kb @(posedge clk iff midend_txn_done);
  cp_stride_sign : coverpoint txn.stride_sign
    { bins pos = {POS}; bins zero = {ZERO}; bins neg = {NEG}; }
  // txn.bnd_rel: per-row relation, computed by the monitor from the row's
  // headroom (bytes to the next 4 KB frontier, in the stride's direction)
  // and this row's burst bytes. The four values partition every row once.
  cp_boundary_dist : coverpoint txn.bnd_rel
    { bins gt_burst = {GT_BURST};     // stays in frame, more than a burst of headroom
      bins eq_burst = {EQ_BURST};     // stays in frame, exactly a burst of headroom
      bins lt_burst = {LT_BURST};     // stays in frame, less than a burst of headroom
      bins straddle = {STRADDLE}; }   // reaches past the frontier — must be split
  cp_len : coverpoint txn.burst_len
    { bins one = {1}; bins max_m1 = {255}; bins max = {256}; }
  cp_other_ch : coverpoint other_channel_active;
  x_worst : cross cp_stride_sign, cp_boundary_dist, cp_len, cp_other_ch;
endgroup
```

The UART status register RAL model — **the canonical register artifact**, promoted
verbatim from chapter 10 §10.6, where it carries the front-door/back-door argument
and the canonical UART overrun bug. Any chapter modelling this register MUST copy
it exactly. What it pins: a 32-bit register with no coverage, holding one field
`oe` (RX overrun error) of width **1 at lsb 3**, access `"W1C"`, `volatile` = 1,
reset 0 with `has_reset` = 1, `is_rand` = 0 and not individually accessible. The
`volatile` flag and the `"W1C"` policy are the load-bearing arguments — drop
either and the mirror's predictions stop meaning anything. The `rand` qualifier on
the declaration is habit, not a claim: randomization is off twice over. `is_rand`
is passed as 0, and — the part that actually settles it — for a predefined access
policy outside the writable set, which `"W1C"` is, the library **ignores**
`is_rand` and turns the field's `rand_mode()` off regardless of what was passed
[cit:S4]. So a reader who flipped only the argument would not have re-enabled
anything.

*Corrected 2026-08-27.* This paragraph previously read "randomization is off
because `is_rand` is passed as 0 — and `"W1C"` … would ignore a 1 there anyway",
which puts the causation the wrong way round: S4 makes the access policy
operative and the argument inert, not the reverse. The earlier wording had been
escalated as a chapter-versus-bank conflict with a recommendation to correct
ch10 *to* the bank; reading S4 showed the bank was the wrong side, so ch10:222
now names both mechanisms and this row was fixed to match. Do not re-invert it.

```systemverilog
class uart_status_reg extends uvm_reg;
  rand uvm_reg_field oe;   // RX overrun error

  function new(string name = "uart_status_reg");
    super.new(name, 32, 0);
  endfunction

  virtual function void build();
    oe = uvm_reg_field::type_id::create("oe");
    //          parent size lsb access volatile reset has_rst rand indiv
    oe.configure(this,  1,   3,  "W1C",   1,      1'b0,  1,     0,   0);
  endfunction
endclass
```

Note that `build()` here is the register generator's convention, not a UVM phase.

Writing hygiene note: our QA tooling greps chapters for banned names with a pattern
that also matches the ordinary English collocation "chips it" — phrase around it
(e.g. "the devices it replaced").

Second known false positive, in the References sections rather than the prose: the
banned-name pattern `idma` is a substring of the surname **Davidmann**, which appears
as a cited author (D6). A banned-name hit inside a bibliography entry is almost
certainly one of these — read the match before acting on it, and never "fix" an
author's name. Both traps share one shape: a banned token that is also a substring of
legitimate text. Check hits, don't count them.

## Canonical numbers (QUOTE — never re-derive a count from memory)

Copying artifacts verbatim solved code drift; it does nothing for the *numbers*
chapters state ABOUT those artifacts. Those have drifted worse, because a count
looks like something you can recompute in your head — and four files independently
"recomputed" the same wrong one. **A chapter that states any number below must
quote this table and, where a derivation is given, restate that derivation rather
than inventing its own.** If a derivation here looks wrong to you, fix it HERE and
propagate; do not quietly write a different number in a chapter.

| Quantity | Value | Derivation / authority |
|---|---|---|
| `cg_2d_4kb` cross `x_worst` size | **72** | 3 (`cp_stride_sign`) × 4 (`cp_boundary_dist`) × 3 (`cp_len`) × 2 (`cp_other_ch`) |
| Cells the canonical DMA bug occupies | **2** | `neg` × `straddle` × other-ch-active, with `cp_len` ∈ {`one`, `max_m1`}. NOT 3: see the solver-budget argument below |
| `(·, straddle, max, ·)` cells — unreachable | **6** | 3 stride signs × 2 other-ch states; excluded by the generator's `c_solver_budget`, **not** by geometry — a recorded team choice that a later test may lift |
| One DMA channel's architecturally visible state | **192 bits** | ch03 §"the state space", authority for both numbers. (Label corrected 2026-08-27: this row said "the core's". Every one of the book's four uses attributes the figure to one DMA channel, and the derivation is the channel register map — 5×32 + 16 + 8 programmable = 184, plus a read-only status byte = 192. It cannot be the core: an RV32IMC core has 32×32 = 1,024 bits of register file alone. Do not regress.) **The predicate is load-bearing: 192 is *architecturally visible*, 184 is *programmable*, and they are not interchangeable.** The book shipped "192 programmable bits" once and it survived to review — quote the noun as well as the digits. Any 2^N built on this must say which N it used. |
| Reachable cells of `cg_2d_4kb` | **66** | 72 − 6, under the generator's `c_solver_budget` |
| `cg_legalizer_stress` cross size (ch02) | **36** | 2 × 3 × 3 × 2 — the deliberately narrower mindset-stage variant, NOT a competing count of the same model |
| reference SoC ADC reference voltage | **1.8 V** | 12-bit converter, so 1 LSB = 1.8 / 4096 ≈ **439 µV**. Verified against every chapter before adopting: ch19 says both power domains run at one nominal voltage without naming it, so nothing conflicts. Any tolerance stated in LSBs must be convertible to volts through this. *(ch21's PLL plan-row parameters — 100 ppm, 1024 cycles, 20 µs — are illustrative and chapter-local: do NOT canonicalise them unless a later chapter recurs them.)* |
| flagship cycles in a 40-minute run | **1.4–3.6 × 10¹²** | 2,400 s × the DVFS band 0.6–1.5 GHz. Deliberately robust: *every* operating point lands on order 10¹², which is what licenses ch20's "of order 10¹²" without pinning the DVFS point. Any chapter quoting a cycle count for a wall-clock duration must show the clock it used — this figure was underivable until the clock rates were added to the flagship's clocking row above |
| Crossbar manager ports | **5** | core-I, core-D, DMA ch0, DMA ch1, debug = indices 0-4 |
| Crossbar subordinate ports | **4** | SRAM, boot ROM, APB bridge, neural accelerator = indices 0-3 |
| Subordinate-side ID width | **7 bits** | 4-bit manager ID + ⌈log₂ 5⌉ = 3 manager-identifying bits. Widening is mandatory, not a design choice: AMBA AXI/ACE, ARM IHI 0022H §A5.2.3, p. A5-81 — the interconnect appends bits unique to the source port so masters need not know each other's IDs, and so responses can be routed home. **Consequence to keep in view:** two managers using the same manager-side ID arrive at a subordinate with *different* IDs, so no subordinate-side property or cover can ever see a cross-manager ID collision |
| `uart_status_reg.oe` position | **lsb 3, width 1** | `configure(this, 1, 3, "W1C", 1, 1'b0, 1, 0, 0)` — W1C, volatile, reset 0 |

**The solver-budget argument, stated once (quote it, don't re-derive it).** The two
axes sample at different scopes: `cp_len` samples the emitted burst length *after*
the midend splits a row, while `cp_boundary_dist` is a per-row relation computed by
the monitor. Every burst emitted from a straddling row carries that row's `straddle`
value. The exclusion then turns on a single premise, and that premise is *policy*:
`c_solver_budget` (chapter 9) caps a row at 2048 bytes — 256 beats on the 64-bit
path, one maximum burst, half a page — so a row reaches past at most one frontier,
and a straddling row splits into exactly two bursts whose beat counts sum to the
row's, at most 256, each of them at least one. Neither piece can be 256, so the
whole `straddle × max` column is dead for any stride sign and either other-channel
state.

**It is dead by choice, and that is the pedagogical point.** The cap is an
engineering choice about solve time, not a statement about the DUT — chapter 9 says
so where the constraint is written — and lifting it makes the column reachable: a
4104-byte row at offset 4088 splits into 1 beat and 512 beats, and the 512 splits
again into 256 + 256, which is `straddle` × `max`. So the six cells are an exclusion
that must be *recorded on vplan row `DMA-F06a`* and revisited when the budget moves,
which is precisely the bookkeeping chapter 5's *100% means 100% of the cells the
model can legitimately reach* demands — a convention that turns on separating what
is impossible from what was merely decided, and these six are the second kind.
Never write these six as dead "by geometry" or "before any constraint": both were
the pre-2026 formulation, and the second is now flatly false — the exclusion
depends on a constraint.

*Anti-pattern that produced this section:* "three of the 72 cells, one per
burst-length bin" — an inherited premise, plausible-sounding, wrong, and propagated
into four files before anyone re-derived it. Its cousin, "18 of 72", was wrong the
same way (the true figure is 12: six of the eighteen straddle cells are already dead).

*The third drift is subtler and worth naming, because a count check cannot catch it:*
"dead by geometry, before any constraint" attached the **wrong reason to a right
number**. Six is correct; the premise offered for it — "a row is at most 256 beats" —
is not a property of the model but a line of `c_solver_budget`. A number can be
audited by recomputation; a *reason* can only be audited by re-deriving it from the
artifact it claims to be about. When a derivation cites a bound, go and find where
that bound is written: if it lives in a constraint block, the exclusion is policy and
belongs in a waiver, not in the geometry.

## Canonical recurring bugs (reusable across chapters, keep consistent)

- DMA: 2D transfer with negative stride mis-legalized at the 4 KB AXI boundary → data corruption only when channel 1 is also active (found by constrained-random + scoreboard; missed by directed tests).
  - *Flagship descendant:* the same mis-legalization on the flagship's DMA, now under coherence — the split's second half writes a line the host cluster holds Modified, so the corruption stays invisible until the writeback.
- Crossbar: write-data interleaving at a subordinate port under back-pressure — two managers have writes in flight to one subordinate, the subordinate stalls `WREADY` on the first data beat, the crossbar's write arbiter releases the grant mid-burst, and beats of the two bursts arrive interleaved → found by protocol assertions in formal, 11-cycle trace.
  - **Do NOT write this as "same-ID write interleaving"** (the pre-2026 formulation, still findable in drafts). It is wrong twice over under AXI4, and both halves are load-bearing elsewhere in the book. *(1)* AXI4 deleted `WID`, so the write-data channel carries one burst at a time in address order regardless of ID; interleaving is illegal outright, and the checker that catches it (`a_w_burst_len`, ch. 11) never inspects an ID. *(2)* An interconnect widens IDs toward the subordinate (see "Subordinate-side ID width" above), so two managers presenting the same manager-side ID arrive at a subordinate with *different* IDs — the cross-manager same-ID collision is unreachable at that port by construction. The bug's precondition at a subordinate port is therefore `c_w_overlap` (a second write address accepted while an earlier burst is still unfinished on the write-data channel), never `c_same_id_pair`. Authority: AMBA AXI and ACE Protocol Specification, ARM IHI 0022H, §A5.2.2 and §A5.2.3, p. A5-81. Not a citable corpus source — state the rule unmarked, as ch. 4 and ch. 11 do.
  - *Flagship descendant:* the crossbar's write-data ordering obligation becomes end-to-end ordering between two mesh endpoints under virtual-channel congestion — the crossbar's verification story scaling into the NoC's.
- Core: custom SIMD instruction corrupts a saturation flag only when an interrupt lands in the same cycle → found by ISS co-simulation with random IRQ injection.
- Event unit: retention register loses configuration on power-domain re-entry when a wake event races isolation release → found by UPF-aware GLS, escaped RTL sim.
- NoC: deadlock with three-way circular wait across virtual channels under a rare traffic pattern → found by formal deadlock check on an abstracted model.
  - *Already flagship-side:* the NoC is the flagship's system interconnect, so this is a system-level find there and a block-level find standalone — the same bug on two platforms.
- UART: RX overrun flag never cleared if software reads status in the same cycle as a stop-bit error → found by directed test derived from a firmware bug report.
- Wake-cause CDC: the 3-bit wake-cause code crosses from the always-on 32 kHz island to the 200 MHz system domain through *per-bit* two-flop synchronizers, so a legal `3'b010 → 3'b100` transition is observed for one cycle as the reserved code `3'b110`; an incomplete `always_comb` decoder holds its previous decode and the handshake stalls → found by structural CDC analysis in seconds, invisible to simulation unless the transition and the sampling edge align. The canonical multi-bit-crossing bug: it needs a gray code or a handshake, not more synchronizer stages.
- Neural accelerator: the weight prefetcher wraps its buffer pointer one entry early when the weight stream ends mid-beat under DMA contention — reachable only at the narrowest precision (2-bit weights) with a degenerate tensor geometry (width 1) → escaped 100% code coverage entirely; only a functional cross of precision × width class × contention demands the scenario.
