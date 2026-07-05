# QRT v5 Artifact Manifest

**Status:** repository filing record for proper QRT v5 artifacts  
**Filed by:** Codex  
**Filed on:** 2026-07-05  
**Purpose:** preserve the preregistered QRT v5 point-claim replication package and result

---

## Provenance Boundary

This manifest records the proper QRT v5 package supplied from Downloads on 2026-07-05:

- `qrt5_osf_fields.md`
- `qrt5_escalation_test.py`
- `qrt5_calibration.json`
- IBM job result `d957fkuvtlqs73fv33i0`

This proper QRT v5 package is separate from the earlier Codex-drafted packed-threshold design, which is quarantined under `unused_experiments/qrt5_packed_threshold_design/` as unused Codex design history. The quarantined design is not part of this QRT v5 result.

---

## Filed Artifacts

Filed paths:

- `docs/qrt5_osf_fields.md`
- `tests/qrt5_escalation_test.py`
- `results/qrt5/qrt5_calibration.json`
- `results/qrt5/job-d957fkuvtlqs73fv33i0-info.json`
- `results/qrt5/job-d957fkuvtlqs73fv33i0-result.json`
- `results/qrt5/qrt5_hardware_results.json`
- `reports/OUTCOME_REPORT_v5.md`

SHA-256 hashes:

- `docs/qrt5_osf_fields.md`: `8106bd0603d0391e6f1c142c5c67bb1338d4cf537946d1e4837196dba2206052`
- `tests/qrt5_escalation_test.py`: `e37fa996cbe2491dcdd02e1f8d4f72e5880838a72fd523c5697162ae12a267a7`
- `results/qrt5/qrt5_calibration.json`: `28336337f5a2c774dff0f1d3d0065f08a3a771da93a5726eb5779169276a912f`
- `results/qrt5/job-d957fkuvtlqs73fv33i0-info.json`: `1540671e6e8174477f12f002fad64b2eb00a973a8c4f3cc8ac6427d60478c436`
- `results/qrt5/job-d957fkuvtlqs73fv33i0-result.json`: `8ee29b20ab162c0e75812aaf9c6000e3e26d66af3237e64469bc90da294a8106`
- `results/qrt5/qrt5_hardware_results.json`: `3e484e384c7709c3867abc502337cc59c9deb4c1d7bca2fffc5c300f506acde7`
- `reports/OUTCOME_REPORT_v5.md`: `9f3f22bc1eefd109757e339e34380a12388b661d80cd6a37fc20a17cc2d93b51`

---

## Hardware Result Summary

From `results/qrt5/qrt5_hardware_results.json`:

- Job ID: `d957fkuvtlqs73fv33i0`
- Backend: `ibm_marrakesh`
- Status: `Completed`
- Created: `2026-07-05T15:27:16.161957Z`
- Circuits/PUBs: 72
- Total shots: 432,000
- Primary `G_rep = +4.75%`
- 95% CI: `[+4.22%, +5.24%]`
- Preregistered decision: `REPLICATED_ON_SECOND_DEVICE`

Secondary descriptive indices, with no inferential weight under the preregistration:

- `G_amp_10x = -1.81%`
- `G_phase_rand = +2.42%`

---

## Interpretation Boundary

The preregistered primary endpoint replicated on a second non-`ibm_fez` device under the QRT v5 decision rule.

Per the QRT v5 registration, this means the paper's point claim survives the second-device confirmatory test at the stated 10 MHz / R0 parameter point. It does not by itself constitute final confirmation of QRT. The preregistered next step is independent-party verification.

The secondary indices are descriptive only. They may inform successor designs but cannot support or defeat the confirmatory QRT v5 decision.
