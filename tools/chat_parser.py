#!/usr/bin/env python3
"""Extract counselor pressure style from simple chat logs."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path


COUNSELOR_HINTS = ["老师", "导员", "辅导员", "周老师", "王老师", "李老师"]


def parse_messages(text: str) -> list[dict[str, str]]:
    lines = [line.rstrip() for line in text.splitlines()]
    messages: list[dict[str, str]] = []
    current: dict[str, str] | None = None

    header_re = re.compile(r"^(.+?)\s+\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}$")

    for line in lines:
        if not line.strip():
            continue
        header = header_re.match(line)
        if header:
            if current:
                messages.append(current)
            current = {"speaker": header.group(1).strip(), "content": ""}
            continue
        if current is None:
            continue
        current["content"] = f"{current['content']}\n{line}".strip()

    if current:
        messages.append(current)
    return messages


def is_counselor(speaker: str) -> bool:
    return any(hint in speaker for hint in COUNSELOR_HINTS)


def analyze(text: str) -> dict:
    messages = parse_messages(text)
    counselor_msgs = [m["content"] for m in messages if is_counselor(m["speaker"])]
    merged = "\n".join(counselor_msgs)
    markers = Counter()

    for token in [
        "先说",
        "先别解释",
        "不是",
        "登记",
        "反馈",
        "情况",
        "解释",
        "不报备",
        "不行",
        "都一致",
        "大家都",
        "可以去",
        "反正",
        "就一个月",
        "没法",
        "登录不了",
        "你就",
        "来补",
        "下午2点",
        "A412",
    ]:
        count = merged.count(token)
        if count:
            markers[token] = count

    bureaucratic_markers = [
        token for token in ["不行", "都一致", "大家都", "反正", "就一个月", "你就"] if token in merged
    ]

    dismissal_markers = [
        token for token in ["不行", "可以去", "反正", "没法", "登录不了"] if token in merged
    ]

    delay_markers = [
        token for token in ["来补", "下午2点", "A412"] if token in merged
    ]

    return {
        "source_type": "chat",
        "message_count": len(messages),
        "counselor_message_count": len(counselor_msgs),
        "pressure_markers": dict(markers),
        "behavior_signals": {
            "follow_up_pressure": "progressive" if any(
                token in merged for token in ["先说", "先别解释", "情况", "解释"]
            ) else "light",
            "teacher_like_probing": any(token in merged for token in ["先说", "解释", "情况"]),
            "uniformity_pressure": bool(bureaucratic_markers),
            "dismissive_boundary": bool(dismissal_markers),
            "delay_and_redirect": bool(delay_markers),
        },
        "rule_signals": {
            "chat_markers": dict(markers),
            "bureaucratic_markers": bureaucratic_markers,
            "dismissal_markers": dismissal_markers,
            "delay_markers": delay_markers,
        },
        "sample_counselor_messages": counselor_msgs[:5],
        "tone_guess": (
            "bureaucratic-rigid"
            if bureaucratic_markers
            else "progressive-pressure" if markers else "neutral"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Parse counselor chat logs")
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
