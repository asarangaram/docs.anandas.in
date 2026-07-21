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

On a fresh Pi the Wi-Fi radio is **rfkill-blocked until a country is set** — the
symptom is Wi-Fi showing as **"unavailable"**. Set the country first:

```bash
sudo raspi-config nonint do_wifi_country IN
sudo rfkill unblock wifi
nmcli radio wifi on
nmcli device status            # wlan0 should become 'disconnected', not 'unavailable'
sudo nmcli device wifi connect 'YOUR_SSID' password 'YOUR_PASSWORD'
hostname -I                    # confirm it got an IP
```

!!! tip "5 GHz channels under the IN regulatory domain"
    With country `IN`, the Pi only reliably uses the **low UNII-1 channels — 36 / 40 /
    44 / 48**. DFS and higher channels are refused, so the Pi silently won't associate
    on them. Set your **router's 5 GHz channel to 36–48** (avoid "Auto"). This is a
    *router* setting — it can't be baked into the SD card.

## 4. SSH key login

From the laptop:

```bash
ssh anandas@edge-infer-01.local       # or ssh anandas@<ip>
```

If you re-flash and hit `REMOTE HOST IDENTIFICATION HAS CHANGED`, clear the stale
entry: `ssh-keygen -R <ip>`. To install the key without hand-typing it, serve it over
HTTP from the laptop (`python3 -m http.server 8000`) and pull it in on the Pi:
`curl -fsSL http://<laptop-ip>:8000/id_ed25519.pub >> ~/.ssh/authorized_keys`.

## 5. Static IP (NetworkManager)

Raspberry Pi OS (Bookworm / trixie) uses **NetworkManager**, so the old
`/etc/dhcpcd.conf` static-IP trick is gone — and there is no static-IP field in
`custom.toml`. Pin it after first boot on the Wi-Fi connection (named after the SSID):

```bash
sudo nmcli connection modify 'YOUR_SSID' \
    ipv4.method manual \
    ipv4.addresses 192.168.0.105/24 \
    ipv4.gateway 192.168.0.1 \
    ipv4.dns "192.168.0.1 8.8.8.8"
sudo nmcli connection up 'YOUR_SSID'
```

!!! tip "Belt and braces for a monitor-less box"
    Also add a **DHCP reservation** on the router (MAC → 192.168.0.105). The Wi-Fi MAC
    is `cat /sys/class/net/wlan0/address`. On-device static + router reservation agree
    on the same address, so nothing else can grab it and a wrong static config can't
    strand the Pi.

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
