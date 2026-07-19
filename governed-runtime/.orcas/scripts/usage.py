#!/usr/bin/env python3
"""Append privacy-conscious knowledge usage events."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from config import path, relative

EVENTS = path("reports") / "usage" / "events.jsonl"


def record(action: str, query: str, paths: Iterable[Path], adopted: bool | None = None) -> None:
    EVENTS.parent.mkdir(parents=True, exist_ok=True)
    unique_paths: list[str] = []
    for candidate in paths:
        value = relative(candidate)
        if value not in unique_paths:
            unique_paths.append(value)
    event = {
        "at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "action": action,
        "query": query[:300],
        "knowledge": unique_paths,
    }
    if adopted is not None:
        event["adopted"] = adopted
    with EVENTS.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False) + "\n")
