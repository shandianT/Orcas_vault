#!/usr/bin/env python3
"""Show only pending or on-use confirmations worth human attention."""
from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

from config import path as configured_path, relative, roots
from frontmatter import parse


def integer(value: object) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def pending_confirmations() -> list[dict[str, object]]:
    folder = configured_path("reports") / "confirmations"
    results = []
    for candidate in sorted(folder.glob("*.md")) if folder.exists() else []:
        meta = parse(candidate.read_text(encoding="utf-8", errors="ignore"))
        if meta.get("status") == "pending":
            results.append({"reason": "pending_confirmation", "risk": meta.get("risk", "high"), "path": relative(candidate), "target": meta.get("target", "")})
    return results


def on_use_drafts() -> list[dict[str, object]]:
    results = []
    seen: set[Path] = set()
    for root in roots("knowledge_roots"):
        if not root.exists():
            continue
        for candidate in root.rglob("*.md"):
            resolved = candidate.resolve()
            if candidate.name == "README.md" or resolved in seen:
                continue
            seen.add(resolved)
            meta = parse(candidate.read_text(encoding="utf-8", errors="ignore"))
            if meta.get("status") != "draft" or meta.get("resolution", "active") != "active":
                continue
            uses = max(integer(meta.get("use_count")), integer(meta.get("reuse_count")))
            risk = str(meta.get("risk", meta.get("risk_level", "low")))
            if uses > 0 or risk in {"high", "critical"}:
                results.append({
                    "reason": "draft_in_use" if uses > 0 else "high_risk_draft",
                    "risk": risk,
                    "uses": uses,
                    "path": relative(candidate),
                    "summary": meta.get("summary", candidate.stem),
                    "sources": meta.get("sources", []),
                })
    return results


def stale_trusted() -> list[dict[str, object]]:
    results = []
    for root in roots("knowledge_roots"):
        if not root.exists():
            continue
        for candidate in root.rglob("*.md"):
            meta = parse(candidate.read_text(encoding="utf-8", errors="ignore"))
            status = "trusted" if meta.get("status") == "verified" else meta.get("status")
            review_after = str(meta.get("review_after") or meta.get("verification.review_after") or "")
            uses = max(integer(meta.get("use_count")), integer(meta.get("reuse_count")))
            if status == "trusted" and uses > 0 and review_after and review_after < date.today().isoformat():
                results.append({"reason": "trusted_review_due", "risk": "medium", "uses": uses, "path": relative(candidate), "review_after": review_after})
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="列出真正值得处理的确认事项")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    items = pending_confirmations() + on_use_drafts() + stale_trusted()
    items.sort(key=lambda item: ({"critical": 0, "high": 1, "medium": 2, "low": 3}.get(str(item.get("risk")), 4), str(item.get("path"))))
    if args.json:
        print(json.dumps({"count": len(items), "items": items}, ensure_ascii=False, indent=2))
        return 0
    if not items:
        print("当前没有需要人工处理的高价值确认事项。")
        return 0
    print(f"当前有 {len(items)} 项值得确认：")
    for index, item in enumerate(items, 1):
        print(f"{index}. [{item.get('risk', 'unknown')}] {item['path']} - {item['reason']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
