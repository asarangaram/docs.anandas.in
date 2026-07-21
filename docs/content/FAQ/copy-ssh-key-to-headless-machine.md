---
title: How to copy your SSH key to a headless machine
tags:
  - how-to
  - ssh
  - headless
weight: 199230
---

# How to copy your SSH key to a headless machine

You have a long public key on your laptop and need it in `~/.ssh/authorized_keys` on
a new box — but you're at a console where you can't paste, or you want it scripted.

## Easiest: `ssh-copy-id` (when password login still works)

```bash
ssh-copy-id user@host
```

Prompts for the password once, appends your key, and fixes permissions. Done.

## Console-only: serve the key over HTTP and pull it

When you're at the machine's console (no paste) but it's on the LAN, serve the key
from your laptop and `curl` it in — no typing the key:

```bash
# on the laptop, in the folder holding the .pub key
python3 -m http.server 8000
```

```bash
# on the target machine
install -d -m700 ~/.ssh
curl -fsSL http://<laptop-ip>:8000/id_ed25519.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

Stop the `http.server` afterwards.

## Manual, if you must type it

The key must be **one single line**:

```bash
install -d -m700 ~/.ssh
printf '%s\n' 'ssh-ed25519 AAAA... you@laptop' >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

!!! warning "Permissions matter"
    SSH silently refuses keys if permissions are loose: `~/.ssh` must be `700`,
    `authorized_keys` must be `600`, both owned by the user. A key split across multiple
    lines is also rejected — paste/append it as exactly one line.
