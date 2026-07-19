# Trust And Review Workflow

## Confirmation On Use

Do not create a queue from every draft. Surface an item only when:

- the current answer or task will rely on it
- it conflicts with trusted knowledge
- it changes trusted content
- it contains a high-risk commitment, owner, amount, or deadline
- it is stale trusted knowledge being reused
- the operation deletes, publishes, replaces, or activates a rule

Unused low-risk drafts remain quiet.

## Explicit Trust Promotion

Before changing `draft` to `trusted`:

1. Identify one exact Markdown file.
2. Show its claim and source.
3. Obtain an explicit user confirmation.
4. Change only that file.
5. Add a trust record with date, actor, and evidence.

Never promote a directory, wildcard, query result set, or implicit group.

## Conflicts

Do not overwrite either side. Mark the unresolved relationship and present both sources. Let the user decide whether one item becomes `superseded`, remains `disputed`, or needs more evidence.
