# How to Build this workspace?

The site is published at [til.anandas.in](https://til.anandas.in).

Source of truth is a self-hosted Forgejo instance on the LAN. GitHub is a
read-only push mirror — do not commit there, its history is overwritten on
every sync. See
[Self-hosting this TIL site](https://til.anandas.in/content/linux-infra/til_website_setup/)
for the full setup.

Perform the following steps once.

### Clone the package

```
git clone git@<LAN_ADDRESS>:<USER>/til.git
```

### Install required Linux packages

```
sudo apt install python3 python3-venv
```

### Create a Virtual environment and activate

```
python3 -m venv .venv
source .venv/bin/activate
```

### Install python dependencies

```
pip install -r requirements.in
```

Read the Docs installs the same `requirements.in`, so there is no compiled
lockfile to keep in sync. The pins are open; if an upstream release ever
breaks a build, pin that one package in `requirements.in`.

### Run locally

```
mkdocs serve
mkdocs build --strict
```

Use `--strict` before pushing. It turns "page not in nav", missing-file and
broken-link warnings into errors, which is what keeps the published nav and
the files on disk from drifting apart.

### The two builds

`mkdocs.yml` is the **public** build: no `repo_url`, so Material renders no
"edit this page" button and the git host never appears in the output.

`mkdocs.internal.yml` inherits it and adds the repository link, for the copy
served on the LAN only:

```
FORGEJO_REPO_URL=http://<LAN_ADDRESS>:3000/<USER>/til \
  mkdocs build --strict -f mkdocs.internal.yml
```

### Adding a page

Navigation is derived from the directory tree by `mkdocs-awesome-nav`, so a
new file appears without editing `mkdocs.yml`. Use a directory's `.nav.yml`
to set its title or pin ordering.

Unfinished pages are published rather than hidden: give them `tags: [todo]`
frontmatter and a work-in-progress admonition. They are indexed at
[/tags/](https://til.anandas.in/tags/).
