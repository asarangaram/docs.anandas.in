---
title: Basic Git CLI
weight: 120000
pre: "<b>1.2. </b>"
---

## Git global setup

```
git config --global user.name "<Your Full Name>"
git config --global user.email "<Email id"
```

## Create a new repository

```
git clone origin git@gitlab.com:path/to/project.git project
cd project
git switch -c main
touch README.md
git add README.md
git commit -m "add README"
git push -u origin main
```

## Push an existing folder

````
cd existing_folder
git init --initial-branch=main
git remote add origin git@gitlab.com:path/to/project.git
git add .
git commit -m "Initial commit"
git push -u origin main
```110000

## Push an existing Git repository

````

cd existing_repo
git remote rename origin old-origin
git remote add origin git@gitlab.com:path/to/project.git
git push -u origin --all
git push -u origin --tags

```

## Recover deleted file

{{< tweet user="joshwcomeau" id="1609320980622581761" >}}

In a scenario where you want to recover a file deleted long back (assuming you know the file), first run the following command

```

git log --full-history -- src/path/to/file

```

This finds the commit that deleted the file.
Checked out that commit, and then backed up one more (`git checkout HEAD~1`).

This loads the file right before it was deleted!
```

## Submodule

Refer [here](https://devconnected.com/how-to-add-and-update-git-submodules/)
