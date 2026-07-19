# Changelog

## 0.8.1 - 2026-07-19

- 补充 `START-HERE.md` 的二级目录地图，明确 `knowledge/` 与 `work/` 各子目录的职责。
- 将 `work/` 默认结构调整为按对象组织的 `tasks/`、`outputs/` 和 `archive/`，任务状态继续由 frontmatter 表达。
- 将发布流程改为按需创建的 `work/outputs/publishing/`，避免默认暴露 `_publish` 实现目录。
- Governed Runtime 默认写入新路径，并为旧 `work/`、`_done/`、`_publish/` 提供无损迁移兼容。

## 0.8.0 - 2026-07-19

- 将产品重构为 `Orcas Obsidian Skill`，默认面向个人 Obsidian 自然语言运营。
- 新增标准 `orcas-skill/` 包，包含 `SKILL.md`、Agent UI 元数据、会议处理、查询任务、确认策略和安装模式 references。
- 新增安装器，默认安装无 Python 的 Personal 模式，可选 `--mode governed` 注入轻量确定性 Runtime。
- Personal 模式允许 Agent 直接维护 active draft，同时保留来源只增不改、protected 状态和人工确认边界。
- Governed Runtime 移除内置模型调用、AI 编排、mock AI 和规则自生成，只保留来源、查询、上下文、实体、Action Gateway、确认、审计和健康检查。
- 将 `starter-vault/` 改为纯个人 Vault 模板，并将 Runtime 独立到 `governed-runtime/`。
- 更新 README、开始页、架构、快速开始和 Obsidian 指南，明确 Skill-first、Runtime optional。

## 0.7.2 - 2026-07-19

- 新增 `orcas-action-v1` 统一 Agent 操作协议和 `orcas.py agent` 入口，支持 JSON 文件或标准输入。
- 新增 dry-run、操作白名单、Vault 路径限制、顺序感知来源校验、自动状态限制和执行审计。
- 支持第三方 Agent 受控执行来源封存、实体 upsert、实体时间线、任务、行动项和高风险确认项。
- 新增 `orcas.py review`，只汇总使用中的 draft、高风险 draft、待处理确认和正在使用的过期 trusted。
- 阻止自动实体工具修改已有 trusted、stale、disputed 或 superseded 实体。
- 将开始页、快速开始和 Obsidian 指南改为自然语言优先，Python 命令降级为插件集成和兼容入口。

## 0.7.1 - 2026-07-19

- 人物实体页标题改为 Obsidian 双链，例如 `# [[林舟]]`。
- 实体 frontmatter 新增固定类型标签，人物默认包含 `entity/person`。
- `entity.py new` 新增可重复使用的 `--tag` 参数，并自动去重标签、别名和来源。
- 再次创建已有人物时会兼容升级纯文本标题和缺失标签，不破坏原有时间线。
- 时间线中的来源改为 Obsidian 双链，同时保持 frontmatter 相对路径和查询兼容。

## 0.7.0 - 2026-07-19

- 将默认用户界面收敛为四个一级目录：`inbox/`、`sources/`、`knowledge/`、`work/`。
- 将脚本、模板、规则、确认队列、健康报告和学习报告全部收入隐藏的 `.orcas/`。
- `knowledge/` 按需承载 notes、people、organizations、projects、playbooks 和 attachments。
- `work/` 按需承载进行中任务、`_done/` 和 `_publish/`，不再暴露多个生命周期一级目录。
- 新增编号版 v0.6 到 work-first 四目录结构的无损迁移映射。
- 保留 v0.5 legacy、编号版 v0.6 和四目录 work-first 三种结构兼容读取。
- 修复隐藏脚本目录作为 Vault 根路径时的报告、规则提案和 AI 编排路径问题。
- 更新开源文档，明确目录是用户心智模型，Capture -> Ground -> Apply -> Learn 是运行方法而不是额外目录。

## 0.6.0 - 2026-07-19

- 融合低认知业务目录与 Orcas 治理内核，Standard 默认使用 `00-Inbox`、`01-Raw`、`02-Wiki`、`03-Projects`、`04-Playbooks` 和 `05-Publish`。
- 新增 `.orcas/config.json` 和 `scripts/config.py`，目录可映射到现有 Vault 或 llm-wiki，同时保留无配置 v0.5 自动回退。
- 新增统一入口 `orcas.py`，覆盖初始化、收集、查询、项目、人工信任、健康检查和无损迁移。
- 发布 `Capture -> Ground -> Apply -> Learn` 方法论，并定义 Lite、Standard、Governed 渐进采用级别。
- 统一新内容状态为 `trusted`，继续兼容旧 `verified`；AI 仍只能自动生成 `draft`。
- 修复中文无关查询误命中、上下文重复注入、使用路径重复、trusted 正文状态不同步和过期 trusted 复核。
- 强化 AI JSON 契约，空响应、缺少必需字段或越权输出不写入 Vault。
- 增加 Standard、legacy 回退、迁移预览/执行、统一入口和治理闭环回归测试。

## 0.5.0 - 2026-07-19

- 增加共享 frontmatter 解析器，支持嵌套字段和 Obsidian 多行列表。
- 引入 `draft / trusted / stale` 与独立 `resolution`，兼容旧 `verified`。
- 上下文递归检索知识和实体，高相关 draft 以候选形式注入。
- 来源只来自选中知识引用，取消 mtime 回退。
- 增加实体时间线、零仪式查询、单条信任升级、偏好、playbook、skill 注册表和使用事件。
- 保留 AI 不得自动 trusted、sources 只增不改和提示注入边界。

## 0.4.0 - 2026-07-19

增加受控规则自迭代闭环。

- 新增 `scripts/learn.py`，支持学习事件记录、证据门槛、候选提案、离线评估、人工批准、版本归档、回滚和指标报告
- AI 只能生成 `_meta/rules/proposals/` 候选，不能直接激活或修改生效规则
- 新增 `_reports/learning/` 审计事件、评估和回滚记录
- 新增 active/archive 规则版本模型，回滚后版本号保持单调递增
- 健康检查增加 active 规则结构校验
- 新增自迭代文档和端到端烟囱测试

## 0.3.0 - 2026-07-18

接入可替换的 AI 编排层。

- 新增 `scripts/ai.py`，支持材料处理、任务准备、任务复盘和过期复核
- 新增本地命令适配器和 OpenAI-compatible HTTP 适配器
- AI 输出必须符合 JSON schema，非法输出不会写入 Vault
- AI 自动写入限制为 `draft`，高风险变更进入确认队列
- 新增离线 `examples/mock-ai.py`，无需 API 密钥即可测试编排协议
- 扩展端到端测试，覆盖来源注入、越权状态、任务简报和过期复核
- 补齐完整架构和 AI 编排文档

## 0.2.0 - 2026-07-18

将项目从低摩擦试点推进为可公开发布、可直接复制到 Obsidian 的方法论包。

- 新增任务上下文规范，固定 task、context、output 三层结构
- 新增 Obsidian 使用指南，明确无插件最低可用路径
- 新增三阶段实施路线，避免过早实现复杂治理
- 上下文构建改为区分已核实知识、历史决策、可复用经验和未解决冲突
- 上下文排序加入状态、来源质量、新鲜度和复用次数
- 上下文来源优先使用被选知识实际引用的来源，不再按文件名盲选
- 任务模板增加 audience、deadline、output 和 risk_level
- 新增上下文包与知识增量模板
- 扩展烟囱测试覆盖上下文字段、预算和冲突
- 新增 CONTRIBUTING、SECURITY、CODE_OF_CONDUCT 和 VERSION

## 0.1.0 - 2026-07-18

首个低摩擦试点版本。

- 将七个生命周期工位压缩为六个用户可理解目录
- 将知识明确拆为 fact、insight、decision、lesson、rule
- 引入 draft、verified、stale、disputed、superseded 状态
- 将状态映射为明确的读取、修改和删除权限
- 引入任务上下文预算与轻量相关性排序
- 增加原始来源防覆盖 intake 脚本
- 增加高风险确认队列
- 增加可追溯性、新鲜度和结构健康检查
- 增加四周效果试点与 ORCA 迁移指南
