<!-- SPDX-License-Identifier: Apache-2.0. Generated from skills/*/SKILL.md by scripts/render_adapters.py. Edit the SKILL.md, not this file, then re-run the script. -->

# mathema

## clear-the-gate

Take a repository from a red `mathema verify` to a green one by preparing every pending human decision so a person can make it in seconds: gather the witness and the source, derive which acceptance verbs are legal, pre-adjudicate any corrected claim, and print the exact command. You never run `mathema accept`. Use when the user asks to "clear the gate", "get verify green", "go through the pending decisions", or "what am I accepting".

Two rules are non-negotiable, whatever tool you drive mathema with:
1. You never adjudicate your own claims. Every verdict you report comes from a mathema call you actually made.
2. You never close your own diagnosis. A falsification says a claim and the code disagree, not which is wrong; that is a human's call (`mathema accept` is deliberately not an agent surface). The same goes for `mathema unlock`: you may lock a function you finished, and only a person unlocks one.

The full procedure is in `skills/clear-the-gate/SKILL.md` (vendor the `skills/` directory from mathema-agents into this repo). Read it before proposing or adjudicating claims, and fetch mathema's own grammar, verdict and reason-code references (served by its MCP server, or `mathema` on the CLI) just in time rather than working from memory.

## design-claims

Design a claim set for a function following the Claim-Driven Development spec: state checkable properties before generating or reviewing code, in the spec's authoring YAML shape, then verify every one against the real implementation instead of asserting it holds. Staged to match the CDD loop in cdd.md (state, implement, verify, diagnose, retain, accept). Use when the user asks to "add claims", "write a claim set", "design claims for this function", or wants code reviewed the CDD way instead of by reading the diff.

Two rules are non-negotiable, whatever tool you drive mathema with:
1. You never adjudicate your own claims. Every verdict you report comes from a mathema call you actually made.
2. You never close your own diagnosis. A falsification says a claim and the code disagree, not which is wrong; that is a human's call (`mathema accept` is deliberately not an agent surface). The same goes for `mathema unlock`: you may lock a function you finished, and only a person unlocks one.

The full procedure is in `skills/design-claims/SKILL.md` (vendor the `skills/` directory from mathema-agents into this repo). Read it before proposing or adjudicating claims, and fetch mathema's own grammar, verdict and reason-code references (served by its MCP server, or `mathema` on the CLI) just in time rather than working from memory.

## start-from-claims

Begin a brand-new project or module the claim-driven-development way: intent and claims are authored first, as the specification, and the implementation is written to satisfy them, the way tests lead in TDD and specs lead in spec-driven development. Covers scaffolding, writing intent before code, stating claims against signatures before bodies exist, and designing the code so its claims can be proved rather than only sampled. Use when the user is starting a new repository or module and asks to "do this claims-first", "spec it with claims", "set up CDD from scratch", or "design the claims before the code".

Two rules are non-negotiable, whatever tool you drive mathema with:
1. You never adjudicate your own claims. Every verdict you report comes from a mathema call you actually made.
2. You never close your own diagnosis. A falsification says a claim and the code disagree, not which is wrong; that is a human's call (`mathema accept` is deliberately not an agent surface). The same goes for `mathema unlock`: you may lock a function you finished, and only a person unlocks one.

The full procedure is in `skills/start-from-claims/SKILL.md` (vendor the `skills/` directory from mathema-agents into this repo). Read it before proposing or adjudicating claims, and fetch mathema's own grammar, verdict and reason-code references (served by its MCP server, or `mathema` on the CLI) just in time rather than working from memory.

## use-mathema-mcp

Drive mathema's MCP server to orient on an unfamiliar codebase, propose claims, and get real verdicts, without reading more source than the job needs. Covers the fifteen tools, the reference resources and procedure prompts the server itself serves, the order that works, and the judgement calls the server cannot make for you. Use when a mathema MCP server is available and the task is "what can be proved about this code", "add claims", "why won't this derive", or any CDD loop step against a real repository.

Two rules are non-negotiable, whatever tool you drive mathema with:
1. You never adjudicate your own claims. Every verdict you report comes from a mathema call you actually made.
2. You never close your own diagnosis. A falsification says a claim and the code disagree, not which is wrong; that is a human's call (`mathema accept` is deliberately not an agent surface). The same goes for `mathema unlock`: you may lock a function you finished, and only a person unlocks one.

The full procedure is in `skills/use-mathema-mcp/SKILL.md` (vendor the `skills/` directory from mathema-agents into this repo). Read it before proposing or adjudicating claims, and fetch mathema's own grammar, verdict and reason-code references (served by its MCP server, or `mathema` on the CLI) just in time rather than working from memory.
