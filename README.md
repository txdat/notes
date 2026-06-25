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
   - push to `master`

Examples:

```bash
# push-based deploy
git push origin master
```

Notes:

- pushes to `master` trigger the Pages deploy workflow
- `workflow_dispatch` is available for manual deploys

The workflow is in [deploy-pages.yml](/home/txdat/work/notes/.github/workflows/deploy-pages.yml).
