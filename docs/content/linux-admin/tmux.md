# `tmux` (Terminal Multiplexer)

The `tmux` is a terminal multiplexer that allows you to run separate processes or commands and preview the output at the same time.

Install `tmux`, and then jus type `tmux` to enter into `tmux`.  

## Basic Commands

```bash
tmux new-session -s <your_session_name>
tmux list-sessions
tmux attach -t <your_session_name>
tmux detach
```
### Shortcuts
```
Ctrl+b ?           :  Show all commands

# New
Ctrl+b c           : Create a new window
Ctrl+b “           : Split horizontally
Ctrl+b %           : Split vertically

# Navigate
Ctrl+b <arrow-key> : Switch pane
Ctrl+b n           : Next Window
Ctrl+b p           : Previous Window
```

## On MAC, 
`tmux` may be installed via `brew`.

:::note
**When installing `tmux` through brew, note down the following:** 
Example configuration has been installed to `/usr/local/opt/tmux/share/tmux` and Bash completion has been installed to `/usr/local/etc/bash_completion.d`.
:::
### Are you getting a warning?

If you are using `bash` as default terminal,  the MAC os displays a warning message

```
The default interactive shell is now zsh.
To update your account to use zsh, please run `chsh -s /bin/zsh`.
For more details, please visit https://support.apple.com/kb/HT208050.
```

if you want to keep bash as your shell, you may ignore this warning or disable it by adding  `export BASH_SILENCE_DEPRECATION_WARNING=1` into ~/.bash_profile. To change to zsh, 
add the following into the tmux config file.
```
set -g default-command /bin/zsh 
set -g default-shell /bin/zsh
```