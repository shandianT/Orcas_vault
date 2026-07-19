# 快速开始

## 个人模式

```sh
python3 orcas-skill/scripts/install.py /path/to/my-vault
```

在 Obsidian 中打开目标目录，并在 Agent 中启用 Orcas Skill。

```text
处理 inbox 里的新材料，提取人物、需求和行动项。保留来源，新增内容保持 draft。
```

个人模式没有 Python 运行时。Agent 根据 `SKILL.md` 和 Vault 中的 `AGENTS.md` 直接维护 active draft。

## 可选 Governed 模式

```sh
python3 orcas-skill/scripts/install.py /path/to/my-vault --mode governed
```

只有需要多 Agent、团队协作、严格审计或强制来源保护时才启用。

## 四个目录

```text
inbox/       收材料
sources/     查原文
knowledge/   找可复用内容
work/        做当前任务
```

`work/tasks/` 保存当前任务和行动项，`work/outputs/` 保存交付物，`work/archive/` 保存不再活跃的历史内容。完成状态以前置元数据为准。
