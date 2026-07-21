---
title: Samba file sharing (SMB)
tags:
  - samba
  - smb
  - file-sharing
  - networking
  - storage
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
    Browse `smb://192.168.0.105/colan_storage` in the file manager, or mount it:
    ```bash
    sudo mount -t cifs //192.168.0.105/colan_storage /mnt/colan \
        -o username=anandas,uid=$(id -u),gid=$(id -g)
    ```

=== "Windows"
    Explorer address bar → `\\192.168.0.105\colan_storage`.

## Gotchas

- **SMB password ≠ login password** — set it explicitly with `smbpasswd -a`.
- **`valid users`** must list the account, or login is refused even with the right password.
- **Permissions still apply**: the Linux user needs real read/write on `path`. Sharing a
  disk owned by another UID means fixing ownership (`chown`) or using `force user`.
- **Firewall**: Raspberry Pi OS ships with no firewall enabled, so SMB (139/445) is
  reachable as-is. On a box with `ufw`/`nftables`, open those ports to the LAN.
- **Discovery**: file browsers find the share via `nmbd`/mDNS; if it doesn't appear,
  connect straight to `smb://<ip>/<share>`.
