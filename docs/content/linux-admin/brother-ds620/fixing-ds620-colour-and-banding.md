---
tags:
  - scanner
  - image-processing
---

# Fixing the DS-620's yellow cast and vertical banding

Scans from the DS-620 came out **yellowish** — a scan of plain white paper was
visibly warm. Measuring the channels (rather than eyeballing) confirmed it: the
**blue channel sat well below red and green**. A global white balance pulled the
paper back to true white and fixed the cast.

But that wasn't the whole story. Even after white-balancing, there were faint
**vertical bands** of slightly different colour running down the page — not a
single global tint, but *column-to-column* variation.

## Why: an uncalibrated CIS sensor

The DS-620 uses a **CIS** sensor — one row of sensor elements spanning the page
width, each reading its own column. Those elements differ slightly in gain and
colour, and the scanner corrects for it using a **calibration** taken against a
reference sheet. That calibration was never done here (the little calibration
sheet that ships with it was long lost), so every column carried its own tint →
vertical banding.

## The insight: a white sheet *is* the calibration reference

You don't need the special sheet. **A scan of plain white paper is the
reference.** If the paper is uniform, any column-to-column difference in that
scan *is* the sensor's error — so you can measure and cancel it.

This is a **flat-field correction**:

1. Scan a sheet of **pure white paper** once.
2. For each sensor **column**, measure its average R/G/B on that white scan.
3. Compute a **per-column gain** that maps every column to the same white.
4. Multiply every future scan by those gains → even illumination, **banding
   gone**. (A global white balance is the fallback when no map exists.)

## Doing it with the tool

```sh
./scan _white.jpg                 # scan a blank white sheet
./correct --calibrate _white.jpg  # build the flat-field map (per-column gains)

./correct scan.jpg                # every later correction applies the map
```

Re-run the calibration if scans drift over time.

## Bonus: black & white belongs in software, not the scanner

The DS-620's hardware "LineArt" thresholds using the **raw, uneven** sensor
data, giving patchy text. Scanning in **Gray**, applying the flat-field
correction so illumination is even, *then* adaptive-thresholding in software
gives clean bilevel and keeps faint pencil strokes the hardware would drop.

Related: [Installing the DS-620 on Linux](installing-ds620-on-linux.md).
