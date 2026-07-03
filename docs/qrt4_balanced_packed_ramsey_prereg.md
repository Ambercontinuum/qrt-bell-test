# OSF Preregistration #4 - Field-by-Field Draft
## Balanced Packed Ramsey/T2 Test of QRT's 10 MHz Coherence Prediction

**Theory under test:** Quantum Resonance Theory (Anson 2024, DOI 10.5281/ZENODO.15105902)  
**Prereg author:** Amber Anson, AmberContinuum Research  
**Status:** New registration draft for the balanced packed execution design

---

### Title

Preregistered Balanced Packed Ramsey Test of Quantum Resonance Theory's 10 MHz Coherence Prediction on Superconducting Quantum Hardware

---

### Description

Quantum Resonance Theory predicts that superconducting-qubit coherence should increase by 5-10% at wr = 10 MHz, with Ramsey interferometry identified as the appropriate quantum-computing test. This registration tests that same substantive claim using a revised execution design.

The prior Ramsey preregistration used a serial circuit layout: one condition and one Ramsey delay per circuit. IBM runtime estimates made that layout difficult to execute within the available public allocation. This new registration uses a balanced packed layout: all six drive conditions are measured in parallel within each Ramsey-delay circuit, and the condition-to-qubit assignment is rotated across two planned repetitions to reduce fixed-qubit-position confounding.

The hypothesis, waveform audit, physical fractional-RX drive implementation, T2* endpoint, fit model, control aggregate, and decision rule remain aligned with the prior Ramsey registration. The execution methodology is different enough that this is a new preregistration, not an amendment.

The result will be reported publicly regardless of outcome.

---

### Research Questions Or Hypotheses

H1: A physically delivered 10 MHz resonance drive increases fitted Ramsey coherence time T2* by at least +5% relative to matched off-resonance driven controls, with the 95% confidence interval excluding 0.

H0: A milliradian-scale periodic drive does not improve Ramsey coherence; the 95% confidence interval upper bound on the 10 MHz relative T2* gain is below +5%.

Primary contrast:

G_T2 = T2*(10 MHz driven) / mean(T2*(off-resonance driven controls)) - 1

Off-resonance controls are 1, 5, 15, and 25 MHz. The undriven Ramsey reference is measured and reported descriptively.

---

### Foreknowledge Of Data Or Evidence

No confirmatory hardware counts exist for this balanced packed Ramsey design at the time of registration. Prior Bell-test datasets and cancelled IBM Ramsey attempts motivated the design, but they are not analyzed as confirmatory evidence for this registration.

Cancelled IBM attempts:

- `d93vf0tgc6cc73fefs5g`: 32,000-shot, 25-delay serial design, cancelled before counts.
- `d93vrmmvtlqs73ftmpig`: 19,500-shot, 25-delay serial design, cancelled before counts.

These attempts are non-evidential because no counts were returned.

---

### Explanation Of Foreknowledge And Managing Unintended Influences

The theory under test and this preregistration share an author. This creates an incentive to rescue the theory after falsifying or implementation-limited prior tests, and an opposing incentive to complete a cleaner falsification. The protocol manages this by freezing the hypothesis, endpoint, waveform audit, execution design, seed, analysis script, and decision rule before confirmatory hardware counts are collected.

Any later change to frequency set, amplitude, delay grid, condition packing, assignment rotations, endpoint, fit model, confidence rule, or threshold is exploratory unless separately preregistered before new confirmatory execution.

---

### Study Type

Randomized experiment on superconducting quantum hardware.

---

### Study Design

Single-qubit Ramsey/T2-style experiment executed in a packed multi-qubit layout.

For each Ramsey delay tau, one circuit contains all six conditions in parallel:

- 10 MHz driven resonance condition.
- 1, 5, 15, and 25 MHz driven off-resonance controls.
- Undriven Ramsey reference.

Each condition is assigned to one qubit in the packed circuit. The design uses two balanced assignment repetitions. The second repetition rotates condition-to-qubit assignment so that the 10 MHz condition is not tied to one fixed qubit position.

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

---

### Randomization

The packed circuits are randomized across Ramsey delay and balanced assignment repetition using the frozen seed in the uploaded script. The executed order is saved.

---

### Data Collection Procedures

Hardware:

- IBM superconducting backend selected before execution by the frozen script, preferably least-busy among devices satisfying required qubit count and fractional-gate constraints.
- Backend name, calibration snapshot, qubit indices, T1, T2, readout error, gate errors, timing granularity, and supported basis/fractional gates are saved when available.

Shots:

- 19,500 shots per packed circuit.
- Two balanced assignment repetitions.
- Effective planned marginal observations per condition-delay cell: 39,000 shots.

Data:

- Raw packed bitstring counts for each submitted circuit.
- Reduced per-condition marginal counts.
- Executed order and assignment map.
- Transpiled circuit summaries.
- Waveform-audit file.
- Calibration snapshot.

No measurement-error mitigation, dynamical decoupling, twirling, zero-noise extrapolation, outlier removal, smoothing, or post-hoc fitting-window selection is applied in the confirmatory analysis.

---

### Sample Size

Planned structure:

- Conditions: 6.
- Ramsey delays: 15.
- Balanced assignment repetitions: 2.
- IBM PUBs: 30.
- Shots per PUB: 19,500.
- Circuit shots submitted: 585,000.
- Condition-level marginal observations used for fitting: 3,510,000.

This design reduces IBM PUB count while preserving the same frequencies, delay grid, physical-drive implementation, endpoint, fit model, and decision threshold.

---

### Sample Size Rationale

Synthetic checks are non-evidential and used only to verify analysis behavior.

For the balanced packed default at 19,500 shots, 15 tau points, and 2 assignment repetitions:

- Null synthetic: G_T2 = +0.00%, 95% CI approximately [-3.11%, +3.25%], decision = falsified as specified.
- +5% synthetic effect: G_T2 = +4.99%, 95% CI approximately [+1.30%, +8.39%], decision = inconclusive under the strict threshold rule.
- +6% synthetic effect: G_T2 = +6.00%, 95% CI approximately [+2.37%, +9.75%], decision = QRT-consistent escalation.

---

### Starting And Stopping Rules

Starting rule. Data collection begins only after:

1. This preregistration is frozen.
2. The execution and analysis script is attached with a recorded SHA-256 hash.
3. Backend selection is complete and calibration snapshot is saved.
4. The waveform audit passes.
5. Transpiled circuits satisfy the physicality criteria.

Normal stopping rule. The confirmatory dataset is one completed randomized session containing all planned delays, assignment repetitions, conditions, and shots.

Abort conditions. A session is aborted and rerun in full if the waveform audit fails, physicality criteria fail, backend recalibration interrupts execution, more than 10% of jobs fail, the backend is decommissioned, or any permanent missing condition-delay cell occurs.

Inconclusive escalation. If the 95% CI on G_T2 spans the +5% boundary, one preregistered double-shot rerun may be performed on the same backend within 14 days. The escalation dataset is analyzed alone.

---

### Manipulated Variables

Primary manipulated variable: drive condition during the Ramsey delay.

Levels:

- 10 MHz physical drive.
- 1, 5, 15, and 25 MHz physical drives.
- Undriven reference.

Secondary design variables:

- Ramsey delay tau.
- Balanced condition-to-qubit assignment repetition.

---

### Measured Variables

Primitive data:

- Packed raw bitstring counts per circuit.
- Per-condition marginal counts for outcome 0 and outcome 1 at each delay.

Derived quantities:

- Probability of outcome 0 as a function of tau.
- Fitted T2* per condition.
- Relative T2* gain G_T2.

Recorded covariates:

- Backend identity and calibration.
- Qubit indices and condition-to-qubit assignments.
- Transpiled operations and depth.
- Waveform diagnostics.
- Job IDs and timestamps.

---

### Statistical Models

For each condition, fit:

P(tau) = C + A exp(-tau / T2*)

The uploaded script fixes the nonlinear least-squares method, parameter bounds, initial values, bootstrap method, and failure behavior.

Uncertainty:

- Bootstrap resampling over binomial counts per delay point.
- Refit T2* for each condition on each bootstrap draw.
- Compute G_T2 for each bootstrap draw.
- Report 2.5th and 97.5th percentiles as the 95% CI.

Decision rule:

- QRT-consistent escalation: G_T2 >= +5% and 95% CI lower bound > 0.
- Falsified as specified: 95% CI upper bound on G_T2 < +5%.
- Inconclusive: CI spans +5%.

---

### Transformations

Packed bitstring counts are reduced to single-qubit marginal counts for each assigned condition. Marginal counts are divided by shots to produce probabilities. Fitted T2* values are transformed into G_T2.

No readout-error correction, smoothing, delay removal, alternate control aggregate, or alternate fit model is used for the confirmatory verdict.

---

### Data Inclusion And Exclusion

All shots from a completed confirmatory session are included. There are no shot-level, delay-level, or condition-level exclusions.

The only exclusion unit is the full session under the abort conditions above. Excluded sessions are archived and published as aborted.

---

### Missing Data

No missing cell is imputed, interpolated, or filled from another session. A permanent missing condition-delay cell aborts the session.

---

### Other Planned Analysis

None for confirmatory inference. Any alternate analyses are exploratory and cannot alter the confirmatory decision.

---

### Context And Additional Information

This registration differs from the prior Ramsey registration in execution layout. The prior design was serial: one condition-delay cell per circuit. This design is packed: all six conditions are measured within each delay circuit, with two balanced assignment repetitions.

The scientific claim and confirmatory analysis are otherwise intentionally preserved: same theory prediction, same 10 MHz resonance condition, same off-resonance controls, same tau grid, same physical fractional-RX drive strategy, same waveform audit, same T2* model, same primary contrast, and same decision rule.

Known limitation: because conditions are measured on different qubits within a packed circuit, residual qubit-to-qubit calibration differences may affect estimates. The balanced assignment repetitions reduce but do not eliminate this risk.

---

### Attachments To Upload With Registration

Uploaded or recorded before freeze:

- `tests/qrt_ramsey_test.py` frozen execution/analysis script.
- SHA-256: `a6d79659ade2afba6ce95f40c3db7b583d958da75795815095a0667ae076e41f`
- Simulator/power-check output, labeled non-evidential.
- Waveform-audit output from the frozen script before hardware execution.
