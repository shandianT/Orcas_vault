# 参与贡献

感谢你帮助改进 Orcas Context OS。项目优先接受能降低维护摩擦、提高上下文准确性或增强 Obsidian 可用性的改动，不以增加目录和规则数量为目标。

## 开始之前

1. 先阅读 `docs/method.md`、`docs/task-context-spec.md` 和 `starter-vault/AGENTS.md`。
2. 新功能应说明解决的真实任务问题、用户维护成本和失败时的降级方式。
3. 不要在示例和测试中加入真实个人数据、密钥或受限资料。

## 提交改动

- 文档和模板保持普通 Markdown，可在无插件 Obsidian 中打开。
- 脚本只使用 Python 3 标准库，除非项目先形成明确的依赖策略。
- 不得覆盖或删除 `sources/` 中的已有证据。
- 不得让 AI 自动把知识升级为 `verified`。
- 规则演进必须给出失败证据、适用范围、例外、验证和回滚方式。
- 新行为需要在 `tests/test_smoke.py` 或相邻测试中覆盖。

运行验证：

```sh
python3 -m py_compile starter-vault/scripts/*.py tests/test_smoke.py
python3 tests/test_smoke.py
```

## Issue 建议格式

请说明：任务场景、当前行为、期望行为、维护成本变化、风险等级、可复现材料和可能的降级方案。效果数字必须来自实际试点，不能使用推测值冒充结果。
