---
title: Home NAS with an old desktop
tags:
  - nas
  - samba
  - smb
  - cifs
  - storage
  - mount
  - fstab
  - recycle
---

# Home NAS with an old desktop

Turn a spare desktop + a USB disk into a simple LAN file store: format the disk,
share **one folder** over Samba, add a server-side recycle bin, then mount it on a
laptop so it's just there after boot.

!!! note "Tested on"
    Server: Ubuntu 24.04 on an OptiPlex (`udesktop`, `192.168.0.104`) with a 4 TB WD
    drive in a USB 3.0 enclosure. Client: Ubuntu laptop. Samba 4.19.

This page is the **assembly + the non-obvious lessons**. For the step-by-step Samba
server config and the generic client mount, see *Samba file sharing (SMB)*; for
mounting local disks on the server, see *Setup Data Server*.

## 1. Prepare the disk

Check what the OS sees, and confirm which port speed the enclosure negotiated —
a USB 3.0 drive dropped onto a USB 2.0 port is ~10× slower.

```bash
lsblk -o NAME,SIZE,TYPE,FSTYPE,TRAN,MODEL   # find the disk (e.g. sdb, TRAN=usb)
lsusb -t                                    # 5000M = USB 3.0, 480M = USB 2.0
```

!!! warning "Check the link speed before you commit"
    A blue/`SS` port is usually USB 3.0. `lsusb -t` showing the disk under a `480M`
    bus means it's on a USB 2.0 port — move the cable before formatting, or the NAS
    is stuck at ~40 MB/s forever.

Confirm it's blank, then lay down a GPT table + one ext4 partition:

```bash
sudo wipefs /dev/sdb                        # empty output = no existing signatures
sudo parted -s /dev/sdb mklabel gpt
sudo parted -s -a optimal /dev/sdb mkpart primary ext4 0% 100%
sudo mkfs.ext4 -L nas4t -m 0 /dev/sdb1      # -m 0: no root-reserved blocks on a data disk
```

Mount it on the server by UUID with `nofail` so a missing disk never hangs boot:

```
UUID=<uuid>  /disks/nas4t  ext4  defaults,nofail,x-systemd.device-timeout=10  0  2
```

## 2. Share one folder, not the whole disk

Point the Samba share at a **subfolder**, so anything else on the disk stays off the
network:

```
/disks/nas4t/                ← full disk (private, server-local only)
└── AanaOhana/               ← the ONLY folder exposed over SMB
```

```ini
[AanaOhana]
   comment = AanaOhana shared folder
   path = /disks/nas4t/AanaOhana
   browseable = yes
   read only = no
   guest ok = no
   valid users = anandas
```

(Install Samba, set the SMB password with `smbpasswd -a`, disable `samba-ad-dc`, and
start `smbd`/`nmbd` — see *Samba file sharing (SMB)* for the full sequence.)

## 3. A recycle bin (server-side trash)

By default an SMB delete is **permanent** — there is no undo. Samba's `recycle` VFS
module intercepts deletes and moves files into a hidden folder instead. Add to the
share block:

```ini
   vfs objects = recycle
   recycle:repository = .recycle/%U
   recycle:keeptree = yes
   recycle:versions = yes
   recycle:touch = yes
   recycle:exclude = *.tmp *.temp *.o *.obj *~ ~$*
   recycle:maxsize = 0
```

Deleted files land in `.recycle/<user>/…` on the share, with their folder path
preserved (`keeptree`). To restore, browse into the hidden `.recycle` folder and drag
the file back out.

!!! warning "It catches files, not empty folders"
    - Delete a **file** → recycled. ✅
    - Delete a **folder with files** → the files are recycled under
      `.recycle/<user>/<Folder>/`. ✅
    - Delete an **empty folder** → gone, not recoverable (but it held nothing). ❌

    Also: `%U` puts each user's deletions in their own subfolder — look in
    `.recycle/<user>/`, not `.recycle/` directly. And the bin grows forever until you
    empty it (`maxsize = 0` = no cap).

## 4. Deleting over the share skips the desktop Trash

On a mounted SMB share, the file manager shows *"Cannot move file to trash, do you
want to delete immediately?"*. This is **normal**, not a fault: the desktop Trash is a
local-filesystem feature, and a network mount has no local trash. With the recycle bin
(step 3) in place, clicking **Delete** still isn't truly permanent — the file goes to
the **server-side** `.recycle`, not the desktop trash.

## 5. Mount on the client — pick ONE model

The big lesson. There are two sane ways to mount this on a laptop, and **they are
mutually exclusive** — trying to have both is where all the pain came from.

| | Auto-mount (autofs) | Removable-disk (gvfs eject) |
|---|---|---|
| Behaviour | Always mounted, remounts on access | Click to connect, eject to disconnect |
| fstab keys | `x-systemd.automount` | `users`, `x-gvfs-show`, `noauto` |
| Sidebar eject | — | yes |
| At boot | mounts automatically | not mounted until clicked |

!!! danger "Auto-mount and the eject button fight over the mount point"
    Combining `x-systemd.automount` with `x-gvfs-show` looks like "best of both" but
    isn't: autofs remounts the share the instant *anything* touches the folder —
    including the file manager merely drawing the sidebar. So the GUI **Reconnect**
    click hits an already-mounted point and fails with
    `mount error(16): Device or resource busy`, while **eject** on a system mount fails
    with `must be superuser to unmount`. Pick one model and stop there.

For a personal machine, the simplest choice wins: a **plain per-user mount** in your
home folder that appears at boot, no sidebar theatrics.

```
//192.168.0.104/AanaOhana  /home/anandas/nas/aana_ohana  cifs  \
  credentials=/etc/samba/credentials/aanaohana,uid=1000,gid=1000,\
  file_mode=0600,dir_mode=0700,iocharset=utf8,_netdev,nofail  0  0
```

- `credentials=…` — a root-only (`chmod 600`) file holding `username=`/`password=`,
  keeping the password out of `/etc/fstab`.
- `uid`/`gid=1000`, `dir_mode=0700` — owned by and private to you.
- `_netdev,nofail` — wait for the network; never stall boot if the NAS is offline.

Verify it's wired into boot without actually rebooting:

```bash
sudo mount -a
systemctl show home-anandas-nas-aana_ohana.mount -p WantedBy   # → remote-fs.target
```

`WantedBy=remote-fs.target` is the proof: that target is what mounts network
filesystems at boot.

## 6. Who is the "user"? (the identity model)

The confusing bit when the laptop login and the Samba login share a name:

- **Samba authenticates against the _server's_ account database.** The client sends a
  username + password, checked against `smbpasswd` accounts **on the server**. The
  local laptop user is irrelevant to that check.
- A Samba user is **backed by a Unix user on the server** — to log in as `foo`, a Unix
  `foo` must exist on the server (it can be a `nologin` service account created just
  for Samba).
- **Real file ownership is decided on the server.** Files written through the share are
  owned by the server-side Unix user the Samba session maps to — regardless of which
  machine or which local user created them.
- **`uid=`/`gid=` on the client mount is only cosmetic** — it relabels how ownership
  *looks* locally; it changes nothing on the server. A CIFS mount maps the whole mount
  to one uid/gid, so it can't show "whoever is logged in" as the owner.

## Gotchas

- **USB 2.0 trap** — always `lsusb -t` after plugging in; a NAS silently stuck at
  `480M` is miserable.
- **Recycle bin ≠ backup** — it only catches SMB deletes (not overwrites, not
  server-local deletes), and empty folders vanish. It grows until emptied.
- **Don't mix auto-mount with GUI eject** — the `Device or resource busy` /
  `must be superuser` errors come straight from that combination.
- **Credentials file needs to be reachable by whoever mounts** — a boot mount runs as
  root, so root-only `600` is fine. Only if a *user* triggers the mount (gvfs) do the
  file and its parent directory need to be group-readable by that user.
- **`nofail` everywhere** for network and removable mounts, or an absent NAS drops boot
  into an emergency shell.
