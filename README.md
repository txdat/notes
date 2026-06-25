# txdat's notes

- open **obsidian** as a vault of [obsidian](https://obsidian.md/)

## GitHub Pages

This repo now includes a Quartz site scaffold in [`site/`](/home/txdat/work/notes/site) that publishes the
[`obsidian/`](/home/txdat/work/notes/obsidian) vault to GitHub Pages.

### Local preview

```bash
cd site
npm ci
npm run dev
```

Quartz will serve the site at `http://localhost:8080`.

### Deploy

1. In the repository settings, open `Pages`.
2. Set `Source` to `GitHub Actions`.
3. Trigger a deploy in one of these ways:
   - run the workflow manually from the `Actions` tab
   - push a tag that matches `pages-v*`
   - bump [`.pages-version`](/home/txdat/work/notes/.pages-version) on `main` and push that file

Examples:

```bash
# tag-based deploy
git tag pages-v1
git push origin pages-v1

# version-file deploy
printf '2\n' > .pages-version
git add .pages-version
git commit -m "trigger pages deploy"
git push origin main
```

Notes:

- normal content/code pushes no longer trigger Pages automatically
- `workflow_dispatch` is still available for truly manual deploys

The workflow is in [deploy-pages.yml](/home/txdat/work/notes/.github/workflows/deploy-pages.yml).
