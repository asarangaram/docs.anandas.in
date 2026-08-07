---
tags:
  - images
  - upscaling
  - super-resolution
  - real-esrgan
  - printing
  - dpi
  - python
  - uv
  - how-to
---

# Upscaling a small photo for print (and knowing when it's actually big enough)

You have a small photo — say a phone screenshot or a cropped image — and you
want to print it on A4, or just have it larger and sharper. Two separate
questions come up, and it's worth keeping them apart:

1. **How** do you enlarge it? (interpolation vs AI super-resolution)
2. **Is the result big enough** for the paper size you want? (the DPI maths)

## Two ways to make an image bigger — they are not the same

**Interpolation** (Lanczos, bicubic) just spreads the existing pixels over a
larger grid and smooths between them. The picture gets bigger but no new detail
appears — edges go soft and text stays as fuzzy as it was, only larger. It's
instant and needs no model. Good enough when you only need a modest size bump.

**AI super-resolution** (Real-ESRGAN and friends) is different: a neural network
*reconstructs* plausible fine detail — it has learned what sharp edges, text and
texture tend to look like, and paints them back in. On a photo this genuinely
recovers legibility: a signboard that was a blur becomes readable. The catch is
that it is *inventing* detail it thinks was there, so it's reconstruction, not
truth — fine for a photo, not something to trust for forensic detail.

Rule of thumb: **interpolation for a small bump, AI when you need the detail
back.** Doing both and comparing side by side is the quickest way to see whether
the AI pass was worth it for your image.

## The DPI maths: will it print cleanly at A4?

This is the part people skip and then wonder why the print looks soft. Print
sharpness is **pixels ÷ physical inches = DPI**:

- **A4** is 210 × 297 mm = **8.27 × 11.69 inches**.
- **300 DPI** = crisp, magazine quality → needs **2480 × 3508 px**.
- **150 DPI** = acceptable for a photo at arm's length → needs **1240 × 1754 px**.
- Below ~120 DPI you start to see softness/pixelation on paper.

So to check any image: divide its longest side by the paper's longest side in
inches.

> A 321 × 452 px photo printed at A4 → 452 / 11.69 ≈ **39 DPI**. Nowhere near.
> Even doubled (642 × 904) it's only ~77 DPI — fine on screen, still too soft to
> print. A **4× pass** (1284 × 1808) lands at ~155 DPI, which *is* good enough
> for a normal A4 photo print.

**DPI metadata is not resolution.** You can tag a file "300 DPI" and it changes
nothing about the actual detail — it only tells the printer what physical size to
lay the pixels out at. Real sharpness comes from the pixel count, full stop.
Don't chase literal 300 DPI by upscaling 8×+ from a tiny source; past a point the
AI is inventing more than it's recovering and it starts to look plastic.

## The recipe (Python + uv, no system Python)

This uses [`spandrel`](https://github.com/chaiNNer-org/spandrel) to load the
Real-ESRGAN weights — it sidesteps the old `basicsr`/`realesrgan` packages, which
are a dependency headache on modern Python.

```sh
uv venv --python 3.11 .venv
uv pip install --python .venv/bin/python \
    pillow "numpy<2" torch torchvision spandrel
```

Grab a model checkpoint (x2 for a modest bump, x4 for print):

```sh
curl -sL https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth \
    -o RealESRGAN_x4plus.pth
```

```python
import numpy as np, torch
from PIL import Image
from spandrel import ModelLoader

im = Image.open("input.jpg").convert("RGB")

model = ModelLoader().load_from_file("RealESRGAN_x4plus.pth").eval()
t = torch.from_numpy(np.array(im)).permute(2, 0, 1).float().div(255).unsqueeze(0)
with torch.no_grad():
    out = model(t).clamp(0, 1)
arr = (out.squeeze(0).permute(1, 2, 0).numpy() * 255).round().astype("uint8")

# dpi=(300, 300) only sets the print-layout size, not the detail — see above
Image.fromarray(arr).save("output_4x.png", dpi=(300, 300))
```

A 0.3 MP image runs in a few seconds on CPU — no GPU needed. For a plain
interpolation comparison, `im.resize((w*4, h*4), Image.LANCZOS)` is a one-liner.

## Gotchas worth remembering

- **`RuntimeError: Numpy is not available`** — this is torch 2.2 built against
  NumPy 1.x while NumPy 2.x is installed. Pin **`numpy<2`** and it goes away. Easy
  to lose an hour to if you don't recognise it.
- **You can't upscale a picture pasted into a chat.** The tool needs the *file on
  disk* — a preview embedded in a conversation has no path to read pixels from.
  Point it at the real file.
- **AI upscaling can't recover what was never captured.** It reconstructs
  plausible detail; it cannot bring back text or faces the source genuinely
  doesn't contain. Start from the best original you have, not a small re-save.
- **Check the size before printing, not after.** Do the DPI division first —
  it tells you whether you need 2× or 4× before you spend time on the pass.

## See also

- [Super-resolution on the Pi 5 — CPU vs GPU vs Hailo](../embedded/Hailo Extension for RPi 5/Super-resolution on RPi 5 - CPU vs GPU vs Hailo.md)
  — running the same upscaling on an edge box: what worked, what didn't (the Pi's
  GPU can't), and how the Hailo NPU compares once a `dkms` gotcha is sorted.
