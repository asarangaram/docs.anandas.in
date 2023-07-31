---
title: MySQL
weight: 116000
---

{{% button href="https://www.mysql.com/" icon="fas fa-external-link-alt" icon-position="right" %}}MySQL Home{{% /button %}}
{{% button href="https://www.mysql.com/" icon="fas fa-external-link-alt" icon-position="right" %}}MySQL Home{{% /button %}}

### How to install and configure?

#### install and start the service

```
sudo apt update
sudo apt install mysql-server
sudo service mysql start
```

#### setup root password

```
sudo mysql -u root
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'new_password';
FLUSH PRIVILEGES;
EXIT;
```

#### Configure MySQL security

```
sudo mysql_secure_installation
```

Note, after this, root can be accessed by `mysql -u root -p`

### Where the MySQL database is stored and do we have control over it?

MySQL stores its tables and data in a directory called the "data directory." The location of the data directory depends on the operating system and the configuration settings of your MySQL installation.

the default location is `/var/lib/mysql`. this can be moved to another location by editing `/etc/mysql/mysql.conf.d/mysqld.cnf`.

This can be useful, for example, if you want to store the MySQL data on a different disk or partition with more storage capacity.

```
sudo service mysql stop
sudo rsync -av /var/lib/mysql /new/datadir/location
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
# replace /var/lib/mysql with the new data directory path
sudo chown -R mysql:mysql /new/datadir/location
sudo chmod -R 755 /new/datadir/location
# update the AppArmor profile to allow MySQL access to the new data directory
sudo vi /etc/apparmor.d/usr.sbin.mysqld
# replace /var/lib/mysql with the new data directory path
sudo apparmor_parser -r /etc/apparmor.d/usr.sbin.mysqld
sudo service mysql start
```

### How to check if MySQL is running and functional?

First check `sudo service mysql status` and then,

```
mysql -u root -p
SHOW DATABASES;
CREATE DATABASE testdb;
USE testdb;
CREATE TABLE testtable (id INT, name VARCHAR(50));
SHOW TABLES;
INSERT INTO testtable (id, name) VALUES (1, 'John');
SELECT * FROM testtable;
EXIT;

```

### How to make sure it is secure and can be accessed only from localhost?

by default, bind-address is set to 127.0.0.1. It means, it listens only localhost.
If we maintain the db in a maching and access it from another, it may be required. For current use case, there is no such need.

# How to create an user and give permission to a database?

```
CREATE USER 'clapps'@'localhost' IDENTIFIED BY <pw>
CREATE DATABASE CLAPPS_v1;
GRANT ALL PRIVILEGES ON CLAPPS_v1.* TO 'clapps'@'localhost';
```

### How to migrate the db from one machine to another?

It is possilbe to dump each database using mysqldump and restore in different machine.

```
mysqldump -u root -p --opt mydatabase > mydatabase_backup.sql
mysql -u root -p mydatabase < mydatabase_backup.sql

```

Additionally,

> Consider any configuration differences, user accounts, and privileges, as they may need to be adjusted to match the new environment.
>
> Ensure compatibility between the MySQL versions on both systems. If the MySQL versions differ, you may need to perform additional steps, such as exporting and importing data in a compatible format or upgrading the MySQL server on the destination system.\*\*\*\*

`SHOW DATABASES;` gives the database names of the given user.

### How to change the table?

### This yet to learn

- MySQL Workbench
- Complete understanidng of "Migrating a MySQL database"
