---
title: Chapter 1 - Installation | Image Repo as a Flask Microservice
weight: 551100
---

# Installation
In this chapter, our tasks include establishing a fundamental repository on GitHub, configuring a Python Virtual Environment, and creating an `/helloworld` endpoint. Additionally, we will incorporate WSGI (Web Server Gateway Interface) at this stage, as it will prove beneficial when setting up an external server using Nginx in a later phase.

## Create Project
Python projects, being scripting-based, typically require minimal setup. However, to maintain improved organization and traceability of our work, it is crucial to always begin with a version control tool. In this particular project, I have opted for a GitHub repository.
as a first step, We create a empty project with `README.md`, `LICENSE` (MIT License) and `.gitignore` (configured for Python)  files and name it as `image_repo` using GitHub's webinterface and cloned it in to a folder in local machine.

```bash
mkdir -p ~/work && cd ~/work && git clone git@github.com:<user>/image_repo.git image_repo
```
## Python Virtual Environment
As a first step, we need to create a virtual environment for Python. The Virtual environments in Python, considerred as a best practice to ensure consistent and reliable project setups, are crucial for creating isolated and self-contained development environments. Python 3 provides a built-in `venv`. There are few others like `virtualenv` and `conda` that provides advanced features. However, for the scope of this project, running only on Linux, supporting only Python 3, `venv` is sufficent.

Lets create…
```bash
cd ~/work/image_repo
image_repo $ ls -a
.  ..  .git  .gitignore  LICENSE  README.md
image_repo $ python3 -m venv .venv
image_repo $ ls -a
.  ..  .git  .gitignore  LICENSE  README.md  .venv
```

❗ __Remember This__
To enter into the virtual environment, we need to use activate script present in .venv/bin directory and to exit from the environment, deactivate script as below.

```bash
image_repo $ source .venv/bin/activate
(.venv) image_repo $ dea
deactivate  deallocvt   
(.venv) image_repo $ deactivate 
image_repo $ 
```
## Installing Modules using `pip`
Python Package Installer (`pip`) is the standard package manager for Python. It can be used to install the modules from PyPI (Python Package Index) and other repositories. `pip` will automatically download and install the module and its dependencies. There are few other package installers like `conda`, but we will be using pip.

### `pip list`
```bash
(.venv) image_repo $ pip list
Package    Version
---------- -------
pip        23.0.1
setuptools 67.6.1

[notice] A new release of pip is available: 23.0.1 -> 23.1.2
[notice] To update, run: pip install --upgrade pip
```
It is __not__ recommended to upgrade `pip` unless there is a specific need or issue that requires a newer version once we start using this environment, hence it is better to update at this stage and stick with the version throughout this tutorial. In later state, unless there is an instruction to update pip, ignore the notice about `pip` new release.
```bash
(.venv) image_repo $ pip install --upgrade pip
...
...
Successfully installed pip-23.1.2
(.venv) image_repo $ pip list
Package    Version
---------- -------
pip        23.1.2
setuptools 67.6.1
(.venv) image_repo $ 
```

❗ __Remember This__

The pip commands used in this tutorial.
|                                                               | PIP command                       |
| ------------------------------------------------------------- | --------------------------------- |
| to list the modules already installed                         | `pip list`                        |
| to install a module (and its dependencies)                    | `pip install <module>`            |
| to uninstall a package                                        | `pip uninstall `                  |
| to install packages listed in `requirements.txt`              | `pip install  < requirements.txt` |
| to output installed packages in requirements format and store | `pip freeze > requirements.txt`   |
##  Install Modules
To begin, let us start with flask, flask_restful,  uWSGI

**`flask`** is a popular choice for creating microservices in Python. Flask follows  WSGI speficifcation and is minimalistic. the core is lightweigth and unopinionated. We can integrate components as needed.

**`uWSGI`**  acts as a bridge between the web server (e.g., Nginx) and the `flask` application, handling high traffic with the WSGI protocol and forwarding requests to the appropriate Flask route. It is common practice for deploying Flask applications in production environments.
**`flask_restful`** module is an extension for Flask, a popular web framework in Python, that simplifies the development of RESTful APIs.
Let us install these three modules, create a requirements.txt and save it in our repository.
```bash
(.venv) image_repo $ pip install flask flask_restful uWSGI
Collecting flask
...
...
Collecting ...
Collecting ...
Installing collected packages: ...
Successfully installed ....
(.venv) image_repo $ pip freeze > requirements.txt
(.venv) image_repo $ cat requirements.txt 
aniso8601==9.0.1
blinker==1.6.2
click==8.1.3
Flask==2.3.2
Flask-RESTful==0.3.10
itsdangerous==2.1.2
Jinja2==3.1.2
MarkupSafe==2.1.3
pytz==2023.3
six==1.16.0
uWSGI==2.0.21
Werkzeug==2.3.6
(.venv) image_repo $ git add requirements.txt 
(.venv) image_repo $ git commit -m "requirement.txt file from pip"
[dev ****] requirement.txt file from pip
 1 file changed, 12 insertions(+)
 create mode 100644 requirements.txt
 (.venv) image_repo $ 
```

The version of the modules plays a big role in python development, upgraded version may add new features but may break the existing implementations due to change in the inferfaces and functionality. It is better to stick with the version unless a feature in the new feature is required. if you face any issue with this tutorial, please check the version of the packages by comparing the requirements.txt with author's repository.

## Wind up

### Summary
In this section, we learned how to setup environment for Flask.