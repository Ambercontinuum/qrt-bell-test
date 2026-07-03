# Fable Divergence Audit — Original QRT Paper vs. Bell-Test Code

**Status:** audit note for repository record  
**Scope:** original QRT paper, Test #1 Bell-state code, Test #2 physical-drive code, and Codex peer review  
**Purpose:** document implementation divergences and the author's code-instinct concerns before Test #3 is frozen

---

## 1. Source-paper claims

The original paper, *Quantum Resonance Theory (QRT): A Mathematical Framework for Unified Quantum Mechanics*, gives three related but non-identical formulations:

- Wavefunction phase term: `R(t) = R0 cos(wr t)`, with `R0` approximately `10^-3 rad` and `wr` approximately `10 MHz`.
- Entanglement correlation term: `Eres(a,b) = -cos(theta_a - theta_b + Rtheta)`, with `Rtheta = R0 sin(wr t)`, predicting a 5% Bell-state fidelity boost.
- Hamiltonian perturbation term: `H(t) = H0 + V0 cos(wr t)`, with `V0` approximately `10^-3 eV`.

The paper's most explicit quantum-computing experimental statement is a Ramsey/coherence claim: superconducting-qubit `T2` should rise by 5-10% at `wr = 10 MHz`, tested with Ramsey interferometry.

---

## 2. Author concern to preserve

The author's concern was not "the theory cannot be wrong." The concern was that the falsifying tests may not have implemented the original paper's claim faithfully enough for the resulting falsification language to bind the theory rather than the code.

Specific concern:

- The code may have encoded a convenient runnable proxy instead of the source-paper stimulus.
- The falsification might be a result of hardcoded or poorly sampled values.
- Quantum-control code is not linearly obvious to audit by inspection, so implementation details can silently decide the outcome.
- A correct falsification must let the result emerge from a faithful physical test, not from a sampling mistake, virtual operation, or threshold mismatch.

Codex peer-review summary: that instinct is scientifically legitimate. It identifies implementation risk, not an escape from falsifiability.

---

## 3. Test #1 divergence: virtual drive and zero-crossing lock-in

Test #1 implemented the Bell-state prediction using `RZ(2 * R0 * sin(wr * t_k))` inside a sliced hold window.

Observed divergences:

- IBM hardware treats `RZ` as a virtual frame update, not as injected physical microwave energy.
- The paper includes a phase term, so a virtual phase operation is not irrational as an initial operationalization; however, the paper also gives a Hamiltonian perturbation form, and virtual `RZ` does not test that physical perturbation.
- The 10 MHz schedule used a 50 ns sample spacing: `HOLD_NS = 2000`, `N_SLICES = 40`, so `dt = 50 ns`.
- At 10 MHz the period is 100 ns. Sampling at `(k + 1) * 50 ns` evaluates `sin(pi * k)`, which is zero at every integer sample.
- Therefore the theory-designated 10 MHz drive in Test #1 was effectively absent at the exact primary frequency.

Material consequence:

Test #1 can be described as a falsification of the specific virtual-RZ, zero-sampled implementation that was run. It should not be treated as a clean falsification of a physical 10 MHz resonance drive or of the paper's Ramsey/T2 claim.

---

## 4. Test #2 divergence: physical drive, but still stroboscopic and near-aliasing

Test #2 corrected the physicality problem by using native fractional `RX` pulses with IBM fractional gates enabled. This was a meaningful improvement over Test #1.

Observed divergences:

- The paper's Hamiltonian term is continuous: `V0 cos(wr t)`.
- Test #2 approximated the drive as discrete fractional `RX` pulses.
- The schedule used 48 ns slices, placing 10 MHz close to the Nyquist boundary of the discrete control schedule.
- The off-resonance frequencies included 20 and 50 MHz, which can become alias-prone under discrete sampling.
- The primary endpoint remained Bell-state fidelity/frequency contrast, whereas the paper's most explicit quantum-computing setup points to Ramsey/T2.

Material consequence:

Test #2 is a stronger physical-drive test than Test #1, but it still binds a discrete fractional-RX Bell-test operationalization. It does not exhaust the original paper's continuous-drive or Ramsey/T2 parameterization.

---

## 5. Parameter divergence: R0 versus V0

The paper gives both:

- `R0 approximately 10^-3 rad`
- `V0 approximately 10^-3 eV`

The Bell tests used the radian phase-amplitude value as a gate angle. That is a practical circuit-level mapping, but it leaves the `V0` energy-perturbation statement untested unless a hardware-calibrated conversion is declared.

Material consequence:

Future claims should specify which source-paper parameter is being tested. If testing `R0`, say the result binds the phase-amplitude implementation. If testing `V0`, the preregistration needs a defensible hardware calibration pathway.

---

## 6. Decision-threshold and endpoint divergence

The Bell tests used a +2.5% threshold because the Bell prediction was approximately +5% fidelity. That threshold is reasonable for the Bell-fidelity endpoint, but the original paper's Ramsey/coherence claim states a 5-10% `T2` increase.

Material consequence:

For a Ramsey/T2 test, the threshold should be +5%, the lower edge of the paper's stated coherence prediction, not +2.5% inherited from the Bell-test design.

---

## 7. Codex peer-review findings

Findings:

- The author's suspicion that code details could be deciding the verdict was valid.
- Test #1 contained a serious stimulus-construction flaw at the primary 10 MHz condition.
- Test #2 addressed physicality but not the deeper issue that a discrete circuit schedule is not automatically equivalent to the paper's continuous perturbation.
- The strongest next test should keep Test #2's physical-drive correction but change the endpoint to Ramsey/T2 and require a waveform audit before hardware execution.
- Any new test must distinguish between "falsified as coded" and "falsified as stated in the source paper."

Recommended corrective action:

- Create Test #3 as a new preregistration, not a reinterpretation of Tests #1 or #2.
- Use a physical fractional-`RX` hardware path, as in Test #2.
- Target Ramsey/T2, because the paper explicitly names that endpoint and method.
- Include a mandatory waveform audit checking RMS amplitude, phase coverage, zero-crossing lock-in, and alias similarity between controls.
- Freeze the script hash, sampling schedule, control frequencies, fit model, and decision rule before confirmatory hardware execution.

---

## 8. Record statement

The prior falsifications remain records of the protocols that were run. This audit does not erase them. It records that the protocols diverged from the original paper in ways that matter for interpretation.

The author's instinct was therefore not a post-hoc refusal to be wrong. It was an implementation-validity objection: before accepting a falsification of the theory, verify that the code actually implemented the theory's stated physical claim.
