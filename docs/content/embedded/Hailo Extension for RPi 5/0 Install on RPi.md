---
title: Install Hailo + DeGirum on Raspberry Pi
tags:
  - raspberry-pi
  - raspberry-pi-os
  - hailo
  - ai
  - degirum
  - setup
---

# Installation on Raspberry Pi
## Vim
The Vi Editor is older, install Vim
```
sudo apt install vim
```
## Bash 
Add the following into ~/.bashrc file
```
alias ll="ls -l"
export HISTSIZE=2000
export HISTFILESIZE=2000
# ignorespace erasedups
export HISTCONTROL=ignoreboth
```
## SSH and Git 
```
ssh-keygen -t ed25519
cat /home/anandas/.ssh/id_ed25519.pub
```
copy the output into git's settings 
```
git config --global user.email "4833102+asarangaram@users.noreply.github.com"
git config --global user.name "Ananda S RPi"
```
## Hardware
```
sudo apt update && sudo apt full-upgrade
sudo raspi-config
```
Modify the following via TUI
> `Advanced Options` => `PCIe Speed` => `Yes` =>  `Finish` 
> `Advanced Options` > `Bootloader Version`, choose `Latest` , allow the system to update.

When requesting to reboot, accept `yes` or  `sudo reboot now`
## Install Hailo
The below installs the default version. Just check if the version is supported by Digirum.
```
sudo apt install hailo-all
hailortcli fw-control identify
sudo systemctl enable --now hailort.service
```
## Install DeGirum
### Create a virtual Environment
``` bash
python3 -m venv ~/degirum_env
source ~/degirum_env/bin/activate
cd ~/demos
git clone git@github.com:asarangaram/degirum_hailo_examples.git
cd degirum_hailo_examples
pip install -r requirements.txt
# for some reasons, these two needed to be installed seperately
pip install matplotlib lancedb
python test.py 
```
## setup Jupiter Lab.

```
python -m ipykernel install --user --name=degirum_env --display-name "Python (degirum_env)"
jupyter lab --no-browser --port=8889
```
# Now you can access the Jupiter Notebooks from a browser with the link displayed on the terminal


## Take Backup 
	Image Name: SDCardBackup_Hailo_Digirum.img

