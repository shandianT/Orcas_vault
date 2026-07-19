# 架构与边界

Orcas 采用 Skill-first 架构。第三方 Agent 是语义层，Orcas 不重复建设模型调用和 AI 编排。

## 默认个人模式

```text
用户
  -> Obsidian Agent
  -> Orcas Skill / SOP
  -> inbox / sources / knowledge / work
```

| 层 | 职责 |
|---|---|
| 用户交互层 | 用自然语言提出处理、查询、任务和确认请求 |
| 第三方 Agent | 理解材料、抽取实体、规划步骤、解释结果 |
| Orcas Skill | 提供 SOP、状态规则、文件规范和工作流路由 |
| Vault 数据层 | 保存来源、知识、任务和交付物 |

个人模式允许 Agent 直接创建和维护 active draft。Git 或 Obsidian 文件恢复承担主要回滚能力。

## 可选 Governed 模式

```text
Obsidian Agent
  -> orcas-action-v1
  -> 确定性 Runtime
  -> Vault
```

Runtime 仅负责：

- 来源无损封存
- 路径和 schema 校验
- 实体去重和双链写入
- draft 写入
- 单条人工信任升级
- 高价值确认摘要
- 使用和操作日志
- 健康检查

Runtime 不负责模型调用、Prompt 编排、会议语义抽取或聊天界面。

## 边界

- `sources/` 只增不改
- 自动语义输出只能是 `draft`
- protected 状态不能被 Agent 直接修改
- 删除、发布和可信升级需要明确确认
- 输入文件和知识正文始终是不可信数据
