# Preregistration: QRT Bell-State Fidelity Test

**Theory under test:** Quantum Resonance Theory (Anson 2024, DOI 10.5281/ZENODO.15105902)
**Prereg author:** Amber Anson, AmberContinuum Research
**Protocol drafted in collaboration with:** Claude (Anthropic), July 2, 2026
**Status:** DRAFT — freeze before hardware execution; register at OSF alongside 7mejx / 2vb7z

---

## 1. Claim under test

QRT Section 4 predicts that a weak periodic resonance drive applied during a Bell-state
hold period increases entanglement fidelity by ~5% relative (paper's figures: 0.95 → 0.9975),
via Rθ = R0·sin(ωr·t) with **R0 = 10⁻³ rad** and **ωr = 10 MHz** (Section 3 exemplar values).

**Standard QM prediction for the identical intervention:** no fidelity gain. A milliradian
phase drive is ~3 orders of magnitude below the pulse amplitudes required for dynamical
decoupling; within standard theory the drive is a negligible coherent perturbation and the
expected relative gain is 0, bounded well under +1%.

This is a genuine divergence: the two theories disagree about an experiment that costs
nothing to run. Exactly one of them is wrong about it.

## 2. Design

Two-qubit interleaved A/B on IBM Quantum hardware (open tier), frequency sweep.

- **Preparation:** |Φ+⟩ via H + CNOT.
- **Hold window:** 2 µs, sliced into 40 × 50 ns delay segments on both qubits.
- **Drive arm (D):** after each slice k, apply RZ(2·R0·sin(ωr·t_k)) on both qubits —
  the QRT drive implemented as stroboscopic phase modulation.
- **Control arm (C):** identical circuit with RZ(0) — identical gate count, identical
  scheduling, zero drive amplitude.
- **Frequency sweep:** ωr ∈ {1, 5, 10, 20, 50} MHz. QRT names 10 MHz; a resonance
  mechanism implies frequency structure. A flat response across the sweep is evidence
  against resonance specificity even if some uniform offset appears.
- **Fidelity estimator:** F = (1 + ⟨XX⟩ − ⟨YY⟩ + ⟨ZZ⟩)/4 from three parity settings.
- **Shots:** 8,000 per circuit per basis (30 circuits total). Bootstrap 95% CI (4,000
  resamples) on relative gain G = F_D/F_C − 1.
- **Interleaving:** C and D arms submitted in the same session, alternating, to control
  calibration drift.

## 3. Preregistered decision rule

At ωr = 10 MHz:

- **QRT-consistent:** G ≥ +2.5% with 95% CI excluding 0, AND the 10 MHz effect exceeds
  all off-resonance frequencies. → Escalate: independent replication on a second device,
  amplitude sweep (R0 × {0.1, 1, 10}), and explicit dynamical-decoupling controls before
  any claim is made.
- **Falsified at stated parameters:** 95% CI upper bound < +2.5%. → QRT's Bell-fidelity
  prediction is dead as specified (R0 = 10⁻³ rad, ωr = 10 MHz). Result posted publicly
  either way; this is the graveyard condition.
- **Inconclusive:** CI spans the boundary. → Double shots and rerun; do not reinterpret.

## 4. Scope and honesty constraints

- A positive result at these amplitudes would be extraordinary and is *expected to be
  an artifact* until replication + DD controls pass. The escalation path exists so that
  a fluke cannot be published as a finding.
- A null result kills the prediction **as specified in the paper**. It does not kill
  resonance mechanisms at other amplitudes/frequencies — but any post-hoc migration of
  R0 or ωr must be declared as a new prediction in a new preregistration, not a rescue.
- The Aer simulator run included with the code is a **pipeline check only**. The simulator
  implements standard QM; its null is by construction and carries zero evidential weight.
- Known limitation: stroboscopic RZ sampling approximates the continuous drive at 20
  samples per 10 MHz period (adequate; Nyquist ×10). Hardware delay granularity may
  round slice durations; actual scheduled durations will be recorded from the transpiled
  circuits and reported.

## 5. Outputs

- qrt_bell_results.json (raw counts retained), transpiled circuit listings, backend
  calibration snapshot at execution time, and this document — posted regardless of outcome.
