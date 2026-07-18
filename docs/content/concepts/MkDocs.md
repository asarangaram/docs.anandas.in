---
title: MkDocs
---

# MkDocs

This documentation is being created using MkDocs with the theme "Material for MkDocs".

Few extensions worth knowing:

[MagicLink](https://facelessuser.github.io/pymdown-extensions/extensions/magiclink)
Usually, markdown expects the links to be written with the syntax, ```[Text](<Link>)```. However in most scenarios we simply want to paste the link or use shortcuts. This plugin makes this simple. The Auto-Linking feature allows to paste the http(s) links as raw text. If configured,  it can also use shorthand links to git repositories.

With a repository configured, shorthand works too:

```yaml
repo_url: "https://github.com/<user>/<repo>"
edit_uri: "edit/main/docs/"
...
markdown_extensions:
  - pymdownx.magiclink:
      repo_url_shorthand: true
      user: <user>
      repo: <repo>
```

`@user` then links to a profile, and `#123` to an issue.

!!! note
    This site no longer sets `repo_url`. Its repository is a private Forgejo
    instance on the LAN, so shorthand links would point somewhere no visitor
    could reach — only plain URL auto-linking is enabled here. See
    [Self-hosting this TIL site](../linux-infra/til_website_setup.md).



