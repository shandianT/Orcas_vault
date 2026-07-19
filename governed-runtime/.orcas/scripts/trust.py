#!/usr/bin/env python3
"""Explicitly promote one current draft knowledge item to trusted."""
from __future__ import annotations

import argparse
import re
from datetime import date, datetime, timezone
from pathlib import Path

from config import VAULT, relative
from frontmatter import parse, replace_scalar

DRAFT_SENTENCES = (
    "- 当前状态为 draft，尚未经过人工核实。",
    "- 当前状态为 draft，尚未经过人工确认。"
)


def promote(target: str, actor: str, evidence: str) -> Path:
    candidate = (VAULT / target).resolve()
    try:
        candidate.relative_to(VAULT.resolve())
    except ValueError as exc:
        raise SystemExit("目标必须位于 Vault 内") from exc
    if not candidate.is_file() or candidate.suffix != ".md":
        raise SystemExit("必须明确指定一个现有 Markdown 条目")
    text = candidate.read_text(encoding="utf-8")
    meta = parse(text)
    if meta.get("status") != "draft" or meta.get("resolution", "active") != "active":
        raise SystemExit("只能升级一个 active draft 条目")
    text = replace_scalar(text, "status", "trusted")
    text = replace_scalar(text, "updated", date.today().isoformat())
    for sentence in DRAFT_SENTENCES:
        text = text.replace(sentence, "- 当前状态为 trusted，已由人工明确确认。")
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    entry = f"- {stamp} 由 {actor} 明确确认。证据：{evidence or '当前对话中的明确确认'}"
    text = text.rstrip() + (f"\n{entry}\n" if "## 信任记录" in text else f"\n\n## 信任记录\n\n{entry}\n")
    candidate.write_text(text, encoding="utf-8")
    return candidate


def main() -> int:
    parser = argparse.ArgumentParser(description="将一个明确目标从 draft 升级为 trusted")
    parser.add_argument("target", help="单个知识文件路径，不接受目录或通配符")
    parser.add_argument("--actor", required=True)
    parser.add_argument("--evidence", default="")
    args = parser.parse_args()
    if any(char in args.target for char in "*?[]"):
        raise SystemExit("不允许通配或批量升级")
    print(relative(promote(args.target, args.actor, args.evidence)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
