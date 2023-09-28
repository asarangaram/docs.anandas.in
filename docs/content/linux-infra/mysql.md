---
title: MySQL
weight: 116000
---

[:fontawesome-solid-arrow-up-right-from-square: MySQL Documentation  ](https://dev.mysql.com/doc){ .md-button .md-button--primary }

## Setting up
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
If we maintain the db in a machine and access it from another, it may be required. For current use case, there is no such need.

### How to create an user and give permission to a database?

Login as root
```
mysql -u root -p
```

If user doesn't exists, create.
```
CREATE USER 'clapps'@'localhost' IDENTIFIED BY <pw>;
```
If data base doesn't exists, create
```
CREATE DATABASE CLAPPS_v1;
```
to give complete access, 
```
GRANT ALL PRIVILEGES ON CLAPPS_v1.* TO 'clapps'@'localhost';
```

If read only access is enough for a user, use SELECT instead of ALL
```
GRANT SELECT PRIVILEGES ON CLAPPS_v1.* TO 'clapps'@'localhost';
```

at the end,
```
FLUSH PRIVILEGES;
EXIT;
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

### Can multiple users access the database simultaneously?

Set up the following.

### Transaction Isolation Levels

The default isolation level is "REPEATABLE READ," which may not be suitable for concurrent operations. 
Change it into "READ COMMITTED"
```
SET TRANSACTION ISOLATION LEVEL READ COMMITTED
```

### Set Concurrent Connections

edit `sudo vi /etc/mysql/mysql.conf.d/mysqld.cnf` and update `max_connections`.

### Locking mechanism
It is better to setup a locking mechanism for update/insert/delete, to avoid conflict. 

One method is to use a table, and update the entry.

## Basics
Assuming the database is setup, to interact with it, we need to know the following basics.

Remember CRUD, when reading each section below

### Top level
There are databases and user authorized to use.

#### DATABASE
C. `CREATE DATABASE <name>;`
R. `USE <name>;`
U. - 
D. `DROP DATABASE <name>;`
L. `SHOW DATABASES;`

* There is nothing to alter within SQL. The properties of the tables are handled by configrations and other external tools. Understand more about **Configuration File**, **Command-Line Option** and **MySQL Admin Tools** to change anything on the databases.
*
##### Core Databases

There are four core databases that are integral to the operation of MySQL.
1.  `mysql`: contains user accounts, privileges, and configuration settings. It's used for user authentication and authorization.
2.  `sys`: performance-related insights and monitoring capabilities for the MySQL server.   
3.   `information_schema`: metadata information about the MySQL server, including details about databases, tables, columns, indexes, and privileges.
4.   `performance_schema`: performance-related metrics and instrumentation data, allowing you to monitor and analyze server performance.

Except `user` table in `mysql` database, none are required to be understood for basic operations. 

#### USER (table: `mysql.user`)
C. `CREATE USER <name>;`
R. `SELECT * FROM mysql.user WHERE user = 'username' AND host = 'host';`
U. `ALTER USER 'username'@'host'...` – Refer below 
D. `DROP USER <name>`
L. `SELECT user, host FROM mysql.user;`, `SHOW GRANTS`

**Notes on ALTER USER**
* `user` is always referred along with host
* As `user` is maintained in a table, it is possible to alter the columns as required, some required administrative privileges. 
    * `ALTER USER 'username'@'host' WITH MAX_CONNECTIONS 100;`
    * `ALTER USER 'username'@'host' IDENTIFIED WITH 'auth_plugin';`
    * `ALTER USER 'username'@'host' PASSWORD EXPIRE INTERVAL 180 DAY;`
* There are few special commands
    * `SET PASSWORD FOR 'username'@'host' = PASSWORD('newpassword');`
    * `RENAME USER 'olduser'@'oldhost' TO 'newuser'@'newhost';`
    * `GRANT privilege_type ON database_name.table_name TO 'username'@'host';`
    * `REVOKE privilege_type ON database_name.table_name FROM 'username'@'host';`
* One of the important command to know is `FLUSH PRIVILEGES;`
    * once the user is alterred, thje changes take effect immediately within the current session. but will not be visible to other sessions until you restart the MySQL server. To ensure that the  changes applied globally, **it's recommended to run `FLUSH PRIVILEGES` after making any changes to user accounts or privileges**.
   
### On Database
There are many many things inside a database other than tables. In basic level, you should know TABLE, INDEX and VIEW. 

C. `CREATE TABLE | INDEX | VIEW | PROCEDURE | FUNCTION | TRIGGER | EVENT`
R.  - 
U. `ALTER TABLE | VIEW |  | TRIGGER | EVENT` `CREATE OR REPLACE  PROCEDURE | FUNCTION`
D. `CREATE TABLE | INDEX | VIEW | PROCEDURE | FUNCTION | TRIGGER | EVENT`

* Anything that can be created can also be dropped
* `INDEX` can't be alterred.
* There are few more ALTER commands, `ALTER SERVER | LOGFILE GROUP | INSTANCE` which are for intermediate or advance level.
* REPLACE just drops and recreates, not really to **UPDATE**

### On Table

C. `INSERT 

#### INSERT

#### UPDATE

#### SELECT
Understanding `select` is most crucial.

### This yet to learn

- MySQL Workbench
- Complete understanidng of "Migrating a MySQL database"
