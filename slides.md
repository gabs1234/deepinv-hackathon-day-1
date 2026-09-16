---
theme: default
title: Propagation-based phase retrieval with deepinv
mathRenderer: typst
colorSchema: light
aspectRatio: 4/3
hideInToc: true
---

# Optimization-base multi-distance phase retrieval

DEEPINV Hackathon summary

Aug 30 - Sept 2  2026

---
hideInToc: true
---

# Table of contents

<Toc columns="2" maxDepth="2" class="text-base" />

<style>
:deep(.slidev-toc-list-level-1 > li) {
  break-inside: avoid;
}
</style>

---
layout: section
level: 1
---

# Experiment and forward model

---
src: ./pages/direct-methods-setup.md
---

---
level: 2
---

# Notation & Conventions

Consistent notation mapping deepinv/machine learning standards to phase retrieval physics.

**Variables & Estimates:**
- $x$: Ground truth / unknown variable (e.g., the complex exit wave)
- $bold(y)$: Measured data / observations (e.g., intensity at the detector)
- $hat(x)$: Reconstructed / estimated variable 

**Operators:**
- $cal(F), cal(F)^(-1)$: Forward and inverse Fourier transforms
- $cal(B)_z$: Linear propagation of the complex field to distance $z$
- $cal(A)_z(x) = abs(cal(B)_z x)^2$: Nonlinear intensity measurement

---
level: 3
---

# From projected object to intensity

The object parametrization is nonlinear; free-space propagation remains the linear operator *B*.

**1. Projected material (phase decrement and absorption)**
$$
accent(delta, macron)(r) = integral_"ray" delta(r, s) dif s, quad accent(beta, macron)(r) = integral_"ray" beta(r, s) dif s
$$

**2. Exit wave** ($k = (2 pi) / lambda$, plane wave $p=1$)
$$
x(accent(delta, macron), accent(beta, macron))
= p e^(-k accent(beta, macron) - i k accent(delta, macron))
$$

**3. Field → intensity** (linear propagation, nonlinear readout)
$$
cal(B)_z x = cal(F)^(-1)[H_z cal(F)(x)]
$$
$$
cal(A)_z (x) = abs(cal(B)_z x)^2
$$

> **Note:** Choose the reconstruction variable deliberately. deepinv’s phase-retrieval form is linear in the complex field *x*. Optimizing $(accent(delta, macron), accent(beta, macron))$ adds the nonlinear transmission map before *B*.

---
level: 3
---

# Joint phase and absorption retrieval

Stack all propagation distances and estimate both projected material maps from one objective.

**Measurements & Stacked Operators:**
$$
bold(y) = mat(y_1; dots.v; y_J), quad
cal(B)_"stack" x = mat(cal(B)_(z_1)x; dots.v; cal(B)_(z_J)x), quad
cal(A)_"stack" (x) = abs(cal(B)_"stack" x)^2
$$
where $bold(y)$ contains the measured intensity images across all $J$ distances.

**Constrained reconstruction:**
$$
(hat(accent(delta, macron)), hat(accent(beta, macron))) = limits("argmin")_(accent(delta, macron), accent(beta, macron)) [
  1/2 norm(cal(A)_"stack" (x(accent(delta, macron), accent(beta, macron))) - bold(y))_2^2
  + R(accent(delta, macron), accent(beta, macron))
]
$$
where $R$ represents regularization terms and constraints on the material maps.

---
src: ./pages/phase-retrieval-results.md
---
