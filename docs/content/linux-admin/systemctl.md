---
tags:
  - todo
---

!!! warning "Work in progress"
    These are rough notes, not a finished write-up.

# Useful commands with systemctl (tested on Ubuntu)

* [***Hint***] You may need to use 'sudo' before every command below if your OS is configured so.

## How to create a service?
-- TODO

## How to check the status of a service?
```
systemctl status [servicename]
```

## How to restart  a service after a file changes?
```
systemctl daemon-reload
systemctl restart [servicename]
```

## How to remove a service? 
```
systemctl stop [servicename]
systemctl disable [servicename]
rm /etc/systemd/system/[servicename]
rm /etc/systemd/system/[servicename] # and symlinks that might be related
rm /usr/lib/systemd/system/[servicename] 
rm /usr/lib/systemd/system/[servicename] # and symlinks that might be related
systemctl daemon-reload
systemctl reset-failed
```


## Example services

### Avahi service

```
[Unit]
Description= Avahi Broadcast Service
After=network.target

[Service]
Type=simple
User=anandas
Group=anandas
# this service ignores WorkingDirecotyr
WorkingDirectory=/

# Activate the virtual environment and run Celery
ExecStart=/bin/bash -c 'avahi-publish-service -s "server100@cloudonlapapps" _http._tcp 5000 "CL Image Repo Service" '

# Restart automatically if the service fails
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
```

### Celery Service

```
[Unit]
Description=Celery Worker Service
After=network.target

[Service]
Type=simple
User=anandas
Group=anandas
WorkingDirectory=/home/anandas/app/media_repo

# Activate the virtual environment and run Celery
ExecStart=/bin/bash -c 'source /home/anandas/app/media_repo/.venv/bin/activate && celery -A src.celery_worker.celery worker --loglevel=info --concurrency=4'

# Restart automatically if the service fails
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
```