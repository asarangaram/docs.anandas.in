---
title: Setting up RPi to work with Hailo HAT
tags:
  - raspberry-pi
  - raspberry-pi-os
  - hailo
  - ai
  - setup
  - headless
  - ssh
  - static-ip
---

# Setting up RPi to work with Hailo HAT

A clean, **headless** bring-up of a Raspberry Pi 5 with a Hailo AI HAT — from a
blank SD card to `hailortcli fw-control identify` reporting the NPU. After the first
boot no monitor is attached; everything is driven over SSH.

!!! note "What this was tested on (2026)"
    - **Raspberry Pi 5 (8 GB)** + **Hailo-8** (26 TOPS AI HAT+)
    - **Raspberry Pi OS Lite (64-bit)** — which is now **Debian 13 "trixie"**, kernel 6.18
    - **HailoRT 4.23.0** (the `hailort` apt package)
    - 16 GB SD card for boot; Wi-Fi on a 5 GHz network in India

    The older RPi write-ups in this vault target Ubuntu / earlier releases and have
    drifted — this one reflects the current packages.

## 1. Flash Raspberry Pi OS Lite (headless)

Use **Raspberry Pi Imager** and choose *Raspberry Pi OS Lite (64-bit)* — "Lite" means
no desktop, exactly what a headless appliance wants.

!!! warning "Use Imager's customization, not a raw image drop-in"
    Imager's gear / *Edit Settings* screen (hostname, user, SSH key, Wi-Fi, locale)
    wires up the first-boot config reliably. Writing the raw `.img` with `dd` and
    dropping a `custom.toml` on the boot partition **did not auto-apply** on the trixie
    image — the Pi booted into the interactive first-boot user wizard instead. If that
    happens, just configure it live on the console once (next step).

Set at flash time: hostname (e.g. `edge-infer-01`), username, **SSH public key**,
Wi-Fi with the correct **country**, and timezone.

## 2. First boot & headless basics (if not preset)

If the customization didn't take, attach HDMI + keyboard **once**, create the user,
then set the essentials:

```bash
sudo hostnamectl set-hostname edge-infer-01
# keep /etc/hosts in sync, or sudo warns "unable to resolve host edge-infer-01":
echo "127.0.1.1 edge-infer-01" | sudo tee -a /etc/hosts

sudo systemctl enable --now ssh
install -d -m700 ~/.ssh
echo 'ssh-ed25519 AAAA... you@laptop' >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

## 3. Wi-Fi on 5 GHz (the India / regulatory gotcha)

Two Pi quirks bite here: the radio is **rfkill-blocked until a country is set**
(Wi-Fi shows as "unavailable"), and under `IN` the 5 GHz band only works on the low
channels **36–48**. Set the country, then connect:

```bash
sudo raspi-config nonint do_wifi_country IN
sudo nmcli device wifi connect '<SSID>' password '<password>'
```

Full walkthrough + the router-channel fix →
[How to fix Raspberry Pi Wi-Fi that won't connect](../../FAQ/raspberry-pi-wifi-wont-connect.md).

## 4. SSH key login

```bash
ssh anandas@edge-infer-01.local       # or ssh anandas@<ip>
```

If the key isn't in place yet (or you can't paste it at a console) →
[How to copy your SSH key to a headless machine](../../FAQ/copy-ssh-key-to-headless-machine.md).
After a re-flash, clear a stale host key with `ssh-keygen -R <ip>`.

## 5. Static IP

Raspberry Pi OS uses **NetworkManager**, so pin the address with `nmcli` (there's no
static-IP field in `custom.toml`) — use `192.168.0.105/24`, gateway `192.168.0.1`, and
add a matching **router DHCP reservation**. Full steps →
[How to set a static IP with NetworkManager (nmcli)](../../FAQ/static-ip-with-networkmanager.md).

## 6. Base upgrade

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

## 7. Install HailoRT — the lean set (no UI stack)

`hailo-all` is a meta-package that drags in **hundreds** of packages: a full
GUI/GStreamer/OpenCV/TAPPAS/`rpicam-apps` stack. For a **headless image-inference**
box you only need the runtime, the PCIe driver, and (optionally) the Python bindings:

```bash
sudo apt install hailort hailort-pcie-driver python3-hailort
sudo reboot          # required so the hailo_pci kernel module loads
```

!!! warning "DKMS fallback on trixie"
    The PCIe driver may print *"Failed to install PCIe driver to the DKMS tree. Trying
    to install PCIe driver without DKMS."* It works for the **current** kernel, but it
    will **not** auto-rebuild on a kernel upgrade. On an always-on box, hold kernel
    updates (or fix DKMS) before upgrading the kernel — otherwise the NPU disappears
    after the next reboot.

Add `hailo-tappas-core` (GStreamer pipelines) only if/when you tackle live **video**.

## 8. Verify the NPU

```bash
lsmod | grep hailo            # -> hailo_pci ...
ls -l /dev/hailo0             # device node present
hailortcli scan               # -> Device: 0001:01:00.0
hailortcli fw-control identify
```

Expected:

```text
Firmware Version: 4.23.0 (release,app,extended context switch buffer)
Board Name:          Hailo-8
Device Architecture: HAILO8
```

That's the milestone — HailoRT is talking to the Hailo-8 over PCIe, and the box is
ready to run compiled `.hef` models. Next: obtain/compile a HEF (see
[Data Flow Compiler](<Data Flow Compiler.md>)) and run one end-to-end.

## Gotchas, in one place

- **`custom.toml` ignored on a raw `dd` flash** → use Imager's customization, or configure on first boot.
- **Wi-Fi "unavailable"** = rfkill until `do_wifi_country` is set.
- **5 GHz won't associate under `IN`** unless the router is on channel 36–48.
- **Static IP is NetworkManager now**, not `dhcpcd.conf`; no `custom.toml` field for it.
- **`sudo` warns "unable to resolve host"** until `/etc/hosts` carries the new hostname.
- **`hailo-all` is huge** — install `hailort` + `hailort-pcie-driver` + `python3-hailort` for headless.
- **PCIe driver DKMS fallback** — won't survive kernel upgrades unattended.
