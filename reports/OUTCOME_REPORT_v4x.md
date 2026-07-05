# Outcome Report — QRT Ramsey/T2 Program: v4 (withdrawn), v4.1 (QRT-consistent escalation trigger), v4.2 (does not scale)

**Author:** Amber Anson, AmberContinuum Research
**Protocol and analysis drafted in collaboration with:** Claude (Anthropic); v4 implementation by a third-party AI coding tool under the author's design
**Theory under test:** Quantum Resonance Theory (Anson 2024, DOI 10.5281/zenodo.15105902) — prediction: superconducting-qubit coherence increases 5–10% under a physical periodic drive at ωr = 10 MHz, R0 = 10⁻³ rad.

---

## 1. v4 (job d940k9lgc6cc73feh290, ibm_marrakesh) — VERDICT WITHDRAWN

The v4 execution used the author's balanced-packed layout with two implementation flaws identified post-hoc: (a) only 2 of 6 condition-to-qubit rotations were executed, confounding condition with physical-qubit position on hardware whose per-qubit behavior varies by more than an order of magnitude; (b) the analysis fit a pure-decay model to Ramsey data exhibiting detuning fringes (~50–85 kHz per qubit), producing invalid coherence estimates (parameters pinned at bounds). The apparent anomalies in that run — non-monotone "revivals" and extreme T2 spread — are fully explained as Ramsey fringes under a misspecified model; same-qubit condition pairs were statistically identical, showing no drive effect resolvable in that design. **The v4 falsification verdict was withdrawn by the author as improperly derived, rather than claimed.** Raw data published.

## 2. v4.1 (job d94hi4lgc6cc73ff4cc0, ibm_fez, July 4 2026) — QRT-CONSISTENT AT STATED PARAMETERS; NO CLAIM; ESCALATION MANDATED

Corrected implementation, preregistered (frozen; script SHA-256 348696aa…cd7b; calibration 03878e4c…ade5): full 6-fold rotation (condition × qubit fully crossed), fitting-free primary index (coherence-envelope area, |P(0)−0.5| integrated over the delay grid), same-qubit paired difference contrast, physical fractional-RX drive with pre-submission physicality assertion (passed, 72/72), no mitigation, randomized order (seed 20260705), 72 circuits × 6,000 shots.

**Result:** G_A = **+2.87%**, bootstrap 95% CI **[+2.35%, +3.46%]**. Preregistered decision: **QRT_CONSISTENT_ESCALATE** — the first H1-branch outcome in the program's four hardware executions.

Descriptive structure:
- 10 MHz sits at or near the top of the driven conditions on five of six physical qubits — a small effect consistent across independent qubits.
- The undriven reference exceeds every driven condition on every qubit (uniform physical drive damage; replicates Test #2's signature and confirms the drive is physically real).
- Post-hoc artifact check, performed and passed: variance decomposition attributes 96% of cell variance to physical-qubit identity, 0% to rotation, ~3% to condition — the transpiler's virtual→physical mapping was stable across all 72 circuits, so the same-qubit pairing assumption holds and a layout confound is excluded.
- **Declared caution:** the frequency profile is not a clean peak. 1 MHz runs nearly as high as 10 MHz on several qubits, with 5/15/25 MHz lower. A genuine QRT resonance predicts a local peak at 10 MHz; elevation at both 1 and 10 MHz is also consistent with a frequency-dependent pulse-train × noise-spectrum interaction (a filter-function-class effect within standard quantum mechanics). The confirmatory index cannot distinguish these; the escalation protocol is designed to.

**Per the registration's own terms, this result is treated as an artifact until it survives: (i) replication on a second fractional-gate device, (ii) an amplitude sweep (R0 × {0.1, 1, 10}), and (iii) drive-phase randomization.** No positive claim is made or implied by this report.

## 3. v4.2 amplitude-scaling micro-discriminator (job d94j866vtlqs73fucnvg, ibm_marrakesh, July 4-5 2026) — DOES NOT SCALE

Preregistered amplitude-scaling and multi-vector adjudication of the v4.1 QRT-consistent result, frozen to `qrt42_scaling_test.py` (SHA-256 `9a386ccfb658f64417c5795ca7d1261ad1e1a80ff5bae1cc86f85f3099843318`). The run used a second device relative to v4.1 (`ibm_marrakesh`, not `ibm_fez`), full six-fold condition-to-qubit rotation, four Ramsey delays, 5,000 shots per circuit, physical fractional-RX drive, and the preregistered amplified-arm contrast:

```text
G_scale = A(10 MHz @ 10x R0) / mean(A(9 MHz @ 1x R0), A(11 MHz @ 1x R0)) - 1
```

**Result:** G_scale = **+1.07%**, bootstrap 95% CI **[-0.16%, +2.24%]**. Preregistered decision: **DOES_NOT_SCALE** because the 95% CI upper bound falls below the +3% amplitude-scaling threshold.

Secondary descriptive indices:

- G_rep(10 MHz @ 1x vs 9/11 MHz neighbors) = **-0.88%**.
- G_phase_rand(10 MHz randomized phase vs 9/11 MHz neighbors) = **-1.33%**.

Interpretation under the v4.2 registration: the v4.1 QRT-consistent result does **not** survive the amplitude-scaling discriminator. This removes the drive-coupled scaling interpretation targeted by v4.2 and favors a non-scaling artifact/noise-spectrum/filter-function explanation over a QRT-class amplitude-coupled mechanism. Per the v4.2 registration's own scope statement, a DOES_NOT_SCALE outcome does not formally falsify the original paper's exact R0-point prediction; it adjudicates the v4.1 escalation result against the registered scaling mechanism.

## 4. Program standing

| Test | Form | Verdict |
|---|---|---|
| #1 (Bell, phase modulation) | virtual RZ drive | Falsified as specified |
| #2 (Bell, physical drive) | fractional RX | Falsified as specified |
| v4 (Ramsey) | flawed implementation | Verdict withdrawn |
| v4.1 (Ramsey, corrected) | fractional RX | QRT-consistent escalation trigger |
| v4.2 (amplitude scaling) | fractional RX | **Does not scale** |

The Bell-fidelity prediction remains falsified in both implementable forms. The corrected v4.1 Ramsey implementation produced a QRT-consistent escalation trigger, but v4.2 did not support the registered amplitude-scaling mechanism needed to interpret that trigger as drive-coupled. The current program standing is therefore: v4.1 found an anomaly worth escalating; v4.2 failed the first scaling adjudication of that anomaly.

Subsequent proper QRT5 point-claim replication is reported separately in `reports/OUTCOME_REPORT_v5.md`.

All raw data, frozen scripts, hashes, calibration snapshots, and this report are published together regardless of outcome, per every registration in the program.
