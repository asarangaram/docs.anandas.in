
Assume you have created a Flask Application for your micro service. to deploy it on a linux machine, there are many ways. Most of the people provide containers. However, for most of the cases I came across the container is a overkill and most of the time providing a installer is sufficient. This installer will setup the files, create a WSGI service on the machine, then setup a nginx site by which the clients can access. Once this installer is run, the service should be up and running. This script can also handle ??
Some of the important aspect of this script:
1. This should interactive to get some of the configuration parameters the flaks application required in addition to the ports. 
	1. We need to keep the ports configurable so that the user can handle the port conflict with other applications.
	2. The storage location for your app should be configurable, as user may want to place it in another device that has enough space.
2. It should be fully automated and avoid manual editing of the system files later. 
	1. 


#### Service requirement
There are three services to start
1. WSGI service
2. Celery service
3. Avahi service



Let us use a simple 'Hello world' program for ease of understanding. 
## What we are creating?

Assume we have a myapp. The objective of this project is to create myapp.deb that can be installed on a debian machine using apt.

apt install ./myapp.deb

The installer creates an app folder in /opt/myapp. Copies the python script. Create a virtual environment and install the required packages inside the virtual environment  using pip. run a sanity test to confirm the application runs. Then it creates a system service that runs this application when the system starts. 

### The files we need to  create