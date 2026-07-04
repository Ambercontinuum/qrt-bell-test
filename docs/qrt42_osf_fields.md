# OSF Preregistration — QRT v4.2 All-Vectors Amplitude-Scaling Micro-Test

All values match qrt42_scaling_test.py (SHA-256
9a386ccfb658f64417c5795ca7d1261ad1e1a80ff5bae1cc86f85f3099843318) exactly.

---

### Title

Preregistered Amplitude-Scaling and Multi-Vector Adjudication of a QRT-Consistent Coherence Result on Superconducting Hardware (v4.2)

---

### Description

A preregistered Ramsey test (v4.1, job d94hi4lgc6cc73ff4cc0, ibm_fez, July 2026) of Quantum Resonance Theory's coherence-enhancement prediction (Anson 2024, DOI 10.5281/ZENODO.15105902) returned a QRT-consistent result: G_A = +2.87%, 95% CI [+2.35%, +3.46%], at the theory-designated ωr = 10 MHz with R0 = 10⁻³ rad. Per that registration's own terms, the result is treated as an artifact until it survives escalation. This study executes the highest-information single-session adjudication available within remaining hardware quota, exploiting two facts: (1) a genuine drive-coupled effect must scale with drive amplitude, while calibration-floor and noise-spectrum artifacts at milliradian angles do not — so a 10× amplitude arm converts a marginal effect into a decisively resolvable one; (2) the packed six-qubit layout carries six conditions per circuit, so amplitude scaling, second-device replication at original amplitude, neighbor peak structure, drive-phase randomization, and an undriven reference all execute in the same 24 circuits. The primary decision rests on the amplitude arm alone; all other vectors are declared secondary and descriptive. The backend is required in code to differ from ibm_fez (the v4.1 device). The result will be published regardless of outcome.

---

### Research questions or hypotheses

Primary index: G_scale = Σ_q [A(10 MHz @ 10×R0, q) − mean(A(9 MHz @ 1×, q), A(11 MHz @ 1×, q))] / Σ_q mean(A(9 MHz, q), A(11 MHz, q)), where A is the trapezoidal integral of |P(0) − 0.5| over the delay grid, per condition per physical qubit.

H1 (drive-coupled mechanism, QRT-class): G_scale ≥ +3% with 95% CI excluding zero. Under the attached synthetic calibration, a drive-coupled effect of even half the v4.1-implied size produces G_scale ≈ +10.9% [+9.6%, +12.3%] at the 10× amplitude; the +3% threshold is conservative by a factor of ~3 against the minimum expected scaling.

H0 (non-scaling artifact): the amplified arm shows no elevation; 95% CI upper bound on G_scale falls below +3%. Under the null calibration: G_scale = +0.6% [−0.7%, +2.0%] — the decision categories separate cleanly at this budget in both directions.

Declared scope: 10×R0 = 10⁻² rad extends beyond the paper's stated amplitude and tests the mechanism class (drive-coupled coherence modification), not the paper's exact parameter point. A DOES_NOT_SCALE outcome does not formally falsify the paper's R0-point prediction; it removes the drive-coupled interpretation of the v4.1 result. A SCALES outcome does not confirm QRT; it advances the effect to full escalation (v5).

---

### Foreknowledge of data or evidence

No confirmatory data for this analysis plan exist. The v4.1 dataset exists, motivated this adjudication, and fixed the effect size against which the amplitude arm is calibrated; it is not analyzed by this plan.

---

### Explanation of foreknowledge and managing unintended influences

Shared authorship of theory and test; AI-collaborative protocol drafting (Claude, Anthropic); and a live QRT-consistent prior result create incentives in both directions — to confirm on a third run, and to dispatch the anomaly. Managed structurally: decision rule and threshold frozen before execution; script frozen, seed-fixed, hash-anchored; the primary index is fitting-free arithmetic on raw counts; exclusion is session-level only under mechanical abort conditions; execution order randomized by recorded seed; phase-randomization angles drawn from a fixed recorded seed; the second-device rule is enforced in code (ibm_fez refused both by default selection and explicit request); physicality assertion aborts a non-physical compilation before any shot; all data and code published regardless of outcome. Sole prior executions: attached synthetic calibration runs, non-evidential.

---

### Study type

Randomized Experiment: Must include random assignment of subjects to treatments or conditions. This usually includes lab experiments, field experiments, intervention experiments, randomized controlled trials, and A/B testing.

---

### Intention for causal interpretation

Direct inference on causal relationship(s): This study is intended to infer or estimate a causal relationship between two or more variables. It is designed specifically for the purposes of causal inference or identification. Any envelope-area difference within a qubit across conditions is attributed causally to the drive parameters (amplitude, frequency, phase coherence), since pulse count, scheduling, and physical qubit are identical within each paired contrast; randomized execution order removes drift; full rotation crosses condition with qubit completely.

---

### Blinding of experimental treatments

No blinding is involved. Collection and primary analysis are fully scripted; the primary index involves no fitting and no analyst discretion.

---

### Study design

Six-condition, fully rotated, packed Ramsey design on a single IBM Quantum Heron-class device that is NOT ibm_fez, fractional gates enabled.

Per circuit: six qubits, one condition per qubit; each qubit runs H → driven delay grid → H → measure.

Conditions (6): A2 = 10 MHz @ 1×R0 (replication arm); A3 = 10 MHz @ 10×R0 (amplitude arm, primary); NB9 = 9 MHz @ 1×; NB11 = 11 MHz @ 1× (neighbor controls); PR = 10 MHz @ 1× with per-pulse random phase from a fixed seed (spectral-specificity arm); REF = undriven (descriptive). Drives applied as RX(2·R0·scale·cos(ωr·t_k + φ_k)) every 16 ns, native fractional RX pulses.

Rotation: 6-fold complete — every condition on every physical qubit.

Delay grid: 4 points, 0–12,000 ns (linear).

Physicality assertion (preregistered): every nonzero-delay circuit must contain native rx after transpilation or the run aborts before submission; operation counts logged and published.

Total: 24 circuits (4 delays × 6 rotations), all six conditions in parallel per circuit.

---

### Randomization

All 24 circuits executed in an order randomized by fixed, recorded seed 20260708 (implemented in the attached script; executed order written to the results file). Randomization is over execution order, the channel through which calibration drift could enter; within each circuit all six conditions execute simultaneously on parallel qubits, so drift affects all conditions of a circuit identically by construction. The PR arm's per-pulse phases are drawn from seed 20260709 (SEED+1), fixed and reproducible.

---

### Data collection procedures

5,000 shots per circuit (120,000 total shots; each shot measures all six conditions in parallel). No confirmatory data exist at registration; prior executions are the attached synthetic calibration, non-evidential. Hardware: an IBM Heron-class backend with native fractional gates and ≥6 operational qubits, selected as least-busy among non-fez devices; device name, calibration snapshot, physicality log, and executed order recorded and reported. One session is the confirmatory dataset; a single preregistered escalation (double shots) exists for an inconclusive result.

---

### Sample size

5,000 shots per circuit; 24 circuits (4 delays × 6 rotations); 120,000 total shots in the confirmatory session. If escalation is triggered, one additional session at 10,000 shots per circuit (240,000 shots), for a maximum of 360,000 shots.

---

### Sample size rationale

The amplitude arm is the design's power source: rather than resolving a ~+2.9% effect (which requires the full-session budgets of v4.1), the 10× arm amplifies a drive-coupled effect into the +10–17% range, where the micro-budget's ±1.4% confidence intervals resolve it decisively. Attached synthetic calibration: null G_scale = +0.61% [−0.74%, +2.00%] → DOES_NOT_SCALE; half-sized drive-coupled effect → +10.92% [+9.60%, +12.28%] → SCALES; full-sized → +17.09% [+15.71%, +18.50%] → SCALES. Both decision categories are reached correctly with wide margins; the hypotheses are separated by roughly an order of magnitude relative to CI width. The escalation tier exists for the unlikely marginal case near +3%.

---

### Starting and stopping rules

Starting rule: (1) registration frozen on OSF; (2) qrt42_scaling_test.py attached, seed fixed, SHA-256 recorded in the registration; (3) a non-fez fractional-gate backend selected and calibration snapshot captured; (4) all nonzero-delay circuits pass the physicality assertion. First hardware shot defines study start. Pre-freeze executions do not count and would be disclosed (none planned beyond the attached synthetic checks).

Normal stop: one full session, 24 circuits × 5,000 shots; decision applied once after all counts collected; no interim analyses.

Escalation (single use): if the CI spans +3%, one session at 10,000 shots per circuit within 14 days, same backend, fresh calibration snapshot, re-passed physicality assertion; decision applied to the escalation dataset alone; a second inconclusive terminates the study as inconclusive with both datasets published.

Abort conditions: physicality failure at transpilation (pre-submission, costs nothing); mid-session recalibration; >10% job errors; decommission. Aborted sessions published in full, excluded from confirmatory analysis, do not consume escalation.

Nothing else can stop the study: no data peeking, no author discretion, no reaction to partial results.

---

### Manipulated variables

Within the driven conditions, three drive parameters are manipulated with pulse count, scheduling, and qubit identity held fixed: amplitude scale (1× vs 10× R0 at 10 MHz), frequency (9, 10, 11 MHz at 1×), and phase coherence (deterministic vs per-pulse randomized at 10 MHz, 1×). Condition-to-qubit assignment is fully crossed by the 6-fold rotation. The undriven REF is descriptive.

---

### Measured variables

Raw six-bit counts per circuit (5,000 shots each; published in full); P(0) per condition per qubit per delay point via fixed bit-marginal extraction; envelope area A(condition, qubit) = trapezoidal integral of |P(0) − 0.5| over the 4-point grid (no fitting). Recorded covariates (not analyzed): backend calibration snapshot; physicality log; executed order; job timestamps.

---

### Indices

Primary: G_scale as defined in the hypotheses — the same-qubit paired difference contrast of the 10×-amplitude arm against the neighbor mean. Uncertainty: bootstrap 95% CI, 2,000 resamples redrawing every P(0) as a binomial proportion at observed rate and shot count, seed fixed in the attached script. G_scale and its CI are the sole inputs to the decision rule.

Secondary (descriptive only, no inferential weight): G_rep (10 MHz @ 1× vs neighbor mean — the v4.1 effect's second-device point estimate); G_phase_rand (PR vs neighbor mean); per-condition per-qubit areas; REF areas. These inform the interpretation section of the outcome report and the design of v5; none can support or defeat a claim here.

No other indices; the difference-contrast form is preregistered because the folding bias of |P̂ − 0.5| is condition-independent within a qubit and cancels in differences.

---

### Statistical models

No statistical model in the confirmatory path: areas are fixed arithmetic; G_scale is a ratio of sums; the bootstrap is nonparametric.

Decision rule: SCALES_WITH_AMPLITUDE if G_scale ≥ +3% and CI lower bound > 0 → outcome: the drive-coupled reading of v4.1 survives; full escalation (v5: replication, full amplitude curve, phase randomization at power) is executed before any claim; no claim is made by this study. DOES_NOT_SCALE if CI upper bound < +3% → outcome: the v4.1 effect is attributed to a non-scaling artifact class; the drive-coupled/resonance interpretation is reported as unsupported; v5 proceeds as diagnostic autopsy if quota permits. INCONCLUSIVE otherwise → single preregistered escalation.

---

### Transformations

Counts → per-qubit marginals → P(0) → |P(0) − 0.5| → trapezoidal integral → paired difference contrast. Nothing else. No mitigation, no DD, no twirling (disabled in options), no outlier handling, no smoothing, no normalization, no fitting. Gross hardware failure (any condition's τ = 0 point returning P(0) < 0.8) triggers the abort pathway.

---

### Inference criteria

Interval-based, on G_scale against 0 and +3%. H1 requires the point estimate at/above threshold and CI excluding zero; H0 requires CI upper bound below threshold — positive evidence of non-scaling, not failure-to-reject. One confirmatory comparison; no multiplicity. H1 is directional; a significantly negative G_scale (amplified drive damaging coherence at 10 MHz specifically) supports H0 for the decision and is reported descriptively. Nothing outside G_scale and its CI carries inferential weight, explicitly including all secondary indices, the v4.1 dataset, and aborted-session data.

---

### Data inclusion and exclusion

All shots of a completed session included unconditionally; no sub-session filters of any kind. Exclusion is session-level only, on the mechanical abort conditions. Aborted sessions published, labeled, never partially harvested. No performance-based exclusion.

---

### Missing data

Job-level only (shots complete whole or error whole). Failed jobs resubmitted identically under the 10% abort ceiling; repeated same-circuit failure aborts the session; no imputation, interpolation, or cross-session filling; complete design or aborted session, nothing between.

---

### Other planned analysis

None.

---

### Context and additional information

Frozen attachments, hash-anchored:
- qrt42_scaling_test.py, SHA-256 9a386ccfb658f64417c5795ca7d1261ad1e1a80ff5bae1cc86f85f3099843318 — the script referenced by the Starting Rule.
- qrt42_scaling_calibration.json, SHA-256 08d71f10a244447fa3e9bb95a9fd16ec8c0d43f9ed0fe2f86daefc92d6f0b2cc — the synthetic calibration from which the +3% threshold and the power claims derive. The threshold is valid only with respect to the attached file matching this hash.

Any attached file not matching its recorded hash is not part of this registration.

Relationship to prior tests: Tests #1 and #2 (Bell fidelity) falsified as specified. v4 executed, verdict withdrawn as improperly derived (documented). v4.1 returned QRT_CONSISTENT_ESCALATE (G_A = +2.87% [+2.35%, +3.46%], ibm_fez); per its registration that result is an artifact until it survives escalation; this study is the first escalation arm. The v5 full-escalation protocol (script hash ea46028b57f769a65f19c06a9b9789646457124001da1781ed7a6cd55fadd840) is drafted and follows regardless of this study's outcome, as confirmation campaign or autopsy respectively.

Known limitations: the 10× arm's per-pulse angle (10⁻² rad) remains far below decoupling amplitudes but is no longer at the calibration floor — partially removing, by design, the tiny-angle calibration concern of prior tests; the 4-point delay grid compresses the envelope relative to v4.1's 12-point grid, and the calibration maps effects into this grid's units; the drive is stroboscopic; secondary indices are underpowered by design and declared descriptive.

Conflicts / Provenance: shared authorship of theory and test; AI-collaborative drafting (Claude, Anthropic); a live QRT-consistent prior result. The frozen decision rule, code-enforced second-device requirement, fitting-free index, seeded phase randomization, and hash-anchored calibration exist specifically to remove author degrees of freedom in all directions.

---

### Attachments

- qrt42_scaling_test.py
- qrt42_scaling_calibration.json
