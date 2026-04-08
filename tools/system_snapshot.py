#!/usr/bin/env python3
"""Build a concise snapshot for a counselor system directory."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8-sig"))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig") if path.exists() else ""


def first_heading(path: Path) -> str | None:
    for line in read_text(path).splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return None


def latest_paths(folder: Path, limit: int = 3) -> list[Path]:
    if not folder.exists():
        return []
    return sorted(item for item in folder.iterdir() if item.is_file())[-limit:]


def latest_names(folder: Path, limit: int = 3) -> list[str]:
    return [path.name for path in latest_paths(folder, limit)]


def file_count(folder: Path) -> int:
    if not folder.exists():
        return 0
    return sum(1 for item in folder.iterdir() if item.is_file())


def extract_session_meta(path: Path) -> dict:
    info = {"file": path.name, "date": None, "mode": None, "next_step": None}
    waiting_next_step = False

    for raw_line in read_text(path).splitlines():
        line = raw_line.strip()
        if line.startswith("- 日期："):
            info["date"] = line.split("：", 1)[1].strip()
        elif line.startswith("- 模式："):
            info["mode"] = line.split("：", 1)[1].strip()
        elif line.startswith("## 下次可以继续"):
            waiting_next_step = True
        elif waiting_next_step and line:
            info["next_step"] = line
            break

    return info


def build_snapshot(system_dir: Path) -> dict:
    meta = read_json(system_dir / "meta.json")
    archive = read_json(system_dir / "archive.json")
    distillation_impact = read_json(system_dir / "distillation-impact.json")
    authenticity_report = read_json(system_dir / "distillation-authenticity-report.json")

    persona_name = first_heading(system_dir / "persona.md")
    sessions_dir = system_dir / "sessions"
    corrections_dir = system_dir / "corrections"
    session_paths = latest_paths(sessions_dir, 9999)
    correction_paths = latest_paths(corrections_dir, 9999)
    latest_correction = read_json(correction_paths[-1]) if correction_paths else {}
    session_meta = [extract_session_meta(path) for path in session_paths]

    modes_seen: list[str] = []
    for item in session_meta:
        mode = item.get("mode")
        if mode and mode not in modes_seen:
            modes_seen.append(mode)

    return {
        "system_name": meta.get("name") or persona_name or system_dir.name,
        "slug": meta.get("slug", system_dir.name),
        "version": meta.get("version"),
        "archetype": meta.get("archetype"),
        "mode_focus": meta.get("mode_focus", []),
        "memory_enabled": meta.get("memory_enabled", False),
        "created_at": meta.get("created_at"),
        "updated_at": meta.get("updated_at"),
        "counts": {
            "sessions": file_count(sessions_dir),
            "corrections": file_count(corrections_dir),
        },
        "modes_seen": modes_seen,
        "archive_summary": {
            "current_focus": archive.get("student_profile", {}).get("current_focus", []),
            "active_flags": archive.get("risk_ledger", {}).get("active_flags", []),
            "active_threads": [item.get("topic") for item in archive.get("active_threads", [])],
            "recommended_next_modes": archive.get("recommended_next_modes", []),
        },
        "correction_summary": {
            "summary": latest_correction.get("summary"),
            "stable_constraints": latest_correction.get("stable_constraints", []),
            "change_keys": list(latest_correction.get("changes", {}).keys()),
        },
        "distillation_summary": {
            "system_effect_keys": list(distillation_impact.get("system_effects", {}).keys()),
            "recommended_updates": distillation_impact.get("recommended_updates", []),
        },
        "authenticity_summary": {
            "score": authenticity_report.get("authenticity_score"),
            "band": authenticity_report.get("authenticity_band"),
            "ready_modes": authenticity_report.get("real_world_sync_readiness", {}).get("ready_modes", []),
            "summary": authenticity_report.get("operator_judgement", {}).get("summary"),
        },
        "latest": {
            "sessions": latest_names(sessions_dir),
            "corrections": latest_names(corrections_dir),
            "session_meta": session_meta[-3:],
            "latest_correction_summary": latest_correction.get("summary"),
        },
        "notes": meta.get("notes", []),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a system snapshot json")
    parser.add_argument("--dir", required=True, help="Counselor system directory")
    parser.add_argument("--out", help="Output file path, defaults to snapshot.json under the system directory")
    args = parser.parse_args()

    system_dir = Path(args.dir).resolve()
    snapshot = build_snapshot(system_dir)
    out_path = Path(args.out).resolve() if args.out else system_dir / "snapshot.json"
    out_path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
    print(out_path)


if __name__ == "__main__":
    main()
