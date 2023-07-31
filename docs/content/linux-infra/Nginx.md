---
title: Nginx
weight: 112000
---

## Why apache need to be removed?

I use `nginx` as webserver. By default, the `apache` is installed and listens the ports required. So, we need to disable it and install `nginx`. While disabling the `a111pache` service is sufficient, I found that sometime the software update tries to restart the service. As I couldn't find an easier way to stop the auto start of `apache` now and then and conflict with `nginx` setup, I remove `apache` completely and then install. Anyways I will not use `apache` and Nginx together.

## Few utility commands, useful at this stage.

| command                               | purpose                                                                 |
| ------------------------------------- | ----------------------------------------------------------------------- |
| `apt update && apt upgrade -y`        | to update and upgrade the system, now and then we may need to run this. |
| `lsof -i -P -n \| grep LISTEN`        | To list the ports being listen to and by what service                   |
| `systemctl list-units --type=service` | list the services running                                               |
| `systemctl list-units --all`          | list services including inactive                                        |

## Remove apache

```
systemctl stop apache2
sudo systemctl disable apache2

sudo apt-get purge apache2 apache2-utils apache2.2-bin apache2-common
sudo apt-get autoremove
whereis apache2
sudo rm -rf /etc/apache2 /usr/sbin/apache2 /usr/lib/apache2 /usr/share/apache2 /usr/share/man/man8/apache2.8.gz
whereis apache2

```

## Install nginx

```
sudo apt update
sudo apt-get install nginx
sudo service nginx start # required if it fails to auto start
```
