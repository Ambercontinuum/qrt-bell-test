# QRT v4.x Artifact Manifest

**Status:** repository filing record for Fable/Claude QRT v4.1 and v4.2 artifacts  
**Filed by:** Codex  
**Filed on:** 2026-07-04  
**QRT4.2 result added:** 2026-07-05  
**Purpose:** preserve the v4.x sequence and distinguish it from both the proper QRT5 result and the unused Codex QRT5 draft

---

## Program Timeline Boundary

This manifest records that the QRT4.1 and QRT4.2 materials were added to the repository after Codex-managed QRT work through QRT4 and after a draft QRT5 preregistration had been prepared.

The earlier Codex-drafted QRT5 packed-threshold work is quarantined under `unused_experiments/qrt5_packed_threshold_design/` as an unused experimental design. This QRT5 draft is Codex work, not Fable/Claude QRT4.1 or QRT4.2 work. It has not been adjudicated or run as a hardware result in this repository record and should not be confused with the proper QRT5 package.

The proper QRT5 point-claim replication package is filed separately in `docs/qrt5_artifact_manifest.md` and `reports/OUTCOME_REPORT_v5.md`.

---

## QRT4.1 Filed Artifacts

QRT4.1 is the corrected Ramsey/T2 implementation generated outside the Codex-managed QRT4 workflow. It uses full six-fold condition-to-qubit rotation and a fitting-free coherence-envelope-area endpoint.

Filed paths:

- `docs/qrt41_osf_fields.md`
- `tests/qrt41_ramsey_test.py`
- `results/qrt41/qrt41_hardware_results.json`
- `results/qrt41/qrt41_calibration.json`
- `results/qrt41/calibration_snapshot_v41.json`

Hardware result summary from `results/qrt41/qrt41_hardware_results.json`:

- Job ID: `d94hi4lgc6cc73ff4cc0`
- Backend: `ibm_fez`
- `G_A = +2.87%`
- 95% CI: `[+2.36%, +3.46%]`
- Decision: `QRT_CONSISTENT_ESCALATE`

SHA-256 hashes:

- `docs/qrt41_osf_fields.md`: `987f08e05ede3825bc009f4166725c96dcefe2e3d4c476aa75832954f4a535bf`
- `tests/qrt41_ramsey_test.py`: `348696aa401d40c4557c559d8d7636aa3a7ee1336ae66315f188fb665fb1cd7b`
- `results/qrt41/qrt41_hardware_results.json`: `53c2eb6272b258dd321b2162664229e15e4d1ac700d08fc45bbfdd21c53123fb`
- `results/qrt41/qrt41_calibration.json`: `03878e4c22c466ebff0963c472289a1978ff0fa6ea8af91ffa83e2951aafade5`
- `results/qrt41/calibration_snapshot_v41.json`: `b75d8851c6b38512aafad0d9420b80e77927b3cad6be6fa1d42adf3fd5e995bf`

---

## QRT4.2 Filed Artifacts

QRT4.2 is the amplitude-scaling and multi-vector adjudication micro-test registered after the QRT4.1 escalation result. The completed IBM job result was added on 2026-07-05 and analyzed with the filed `tests/qrt42_scaling_test.py` logic.

Filed paths:

- `docs/qrt42_osf_fields.md`
- `tests/qrt42_scaling_test.py`
- `results/qrt42/qrt42_scaling_calibration.json`
- `results/qrt42/calibration_snapshot_v42.json`
- `results/qrt42/job-d94j866vtlqs73fucnvg-info.json`
- `results/qrt42/job-d94j866vtlqs73fucnvg-result.json`
- `results/qrt42/qrt42_hardware_results.json`

Hardware result summary from `results/qrt42/qrt42_hardware_results.json`:

- Job ID: `d94j866vtlqs73fucnvg`
- Backend: `ibm_marrakesh`
- Status: `Completed`
- `G_scale_10x = +1.07%`
- 95% CI: `[-0.16%, +2.24%]`
- Secondary `G_rep_1x = -0.88%`
- Secondary `G_phase_rand = -1.33%`
- Decision: `DOES_NOT_SCALE`

SHA-256 hashes:

- `docs/qrt42_osf_fields.md`: `53549c05fce951bf684dc2523f691c53a15ca37965a0b041c551c5b6ab7a1281`
- `tests/qrt42_scaling_test.py`: `9a386ccfb658f64417c5795ca7d1261ad1e1a80ff5bae1cc86f85f3099843318`
- `results/qrt42/qrt42_scaling_calibration.json`: `08d71f10a244447fa3e9bb95a9fd16ec8c0d43f9ed0fe2f86daefc92d6f0b2cc`
- `results/qrt42/calibration_snapshot_v42.json`: `f97e6584222407f27d1be57485510767c63b236fe19e4cf0642e4e68b036b758`
- `results/qrt42/job-d94j866vtlqs73fucnvg-info.json`: `4a16c5bece7d4f5e71b3327dbfd129aeca8c9c161d04d0bf4f58cba741131c2b`
- `results/qrt42/job-d94j866vtlqs73fucnvg-result.json`: `2377e600e5f376207c5374588a1ddc343e101729e5fa436b6292b8a761eeba5f`
- `results/qrt42/qrt42_hardware_results.json`: `b071679d4d67a4fa335103da84d7ad80901f8abd5b8a0e75a4e429f532b64515`

Note: `docs/qrt42_osf_fields.md` records the v4.2 script hash as `9a386ccfb658f64417c5795ca7d1261ad1e1a80ff5bae1cc86f85f3099843318`, matching the filed script. The filed outcome report contains an abbreviated v4.2 script hash beginning `75fed415`; that appears stale or refers to a different draft than the supplied `qrt42_scaling_test.py`. The repository preserves the report unchanged and records the actual filed-script hash here.

---

## Filed Outcome Report

Filed path:

- `reports/OUTCOME_REPORT_v4x.md`

SHA-256 hash:

- `reports/OUTCOME_REPORT_v4x.md`: `4fd2af2146132f08866f6c3f590ccc5a62e86e3f195fa80f2d227299c97a5813`

The report states:

- v4 verdict withdrawn as improperly derived.
- v4.1 returned `QRT_CONSISTENT_ESCALATE`.
- v4.2 returned `DOES_NOT_SCALE`.
- Proper QRT5 point-claim replication was filed separately after v4.2; see `docs/qrt5_artifact_manifest.md` and `reports/OUTCOME_REPORT_v5.md`.
- The Codex QRT5 packed-threshold draft remains unused design history under `unused_experiments/`.
