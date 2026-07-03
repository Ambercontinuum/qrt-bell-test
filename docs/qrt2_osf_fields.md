# OSF Preregistration #2 — Field-by-Field Text
## QRT Physical-Drive Bell Test

All values in this document match qrt_physical_test.py (SHA-256
ea99e8e5f427e54735820624fbd4e856f97cfdc177fefa4a8b35ce5d7a9f36eb) exactly.
Paste each section into the corresponding OSF field.

---

### Title

Preregistered Test of Quantum Resonance Theory Under a Physically Delivered Periodic Drive on Superconducting Quantum Hardware

---

### Description

Quantum Resonance Theory (QRT; Anson 2024, DOI 10.5281/ZENODO.15105902) predicts a resonance enhancement of Bell-state fidelity under a periodic drive with amplitude R0 = 10⁻³ rad at ωr = 10 MHz. A prior preregistered test (Test #1, this author, July 2026) falsified the prediction as delivered by phase modulation, which superconducting hardware implements as virtual (non-physical) frame rotations. This study tests the physically delivered form of the drive, corresponding to the paper's Hamiltonian H = H0 + V0·cos(ωr·t): the drive is implemented as native fractional RX pulses on IBM Heron-class hardware — real microwave energy entering the device, modulated at the drive frequency — with a preregistered physicality assertion that aborts the run if the transpiler decomposes the drive into virtual rotations. Because physical pulses can degrade fidelity uniformly, the design compares fidelity ACROSS drive frequencies at identical amplitude schedules rather than driven-versus-idle: QRT's resonance mechanism predicts fidelity at 10 MHz elevated above off-resonance frequencies; standard quantum mechanics predicts a flat profile. This is a new prediction under a new registration, per the rules of Test #1's registration; it does not reopen or rescue Test #1's result. The result will be published regardless of outcome.

---

### Research questions or hypotheses

H1 (QRT, physical-drive form): The resonance contrast G_res = F(10 MHz) / mean(F at 1, 5, 20, 50 MHz) − 1 is ≥ +2.5%, with 95% confidence interval excluding zero.

H0 (Standard QM): The frequency profile is flat; the 95% confidence interval upper bound on G_res falls below +2.5%.

The +2.5% threshold is half the effect size predicted by the source paper (~5%), matching Test #1's threshold, so that a true effect passes comfortably while hardware drift cannot.

Note on design logic: all comparison arms are physically driven at identical amplitude schedules; only the drive frequency differs. Uniform pulse-induced degradation therefore cancels in G_res, and only frequency structure can produce a signal. An undriven reference arm is collected for descriptive context only and carries no inferential weight.

---

### Foreknowledge of data or evidence

Data does not yet exist. No part of the data that will be used for this analysis plan exists, and no part will be generated until after this plan is registered. Test #1's dataset (a different stimulus implementation and a different primary index) informed the design of this study but is not analyzed by it.

---

### Explanation of foreknowledge and managing unintended influences

The theory under test and this preregistration share an author, and the protocol was drafted in collaboration with an AI system (Claude, Anthropic), consistent with the declared authorship practices of the underlying paper. A prior test by the same author falsified the phase-modulation form of the prediction; this creates a potential influence in both directions — an incentive to rescue the theory under the physical-drive form, and an incentive to complete a second falsification. These are managed structurally rather than by intention: the decision rule is fixed before any hardware execution and admits no reinterpretation; the execution and analysis script is frozen, seed-fixed, and attached, with its SHA-256 hash recorded in this registration; data exclusion exists only at the session level under mechanical abort conditions; execution order is randomized by a recorded seed; the physicality assertion is preregistered so that a non-physical compilation aborts rather than silently reverting to Test #1's stimulus; and all raw data, code, and calibration snapshots are published regardless of outcome. The sole prior execution of this pipeline is a simulator check that implements standard quantum mechanics and does not model pulse physicality; it is attached, labeled non-evidential.

---

### Study type

Randomized Experiment: Must include random assignment of subjects to treatments or conditions. This usually includes lab experiments, field experiments, intervention experiments, randomized controlled trials, and A/B testing.

---

### Intention for causal interpretation

Direct inference on causal relationship(s): This study is intended to infer or estimate a causal relationship between two or more variables. It is designed specifically for the purposes of causal inference or identification.

Any fidelity difference across frequency conditions is attributed causally to the drive frequency, because amplitude schedule, gate count, circuit depth, and scheduling are identical across all driven arms and only frequency differs; randomized execution order removes calibration drift as an alternative explanation.

---

### Blinding of experimental treatments

No blinding is involved. Data collection and fidelity computation are fully scripted with no analyst degrees of freedom between measurement and decision; the analysis script, including the decision rule and the physicality assertion, is frozen and attached prior to any hardware execution.

---

### Study design

Six-condition interleaved design on a single IBM Quantum Heron-class superconducting device (open access tier), with native fractional gates enabled.

Preparation: two-qubit Bell state |Φ+⟩ via Hadamard + CNOT.

Hold window: 1,920 ns total, sliced into 40 segments of 48 ns (matching Heron timing granularity of 12 dt directly, eliminating Test #1's rounding limitation).

Driven arms (5): after each slice k at elapsed time t_k, apply RX(2·R0·sin(ωr·t_k)) to both qubits, with R0 = 10⁻³ rad — the QRT drive implemented as native fractional RX pulses (physical microwave drive). One arm per frequency: ωr ∈ {1, 5, 10, 20, 50} MHz. 10 MHz is the theory-designated resonance level. Amplitude schedule is identical across arms; only frequency differs.

Undriven reference arm (1): identical circuits with RX(0); descriptive only, no inferential role.

Physicality assertion (preregistered): after transpilation, every driven circuit must contain native rx operations. If the transpiler decomposes the drive into sx/x plus virtual rz, the run aborts before submission. Per-circuit operation counts are logged and published.

Measurement: three parity settings (XX, YY, ZZ) per condition. Fidelity estimated as F = (1 + ⟨XX⟩ − ⟨YY⟩ + ⟨ZZ⟩)/4.

Interleaving: all circuits submitted within the same session in an order randomized by the fixed, recorded seed described under Randomization; the executed order is logged to the results file.

Total: 18 circuits (6 conditions × 3 bases).

---

### Randomization

All 18 circuits (5 driven frequencies + 1 undriven reference, × 3 bases) are executed in an order randomized by a fixed, recorded seed (seed 20260703, implemented in the attached script; the executed order is written into the results file for audit). Randomization is over execution order rather than assignment of subjects, since each circuit constitutes its condition by construction; run order is the channel through which the design's principal confound (hardware calibration drift) could enter, and randomizing it serves the same confound-elimination function that random assignment serves in subject-based designs.

---

### Data collection procedures

8,000 shots per circuit (144,000 total shots). No data relevant to this hypothesis have been collected at the time of registration; the only prior execution of the pipeline was on a local noisy simulator as a code-validation step, which implements standard quantum mechanics, does not model pulse physicality, and carries no evidential weight for the hypothesis (its null is by construction). Simulator validation output is attached for transparency.

Hardware: an IBM Quantum Heron-class superconducting backend supporting native fractional gates, selected as least-busy at execution time and loaded with fractional gates enabled; device name, calibration snapshot (T1, T2, gate and readout errors), per-circuit transpiled operation counts (the physicality log), and actual scheduled circuit durations will be recorded and reported.

Stopping rule: one full session constitutes the confirmatory dataset. If the decision rule returns "inconclusive" (CI spanning the boundary), shots are doubled and the session rerun once; this escalation is preregistered and does not permit reinterpretation of the decision rule. Full starting, stopping, and abort conditions are specified under Starting and Stopping Rules.

---

### Sample size

8,000 shots per circuit. 18 circuits total (6 conditions × 3 measurement bases), for 144,000 total shots in the confirmatory session. If the preregistered escalation is triggered (inconclusive result), one additional session at 16,000 shots per circuit (288,000 shots) is run, for a maximum of 432,000 shots across the study.

---

### Sample size rationale

The unit of statistical inference is the measurement shot; shots are i.i.d. draws per circuit under fixed calibration. At 8,000 shots per basis, each parity expectation has standard error ≤ 1/√8000 ≈ 0.011, propagating to a standard error on fidelity of approximately 0.005. The primary index G_res compares one fidelity against the mean of four, whose averaging reduces the denominator's error; the attached simulator validation run produced a bootstrap 95% CI on G_res of [−0.28%, +0.29%]. The predicted effect is ~+5% and the decision threshold is +2.5%: the design resolves the threshold at roughly 9× the CI half-width and the predicted effect at roughly 17×, giving power effectively indistinguishable from 1 against H1's stated effect size while remaining within IBM open-tier session limits. The escalation tier exists not for power against the stated effect — which is already saturated — but to resolve a marginal result near the threshold, roughly halving the CI width if triggered.

---

### Starting and stopping rules

Starting rule. Data collection begins only after all of the following are satisfied, in order: (1) this registration is frozen on OSF; (2) the execution script (qrt_physical_test.py) is attached to the registration with its seed fixed, and its SHA-256 hash recorded in the registration; (3) a fractional-gate-capable backend is selected by the least-busy criterion and its calibration snapshot is captured; (4) all driven circuits pass the physicality assertion after transpilation. The first hardware shot defines study start. Any execution that occurs before the registration freeze does not count toward the confirmatory dataset and will be disclosed as such if it exists (none is planned; the only pre-registration execution is the simulator pipeline check, attached and labeled non-evidential).

Stopping rule — normal completion. The confirmatory dataset is exactly one full session: 18 circuits × 8,000 shots. Data collection stops when the final circuit completes. The decision rule is then applied once. No interim analyses are performed during the session; fidelity is not computed until all counts are collected.

Stopping rule — preregistered escalation (single use). If and only if the decision rule returns "inconclusive" (95% CI spanning the +2.5% boundary), one additional session at 16,000 shots per circuit is run on the same backend within 14 days, using a freshly captured calibration snapshot and re-passing the physicality assertion. The decision rule is applied to the escalation dataset alone. No further escalations are permitted; if the escalated session is also inconclusive, the study terminates and is reported as inconclusive with both datasets published.

Abort conditions (non-evidential termination). A session is aborted and rerun in full — with the abort disclosed in the final report — if any of the following occur: the physicality assertion fails at transpilation (before submission; costs no shots); backend recalibration or maintenance interrupts the interleaved sequence; more than 10% of jobs return errors; or the backend is decommissioned. An aborted session's partial data are published but excluded from the confirmatory analysis. Aborts do not consume the escalation tier.

What cannot stop the study. Interim glances at raw counts, disappointing or exciting partial results, author discretion, or any consideration not listed above. There is no data-peeking pathway to early termination: the session runs to completion or aborts on the mechanical conditions stated, nothing else.

---

### Manipulated variables

Drive frequency (five levels): ωr ∈ {1, 5, 10, 20, 50} MHz, applied as RX(2·R0·sin(ωr·t_k)) on both qubits after each of the 40 hold-window slices, with R0 = 10⁻³ rad delivered as native fractional RX pulses. 10 MHz is the theory-designated resonance level; the remaining four are off-resonance comparators. Amplitude schedule, gate count, circuit depth, and scheduling are identical across all driven arms; frequency is the sole manipulated difference among them.

A sixth condition (undriven reference, RX(0) at identical positions) is collected for descriptive context and carries no inferential weight.

The inferential design is a one-factor, five-level frequency comparison among physically driven arms.

---

### Measured variables

Raw measurement counts: two-bit outcome frequencies per circuit per basis (XX, YY, ZZ), 8,000 shots each. These are the primitive data; all quantities below are computed from them and the raw counts are published.

Parity expectations ⟨XX⟩, ⟨YY⟩, ⟨ZZ⟩ per condition, computed as the shot-weighted mean of (+1 for even-parity outcomes, −1 for odd).

Bell-state fidelity per condition: F = (1 + ⟨XX⟩ − ⟨YY⟩ + ⟨ZZ⟩)/4 with respect to |Φ+⟩.

Recorded covariates (not analyzed, reported for reproducibility). Backend identity and calibration snapshot at execution (T1, T2, gate and readout error rates for the qubits used); the per-circuit physicality log (transpiled operation counts confirming native rx); actual scheduled circuit durations from the transpiled circuits; job submission and completion timestamps; the randomized executed order of the 18 circuits.

---

### Indices

Primary index. Resonance contrast at the theory-designated frequency:

G_res = F(10 MHz) / mean(F(1 MHz), F(5 MHz), F(20 MHz), F(50 MHz)) − 1

where each F is computed as (1 + ⟨XX⟩ − ⟨YY⟩ + ⟨ZZ⟩)/4 from the three measured parity expectations of that condition. Uncertainty on G_res is a bootstrap 95% confidence interval: 4,000 resamples, each drawing multinomial counts per basis per condition from the observed raw counts, recomputing all five fidelities and the contrast per resample, with the random seed fixed in the attached script. G_res and its CI are the sole inputs to the preregistered decision rule.

Secondary (descriptive only). The five per-frequency fidelities and the undriven-reference fidelity, reported with no inferential role.

No other indices. No composite scores beyond G_res, no per-basis sub-fidelities analyzed separately, no post-hoc transformations. Only G_res carries inferential weight.

---

### Statistical models

Fidelity per condition from parity expectations as specified above. Resonance contrast G_res and its 95% CI computed by nonparametric bootstrap over raw measurement counts (4,000 resamples, multinomial per basis per condition, seed fixed in the attached script).

Decision rule, applied to G_res:

QRT-consistent: G_res ≥ +2.5% AND CI excludes 0. Outcome: escalation, not publication of a positive claim — independent replication on a second fractional-gate device, an amplitude sweep (R0 × {0.1, 1, 10}), and verification that the effect survives with the drive schedule's phase randomized are required before any claim is made. A resonance effect at milliradian pulse amplitude is extraordinary and will be treated as an artifact until it survives all three.

Falsified as specified: CI upper bound < +2.5%. Outcome: QRT's resonance prediction is reported as falsified under a physically delivered drive at its stated parameters (R0 = 10⁻³ rad, ωr = 10 MHz). Any future revision of R0 or ωr constitutes a new prediction requiring a new preregistration and will not be presented as a rescue of this one.

Inconclusive: CI spans +2.5% and the escalated (double-shot) rerun also spans it. Outcome: reported as inconclusive with both datasets published.

No optional analyses. No post-hoc subgroups. Raw counts, physicality logs, calibration snapshots, analysis code, and this registration are published together regardless of outcome.

---

### Transformations

Raw two-bit counts are transformed to parity expectations by mapping each outcome to +1 (even parity: 00, 11) or −1 (odd parity: 01, 10) and taking the shot-weighted mean. Parities are transformed to fidelity via F = (1 + ⟨XX⟩ − ⟨YY⟩ + ⟨ZZ⟩)/4, and fidelities to the resonance contrast G_res as specified in Indices. These are the only transformations.

Explicitly excluded transformations: no measurement-error mitigation (no readout-error correction, no zero-noise extrapolation, no probabilistic error cancellation) is applied in the confirmatory analysis. All conditions experience identical readout error, which cancels to first order in the contrast; applying mitigation would introduce an analyst degree of freedom larger than the quantity it corrects. Dynamical decoupling and twirling are explicitly disabled in the runtime options. No outlier removal, winsorizing, or smoothing at the shot level. No normalization across conditions or sessions. If a negative fidelity or any driven-arm fidelity ≤ 0.5 is observed (indicating gross hardware failure rather than a physics result), this triggers the abort pathway under Starting and Stopping Rules rather than any transformation.

---

### Inference criteria

Inference is interval-based: the preregistered criterion is the position of the bootstrap 95% confidence interval on G_res relative to two fixed reference values, 0 and +2.5%. This is equivalent to two one-sided tests at α = 0.025 each, stated in CI form because the decision rule depends on the interval's location.

Criterion for supporting H1 (QRT-consistent). Both conjuncts must hold: (a) the CI lower bound on G_res exceeds 0; (b) the point estimate G_res ≥ +2.5%. Frequency specificity is built into the index itself — G_res is a contrast of the resonance frequency against off-resonance frequencies — so no separate ordinal conjunct is required in this design.

Criterion for supporting H0 (falsification as specified). The CI upper bound on G_res falls below +2.5%. This is an interval-exclusion criterion rather than failure-to-reject: H0 is supported by positive evidence that the resonance contrast, if any, is smaller than half the predicted size.

Inconclusive. The CI contains +2.5%. Handled solely by the preregistered escalation under Starting and Stopping Rules.

Multiple comparisons. No correction is applied, because exactly one confirmatory comparison is made (G_res against the two reference values). Individual per-frequency fidelities are reported descriptively and never individually tested. The three measurement bases are components of a single fidelity estimator, not separate hypotheses.

One-sidedness. H1 is directional (QRT predicts resonance elevation, not depression). A significantly negative G_res — fidelity depressed at the resonance frequency — supports H0 for the purpose of the decision rule and is additionally reported descriptively.

What does not count as inference. Point-estimate comparisons without CI backing, per-basis parity differences, the undriven reference arm, covariate patterns in calibration data, and any quantity computed from the aborted-session archive. These may motivate future preregistrations; they carry no inferential weight here.

---

### Data inclusion and exclusion

Inclusion. All shots from all 18 circuits of a completed confirmatory session are included, unconditionally. There are no shot-level, outcome-level, or circuit-level quality filters. Inclusion is determined entirely by session-level criteria fixed before execution.

Exclusion (session level only). A session's data are excluded from confirmatory analysis if and only if the session met an abort condition (physicality-assertion failure at transpilation, mid-session recalibration, >10% job errors, backend decommission — as defined under Starting and Stopping Rules). Excluded sessions are published in full and labeled as aborted; they are never partially harvested. There is no mechanism for excluding individual circuits, bases, or shots from an otherwise-complete session — the unit of exclusion is the session, whole or not at all.

No performance-based exclusion. Data are never excluded because fidelity values look anomalous, because one basis disagrees with the others, or because the result is surprising in either direction. A surprising number is a result, not a defect.

---

### Missing data

The measurement process makes shot-level missingness structurally impossible: the backend returns exactly the requested number of shots per circuit or the job errors in its entirety. Missingness therefore occurs only at job granularity, and is handled as follows:

A failed job (returned error, timeout, or cancellation) is resubmitted identically until it completes, provided total failed jobs remain ≤ 10% of the session's jobs (the abort threshold). Resubmission timestamps are recorded and reported.

If a job repeatedly fails on the same circuit while others succeed — indicating a circuit-specific compilation or scheduling fault — the session is aborted and the fault investigated before a fresh session, since a systematic per-circuit failure could correlate with condition and silently bias the design.

Under no circumstances is a missing job's cell imputed, interpolated from neighboring frequencies, or filled from a different session. The design is analyzed complete or not at all: a confirmatory dataset with any permanently missing cell is treated as an aborted session.

No participant-style attrition exists in this design; there are no other missing-data pathways.

---

### Other planned analysis

None.

---

### Context and additional information

Frozen analysis script: qrt_physical_test.py, SHA-256 ea99e8e5f427e54735820624fbd4e856f97cfdc177fefa4a8b35ce5d7a9f36eb. The attached file matching this hash is the script referenced by the Starting Rule.

Relationship to Test #1: A prior registration by this author tested the same prediction under phase modulation (virtual RZ) and returned falsification as specified. Per that registration's own rules, the present study is a new prediction under a new registration — the physically delivered form of the drive — and does not reopen, re-adjudicate, or rescue Test #1's result.

Known Limitations:

The drive amplitude (R0 = 10⁻³ rad per pulse) is ~0.03% of a π-pulse amplitude; the pulses are physical but their delivered amplitude carries calibration uncertainty at this scale, which is declared rather than corrected. The stroboscopic implementation applies discrete pulses, 40 across the hold window, rather than a continuous tone; continuous-tone delivery (Qiskit Pulse) is no longer available on this platform. Slice duration is set to 48 ns, matching hardware granularity exactly, eliminating Test #1's rounding limitation. The source paper's stated perturbation strength (V0 ≈ 10⁻³ eV) is large relative to transmon energy scales; this test binds the prediction at the paper's phase-amplitude specification (R0 = 10⁻³ rad), consistent with Test #1, and the tension in the paper's parameter set is noted without adjudication. The test binds QRT's prediction only at its stated parameter values; it does not exhaust the theory's parameter space.

Conflicts / Provenance:

The theory under test and this preregistration share an author. The protocol was drafted in collaboration with an AI system (Claude, Anthropic), consistent with the declared authorship practices of the underlying paper. The decision rule and the physicality assertion were fixed before any hardware execution specifically to remove author degrees of freedom in either direction — including the incentive to rescue the theory after Test #1's falsification, and the incentive to complete a second falsification.

---

### Attachments to upload with registration

- qrt_physical_test.py (frozen execution and analysis script, seed fixed)
- qrt2_sim_results.json (simulator pipeline-validation output, labeled non-evidential)
