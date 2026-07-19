# Skill 的受控改进

Orcas 的“越用越聪明”不是让模型自行修改规则，而是把重复纠正沉淀为可审核的 Skill 或 SOP 修改。

```text
真实任务失败
  -> 记录具体例子
  -> 判断是否重复出现
  -> 修改 SKILL.md 或 reference
  -> 用历史材料回放验证
  -> 人工接受后发布新版本
```

## 什么时候值得修改 Skill

只有满足以下条件之一才建议修改：

- 同类错误在不同任务中重复出现
- 用户多次纠正同一工作步骤
- 某个字段、路径或状态规则经常被遗漏
- 一个新流程已被真实采用并证明可复用

单次偏好、偶发错误和没有实际使用记录的想法，不应立即写成全局规则。

## 修改位置

- 触发范围或总原则：`orcas-skill/SKILL.md`
- 会议和材料处理：`references/meeting-workflow.md`
- 查询和任务上下文：`references/query-and-work.md`
- 确认和状态变化：`references/trust-and-review.md`
- 安装和模式选择：`references/modes.md`
- 确定性写入约束：`governed-runtime/`

## 验证方法

1. 保存导致修订的真实输入和错误结果。
2. 至少选择一个不同来源的相似任务。
3. 验证新规则能修复原错误。
4. 验证它不会扩大到无关任务。
5. 运行烟囱测试和安装测试。
6. 通过 Git diff 审核后再发布。

Agent 可以提出 Skill 修改建议，但不能自行发布新版本、删除旧规则或改变 protected 状态边界。
