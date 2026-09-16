# Multi-distance phase retrieval — presentation

Slidev presentation for the DeepInv hackathon, with native Typst mathematics.

- [Presentation site](https://gabs1234.github.io/deepinv-hackathon-day-1/)
- [Scientific code and notebook](https://github.com/gabs1234/multi-distance-phase-retrieval)

This repository contains the slides, diagrams, rendered result figures, and
static Pages site. The scientific repository contains the reconstruction and
plotting implementations. **The real dataset and numerical reconstruction
caches are not uploaded.** The local `multi-distance-phase-retrieval` symlink is
ignored and is only useful when regenerating figures.

## Build or present

With Node.js 22+ and pnpm installed:

```sh
pnpm run setup
pnpm run dev
pnpm run build:pages
```

`setup` downloads and builds a pinned public Slidev/Typst fork into the ignored
`.slidev/` directory. It replaces the previous machine-specific dependency.
Building or displaying the deck does not require the Python repository or data.
Pages serves the checked-in `docs/` directory from this repository. See
[deployment instructions](deployment/DEPLOY-SLIDES.md).

Edit [slides.md](slides.md) and the imported files under `pages/`.

## Figures and scientific provenance

[Figure provenance](deployment/figure-provenance.json) records the scientific
code commit and hashes of every displayed asset and figure manifest. After
regenerating figures from committed scientific code, update it with
`pnpm run figures:record`. The original numerical-run provenance remains in
the figure manifests.

The appended notebook comparisons are in
[pages/phase-retrieval-results.md](./pages/phase-retrieval-results.md). Each of the
five stages has one equation slide followed by full result figures.
The comparisons use measured beads at 2048 × 1920 pixels, with iterative methods
run to explicit numerical convergence tolerances.
Each phase comparison also has a tight, native-resolution ROI view, followed by
a final recap of the complete NLTikh method.

Two introductory slides in [pages/direct-methods-setup.md](./pages/direct-methods-setup.md)
recall CTF/TIE/ICT direct inverses and show the experimental geometry in CeTZ.
All equations keep the DeepInv notation: `B_z` propagates the complex field,
`A_z(x) = |B_z x|^2` predicts the intensity, and `y_j` denotes measured data.
The phase constraint set is written `C` to distinguish it from the measurement operator.

To regenerate the analytical line cuts and setup schematic:

```bash
multi-distance-phase-retrieval/.venv/bin/python scripts/render-direct-methods.py
typst compile figures/multi-distance-setup.typ public/phase-retrieval/multi-distance-setup.svg
```

The transfer plots use illustrative distances, separate from the measured runs.
Pure-phase CTF has repeated zeros; pure-phase TIE has only the DC null, shown
in a low-frequency zoom. Faragó's homogeneous ICT uses `cos(chi) + gamma sin(chi)`
and has shifted oscillatory zeros. Its known material ratio ties phase to
attenuation, so its DC response is one. Multiple distances reduce common
transfer-function nulls but never determine an absolute pure-phase offset.
The setup shows the same sample translated to four source-to-sample positions
with a fixed detector, following Huhn et al., Table 1; it is not to scale.

To recompute the full-resolution runs on CUDA:

```bash
multi-distance-phase-retrieval/.venv/bin/python scripts/converge-phase-retrieval.py
```

The scientific implementations, convergence runner, and shared plotting code live in
[the linked Python repository](./multi-distance-phase-retrieval/README.md#reproduce-the-presentation-comparisons).
The commands here are thin wrappers. Fresh runs use the repository's
`.cache/phase-retrieval/converged/`; the original saved runs have been imported
unchanged into `.cache/phase-retrieval/presentation/`. Completed fresh runs are
reused and unfinished runs resume. Historical imports can be rendered and
verified, but are never resumed with changed source. The direct CTF inversions
need no iterative stopping test.

To regenerate all 21 plots, including holograms, phase maps, tight ROIs,
conditioning, frequency weights, and convergence curves:

```bash
multi-distance-phase-retrieval/.venv/bin/python scripts/render-converged-phase-retrieval.py
multi-distance-phase-retrieval/.venv/bin/python scripts/render-tie-introduction.py
```

The second command generates the seven TIE/CTF/ICT introduction figures.
Rendering needs no GPU and validates completeness and checkpoint provenance.
The wrappers select the fresh cache when present, otherwise the imported
presentation cache; `--cache` (or `--converged-cache` for the introduction)
overrides that choice. Output defaults to `public/phase-retrieval/`.
The deck builds from the generated assets without the notebook environment or data.

PGD and NLTikh stop when the projected-gradient ratio
`||phi - Pi_C(phi - grad E(phi))|| / ||grad E(0)|| <= 1e-3`.
AP requires its last 20 relative phase updates to be at most `1e-5`.
Both also require `abs(E_k - E_(k-100)) / E(0) <= 1e-4`, checked every 100 steps.
The constrained CTF initialization uses the notebook's accelerated ADMM, reaching
both relative primal and dual tolerances of `1e-3` after 350 iterations.

PGD uses the notebook's fixed step (0.2 for mean loss, 0.05 for the equivalent
four-plane summed loss). NLTikh uses its BB steps and nonmonotone line search;
the optimizer history restarts at each 100-step checkpoint. Checkpoints and
external stationarity checks are excluded from solver propagation-work curves;
the shared CTF initialization is excluded too. Numerical convergence does not
establish a global optimum or physical phase accuracy.

The AP rerun corrects a phase-branch discontinuity: the original principal
argument followed by clamping maps phases just below `-pi` to zero. The corrected
update is `Pi_C(phi + arg(exp(-i*phi) * averaged_wave))`, which tracks the current
phase continuously before applying the nonpositive constraint. Its detector
amplitude replacement and averaging are unchanged. The original oscillating run
is retained in the presentation audit archive; the plotted run is `ap_continuous.npz`.

The shared 192 × 192 ROI (37.6 μm square) is an approximate match to the red box in
Huhn et al., Figure 1: zero-based rows 583–774 and columns 870–1061. The paper
does not give pixel coordinates. Every crop comes from a full-field
reconstruction, and each comparison retains its full-field color scale.
`public/phase-retrieval/manifest.json` and `details-manifest.json` record source and
figure checksums, settings, histories, residuals, and ROI registration.
`convergence-summary.json` contains the stopping checks and iteration counts.
All displayed measurement residuals use the nonlinear intensity model, including
the CTF panels, and are normalized by measured contrast `||I - 1||`.

The former extraction/detail commands now delegate to the same converged
renderer. They no longer contain a second reconstruction implementation or
publish the old 25-step snapshots. The notebook imports the shared plotting
policy and can display these saved full-field results and their tight ROIs.

## GitHub Pages export

`pnpm run build:pages` rebuilds `docs/` for this presentation repository, with
hash routing and speaker notes omitted. Commit the updated export and push;
Pages publishes `main /docs`. The old ZIP export and copied site in the Python
checkout are local historical artifacts and are not part of the new repository.

Before pushing, `pnpm run check:publish` checks the Git index for dataset files,
caches, symlinks, and nested repositories. Do not use `git add -f` to include
ignored experimental files.
