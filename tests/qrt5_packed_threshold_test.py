#!/usr/bin/env python3
"""
QRT5 Packed-State Threshold Test
================================

Confirmatory follow-up to the exploratory signal observed in QRT4.

QRT4 falsified the preregistered 10 MHz T2* coherence-gain endpoint, but the
packed readout showed tau-localized joint-state population waves. QRT5 tests a
new, explicitly preregistered endpoint: whether any nonzero packed bitstring
state exhibits a reproducible threshold-like transition across balanced
assignment repetitions. The QRT4 carrier state 011001 is retained as a
secondary prior state, not as the sole primary endpoint.

Usage:
  python tests/qrt5_packed_threshold_test.py --backend synthetic
  python tests/qrt5_packed_threshold_test.py --backend ibm --device ibm_marrakesh

The synthetic backend is a pipeline check only. It is non-evidential.
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
BALANCED_REPS = 2
PRIOR_STATE = "011001"
EXCLUDED_STATES = {"000000"}

MIN_PEAK_PROB = 0.20
MIN_LIFT_FROM_EDGE = 0.15
MIN_BOOT_LIFT = 0.10
MIN_BOOT_PEAK = 0.15
MAX_PEAK_TAU_SPAN_NS = 1000
MIN_WINNER_STABILITY = 0.90

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
    if tau_ns <= 0:
        return [], []
    n_steps = tau_ns // drive_step_ns
    times = [(k + 1) * drive_step_ns for k in range(n_steps)]
    if not driven:
        return times, [0.0 for _ in times]
    w = 2 * math.pi * freq_mhz * 1e6
    angles = [2 * R0 * math.cos(w * t_ns * 1e-9 + phase_rad) for t_ns in times]
    return times, angles


def waveform_audit(
    freqs_mhz: list[int],
    taus_ns: list[int],
    drive_step_ns: int = DRIVE_STEP_NS,
) -> dict[str, Any]:
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


def balanced_assignments(
    reps_requested: int,
) -> list[list[tuple[str, int, bool]]]:
    base = condition_specs()
    n = len(base)
    reps = max(1, min(int(reps_requested), n))
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


def packed_ramsey_circuit(
    tau_ns: int,
    assignment: list[tuple[str, int, bool]],
    drive_step_ns: int = DRIVE_STEP_NS,
) -> QuantumCircuit:
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


def make_pubs(
    taus: list[int],
    balance_reps: int = BALANCED_REPS,
    seed: int = SEED,
) -> list[dict[str, Any]]:
    assignments = balanced_assignments(balance_reps)
    pubs = [
        {
            "layout": "balanced-packed",
            "tau_ns": tau,
            "balance_rep": balance_rep,
            "assignment": [
                {"condition": c, "freq_mhz": f, "driven": d, "qubit_index": q}
                for q, (c, f, d) in enumerate(assignment)
            ],
        }
        for tau in taus
        for balance_rep, assignment in enumerate(assignments)
    ]
    rng = np.random.default_rng(seed)
    rng.shuffle(pubs)
    return pubs


def normalize_counts(counts: dict[str, int], n_clbits: int) -> dict[str, int]:
    norm: dict[str, int] = {}
    for bitstring, count in counts.items():
        key = bitstring.replace(" ", "").zfill(n_clbits)
        norm[key] = norm.get(key, 0) + int(count)
    return norm


def state_probability(row: dict[str, Any], state: str) -> float:
    counts = row["counts"]
    total = int(sum(counts.values()))
    return 0.0 if total == 0 else counts.get(state, 0) / total


def _edge_mean(vals: list[float], edge_n: int = 3) -> float:
    if len(vals) < edge_n * 2:
        return float(max(vals)) if vals else 0.0
    return float(max(np.mean(vals[:edge_n]), np.mean(vals[-edge_n:])))


def _state_metrics(
    packed_rows: list[dict[str, Any]],
    state: str,
) -> dict[str, Any]:
    taus = sorted({int(r["tau_ns"]) for r in packed_rows})
    reps = sorted({int(r["balance_rep"]) for r in packed_rows})
    by = {(int(r["tau_ns"]), int(r["balance_rep"])): r for r in packed_rows}

    series: dict[str, list[float]] = {}
    peak_by_rep = {}
    lifts = []
    peak_probs = []
    peak_taus = []
    for rep in reps:
        vals = [state_probability(by[(tau, rep)], state) for tau in taus]
        series[str(rep)] = [float(v) for v in vals]
        peak_idx = int(np.argmax(vals))
        peak_prob = float(vals[peak_idx])
        edge = _edge_mean(vals)
        lift = float(peak_prob - edge)
        peak_by_rep[str(rep)] = {
            "peak_tau_ns": taus[peak_idx],
            "peak_prob": peak_prob,
            "edge_prob": edge,
            "lift_from_edge": lift,
        }
        peak_probs.append(peak_prob)
        lifts.append(lift)
        peak_taus.append(taus[peak_idx])

    observed = {
        "min_peak_prob": float(min(peak_probs)),
        "min_lift_from_edge": float(min(lifts)),
        "peak_tau_span_ns": int(max(peak_taus) - min(peak_taus)),
    }
    return {
        "state": state,
        "taus_ns": taus,
        "state_probability_by_rep": series,
        "peak_by_rep": peak_by_rep,
        "observed": observed,
    }


def _all_candidate_states(packed_rows: list[dict[str, Any]]) -> list[str]:
    states = set()
    for row in packed_rows:
        states.update(row["counts"])
    return sorted(s for s in states if s not in EXCLUDED_STATES)


def _transition_score(metrics: dict[str, Any]) -> float:
    obs = metrics["observed"]
    if obs["peak_tau_span_ns"] > MAX_PEAK_TAU_SPAN_NS:
        return -1.0
    return float(min(obs["min_peak_prob"], obs["min_lift_from_edge"]))


def _select_winner(packed_rows: list[dict[str, Any]]) -> dict[str, Any]:
    candidates = _all_candidate_states(packed_rows)
    metrics = [_state_metrics(packed_rows, state) for state in candidates]
    if not metrics:
        raise RuntimeError("No candidate packed states available for threshold scan")
    metrics.sort(
        key=lambda m: (
            _transition_score(m),
            m["observed"]["min_lift_from_edge"],
            m["observed"]["min_peak_prob"],
            m["state"],
        ),
        reverse=True,
    )
    winner = metrics[0]
    winner["candidate_count"] = len(candidates)
    winner["top_candidates"] = [
        {
            "state": m["state"],
            "score": _transition_score(m),
            "observed": m["observed"],
        }
        for m in metrics[:10]
    ]
    return winner


def analyze_packed_counts(
    packed_rows: list[dict[str, Any]],
    n_boot: int = N_BOOT,
    seed: int = SEED,
    prior_state: str = PRIOR_STATE,
) -> dict[str, Any]:
    winner = _select_winner(packed_rows)
    winner_state = winner["state"]
    prior = _state_metrics(packed_rows, prior_state) if prior_state else None
    observed = winner["observed"]

    rng = np.random.default_rng(seed)
    boot_min_peaks = []
    boot_min_lifts = []
    boot_winner_states = []
    for _ in range(n_boot):
        boot_rows = []
        for row in packed_rows:
            counts = row["counts"]
            keys = sorted(counts)
            vals = np.array([counts[k] for k in keys], dtype=int)
            total = int(vals.sum())
            if total <= 0:
                continue
            probs = vals / total
            sample = rng.multinomial(total, probs)
            boot_counts = {k: int(v) for k, v in zip(keys, sample)}
            boot_rows.append({**row, "counts": boot_counts})
        boot_winner = _select_winner(boot_rows)
        boot_winner_states.append(boot_winner["state"])
        boot = _state_metrics(boot_rows, winner_state)
        boot_min_peaks.append(boot["observed"]["min_peak_prob"])
        boot_min_lifts.append(boot["observed"]["min_lift_from_edge"])

    if n_boot > 0 and boot_min_peaks:
        peak_ci = [float(x) for x in np.percentile(boot_min_peaks, [2.5, 97.5])]
        lift_ci = [float(x) for x in np.percentile(boot_min_lifts, [2.5, 97.5])]
    else:
        peak_ci = [math.nan, math.nan]
        lift_ci = [math.nan, math.nan]
    winner_stability = (
        boot_winner_states.count(winner_state) / len(boot_winner_states)
        if boot_winner_states else 1.0
    )

    if (
        observed["min_peak_prob"] >= MIN_PEAK_PROB
        and observed["min_lift_from_edge"] >= MIN_LIFT_FROM_EDGE
        and observed["peak_tau_span_ns"] <= MAX_PEAK_TAU_SPAN_NS
        and winner_stability >= MIN_WINNER_STABILITY
        and peak_ci[0] >= MIN_BOOT_PEAK
        and lift_ci[0] >= MIN_BOOT_LIFT
    ):
        decision = "RESONANCE_THRESHOLD_REPLICATED"
    elif peak_ci[1] < MIN_BOOT_PEAK or lift_ci[1] < MIN_BOOT_LIFT:
        decision = "NO_REPLICATED_RESONANCE_THRESHOLD"
    else:
        decision = "INCONCLUSIVE"

    return {
        "primary_scan": "all observed six-bit states excluding 000000",
        "excluded_states": sorted(EXCLUDED_STATES),
        "winner_state": winner_state,
        "prior_state": prior_state,
        "candidate_count": winner["candidate_count"],
        "top_candidates": winner["top_candidates"],
        "taus_ns": winner["taus_ns"],
        "state_probability_by_rep": winner["state_probability_by_rep"],
        "peak_by_rep": winner["peak_by_rep"],
        "observed": observed,
        "prior_state_metrics": prior,
        "ci95": {
            "min_peak_prob": peak_ci,
            "min_lift_from_edge": lift_ci,
        },
        "winner_bootstrap_stability": winner_stability,
        "decision_thresholds": {
            "min_peak_prob": MIN_PEAK_PROB,
            "min_lift_from_edge": MIN_LIFT_FROM_EDGE,
            "min_boot_peak": MIN_BOOT_PEAK,
            "min_boot_lift": MIN_BOOT_LIFT,
            "max_peak_tau_span_ns": MAX_PEAK_TAU_SPAN_NS,
            "min_winner_stability": MIN_WINNER_STABILITY,
        },
        "n_boot": n_boot,
        "decision": decision,
    }


def synthetic_packed_counts(
    taus: list[int],
    shots: int,
    seed: int = SEED,
    target_state: str = PRIOR_STATE,
    peak_prob: float = 0.30,
) -> list[dict[str, Any]]:
    rng = np.random.default_rng(seed)
    pubs = make_pubs(taus, BALANCED_REPS, seed)
    packed_rows = []
    n_states = 2 ** len(condition_specs())
    all_states = [format(i, "06b") for i in range(n_states)]
    other_states = [s for s in all_states if s != target_state]
    center = 0.60 * max(taus)
    width = 0.18 * max(taus)
    for pub in pubs:
        tau = pub["tau_ns"]
        p_target = peak_prob * math.exp(-0.5 * ((tau - center) / width) ** 2)
        p_target = float(np.clip(p_target, 0.0, 0.95))
        probs = np.full(n_states, (1.0 - p_target) / (n_states - 1), dtype=float)
        target_idx = all_states.index(target_state)
        probs[target_idx] = p_target
        sample = rng.multinomial(shots, probs)
        counts = {state: int(sample[i]) for i, state in enumerate(all_states) if sample[i] > 0}
        packed_rows.append({
            "tau_ns": tau,
            "balance_rep": pub["balance_rep"],
            "assignment": pub["assignment"],
            "counts": counts,
        })
    return packed_rows


def run_synthetic(args: argparse.Namespace, audit: dict[str, Any]) -> dict[str, Any]:
    taus = tau_grid_ns(args.tau_max_ns, args.n_taus)
    packed_rows = synthetic_packed_counts(
        taus,
        args.shots,
        args.seed,
        args.prior_state,
        args.synthetic_peak_prob,
    )
    analysis = analyze_packed_counts(packed_rows, args.n_boot, args.seed, args.prior_state)
    return {
        "backend_kind": "synthetic",
        "non_evidential": True,
        "parameters": frozen_parameters(args),
        "waveform_audit": audit,
        "packed_counts": packed_rows,
        "analysis": analysis,
    }


def run_ibm(args: argparse.Namespace, audit: dict[str, Any]) -> dict[str, Any]:
    from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
    from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler

    service = QiskitRuntimeService()
    if args.device is None:
        raise RuntimeError(
            "QRT5 freezes the backend choice; pass --device ibm_marrakesh "
            "or register a new backend-specific version."
        )
    backend = service.backend(args.device, use_fractional_gates=True)
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
    calib_path = RESULTS_DIR / "calibration_snapshot_qrt5.json"
    calib_path.write_text(json.dumps(calib, indent=2, default=str), encoding="utf-8")

    taus = tau_grid_ns(args.tau_max_ns, args.n_taus)
    pubs = make_pubs(taus, args.balance_reps, args.seed)

    pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
    isa = []
    physicality_log = []
    for pub in pubs:
        tau = pub["tau_ns"]
        assignment = [
            (item["condition"], item["freq_mhz"], item["driven"])
            for item in pub["assignment"]
        ]
        qc = packed_ramsey_circuit(tau, assignment, args.drive_step_ns)
        tqc = pm.run(qc)
        ops = dict(tqc.count_ops())
        if tau > 0 and "rx" not in ops:
            raise RuntimeError(
                f"PHYSICALITY VIOLATION in rep={pub['balance_rep']}/tau={tau}: no native rx in {ops}"
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

    print(f"[submit] {len(isa)} PUBs x {args.shots} shots, prior_state={args.prior_state}")
    job = sampler.run([(qc,) for qc in isa])
    print(f"[job] id = {job.job_id()} - waiting...")
    result = job.result()

    packed_rows = []
    for pub, pub_result in zip(pubs, result):
        n_clbits = len(pub["assignment"])
        counts = normalize_counts(pub_result.data.c.get_counts(), n_clbits)
        packed_rows.append({
            "tau_ns": pub["tau_ns"],
            "balance_rep": pub["balance_rep"],
            "assignment": pub["assignment"],
            "counts": counts,
        })

    analysis = analyze_packed_counts(packed_rows, args.n_boot, args.seed, args.prior_state)
    return {
        "backend_kind": "ibm",
        "backend": backend.name,
        "job_id": job.job_id(),
        "parameters": frozen_parameters(args),
        "waveform_audit": audit,
        "executed_order": pubs,
        "physicality_log": physicality_log,
        "packed_counts": packed_rows,
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
        "balance_reps": args.balance_reps,
        "prior_state": args.prior_state,
        "planned_pubs": args.n_taus * len(balanced_assignments(args.balance_reps)),
        "n_boot": args.n_boot,
        "seed": args.seed,
        "thresholds": {
            "min_peak_prob": MIN_PEAK_PROB,
            "min_lift_from_edge": MIN_LIFT_FROM_EDGE,
            "min_boot_peak": MIN_BOOT_PEAK,
            "min_boot_lift": MIN_BOOT_LIFT,
            "max_peak_tau_span_ns": MAX_PEAK_TAU_SPAN_NS,
        },
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
    ap.add_argument("--balance-reps", type=int, default=BALANCED_REPS)
    ap.add_argument("--prior-state", default=PRIOR_STATE)
    ap.add_argument("--synthetic-peak-prob", type=float, default=0.30)
    ap.add_argument("--out-dir", default=str(RESULTS_DIR))
    args = ap.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(exist_ok=True)
    RESULTS_DIR = out_dir

    taus = tau_grid_ns(args.tau_max_ns, args.n_taus)
    audit = waveform_audit(FREQS_MHZ, taus, args.drive_step_ns)
    audit_path = out_dir / "qrt5_waveform_audit.json"
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
        fname = out_dir / "qrt5_sim_results.json"
    else:
        out = run_ibm(args, audit)
        fname = out_dir / "qrt5_hardware_results.json"

    fname.write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")
    analysis = out["analysis"]
    obs = analysis["observed"]
    ci = analysis["ci95"]
    print(f"results -> {fname}")
    print(
        "winner_state = "
        f"{analysis['winner_state']} "
        f"prior_state={analysis['prior_state']} "
        f"min_peak={obs['min_peak_prob']:.3f} "
        f"min_lift={obs['min_lift_from_edge']:.3f} "
        f"peak_tau_span_ns={obs['peak_tau_span_ns']} "
        f"winner_stability={analysis['winner_bootstrap_stability']:.3f}"
    )
    print(
        "95% CI min_peak "
        f"[{ci['min_peak_prob'][0]:.3f}, {ci['min_peak_prob'][1]:.3f}], "
        "min_lift "
        f"[{ci['min_lift_from_edge'][0]:.3f}, {ci['min_lift_from_edge'][1]:.3f}]"
    )
    print(f"decision = {analysis['decision']}")


if __name__ == "__main__":
    main()
