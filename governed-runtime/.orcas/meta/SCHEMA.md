# 数据结构

Orcas 只要求用户理解三个核心对象：`Source`、`Knowledge`、`Work`。目录是 Obsidian 中的默认落点，可通过 `.orcas/config.json` 映射，不把业务模型锁死在某套目录名称上。

## Source

原始来源保存在配置中的 `paths.sources`，Standard 默认是 `sources/`，只增不改。知识和任务通过路径或 Wikilink 引用来源。

## Knowledge

必需字段：

- `type`：`fact`、`insight`、`decision`、`lesson`、`rule`
- `status`：`draft`、`trusted`、`stale`、`disputed`、`superseded`
- `summary`：用于检索排序的短摘要
- `sources`：来源路径数组
- `source_quality`：`primary`、`secondary`、`unknown`
- `reuse_count`：历史复用次数
- `review_after`：建议复核日期
- `verification`：核实证据和主张计数

`verified` 是 v0.5 兼容状态，读取时等价于 `trusted`，新文件使用 `trusted`。`verification` 至少包含 `checked_at`、`evidence`、`claims_checked`、`claims_uncertain`、`review_after`。

## Work 与任务上下文包

任务文件应包含 `goal`、`audience`、`deadline`、`constraints`、`output.format` 和 `output.risk_level`。构建后的上下文包固定包含可信知识、候选知识、相关来源、历史决策、可复用经验和未解决冲突。

默认预算为 5 条核心知识、3 个来源、2 条历史决策或经验、1 个未解决冲突。超过预算先排序和摘要，不直接扩大上下文。

## Entity

实体必需保留 `type: entity`、`entity_kind`、`name`、`aliases`、`tags` 和 `sources`。`tags` 至少包含对应类型标签，例如人物使用 `entity/person`；人物页标题使用 `# [[姓名]]`，来源在正文中使用 `[[相对路径]]`。

## Agent 操作协议

第三方 Agent 使用 `orcas-action-v1` JSON 请求调用 Orcas，不直接写入 Vault。

顶层字段：

- `protocol`：固定为 `orcas-action-v1`
- `request_id`：调用方生成的非空唯一标识
- `intent`：可选的自然语言任务类型
- `actions`：按顺序执行的非空操作数组

首版白名单操作：

- `ingest_source`：将 `inbox/` 文件封存到 `sources/`
- `upsert_entity`：创建或更新 active draft 人物、组织或项目
- `append_entity_timeline`：向 active draft 实体追加带来源的时间线
- `create_task`：在 `work/` 创建任务
- `create_action_item`：在 `work/` 创建带来源的 draft 行动项
- `create_confirmation`：创建高风险人工确认项

执行约束：

- 建议先使用 `--dry-run`
- 自动操作不得请求 `trusted`、`verified` 或其他受保护状态
- 实体和行动项来源必须位于 `sources/`
- 同一请求可以先 `ingest_source`，再引用该操作将生成的来源路径
- 不允许修改已有 trusted、stale、disputed 或 superseded 实体
- 不允许覆盖同名任务、行动项或确认项
- 执行记录写入 `.orcas/reports/agent-actions/`
