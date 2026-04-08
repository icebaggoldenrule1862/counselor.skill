#!/usr/bin/env python3
"""Update a long-term student archive with a merge patch."""

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


def default_archive() -> dict:
    return {
        "student_profile": {
            "display_name": "未命名学生",
            "grade": None,
            "department": None,
            "current_focus": [],
            "background_notes": [],
        },
        "communication_profile": {
            "preferred_style": [],
            "common_failure_points": [],
            "stable_strengths": [],
            "effective_moves": [],
        },
        "relationship_state": {
            "counselor_impression": "neutral",
            "trust_trend": "unknown",
            "latest_read": "unknown",
            "pressure_pattern": [],
        },
        "risk_ledger": {
            "active_flags": [],
            "historical_flags": [],
            "escalation_watchpoints": [],
            "protected_areas": [],
        },
        "active_threads": [],
        "longitudinal_notes": [],
        "recommended_next_modes": [],
        "updated_at": None,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Update archive.json with a merge patch")
    parser.add_argument("--archive", required=True, help="Path to archive.json")
    parser.add_argument("--patch-file", required=True, help="Path to patch JSON")
    args = parser.parse_args()

    archive_path = Path(args.archive)
    patch_path = Path(args.patch_file)

    archive = default_archive()
    if archive_path.exists():
        archive = merge(archive, json.loads(archive_path.read_text(encoding="utf-8-sig")))

    patch = json.loads(patch_path.read_text(encoding="utf-8-sig"))
    updated = merge(archive, patch)
    updated["updated_at"] = datetime.now().isoformat(timespec="seconds")

    archive_path.parent.mkdir(parents=True, exist_ok=True)
    archive_path.write_text(json.dumps(updated, ensure_ascii=False, indent=2), encoding="utf-8")
    print(archive_path)


if __name__ == "__main__":
    main()
