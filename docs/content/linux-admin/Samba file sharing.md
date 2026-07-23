---
title: Samba file sharing (SMB)
tags:
  - samba
  - smb
  - cifs
  - file-sharing
  - networking
  - storage
  - mount
  - fstab
---

# Samba file sharing (SMB)

Share a folder over **SMB** so macOS, Linux, and Windows can read/write it over the
LAN. Typical use: expose a mounted data disk (see the *Mount disks* section in
*Setup Data Server*) from a headless box.

!!! note "Tested on"
    Debian 13 / Raspberry Pi OS, **Samba 4.22**. Sharing `/colan_storage` from a
    headless Raspberry Pi 5 to Mac + Linux.

## 1. Install

```bash
sudo apt install samba
```

!!! tip "`smbd` lives in `/usr/sbin`"
    A non-login shell often doesn't have `/usr/sbin` on `PATH`, so `command -v smbd`
    can wrongly say "not found". Check with the full path: `/usr/sbin/smbd --version`.

## 2. Define a share

Append a share block to `/etc/samba/smb.conf`:

```ini
[colan_storage]
   comment = Edge appliance storage
   path = /colan_storage
   browseable = yes
   read only = no
   guest ok = no
   valid users = anandas
   create mask = 0664
   directory mask = 0775
```

Validate the config (prints the effective settings, flags syntax errors):

```bash
sudo testparm -s
```

## 3. Set an SMB password

Samba keeps its **own** password database — the SMB password is **separate from the
Linux login password**, even for the same username. Add the user (interactive; run it
where you can type):

```bash
sudo smbpasswd -a anandas      # prompts for a new SMB password, twice
```

The user must already be a Linux user, and must be listed under `valid users`.

## 4. Start the service

```bash
sudo systemctl enable --now smbd
sudo systemctl restart smbd
systemctl is-active smbd                 # -> active
sudo ss -tlnp | grep ':445'              # smbd listening on 445
```

!!! warning "`smbd` vs `samba-ad-dc`"
    The `samba` package also ships `samba-ad-dc` (Active Directory Domain Controller).
    For plain file sharing you want **`smbd`** (+ `nmbd` for NetBIOS discovery), not the
    AD-DC. Leave `samba-ad-dc` disabled:
    ```bash
    sudo systemctl disable --now samba-ad-dc
    ```

## 5. Access it

=== "macOS"
    Finder → `⌘K` → `smb://192.168.0.105/colan_storage` → log in as `anandas` + the
    SMB password.

=== "Linux"
    Browse `smb://192.168.0.105/colan_storage` in the file manager, or mount it from
    the command line — see **[Mount on a Linux client](#6-mount-on-a-linux-client)** below.

=== "Windows"
    Explorer address bar → `\\192.168.0.105\colan_storage`.

## 6. Mount on a Linux client

This is the **client** side — a Linux box mounting a share the server above exposes.

!!! note "Prerequisite: `cifs-utils` is not installed by default"
    A fresh Ubuntu (tested on **24.04**) has **no** `mount.cifs` helper and no
    `smbclient`, so `mount -t cifs` fails with *"cannot mount ... wrong fs type"* until
    you install them:
    ```bash
    sudo apt update && sudo apt install -y cifs-utils smbclient
    ```

**First, confirm the server is reachable and SMB is up** (445 is the SMB port):

```bash
ping -c2 192.168.0.105
timeout 3 bash -c '</dev/tcp/192.168.0.105/445' && echo "445 open"
```

**List the shares** the server offers (so you know the exact share name to mount):

```bash
smbclient -L 192.168.0.105 -U anandas      # -N instead of -U for guest/anonymous
```

**Mount it** — `uid`/`gid` make the files owned by you, so you can read/write without
`sudo`; `vers=3.0` pins a modern SMB protocol:

```bash
sudo mkdir -p /mnt/colan
sudo mount -t cifs //192.168.0.105/colan_storage /mnt/colan \
    -o username=anandas,uid=$(id -u),gid=$(id -g),vers=3.0
```

It prompts for the **SMB** password (the one set with `smbpasswd -a`, not the login one).

### Persist across reboots (fstab + credentials file)

Keep the password out of `/etc/fstab` by putting it in a root-only credentials file:

```bash
sudo tee /etc/cifs-colan.cred >/dev/null <<'EOF'
username=anandas
password=your-smb-password
EOF
sudo chmod 600 /etc/cifs-colan.cred
```

Add one line to `/etc/fstab`:

```
//192.168.0.105/colan_storage  /mnt/colan  cifs  credentials=/etc/cifs-colan.cred,uid=1000,gid=1000,vers=3.0,_netdev,nofail  0  0
```

Then test without rebooting:

```bash
sudo mount -a
```

!!! tip "`_netdev,nofail` keep boot safe"
    `_netdev` waits for the network before mounting; `nofail` stops a missing/offline
    server from dropping boot into an emergency shell. Always use both for network mounts.

## Gotchas

- **SMB password ≠ login password** — set it explicitly with `smbpasswd -a`.
- **`valid users`** must list the account, or login is refused even with the right password.
- **Permissions still apply**: the Linux user needs real read/write on `path`. Sharing a
  disk owned by another UID means fixing ownership (`chown`) or using `force user`.
- **Firewall**: Raspberry Pi OS ships with no firewall enabled, so SMB (139/445) is
  reachable as-is. On a box with `ufw`/`nftables`, open those ports to the LAN.
- **Discovery**: file browsers find the share via `nmbd`/mDNS; if it doesn't appear,
  connect straight to `smb://<ip>/<share>`.
- **Client needs `cifs-utils`** — `mount -t cifs` on a bare Ubuntu fails until it's
  installed; the error (*"wrong fs type"*) doesn't mention the missing package.
- **`vers=` mismatch**: very old servers need `vers=2.0`/`1.0`; new ones reject `1.0`.
  If a mount hangs or is refused, try pinning `vers=3.0` explicitly.
