# 目录配置

默认 `.orcas/config.json` 将治理语义映射到四目录结构：

```json
{
  "profile": "work-first",
  "paths": {
    "inbox": "inbox",
    "sources": "sources",
    "knowledge_roots": ["knowledge"],
    "knowledge": "knowledge/notes",
    "projects": "work/tasks",
    "playbooks": "knowledge/playbooks",
    "publish": "work/outputs/publishing",
    "reports": ".orcas/reports",
    "meta": ".orcas/meta",
    "attachments": "knowledge/attachments"
  }
}
```

## 嫁接现有 Vault

可以保留已有 `llm-wiki`，只修改映射：

```json
{
  "paths": {
    "knowledge_roots": ["llm-wiki"],
    "knowledge": "llm-wiki/notes",
    "projects": "work/tasks"
  },
  "entities": {
    "people": "llm-wiki/people",
    "organizations": "llm-wiki/organizations",
    "projects": "llm-wiki/projects"
  }
}
```

目录名称可换，但来源保护、状态和权限契约保持不变。
