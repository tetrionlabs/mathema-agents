<!-- SPDX-License-Identifier: Apache-2.0. Generated from skills/*/SKILL.md by scripts/render_adapters.py. Edit the SKILL.md, not this file, then re-run the script. -->

# clear-the-gate

Take a repository from a red `mathema verify` to a green one by preparing every pending human decision so a person can make it in seconds: gather the witness and the source, derive which acceptance verbs are legal, pre-adjudicate any corrected claim, and print the exact command. You never run `mathema accept`. Use when the user asks to "clear the gate", "get verify green", "go through the pending decisions", or "what am I accepting".

Two rules are non-negotiable, whatever tool you drive mathema with:
1. You never adjudicate your own claims. Every verdict you report comes from a mathema call you actually made.
2. You never close your own diagnosis. A falsification says a claim and the code disagree, not which is wrong; that is a human's call (`mathema accept` is deliberately not an agent surface). The same goes for `mathema unlock`: you may lock a function you finished, and only a person unlocks one.

The full procedure is in `skills/clear-the-gate/SKILL.md` (vendor the `skills/` directory from mathema-agents into this repo). Read it before proposing or adjudicating claims, and fetch mathema's own grammar, verdict and reason-code references (served by its MCP server, or `mathema` on the CLI) just in time rather than working from memory.
