#!/usr/bin/env python3
"""Extract counselor style signals from notice-like text."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path


KEY_PHRASES = [
    "我再强调一次",
    "不要等",
    "必须",
    "后续不会只停留在口头提醒",
    "先说",
    "你先别解释",
    "按规定",
    "情况说明",
]


def split_lines(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if line.strip()]


def analyze(text: str) -> dict:
    lines = split_lines(text)
    phrase_hits = [phrase for phrase in KEY_PHRASES if phrase in text]
    pressure_markers = Counter()

    for token in ["必须", "不要", "不会", "提醒", "说明", "登记", "反馈", "学院"]:
        count = text.count(token)
        if count:
            pressure_markers[token] = count

    return {
        "source_type": "notice",
        "line_count": len(lines),
        "key_phrases": phrase_hits,
        "pressure_markers": dict(pressure_markers),
        "behavior_signals": {
            "command_heaviness": "high" if phrase_hits or pressure_markers else "low",
            "public_tone": "formal-pressure" if pressure_markers else "neutral",
        },
        "rule_signals": {
            "notice_markers": dict(pressure_markers),
            "key_phrases": phrase_hits,
        },
        "tone_guess": "formal-pressure" if pressure_markers else "neutral",
        "sample_lines": lines[:5],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Parse notice-style counselor text")
    parser.add_argument("--file", required=True, help="Input text file")
    parser.add_argument("--output", required=True, help="Output JSON file")
    args = parser.parse_args()

    text = Path(args.file).read_text(encoding="utf-8")
    result = analyze(text)
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(out_path)


if __name__ == "__main__":
    main()
