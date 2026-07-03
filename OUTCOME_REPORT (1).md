# Outcome Report: Preregistered Test of Quantum Resonance Theory's Bell-State Fidelity Prediction on Superconducting Quantum Hardware

**Author:** Amber Anson, AmberContinuum Research
**Protocol and analysis drafted in collaboration with:** Claude (Anthropic)
**Execution date:** July 3, 2026
**Registration:** OSF, frozen prior to execution (embargoed at time of writing; this report is to be published alongside the registration when the embargo lifts)
**Theory under test:** Quantum Resonance Theory (Anson 2024, DOI 10.5281/zenodo.15105902)

---

## Abstract

Quantum Resonance Theory (QRT) predicts that a weak periodic resonance drive — Rθ = R₀·sin(ωᵣt), with R₀ = 10⁻³ rad and ωᵣ = 10 MHz — applied to an entangled pair during a hold period increases Bell-state fidelity by approximately 5% relative to an undriven baseline. Standard quantum mechanics predicts no fidelity gain from this intervention: a milliradian-amplitude phase drive is roughly three orders of magnitude below the amplitudes required for dynamical decoupling. The prediction was tested on IBM superconducting hardware (ibm_marrakesh) in a preregistered, interleaved, order-randomized A/B design with a five-level frequency sweep. At the theory-designated 10 MHz, the observed relative fidelity gain was −0.12% with a bootstrap 95% confidence interval of [−0.86%, +0.62%]. The interval's upper bound falls far below the preregistered decision threshold of +2.5%, and no resonance structure appears anywhere in the 1–50 MHz sweep. Under the preregistered decision rule, **QRT's Bell-state fidelity prediction is falsified at its stated parameters.** The result is consistent in every respect with standard quantum mechanics.

## 1. Background and hypotheses

QRT proposes a resonance modification to quantum dynamics whose entanglement consequence is stated quantitatively in the source paper: a Bell-state fidelity increase of ~5% relative (0.95 → 0.9975) under a drive with R₀ = 10⁻³ rad at ωᵣ = 10 MHz. This constitutes a genuine divergence from standard quantum mechanics, which predicts that a phase drive of milliradian amplitude is a negligible coherent perturbation with no fidelity benefit. The two theories therefore disagree about the outcome of a single inexpensive experiment.

Preregistered hypotheses:

- **H1 (QRT):** relative gain G = F_drive/F_control − 1 at ωᵣ = 10 MHz is ≥ +2.5%, with 95% CI excluding zero, and the 10 MHz effect exceeds all off-resonance frequencies tested. Frequency specificity is part of H1: a uniform offset across frequencies does not support a resonance mechanism.
- **H0 (Standard QM):** G at 10 MHz is indistinguishable from zero; CI upper bound below +2.5%.

The +2.5% threshold was set at half the predicted effect, so that a true 5% effect passes comfortably while hardware drift cannot.

## 2. Methods

**Design.** Two-arm interleaved A/B with a five-level frequency sweep on a single IBM Quantum superconducting device; 2 × 5 factorial (arm × frequency), fully crossed; 30 circuits total (2 arms × 5 frequencies × 3 measurement bases); 8,000 shots per circuit (240,000 total).

**Circuits.** Bell state |Φ+⟩ prepared via Hadamard + CNOT; 2 µs hold window sliced into 40 delay segments on both qubits. Drive arm: RZ(2·R₀·sin(ωᵣ·t_k)) applied to both qubits after each slice — the QRT drive implemented as stroboscopic phase modulation (20 samples per period at 10 MHz). Control arm: identical circuits with RZ(0); drive amplitude is the sole difference between arms. Frequencies: ωᵣ ∈ {1, 5, 10, 20, 50} MHz.

**Randomization.** All 30 circuits executed in an order randomized by a fixed, recorded seed (20260702); the executed order is logged in the results file and reproduces the registered order exactly.

**Measurement and estimation.** Three parity settings (XX, YY, ZZ) per arm per frequency; fidelity F = (1 + ⟨XX⟩ − ⟨YY⟩ + ⟨ZZ⟩)/4. Primary index G₁₀ = F_D/F_C − 1 at 10 MHz with bootstrap 95% CI (4,000 multinomial resamples of raw counts, fixed seed). No error mitigation, no outlier removal, no exclusions: all 240,000 shots analyzed as returned.

**Execution.** Backend ibm_marrakesh (Heron class), selected by least-busy criterion; calibration snapshot captured before the first shot per the registered starting rule; single session, job ID `d93t71fu62ks7395a110`; no aborts, no job failures, escalation tier not triggered.

**Protocol integrity.** The analysis script was frozen and attached to the registration with its SHA-256 hash recorded (318bbf27ba75ca8a16592afee07cd8415cedd5585a17b12f06d02f429756ee50). Between registration and execution, IBM's runtime client removed the script's submission interface (backend.run); submission was performed through a documented compatibility runner that imports the frozen file's circuit construction, parameters, randomization, and statistics verbatim and replaces only the submission call (SamplerV2 primitive, ISA transpilation at the same optimization level, with dynamical decoupling and twirling explicitly disabled per the registration's no-mitigation commitment). Execution of the frozen file itself was attempted and failed at the submission call with the API's removal error, before any shot; the log is archived. The verdict was independently re-derived from the raw hardware counts using exclusively the frozen file's functions and its decision block verbatim, reproducing the runner's fidelities, gains, and intervals to four decimal places and returning the identical decision. One discrepancy of record is disclosed: the frozen script's decision block omits the registration's frequency-specificity conjunct; the runner enforces the registration's version; the divergent branch was never reached by the data. Full accounting in DIVERGENCE.md.

## 3. Results

| ωᵣ (MHz) | F_control | F_drive | G (relative) | 95% CI |
|---------:|----------:|--------:|-------------:|:-------|
| 1  | 0.9052 | 0.9027 | −0.28% | [−1.01%, +0.41%] |
| 5  | 0.9059 | 0.9099 | +0.44% | [−0.27%, +1.15%] |
| **10** | **0.9046** | **0.9035** | **−0.12%** | **[−0.86%, +0.62%]** |
| 20 | 0.9094 | 0.9050 | −0.49% | [−1.20%, +0.24%] |
| 50 | 0.9071 | 0.9068 | −0.03% | [−0.74%, +0.68%] |

Control-arm fidelities (~0.905) are typical for a 2 µs two-qubit hold on current hardware and sit near the source paper's assumed 0.95 baseline regime. Statistical resolution matched the registered power analysis (CI half-widths ~±0.7%, resolving the +2.5% threshold with wide margin).

**Primary outcome.** G₁₀ = −0.12%, 95% CI [−0.86%, +0.62%]. The interval upper bound is below the +2.5% falsification threshold by more than 1.8 percentage points, and the interval comfortably contains zero.

**Secondary outcome (resonance specificity).** No frequency structure. All five gains are statistically indistinguishable from zero; the profile shows no peak at the theory-designated 10 MHz. The largest excursion (+0.44% at 5 MHz, CI spanning zero) is consistent with sampling noise.

## 4. Decision

Applying the preregistered rule: the CI upper bound on G₁₀ (+0.62%) falls below +2.5%. **Falsified as specified.** QRT's prediction of a ~5% relative Bell-state fidelity gain at R₀ = 10⁻³ rad, ωᵣ = 10 MHz is inconsistent with the data; the effect, if any exists, is bounded well under one percent. The observed physics is fully consistent with standard quantum mechanics' prediction for a milliradian phase drive: no effect.

Per the registration, this outcome supports H0 by interval exclusion — positive evidence that the effect is smaller than half the predicted size — not by mere failure to reject.

## 5. Limitations (as declared in the registration)

1. **Timing granularity.** Hardware rounding set slice durations to 48 ns (12 dt) versus the nominal 50 ns, shifting effective drive frequencies by ~4%. This cannot rescue the prediction: the sweep spans 1–50 MHz and shows no structure anywhere in that range.
2. **Stroboscopic approximation.** The continuous drive was implemented as discrete phase samples, 20 per period at 10 MHz (10× Nyquist), as declared.
3. **Scope.** This result binds the prediction at its stated parameter values. Per the registration, revised values of R₀ or ωᵣ constitute a new prediction requiring a new preregistration and do not rescue this one. The result does not address QRT's other predicted observables (energy shifts of ~10⁻¹⁷ eV; gravitational-wave signatures), which require instrumentation beyond this study.
4. **Stimulus physicality (identified post-execution).** The drive was implemented as RZ rotations, which IBM hardware executes as *virtual* frame changes — software reference-frame rotations, not physical pulses into the chip. Under standard quantum mechanics, virtual and physical Z-rotations are exactly equivalent; but that equivalence is itself a theorem of the theory under test. The result therefore falsifies QRT's fidelity prediction *as deliverable by phase modulation* — which is the form stated in the source paper's resonance term Rθ = R₀·sin(ωᵣt) — but does not test the response to a physically delivered periodic perturbation of the form H₀ + V₀cos(ωᵣt), which the paper's Hamiltonian also describes. A second preregistered test implementing the drive as physical pulses (native fractional RX on Heron-class hardware) addresses this form separately, as a new prediction under a new registration, per the rules of this one.

## 6. Conflicts and provenance

The author of the theory is the author of this test; the protocol was drafted in collaboration with an AI system, consistent with the declared authorship practices of the underlying paper. Both incentives — to rescue the theory and to perform its falsification — were managed structurally: decision rule frozen before execution, hash-anchored script, session-level-only exclusions, randomized order, and publication committed regardless of outcome. This report discharges that commitment.

## 7. Data and materials availability

All materials are published together: the frozen protocol and its hash, the compatibility runner, raw counts per circuit per basis, executed order, transpiled durations, the calibration snapshot, the frozen-execution attempt log, the independent verification script and its output, and the divergence accounting. Registration to be made public upon embargo lift, with its original freeze timestamp intact.

## 8. Conclusion

A quantitative prediction of Quantum Resonance Theory was given a preregistered, adequately powered, randomized test on superconducting quantum hardware, with the kill condition fixed in advance and no analyst degrees of freedom. It did not survive. The prediction is falsified at its stated parameters; standard quantum mechanics is confirmed in this regime, as it has been in every regime where the two were made to disagree.

The author notes, as the registration's design intended, that this document is the point: a theory whose kill condition was stated, armed, and executed by its own author. The framework's remaining claims inherit the same standard.
