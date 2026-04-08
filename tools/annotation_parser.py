#!/usr/bin/env python3
"""Extract statement-review and approval style signals from short annotations."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


TOKENS = ["重写", "补材料", "不完整", "重新提交", "先说明时间线", "审批", "不予通过", "先联系任课老师"]


def analyze(text: str) -> dict:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    markers = Counter()
    for token in TOKENS:
        count = text.count(token)
        if count:
            markers[token] = count

    return {
        "source_type": "annotation",
        "behavior_signals": {
            "document_strictness": "high" if markers else "medium",
            "material_focus": [token for token in ["补材料", "重新提交", "先说明时间线"] if token in text],
        },
        "rule_signals": {
            "approval_markers": dict(markers),
        },
        "tone_guess": "document-review",
        "sample_lines": lines[:6],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Parse annotation/review text")
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
