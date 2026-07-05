# Outcome Report - QRT v5 Proper Point-Claim Replication

**Author:** Amber Anson, AmberContinuum Research  
**Protocol and analysis drafted in collaboration with:** Claude (Anthropic)  
**Filed by:** Codex  
**Theory under test:** Quantum Resonance Theory coherence-enhancement point claim at `wr = 10 MHz`, `R0 = 10^-3 rad`

---

## Status

QRT v5 was a preregistered confirmatory replication of the QRT v4.1 point-claim result on a second device, using the frozen script `tests/qrt5_escalation_test.py`.

This is the proper QRT v5 package. It is separate from the earlier Codex-drafted packed-threshold design quarantined under `unused_experiments/qrt5_packed_threshold_design/`.

---

## Hardware Run

- Job ID: `d957fkuvtlqs73fv33i0`
- Backend: `ibm_marrakesh`
- Status: `Completed`
- Created: `2026-07-05T15:27:16.161957Z`
- Design: 72 circuits, 6,000 shots each
- Total shots: 432,000
- Frozen script SHA-256: `e37fa996cbe2491dcdd02e1f8d4f72e5880838a72fd523c5697162ae12a267a7`

---

## Preregistered Primary Result

Primary endpoint:

```text
G_rep = A(10 MHz @ 1x R0) / mean(A(9 MHz @ 1x R0), A(11 MHz @ 1x R0)) - 1
```

Result:

```text
G_rep = +4.75%
95% CI = [+4.22%, +5.24%]
decision = REPLICATED_ON_SECOND_DEVICE
```

The preregistered H1 rule was `G_rep >= +0.9%` with the 95% CI lower bound above zero. QRT v5 passes that rule.

---

## Secondary Descriptive Results

These indices carry no inferential weight under the preregistration:

```text
G_amp_10x = -1.81%
G_phase_rand = +2.42%
```

They should be treated as design information for later interpretation, not as confirmatory support or defeat of the v5 primary decision.

---

## Interpretation

QRT v5 replicated the v4.1 point-claim signal on a second non-`ibm_fez` device at the stated 10 MHz / R0 parameter point.

Per the registration, this does not constitute final confirmation of QRT. It means the point claim survived the preregistered second-device confirmatory test and advances to independent-party verification.

The v4.2 amplitude-scaling result remains adverse to a simple drive-coupled scaling mechanism. QRT v5 addresses the exact stated-parameter point claim, not the broader mechanism class tested by v4.2.

---

## Filed Artifacts

- `docs/qrt5_osf_fields.md`
- `docs/qrt5_artifact_manifest.md`
- `tests/qrt5_escalation_test.py`
- `results/qrt5/qrt5_calibration.json`
- `results/qrt5/job-d957fkuvtlqs73fv33i0-info.json`
- `results/qrt5/job-d957fkuvtlqs73fv33i0-result.json`
- `results/qrt5/qrt5_hardware_results.json`

