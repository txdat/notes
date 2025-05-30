# cherry-pick
- `git cherry-pick <commit1> <commit2> ...`
- if having any conflict, resolve it, `git add` and `git cherry-pick --continue`
- to abort git cheery-picking, `git cherry-pick --abort`
- to disable linting for git commit (like `--no-verify` for commit),
```bash
git config core.hooksPath # see current settings
git config core.hooksPath '/dev/null'
git config core.hooksPath '<previous path>' # or unset it git config --unset core.hooksPath
```

# compare local file with remote at specific SHA commit
```bash
git diff HEAD <remote-sha> -- <file-path>
```