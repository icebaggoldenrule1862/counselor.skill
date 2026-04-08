#!/usr/bin/env python3
"""Extract rule and escalation signals from school policy text."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


RULE_TOKENS = [
    "必须",
    "原则上",
    "不得",
    "上报",
    "批评教育",
    "书面说明",
    "约谈",
    "情节严重",
    "屡次发生",
    "第一时间反馈",
]


def analyze(text: str) -> dict:
    markers = Counter()
    for token in RULE_TOKENS:
        count = text.count(token)
        if count:
            markers[token] = count

    escalation_path = []
    for token in ["批评教育", "书面说明", "约谈", "上报"]:
        if token in text:
            escalation_path.append(token)

    return {
        "source_type": "policy",
        "rule_markers": dict(markers),
        "escalation_path": escalation_path,
        "behavior_signals": {
            "rule_hardness": "high" if markers else "medium",
        },
        "rule_signals": {
            "policy_markers": dict(markers),
            "escalation_path": escalation_path,
        },
        "tone_guess": "rule-heavy" if markers else "neutral",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Parse policy-style counselor text")
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
