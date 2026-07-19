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

| Event | Fires |
| --- | --- |
| `SessionStart` | session opens |
| `UserPromptSubmit` | you send a message |
| `PreToolUse` | before a tool runs — **can block it** |
| `PostToolUse` | after a tool succeeds |
| `Stop` | Claude finishes a turn, or you clear/compact/exit |
| `PreCompact` / `PostCompact` | around context compaction |

`PreToolUse` and `PostToolUse` accept a `matcher` to fire only for particular
tools (`Bash`, `Write|Edit`, …). `Stop` takes no matcher.

## A worked example: guaranteeing the work log gets written

The problem: this site keeps a daily diary, but it only ever got written when
someone remembered to ask. A habit that depends on memory eventually stops.

The requirement — *"every session must end with a diary entry"* — is a
per-event guarantee, so it is a `Stop` hook.

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

session_id="$(printf '%s' "$payload" | python3 -c '
import sys, json
try:
    print(json.load(sys.stdin).get("session_id", ""))
except Exception:
    print("")
' 2>/dev/null)"

# No session id -> cannot track state -> never block.
[ -n "$session_id" ] || exit 0

# Only act on the machine that actually holds the diary.
[ -d "$WORKLOG_DIR" ] || exit 0

marker="$STATE_DIR/${session_id//[^a-zA-Z0-9_-]/_}"

# Already prompted this session: let the session end.
if [ -e "$marker" ]; then
    find "$STATE_DIR" -type f -mtime +7 -delete 2>/dev/null
    exit 0
fi

# Record the prompt BEFORE emitting it, so a failure cannot cause a loop.
: > "$marker" || exit 0

target="$WORKLOG_DIR/$(date +%Y%m%d).md"

python3 - "$target" <<'PY'
import json, sys
print(json.dumps({
    "decision": "block",
    "reason": (
        f"Before finishing, write today's entry to {sys.argv[1]}.\n"
        "Style: a short diary in plain language, not technical notes.\n"
        "If nothing meaningful happened, say so -- do not invent an entry.\n"
        "Commit and push to origin. Do NOT publish to the public site.\n"
        "This prompt fires once per session."
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
# first call -- expect the JSON block
echo '{"session_id":"test123"}' | ~/.claude/hooks/worklog-check.sh

# second call, same session -- expect silence
echo '{"session_id":"test123"}' | ~/.claude/hooks/worklog-check.sh

# malformed and empty input -- expect silence, exit 0
echo 'not json' | ~/.claude/hooks/worklog-check.sh
echo ''         | ~/.claude/hooks/worklog-check.sh

rm -f ~/.claude/worklog-state/test123
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
* `Stop` fires on clear, compact and resume too — not only at the very end.
* Blocking is only meaningful for `Stop`, `PreToolUse` and `UserPromptSubmit`.
  Blocking a `PostToolUse` cannot un-run the tool.
* `settings.json` is not reloaded mid-session on first install (see above).
* Review what you have with `/hooks`; a working hook is invisible by design.
