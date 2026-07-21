---
title: How to set a static IP with NetworkManager (nmcli)
tags:
  - how-to
  - networking
  - networkmanager
  - static-ip
  - linux
weight: 199210
---

# How to set a static IP with NetworkManager (nmcli)

On modern Debian / Ubuntu / Raspberry Pi OS (Bookworm and later) the network is
managed by **NetworkManager** — the old `/etc/dhcpcd.conf` static-IP trick no longer
applies.

## 1. Find the connection name

```bash
nmcli -t -f NAME,DEVICE,TYPE connection show --active
```

Wi-Fi connections are usually named after the SSID; Ethernet is often
`Wired connection 1`.

## 2. Read the current gateway/DNS (don't guess)

While still on DHCP, note what the network actually uses so you reuse the right
values:

```bash
nmcli device show <device> | grep -E 'IP4.GATEWAY|IP4.DNS'
```

## 3. Switch the connection to manual

```bash
sudo nmcli connection modify '<connection>' \
    ipv4.method manual \
    ipv4.addresses 192.168.0.105/24 \
    ipv4.gateway 192.168.0.1 \
    ipv4.dns "192.168.0.1 8.8.8.8"
sudo nmcli connection up '<connection>'
```

Verify:

```bash
ip route | grep default        # should show 'proto static'
hostname -I
```

!!! warning "If you're doing this over SSH"
    Bringing the connection down/up can drop your session. Keep the **same IP** you're
    already on (so you reconnect instantly), or schedule the reactivation detached so
    the command returns first:
    `sudo systemd-run --on-active=2 nmcli connection up '<connection>'`.
    After reactivation, re-check the **default route** — a race can leave the gateway
    route missing until the connection fully settles, which looks like "no internet".

!!! tip "Belt and braces on a headless box"
    Also add a **DHCP reservation** on the router (MAC → the same IP). The interface MAC
    is `cat /sys/class/net/<device>/address`. On-device static + router reservation
    agree on the address, so nothing else grabs it and a wrong static config can't
    strand a monitor-less machine.
