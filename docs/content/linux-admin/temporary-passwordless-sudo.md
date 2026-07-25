---
title: Temporarily make sudo passwordless (and undo it)
tags:
  - sudo
  - security
  - linux
---

# Temporarily make sudo passwordless (and undo it)

During a hands-on admin session — especially driving a machine over SSH with lots of
root commands — retyping the sudo password every few minutes is painful. A quick
`NOPASSWD:ALL` drop-in removes the prompt for the session; **remove it when done.**

🛑 **Security risk.** This lets *any* `sudo` run without a password. Only on a machine
whose access is restricted and trusted, and **always revert** afterwards.

## Make it passwordless

```bash
echo "$USER ALL=(ALL) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/99-$USER-nopasswd \
  && sudo chmod 440 /etc/sudoers.d/99-$USER-nopasswd \
  && sudo visudo -c
```

- A **drop-in** under `/etc/sudoers.d/` (never edit the main `/etc/sudoers`).
- `chmod 440` — sudo ignores the file if permissions are looser.
- `visudo -c` **validates** all sudoers files; if it doesn't report OK, fix/remove the
  file before relying on it (a broken sudoers can lock you out).

## Restore the password prompt

```bash
sudo rm /etc/sudoers.d/99-$USER-nopasswd
```

## Verify which state you're in

```bash
sudo -n true && echo "passwordless is ACTIVE" || echo "password is required (restored)"
```

## See also

For a **permanent, command-scoped** version — letting a specific script or command run
without a password (e.g. a deploy script restarting nginx) rather than a blanket toggle —
see [Running a script without password](runscript_without_password.md).
