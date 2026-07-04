# QRT4 Result And Exploratory Note

**Test:** QRT4 balanced packed Ramsey/T2 test  
**Registration:** Preregistered Balanced Packed Ramsey Test of Quantum Resonance Theory's 10 MHz Coherence Prediction on Superconducting Quantum Hardware  
**Script:** `tests/qrt4_balanced_packed_ramsey_test.py`  
**Script SHA-256:** `d97c88ed1018e8290e7facd50dd264eaf699f585b62705b44e64ed4f2a769a5f`  
**IBM job ID:** `d940k9lgc6cc73feh290`  
**Backend:** `ibm_marrakesh`  
**Result file:** `results/qrt4_hardware_results.json`

---

## Confirmatory Result

The preregistered QRT4 prediction was:

> A physically delivered 10 MHz resonance drive increases fitted Ramsey coherence
> time T2* by at least +5% relative to matched off-resonance driven controls.

The observed primary index was:

```text
G_T2 = -77.30%
95% CI = [-77.66%, -76.98%]
decision = FALSIFIED_AS_SPECIFIED
```

Under the preregistered QRT4 implementation, the predicted +5% to +10% 10 MHz
T2* coherence gain was not observed. The 10 MHz condition fitted substantially
worse than the off-resonance driven control aggregate.

This falsifies the preregistered QRT4 operationalization as specified. It does
not, by itself, adjudicate every possible continuous-drive or hardware-native
formulation of QRT. The tested implementation was limited to what IBM public
superconducting hardware allowed:

- balanced packed multi-qubit Ramsey circuits,
- discrete sampled fractional-RX drive approximation,
- public backend calibration/noise environment,
- marginal-count T2* fitting,
- and the preregistered off-resonance control aggregate.

---

## Fitted T2* Summary

The retrieved hardware analysis produced the following fitted T2* values:

```text
10MHz:  2,582.74 ns
15MHz: 33,020.78 ns
1MHz:   5,258.43 ns
25MHz:  4,086.91 ns
5MHz:   3,151.38 ns
REF:  112,733.56 ns
```

These fits are the basis for the preregistered primary verdict. They should be
reported as the confirmatory result.

---

## Exploratory Finding

Although the preregistered 10 MHz T2* gain failed, the packed readout was not
featureless. The raw packed bitstrings show a structured, tau-localized
joint-state population transition.

The most prominent observed packed state was `011001`. Its counts across the
15 tau points were:

```text
tau ns:  0, 857, 1714, 2571, 3429, 4286, 5143, 6000, 6857, 7714, 8571, 9429, 10286, 11143, 12000

rep 0:   0, 13, 86, 438, 1369, 2918, 4538, 5543, 6037, 5472, 4185, 2824, 1801, 1249, 832
rep 1:   0, 7, 72, 348, 1114, 2452, 3954, 5183, 5958, 5771, 4689, 3479, 2352, 1557, 1100
```

This is a real structure in the hardware readout: the population rises from
near zero, peaks in the mid-delay region, and then decays or gives way to other
joint states.

However, because the balanced packed design rotated condition-to-qubit
assignment across repetitions, this joint bitstring pattern does not track the
10 MHz condition label. It tracks a physical packed-readout pattern more than a
frequency-specific 10 MHz coherence gain.

Therefore, this structure is exploratory. It cannot alter the preregistered
QRT4 verdict.

---

## Interpretation Boundary

The correct interpretation is two-layered:

1. **Confirmatory:** QRT4 falsified the preregistered 10 MHz T2* coherence-gain
   prediction under the frozen balanced packed Ramsey implementation.
2. **Exploratory:** QRT4 revealed a reproducible tau-dependent joint-state
   population structure that may point to a different threshold/correlation
   phenomenon.

This is not a positive QRT4 result. It is a failed preregistered endpoint that
generated a new exploratory target.

---

## Candidate Follow-Up Hypothesis

A future QRT5-style preregistration could test a different claim:

> Packed Ramsey circuits exhibit reproducible threshold-like joint-state
> population transitions as a function of tau, independent of condition-label
> assignment, and those transitions may be modulated by drive frequency or
> hardware geometry.

This would require a new registration with a new primary endpoint, likely based
on joint-bitstring population geometry rather than single-condition T2* gain.

Possible preregistered endpoints:

- peak tau and peak height of selected joint-state populations,
- entropy or concentration of packed-state distributions as a function of tau,
- reproducibility of joint-state transition curves across assignment rotations,
- condition-label independence versus frequency-modulated deviations,
- and backend/qubit-geometry replication.

Any such test must be treated as new confirmatory work, not as a reinterpretation
of the QRT4 primary outcome.
