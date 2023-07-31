---
title: Chapter 3 - Image Endpoint | Image Repo as a Flask Microservice
weight: 551300
---

# Image Endpoint

In this chapter, we shall create few end point to store and retrieve images
* upload an image `POST /image/upload`
* download an image `GET /image/<id>`
* delete an image `DELETE /image/<id>'
* list the images `GET /image/list`

Images are uploaded as binary data, hence they need to be stored in a _file_. Image can be created, retrieved and deleted. Image also has auxilary data, like who created it, when it was uploaded, what was its original name and metadata already attached into it, like EXIF data. To ensure better retriavability, we need to extract these information and store them in a data base. Having a data base also help to uniquely identify an image, filter the image list based on various parameters. 

We shall use _MySQL_ database and _SQLAlchemy_. _SQLAlchemy_ is an Object-Relational Mapping (ORM) library primarily designed for working with relational databases in Python. We use this to map the Python object into row in a table. 

## Installation
### Create _MySQL_ Database
We need to install _MySQL_, and start as service. This is explained here/TODO. Once the MySQL is installed, we need a user account and a database in _MySQL_ to proceed.

Login to _MySQL_ as `root`.

```bash
mysql -u root -p
Enter password: 
...
Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> 
```

On the mysql prompt, perform the following to create database (`image_repo_db`), create user (`image_repo_admin`) and give all privileges on the data base to the user. Note down the password used to create the account.

```sql
mysql> CREATE DATABASE image_repo_db
Query OK, 1 row affected (0.01 sec)

mysql> CREATE USER 'image_repo_admin'@'localhost' IDENTIFIED BY '<pw>';
Query OK, 0 rows affected (0.03 sec)

mysql> GRANT ALL PRIVILEGES ON image_repo_db.* TO 'image_repo_admin'@'localhost';
Query OK, 0 rows affected (0.00 sec)

mysql> EXIT;
Bye
```
### Test _MySQL_ Database

Test the database and user, by connecting to _MySQL_ with newly created user.

```bash
mysql -u image_repo_admin -p
Enter password: 
...
Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> 
```

Perform the following commands in _MySQL_ prompt.
```sql
mysql> SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| image_repo_db      |
| information_schema |
| performance_schema |
+--------------------+
3 rows in set (0.00 sec)

mysql> USE image_repo_db;
Database changed
mysql> CREATE TABLE testtable (id INT, name VARCHAR(50));
Query OK, 0 rows affected (0.19 sec)

mysql> SHOW TABLES;
+-------------------------+
| Tables_in_image_repo_db |
+-------------------------+
| testtable               |
+-------------------------+
1 row in set (0.00 sec)

mysql> INSERT INTO testtable (id, name) VALUES (1, 'John');
Query OK, 1 row affected (0.02 sec)

mysql> SELECT * FROM testtable;
+------+------+
| id   | name |
+------+------+
|    1 | John |
+------+------+
1 row in set (0.00 sec)

mysql> DROP TABLE testtable
    -> ;
Query OK, 0 rows affected (0.03 sec)

mysql> SHOW TABLES;
Empty set (0.00 sec)

mysql> EXIT;
Bye
```

### Install Modules
We could install _SQLAlchmey_ module using pip and update requirement.txt as below.

```bash
image_repo $ cd ~/work/image_repo
image_repo $ source .venv/bin/activate

(.venv) image_repo $ pip install Flask-SQLAlchemy PyMySQL Pillow cryptography
(.venv) image_repo $ pip freeze > requirements.txt

(.venv) image_repo $ git add requirements.txt 
(.venv) image_repo $ git commit -m "update requirement.txt"
[ImageEndPoint 4588e50] update requirement.txt
 1 file changed, 9 insertions(+)
(.venv) image_repo $ 
```
You may notice this has installed few more dependent modules too.





### Utility functions
we require two utility functions that will be used by our models, to load the image from the cache of werkzeug and to compute hash.

When a file is uploaded and received by Flask, it goes to werkzeug's cache. The file in this cache is one time read, i.e., once the file content is read from the file storage, it is removed. Hence the application should buffer it till it get saved.

**Why we can't store immeidately?**
because, we may want to preprocess it before storing. One such preprocessing is to find if the file being uploaded has any duplicate in our storage. We are going to achieve this by comparing the hash (sha512) value of existing files. By making this hash as unique, we can ensure that we only compare only one hash and don't store the file twice.

Once the preprocessing is done, we can store the image into the storage area and discard the buffer.

####  `load_image_from_werkzeug_cache`
```python
# image_proc/file_utilities.py

from io import BytesIO
from werkzeug.datastructures import FileStorage

def load_image_from_werkzeug_cache(im:FileStorage):
    """ If successful, return the bytes, else raise exceptions"""
    bytes_io = BytesIO()
    im.save(bytes_io)
    bytes_io.seek(0)
    return bytes_io

```

#### `sha512hash`
```python
# image_proc/hash.py
from PIL import Image
import hashlib

def sha512hash(image_data):   
    with Image.open(image_data) as im:
        hash = hashlib.sha512(im.tobytes()).hexdigest()
    return hash
    
```

### Endpoint implementation

Similar to landingpage, we implement 4 files for image endpoint.
```
src/endpoint/image/
├── blueprints.py
├── __init__.py
├── models.py
└── resources.py
```

We implement the following endpoints.

| Endpoint              | Supported methods | Usage                                                        | Comments                                                   |
|-----------------------|-------------------|--------------------------------------------------------------|------------------------------------------------------------|
| /upload               | POST              | `http  -b --multipart POST :5000/image/upload image@`        | Uploads the image                                          |
| `/IMAGE_ID`           | GET, DELETE       | http GET :5000/image/1 --download
http DELETE :5000/image/1
 | replace IMAGE_ID by appropriate int id, provided by server |
| `/IMAGE_ID/details`   | GET               | http  GET :5000/image/1/details                              |                                                            |
| `/IMAGE_ID/thumbnail` | GET               | http  GET :5000/image/1/thumbnail                            |                                                            |
| `/list`               | GET               | http  GET :5000/image/list                                   |                                                            |
|                       |                   |                                                              |                                                            |
These are the basic end points, we may enhance the functionality of each endpoint by adding query parameters. Which we shall implement in later chapters.

### Create `db.py`
Create a new file `src/db.py` and add the following lines.
```python
# db.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
```

### Changes in `src/app_factory.py`

Edit the file `src/app_factory.py` , as below. 
1.  import `db` from `db.py`,  initialize it and create all required tables.
2.  register `image_bp` blueprint.

```python
(.venv) image_repo $ git diff src/app_factory.py
diff --git a/src/app_factory.py b/src/app_factory.py
index 5873a12..78306f7 100644
--- a/src/app_factory.py
+++ b/src/app_factory.py
@@ -1,13 +1,21 @@
 # app_factory.py
 
 from flask import Flask
+
+from db import db
 from endpoint.landing.blueprint import landing_bp
+from endpoint.image.blueprints import image_bp
 
 def create_app(config_object):
     app = Flask(config_object.APP_NAME)
     app.config.from_object(config_object)
     
+    db.init_app(app)
+    with app.app_context():
+        db.create_all()
+    
     ## Landing Page
     app.register_blueprint(landing_bp)
+    app.register_blueprint(image_bp)
     
     return app



```


### Changes in `config.py`


```python
image_repo $ git diff src/config.py
diff --git a/src/config.py b/src/config.py
index f624444..743a042 100644
--- a/src/config.py
+++ b/src/config.py
@@ -8,4 +8,12 @@ class ConfigClass(object):
     except: 
         SECRET_KEY = 'Secret!'
     PROPAGATE_EXCEPTIONS = True
-    

+    
+    # Flask-SQLAlchemy
+    password = os.environ['MYSQL_IMAGE_REPO_ADMIN_PW']
+    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://image_repo_admin:{password}@localhost/image_repo_db"
+    
+    SQLALCHEMY_TRACK_MODIFICATIONS = False
+    
+    # File Save
+    FILE_STORAGE_LOCATION = "/home/anandas/storage/image_repo"


```
#### For SQLAlchemy
We need to setup two config variables in `ConfigClass` (`config.py`) for `FLASK-SQLAlchemy` as below.  

```python
password = os.environ['MYSQL_IMAGE_REPO_ADMIN_PW']
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://image_repo_admin:{password}@localhost/image_repo_admin"
SQLALCHEMY_TRACK_MODIFICATIONS = False
```
* we retrieve the password from an environment variable called `MYSQL_IMAGE_REPO_ADMIN_PW`.Ensure that `MYSQL_IMAGE_REPO_ADMIN_PW` is defined using the same password used in _MySQL_ and exported as an environment variable. Additionally, remember not to store this password in any repositories and keep it confidential.

* The `SQLALCHEMY_TRACK_MODIFICATIONS` is an option configuration option in Flask-SQLAlchemy that determines whether to track modifications of objects and emit signals (before and after each database operation). Keeping track of every change in the session, can consume memory and CPU resources, especially in large-scale applications. Therefore, it is recommended to set `SQLALCHEMY_TRACK_MODIFICATIONS` to `False` in production environments unless you specifically need the modification tracking functionality. 

#### For File storage
Point this variable to the location where we store the images, and other artifaces that will be generated by the server.
```python
FILE_STORAGE_LOCATION = "/path/to/storage"
```


## Wind up

Now that we have impemented all, we can commit the changes to git.
We can run the server and test it using httpie's http command.
