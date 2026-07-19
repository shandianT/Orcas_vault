# 人物实体

人物名称使用 Obsidian 双链，人物页的 `tags` 用于检索和分类。固定类型标签为 `entity/person`，业务标签可在创建时重复传入 `--tag`。

```sh
python3 .orcas/scripts/entity.py new person "林舟" \
  --alias "小林" \
  --tag "客户" \
  --tag "决策人" \
  --source sources/meeting.md
```

生成的标题为 `# [[林舟]]`。不要把整段会话直接归档到人物页；后续变化使用 `append` 追加带日期的时间线，并继续引用来源双链。
