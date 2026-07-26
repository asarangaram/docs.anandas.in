---
tags:
  - checksums
  - backup
  - rsync
  - linux
  - how-to
---

# Confirm one folder is a content-superset of another (before deleting the old copy)

You have two copies of a large tree — an **old** one you want to delete and a
**new** one you want to keep — and before you `rm -rf` the old one you need to be
sure every file in it is present, *with identical content*, in the new one. Extra
files that exist only in the new copy don't matter; the question is strictly:

> Is `OLD` ⊆ `NEW`?

## Don't reach for `diff -qr`

`diff -qr OLD NEW` answers a *different* (symmetric) question and does it the
expensive way: it reads **every byte of both sides**. On hundreds of GB that's
slow, and if both folders live on the **same spinning disk** it's pathological —
diff interleaves reads from the two trees, so the drive head thrashes seeking
back and forth instead of streaming.

## Do this instead: hash the old tree, then verify with `sha256sum -c`

`sha256sum -c` reads a checksum list and, for each line, re-hashes the file **at
that path in the current directory** and reports OK / FAILED. Point it at the old
tree's checksums but run it from the *new* tree, and it verifies exactly the
old-tree files against their new-tree counterparts — and touches nothing else.

**1. Hash the OLD tree** (paths come out relative, e.g. `./sub/file`):

```sh
cd /path/to/OLD
find . -type f -print0 | sort -z | xargs -0 sha256sum > /tmp/old.sums
```

`-print0` / `sort -z` / `xargs -0` speak NUL end-to-end, so filenames with
**spaces or newlines** are handled correctly.

**2. Verify against the NEW tree** — same relative paths resolve against `NEW`:

```sh
cd /path/to/NEW
sha256sum -c /tmp/old.sums > /tmp/check.out 2>&1
```

**3. Read only what matters** (ignore the flood of `OK`):

```sh
grep ": FAILED$"            /tmp/check.out   # in both, content DIFFERS  -> inspect
grep "FAILED open or read"  /tmp/check.out   # only in OLD               -> merge in
tail -3                     /tmp/check.out   # sha256sum's own summary
```

| Result line | Meaning | What to do |
| --- | --- | --- |
| `path: OK` | identical in both | safe — old copy is redundant |
| `path: FAILED` | exists in both, bytes differ | a real conflict — judge it |
| `path: FAILED open or read` | missing from NEW | copy it over |

If every line is `OK` (no `FAILED` of either kind), `OLD ⊆ NEW` is proven and the
old copy is safe to delete.

## Why this is cheaper

You hash the old tree **once** and read only the *overlapping* files from the new
tree — never the files that exist solely in the new copy. And each side is read
in **one sequential pass**, which is far kinder to a single disk than diff's
interleaved reads.

## Bonus: it hands you the merge list for free

The `FAILED open or read` lines *are* the set of files missing from the new copy.
Bring them in additively — copying only what's absent, never overwriting the
newer copies — with:

```sh
rsync -av --ignore-existing /path/to/OLD/ /path/to/NEW/
```

`--ignore-existing` skips any path already present in `NEW`, so it can't clobber
the files that came back `OK` or the ones you resolved as conflicts.

## Notes

- Use `sha256sum`, not `cksum`: `cksum` is a 32-bit CRC (fine for catching
  accidental corruption, but weak); SHA-256 makes a matching hash as trustworthy
  as a byte-for-byte compare, and the disk read — not the hashing — is the
  bottleneck anyway.
- `sha256sum -c` reads paths **relative to the current directory**, so `cd` into
  the tree you're verifying and generate the list with `find .` (relative), not
  absolute paths.
- To watch progress live, see [stdbuf](stdbuf-line-buffering.md) — `sha256sum`
  block-buffers its output when redirected to a file, so a naive `wc -l` on the
  output looks frozen.
