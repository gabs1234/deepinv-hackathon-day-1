import { execFileSync } from 'node:child_process'
import { createHash } from 'node:crypto'
import { readdir, readFile, writeFile } from 'node:fs/promises'
import { fileURLToPath } from 'node:url'
import { join } from 'node:path'

const root = fileURLToPath(new URL('../', import.meta.url))
const repo = process.argv[2] ?? join(root, 'multi-distance-phase-retrieval')
const git = (...args) => execFileSync('git', ['-C', repo, ...args], { encoding: 'utf8' }).trim()
if (git('status', '--porcelain', '--untracked-files=no'))
  throw new Error('Commit the scientific source changes before recording figure provenance')
const directory = join(root, 'public/phase-retrieval')
const files = {}
for (const name of (await readdir(directory)).sort()) {
  if (!/\.(png|svg|json)$/.test(name)) continue
  files[name] = createHash('sha256').update(await readFile(join(directory, name))).digest('hex')
}
const provenance = {
  scientific_repository: 'https://github.com/gabs1234/multi-distance-phase-retrieval',
  renderer_and_verification_commit: git('rev-parse', 'HEAD'),
  note: 'The commit contains the shared scientific implementations and renderers. The imported numerical runs retain their original source hashes in the figure manifests; they are not relabeled as newly computed runs.',
  numerical_data_included: false,
  figure_directory: 'public/phase-retrieval',
  sha256: files,
}
await writeFile(join(root, 'deployment/figure-provenance.json'), `${JSON.stringify(provenance, null, 2)}\n`)
console.log(`Recorded provenance for ${Object.keys(files).length} figure assets and manifests.`)
