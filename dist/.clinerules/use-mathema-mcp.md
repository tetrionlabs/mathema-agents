<!-- SPDX-License-Identifier: Apache-2.0. Generated from skills/*/SKILL.md by scripts/render_adapters.py. Edit the SKILL.md, not this file, then re-run the script. -->

# use-mathema-mcp

Drive mathema's MCP server to orient on an unfamiliar codebase, propose claims, and get real verdicts, without reading more source than the job needs. Covers the fifteen tools, the reference resources and procedure prompts the server itself serves, the order that works, and the judgement calls the server cannot make for you. Use when a mathema MCP server is available and the task is "what can be proved about this code", "add claims", "why won't this derive", or any CDD loop step against a real repository.

Two rules are non-negotiable, whatever tool you drive mathema with:
1. You never adjudicate your own claims. Every verdict you report comes from a mathema call you actually made.
2. You never close your own diagnosis. A falsification says a claim and the code disagree, not which is wrong; that is a human's call (`mathema accept` is deliberately not an agent surface). The same goes for `mathema unlock`: you may lock a function you finished, and only a person unlocks one.

The full procedure is in `skills/use-mathema-mcp/SKILL.md` (vendor the `skills/` directory from mathema-agents into this repo). Read it before proposing or adjudicating claims, and fetch mathema's own grammar, verdict and reason-code references (served by its MCP server, or `mathema` on the CLI) just in time rather than working from memory.
