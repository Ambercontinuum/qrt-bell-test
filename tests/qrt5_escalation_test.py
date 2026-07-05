#!/usr/bin/env python3
"""
QRT Escalation Test v5 — adjudicating the v4.1 QRT-consistent result
======================================================================
v4.1 (job d94hi4lgc6cc73ff4cc0, ibm_fez) returned G_A = +2.87% [+2.35, +3.46],
QRT_CONSISTENT_ESCALATE. Per that registration, the result is an artifact
until it survives: (i) a second device, (ii) an amplitude sweep, and
(iii) drive-phase randomization. This test runs all three arms in one
packed session on a NON-fez fractional-gate device.

Conditions (6, packed one per qubit, full 6-fold rotation):
  A2   10MHz @ 1x R0     PRIMARY: the paper's point claim, confirmatory power
  A3   10MHz @ 10x R0    secondary: cross-device check of the scaling exclusion
  NB9  9MHz  @ 1x        neighbor control (primary comparator, with NB11)
  NB11 11MHz @ 1x        neighbor control
  PR   10MHz @ 1x, per-pulse random phase (seeded) — spectral specificity
  REF  undriven          descriptive reference

Primary index: G_rep = same-qubit paired difference contrast, envelope area,
A2 (10MHz@1x) vs mean(NB9, NB11). Decision (preregistered):
  REPLICATED_ON_SECOND_DEVICE: G_rep >= +0.9% AND 95% CI lower bound > 0
  NOT_REPLICATED:              95% CI upper bound < +0.9%
  INCONCLUSIVE:                otherwise -> one double-shot rerun

Preregistered secondary predictions (descriptive, reported either way):
  - Amplitude monotonicity: a real drive-coupled effect scales with R0
    (G(A3) > G(A2) > G(A1) expected under QRT); a tiny-angle calibration
    artifact does not scale coherently.
  - Phase randomization: PR destroys spectral concentration at 10 MHz; any
    frequency-specific mechanism (QRT or filter-function) should vanish
    (G(PR vs NB) ~ 0). PR surviving would indicate a non-spectral artifact.

Device rule: the backend MUST NOT be ibm_fez (the v4.1 device). Enforced.

Usage:
  python qrt5_escalation_test.py --backend synthetic [--synthetic-effect 0.10]
  python qrt5_escalation_test.py --backend ibm [--device ibm_marrakesh]
"""
from __future__ import annotations
import argparse, datetime as _dt, json, math
import numpy as np
from qiskit import QuantumCircuit
from scipy.optimize import curve_fit

R0 = 1e-3
RES_FREQ_MHZ = 10
NB_FREQ_MHZ = 11
DRIVE_STEP_NS = 16
TAU_MAX_NS = 12000
N_TAUS = 12
SHOTS = 6000
N_BOOT = 2000
SEED = 20260710
THRESHOLD_AREA = 0.009   # half the v4.1-observed effect in area units
FORBIDDEN_DEVICE = "ibm_fez"

# condition tuple: (name, freq_mhz, amp_scale, phase_random, driven)
def condition_specs():
    return [
        ("A2_10MHz_1x",   RES_FREQ_MHZ, 1.0, False, True),
        ("A3_10MHz_10x",  RES_FREQ_MHZ, 10.0, False, True),
        ("NB9_9MHz_1x",   9,            1.0, False, True),
        ("NB11_11MHz_1x", NB_FREQ_MHZ,  1.0, False, True),
        ("PR_10MHz_1x",   RES_FREQ_MHZ, 1.0, True,  True),
        ("REF",           0,            0.0, False, False),
    ]

def tau_grid_ns():
    return sorted(set(int(round(v)) for v in np.linspace(0, TAU_MAX_NS, N_TAUS)))

def drive_angles(tau_ns, freq_mhz, amp_scale, phase_random, driven, rng):
    if tau_ns <= 0: return []
    n = tau_ns // DRIVE_STEP_NS
    times = [(k + 1) * DRIVE_STEP_NS for k in range(n)]
    if not driven: return [0.0] * n
    w = 2 * math.pi * freq_mhz * 1e6
    out = []
    for t in times:
        ph = rng.uniform(0, 2 * math.pi) if phase_random else 0.0
        out.append(2 * R0 * amp_scale * math.cos(w * t * 1e-9 + ph))
    return out

def rotations():
    base = condition_specs()
    return [base[s:] + base[:s] for s in range(6)]

def packed_circuit(tau_ns, assignment, angle_rng):
    nq = len(assignment)
    qc = QuantumCircuit(nq, nq)
    for q in range(nq): qc.h(q)
    per_q = [drive_angles(tau_ns, max(f, 1), a, pr, d, angle_rng)
             for _, f, a, pr, d in assignment]
    n = tau_ns // DRIVE_STEP_NS
    used = 0
    for step in range(n):
        for q in range(nq): qc.delay(DRIVE_STEP_NS, q, unit="ns")
        used += DRIVE_STEP_NS
        for q, (_, _, _, _, d) in enumerate(assignment):
            if d: qc.rx(per_q[q][step], q)
    if tau_ns - used > 0:
        for q in range(nq): qc.delay(tau_ns - used, q, unit="ns")
    for q in range(nq):
        qc.h(q); qc.measure(q, q)
    return qc

def envelope_area(cr):
    cr = sorted(cr, key=lambda r: r["tau_ns"])
    tau = np.array([r["tau_ns"] for r in cr], float)
    dev = np.array([abs(r["p0"] - 0.5) for r in cr], float)
    return float(np.trapezoid(dev, tau))

def contrast(cell_area, num_cond, den_conds):
    if isinstance(den_conds, str): den_conds = [den_conds]
    qubits = sorted({q for q, _ in cell_area})
    num = den = 0.0
    for q in qubits:
        a_ctl = float(np.mean([cell_area[(q, c)] for c in den_conds]))
        num += cell_area[(q, num_cond)] - a_ctl
        den += a_ctl
    return float(num / den)

def analyze(rows, n_boot=N_BOOT, seed=SEED):
    cells = {}
    for r in rows:
        cells.setdefault((r["qubit"], r["condition"]), []).append(r)
    area = {k: envelope_area(v) for k, v in cells.items()}
    NBS = ["NB9_9MHz_1x", "NB11_11MHz_1x"]
    g_rep = contrast(area, "A2_10MHz_1x", NBS)      # PRIMARY: paper's point claim
    g_a3  = contrast(area, "A3_10MHz_10x", NBS)      # secondary: cross-device scaling
    g_pr  = contrast(area, "PR_10MHz_1x", NBS)       # secondary: spectral specificity
    rng = np.random.default_rng(seed)
    boots = []
    for _ in range(n_boot):
        ba = {}
        for key, cr in cells.items():
            bcr = [{**r, "p0": rng.binomial(r["shots"], r["p0"]) / r["shots"]} for r in cr]
            ba[key] = envelope_area(bcr)
        boots.append(contrast(ba, "A2_10MHz_1x", NBS))
    lo, hi = np.percentile(boots, [2.5, 97.5])
    if g_rep >= THRESHOLD_AREA and lo > 0: decision = "REPLICATED_ON_SECOND_DEVICE"
    elif hi < THRESHOLD_AREA: decision = "NOT_REPLICATED"
    else: decision = "INCONCLUSIVE"
    return {"G_rep": g_rep, "ci95": [float(lo), float(hi)],
            "G_amp_10x": g_a3, "G_phase_rand": g_pr,
            "per_cell_area": {str(k): v for k, v in area.items()},
            "decision": decision}

def build_pubs():
    taus = tau_grid_ns(); rots = rotations()
    pubs = [{"tau_ns": t, "rotation": ri, "assignment": rots[ri]}
            for t in taus for ri in range(6)]
    np.random.default_rng(SEED).shuffle(pubs)
    return pubs

def rows_from_counts(pubs, counts_list):
    rows = []
    for pub, counts in zip(pubs, counts_list):
        tot = sum(counts.values())
        for q, (cond, f, a, pr, d) in enumerate(pub["assignment"]):
            zeros = sum(c for bs, c in counts.items()
                        if bs.replace(" ", "").zfill(6)[::-1][q] == "0")
            rows.append({"qubit": q, "condition": cond, "tau_ns": pub["tau_ns"],
                         "p0": zeros / tot, "shots": tot})
    return rows

def run_synthetic(effect):
    rng = np.random.default_rng(SEED)
    q_t2 = rng.uniform(3000, 30000, 6); q_df = rng.uniform(5, 120, 6)
    q_phi = rng.uniform(-0.3, 0.3, 6)
    def model(t, c, a, t2, dfk, ph):
        return c + a*np.exp(-t/t2)*np.cos(2*np.pi*dfk*1e-6*t + ph)
    pubs = build_pubs(); rows = []
    for pub in pubs:
        for q, (cond, f, amp, pr, d) in enumerate(pub["assignment"]):
            # injected QRT effect: coherent 10MHz arms only, scaling with amplitude
            scale = 1.0
            if d and f == RES_FREQ_MHZ and not pr:
                scale = 1 + effect * amp   # effect proportional to amp_scale
            t2 = q_t2[q] * scale
            p0 = float(np.clip(model(pub["tau_ns"], 0.5, 0.48, t2, q_df[q], q_phi[q]), 0, 1))
            rows.append({"qubit": q, "condition": cond, "tau_ns": pub["tau_ns"],
                         "p0": rng.binomial(SHOTS, p0) / SHOTS, "shots": SHOTS})
    return rows

def run_ibm(device):
    from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
    from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
    service = QiskitRuntimeService()
    if device is None:
        cands = [b for b in service.backends(operational=True, simulator=False,
                                             min_num_qubits=6)
                 if b.name != FORBIDDEN_DEVICE]
        if not cands:
            raise RuntimeError("No non-fez backend available; second-device rule blocks execution.")
        backend_name = min(cands, key=lambda b: b.status().pending_jobs).name
    else:
        backend_name = device
    if backend_name == FORBIDDEN_DEVICE:
        raise RuntimeError("Second-device rule: ibm_fez (the v4.1 device) is forbidden for v5.")
    backend = service.backend(backend_name, use_fractional_gates=True)
    print(f"[backend] {backend.name} (fractional gates enabled; fez excluded)")
    calib = {"backend_name": backend.name,
             "captured_at_utc": _dt.datetime.now(_dt.timezone.utc).isoformat()}
    try:
        p = backend.properties()
        calib["properties"] = p.to_dict() if hasattr(p, "to_dict") else str(p)
    except Exception as e:
        calib["properties_error"] = repr(e)
    json.dump(calib, open("calibration_snapshot_v5.json", "w"), indent=2, default=str)
    print("[calibration] saved -> calibration_snapshot_v5.json")

    pubs = build_pubs()
    angle_rng = np.random.default_rng(SEED + 1)   # fixed seed for PR arm phases
    pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
    isa, phys = [], []
    for pub in pubs:
        qc = packed_circuit(pub["tau_ns"], pub["assignment"], angle_rng)
        tqc = pm.run(qc)
        ops = dict(tqc.count_ops())
        if pub["tau_ns"] > 0 and "rx" not in ops:
            raise RuntimeError(f"PHYSICALITY VIOLATION tau={pub['tau_ns']}: {ops}")
        phys.append({"tau_ns": pub["tau_ns"], "rotation": pub["rotation"], "ops": ops})
        isa.append(tqc)
    print(f"[physicality] all {len(isa)} circuits carry native rx — drive is physical")
    sampler = Sampler(mode=backend); sampler.options.default_shots = SHOTS
    try:
        sampler.options.dynamical_decoupling.enable = False
        sampler.options.twirling.enable_gates = False
        sampler.options.twirling.enable_measure = False
    except Exception as e:
        print(f"[options] {e!r}")
    print(f"[submit] {len(isa)} PUBs x {SHOTS} shots (seed {SEED})")
    job = sampler.run([(qc,) for qc in isa])
    print(f"[job] id = {job.job_id()} — waiting...")
    result = job.result()
    counts_list = [pr_.data.c.get_counts() for pr_ in result]
    rows = rows_from_counts(pubs, counts_list)
    out = {"job_id": job.job_id(), "backend": backend.name,
           "executed_order": [(p["tau_ns"], p["rotation"]) for p in pubs],
           "physicality_log": phys,
           "raw_counts": [{"tau_ns": p["tau_ns"], "rotation": p["rotation"], "counts": c}
                          for p, c in zip(pubs, counts_list)]}
    return rows, out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--backend", choices=["synthetic", "ibm"], default="synthetic")
    ap.add_argument("--device", default=None)
    ap.add_argument("--synthetic-effect", type=float, default=0.0)
    args = ap.parse_args()
    if args.backend == "synthetic":
        print(f"[synthetic] injected amp-scaling QRT effect = {args.synthetic_effect:+.1%} (NON-EVIDENTIAL)")
        rows, out = run_synthetic(args.synthetic_effect), {"non_evidential": True}
    else:
        rows, out = run_ibm(args.device)
    a = analyze(rows)
    print(f"\nG_rep (10@1x vs 11@1x) = {a['G_rep']*100:+.2f}%  "
          f"95% CI [{a['ci95'][0]*100:+.2f}%, {a['ci95'][1]*100:+.2f}%]")
    print(f"secondary: G(10x)={a['G_amp_10x']*100:+.2f}%  "
          f"G(phase-rand)={a['G_phase_rand']*100:+.2f}%")
    print(f"=== DECISION (preregistered, v5) === {a['decision']}")
    out["analysis"] = a
    fn = "qrt5_hardware_results.json" if args.backend == "ibm" else "qrt5_sim_results.json"
    json.dump(out, open(fn, "w"), indent=2, default=str)
    print(f"results -> {fn}")

if __name__ == "__main__":
    main()
