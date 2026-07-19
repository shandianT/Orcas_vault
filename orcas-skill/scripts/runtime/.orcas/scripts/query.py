#!/usr/bin/env python3
"""Zero-ceremony retrieval across configured knowledge roots."""
from __future__ import annotations

import argparse
from pathlib import Path

from config import VAULT, relative
from context import knowledge_files, normalized_status, rank, resolution
from frontmatter import list_value
from usage import record


def candidates(question: str, limit: int, status: str, kind: str) -> list[tuple[int, dict[str, object], Path]]:
    ranked = sorted((rank(question, candidate) for candidate in knowledge_files()), key=lambda item: (-item[0], str(item[2])))
    result = []
    for item in ranked:
        meta = item[1]
        if int(meta.get("_term_overlap", 0)) <= 0 or resolution(meta) == "superseded":
            continue
        if status != "all" and normalized_status(meta) != status:
            continue
        is_entity = meta.get("type") == "entity"
        if kind == "entity" and not is_entity:
            continue
        if kind == "knowledge" and is_entity:
            continue
        if kind == "decision" and meta.get("type") != "decision":
            continue
        result.append(item)
    return result[:limit]


def render(question: str, items: list[tuple[int, dict[str, object], Path]]) -> str:
    lines = [f"# 查询：{question}", ""]
    if not items:
        return "\n".join(lines + ["未找到足够相关的知识。", "", "## 来源", "", "- 暂无来源"])
    lines += ["## 可用结论", ""]
    for _, meta, candidate in items:
        certainty = "可信" if normalized_status(meta) == "trusted" and resolution(meta) == "active" else "候选，需核实"
        lines.append(f"- {meta.get('summary') or candidate.stem}（{certainty}，置信度 {meta.get('confidence', '未标注')}）")
    sources: list[str] = []
    for _, meta, candidate in items:
        for value in [relative(candidate), *list_value(meta, "sources")]:
            if value not in sources:
                sources.append(value)
    lines += ["", "## 来源", ""] + [f"- {source}" for source in sources]
    lines += ["", "## 边界", "", "- draft、stale 或 disputed 内容只作为候选，不作为确定事实。"]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="直接查询知识，不创建项目文件")
    parser.add_argument("question")
    parser.add_argument("--limit", type=int, default=6)
    parser.add_argument("--status", choices=["all", "trusted", "draft", "stale"], default="all")
    parser.add_argument("--kind", choices=["all", "knowledge", "entity", "decision"], default="all")
    parser.add_argument("--adopt", action="store_true", help="记录本次检索结果被实际采用")
    args = parser.parse_args()
    items = candidates(args.question, max(1, args.limit), args.status, args.kind)
    print(render(args.question, items))
    record("query", args.question, [item[2] for item in items], adopted=args.adopt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
