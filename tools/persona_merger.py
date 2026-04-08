#!/usr/bin/env python3
"""Merge counselor persona layers with stable priority.

Priority:
1. manual
2. corrections
3. distilled
4. archetype
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: str | None) -> dict[str, Any]:
    if not path:
        return {}
    file_path = Path(path)
    if not file_path.exists():
        return {}
    with file_path.open("r", encoding="utf-8-sig") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError(f"{file_path} must contain a JSON object")
    return data


def merge(base: Any, override: Any) -> Any:
    if override is None:
        return base
    if isinstance(base, dict) and isinstance(override, dict):
        result = dict(base)
        for key, value in override.items():
            if key in result:
                result[key] = merge(result[key], value)
            else:
                result[key] = value
        return result
    return override


def main() -> None:
    parser = argparse.ArgumentParser(description="Merge counselor persona layers")
    parser.add_argument("--archetype", help="Base archetype JSON")
    parser.add_argument("--distilled", help="Distilled evidence JSON")
    parser.add_argument("--corrections", help="Corrections JSON")
    parser.add_argument("--manual", help="Manual persona JSON")
    parser.add_argument("--output", required=True, help="Output JSON path")
    args = parser.parse_args()

    merged = {}
    for path in [args.archetype, args.distilled, args.corrections, args.manual]:
        merged = merge(merged, load_json(path))

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)

    print(f"merged persona written to {out_path}")


if __name__ == "__main__":
    main()
