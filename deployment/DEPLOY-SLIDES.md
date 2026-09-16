# Publish the presentation

The presentation repository is `gabs1234/deepinv-hackathon-day-1`.
The intended site is https://gabs1234.github.io/deepinv-hackathon-day-1/.
The Python implementation remains in `gabs1234/multi-distance-phase-retrieval`.

## Rebuild and publish

```sh
pnpm run build:pages
pnpm run check:publish
git add docs
git commit -m "Update published slides"
git push
```

`build:pages` writes the static site to this presentation repository's `docs/`
directory, with the `/deepinv-hackathon-day-1/` base path, hash routes, and no
speaker notes. GitHub Pages publishes **main /docs**. For a new repository,
select that publishing source in **Settings → Pages** once.

A reader or hosting server needs only the exported HTML, JavaScript, fonts,
and displayed result images. It needs no Python, experimental dataset, or
Typst installation. The real dataset, reconstructed numerical arrays, local
caches, and the symlink to the Python repository are excluded from Git.

## First checkout

Install Node.js 22+ and pnpm, then run:

```sh
pnpm run setup
pnpm run dev
```

The setup command downloads and builds the exact public Slidev/Typst fork
revision in `deployment/slidev-source.json`, then installs the deck's locked
dependencies. Its `.slidev/` checkout is ignored. There is no dependency on
another checkout elsewhere on the author's machine.

The checked-in `docs/` directory can also be served directly without installing
build dependencies. For another repository name, rebuild with an explicit base:

```sh
SLIDEV_BASE=/another-repository/ pnpm run build:pages
```

See [GitHub Pages publishing sources](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).
