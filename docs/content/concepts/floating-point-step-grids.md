---
title: Floating-point step grids stall
---

# Floating-point step grids stall

A discrete "grid" of values — zoom stops at 20 %, 40 %, 60 %, 80 %, 100 %… — plus
a *next step / previous step* control is a common little UI. Build the grid in
floating point and it can quietly refuse to move at one particular value. The
button looks dead even though there is obviously a step to go to.

## What happens

Say zoom is stored as a scale factor (a `double`) and the stops are computed as
`k * 0.2`. The catch: **0.2 has no exact binary representation** (the same way ⅓
has none in decimal), so the arithmetic drifts by a hair:

```
3 * 0.2 = 0.6000000000000001   // not 0.6
7 * 0.2 = 1.4000000000000001   // not 1.4
```

Now "zoom out" wants the largest stop **strictly below** the current scale. If
the current scale is `0.6000000000000001`, the candidate it computes for the
step below comes out as `0.6000000000000001` too — so the test
`candidate < current` is **false** (they're equal within the float noise) and it
hands back the same value. Nothing changes. It's stuck at 60 % even though 40 %
plainly exists.

## The fix: do the grid maths in integers

Never build or compare the grid in floating point. Convert to a whole-number
percent, step by whole numbers, and turn it back into a scale only at the very
end:

```dart
final percent      = (scale * 100).round();        // 0.6000…1 -> 60   (exact int)
final prevPercent  = ((percent - 1) ~/ 20) * 20;   // largest multiple of 20 below 60 -> 40
final zoomOutScale = prevPercent / 100;            // -> 0.4
```

Integers are exact, so "the step below" is *always* genuinely smaller — no
epsilon, no equality trap, no stall.

## The general rule

Whenever you have a **discrete set of values** and you search for the
next/previous one, snap to the nearest, or test equality — don't represent or
accumulate that set in floating point. Decimal fractions like 0.1 / 0.2 / 0.3
aren't exact in binary, and the sub-epsilon errors break `<`, `==`, and
snap-to-step. Keep the steps as **integers or fixed-point** and convert to float
only at the boundary where you actually need it.

!!! tip "Symptom to recognise"
    An increment/decrement button that does nothing **at one specific value**
    while working everywhere else is almost always this — a comparison against a
    float that's a whispered epsilon away from where you think it is.
