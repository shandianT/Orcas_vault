#!/usr/bin/env python3
"""Load Orcas's portable vault path profile."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

VAULT = Path(__file__).resolve().parent.parent.parent
DEFAULTS: dict[str, Any] = {
    "version": 2,
    "profile": "work-first",
    "paths": {
        "inbox": "inbox",
        "processed": "inbox/_processed",
        "sources": "sources",
        "knowledge_roots": ["knowledge"],
        "knowledge": "knowledge/notes",
        "projects": "work/tasks",
        "playbooks": "knowledge/playbooks",
        "publish": "work/outputs/publishing",
        "reports": ".orcas/reports",
        "meta": ".orcas/meta",
        "attachments": "knowledge/attachments"
    },
    "entities": {
        "people": "knowledge/people",
        "organizations": "knowledge/organizations",
        "projects": "knowledge/projects"
    }
}
LEGACY_DEFAULTS: dict[str, Any] = {
    "version": 1,
    "profile": "legacy-v05",
    "paths": {
        "inbox": "inbox",
        "processed": "inbox/_processed",
        "sources": "sources",
        "knowledge_roots": ["knowledge", "wiki/entities"],
        "knowledge": "knowledge",
        "projects": "work",
        "playbooks": "playbooks",
        "publish": "publish",
        "reports": "_reports",
        "meta": "_meta",
        "attachments": "attachments"
    },
    "entities": {
        "people": "wiki/entities/people",
        "organizations": "wiki/entities/organizations",
        "projects": "wiki/entities/projects"
    }
}
NUMBERED_DEFAULTS: dict[str, Any] = {
    "version": 1,
    "profile": "numbered-v06",
    "paths": {
        "inbox": "00-Inbox",
        "processed": "00-Inbox/_processed",
        "sources": "01-Raw",
        "knowledge_roots": ["02-Wiki"],
        "knowledge": "02-Wiki/Knowledge",
        "projects": "03-Projects",
        "playbooks": "04-Playbooks",
        "publish": "05-Publish",
        "reports": "_reports",
        "meta": "_meta",
        "attachments": "attachments"
    },
    "entities": {
        "people": "02-Wiki/People",
        "organizations": "02-Wiki/Organizations",
        "projects": "02-Wiki/Projects"
    }
}


def _merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    result = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _merge(result[key], value)
        else:
            result[key] = value
    return result


def load() -> dict[str, Any]:
    config_path = VAULT / ".orcas" / "config.json"
    if config_path.exists():
        try:
            raw = json.loads(config_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise SystemExit(f".orcas/config.json 无效: {exc}") from exc
        if not isinstance(raw, dict):
            raise SystemExit(".orcas/config.json 必须是 JSON 对象")
        return _merge(DEFAULTS, raw)
    if (VAULT / "00-Inbox").exists() or (VAULT / "02-Wiki").exists():
        return NUMBERED_DEFAULTS
    if (VAULT / "wiki" / "entities").exists() or (VAULT / "_meta").exists():
        return LEGACY_DEFAULTS
    if (VAULT / "inbox").exists() or (VAULT / "knowledge").exists() or (VAULT / "work").exists():
        return DEFAULTS
    return DEFAULTS


CONFIG = load()


def path(name: str) -> Path:
    value = CONFIG.get("paths", {}).get(name)
    if not isinstance(value, str) or not value:
        raise SystemExit(f"Orcas 配置缺少 paths.{name}")
    return VAULT / value


def roots(name: str) -> list[Path]:
    value = CONFIG.get("paths", {}).get(name, [])
    if isinstance(value, str):
        value = [value]
    if not isinstance(value, list):
        raise SystemExit(f"Orcas 配置中的 paths.{name} 必须是路径数组")
    return [VAULT / str(item) for item in value if str(item).strip()]


def entity_path(kind: str) -> Path:
    value = CONFIG.get("entities", {}).get(kind)
    if not isinstance(value, str) or not value:
        raise SystemExit(f"Orcas 配置缺少 entities.{kind}")
    return VAULT / value


def relative(target: Path) -> str:
    return str(target.resolve().relative_to(VAULT.resolve()))


def ensure_layout() -> None:
    for key in ("inbox", "processed", "sources", "knowledge", "projects", "playbooks", "reports", "meta", "attachments"):
        path(key).mkdir(parents=True, exist_ok=True)
    for key in ("people", "organizations", "projects"):
        entity_path(key).mkdir(parents=True, exist_ok=True)
