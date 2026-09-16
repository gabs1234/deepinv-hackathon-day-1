"""Delegate scientific work to the linked phase-retrieval repository."""
from pathlib import Path
import runpy
import sys

ROOT = Path(__file__).resolve().parents[1]
REPO = (ROOT / "multi-distance-phase-retrieval").resolve()
ENTRY = REPO / "scripts/render-tie-introduction.py"

if __name__ == "__main__":
    if not ENTRY.is_file():
        raise SystemExit(f"Missing repository entry point: {ENTRY}")
    cache = REPO / ".cache/phase-retrieval/converged"
    if not cache.exists():
        cache = REPO / ".cache/phase-retrieval/presentation"
    sys.argv = [str(ENTRY), "--converged-cache", str(cache),
                "--output", str(ROOT / "public/phase-retrieval"), *sys.argv[1:]]
    runpy.run_path(str(ENTRY), run_name="__main__")
