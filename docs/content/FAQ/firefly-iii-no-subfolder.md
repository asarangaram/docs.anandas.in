---
title: Firefly III won't run under a sub-folder (reverse-proxy path)
tags:
  - how-to
  - firefly-iii
  - nginx
  - reverse-proxy
  - self-hosted
weight: 199320
---

# Firefly III won't run under a sub-folder (reverse-proxy path)

You try to serve Firefly III behind a reverse proxy at a **path** like
`https://host/firefly/`, alongside other apps on the same domain. Pages load broken —
missing CSS, wrong redirects, links pointing at the domain root.

## Cause

**Firefly III does not support running from a sub-directory.** It builds absolute,
root-relative URLs from `APP_URL`, assuming it lives at the **root of a (sub)domain**.
Under `/firefly/`, its own links and assets resolve to `/…` instead of `/firefly/…`.

## What works instead

- **A dedicated (sub)domain at root** — e.g. `firefly.host`, proxied to the container,
  with `APP_URL=https://firefly.host`. This is the supported layout.
- **Its own port/host** at root (no path prefix), if you'd rather not add a subdomain.

Set `TRUSTED_PROXIES=**` (or your proxy's IP) so Firefly honours `X-Forwarded-*` headers,
and make `APP_URL` match **exactly** how you reach it.

## Takeaway

Path-based reverse proxying (`/app/`) works for many self-hosted apps — but **not**
Firefly III. Give it a subdomain or a dedicated host root.
