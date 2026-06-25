import { cp, mkdir, readdir, rm, stat, writeFile } from "node:fs/promises"
import path from "node:path"
import { fileURLToPath } from "node:url"

const excludedDirectoryNames = new Set([".obsidian", ".trash"])
const hiddenHomeSections = new Set(["attachments"])

const scriptDir = path.dirname(fileURLToPath(import.meta.url))
const siteRoot = path.resolve(scriptDir, "..")
const repoRoot = path.resolve(siteRoot, "..")
const sourceDir = path.join(repoRoot, "obsidian")
const targetDir = path.join(siteRoot, "content-generated")

function isExcluded(relativePath) {
  if (!relativePath || relativePath === ".") {
    return false
  }

  return relativePath.split(path.sep).some((segment) => excludedDirectoryNames.has(segment))
}

function toTitleCase(value) {
  return value
    .split(/[\s-]+/)
    .filter(Boolean)
    .map((segment) => segment.charAt(0).toUpperCase() + segment.slice(1))
    .join(" ")
}

async function ensureSourceExists() {
  try {
    const sourceStats = await stat(sourceDir)
    if (!sourceStats.isDirectory()) {
      throw new Error(`${sourceDir} is not a directory`)
    }
  } catch (error) {
    throw new Error(`Expected an Obsidian vault at ${sourceDir}`, { cause: error })
  }
}

async function copyVault() {
  await rm(targetDir, { recursive: true, force: true })
  await mkdir(targetDir, { recursive: true })

  await cp(sourceDir, targetDir, {
    recursive: true,
    preserveTimestamps: true,
    filter: (currentSource) => {
      const relativePath = path.relative(sourceDir, currentSource)
      return !isExcluded(relativePath)
    },
  })
}

async function buildHomePage() {
  const entries = await readdir(targetDir, { withFileTypes: true })

  const sectionLinks = entries
    .filter(
      (entry) =>
        entry.isDirectory() &&
        !entry.name.startsWith(".") &&
        !hiddenHomeSections.has(entry.name),
    )
    .map((entry) => `- [${toTitleCase(entry.name)}](./${entry.name}/)`)
    .sort((left, right) => left.localeCompare(right))

  const homePage = [
    "---",
    "title: txdat's notes",
    "---",
    "",
    "Published from the `obsidian/` folder in this repository.",
    "",
    "## Sections",
    "",
    ...sectionLinks,
    "",
  ].join("\n")

  await writeFile(path.join(targetDir, "index.md"), homePage)
}

await ensureSourceExists()
await copyVault()
await buildHomePage()
