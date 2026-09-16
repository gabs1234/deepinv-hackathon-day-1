---
level: 2
class: text-sm
---

# Experimental setup

<img src="/phase-retrieval/multi-distance-setup.svg" alt="CeTZ schematic of the Huhn bead experiment, not to scale. A waveguide point source illuminates the same sample at four successive source-to-sample positions: 156, 158, 166, and 187 millimetres. The fixed detector has 6.5 micrometre physical pixels and remains 5.178 metres from the source. Source-to-sample and sample-to-detector distances are labelled for one acquisition." class="w-full h-56 object-contain" />

**Physical detector:** 2048 × 2048 pixels · **6.5 μm pitch** · 13.31 × 13.31 mm.

$M_j = (R_(1,j) + R_(2,j)) / R_(1,j) = (5.178 "m") / R_(1,j)$, with object-plane pitch $Delta x_j = (6.5 "μm") / M_j$.

| Source–sample distance (mm) | 156 | 158 | 166 | 187 |
| --- | ---: | ---: | ---: | ---: |
| Derived magnification (approx.) | 33.2× | 32.8× | 31.2× | 27.7× |
| Object-plane pitch before registration (nm) | 196 | 198 | 208 | 235 |

**After registration:** all four holograms share a **196 nm effective object-plane pitch**.

At **8 keV**, the stored effective propagation distances are $z_j = (155.89, 157.90, 165.95, 185.95) "mm"$.

<div class="text-xs mt-3">

[Huhn et al. (2022), Table 1](https://arxiv.org/html/2205.01099v2) · Derived values use the rounded physical distances; schematic not to scale.

</div>

<!--
The four drawn object planes are successive positions of the same specimen,
not four objects in the beam simultaneously. The acquisition changes the
source-to-sample distance R_(1,j); R_(2,j) is the remaining physical distance
to the fixed detector. The detector is 5.178 m from the waveguide source.
Reported source-to-sample positions: 156, 158, 166, 187 mm.
The positions are spread out in the drawing for legibility, not plotted to scale.
Physical detector pitch is 6.5 micrometres at every position.
Using M_j = 5178 / R_(1,j), with both distances in millimetres, gives
33.1923, 32.7722, 31.1928, and 27.6898. These are approximate values derived
from the rounded reported positions; the paper tabulates a reference M=33.1.
The corresponding object-plane pitches before registration are
195.83, 198.34, 208.38, and 234.74 nm. They are not four physical detector pitches.

Cone-beam Fresnel scaling uses M_j=(R_(1,j)+R_(2,j))/R_(1,j) and maps each
acquisition to a plane-wave distance R_2/M in its demagnified object-plane
coordinates. Registering all images onto
one common sampling grid also transforms the dimensionless Fresnel numbers.
The notebook propagators use the supplied Fresnel numbers on the registered
196 nm grid; do not recompute them from rounded physical table positions.
The stored arrays are 2048 by 1920 after registration/cropping; the physical
detector images reported in the paper are 2048 by 2048.
-->


---
level: 3
---

# Small angles · fine spatial sampling

**15 μm polystyrene spheres** · 2048 × 1920 measured pixels · field of view 401 × 376 μm.

| Quantity | Value |
| --- | ---: |
| Wavelength at 8 keV | 0.155 nm |
| Physical detector pixel pitch | 6.5 μm |
| Effective pitch on the common object grid | 196 nm |
| Smallest sampled period along an axis | 392 nm |

The sampled period is a **sampling limit**, not a measured spatial resolution.

$$
q_"Nyq" = 1/(2 Delta x), quad
lambda q_"max" = lambda/(sqrt(2) Delta x) approx 5.6 times 10^(-4) << 1
$$

Geometric rays across the field are also paraxial: at most about **1.8 mrad**.

**Fresnel propagation is appropriate. Small-defocus TIE needs a separate check.**

<!--
Field sizes, Nyquist scales, and spatial frequencies refer to the common
registered object-plane grid; the physical detector pitch refers to the camera.
The Nyquist period 2 Delta x = 392 nm is along either pixel axis. It does not
establish the optical resolution or claim that a 392 nm object feature is resolved.
The radial corner frequency is sqrt(2)/(2 Delta x), giving lambda q_max = 5.59e-4.
The half-diagonal of the 2048 by 1920 field is 275.1 micrometres. Dividing by the
shortest source-to-sample distance, 156 mm, gives a geometric ray angle of 1.76 mrad.
These small-angle estimates support the paraxial model at the sampled scales;
they do not imply small chi = pi lambda z q^2. Projection, coherence, calibration,
and finite-field assumptions remain those of the notebook and Huhn experiment.
Source geometry and sphere size: Huhn et al. (2022), Table 1 and Section 4.1:
https://arxiv.org/html/2205.01099v2
Calculated numbers: public/phase-retrieval/tie-introduction-manifest.json.
-->
