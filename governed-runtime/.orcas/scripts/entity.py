#!/usr/bin/env python3
"""Create entity pages and append dated timeline increments."""
from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path

from config import VAULT, entity_path as entity_root, relative
from frontmatter import list_value, parse

KINDS = {"person": "people", "project": "projects", "organization": "organizations"}
KIND_TAGS = {kind: f"entity/{kind}" for kind in KINDS}


def slug(value: str) -> str:
    return re.sub(r"[^\w\u4e00-\u9fff]+", "-", value.strip().lower()).strip("-")[:80] or "entity"


def entity_path(kind: str, name: str) -> Path:
    return entity_root(KINDS[kind]) / f"{slug(name)}.md"


def unique(values: list[str], strip_hash: bool = False) -> list[str]:
    result = []
    for value in values:
        normalized = value.strip()
        if strip_hash:
            normalized = normalized.lstrip("#")
        if normalized and normalized not in result:
            result.append(normalized)
    return result


def encoded_list(values: list[str]) -> str:
    return "[" + ", ".join(json.dumps(item, ensure_ascii=False) for item in values) + "]"


def replace_list(text: str, key: str, values: list[str]) -> str:
    line = f"{key}: {encoded_list(values)}"
    pattern = re.compile(rf"^{re.escape(key)}:(?:[^\n]*)(?:\n[ \t]+- [^\n]*)*", re.MULTILINE)
    if pattern.search(text):
        return pattern.sub(line, text, count=1)
    return text.replace("---\n", f"---\n{line}\n", 1)


def update_existing(output: Path, kind: str, name: str, aliases: list[str], tags: list[str], source: str) -> None:
    text = output.read_text(encoding="utf-8")
    meta = parse(text)
    status = "trusted" if meta.get("status") == "verified" else meta.get("status", "draft")
    if status != "draft" or meta.get("resolution", "active") != "active":
        raise SystemExit(f"只能自动更新 active draft 实体: {relative(output)}")
    changed = False

    merged_aliases = unique(list_value(meta, "aliases") + aliases)
    if merged_aliases != list_value(meta, "aliases"):
        text = replace_list(text, "aliases", merged_aliases)
        changed = True

    merged_tags = unique([KIND_TAGS[kind]] + list_value(meta, "tags") + tags, strip_hash=True)
    if merged_tags != list_value(meta, "tags"):
        text = replace_list(text, "tags", merged_tags)
        changed = True

    merged_sources = unique(list_value(meta, "sources") + ([source] if source else []))
    if merged_sources != list_value(meta, "sources"):
        text = replace_list(text, "sources", merged_sources)
        changed = True

    if kind == "person":
        linked_heading = f"# [[{name}]]"
        updated_text = re.sub(rf"^#\s+{re.escape(name)}\s*$", linked_heading, text, count=1, flags=re.MULTILINE)
        if updated_text != text:
            text = updated_text
            changed = True

    if changed:
        text = re.sub(r"^updated:.*$", f"updated: {date.today().isoformat()}", text, count=1, flags=re.MULTILINE)
        output.write_text(text, encoding="utf-8")


def create(kind: str, name: str, aliases: list[str], tags: list[str], source: str) -> Path:
    output = entity_path(kind, name)
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        update_existing(output, kind, name, aliases, tags, source)
        return output
    aliases = unique(aliases)
    tags = unique([KIND_TAGS[kind]] + tags, strip_hash=True)
    sources = [source] if source else []
    heading = f"[[{name}]]" if kind == "person" else name
    output.write_text(
        f'''---
type: entity
entity_kind: {kind}
status: draft
resolution: active
name: {json.dumps(name, ensure_ascii=False)}
aliases: {encoded_list(aliases)}
tags: {encoded_list(tags)}
summary: {json.dumps(f"{name} 的实体档案", ensure_ascii=False)}
sources: {encoded_list(sources)}
confidence: medium
created: {date.today().isoformat()}
updated: {date.today().isoformat()}
---

# {heading}

## 当前状态

待补充

## 关系

待补充

## 未解决事项

待补充

## 时间线

''', encoding="utf-8")
    return output


def append(kind: str, name: str, when: str, note: str, source: str) -> Path:
    output = create(kind, name, [], [], source)
    text = output.read_text(encoding="utf-8")
    marker = f"- {when}：{note}" + (f"（来源：[[{source}]]）" if source else "")
    if marker not in text:
        text = text.rstrip() + "\n" + marker + "\n"
    if source:
        sources = list_value(parse(text), "sources")
        if source not in sources:
            sources.append(source)
            text = replace_list(text, "sources", sources)
    text = re.sub(r"^updated:.*$", f"updated: {date.today().isoformat()}", text, count=1, flags=re.MULTILINE)
    output.write_text(text, encoding="utf-8")
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description="管理人物、项目和组织实体")
    sub = parser.add_subparsers(dest="command", required=True)
    new = sub.add_parser("new")
    new.add_argument("kind", choices=KINDS)
    new.add_argument("name")
    new.add_argument("--alias", action="append", default=[])
    new.add_argument("--tag", action="append", default=[])
    new.add_argument("--source", default="")
    timeline = sub.add_parser("append")
    timeline.add_argument("kind", choices=KINDS)
    timeline.add_argument("name")
    timeline.add_argument("note")
    timeline.add_argument("--date", default=date.today().isoformat())
    timeline.add_argument("--source", default="")
    args = parser.parse_args()
    output = create(args.kind, args.name, args.alias, args.tag, args.source) if args.command == "new" else append(args.kind, args.name, args.date, args.note, args.source)
    print(relative(output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
