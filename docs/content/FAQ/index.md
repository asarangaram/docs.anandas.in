---
title: Frequently asked Questions
weight: 199000
---

## Identify the type of files in folder

This command lists all the extensions used in the current folder.

```
find . -type f | sed 's/.*\.//' | sort | uniq
```

This will help when organizing a large disk.

## Filterout Images and Videos while retaining the folder structure.

```
find . -type f  -exec sh -c 'mimetype -b  "{}" | grep -q "^image/" && mkdir -p "/path/to/images/$(dirname "{}")" && mv -v -n "{}" "/path/to/images/{}"' \; -o -type f  -name MyPhotos\*  -exec sh -c 'mimetype -b "{}" | grep -q "^video/" && mkdir -p "/path/to/videos/$(dirname "{}")" && mv -n -v "{}" "/path/to/videos/{}"' \;
```
