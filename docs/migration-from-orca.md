# 从 ORCA 迁移

> 历史迁移文档：仅用于旧版 Orcas Context OS Vault 升级，不代表 v0.8.1 的默认 Skill-first 工作流。

迁移采用复制和验证，不在原库上直接移动或删除文件。ORCA 的业务目录与 Orcas Standard 接近，但 Orcas 额外区分实体、可复用知识、任务工作区和治理配置。

## 目录映射

| ORCA | Orcas Standard |
|---|---|
| `00-inbox/` | `00-Inbox/` |
| `01-raw/` | `01-Raw/` |
| `02-wiki/` | `02-Wiki/Knowledge/`，实体页分别进入 People、Organizations、Projects |
| `03-projects/` | `03-Projects/` |
| `04-relations/` | 实体关系进入对应实体页；跨实体结论进入 `02-Wiki/Knowledge/` |
| `05-playbooks/` | `04-Playbooks/` |
| `06-publish/` | `05-Publish/Drafts/` 或 `Published/` |
| `_meta/` | `_meta/`，人工合并模板和规则 |
| `_reports/` | `_reports/`，人工合并审计记录 |

## 推荐步骤

1. 备份原 Vault。
2. 创建新的 Orcas Standard Vault。
3. 复制 `01-raw/` 到 `01-Raw/`，不修改正文。
4. 将人物、组织、项目页归入对应实体目录。
5. 将跨任务知识复制到 `02-Wiki/Knowledge/` 并补齐来源和状态。
6. 将当前项目复制到 `03-Projects/`，发布物按审批状态进入 `05-Publish/`。
7. 运行 `python3 orcas.py doctor`。
8. 抽查重要结论是否能定位来源，并用真实问题验证查询。
9. 试运行后再决定是否归档 ORCA 旧目录。
