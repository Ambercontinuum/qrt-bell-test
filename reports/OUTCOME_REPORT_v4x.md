# Outcome Report — QRT Ramsey/T2 Program: v4 (withdrawn), v4.1 (QRT-consistent, escalation pending), v4.2 (micro-discriminator, result pending)

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

## 3. v4.2 micro-discriminator (preregistered; script SHA-256 75fed415…6d96a9) — RESULT PENDING

One-sided neighbor test executed within residual QPU quota: is the 10 MHz elevation locally peaked (resonance signature) or shared by 9/11 MHz (broad-artifact signature)? Conditions {10, 9×2, 11×2, REF}, full rotation, 4-delay grid, declared one-sided decision (LOCAL_PEAK_REPLICATED / PEAK_NOT_DETECTED); the budget cannot support and does not claim a falsification branch. Result to be appended on completion.

## 4. Program standing

| Test | Form | Verdict |
|---|---|---|
| #1 (Bell, phase modulation) | virtual RZ drive | Falsified as specified |
| #2 (Bell, physical drive) | fractional RX | Falsified as specified |
| v4 (Ramsey) | flawed implementation | Verdict withdrawn |
| v4.1 (Ramsey, corrected) | fractional RX | **QRT-consistent; escalation pending** |
| v4.2 (neighbor micro-test) | fractional RX | Pending |

The Bell-fidelity prediction is dead in both implementable forms. The coherence prediction, under the strictest estimator in the program, returned its first surviving result — gated behind three preregistered kill conditions, with a named standard-QM alternative (filter-function interaction) that the 1 MHz elevation currently favors. Escalation (v5) is preregistration-ready: second device, amplitude sweep, phase randomization, each arm targeting a specific alternative hypothesis.

All raw data, frozen scripts, hashes, calibration snapshots, and this report are published together regardless of outcome, per every registration in the program.
