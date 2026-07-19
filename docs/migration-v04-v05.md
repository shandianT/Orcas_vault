# 从 v0.4 迁移到 v0.5

> 历史迁移文档：仅用于旧版 Orcas Context OS Vault 升级，不代表 v0.8.1 的默认 Skill-first 工作流。

v0.5 保持旧 Vault 可读，不要求一次性重写历史文件。

## 状态兼容

- 新状态：`draft`、`trusted`、`stale`。
- 新解析维度：`resolution: active | disputed | superseded`。
- 旧 `verified` 自动按 `trusted` 读取。
- 旧 `status: disputed` 和 `status: superseded` 仍可读取，建议后续维护时拆到 `resolution`。

AI 仍然只能创建 `draft`。人工明确确认某个当前条目后，可执行：

```sh
python3 scripts/trust.py knowledge/example.md --actor "你的名字" --evidence "用户明确回复：对的"
```

命令只接受单个文件，不接受目录或通配符。

## 检索变化

- `knowledge/` 改为递归检索。
- 支持 Obsidian 多行 YAML 列表。
- 高相关 draft 会进入“候选知识”，并标注置信度和未核实状态。
- 来源只来自实际选中条目的 `sources`，不再按文件修改时间随机补齐。
- `reuse_count` 保持可读，但新系统使用 `_reports/usage/events.jsonl` 记录真实检索和采用事件。

## 新目录

- `wiki/entities/`
- `skills/registry.json`
- `playbooks/`
- `preferences/profile.md`
- `_reports/usage/`

旧版 `learn.py` 不再随 v0.8.0 Runtime 发布。需要保留旧规则历史时，应先归档旧 Vault，再将有效经验人工整理进 Orcas Skill references。
