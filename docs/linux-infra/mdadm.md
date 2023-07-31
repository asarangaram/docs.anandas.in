---
title: Multiple Disk and Device Management
weight: 115000
---

`Multiple Disk and Device Management`

`mdadm` is a Linux utility used to manage and monitor software RAID devices.

## To create, format and mount

```bash
#create
sudo mdadm --create --verbose /dev/md0 --level=1 --raid-devices=2 /dev/sda /dev/sdb

# monitor
mdadm --detail /dev/md0

# format
sudo mkfs.ext4 /dev/md0

sudo mkdir /vol/raid
sudo mount /dev/md0  /vol/raid
```
