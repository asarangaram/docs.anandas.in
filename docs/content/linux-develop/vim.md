
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

## VIM Delete lines
Source: [https://linuxize.com/post/vim-delete-line/](https://linuxize.com/post/vim-delete-line/)
```
The command to delete a line in Vim is dd.
To delete multiple lines at once, Type 5dd
Delete a range of lines  :[start],[end]d
    . (dot) - The current line.
    $ - The last line.
    % - All lines.

    :.,$d - From the current line to the end of the file.
    :.,1d - From the current line to the beginning of the file.
    10,$d - From the 10th line to the end of the file.

    :g/<pattern>/d

:g/foo/d - Delete all lines containing the string “foo”. It also removes line where “foo” is embedded in larger words, such as “football”.
:g!/foo/d - Delete all lines not containing the string “foo”.
:g/^#/d - Remove all comments from a Bash script. The pattern ^# means each line beginning with #.
:g/^$/d - Remove all blank lines. The pattern ^$ matches all empty lines.
:g/^\s*$/d - Remove all blank lines. Unlike the previous command, this also removes the blank lines that have zero or more whitespace characters (\s*).
```

# VIM Macro

## Record the macro

```
    q<register><commands>q
         <register> - a-z

```

## View macro 

```
:reg h
```

## Copy into different macro (not tried)

First, copy the macro content and paste it to an empty line in the buffer. Then replace special characters with their Vim representation by using Ctrl+v+<ESC> and Ctrl+v+<ENTER> in Insert mode. Then copy the macro content in the desired register, for example, register h with this command:

```
"hy$

```
## Replay

``` 
@<register>
@@ - repeat last played macro
```

[Reference](https://www.redhat.com/sysadmin/use-vim-macros)