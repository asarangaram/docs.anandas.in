---
title: Super-resolution on the Pi 5 — CPU vs GPU vs Hailo
tags:
  - hailo
  - raspberry-pi
  - super-resolution
  - upscaling
  - onnx
  - dkms
  - vulkan
  - ocr
---

# Super-resolution on the Pi 5 — CPU vs GPU vs Hailo

Notes from getting AI image **upscaling** (super-resolution) to run on a Raspberry Pi 5
edge box that also has a **Hailo-8** accelerator. The goal was to add an "upscale this
image" capability to the compute server, so I tried all three routes it offers — the CPU,
the Pi's own GPU, and the Hailo NPU — and measured them. This is the messy-reality
companion to the general write-up on [upscaling images for print](../../general/upscaling-images-for-print.md).

Short version: **the CPU works but is slow, the Pi's GPU can't do it at all, and the Hailo
works beautifully once you get past a driver gotcha.**

## Route 1 — CPU (ONNX Runtime): works, slow, but honest

Real-ESRGAN exported to ONNX runs on the Pi's four A76 cores with `onnxruntime` — no PyTorch
needed. Two flavours:

- a **compact** model (`realesr-general-x4v3`, ~5 MB) — a few seconds per small image;
- the **heavyweight** `x4plus` (RRDBNet, ~67 MB) — ~1.5 minutes per small image and nearly
  2 GB of RAM, because its memory grows with the image area (~12 GB per megapixel). Anything
  HD-sized has to be tiled or it runs out of memory.

Nothing exotic here — it just works. The compact model is the sensible default.

## Route 2 — the Pi's GPU (Vulkan / ncnn): a dead end

The idea was to use the Pi 5's own GPU via `realesrgan-ncnn-vulkan`. It **compiled fine**,
the GPU **showed up under Vulkan** (`V3D 7.1.10.2`, driver "V3DV Mesa", Vulkan 1.3)… and then
inference **segfaulted** at the moment it tried to build its GPU compute pipeline:

```
Failed to compile MESA_SHADER_COMPUTE prog 5/0 with any strategy.
MESA: error: Failed to compile ... NIR to VIR
vkCreateComputePipelines failed  → Segmentation fault
```

That crash happens *before any model weights are loaded*, so it isn't a model problem — the
Pi's Vulkan driver (V3DV) simply **can't compile the compute shaders** that ncnn needs. The
GPU advertises Vulkan but can't actually run this kind of workload. Abandoned this route;
noted a few things to retry someday (simpler shaders, a newer Mesa, or a different runtime).

## Route 3 — Hailo-8 NPU: the winner, after one driver gotcha

### The gotcha: detected but not usable

`lspci` clearly showed the **Hailo-8** on the bus, and the HailoRT tools were installed — but
there was **no `/dev/hailo0`**, so nothing could use it. The cause was subtle:

- The driver package ships its source under `/usr/src/hailort-pcie-driver`, meant to be built
  by **DKMS** for whatever kernel you're running.
- But **`dkms` itself wasn't installed**, so the kernel module was **never built** for the
  running kernel (a fairly new `6.18.34`). No module → no device node.

The fix was undramatic once the cause was clear:

```sh
sudo apt install dkms
cd /usr/src/hailort-pcie-driver/linux/pcie
sudo make install_dkms          # registers + builds hailo_pci for this kernel
```

After that `/dev/hailo0` appeared, the firmware loaded, and `hailortcli fw-control identify`
returned `Board Name: Hailo-8`. Because it's now under DKMS (plus a PCI auto-load alias and the
`hailort.service`), it **survives reboots and kernel updates** — the exact thing that had
originally broken it.

**Lesson worth keeping:** if a Hailo (or any PCIe accelerator) is visible in `lspci` but has no
`/dev` node, check `dkms status` and whether the kernel *headers* are installed — the module
probably just never got built for your current kernel.

### The pleasant surprise: no compiler needed

I'd braced for the full **Dataflow Compiler** pipeline (needs an x86 machine + a Hailo
Developer Zone login + a calibration image set to quantise a model to a `.hef`). It turned out
the **Hailo Model Zoo publishes pre-compiled `.hef` files on a public S3 bucket** — for
Hailo-8 there are ready super-resolution models:

- `real_esrgan_x2` — RGB, ×2 (a full Real-ESRGAN)
- `espcn_x2 / x3 / x4` — **luminance-only** (a light, fast classic upscaler)

Download the `.hef`, run it — no compiler, no account, no calibration. (You still need the
x86 compiler only if you want a *custom* model, or a native ×4 RGB model, which the Hailo-8
Model Zoo doesn't have — that caps at ×2 for RGB.)

### The catch: fixed input, so you tile on the host

A Hailo `.hef` is a **fixed-shape black box** — `real_esrgan_x2` only ever takes a **512×512**
image and returns 1024×1024. It does **no tiling itself**. So the host CPU does the bookkeeping:
pad small images up to 512 (reflect-pad, not black), or cut big images into 512 tiles with a bit
of **overlap** and throw away the unreliable border of each tile when stitching (otherwise you
get visible seams). The NPU does the heavy maths; the CPU just shuffles tiles.

## The numbers

Same image, upscaled ×4 on the Pi 5 (indicative, single runs):

| Route | Model | Time / image | Host RAM | Notes |
|---|---:|---:|---:|---|
| CPU (ONNX) | compact `x4v3` | ~4 s | ~240 MB | good default |
| CPU (ONNX) | heavy `x4plus` | ~85 s | ~1.9 GB | best quality, slow, RAM-hungry |
| GPU (Vulkan) | — | — | — | **fails** (V3DV can't compile shaders) |
| Hailo NPU | `real_esrgan_x2` (×2) | ~0.5 s | ~170 MB | on-chip; **frees the CPU** |
| Hailo NPU | `espcn` (luma) | ~0.01 s | ~50 MB | near-free; modest quality |

The Hailo `real_esrgan_x2` is **~15× faster than the compact CPU model and hundreds of times
faster than the heavy one** — and, crucially, it runs *on the NPU*, leaving all four CPU cores
free for the other jobs the box is doing. That last point is the real reason to bother with the
accelerator on a shared appliance.

## Two takeaways

1. **The luminance ESPCN models are almost free** and, because OCR works on greyscale anyway,
   they're a great *pre-processing* step to sharpen small text before recognition.
2. **Match the runtime to the hardware.** On the Pi 5 the ordering was the opposite of intuition:
   the general-purpose "GPU" was useless, the CPU was fine-but-slow, and the purpose-built NPU won
   — once a missing `dkms` package stopped hiding it.

See also: [Upscaling images for print](../../general/upscaling-images-for-print.md) for the
plain-English background on how upscaling works and the DPI maths for print sizes.
