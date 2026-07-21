---
title: How to fix Raspberry Pi Wi-Fi that won't connect
tags:
  - how-to
  - raspberry-pi
  - networking
  - wifi
weight: 199220
---

# How to fix Raspberry Pi Wi-Fi that won't connect

Two Pi-specific gotchas cause "it just won't join", especially on a fresh headless
install.

## Symptom 1: Wi-Fi shows as "unavailable"

The Pi's radio is **rfkill-blocked until you set the Wi-Fi country** (a regulatory
requirement). Until then `nmcli device status` shows `wlan0` as `unavailable`.

```bash
sudo raspi-config nonint do_wifi_country IN     # your ISO country code
sudo rfkill unblock wifi
nmcli radio wifi on
nmcli device status                              # wlan0 -> 'disconnected', not 'unavailable'
sudo nmcli device wifi connect '<SSID>' password '<password>'
hostname -I                                      # did it get an IP?
```

## Symptom 2: a 5 GHz network never associates

Under some regulatory domains (e.g. **IN**, India) the Pi only reliably uses the
**low UNII-1 channels — 36 / 40 / 44 / 48**. DFS and higher channels are refused, so
the Pi silently won't join a 5 GHz SSID broadcasting on them.

**Fix (on the router):** set the 5 GHz band to a fixed **channel 36–48** — avoid
"Auto", which can wander onto a channel the Pi rejects. This is a router-side setting;
it can't be configured on the Pi.

!!! note "Confirm it's a Pi-side issue"
    Check that another device joins the *same* 5 GHz SSID. If your laptop is happily on
    it at channel 36 with WPA2, the network is fine and the fix is the country/channel
    steps above — not the password or the router security mode.
