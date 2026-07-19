# 实体优先工作流

长期工作中的变化通常围绕人物、组织和项目发生。Standard 默认使用：

- `knowledge/people/`：人物、角色、偏好、承诺和关系
- `knowledge/projects/`：项目状态、关键决策、风险和下一步
- `knowledge/organizations/`：组织背景、合作关系和约束
- `knowledge/notes/`：跨实体、跨任务仍可复用的结论

实体页包含别名、类型标签、当前状态、关系、未解决事项、带日期的时间线和来源。人物标题使用 Obsidian 双链，例如 `# [[林舟]]`；固定标签为 `entity/person`，业务标签可用多个 `--tag` 追加。新材料若只是更新某个实体，优先追加时间线。

```sh
python3 .orcas/scripts/entity.py new person "林舟" --alias "小林" --tag "客户" --source sources/meeting.md
python3 .orcas/scripts/entity.py append person "林舟" "确认先提交风险清单" --date 2026-07-19 --source sources/meeting.md
python3 orcas.py ask "林舟最近确认了什么" --kind entity
```

查询不会创建任务文件。只有需要交付物、持续决策记录或较高风险的工作，才运行 `python3 orcas.py project "任务目标"` 创建 `work/` 文件。
