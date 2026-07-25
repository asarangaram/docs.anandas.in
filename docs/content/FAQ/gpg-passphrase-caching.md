---
title: Why does pass/GnuPG prompt for the passphrase every time (or never)?
tags:
  - how-to
  - gpg
  - pass
  - security
  - linux
weight: 199300
---

# Why does `pass`/GnuPG prompt for the passphrase every time (or never)?

`pass` (and any `gpg` decrypt) either **nags for the passphrase on every entry**, or
**never asks at all** — and it isn't obvious which knob controls which. The trick: there
are **two independent caches**, with very different security implications.

## The two caches

| Cache | Where it lives | Controlled by |
| ----- | -------------- | ------------- |
| **External** | the desktop **keyring** (GNOME/libsecret) — **on disk, persistent** | `no-allow-external-cache` |
| **Agent** | `gpg-agent` in **RAM** — cleared on reboot/logout | `default-cache-ttl` / `max-cache-ttl` |

- If pinentry's *"save in keyring"* is allowed/ticked, the passphrase is written to the
  **keyring on disk** — so gpg **never asks again**, even across reboots. Convenient, but
  anyone who can read your files/keyring can then decrypt without the passphrase.
- If you disable *all* caching (`default-cache-ttl 0`), gpg asks **every single time** —
  secure, but painful for bulk operations.

## The balance you usually want

Keep the passphrase **off disk**, but allow a **short in-RAM cache** so a burst of
commands doesn't re-prompt:

```
# ~/.gnupg/gpg-agent.conf
default-cache-ttl 300     # remember for 5 min of activity
max-cache-ttl 1800        # ...up to 30 min total
no-allow-external-cache   # NEVER persist to the keyring/disk
```

```
gpgconf --kill gpg-agent   # reload
```

Now you type it once, run a batch of `pass`/`gpg` commands with no nagging, and it's
forgotten after a few minutes — and **never written to disk**, so a stolen file/keyring
copy can't decrypt without the passphrase in your head.

> The security-critical line is **`no-allow-external-cache`** (no on-disk persistence).
> The TTLs are pure convenience — a RAM cache clears on reboot and never touches disk.

**Also:** when a pinentry dialog offers *"Save in keyring"*, leave it **unchecked** to keep
the passphrase required.
