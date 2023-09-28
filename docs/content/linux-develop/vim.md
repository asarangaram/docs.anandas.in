
[:fontawesome-solid-arrow-up-right-from-square: Official Vim documentation  ](https://vimdoc.sourceforge.net/){ .md-button .md-button--primary }

## VIM Commands

VIM can be configured via commands. These commands can be issued in command mode (for current session) or via .vimrc file.

The default .vimrc is always placed in ~/.vimrc, however, we can use different 
.virmc file via -u command

```
vim -u <.vimrc file>
```

This option helps to have different configuration based on what we load to edit.
For example, for a normal document, we would like to keep the vim more customized and for huge documents, we prefer to disable all customizations and load the document.

To use vim without any configuration, we can use NONE
```
vim -u NONE /tmp/log.txt
```

## Opening Huge documents

It is always better to use `less` or `more`  to view large commands. they are called [**Terminal Pagers**](https://en.wikipedia.org/wiki/Terminal_pager)

If we need to edit the file, we can turn off the plugins and the visual enhancements.

## Visual Enhancements

`set` command is used to enable or disable visual enhancements.

### `syntax`

Vim will open the supported files with syntax highlighting enabled. We can turn off the syntax highlighting by 
```vim
: set syntax=off
```

### filetype

```
: set ft=
```

### `nowrap` / `wrap`
```
set nowrap
set wrap
```
### code `foldenable`

```
: set nofoldenable
```

Set fileformat to unix: 

```
:w ++ff=unix 
:set ff=unix
```

```
:set list
```