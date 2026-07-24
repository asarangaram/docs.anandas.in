---
tags:
  - scanner
  - sane
  - linux
---

# Scanning from (almost) any scanner on Linux with SANE

On Linux, scanners are driven by **SANE** (Scanner Access Now Easy). The
command-line front-end is `scanimage`; it supports a huge range of USB and
network scanners, and many network multifunction printers work driverless via
`sane-airscan` (eSCL/WSD).

The essentials:

```sh
sudo apt install -y sane-utils      # scanimage + core backends

scanimage -L                        # list detected scanners and their ids
scanimage -d '<id>' --format=png --resolution 300 > page.png
```

Rather than duplicate the excellent existing documentation, use these:

- **ArchWiki — SANE**: <https://wiki.archlinux.org/title/SANE> — setup,
  backends, permissions, network scanning, troubleshooting. The best single
  reference even if you're not on Arch.
- **SANE supported devices**: <http://www.sane-project.org/sane-supported-devices.html>
  — check your model and which backend it needs before buying/installing.

Scanner-specific notes on this site:

- [Installing the Brother DS-620 on Linux](brother-ds620/installing-ds620-on-linux.md)
  — a scanner whose backend is **not** in stock SANE.
- FAQ: [Why `scanimage` is slow](../FAQ/scanimage-slow-airscan.md).
