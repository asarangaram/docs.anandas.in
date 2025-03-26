
When using rsync to transfer a folder from case-sensitive to case-insensitive storage, duplicate names can arise due to differing cases, such as "image.PNG" and "image.png." To resolve this, we need to rename the files. One approach is to standardise all names to either uppercase or lowercase; if conflicts persist, rename by appending a suffix like "_1," "_2," etc. 

This works when names can be uniformly adjusted, but in cases where it’s not feasible, the suffix method ensures conflicts are avoided before uploading.

```
# Get list of files in lowercase, find duplicates
find . -type f | tr '[:upper:]' '[:lower:]' | sort | uniq -d | while IFS= read -r lower_name; do
    # Find all files matching this lowercase name (case-insensitive)
    fdfind -p "$lower_name" | cat -n | tail -n +2 | while read -r idx file; do
      new_idx=$((idx - 1))
      ext="${file##*.}"
      base="${file%.*}"
      new_name="${base}_${new_idx}.${ext}"
      mv -v -n "$file" "$new_name"
      if [ -f "$file" ]; then
        echo "Rename failed for $file: $new_name already exists"
      fi
    done
done
```

first we find the duplicates with `find . -type f | tr '[:upper:]' '[:lower:]' | sort | uniq -d`. This returns all the duplicates in lower case. Most of the time, its not the real file name but lower cased. 
Now for each case, we list the file with its index, skilling second with index `fdfind -p "$lower_name" | cat -n | tail -n +2`.
These files need renaming we add a _\<index> with these files. 
Note, I use -n, this ensures not overwriting the file if any exists. 

Two improvements we can do,
1. when the file we try to rename exists, we need to increase the index and it will have cascade effect for all remaining files.
2. If directory names conflicts, we need to first resolve it before we look into file. We can use the same logic, but mv the directory. 
-- as of now, I didn't encounter any of these problem, hence keeping my script simple.
