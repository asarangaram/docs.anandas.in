---
title: Image Magic
weight: 118000
---

The simplest way to install ImageMagic is to use [ImageMagic Easy Install](https://github.com/SoftCreatR/imei). However, it may be difficult to completely remove it (uninstall and purge) in later stage.

## Profile issue

Libpng-1.6 is more stringent about checking ICC profiles than previous versions; you can ignore the warning.

`libpng warning: iCCP: known incorrect sRGB profile`

To get rid of it, remove the iCCP chunk from the PNG image.
This can be done with Image Magic, by converting the image.

```bash
convert in.png out.png
```

To remove the invalid iCCP chunk from all of the PNG files in a folder (directory), you can use mogrify from ImageMagick:

```bash
mogrify *.png
```

This requires that your ImageMagick was built with libpng16. You can easily check it by running:

```bash
convert -list format | grep PNG
```

If you'd like to find out which files need to be fixed instead of blindly processing all of them, you can run

```bash
pngcrush -n -q *.png
```

where the -n means don't rewrite the files and -q means suppress most of the output except for warnings. Sorry, there's no option yet in pngcrush to suppress everything but the warnings.

Note: You must have pngcrush installed.

[Source](https://stackoverflow.com/questions/22745076/libpng-warning-iccp-known-incorrect-srgb-profile)
