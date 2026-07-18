# How to Build this workspace?

Perform the following steps once.

### Clone the package

```
git clone git@github.com:asarangaram/docs.anandas.in.git
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
lockfile to keep in sync (this resolves the old `pip-compile` step and its
FIXME). The pins are open; if an upstream release ever breaks a build, pin
that one package in `requirements.in`.

### Run locally

```
mkdocs serve
mkdocs build --strict
```

Use `--strict` before pushing. It turns "page not in nav", missing-file and
broken-link warnings into errors, which is what keeps the published nav and
the files on disk from drifting apart.
