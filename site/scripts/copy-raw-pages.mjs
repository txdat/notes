import { cp, rm } from "node:fs/promises"
import path from "node:path"
import { fileURLToPath } from "node:url"

// Standalone HTML pages served verbatim. Quartz strips `.html` from content
// assets and must ignore these folders (see ignorePatterns in quartz.config.yaml).
const rawPageDirs = ["linh-dat-wedding"]

const scriptDir = path.dirname(fileURLToPath(import.meta.url))
const siteRoot = path.resolve(scriptDir, "..")
const sourceDir = path.resolve(siteRoot, "..", "obsidian")
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
