# Site Design Blueprint

How this repository is structured so that **one set of Markdown files works two ways at once**:

1. **Browsable on GitHub** — every folder has a branded `README.md`, links resolve, badges render.
2. **Published as a polished site** — the same files build into a [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) site, auto-deployed to GitHub Pages at a custom domain.

This repo is a direct adaptation of the `ijk37/network-systems` blueprint (see that repo's `assets/site_design.md` for the original, fully-documented version) — same mechanism, different palette and content shape. Deltas from that original are called out below.

> [!NOTE]
> This file lives in `assets/` and is excluded from the built site (it is internal documentation, not a course page).

---

## 1. The core idea

A normal MkDocs project keeps docs in a `docs/` subfolder. That makes GitHub browsing ugly (everything nested under `docs/`). Instead, this repo builds **from the repository root** (`docs_dir: .`) so:

- The folders you see on GitHub (`01-notes/`, `02-exercises/`, …) **are** the site's content.
- Each folder's `README.md` is both the GitHub folder landing page **and** the site section index.

Two settings make links behave identically in both places:

| Setting | Value | Why |
| --- | --- | --- |
| `docs_dir` | `.` | Build from repo root, not `docs/` |
| `use_directory_urls` | `false` | URLs mirror file paths, so relative `.md` links map 1:1 to `.html` |

---

## 2. Repository structure

```
data-analytics/
├── .github/workflows/deploy.yml   # CI: build + deploy to GitHub Pages (REQUIRED at this path)
├── 01-notes/            # 8 chapter notes files + README.md (section index)
├── 02-exercises/        # NN-exercise.md per chapter + README.md dashboard
├── 03-quiz/             # Static quiz app (own index.html, owns this URL path)
├── 04-projects/         # 32 project folders (README.md per project) + README.md dashboard
├── 05-resources/        # Only README.md is published; lecture PDFs/docx/pptx stay local
│   ├── Class Lectures/.gitignore-equivalent (see 05-resources/.gitignore)
│   └── README.md
├── assets/
│   ├── banner.svg       # Hero banner embedded on every section README
│   ├── images/          # favicon.svg, data-logo.svg
│   ├── stylesheets/extra.css   # Brand theme (slate blue + emerald)
│   ├── javascripts/extra.js
│   └── site_design.md   # ← this file (excluded from build)
├── overrides/           # MkDocs theme custom_dir (theme tweaks)
├── tools/finalize.py    # Idempotent pre-build fixer (see §8)
├── index.md             # Site home page (REQUIRED at root, docs_dir=.)
├── README.md            # GitHub landing page (excluded from build; index.md is the site home)
├── 01-notes.md … 04-projects.md   # Root "shortcut" pages → redirect to live site (GitHub-only)
├── mkdocs.yml           # Site config (REQUIRED at root)
└── requirements.txt     # Build deps (REQUIRED by CI)
```

**Delta from network-systems:** the `04-projects/*` folders here also hold Python/R scripts and CSV datasets alongside each `README.md` (network-systems' project folders only ever held a README). `mkdocs.yml`'s `exclude_docs` therefore excludes `04-projects/**` wholesale and re-includes only the `README.md` files (see §3), so datasets/scripts never get copied into the built site.

**Load-bearing files that cannot be hidden or moved**: `.github/`, `mkdocs.yml`, `index.md`, `requirements.txt`, `assets/`, `overrides/`, `tools/`, and the content folders. Hiding any of them via `.gitignore` breaks the deploy.

---

## 3. MkDocs configuration essentials

```yaml
site_name: Data Analytics
site_url: https://ijk37.com/data-analytics/
repo_url: https://github.com/ijk37/data-analytics

docs_dir: .
site_dir: ../data-analytics-site
use_directory_urls: false

exclude_docs: |
  mkdocs.yml
  requirements.txt
  .gitignore
  .git/**
  tools/**
  assets/site_design.md
  05-resources/**
  !05-resources/README.md
  04-projects/**
  !04-projects/README.md
  !04-projects/*/README.md
  01-notes.md
  02-exercises.md
  03-quiz.md
  04-projects.md

theme:
  name: material
  custom_dir: overrides
  logo: assets/images/data-logo.svg
  favicon: assets/images/favicon.svg
  palette:
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: custom
      accent: custom
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: custom
      accent: custom

plugins:
  - same-dir
  - search
  - callouts

markdown_extensions:
  - admonition
  - attr_list
  - md_in_html
  - pymdownx.superfences
  - toc: { permalink: true }

extra_css:
  - assets/stylesheets/extra.css
```

Same plugin/extension roles as network-systems: `same-dir` required for `docs_dir: .`; `callouts` renders `> [!NOTE]`/`> [!TIP]`; `md_in_html` + `attr_list` are what let the home-page `.da-card` links and the `<div markdown>` nav blocks work.

---

## 4. Branding & theme

**Palette** (CSS variables in `assets/stylesheets/extra.css`, wired into Material's own variables):

```css
:root {
  --da-slate:        #34526b;
  --da-slate-dark:   #22384a;
  --da-slate-bright: #4a7196;
  --da-emerald:      #1e9e75;
  --da-emerald-deep: #167a5a;

  --md-primary-fg-color: #34526b;
  --md-accent-fg-color:  #167a5a;
}
[data-md-color-scheme="slate"] { /* dark-mode overrides bump accent to #34d399 */ }
```

Reusable brand elements:
- **Hero banner** — `assets/banner.svg` (slate gradient + emerald bar-chart/trend-line motif), embedded as a Markdown image `![Data Analytics](../assets/banner.svg)` at the top of every section README.
- **Home-page cards** — `attr_list` links with `.da-card .da-card-<name>` classes; each card gets a colored left border.
- **Badges** — [shields.io](https://shields.io) `for-the-badge` style, section badges in the new slate/emerald hexes. The **"View the Live Site"** badge keeps the original Bangladesh-flag palette (green `#006A4E` + red `#F42A41`) unchanged across all `ijk37.com` repos for brand recognition:

  ```markdown
  [![View the live site — ijk37.com](https://img.shields.io/badge/%F0%9F%87%A7%F0%9F%87%A9_View_the_Live_Site-IJK37.COM-F42A41?style=for-the-badge&labelColor=006A4E)](https://ijk37.com/data-analytics/)
  ```

---

## 5. Two-way navigation pattern

Every section `README.md` starts with the same block (identical mechanism to network-systems §6):

```markdown
<div align="center" markdown>

![Data Analytics](../assets/banner.svg)

[![View the live site — ijk37.com](…flag badge…)](https://ijk37.com/data-analytics/)

<img src="…section badge…" alt="Section">

[Home](../index.md) | [Notes](../01-notes/README.md) | [Exercises](../02-exercises/README.md) | [Quiz Hub](../03-quiz/) | [Projects](../04-projects/README.md)

</div>
```

Same rules apply: banner/nav must be **Markdown**, not raw HTML `<a>`/`<img>` (raw HTML isn't rewritten by MkDocs and would 404 on the site); links are relative and map 1:1 to built `.html` files because `use_directory_urls: false`.

---

## 6. Special folders

**`03-quiz/`** — static app owns its URL, same as network-systems. Nav points at `03-quiz/index.html`.

**`04-projects/`** — each of the 32 project folders has its own `README.md` (renamed from the working title `project_README.md` used during content authoring) so GitHub auto-renders it and the site can index it directly.

**`05-resources/`** — local-only lecture/exercise source material (PDF/docx/pptx/xlsx) stays out of git via `05-resources/.gitignore`; only `README.md` is published, same negation trick as network-systems.

---

## 7. `tools/finalize.py`

Same idempotent pre-build fixer pattern as network-systems, adapted paths: `01-notes/*.md`, `02-exercises/*.md`, `04-projects/README.md`, `04-projects/*/README.md`, `05-resources/README.md`. Run `python tools/finalize.py` before `python -m mkdocs build`.

---

## 8. Deployment

Identical workflow to network-systems: `.github/workflows/deploy.yml` builds on push to `main` and deploys via GitHub Pages (`Settings → Pages → Source = GitHub Actions`). The custom domain `ijk37.com` cascades from the user-site repo to every project site, so this repo is automatically served at `https://ijk37.com/data-analytics/` with no `CNAME` file needed here.
