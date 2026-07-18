search Image and Video
```
find . -type f | grep -v -E -i '\.(jpeg|jpg|png|mp4|mov|heic|tif|tiff|gif|bmp|svg|avi|dng|3gp|mpg|webp|m4v|iMovieMobile|psd|vob)$'
```

add new extensions if found.
Other extensions came across... Mostly comes from code base and documents folder. 
We can separate out audio if needed.

```
find ananda.sarangaram/ -type f | grep -v -E -i '\.(jpeg|jpg|png|mp4|mov|heic|tif|tiff|gif|bmp|svg|avi|dng|3gp|mpg|webp|m4v|iMovieMobile|psd|vob)$' | grep -v -E -i '\.(pdf|opf|txt|docx|doc|pages|epub|xlsx|pptx|odt|rtf|ods|ots|csv|md|djvu|xls|webloc|dotx|odp|mm|webarchive)$' | grep -v -E -i '\.(mp3|json|apk|m4a|db|rsrc|pls|m3u|nmbtemplate|game|mobi|nib|strings|xps|pgn|inf|ico|swf|icns|cdr|dmg|dll|ini|mst|cab|bin|iss|inx|isn|hdr|xml|exe|msi|pkg|id|htm|ppt|zip|dms|ex_)$' | grep -v -E '.*\..*'

```