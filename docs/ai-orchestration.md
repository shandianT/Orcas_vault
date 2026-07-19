# Agent 接入

Orcas 不内置 AI 编排层。用户选择的 Obsidian Agent 负责理解、抽取、规划和对话。

Orcas 提供两种接入方式：

## Personal

Agent 根据 `orcas-skill/SKILL.md` 和 references 中的 SOP，直接维护 active draft Markdown。

## Governed

Agent 生成 `orcas-action-v1` JSON，通过可选 Runtime 执行确定性写入：

```sh
python3 orcas.py agent request.json --dry-run
python3 orcas.py agent request.json
```

Runtime 只接受白名单操作，并拒绝 protected 状态、非法路径、缺失来源和重复输出。它不调用任何模型。
