# Contributing

Thanks for helping improve mathema-agents.

**Licence.** This repository is licensed under Apache-2.0. By submitting a
contribution you agree it is provided under that same licence (inbound =
outbound); you retain your copyright.

**What to change.** The skills in `skills/*/SKILL.md` are the source of
truth. Edit those, not the generated files under `dist/`; then re-run

```
python3 scripts/render_adapters.py
```

and commit the regenerated `dist/` alongside your change so every tool's
adapter stays in sync.

**Style.** Keep the skills provider-neutral: they describe mathema (its
MCP server and CLI), not any one agent or harness. Prefer pointing an
agent at mathema's own just-in-time references (the grammar, verdict and
reason-code resources, and the lexicon) over restating them here.
