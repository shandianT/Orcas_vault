# Obsidian 使用指南

Orcas 的默认形态是 Obsidian + 第三方 Agent + Orcas Skill。用户只进行自然语言交互。

## 日常流程

1. 把新材料放进 `inbox/`。
2. 告诉 Agent 要处理、查询或交付什么。
3. Agent 先保存来源，再创建 draft 人物、项目、知识和行动项。
4. 查询结果区分 trusted、draft 和缺失证据。
5. 当前任务真正使用关键 draft 时，再请求确认。
6. 任务结束后只保存可复用增量。

当前工作放在 `work/tasks/`，交付物放在 `work/outputs/`。任务状态使用 frontmatter 表示；只有已经结束且近期不再使用的内容才放入 `work/archive/`。

## 个人模式

个人模式是默认方案：

- 不安装 `.orcas/` 和 `orcas.py`
- Agent 可以直接编辑 active draft
- Agent 不得修改 protected 状态
- Git 或 Obsidian 文件恢复提供回滚

## Governed 模式

当多人或多个 Agent 操作同一 Vault，或来源和审计要求较高时，再启用可选 Runtime。第三方 Agent 通过 `orcas-action-v1` 提交结构化操作，Runtime 只做确定性校验和落盘。

## 可选插件

Copilot、Smart Connections 或其他支持文件访问与 Skill/SOP 的 Agent 插件都可以作为自然语言入口。插件不应建立第二套知识数据库，也不应绕过 Orcas 的来源和状态边界。
