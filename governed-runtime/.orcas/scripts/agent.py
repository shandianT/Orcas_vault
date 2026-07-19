#!/usr/bin/env python3
"""Validate and execute a small, provider-neutral Agent action contract."""
from __future__ import annotations

import argparse
import json
import shutil
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

from config import VAULT, path as configured_path, relative
from context import new_task
from entity import KINDS, append as append_entity, create as create_entity, entity_path
from frontmatter import parse
from intake import PROCESSED, SOURCES, target_for

PROTOCOL = "orcas-action-v1"
SUPPORTED_ACTIONS = {
    "ingest_source",
    "upsert_entity",
    "append_entity_timeline",
    "create_task",
    "create_action_item",
    "create_confirmation",
}


def fail(message: str) -> None:
    raise SystemExit(message)


def require_text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        fail(f"{field} 必须是非空字符串")
    return value.strip()


def require_list(value: Any, field: str) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        fail(f"{field} 必须是字符串数组")
    return [item.strip() for item in value if item.strip()]


def vault_path(value: str, field: str) -> Path:
    candidate = (VAULT / require_text(value, field)).resolve()
    try:
        candidate.relative_to(VAULT.resolve())
    except ValueError as exc:
        raise SystemExit(f"{field} 必须位于 Vault 内") from exc
    return candidate


def source_path(value: str, planned_sources: set[Path]) -> Path:
    candidate = vault_path(value, "source")
    try:
        candidate.relative_to(SOURCES.resolve())
    except ValueError as exc:
        raise SystemExit("source 必须位于 sources/ 内") from exc
    if not candidate.is_file() and candidate not in planned_sources:
        fail(f"来源不存在: {relative(candidate)}")
    return candidate


def action_item_path(summary: str) -> Path:
    from context import slug

    return configured_path("projects") / f"{date.today().isoformat()}-action-{slug(summary)}.md"


def task_path(goal: str) -> Path:
    from context import slug

    return configured_path("projects") / f"{date.today().isoformat()}-{slug(goal)}.md"


def confirmation_path(target: str) -> Path:
    from confirm import slug

    return configured_path("reports") / "confirmations" / f"{date.today().isoformat()}-{slug(target)}.md"


def reserve_output(candidate: Path, planned_outputs: set[Path]) -> None:
    resolved = candidate.resolve()
    if candidate.exists() or resolved in planned_outputs:
        fail(f"目标已存在或在同一请求中重复: {relative(candidate)}")
    planned_outputs.add(resolved)


def validate_action(action: Any, index: int, planned_sources: set[Path], planned_outputs: set[Path]) -> dict[str, Any]:
    if not isinstance(action, dict):
        fail(f"actions[{index}] 必须是对象")
    kind = require_text(action.get("type"), f"actions[{index}].type")
    if kind not in SUPPORTED_ACTIONS:
        fail(f"不支持的操作: {kind}")
    if action.get("status") not in {None, "draft", "active", "open"}:
        fail(f"{kind} 不允许请求 trusted 或其他受保护状态")

    normalized = dict(action)
    normalized["type"] = kind
    if kind == "ingest_source":
        inbox = configured_path("inbox").resolve()
        candidate = vault_path(require_text(action.get("path"), "path"), "path")
        try:
            candidate.relative_to(inbox)
        except ValueError as exc:
            raise SystemExit("ingest_source 只能处理 inbox/ 中的文件") from exc
        if not candidate.is_file() or candidate.name == "README.md":
            fail(f"待封存文件不存在: {relative(candidate)}")
        normalized["path"] = relative(candidate)
        normalized["target"] = relative(target_for(candidate))
        planned_sources.add((VAULT / normalized["target"]).resolve())
    elif kind in {"upsert_entity", "append_entity_timeline"}:
        entity_kind = require_text(action.get("kind"), "kind")
        if entity_kind not in KINDS:
            fail(f"未知实体类型: {entity_kind}")
        name = require_text(action.get("name"), "name")
        normalized["kind"] = entity_kind
        normalized["name"] = name
        normalized["source"] = relative(source_path(require_text(action.get("source"), "source"), planned_sources))
        target = entity_path(entity_kind, name)
        if target.exists():
            meta = parse(target.read_text(encoding="utf-8"))
            status = "trusted" if meta.get("status") == "verified" else meta.get("status", "draft")
            if status != "draft" or meta.get("resolution", "active") != "active":
                fail(f"Agent 不能修改受保护实体: {relative(target)}")
        if kind == "upsert_entity":
            normalized["aliases"] = require_list(action.get("aliases"), "aliases")
            normalized["tags"] = require_list(action.get("tags"), "tags")
        else:
            normalized["note"] = require_text(action.get("note"), "note")
            normalized["date"] = str(action.get("date") or date.today().isoformat())
    elif kind == "create_task":
        normalized["goal"] = require_text(action.get("goal"), "goal")
        reserve_output(task_path(normalized["goal"]), planned_outputs)
    elif kind == "create_action_item":
        summary = require_text(action.get("summary"), "summary")
        normalized["summary"] = summary
        normalized["owner"] = str(action.get("owner") or "").strip()
        normalized["due"] = str(action.get("due") or "").strip()
        normalized["source"] = relative(source_path(require_text(action.get("source"), "source"), planned_sources))
        reserve_output(action_item_path(summary), planned_outputs)
    elif kind == "create_confirmation":
        normalized["target"] = require_text(action.get("target"), "target")
        normalized["suggestion"] = require_text(action.get("suggestion"), "suggestion")
        normalized["evidence"] = str(action.get("evidence") or "").strip()
        normalized["uncertainty"] = str(action.get("uncertainty") or "").strip()
        reserve_output(confirmation_path(normalized["target"]), planned_outputs)
    return normalized


def validate_request(raw: Any) -> dict[str, Any]:
    if not isinstance(raw, dict):
        fail("请求必须是 JSON 对象")
    if raw.get("protocol") != PROTOCOL:
        fail(f"protocol 必须是 {PROTOCOL}")
    request_id = require_text(raw.get("request_id"), "request_id")
    actions = raw.get("actions")
    if not isinstance(actions, list) or not actions:
        fail("actions 必须是非空数组")
    planned_sources: set[Path] = set()
    planned_outputs: set[Path] = set()
    normalized_actions = []
    for index, action in enumerate(actions):
        normalized_actions.append(validate_action(action, index, planned_sources, planned_outputs))
    return {
        "protocol": PROTOCOL,
        "request_id": request_id,
        "intent": str(raw.get("intent") or "").strip(),
        "actions": normalized_actions,
    }


def ingest(path_value: str) -> Path:
    source = VAULT / path_value
    target = target_for(source)
    target.parent.mkdir(parents=True, exist_ok=True)
    PROCESSED.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        shutil.copy2(source, target)
    processed = PROCESSED / source.name
    if processed.exists():
        from intake import digest

        processed = PROCESSED / f"{source.stem}-{digest(source)}{source.suffix}"
    source.replace(processed)
    return target


def create_action_item(action: dict[str, Any]) -> Path:
    output = action_item_path(action["summary"])
    output.parent.mkdir(parents=True, exist_ok=True)
    owner = action["owner"] or "待确认"
    due = action["due"] or "待确认"
    output.write_text(
        f'''---
type: action-item
status: draft
action_status: open
summary: {json.dumps(action["summary"], ensure_ascii=False)}
owner: {json.dumps(action["owner"], ensure_ascii=False)}
due: {json.dumps(action["due"], ensure_ascii=False)}
sources: [{json.dumps(action["source"], ensure_ascii=False)}]
created: {date.today().isoformat()}
updated: {date.today().isoformat()}
---

# {action["summary"]}

- 负责人：{owner}
- 截止时间：{due}
- 来源：[[{action["source"]}]]
- 当前状态：draft，使用前按风险决定是否确认。
''', encoding="utf-8")
    return output


def create_confirmation(action: dict[str, Any]) -> Path:
    output = confirmation_path(action["target"])
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        f'''---
type: confirmation
status: pending
risk: high
target: {json.dumps(action["target"], ensure_ascii=False)}
created: {date.today().isoformat()}
---

# 待确认事项

## 建议

{action["suggestion"]}

## 依据

{action["evidence"] or "未提供"}

## 不确定点

{action["uncertainty"] or "未提供"}

## 可选动作

- 批准
- 修改
- 暂不处理
- 标记为错误
''', encoding="utf-8")
    return output


def execute(action: dict[str, Any]) -> Path:
    kind = action["type"]
    if kind == "ingest_source":
        return ingest(action["path"])
    if kind == "upsert_entity":
        return create_entity(action["kind"], action["name"], action["aliases"], action["tags"], action["source"])
    if kind == "append_entity_timeline":
        return append_entity(action["kind"], action["name"], action["date"], action["note"], action["source"])
    if kind == "create_task":
        return new_task(action["goal"])
    if kind == "create_action_item":
        return create_action_item(action)
    return create_confirmation(action)


def record(request: dict[str, Any], outputs: list[str]) -> None:
    folder = configured_path("reports") / "agent-actions"
    folder.mkdir(parents=True, exist_ok=True)
    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "request_id": request["request_id"],
        "intent": request["intent"],
        "actions": [action["type"] for action in request["actions"]],
        "outputs": outputs,
    }
    with (folder / f"{date.today().isoformat()}.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def load_request(path_value: str) -> Any:
    if path_value == "-":
        return json.load(__import__("sys").stdin)
    return json.loads(Path(path_value).read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="执行 Orcas Agent 结构化操作")
    parser.add_argument("request", help="请求 JSON 文件；使用 - 从标准输入读取")
    parser.add_argument("--dry-run", action="store_true", help="只校验并返回计划，不写入 Vault")
    args = parser.parse_args()
    request = validate_request(load_request(args.request))
    if args.dry_run:
        print(json.dumps({"ok": True, "dry_run": True, **request}, ensure_ascii=False, indent=2))
        return 0
    outputs = [relative(execute(action)) for action in request["actions"]]
    record(request, outputs)
    print(json.dumps({"ok": True, "request_id": request["request_id"], "outputs": outputs}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
