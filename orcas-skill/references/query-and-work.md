# Query And Work Workflow

## Answering Questions

1. Search entity names, aliases, summaries, body text, and source links.
2. Prefer active `trusted` knowledge for conclusions.
3. Include relevant `draft` only as a candidate and label it clearly.
4. Treat `stale`, `disputed`, and `superseded` as warnings, not settled facts.
5. Link every important conclusion to the exact knowledge page and original source.
6. Say when evidence is missing instead of filling the gap.

## Preparing Work

Create a task in `work/tasks/` when the request has a goal, audience, deadline, constraints, or deliverable. Store resulting deliverables in `work/outputs/`.

Represent task progress with frontmatter such as `status` or `action_status`; do not use folder moves as the primary state machine. Move inactive historical material to `work/archive/` only when it is no longer part of current work. Create `work/outputs/publishing/` only when a real publishing workflow is needed, and require explicit approval before publication.

Keep the task context small:

- up to 5 relevant knowledge items
- up to 3 original sources
- up to 2 reusable lessons
- up to 1 unresolved conflict

Do not load the entire Vault. Record decisions and outputs in the task; after completion, save only reusable increments to `knowledge/`.

## Default Task Sections

- 当前目标
- 任务信息
- 已确认上下文
- 候选上下文
- 缠绕风险与缺失证据
- 决策记录
- 可复用知识增量
