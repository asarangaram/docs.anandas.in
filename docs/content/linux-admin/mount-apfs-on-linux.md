---
tags:
  - apfs
  - macos
  - filesystem
  - mount
  - ubuntu
  - linux
  - how-to
---

# Mount an APFS (macOS) drive read-only on Linux and copy from it

You've unplugged a macOS external drive and want to read it on a Linux box —
e.g. to copy a Mac backup straight onto a NAS instead of pushing it over the
network. The drive is formatted **APFS**, which Linux does not read out of the
box. Here's the route that actually works on Ubuntu, plus two gotchas that will
bite you.

Tested on **Ubuntu 24.04**.

## `apfs-fuse` isn't packaged — use the kernel module instead

The commonly-cited `apfs-fuse` isn't in the Ubuntu repos. But two useful things
*are*:

```sh
sudo apt install apfs-dkms libfsapfs-utils
```

- **`apfs-dkms`** — the [`linux-apfs-rw`](https://github.com/linux-apfs/linux-apfs-rw)
  kernel module, built for your running kernel via DKMS. Gives a native
  `mount -t apfs`. (DKMS needs your kernel headers: `linux-headers-$(uname -r)`.)
- **`libfsapfs-utils`** — userspace tools, including **`fsapfsinfo`** for reading
  an APFS container's volumes without mounting.

Load the module (DKMS does this on install, but after a reboot):

```sh
sudo modprobe apfs
```

## Identify the volume first — don't guess the device

An APFS **container** (the partition, e.g. `/dev/sdc2`) can hold several
**volumes**, and device letters (`sdc`, `sdd`, …) can swap between reboots or
re-plugs. Read the volume names before mounting:

```sh
sudo fsapfsinfo /dev/sdc2
```
```
Container information:
	Number of volumes		: 1
Volume: 1 information:
	Name				: SARVA_BKUP
```

That `Name` is stable; the device node is not. Two identical drives are easy to
mix up — check names, not letters, before you copy into the wrong destination.

## Mount read-only

```sh
sudo mkdir -p /mnt/macdrive
sudo mount -t apfs -o ro,vol=0 /dev/sdc2 /mnt/macdrive
```

- **`ro`** — read-only. Exactly what you want for a backup *source*: no chance of
  writing to the original. (`linux-apfs-rw`'s write support is experimental;
  don't use it here.)
- **`vol=N`** — pick the volume by **0-based index**, in the order `fsapfsinfo`
  lists them. A single-volume container is `vol=0`. If a container has a bootable
  macOS install you'll see extra volumes (e.g. a `... - Data` or an `Update`
  volume) — pick the one whose `Name` you want.

Unmount when done:

```sh
sudo umount /mnt/macdrive
```

## Gotcha 1 — everything is owned by "uid 99"

Files copied off the drive land owned by a bare numeric **`99:99`**, and some
directories (`700`) end up unreadable by your normal user:

```
drwx------ 1 99 99 ... EverythingElse
```

macOS uses uid **99** (`_unknown`) as a placeholder on any volume that has
**"Ignore ownership on this volume"** enabled (the default for external drives).
On the Mac it's dynamically shown as the logged-in user; on Linux there's no such
remapping, so you see the raw `99`. It's a display/ownership artifact, **not
corruption**.

Fix it as you copy by rewriting ownership (mode bits are preserved):

```sh
sudo rsync -a --chown=youruser:youruser /mnt/macdrive/ /dest/
```

Or fix an already-copied tree after the fact:

```sh
sudo chown -R youruser:youruser /dest
```

`sudo` is needed on the read side too, because the `700` files are only readable
by their (nonexistent) owner.

## Gotcha 2 — skip the macOS metadata dirs

Every macOS volume has protected system-metadata directories at its root that are
unreadable (`Operation not permitted`), rebuilt automatically, and useless in a
backup. Exclude them so rsync doesn't spam errors:

```
.Spotlight-V100
.Trashes
.DocumentRevisions-V100
.TemporaryItems
.fseventsd
.DS_Store
```

```sh
sudo rsync -a --chown=youruser:youruser \
  --exclude='.Spotlight-V100' --exclude='.Trashes' \
  --exclude='.DocumentRevisions-V100' --exclude='.TemporaryItems' \
  --exclude='.fseventsd' --exclude='.DS_Store' \
  /mnt/macdrive/ /dest/
```

## Notes

- **x86-only.** The `linux-apfs-rw`/Brother-style driver stack builds on amd64;
  there's no ARM build, so a Raspberry Pi can't be the host for this.
- **Unencrypted volumes only, easily.** If the drive has FileVault enabled you'll
  need to supply the passphrase and the flow is fiddlier — check `fsapfsinfo`
  output for encryption before assuming a plain mount will work.
- The read-only native mount is fast enough that a local copy is limited by the
  disks, not the filesystem driver — the whole point of doing it locally on the
  NAS instead of over Wi-Fi.
