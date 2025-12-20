If you start from `SDCardBackup_Hailo_Digirum.img`, else complete steps in [[0 Install on RPi]]

Login to the session with 
```
ssh -L 8889:localhost:8889 anandas@192.168.0.225
```

Then start the Jupiter lab server
```
source ~/degirum_env/bin/activate
jupyter lab --no-browser --port=8889
```

