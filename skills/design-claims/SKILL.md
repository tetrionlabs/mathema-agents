---
name: design-claims
license: Apache-2.0
description: >-
  Design a claim set for a function following the Claim-Driven Development
  spec: state checkable properties before generating or reviewing code, in
  the spec's authoring YAML shape, then verify every one against the real
  implementation instead of asserting it holds. Staged to match the CDD
  loop in cdd.md (state, implement, verify, diagnose, retain, accept). Use
  when the user asks to "add claims", "write a claim set", "design claims
  for this function", or wants code reviewed the CDD way instead of by
  reading the diff.
---

# Design claims

A method for authoring claims on a function or codebase that prevent
regressions, check assumptions, and tie down expected behavior, in the
shape defined by the Claim-Driven Development spec
(<https://github.com/aaronbyrnephd/claim-driven-development>, version
`v0.2.0/`), and run through the CDD loop
that spec defines. The deliverable is a claim set plus its actual verified
verdicts, never a claim set alone.

**The rule that matters most: you never adjudicate your own claims, and
you never close your own diagnosis.** Proposing a law and believing it
holds are different acts, and so are establishing that a claim and an
implementation disagree and deciding which of them is at fault. Every claim you
write here gets run through the real checker against the real function
before you report anything about it. If you cannot run the checker (no
implementation available, no test harness), say that plainly instead of
asserting a verdict.

**Written against mathema 0.6** (`>=0.6,<0.7`). Tool names, the verdict and
acceptance vocabularies, the claim grammar and the badge artifacts all move
between minor versions. If `mathema --version` reports a different line,
say so and check the surface rather than trusting this document.

## Before you start

Read `claim-anatomy.md` and `record-schema.md` in the spec's `v0.2.0/`
(<https://github.com/aaronbyrnephd/claim-driven-development/tree/main/v0.2.0>)
if you have not already. This
skill assumes you know the claim tuple (quantifiers, law, domain,
tolerance, evidence route) and the authoring YAML shape.

## Four things every claim routes through

Before writing any claim, know which of these four things you're actually
looking at; conflating them is where most bad claim sets come from.

- **Intent**: why the function exists, what it's for. Declared (someone's
  stated purpose, written before checking) or documented (read from the
  function's own docstring); see `record-schema.md`, "Where `intent`
  comes from," for how those two differ and which wins when they disagree.
- **Concept**: the claim itself, the specific behavior being asserted
  ("f is odd," "this sum is conserved"). This is the core of the four; the
  other three all exist in relation to it. The claim families in
  `claim-anatomy.md` (symmetry, order, conservation, ...) aren't the
  concept, they're a checklist for *finding* one: walking them
  systematically is how you discover candidate concepts worth turning into
  claims. There's no `family` field in the v0.2 schema, and there doesn't
  need to be; the concept lives as the claim's own `law`, not as a
  separate tag.
- **Evidence**: what checking actually produces, the test outcomes and
  claim-check results, a verdict and its basis (`holds (n=...)`,
  `falsified` with a counterexample, `skipped` with a reason). See
  `evidence-ladder.md` for what each is worth. This is the one thing on
  this list you cannot supply yourself; only the real checker, run against
  the real codebase, produces it.
- **Implementation**: the actual codebase, not your model of it. Every
  claim ultimately has to be checked against this, and against nothing
  else.

A good claim-design pass keeps these straight: state the intent you're
working from, find a concept worth claiming by walking the families as a
checklist, then get real evidence by checking that concept against the
actual implementation. Skip the last step and you've produced a
plausible-sounding claim with no epistemic weight behind it, which is
exactly the failure mode this whole method exists to prevent.

## Stages

Staged to match `cdd.md`'s loop exactly, one section per step, so it's
always clear which part of the cycle you're in.

### Stage 1: State claims

This is the stage this skill mainly does. Three parts:

1. **Read the function, not just its name.** Get its intent (its
   docstring if it has one, or ask), its parameters and their kinds
   (scalar, sequence, int), and whether it's pure. Impure functions still
   get claims about determinism and effects, but algebraic laws over their
   output are not meaningful; say so rather than proposing them.

2. **Walk the concepts and ask, for each, "does this plausibly apply?"**
   Do not propose one just because it exists in `claim-anatomy.md`;
   propose it because you have a specific reason to think the function has
   that property.
   - **Symmetry / intertwining**: is there an operation `T` on the input
     that induces a predictable operation `S` on the output? Even/odd,
     permutation-invariance, scale- or translation-equivariance are common
     instances. A moving average over time is *not* permutation-invariant;
     saying so is itself a claim worth stating and falsifying on purpose.
   - **Order**: is the output monotone in some input? Bounded by the
     input's own range? A contraction?
   - **Compositional**: is `f` idempotent (`f(f(x)) == f(x)`)? Involutive?
     A homomorphism over some operation?
   - **Aggregate / conservation**: does some total, sum, or norm get
     preserved or predictably transformed?
   - **Asymptotic**: does behavior over a growing family of inputs matter
     more than any single call? (Not evaluable by the reference
     implementation's conjecture pipeline in v0.2; state it anyway if it's
     true, and expect `skipped`.)
   - **Structural**: purity, determinism, complexity. Cheap to state,
     often skipped because they seem too obvious to write down; write them
     down anyway, they're real coverage.

3. **Write each candidate as a law and assemble the authoring-shape
   YAML**, over `f` and the function's own parameter names, plus any
   auxiliary variable you need (an extra lowercase name not among the
   parameters; the reference checker samples it independently as a real
   number). Calls are restricted, by design, because claim sets are meant
   to accept untrusted proposals: a safe set of maths functions is
   admitted and anything else is rejected before it runs. Don't fight it;
   restate the law inside the allowed grammar.

   **Read the checker's own grammar reference rather than trusting this
   paragraph.** The accepted language is materially richer than any
   summary suggests, and an author working from a paraphrase leaves
   evidence on the table. Two constructs earn their keep often enough to
   name here:

   - `assuming <precondition>, <law>` states the condition a law holds
     under. `assuming is_defined(f), |f(x, y)| <= 1` is what lets a claim
     about a two-sequence function survive inputs the function
     legitimately refuses; without it the same law falsifies on
     synthesised mismatched-length arguments and reads like a bug in the
     code. On one real run that single spelling was what made fourteen
     claims adjudicable at all.
   - `let g = pkg.module.function` binds a named function, so a law can
     relate two implementations: how you claim that a vectorised routine
     agrees with the scalar core you extracted from it.
   - **A dimension premise states a size precondition directly**, which is
     what most numeric code actually needs.
     `assuming len(x) == len(y), f(x, y) == f(y, x)` says the two sequences
     must agree, rather than leaning on `assuming is_defined(f)` to imply
     it. A minimum works on the length or on a named dimension:
     `assuming len(X) > 6, ...` and
     `for X in R^(n*m), assuming n > 6, ...` both adjudicate. Constrain a
     dimension as a premise, not as a quantifier.

   Where the checker publishes its lexicon (mathema serves it as a
   resource, and `claim_grammar` returns the same content), fetch it once
   at the start and write against that.

   ```yaml
   module.qualname:
     intent: one line, what the function is for
     signature: "(types) -> type"
     grammar: python-expression   # names the dialect the law strings below are written in
     claims:
       - name: odd
         law: "f(-x) == -f(x)"
   ```

   **Omit `route:` unless you mean to constrain it.** A checker with more
   than one route picks the strongest it can serve for each claim, and
   pinning a route can only take evidence away. This is worth stating
   flatly, because getting it wrong is expensive and entirely silent. On
   one real run a claim set written with `route: probe` throughout
   adjudicated **0 proven, 70 holds, 22 skipped**; the identical file with
   the route line removed gave **39 proven** and adjudicated 20 of the 22.
   Nothing anywhere indicated that the pin was the cause.

   Pin a route only to *say something*: `derive` to record that you believe
   a proof exists even where no available tool can check it yet, or `probe`
   to say a symbolic proof is not what you want here. If you have no such
   intent, leave the field out. Set `grammar` to whatever names the dialect
   your `law` strings are actually written in; don't leave it unset and
   assume a reader will guess right.

### Stage 2: Implement, or generate

Not usually this skill's job; the function you're designing claims for
typically already exists. When it doesn't yet, the claim set from Stage 1
is exactly the contract that generation (human or agent) should work
from, the same way a test suite already informs implementation in TDD.
Nothing else to do here beyond handing that claim set over.

### Stage 3: Verify

The stage the non-negotiable rule is about, and where **evidence** actually
gets produced; nothing in Stage 1 was evidence yet. Run the claims against
the real function, immediately, before reporting anything:

Write the claims into `claims/*.claims.yaml`, keyed by dotted function
name, and adjudicate the file rather than a hand-assembled list. Against a
reference implementation that reads the declared layer, that is one command
for a whole project:

```bash
mathema verify --root .
```

or, over MCP, `adjudicate_targets` for a pass and `verify_project` for the
sweep. Adjudicating the file rather than a Python list matters for a reason
the spec cares about: the claims a human reviews in the diff are exactly the
claims that were run.

Whatever the surface, the spec-defined part is the same: report the real
verdicts, `proven` where a symbolic derivation closed, `holds (n=...)` under
seeded probing, `falsified` with its counterexample, or `skipped` with the
reason. Report the strongest evidence honestly rather than flattening the
tiers; a summary that calls a proof a `holds` has thrown away the thing the
ladder exists to record.

### Stage 4: Diagnose

For every falsified claim, determine which of the two causes it is,
mirroring `cdd.md`'s loop exactly: either the **implementation** is
wrong, in which case the counterexample belongs in a regeneration prompt
(back to Stage 2), or the claim was wrong, a genuine discovery about the
function rather than a defect in it. A falsified claim is not a failure
to explain away; it's exactly the information this method exists to
produce.

**The two causes are not equally likely, and which one to suspect first
depends on the code you're pointed at.** A falsification tells you a claim
and an implementation disagree, and it is silent on which of them is wrong,
so the prior you bring to that question does most of the work. Read the
prior off the code rather than guessing at it:

- **Fresh, generated, or thinly tested code.** The claim is doing the job a
  specification does, namely saying what the function is supposed to be, so
  a disagreement is a defect until shown otherwise. This is the greenfield
  case the loop was written for, and the counterexample goes straight into
  a regeneration prompt.
- **Mature, released, well-tested code.** The implementation is the artifact
  with years of evidence behind it and your claim is a few minutes old, so a
  novel claim that falsifies is more likely to have misread the design than
  to have found a bug nobody hit. Treat it as a misunderstanding until a
  human says otherwise.

The signals are all readable, so look them up instead of forming an
impression: `mathema audit`'s `tested` column says whether an existing
coverage report reaches this specific function, the git history says how
long the code has been still, release tags and downstream dependents say
whether anyone would have noticed, and the presence of a property-style
test suite says whether the behaviour you're claiming was already someone
else's concern. Most codebases are mixed, and the level that matters is the
function's, not the repository's.

**Before reporting any falsification as a defect, write the claim that
would hold if the code were right, and check it.** If the code is correct,
some other statement of the same behaviour must be true, and a held claim
that cleanly explains the falsification is strong evidence that the claim,
not the code, was wrong. This costs one more round through Stage 3 and it
is the single highest-value habit in this stage.

**Report a falsification as a disagreement, never as a verdict on the
code.** "Claim X and the implementation disagree, here is the witness"
carries exactly the same information as "the code is wrong" while leaving
the diagnosis open, and it invites the correction rather than foreclosing
it. Where the diagnosis turns on design intent that is not present in the
source, namely the reasons a thing was built the way it was, route it to a
human as a question; no amount of further reading will recover intent that
was never written down, and a confident guess at it is how working code
gets "fixed".

**You propose claims and you do not close your own diagnosis.** The rule at
the top of this skill has a second half here. The checker adjudicates, and
it will be right that the claim and the code disagree, but deciding which
of them is at fault is a judgement about intent rather than about evidence,
which is why `mathema accept --as discovery` is a human step and is
deliberately absent from every agent-facing surface. An agent that closes
its own diagnosis files bugs against working code.

### Stage 5: Retain as new knowledge

A claim diagnosed as a genuine discovery gets kept, not deleted and not
quietly rewritten into something true. Report it as falsified, with its
counterexample, as part of the record. This is knowledge about the
function now, the same standing as any held claim.

mathema enforces this rather than trusting it. An adjudicated claim joins
the store's append-only membership, so deleting it from a claims file does
not remove it: membership is repopulated from the verified row. The only
exits are supersession and human acceptance. Treat that as a reason to
**author deliberately**, exploring each spelling with `check()` (which
writes nothing) and moving only the ones you mean into a claims file.

### Stage 6: Accept

Report claim coverage, not a pass/fail summary: how many claims were
proposed, how many hold, how many were falsified (with their
counterexamples, carried over from Stage 5), and how many could not be
evaluated and why. Unclaimed behavior is not neutral: it's a degree of
freedom nobody checked, and it's fine to say so explicitly.

Reporting is where your part ends. A falsified or unknown claim leaves a
decision owed to a person, which they record with `mathema accept`, and
**you never run that command**. Preparing those decisions well, with the
witness, the legal verbs and a pre-adjudicated correction, is the
`clear-the-gate` skill.

## What "done" looks like

A finished claim-design pass produces: the YAML claim set in the authoring
shape, and a real verdict for every claim in it, obtained by actually
running the checker in Stage 3, not by reasoning about what you expect it
to say. Anything you could not run gets an honest `skipped`, not a
confident guess dressed up as a verdict.

## Common mistakes to avoid

- **Asserting a verdict without running the checker.** This is the one
  failure mode that defeats the entire point of CDD; the whole method
  exists because trusting an agent's unverified claim about its own code
  is exactly the problem it's solving.
- **Treating the claim families as a field to fill in rather than a
  checklist for finding concepts.** There's no `family` field in the v0.2
  schema; walking symmetry, order, conservation, and so on is how you
  discover which concepts are worth claiming in Stage 1, not something to
  invent schema for once you've found one.
- **Proposing a claim in a grammar the checker will reject**, then
  reporting it as `falsified` when it was actually `skipped` for being
  unparseable. Read the note field; a skip and a falsification mean
  different things.
- **Reporting a falsification as a bug in the code.** The checker
  establishes that a claim and an implementation disagree and says nothing
  about which is wrong, so the wording that matches the evidence is "these
  disagree, here is the witness". The pull toward blaming the code is
  strong and worth naming: you wrote the claim so you already believe it,
  the counterexample is concrete and arrives with machine authority while
  "I misread the design" comes with no artifact at all, and finding a
  falsification feels like the method working. On mature, well-tested code
  that instinct is usually wrong. See Stage 4.

- **Deleting or rewriting a falsified claim to make it pass.** If the code
  is right and the claim was wrong, the falsified claim stays in the
  record as a discovery (Stage 5). If the code is wrong, fix the code and
  re-run from Stage 3; don't weaken the claim until it happens to hold.
- **Padding coverage with trivial claims** (`f(x) == f(x)`) to inflate the
  count in Stage 6. A trivial claim is fine as a determinism check,
  labeled as one; it is not a substitute for a real property.
