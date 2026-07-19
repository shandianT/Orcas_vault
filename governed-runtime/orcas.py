#!/usr/bin/env python3
"""Optional deterministic runtime for Orcas Obsidian governed mode."""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCRIPTS = ROOT / ".orcas" / "scripts"
sys.path.insert(0, str(SCRIPTS))
from config import CONFIG, DEFAULTS, VAULT, ensure_layout, path as configured_path, relative  # noqa: E402

MIGRATION_MAP = {
    "00-Inbox": "inbox",
    "01-Raw": "sources",
    "02-Wiki/Knowledge": "knowledge/notes",
    "02-Wiki/People": "knowledge/people",
    "02-Wiki/Organizations": "knowledge/organizations",
    "02-Wiki/Projects": "knowledge/projects",
    "03-Projects": "work/tasks",
    "04-Playbooks": "knowledge/playbooks",
    "05-Publish/Drafts": "work/outputs/publishing/drafts",
    "05-Publish/Published": "work/outputs/publishing/published",
    "wiki/entities/people": "knowledge/people",
    "wiki/entities/organizations": "knowledge/organizations",
    "wiki/entities/projects": "knowledge/projects",
    "playbooks": "knowledge/playbooks",
    "publish": "work/outputs/publishing",
    "attachments": "knowledge/attachments",
    "preferences": ".orcas/meta/preferences",
    "skills": ".orcas/meta/skills",
    "_meta": ".orcas/meta",
    "_reports": ".orcas/reports",
    "scripts": ".orcas/scripts",
    "work/_done": "work/archive",
    "work/_publish": "work/outputs/publishing"
}


def run_script(name: str, *args: str) -> int:
    return subprocess.run([sys.executable, str(SCRIPTS / name), *args], cwd=VAULT, check=False).returncode


def init(profile: str) -> int:
    config_dir = VAULT / ".orcas"
    config_dir.mkdir(parents=True, exist_ok=True)
    config_path = config_dir / "config.json"
    if config_path.exists():
        print(f"已存在配置: {relative(config_path)}")
    else:
        value = dict(DEFAULTS)
        value["profile"] = profile
        config_path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"已创建配置: {relative(config_path)}")
    ensure_layout()
    print("Orcas 工作空间已初始化。")
    return 0


def migration_plan() -> list[tuple[Path, Path]]:
    plan = []
    for source_name, target_name in MIGRATION_MAP.items():
        source = VAULT / source_name
        target = VAULT / target_name
        if not source.exists() or source.resolve() == target.resolve():
            continue
        for candidate in source.rglob("*"):
            if not candidate.is_file():
                continue
            relative_candidate = candidate.relative_to(source)
            if relative_candidate == Path("README.md"):
                continue
            plan.append((candidate, target / relative_candidate))
    work_root = VAULT / "work"
    tasks_root = VAULT / "work/tasks"
    if work_root.exists():
        reserved = {"README.md", "tasks", "outputs", "archive", "_done", "_publish"}
        for candidate in work_root.iterdir():
            if candidate.name in reserved or not candidate.is_file():
                continue
            plan.append((candidate, tasks_root / candidate.name))
    return plan


def migrate(apply: bool) -> int:
    plan = migration_plan()
    if not plan:
        print("没有需要迁移到四目录结构的内容。")
        return 0
    conflicts = [target for _, target in plan if target.exists()]
    print(f"计划复制 {len(plan)} 个文件，冲突 {len(conflicts)} 个。")
    for source, target in plan:
        label = "冲突" if target.exists() else "复制"
        print(f"{label}: {relative(source)} -> {relative(target)}")
    if not apply:
        print("当前为预览。确认后追加 --apply 执行复制，旧文件不会删除。")
        return 0
    if conflicts:
        print("存在目标文件冲突，迁移已中止。")
        return 2
    for source, target in plan:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    config_path = VAULT / ".orcas" / "config.json"
    if not config_path.exists():
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(json.dumps(DEFAULTS, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"已创建 work-first 配置: {relative(config_path)}")
    else:
        try:
            config = json.loads(config_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise SystemExit(f".orcas/config.json 无效，未更新路径: {exc}") from exc
        paths = config.setdefault("paths", {})
        changed = False
        if paths.get("projects") == "work":
            paths["projects"] = "work/tasks"
            changed = True
        if paths.get("publish") == "work/_publish":
            paths["publish"] = "work/outputs/publishing"
            changed = True
        if changed:
            config_path.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(f"已更新工作目录配置: {relative(config_path)}")
    print("迁移复制完成。旧目录仍保留，可在验证后人工归档。")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Orcas Obsidian 可选治理运行时")
    sub = parser.add_subparsers(dest="command", required=True)
    init_cmd = sub.add_parser("init", help="初始化可移植目录配置")
    init_cmd.add_argument("--profile", choices=["lite", "standard", "governed"], default="standard")
    sub.add_parser("ingest", help="封存 Inbox 材料")
    ask = sub.add_parser("ask", help="直接查询知识库")
    ask.add_argument("question")
    ask.add_argument("--limit", default="6")
    ask.add_argument("--status", choices=["all", "trusted", "draft", "stale"], default="all")
    ask.add_argument("--kind", choices=["all", "knowledge", "entity", "decision"], default="all")
    ask.add_argument("--adopt", action="store_true")
    project = sub.add_parser("project", help="创建重任务项目")
    project.add_argument("goal")
    trust = sub.add_parser("trust", help="人工确认一个 draft")
    trust.add_argument("target")
    trust.add_argument("--actor", required=True)
    trust.add_argument("--evidence", default="")
    sub.add_parser("doctor", help="运行健康检查")
    agent = sub.add_parser("agent", help="执行第三方 Agent 提交的结构化操作")
    agent.add_argument("request", help="请求 JSON 文件；使用 - 从标准输入读取")
    agent.add_argument("--dry-run", action="store_true")
    review = sub.add_parser("review", help="只列出值得人工处理的确认事项")
    review.add_argument("--json", action="store_true")
    migration = sub.add_parser("migrate", help="预览或复制旧目录到四目录结构")
    migration.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    if args.command == "init":
        return init(args.profile)
    if args.command == "ingest":
        return run_script("intake.py")
    if args.command == "ask":
        command = [args.question, "--limit", args.limit, "--status", args.status, "--kind", args.kind]
        if args.adopt:
            command.append("--adopt")
        return run_script("query.py", *command)
    if args.command == "project":
        return run_script("context.py", "new", args.goal)
    if args.command == "trust":
        return run_script("trust.py", args.target, "--actor", args.actor, "--evidence", args.evidence)
    if args.command == "doctor":
        return run_script("health.py")
    if args.command == "agent":
        command = [args.request]
        if args.dry_run:
            command.append("--dry-run")
        return run_script("agent.py", *command)
    if args.command == "review":
        return run_script("review.py", "--json") if args.json else run_script("review.py")
    return migrate(args.apply)


if __name__ == "__main__":
    raise SystemExit(main())
