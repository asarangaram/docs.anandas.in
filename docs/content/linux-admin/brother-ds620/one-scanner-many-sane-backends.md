---
tags:
  - todo
  - scanner
  - sane
---

!!! warning "Work in progress"
    Rough notes — the de-duplication approach here is a stopgap and will be
    revisited with a proper per-device fingerprint.

# One physical scanner, listed under several SANE backends

`scanimage -L` can show the **same physical scanner more than once** — once per
backend that can reach it. A single network Epson showed up three times:

```
device `epsonds:net:192.168.0.176'      is a Epson ET-2810 Series ESC/I-2
device `epson2:net:192.168.0.176'       is a Epson PID flatbed scanner
device `airscan:w1:EPSON L3250 Series'  is a WSD EPSON L3250 Series ip=192.168.0.176
```

The id is `backend:transport:address`:

| backend | what it is |
|---|---|
| `epsonds` | Epson's **modern** vendor driver (ESC/I-2) over the network |
| `epson2`  | Epson's **legacy** vendor driver (older ESC/I) — same device |
| `airscan` | **driverless** eSCL/WSD via `sane-airscan` (`e*` = eSCL, `w*` = WSD) |

Any of the ids works with `scanimage -d <id>`. A rough preference is
`epsonds` (native) or `airscan` (driverless); `epson2` is the legacy fallback.
A USB device like `dsseries:usb:0x04F9:0x60E0` is separate — its own backend
over USB, and the only one here with a real serial.

## De-duplicating (open question)

To collapse duplicates you need a **stable physical-device identity**. Current
stopgap: group by USB serial, else by network IP (parsed from the id/description).
That's heuristic and can be fooled. The better approach — **build a real
fingerprint per device** (USB bus/topology, eSCL/WSD UUID, MAC) — is still to be
designed. TODO.

Related: [Installing the DS-620 on Linux](installing-ds620-on-linux.md).
