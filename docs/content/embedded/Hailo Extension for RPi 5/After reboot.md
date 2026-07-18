---
title: After reboot
tags:
  - todo
---

# After reboot

!!! warning "Work in progress"
    These are rough notes, not a finished write-up.

If you start from `SDCardBackup_Hailo_Digirum.img`, else complete steps in [Install on RPi](0 Install on RPi.md)

Login to the session with 
```
ssh -L 8889:localhost:8889 anandas@192.168.0.225
```

Then start the Jupiter lab server
```
source ~/degirum_env/bin/activate
jupyter lab --no-browser --port=8889
```

