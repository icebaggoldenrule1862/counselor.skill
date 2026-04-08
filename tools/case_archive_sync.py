#!/usr/bin/env python3
"""Sync a resolved case back into a long-term archive."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def unique_append(items: list[str], value: str) -> list[str]:
    if value and value not in items:
        items.append(value)
    return items


def upsert_thread(threads: list[dict], topic: str, status: str, last_mode: str, last_updated: str, next_risk: str) -> list[dict]:
    updated = []
    found = False
    for thread in threads:
        if thread.get("topic") == topic:
            updated.append(
                {
                    "topic": topic,
                    "status": status,
                    "last_mode": last_mode,
                    "last_updated": last_updated,
                    "next_risk": next_risk,
                }
            )
            found = True
        else:
            updated.append(thread)
    if not found:
        updated.append(
            {
                "topic": topic,
                "status": status,
                "last_mode": last_mode,
                "last_updated": last_updated,
                "next_risk": next_risk,
            }
        )
    return updated


def next_modes_for_result(result_tier: int | None, scene_type: str) -> list[str]:
    if result_tier is None:
        return ["debrief"]
    if result_tier <= 2:
        return ["debrief"]
    if result_tier == 3:
        return ["statement-writing", "debrief"]
    if result_tier == 4:
        return ["debrief", "repair", "statement-writing"]
    return ["debrief", "statement-writing", "repair"]


def sync_archive(archive: dict, state: dict) -> dict:
    result = state.get("result", {})
    result_tier = result.get("tier")
    scene_label = state.get("scene_label", state.get("scene_type", "未命名场景"))
    stage = state.get("stage", "unknown")
    updated_at = state.get("updated_at") or datetime.now().isoformat(timespec="seconds")
    latest_read = state.get("attitude", {}).get("current_read", "unknown")
    reasons = result.get("reasons", [])
    escalation = state.get("escalation", {})
    current_level = escalation.get("current_level", "watch")

    relationship = archive.setdefault("relationship_state", {})
    if result_tier is not None and result_tier >= 4:
        relationship["trust_trend"] = "declining"
    elif result_tier == 3:
        relationship["trust_trend"] = "fragile-but-recoverable"
    relationship["latest_read"] = f"{latest_read}; {result.get('label') or '待收口'}"
    if current_level in {"formal-watch", "formal"}:
        relationship["counselor_impression"] = "cautious-watch"

    risk = archive.setdefault("risk_ledger", {})
    active_flags = risk.setdefault("active_flags", [])
    historical_flags = risk.setdefault("historical_flags", [])
    protected_areas = risk.setdefault("protected_areas", [])
    watchpoints = risk.setdefault("escalation_watchpoints", [])
    historical_flags = unique_append(historical_flags, scene_label)
    risk["historical_flags"] = historical_flags
    if result_tier is not None and result_tier >= 3:
        active_flags = unique_append(active_flags, f"{scene_label}仍需后续跟进")
    if result_tier is not None and result_tier <= 2:
        protected_areas = unique_append(protected_areas, "本轮愿意配合处理")
    for reason in reasons:
        if "说明" in reason or "配合" in reason:
            protected_areas = unique_append(protected_areas, "愿意补说明和配合流程")
        if "风险" in reason or "记录" in reason:
            watchpoints = unique_append(watchpoints, f"{scene_label}主题后续仍需观察")
    risk["active_flags"] = active_flags
    risk["protected_areas"] = protected_areas
    risk["escalation_watchpoints"] = watchpoints

    threads = archive.setdefault("active_threads", [])
    if result_tier is not None and result_tier <= 2:
        thread_status = "watching"
    elif result_tier == 3:
        thread_status = "ongoing"
    else:
        thread_status = "formal-watch"
    next_risk = (escalation.get("likely_next_steps") or ["继续观察后续处理"]).copy()[0]
    archive["active_threads"] = upsert_thread(
        threads,
        scene_label,
        thread_status,
        stage,
        updated_at,
        next_risk,
    )

    notes = archive.setdefault("longitudinal_notes", [])
    summary_bits = []
    if result.get("label"):
        summary_bits.append(result["label"])
    if reasons:
        summary_bits.append(reasons[0])
    if summary_bits:
        note = f"{scene_label}本轮结果：{'；'.join(summary_bits)}"
        if note not in notes:
            notes.append(note)

    archive["recommended_next_modes"] = next_modes_for_result(result_tier, state.get("scene_type", ""))
    archive["updated_at"] = datetime.now().isoformat(timespec="seconds")
    return archive


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync a case result back into archive.json")
    parser.add_argument("--archive", required=True, help="Path to archive.json")
    parser.add_argument("--state", required=True, help="Path to case state.json")
    parser.add_argument("--out", help="Optional output path, defaults to updating archive in place")
    args = parser.parse_args()

    archive_path = Path(args.archive)
    state_path = Path(args.state)
    archive = read_json(archive_path)
    state = read_json(state_path)
    updated = sync_archive(archive, state)

    out_path = Path(args.out) if args.out else archive_path
    out_path.write_text(json.dumps(updated, ensure_ascii=False, indent=2), encoding="utf-8")
    print(out_path)


if __name__ == "__main__":
    main()
