#!/usr/bin/env python3
"""Extract pressure rhythm from meeting or office-talk transcripts."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


TOKENS = [
    "我再强调一次",
    "不是跟你商量",
    "先把情况说清楚",
    "后果",
    "记录",
    "约谈",
    "上报",
    "先听你说",
    "任课老师",
    "班长",
    "家长",
]


def analyze(text: str) -> dict:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    markers = Counter()
    for token in TOKENS:
        count = text.count(token)
        if count:
            markers[token] = count

    rhythm = []
    if "先听你说" in text or "先把情况说清楚" in text:
        rhythm.append("listen-first")
    if "任课老师" in text:
        rhythm.append("teacher-feedback-early")
    if "班长" in text:
        rhythm.append("monitor-feedback-mid")
    if "家长" in text:
        rhythm.append("family-link-present")

    return {
        "source_type": "meeting",
        "line_count": len(lines),
        "pressure_markers": dict(markers),
        "behavior_signals": {
            "pressure_rhythm": rhythm,
            "long_form_pressure": bool(lines and len(lines) >= 4),
        },
        "tone_guess": "meeting-pressure" if markers else "neutral",
        "sample_lines": lines[:6],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Parse meeting/office transcript text")
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
