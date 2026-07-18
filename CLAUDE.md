# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A personal "Today I Learned" documentation site (https://docs.anandas.in) built with MkDocs + the Material theme. There is no application code — the deliverable is Markdown under `docs/content/`, plus three Jupyter notebooks. Hosted/built by Read the Docs (`.readthedocs.yaml`).

## Commands

```bash
source .venv/bin/activate      # required first; deps live in the venv
mkdocs serve                   # live-reload preview at http://127.0.0.1:8000
mkdocs build --strict          # renders into site/ (gitignored)
```

**Always use `--strict`.** It promotes "page not in nav", missing-file, and broken-link warnings into errors. The repo was cleaned up specifically to build clean under `--strict`; keep it that way, because those warnings are exactly how the nav and the files on disk drift apart.

Dependencies are installed straight from `requirements.in` (`pip install -r requirements.in`) — there is no compiled lockfile, and Read the Docs installs the same file. Pins are open by design; if an upstream release breaks a build, pin that one package in `requirements.in`.

There are no tests or linters. The one executable check is `validate_passwords.ipynb`, which asserts `wasSuccessful()` — a regression there fails the build.

## Architecture / conventions

- **`mkdocs.yml` `nav` is an explicit allowlist**, and nav sections now mirror directory names. When adding a page, add it to `nav` in the section matching its directory, or `--strict` will fail. Note that URLs derive from *file paths*, not nav position — moving a nav entry between sections is free, moving a file on disk changes its URL.
- **Unfinished pages are published, not hidden.** They carry `tags: [todo]` frontmatter and a `!!! warning "Work in progress"` admonition, and are indexed at `docs/tags.md` (which uses the `<!-- material/tags -->` marker; the `tags_file:` config option is deprecated in current Material). Prefer this over leaving a page out of `nav`.
- **The `exclude` plugin serves two distinct purposes** — read the comments in the block before touching it:
  1. `content/concepts/ai_ml_basics/{approaches,cognitive_functions,tasks,ann}.md` are fragments inlined into that directory's `index.md` via `markdown-include` (`{!path!}`, `base_path: docs`). Excluding them prevents duplicate standalone pages. **Removing them from the glob breaks the page.**
  2. `course_activeloop/` and `python/pycallgraph.md` are third-party text kept for reference but deliberately not republished. `content/WorkingScripts/` is a Python/shell script stash that lives under `docs/` but is not documentation.
- **Notebooks execute at build time** (`mkdocs-jupyter`, `execute: True`). They are all stdlib-only and deliberately kept that way — a notebook importing a package not in `requirements.in`, or reading a local data file, will break the Read the Docs build.
- **Theme customization** lives in `overrides/` (`main.html`, `partials/copyright.html`) via `theme.custom_dir` — do not fork the Material theme itself.
- Markdown authoring leans on Material/pymdownx features already enabled: admonitions, content tabs, task lists, mermaid fences (```mermaid), MathJax via `pymdownx.arithmatex` (config in `docs/javascripts/mathjax.js`), and file inclusion via `markdown-include`. `docs/content/features_demo/feature_demo.md` is the working reference for these.
- **The docs tree doubles as an Obsidian vault**, so Obsidian syntax leaks in. `![[image]]` embeds and `[[wikilinks]]` render as literal text in mkdocs — convert them to standard Markdown when you find them.
