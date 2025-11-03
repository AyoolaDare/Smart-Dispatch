"""
Top-level `app` package shim.

This package makes it possible to run `uvicorn app.main:app` from the
repository root by telling Python to look for submodules inside
`<repo_root>/backend/app`.

It avoids duplicating code and keeps the existing project layout.
"""
from pathlib import Path
import sys

# Resolve repo root and point to backend/app
_this_dir = Path(__file__).resolve().parent
_repo_root = _this_dir.parent
_backend_app = _repo_root / "backend" / "app"

if str(_backend_app) not in sys.path:
    # Add backend/app to the package search path for this package only.
    __path__.insert(0, str(_backend_app))
