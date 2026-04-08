#!/usr/bin/env python3
"""Write a dated session summary for a counselor system."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Write a session summary markdown file")
    parser.add_argument("--dir", required=True, help="Sessions directory")
    parser.add_argument("--content-file", required=True, help="Summary markdown content file")
    args = parser.parse_args()

    session_dir = Path(args.dir)
    session_dir.mkdir(parents=True, exist_ok=True)
    content = Path(args.content_file).read_text(encoding="utf-8")
    name = datetime.now().strftime("%Y%m%d_%H%M%S") + ".md"
    out_path = session_dir / name
    out_path.write_text(content, encoding="utf-8")
    print(out_path)


if __name__ == "__main__":
    main()
