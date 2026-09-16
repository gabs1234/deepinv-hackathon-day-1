---
level: 2
---

# Measured beads · numerical convergence

The notebook retrieves a **pure phase** object: absorption is fixed to zero.

$$
phi = -k integral_"ray" delta dif s, quad x = e^(i phi), quad
y_j approx cal(A)_(z_j)(x) = abs(cal(B)_(z_j) x)^2
$$

- Four measured holograms, **2048 × 1920** pixels at native sampling.
- **Convergence:** projected-gradient ratio $<= 10^(-3)$; alternating projections (AP) phase updates $<= 10^(-5)$.
- Constrained runs use **nonpositive phase**, with no support mask:

$$
cal(C) = {phi : phi <= 0}, quad Pi_cal(C) (v) = min(v, 0)
$$

**Reported relative intensity error:**

$$
r_I = norm(hat(bold(y)) - bold(y))_2 / norm(bold(y) - bold(1))_2,
quad hat(y)_j = cal(A)_(z_j)(x)
$$

$bold(y)$: measured intensities; $hat(bold(y))$: nonlinear Fresnel predictions.
Scores use the **full field** and each method's measured distances, even on region-of-interest (ROI) slides.
The denominator measures contrast around the flat field $1$; this is **not phase error**.

<!--
Source: multi-distance-phase-retrieval/phase_retrieval_comparison.py, rerun by
scripts/converge-phase-retrieval.py on the complete measured field.
PGD and NLTikh use ||phi - Pi_C(phi - grad E(phi))|| / ||grad E(0)|| <= 1e-3.
AP requires the last 20 relative phase updates to be <= 1e-5.
Every method also requires |E_k - E_(k-100)| / E(0) <= 1e-4.
Convergence is checked every 100 iterations; E(0) refers to zero phase, including
for warm-started runs. These are numerical tolerances, not a guarantee of a global
minimum or physical phase accuracy. Raw gradients need not vanish at a constrained
minimum, so the rerun uses the projected-gradient mapping.
The measurements are the experimental bead data used by Huhn et al. (2022),
previously studied by Hagemann, Töpperwien, and Salditt (2018).
The AP phase update is corrected to track phase continuously across -pi.
-->

---
layout: none
level: 3
title: Full measured hologram — first distance
---

<img src="/phase-retrieval/00-single-distance-data.png" alt="Complete measured hologram at the first propagation distance, 2048 by 1920 pixels. The orange box locates the tight ROI used in every method comparison." class="absolute inset-0 w-full h-full object-contain" />

<!--
First stored hologram, at equivalent plane-wave distance 155.89 mm.
The complete measured field is shown. The orange box locates the paper's
Figure 1 detail region, approximately matched to the registered data:
zero-based rows 583–774 and columns 870–1061 (192 × 192 pixels, 37.6 μm square).
-->

---
layout: none
level: 3
title: Measured holograms and line profiles
---

<img src="/phase-retrieval/00-measured-holograms.png" alt="Four measured bead holograms with a common line cut showing changes in the fringes across propagation distances." class="absolute inset-0 w-full h-full object-contain" />

<!--
Regenerated figure. Full registered holograms and their intensity profiles.
The equivalent plane-wave distances span 155.89–185.95 mm; intensities are the
stored measurements without additional per-image normalization.
-->

---
layout: section
level: 1
---

# Direct phase retrieval

Recover phase by Fourier filtering under an approximate intensity model.

---
level: 2
---

# Is small-defocus phase retrieval valid here?

Finite-distance inversion with the **transport of intensity equation (TIE)** requires $chi_j << 1$ at the retained spatial scales.

$$
chi_j (q) = pi lambda z_j q^2, quad
F_j = (Delta x)^2/(lambda z_j)
$$

| Spatial period $L = 1/q$ | $chi_j$ across the four distances |
| --- | ---: |
| 1 μm | 75.9–90.5 |
| 5 μm | 3.04–3.62 |
| 15 μm | 0.34–0.40 |
| 30 μm | 0.084–0.101 |

At the axis Nyquist frequency: $chi_j = pi/(4 F_j) approx 494$–$589$, far above one.

**TIE can approximate coarse contrast; the fine sphere edges are outside its small-defocus regime.**

<!--
F_j = (1.590111956, 1.569813695, 1.493700009, 1.333046878) times 10^-3,
read directly from holograms_beads_updated.npz. Values in the table use the common
196 nm grid, q in cycles per length, and the stored effective Fresnel numbers.
The 15 micrometre sphere diameter is not a band limit: its edges contain finer scales.
Small chi is a spectral check, not a sufficient validity certificate for arbitrary
strong phase gradients. The local object/propagation expansion must also hold.
The differential TIE remains valid within paraxial optics; it is the finite-distance
object-plane inversion being tested here. Low-pass filtering to periods above
about 30 micrometres could support a coarse approximation, subject to the other
conditions. Cropping an ROI does not change sampling or Fresnel number.
Validity analysis: https://arxiv.org/pdf/1503.06949
Dataset and geometry: https://arxiv.org/html/2205.01099v2
-->

---
level: 3
---

# TIE: recover phase from one hologram

Use the **first hologram**, with the same pure-phase model as the notebook.

$$
y_1 - 1 approx -lambda z_1/(2 pi) nabla^2 phi, quad
h_1^"TIE" (q) = 2 pi lambda z_1 q^2 = 2 chi_1 (q)
$$

$$
hat(phi)_"TIE" = cal(F)^(-1) lr([
  (h_1^"TIE" cal(F) lr((y_1 - 1)))
  / ((h_1^"TIE")^2 + alpha)
])
$$

Set $alpha = 10^(-2)$ to stabilize low frequencies; fix the unobservable mean phase to zero.

Check the result by propagating it with the **full Fresnel model**:

$$
hat(y)_1 = cal(A)_(z_1)(e^(i hat(phi)_"TIE"))
$$

<!--
This new example is a closed-form single-distance pure-phase TIE inversion.
It is not the single-material Paganin formula. No positivity/support constraint
or additional normalization is applied. It uses every pixel of the native field,
with FFT-periodic boundaries and scalar Tikhonov alpha=0.01, as in the following
regularized pure-phase CTF example. The unknown at DC is zero.
The figure shows stabilized TIE so that the well-known amplification of low spatial
frequency noise is not the only visible effect. An unregularized result is also
saved for reproducibility; its nonlinear residual is 0.63996, versus 0.49078 after
regularization. Numerical inversion is exact for the stated regularized linear
problem; no iterative convergence issue is involved.
Full Fresnel predictions from NumPy are independently checked against DeepInv.
The forward-prediction discrepancy diagnoses data consistency, not phase accuracy.
In particular, this residual need not rank TIE below an ill-conditioned CTF inverse.
Source: scripts/render-tie-introduction.py; .audit/tie-introduction/tie-single.npz.
-->

---
layout: none
level: 3
title: TIE reconstruction and Fresnel prediction — full field
---

<img src="/phase-retrieval/00-tie-full.png" alt="Regularized TIE phase from the first measured hologram, alongside the measured intensity and the full Fresnel prediction of that phase. The two intensities share one scale; the full-field nonlinear intensity residual is 0.491." class="absolute inset-0 w-full h-full object-contain" />

<!--
Full 2048 by 1920 reconstruction. The common paper ROI is outlined in orange.
The fine-scale TIE approximation is invalid for this geometry; residuals also
include noise, calibration and boundary mismatch and are not phase-error scores.
-->

---
layout: none
level: 3
title: TIE reconstruction and Fresnel prediction — tight ROI
---

<img src="/phase-retrieval/00-tie-roi.png" alt="The same paper-matched sphere ROI in the regularized TIE phase, measured hologram, and Fresnel prediction. TIE retains broad contrast while the predicted hologram lacks the measured fine fringes. Scales match the full-field slide." class="absolute inset-0 w-full h-full object-contain" />

<!--
Rows 583–774 and columns 870–1061, inclusive and zero-based; cropped only after
full-field reconstruction. All limits match the preceding full-field view.
-->

---
level: 2
---

# CTF: phase retrieval with regularization

The **contrast transfer function (CTF)** model uses weak phase increments while retaining the Fresnel oscillations. Here, absorption is zero.

$$
h_1 (q) = 2 sin(chi_1 (q)), quad
chi_1 (q) = pi lambda z_1 q^2
$$

$$
hat(phi)_"CTF" = cal(F)^(-1) lr([
  (h_1 cal(F) lr((y_1 - 1))) / (h_1^2 + alpha)
])
$$

Compare **direct inversion** ($alpha=0$) and **Tikhonov regularization** ($alpha=10^(-2)$).

Both use the same first hologram. Near zeros of $h_1$, regularization limits noise amplification.

<!--
The cached, converged notebook CTF runs are reused without recomputation.
Alpha=0 uses the existing Moore–Penrose-style spectral cutoff at 1e-6 of the
maximum squared response. It zeros unresolved modes including DC.
Weak phase increments mean |phi(r+lambda z q/2)-phi(r-lambda z q/2)| << 1
over relevant positions and spatial frequencies. Sharp sphere boundaries can
violate this condition, even though CTF retains the complete Fresnel oscillations.
Huhn et al. (2022), Eqs. (2), (4) and Section 4.1:
https://arxiv.org/html/2205.01099v2
-->

---
layout: none
level: 3
title: Single-distance CTF without and with regularization — full field
---

<img src="/phase-retrieval/01-ctf-single-full.png" alt="Full-field pure-phase CTF reconstructions of the first hologram without and with scalar Tikhonov regularization. Both use one shared phase scale. Nonlinear intensity residuals are 2.290 and 0.814." class="absolute inset-0 w-full h-full object-contain" />

---
layout: none
level: 3
title: Single-distance CTF without and with regularization — tight ROI
---

<img src="/phase-retrieval/01-ctf-single-roi.png" alt="The same tight sphere ROI for unregularized and regularized single-distance CTF, using the preceding full-field phase scale." class="absolute inset-0 w-full h-full object-contain" />

---
level: 2
---

# CTF vs ICT: compare attenuation models

**Intensity contrast transfer (ICT)** retains exponential attenuation; compare with single-material CTF.

For polystyrene at 8 keV, tabulated optical constants give $gamma = delta/beta approx 721$.

$$
h_gamma = 2 lr((sin(chi_1) + (cos(chi_1)) / gamma)), quad
u_alpha = cal(F)^(-1) lr([
  (h_gamma cal(F) lr((y_1 - 1))) / (h_gamma^2 + alpha)
])
$$

$$
hat(phi)_"CTF" = u_alpha, quad
hat(phi)_"ICT" = gamma/2 ln lr((1 + 2 u_alpha/gamma))
$$

Same first hologram, material ratio $gamma$, and regularization $alpha=10^(-2)$.

Both still require weak phase increments. The estimated intensity loss through one 15 μm sphere is only **about 0.6%**.

<!--
This is a matched single-material CTF–ICT comparison, separate from the pure-phase
notebook baseline. gamma is calculated from CXRO Henke f1/f2 for C8H8 at 8000 eV;
see multi-distance-phase-retrieval/src/multi_distance_phase_retrival_huhn/data/polystyrene-8kev.json. It is a tabulated prior, not a fitted or
measured material ratio. Density 1.05 g/cm^3 is used for the illustrative transmission.
Both inverses use h_gamma = 2 D/gamma, where D = cos chi + gamma sin chi.
Define s = gamma/2 (I0-1). The forward ICT relation is y-1 = F^-1[h_gamma F(s)].
The shared Tikhonov penalty is alpha ||s||^2; homogeneous CTF identifies s with
phase, whereas ICT maps the recovered contact intensity through its logarithm.
This regularizes contact-intensity CONTRAST about the incident level 1, not the
absolute intensity about zero. In D units alpha_D = gamma^2 alpha/4. Using the
same numeric alpha with h_gamma and D would make an unfair comparison.
No per-image normalization, phase shift, clipping before log, or nonpositive
constraint is applied. The reconstructed contact intensity is checked positive.
Both new residuals use the same absorbing-object nonlinear model:
|B_z exp(phi/gamma + i phi)|^2. The other notebook runs retain pure-phase physics.
ICT: Farago et al. (2024), Eqs. (7)–(9), https://doi.org/10.1364/OL.530330
Atomic factors: https://henke.lbl.gov/optical_constants/asf.html
-->

---
layout: none
level: 3
title: Matched CTF and ICT reconstruction — full field
---

<img src="/phase-retrieval/01-ctf-ict-full.png" alt="Homogeneous CTF and ICT at the same tabulated polystyrene ratio and matched regularization, using the first measured hologram. The phase maps share a scale; a third panel shows ICT minus CTF on a separate difference scale." class="absolute inset-0 w-full h-full object-contain" />

---
layout: none
level: 3
title: Matched CTF and ICT reconstruction — tight ROI
---

<img src="/phase-retrieval/01-ctf-ict-roi.png" alt="The same tight sphere ROI in homogeneous CTF, ICT, and their difference. Shared full-field phase scales make the small change from the ICT logarithm visible without implying phase ground truth." class="absolute inset-0 w-full h-full object-contain" />

---
layout: section
level: 1
---

# Multiple distances

Combine holograms whose contrast transfer functions have different zeros.

---
level: 2
---

# Transfer-function zeros motivate several distances

At one distance, pure-phase CTF cannot observe frequencies where $h_j (q)=0$.

<img src="/phase-retrieval/01-ctf-null-space.svg" alt="Exact CTF line cuts at the actual first and fourth measured distances. Nonzero-frequency zeros move with distance, while the DC zero is common." class="w-full h-55 object-contain" />

$$
sum_(j=1)^J abs(h_j (q))^2 = 0
quad arrow.l.r quad h_j (q) = 0 quad "for every" j
$$

**Extra distances fill individual gaps.** The mean phase (DC) stays invisible; small combined responses still need regularization.

ICT also has oscillatory zeros; its material prior supplies a nonzero DC response.

<!--
The plot uses the actual stored first and fourth Fresnel numbers, not illustrative
distances. q is cycles per length. u = q sqrt(lambda z_1). The zero positions are
sqrt(n z_1/z_j), n=0,1,... . The first/fourth distance ratio is about 1.193.
These are continuous-frequency transfer-function zeros; a finite FFT grid may
sample near a zero instead of landing on it exactly. The inverse is nevertheless
poorly conditioned near those frequencies. Radial averaging can conceal zeros,
which is why this introductory plot uses exact one-dimensional line cuts.
Regularization reduces instability but does not create measurements at missing
frequencies. For several distances, only common zeros remain in the linear model.
For homogeneous CTF and ICT, D_j = cos chi_j + gamma sin chi_j and D_j(0)=1.
They have the same zeros for a fixed material ratio because h_gamma=2D/gamma.
Their nonzero zeros also shift with distance; the pure-phase DC statement does
not apply after a finite, known phase-to-attenuation ratio is imposed.
-->

---
level: 2
---

# CTF: one distance versus four

Compare pure-phase Fourier inversions using **one or four holograms**, each **without or with scalar Tikhonov regularization**.

$$
h_j (xi) = 2 sin(norm(xi)^2 / (4 pi F_j)), quad
F_j = (Delta x)^2 / (lambda z_j)
$$

$$
hat(phi)_"CTF" = cal(F)^(-1) lr([
  (sum_(j=1)^J h_j cal(F)(y_j - 1))
  / (alpha + sum_(j=1)^J h_j^2)
])
$$

$J in {1, 4}$, $alpha in {0, 10^(-2)}$; $xi$ is angular frequency in rad/pixel.

The inverse sets unresolved Fourier modes to zero, including DC when $alpha = 0$.

<!--
Notebook stage 1: pure-phase CTF, Huhn et al. Eqs. (2) and (4).
The implementation zeroes Fourier estimates where the denominator is at most
1e-6 times its maximum. The orthonormal Fourier transform is used throughout.
-->

---
layout: none
level: 3
title: CTF phase reconstructions
---

<img src="/phase-retrieval/01-ctf-phase.png" alt="CTF reconstructed phase: one distance without regularization, one with scalar Tikhonov, four without regularization, and four with scalar Tikhonov. All panels share a phase scale in radians." class="absolute inset-0 w-full h-full object-contain" />

<!--
All four CTF reconstructions are closed-form inversions. The displayed residuals
now use the same nonlinear intensity diagnostic as later stages: 2.2902, 0.8141,
0.6043, and 0.5588.
-->

---
layout: none
level: 3
title: CTF phase reconstructions — tight ROI
---

<img src="/phase-retrieval/01-ctf-roi.png" alt="The same tight sphere ROI in all four CTF reconstructions: one or four distances, without or with scalar Tikhonov regularization. Native-resolution crops share the full comparison's phase scale." class="absolute inset-0 w-full h-full object-contain" />

<!--
Detail region matched to the red dashed box in Huhn et al. (2022), Figure 1.
The paper does not report pixel coordinates. Matching panel (c) to the native
phase map gives rows 583–774, columns 870–1061 (zero-based, inclusive).
The native phase arrays use the notebook's model and
cropped after reconstructing the full 2048 × 1920 field.
All panels use one shared phase scale, matching the preceding full-field view.
-->

---
layout: section
level: 1
---

# Fitting the nonlinear Fresnel model

Iteratively recover a pure-phase object from measured intensities.

Compare the model and phase constraint, then the distance count, solver, and regularization.

---
level: 2
---

# One hologram: CTF vs gradient descent

Recover phase $phi$ from one hologram using **projected gradient descent (PGD)** and the full Fresnel model.

**Compare:** linear CTF → unconstrained gradient descent → PGD with $phi <= 0$.

$$
hat(phi) in limits("argmin")_(phi in cal(C)) f_1 (phi), quad
f_1 (phi) = 1/2 norm(cal(A)_(z_1)(e^(i phi)) - y_1)_2^2
$$

$$
phi_(k+1) = Pi_cal(C) (phi_k - eta nabla f_1 (phi_k)), quad phi_0 = 0
$$

Unconstrained: $cal(C) = RR^(H times W)$. Nonpositive phase: $cal(C) = {phi : phi <= 0}$.

Same measured plane; no regularization. Fixed step $eta = 0.2$, run to convergence.

<!--
Notebook stage 2. CTF uses the unregularized one-plane result from stage 1.
The nonlinear runs share zero initialization and a fixed step of 0.2.
Free PGD converges after 1,100 steps; nonpositive PGD after 1,600 steps.
Only the feasible set changes between the two nonlinear runs.
Unconstrained still means pure-phase transmission, with unit object amplitude.
All iterative nonlinear phase images use one magma scale, -5 to +4 rad, across
comparisons and full-field/ROI views. The CTF panel has its own labeled colorbar.
-->

---
layout: none
level: 3
title: Single-distance phase reconstructions
---

<img src="/phase-retrieval/02-single-distance-phase.png" alt="Single-distance phase reconstructions from unregularized CTF, unconstrained nonlinear PGD, and nonlinear PGD with nonpositive phase. CTF has a separate labeled colorbar; both nonlinear panels use the common -5 to +4 rad scale used throughout the nonlinear comparisons." class="absolute inset-0 w-full h-full object-contain" />

<!--
Relative nonlinear intensity residuals in panel order: CTF 2.290,
unconstrained PGD 0.03787, nonpositive PGD 0.03885. No phase ground truth.
-->

---
layout: none
level: 3
title: Single-distance phase reconstructions — tight ROI
---

<img src="/phase-retrieval/02-single-distance-roi.png" alt="The same tight sphere ROI for linear CTF, free nonlinear PGD, and nonpositive nonlinear PGD using one measured distance. CTF has its own scale; both nonlinear crops retain the common -5 to +4 rad scale of the full-field and subsequent comparisons." class="absolute inset-0 w-full h-full object-contain" />

<!--
Same Figure 1 detail region and full-field reconstructions as the other ROI slides.
-->

---
layout: none
level: 3
title: Single-distance PGD convergence
---

<img src="/phase-retrieval/02-single-distance-convergence.png" alt="Measurement residual and projected-gradient stopping measure for free and nonpositive single-distance PGD, converged after 1,100 and 1,600 iterations." class="absolute inset-0 w-full h-full object-contain" />

---
level: 2
---

# PGD: one distance versus four

**Change only the data:** fit one or four holograms with the same nonlinear model and projected-gradient solver.

$$
hat(phi) in limits("argmin")_(phi <= 0) f_J (phi), quad
f_J (phi) = 1/(2J) sum_(j=1)^J norm(cal(A)_(z_j)(e^(i phi)) - y_j)_2^2
$$

$$
phi_(k+1) = Pi_cal(C) (phi_k - eta nabla f_J (phi_k)), quad J in {1, 4}
$$

Both use nonpositive phase, zero initialization, and fixed step $eta = 0.2$.

Averaging over distances keeps the data-gradient scaling comparable.

Both runs reach the stopping criteria; residuals use their own measured planes.

<!--
Notebook stage 3. The single-distance result is reused from stage 2.
Its magma color mapping is also identical: -5 to +4 rad, without any phase shift
or independent rescaling of the ROI. This scale is shared by all nonlinear runs.
The two residual curves use different measurement sets: they are not phase
accuracy scores or a ranking on a common held-out measurement set.
-->

---
layout: none
level: 3
title: One versus four distances — phase
---

<img src="/phase-retrieval/03-distance-comparison-phase.png" alt="Nonpositive phase reconstructed by nonlinear PGD using one distance and four distances, with a shared phase color scale." class="absolute inset-0 w-full h-full object-contain" />

<!--
Relative intensity residual: single distance 0.03885; four distances 0.13012.
Convergence after 1,600 and 800 iterations. Residuals use their respective data sets.
-->

---
layout: none
level: 3
title: One versus four distances — tight ROI
---

<img src="/phase-retrieval/03-distance-comparison-roi.png" alt="The same tight sphere ROI from converged nonpositive PGD using one and four distances, with a shared phase scale." class="absolute inset-0 w-full h-full object-contain" />

<!--
Same Figure 1 detail region, cropped after full-field reconstruction.
-->

---
layout: none
level: 3
title: One versus four distances — convergence
---

<img src="/phase-retrieval/03-distance-comparison-convergence.png" alt="Measurement residual and projected-gradient stopping measure for one-distance and four-distance PGD, converged after 1,600 and 800 iterations; each residual uses its own measurements." class="absolute inset-0 w-full h-full object-contain" />

---
level: 2
---

# Four distances: projections vs gradients

Compare **alternating projections (AP)** with **projected gradient descent (PGD)**.

Same four holograms, nonpositive phase, and zero start; both run to convergence.

$$
u_(j,k) = cal(B)_(z_j) e^(i phi_k), quad
tilde(u)_(j,k) = sqrt(max(y_j, 0))
  u_(j,k) / max(abs(u_(j,k)), epsilon)
$$

$$
accent(v, macron)_k = 1/J sum_(j=1)^J cal(B)_(z_j)^* tilde(u)_(j,k), quad
phi_(k+1) = Pi_cal(C) lr([phi_k + arg(e^(-i phi_k) accent(v, macron)_k)])
$$

PGD: $phi_(k+1) = Pi_cal(C) (phi_k - eta nabla f_J (phi_k))$.

AP imposes measured detector amplitudes and averages back-propagated fields; PGD minimizes intensity mismatch.

<!--
Notebook stage 4. cal(B)_(z_j)^* is adjoint Fresnel propagation.
AP is an amplitude-projection algorithm, not gradient descent on the intensity
least-squares objective. Both methods are evaluated with the same intensity
residual, versus iterations and equivalent forward/adjoint propagation work.
The original principal-argument-then-clamp update jumped to zero when phases
crossed -pi and remained oscillatory after 4,000 iterations. The displayed rerun
uses increments arg(exp(-i phi_k) * averaged_wave), preserving the phase branch
before nonpositive projection. This correction is local to the presentation runner;
the linked notebook package is unchanged. The amplitude denominator uses epsilon=1e-8.
-->

---
layout: none
level: 3
title: AP versus PGD — phase
---

<img src="/phase-retrieval/04-optimizer-phase.png" alt="Converged four-distance phase reconstructions from DeepInv PGD and averaged AP with continuous phase tracking, under identical nonpositive constraints." class="absolute inset-0 w-full h-full object-contain" />

<!--
PGD converges after 800 iterations with residual 0.13012.
Corrected AP converges after 10,200 iterations with residual 0.13434.
Its maximum relative update over the last 20 steps is 9.96e-6 (tolerance 1e-5).
-->

---
layout: none
level: 3
title: AP versus PGD — tight ROI
---

<img src="/phase-retrieval/04-optimizer-roi.png" alt="The same tight sphere ROI reconstructed by converged four-distance PGD and AP with continuous phase tracking. Both use nonpositive phase and a shared phase scale." class="absolute inset-0 w-full h-full object-contain" />

<!--
Same Figure 1 detail region, cropped after full-field reconstruction.
-->

---
layout: none
level: 3
title: AP versus PGD — iterations
---

<img src="/phase-retrieval/04-optimizer-iterations.png" alt="Intensity residual and normalized stopping measure versus iteration for four-distance PGD and AP with continuous phase tracking. They converge after 800 and 10,200 iterations." class="absolute inset-0 w-full h-full object-contain" />

---
layout: none
level: 3
title: AP versus PGD — propagation work
---

<img src="/phase-retrieval/04-optimizer-work.png" alt="Intensity residual and normalized stopping measure versus forward and adjoint propagations for converged PGD and AP with continuous phase tracking." class="absolute inset-0 w-full h-full object-contain" />

---
level: 2
---

# From PGD to nonlinear Tikhonov

**Nonlinear Tikhonov (NLTikh)**, following Huhn et al.: four holograms and nonpositive phase.

**Add in sequence:** CTF initialization → frequency regularization → adaptive steps.

$$
hat(phi) in limits("argmin")_(phi <= 0) lr([
  1/2 sum_(j=1)^4 norm(cal(A)_(z_j)(e^(i phi)) - y_j)_2^2
  + 1/2 norm(sqrt(alpha) cal(F) phi)_2^2
])
$$

$$
phi_0 approx limits("argmin")_(phi <= 0) lr([
  1/2 sum_(j=1)^4 norm(cal(A)_(z_j)^"lin" (phi) - y_j)_2^2
  + 1/2 norm(sqrt(alpha) cal(F) phi)_2^2
])
$$

$cal(A)_(z_j)^"lin" (phi) = 1 + cal(F)^(-1)[h_j cal(F) phi]$ linearizes $cal(A)_(z_j)(e^(i phi))$ at $phi=0$.

Frequency weights $alpha(xi)$; projected steps with **Barzilai–Borwein (BB)** step-size proposals and nonmonotone backtracking.

<!--
Notebook stage 5, following Huhn et al. (2022), Eqs. (6), (7), and (11).
The shared constrained CTF warm start converges after 350 accelerated ADMM
iterations. The first column is stage-3 PGD from zero with mean loss and eta=0.2.
The next column changes only the initialization, using summed loss and eta/J=0.05.
The third adds the frequency Tikhonov term; the fourth changes the adaptive policy.
All three warm-started runs start from the SAME regularized constrained CTF result.
The smooth filter levels are alpha_low=1e-3, alpha_high=1e-1, alpha_beyond_NA=8.
The phase update is Pi_C(phi_k - tau_k * grad E_alpha(phi_k)).
The nonlinear runs use the same projected-gradient stopping criterion, including
the 100-step objective-change check. NLTikh's BB and nonmonotone-search history
restart at each 100-step checkpoint. Work counts exclude the shared CTF solve
and external diagnostic gradient checks.
Reference: Huhn, Lohse, Lucht & Salditt, Optics Express 30, 32871–32886 (2022),
doi:10.1364/OE.462368. This is the notebook's implementation and measured run.
-->

---
layout: none
level: 3
title: Nonlinear Tikhonov ablation — phase
---

<img src="/phase-retrieval/05-nltikh-phase.png" alt="Sequential nonlinear Tikhonov ablation: PGD baseline, constrained CTF initialization, frequency Tikhonov regularization, and adaptive BB with nonmonotone search. The four phase maps share one scale." class="absolute inset-0 w-full h-full object-contain" />

<!--
Final relative intensity residuals, in panel order: 0.13012, 0.12828, 0.12855, 0.12845.
The zero-start baseline uses 800 steps; the three warm-started runs use 300 each.
All reach the numerical stopping criteria and share the converged CTF start.
-->

---
layout: none
level: 3
title: Nonlinear Tikhonov ablation — tight ROI
---

<img src="/phase-retrieval/05-nltikh-roi.png" alt="The same tight sphere ROI across the nonlinear Tikhonov ablation: PGD baseline, constrained CTF start, frequency regularization, and BB with nonmonotone search. All four crops share one phase scale." class="absolute inset-0 w-full h-full object-contain" />

<!--
Same Figure 1 detail region, cropped after full-field reconstruction.
The three warm-started methods share the same constrained CTF initialization.
-->

---
layout: none
level: 3
title: Nonlinear Tikhonov — frequency weights
---

<img src="/phase-retrieval/05-nltikh-filter.png" alt="Radial Huhn Tikhonov frequency weights, with the first CTF maximum marked. The numerical aperture cutoff lies beyond the sampled radial range and is reported below the plot." class="absolute inset-0 w-full h-full object-contain" />

---
layout: none
level: 3
title: Nonlinear Tikhonov ablation — convergence
---

<img src="/phase-retrieval/05-nltikh-convergence.png" alt="Intensity residual and projected-gradient convergence versus propagation work for the four nonlinear Tikhonov ablation runs. All curves terminate after meeting the numerical stopping criteria." class="absolute inset-0 w-full h-full object-contain" />

<!--
Regenerated from the complete solver histories. Direct labels identify each curve.
The right panel shows the projected-gradient residual divided by its tolerance.
-->

---
layout: none
level: 3
title: Full-field NLTikh reconstruction and close-up
---

<img src="/phase-retrieval/05-full-field-paper-roi.png" alt="Full nonlinear Tikhonov phase reconstruction at 2048 by 1920 pixels, alongside the same tight sphere ROI used throughout the comparisons. The orange rectangle locates the detail, and both views share one phase scale." class="absolute inset-0 w-full h-full object-contain" />

<!--
Full Huhn-style NLTikh result rerun to the stated numerical tolerances.
The displayed detail matches the paper's Figure 1 region and every ROI comparison.
Approximate registered bounds: rows 583–774, columns 870–1061 (zero-based).
This is a crop of the reconstructed phase, not an independent ROI reconstruction.
-->

---
level: 2
---

# Nonlinear Tikhonov: complete method

**Huhn-style nonlinear Tikhonov**, using all four measured holograms at native resolution.

$$
hat(phi) in limits("argmin")_(phi <= 0) lr([
  1/2 sum_(j=1)^4 norm(cal(A)_(z_j)(e^(i phi)) - y_j)_2^2
  + 1/2 norm(sqrt(alpha) cal(F) phi)_2^2
])
$$

- **Model:** nonlinear Fresnel propagation of a pure-phase object, $x = e^(i phi)$.
- **Initialization:** constrained CTF via the **alternating direction method of multipliers (ADMM)**, converged after 350 accelerated iterations.
- **Prior:** nonpositive phase and frequency-dependent Tikhonov regularization.
- **Optimization:** projected gradient, alternating Barzilai–Borwein steps, and nonmonotone backtracking.

Shown run: **300 nonlinear iterations**, stopping criteria reached on the full field.

<!--
The regularization filter uses low/high/beyond-NA levels 1e-3, 1e-1, and 8.
No support mask is supplied, and absorption is fixed to zero.
The relative projected-gradient residual is 4.20e-4 (tolerance 1e-3).
The 100-step objective change divided by E(0) is 6.44e-5 (tolerance 1e-4).
Final relative intensity residual is 0.12845. Spatial resolution is 2048 × 1920.
The ROI changes only the displayed region; every solver ran on the full field.
-->

---
level: 2
class: text-sm
---

# CTF vs nonlinear Tikhonov: results

Same **four holograms**, full field and sphere ROI · one shared phase color scale.

<img src="/phase-retrieval/06-ctf-vs-nltikh-summary.png" alt="Regularized four-distance CTF and the full Huhn-style nonlinear Tikhonov reconstruction, each shown as a full field and the same tight sphere ROI. All four views use the same phase scale, from minus 5 to plus 4 radians." class="w-full h-76 object-contain" />

| | Regularized multi-distance CTF | Huhn-style NLTikh with DeepInv |
| --- | --- | --- |
| Model / prior | Linear CTF · scalar $alpha = 0.01$ | Full Fresnel · frequency Tikhonov + $phi <= 0$ |
| Solve | Direct Fourier inverse | Constrained CTF start + 300 nonlinear steps |
| Relative intensity error $r_I$ ↓ | **0.559** | **0.128 — 4.35× lower** |

**Takeaway:** the full nonlinear method fits these measured holograms substantially better.

<div class="text-xs leading-snug mt-2">
CTF has zero mean; NLTikh enforces nonpositive phase. No phase offsets were aligned.<br>
This compares complete methods with different priors. There is no measured phase ground truth.
</div>

<!--
This is the best of the four direct CTF baselines shown, not a search over
regularization strengths: ctf_multi_tikh, four distances, scalar alpha=0.01.
Its nonlinear full-data intensity residual is 0.5587598085403442.
The comparison is the notebook's full Huhn-style NLTikh implementation in
DeepInv, not the authors' reconstructed image or their original code.
NLTikh uses frequency-dependent Tikhonov weights (1e-3, 1e-1, 8), phi<=0,
a constrained CTF start (350 ADMM iterations), and BB steps with nonmonotone
backtracking. Its 300 nonlinear steps reach the stated convergence criteria.
Its full-data residual is 0.12844941020011902; the ratio is about 4.35.
Both residuals use all four measured planes and the same nonlinear pure-phase
Fresnel model, normalized by ||I-1||. These are intensity consistency measures.
NLTikh is the complete paper-inspired method, not the lowest residual in every
ablation: unregularized warm-started PGD gives 0.12828 on this dataset.
The images use the original phase values and a shared -5 to +4 rad scale,
including positive CTF values. Gauge/prior differences affect absolute colors;
do not interpret brightness or the residual reduction as phase error against truth.
ROI: zero-based top=583, left=870, size=192 (37.632 micrometres square),
approximately matched to Huhn et al., Figure 1. Cropping follows reconstruction.
Source: Huhn et al. (2022), https://doi.org/10.1364/OE.462368.
Regenerate with the scientific repository's scripts/render-method-summary.py.
-->
