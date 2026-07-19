# Orcas Obsidian 开始页

Orcas 是一套供个人 Obsidian Agent 使用的自然语言运营 Skill。你只需要放入材料，然后说明你想完成什么。

## 直接开始

1. 把会议纪要、文档或网页摘录放进 `inbox/`。
2. 打开 Obsidian 中的 Agent 面板。
3. 用自然语言提出任务。

```text
处理 inbox 里的新材料，提取人物、项目、需求和行动项。保留原始来源，新增内容保持 draft。

查一下 Nicole 提过哪些采购需求，每条结论都给出来源。

根据最近会议生成本周跟进计划，区分已确认事实和候选判断。

找出当前任务真正需要我确认的内容，不要列出所有 draft。
```

## 目录地图

```text
inbox/                         等待处理的新材料
  _processed/                  已处理的入口文件
sources/                       已保存的原始来源，只增不改
knowledge/                     可跨任务复用的知识
  notes/                       事实、决策、经验和主题笔记
  people/                      人物、别名、职责和时间线
  organizations/               组织、客户、供应商和团队
  projects/                    长期项目状态、风险和关键决策
  playbooks/                   可重复使用的方法和检查清单
  attachments/                 知识页面引用的附件
work/                          为完成具体目标而产生的工作内容
  tasks/                       当前任务、行动项、上下文和决策记录
  outputs/                     报告、方案、清单等交付物
  archive/                     已结束且不再活跃的任务与历史结果
```

`knowledge/projects/` 记录可复用的“项目知识”，`work/tasks/` 记录当前要完成的“具体工作”，两者不要混用。

任务是否完成由 frontmatter 中的 `status` 或 `action_status` 表示，不依赖在目录之间反复移动文件。只有内容已经结束、近期也不会继续使用时，才归入 `work/archive/`。需要对外发布时，可按需在 `work/outputs/publishing/` 下建立 `drafts/` 和 `published/`，发布仍需你明确确认。

通常不需要手动整理目录。Agent 会按 Orcas Skill 的规则维护状态、双链和来源。

## 个人模式

默认安装是个人模式：

- 不需要 Python
- Agent 可以直接维护 active draft
- `trusted` 仍只能由你明确确认
- 建议使用 Git 或 Obsidian 文件恢复功能回滚

## 可选 Governed 模式

只有在多人协作、多 Agent、严格审计或高价值知识场景下，才需要安装可选 Runtime。它会增加来源保护、dry-run、状态校验和操作日志。

个人日常使用不需要打开 `.orcas/`，也不需要运行命令。
