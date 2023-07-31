---
title: Chapter 2 - First Flask App | Image Repo as a Flask Microservice
weight: 551200
---

# First Flask App
## Writing The App
The microservice we create may be used for many clients, with many endpoints. At some point, we may want to control the end points a client has access based on the client's group. As well, due to various reasons, we may want to to isolate the resources like data base for different users. One way of achieving this is to  implement authentication and maintain the user's previlage to access resources. To give the protection at higher level, we can run multiple applications that has isolated environments, custom configurations and security and data separation. For some use cases we may implement different endpoints. In this scenario, we use [`Application Factories`](https://flask.palletsprojects.com/en/2.3.x/patterns/appfactories/).

In this patern, the idea is to set up the application in a function and create instances by passing configurations. The current app configuration can be accessed from any of the file by importing `current_app` from `flask`.

Create three files, src/app_factory.py, app1/wsgi1.py and app1/config1.py. The folder structure should be as below and add the code given in this section.
```
.
├── src
│   ├── app_factory.py
│   ├── config.py
│   └── wsgi.py
├── LICENSE
├── README.md
└── requirements.txt

```

###  `config.py`
```python
# config.py
import os

class ConfigClass(object):
    APP_NAME = "Image Repo"
    try:
        SECRET_KEY = os.environ['FLASK_SECRET_KEY1'] 
    except: 
        SECRET_KEY = 'Secret!'
    PROPAGATE_EXCEPTIONS = True
    
```
SECRET_KEY and   PROPAGATE_EXCEPTIONS are two configurations required by Flask. There are many other configurations used by Flask and its Extensions. We shall add them when needed.

The `SECRET_KEY` configuration is an essential requirement in Flask. It serves as the secret key for cryptographic operations, playing a crucial role in securely signing session cookies, generating secure tokens, and protecting against specific security vulnerabilities.

* In this tutorial, we retrieve the secret key from an environment variable called `FLASK_SECRET_KEY1`. If this environment variable is not found, we fallback to using a default string. When deploying in a production environment, ensure that `FLASK_SECRET_KEY1` is defined and exported as an environment variable. Additionally, remember not to store this key in any repositories and keep it confidential.
* Depending on your requirements, you might need to configure different keys for each Flask application you develop.

The `PROPAGATE_EXCEPTIONS` configuration option in Flask controls how unhandled exceptions are handled by Flask's error handling mechanism. By default, `PROPAGATE_EXCEPTIONS` is set to `False`, which means Flask catches unhandled exceptions and handles them internally.
* In our specific deployment scenario with uWSGI, setting `PROPAGATE_EXCEPTIONS` to `True` allows uWSGI to handle exceptions and potentially log them. The details of uWSGI logging will be explained in a later chapter, providing further insights into how exceptions are handled within the uWSGI environment.[TODO:]. 

### `app_factory.py`
```python
# app_factory.py

from flask import Flask

def create_app(config_object):
    app = Flask(config_object.APP_NAME)
    app.config.from_object(config_object)
    return app
```
This provides the function that creates the Flask app, configure it from `config_object` provided and returns it.

### `wsgi.py`
```python
# wsgi.py

from app_factory import create_app
from config import ConfigClass

app = create_app(ConfigClass)

if __name__ == '__main__':   
    app.run(debug=True)

```
This module, creates the `app` by calling the app factory with `ConfigClass` and calls `app.run()` in debug mode. The method `app.run()` takes few other arguments, other than debug, which we shall discuss in later chapter.
I'll also explain why this file is named as `wsgi.py`, in later stage

##  Running The  App
### Check the port
Flask by default using port 5000.  Open a browser window and type [http://127.0.0.1:5000](http://127.0.0.1:5000) or [http://localhost:5000](http://localhost:5000).  

If port 5000 is unused, this will show a error page as we have not started the app yet. If you see, some other valid page, you are already running a flask app OR port 5000 is being used by someother application. based on the situation, either kill other process that uses the port or change the port for our application, by modifying `app.run` arguments.

> ~~`app.run(debug=True)`~~
> `app.run(debug=True, port=5002)`

Use any port that is not used in the system. If the port is free, you should get an error page similar to the following.

In firefox, I got 
```
Unable to connect

Firefox can’t establish a connection to the server at localhost:5000.

    The site could be temporarily unavailable or too busy. Try again in a few moments.
    If you are unable to load any pages, check your computer’s network connection.
    If your computer or network is protected by a firewall or proxy, make sure that Firefox is permitted to access the web.

                            [Try Again]
```

### Run App

In the terminal, run the following.
```bash
(.venv) image_repo $ python src/wsgi.py 
 * Serving Flask app 'Image Repo'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 679-157-157
```
The app is now working, with debugger enabled.  Debugger is discussed in Chapter  TODO. Now, try to access the same page [http://127.0.0.1:5000](http://127.0.0.1:5000). This time, you should get 404 error page, instead of connecting error as our app is serving on this port. However, we have not defined any landing page, hence 404 error page is displayed. 

## Adding End point
Let us implement our first end point `/` using blueprint and flask_restful. This page could be rendered from a template as a html also. However, we render JSON created by restful resource. 

Lets create a endpoint module `landing` with four files in it as below.
```
└── src
    ├── endpoint
    │   └── landing
    │       ├── blueprint.py
    │       ├── __init__.py
    │       ├── models.py
    │       └── resources.py
```
### `__init__.py`
Leave the `__init__.py` file empty. This is required as we consider this as a module while importing files. 

###  `models.py`
```python

_info = """
This is an API service that provides Microservices using REST API. Please ensure \
that you refer to the appropriate endpoint based on your specific requirements. \
Make sure to consult the API documentation or relevant resources to identify the \
suitable endpoints for your desired functionalities.\
""".strip()

class LandingPageModel:
    def __init__(self, name):
        self.name = name
        self.info = _info
    def jsonify(self):
        {"hello": self.name, "info":self.info}
```

This file contains the logics to generate content, will have access to data base etc. This file may be used independent of our Flask/REST framework. You should never import `resources.py` or `blueprint.py` into this. These files may include external modules and implement various logics to generate content. If more than one model is required, we can implement them and import into this models.py.
All the classed in this file must have Model suffix.

###  `resources.py`
```python
from flask_restful import Resource, request

from .models import LandingPageModel

class LandingPage(Resource):
    def get(self):
        name = request.args.get("name")
        if not name:
            name = "guest"
        return LandingPageModel(name), 201
```
In this file, we implement REST Resources. It may have more than one `Resource` and preferrably must be thin and call methods from models.py. all the resources related to the given endpoint (group) must be in single `resources.py`.
The class names should be meaningful and related to the endpoint, Resolving the arguments passed as part of the URL or the body must be done here.

###  `blueprint.py`
```python
from flask import Blueprint
from flask_restful import Api
from .resources import LandingPage

landing_bp = Blueprint('landing_bp', __name__, url_prefix='')
_api = Api(landing_bp)

_api.add_resource(LandingPage, '/')
```
This file maps the resources into child endpoints. There shouldn't be any other logic in it.
the variables and name must be \<endpoint\>_bp. We shouldn't import models or implement any logic in this file.

## Add Landing Page into App

Now that we have a landing page ready, let us import it into the app.
```python
# app_factory.py

from flask import Flask
from endpoint.landing.blueprint import landing_bp # Import Landing Page

def create_app(config_object):
    app = Flask(config_object.APP_NAME)
    app.config.from_object(config_object)
    
    ## Landing Page
    app.register_blueprint(landing_bp) # Register Landing Page
    
    return app
```
 
When the server is running, saving this file will automatically update it, including the new endpoint that was created. If the server is not running, you will need to restart it and then navigate to http://127.0.0.1:5000. Since we are rendering JSON, the browser may display the raw JSON or a formatted JSON content, depending on its settings.

##  API testing 
In order to overcome limitations of browsers in supporting all features of HTTP and properly handling the JSON output generated by the server, we rely on API testing tools. These tools are specifically developed to interact with APIs, allowing us to send requests and validate the responses received. Popular options like Postman and Swagger provide browser-based interfaces for conducting API testing. Additionally, there is a command-line tool called `httpie` that offers convenient API testing capabilities directly in the CLI/Terminal.

While browser-based tools are generally convenient, having a command-line tool that can be integrated into scripts greatly enhances the efficiency of writing tests. With a command-line API testing tool, it becomes easier to automate testing processes and incorporate them into various workflows.

we can install `httpie` using `sudo apt install httpie`. `httpie` tool gives a commandline executable called `http`. 
refer [`https://httpie.io/`](https://httpie.io/) for more details. [devhints.io](https://devhints.io) has a httpie cheetsheet [here](https://devhints.io/httpie)

Most of the things explained with `http` can be easily done with Postman or other API testing tools too.. 

Let us try it on our server.
```bash
(.venv) image_repo $ http http://127.0.0.1:5000
HTTP/1.1 201 CREATED
Connection: close
Content-Length: 335
Content-Type: application/json
Date: Wed, 21 Jun 2023 12:29:55 GMT
Server: Werkzeug/2.3.6 Python/3.11.3

{
    "hello": "guest",
    "info": "This is an API service that provides Microservices using REST API. Please ensure that you refer to the appropriate endpoint based on your specific requirements. Make sure to consult the API documentation or relevant resources to identify the suitable endpoints for your desired functionalities."
}

(.venv) image_repo $ 

```

If we need only body, 
```bash
(.venv) image_repo $ http -b http://127.0.0.1:5000
{
    "hello": "guest",
    "info": "This is an API service that provides Microservices using REST API. Please ensure that you refer to the appropriate endpoint based on your specific requirements. Make sure to consult the API documentation or relevant resources to identify the suitable endpoints for your desired functionalities."
}

(.venv) image_repo $ 

```

## Wind up

### Summary
In this section, we learned  how to create a Flask app, how to write resources using flask_restful, and connect it with endpoints using blueprint.  we also learned about API testing tool, `httpie`.

#### Git update
Now that our application is ready, let us submit to git.
```
(.venv) image_repo $ git add src/.
(.venv) image_repo $ git commit -m "my firstapp"
[dev cbc752b] my firstapp
 7 files changed, 65 insertions(+)
 create mode 100644 src/app_factory.py
 create mode 100644 src/config.py
 create mode 100644 src/endpoint/landing/__init__.py
 create mode 100644 src/endpoint/landing/blueprint.py
 create mode 100644 src/endpoint/landing/models.py
 create mode 100644 src/endpoint/landing/resources.py
 create mode 100644 src/wsgi.py
```

—
