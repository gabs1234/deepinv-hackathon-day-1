import { spawnSync } from 'node:child_process'
import { existsSync, readFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { join } from 'node:path'

const root = fileURLToPath(new URL('../', import.meta.url))
const source = JSON.parse(readFileSync(join(root, 'deployment/slidev-source.json'), 'utf8'))
const checkout = join(root, '.slidev')
const env = {
  ...process.env,
  CYPRESS_INSTALL_BINARY: '0',
  PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD: '1',
  SKIP_INSTALL_SIMPLE_GIT_HOOKS: '1',
}

function run(command, args, cwd = root, capture = false) {
  const result = spawnSync(command, args, { cwd, env, encoding: 'utf8', stdio: capture ? 'pipe' : 'inherit' })
  if (result.error) throw result.error
  if (result.status !== 0) throw new Error(`${command} failed (${result.status}): ${result.stderr ?? ''}`)
  return result.stdout?.trim()
}

if (!existsSync(checkout)) {
  run('git', ['init', checkout])
  run('git', ['remote', 'add', 'origin', source.repository], checkout)
  run('git', ['fetch', '--depth=1', 'origin', source.commit], checkout)
  run('git', ['checkout', '--detach', 'FETCH_HEAD'], checkout)
}
const revision = run('git', ['rev-parse', 'HEAD'], checkout, true)
if (revision !== source.commit)
  throw new Error(`Expected Slidev ${source.commit}, found ${revision}; inspect .slidev before continuing`)
run('pnpm', ['install', '--frozen-lockfile'], checkout)
for (const name of ['types', 'parser', 'cli'])
  run('pnpm', ['--filter', `@slidev/${name}`, 'run', 'build'], checkout)
run('pnpm', ['install', '--frozen-lockfile'])
console.log('Slidev/Typst is ready. Run pnpm dev or pnpm build:pages. No experimental dataset is needed.')
