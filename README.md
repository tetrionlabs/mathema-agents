# mathema-agents

Agent-facing setup for [mathema](https://github.com/tetrionlabs/mathema):
skills, prompts, and configuration files that teach coding agents and
assistants to use mathema well, through its public interfaces and its
MCP module.

This repository is deliberately configuration-only. It contains no
Python package, makes no LLM calls, needs no API keys, and has no
dependencies. It works with any provider or harness: the same
material serves Claude Code, Cursor, Codex-style CLIs, or a local
model wired through MCP. Anything that calls a model on your behalf
is a different product and does not live here.

## What's here

- [`skills/design-claims/`](skills/design-claims/SKILL.md): a
  procedure for producing a claim set for a function the
  claim-driven-development way, ending with real verdicts from the
  real checker. The one rule it exists to enforce, and the spine of
  everything in this repository: **an agent proposing a claim never
  adjudicates it, and never closes its own diagnosis.** Verdicts come
  from mathema, or they are not verdicts; and a falsification
  establishes that a claim and an implementation disagree without
  saying which of them is wrong, which is a judgement about intent and
  therefore a human's to make.

- [`skills/start-from-claims/`](skills/start-from-claims/SKILL.md): the
  greenfield inversion of it. On a brand-new project the claims are the
  specification: intent is written first, laws are stated against stub
  signatures and parsed before any body exists, and the implementation
  is done when the checker says the spec holds, the way tests lead in
  TDD. What a green field uniquely buys is provability by design: pure
  scalar cores whose claims come back `proven`, wrappers claimed
  against them, and third-party calls contained where they cannot tax
  what can be known.

- [`skills/clear-the-gate/`](skills/clear-the-gate/SKILL.md): the other
  side of that rule. When a repository's claims are adjudicated, a red
  `mathema verify` is a queue of decisions owed to a person, and this is
  how an agent prepares them without making any of them: the witness
  beside the source it contradicts, which acceptance verbs the verdict
  actually admits, a correction already run so it cannot turn out wrong,
  and the exact command for a human to type. **The agent never runs
  `mathema accept`.** The wall is about who decides, not who types:
  of everything around a decision, only the decision itself needs
  judgement, so everything else is the agent's to prepare.

- [`skills/use-mathema-mcp/`](skills/use-mathema-mcp/SKILL.md): driving
  the MCP server that ships as `mathema[mcp]`, written against the
  fifteen tools, three reference resources and three procedure prompts
  it advertises, and exercised end to end on a real package. The
  server serves its own grammar, reason-code and verdict
  references, and its own procedures as prompts, so this skill covers
  what those cannot: the shape of the surface, what each call costs,
  and the judgement calls. Chiefly that claims compound, since a
  proven claim becomes a lemma the next one can rest on.

## Setup

Three steps: install mathema, register its MCP server (only if you drive
it over MCP), and load these skills into your agent.

These skills target **mathema 0.6**; pin to that line so the tools,
resources and grammar they describe match what you run.

**1. Install mathema** in your project's environment:

```
pip install "mathema[mcp]>=0.6,<0.7"
```

The `[mcp]` extra is only for the MCP server; plain `pip install
"mathema>=0.6,<0.7"` is enough to use it from the CLI (`mathema verify`,
`mathema check`), which the `design-claims` skill works against directly.

**2. Register the MCP server** (skip if you only use the CLI). mathema
serves over stdio via `mathema mcp serve`. Most clients take a JSON
entry:

```json
{
  "mcpServers": {
    "mathema": { "command": "mathema", "args": ["mcp", "serve"] }
  }
}
```

In Claude Code that is one command: `claude mcp add mathema -- mathema
mcp serve`.

**3. Load the skills.** From mathema 0.6, one command fetches this repo
and drops the skills and your tool's adapter into the right places:

```
mathema init --agents claude    # or codex, gemini, cursor, copilot, windsurf, cline
```

Bare `mathema init --agents` detects the tool your project already uses.
It copies only the skills and your one adapter, never this repo's notes
or history; every copied file carries its Apache-2.0 licence line. It leaves any file you have already edited in place
(`--force` to refresh), and if it cannot reach the repo it prints the
manual steps and exits cleanly.

To do it by hand instead, vendor the `skills/` directory into your
repository (copy it in, or add this repo as a git submodule), then copy
the one adapter your tool reads, from the table below.

## Using these with your agent

The skills are the source of truth; anything Claude-specific about them
is only the frontmatter and the `.claude/skills/` location. The same
content is rendered into every other tool's native format by
`scripts/render_adapters.py`, which reads `skills/*/SKILL.md` and writes
lean pointer-adapters into `dist/`. Vendor the `skills/` directory into
your repository, then copy the adapter your tool reads:

| your tool | copy from `dist/` to your repo |
|---|---|
| Claude Code | (none) use `skills/` directly, or copy it under `.claude/skills/` |
| Codex / Zed / Aider / Jules / most others | `AGENTS.md` |
| Gemini CLI | `GEMINI.md` |
| Cursor | `.cursor/rules/*.mdc` |
| GitHub Copilot | `.github/copilot-instructions.md` |
| Windsurf | `.windsurf/rules/*.md` |
| Cline / Roo | `.clinerules/*.md` |

Each adapter carries the skill's description and the two non-negotiable
rules, and points at the vendored `SKILL.md` for the full procedure, so
every tool's config file stays small and there is one source of depth.
Edit a `SKILL.md`, re-run `python3 scripts/render_adapters.py`, and
commit the regenerated `dist/`. `python3 scripts/check_skills.py` verifies
that, and is what CI runs: it fails when `dist/` no longer matches the
skills, so a stale adapter cannot ship unnoticed.

## Relationship to mathema and the spec

Readable without either installed; actionable where an
implementation of the claim-driven-development spec (mathema, today)
is present. Nothing in mathema or the spec depends on this
repository.
