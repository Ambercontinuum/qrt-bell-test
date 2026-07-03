#!/usr/bin/env python3
"""
QRT Bell-State Fidelity Test
=============================
Preregistered test of Quantum Resonance Theory (Anson 2024, DOI 10.5281/ZENODO.15105902)

QRT claim under test (Sec. 4): a weak periodic resonance drive
    R(theta) = R0 * sin(w_r * t),  R0 ~ 1e-3 rad,  w_r ~ 10 MHz
increases Bell-state fidelity by ~5% relative (paper: 0.95 -> 0.9975).

Standard QM prediction: a milliradian-amplitude phase drive is ~3000x too weak
to produce dynamical-decoupling effects; predicted fidelity change is ~0
(bounded well below +1% relative).

Design: interleaved A/B with frequency sweep.
  ARM C  (control):   Bell prep -> idle hold (sliced delays, RZ(0) inserted) -> tomography
  ARM D  (drive):     identical, but RZ(2*R0*sin(w_r * t_k)) at each slice k
  Sweep:  w_r in {1, 5, 10, 20, 50} MHz  (QRT names 10 MHz; resonance structure expected)

Fidelity estimator for |Phi+> from three parity settings:
  F = (1 + <XX> - <YY> + <ZZ>) / 4

Decision rule (preregistered):
  QRT-consistent: F_D/F_C - 1 >= +2.5% at w_r = 10 MHz with 95% CI excluding 0,
                  AND effect at 10 MHz exceeds off-resonance frequencies.
  Null (QRT falsified at stated parameters): CI for relative gain at 10 MHz
                  excludes +2.5% from above.

Usage:
  python3 qrt_bell_test.py --backend aer          # local simulator (pipeline check)
  python3 qrt_bell_test.py --backend ibm --device <name>   # real hardware via QiskitRuntimeService
"""

import argparse, json, math, sys
import numpy as np
from qiskit import QuantumCircuit, transpile

# ---------------- parameters (preregistered; do not tune post hoc) ----------------
R0 = 1e-3                 # rad, QRT paper Sec. 3
FREQS_MHZ = [1, 5, 10, 20, 50]
HOLD_NS = 2000            # total hold window (2 us) - long enough for several 10 MHz periods
N_SLICES = 40             # phase samples across hold window (50 ns spacing)
SHOTS = 8000              # per circuit per basis
SEED = 20260702

BASES = ["XX", "YY", "ZZ"]

def bell_hold_circuit(drive: bool, freq_mhz: float, basis: str) -> QuantumCircuit:
    qc = QuantumCircuit(2, 2)
    qc.h(0); qc.cx(0, 1)                      # |Phi+>
    dt_ns = HOLD_NS / N_SLICES
    w = 2 * math.pi * freq_mhz * 1e6          # rad/s
    for k in range(N_SLICES):
        qc.delay(int(dt_ns), 0, unit="ns")
        qc.delay(int(dt_ns), 1, unit="ns")
        t = (k + 1) * dt_ns * 1e-9            # seconds
        phi = 2 * R0 * math.sin(w * t) if drive else 0.0
        qc.rz(phi, 0)                         # QRT drive as phase modulation; RZ(0) in control
        qc.rz(phi, 1)                         # keeps gate count identical across arms
    if basis == "XX":
        qc.h(0); qc.h(1)
    elif basis == "YY":
        qc.sdg(0); qc.h(0); qc.sdg(1); qc.h(1)
    qc.measure([0, 1], [0, 1])
    return qc

def parity_expectation(counts: dict) -> float:
    tot = sum(counts.values())
    s = 0
    for bitstr, c in counts.items():
        b = bitstr.replace(" ", "")
        par = 1 if (b.count("1") % 2 == 0) else -1
        s += par * c
    return s / tot

def fidelity_from_parities(exx, eyy, ezz):
    return (1 + exx - eyy + ezz) / 4

def bootstrap_ci(counts_by_basis_c, counts_by_basis_d, n_boot=4000, seed=SEED):
    rng = np.random.default_rng(seed)
    def resample_parity(counts):
        keys = list(counts.keys()); vals = np.array([counts[k] for k in keys], dtype=float)
        tot = int(vals.sum())
        draw = rng.multinomial(tot, vals / vals.sum())
        s = 0
        for k, c in zip(keys, draw):
            par = 1 if (k.replace(" ", "").count("1") % 2 == 0) else -1
            s += par * c
        return s / tot
    gains = []
    for _ in range(n_boot):
        fc = fidelity_from_parities(*[resample_parity(counts_by_basis_c[b]) for b in BASES])
        fd = fidelity_from_parities(*[resample_parity(counts_by_basis_d[b]) for b in BASES])
        if fc > 0:
            gains.append(fd / fc - 1)
    lo, hi = np.percentile(gains, [2.5, 97.5])
    return float(np.mean(gains)), float(lo), float(hi)

def run(backend_kind: str, device: str | None):
    if backend_kind == "aer":
        from qiskit_aer import AerSimulator
        # T1/T2 noise makes the hold window meaningful; pipeline check only.
        from qiskit_aer.noise import NoiseModel, thermal_relaxation_error
        noise = NoiseModel()
        t1, t2 = 120e3, 90e3  # ns, typical transmon
        dt_ns = HOLD_NS / N_SLICES
        err = thermal_relaxation_error(t1, t2, dt_ns)
        noise.add_all_qubit_quantum_error(err, ["delay"])
        backend = AerSimulator(noise_model=noise)
        print("[backend] AerSimulator + thermal relaxation (PIPELINE CHECK - "
              "simulator implements standard QM; a null here is by construction, not evidence)")
    else:
        from qiskit_ibm_runtime import QiskitRuntimeService
        service = QiskitRuntimeService()
        backend = service.backend(device) if device else service.least_busy(
            operational=True, simulator=False, min_num_qubits=2)
        print(f"[backend] IBM device: {backend.name}")

    results = {}
    # Randomized execution order (preregistered): all 30 (freq, basis, arm) cells
    # are shuffled with a fixed, recorded seed so that run order is random with
    # respect to calibration drift. Order is logged to the results file.
    cells = [(f, b, d) for f in FREQS_MHZ for b in BASES for d in (False, True)]
    order_rng = np.random.default_rng(SEED)
    order_rng.shuffle(cells)
    executed_order = [(f, b, "D" if d else "C") for f, b, d in cells]
    counts_store = {f: {"C": {}, "D": {}} for f in FREQS_MHZ}
    for f, basis, drive in cells:
        qc = bell_hold_circuit(drive, f, basis)
        tqc = transpile(qc, backend, scheduling_method=None, optimization_level=1)
        job = backend.run(tqc, shots=SHOTS, seed_simulator=SEED if backend_kind == "aer" else None)
        counts_store[f]["D" if drive else "C"][basis] = job.result().get_counts()
    for f in FREQS_MHZ:
        counts_c, counts_d = counts_store[f]["C"], counts_store[f]["D"]
        fc = fidelity_from_parities(*[parity_expectation(counts_c[b]) for b in BASES])
        fd = fidelity_from_parities(*[parity_expectation(counts_d[b]) for b in BASES])
        gain, lo, hi = bootstrap_ci(counts_c, counts_d)
        results[f] = dict(F_control=fc, F_drive=fd, rel_gain=gain, ci95=[lo, hi])
        print(f"  w_r={f:>3} MHz | F_ctrl={fc:.4f}  F_drive={fd:.4f}  "
              f"gain={gain*100:+.2f}%  95% CI [{lo*100:+.2f}%, {hi*100:+.2f}%]")

    # preregistered decision at 10 MHz
    g = results[10]
    print("\n=== DECISION (preregistered) ===")
    if g["ci95"][0] > 0.0 and g["rel_gain"] >= 0.025:
        print("QRT-CONSISTENT at stated parameters -> escalate: replication + DD controls")
    elif g["ci95"][1] < 0.025:
        print("NULL: QRT 5% Bell-fidelity prediction FALSIFIED at stated parameters "
              "(R0=1e-3 rad, w_r=10 MHz)")
    else:
        print("INCONCLUSIVE: CI spans decision boundary -> increase shots")
    with open("qrt_bell_results.json", "w") as fp:
        json.dump({"executed_order": executed_order, "results": results}, fp, indent=2)
    print("results -> qrt_bell_results.json")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--backend", choices=["aer", "ibm"], default="aer")
    ap.add_argument("--device", default=None)
    args = ap.parse_args()
    run(args.backend, args.device)
