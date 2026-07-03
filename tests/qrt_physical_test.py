#!/usr/bin/env python3
"""
QRT Physical-Drive Bell Test (Test #2)
=======================================
Preregistered test of Quantum Resonance Theory's fidelity prediction under a
PHYSICALLY delivered periodic drive (Anson 2024, DOI 10.5281/ZENODO.15105902).

Test #1 (falsified as specified) implemented the drive as RZ phase modulation,
which IBM hardware executes as virtual frame changes. This test implements the
drive as native fractional RX pulses on Heron-class hardware — real microwave
energy entering the chip, modulated at the drive frequency — testing the
paper's Hamiltonian form H = H0 + V0*cos(w_r*t) as a physical perturbation.

Design change from Test #1: all comparison arms are PHYSICALLY DRIVEN at
identical amplitude schedules; the comparison is ACROSS FREQUENCIES. Uniform
pulse-induced degradation cancels; only frequency structure can produce a
signal. QRT's resonance claim predicts F(10 MHz) elevated above off-resonance;
standard QM predicts a flat profile.

Primary index: G_res = F(10 MHz) / mean(F at {1, 5, 20, 50} MHz) - 1
Decision (preregistered, mirrors Test #1 thresholds):
  QRT-consistent: G_res >= +2.5% with 95% CI excluding 0
  Falsified as specified: CI upper bound < +2.5%
  Inconclusive: CI spans +2.5% -> one preregistered double-shot rerun

PHYSICALITY ASSERTION: after transpilation, every driven circuit must contain
native 'rx' operations in the hold window. If the transpiler decomposed the
drive into sx/x + virtual rz, the run ABORTS — the entire point of this test
is that the drive is physical.

Usage:
  python3 qrt_physical_test.py --backend aer    # statistics pipeline check only
  python3 qrt_physical_test.py --backend ibm    # confirmatory run
"""

import argparse, json, math, datetime
import numpy as np
from qiskit import QuantumCircuit

# ---------------- parameters (preregistered; do not tune post hoc) ----------
R0 = 1e-3                  # rad — same amplitude as Test #1 / QRT Sec. 3
FREQS_MHZ = [1, 5, 10, 20, 50]   # same sweep as Test #1; 10 MHz theory-designated
RES_FREQ = 10
SLICE_NS = 48              # matches Heron timing granularity (12 dt) directly
N_SLICES = 40              # hold window = 1920 ns
SHOTS = 8000               # same as Test #1
N_BOOT = 4000              # same as Test #1
SEED = 20260703            # new seed for the new registration
BASES = ["XX", "YY", "ZZ"]
THRESHOLD = 0.025          # same +2.5% decision threshold as Test #1

def bell_drive_circuit(freq_mhz: float, basis: str, driven: bool = True) -> QuantumCircuit:
    """Bell prep -> sliced hold with physical RX drive -> basis rotation -> measure.
    driven=False builds the undriven reference arm (descriptive only)."""
    qc = QuantumCircuit(2, 2)
    qc.h(0); qc.cx(0, 1)                              # |Phi+>
    w = 2 * math.pi * freq_mhz * 1e6                  # rad/s
    for k in range(N_SLICES):
        qc.delay(SLICE_NS, 0, unit="ns")
        qc.delay(SLICE_NS, 1, unit="ns")
        t = (k + 1) * SLICE_NS * 1e-9
        theta = 2 * R0 * math.sin(w * t) if driven else 0.0
        qc.rx(theta, 0)                               # PHYSICAL pulse (fractional RX)
        qc.rx(theta, 1)
    if basis == "XX":
        qc.h(0); qc.h(1)
    elif basis == "YY":
        qc.sdg(0); qc.h(0); qc.sdg(1); qc.h(1)
    qc.measure([0, 1], [0, 1])
    return qc

def parity_expectation(counts: dict) -> float:
    tot = sum(counts.values()); s = 0
    for bitstr, c in counts.items():
        b = bitstr.replace(" ", "")
        s += (1 if b.count("1") % 2 == 0 else -1) * c
    return s / tot

def fidelity_from_parities(exx, eyy, ezz):
    return (1 + exx - eyy + ezz) / 4

def assert_physicality(isa_circuit, label: str):
    """ABORT if the drive was compiled away from native rx pulses."""
    ops = isa_circuit.count_ops()
    if "rx" not in ops:
        raise RuntimeError(
            f"PHYSICALITY VIOLATION in {label}: transpiled circuit contains no "
            f"native rx operations (ops: {dict(ops)}). The drive would not be "
            f"physical. Aborting per protocol — enable fractional gates or "
            f"adjust transpilation; do not proceed.")
    return dict(ops)

def bootstrap_res_ci(counts_by_freq, n_boot=N_BOOT, seed=SEED):
    """Bootstrap CI on G_res = F(10)/mean(F offres) - 1 over raw counts."""
    rng = np.random.default_rng(seed)
    def resample_parity(counts):
        keys = list(counts.keys()); vals = np.array([counts[k] for k in keys], dtype=float)
        draw = rng.multinomial(int(vals.sum()), vals / vals.sum())
        s = sum((1 if k.replace(" ", "").count("1") % 2 == 0 else -1) * c
                for k, c in zip(keys, draw))
        return s / vals.sum()
    gains = []
    for _ in range(n_boot):
        F = {}
        for f in FREQS_MHZ:
            F[f] = fidelity_from_parities(
                *[resample_parity(counts_by_freq[f][b]) for b in BASES])
        offres = [F[f] for f in FREQS_MHZ if f != RES_FREQ]
        m = float(np.mean(offres))
        if m > 0:
            gains.append(F[RES_FREQ] / m - 1)
    lo, hi = np.percentile(gains, [2.5, 97.5])
    return float(np.mean(gains)), float(lo), float(hi)

def run(backend_kind: str, device: str | None):
    # ---- build all cells in the frozen randomized order --------------------
    # 5 driven frequencies + 1 undriven reference, x 3 bases = 18 circuits
    cells = [(f, b, True) for f in FREQS_MHZ for b in BASES]
    cells += [(0, b, False) for b in BASES]           # freq 0 = undriven reference
    order_rng = np.random.default_rng(SEED)
    order_rng.shuffle(cells)
    executed_order = [(f, b, "DRIVEN" if d else "REF") for f, b, d in cells]

    if backend_kind == "aer":
        from qiskit_aer import AerSimulator
        from qiskit_aer.noise import NoiseModel, thermal_relaxation_error
        noise = NoiseModel()
        err = thermal_relaxation_error(120e3, 90e3, SLICE_NS)
        noise.add_all_qubit_quantum_error(err, ["delay"])
        backend = AerSimulator(noise_model=noise)
        print("[backend] AerSimulator + thermal relaxation (PIPELINE CHECK ONLY — "
              "simulator implements standard QM AND does not model pulse "
              "physicality; carries zero evidential weight)")
        from qiskit import transpile
        counts_store = {f: {} for f in FREQS_MHZ}; ref_store = {}
        for f, b, driven in cells:
            qc = bell_drive_circuit(max(f, 1), b, driven)
            tqc = transpile(qc, backend, optimization_level=1)
            counts = backend.run(tqc, shots=SHOTS,
                                 seed_simulator=SEED).result().get_counts()
            (counts_store[f] if driven else ref_store)[b] = counts
    else:
        from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
        from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
        service = QiskitRuntimeService()
        # fractional gates REQUIRED for physical arbitrary-angle RX
        name = device or service.least_busy(
            operational=True, simulator=False, min_num_qubits=2).name
        backend = service.backend(name, use_fractional_gates=True)
        print(f"[backend] {backend.name} (fractional gates enabled)")

        calib = {"backend_name": backend.name,
                 "captured_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}
        try:
            props = backend.properties()
            calib["properties"] = props.to_dict() if hasattr(props, "to_dict") else str(props)
        except Exception as e:
            calib["properties_error"] = repr(e)
        with open("calibration_snapshot_test2.json", "w") as fp:
            json.dump(calib, fp, indent=2, default=str)
        print("[calibration] saved -> calibration_snapshot_test2.json")

        pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
        isa, physicality_log = [], []
        for f, b, driven in cells:
            qc = bell_drive_circuit(max(f, 1), b, driven)
            tqc = pm.run(qc)
            if driven:
                ops = assert_physicality(tqc, f"{f}MHz/{b}")
                physicality_log.append({"freq_mhz": f, "basis": b, "ops": ops})
            isa.append(tqc)
        print(f"[physicality] all {sum(1 for c in cells if c[2])} driven circuits "
              "contain native rx — drive is physical")

        sampler = Sampler(mode=backend)
        sampler.options.default_shots = SHOTS
        try:
            sampler.options.dynamical_decoupling.enable = False
            sampler.options.twirling.enable_gates = False
            sampler.options.twirling.enable_measure = False
        except Exception as e:
            print(f"[options] note: {e!r}")

        print(f"[submit] 18 PUBs x {SHOTS} shots, randomized order (seed {SEED})")
        job = sampler.run([(qc,) for qc in isa])
        print(f"[job] id = {job.job_id()} — waiting...")
        result = job.result()

        counts_store = {f: {} for f in FREQS_MHZ}; ref_store = {}
        raw = []
        for (f, b, driven), pub in zip(cells, result):
            counts = pub.data.c.get_counts()
            (counts_store[f] if driven else ref_store)[b] = counts
            raw.append({"freq_mhz": f, "basis": b,
                        "arm": "DRIVEN" if driven else "REF", "counts": counts})

    # ---- analysis -----------------------------------------------------------
    F = {}
    for f in FREQS_MHZ:
        F[f] = fidelity_from_parities(
            *[parity_expectation(counts_store[f][b]) for b in BASES])
        print(f"  w_r={f:>3} MHz | F={F[f]:.4f}")
    f_ref = fidelity_from_parities(
        *[parity_expectation(ref_store[b]) for b in BASES])
    print(f"  undriven ref | F={f_ref:.4f}  (descriptive only)")

    gain, lo, hi = bootstrap_res_ci(counts_store)
    offres_mean = float(np.mean([F[f] for f in FREQS_MHZ if f != RES_FREQ]))
    print(f"\n  G_res = F(10MHz)/mean(offres) - 1 = {gain*100:+.2f}%  "
          f"95% CI [{lo*100:+.2f}%, {hi*100:+.2f}%]")
    print(f"  (F_10 = {F[RES_FREQ]:.4f}, mean offres = {offres_mean:.4f})")

    print("\n=== DECISION (preregistered, Test #2) ===")
    if lo > 0.0 and gain >= THRESHOLD:
        print("QRT-CONSISTENT under physical drive -> escalate: replication + "
              "amplitude sweep + second device before any claim")
    elif hi < THRESHOLD:
        print("NULL: QRT resonance prediction FALSIFIED under PHYSICAL drive "
              "at stated parameters (R0=1e-3 rad, w_r=10 MHz)")
    else:
        print("INCONCLUSIVE: CI spans boundary -> preregistered escalation "
              "(double shots, one rerun)")

    out = {"executed_order": executed_order,
           "fidelities": {str(f): F[f] for f in FREQS_MHZ},
           "fidelity_ref": f_ref,
           "G_res": gain, "ci95": [lo, hi]}
    if backend_kind == "ibm":
        out["job_id"] = job.job_id(); out["backend"] = backend.name
        out["raw_counts"] = raw; out["physicality_log"] = physicality_log
    fname = ("qrt2_hardware_results.json" if backend_kind == "ibm"
             else "qrt2_sim_results.json")
    with open(fname, "w") as fp:
        json.dump(out, fp, indent=2, default=str)
    print(f"results -> {fname}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--backend", choices=["aer", "ibm"], default="aer")
    ap.add_argument("--device", default=None)
    args = ap.parse_args()
    run(args.backend, args.device)
