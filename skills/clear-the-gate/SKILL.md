---
name: clear-the-gate
license: Apache-2.0
description: >-
  Take a repository from a red `mathema verify` to a green one by preparing
  every pending human decision so a person can make it in seconds: gather
  the witness and the source, derive which acceptance verbs are legal,
  pre-adjudicate any corrected claim, and print the exact command. You
  never run `mathema accept`. Use when the user asks to "clear the gate",
  "get verify green", "go through the pending decisions", or "what am I
  accepting".
---

# Clear the gate

A red `mathema verify` is a queue of decisions, not a list of bugs. A
falsified claim means the code and a claim disagree, and deciding which of
them is wrong is a human act.

**The rule that matters most: you never run `mathema accept`.** Not with
`--yes`, not inside a script, not to save a step. There is deliberately no
accept tool on the MCP surface and a schema test pins that absence. You
prepare the decision and print the command; a person runs it.

That wall is about who decides, not who types. Everything around the
decision is yours: the witness, the source, which verbs are legal, drafting
a correction, running it to see whether it holds, and what comes after.

**Written against mathema 0.6** (`>=0.6,<0.7`). Tool names, the verdict and
acceptance vocabularies, the claim grammar and the badge artifacts all move
between minor versions. If `mathema --version` reports a different line,
say so and check the surface rather than trusting this document.

## What the gate fails on

`verify` defaults to **strict**: a falsified claim, an unaccepted unknown,
and an unverifiable (skipped) one all fail. `--lenient` still fails the
first two and tolerates the third.

Most repositories have surface the routes cannot reach, and those arrive as
`skipped`. They are not decisions anyone owes. Say which mode you are
advising and why, rather than letting a default decide it silently.

Exit codes: `0` clean, `1` gate failure, `2` broken invocation or store.

## Which verb is legal

Derive the legal set from the verdict. Never suggest one the vocabulary
refuses.

| verdict | legal |
|---|---|
| falsified | fix the code, `discovery`, `superseded` |
| unknown, skipped | `risk`, `superseded`, `historical` |
| proven | nothing, a proof is its own acceptance |
| a whole record after a merge | `reconciled`, no claim name |
| a record whose function moved | `reconciled --from OLD_KEY`, keyed by the new name |

**There is no accepting a bug.** If the code is wrong, the code changes,
and the counterexample replays until the claim proves. `--as risk` on a
falsification is refused for exactly this reason.

## `discovery` or `superseded`

Both retire a falsified row; the difference is what you are saying.

**`discovery`**: the falsification was right about the code and wrong about
the claim. The row moves to `discoveries:` **keeping its counterexample as
the witness**, so what was learned survives. Use it when the falsification
taught you something about the code.

**`superseded`**: you are changing what is claimed without disputing the
adjudication. The row moves to an append-only `superseded:` section with
the commit its truth held at. Use it when the claim was mis-stated and
there is nothing to learn.

The test: did this teach you about the code, or only about the claim?

## Pre-adjudicate any correction

`accept --as discovery --corrected "<law>"` runs the replacement against
the live function **before anything is written**, refusing the acceptance
with a counterexample if it falsifies. That only helps if you use it.

Never propose a correction you have not run. Check the grammar with
`parse_claim` (executes nothing), then adjudicate with in-process
`check()`, which writes nothing. Put the result in the brief.

Without `--corrected`, mathema offers a mechanical inverse only when one is
sound and holds, and refuses to invent one from a chained comparison, an
`assuming` premise, a `let` section, an outcome clause or a negated form.
A refusal there means the true law is yours to state.

## Acceptance rewrites the claims files, so leave them alone

When a discovery retires a law, `accept` rewrites every claims file that
declares it, matched canonically. The stanza is replaced by the corrected
claim or removed when there is none, and the plan announces each rewrite
before anything happens. Read those lines into the brief: the user is
consenting to a source edit, not only a record change.

Do not delete the declared claim first, and do not re-author it in advance.
Both fight the acceptance.

A docstring or decorator surface cannot be rewritten this way, so `verify`
is the backstop: a declared claim matching a retired discovery is skipped
with a non-fatal note naming the remedy. **That note is not a gate
failure.** A different law under a retired name is new authorship and
adjudicates normally.

## The unit of interaction is a decision brief

Hand the user what they need in order to choose, with the command at the
end of it, rather than a command with an explanation attached.

```
DECISION n of N                              <dotted.key>
────────────────────────────────────────────────────────
claim      <name>
verdict    falsified          route  <route>
witness    <inputs>  ->  <output>      (claim asserts <law>)
source     <file>:<line>
docstring  "<the line it contradicts>"

WHAT HAPPENED
  <why, in two or three lines, with any threshold measured
  rather than estimated>

YOUR OPTIONS
  [1] the CODE is wrong     <the fix, and its cost>
  [2] the CLAIM was wrong   accept --as discovery
      correction: <law>
      pre-adjudicated: HOLDS over <n> trials
  [3] re-author instead     accept --as superseded
      -> retires without keeping the witness

IF YOU CHOOSE [2], ACCEPT WILL ALSO
  - rewrite <claims file>: <what it does to the stanza>
```

Three things that does which a bare command does not: it puts the
**witness beside the source and the docstring** so the contradiction is
visible rather than inferred; it **pre-adjudicates the options** so the
user cannot pick one that turns out wrong; and it **declares the side
effects before the choice**.

Measure thresholds rather than estimating them. A bisection costs seconds
and "18.714973875118524" is worth far more to the person deciding than
"around 18".

## An adjudication is not undoable, so author deliberately

A claim that falsifies on its first adjudication joins the store's
append-only membership. Deleting it from the claims file does not remove
it: membership is repopulated from the verified row so an adjudication set
never silently shrinks. The exits are supersession and human acceptance.

This is the method, not an obstacle. A verdict that could be erased would
be worth nothing. What follows is that **authoring a claim is a
commitment**, so do the exploring first: try each spelling with in-process
`check()`, which writes nothing, and move only the ones you mean into a
claims file. mathema prints a line naming this the first time a claim
falsifies.

If a bad claim does land, dispose of it through the vocabulary like any
other, usually `superseded`. Never hand-edit or revert the verified layer
to make a falsification disappear: that is the "quietly rewritten into
something true" failure the whole method exists to prevent, and it breaks
the record's integrity stamp besides.

## Order of operations

Gather once (`pending_decisions`, `verify_project`, source spans from
`project_index`), classify, prepare, brief, let the human accept,
re-verify, then refresh coverage, then regenerate badges, then commit.

The two ordering mistakes that actually happen: generating badges **before**
the acceptances, which describes a store that no longer exists, and running
`badges` without refreshing coverage, which silently understates the
implementation score (it unions test, probe and proof reach) or, with no
coverage at all, re-derives reach and runs for many minutes.

## Integrity, and the verb never to reach for

A record whose contents drift from its stamp emits a checksum warning. Fix
it by re-adjudicating the named key, which re-stamps from evidence:

```
mathema verify <key>
```

`accept <key> --as reconciled` vouches for contents **as they stand,
without checking them**. It is for the state after a merge or rebase, where
the cause is known. Never use it to silence a checksum complaint you have
not explained, and never offer it as a peer of re-adjudication.

## A function that moved

A record is keyed by the function's dotted name, so moving or renaming a
function leaves its record under a key that no longer resolves. When that
orphan's form hash matches a function with no record, `verify` fails both
keys and prints the exact command:

```
mathema accept <new.key> --as reconciled --from <old.key>
```

It renames the record, carrying every claim row, acceptance and its
history, the lineage, the PIN stamp and any lock, and removes the old
file. Until someone runs it, the new key gets no record, because a fresh
one would start the history over. Over MCP the same pairing arrives as a
`moved` row from `pending_decisions`, with the command in its detail.

Whether the two are the same function is the human's call, so it goes in
a brief like any other decision. Put both sources side by side: a matching
form hash is strong evidence, not proof, since two small functions can
share one. When the forms differ, mathema asks a second question before
renaming, and `--yes` does not answer it (only `--accept-form-change`
does, and that is the person's flag to pass, never yours); the record then re-adjudicates
against the new code on the next sweep. Never run the rename yourself, and
never delete the orphan record to make the failure go away: that discards
the history the rename exists to keep.

## Report honestly when it is done

**Say what the badges deleted, not only what they wrote.** `badges --out`
owns its directory and prunes any badge-shaped file it did not write,
returning both lists. A deletion usually means a rename upstream, and a
README pointing at the old name would otherwise serve a frozen number.

**Start a README from `readme-snippet.md`**, written beside the badges.
Hand-authoring that block is how a stale badge name survives.

**Quote the clarity ceiling with the clarity score.** A call into a
library the compendium does not model is unknowable from this code, so
clarity tops out below 100 by design; 100 belongs to a pure function whose
entire behaviour is known and claimed, and above 60 a repository is doing
well. A bare percentage invites someone to chase a number that does not
exist, when the ceiling rises with compendium coverage, not with more
claims here.

**Do not claim a falsification feeds clarity.** A row retired into
`discoveries:` leaves the calculation, so accepting a discovery can lower
the score. Say that plainly rather than presenting it as a regression.

## What "done" looks like

`verify` exits 0 in the mode you named, every decision was made by a
person, and you can say for each one what they chose and why. Badges were
regenerated after the acceptances and provably match the store, which
`git diff --exit-code .mathema/badges/` shows. Nothing was pushed unasked.

Then report what stayed open: the claims still skipped, the clarity
ceiling, the risks a human chose to carry. A green gate with unstated gaps
is worth less than a green gate whose gaps are written down.
