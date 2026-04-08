#!/usr/bin/env python3
"""Build a cross-mode correction impact snapshot from a correction JSON file."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


MODE_KEYS = ["opening", "follow-up", "office-talk", "debrief"]


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def build_snapshot(correction: dict) -> dict:
    changes = correction.get("changes", {})
    affected_dimensions = list(changes.keys())

    pressure = changes.get("pressure_style", {})
    coordination = changes.get("coordination_style", {})
    speech = changes.get("speech_style", {})

    mode_effects: dict[str, list[str]] = {key: [] for key in MODE_KEYS}

    if pressure.get("first_round_style") == "listen-first":
        mode_effects["opening"].append("第一轮先试探，不一上来把话说死")
        mode_effects["follow-up"].append("先让学生补时间线，再判断是否继续收口")
        mode_effects["office-talk"].append("开场先听解释，再决定何时亮任课老师反馈")
        mode_effects["debrief"].append("复盘时重点标记从哪一轮开始转硬")

    if pressure.get("evidence_reveal") == "progressive":
        mode_effects["opening"].append("保留部分底牌，不在第一条就全部亮证据")
        mode_effects["follow-up"].append("第二轮和第三轮才逐步加重证据")
        mode_effects["office-talk"].append("证据按队列揭示，先老师反馈，再班长补强")
        mode_effects["debrief"].append("复盘里强调证据如何一步步抬高压力")

    if pressure.get("family_contact_timing") == "late":
        mode_effects["opening"].append("不开场提家长，只保留为后段升级可能")
        mode_effects["follow-up"].append("只有持续失控时才提家长联动风险")
        mode_effects["office-talk"].append("家长联动作为高阶后果，不作为第一轮威慑")
        mode_effects["debrief"].append("说明为什么这轮还没到家长联动")

    if coordination.get("teacher_feedback") == "early":
        mode_effects["follow-up"].append("更早使用任课老师反馈来校准说法")
        mode_effects["office-talk"].append("任课老师反馈优先于班长反馈出现")

    if coordination.get("class_monitor_feedback") == "mid":
        mode_effects["office-talk"].append("班长反馈作为中段补强，而不是开场压人")
        mode_effects["debrief"].append("复盘时把班长反馈视为中段转折点")

    if speech.get("opening_preference"):
        mode_effects["opening"].append(f"常用开场倾向于“{speech['opening_preference']}”")

    stable_constraints = []
    if pressure.get("first_round_style") == "listen-first":
        stable_constraints.append("第一轮不得上来直接宣判")
    if pressure.get("family_contact_timing") == "late":
        stable_constraints.append("家长联动只能出现在后段升级语境")
    if pressure.get("evidence_reveal") == "progressive":
        stable_constraints.append("证据应分步揭示，不一次性铺满")

    return {
        "summary": correction.get("summary"),
        "affected_dimensions": affected_dimensions,
        "mode_effects": mode_effects,
        "stable_constraints": stable_constraints,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build correction impact snapshot")
    parser.add_argument("--correction", required=True, help="Path to correction json")
    parser.add_argument("--out", help="Output file path")
    args = parser.parse_args()

    correction_path = Path(args.correction)
    correction = read_json(correction_path)
    snapshot = build_snapshot(correction)
    out_path = Path(args.out) if args.out else correction_path.with_name("correction-impact.json")
    out_path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
    print(out_path)


if __name__ == "__main__":
    main()
