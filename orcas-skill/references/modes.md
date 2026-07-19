# Installation Modes

## Personal Mode

Recommended for an individual Obsidian Vault.

- no Python runtime installed in the Vault
- Agent directly maintains active draft Markdown
- Git is the preferred rollback mechanism
- protected state changes still require explicit confirmation

Install:

```sh
python3 scripts/install.py /path/to/vault
```

## Governed Mode

Use when multiple Agents, team collaboration, strict source immutability, or audit logs justify stronger enforcement.

- includes `.orcas/` and `orcas.py`
- writes go through `orcas-action-v1`
- dry-run, path validation, status checks, and action logs are enabled

Install:

```sh
python3 scripts/install.py /path/to/vault --mode governed
```

Enabling governed mode later is additive. It does not delete or relocate existing Vault content.
