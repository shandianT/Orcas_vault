#!/usr/bin/env python3
"""Parse and update the small YAML subset used by Orcas Markdown files."""
from __future__ import annotations

import ast
import json
import re
from typing import Any


def _scalar(value: str) -> Any:
    value = value.strip()
    if not value:
        return ""
    if value in {"null", "~"}:
        return None
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    if value.startswith("[") and value.endswith("]"):
        try:
            parsed = ast.literal_eval(value)
            return parsed if isinstance(parsed, list) else value
        except (SyntaxError, ValueError):
            return [item.strip().strip("'\"") for item in value[1:-1].split(",") if item.strip()]
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        try:
            return ast.literal_eval(value)
        except (SyntaxError, ValueError):
            return value[1:-1]
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    return value


def parse(text: str) -> dict[str, Any]:
    """Return flattened frontmatter keys, including multiline lists."""
    if not text.startswith("---\n"):
        return {}
    try:
        block = text.split("---\n", 2)[1]
    except IndexError:
        return {}
    result: dict[str, Any] = {}
    stack: list[tuple[int, str]] = []
    list_key = ""
    list_indent = -1
    for raw_line in block.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip())
        stripped = raw_line.strip()
        if stripped.startswith("- ") and list_key and indent > list_indent:
            result.setdefault(list_key, []).append(_scalar(stripped[2:]))
            continue
        list_key = ""
        list_indent = -1
        if ":" not in stripped:
            continue
        key, raw_value = stripped.split(":", 1)
        while stack and stack[-1][0] >= indent:
            stack.pop()
        full_key = ".".join([item[1] for item in stack] + [key.strip()])
        value = raw_value.strip()
        if value:
            result[full_key] = _scalar(value)
        else:
            stack.append((indent, key.strip()))
            list_key = full_key
            list_indent = indent
            result.setdefault(full_key, [])
    return result


def list_value(meta: dict[str, Any], key: str) -> list[str]:
    value = meta.get(key, [])
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        parsed = _scalar(value)
        if isinstance(parsed, list):
            return [str(item) for item in parsed if str(item).strip()]
        return [value]
    return []


def replace_scalar(text: str, key: str, value: str) -> str:
    """Replace one top-level scalar without rewriting unrelated Markdown."""
    if not text.startswith("---\n"):
        raise ValueError("文件缺少 frontmatter")
    encoded = json.dumps(value, ensure_ascii=False) if any(char in value for char in ':#[]{}"\'') else value
    pattern = re.compile(rf"^(?P<prefix>{re.escape(key)}:\s*).*$", re.MULTILINE)
    if pattern.search(text):
        return pattern.sub(lambda match: match.group("prefix") + encoded, text, count=1)
    return text.replace("---\n", f"---\n{key}: {encoded}\n", 1)
