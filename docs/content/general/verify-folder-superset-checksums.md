---
tags:
  - checksums
  - backup
  - rsync
  - jdupes
  - deduplication
  - exiftool
  - photos
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

## Gotcha: "same size + same date" is NOT "same content"

`sha256sum -c` compares bytes, so it catches a class of duplicates a faster
metadata check silently gets wrong. Real cases that bit me:

- A SQLite database (a Calibre e-book library) looked **newer** on the copy I
  planned to keep — but it was **empty** (0 books), while the "old" copy held all
  1,388. Keeping by timestamp would have thrown the real library away.
- Two versions of a photo had the **exact same byte size** but different content.
  A size-only comparison calls them identical; the hash does not.
- Worse: I'd earlier run `touch -r old new` to tidy up mismatched timestamps —
  which made two genuinely *different* files share the same size **and** mtime.
  Any tool trusting size+mtime (including rsync's default quick check) would now
  treat them as identical and skip them.

The rule: **for anything irreplaceable, trust the checksum, not the timestamp or
size.** Use metadata only to *narrow* the candidates, never to decide a deletion.

## Scope cheaply first, verify by content second

Hashing terabytes is slow, so don't hash everything blindly — a fast metadata pass
finds the *candidates*, and the content check confirms only those:

1. **`rsync -avni OLD/ NEW/`** (dry-run, itemize) — size+mtime only, no reads.
   `>f+++++++++` = missing from NEW; `>f.st.....` / `>f..t.....` = exists but
   differs. That's your shortlist.
2. **`sha256sum -c`** the shortlist (or the whole tree, if small) to confirm which
   are *really* identical vs. a size coincidence.

You read the tree once to hash, but only have to *think* about the handful of files
metadata flagged as different.

## When the folders are reorganized: anchor the `-c`, or go path-independent

`sha256sum -c` matches by **relative path**. If the two trees hold the same files
under a **different folder layout**, the path-based check reports everything as
missing even though the content is identical. Two ways out:

- **Anchor at the matching sub-level.** If `A/Datewise/…` mirrors
  `B/nalini/DateWise/…`, generate the sums from `A/Datewise` and run `-c` from
  `B/nalini/DateWise` — now the relative paths line up (only the top folder
  name/case differed).
- **Compare by content hash, ignoring paths entirely** — check the old hash set is
  a subset of the new:
  ```sh
  cd OLD; find . -type f -print0 | sort -z | xargs -0 sha256sum | awk '{print $1}' | sort -u > /tmp/old.h
  cd NEW; find . -type f -print0 | sort -z | xargs -0 sha256sum | awk '{print $1}' | sort -u > /tmp/new.h
  comm -23 /tmp/old.h /tmp/new.h    # hashes in OLD but not NEW = would be lost
  ```
  Empty output → every old file's content exists somewhere in NEW, wherever it was
  filed.

## Or use `jdupes` — but know its cost

For path-independent dedup, [`jdupes`](https://github.com/jbruchon/jdupes) finds
byte-identical files across trees and can delete them in place:

```sh
# keep the master (first param), delete duplicates only from the copy:
jdupes -r -O --isolate -d -N MASTER COPY
```

- `-O` (paramorder) → the first path listed is the preferred **keeper**.
- `--isolate` → only match *across* the given paths, never within one, so the copy
  can't lose a file the master doesn't also have.
- `-d -N` → delete duplicates without prompting, keeping the preferred one.
- jdupes always keeps **one** copy of each identical set, so no unique content is
  ever lost — the only question is *which* copy survives (that's what `-O` controls).

Trade-off vs. a plain hash pass: jdupes verifies matches with a **final
byte-for-byte comparison** that *re-reads* the matched files — roughly 1.5× the I/O
of hashing each side once. On a spinning disk full of small photos that's the
difference between a couple of hours and an overnight run. Use the hash-set method
when you just need the answer; use jdupes when you want it to do the deletion too.

Note: jdupes hides its progress bar when its output isn't a terminal, so
`jdupes … 2>&1 | tee log` shows nothing until the end. Send results to the file but
leave stderr on the terminal instead: `jdupes … > jdupes.log` — the live progress
stays visible. (To watch a run that's *already* piped, sample bytes read from
`/proc/$(pgrep -x jdupes)/io`.)

## Photos: hash the pixels, not the file, to catch "same image, different EXIF"

A whole-file checksum (and jdupes, and any byte compare) treats two copies of the *same
photo* as different the moment their metadata differs by one byte — a rewritten
timestamp, a stripped GPS tag, an orientation flag. So a de-dup by file hash leaves
thousands of near-identical photos behind. To compare only the **image data**, strip the
metadata on the fly and hash what's left:

```sh
pixhash() { exiftool -all= -o - "$1" 2>/dev/null | sha256sum | cut -d' ' -f1; }
[ "$(pixhash a.jpg)" = "$(pixhash b.jpg)" ] && echo "same image (metadata aside)"
```

`exiftool -all= -o -` writes a metadata-stripped copy to stdout without touching the
original; the hash of that is stable across EXIF-only differences. This is what turns
"same size, same day, different bytes" from an unresolved conflict into a confident
drop-the-duplicate.

Confirming the difference *is* only metadata: `cmp` the two files and check the first
differing byte — if it's near the front (in the EXIF header) and the pixel hashes match,
the images are identical and only the tags differ.

## Gotcha: exiftool's own `*_original` backups

When exiftool edits a file in place without `-overwrite_original`, it renames the
pre-edit copy to `name.ext_original` (e.g. `IMG_1234.jpg_original`). After a big metadata
pass you can be left with thousands of these. They're **redundant only if the edited
sibling still exists** — check before deleting:

```sh
find . -type f -name '*_original' | while IFS= read -r f; do
  [ -e "${f%_original}" ] || echo "ORPHAN: $f"   # no sibling -> the only copy, keep it
done
```

Since exiftool only writes them on *metadata* edits, each `_original` is pixel-identical
to its sibling — safe to bulk-delete once you've confirmed none are orphans.

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
