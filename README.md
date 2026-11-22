# DEBRIEF-math-primegaps

A DEBRIEF mission record (protocol https://github.com/Nervous-Machine/DEBRIEF) for **the claim that primes come within 186 of each other infinitely often**, posted by OpenAI in September 2026 as a conditional Lean development, a numerical certificate and a paper.

<!-- standing:begin -->
**Standing, 17 Nov 2026.** Stage: Reading guide written. Needs next: Do the formal statements say what a mathematician means? ([what would close it](ASKS.md)).

| certified | accepted | refuted | open gaps | cycles filed | last cycle |
|---|---|---|---|---|---|
| 5 | 5 | 0 | 3 | 4 | 17 Nov 2026 |

| | |
|---|---|
| checked by machine | Nervous Machine, Fredrik Prüzelius |
| read by a person | nobody yet; [reading guide](trace/DEFINITIONAL-TRACE.md) |
| elsewhere | — |
| related | [Prime gaps ≤ 240 (Zhang)](https://github.com/Nervous-Machine/DEBRIEF-math-zhang240): the same problem, sharper bound (186 against 240) |

Rendered from `ledger/` at regeneration; the full record is `SCORECARD.md`, what is owed is `ASKS.md`. Standing words: 5 certified · 5 accepted.
<!-- standing:end -->

This claim is on the public claims board, https://math-board.nervousmachine.com, which shows its stage, who has contributed, and what it needs next.

## Who did the work

Nervous Machine, with Claude Code as the operating agent that wrote the checks, ran them and kept the ledger. Heidi Bennett, who keeps this record, is independent of the claimant. The agent did not read the proof and makes no claim about the mathematics beyond what the checks establish; everything it did is in the logs. A second rerun was contributed by Fredrik Prüzelius on 14 November 2026.

## The problem

How close together do primes come, infinitely often? Zhang showed in 2013 that some fixed gap occurs infinitely often; Maynard and the Polymath 8 project brought the gap down to 246 in 2014, where it stood for over a decade. In late August and early September 2026 four groups announced smaller bounds by related routes: Hanxin Zhang and Julia Stadlmann each reached 240, Axiom Math announced 212, and OpenAI posted 186. Zhang's 240 has its own record, `DEBRIEF-math-zhang240`.

There is no third-party formal statement of the problem to compare against. The three goal statements in the claimant's `Challenge.lean` are the claimant's own, which is why reading them is the first thing owed.

## The claim

**OpenAI**, credited to its model GPT 6 Astra, in the paper *Improved short gaps between primes* (2026) and the repository `github.com/openai/PrimeGaps186`, pinned at commit `61340d0b74163003b32756bb16e91d9209a5e330` (2 September 2026, the repository's only commit). `Challenge.lean` at that commit has sha256 `b99a403b1946547ef1926cd43ebce717640f7f76fa7e1f8f5a4b19ac2e53e1f0`; a verbatim copy is in `source/`.

The Lean development proves that a fixed list of forty numbers has infinitely many shifts that contain at least two primes, which gives the bound 186, from three inputs taken as axioms: two classical exponential-sum bounds (Deligne's hyper-Kloosterman bound; Fouvry, Kowalski and Michel's correlation bound) and 152 numerical bounds computed by a separate certificate program. The repository's own metadata records its review status as self-assessed, with no independent human semantic review.

What has been reproduced: the forty-number list and its admissibility; the Lean build, the Comparator statement match and both kernel replays on exactly the three stated inputs plus Lean's three standard axioms; the certificate program to completion, on a public FLINT build; and every number in `Challenge.lean` against the numerics paper. What has not: whether the three goal statements say what the paper claims, and the paper itself, which has not been refereed. The record's own words for this: conditionally supported, with the computation independently reproduced; not settled.

## What is owed

Each open gap is in `ASKS.md` with what closes it and who could act. In order:

1. **Do the formal statements say what a mathematician means?** (G2): A number theorist reads the three goal statements against the paper, with the reading guide, and signs or refuses its checklist. This is the step that decides whether "conditionally supported" becomes something stronger.
2. **The two classical exponential-sum bounds are assumed in Lean** (G3): Formalize them, or record that the field accepts them as standard.
3. **No independent review of the written proof** (G4): A referee report, or an independent expert's account of having read it through.

Closed: **G1**, the 152 numerical bounds, reproduced by Nervous Machine on 7 November 2026 and by a second party on 14 November.

## Contributing

- **Rerun**: `REPRODUCE.md` is the recipe from a fresh Ubuntu machine, about two hours of machine time on 20 cores. Ours ran on aarch64; the FLINT bug the certificate guards against is in the FFT multiplication path, so x86 is a real variable. Report with the **Rerun report** issue form; it becomes a `rerun` cycle under your name and a row in `RESULTS.md`. A failed check is as welcome as a pass.
- **Read**: the reading guide is `trace/DEFINITIONAL-TRACE.md`. It quotes each of the three goals and three axioms verbatim, traces every definition to Mathlib with file and line, gives a plain-language rendering that carries no standing, and names the paper location to compare against. Parts A and B take under an hour. Sign or refuse its checklist with the **Semantic read** issue form; either becomes a `read` cycle under your name. Two independent signatures close the semantic gap; one refusal reopens it.
- **Anything else**: open a plain issue.

Rules and templates: https://github.com/Nervous-Machine/DEBRIEF/blob/main/CONTRIBUTING.md. Every contribution is one dated cycle under your own name and goes into `CITATION.cff` and the next release.

One note on the record itself: Nervous Machine's own pre-registrations were written before their checks ran, but each entered git in the same commit as its results, so git history cannot confirm the order; it rests on our word. A contributed rerun whose pre-registration is committed before it runs does not have this weakness.

## Layout

```
ledger/primegaps.json   the ledger (protocol 0.1.0)
SCORECARD.md / ASKS.md  generated from the ledger
RESULTS.md              one row per independent rerun; how to add yours
REPRODUCE.md            the recipe, step by step, from a fresh Ubuntu machine
trace/                  the reading guide for the three goal statements (a `trace` cycle)
prereg*.yaml            Nervous Machine's pre-registrations, hashed before their checks ran (.sha256 sidecars)
checks.py, results.json the tuple and small-prime checks, rerunnable in seconds (python3 -I checks.py)
cycle6/, cycle7/        logs, receipts, environment and scripts of the rerun and the trace
source/                 Challenge.lean at the pinned commit, verbatim, with its Apache-2.0 licence
cycles/                 contributed cycles, one file each
```

## Words

This record never calls the claim proved, verified or a theorem. It records what was claimed, what was checked by whom under what rule, and what is still open. Nothing here has standing until a cycle gives it one.

## Provenance and licences

`source/Challenge.lean` is OpenAI's, unmodified, under Apache-2.0 (`source/LICENSE-openai-PrimeGaps186`). The certificate program is not vendored; the recipe fetches it at the pinned commit and records its hash. Everything else here is by Nervous Machine under Apache-2.0 (`LICENSE`). This repository was `primegaps-186-rerun` until 8 November 2026; the old URL redirects.
