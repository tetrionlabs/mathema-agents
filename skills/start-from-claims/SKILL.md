---
name: start-from-claims
license: Apache-2.0
description: >-
  Begin a brand-new project or module the claim-driven-development way:
  intent and claims are authored first, as the specification, and the
  implementation is written to satisfy them, the way tests lead in TDD and
  specs lead in spec-driven development. Covers scaffolding, writing intent
  before code, stating claims against signatures before bodies exist, and
  designing the code so its claims can be proved rather than only sampled.
  Use when the user is starting a new repository or module and asks to "do
  this claims-first", "spec it with claims", "set up CDD from scratch", or
  "design the claims before the code".
---

# Start from claims

On a green field the claims are the specification. Nothing exists yet to
audit, so the order of an adoption inverts: you write down what the code
is for, state the laws it must satisfy, and only then write code, which is
finished when the checker says the laws hold, not when it looks right.

This is TDD's shape with a stronger unit. A test pins one example; a claim
pins a law over a domain, and the checker samples or proves it. The
red-green rhythm survives intact: a claim stated before its implementation
falsifies, and the recorded counterexample replays on every verify until
the body satisfies it. The prior is also the comfortable one, as the
`design-claims` skill puts it: on fresh code a disagreement is a defect
until shown otherwise, so a falsification means "not implemented yet" or
"implemented wrong", never a mystery.

**Written against mathema 0.6** (`>=0.6,<0.7`). Tool names, the verdict and
acceptance vocabularies, the claim grammar and the badge artifacts all move
between minor versions. If `mathema --version` reports a different line,
say so and check the surface rather than trusting this document.

The other skills carry the depth this one sequences: `design-claims` for
authoring any one claim set, `use-mathema-mcp` for the tool surface, and
`clear-the-gate` once verdicts leave decisions owed to a person.

## Scaffold before any code

```
mathema init --ci
```

Bare `init` writes the git files: a `.gitattributes` marking verified
records as generated (collapsed in diffs, out of language stats, still
reviewable) and a `.mathema/.gitignore` that keeps regenerable layers out
while the evidence layers stay in. `--ci` adds the verify-gate workflow.
`--agents` vendors these skills for your tool.

Two placement decisions to make now, not later:

- **The store is committed.** `.mathema/verified/` ships with the code,
  like a test suite with lineage: verdicts, acceptance history, integrity
  stamps. It is the project's memory of what has been established, and CI
  re-adjudicates against it.
- **Claims live in `claims/*.claims.yaml`**, keyed by dotted function
  name, one file per module is the shape that stays navigable. These files
  are the authored specification; the store is the evidence it earned.

## Intent is the first artifact

Before any signature, write what the project is for at the top of
`README.md`, then a module docstring per planned module, then an `Intent:`
block per planned function. Keep each under forty words: longer usually
describes an implementation you have not written yet, and a purpose you
cannot state briefly is often two functions.

This is the specification's prose half, and it is load-bearing three
times over: it is what the claims are *about*, it is what a human accepts
when they sign intent later, and it is the intent badge. `mathema docsync
<target> --report` names what each docstring still omits, so keeping it
current is mechanical.

## State claims against signatures, not bodies

Write the signatures next, bodies as bare `raise NotImplementedError`
stubs, and author the claim set for each function as if the function
worked. This is the specification's formal half. Walk the concept
families as a checklist (`design-claims`, Stage 1) and write each law in
the authoring YAML.

Everything about a claim except its verdict can be settled with no body:

```
parse_claim(statement, target="pkg.measures.ema")
```

validates grammar, parameter names and arity against the real signature,
and a stub has a real signature. Run every claim through it as you write.
What you cannot have yet is evidence, and you do not pretend to: the
deliverable of this stage is a parsed claim set and stubs, with no
verdicts claimed.

Adjudicating the stubs is optional but honest, and it is the red run: every
value claim falsifies with the unimplemented raise as its witness, which
then replays until the body satisfies the law. That is the counterexample
mechanic doing exactly what it is for. Skip it if you prefer the first
verify to come after the first body; do not skip `parse_claim`.

## Signatures are design surface

A green field means the signatures can carry meaning from the start
instead of having it retrofitted:

- **Mark returns.** `UnitInterval`, `Probability`, `InRange(lo, hi)`,
  `Positive`, `Nonnegative` on returns; `Mat("n", "m")` / `Vec("n")` on
  array shapes. A marker is itself a claim, stated where every reader
  looks, and the suggestion battery is gated on them: an unmarked
  signature earns almost no suggestions, a marked one earns the bound
  written out.
- **`Literal[...]` on every string mode parameter**, so the domain is
  declared rather than discovered, and a bare `str` parameter only where
  input is genuinely open, where it earns the arbitrary-input fuzz check.
- **Refusals are part of the spec.** A function that rejects some inputs
  does so with an explicit guard and a claim that says so
  (`raises(f(...), ValueError)`, or a stated `is_defined` region). The
  domain a function accepts is a designed thing here, not an accident to
  document later.
- **Dimensions are premises**: `assuming len(x) == len(y), <law>` is the
  spelling that adjudicates; a dimension stated as a quantifier is
  skipped.

## Implement until the record says done

Now write bodies, and let the loop be the loop: implement, adjudicate
that function, read the verdict. A falsification's witness is the next
input to handle; `holds` means the law survived real sampling; done is
when the claim set you authored as the spec adjudicates clean. Nothing
about the code's completeness is asserted by you: the record says it.

Two rules from the wider method apply with full force even though all the
code is yours:

- **You never adjudicate your own claims.** Every verdict comes from the
  checker. This is what makes the claim set a spec rather than a hope.
- **Author deliberately.** An adjudicated claim joins the store's
  append-only membership, and the exits are supersession and human
  acceptance, not deletion. Explore candidate spellings with in-process
  `check()`, which writes nothing, and put into the claims file only what
  you mean the code to satisfy.

## Design for the derive route

The largest thing a green field buys: code can be shaped so its claims
are *proved* rather than sampled, which no adoption can retrofit cheaply.

- **Pure scalar cores, effects at the edges.** The mathematical heart of
  each computation is its own small pure function of scalars; I/O,
  plotting, batching and state live in wrappers. The core lifts and its
  claims can come back `proven`; the wrapper's claims are relational.
- **No defensive coercion inside a core.** A `clip`/`asarray` at the top
  of a numeric function is what turns a provable identity into a sampled
  one. Coerce in the wrapper, keep the core exact.
- **Relate wrapper to core explicitly**: `let g = pkg.mod._core,
  f(x) == g(x)` over the scalar domain. Claims compound: a proven core is
  a lemma, and `assuming <claim> is proven` lets the next claim rest on
  it, so prove the base of the pyramid first and spend it upward.
- **One branch per declared domain.** Branches that switch on a declared
  `Literal` or a stated premise stay derivable; branches on computed
  conditions push claims to the probe route. Probe evidence is real
  evidence, so this is a preference, not a rule.

## Clarity tops out where knowledge does

Clarity, the badge that scores how much of the knowable behaviour is
pinned down, has a ceiling: a call into a library the compendium does not
model is unknowable from your code, and no claim you write reduces it. So
clarity is not expected to reach 100, and does not on anything real. 100
belongs to a pure function whose entire behaviour is known and claimed;
a repository holding above 60 is doing well. Report the score with its
ceiling so both halves are read as what they are.

Raising the ceiling is the compendium's job, not your code's. A
compendium entry models where a library's functions are defined and how
they fail, which is what lets `is_compendium_safe(<library>)` adjudicate
that an unguarded nan or inf cannot arrive silently through it; claim it
wherever the library is covered. More compendiums are planned, and that
is the design: knowledge established about a library once transfers to
every repository that calls it, instead of being rebuilt in each. The gap
between your score and the ceiling is your work; the ceiling itself moves
as the compendiums grow.

## Lock what settles, gate from the first push

When a function's claim set adjudicates clean and its design has stopped
moving, `lock_target` pins its form hash: `verify` then refuses a changed
body until a person unlocks at a terminal. Locking is the safe direction,
so an agent may lock and say so; there is deliberately no unlock tool.

The CI gate from `init --ci` runs `verify` on every push. Decide its mode
consciously: strict fails structurally-skipped claims too, `--lenient`
tolerates them, and a young project usually wants lenient with strict as
a stated goal. From the very first push, the gate is only ever green or
red for a reason someone can read in the record.

## What "done" looks like

Every public function has stated intent, a claim set authored before its
body, and a verdict for every claim from the real checker. The store and
claims files are committed together, the gate is green in a mode you
chose on purpose, and the badges report numbers a green field earned by
design: implementation from tests, probes and proofs unioned, intent from
docsync, clarity from what the claims pinned down.

What you never have is the adoption backlog this method otherwise meets:
undocumented contracts, unliftable cores, a store bolted on after the
fact. The point of starting from claims is that the specification, the
evidence and the code grow up together, and the record can say at every
commit exactly how much of the spec is now true.
