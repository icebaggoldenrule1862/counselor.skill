#!/usr/bin/env python3
"""Extract high-confidence counselor behavior hints from manual notes."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


PATTERN_RULES = [
    ("不会一上来", "first-round-soft"),
    ("先听你说", "listen-first"),
    ("慢慢收口", "progressive-pressure"),
    ("爱拿任课老师", "teacher-feedback-early"),
    ("不太会提家长", "family-link-late"),
    ("嘴上温和", "soft-surface"),
    ("流程很重", "process-heavy"),
    ("官僚主义极强", "bureaucratic-heavy"),
    ("不懂变通", "rigid-no-flex"),
    ("喜欢吹嘘", "self-credit-heavy"),
    ("打压", "student-suppression"),
    ("任务分配极其不合理", "unfair-task-loading"),
    ("统一要求", "uniformity-first"),
    ("控制欲很强", "control-heavy"),
]


def analyze(text: str) -> dict:
    hints = []
    for phrase, label in PATTERN_RULES:
        if phrase in text:
            hints.append({"phrase": phrase, "label": label})

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    correction_candidates = [line for line in lines if any(key in line for key in ["不会", "更像", "其实", "一般"])]

    return {
        "source_type": "manual-profile",
        "behavior_signals": {
            "high_confidence_hints": hints,
            "manual_impression_count": len(lines),
        },
        "correction_candidates": correction_candidates[:8],
        "tone_guess": "manual-impression",
        "sample_lines": lines[:6],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Parse manual counselor profile notes")
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
