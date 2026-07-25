---
title: Stop Pictures/Music/Videos from reappearing after I delete them
tags:
  - how-to
  - xdg
  - gnome
  - linux
weight: 199330
---

# Stop Pictures/Music/Videos from reappearing after I delete them

You delete the empty `~/Pictures`, `~/Music`, `~/Videos` folders you never use — and
they're **back at the next login**.

## Cause

`xdg-user-dirs-update` runs at login and **recreates** any standard directory listed in
`~/.config/user-dirs.dirs`. Deleting the folder doesn't help; the entry brings it back.

## Fix

Point the ones you don't want at **`$HOME`** — the documented "no dedicated folder"
setting — then delete them:

```
# ~/.config/user-dirs.dirs
XDG_MUSIC_DIR="$HOME"
XDG_PICTURES_DIR="$HOME"
XDG_VIDEOS_DIR="$HOME"
```

```
rmdir ~/Music ~/Pictures ~/Videos
xdg-user-dirs-update        # runs the login logic now; they should NOT reappear
```

Your edits are preserved — `xdg-user-dirs-update` keeps local changes on future runs.

## Notes

- Your **file manager** may still list them in its sidebar (now pointing at `$HOME`)
  until you remove those places/bookmarks or restart it.
- To disable the updater **entirely** (stops managing *all* XDG dirs), set
  `enabled=False` in `~/.config/user-dirs.conf` — usually overkill; the `$HOME` trick is
  more surgical.
