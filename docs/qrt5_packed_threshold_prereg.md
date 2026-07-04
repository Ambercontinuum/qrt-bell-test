# OSF Preregistration #5 - Field-by-Field Draft
## Packed-State Threshold Test Following QRT4

**Theory/phenomenon under test:** exploratory packed-state threshold/correlation structure observed after QRT4  
**Prereg author:** Amber Anson, AmberContinuum Research  
**Status:** new confirmatory registration draft for packed joint-state transition endpoint

---

### Title

Preregistered Packed-State Threshold Test of QRT4's Joint Readout Transition Signal on IBM Superconducting Hardware

---

### Description

QRT4 falsified the preregistered 10 MHz T2* coherence-gain endpoint. However, its packed Ramsey readout produced a structured tau-dependent joint-state population wave. The most prominent exploratory packed bitstring was `011001`, which rose from near zero, peaked in the mid-delay region, and declined or gave way to other joint states.

This QRT5 registration does not reinterpret QRT4 as positive. It tests a new claim: whether the packed bitstring `011001` exhibits a reproducible threshold-like population transition across balanced assignment repetitions in a new hardware run.

The endpoint is joint-state population geometry, not single-condition T2* gain. The result will be reported publicly regardless of outcome.

---

### Research Questions Or Hypotheses

H1: The packed bitstring `011001` exhibits a reproducible tau-localized threshold-like population transition across both balanced assignment repetitions.

H0: The packed bitstring `011001` does not show a reproducible threshold-like transition under the preregistered peak, lift, and assignment-repetition criteria.

Primary quantities:

- `p_r(tau)`: probability of packed bitstring `011001` at delay tau in assignment repetition r.
- `peak_prob_r`: maximum `p_r(tau)` over the frozen tau grid.
- `edge_prob_r`: larger of the early-edge mean and late-edge mean, where each edge mean uses three tau points.
- `lift_r = peak_prob_r - edge_prob_r`.
- `min_peak_prob = min_r(peak_prob_r)`.
- `min_lift_from_edge = min_r(lift_r)`.
- `peak_tau_span_ns = max_r(peak_tau_r) - min_r(peak_tau_r)`.

Confirmatory success requires the same target state to peak strongly in both assignment repetitions, with peak locations close in tau.

---

### Foreknowledge Of Data Or Evidence

No QRT5 hardware data exist at the time of this registration.

QRT4 data exist and motivated this new endpoint. QRT4 is not used as confirmatory evidence for QRT5. It is prior exploratory evidence used to choose:

- the packed-state endpoint,
- target bitstring `011001`,
- the same tau grid,
- the same balanced packed circuit family,
- and the target backend family, preferably `ibm_marrakesh`.

QRT4's confirmatory verdict remains falsified as specified for its T2* endpoint.

---

### Explanation Of Foreknowledge And Managing Unintended Influences

The target state `011001` and threshold-style endpoint were selected after inspecting QRT4. This makes QRT5 a new confirmatory test, not a post-hoc reinterpretation of QRT4.

The target state, tau grid, assignment repetitions, backend rule, script, random seed, peak/lift thresholds, bootstrap rules, and decision criteria are frozen before QRT5 hardware execution. Any later change to target state, tau grid, backend, assignment mapping, bit-order convention, threshold values, or decision rule is exploratory unless separately preregistered before new execution.

---

### Study Type

Randomized experiment on superconducting quantum hardware.

---

### Intention For Causal Interpretation

Direct inference on causal relationship(s) is limited. The study tests whether a specific packed joint-state transition reproducibly appears under a fixed circuit construction and backend context. It is not designed to prove a universal physical mechanism by itself. If replicated, causal interpretation would require follow-up controls separating drive-frequency effects, qubit geometry, readout correlations, and backend-specific calibration.

---

### Blinding Of Experimental Treatments

No blinding is involved. The target bitstring and assignment maps are embedded in the frozen analysis script. The confirmatory decision rule is applied once after all planned counts return.

---

### Study Design

Packed multi-qubit Ramsey-style experiment on IBM superconducting hardware.

For each Ramsey delay tau, one circuit contains all six conditions in parallel:

- 10 MHz driven condition.
- 1, 5, 15, and 25 MHz driven conditions.
- Undriven reference.

The design uses two balanced assignment repetitions. The second repetition rotates condition-to-qubit assignment so the target bitstring can be tested for reproducibility across assignment labels.

Preparation and measurement for each condition/qubit:

- Prepare |0>.
- Apply H.
- Insert Ramsey delay tau.
- During the delay, apply the assigned fractional-RX drive schedule when driven.
- Apply final H.
- Measure in the computational basis.

Ramsey delays:

- 15 tau values linearly spaced from 0 ns to 12,000 ns.

Drive implementation:

- Physical fractional RX pulses with `use_fractional_gates=True`.
- The hardware path aborts if driven circuits transpile without native `rx` operations.
- A waveform audit must pass before hardware submission.

Backend:

- Confirmatory backend target is `ibm_marrakesh`, matching the QRT4 exploratory origin.
- If `ibm_marrakesh` is unavailable, unavailable under fractional gates, or materially incompatible with the frozen script, the run aborts and a backend-specific registration is required before substituting another backend.

---

### Randomization

Packed circuits are randomized across Ramsey delay and balanced assignment repetition using the frozen seed `20260704`. The executed order is saved.

---

### Data Collection Procedures

Hardware:

- IBM superconducting backend `ibm_marrakesh`.
- Backend name, calibration snapshot, qubit indices, T1, T2, readout error, gate errors, timing granularity, and supported basis/fractional gates are saved when available.

Shots:

- 19,500 shots per packed circuit.
- Two balanced assignment repetitions.

Data:

- Raw packed bitstring counts for each submitted circuit.
- Executed order and assignment map.
- Transpiled circuit summaries.
- Waveform-audit file.
- Calibration snapshot.

No measurement-error mitigation, dynamical decoupling, twirling, zero-noise extrapolation, smoothing, state merging, target-state switching, tau-window selection, or post-hoc bit-order reinterpretation is applied in the confirmatory analysis.

---

### Sample Size

Planned structure:

- Conditions inside each packed circuit: 6.
- Ramsey delays: 15.
- Balanced assignment repetitions: 2.
- IBM PUBs: 30.
- Shots per PUB: 19,500.
- Circuit shots submitted: 585,000.

The target-state probability is estimated separately for each tau and assignment repetition from packed bitstring counts.

---

### Sample Size Rationale

QRT4 observed the target state at approximately 30% peak probability in both assignment repetitions. QRT5 uses the same 19,500 shots per PUB so that a replicated peak at or near that scale should be far above binomial sampling noise.

Synthetic pipeline checks are non-evidential and verify only that the frozen analysis detects an injected threshold-like target-state population wave.

---

### Starting And Stopping Rules

Starting rule. Data collection begins only after:

1. This preregistration is frozen.
2. `tests/qrt5_packed_threshold_test.py` is attached with SHA-256 recorded.
3. Backend selection confirms `ibm_marrakesh`.
4. Calibration snapshot is saved.
5. Waveform audit passes.
6. Transpiled circuits satisfy physicality criteria.

Normal stopping rule. The confirmatory dataset is exactly one completed randomized session containing all 30 planned PUBs at 19,500 shots per PUB.

Abort conditions. A session is aborted and rerun in full if the waveform audit fails, physicality criteria fail, backend recalibration interrupts execution, more than 10% of jobs fail, the backend is decommissioned, `ibm_marrakesh` is unavailable, or any permanent missing tau/assignment cell occurs.

What cannot stop the study. Interim results, dashboard visualizations, exciting or disappointing partial counts, or author discretion cannot stop or alter the confirmatory analysis.

---

### Manipulated Variables

Primary manipulated/design variables:

- Ramsey delay tau.
- Balanced assignment repetition.

Embedded drive conditions:

- 10 MHz, 1 MHz, 5 MHz, 15 MHz, 25 MHz, and undriven reference.

The confirmatory endpoint is not a 10 MHz-vs-control T2* contrast. It is the packed population trajectory of target bitstring `011001`.

---

### Measured Variables

Primitive data:

- Raw packed bitstring counts per circuit.

Derived quantities:

- `p_r(tau)` for target state `011001`.
- Peak probability per assignment repetition.
- Edge probability per assignment repetition.
- Lift from edge per assignment repetition.
- Peak tau per assignment repetition.
- Minimum peak probability across repetitions.
- Minimum lift from edge across repetitions.
- Peak tau span across repetitions.

Recorded covariates:

- Backend identity and calibration.
- Qubit indices and condition-to-qubit assignments.
- Transpiled operations and depth.
- Waveform diagnostics.
- Job ID and timestamps.

---

### Indices

Primary indices:

- `min_peak_prob`.
- `min_lift_from_edge`.
- `peak_tau_span_ns`.

Definitions:

- `peak_prob_r = max_tau p_r(tau)`.
- `edge_prob_r = max(mean(p_r(first three tau points)), mean(p_r(last three tau points)))`.
- `lift_r = peak_prob_r - edge_prob_r`.
- `min_peak_prob = min_r(peak_prob_r)`.
- `min_lift_from_edge = min_r(lift_r)`.
- `peak_tau_span_ns = max_r(peak_tau_r) - min_r(peak_tau_r)`.

Secondary descriptive indices:

- Full target-state probability curve by tau and repetition.
- Top packed states by tau.
- Entropy or concentration of packed-state distributions.
- Assignment-specific state trajectories.

Only the primary indices enter the confirmatory decision rule.

---

### Statistical Models

No T2* model is fit for QRT5's confirmatory endpoint.

For each tau and assignment repetition, target-state probability is:

```text
p_r(tau) = count(011001 at tau, repetition r) / total shots at tau, repetition r
```

Uncertainty:

- Bootstrap resampling over each packed circuit's multinomial bitstring counts.
- Recompute the full target-state trajectory and primary indices for each bootstrap draw.
- Report 2.5th and 97.5th percentiles for `min_peak_prob` and `min_lift_from_edge`.

Decision rule:

- `THRESHOLD_REPLICATED` if all are true:
  - observed `min_peak_prob >= 0.20`,
  - observed `min_lift_from_edge >= 0.15`,
  - observed `peak_tau_span_ns <= 1000`,
  - bootstrap 95% CI lower bound for `min_peak_prob >= 0.15`,
  - bootstrap 95% CI lower bound for `min_lift_from_edge >= 0.10`.
- `NO_REPLICATED_THRESHOLD` if bootstrap 95% CI upper bound for `min_peak_prob < 0.15` or bootstrap 95% CI upper bound for `min_lift_from_edge < 0.10`.
- Otherwise `INCONCLUSIVE`.

---

### Transformations

Raw packed bitstring counts are normalized to fixed six-bit strings using the bit-order convention in the frozen script. Counts for target state `011001` are divided by total shots at each tau and assignment repetition.

No target-state switching, smoothing, curve fitting, state aggregation, tau-window trimming, readout correction, or post-hoc bit-order reversal is permitted for the confirmatory verdict.

---

### Inference Criteria

Inference is interval-based and threshold-based. The target-state transition is considered replicated only if the observed peak/lift/tau-alignment criteria and bootstrap lower-bound criteria all pass.

This test does not support or refute the QRT4 T2* coherence-gain claim. It tests a new packed-state threshold endpoint motivated by QRT4's exploratory readout structure.

---

### Data Inclusion And Exclusion

All shots from a completed confirmatory session are included. There are no shot-level, tau-level, state-level, or assignment-level exclusions.

The only exclusion unit is the full session under the abort conditions above. Excluded sessions are archived and published as aborted.

---

### Missing Data

No missing cell is imputed, interpolated, or filled from another session. A permanent missing tau/assignment cell aborts the session.

---

### Other Planned Analysis

None for confirmatory inference.

Exploratory analyses, if performed, may inspect non-target bitstrings, entropy, backend calibration relationships, or qubit-geometry correlations. These cannot alter the confirmatory QRT5 decision.

---

### Context And Additional Information

QRT4 failed its preregistered 10 MHz T2* coherence-gain endpoint:

```text
G_T2 = -77.30%
95% CI = [-77.66%, -76.98%]
decision = FALSIFIED_AS_SPECIFIED
```

QRT4 also revealed a tau-localized packed bitstring structure, especially for `011001`. QRT5 is the new confirmatory test of that exploratory structure.

This registration therefore separates:

- QRT4 confirmatory failure, which stands as reported.
- QRT5 packed-state threshold hypothesis, which is new and must stand or fall on new data.

---

### Attachments To Upload With Registration

Uploaded or recorded before freeze:

- `tests/qrt5_packed_threshold_test.py` frozen execution/analysis script.
- SHA-256: `bc8502f40c9da0a987eec79ebef99ad0d704492b4fc3a205a08803acd091f4ab`
