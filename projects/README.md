# Projects

One folder per research project. Each subfolder is a git submodule pinned to a commit; see the project README for the repositories and the thesis chapter it feeds.

To move a submodule to the commit used for the thesis results:
```
git -C projects/<project>/<folder> checkout <commit>
git add projects/<project>/<folder>
```
