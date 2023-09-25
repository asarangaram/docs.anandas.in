# How to Build this workspace?

Perform the following steps once.

### Clone the package

```
git clone git@github.com:asarangaram/docs.anandas.in.git
```

### Install required Linux packages

```
sudo  apt install python3.10 python3.10-venv mkdocs
```

### Create a Virtual environment and activiate

```
python -m venv .venv
source .venv/bin/activate
```

### Install `pip-tools`

```
pip install pip-tools
```

### Install python dependencies

```
pip-compile --config=pyproject.toml requirements.in >& requirements.txt 
pip install -r requirements.txt
```

Note
    : If we use readthedocs' CI/CD, update requirement.txt into git, if there 
    is any change. 
    FIXME: Can we change the configurations in readthedocs.yaml to use
    requirement.in instead of requirement.txt?

### Run locally

```
mkdocs serve
mkdocs build

```
