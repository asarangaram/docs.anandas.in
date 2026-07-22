---
title: How to run Qdrant on a Raspberry Pi 5 (16 KB memory pages)
tags:
  - how-to
  - raspberry-pi
  - qdrant
  - aarch64
  - jemalloc
  - kernel
weight: 199230
---

# How to run Qdrant on a Raspberry Pi 5 (16 KB memory pages)

Qdrant's prebuilt **aarch64 binary is a musl build**, and its bundled jemalloc is
compiled for **4 KB memory pages**. The Raspberry Pi 5's default kernel
(`kernel_2712.img`) uses **16 KB pages**, so the Qdrant binary aborts immediately:

```
<jemalloc>: Unsupported system page size
memory allocation of 144 bytes failed
... process ... killed, signal SIGABRT
```

There is no aarch64 **gnu** build to fall back to — Qdrant ships aarch64 only as
`-musl`, so switching download variants doesn't help.

## Confirm it's the page size

```bash
getconf PAGE_SIZE      # 16384 on a stock Pi 5; Qdrant needs 4096
uname -r               # ...-rpi-2712 = the 16 KB Pi 5 kernel
```

## Fix: boot the 4 KB-page kernel

The Pi 5 firmware ships both kernels; force the 4 KB one (`kernel8.img`). Add this
under the `[all]` section of `/boot/firmware/config.txt`:

```
kernel=kernel8.img
```

Reboot and verify:

```bash
sudo reboot
# after it returns:
getconf PAGE_SIZE      # 4096  -> Qdrant now starts
```

Almost everything else (Python, most C programs) is page-size agnostic, so the
switch is safe; the 16 KB kernel is mainly a throughput optimisation.

!!! tip "Detect it early in an installer"
    If you script the deployment, fail fast instead of dying at Qdrant:
    ```bash
    if [ "$(uname -m)" = aarch64 ] && [ "$(getconf PAGE_SIZE)" != 4096 ]; then
      echo "Add 'kernel=kernel8.img' to /boot/firmware/config.txt and reboot."; exit 1
    fi
    ```

!!! note "If you must keep 16 KB pages"
    Run Qdrant from its **multi-arch Docker image** (which handles the page size),
    or run it on another host and point clients at it over the network. Building
    Qdrant from source against the system allocator also works but is heavy on a Pi.
