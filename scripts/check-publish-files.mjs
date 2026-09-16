// Check the Git index, not the working tree, before publishing the presentation.
import { execFileSync } from 'node:child_process'

const entries = execFileSync('git', ['ls-files', '--stage', '-z'], { encoding: 'utf8' })
  .split('\0').filter(Boolean)
const forbidden = []
for (const entry of entries) {
  const [metadata, path] = entry.split('\t')
  const mode = metadata.split(' ')[0]
  if (mode === '120000' || mode === '160000'
      || /(^|\/)(multi-distance-phase-retrieval|node_modules|\.slidev|\.audit|\.cache|\.venv|__pycache__|datasets?|papers)(\/|$)/i.test(path)
      || /\.(npz|npy|h5|hdf5|h5ad|tiff?|zarr|zip|pkl|pickle|pt|pth)$/i.test(path)
      || /(^|\/)\.env(?:\.|$)/.test(path))
    forbidden.push(path)
}
if (forbidden.length)
  throw new Error(`Refusing to publish local data, caches, or linked directories:\n${forbidden.join('\n')}`)
console.log(`Checked ${entries.length} staged/tracked files: no dataset files, caches, symlinks, or submodules.`)
