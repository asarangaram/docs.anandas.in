Tip while automating Photos App

Export Photo with Album name as Folder name

``` applescript
global gDest
set gDest to "~/Pictures/ExportAll/" as POSIX file as text -- the destination folder (use a valid path)

my makeFolder(gDest)
tell application "Photos"
	activate
	
	repeat with myalbum in albums
		with timeout of 3600 seconds
			set albumName to name of myalbum
			set destFolder to gDest & albumName
			my makeFolder(destFolder)
			
			set allPhotos to get media items of myalbum
			set settings to "JPEG - Original Size"
			export allPhotos to alias destFolder with using originals
			
			
		end timeout
	end repeat
end tell
```