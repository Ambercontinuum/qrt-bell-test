# OSF Preregistration — QRT v5: Confirmatory Point-Claim Replication on a Second Device

All values match qrt5_escalation_test.py (SHA-256
e37fa996cbe2491dcdd02e1f8d4f72e5880838a72fd523c5697162ae12a267a7) exactly.

---

### Title

Preregistered Confirmatory Replication of a QRT-Consistent Coherence Result at Stated Parameters on a Second Superconducting Device (v5)

---

### Description

A preregistered Ramsey test (v4.1, job d94hi4lgc6cc73ff4cc0, ibm_fez) of Quantum Resonance Theory's coherence-enhancement prediction (Anson 2024, DOI 10.5281/ZENODO.15105902) returned G_A = +2.87% [+2.35%, +3.46%] at the theory's stated parameters (ωr = 10 MHz, R0 = 10⁻³ rad) — QRT-consistent, treated per its registration as an artifact pending escalation. A first escalation arm (v4.2, job d94j866vtlqs73fucnvg, ibm_marrakesh) excluded the amplitude-scaling mechanism class (10× arm: G_scale = +1.07% [−0.18%, +2.24%], DOES_NOT_SCALE) but, by its own declared scope, did not adjudicate the paper's point claim: its 1× replication index was preregistered as descriptive, underpowered (4-point grid), and carries no inferential weight. This study is the confirmatory adjudication of the point claim itself: the v4.1 protocol at full power (12-point delay grid, 6,000 shots, 72 circuits) on a second device (ibm_fez refused in code), with the primary index defined at the paper's stated amplitude and frequency against symmetric neighbor controls (9 and 11 MHz). Secondary arms (10× amplitude, per-pulse phase randomization, undriven reference) ride in the same packed session as declared descriptive vectors. The result will be published regardless of outcome. If the point claim does not replicate here, the v4.1 result is attributed to a device-specific or statistical artifact and the program's adjudication of QRT's coherence prediction closes; if it replicates, the effect survives to independent-party verification.

---

### Research questions or hypotheses

Primary index: G_rep = Σ_q [A(10 MHz @ 1×R0, q) − mean(A(9 MHz, q), A(11 MHz, q))] / Σ_q mean(A(9 MHz, q), A(11 MHz, q)), where A is the trapezoidal integral of |P(0) − 0.5| over the 12-point delay grid, per condition per physical qubit.

H1 (QRT point claim replicates): G_rep ≥ +0.9% with 95% CI excluding zero. The threshold is half the v4.1-observed effect as expressed in this design's area units (attached calibration: a v4.1-sized effect produces G_rep ≈ +3.1% [+2.4%, +3.9%]; a half-sized effect ≈ +1.6% [+0.9%, +2.5%] — both correctly classified REPLICATED).

H0 (does not replicate): 95% CI upper bound on G_rep falls below +0.9%. Null calibration: G_rep = +0.01% [−0.77%, +0.83%] — correctly classified NOT_REPLICATED; the decision categories separate cleanly in both directions at this power.

Design logic: identical amplitude schedules on the same qubits; only frequency differs within each qubit's paired contrast; position, detuning, per-qubit coherence, and folding bias cancel in the paired difference; full rotation crosses condition with qubit completely.

---

### Foreknowledge of data or evidence

No confirmatory data for this analysis plan exist. The v4.1 dataset fixed the effect size against which this study's threshold is calibrated; the v4.2 dataset motivated the removal of the low-amplitude arm and the promotion of symmetric neighbor controls. Neither dataset is analyzed by this plan.

---

### Explanation of foreknowledge and managing unintended influences

Shared authorship of theory and test; AI-collaborative protocol drafting (Claude, Anthropic); one live QRT-consistent result and one escalation arm already adverse to it. Incentives exist in both directions — to rescue the surviving result, and to complete the program with a tidy negative. Managed structurally: decision rule and threshold frozen before execution; script frozen, seed-fixed, hash-anchored; fitting-free primary index; session-level-only exclusion under mechanical abort conditions; randomized execution order (recorded seed); seeded phase-randomization angles; second-device rule enforced in code; physicality assertion aborts non-physical compilation before any shot; publication regardless of outcome. Additionally, one prior analysis error is on record and corrected: the author's AI collaborator initially presented v4.2's descriptive 1× index as if it adjudicated replication, in violation of that registration's inference criteria; this registration exists precisely because that index had no confirmatory standing. Sole prior executions of this pipeline: attached synthetic calibration runs, non-evidential.

---

### Study type

Randomized Experiment: Must include random assignment of subjects to treatments or conditions. This usually includes lab experiments, field experiments, intervention experiments, randomized controlled trials, and A/B testing.

---

### Intention for causal interpretation

Direct inference on causal relationship(s): This study is intended to infer or estimate a causal relationship between two or more variables. It is designed specifically for the purposes of causal inference or identification. Any envelope-area difference within a qubit across frequency conditions is attributed causally to drive frequency; pulse count, amplitude schedule, scheduling, and physical qubit are identical within each paired contrast; randomized order removes drift; full rotation crosses condition with qubit.

---

### Blinding of experimental treatments

No blinding is involved. Collection and primary analysis are fully scripted; the primary index involves no fitting and no analyst discretion.

---

### Study design

Six-condition, fully rotated, packed Ramsey design on a single IBM Quantum Heron-class device that is NOT ibm_fez (enforced in code), fractional gates enabled.

Per circuit: six qubits, one condition per qubit; each qubit runs H → driven delay grid → H → measure.

Conditions (6): A2 = 10 MHz @ 1×R0 (PRIMARY arm — the paper's stated parameters); NB9 = 9 MHz @ 1× and NB11 = 11 MHz @ 1× (symmetric neighbor controls, the primary comparator); A3 = 10 MHz @ 10×R0 (secondary: cross-device check of v4.2's scaling exclusion); PR = 10 MHz @ 1× with per-pulse random phase from a fixed seed (secondary: spectral specificity); REF = undriven (descriptive). Drives applied as RX(2·R0·scale·cos(ωr·t_k + φ_k)) every 16 ns, native fractional RX pulses.

Rotation: 6-fold complete — every condition on every physical qubit.

Delay grid: 12 points, 0–12,000 ns (linear) — full v4.1 resolution.

Physicality assertion (preregistered): every nonzero-delay circuit must contain native rx after transpilation or the run aborts before submission; operation counts logged and published.

Total: 72 circuits (12 delays × 6 rotations), all six conditions in parallel per circuit.

---

### Randomization

All 72 circuits executed in an order randomized by fixed, recorded seed 20260710 (implemented in the attached script; executed order written to the results file). Randomization is over execution order, the channel through which calibration drift could enter; within each circuit all six conditions execute simultaneously on parallel qubits, so drift affects all conditions of a circuit identically by construction. PR-arm per-pulse phases are drawn from seed 20260711 (SEED+1), fixed and reproducible.

---

### Data collection procedures

6,000 shots per circuit (432,000 total shots; each shot measures all six conditions in parallel). No confirmatory data exist at registration; prior executions are the attached synthetic calibration, non-evidential. Hardware: an IBM Heron-class backend with native fractional gates and ≥6 operational qubits, selected as least-busy among non-fez devices; device name, calibration snapshot, physicality log, and executed order recorded and reported. One session is the confirmatory dataset; a single preregistered escalation (double shots) exists for an inconclusive result.

---

### Sample size

6,000 shots per circuit; 72 circuits (12 delays × 6 rotations); 432,000 total shots in the confirmatory session. If escalation is triggered, one additional session at 12,000 shots per circuit (864,000 shots), for a maximum of 1,296,000 shots.

---

### Sample size rationale

The design reproduces v4.1's statistical power on its primary contrast, with the control strengthened from a four-condition mean to a symmetric two-neighbor mean at 12-point grid resolution. Attached synthetic calibration (fringe-realistic, per-qubit T2 heterogeneity 3–30 µs, detunings 5–120 kHz): null G_rep = +0.01% [−0.77%, +0.83%] → NOT_REPLICATED; half-v4.1-sized effect → +1.63% [+0.86%, +2.49%] → REPLICATED; v4.1-sized effect → +3.15% [+2.37%, +3.94%] → REPLICATED. Both decision categories resolve correctly, including at half the target effect size, within IBM open-tier session limits. The escalation tier exists for a marginal result near +0.9%.

---

### Starting and stopping rules

Starting rule: (1) registration frozen on OSF; (2) qrt5_escalation_test.py attached, seed fixed, SHA-256 recorded in the registration; (3) a non-fez fractional-gate backend selected and calibration snapshot captured; (4) all nonzero-delay circuits pass the physicality assertion. First hardware shot defines study start. Pre-freeze executions do not count and would be disclosed (none planned beyond the attached synthetic checks).

Normal stop: one full session, 72 circuits × 6,000 shots; decision applied once after all counts collected; no interim analyses.

Escalation (single use): if the CI spans +0.9%, one session at 12,000 shots per circuit within 14 days, same backend, fresh calibration snapshot, re-passed physicality assertion; decision applied to the escalation dataset alone; a second inconclusive terminates the study as inconclusive with both datasets published.

Abort conditions: physicality failure at transpilation (pre-submission, costs nothing); mid-session recalibration; >10% job errors; decommission. Aborted sessions published in full, excluded from confirmatory analysis, do not consume escalation.

Nothing else can stop the study: no data peeking, no author discretion, no reaction to partial results.

---

### Manipulated variables

Within the driven conditions: frequency (9, 10, 11 MHz at 1×R0 — the primary factor), amplitude scale (1× vs 10× at 10 MHz — secondary), and phase coherence (deterministic vs per-pulse randomized at 10 MHz, 1× — secondary), with pulse count, scheduling, and qubit identity held fixed. Condition-to-qubit assignment fully crossed by the 6-fold rotation. Undriven REF descriptive.

---

### Measured variables

Raw six-bit counts per circuit (6,000 shots each; published in full); P(0) per condition per qubit per delay point via fixed bit-marginal extraction; envelope area A(condition, qubit) = trapezoidal integral of |P(0) − 0.5| over the 12-point grid (no fitting). Recorded covariates (not analyzed): backend calibration snapshot; physicality log; executed order; job timestamps.

---

### Indices

Primary: G_rep as defined in the hypotheses — the same-qubit paired difference contrast of the 10 MHz @ 1×R0 arm against the symmetric neighbor mean. Uncertainty: bootstrap 95% CI, 2,000 resamples redrawing every P(0) as a binomial proportion at observed rate and shot count, seed fixed in the attached script. G_rep and its CI are the sole inputs to the decision rule.

Secondary (descriptive only, no inferential weight): G_amp_10x (cross-device check of the v4.2 scaling exclusion); G_phase_rand; per-condition per-qubit areas; REF areas. These inform interpretation and any successor design; none can support or defeat a claim here, and this restriction applies to the narrative of the outcome report as well as its statistics.

No other indices; the difference-contrast form is preregistered because the folding bias of |P̂ − 0.5| is condition-independent within a qubit and cancels in differences.

---

### Statistical models

No statistical model in the confirmatory path: areas are fixed arithmetic; G_rep is a ratio of sums; the bootstrap is nonparametric.

Decision rule: REPLICATED_ON_SECOND_DEVICE if G_rep ≥ +0.9% and CI lower bound > 0 → outcome: the paper's point claim survives a second device at confirmatory power; no claim is made; the preregistered next step is independent-party verification (protocol and data handed to a third party for execution without the author in the loop). NOT_REPLICATED if CI upper bound < +0.9% → outcome: the v4.1 result is attributed to a device-specific or statistical artifact; the program's adjudication of QRT's coherence prediction at stated parameters closes negative. INCONCLUSIVE otherwise → single preregistered escalation.

---

### Transformations

Counts → per-qubit marginals → P(0) → |P(0) − 0.5| → trapezoidal integral → paired difference contrast. Nothing else. No mitigation, no DD, no twirling (disabled in options), no outlier handling, no smoothing, no normalization, no fitting. Gross hardware failure (any condition's τ = 0 point returning P(0) < 0.8) triggers the abort pathway.

---

### Inference criteria

Interval-based, on G_rep against 0 and +0.9%. H1 requires the point estimate at/above threshold and CI excluding zero; H0 requires CI upper bound below threshold — positive evidence of non-replication, not failure-to-reject. One confirmatory comparison; no multiplicity. H1 is directional; a significantly negative G_rep supports H0 for the decision and is reported descriptively. Nothing outside G_rep and its CI carries inferential weight — explicitly including all secondary indices, the v4.1 and v4.2 datasets, and aborted-session data — and this restriction binds the outcome report's narrative claims, not only its statistics.

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
- qrt5_escalation_test.py, SHA-256 e37fa996cbe2491dcdd02e1f8d4f72e5880838a72fd523c5697162ae12a267a7 — the script referenced by the Starting Rule.
- qrt5_calibration.json, SHA-256 28336337f5a2c774dff0f1d3d0065f08a3a771da93a5726eb5779169276a912f — the synthetic calibration from which the +0.9% threshold and power claims derive. The threshold is valid only with respect to the attached file matching this hash.

Any attached file not matching its recorded hash is not part of this registration.

Program record: Tests #1 and #2 (Bell fidelity, both drive forms) falsified as specified. v4 executed, verdict withdrawn as improperly derived (documented). v4.1 returned QRT_CONSISTENT_ESCALATE (G_A = +2.87% [+2.35%, +3.46%], ibm_fez). v4.2 (ibm_marrakesh) excluded the amplitude-scaling mechanism class (DOES_NOT_SCALE) and, per its own scope, left the point claim open. This study is the point claim's confirmatory adjudication and, in either direction, the program's closing act on this platform.

Known limitations: per-pulse amplitude (10⁻³ rad) is physical but small relative to pulse-calibration precision; declared, uncorrected. The drive is stroboscopic. The envelope-area index compresses the decay curve; the threshold is defined by the attached calibration mapping. This test binds the prediction at its stated parameters; a NOT_REPLICATED outcome closes the program's adjudication on this platform without exhausting the theory's parameter space, and says so.

Conflicts / Provenance: shared authorship of theory and test; AI-collaborative drafting (Claude, Anthropic); one live QRT-consistent result and one adverse escalation arm precede this study; one narrative overreach by the AI collaborator regarding v4.2's descriptive index is on record and corrected. The frozen decision rule, code-enforced second-device requirement, fitting-free index, seeded phase randomization, and hash-anchored calibration exist specifically to remove all parties' degrees of freedom in all directions.

---

### Attachments

- qrt5_escalation_test.py
- qrt5_calibration.json
