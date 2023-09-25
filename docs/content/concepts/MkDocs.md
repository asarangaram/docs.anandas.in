This documentation is being created using MkDocs with the theme "Material for MkDocs".

Few extensions worth knowing:

[MagicLink](https://facelessuser.github.io/pymdown-extensions/extensions/magiclink)
Usually, markdown expects the links to be written with the syntax, ```[Text](<Link>)```. However in most scenarios we simply want to paste the link or use shortcuts. This plugin makes this simple. The Auto-Linking feature allows to paste the http(s) links as raw text. If configured,  it can also use shorthand links to git repositories.

Notice, 
```
repo_url: "https://github.com/asarangaram/docs.anandas.in"
edit_uri: "edit/main/docs/"
...
markdown_extensions:
	  - pymdownx.magiclink:
		repo_url_shorthand: true
		user: asarangaram
		repo: docs.anandas.in

```

now, 
@asarangaram - automatically points to my profile.



