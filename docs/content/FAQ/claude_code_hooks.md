---
title: Claude how-to - add a hook
weight: 199100
---

# Claude how-to: add a hook

## Why a hook, and not just an instruction

Claude Code offers several places to put standing guidance — `CLAUDE.md`,
saved memories, the system prompt. All of them are **advisory**. They are text
the model reads and usually follows, and "usually" is the problem: the one
session that skips the step is exactly the session where it mattered.

A **hook** is different. It is a command executed by the harness itself at a
fixed point in the session lifecycle. The model does not decide whether it
runs. If the requirement is *"this must happen every time"*, a hook is the only
mechanism that delivers it.

Rule of thumb:

| Need | Use |
| --- | --- |
| "Prefer X over Y", "our convention is Z" | `CLAUDE.md` |
| "Remember I use `uv`, not `pip`" | memory |
| "**Every time** X happens, do Y" | **hook** |

## Where hooks live

Hooks are declared in a `settings.json`. Which one determines the scope:

| File | Scope |
| --- | --- |
| `~/.claude/settings.json` | every project on this machine |
| `<project>/.claude/settings.json` | this project, shared via git |
| `<project>/.claude/settings.local.json` | this project, private to you |

## The events worth knowing

| Event | Fires | Can make Claude do work? |
| --- | --- | --- |
| `SessionStart` | session opens | — |
| `UserPromptSubmit` | you send a message | yes |
| `PreToolUse` | before a tool runs | blocks the tool |
| `PostToolUse` | after a tool succeeds | — |
| `Stop` | **Claude finishes a turn** | **yes** |
| `PreCompact` | before context compaction | blocks the compaction only |
| `SessionEnd` | after the session has ended | **no** |

`PreToolUse` and `PostToolUse` accept a `matcher` to fire only for particular
tools (`Bash`, `Write|Edit`, …). `Stop` takes no matcher.

### The trap: "do this when the session ends"

This is the most natural thing to want, and the two events whose names promise
it cannot deliver it:

* **`SessionEnd` runs *after* the session is over.** It has no ability to block
  and no ability to inject a prompt — there is no longer a conversation to
  inject into. It can run a shell command and nothing more. Useful for cleanup,
  logging, or leaving a note on disk; useless for "get Claude to write
  something first".
* **`PreCompact` can only refuse the compaction.** It cannot hand Claude
  instructions to act on.

`Stop` is the only event that can make Claude keep working. So anything of the
form *"before we finish, do X"* has to live on `Stop` — and `Stop` fires at the
end of **every turn**, not at the end of the session. There is no "last turn"
event, because nothing knows which turn is the last one until you leave.

That mismatch is the whole design problem, and the next section is about
working around it.

## A worked example: guaranteeing the work log gets written

The problem: this site keeps a daily diary, but it only ever got written when
someone remembered to ask. A habit that depends on memory eventually stops.

The requirement — *"every session must end with a diary entry"* — is a
per-event guarantee, so it is a `Stop` hook.

### 0. Firing at the right moment

The obvious implementation blocks the first `Stop` it sees and sets a marker so
it never blocks again. That is what the first version did, and it was wrong in
a way that only showed up in use: **the first `Stop` is the end of the first
turn.** The hook fired before the session had done anything, and cheerfully
demanded a diary entry about a thirty-second file move.

There is no way to detect the last turn. What you *can* detect is whether the
session has done anything worth writing about — so instead of guessing at
timing, the hook inspects the transcript and stays silent until it has.

The payload carries a `transcript_path`: a JSONL file, one event per line, where
messages carry a `role` and a `content` array whose entries may be `tool_use`
blocks. That gives two independent signals:

* **It changed a file** — a `Write`, `Edit` or `NotebookEdit` appears.
* **It ran long** — a count of assistant turns past a threshold.

The second exists because the first is too narrow. A session can do a great deal
without ever calling `Write`: shell work through `mv` and `git`, or a long
technical discussion that ends in a decision. Those are often the entries most
worth having, since the reasoning is the part that gets forgotten. Matching on
`Bash` instead would not help — `Bash` is also how a session lists a directory.
Length is the better proxy: it does not care *how* the work happened.

Pick the threshold from your own history rather than guessing. Counting assistant
turns across every transcript on this machine showed a clean gap — trivial
sessions ran 0–12 turns, substantial ones 35 and up, with nothing in between. A
threshold of 20 sits in the empty space, so it is not balanced on a cliff edge.

```bash
# how long are my sessions, really?
for f in ~/.claude/projects/*/*.jsonl; do
  python3 -c '
import json, sys
n = sum(1 for l in open(sys.argv[1], encoding="utf-8", errors="replace")
        if (json.loads(l).get("message") or {}).get("role") == "assistant")
print(f"{n:>6}  {sys.argv[1].split(chr(47))[-2][:40]}")' "$f" 2>/dev/null
done | sort -n
```

### 1. The script

Hooks receive a JSON payload on **stdin** and communicate back through
**stdout**. This one reads the session id and decides whether to interrupt.

```bash title="~/.claude/hooks/worklog-check.sh"
#!/usr/bin/env bash
set -uo pipefail

WORKLOG_DIR="$HOME/path/to/site/docs/worklog"
STATE_DIR="$HOME/.claude/worklog-state"
mkdir -p "$STATE_DIR" 2>/dev/null

payload="$(cat)"

# Pull both the session id and the transcript path out in one pass.
read -r session_id transcript_path <<<"$(printf '%s' "$payload" | python3 -c '
import sys, json
try:
    d = json.load(sys.stdin)
    print(d.get("session_id", "") or "-", d.get("transcript_path", "") or "-")
except Exception:
    print("- -")
' 2>/dev/null)"

# No session id -> cannot track state -> never block.
[ "${session_id:--}" != "-" ] || exit 0

# Only nag on the machine that actually holds the worklog.
[ -d "$WORKLOG_DIR" ] || exit 0

marker="$STATE_DIR/${session_id//[^a-zA-Z0-9_-]/_}"

# Already prompted this session: let the session end.
if [ -e "$marker" ]; then
    find "$STATE_DIR" -type f -mtime +7 -delete 2>/dev/null
    exit 0
fi

# Fall back to locating the transcript ourselves if the payload lacks it.
if [ "${transcript_path:--}" = "-" ] || [ ! -f "$transcript_path" ]; then
    transcript_path="$(find "$HOME/.claude/projects" -name "${session_id}.jsonl" \
        -type f -print -quit 2>/dev/null)"
fi

# No transcript -> cannot tell whether work happened -> stay quiet.
[ -n "$transcript_path" ] && [ -f "$transcript_path" ] || exit 0

# Was this session substantial? Two independent reasons to think so:
#   - it changed a file, or
#   - it ran long, which covers technical discussions and shell-only work that
#     never touch Write/Edit but are still worth recording.
# Short read-only sessions match neither and are left alone.
MIN_TURNS=20

did_work="$(MIN_TURNS="$MIN_TURNS" python3 - "$transcript_path" <<'PY' 2>/dev/null
import json, os, sys

MUTATING = {"Write", "Edit", "NotebookEdit"}
min_turns = int(os.environ.get("MIN_TURNS", "20"))

mutated = False
turns = 0

try:
    with open(sys.argv[1], encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except Exception:
                continue
            message = entry.get("message") or {}
            if message.get("role") == "assistant":
                turns += 1
            content = message.get("content")
            if not isinstance(content, list):
                continue
            for block in content:
                if isinstance(block, dict) and block.get("type") == "tool_use":
                    if block.get("name") in MUTATING:
                        mutated = True
except Exception:
    print("no")
    sys.exit(0)

if mutated:
    print("edits")
elif turns >= min_turns:
    print("long")
else:
    print("no")
PY
)"

case "$did_work" in
    edits) why="This session changed files on disk." ;;
    long)  why="This session ran long -- a substantial discussion or a stretch of shell work. It may have produced no file changes; if the outcome was a decision, an explanation, or a dead end, that is still worth recording." ;;
    *)     exit 0 ;;
esac

# Record the prompt BEFORE emitting it, so a failure cannot cause a loop.
: > "$marker" || exit 0

today="$(date +%Y%m%d)"
pretty="$(date '+%-d %B %Y')"
target="$WORKLOG_DIR/${today}.md"

if [ -f "$target" ]; then
    state="It already exists -- append a new section for this session's work rather than rewriting earlier entries."
else
    state="It does not exist yet -- create it with 'title: ${today:0:4}-${today:4:2}-${today:6:2}' frontmatter and a '# ${pretty}' heading."
fi

python3 - "$target" "$state" "$why" <<'PY'
import json, sys
target, state, why = sys.argv[1], sys.argv[2], sys.argv[3]
print(json.dumps({
    "decision": "block",
    "reason": (
        f"Before finishing, consider today's worklog entry at {target}. {state}\n\n"
        f"{why}\n\n"
        "DRAFT FIRST, DO NOT WRITE YET. Compose the entry and show it in full "
        "in your reply as a fenced markdown block, then ask whether to save it. "
        "Only write to the file and commit after the user approves. If they "
        "decline, drop it and finish -- a skipped entry is a fine outcome and "
        "you will not be asked again this session.\n\n"
        "Style: a short diary of what was done and why, in plain language -- "
        "not technical notes. Match the tone of the existing entries. Record "
        "decisions and anything that went wrong, since that is the part worth "
        "remembering later. If the session amounted to little, say so in a "
        "sentence rather than padding it out -- do not invent significance.\n\n"
        "On approval, commit and push to the Forgejo remote (origin), which "
        "publishes the intranet copy automatically. Do NOT publish to the "
        "public site: 'just publish' / 'just release' is manual and never run "
        "by a session.\n\n"
        "This prompt fires once per session; you will not be asked again."
    ),
}))
PY
exit 0
```

```bash
chmod +x ~/.claude/hooks/worklog-check.sh
```

Returning `{"decision": "block", "reason": "..."}` stops the session from
ending and feeds `reason` back to Claude as an instruction. Printing nothing
and exiting `0` lets it end normally.

### 2. Register it

Add to `~/.claude/settings.json`. **Merge** with what is already there — do not
overwrite the file, and note that a malformed `settings.json` silently disables
*every* setting in it, not just the hook.

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$HOME/.claude/hooks/worklog-check.sh",
            "timeout": 15,
            "statusMessage": "Checking worklog..."
          }
        ]
      }
    ]
  }
}
```

### 3. Test it before trusting it

A hook that silently does nothing is worse than no hook, because you believe
you are covered. Feed it the payload it will really receive:

```bash
H=~/.claude/hooks/worklog-check.sh

# build a fake transcript: N plain turns, optionally one tool call
mk(){ f=$(mktemp /tmp/tr-XXXXXX.jsonl); : > "$f"
  for i in $(seq 1 "$1"); do
    printf '%s\n' '{"message":{"role":"assistant","content":[{"type":"text","text":"x"}]}}' >> "$f"
  done
  [ -n "$2" ] && printf '{"message":{"role":"assistant","content":[{"type":"tool_use","name":"%s"}]}}\n' "$2" >> "$f"
  echo "$f"; }

A=$(mk 5 Read); B=$(mk 5 Edit); C=$(mk 30 Read); D=$(mk 30 Edit)

echo "{\"session_id\":\"s1\",\"transcript_path\":\"$A\"}" | bash "$H"  # short+read  -> silence
echo "{\"session_id\":\"s2\",\"transcript_path\":\"$B\"}" | bash "$H"  # short+edit  -> block
echo "{\"session_id\":\"s3\",\"transcript_path\":\"$C\"}" | bash "$H"  # long+read   -> block
echo "{\"session_id\":\"s4\",\"transcript_path\":\"$D\"}" | bash "$H"  # long+edit   -> block
echo "{\"session_id\":\"s4\",\"transcript_path\":\"$D\"}" | bash "$H"  # repeat      -> silence

# missing transcript, malformed and empty input -- expect silence, exit 0
echo '{"session_id":"s5","transcript_path":"/nope.jsonl"}' | bash "$H"
echo 'not json' | bash "$H"
echo ''         | bash "$H"

rm -f "$A" "$B" "$C" "$D" ~/.claude/worklog-state/s{1,2,3,4,5}
```

Better still, replay your **real** transcripts through it and check the verdicts
match your own sense of which sessions deserved an entry. Synthetic tests prove
the branches work; only real ones tell you the threshold is set sensibly.

Worth confirming the transcript really looks the way the parser assumes, rather
than trusting it — point this at a genuine session file and check the tool
names that come back:

```bash
python3 - ~/.claude/projects/<project>/<session-id>.jsonl <<'PY'
import json, sys, collections
names = collections.Counter()
for line in open(sys.argv[1], encoding='utf-8'):
    try: e = json.loads(line)
    except Exception: continue
    c = (e.get("message") or {}).get("content")
    if isinstance(c, list):
        for b in c:
            if isinstance(b, dict) and b.get("type") == "tool_use":
                names[b.get("name")] += 1
print(dict(names))
PY
```

Then check the settings file parses and the hook is where you think it is:

```bash
jq -e '.hooks.Stop[] | .hooks[] | .command' ~/.claude/settings.json
```

### 4. Load it

The settings watcher only monitors directories that already had a settings
file when the session started. After a first-time install, open `/hooks` once
or restart Claude Code, or the hook will sit there doing nothing.

## Designing a blocking hook so it cannot trap you

This is the part that deserves real thought. A `Stop` hook that always blocks
makes the session impossible to leave.

The safeguards above, and why each exists:

* **Block at most once per session.** A marker file keyed by session id. The
  second `Stop` passes straight through.
* **Block only when there is a reason to.** The transcript check means a session
  that changed nothing is never interrupted. This is as much about credibility
  as politeness: a hook that fires when it had nothing to ask for trains you to
  dismiss it.
* **Write the marker _before_ emitting the block.** If the script dies halfway,
  the marker already exists, so the next attempt is allowed. The failure mode
  is "prompt skipped", never "session stuck".
* **Exit 0 on every unexpected input.** No session id, malformed JSON, empty
  stdin — all fall through silently.
* **Check the target exists.** On a machine without the diary the hook is inert
  rather than nagging about a directory that will never be there.
* **Set a `timeout`.** A hook that hangs stalls the session.

The general principle: a hook that guards a *nice-to-have* should fail open. Only
a hook guarding a genuine safety property should fail closed, and then you must
be certain the recovery path does not itself depend on the thing being blocked.

## Ask, do not act: previewing before writing

A hook cannot draw a dialog box. What it *can* do is set the terms of what
happens next, and "show me before you commit to it" is one of those terms.

The `reason` is an instruction to the model, so it can say *draft it, show it,
wait*:

> DRAFT FIRST, DO NOT WRITE YET. Compose the entry and show it in full in your
> reply as a fenced markdown block, then ask whether to save it. Only write to
> the file and commit after the user approves. If they decline, drop it and
> finish — a skipped entry is a fine outcome.

The block is what makes this work. Claude is forced to produce another turn, and
that turn is a draft rather than a commit. You read it, then say yes or no. The
marker file has already been written, so declining genuinely ends it.

This changes the economics of the trigger, which is why it pairs with the
looser rule above. A hook that *writes* must be conservative about firing,
because every false positive puts something into the file that you then have to
go and remove. A hook that only *asks* can afford to fire on anything plausible,
because rejecting a draft costs one word. Being generous about what counts as a
session worth recording is only safe **because** nothing is written without a
yes.

The general principle: separate *noticing* from *doing*. Let the hook be
eager about noticing, and leave the doing behind a confirmation.

## Scoping what the hook is allowed to ask for

Worth stating explicitly in the `reason`, because it becomes a standing
instruction to every future session.

For the diary, the hook may commit and push to the internal git server — which
republishes the intranet copy automatically — but is **forbidden** from
publishing to the public site. Publishing is manual on purpose, so that
unfinished work does not go out. An automatic step that quietly published would
have silently removed that safeguard.

If a hook can trigger an outward-facing action, say so in the `reason` and say
which actions are off limits.

## Gotchas

* Hooks are **not** a place for secrets. Anything in `settings.json` or the
  script is plain text on disk.
* `Stop` fires at the end of **every turn**, not just the last one. There is no
  last-turn event. Design for that rather than hoping.
* `SessionEnd` cannot ask Claude for anything — it runs after the session is
  gone. Reach for it only for cleanup, logging, or a note left on disk.
* Blocking is only meaningful for `Stop`, `PreToolUse` and `UserPromptSubmit`.
  Blocking a `PostToolUse` cannot un-run the tool; blocking `PreCompact` only
  cancels the compaction.
* `settings.json` is not reloaded mid-session on first install (see above).
* Review what you have with `/hooks`; a working hook is invisible by design.
