
# apt 

## To fix any broken packages. 
```
apt-get -f install
```

If your disk is full, this may or may not work depending on whether the broken package has been completely downloaded.

## to free up some space

```
aptitude clean
```

This will clean your `apt` package cache (these are `.deb` files for the packages you installed; stored in `/var/cache/apt/archives`); the actual packages will remain installed, but you will no longer have the `.deb` files on disk and would need to re-download them if you purge/re-install an existing package.

