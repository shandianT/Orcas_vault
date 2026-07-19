#!/usr/bin/env python3
"""Check traceability, state consistency, freshness, and confirmation load."""
from __future__ import annotations

import json
from datetime import date, datetime

from config import path as configured_path, relative, roots
from frontmatter import list_value, parse

VALID_TYPES = {"fact", "insight", "decision", "lesson", "rule", "entity"}
VALID_STATES = {"draft", "trusted", "verified", "stale", "disputed", "superseded"}
VALID_RESOLUTIONS = {"active", "disputed", "superseded"}


def main() -> int:
    findings: list[str] = []
    seen = set()
    knowledge = []
    for root in roots("knowledge_roots"):
        if not root.exists():
            continue
        for candidate in root.rglob("*.md"):
            resolved = candidate.resolve()
            if candidate.name != "README.md" and resolved not in seen:
                seen.add(resolved)
                knowledge.append(candidate)
    for candidate in knowledge:
        text = candidate.read_text(encoding="utf-8", errors="ignore")
        meta = parse(text)
        if meta.get("type") not in VALID_TYPES:
            findings.append(f"P0 {relative(candidate)}: type 无效或缺失")
        if meta.get("status") not in VALID_STATES:
            findings.append(f"P0 {relative(candidate)}: status 无效或缺失")
        if meta.get("resolution", "active") not in VALID_RESOLUTIONS:
            findings.append(f"P0 {relative(candidate)}: resolution 无效")
        if not meta.get("summary"):
            findings.append(f"P1 {relative(candidate)}: 缺少 summary")
        if meta.get("type") in {"fact", "insight"} and not list_value(meta, "sources"):
            findings.append(f"P1 {relative(candidate)}: 可验证知识缺少来源")
        if meta.get("status") in {"trusted", "verified"} and "当前状态为 draft" in text:
            findings.append(f"P0 {relative(candidate)}: frontmatter 与正文状态冲突")
        review = meta.get("review_after", "")
        if review:
            try:
                if datetime.strptime(str(review), "%Y-%m-%d").date() < date.today() and meta.get("status") in {"trusted", "verified"}:
                    findings.append(f"P1 {relative(candidate)}: trusted 已超过复核日期")
            except ValueError:
                findings.append(f"P1 {relative(candidate)}: review_after 日期格式错误")

    meta_root = configured_path("meta")
    rules_active = meta_root / "rules" / "active"
    rules_proposals = meta_root / "rules" / "proposals"
    for candidate in rules_active.glob("*.json") if rules_active.exists() else []:
        try:
            rule = json.loads(candidate.read_text(encoding="utf-8"))
            if rule.get("status") != "active":
                findings.append(f"P0 {candidate.name}: active 规则状态无效")
            if not isinstance(rule.get("version"), int) or rule.get("version", 0) < 1:
                findings.append(f"P0 {candidate.name}: active 规则版本无效")
            for key in ("scope", "exceptions", "side_effects", "validation", "rollback"):
                if key not in rule:
                    findings.append(f"P1 {candidate.name}: 规则缺少 {key}")
        except (OSError, json.JSONDecodeError):
            findings.append(f"P0 {candidate.name}: active 规则 JSON 无效")

    report_root = configured_path("reports")
    pending_root = report_root / "confirmations"
    pending = list(pending_root.glob("*.md")) if pending_root.exists() else []
    report_dir = report_root / "health"
    report_dir.mkdir(parents=True, exist_ok=True)
    report = report_dir / f"{date.today().isoformat()}.md"
    lines = [
        "# 健康检查", "", f"- 知识文件: {len(knowledge)}", f"- 待确认项: {len(pending)}",
        f"- 生效规则: {len(list(rules_active.glob('*.json'))) if rules_active.exists() else 0}",
        f"- 候选规则: {len(list(rules_proposals.glob('*.json'))) if rules_proposals.exists() else 0}",
        f"- 问题数: {len(findings)}", "", "## 问题"
    ]
    lines += [f"- {item}" for item in findings] or ["- 未发现问题"]
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(relative(report))
    for item in findings:
        print(item)
    return 1 if any(item.startswith("P0") for item in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
