---
tags:
  - shell
  - buffering
  - debugging
  - linux
  - how-to
---

# `stdbuf` — why a piped/redirected command's output looks "frozen", and how to unfreeze it

A long-running command whose output you redirect to a file (or pipe into
another tool) can look **stuck**: you watch the file with `wc -l` or `tail`, and
the count sits still for ages, then suddenly jumps by hundreds of lines. The
command isn't hung — its **stdout is block-buffered**.

## The cause: buffering depends on where stdout points

The C standard library picks a buffering mode by looking at stdout:

- **To a terminal (tty):** *line-buffered* — every `\n` is flushed immediately.
- **To a file or pipe (not a tty):** *fully (block) buffered* — output is held in
  a ~4–8 KB buffer and only written when the buffer fills (or the program exits).

So the exact same command behaves differently the moment you add `> file` or
`| something`:

```sh
sha256sum *            # on screen: lines appear one by one
sha256sum * > out.txt  # into a file: out.txt stays empty, then jumps in chunks
```

Watching `wc -l out.txt` during the second form is misleading — the lines exist,
they're just still in the buffer. **A buffered output file is not a reliable
progress meter.**

## The fix: force line buffering with `stdbuf`

`stdbuf` (GNU coreutils) overrides the buffering of the command it launches:

```sh
find . -type f -print0 | sort -z | xargs -0 stdbuf -oL sha256sum > /tmp/out.sums
#                                          ^^^^^^^^^^
```

- `stdbuf -oL <cmd>` → **stdout line-buffered**: one flush per line, so `wc -l`
  and `tail -f` update in real time.
- `stdbuf -o0 <cmd>` → stdout **unbuffered** (flush every write; more syscalls).
- `-eL` / `-e0` do the same for **stderr**, `-iL` for stdin.

Place `stdbuf` immediately before the program whose output you want to unbuffer.
Under `xargs`, it goes before the *child* (`xargs -0 stdbuf -oL sha256sum`), since
that child is the one actually writing.

## Caveats

- **It only works for programs using the libc stdio buffer.** `stdbuf` sets an
  environment/`LD_PRELOAD` hook that libc honours. Programs that manage their own
  buffering or flush explicitly ignore it — notably **`grep`** (use its own
  `--line-buffered`), `awk` (call `fflush()`), `sed` (`-u`), and most statically
  linked or non-libc binaries.
- `tee` is already line-buffered-ish for many cases, but when in doubt wrap the
  producer, not the consumer.
- Line buffering costs a flush per line. For millions of tiny lines that's
  measurable — use it for visibility during a run, not as a permanent default.

## Related: don't trust the output file to tell you a job is alive

`stdbuf` fixes the *display*, but if you can't (or don't want to) restart the job
with it, verify progress a different way — watch the **bytes the process has
actually read**, straight from the kernel, which no buffering can hide:

```sh
pid=$(pgrep -x sha256sum | head -1)
cat /proc/$pid/io           # read_bytes / rchar climb even while the .sums file is frozen
```

Gotcha: match the **right** process. `pgrep -f sha256sum` also matches the
`xargs -0 sha256sum …` parent (its argv contains "sha256sum"), which just waits
on its child and does no I/O — so its `read_bytes` never moves and looks stuck.
Use `pgrep -x sha256sum` to match the worker by exact name.
