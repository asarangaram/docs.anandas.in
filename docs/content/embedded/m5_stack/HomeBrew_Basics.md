---
title: HomeBrew Basics
weight: 151000
---

## What is [HomeBrew][1]]?

It is a package manager. It is used to install packages that are NOT provided
by Apple. This is an useful utility to install various utilities and port
linux projects or develop on MAC.

## How to [install and uninstall][2]?

Its a command-line utility.

### Install HomeBrew

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

The script installs:
`  /usr/local/bin/brew
  /usr/local/share/doc/homebrew
  /usr/local/share/man/man1/brew.1
  /usr/local/share/zsh/site-functions/_brew
  /usr/local/etc/bash_completion.d/brew
  /usr/local/Homebrew
 `

and creates the following directories:
`/usr/local/bin
  /usr/local/etc
  /usr/local/include
  /usr/local/lib
  /usr/local/sbin
  /usr/local/share
  /usr/local/var
  /usr/local/opt
  /usr/local/share/zsh
  /usr/local/share/zsh/site-functions
  /usr/local/var/homebrew
  /usr/local/var/homebrew/linked
  /usr/local/Cellar
  /usr/local/Caskroom
  /usr/local/Frameworks
  `

### Uninstall HomeBrew

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/uninstall.sh)"
```

HomeBrew keeps all its installation under /usr/local.
Read the [Documentation][3] for more details.

## Basics commands:

### brew install <>

### brew uninstall <>

### brew list

### brew leaves

- importantly, you must know about
  \*\* taps (Third party repositories)

[1]: https://brew.sh
[2]: https://github.com/homebrew/install
[3]: https://docs.brew.sh
