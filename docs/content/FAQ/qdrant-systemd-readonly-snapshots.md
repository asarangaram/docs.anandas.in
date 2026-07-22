---
title: How to fix Qdrant "Read-only file system" for snapshots under systemd hardening
tags:
  - how-to
  - qdrant
  - systemd
  - sandboxing
  - linux
weight: 199240
---

# How to fix Qdrant "Read-only file system" for snapshots under systemd hardening

Running Qdrant as a hardened systemd service — `ProtectSystem=strict` plus a single
`ReadWritePaths=` for its storage — makes the whole filesystem read-only except that
one tree. Qdrant then panics at startup, even though storage is configured:

```
Failed to create snapshots temp directory at ./snapshots/tmp:
  ReadOnlyFilesystem ... path: "./snapshots/tmp"
thread 'main' panicked ... status=101
```

## Cause

Qdrant's **snapshots path defaults to `./snapshots`** — *relative to the working
directory*. A systemd unit with no `WorkingDirectory=` runs in `/`, which is
read-only under `ProtectSystem=strict`, so it can't create `./snapshots`. Setting
`QDRANT__STORAGE__STORAGE_PATH` alone is **not** enough — the snapshots path is a
separate setting.

## Fix

Give it an explicit working directory and snapshots path inside the writable tree:

```ini
[Service]
WorkingDirectory=/srv/qdrant
Environment=QDRANT__STORAGE__STORAGE_PATH=/srv/qdrant/storage
Environment=QDRANT__STORAGE__SNAPSHOTS_PATH=/srv/qdrant/snapshots
ProtectSystem=strict
ReadWritePaths=/srv/qdrant
ExecStart=/usr/local/bin/qdrant
```

Create the dirs (owned by the service user), then `systemctl daemon-reload &&
systemctl restart`.

!!! tip "General rule for sandboxed daemons"
    Any service that writes to **relative paths** breaks the moment you add
    `ProtectSystem=strict`. Set an explicit `WorkingDirectory=` inside a
    `ReadWritePaths=` tree, and pin every data / temp / snapshot / log path via
    config so nothing lands in `/` or the read-only install directory. `PrivateTmp=true`
    covers anything that only needs a scratch `/tmp`.
