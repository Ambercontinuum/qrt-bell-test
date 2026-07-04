# QRT v4.x Artifact Manifest

**Status:** repository filing record for Fable/Claude QRT v4.1 and v4.2 artifacts  
**Filed by:** Codex  
**Filed on:** 2026-07-04  
**Purpose:** preserve the v4.x sequence before any QRT5 execution or adjudication

---

## Program Timeline Boundary

This manifest records that the QRT4.1 and QRT4.2 materials were added to the repository after Codex-managed QRT work through QRT4 and after a draft QRT5 preregistration had been prepared.

QRT5 remains preemptive and has not been adjudicated or run in this repository record. QRT5 should be interpreted as pending the QRT4.2 outcome unless explicitly rerun or re-registered after the v4.2 result is available.

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

QRT4.2 is the amplitude-scaling and multi-vector adjudication micro-test registered after the QRT4.1 escalation result. At the time of filing, the provided outcome report states that QRT4.2 is pending.

Filed paths:

- `docs/qrt42_osf_fields.md`
- `tests/qrt42_scaling_test.py`
- `results/qrt42/qrt42_scaling_calibration.json`
- `results/qrt42/calibration_snapshot_v42.json`

SHA-256 hashes:

- `docs/qrt42_osf_fields.md`: `53549c05fce951bf684dc2523f691c53a15ca37965a0b041c551c5b6ab7a1281`
- `tests/qrt42_scaling_test.py`: `9a386ccfb658f64417c5795ca7d1261ad1e1a80ff5bae1cc86f85f3099843318`
- `results/qrt42/qrt42_scaling_calibration.json`: `08d71f10a244447fa3e9bb95a9fd16ec8c0d43f9ed0fe2f86daefc92d6f0b2cc`
- `results/qrt42/calibration_snapshot_v42.json`: `f97e6584222407f27d1be57485510767c63b236fe19e4cf0642e4e68b036b758`

Note: `docs/qrt42_osf_fields.md` records the v4.2 script hash as `9a386ccfb658f64417c5795ca7d1261ad1e1a80ff5bae1cc86f85f3099843318`, matching the filed script. The filed outcome report contains an abbreviated v4.2 script hash beginning `75fed415`; that appears stale or refers to a different draft than the supplied `qrt42_scaling_test.py`. The repository preserves the report unchanged and records the actual filed-script hash here.

---

## Filed Outcome Report

Filed path:

- `reports/OUTCOME_REPORT_v4x.md`

SHA-256 hash:

- `reports/OUTCOME_REPORT_v4x.md`: `9e2cc9439e40e521018da8baffaee96d24ee7ac7c6871b0b6ab976831ba7d509`

The report states:

- v4 verdict withdrawn as improperly derived.
- v4.1 returned `QRT_CONSISTENT_ESCALATE`.
- v4.2 micro-discriminator result pending.
- QRT5/escalation should not be treated as adjudicated until v4.2 has been incorporated.

