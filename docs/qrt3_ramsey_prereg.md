# OSF Preregistration #3 — Field-by-Field Draft
## QRT Ramsey/T2 Resonance Test

**Theory under test:** Quantum Resonance Theory (Anson 2024, DOI 10.5281/ZENODO.15105902)
**Prereg author:** Amber Anson, AmberContinuum Research
**Status:** Resource-constrained amendment — execution script updated after IBM runtime rejection/cancellation of the larger frozen design

This draft follows the structure of `docs/qrt2_osf_fields.md`, but targets the
source paper's most explicit quantum-computing prediction: a 5-10% coherence
increase under a 10 MHz resonance drive, tested with Ramsey/T2-style circuits.

---

### Title

Preregistered Ramsey Test of Quantum Resonance Theory's 10 MHz Coherence Prediction on Superconducting Quantum Hardware

---

### Description

Quantum Resonance Theory (QRT; Anson 2024, DOI 10.5281/ZENODO.15105902) predicts that resonance extends superconducting-qubit coherence: the source paper states that T2 should rise by 5-10% at wr = 10 MHz and identifies Ramsey interferometry as the appropriate quantum-computing test. The paper also gives a phase-amplitude form R(t) = R0 cos(wr t), with R0 approximately 10^-3 rad, and a Hamiltonian perturbation form H(t) = H0 + V0 cos(wr t), with V0 approximately 10^-3 eV.

Two prior preregistered Bell-state tests were informative but implementation-limited. Test #1 used virtual RZ phase rotations and, at the theory-designated 10 MHz point, sampled the sine drive at zero crossings. Test #2 used physical fractional RX pulses and compared frequency structure across driven arms, but its stroboscopic schedule was still a discrete approximation near the Nyquist boundary rather than the continuous perturbation described in the source paper. This study is therefore a new, non-rescue preregistration focused on the paper's explicit Ramsey/T2 prediction rather than on the prior Bell-fidelity operationalization.

This study tests whether a 10 MHz physically delivered periodic drive improves Ramsey coherence relative to matched off-resonance and no-drive controls. The physical-drive implementation follows the Test #2 correction in kind: the confirmatory hardware path uses native fractional RX pulses with `use_fractional_gates=True`, and it aborts if driven circuits transpile without native `rx` operations. The execution script will include a waveform audit before hardware submission: no confirmatory data collection begins unless the actual discrete schedule avoids zero-crossing lock-in, documents its effective frequency content, and samples the 10 MHz waveform with enough phase coverage to make the intended stimulus identifiable.

The result will be reported publicly regardless of outcome.

---

### Research Questions Or Hypotheses

H1 (QRT Ramsey/coherence form): A physically delivered 10 MHz resonance drive increases the fitted Ramsey coherence time T2* by at least +5% relative to matched controls, with a 95% confidence interval excluding 0. A +5% threshold is the lower edge of the paper's stated 5-10% coherence prediction.

H0 (standard quantum mechanics): A milliradian-scale periodic drive does not improve Ramsey coherence; the 95% confidence interval upper bound on the 10 MHz relative T2* gain is below +5%.

Primary contrast:

G_T2 = T2*(10 MHz driven) / mean(T2*(controls)) - 1

Controls include an undriven Ramsey condition and off-resonance driven conditions. The frozen script uses off-resonance controls at 1, 5, 15, and 25 MHz, selected to avoid the clearest alias traps identified in the earlier review, subject to the waveform audit's aliasing constraints.

---

### Foreknowledge Of Data Or Evidence

No data for this Ramsey/T2 confirmatory test exist at the time of this draft. Prior Bell-test hardware datasets exist and motivated this design, but they do not test the same primary endpoint and will not be analyzed as part of this preregistered Ramsey study.

Prior knowledge used to shape this preregistration:

- The source paper explicitly names a 5-10% T2 increase at 10 MHz and Ramsey interferometry.
- Test #1 showed that naive stroboscopic choices can accidentally eliminate the intended 10 MHz stimulus.
- Test #2 showed that physical fractional pulses are possible on IBM Heron-class hardware, but also that discrete sampling and aliasing must be audited before the result can be interpreted as a resonance-frequency test.

---

### Explanation Of Foreknowledge And Managing Unintended Influences

The theory under test and this preregistration share an author. The protocol is being drafted after two prior falsifying Bell-test results and after identifying implementation limitations in those tests. This creates incentives in both directions: an incentive to rescue the theory by moving to a cleaner operationalization, and an incentive to complete a stronger falsification.

These incentives are managed structurally. The claim, endpoint, waveform-audit criteria, starting rule, stopping rule, analysis script, randomization seed, and decision rule will be frozen before any confirmatory hardware execution. Any post-hoc movement of frequency, amplitude, endpoint, exclusion criteria, fitting window, or decision threshold will be labeled as exploratory and cannot alter the confirmatory verdict.

---

### Study Type

Randomized Experiment: quantum-circuit execution order is randomized across conditions and Ramsey delay points to control calibration drift and queue-time artifacts.

---

### Intention For Causal Interpretation

Direct inference on causal relationship(s). The study is designed to estimate whether the manipulated drive condition causes a change in Ramsey coherence. Because the same backend, qubit selection procedure, Ramsey delays, fitting model, shot count, and execution session are used across conditions, and because execution order is randomized, the primary planned alternative explanation is calibration drift rather than uncontrolled condition assignment.

---

### Blinding Of Experimental Treatments

No blinding is involved. Treatment labels are embedded in the scripted circuits. The analysis is fully scripted, and the confirmatory decision rule is applied once after all planned circuits complete.

---

### Study Design

Single-qubit Ramsey/T2-style experiment on an IBM superconducting backend supporting the required physical drive implementation.

Preparation and measurement:

- Prepare |0>.
- Apply H or equivalent pi/2 preparation pulse to place the qubit on the equator.
- Insert a variable Ramsey delay tau.
- During the delay, apply the assigned drive schedule for that condition.
- Apply the final pi/2 analysis pulse.
- Measure in the computational basis.

Conditions:

- Theory-designated resonance drive: 10 MHz.
- Off-resonance driven controls: the frozen script uses 1, 5, 15, and 25 MHz, finalized by the uploaded script and subject to the waveform audit showing they are not aliased into misleadingly equivalent discrete schedules.
- Undriven reference: identical Ramsey delays with no resonance drive.

Ramsey delays:

- The amended script uses 15 tau values linearly spaced from 0 ns to 12,000 ns.
- This grid is fixed before confirmatory execution; no fitting-window selection occurs after seeing data.
- If hardware duration constraints prevent this grid from running, the session aborts before confirmatory data collection and any revised grid requires a new script hash or disclosed amendment before execution.

Drive implementation:

- Preferred implementation is a physically delivered periodic perturbation, not a virtual frame update.
- The current IBM hardware path implements the drive with native fractional RX pulses, matching Test #2's physical-drive correction rather than Test #1's virtual RZ frame-update implementation.
- If only discrete fractional gates are available, the schedule must be audited before execution and reported as a discrete approximation to the source paper's continuous perturbation.
- The schedule must not sample the 10 MHz waveform only at zero crossings or at phase-equivalent points.

Waveform audit, required before confirmatory submission:

- Record the scheduled sample times for each drive condition.
- Record the drive amplitudes/angles applied at each sample.
- Compute and save the effective discrete waveform, RMS amplitude, maximum absolute amplitude, phase coverage, and frequency/alias diagnostics.
- Abort before hardware submission if the 10 MHz schedule has near-zero RMS amplitude, inadequate phase coverage, or aliases to the same discrete sequence as a control condition.

---

### Randomization

All circuits are executed in a randomized order with a fixed, recorded seed. Randomization crosses condition and Ramsey delay so that calibration drift cannot systematically favor the 10 MHz condition or a particular portion of the decay curve.

The executed order is saved in the results file. The randomization seed will be frozen in the execution script before registration.

---

### Data Collection Procedures

Hardware:

- IBM superconducting backend selected before execution by a frozen rule, preferably least-busy among devices satisfying the required drive and timing constraints.
- Backend name, qubit index, calibration snapshot, T1, T2, readout error, gate errors, timing granularity, and supported basis/fractional gates will be saved before execution.

Shots:

- Amended frozen value: 19,500 shots per circuit, reduced from 32,000 after IBM estimated the original design above the available Open Plan runtime.

Data:

- Raw counts for each condition and Ramsey delay.
- Executed order.
- Transpiled circuit summaries.
- Waveform-audit file.
- Calibration snapshot.

No measurement-error mitigation, dynamical decoupling, twirling, zero-noise extrapolation, outlier removal, smoothing, or post-hoc fitting-window selection is applied in the confirmatory analysis.

---

### Sample Size

The amended sample size is fixed in the uploaded execution script.

Planned structure:

- Conditions: 1 resonance condition, 4 off-resonance driven controls, 1 undriven reference.
- Ramsey delays: 15 tau points, linearly spaced from 0 ns to 12,000 ns.
- Shots: planned 19,500 per circuit.

At 6 conditions x 15 delay points x 19,500 shots, the amended session contains 1,755,000 shots. This preserves the original conditions, physical-drive implementation, endpoint, model, and decision rule while reducing runtime enough to fit IBM Open Plan constraints.

---

### Sample Size Rationale

The paper's predicted coherence effect is large by Ramsey standards: +5-10% in T2. The design aims to resolve the lower bound of that prediction, +5%, rather than merely detect any nonzero effect.

The initial synthetic power check at 8,000 shots per circuit was too wide to separate the null from the +5% decision threshold. At 32,000 shots per circuit, the deterministic synthetic null produced G_T2 = +0.00% with a 95% CI of approximately [-2.92%, +2.99%], while a synthetic +5% effect produced G_T2 = +5.01% with a 95% CI of approximately [+1.90%, +8.21%]. IBM estimated that design above the available runtime. The amended 19,500-shot, 15-delay design is a resource-constrained coding/platform adaptation, not a hypothesis change.

Amended synthetic checks at 19,500 shots and 15 tau points:

- Null synthetic: G_T2 = +0.00%, 95% CI approximately [-5.36%, +4.95%], decision = falsified as specified.
- +5% synthetic effect: G_T2 = +5.03%, 95% CI approximately [-0.83%, +10.59%], decision = inconclusive.
- +6% synthetic effect: G_T2 = +6.02%, 95% CI approximately [+0.82%, +11.20%], decision = QRT-consistent escalation.

The simulator/power check is a design calibration only. It carries no evidential weight for QRT because it implements standard quantum mechanics by construction.

---

### Starting And Stopping Rules

Starting rule. Data collection begins only after all of the following are satisfied:

1. This preregistration is frozen.
2. The execution and analysis script is attached with a recorded SHA-256 hash.
3. Backend selection is complete and the calibration snapshot is saved.
4. The waveform audit passes for all driven conditions.
5. The transpiled circuits satisfy the physicality criteria declared in the execution script.

Normal stopping rule. The confirmatory dataset is exactly one completed randomized session containing all planned conditions, delays, and shots. The analysis is run once after the session completes.

Inconclusive escalation. If the 95% CI on G_T2 spans the +5% decision boundary, one preregistered double-shot rerun may be performed on the same backend within 14 days, with a fresh calibration snapshot and a new waveform audit. The escalation dataset is analyzed alone. No further escalations are permitted.

Abort conditions. A session is aborted and rerun in full if the waveform audit fails, physicality criteria fail, backend recalibration interrupts execution, more than 10% of jobs fail, the selected backend is decommissioned, or any permanent missing cell occurs. Aborted-session data are published but excluded from confirmatory analysis.

What cannot stop the study. Interim results, disappointing or exciting partial counts, author discretion, or post-hoc concern about the outcome cannot stop or alter the study.

---

### Manipulated Variables

Primary manipulated variable: drive condition during the Ramsey delay.

Levels:

- 10 MHz physical drive, the theory-designated resonance condition.
- Off-resonance physical drives, finalized before registration subject to aliasing/waveform constraints.
- Undriven reference.

Secondary design variable: Ramsey delay tau, fixed by the preregistered grid and used to estimate T2*.

Amplitude:

- Initial target is R0 = 10^-3 rad, matching the source paper's phase-amplitude parameter.
- If hardware constraints require a different calibrated physical-amplitude representation, the conversion and rationale must be documented before registration. A changed amplitude is a new parameterization and must not be described as identical to the earlier Bell tests.

---

### Measured Variables

Primitive data:

- Raw counts for outcome 0 and outcome 1 for each condition and Ramsey delay.

Derived quantities:

- Excited-state or ground-state probability as a function of tau.
- Fitted Ramsey coherence time T2* per condition.
- Relative T2* gain G_T2 for the 10 MHz condition against the preregistered control aggregate.

Recorded covariates:

- Backend identity and calibration.
- Qubit index.
- Actual transpiled durations.
- Actual scheduled drive sample times and amplitudes.
- Discrete-waveform audit diagnostics.
- Job IDs and timestamps.
- Executed random order.

---

### Indices

Primary index:

G_T2 = T2*(10 MHz) / mean(T2*(controls)) - 1

The control aggregate will include the off-resonance driven controls and may include the undriven reference only if this is declared in the frozen script before registration. The default planned primary control aggregate is the mean of off-resonance driven controls, with the undriven reference reported descriptively, because driven controls better cancel pulse-induced degradation.

Secondary descriptive indices:

- T2* for each condition.
- 10 MHz versus undriven relative T2* gain.
- Per-condition fitted amplitude, offset, and Ramsey frequency/detuning.
- Waveform RMS and phase-coverage diagnostics.

Only G_T2 carries confirmatory inferential weight.

---

### Statistical Models

For each condition, fit the fixed exponential Ramsey/T2-style decay model used by the uploaded script to the observed probabilities:

P(tau) = C + A exp(-tau / T2*)

The exact fitting method, parameter bounds, initial values, and failure behavior are fixed in the uploaded execution script. The frozen script uses nonlinear least squares on probabilities derived from raw counts.

Uncertainty:

- Bootstrap resampling over binomial counts per delay point.
- Refit T2* for each condition on each bootstrap draw.
- Compute G_T2 for each bootstrap draw.
- Report the 2.5th and 97.5th percentiles as the 95% CI.

Decision rule:

- QRT-consistent: G_T2 >= +5% and the 95% CI excludes 0. Outcome: escalation, not final publication of a positive claim. Escalation requires independent replication, an amplitude sweep, and phase-randomized drive controls.
- Falsified as specified: 95% CI upper bound on G_T2 < +5%. Outcome: QRT's Ramsey/T2 prediction is reported as falsified under this physical-drive implementation at the preregistered parameters.
- Inconclusive: CI spans +5%. Outcome: one preregistered double-shot rerun, then report the result as inconclusive if the escalated dataset also spans the boundary.

No optional confirmatory analyses. Any alternate fit model, alternate control aggregate, alternate frequency set, or amplitude tuning after seeing data is exploratory.

---

### Transformations

Raw counts are transformed to probabilities by dividing counts by shots at each delay point. Probabilities are fit to the fixed Ramsey decay model. Fitted T2* values are transformed to the primary relative gain G_T2.

Explicitly excluded transformations:

- No readout-error correction.
- No zero-noise extrapolation.
- No probabilistic error cancellation.
- No smoothing of the Ramsey curve.
- No removal of delay points after seeing data.
- No post-hoc refitting with alternate models for the confirmatory verdict.

---

### Inference Criteria

Inference is interval-based. The primary 95% CI for G_T2 is compared against 0 and +5%.

Criterion for supporting H1:

- G_T2 point estimate is at least +5%.
- The 95% CI lower bound is greater than 0.

Criterion for supporting H0/falsification as specified:

- The 95% CI upper bound is below +5%.

Inconclusive:

- The 95% CI includes +5%.

Multiple comparisons:

- No correction is applied because one primary contrast is confirmatory.
- Per-frequency, per-delay, and waveform diagnostics are descriptive unless separately preregistered.

---

### Data Inclusion And Exclusion

All shots from a completed confirmatory session are included. There are no shot-level, delay-level, or condition-level exclusions.

The only exclusion unit is the full session. A session is excluded from confirmatory analysis only if it meets an abort condition listed above. Excluded sessions are archived and published as aborted, not mined for partial support.

---

### Missing Data

Shot-level missingness is not expected because the backend returns the requested number of shots or a job error. A failed job may be resubmitted identically if total failed jobs remain within the preregistered abort threshold. A permanent missing cell aborts the session.

No missing cell is imputed, interpolated, or filled from another session.

---

### Other Planned Analysis

None for confirmatory inference.

Exploratory analyses, if performed, will be labeled exploratory and cannot alter the confirmatory decision. Candidate exploratory checks include comparing 10 MHz directly against undriven Ramsey, inspecting fitted detuning shifts, and plotting residuals by delay point.

---

### Context And Additional Information

Relationship to prior tests:

- Test #1 tested a Bell-state fidelity prediction with virtual RZ phase modulation. A post-hoc audit identified that the 10 MHz drive schedule sampled zero crossings under the chosen 50 ns step, so the intended 10 MHz stimulus was not cleanly delivered.
- Test #2 tested physical fractional RX drive across frequencies. It was a stronger physical-drive test but remained a discrete approximation with aliasing/sampling limitations relative to the paper's continuous Hamiltonian term.
- This Test #3 is a new preregistration focused on the paper's explicit Ramsey/T2 prediction. It keeps Test #2's physical-drive correction while changing the endpoint to the source paper's Ramsey/T2 claim. It does not reinterpret the prior datasets and does not rescue their preregistered verdicts.

Resource-constrained amendment:

- The originally uploaded 32,000-shot, 25-delay design submitted to IBM as job `d93vf0tgc6cc73fefs5g` but was cancelled before counts were returned after IBM estimated runtime above the available Open Plan allocation.
- A 19,500-shot, 25-delay amended attempt submitted as job `d93vrmmvtlqs73ftmpig` was also cancelled before counts were returned, with IBM estimating approximately 11 minutes.
- The current amendment reduces tau points from 25 to 15 and keeps 19,500 shots per circuit. This reduces circuit count from 150 to 90 while preserving all drive conditions, the physical fractional-RX implementation, the waveform audit, the primary endpoint, and the decision rule.
- No counts were returned from the cancelled attempts. They are non-evidential resource/cancellation attempts, not confirmatory datasets.

Known limitations:

- IBM public hardware may not support a literal continuous 10 MHz tone through the circuit interface. If the implementation uses discrete pulses, the result binds that discrete approximation, not every possible continuous-drive realization.
- The paper gives both a phase amplitude R0 approximately 10^-3 rad and an energy perturbation V0 approximately 10^-3 eV. This preregistration initially targets the phase-amplitude form because it is implementable as quantum-circuit control. The V0 mapping is not adjudicated here unless a hardware-calibrated conversion is specified before freeze.
- Ramsey T2* can drift with calibration and environment. Randomization and same-session controls reduce but do not eliminate this limitation.

Conflicts/provenance:

The theory under test and this preregistration share an author. The draft was prepared with AI assistance. The purpose of this registration is to make the next test harder to fool in either direction: no accidental zero-drive schedules, no post-hoc threshold migration, and no unstated equivalence between a runnable circuit and the source paper's continuous perturbation.

---

### Attachments To Upload With Registration

Uploaded or recorded before freeze:

- `tests/qrt3_ramsey_test.py` frozen execution/analysis script.
- SHA-256: `36afe14a2a8f2147a81b66fcfec123b3402a239a95ea170a9146c62b53acfbb0`
- Simulator/power-check output, labeled non-evidential.
- Waveform-audit output from the frozen script before hardware execution.
