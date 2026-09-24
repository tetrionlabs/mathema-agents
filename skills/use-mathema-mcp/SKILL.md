---
name: use-mathema-mcp
license: Apache-2.0
description: >-
  Drive mathema's MCP server to orient on an unfamiliar codebase, propose
  claims, and get real verdicts, without reading more source than the job
  needs. Covers the fifteen tools, the reference resources and procedure
  prompts the server itself serves, the order that works, and the judgement
  calls the server cannot make for you. Use when a mathema MCP server is
  available and the task is "what can be proved about this code", "add
  claims", "why won't this derive", or any CDD loop step against a real
  repository.
---

# Use mathema over MCP

mathema adjudicates claims about code: you state a property, it decides
whether it holds, and it says how strongly it knows. This skill drives it
through its MCP server.

Two rules govern everything, and neither is negotiable.

**You never adjudicate your own claims.** Proposing a law and believing it
holds are different acts. Every verdict in your report comes from a tool
call you actually made, or it is not a verdict.

**You never close your own diagnosis.** A falsification establishes that a
claim and an implementation disagree; it does not say which is wrong. That
turns on intent, not evidence, which is why there is no accept tool and why
`pending_decisions` can only tell you a decision is owed.

**Written against mathema 0.6** (`>=0.6,<0.7`). Tool names, the verdict and
acceptance vocabularies, the claim grammar and the badge artifacts all move
between minor versions. If `mathema --version` reports a different line,
say so and check the surface rather than trusting this document.

## Read the server first, and fetch reference just in time

The server carries its own reference material and procedures, generated
from what mathema owns, so they cannot drift from the code. Reach for them
rather than memorising, and rather than this skill restating them.

**Resources**, attach once at the start of a session:

- `mathema://reference/grammar`: every spelling the claim language
  accepts, rendered from the lexicon itself, so it never drifts from what
  parses. Fetch it and write against it, not against your memory. Two
  constructs repay knowing. `assuming is_defined(f), <law>` states the
  condition a law holds under, which is what lets a claim about a
  two-sequence function survive inputs the function legitimately refuses.
  `let g = pkg.module.function` binds a named function so a law can relate
  a vectorised routine to the scalar core you extracted from it. And
  dimensions are constrainable as a **premise**: `assuming len(x) ==
  len(y), f(x, y) == f(y, x)` and `assuming len(X) > 6, 0 <= f(X) <= 1`
  both adjudicate, which numeric code needs constantly; a dimension stated
  as a quantifier (`for X in R^(n*m), n in [7, 40] subset Z`) is skipped.
- `mathema://reference/verdicts`: the stance fold and what each verdict
  licenses (~400 tokens). It settles the most confusable thing in the
  system; read it before you read a verdict.
- `mathema://reference/codes`: why a function did not lift and whose move
  it is (~2,500 tokens). Fetch it when triaging, or use the `blocker_hint`
  column and skip it.

**Prompts**, a procedure put in front of you at the moment you choose what
to do: `claim_this_function(target)` (authoring, real signature resolved
in), `triage_repository(targets)` (where to start),
`diagnose_falsification(target, claim)` (a claim came back refuted).

This skill covers what those cannot: the shape of the surface, what things
cost, and the judgement calls.

## The tools, by what you are doing

- **Orienting.** `audit_targets` is the population report you start with;
  `project_index` reads the generated navigable index; `resolve_target`
  turns a path or partial name into the dotted keys everything takes.
- **Understanding one function.** `describe_target` gives the signature,
  identity hashes, inferred domains, declared claims with verdicts, and the
  tier ladder.
- **Proposing.** `suggest_claims` returns the candidates mathema would
  offer; `parse_claim` validates a statement without running anything;
  `claim_grammar` returns the lexicon (same content as the grammar
  resource).
- **Adjudicating.** `adjudicate_target` does one and gates it;
  `adjudicate_targets` batches a whole pass into one call; `verify_project`
  is the sweep (freshness, re-adjudication, record refresh, the gate).
- **Diagnosing.** `reason_code` turns a blocker into its meaning and remedy.
- **Measuring.** `implementation_coverage` gives per-function coverage
  **without running the suite** (a line counts as covered by a test, a
  probe, or a proof, unioned); `badges` rolls the three health numbers up.
- **The human boundary.** `pending_decisions` lists what a person owes;
  `lock_target` pins a form hash so `verify` refuses a changed body
  (locking is the safe direction, so an agent may do it, and there is
  deliberately **no unlock tool**).

## The order that works

1. **`audit_targets` with the columns you need.** A column no analysis
   requires is never computed, so a three-column triage runs far faster
   than the full sweep. Start with `key`, `span`, `claims`, `blocker`; add
   `docsync` before authoring. `derivable` and `unconditional` both ship by
   default and answer different questions (below).
2. **Narrow with `filter` before reading anything.** Semantic terms:
   `actionable` / `limitation` / `N/A`, `claimed` / `unclaimed`,
   `derivable` / `underivable`, `underclaimed`. Columnar: `blocker~loop`
   (one column) or `~mutual` (any). Same-dimension terms OR, dimensions
   AND. `unclaimed,derivable` is the "where do I start" query.
3. **Read the span, not the file.** Every row carries `span`, a sed
   address covering the whole function (below).
4. **Check `docsync` and the intent hierarchy before authoring.** A low
   score means the contract you would claim against is mostly unwritten;
   write the `Intent:` blocks first (below), which is cheaper than the
   claim and makes it obvious.
5. **`suggest_claims`, after annotating the return.** The battery offers a
   shape family (monotonic/affine/convex/concave per parameter)
   unconditionally, a menu rather than a suggestion since it proposes a
   property alongside its negation. The valuable half is **marker-gated**
   and silent until the signature says something:
   - a return marked `Probability` / `UnitInterval` / `InRange(lo, hi)` /
     `Positive` / `Nonnegative` earns `returns_in_range`, the bound written
     out;
   - a square-matrix return earns `is_symmetric(f(A))`;
   - a pure single-delegate wrapper earns `let g = pkg.mod.core, f =:= g`;
   - a structurally bounded but unannotated return earns a hint to
     annotate it;
   - a bare `str` parameter earns `is_arbitrary_input_safe[param]`.

   So: mark the return, then ask. On an unmarked codebase the battery looks
   worthless and stays that way until the signature carries what it reads.
   **A return marker is itself a claim**: marking `max(abs(r), abs(rho))`
   as `UnitInterval` earned a bound that falsified at `(2, 0) -> 2.0`,
   because the function is bounded only where its inputs are. State the
   bound over the domain callers actually pass instead.
6. **`parse_claim(statement, target=...)` for anything you will keep.**
   Always pass the target: without it only grammar is checked; with it the
   parameter names and arity are checked against the real signature, the
   commonest authoring mistake. `adjudicate_target` lints internally too,
   so this is about catching the error before it reaches a file.
7. **Write the claims into a file, then adjudicate.** Declared claims live
   in `claims/*.claims.yaml` keyed by dotted function name; you write the
   file so the claims land in a diff a human reviews, and mathema never
   edits the repository on your behalf. **Both `claims/` and `.mathema/`
   are part of the repository**, not a cache: they are the evidence, and
   each record binds a verdict to a form hash and the commit it was
   established at, so a reviewer sees when a claim started holding and
   against what. Treat a record change as part of your diff. (After a git
   merge or rebase touches `.mathema/`, the integrity check will flag a
   record whose contents no longer match its stamp; that is expected, not
   tampering. Re-run `verify` to re-adjudicate and re-anchor, or a person
   runs `mathema accept KEY --as reconciled` (or `--all` for every
   mismatched record). A function you move to another
   module leaves its record behind under the old key; `verify` names the
   move and the command, `mathema accept NEW --as reconciled --from OLD`,
   which a person runs to carry the record and its history across. See
   <https://mathema.tetrionlabs.com/modes/accept/>.) Every field in a claims file is one mathema reads,
   and an unknown one is refused, so annotate with the fields that exist:
   `note:` on a claim for free text, `meta:` for structured data,
   `references:` on the entry for links, and tags as `meta: {concepts:
   [...]}` on the entry. Prefer `note:` to a YAML comment, which does not
   survive a rewrite of the file.
8. **`adjudicate_targets` for a pass; reach for the batch far more than
   feels natural.** It returns column-oriented rows across every target in
   one round trip with the gate applied once. Fewer, larger calls are
   cheaper and keep a whole module's verdicts in front of you at once,
   which is where the pattern in them becomes visible.
9. **`implementation_coverage` to see what is still unevidenced.** It does
   not run the suite, so call it whenever you want to know where to go
   next; each row's `remedy` names the single most useful action.
10. **`pending_decisions` last**, and hand what it returns to a person.
    A `moved` row is a record whose function moved: its detail carries
    the rename command a person runs.

## What things cost

`include` defaults to `declared`, which is what you want when re-checking
your own work; `include="suggested"` gets the battery and `include="all"`
gets both at roughly four times the cost. Ask for suggestions when you want
them, not by accident. As ratios: a rejected `parse_claim` and a
one-dimension `audit_targets` are tiny; a default `adjudicate_target` is
mid; `include="all"` is the expensive one.

## Navigate by span, never by search

Every `audit_targets` row carries `span`, a **sed address covering the
whole function**:

```
["measures.linfoot", "185:193p", 7, true, "", [1,1], "yes"]
```

So `sed -n '185,193p' src/pkg/measures.py` is the function, exactly.
Ask for `span` and you never grep for a definition or read a module to find
one function; `project_index` gives every span in one call. **Use the key,
not the path**: every tool takes the dotted key
(`pkg.measures.linfoot`), which is also what files, records and
verdicts are keyed on. The saving scales with file size over functions
touched, so it wins on large files you touch lightly and can be a net loss
on a small package you will read most of anyway. The habit does not form on
its own; reach for the index deliberately.

## Intent, and why you read it before you claim

**Intent is why the function exists, not what it does.** The body says what
it does, a claim says what is true of it, intent says what it is for. That
is what makes a claim worth writing rather than merely true, and the one of
the three a checker cannot recover for you.

Intent sits on a ladder mathema records: **none**; **`declared`** (only the
summary line, a bare declaration); **`documented`** (an explicit `Intent:`
block); **accepted** (a human ran `mathema accept --intent`, binding the
text to the signature and raised-exception surface, so a body-only refactor
keeps it and changing any of those re-opens it). The top rung is a human
act, not yours to grant, like a verdict. **Your move is the middle one:
writing an `Intent:` block promotes `declared` to `documented`**, the
cheapest promotion in the system.

`docsync` (0-100) is how much of what the function does is surfaced as
readable context: intent at function, module and project level, declared
domains, raise conditions, types, the call surface. It is **not**
proveability. Context is reported, never inherited downward: a function
with no intent of its own stays a gap whatever its module or README says.
Each level's `evidence` field names the distinction, an `Intent:` block is
`explicit`, a bare summary `implicit`, and only the first is a contract
anyone could sign off.

```python
def linfoot(mi: float) -> float:
    """Intent:
        Put mutual information on the correlation scale so a nonlinear
        dependence can be compared against an ordinary correlation.
    """
```

Do the same at module level and once atop `README.md`. **Keep it under
forty words**: longer usually describes an implementation rather than a
purpose, and a purpose you cannot state briefly is often two. Where intent
is thin, write it first, `mathema docsync <target> --report` names exactly
which symbols each docstring omits, so the writing is mechanical and the
docsync mean moves sharply in one focused pass. It is cheaper than the
claim, makes the claim obvious, and is the part a checker can never supply.

## The three badges, and what each asks

`badges` emits three numbers over a target set, plus `overall`. They are
not three views of one thing:

| badge | the question | how it rolls up |
|---|---|---|
| **implementation** | is this line reached by anything current? | raw line ratio |
| **intent** | is what this code is for written down? | centrality-weighted docsync |
| **clarity** | how much is *known* about the behaviour? | centrality-weighted, from verified claims |

**Implementation** is test coverage generalised: a test, a probe or a
proof all count as reaching a line, unioned. It says nothing about how well
anything is known. **Intent** is the docsync score, the cheapest to move
and usually the first worth moving, because a claim needs a stated contract
to be a claim *about* something.

**Clarity is the one to care about**, and the most misread. It scores how
much is known about what the code does, from verified claims, and is **not
a pass rate**: a witnessed falsification of a **live** claim counts as
knowledge, because learning that a documented bound does not hold is
learning something real. A repository can be green on tests and low here,
the honest reading that nothing has been established about what its
functions do. It is the number that moves when you do the work this method
is for.

Two things to state before anyone chases it. A claim **retired into
`discoveries:` is history and stops counting**, so accepting a
falsification as a discovery can lower clarity; that is the metric as
implemented, not a regression, and it is worth saying out loud when it
happens. And clarity **tops out below 100 by design**: a call into a
library the compendium does not model is unknowable from the caller's
code, so no claim there reduces it. 100 belongs to a pure function whose
entire behaviour is known and claimed, and a repository holding above 60
is doing well. Quote the ceiling beside the score, and read the two halves
separately: the gap up to the ceiling is the repository's work, while the
ceiling itself rises as compendiums are added, which is the mechanism that
lets knowledge about a library transfer to every repository calling it.

Intent and clarity are **centrality-weighted** by PageRank over the call
graph, so a core function counts for more than a leaf; implementation stays
a raw ratio. A `null` clarity on a row means the **source is unavailable**
(a builtin or C extension), so the row drops out of the roll-up; it is not
a zero, and a function with no claims scores a low baseline rather than
zero. `overall` is the **fraction of the frame the triangle shades**:
clarity is the apex height and implementation and intent the base, so it is
zero whenever clarity is zero and rises as you raise all three. Diff it
across commits rather than reading it as a grade.

**Publishing them.** The `badges` tool gives the numbers to reason about;
to ship them, the CLI writes the artifacts to the standard
`.mathema/badges/`: `mathema badges --out .mathema/badges/` emits
`triangle.svg` and `triangle.txt`, the `implementation.json` /
`intent.json` / `clarity.json` shields.io endpoints, `snapshot.json` for a
CI area-delta comment, and `readme-snippet.md`, a paste-ready block with
the three shields, the triangle and one line on what each score means.
Commit them with the store, and **start the README from the snippet**
rather than hand-authoring the block: a hand-written one is how a badge
name that changed upstream goes on silently serving a frozen number.

mathema **owns that directory**. `--out` prunes any badge-shaped file it
did not write this run and returns what it deleted as well as what it
wrote, so a rename upstream surfaces as a visible deletion instead of a
stale file nothing rewrites. Report the deletions: a `git diff` guard
cannot see a file that is never written. Full detail at
<https://mathema.tetrionlabs.com/modes/badges/>.

## Implementation coverage: the other half of the evidence

**Test coverage, generalised.** Same question line coverage always
answered, what share of a function's statements is reached, changing only
what counts: a **test, a probe, or a derive proof**, unioned. It does not
run your suite, mathema supplies the probe and derive evidence itself, so
it is cheap and side-effect-free; only `run_tests=true` invokes pytest, so
opt into that deliberately, typically after a `re-run tests` remedy. Each
row's **`remedy`** is the field to act on: re-run tests to reclaim a stale
report, declare a claim where a derivable body would derive, or cover named
lines, which makes the output a worklist.

It inherits coverage's meaning and nothing more. A line reached by a proof
counts the same as one reached by a test; a function can sit at 100% with
no claims at all, and that is correct rather than a gap. **Do not read it
as how certain anything is**; that is a different measure. `sources` is
diagnostic (which mechanisms reach a line, so you know what would go dark
without the tests); `potential` is what a test re-run would reclaim; and
`test_stale` flags a report predating the source, excluded from the score
rather than silently trusted.

## Locking, and the acceptance PIN

**`lock_target` pins a form hash.** After it, `verify` refuses to
re-adjudicate a changed body until a person runs `mathema unlock` at a
terminal; docstring edits never trip it. Locking is the safe direction, so
an agent may do it, and there is deliberately **no unlock tool**: a lock
you place is one only a human can lift. Lock a settled implementation, not
one you are still working on, and say what you locked and why.

**Acceptance may be PIN-gated.** Where a person has configured a PIN, every
acceptance write requires a human at a terminal and the record names which
credential authorised it, on the JSON and scripted paths too. Where none is
configured the gate does not fire. Either way this is not a surface you
operate: it is the wall, made enforceable rather than merely documented.

**You do not operate it, but you do prepare it.** Deciding whether the code
or the claim is wrong is the human's; gathering the witness, deriving which
verbs are legal, drafting and pre-adjudicating a correction, and printing
the command are yours. When a repository has falsified or unknown claims
waiting on a person, that is the `clear-the-gate` skill.

## `is_defined` reads two ways

Which one you get depends on whether you state a region.

**With a region**, it claims definedness is bounded to exactly that region:

```yaml
- name: is_defined
  statement: "x >= 0"
```

It proves when the stated region matches the one mathema computes from the
body's raise guards, and falsifies when the two differ (naming the region
it computed) or when the function turns out to be total, because then there
is no restriction to state.

**Bare**, it claims the opposite: that there is no restriction at all.

```
is_defined(f)          # or: f is defined
```

It proves when the body has no raise region, and falsifies when it has one,
naming the region the function does return on.

So state a region for a function that refuses some inputs deliberately, and
use the bare form for one you believe accepts everything. mathema suggests
the region form for a partial function, and suggests neither for a total
one.

## String parameters have their own hazard check

`is_arbitrary_input_safe[param]` fuzzes a bare `str` parameter over an
edge-case corpus and **shrinks any unguarded crash to a minimal witness**,
on the `probe:minimal_example` route. A guarded raise or a deliberate
`ValueError` holds; an accidental `IndexError` or `KeyError` from
unvalidated input falsifies with the smallest input that triggers it. It is
auto-suggested for every bare-`str` parameter, and the shrunk witness is
directly usable as a regression test. The derive half declines by
construction: "no accidental crash on any string" is not something a
symbolic route can establish, so the member is empirical and the record
says so.

## Claims compound, so build the base and then spend it

A proven claim becomes a **lemma other claims rest on**: `assuming <name>
is proven` lets a claim about a caller stand on a claim about what it
calls, and a discharged lemma lends its *statement* into the proof, guarded
so it only lends where it was established (a lemma proven on `[0, 10]` says
nothing at `-3`). So the cheap claims are not consolation prizes: a scalar
helper lifts and proves quickly, and every `proven` there is a premise for
everything above it. **Prove the scalar core first**; the effect is
superlinear, because each claim is both evidence and a possible premise.

The failure mode is not starting there, it is **stopping there**, proving
the helpers and never coming back up the call graph to spend the base on
the risky functions above. Three habits keep it working:

- **Come back up the call graph.** Once a helper is proven, the claim you
  could not state about its caller may be reachable with `assuming
  <helper_claim> is proven` in front of it. This is the step most often
  skipped, and where the compounding happens.
- **Get something onto the risky function early**, even a refusal contract
  or a probe verdict. A `holds` is real evidence and tells you what the
  function will not accept, often what the next claim needs.
- **Watch `claims_vs_floor` and the `underclaimed` filter.** They pair what
  a function has against the structural floor it admits, per function, so a
  surface still at zero is visible without a client-side join.

**A function you cannot write a claim about is telling you something**:
usually that it does several things at once, or takes arguments whose shape
nothing constrains. The decomposition that makes it claimable makes it
testable.

### Extract the decidable core, and claim that

Split the *decision* out of the *estimation*, so the part carrying the
logic takes numbers rather than data:

```python
def cointegration_score(memory_x: float, memory_y: float,
                        memory_residual: float, max_lag: int) -> float:
```

Three floats and an integer, no series. The estimation happens elsewhere;
what is left is the reasoning, and it carried six adjudicated claims where
the same feature written as one measure-and-decide function carried none.
Look for this whenever a function both computes a quantity and draws a
conclusion from it; the conclusion is almost always a small scalar function
of a few numbers.

### Let a refusal contract tell you to add a guard

Claim what a function refuses, not only what it returns:

```
raises(f(series, 0), ValueError)
```

A witness like *"the empty boundary is stumbled into, not handled"* means
the exception happens by accident downstream. Adding the guard turns the
same claim into a proof by construction, and the function is better for it.
The related blocker *"no explicit raise statement... an exception implicit
in an arithmetic operation"* means the function relies on NumPy or the
interpreter to raise; worth fixing on its own terms, and it converts the
claim from a probe to a proof.

## Claim what you depend on, not only what you wrote

The highest-yield claim is often not about new code. State the contract you
rely on from an existing function, over the full domain its docstring
asserts:

```
for mi in [0, 50], 0 <= f(mi) < 1
```

Documented as returning below one, property-tested, released, this
falsified at `mi = 37.31`, where the expression saturates to exactly `1.0`
in float64; the existing test checked only up to `6`. A test checks the
values its author chose; a claim hands the search to the checker, and the
interesting failures live at the far end of a domain nobody thought to
visit. It also feeds the compounding above: a contract proved about a
dependency is exactly the lemma a claim about your own function will want.

## `derivable` and `unconditional` are two different questions

They sit side by side in the default columns and mean different things.

- **`unconditional`** is a property of the body alone: does it lift
  symbolically with no help, no declared domain, no conditioning.
- **`derivable`** is what the derive route can do here **given the declared
  context**, so a domain you declare can move it.

The gap between them is where your claims do work: a branch that cannot be
settled in the abstract is often settled the moment a claim says `for scale
in {"info"}`, and the pruned branch then lifts. So `unconditional: false`
is a fact about the code; `derivable: false` is about the code *plus what
has been declared so far*, which you can change without touching the body.
**Read the routes, not only the columns**: the ground truth for "did this
prove" is the `route` on the claim row, and a function can carry several
`derive` proofs while both columns read false, because branch pruning
happens per claim. Count routes on the rows if you want to know what proved.

## Underivable does not mean unclaimable

The `blocker` gates **proof-strength evidence only**, the derive route's
symbolic lift. A probe claim can still be written and adjudicated for every
function, and for loop-heavy or array-shaped code a seeded `holds (n=...)`
is frequently the only evidence obtainable, which makes it valuable rather
than second best. This matters for `filter`: `actionable` answers "which
functions could I make provable by editing this repo", right for a
refactoring pass and wrong for a claims pass. Filter by it when you intend
to change code, or you will silently discard most of the claimable surface.

## Diagnosing a falsification

Use the `diagnose_falsification` prompt. The judgement it cannot make is
which cause to suspect first, and that depends on the code. Fresh,
generated, or thinly tested code: your claim is doing a specification's
job, so a disagreement is a defect until shown otherwise. Mature, released,
well-covered code: the implementation carries years of evidence and your
claim is minutes old, so a novel falsification is more likely a misreading
than a bug nobody has hit. The level that matters is the function's own,
not the repository's.

Before reporting any falsification as a defect, **write the claim that
would hold if the code were right and check it**; a held claim that cleanly
explains the falsification is strong evidence the claim, not the code, was
wrong. Report "claim X and the implementation disagree, here is the
witness", never "the code is wrong", and route anything whose diagnosis
depends on intent not in the source to a human. See the `design-claims`
skill, Stage 4, for the longer form.

## Traps worth knowing before you hit them

- **Omit `route:` in a claims file unless you mean to constrain it.** A
  checker with more than one route picks the strongest it can serve;
  pinning one can only take evidence away. A file pinned to `route: probe`
  gave 0 proven where the same file without the line gave dozens.
- **Explore ad-hoc claims against a scratch root, never your project
  root.** `adjudicate_target(claims=[...])` writes nothing, but the tool
  `verify_project` and the Python API's `mathema.write_spec` persist, and ad-hoc claims have
  turned up in `.mathema/verified/` with supersession markers against
  declared claims. Keep exploration in a throwaway directory.
- **Ad-hoc claims that canonicalise alike collapse into one row.** Names
  derive from the canonical statement, which drops the `for ...` prefix, so
  domain-variants of one law come back as a single row and read as
  rejections. Vary one thing at a time, or name them in a file.
- **`claims=[...]` takes strings**, not the `{"name", "statement",
  "route"}` dicts a file uses; passing dicts crashes inside the declaration
  machinery.
- **Do not trust a `raises(...)` claim with literal arguments when the
  signature also has a non-scalar parameter.** The literals are replaced by
  synthesised scalars, so `raises(f(values, "nope", 0.35), ValueError)` can
  falsify with `(2, 0, 0.35)`, a call your claim never made, gating on it.
  On an all-scalar signature the shape is reliable; elsewhere keep the unit
  test and say why the contract is absent.
- **A pinned argument does not always reach the function.** If the default
  call raises for every synthesised input, a claim can come back `unknown`
  with `n=0` even when its own arguments take a non-raising branch, and
  `assuming is_defined(f)` does not rescue it. If a cheap claim returns
  `unknown` with no trials, check whether the function refuses its defaults.
- **A `skipped` row tells you nothing about why.** There is no reason code
  on skips the way there is on derive blockers, so you cannot tell a
  mis-stated claim from one the checker could not reach. Bisect against a
  scratch root.
- **Some code is simply unclaimable.** Two-dimensional arrays and dicts
  cannot be synthesised, so every claim comes back `skipped` on probe and
  `unknown` on derive, often most of an orchestration layer. Say so in your
  report, name the functions, and let the tests carry that half; padding
  the file to hide it is worse than the gap.

## When the checker itself looks wrong, say so

Sometimes the tool is what is wrong. Report rather than route around in
silence: **two surfaces disagreeing about one claim** (`adjudicate_target`
and `verify_project` returning different verdicts, the record is at risk,
report both with the claim text), and **a witness that does not support its
verdict** (a counterexample whose before and after are identical, or naming
something the claim never mentioned, is a defect in the check). Work around
it if you must, and **say which claims carry a workaround and why**, because
a claim split in two or restated without a bound is weaker than the one you
meant, and the next reader cannot tell.
