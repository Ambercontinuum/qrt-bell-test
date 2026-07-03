# DIVERGENCE.md — Frozen Protocol vs. Hardware Runner

The confirmatory session was submitted through `qrt_bell_run_ibm.py` rather
than the frozen file's own `--backend ibm` path, because that path calls
`backend.run()`, which was removed from qiskit-ibm-runtime before execution
(the current API requires the SamplerV2 primitive with ISA circuits). This
document is the complete accounting of what that substitution did and did not
change, so the audit trail contains no implicit trust.

## Executed verbatim from the frozen file (imported as a module)

The runner imports — and therefore executes the hashed bytes of — every
protocol-relevant component:

- `bell_hold_circuit` — construction of all 30 circuits (both arms, all
  frequencies, all bases)
- All parameters: `R0`, `FREQS_MHZ`, `BASES`, `SHOTS`, `SEED`
- The randomized execution order: rebuilt with the same seed and the same
  shuffle call; verified to reproduce the frozen order cell-for-cell (the
  simulator run's logged `executed_order` matches the runner's exactly)
- The full analysis chain: `parity_expectation`, `fidelity_from_parities`,
  `bootstrap_ci`

## Replaced (submission plumbing only)

- **Job submission:** `backend.run(tqc, shots=...)` → `SamplerV2.run([PUBs])`.
  Non-optional: the former no longer exists in the runtime client.
- **Transpilation:** `transpile(qc, backend, optimization_level=1)` →
  `generate_preset_pass_manager(backend=backend, optimization_level=1).run(qc)`.
  The latter is the pass-manager construction that `transpile` performs
  internally at the same optimization level; logged as a substitution for
  completeness.
- **Runtime options:** the runner explicitly disables dynamical decoupling
  and measurement/gate twirling. The frozen file did not specify these
  options (they did not exist in its API path). The preregistration's
  Transformations field forbids error suppression/mitigation in the
  confirmatory analysis; the runner's setting enforces the registration.
  This divergence is toward the registration, not away from it.

## Genuinely diverged: the decision block

- **Frozen file:** three branches — QRT-consistent (CI lower bound > 0 AND
  gain ≥ +2.5%), NULL (CI upper bound < +2.5%), else INCONCLUSIVE. No
  frequency-specificity check.
- **Runner:** identical branches, plus the registration's conjunct (c)
  (10 MHz must top the frequency profile) evaluated inside the
  QRT-consistent branch.
- **Discrepancy of record:** the frozen file and the OSF registration
  disagree — the registration requires conjunct (c); the frozen file omits
  it. The runner sided with the registration. This is disclosed rather than
  hidden: had the data landed in the QRT-consistent branch, the applicable
  rule would have been the registration's (the registration, not the script,
  is the binding preregistration document; the script is its attached
  implementation).
- **Materiality for the observed data: none.** The observed result fired the
  NULL branch (CI upper bound +0.62% < +2.5%), whose condition and text are
  character-identical in both files. The diverged branch never executed.

## Independent verification

**Execution of the frozen file was attempted, not merely declared impossible.**
On July 3, 2026, `python qrt_bell_test.py --backend ibm` was run against the
live service. It authenticated, selected ibm_marrakesh, transpiled its
circuits, and failed at the submission call (line 131) with
`qiskit_ibm_runtime.exceptions.IBMBackendError: 'Support for backend.run()
has been removed...'` — before any shot executed. The full log is committed
as `frozen_execution_attempt.log`. The necessity of the compatibility runner
is therefore demonstrated by the API's own error, not asserted.

`verify_frozen.py` closes the loop: it loads the raw hardware counts from
`results/qrt_hardware_results.json` and recomputes all fidelities, CIs, and
the decision using exclusively functions imported from the frozen file, with
the frozen file's decision block reproduced character-for-character. No
runner code participates. Its output (`qrt_frozen_verification.json`) is
committed alongside the hardware results.

Verdict under the frozen decision logic, on the hardware counts: **NULL —
falsified as specified** — identical to the runner's verdict. Executed
July 3, 2026: all fidelities, gains, and confidence intervals reproduced the
runner's values exactly (to four decimal places at every frequency), and the
frozen decision block returned the same NULL. Output committed as
`qrt_frozen_verification.json`.

## Summary

The hashed protocol could not be executed against the current IBM API in its
original form; its circuits, parameters, ordering, and statistics were
executed verbatim via import, its submission plumbing was replaced out of
necessity, and its decision logic has been re-applied to the raw hardware
data independently of the runner, producing the same verdict. The one
substantive discrepancy (conjunct (c)) is between the frozen script and the
registration, is disclosed here, favored the registration, and was never
reached by the data.
