#!/usr/bin/env python3
"""Build an authenticity report from a distillation bundle."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


SOURCE_LABELS = {
    "chat": "私聊 / 追问记录",
    "meeting": "班会 / 办公室转写",
    "policy": "制度文本",
    "annotation": "批注 / 审批反馈",
    "manual-profile": "用户手打印象",
    "notice": "通知 / 公告",
}


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def authenticity_band(score: int) -> str:
    if score >= 85:
        return "high"
    if score >= 65:
        return "medium"
    return "low"


def has_source(bundle: dict, source_type: str) -> bool:
    return source_type in set(bundle.get("source_types", []))


def dimension_scores(bundle: dict) -> tuple[dict, list[str], list[str]]:
    strengths: list[str] = []
    gaps: list[str] = []

    tone_score = 0
    if has_source(bundle, "chat"):
        tone_score += 35
        strengths.append("有私聊 / 追问记录，能校准真实接话方式。")
    else:
        gaps.append("缺少私聊 / 追问记录，第一句话和下一句的真实性不够稳。")
    if has_source(bundle, "notice"):
        tone_score += 25
        strengths.append("有通知 / 公告，能校准公开场景的纪律语气。")
    else:
        gaps.append("缺少通知 / 公告，公开语气层可能会偏软或偏虚。")
    if has_source(bundle, "manual-profile"):
        tone_score += 20
        strengths.append("有用户手打印象，能压住最容易跑偏的人格边界。")
    else:
        gaps.append("缺少用户手打印象，系统更容易蒸成泛化的“辅导员形象”。")
    if bundle.get("tone_profile"):
        tone_score += 20
    tone_score = min(tone_score, 100)

    pursuit_score = 0
    if has_source(bundle, "chat"):
        pursuit_score += 45
    if has_source(bundle, "meeting"):
        pursuit_score += 35
        strengths.append("有班会 / 办公室转写，能校准高压追问节奏。")
    else:
        gaps.append("缺少班会 / 办公室转写，约谈节奏和压迫方式会偏虚。")
    if any(item.get("source_type") == "meeting" for item in bundle.get("behavior_signals", [])):
        pursuit_score += 20
    pursuit_score = min(pursuit_score, 100)

    rule_score = 0
    if has_source(bundle, "policy"):
        rule_score += 45
        strengths.append("有制度文本，能校准规则路径和升级边界。")
    else:
        gaps.append("缺少制度文本，系统容易只会像在说话，不会像在办事。")
    if has_source(bundle, "notice"):
        rule_score += 20
    if has_source(bundle, "annotation"):
        rule_score += 20
        strengths.append("有批注 / 审批反馈，能校准说明文和补材料标准。")
    else:
        gaps.append("缺少批注 / 审批反馈，说明文工坊的真实性不够实。")
    if bundle.get("rule_signals"):
        rule_score += 15
    rule_score = min(rule_score, 100)

    closing_score = 0
    if has_source(bundle, "meeting"):
        closing_score += 35
    if has_source(bundle, "annotation"):
        closing_score += 25
    if has_source(bundle, "manual-profile"):
        closing_score += 25
    if bundle.get("conflict_candidates"):
        closing_score += 15
        strengths.append("已经识别到需要人工确认的冲突点，后续更容易做校准。")
    closing_score = min(closing_score, 100)
    if closing_score < 60:
        gaps.append("收口方式相关素材还不够，系统可能会在“给台阶”和“正式留痕”之间混掉。")

    scores = {
        "tone_authenticity": tone_score,
        "pursuit_logic": pursuit_score,
        "rule_path": rule_score,
        "closing_pattern": closing_score,
    }
    return scores, strengths, gaps


def overall_score(scores: dict, bundle: dict) -> int:
    base = round(
        scores["tone_authenticity"] * 0.30
        + scores["pursuit_logic"] * 0.30
        + scores["rule_path"] * 0.25
        + scores["closing_pattern"] * 0.15
    )
    if bundle.get("source_count", 0) >= 5:
        base += 5
    return min(base, 100)


def mode_readiness(bundle: dict, scores: dict) -> dict:
    opening_ready = scores["tone_authenticity"] >= 60
    follow_up_ready = scores["tone_authenticity"] >= 55 and scores["pursuit_logic"] >= 55
    office_talk_ready = scores["pursuit_logic"] >= 65 and scores["rule_path"] >= 55
    statement_ready = scores["rule_path"] >= 60

    return {
        "opening": {
            "ready": opening_ready,
            "reason": "已具备较稳定的第一句话语气校准。" if opening_ready else "第一句话和接话逻辑还不够稳。",
        },
        "follow_up": {
            "ready": follow_up_ready,
            "reason": "已具备较稳定的追问节奏。" if follow_up_ready else "被追问后的节奏还需要更多私聊或转写素材。",
        },
        "office_talk": {
            "ready": office_talk_ready,
            "reason": "已具备办公室高压预演所需的节奏和规则路径。" if office_talk_ready else "办公室场景仍缺少高压节奏或升级路径证据。",
        },
        "statement_writing": {
            "ready": statement_ready,
            "reason": "已具备说明文结构和打回点的规则基础。" if statement_ready else "说明文相关规则和批注证据仍偏弱。",
        },
    }


def recommended_next_sources(bundle: dict, scores: dict) -> list[dict]:
    recommendations: list[dict] = []

    if not has_source(bundle, "chat"):
        recommendations.append(
            {
                "source_type": "chat",
                "label": SOURCE_LABELS["chat"],
                "why": "最能提升第一句话和下一句的真实性。",
            }
        )
    if not has_source(bundle, "meeting"):
        recommendations.append(
            {
                "source_type": "meeting",
                "label": SOURCE_LABELS["meeting"],
                "why": "最能提升办公室约谈和高压节奏的真实性。",
            }
        )
    if not has_source(bundle, "annotation") and scores["rule_path"] < 80:
        recommendations.append(
            {
                "source_type": "annotation",
                "label": SOURCE_LABELS["annotation"],
                "why": "最能提升说明文、补材料、审批反馈这层真实性。",
            }
        )
    if not has_source(bundle, "manual-profile"):
        recommendations.append(
            {
                "source_type": "manual-profile",
                "label": SOURCE_LABELS["manual-profile"],
                "why": "最能压住“最像 / 最不像”的高优先级边界。",
            }
        )
    if not has_source(bundle, "policy"):
        recommendations.append(
            {
                "source_type": "policy",
                "label": SOURCE_LABELS["policy"],
                "why": "最能提升规则路径和升级边界的真实性。",
            }
        )

    return recommendations[:3]


def build_report(bundle: dict) -> dict:
    scores, strengths, gaps = dimension_scores(bundle)
    score = overall_score(scores, bundle)
    readiness = mode_readiness(bundle, scores)
    ready_modes = [name for name, item in readiness.items() if item["ready"]]

    return {
        "authenticity_score": score,
        "authenticity_band": authenticity_band(score),
        "dimension_scores": scores,
        "strengths": strengths,
        "gaps": gaps,
        "real_world_sync_readiness": {
            "ready_modes": ready_modes,
            "mode_readiness": readiness,
            "can_sync_now": len(ready_modes) >= 2,
            "needs_more_sources": len(ready_modes) < 2,
        },
        "recommended_next_sources": recommended_next_sources(bundle, scores),
        "operator_judgement": {
            "summary": (
                "这套蒸馏已经足够支持真实排练，并能给出可同步到现实的结果。"
                if score >= 85
                else "这套蒸馏已经可以开始用，但仍建议继续补素材让系统更稳。"
                if score >= 65
                else "这套蒸馏还更适合预览和试跑，不建议直接拿去现实同步。"
            )
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build distillation authenticity report")
    parser.add_argument("--bundle", required=True, help="Path to distillation bundle json")
    parser.add_argument("--output", required=True, help="Output report json path")
    args = parser.parse_args()

    bundle = read_json(Path(args.bundle))
    report = build_report(bundle)
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(out_path)


if __name__ == "__main__":
    main()
