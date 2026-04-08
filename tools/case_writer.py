#!/usr/bin/env python3
"""Initialize generated counselor and case folders."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path


SCENE_PRESETS = {
    "leave-request": {
        "scene_label": "请假申请",
        "stage": "opening",
        "known_info": ["学生主动来请假"],
        "hidden_evidence": ["是否存在关键课程安排", "近期请假频次"],
        "redlines": ["模糊理由重复出现", "关键课程临时请假"],
        "next_actions": ["确认请假理由", "确认课程影响"],
        "base_scores": {"impression_score": 0, "trust_level": 0, "evidence_level": 1, "risk_level": 1},
        "base_escalation_level": "watch",
    },
    "truancy": {
        "scene_label": "逃课被抓",
        "stage": "probing",
        "known_info": ["任课老师已反馈缺席问题"],
        "hidden_evidence": ["班长反馈", "考勤截图", "预警线情况"],
        "redlines": ["重复旷课", "继续嘴硬甩锅"],
        "next_actions": ["确认是否为重复问题", "决定何时亮证据"],
        "base_scores": {"impression_score": -1, "trust_level": 0, "evidence_level": 2, "risk_level": 2},
        "base_escalation_level": "watch",
    },
    "late-return": {
        "scene_label": "夜不归宿",
        "stage": "opening",
        "known_info": ["宿管已登记未归"],
        "hidden_evidence": ["宿舍长反馈", "历史未归记录"],
        "redlines": ["安全问题轻描淡写", "重复未归"],
        "next_actions": ["确认去向和时间线", "确认是否需要升级处理"],
        "base_scores": {"impression_score": 0, "trust_level": -1, "evidence_level": 2, "risk_level": 3},
        "base_escalation_level": "formal-watch",
    },
}


def slugify(value: str) -> str:
    cleaned = "".join(ch.lower() if ch.isascii() and ch.isalnum() else "-" for ch in value)
    while "--" in cleaned:
        cleaned = cleaned.replace("--", "-")
    cleaned = cleaned.strip("-")
    if cleaned:
        return cleaned
    digest = hashlib.sha1(value.encode("utf-8")).hexdigest()[:8]
    return f"item-{digest}"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def clamp(value: int, low: int = -3, high: int = 5) -> int:
    return max(low, min(high, value))


def build_archive_context(archive: dict) -> dict:
    student_profile = archive.get("student_profile", {})
    relationship_state = archive.get("relationship_state", {})
    risk_ledger = archive.get("risk_ledger", {})
    return {
        "current_focus": student_profile.get("current_focus", []),
        "active_flags": risk_ledger.get("active_flags", []),
        "active_threads": [item.get("topic") for item in archive.get("active_threads", [])],
        "counselor_impression": relationship_state.get("counselor_impression", "neutral"),
        "trust_trend": relationship_state.get("trust_trend", "unknown"),
        "pressure_pattern": relationship_state.get("pressure_pattern", []),
        "carry_over_notes": archive.get("longitudinal_notes", []),
    }


def score_overrides_from_archive(scene: str, archive: dict, preset: dict) -> dict:
    scores = dict(preset.get("base_scores", {}))
    active_flags = archive.get("risk_ledger", {}).get("active_flags", [])
    active_threads = archive.get("active_threads", [])
    relation = archive.get("relationship_state", {})
    communication = archive.get("communication_profile", {})

    if scene == "truancy" and any("考勤" in item for item in active_flags):
        scores["risk_level"] = clamp(scores.get("risk_level", 0) + 1)
        scores["impression_score"] = clamp(scores.get("impression_score", 0) - 1)
    if scene == "late-return" and any("安全" in item for item in active_flags):
        scores["risk_level"] = clamp(scores.get("risk_level", 0) + 1)
    if any(scene in (thread.get("topic") or "") for thread in active_threads):
        scores["risk_level"] = clamp(scores.get("risk_level", 0) + 1)
    if relation.get("trust_trend") == "fragile-but-recoverable":
        scores["trust_level"] = clamp(scores.get("trust_level", 0))
    if communication.get("effective_moves"):
        scores["trust_level"] = clamp(scores.get("trust_level", 0) + 1)
    return scores


def build_evidence_queue(scene: str, archive: dict, preset: dict) -> list[dict]:
    hidden = preset.get("hidden_evidence", [])
    queue = []
    for index, item in enumerate(hidden):
        queue.append(
            {
                "label": item,
                "source": "scene-preset",
                "reveal_stage": "probing" if index == 0 else "pressure",
                "impact": "medium",
                "revealed": False,
            }
        )
    for flag in archive.get("risk_ledger", {}).get("escalation_watchpoints", []):
        queue.append(
            {
                "label": flag,
                "source": "archive-watchpoint",
                "reveal_stage": "closure",
                "impact": "high",
                "revealed": False,
            }
        )
    return queue


def build_escalation(scene: str, archive: dict, preset: dict) -> dict:
    triggers = []
    active_flags = archive.get("risk_ledger", {}).get("active_flags", [])
    active_threads = archive.get("active_threads", [])
    level = preset.get("base_escalation_level", "watch")
    if scene == "truancy" and any("考勤" in item for item in active_flags):
        triggers.append("attendance-risk-repeat")
        level = "formal-watch"
    if scene == "late-return" and any("安全" in item for item in active_flags):
        triggers.append("safety-risk-repeat")
        level = "formal-watch"
    if active_threads:
        triggers.append("active-thread-overlap")
    likely_next_steps = list(preset.get("next_actions", []))
    if triggers:
        likely_next_steps.append("根据长期档案决定是否升级正式记录")
    trigger_log = []
    for item in triggers:
        trigger_log.append(f"已触发 {item}，本局起始升级压力抬高")
    return {
        "current_level": level,
        "likely_next_steps": likely_next_steps,
        "triggers_met": triggers,
        "trigger_log": trigger_log,
    }


def init_counselor(base_dir: Path, name: str) -> None:
    slug = slugify(name)
    folder = base_dir / "generated" / "counselors" / slug
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "sessions").mkdir(parents=True, exist_ok=True)
    (folder / "corrections").mkdir(parents=True, exist_ok=True)
    meta = {
        "name": name,
        "slug": slug,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "version": "0.1.0",
    }
    (folder / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    if not (folder / "persona.md").exists():
        (folder / "persona.md").write_text(f"# {name}\n\n## 核心定位\n- 待创建\n", encoding="utf-8")
    if not (folder / "archive.json").exists():
        archive = {
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
            "updated_at": datetime.now().isoformat(timespec="seconds"),
        }
        (folder / "archive.json").write_text(json.dumps(archive, ensure_ascii=False, indent=2), encoding="utf-8")
    print(folder)


def init_case(base_dir: Path, scene: str, archive_path: Path | None, persona_slug: str | None) -> None:
    slug = slugify(scene)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    folder = base_dir / "generated" / "cases" / f"{timestamp}-{slug}"
    folder.mkdir(parents=True, exist_ok=True)
    preset = SCENE_PRESETS.get(scene, {})
    now = datetime.now().isoformat(timespec="seconds")
    archive = read_json(archive_path) if archive_path and archive_path.exists() else {}
    state = {
        "case_id": f"{timestamp}-{slug}",
        "scene_type": scene,
        "scene_label": preset.get("scene_label", scene),
        "created_at": now,
        "updated_at": now,
        "stage": preset.get("stage", "opening"),
        "status": "active",
        "persona_slug": persona_slug,
        "student_profile": {
            "display_name": archive.get("student_profile", {}).get("display_name", "未命名学生"),
            "history_flags": archive.get("risk_ledger", {}).get("historical_flags", []),
            "recent_record": archive.get("student_profile", {}).get("background_notes", []),
        },
        "archive_context": build_archive_context(archive),
        "scores": score_overrides_from_archive(scene, archive, preset),
        "attitude": {
            "current_read": "unknown",
            "history": [],
        },
        "evidence_queue": build_evidence_queue(scene, archive, preset),
        "escalation": build_escalation(scene, archive, preset),
        "known_info": preset.get("known_info", []),
        "hidden_evidence": preset.get("hidden_evidence", []),
        "redlines": preset.get("redlines", []),
        "branch_notes": [],
        "result": {
            "tier": None,
            "label": None,
            "reasons": [],
        },
        "next_actions": preset.get("next_actions", []),
    }
    (folder / "state.json").write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    (folder / "case.md").write_text(
        f"# {preset.get('scene_label', scene)}\n\n## 场景记录\n\n## 已知信息\n\n## 隐藏证据\n\n## 分支记录\n",
        encoding="utf-8",
    )
    (folder / "transcript.md").write_text(f"# {preset.get('scene_label', scene)} 对局记录\n\n", encoding="utf-8")
    print(folder)


def main() -> None:
    parser = argparse.ArgumentParser(description="Initialize counselor or case folders")
    parser.add_argument("--mode", required=True, choices=["counselor", "case"])
    parser.add_argument("--name", required=True, help="Counselor name or scene name")
    parser.add_argument("--base-dir", default=".", help="Project root")
    parser.add_argument("--archive", help="Optional path to archive.json when initializing a case")
    parser.add_argument("--persona-slug", help="Optional persona slug for a case")
    args = parser.parse_args()

    base_dir = Path(args.base_dir).resolve()
    if args.mode == "counselor":
        init_counselor(base_dir, args.name)
    else:
        archive_path = Path(args.archive).resolve() if args.archive else None
        init_case(base_dir, args.name, archive_path, args.persona_slug)


if __name__ == "__main__":
    main()
