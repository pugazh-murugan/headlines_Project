"""Convenience entry point: `python main.py` (same as `python -m headlines`)."""

import sys

from headlines.cli import main

if __name__ == "__main__":
    sys.exit(main())
