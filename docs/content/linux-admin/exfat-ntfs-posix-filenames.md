---
tags:
  - exfat
  - ntfs
  - udf
  - filesystem
  - rsync
  - symlinks
  - macos
  - linux
  - cross-platform
  - how-to
---

# Why exFAT and NTFS choke on Unix files (illegal characters + symlinks)

You mirror a Linux or macOS tree onto a portable disk that's formatted **exFAT**
(the usual choice so it reads on any machine), and `rsync` spits out a wall of
errors. Look closely and they're all one of **two** kinds:

```
rsync: [receiver] mkstemp ".../22-04-18, 6:17 PM Office Lens.pdf.Z4qEqF" failed: Invalid argument (22)
```
```
skipping non-regular file "project/ios/.symlinks/plugins/share_plus"
```

Neither is a bug in your script. Both come from the same place: **exFAT and
NTFS are DOS-lineage filesystems**, and they disagree with Unix about what a
valid file even is.

## The root cause

FAT / exFAT / NTFS all inherit two DOS-era rules that POSIX filesystems don't
have:

1. **A set of forbidden filename characters.** These are illegal in a filename:

    ```
    "   *   /   :   <   >   ?   \   |
    ```

    plus the control characters `0x00`–`0x1F`. A POSIX filesystem (ext4, XFS,
    btrfs, APFS, HFS+, UDF) forbids only **`/`** and the **NUL** byte — *every*
    other byte is legal. So a perfectly ordinary Unix/mac file like
    `Meeting 6:17 PM.pdf` or `report?draft.txt` simply **cannot exist** on
    exFAT. `rsync` tries to create it and the kernel rejects the name with
    `EINVAL` → `Invalid argument (22)`.

2. **No POSIX metadata.** exFAT stores no ownership, no Unix permission bits, and
    **no symlinks / special files**. When the destination can't hold a symlink,
    `rsync` prints `skipping non-regular file` and moves on — so those files are
    silently *missing* from the backup. (This is also why exFAT backup scripts
    use `rsync -rt` instead of `-a`: `-a` implies `-l`/`-o`/`-p`, which exFAT
    can't honour.)

## NTFS is **not** an escape

A common instinct is "exFAT is limited, I'll use NTFS instead." It doesn't help:
**NTFS forbids the exact same characters** (`: ? * " < > \ |` are reserved by
Win32). NTFS *can* store symlinks and ACLs in principle, but on Linux the
`ntfs-3g` driver only creates symlinks in a special interop mode, and the
character ban is absolute regardless. If your problem is Unix filenames, NTFS
buys you nothing.

## How each filesystem compares

| Filesystem | `: ? *` in names | Symlinks / perms | macOS native | Linux native |
|---|---|---|---|---|
| **exFAT** | ❌ rejected | ❌ none | ✅ read-write | ✅ read-write |
| **NTFS** | ❌ rejected | ~ (interop only) | read-only\* | ✅ read-write |
| **ext4** | ✅ | ✅ | ✗ (needs driver) | ✅ |
| **APFS / HFS+** | ✅ | ✅ | ✅ | ✗ / read-only |
| **UDF** | ✅ | ✅ | ✅ read-write | ✅ read-write |

\* macOS writes NTFS only with third-party drivers.

The pattern is clear: the moment you need `:`/`?` in names *or* real symlinks,
you need a **POSIX** filesystem — the only question is which one both of your
operating systems can mount.

## Diagnosing the noise (it's smaller than it looks)

`rsync --info=progress2` draws its progress bar with **carriage returns** (`\r`),
so a log can look like thousands of error lines when it's really a handful of
real errors buried in one giant redrawing line. Split on `\r` before you count:

```sh
tr '\r' '\n' < backup.log | grep -E 'Invalid argument|skipping non-regular' | sort | uniq -c
```

That usually turns "≈1000 errors" into "47 illegal-character files and a few
hundred skipped symlinks."

## The fix — pick a POSIX filesystem by who needs to mount it

- **Linux only (or Linux-primary):** use **ext4**. Rock-solid and journaled.
  A Mac can read it with a helper (`fuse-ext2` read-only, or a paid driver),
  but if the Mac only browses the backup, read-only is fine.

- **macOS *and* Linux, both native, no extra software:** use **UDF**. It's the
  one filesystem both mount **read-write out of the box** and it's POSIX, so
  `:`/`?` and symlinks just work. Then switch `rsync` back to `-a` and the
  previously-skipped files transfer.

### UDF gotchas worth knowing

- **Format the whole raw device, not a partition** (`mkudffs ... /dev/sdX`, not
  `/dev/sdX1`) — macOS mounts whole-disk UDF reliably but is finicky about UDF
  inside a partition.
- **`--blocksize=512`** must match the drive's logical sector size, or macOS
  won't mount it.
- **No journaling** — a power cut mid-write can corrupt the volume. Fine for a
  backup mirror; think twice for primary storage.

```sh
sudo apt install udftools
sudo wipefs -a /dev/sdX
sudo mkudffs --media-type=hd --blocksize=512 --lvid=mydisk --vid=mydisk /dev/sdX
```

## Notes

- The character limits are about the **filesystem**, not the OS — a Linux box
  writing to an exFAT stick hits the same wall a Windows box would.
- Related, and a separate trap when moving names between filesystems: Unicode
  **normalization** differs (APFS decomposes, exFAT stores as-given), so names
  can *look* identical yet not match — see [Japanese filenames](../general/Japanese filenames.md).
- Going the other direction (reading a Mac disk on Linux) has its own quirks —
  see [Mount an APFS drive on Linux](mount-apfs-on-linux.md).
