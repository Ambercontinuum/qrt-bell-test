# QRT Bell-State Fidelity Test

Preregistered experimental test of Quantum Resonance Theory's Bell-state fidelity
prediction on superconducting quantum hardware.

**Status: registered · awaiting hardware execution**

## What this is

Quantum Resonance Theory (QRT; Anson 2024, DOI [10.5281/zenodo.15105902](https://doi.org/10.5281/zenodo.15105902))
predicts that a weak periodic resonance drive — Rθ = R0·sin(ωr·t), with R0 = 10⁻³ rad
and ωr = 10 MHz — applied to an entangled pair during a hold period increases
Bell-state fidelity by ~5% relative to an undriven baseline.

Standard quantum mechanics predicts no fidelity gain from this intervention: a
milliradian-amplitude phase drive is roughly three orders of magnitude below the
pulse amplitudes required for dynamical decoupling.

The two theories disagree about the outcome of a single inexpensive experiment.
This repository contains the frozen protocol that runs it, and will contain the
result — whichever way it goes.

The author of the theory is the author of this test. That is the point: the
prediction is either load-bearing or it isn't, and the only way to find out is
to build the kill condition and pull the trigger. The decision rule was frozen
by preregistration before any hardware execution, with no analyst degrees of
freedom in either direction — including the incentive to rescue the theory, and
the incentive to perform its falsification.

## Design in one paragraph

Two-arm interleaved A/B on IBM Quantum hardware. Both arms prepare |Φ+⟩ and hold
for 2 µs across 40 sliced delays; the drive arm applies RZ(2·R0·sin(ωr·t_k)) at
each slice, the control arm applies RZ(0) at identical positions — drive amplitude
is the sole difference. Frequency sweep across ωr ∈ {1, 5, 10, 20, 50} MHz tests
resonance specificity. Execution order of all 30 circuits is randomized by a fixed,
recorded seed. Fidelity per arm from three parity settings: F = (1 + ⟨XX⟩ − ⟨YY⟩ + ⟨ZZ⟩)/4.
Primary index: G₁₀ = F_D/F_C − 1 at 10 MHz, bootstrap 95% CI.

**Preregistered decision rule (at 10 MHz):**
- **QRT-consistent:** G₁₀ ≥ +2.5%, CI excludes 0, and 10 MHz tops the frequency
  profile → escalation only (replication on a second device, amplitude sweep,
  dynamical-decoupling controls) before any claim.
- **Falsified as specified:** CI upper bound < +2.5% → the prediction is dead at
  its stated parameters. Posted regardless.
- **Inconclusive:** CI spans the boundary → one preregistered double-shot rerun,
  then report as-is.

## Provenance

- **Preregistration:** frozen on OSF prior to any hardware execution (currently
  embargoed; link will be added when the embargo lifts).
- **Frozen script:** `qrt_bell_test.py`, SHA-256
  `318bbf27ba75ca8a16592afee07cd8415cedd5585a17b12f06d02f429756ee50`.
  The file in this repository is byte-identical to the file attached to the
  registration. It will not be edited. Any post-freeze compatibility fixes
  (e.g., runtime API changes) will appear as separate, documented files with
  the core logic and seed untouched.
- **Simulator validation:** `qrt_bell_results.json` is the output of a local
  noisy-simulator pipeline check. The simulator implements standard QM; its
  null result is by construction and carries **zero evidential weight**. It is
  included for transparency only.

## Repository layout

```
qrt_bell_test.py        frozen protocol + analysis (do not edit)
qrt_bell_results.json   simulator pipeline check (non-evidential)
calibration/            backend calibration snapshot at execution
results/                hardware results (raw counts, transpiled circuits, decision output)
```

## Reproducing

```bash
pip install qiskit qiskit-ibm-runtime qiskit-aer

# pipeline check (local, non-evidential)
python3 qrt_bell_test.py --backend aer

# confirmatory run (IBM account + saved token required)
python3 qrt_bell_test.py --backend ibm
```

Verify the frozen script before running:

```bash
sha256sum qrt_bell_test.py
# expect: 318bbf27ba75ca8a16592afee07cd8415cedd5585a17b12f06d02f429756ee50
```

## Authorship

Amber Anson, AmberContinuum Research. Protocol drafted in collaboration with
Claude (Anthropic), consistent with the declared authorship practices of the
underlying paper.

## License

Code: MIT. Data and documents: CC-BY 4.0.
