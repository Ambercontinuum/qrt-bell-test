#!/usr/bin/env python3
"""
QRT Ramsey/T2 Resonance Test (Test #3 draft)
============================================

Draft execution + analysis script for the Ramsey/T2 preregistration in
docs/qrt3_ramsey_prereg.md.

This targets the source paper's explicit quantum-computing prediction:
superconducting-qubit coherence should increase by 5-10% at wr = 10 MHz,
tested with Ramsey/T2-style circuits.

Core safeguards:
  * A waveform audit runs before any hardware submission.
  * The 10 MHz schedule must not collapse to zero-crossing samples.
  * Off-resonance controls must not alias into the same discrete waveform.
  * IBM execution uses physical fractional RX pulses when available.
  * The default IBM layout uses an RRC-native orbit-packed workload: all
    conditions are run in parallel across qubits, with condition-to-qubit
    rotations sampling hardware-position bias while cutting PUB count.

Usage:
  python tests/qrt_ramsey_test.py --backend synthetic
  python tests/qrt_ramsey_test.py --backend ibm --device <backend_name>

The synthetic backend is a pipeline/power check only. It is non-evidential.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
from qiskit import QuantumCircuit
from scipy.optimize import curve_fit

# ---------------- parameters to freeze before confirmatory execution --------
R0 = 1e-3
RES_FREQ_MHZ = 10
OFF_RESONANCE_FREQS_MHZ = [1, 5, 15, 25]
FREQS_MHZ = OFF_RESONANCE_FREQS_MHZ + [RES_FREQ_MHZ]
DRIVE_STEP_NS = 16
TAU_MAX_NS = 12000
N_TAUS = 15
SHOTS = 19500
N_BOOT = 1000
SEED = 20260704
THRESHOLD = 0.05
LAYOUT = "rrc-packed"
RRC_ORBIT_REPS = 2

RESULTS_DIR = Path("results")


def condition_specs() -> list[tuple[str, int, bool]]:
    conditions = [(f"{f}MHz", f, True) for f in FREQS_MHZ]
    conditions.append(("REF", 0, False))
    return conditions


def tau_grid_ns(tau_max_ns: int = TAU_MAX_NS, n_taus: int = N_TAUS) -> list[int]:
    vals = np.linspace(0, tau_max_ns, n_taus)
    return sorted(set(int(round(v)) for v in vals))


def drive_samples(
    tau_ns: int,
    freq_mhz: float,
    driven: bool,
    drive_step_ns: int = DRIVE_STEP_NS,
    phase_rad: float = 0.0,
) -> tuple[list[int], list[float]]:
    """Return delay samples and RX angles for a discrete physical drive."""
    if tau_ns <= 0:
        return [], []
    n_steps = tau_ns // drive_step_ns
    times = [(k + 1) * drive_step_ns for k in range(n_steps)]
    if not driven:
        return times, [0.0 for _ in times]
    w = 2 * math.pi * freq_mhz * 1e6
    angles = [
        2 * R0 * math.cos(w * t_ns * 1e-9 + phase_rad)
        for t_ns in times
    ]
    return times, angles


def waveform_audit(
    freqs_mhz: list[int],
    taus_ns: list[int],
    drive_step_ns: int = DRIVE_STEP_NS,
) -> dict[str, Any]:
    """Validate that the discrete schedules are meaningful before hardware."""
    tau_ns = max(taus_ns)
    entries = {}
    vectors = {}
    failures = []
    for freq in freqs_mhz:
        times, angles = drive_samples(tau_ns, freq, True, drive_step_ns)
        arr = np.array(angles, dtype=float)
        if len(arr) == 0:
            rms = max_abs = 0.0
            occupied_phase_bins = 0
        else:
            rms = float(np.sqrt(np.mean(arr * arr)))
            max_abs = float(np.max(np.abs(arr)))
            phases = ((np.array(times) * freq * 1e-3) % 1.0)
            occupied_phase_bins = int(len(set(np.floor(phases * 12).astype(int))))
        entries[str(freq)] = {
            "freq_mhz": freq,
            "tau_ns": tau_ns,
            "drive_step_ns": drive_step_ns,
            "n_samples": len(arr),
            "rms_angle_rad": rms,
            "max_abs_angle_rad": max_abs,
            "occupied_phase_bins_12": occupied_phase_bins,
            "first_12_angles_rad": [float(x) for x in arr[:12]],
        }
        vectors[freq] = arr

        if freq == RES_FREQ_MHZ:
            if rms < 5e-4:
                failures.append("10 MHz RMS angle is too small; possible zero-crossing lock-in")
            if occupied_phase_bins < 6:
                failures.append("10 MHz schedule has inadequate phase coverage")

    res_vec = vectors[RES_FREQ_MHZ]
    for freq in freqs_mhz:
        if freq == RES_FREQ_MHZ:
            continue
        other = vectors[freq]
        n = min(len(res_vec), len(other))
        if n < 2:
            continue
        a = res_vec[:n] - float(np.mean(res_vec[:n]))
        b = other[:n] - float(np.mean(other[:n]))
        denom = float(np.linalg.norm(a) * np.linalg.norm(b))
        corr = 0.0 if denom == 0 else float(np.dot(a, b) / denom)
        entries[str(freq)]["corr_with_10mhz"] = corr
        if abs(corr) > 0.995:
            failures.append(f"{freq} MHz aliases too closely to 10 MHz (corr={corr:.4f})")

    return {
        "passed": not failures,
        "failures": failures,
        "audit_tau_ns": tau_ns,
        "frequencies_mhz": freqs_mhz,
        "entries": entries,
    }


def ramsey_drive_circuit(
    tau_ns: int,
    freq_mhz: float,
    driven: bool,
    drive_step_ns: int = DRIVE_STEP_NS,
) -> QuantumCircuit:
    """H -> driven delay -> H -> measure; P(0) decays toward 0.5 with T2*."""
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    times, angles = drive_samples(tau_ns, freq_mhz, driven, drive_step_ns)
    used_ns = 0
    for _, theta in zip(times, angles):
        qc.delay(drive_step_ns, 0, unit="ns")
        used_ns += drive_step_ns
        if driven:
            qc.rx(theta, 0)
    rem = tau_ns - used_ns
    if rem > 0:
        qc.delay(rem, 0, unit="ns")
    qc.h(0)
    qc.measure(0, 0)
    return qc


def rrc_orbit_assignments(
    orbit_reps: int,
) -> list[list[tuple[str, int, bool]]]:
    """Condition-to-qubit orbit reps, following RRC representative rotation."""
    base = condition_specs()
    n = len(base)
    reps = max(1, min(int(orbit_reps), n))
    assignments = []
    seen = set()
    for rep in range(reps):
        shift = (rep * n) // reps
        rotated = base[shift:] + base[:shift]
        key = tuple(c for c, _, _ in rotated)
        if key not in seen:
            assignments.append(rotated)
            seen.add(key)
    return assignments


def rrc_packed_ramsey_circuit(
    tau_ns: int,
    assignment: list[tuple[str, int, bool]],
    drive_step_ns: int = DRIVE_STEP_NS,
) -> QuantumCircuit:
    """Packed Ramsey circuit: one condition per qubit, one tau per PUB."""
    n_qubits = len(assignment)
    qc = QuantumCircuit(n_qubits, n_qubits)
    for q in range(n_qubits):
        qc.h(q)

    per_qubit_angles = [
        drive_samples(tau_ns, max(freq, 1), driven, drive_step_ns)[1]
        for _, freq, driven in assignment
    ]
    n_steps = tau_ns // drive_step_ns
    used_ns = 0
    for step in range(n_steps):
        for q in range(n_qubits):
            qc.delay(drive_step_ns, q, unit="ns")
        used_ns += drive_step_ns
        for q, (_, _, driven) in enumerate(assignment):
            if driven:
                qc.rx(per_qubit_angles[q][step], q)

    rem = tau_ns - used_ns
    if rem > 0:
        for q in range(n_qubits):
            qc.delay(rem, q, unit="ns")

    for q in range(n_qubits):
        qc.h(q)
        qc.measure(q, q)
    return qc


def marginal_counts(
    counts: dict[str, int],
    classical_index: int,
    n_clbits: int,
) -> dict[str, int]:
    zeros = 0
    ones = 0
    for bitstring, count in counts.items():
        compact = bitstring.replace(" ", "").zfill(n_clbits)
        bit = compact[::-1][classical_index]
        if bit == "0":
            zeros += int(count)
        else:
            ones += int(count)
    return {"0": zeros, "1": ones}


def count_zero_probability(counts: dict[str, int]) -> tuple[float, int]:
    shots = int(sum(counts.values()))
    zeros = int(counts.get("0", 0) + counts.get("00", 0))
    return zeros / shots, shots


def decay_model(tau_ns: np.ndarray, c: float, a: float, t2_ns: float) -> np.ndarray:
    return c + a * np.exp(-tau_ns / t2_ns)


def fit_t2_from_counts(rows: list[dict[str, Any]]) -> dict[str, float]:
    tau = np.array([r["tau_ns"] for r in rows], dtype=float)
    probs = []
    sigmas = []
    for r in rows:
        p0, shots = count_zero_probability(r["counts"])
        probs.append(p0)
        sigmas.append(max(math.sqrt(max(p0 * (1 - p0), 1e-6) / shots), 1e-4))
    y = np.array(probs, dtype=float)
    sigma = np.array(sigmas, dtype=float)

    c0 = float(np.clip(np.median(y[-max(3, len(y) // 5):]), 0.2, 0.8))
    a0 = float(np.clip(y[0] - c0, 0.05, 0.5))
    t20 = max(float(np.median(tau[tau > 0])) if np.any(tau > 0) else 1000.0, 1.0)
    lower = [0.0, 0.0, 1.0]
    upper = [1.0, 1.0, max(float(np.max(tau)) * 100, 1e6)]
    popt, pcov = curve_fit(
        decay_model,
        tau,
        y,
        p0=[c0, a0, t20],
        sigma=sigma,
        absolute_sigma=True,
        bounds=(lower, upper),
        maxfev=20000,
    )
    return {
        "offset": float(popt[0]),
        "amplitude": float(popt[1]),
        "t2star_ns": float(popt[2]),
        "t2star_se_ns": float(math.sqrt(max(float(pcov[2, 2]), 0.0))),
    }


def analyze_counts(
    raw_rows: list[dict[str, Any]],
    n_boot: int = N_BOOT,
    seed: int = SEED,
) -> dict[str, Any]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in raw_rows:
        grouped.setdefault(row["condition"], []).append(row)
    for rows in grouped.values():
        rows.sort(key=lambda r: r["tau_ns"])

    fits = {cond: fit_t2_from_counts(rows) for cond, rows in grouped.items()}
    control_conds = [f"{f}MHz" for f in OFF_RESONANCE_FREQS_MHZ]
    t2_res = fits[f"{RES_FREQ_MHZ}MHz"]["t2star_ns"]
    t2_controls = [fits[c]["t2star_ns"] for c in control_conds]
    gain = float(t2_res / float(np.mean(t2_controls)) - 1)

    rng = np.random.default_rng(seed)
    boot_gains = []
    for _ in range(n_boot):
        boot_rows = []
        for row in raw_rows:
            p0, shots = count_zero_probability(row["counts"])
            zeros = int(rng.binomial(shots, p0))
            boot_counts = {"0": zeros, "1": shots - zeros}
            boot_rows.append({**row, "counts": boot_counts})
        try:
            boot_fits = {
                cond: fit_t2_from_counts(rows)
                for cond, rows in _group_rows(boot_rows).items()
            }
            bt2_res = boot_fits[f"{RES_FREQ_MHZ}MHz"]["t2star_ns"]
            bt2_controls = [boot_fits[c]["t2star_ns"] for c in control_conds]
            boot_gains.append(bt2_res / float(np.mean(bt2_controls)) - 1)
        except Exception:
            continue
    lo, hi = np.percentile(boot_gains, [2.5, 97.5]) if boot_gains else (math.nan, math.nan)

    if gain >= THRESHOLD and lo > 0:
        decision = "QRT_CONSISTENT_ESCALATE"
    elif hi < THRESHOLD:
        decision = "FALSIFIED_AS_SPECIFIED"
    else:
        decision = "INCONCLUSIVE"

    return {
        "fits": fits,
        "primary_control_conditions": control_conds,
        "G_T2": gain,
        "ci95": [float(lo), float(hi)],
        "n_boot_success": len(boot_gains),
        "decision": decision,
    }


def _group_rows(raw_rows: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in raw_rows:
        grouped.setdefault(row["condition"], []).append(row)
    for rows in grouped.values():
        rows.sort(key=lambda r: r["tau_ns"])
    return grouped


def synthetic_counts(
    taus_ns: list[int],
    shots: int,
    seed: int = SEED,
    true_t2_ns: float | None = None,
    qrt_effect: float = 0.0,
    shot_noise: bool = False,
) -> list[dict[str, Any]]:
    rng = np.random.default_rng(seed)
    if true_t2_ns is None:
        true_t2_ns = max(float(max(taus_ns)) / 2.0, 1000.0)
    raw = []
    for condition, freq, driven in condition_specs():
        t2 = true_t2_ns * (1 + qrt_effect if freq == RES_FREQ_MHZ and driven else 1)
        for tau in taus_ns:
            p0 = float(decay_model(np.array([tau], dtype=float), 0.5, 0.48, t2)[0])
            p0 = float(np.clip(p0, 0, 1))
            zeros = int(rng.binomial(shots, p0)) if shot_noise else int(round(shots * p0))
            raw.append({
                "condition": condition,
                "freq_mhz": freq,
                "driven": driven,
                "tau_ns": tau,
                "counts": {"0": zeros, "1": shots - zeros},
            })
    return raw


def run_synthetic(args: argparse.Namespace, audit: dict[str, Any]) -> dict[str, Any]:
    taus = tau_grid_ns(args.tau_max_ns, args.n_taus)
    effective_shots = args.shots
    if args.layout == "rrc-packed":
        effective_shots *= len(rrc_orbit_assignments(args.rrc_orbit_reps))
    raw = synthetic_counts(
        taus,
        effective_shots,
        args.seed,
        qrt_effect=args.synthetic_effect,
        shot_noise=args.synthetic_shot_noise,
    )
    analysis = analyze_counts(raw, args.n_boot, args.seed)
    return {
        "backend_kind": "synthetic",
        "non_evidential": True,
        "parameters": frozen_parameters(args),
        "waveform_audit": audit,
        "raw_counts": raw,
        "analysis": analysis,
    }


def run_ibm(args: argparse.Namespace, audit: dict[str, Any]) -> dict[str, Any]:
    from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
    from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler

    service = QiskitRuntimeService()
    min_qubits = len(condition_specs()) if args.layout == "rrc-packed" else 1
    name = args.device or service.least_busy(
        operational=True, simulator=False, min_num_qubits=min_qubits
    ).name
    backend = service.backend(name, use_fractional_gates=True)
    print(f"[backend] {backend.name} (fractional gates enabled)")

    calib = {
        "backend_name": backend.name,
        "captured_at_utc": _dt.datetime.now(_dt.timezone.utc).isoformat(),
    }
    try:
        props = backend.properties()
        calib["properties"] = props.to_dict() if hasattr(props, "to_dict") else str(props)
    except Exception as exc:
        calib["properties_error"] = repr(exc)
    RESULTS_DIR.mkdir(exist_ok=True)
    calib_path = RESULTS_DIR / "calibration_snapshot_ramsey.json"
    calib_path.write_text(json.dumps(calib, indent=2, default=str), encoding="utf-8")

    taus = tau_grid_ns(args.tau_max_ns, args.n_taus)
    rng = np.random.default_rng(args.seed)
    if args.layout == "serial":
        pubs = [
            {
                "layout": "serial",
                "condition": c,
                "freq_mhz": f,
                "driven": d,
                "tau_ns": tau,
            }
            for c, f, d in condition_specs()
            for tau in taus
        ]
    else:
        assignments = rrc_orbit_assignments(args.rrc_orbit_reps)
        pubs = [
            {
                "layout": "rrc-packed",
                "tau_ns": tau,
                "orbit_rep": orbit_rep,
                "assignment": [
                    {"condition": c, "freq_mhz": f, "driven": d, "qubit_index": q}
                    for q, (c, f, d) in enumerate(assignment)
                ],
            }
            for tau in taus
            for orbit_rep, assignment in enumerate(assignments)
        ]
    rng.shuffle(pubs)
    executed_order = pubs

    pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
    isa = []
    physicality_log = []
    for pub in pubs:
        tau = pub["tau_ns"]
        if pub["layout"] == "serial":
            qc = ramsey_drive_circuit(
                tau,
                max(pub["freq_mhz"], 1),
                pub["driven"],
                args.drive_step_ns,
            )
            physicality_subject = pub["condition"]
            needs_rx = pub["driven"] and tau > 0
        else:
            assignment = [
                (item["condition"], item["freq_mhz"], item["driven"])
                for item in pub["assignment"]
            ]
            qc = rrc_packed_ramsey_circuit(tau, assignment, args.drive_step_ns)
            physicality_subject = f"rrc-packed/orbit={pub['orbit_rep']}"
            needs_rx = tau > 0 and any(item["driven"] for item in pub["assignment"])
        tqc = pm.run(qc)
        ops = dict(tqc.count_ops())
        if needs_rx and "rx" not in ops:
            raise RuntimeError(
                f"PHYSICALITY VIOLATION in {physicality_subject}/tau={tau}: no native rx in {ops}"
            )
        physicality_log.append({**pub, "ops": ops, "depth": tqc.depth()})
        isa.append(tqc)

    sampler = Sampler(mode=backend)
    sampler.options.default_shots = args.shots
    try:
        sampler.options.dynamical_decoupling.enable = False
        sampler.options.twirling.enable_gates = False
        sampler.options.twirling.enable_measure = False
    except Exception as exc:
        print(f"[options] note: {exc!r}")

    print(
        f"[submit] {len(isa)} PUBs x {args.shots} shots, "
        f"layout={args.layout}, randomized seed {args.seed}"
    )
    job = sampler.run([(qc,) for qc in isa])
    print(f"[job] id = {job.job_id()} - waiting...")
    result = job.result()

    if args.layout == "serial":
        raw = []
    else:
        aggregated: dict[tuple[str, int], dict[str, Any]] = {}
    for pub, pub_result in zip(pubs, result):
        tau = pub["tau_ns"]
        counts = pub_result.data.c.get_counts()
        if pub["layout"] == "serial":
            condition = pub["condition"]
            freq = pub["freq_mhz"]
            driven = pub["driven"]
            raw.append({
                "condition": condition,
                "freq_mhz": freq,
                "driven": driven,
                "tau_ns": tau,
                "counts": counts,
            })
            continue

        n_clbits = len(pub["assignment"])
        for item in pub["assignment"]:
            condition = item["condition"]
            freq = item["freq_mhz"]
            driven = item["driven"]
            key = (condition, tau)
            marg = marginal_counts(counts, item["qubit_index"], n_clbits)
            row = aggregated.setdefault(
                key,
                {
                    "condition": condition,
                    "freq_mhz": freq,
                    "driven": driven,
                    "tau_ns": tau,
                    "counts": {"0": 0, "1": 0},
                    "rrc_orbit_reps_observed": 0,
                    "source_layout": "rrc-packed",
                },
            )
            row["counts"]["0"] += marg["0"]
            row["counts"]["1"] += marg["1"]
            row["rrc_orbit_reps_observed"] += 1

    if args.layout == "rrc-packed":
        raw = list(aggregated.values())
        raw.sort(key=lambda r: (r["condition"], r["tau_ns"]))

    analysis = analyze_counts(raw, args.n_boot, args.seed)
    return {
        "backend_kind": "ibm",
        "backend": backend.name,
        "job_id": job.job_id(),
        "parameters": frozen_parameters(args),
        "waveform_audit": audit,
        "executed_order": executed_order,
        "physicality_log": physicality_log,
        "raw_counts": raw,
        "analysis": analysis,
    }


def frozen_parameters(args: argparse.Namespace) -> dict[str, Any]:
    return {
        "R0": R0,
        "res_freq_mhz": RES_FREQ_MHZ,
        "off_resonance_freqs_mhz": OFF_RESONANCE_FREQS_MHZ,
        "freqs_mhz": FREQS_MHZ,
        "drive_step_ns": args.drive_step_ns,
        "tau_max_ns": args.tau_max_ns,
        "n_taus": args.n_taus,
        "shots": args.shots,
        "layout": args.layout,
        "rrc_orbit_reps": args.rrc_orbit_reps,
        "conditions": [
            {"condition": c, "freq_mhz": f, "driven": d}
            for c, f, d in condition_specs()
        ],
        "planned_pubs": (
            args.n_taus * len(condition_specs())
            if args.layout == "serial"
            else args.n_taus * len(rrc_orbit_assignments(args.rrc_orbit_reps))
        ),
        "effective_shots_per_condition_tau": (
            args.shots
            if args.layout == "serial"
            else args.shots * len(rrc_orbit_assignments(args.rrc_orbit_reps))
        ),
        "n_boot": args.n_boot,
        "seed": args.seed,
        "threshold": THRESHOLD,
    }


def main() -> None:
    global RESULTS_DIR
    ap = argparse.ArgumentParser()
    ap.add_argument("--backend", choices=["synthetic", "ibm"], default="synthetic")
    ap.add_argument("--device", default=None)
    ap.add_argument("--shots", type=int, default=SHOTS)
    ap.add_argument("--n-boot", type=int, default=N_BOOT)
    ap.add_argument("--seed", type=int, default=SEED)
    ap.add_argument("--drive-step-ns", type=int, default=DRIVE_STEP_NS)
    ap.add_argument("--tau-max-ns", type=int, default=TAU_MAX_NS)
    ap.add_argument("--n-taus", type=int, default=N_TAUS)
    ap.add_argument("--layout", choices=["serial", "rrc-packed"], default=LAYOUT)
    ap.add_argument("--rrc-orbit-reps", type=int, default=RRC_ORBIT_REPS)
    ap.add_argument(
        "--synthetic-effect",
        type=float,
        default=0.0,
        help="Non-evidential synthetic 10 MHz T2 effect, e.g. 0.05 for +5%.",
    )
    ap.add_argument(
        "--synthetic-shot-noise",
        action="store_true",
        help="Add random shot noise to synthetic data; default uses expected counts.",
    )
    ap.add_argument("--out-dir", default=str(RESULTS_DIR))
    args = ap.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(exist_ok=True)
    RESULTS_DIR = out_dir

    taus = tau_grid_ns(args.tau_max_ns, args.n_taus)
    audit = waveform_audit(FREQS_MHZ, taus, args.drive_step_ns)
    audit_path = out_dir / "qrt3_waveform_audit.json"
    audit_path.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(f"[audit] saved -> {audit_path}")
    if not audit["passed"]:
        print("[audit] FAILED")
        for failure in audit["failures"]:
            print(f"  - {failure}")
        raise SystemExit(2)
    print("[audit] passed")

    if args.backend == "synthetic":
        out = run_synthetic(args, audit)
        fname = out_dir / "qrt3_sim_results.json"
    else:
        out = run_ibm(args, audit)
        fname = out_dir / "qrt3_hardware_results.json"

    fname.write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")
    analysis = out["analysis"]
    print(f"results -> {fname}")
    print(
        "G_T2 = "
        f"{analysis['G_T2'] * 100:+.2f}% "
        f"95% CI [{analysis['ci95'][0] * 100:+.2f}%, "
        f"{analysis['ci95'][1] * 100:+.2f}%]"
    )
    print(f"decision = {analysis['decision']}")


if __name__ == "__main__":
    main()
