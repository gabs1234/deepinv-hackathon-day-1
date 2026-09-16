import { spawnSync } from 'node:child_process'
import { writeFile } from 'node:fs/promises'
import { fileURLToPath } from 'node:url'
import { join } from 'node:path'

const root = fileURLToPath(new URL('../', import.meta.url))
const output = join(root, 'docs')
const base = process.env.SLIDEV_BASE ?? '/deepinv-hackathon-day-1/'
const result = spawnSync(join(root, 'node_modules/.bin/slidev'), [
  'build', '--base', base, '--router-mode', 'hash',
  '--without-notes', '--out', output,
], { cwd: root, stdio: 'inherit' })
if (result.error) throw result.error
if (result.status !== 0) process.exit(result.status ?? 1)

await writeFile(join(output, '.nojekyll'), '')
console.log(`\nGitHub Pages export: ${output}`)
console.log(`Intended URL after deployment: https://gabs1234.github.io${base}`)
