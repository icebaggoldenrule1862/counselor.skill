#!/usr/bin/env python3
"""Append correction records to a counselor persona markdown file."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path


def ensure_section(text: str) -> str:
    if "## Correction 记录" in text:
        return text
    return text.rstrip() + "\n\n## Correction 记录\n"


def append_correction(persona_path: Path, summary: str, payload: str) -> None:
    existing = persona_path.read_text(encoding="utf-8") if persona_path.exists() else "# Persona\n"
    existing = ensure_section(existing)
    timestamp = datetime.now().isoformat(timespec="seconds")
    block = (
        f"\n### Correction {timestamp}\n"
        f"- 摘要：{summary}\n"
        f"- 结构化修改：\n\n```json\n{payload.strip()}\n```\n"
    )
    persona_path.write_text(existing.rstrip() + block + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Append correction record to persona markdown")
    parser.add_argument("--persona", required=True, help="Persona markdown path")
    parser.add_argument("--summary", required=True, help="Short correction summary")
    parser.add_argument("--payload-file", required=True, help="JSON payload file")
    args = parser.parse_args()

    persona_path = Path(args.persona)
    payload = Path(args.payload_file).read_text(encoding="utf-8")
    persona_path.parent.mkdir(parents=True, exist_ok=True)
    append_correction(persona_path, args.summary, payload)
    print(persona_path)


if __name__ == "__main__":
    main()
