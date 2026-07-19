# 从 v0.5 迁移到 Standard

> 历史迁移文档：仅用于旧版 Orcas Context OS Vault 升级，不代表 v0.8.1 的默认 Skill-first 工作流。

v0.6 将用户目录改为更直观的编号结构，但保留旧 Vault 的运行兼容。

## 映射

| v0.5 | Standard |
|---|---|
| `inbox/` | `00-Inbox/` |
| `sources/` | `01-Raw/` |
| `knowledge/` | `02-Wiki/Knowledge/` |
| `wiki/entities/people/` | `02-Wiki/People/` |
| `wiki/entities/organizations/` | `02-Wiki/Organizations/` |
| `wiki/entities/projects/` | `02-Wiki/Projects/` |
| `work/` | `03-Projects/` |
| `playbooks/` | `04-Playbooks/` |
| `preferences/` | `_meta/preferences/` |
| `skills/` | `_meta/skills/` |

## 安全流程

1. 备份或提交当前 Vault。
2. 将新版 `orcas.py`、`scripts/` 和 `_meta/` 合并到 Vault。
3. 运行 `python3 orcas.py migrate` 查看逐文件计划。
4. 若报告冲突，先人工比较，不要覆盖。
5. 运行 `python3 orcas.py migrate --apply`。
6. 运行 `python3 orcas.py doctor`。
7. 用 `python3 orcas.py ask "一个已知问题"` 验证检索。
8. 验证完成后再人工归档旧目录。

迁移只复制文件，不删除旧内容。根目录的旧 `README.md` 不复制，因为 Standard 目标已带新版说明。成功迁移会在缺少配置时创建 `.orcas/config.json`。

## 状态迁移

不需要批量改写旧文件：

- 旧 `verified` 按 `trusted` 读取
- 新确认统一写 `trusted`
- AI 始终只能写 `draft`

推荐在以后人工复核某条旧知识时再把 `verified` 改为 `trusted`，避免无证据的批量状态改写。
