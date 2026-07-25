---
title: Why doesn't ufw block my Docker-published ports?
tags:
  - how-to
  - docker
  - ufw
  - firewall
  - security
  - linux
weight: 199310
---

# Why doesn't `ufw` block my Docker-published ports?

You set `ufw default deny incoming` (or an `allow from <LAN>` rule), but a container
started with `-p 8080:80` is **still reachable from everywhere**. `ufw status` looks
correct; the port is open anyway.

## Cause

Docker manages its **own iptables rules**. When you publish a port, Docker adds `DNAT`
and `ACCEPT` rules in the **`DOCKER` chain of the `FORWARD` table**, evaluated **before**
ufw's filtering (ufw lives in the `INPUT` / `ufw-*` chains). Container traffic is
forwarded straight past ufw — so `ufw allow`/`deny` **do not apply** to `-p` published
ports.

A `ufw allow 8080` for such a port is a **no-op**, and deleting that rule later won't
close the port either.

## Fixes

**1. Bind the published port to an interface (the usual fix).** Publish to `127.0.0.1`
(localhost-only) or a specific LAN IP instead of all interfaces:

```yaml
# docker-compose.yml
ports:
  - "127.0.0.1:8080:80"      # only reachable on this machine
  - "192.168.0.10:8080:80"   # only on the LAN interface
```

```
docker run -p 127.0.0.1:8080:80 ...
```

Then front it with a reverse proxy (e.g. nginx) on a **ufw-governed** port if you need
LAN access.

**2. Rules in the `DOCKER-USER` chain** — applied *before* Docker's own accept rules:

```
iptables -I DOCKER-USER -i eth0 ! -s 192.168.0.0/24 -j DROP
```

## Note

Behind home NAT, a `0.0.0.0` Docker port is only reachable from the LAN anyway (nothing
external can route in), so this often doesn't bite until the box gets a direct public
path. Either way: **don't rely on ufw** to gate Docker ports — control it with the
binding.
