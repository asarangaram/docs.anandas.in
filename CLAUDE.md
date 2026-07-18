# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A personal "Today I Learned" documentation site (https://docs.anandas.in) built with MkDocs + the Material theme. There is no application code — the deliverable is Markdown under `docs/content/`, plus a handful of Jupyter notebooks. Hosted/built by Read the Docs (`.readthedocs.yaml`).

## Commands

```bash
source .venv/bin/activate      # required first; deps live in the venv
mkdocs serve                   # live-reload preview at http://127.0.0.1:8000
mkdocs build                   # renders into site/ (gitignored)
```

Dependency changes go in `requirements.in`, then:

```bash
pip-compile --config=pyproject.toml requirements.in >& requirements.txt
pip install -r requirements.txt
```

`requirements.txt` **must be committed** — Read the Docs installs from it, not from `requirements.in`.

There are no tests or linters.

## Architecture / conventions

- **`mkdocs.yml` `nav` is an explicit allowlist.** Roughly half the ~120 Markdown files in `docs/content/` are unpublished drafts (`docs/content/drafts/`, `logseq/`, `whiteboards/`, `pages/`, etc.). Creating a new page has no effect on the site until it is added to `nav`. Conversely, when asked to "find a page", check `nav` to know whether it is actually live.
- **`nav` section names do not have to match directory names.** e.g. `content/linux-develop/vim.md` is listed under `linux-admin`, and the `general` section pulls pages from many directories. Directory layout is loose organization; `nav` is the real site structure.
- **The `exclude` plugin suppresses specific files** (currently several `content/concepts/ai_ml_basics/*.md`). If a page mysteriously fails to render, check that block in `mkdocs.yml` before debugging content.
- **Notebooks are executed at build time** (`mkdocs-jupyter` with `execute: True`). A notebook that errors or needs unavailable data will break `mkdocs build`.
- **Theme customization** lives in `overrides/` (`main.html`, `partials/copyright.html`) via `theme.custom_dir` — do not fork the Material theme itself.
- Markdown authoring leans on Material/pymdownx features already enabled: admonitions, content tabs, task lists, mermaid fences (```mermaid), MathJax via `pymdownx.arithmatex` (config in `docs/javascripts/mathjax.js`), and file inclusion via `markdown-include` with `base_path: docs`. `docs/content/features_demo/feature_demo.md` is the working reference for these.
- `docs/.obsidian/` exists because the docs tree doubles as an Obsidian vault. Leave it alone.
