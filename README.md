# QRT Hardware Adjudication Record

This repository contains the public experimental record for a sequence of
preregistered tests of Quantum Resonance Theory (QRT; Anson 2024,
DOI: [10.5281/zenodo.15105902](https://doi.org/10.5281/zenodo.15105902)) on
IBM superconducting quantum hardware.

The repository is organized as an audit and handoff package. It preserves
preregistration text, frozen scripts, hashes, raw job exports, calibration
records, outcome reports, and documented withdrawals. Confirmatory claims are
limited to preregistered primary endpoints.

The development methodology used for the experimental program is referred to
here as **coherence systems architecture**: a design technique for structuring
coherence experiments as linked systems of stated claims, control conditions,
hardware constraints, preregistered endpoints, escalation rules, artifact
boundaries, and reproducibility records.

## Status Summary

The current evidence record separates three claims:

| Claim class | Current status | Primary records |
|---|---|---|
| Bell-state fidelity enhancement at stated parameters | Falsified under the filed tests | `reports/OUTCOME_REPORT.md`, `docs/qrt2_osf_fields.md` |
| Simple drive-coupled amplitude-scaling mechanism | Not supported by v4.2 | `docs/qrt42_osf_fields.md`, `reports/OUTCOME_REPORT_v4x.md` |
| Stated-parameter Ramsey coherence point claim on a second device | Replicated under QRT5 primary rule | `docs/qrt5_osf_fields.md`, `reports/OUTCOME_REPORT_v5.md` |

This record does not establish QRT as a complete theory. The strongest current
finding is a replicated stated-parameter Ramsey coherence anomaly under the
filed QRT5 rule, with mechanism unresolved and independent verification required.

## Evidence Invariants

These statements are invariant across the filed reports and should not be
modified by exploratory interpretation:

1. Tests #1 and #2 closed the Bell-fidelity operationalizations negative under
   their preregistered decision rules.
2. The original v4 Ramsey verdict is withdrawn because the execution/analysis
   path was improperly derived.
3. v4.1 produced a QRT-consistent escalation trigger on the corrected
   Ramsey/T2 envelope-area endpoint.
4. v4.2 did not support the simple amplitude-scaling mechanism class.
5. Proper QRT5 replicated the stated-parameter point claim on a second device.
6. Secondary indices are descriptive only.
7. The next evidential step is independent-party execution of frozen materials.

## Result Overview

```text
Confirmatory result trajectory

Bell tests      v4            v4.1              v4.2              QRT5
---------       --------      ---------------   ---------------   -------------------------
negative  -->   withdrawn --> escalation hit -> no 10x scaling -> second-device replication
```

```text
Primary effect indices

v4.1  G_A          +2.87%   CI [+2.35%, +3.46%]   QRT_CONSISTENT_ESCALATE
v4.2  G_scale_10x  +1.07%   CI [-0.16%, +2.24%]   DOES_NOT_SCALE
QRT5  G_rep        +4.75%   CI [+4.22%, +5.24%]   REPLICATED_ON_SECOND_DEVICE

Scale guide: each # ~= 0.5 percentage points

v4.1  |######              |
v4.2  |##                  |
QRT5  |##########          |
```

## Program Timeline

| Stage | Endpoint | Status | Citation |
|---|---|---|---|
| Test #1 | Bell fidelity, phase/virtual drive | Falsified as specified | `reports/OUTCOME_REPORT.md` |
| Test #2 | Bell fidelity, physical fractional-RX drive | Falsified as specified | `docs/qrt2_osf_fields.md` |
| Test #3/QRT4 draft path | Ramsey/T2 physical-drive designs | Resource-constrained design iteration | `docs/qrt3_ramsey_prereg.md`, `docs/qrt4_balanced_packed_ramsey_prereg.md` |
| v4 | Balanced packed Ramsey | Verdict withdrawn | `reports/OUTCOME_REPORT_v4x.md` |
| v4.1 | Corrected Ramsey/T2 envelope-area endpoint | QRT-consistent escalation trigger | `docs/qrt41_osf_fields.md`, `results/qrt41/qrt41_hardware_results.json` |
| v4.2 | Amplitude-scaling discriminator | Does not scale | `docs/qrt42_osf_fields.md`, `results/qrt42/qrt42_hardware_results.json` |
| QRT5 proper | Second-device stated-point replication | Replicated on second device | `docs/qrt5_osf_fields.md`, `results/qrt5/qrt5_hardware_results.json` |

## Points Adjudicated Or Refuted

The following points are the main claims addressed by the filed tests:

1. **Bell-fidelity implementation of QRT enhancement.**  
   The early filed tests operationalized QRT as a Bell-state fidelity gain under
   weak resonance drive. Those tests returned negative decisions under their own
   rules. See `reports/OUTCOME_REPORT.md` and `docs/qrt2_osf_fields.md`.

2. **Validity of the original v4 Ramsey verdict.**  
   The v4 verdict is not used as evidence. The filed v4x outcome report records
   the withdrawal due to incomplete condition-to-qubit rotation and an invalid
   decay-only fit model for fringed Ramsey data. See
   `reports/OUTCOME_REPORT_v4x.md`.

3. **Corrected Ramsey coherence endpoint at QRT stated parameters.**  
   v4.1 tested the corrected envelope-area contrast at `10 MHz` and
   `R0 = 10^-3 rad`. It returned `G_A = +2.87%` with a positive 95% CI and the
   decision `QRT_CONSISTENT_ESCALATE`. The v4.1 preregistration explicitly
   treated this as escalation, not a final positive claim. See
   `docs/qrt41_osf_fields.md` and `reports/OUTCOME_REPORT_v4x.md`.

4. **Drive-coupled amplitude scaling.**  
   v4.2 tested whether a 10x-amplitude arm produced the large scaling expected
   under the registered drive-coupled mechanism discriminator. It returned
   `G_scale_10x = +1.07%`, CI `[-0.16%, +2.24%]`, and
   `DOES_NOT_SCALE`. This refutes the simple amplitude-scaling mechanism class
   targeted by v4.2, but does not by itself falsify the original `R0` point
   claim. See `docs/qrt42_osf_fields.md` and `reports/OUTCOME_REPORT_v4x.md`.

5. **Second-device replication of the stated-parameter point claim.**  
   QRT5 tested the stated point at confirmatory power on a second device. It
   returned `G_rep = +4.75%`, CI `[+4.22%, +5.24%]`, and
   `REPLICATED_ON_SECOND_DEVICE` under the filed rule. See
   `docs/qrt5_osf_fields.md`, `reports/OUTCOME_REPORT_v5.md`, and
   `results/qrt5/qrt5_hardware_results.json`.

## Working Hypothesis And Research Direction

The post-QRT5 working hypothesis is:

```text
The replicated QRT5 endpoint indicates a hardware-level coherence modulation at
or near the stated QRT point, 10 MHz and R0 = 10^-3 rad. The effect has positive
directional scope for QRT because the surviving signal is located at the theory's
stated frequency/amplitude point and replicated on a second device under the
filed rule. The present evidence does not identify the mechanism.
```

In relation to QRT, the result supports continued investigation of the theory's
coherence-point claim, not acceptance of the full theoretical framework. The
Bell-fidelity operationalizations remain falsified, and the v4.2 amplitude test
does not support a simple drive-coupled scaling mechanism. The surviving QRT
content is therefore narrower:

```text
QRT remains live only as a stated-parameter coherence-point research direction.
```

The leading mechanism-discrimination hypothesis is that the observed endpoint
lies at the boundary between QRT's resonance claim and known coherence-control
physics. Candidate explanations to separate in the next phase are:

- a QRT-specific coherence-point effect;
- a filter-function or device noise-spectrum feature near the tested condition;
- a dressed-frame, spin-locking, or continuous-drive response;
- a Floquet-like weak-drive sweet spot;
- crosstalk, spectator-qubit, calibration, or compilation artifacts.

The next research direction is independent replication followed by mechanism
discrimination. The next protocol family should vary, at minimum:

- frequency around 10 MHz with finer local resolution;
- amplitude around `R0 = 10^-3 rad`, including sub- and super-threshold arms;
- pulse placement and delay-grid geometry;
- backend, qubit topology, and calibration epoch;
- spectator-qubit loading and packed/unpacked layouts;
- explicit DD/mitigation controls and disabled-mitigation controls;
- phase randomization and sign/randomized-drive controls.

The expected outcome of this next phase is not a single positive/negative
verdict on all of QRT. It is a mechanism map: whether the QRT5 signal persists
as a frequency-localized, amplitude-structured, device-independent coherence
effect, or collapses into a known hardware-control/noise artifact class.

## Technical Background References

This section records the technical background used to frame the null
expectation. It is not a complete literature review of quantum control. The
citations below support the narrower claims needed for this repository.

A separate targeted prior-art and parallel-findings scan is filed at
`docs/prior_art_parallel_findings_review.md`. That review identifies adjacent
public mechanism families including dynamical decoupling, filter-function noise
spectroscopy, continuous driving/spin locking, dressed-state physics,
Floquet-engineered coherence enhancement, and IBM-device crosstalk suppression.
It did not identify an exact public match to the filed QRT5 endpoint structure,
but it should not be read as a legal novelty or patentability opinion.

| Background point | What the cited work supports |
|---|---|
| Standard circuit baseline | Quantum circuits are represented as specified unitary gates plus measurement/noise processes; absent an added mechanism, the model does not predict a special coherence gain at an isolated 10 MHz modulation point. |
| Virtual-Z implementation | IBM/Qiskit documents `RZGate` as a diagonal Z-axis gate that can be implemented virtually by frame changes with zero duration and zero gate error; McKay et al. describe arbitrary virtual Z gates for superconducting qubits. |
| Dynamical decoupling and mitigation practice | IBM documents DD, Pauli twirling, TREX, ZNE, PEA, and PEC as available Qiskit Runtime suppression/mitigation methods, and states that DD inserts physical pulse sequences on idle qubits to suppress coherent errors. |
| DD research context | Foundational and superconducting-qubit literature treats DD as pulse-sequence control for suppressing decoherence or performing noise spectroscopy, with sequence choice still an active research area. |
| Circuit vs pulse-level control | Qiskit Pulse literature states that the circuit model abstracts away the physical implementation of gates, while pulse-level programming exposes hardware-control degrees of freedom used for calibration, optimal control, DD, and mitigation research. |

The filed QRT program differs from ordinary error-suppression workflows because
it does not use DD, twirling, readout mitigation, or ZNE as hidden corrections to
produce the confirmatory endpoints. Instead, it tests preregistered contrasts
between specified drive/control conditions and reports the resulting primary
indices directly.

The early virtual-Z Bell-fidelity path is therefore treated as a stringent null
test: a positive effect from virtual-Z-only modulation would have been
nonstandard relative to the documented frame-change implementation. The later
physical-drive Ramsey tests are treated separately because they ask a different
hardware-control question: whether a specified weak physical drive condition
changes a preregistered Ramsey envelope-area endpoint.

## Artifact Map

For external review, start with these files:

| Purpose | File |
|---|---|
| v4 withdrawal, v4.1 result, v4.2 result | `reports/OUTCOME_REPORT_v4x.md` |
| QRT5 outcome report | `reports/OUTCOME_REPORT_v5.md` |
| v4.1/v4.2 hashes and filing record | `docs/qrt4x_artifact_manifest.md` |
| QRT5 hashes and filing record | `docs/qrt5_artifact_manifest.md` |
| Early implementation divergence audit | `docs/fable_divergence_audit.md` |
| Bell-test compatibility divergence record | `DIVERGENCE.md` |
| v4.1 hardware analysis JSON | `results/qrt41/qrt41_hardware_results.json` |
| v4.2 hardware analysis JSON | `results/qrt42/qrt42_hardware_results.json` |
| QRT5 hardware analysis JSON | `results/qrt5/qrt5_hardware_results.json` |

## OSF Registrations

| Stage | OSF registration | Local field copy |
|---|---|---|
| Test #1 Bell fidelity | [Preregistered Test of Quantum Resonance Theory's Bell-State Fidelity Prediction on Superconducting Quantum Hardware](https://osf.io/yg923) | `reports/OUTCOME_REPORT.md` |
| Test #2 physical drive | [Preregistered Test of Quantum Resonance Theory Under a Physically Delivered Periodic Drive on Superconducting Quantum Hardware](https://osf.io/74brn) | `docs/qrt2_osf_fields.md` |
| QRT3 Ramsey | [Preregistered Ramsey Test of Quantum Resonance Theory's 10 MHz Coherence Prediction on Superconducting Quantum Hardware](https://osf.io/u8fv7) | `docs/qrt3_ramsey_prereg.md` |
| QRT4 balanced packed Ramsey | [Preregistered Balanced Packed Ramsey Test of Quantum Resonance Theory's 10 MHz Coherence Prediction on Superconducting Quantum Hardware](https://osf.io/t2vs3) | `docs/qrt4_balanced_packed_ramsey_prereg.md` |
| v4.2 | [Preregistered Amplitude-Scaling and Multi-Vector Adjudication of a QRT-Consistent Coherence Result on Superconducting Hardware (v4.2)](https://osf.io/69pc2) | `docs/qrt42_osf_fields.md` |
| QRT5 proper | [Preregistered Confirmatory Replication of a QRT-Consistent Coherence Result at Stated Parameters on a Second Superconducting Device (v5)](https://osf.io/jw9d6) | `docs/qrt5_osf_fields.md` |
| Earlier registrations | Pending public release / embargo lift | `docs/qrt41_osf_fields.md` |

## Repository Layout

```text
docs/       preregistration fields, manifests, divergence audits
tests/      frozen or filed execution/analysis scripts
results/    hardware results, calibration files, raw job exports, derived analyses
reports/    outcome reports written after adjudication
```

Local-only notes and quarantined drafts are gitignored and are not part of the
public record.

## Reproducibility Notes

The filed result JSON files store IBM Runtime result payloads and derived
analysis outputs. The confirmatory analysis path is defined by the corresponding
frozen scripts and preregistered decision rules.

IBM account-linked identifiers such as exported `user_id` values are redacted
from public job-info files; job IDs, backend names, timestamps, status, cost,
calibration snapshots, raw counts, and result payloads are preserved.

Verify the QRT5 script hash before re-analysis:

```powershell
Get-FileHash tests\qrt5_escalation_test.py -Algorithm SHA256
```

Expected QRT5 script hash:

```text
E37FA996CBE2491DCDD02E1F8D4F72E5880838A72FD523C5697162AE12A267A7
```

The filed QRT5 primary result is:

```text
G_rep = +4.75%
95% CI = [+4.22%, +5.24%]
decision = REPLICATED_ON_SECOND_DEVICE
```

## AI-Assisted Research Process

AI assistance is part of the provenance record. The public record distinguishes
model-assisted drafting, coding, review, and reporting from confirmatory
inference.

Documented roles:

| Participant | Role in record |
|---|---|
| Amber Anson | Human author, theory owner, protocol direction, filing decisions, interpretation constraints |
| Claude/Fable | Preregistration drafting support and supplied v4.1/v4.2/QRT5 materials for filing |
| Codex | Repository operations, code/path review, divergence auditing, result ingestion, hash checks, JSON decoding, reports, provenance cleanup |

Governance rule:

```text
AI systems may assist design, audit, execution, decoding, and writing.
Confirmatory inference is limited to frozen preregistered endpoints.
Claims must remain traceable to scripts, hashes, raw data, and filed reports.
```

The organizing development technique for this work is coherence systems
architecture. In this repository, that means treating each experiment as a
bounded coherence-system test with explicit inputs, controls, decision rules,
failure modes, escalation criteria, and post-result artifact handling. The
technique is methodological and organizational; it is not itself an additional
confirmatory endpoint.

## Integrity Commitments

- Register before confirmatory execution.
- Freeze scripts and record SHA-256 hashes.
- Preserve raw counts, job IDs, calibration snapshots, and derived analyses.
- Publish falsifications, withdrawals, inconclusive results, and replications.
- Label exploratory observations as exploratory.
- Separate mechanism claims from point-claim replication.
- Disclose AI assistance and model provenance.
- Avoid undisclosed post-hoc endpoint migration.

## Citations And Internal References

- QRT source theory: Anson 2024, DOI
  [10.5281/zenodo.15105902](https://doi.org/10.5281/zenodo.15105902).
- Standard gate-model reference: Nielsen, M. A., and Chuang, I. L. (2010).
  *Quantum Computation and Quantum Information*, 10th Anniversary Edition,
  Cambridge University Press.
- IBM Quantum documentation: `RZGate`, documenting virtual frame-change
  implementation of Z-axis rotations:
  <https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.library.RZGate>.
- McKay, D. C., Wood, C. J., Sheldon, S., Chow, J. M., and Gambetta, J. M.
  (2017). "Efficient Z-Gates for Quantum Computing." *Physical Review A* 96,
  022330. DOI: <https://doi.org/10.1103/PhysRevA.96.022330>.
- IBM Quantum documentation: error mitigation and suppression techniques,
  including dynamical decoupling, twirling, TREX, ZNE, PEA, and PEC:
  <https://quantum.cloud.ibm.com/docs/en/guides/error-mitigation-and-suppression-techniques>.
- Viola, L., and Lloyd, S. (1998). "Dynamical suppression of decoherence in
  two-state quantum systems." *Physical Review A* 58, 2733. DOI:
  <https://doi.org/10.1103/PhysRevA.58.2733>.
- Bylander, J., Gustavsson, S., Yan, F., Yoshihara, F., Harrabi, K., Fitch, G.,
  Cory, D. G., Nakamura, Y., Tsai, J. S., and Oliver, W. D. (2011).
  "Dynamical decoupling and noise spectroscopy with a superconducting flux
  qubit." *Nature Physics* 7, 565-570. DOI:
  <https://doi.org/10.1038/nphys1994>.
- Alexander, T., Kanazawa, N., Egger, D. J., Capelluto, L., Wood, C. J.,
  Javadi-Abhari, A., and McKay, D. (2020). "Qiskit Pulse: Programming Quantum
  Computers Through the Cloud with Pulses." *Quantum Science and Technology*,
  5, 044006. DOI: <https://doi.org/10.1088/2058-9565/aba404>.
- Bell-test outcome record: `reports/OUTCOME_REPORT.md`.
- Test #2 preregistration fields: `docs/qrt2_osf_fields.md`.
- v4/v4.1/v4.2 outcome record: `reports/OUTCOME_REPORT_v4x.md`.
- v4.1 preregistration fields: `docs/qrt41_osf_fields.md`.
- v4.2 preregistration fields: `docs/qrt42_osf_fields.md`.
- QRT5 preregistration fields: `docs/qrt5_osf_fields.md`.
- QRT5 outcome record: `reports/OUTCOME_REPORT_v5.md`.
- QRT5 artifact manifest: `docs/qrt5_artifact_manifest.md`.
- Targeted prior-art and parallel-findings review:
  `docs/prior_art_parallel_findings_review.md`.

## Authorship

Amber Anson, AmberContinuum Research.

Protocol design, coding, review, and reporting were conducted through a
human-led, cross-model AI collaboration. Specific model roles are documented in
the preregistration fields, outcome reports, and manifests where relevant.

## License

Code: MIT. Data and documents: CC-BY 4.0.
