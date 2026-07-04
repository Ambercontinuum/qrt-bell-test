# OSF Preregistration — QRT Ramsey/T2 Test v4.1 (Corrected Implementation)

All values match qrt41_ramsey_test.py (SHA-256
348696aa401d40c4557c559d8d7636aa3a7ee1336ae66315f188fb665fb1cd7b) exactly.

---

### Title

Preregistered Test of Quantum Resonance Theory's Coherence-Enhancement Prediction via Ramsey Interferometry: Corrected Implementation (v4.1)

---

### Description

Quantum Resonance Theory (QRT; Anson 2024, DOI 10.5281/ZENODO.15105902) predicts that superconducting-qubit coherence increases by 5–10% under a periodic physical drive at ωr = 10 MHz with amplitude R0 = 10⁻³ rad. A prior execution of this design (v4, job d940k9lgc6cc73feh290, July 2026) was found post-hoc to contain two implementation flaws — condition-to-qubit position confounding from incomplete rotation, and a decay-only fit model unable to represent Ramsey fringes from residual per-qubit detuning (~50–85 kHz observed) — and its verdict was withdrawn as improperly derived rather than claimed. This registration corrects the implementation with the hypothesis, parameters, frequencies, and drive amplitude unchanged: (1) full six-fold condition-to-qubit rotation, so every condition visits every physical qubit and position effects cancel in same-qubit contrasts; (2) a model-free primary index — the coherence-envelope area, the integral of |P(0) − 0.5| over the delay grid — which is monotone in coherence time, immune to fringe phase and detuning, and requires no curve fitting; (3) a same-qubit paired difference contrast as the primary comparison, which the v4 dataset demonstrated is the only clean comparison on this hardware. The drive is delivered as native fractional RX pulses (physical microwave drive) with a preregistered physicality assertion. Six conditions (four off-resonance frequencies, the theory-designated 10 MHz, and an undriven descriptive reference) run in parallel across six qubits per circuit. The result will be published regardless of outcome.

---

### Research questions or hypotheses

Primary index: G_A = Σ_q [A(10 MHz, q) − mean_c A(c, q)] / Σ_q mean_c A(c, q), where A(condition, qubit) is the trapezoidal integral of |P(0) − 0.5| over the delay grid for that condition on that physical qubit, c ranges over the off-resonance controls {1, 5, 15, 25} MHz, and q over the six physical qubits.

H1 (QRT): G_A ≥ +1.1% with 95% confidence interval excluding zero. Calibration of this threshold: the paper predicts a 5–10% coherence-time increase; under the attached synthetic calibration (fringe-realistic, hardware-heterogeneous), the minimum predicted effect (+5% T2) maps to an envelope-area gain of approximately +1.15%, and +10% T2 to approximately +2.2%. The threshold is therefore set at the mapped minimum claim.

H0 (Standard QM): the frequency profile is flat; the 95% CI upper bound on G_A falls below +1.1%.

Design logic: all comparison arms are physically driven at identical amplitude schedules on the same qubits; only frequency differs within each qubit's paired contrast. Position effects, per-qubit detuning, per-qubit T2, and the folding bias of |P − 0.5| are all condition-independent within a qubit and cancel in the paired difference. Only frequency structure can produce a signal.

---

### Foreknowledge of data or evidence

No confirmatory data for this analysis plan exist. The v4 dataset (job d940k9lgc6cc73feh290) exists and informed the identification of the implementation flaws this registration corrects; it is not analyzed by this plan, and its withdrawn analysis used a different estimator and a differently confounded design. The direction of this study's corrections is data-independent: the hypothesis, parameters, frequencies, amplitude, and claim boundary are unchanged, and a fringe-aware analysis could as easily reveal an effect the invalid v4 fits obscured as confirm its absence.

---

### Explanation of foreknowledge and managing unintended influences

The theory under test and this preregistration share an author; the protocol was drafted in collaboration with an AI system (Claude, Anthropic), consistent with the declared authorship practices of the underlying paper; and a prior implementation of this design was executed and its verdict withdrawn for post-hoc identified flaws. All three facts create potential influences in both directions — the incentive to rescue the theory on a third attempt, and the incentive to complete its falsification. These are managed structurally: the decision rule and its calibrated threshold are fixed before execution and admit no reinterpretation; the execution and analysis script is frozen, seed-fixed, and attached with its SHA-256 hash recorded in this registration; the primary index requires no curve fitting and therefore admits no fit-convergence discretion; data exclusion exists only at the session level under mechanical abort conditions; execution order is randomized by a recorded seed; the physicality assertion is preregistered so a non-physical compilation aborts before any shot; and all raw data, code, and calibration snapshots are published regardless of outcome. The sole prior executions of this pipeline are synthetic validation runs (null recovery and injected-effect power checks), attached and labeled non-evidential.

---

### Study type

Randomized Experiment: Must include random assignment of subjects to treatments or conditions. This usually includes lab experiments, field experiments, intervention experiments, randomized controlled trials, and A/B testing.

---

### Intention for causal interpretation

Direct inference on causal relationship(s): This study is intended to infer or estimate a causal relationship between two or more variables. It is designed specifically for the purposes of causal inference or identification.

Any envelope-area difference within a qubit across frequency conditions is attributed causally to drive frequency, because amplitude schedule, gate count, depth, scheduling, and physical qubit are identical within each paired contrast and only frequency differs; randomized execution order removes calibration drift as an alternative explanation; full rotation ensures every condition–qubit pairing is realized.

---

### Blinding of experimental treatments

No blinding is involved. Data collection and the primary analysis are fully scripted with no analyst degrees of freedom between measurement and decision; the primary index is computed by fixed arithmetic on raw counts with no fitting step.

---

### Study design

Six-condition, fully rotated, packed Ramsey design on a single IBM Quantum Heron-class superconducting device (open access tier), fractional gates enabled.

Per circuit: six qubits, one condition per qubit. Each qubit: H → delay grid with drive → H → measure (Ramsey sequence; P(0) decays toward 0.5 with coherence time, modulated by residual detuning fringes).

Conditions (6): driven at ωr ∈ {1, 5, 15, 25, 10} MHz — RX(2·R0·cos(ωr·t_k)) applied every 16 ns during the delay, R0 = 10⁻³ rad, delivered as native fractional RX pulses — plus one undriven reference (RX(0); descriptive only). 10 MHz is the theory-designated resonance level.

Rotation (6-fold, complete): six condition-to-qubit assignments, cyclic shifts of the base ordering, so that every condition is measured on every physical qubit exactly once per delay point. This is the corrected execution of the balanced-packed layout: condition and qubit position are fully crossed.

Delay grid: 12 points, 0 to 12,000 ns (linear).

Physicality assertion (preregistered): after transpilation, every circuit with nonzero delay must contain native rx operations; otherwise the run aborts before submission. Per-circuit operation counts are logged and published.

Measurement: P(0) per qubit per circuit from the computational-basis marginal of that qubit's classical bit.

Total: 72 circuits (12 delays × 6 rotations), each covering all six conditions in parallel.

---

### Randomization

All 72 circuits are executed in an order randomized by a fixed, recorded seed (seed 20260705, implemented in the attached script; the executed order is written into the results file for audit). Randomization is over execution order; run order is the channel through which calibration drift could enter, and randomizing it serves the confound-elimination function of random assignment. Within each circuit, all six conditions execute simultaneously on parallel qubits, so drift affects all conditions of a given circuit identically by construction.

---

### Data collection procedures

6,000 shots per circuit (432,000 total shots; each shot yields one measurement for all six conditions in parallel). No confirmatory data exist at registration; the only prior executions of this pipeline are synthetic validation runs (attached, non-evidential). Hardware: an IBM Quantum Heron-class backend supporting native fractional gates and ≥6 operational qubits, selected as least-busy at execution time; device name, calibration snapshot, per-circuit physicality log, and executed order will be recorded and reported. Stopping rule: one full session is the confirmatory dataset; a single preregistered escalation (double shots) exists for an inconclusive result. Full rules under Starting and Stopping Rules.

---

### Sample size

6,000 shots per circuit. 72 circuits (12 delay points × 6 rotations), for 432,000 total shots in the confirmatory session, each shot measuring all six conditions in parallel. If the preregistered escalation is triggered, one additional session at 12,000 shots per circuit (864,000 shots) is run, for a maximum of 1,296,000 shots across the study.

---

### Sample size rationale

The unit of inference is the measurement shot. Each condition–qubit cell receives 6,000 shots per delay point across 12 points. The primary index is arithmetic on these proportions with no fitting, so its sampling distribution is directly bootstrappable. The attached synthetic validation (fringe-realistic, per-qubit T2 heterogeneity 3–30 µs, detunings 5–120 kHz) produced: null G_A = +0.52% with 95% CI [−0.00%, +1.03%] (CI half-width ~±0.5%); +5% injected T2 effect → G_A = +1.65%, CI [+1.17%, +2.19%], correctly classified QRT-consistent; +10% → G_A = +2.66%, CI [+2.14%, +3.17%], correctly classified. The design therefore separates the null from the paper's minimum claim with the decision categories resolving correctly at both boundaries, within IBM open-tier session limits. The escalation tier exists to resolve marginal results near the +1.1% boundary.

---

### Starting and stopping rules

Starting rule. Data collection begins only after, in order: (1) this registration is frozen on OSF; (2) the execution script (qrt41_ramsey_test.py) is attached with its seed fixed and its SHA-256 hash recorded in the registration; (3) a fractional-gate-capable backend with ≥6 operational qubits is selected by the least-busy criterion and its calibration snapshot captured; (4) all nonzero-delay circuits pass the physicality assertion after transpilation. The first hardware shot defines study start. Any execution before the freeze does not count toward the confirmatory dataset and will be disclosed if it exists (none is planned; prior executions are the attached synthetic checks).

Stopping rule — normal completion. The confirmatory dataset is exactly one full session: 72 circuits × 6,000 shots. The decision rule is applied once, after all counts are collected. No interim analyses.

Stopping rule — preregistered escalation (single use). If and only if the decision rule returns inconclusive (95% CI spanning +1.1%), one additional session at 12,000 shots per circuit is run on the same backend within 14 days, with a fresh calibration snapshot and re-passed physicality assertion. The decision rule is applied to the escalation dataset alone. No further escalations; a second inconclusive terminates the study, reported as inconclusive with both datasets published.

Abort conditions (non-evidential termination). A session is aborted and rerun in full — disclosed in the final report — if: the physicality assertion fails at transpilation (before submission; costs no shots); backend recalibration or maintenance interrupts the sequence; more than 10% of jobs return errors; or the backend is decommissioned. Aborted sessions' partial data are published but excluded from confirmatory analysis; aborts do not consume the escalation tier.

What cannot stop the study. Interim glances at counts, partial results in either direction, author discretion, or any consideration not listed above.

---

### Manipulated variables

Drive frequency (five levels): ωr ∈ {1, 5, 15, 25, 10} MHz, applied as RX(2·R0·cos(ωr·t_k)) every 16 ns during the Ramsey delay, R0 = 10⁻³ rad, delivered as native fractional RX pulses. 10 MHz is the theory-designated resonance level; the remaining four are off-resonance comparators. Amplitude schedule, pulse count, depth, and scheduling are identical across driven conditions; frequency is the sole manipulated difference among them.

Condition-to-qubit assignment (six levels, fully crossed with frequency by the rotation scheme): every condition is measured on every physical qubit, so assignment is a controlled factor that cancels in the paired contrast rather than a confound.

A sixth condition (undriven reference, RX(0)) is collected for descriptive context and carries no inferential weight.

---

### Measured variables

Raw measurement counts: six-bit outcome frequencies per circuit, 6,000 shots each; per-qubit marginals extracted by fixed arithmetic. These are the primitive data and are published in full.

P(0) per condition per qubit per delay point, from the qubit's classical-bit marginal.

Envelope area A(condition, qubit): trapezoidal integral of |P(0) − 0.5| over the 12-point delay grid. No fitting.

Recorded covariates (not analyzed, reported for reproducibility): backend identity and calibration snapshot; per-circuit physicality log (transpiled operation counts confirming native rx); descriptive fringe-model fits per condition–qubit cell (P(0) = c + a·e^(−τ/T2)·cos(2πΔτ + φ)), reported to characterize per-qubit detuning and coherence but carrying no inferential weight; executed order; job timestamps.

---

### Indices

Primary index. G_A = Σ_q [A(10 MHz, q) − mean_c A(c, q)] / Σ_q mean_c A(c, q), the same-qubit paired difference contrast on envelope areas, c over {1, 5, 15, 25} MHz, q over the six physical qubits. Uncertainty: bootstrap 95% CI, 2,000 resamples, each redrawing every P(0) as a binomial proportion at the observed rate and shot count and recomputing all areas and the contrast, seed fixed in the attached script. G_A and its CI are the sole inputs to the decision rule.

Secondary (descriptive only): per-condition–per-qubit envelope areas; descriptive fringe fits (T2, detuning, phase per cell); the undriven reference's areas.

No other indices. The difference form of the contrast is preregistered specifically because the additive folding bias of |P̂ − 0.5| under binomial noise is condition-independent within a qubit and cancels in differences; no bias correction is applied or permitted.

---

### Statistical models

The primary analysis contains no statistical model: envelope areas are fixed arithmetic on measured proportions, and G_A is a ratio of their sums. The bootstrap is nonparametric over binomial resampling of the observed proportions.

Decision rule, applied to G_A:

QRT-consistent: G_A ≥ +1.1% AND 95% CI lower bound > 0. Outcome: escalation, not publication of a positive claim — replication on a second fractional-gate device, an amplitude sweep (R0 × {0.1, 1, 10}), and survival of the effect under drive-phase randomization are required before any claim. A resonance effect at milliradian pulse amplitude remains extraordinary and is treated as an artifact until it survives all three.

Falsified as specified: 95% CI upper bound < +1.1%. Outcome: QRT's coherence-enhancement prediction is reported as falsified under a physically delivered drive with a fringe-robust estimator at its stated parameters (R0 = 10⁻³ rad, ωr = 10 MHz, claim floor 5% T2 gain). Any revision of R0, ωr, or the claimed effect size is a new prediction requiring a new preregistration.

Inconclusive: CI spans +1.1%; handled solely by the preregistered escalation.

The descriptive fringe fits use P(0) = c + a·e^(−τ/T2)·cos(2πΔτ + φ) with bounded parameters and FFT-initialized detuning; they characterize the hardware and carry no inferential weight.

---

### Transformations

Counts → per-qubit marginals (fixed bit extraction) → P(0) proportions → |P(0) − 0.5| → trapezoidal integral over the delay grid → paired difference contrast. These are the only transformations in the confirmatory path. No error mitigation, no dynamical decoupling, no twirling (explicitly disabled in runtime options), no outlier removal, no smoothing, no normalization across sessions, no fitting in the confirmatory path. Gross hardware failure (any condition's τ = 0 point returning P(0) < 0.8) triggers the abort pathway, not a transformation.

---

### Inference criteria

Interval-based: the criterion is the position of the bootstrap 95% CI on G_A relative to 0 and +1.1%. Supporting H1 requires both the point estimate at or above the mapped minimum claim (+1.1%) and the CI excluding zero. Supporting H0 requires the CI upper bound below +1.1% — positive evidence the effect, if any, is smaller than the paper's minimum claim, not mere failure to reject. Frequency specificity is built into the index (a contrast of resonance against off-resonance within qubits). No multiplicity: exactly one confirmatory comparison; per-frequency and per-qubit quantities are descriptive; the six bases of the design do not exist here (single-basis Ramsey readout). One-sidedness: H1 is directional; a significantly negative G_A supports H0 and is reported descriptively. Nothing outside G_A and its CI carries inferential weight, including the descriptive fringe fits, the undriven reference, calibration covariates, and any quantity from aborted sessions or from the withdrawn v4 dataset.

---

### Data inclusion and exclusion

All shots from all 72 circuits of a completed confirmatory session are included unconditionally; no shot-, outcome-, circuit-, or qubit-level filters. Exclusion exists only at session level, if and only if an abort condition was met (physicality failure at transpilation, mid-session recalibration, >10% job errors, decommission). Aborted sessions are published in full, labeled, never partially harvested. No performance-based exclusion: a surprising number is a result, not a defect.

---

### Missing data

Shot-level missingness is structurally impossible (jobs complete whole or error whole). A failed job is resubmitted identically while total failures remain ≤ 10% of session jobs; repeated failure of the same circuit aborts the session for fault investigation, since circuit-specific failure could correlate with the delay grid. No imputation, interpolation, or cross-session filling; the design is analyzed complete or treated as aborted. No other missing-data pathways exist.

---

### Other planned analysis

None.

---

### Context and additional information

Frozen attachments, hash-anchored:
- qrt41_ramsey_test.py, SHA-256 348696aa401d40c4557c559d8d7636aa3a7ee1336ae66315f188fb665fb1cd7b — the script referenced by the Starting Rule.
- qrt41_calibration.json, SHA-256 03878e4c22c466ebff0963c472289a1978ff0fa6ea8af91ffa83e2951aafade5 — the four-arm synthetic calibration from which the +1.1% decision threshold is derived. The threshold is valid only with respect to the attached file matching this hash.

The attached files matching these hashes are the artifacts referenced throughout this registration; any file not matching its recorded hash is not part of this registration.

Relationship to prior tests: Test #1 (Bell fidelity, phase modulation) and Test #2 (Bell fidelity, physical drive) were falsified as specified under their own registrations. Test v4 (this design, incomplete rotation, decay-only model; job d940k9lgc6cc73feh290) was executed and its verdict withdrawn as improperly derived — condition confounded with qubit position, and a fit model unable to represent observed Ramsey fringes — with the flaws documented and the raw data published. v4.1 corrects the implementation with the hypothesis, parameters, frequencies, amplitude, and claim boundary unchanged. The v4 dataset is not analyzed by this plan.

Known limitations: per-pulse amplitude (10⁻³ rad) is physical but small relative to pulse-calibration precision; declared, uncorrected. The drive is stroboscopic (pulses every 16 ns), not a continuous tone; continuous pulse programming is unavailable on this platform. The envelope-area index is monotone in coherence but is a compressed summary of the decay curve; its threshold is defined by the attached synthetic calibration mapping the paper's minimum T2 claim into area units, and that mapping is itself an approximation declared as such. The test binds the prediction at its stated parameters and claim floor.

Conflicts / Provenance: the theory under test and this preregistration share an author; the protocol was drafted in collaboration with an AI system (Claude, Anthropic); a prior implementation's verdict was withdrawn by the author rather than claimed. The decision rule, calibrated threshold, fitting-free primary index, and physicality assertion were fixed before execution specifically to remove author degrees of freedom in all directions.

---

### Attachments to upload with registration

- qrt41_ramsey_test.py (frozen script, seed fixed)
- qrt41_calibration.json (complete four-arm synthetic calibration bundle — null, +5%, +7.5%, +10% injected T2 effects — from which the +1.1% area-units threshold is derived; labeled non-evidential; this attachment exists to freeze the threshold's provenance, not as evidence for any hypothesis)
