
How to group the files as per create date.

```bash
exiftool -v -api largefilesupport=1 -ee -test -o . '-Directory<CreateDate' -d datewise/%Y/%m/%d -r Videos_200MPlus/
```
