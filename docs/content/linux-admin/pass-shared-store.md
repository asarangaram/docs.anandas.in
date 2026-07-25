---
title: A shared, multi-device password store with pass + git
tags:
  - pass
  - gpg
  - git
  - security
  - linux
---

# A shared, multi-device password store with `pass` + git

`pass` stores each secret as a **GPG-encrypted file** in a **git repo**. That combination
lets you share one password store across all your machines — *if* you're clear about what
is safe to sync and what must be guarded.

## The mental model: vault vs. key

- The **git repo** holds only **encrypted blobs**. It's safe to host **anywhere** — a
  private git server, a mirror, even a public host — because without the key it's noise.
- The **GPG private key + its passphrase** are the only things that decrypt it. Guard them
  **separately**, and **never** commit them to the repo.

Sync the vault freely; protect the key like a crown jewel. (Same guarantee a cloud
password manager gives: the encrypted vault syncs everywhere, the master password stays in
your head.)

## Setup (first machine)

```
# 1. a dedicated GPG key for the store
gpg --quick-generate-key "You (pass shared)" default default 0

# 2. init the store to that key and put it in git
pass init <KEY_FINGERPRINT>
pass git init
pass git remote add origin <git-remote-url>
pass git push -u origin main
```

For an **off-site copy**, mirror the git repo to a second host — the blobs are encrypted,
so any git host is safe.

## Every other machine

Because the store lives at the **default location**, plain `pass` just works — no wrapper,
no env vars, nothing in your shell config hinting it exists:

```
gpg --import <key-export>                       # the SAME key
git clone <git-remote-url> ~/.password-store    # local dir name is free; remote name irrelevant
pass show some/entry                            # enter the passphrase
```

## Daily use

```
pass insert some/entry     # auto-commits locally
pass git pull              # before edits
pass git push              # after edits -> your remote(s)
```

`pass` auto-commits on every change; **push/pull is manual** — or automate it (a git hook,
or a small `pass git pull --rebase && pass git push` on a timer).

## Two things people get wrong

- **Passphrase prompts** — by default you may get asked on *every* entry, or never. See
  [Why does pass/GnuPG prompt every time (or never)?](../FAQ/gpg-passphrase-caching.md):
  keep the passphrase off disk, allow a short RAM cache.
- **Merging a machine's existing store** — you can't `git merge` it in, because its files
  are encrypted to a **different key**. Decrypt each old entry and `pass insert` it into the
  shared store (re-encrypts to the shared key). Watch for entries that exist on both with
  **different values** — those diverged and need a manual decision.

## Backing up the key (the part that isn't in git)

The repo is backed up by *being* in git. The **key** needs its own backups, kept **off**
the machines:

```
gpg --armor --export-secret-keys <KEY> > pass-key.asc     # passphrase-encrypted
gpg --export-ownertrust > ownertrust.txt
```

Keep those on **offline media** (a USB), and — as an off-site second copy — in an
**AES-256 archive** in the cloud:

```
7z a -p -mhe=on pass-key.7z pass-key.asc ownertrust.txt   # AES-256 + encrypted filenames
```

The passphrase (and the archive password) live **only in your memory / on paper** — never
digital, and never inside `pass` itself (that would be circular).
