---
title: Why does scanimage take ~15s to start, and how do I speed it up?
tags:
  - how-to
  - scanner
  - sane
  - linux
weight: 199250
---

# Why does `scanimage` take ~15s to start, and how do I speed it up?

Every `scanimage` and `scanimage -L` took **~15 seconds** before doing anything —
even when scanning a **USB** scanner that has nothing to do with the network.

## Cause

`scanimage` starts SANE, which initialises **every configured backend**. If
`sane-airscan` (the driverless eSCL/WSD backend) is installed, it runs
**mDNS/Avahi discovery** to find network scanners and **blocks until a timeout**
on any device that is slow to resolve — paid on *every* scan. The tell is in the
logs:

```
scanimage[…]: protocol/discovery/avahiDiscovery.c 306: (Resolver) Failed to
resolve service 'EPSON L3250 Series' of type '_scanner._tcp' in domain 'local':
Timeout reached
```

Measured:

```sh
time scanimage -L      # → ~15 s
```

## Fix 1 — you already know the device: skip enumeration

`scanimage -L` enumerates *everything*. If you know the device id, pass it with
`-d` and never enumerate:

```sh
scanimage -d 'dsseries:usb:0x04F9:0x60E0' --format=png > page.png   # fast
```

## Fix 2 — restrict which backends load

Point `SANE_CONFIG_DIR` at a temp dir with a minimal `dll.conf` **and an empty
`dll.d/`** (which shadows the system `/etc/sane.d/dll.d/`, where each backend is
otherwise re-enabled):

```sh
TMP=$(mktemp -d)
echo dsseries > "$TMP/dll.conf"
mkdir "$TMP/dll.d"                       # empty → overrides system dll.d

time env SANE_CONFIG_DIR="$TMP:/etc/sane.d" scanimage -L
#   → ~0.1 s   (only the dsseries backend loads; no mDNS)
```

Measured: **~15 s → 0.09 s**. Backend-specific config (e.g. `dsseries.conf`) is
still found via the `/etc/sane.d` fallback in the search path.
