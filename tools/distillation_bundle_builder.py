#!/usr/bin/env python3
"""Merge multiple distillation analysis JSON files into one bundle."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a merged distillation bundle")
    parser.add_argument("--inputs", nargs="+", required=True, help="Input analysis json files")
    parser.add_argument("--output", required=True, help="Output bundle json file")
    args = parser.parse_args()

    sources = [read_json(Path(item)) for item in args.inputs]
    source_types = [item.get("source_type", "unknown") for item in sources]
    tone_counter = Counter(item.get("tone_guess", "unknown") for item in sources)
    behavior_signals = []
    rule_signals = []
    conflicts = []

    for item in sources:
        source_type = item.get("source_type", "unknown")
        behavior = item.get("behavior_signals", {})
        rules = item.get("rule_signals", {})
        if behavior:
            behavior_signals.append({"source_type": source_type, "signals": behavior})
        if rules:
            rule_signals.append({"source_type": source_type, "signals": rules})
        if item.get("correction_candidates"):
            conflicts.append(
                {
                    "source_type": source_type,
                    "type": "manual-correction-candidate",
                    "items": item["correction_candidates"][:4],
                }
            )

    bundle = {
        "source_count": len(sources),
        "source_types": source_types,
        "tone_profile": dict(tone_counter),
        "behavior_signals": behavior_signals,
        "rule_signals": rule_signals,
        "conflict_candidates": conflicts,
        "real_world_sync_targets": [
            "opening-message",
            "follow-up-reply",
            "office-talk-rehearsal",
            "statement-writing",
        ],
        "merge_summary": {
            "has_manual_profile": "manual-profile" in source_types,
            "has_meeting": "meeting" in source_types,
            "has_policy": "policy" in source_types,
            "has_chat": "chat" in source_types,
            "has_notice": "notice" in source_types,
            "has_annotation": "annotation" in source_types,
        },
    }

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(bundle, ensure_ascii=False, indent=2), encoding="utf-8")
    print(out_path)


if __name__ == "__main__":
    main()
