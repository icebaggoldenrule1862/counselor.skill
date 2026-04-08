#!/usr/bin/env python3
"""Apply a JSON patch-like merge to a case state file."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any


def merge(base: Any, patch: Any) -> Any:
    if isinstance(base, dict) and isinstance(patch, dict):
        result = dict(base)
        for key, value in patch.items():
            if key in result:
                result[key] = merge(result[key], value)
            else:
                result[key] = value
        return result
    if isinstance(base, list) and isinstance(patch, list):
        return base + patch
    return patch


def main() -> None:
    parser = argparse.ArgumentParser(description="Update case state with a merge patch")
    parser.add_argument("--state", required=True, help="Path to state.json")
    parser.add_argument("--patch-file", required=True, help="Path to patch JSON")
    args = parser.parse_args()

    state_path = Path(args.state)
    patch_path = Path(args.patch_file)

    state = json.loads(state_path.read_text(encoding="utf-8-sig"))
    patch = json.loads(patch_path.read_text(encoding="utf-8-sig"))

    updated = merge(state, patch)
    updated["updated_at"] = datetime.now().isoformat(timespec="seconds")

    state_path.write_text(json.dumps(updated, ensure_ascii=False, indent=2), encoding="utf-8")
    print(state_path)


if __name__ == "__main__":
    main()
