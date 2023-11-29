
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
