"""Delegate scientific work to the linked phase-retrieval repository."""
from pathlib import Path
import runpy
import sys

ROOT = Path(__file__).resolve().parents[1]
REPO = (ROOT / "multi-distance-phase-retrieval").resolve()
ENTRY = REPO / "scripts/converge-phase-retrieval.py"

if __name__ == "__main__":
    if not ENTRY.is_file():
        raise SystemExit(f"Missing repository entry point: {ENTRY}")
    sys.argv = [str(ENTRY), *sys.argv[1:]]
    runpy.run_path(str(ENTRY), run_name="__main__")
