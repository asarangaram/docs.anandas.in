---
tags:
  - scanner
  - sane
  - linux
---

# Installing the Brother DS-620 on Linux

The **Brother DS-620** is a sheet-fed USB scanner. To drive it from Linux
(`scanimage`, SANE) you need Brother's **closed** `libsane-dsseries` backend —
it is **not** part of the stock `sane-backends`, so a plain `apt install
sane-utils` will *not* see the scanner.

!!! warning "macOS cannot be the scan host"
    On macOS the DS-620 is locked to Brother's TWAIN driver for exclusive
    access, so no SANE/CLI tool can open it. A Mac can only be a *client* that
    scans over SSH from a Linux host. Keep the scanner on a Linux machine.

## Steps (Debian / Ubuntu, amd64)

```sh
sudo apt install -y sane-utils

# Brother's SANE backend for the DS-series (closed x86 binary)
wget https://download.brother.com/welcome/dlf100976/libsane-dsseries_1.0.5-1_amd64.deb
sudo dpkg -i libsane-dsseries_1.0.5-1_amd64.deb
```

Then **unplug and replug** the scanner and verify:

```sh
scanimage -L
# device `dsseries:usb:0x04F9:0x60E0' is a BROTHER DS-620 sheetfed scanner
```

If it lists the device, you can scan:

```sh
scanimage -d 'dsseries:usb:0x04F9:0x60E0' --format=png --resolution 300 > page.png
```

## The `libsane` dependency trap (Ubuntu 24.04+)

The `.deb` declares `Depends: libsane`, but modern Ubuntu **renamed that package
to `libsane1`**. So `dpkg -i` fails with:

```
libsane-dsseries : Depends: libsane but it is not installable
```

`sudo dpkg -i --force-all …` installs it anyway, but it leaves an **unsatisfied
dependency recorded** — which later makes `apt` refuse to do anything ("unmet
dependencies") and can wedge unrelated installs (e.g. it broke a mosquitto
install for me later the same day).

The clean fix is a tiny **shim package** named `libsane` that just depends on
`libsane1`, so the real dependency is satisfied:

```sh
mkdir -p /tmp/libsane-shim/DEBIAN
cat > /tmp/libsane-shim/DEBIAN/control <<'EOF'
Package: libsane
Version: 1.0.0
Architecture: amd64
Maintainer: local
Depends: libsane1
Description: Shim so packages depending on libsane resolve to libsane1.
EOF
dpkg-deb --build /tmp/libsane-shim /tmp/libsane-shim.deb
sudo dpkg -i /tmp/libsane-shim.deb                       # provide 'libsane'
sudo dpkg -i libsane-dsseries_1.0.5-1_amd64.deb          # now resolves cleanly
sudo udevadm control --reload && sudo udevadm trigger
```

## Notes

- **x86/x64 only.** The driver is a closed binary with **no ARM build**, so a
  Raspberry Pi **cannot host** the scanner (a Pi can still be an SSH *client*).
- **RPM systems:** same driver at
  `https://download.brother.com/welcome/dlf100974/libsane-dsseries-1.0.5-1.x86_64.rpm`.
- **Permission errors** from `scanimage -L`: the driver installs a udev rule
  (`/etc/udev/rules.d/…Brother_DSScanner.rules`); add your user to the `scanner`
  group and replug.
- Related: [Fixing the yellow cast and vertical banding](fixing-ds620-colour-and-banding.md)
  and the FAQ [Why `scanimage` is slow](../../FAQ/scanimage-slow-airscan.md).
