---
title: How to fix the ghostty unknown-terminal-type error over SSH
tags:
  - how-to
  - ssh
  - ghostty
  - terminal
weight: 199200
---

# How to fix `xterm-ghostty: unknown terminal type`

## The problem

You SSH from a **Ghostty** terminal into a fresh server and see:

```text
'xterm-ghostty': unknown terminal type.
```

Anything that relies on terminfo — `clear`, `less`, `vim`, `top`, `tmux` —
misbehaves. Cause: your local `TERM=xterm-ghostty`, but the remote host has no
terminfo entry for it (Ghostty is newer than the remote's ncurses database).

## The fix: copy the terminfo to the remote

Your **local** machine already has the `xterm-ghostty` terminfo. Export it and pipe
it into the remote's `tic` compiler — it installs into the remote user's
`~/.terminfo`, no root needed:

```bash
infocmp -x xterm-ghostty | ssh user@host 'tic -x -'
```

Reconnect and the error is gone. A harmless warning like *"older tic versions may
treat the description field as an alias"* is fine — it still installs.

## Quick one-off workaround

If you just need the current session to behave and don't want to install anything:

```bash
TERM=xterm-256color ssh user@host
```

Ghostty is compatible enough with `xterm-256color` for most things; the terminfo copy
above is the proper, permanent fix.
