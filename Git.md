# Git

## Remotes

### Add remote

```bash
git remote add <remote_name> git@<remote_address>
```



## Push and update

### Fetch and merge

`git pull`

## Branching

Create new branch and push to remote

```bash
git checkout -b <branch_name>
git add .
git commit -m <commit message>
git push -u origin <branch_name>
```

### Fetch all remote branches

```bash
 git fetch <remote>
```

### List all branches available for checkout

```bash
git branch -a
```

### Switch to different remote branch

```bash
git branch -u <remote>/<branch>
```



### Create new branch

```bash
git branch <branch_name>
```

### View remote branches

```bash
git fetch origin
git branch -a
```



### Switch branch

```bash
git checkout <branch_name>
```

## Revert

## Submodules

### Add submodule to a project

```bash
git submodule add <submodule repo URL> <optional: folder to clone to>
# E.g.
git submodule add https://github.com/chaconinc/DbConnector services/db
```

### Clone a project, then clone its submodules as well

```bash
git clone <repo URL>
# At this point, submodule subdirectories are present but empty
git submodule init
git submodule update
```

Or, do it all in one command

```bash
git clone --recurse-submodules <repo URL>
```

### Update a submodule

```bash
cd <submodule directory>
git fetch
git merge origin/master
```

Or, from project root,

```bash
git submodule update --remote <submodule dir>
```

### Pull changes from main project remote

```bash
git pull
git submodule update --init --recursive
```

## Remove .DS_Store files

```bash
find . -name .DS_Store -print0 | xargs -0 git rm -f --ignore-unmatch
```

Add the following line to `.gitignore`

```
.DS_Store
```

Commit

```bash
git add .gitignore
git commit -m '.DS_Store banished!'
```

# Mirror a repository

`git clone --bare https://github.com/EXAMPLE-USER/OLD-REPOSITORY.git`

Mirror-push to the new repository.

```bash
cd OLD-REPOSITORY.git
git push --mirror https://github.com/EXAMPLE-USER/NEW-REPOSITORY.git
```


Remove the temporary local repository you created earlier.

```bash
cd ..
rm -rf OLD-REPOSITORY.git
```



