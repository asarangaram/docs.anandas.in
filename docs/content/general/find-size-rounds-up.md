---
title: find -size rounds up, so ranges silently break
tags:
  - find
  - linux
  - gotcha
  - how-to
---

# `find -size` rounds *up* to the unit — size ranges silently return nothing

I wanted every video between 100 MB and 1 GB, so I wrote what looks obviously correct:

```sh
find . -type f -size +100M -size -1G
```

It returned **zero files** — even though the tree was full of 200–800 MB videos. No
error, no warning, just a wrong empty answer. That's the dangerous kind of bug.

## Why it happens

`find -size` measures in **whole units, rounding up**. With `-size -1G`, find takes each
file's size, divides by 1 G, rounds *up* to the next integer, and keeps files where that
rounded value is `< 1`.

A 500 MB file is `0.48 G`, which rounds up to **1**. And `1 < 1` is false — so it's
excluded. In fact *every* non-empty file up to 1 GB rounds up to 1 G, so `-size -1G`
matches essentially **nothing** (only truly 0-byte files round to 0). The same trap hits
`-1M`, `-1k`, any `-size -N<unit>`.

So `-size +100M -size -1G` = "bigger than 100 M **and** smaller than 1 G" collapses to an
empty set, because the second clause excludes everything.

## The fix: use exact bytes with the `c` suffix

The `c` suffix means bytes, and bytes don't round. Compute the thresholds yourself:

```sh
# 100 MiB = 104857600,  1 GiB = 1073741824
find . -type f -size +104857600c -size -1073741824c    # (100 MiB, 1 GiB)
```

Now both bounds are exact and the range works. A tidy way to keep it readable:

```sh
MB=1048576; GB=1073741824
find . -type f -size +$((100*MB))c -size -$((GB))c
```

## Rules of thumb

- **Never use the `k`/`M`/`G` suffixes for a *range*** (`-N` bound). They round up and
  will silently drop everything.
- A single **lower** bound like `-size +100M` is *mostly* fine (it means "rounds up to
  more than 100 M", i.e. roughly > 99 MB) — good enough for a rough filter, but still not
  exact.
- When you need precision or a range, **always use `c` (bytes)** and do the arithmetic.
- Sanity-check any size filter by counting: if a range returns `0`, suspect the rounding
  before you trust it.

Related: [Search for media with find](search_for_media_with_find.md).
