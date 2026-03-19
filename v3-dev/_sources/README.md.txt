# OpenVCAD Documentation Build and Deploy Guide

This directory (`docs/source/`) is the canonical Sphinx source for OpenVCAD docs.

It powers the public multi-version docs site:

- v2 docs from `main`
- v3-dev docs from `attribute-modeling`

## Repositories and Roles

- `openvcad-internal` (this repo)
  - Authoring source for docs (`docs/source/`)
  - Build/deploy automation (`build_scripts/deploy_docs.sh`)
  - C++ API extraction config (`docs/Doxyfile`)
- `OpenVCAD-Docs` (deployment target)
  - Static built HTML for GitHub Pages
  - Receives versioned outputs (`v2/`, `v3-dev/`) and landing page (`index.html`)
- `OpenVCAD-Public`
  - Public hub/examples; some docs content may link to it
  - Not the docs deployment target

## Documentation Stack

- **Sphinx** for site generation
- **MyST-Parser** for Markdown pages (`.md`)
- **Doxygen** for C++ API XML
- **Breathe** to render Doxygen XML in Sphinx

Python API reference pages are generated through `autodoc` imports (e.g., `pyvcad`, `pyvcad_compilers`, `pyvcad_rendering`).

## Source Layout

- `docs/source/index.rst`: site landing + toctrees
- `docs/source/python-api/`: Python API reference pages
- `docs/source/cpp-api/index.rst`: C++ API entry page
- `docs/source/_templates/versions.html`: empty override (sidebar version dropdown disabled)
- `docs/source/_static/`: static assets (including tutorial images)
- `docs/Doxyfile`: Doxygen config used before Sphinx build

## Local Build (single branch)

From repo root:

1. Create/activate a Python environment.
2. Install docs tooling:
   - `sphinx`
   - `sphinx_rtd_theme`
   - `myst-parser`
   - `breathe`
3. Install local packages (editable) so autodoc can import:
   - `pip install -e . -e rendering`
   - (and `-e medical` if needed)
4. Generate C++ XML:
   - `doxygen docs/Doxyfile`
5. Build HTML:
   - `python -m sphinx.cmd.build -b html docs/source docs/build/html`

Output appears in `docs/build/html`.

## Multi-Version Deploy Script

Primary script:

- `build_scripts/deploy_docs.sh`

This script is the standard way to build and publish both v2 and v3-dev docs.

### What it does

1. Defines version mapping:
   - `main -> v2`
   - `attribute-modeling -> v3-dev`
2. Creates per-branch `git worktree`s.
3. Creates isolated per-version virtual environments.
4. Installs docs tooling and local editable packages in one pip invocation:
   - `-e <worktree root>`
   - `-e <worktree>/rendering` (if present)
   - `-e <worktree>/medical` (if present)
5. Verifies core Python imports (`pyvcad`, `pyvcad_compilers`).
6. Runs `doxygen docs/Doxyfile` for each branch, requiring XML output.
7. Runs Sphinx build for each branch.
8. Copies built outputs into deploy layout:
   - `deploy/v2/`
   - `deploy/v3-dev/`
9. Generates top-level landing page (`deploy/index.html`) with version cards.
10. Publishes to local clone of `OpenVCAD-Docs`, commits, and pushes `main`.
11. Generates a docs-specific `.gitattributes` that disables LFS for image files
    (the source repo uses LFS for `*.png` etc., but GitHub Pages needs raw blobs).

### Usage

From repo root:

- Deploy and push:
  - `./build_scripts/deploy_docs.sh`
- Build only (no push):
  - `./build_scripts/deploy_docs.sh --dry-run`

## Deployment Output Structure (`OpenVCAD-Docs`)

After deploy, the `OpenVCAD-Docs` repo contains:

- `index.html` (version hub)
- `v2/` (docs built from `main`)
- `v3-dev/` (docs built from `attribute-modeling`)
- `.nojekyll`
- `.gitattributes` (LFS tracking rules)

GitHub Pages serves this content at:

- `https://matterassembly.org/OpenVCAD-Docs/`

## Notes and Troubleshooting

- If C++ API appears empty, verify Doxygen XML generation:
  - `docs/doxygen_xml/index.xml` must exist for each branch build.
- If Python API pages are sparse/empty, verify editable installs and imports.
- If images fail in tutorials, prefer local assets under `docs/source/_static/` rather than remote links.
- If branch switching fails due to local untracked files, clean or isolate before running multi-worktree/deploy operations.
