<!-- SPDX-License-Identifier: Apache-2.0. Generated from skills/*/SKILL.md by scripts/render_adapters.py. Edit the SKILL.md, not this file, then re-run the script. -->

# design-claims

Design a claim set for a function following the Claim-Driven Development spec: state checkable properties before generating or reviewing code, in the spec's authoring YAML shape, then verify every one against the real implementation instead of asserting it holds. Staged to match the CDD loop in cdd.md (state, implement, verify, diagnose, retain, accept). Use when the user asks to "add claims", "write a claim set", "design claims for this function", or wants code reviewed the CDD way instead of by reading the diff.

Two rules are non-negotiable, whatever tool you drive mathema with:
1. You never adjudicate your own claims. Every verdict you report comes from a mathema call you actually made.
2. You never close your own diagnosis. A falsification says a claim and the code disagree, not which is wrong; that is a human's call (`mathema accept` is deliberately not an agent surface). The same goes for `mathema unlock`: you may lock a function you finished, and only a person unlocks one.

The full procedure is in `skills/design-claims/SKILL.md` (vendor the `skills/` directory from mathema-agents into this repo). Read it before proposing or adjudicating claims, and fetch mathema's own grammar, verdict and reason-code references (served by its MCP server, or `mathema` on the CLI) just in time rather than working from memory.
