"""Top-level shim so users can run `python cli.py` directly."""

from __future__ import annotations

import sys

from src.cli import main

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
