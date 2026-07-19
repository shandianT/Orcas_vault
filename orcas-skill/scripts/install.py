#!/usr/bin/env python3
"""Install the Orcas personal Vault template and optional governed runtime."""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
TEMPLATE = SKILL / "assets" / "starter-vault"
RUNTIME = SKILL / "scripts" / "runtime"


def copy_missing(source: Path, target: Path) -> list[Path]:
    created: list[Path] = []
    for candidate in source.rglob("*"):
        relative = candidate.relative_to(source)
        output = target / relative
        if candidate.is_dir():
            output.mkdir(parents=True, exist_ok=True)
        elif not output.exists():
            output.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(candidate, output)
            created.append(output)
    return created


def main() -> int:
    parser = argparse.ArgumentParser(description="安装 Orcas Obsidian Vault 模板")
    parser.add_argument("vault", help="目标 Obsidian Vault 路径")
    parser.add_argument("--mode", choices=["personal", "governed"], default="personal")
    args = parser.parse_args()

    vault = Path(args.vault).expanduser().resolve()
    vault.mkdir(parents=True, exist_ok=True)
    created = copy_missing(TEMPLATE, vault)
    if args.mode == "governed":
        created.extend(copy_missing(RUNTIME, vault))
    print(f"Orcas 已安装到 {vault}")
    print(f"模式: {args.mode}")
    print(f"新增文件: {len(created)}")
    if args.mode == "personal":
        print("日常直接在 Obsidian Agent 中使用自然语言。")
    else:
        print("受控写入可通过 orcas.py 和 orcas-action-v1 执行。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
