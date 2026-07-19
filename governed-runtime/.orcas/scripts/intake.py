#!/usr/bin/env python3
"""Preserve inbox files in the configured source directory."""
from __future__ import annotations

import hashlib
import shutil
from datetime import date
from pathlib import Path

from config import path, relative

INBOX, SOURCES, PROCESSED = path("inbox"), path("sources"), path("processed")


def digest(candidate: Path) -> str:
    value = hashlib.sha256()
    with candidate.open("rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            value.update(block)
    return value.hexdigest()[:10]


def target_for(candidate: Path) -> Path:
    target = SOURCES / candidate.name
    if not target.exists() or digest(target) == digest(candidate):
        return target
    return SOURCES / f"{candidate.stem}-{date.today().isoformat()}-{digest(candidate)}{candidate.suffix}"


def main() -> int:
    INBOX.mkdir(parents=True, exist_ok=True)
    SOURCES.mkdir(parents=True, exist_ok=True)
    PROCESSED.mkdir(parents=True, exist_ok=True)
    files = [candidate for candidate in INBOX.iterdir() if candidate.is_file() and candidate.name != "README.md"]
    if not files:
        print("没有待处理文件。")
        return 0
    for source in files:
        target = target_for(source)
        if not target.exists():
            shutil.copy2(source, target)
        processed = PROCESSED / source.name
        if processed.exists():
            processed = PROCESSED / f"{source.stem}-{digest(source)}{source.suffix}"
        source.replace(processed)
        print(f"{source.name} -> {relative(target)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
