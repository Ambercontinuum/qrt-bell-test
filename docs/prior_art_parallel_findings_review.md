# Prior-Art And Parallel-Findings Review

**Date:** 2026-07-05  
**Scope:** targeted public-literature scan for mechanisms adjacent to the QRT
hardware program  
**Status:** public review note; not a patentability opinion; not an exhaustive
literature review

## Purpose

This note records a targeted prior-art and parallel-findings scan for the QRT
hardware-adjudication repository. The goal is to identify public mechanisms that
could plausibly overlap with, explain, or contextualize the observed Ramsey
coherence results:

- weak or periodic drive effects on superconducting-qubit coherence;
- Ramsey/T2 coherence modification;
- dynamical decoupling and filter-function physics;
- spin-locking or continuous dynamical decoupling;
- dressed-state and Floquet coherence engineering;
- virtual-Z/frame-change behavior;
- IBM/Qiskit runtime mitigation and suppression practice.

This review does not assert novelty in the legal sense. It identifies related
public work and distinguishes the filed QRT experiments from the closest known
families.

## Search Summary

Search terms included combinations of:

```text
superconducting qubit coherence weak drive resonance Ramsey
superconducting qubit continuous drive coherence protection spin locking
superconducting qubit dynamical decoupling noise spectroscopy Ramsey filter function
superconducting qubit Floquet drive coherence enhancement periodic modulation
10 MHz superconducting qubit Ramsey coherence drive
milliradian superconducting qubit drive coherence
10^-3 rad quantum gate pulse superconducting qubit coherence
virtual Z gate frame change superconducting qubit
Qiskit Runtime dynamical decoupling twirling ZNE TREX
```

No public source was found in this scan that exactly matches the filed QRT5
claim structure:

```text
stated 10 MHz point
R0 = 10^-3 rad weak physical drive
Ramsey envelope-area endpoint
symmetric 9/11 MHz neighbor controls
second-device preregistered replication rule
IBM cloud superconducting hardware result package
```

That absence is not proof of novelty. It means the closest public material found
falls into adjacent mechanism families rather than the same filed endpoint.

## Findings By Mechanism Family

### 1. Standard Gate-Model Baseline

The standard circuit model treats quantum programs as specified gates/unitaries
plus measurement and noise processes. It does not contain a default mechanism by
which a weak drive at an isolated 10 MHz point should improve coherence unless
such a Hamiltonian/control/noise mechanism is explicitly introduced.

**Relevance to QRT:** this supports the null framing used by the repository.
It does not by itself rule out hardware-control effects, because real devices
are open driven systems.

**Reference:** Nielsen and Chuang, *Quantum Computation and Quantum
Information*.

### 2. Virtual-Z / Frame-Change Prior Art

IBM/Qiskit documents `RZGate` as implementable virtually by frame changes, with
zero duration and zero gate error in the compiled control model. McKay et al.
showed efficient arbitrary virtual Z gates for superconducting qubits and used
them to improve algorithmic performance and correct pulse errors.

**Relevance to QRT:** the early virtual-Z Bell-fidelity tests were stringent
null tests. A positive coherence/fidelity effect from virtual-Z-only modulation
would be nonstandard because virtual Z is not a physical microwave pulse acting
during a hold. The later movement to physical fractional rotations and Ramsey
endpoints was therefore methodologically appropriate.

**Closest overlap:** virtual phase control and pulse-error correction.

**Key distinction:** QRT5 is not a virtual-Z claim; it is a physical-drive
Ramsey coherence endpoint.

### 3. Dynamical Decoupling

Dynamical decoupling (DD) is established prior art for preserving coherence by
applying pulse sequences that average or refocus environmental coupling. Viola
and Lloyd provide a foundational two-state-system treatment. Bylander et al.
demonstrate DD and noise spectroscopy in a superconducting flux qubit, including
large T2 improvement under CPMG pulse trains. IBM's current documentation lists
DD as an error-suppression option that inserts physical pulse sequences on idle
qubits.

**Relevance to QRT:** DD is the closest broad family for "external control can
improve coherence." It also shows that pulse timing can select spectral
features of the environment.

**Closest overlap:** pulse-sequence-based coherence protection and spectral
filtering.

**Key distinction:** QRT5 does not use a conventional DD pulse train as the
confirmatory mechanism. It tests a specified weak-drive condition against
frequency-neighbor controls with an unmitigated preregistered endpoint.

### 4. Filter-Function And Noise-Spectroscopy Literature

DD-based noise spectroscopy treats controlled pulse sequences as filters that
map environmental spectral density into coherence decay. Szańkowski et al.
review this framework for qubits under DD, including solid-state systems such
as superconducting qubits. Cywiński et al. analyze engineered pulse sequences
for extending dephasing time in superconducting qubits and using coherence
decay under pulse sequences as a spectroscopy tool.

**Relevance to QRT:** this is a serious alternative interpretive family. A
localized effect near 10 MHz could reflect filter-function interaction with a
device-specific noise spectrum rather than a new theoretical mechanism.

**Closest overlap:** coherence changes dependent on timing/frequency structure.

**Key distinction:** the filed QRT5 endpoint is not a reconstruction of the
noise power spectral density and does not use a standard DD filter sequence.
The result should therefore be described as a replicated anomaly requiring
independent verification, not as mechanism confirmation.

### 5. Continuous Driving, Spin Locking, And Dressed States

Continuous dynamical decoupling and spin-locking approaches protect coherence by
placing the qubit in a driven/dressed frame. Public literature includes dressed
states under strong microwave driving in superconducting qubits, continuous
drive coherence-protection work in other qubit platforms, and recent
superconducting/transmon work on gates in continuously dynamically decoupled
systems.

**Relevance to QRT:** continuous-drive and dressed-state methods show that
drives can change coherence properties in real hardware.

**Closest overlap:** drive-modified coherence under sustained or strong control.

**Key distinction:** these methods typically use explicit dressed-frame or
spin-locking physics and drive amplitudes chosen for Rabi/dressed-state control,
not a milliradian-level stated QRT point with 9/11 MHz neighbor controls.

### 6. Floquet-Engineered Coherence Enhancement

Floquet engineering provides a direct public example of periodic drive creating
high-coherence operating points in superconducting circuits. Mundada et al.
report Floquet-engineered enhancement of coherence times in a driven fluxonium
qubit by dynamically inducing flux-insensitive sweet spots, with Ramsey-type
measurements showing large enhancement at a dynamical sweet spot.

**Relevance to QRT:** this is the strongest parallel in the broad sense that a
periodic drive can create a coherence-enhancing operating point.

**Closest overlap:** periodic-drive-induced coherence improvement in a
superconducting circuit.

**Key distinction:** the mechanism is Floquet quasienergy engineering in
fluxonium with deliberate dynamical sweet-spot construction. QRT5 is a
transpiled IBM cloud hardware Ramsey point-claim test at a weak stated drive
condition. Floquet work supports plausibility that driven systems can have
coherence sweet spots; it does not directly explain or confirm the QRT5 endpoint.

### 7. Crosstalk Suppression And IBM Hardware DD

Tripathi et al. propose and experimentally demonstrate DD-based suppression of
crosstalk on IBM superconducting cloud processors, including improvements in
quantum memory and gate performance. The paper emphasizes that fixed-frequency
transmon processors have coherent and incoherent crosstalk sources and that DD
can be practically useful on IBM devices.

**Relevance to QRT:** IBM cloud processors can show measurable coherence and
memory changes under structured control protocols.

**Closest overlap:** IBM-device coherence/memory improvement under pulse
protocols.

**Key distinction:** the mechanism is DD/crosstalk suppression, not a weak
10 MHz stated-parameter Ramsey point.

## Interpretive Consequences For QRT

The prior-art scan supports a conservative interpretation:

1. The Bell-fidelity virtual-Z path had a strong null expectation because
   virtual Z is documented as frame-change control rather than a physical drive.

2. Physical-drive Ramsey tests are the appropriate class for testing a hardware
   coherence effect, because pulse-level and driven-system literature shows that
   physical drives can modify coherence.

3. The QRT5 result should not be described as proving a new mechanism. Adjacent
   literatures provide plausible conventional families: DD/filter-function
   behavior, device noise spectroscopy, continuous-drive dressed-state physics,
   crosstalk suppression, and Floquet-engineered sweet spots.

4. The currently defensible public label remains:

   ```text
   replicated stated-parameter Ramsey coherence anomaly
   ```

5. The most important next step is independent-party replication and mechanism
   discrimination, especially controls that can separate:

   - QRT-specific point claim;
   - device-specific noise spectral feature;
   - filter-function artifact;
   - crosstalk or spectator-qubit effect;
   - drive calibration/nonlinearity;
   - Floquet/dressed-state-like coherence modification.

## Gap Identified By This Scan

The closest known families show that coherence improvement under structured
control is not unprecedented. However, this scan did not find a public result
with the same combination of:

- 10 MHz stated point;
- milliradian-scale physical drive;
- Ramsey envelope-area endpoint;
- symmetric neighbor frequency controls;
- preregistered second-device replication rule;
- IBM cloud hardware execution record.

This is a gap statement, not a novelty claim.

## Recommended Next Literature Work

For a more complete review, the next pass should include:

- formal patent search;
- IEEE/APS/ACM database search by exact control mechanism;
- search of IBM Quantum, Google Quantum AI, Rigetti, and academic transmon
  control papers for weak-drive coherence anomalies;
- search for device-specific low-frequency modulation artifacts near 10 MHz;
- review of filter-function calculations for the exact QRT pulse schedule;
- consultation with an independent superconducting-qubit control specialist.

## References

- Nielsen, M. A., and Chuang, I. L. (2010). *Quantum Computation and Quantum
  Information*, 10th Anniversary Edition. Cambridge University Press.
- IBM Quantum documentation. `RZGate`.
  <https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.library.RZGate>.
- McKay, D. C., Wood, C. J., Sheldon, S., Chow, J. M., and Gambetta, J. M.
  (2017). "Efficient Z-Gates for Quantum Computing." *Physical Review A* 96,
  022330. <https://doi.org/10.1103/PhysRevA.96.022330>.
- IBM Quantum documentation. "Error mitigation and suppression techniques."
  <https://quantum.cloud.ibm.com/docs/en/guides/error-mitigation-and-suppression-techniques>.
- Viola, L., and Lloyd, S. (1998). "Dynamical suppression of decoherence in
  two-state quantum systems." *Physical Review A* 58, 2733.
  <https://doi.org/10.1103/PhysRevA.58.2733>.
- Bylander, J., Gustavsson, S., Yan, F., Yoshihara, F., Harrabi, K., Fitch, G.,
  Cory, D. G., Nakamura, Y., Tsai, J. S., and Oliver, W. D. (2011).
  "Dynamical decoupling and noise spectroscopy with a superconducting flux
  qubit." *Nature Physics* 7, 565-570.
  <https://doi.org/10.1038/nphys1994>.
- Szańkowski, P., Ramon, G., Krzywda, J., Kwiatkowski, D., and Cywiński, L.
  (2017). "Environmental noise spectroscopy with qubits subjected to dynamical
  decoupling." *Journal of Physics: Condensed Matter* 29, 333001.
  <https://doi.org/10.1088/1361-648X/aa764d>.
- Cywiński, L., Lutchyn, R. M., Nave, C. P., and Das Sarma, S. (2008). "How to
  enhance dephasing time in superconducting qubits." *Physical Review B* 77,
  174509. <https://doi.org/10.1103/PhysRevB.77.174509>.
- Alexander, T., Kanazawa, N., Egger, D. J., Capelluto, L., Wood, C. J.,
  Javadi-Abhari, A., and McKay, D. (2020). "Qiskit Pulse: Programming Quantum
  Computers Through the Cloud with Pulses." *Quantum Science and Technology* 5,
  044006. <https://doi.org/10.1088/2058-9565/aba404>.
- Mundada, P. S., Gyenis, A., Huang, Z., Koch, J., and Houck, A. A. (2020).
  "Floquet-engineered enhancement of coherence times in a driven fluxonium
  qubit." arXiv:2007.13756. <https://arxiv.org/abs/2007.13756>.
- Tripathi, V., Chen, H., Khezri, M., Yip, K.-W., Levenson-Falk, E. M., and
  Lidar, D. A. (2021). "Suppression of crosstalk in superconducting qubits
  using dynamical decoupling." arXiv:2108.04530.
  <https://arxiv.org/abs/2108.04530>.
- Wilson, C. M., Duty, T., Persson, F., Sandberg, M., Johansson, G., and
  Delsing, P. (2007). "Coherence times of dressed states of a superconducting
  qubit under extreme driving." arXiv:cond-mat/0703629.
  <https://arxiv.org/abs/cond-mat/0703629>.
- Senatore, M., Campbell, D. L., Williams, J. A., and LaHaye, M. D. (2024).
  "Fast single-qubit gates for continuous dynamically decoupled systems."
  arXiv:2412.11821. <https://arxiv.org/abs/2412.11821>.

