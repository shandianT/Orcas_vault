# 从编号版 v0.6 迁移到四目录结构

> 历史迁移文档：仅用于旧版 Orcas Context OS Vault 升级，不代表 v0.8.1 的默认 Skill-first 工作流。

## 映射

| 编号版 | work-first |
|---|---|
| `00-Inbox/` | `inbox/` |
| `01-Raw/` | `sources/` |
| `02-Wiki/Knowledge/` | `knowledge/notes/` |
| `02-Wiki/People/` | `knowledge/people/` |
| `02-Wiki/Organizations/` | `knowledge/organizations/` |
| `02-Wiki/Projects/` | `knowledge/projects/` |
| `03-Projects/` | `work/tasks/` |
| `04-Playbooks/` | `knowledge/playbooks/` |
| `05-Publish/` | `work/outputs/publishing/` |
| `_meta/` | `.orcas/meta/` |
| `_reports/` | `.orcas/reports/` |
| `scripts/` | `.orcas/scripts/` |

## 安全流程

```sh
python3 orcas.py migrate
python3 orcas.py migrate --apply
python3 orcas.py doctor
```

迁移只复制文件，不删除旧内容。目标存在同名文件时中止，避免覆盖。

从 v0.7-v0.8.0 升级时，旧 `work/` 根目录中的任务复制到 `work/tasks/`，`work/_done/` 复制到 `work/archive/`，`work/_publish/` 复制到 `work/outputs/publishing/`。旧目录仍保留，确认无误后再人工清理。
