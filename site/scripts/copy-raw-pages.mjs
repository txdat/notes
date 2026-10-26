import { cp, rm } from "node:fs/promises"
import path from "node:path"
import { fileURLToPath } from "node:url"

// Standalone HTML pages served verbatim. They live in pages/, outside the Obsidian
// vault, so Quartz never sees them (it would strip `.html` and render the notes).
const rawPageDirs = ["linh-dat-wedding"]

const scriptDir = path.dirname(fileURLToPath(import.meta.url))
const siteRoot = path.resolve(scriptDir, "..")
const sourceDir = path.resolve(siteRoot, "..", "pages")
const outputDir = path.join(siteRoot, "public")

for (const dir of rawPageDirs) {
  const target = path.join(outputDir, dir)
  await rm(target, { recursive: true, force: true })
  await cp(path.join(sourceDir, dir), target, {
    recursive: true,
    // Skip notes, placeholders, and working files (prompts, drafts) that are not part of the page.
    filter: (src) =>
      !src.endsWith(".md") &&
      ![".gitkeep", "drafts", "prompts"].includes(path.basename(src)),
  })
}
