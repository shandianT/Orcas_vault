#!/usr/bin/env python3
"""Create a compact human confirmation item for a risky change."""
from __future__ import annotations
import argparse, re
from datetime import date
from pathlib import Path
from config import VAULT, path as configured_path, relative
def slug(text: str) -> str: return re.sub(r"[^\w\u4e00-\u9fff]+", "-", text.lower()).strip("-")[:50] or "confirmation"
def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("target"); parser.add_argument("suggestion"); parser.add_argument("--evidence", default=""); parser.add_argument("--uncertainty", default=""); args = parser.parse_args()
    today = date.today().isoformat(); folder = configured_path("reports") / "confirmations"; folder.mkdir(parents=True, exist_ok=True); path = folder / f"{today}-{slug(args.target)}.md"
    path.write_text(f'''---\ntype: confirmation\nstatus: pending\nrisk: high\ntarget: "{args.target}"\ncreated: {today}\n---\n\n# 待确认事项\n\n## 建议\n\n{args.suggestion}\n\n## 依据\n\n{args.evidence or '未提供'}\n\n## 不确定点\n\n{args.uncertainty or '未提供'}\n\n## 可选动作\n\n- 批准\n- 修改\n- 暂不处理\n- 标记为错误\n''', encoding="utf-8")
    print(path.relative_to(VAULT)); return 0
if __name__ == "__main__": raise SystemExit(main())
