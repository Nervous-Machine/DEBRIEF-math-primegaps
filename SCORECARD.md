# DEBRIEF: the claim that primes come within 186 of each other infinitely often (sample, 2026-11-07)

Ledger: `ledger/missions/primegaps.json` (built by `ledger/build_ledger.py`). Pre-registration: `primegaps/prereg.yaml`,
written before any check ran; amendment A1 added after the checks (Axiom wording, provenance, C3 note; verdicts unchanged).
Lean source pinned: openai/PrimeGaps186 commit 61340d0 (2 Sep 2026), `Challenge.lean` sha256 b99a403b…, verbatim copy in
`primegaps/source/`. Cycle 6 (independent rerun, same day): `primegaps/prereg_cycle6.yaml` written first, results in
`primegaps/cycle6/results_cycle6.json`, logs alongside. Checks: `primegaps/checks.py` → `primegaps/results.json`. The agent's knowledge base:
`elevenlabs/knowledge_base_primegaps.generated.md`. Nervous Machine keeps score of the checks; it does not check the
mathematics line by line.

## 1. In one minute

- **The claim.** OpenAI (credited to GPT‑6 Astra; paper dated 30 Aug 2026, public 3 Sep) says infinitely many prime
  pairs are at most **186** apart, beating Polymath 8b's **246** (2014).
- **The same week**, Hanxin Zhang (28 Aug, discovery credited to GPT 5.6 Sol) and Julia Stadlmann (31 Aug, no AI) each
  reached **240**, and Axiom Math announced **212** (3 Sep, nine authors). The approach is credible.
- **The logic is machine-checked in Lean,** but it rests on **three inputs taken on trust**: two classical exponential‑sum
  bounds, and 152 numerical bounds computed by a separate program.
- **What we checked directly holds up.** The 40-number list is correct, and the two classical bounds hold with room to
  spare on small primes.
- **Then we reran OpenAI's own checks.** The Lean build passed with no warnings (9.5 min, 28 GB). Comparator matched
  the three statements; Nanoda and Lean's kernel accepted them, on exactly the six permitted axioms. The numerical
  certificate ran to completion and passed (1 h 04 min, 4 workers) once FLINT had the one public, unreleased fix it needs.
  Per Tao's page and MathWorld, no one had reported a rerun before.
- **Open:** a number theorist has not publicly confirmed the formal goal statements say what the paper claims, and
  the paper hasn't been refereed.
- **Read: conditionally supported, with the computation independently reproduced. Not yet settled; what remains is human.**

## 2. How it was solved, in plain terms

The method gives each shifted copy of a list of numbers a weight, so copies likely to hold two primes count more (the
multidimensional Selberg sieve of Maynard and Tao). The new step is a set of conditions on how the weights' divisors
factor ("triply densely divisible"). These conditions let the weights reach further than the 2014 method allowed, using
Polymath 8a's and Stadlmann's estimates of how primes spread across remainders. A large numerical optimization then shows
forty numbers are enough (DHL[40,2]), and a 40-number list spanning 186 finishes the proof.

## 3. Standing, step by step

| step | standing | basis |
|---|---|---|
| The 40-number list spans 186 and is admissible | **certified** | direct computation on the tuple read from the pinned Lean source, rule written first (C1) |
| Logic from the three inputs to DHL[40,2] and the 186 bound | **certified** | Lean kernel + Nanoda + Comparator, run by the authors and rerun by Nervous Machine (C4, C5); exactly six axioms |
| Polymath 8a estimates, Maynard sieve | **accepted** | published, refereed |
| Hyper-Kloosterman bound (input 1, Deligne) | **accepted** | literature; max seen 2.35 vs limit 3 for all primes ≤ 97 (C2) |
| Kloosterman correlation bound (input 2, Fouvry–Kowalski–Michel) | **accepted** | literature; never above 46% of the limit for primes ≤ 61 (C3) |
| 152 numerical integral and cap bounds (input 3) | **certified** | certificate rerun by Nervous Machine on FLINT 3.6.0 + fix 7ad753d: passed, margin 2.3e-5 > required (C9) |
| The formal goals say what the paper claims | **open** | Comparator matches the proof to the goals, not the goals to the mathematics; the repo's own formalization.yaml says "self-assessed, no independent human semantic review" |
| Independent review of the written proof | **open** | none reported through 2026-11-07 |
| Route plausibility (Zhang 240, Stadlmann 240, Axiom 212) | **accepted** | three independent groups, none refereed; Axiom's Lean certificate described in its draft, not public |

**Refuted: nothing.** Three corrections: some descriptions count six assumptions, but three are Lean's standard logic
rules, so the claim rests on three; an earlier draft of this briefing called Stadlmann's 240 the first improvement in a
decade, when Zhang's 240 was deposited three days earlier; and this briefing said the certificate needed a library build
OpenAI had not published, when the missing piece is a public upstream FLINT fix (PR 2790) that is in no release.

## 4. Replay, no look-ahead

| cycle | date | what was public | verdict |
|---|---|---|---|
| 0 | 2014–15 | Polymath 8a/8b (246), Maynard sieve; 8b names the dense-divisibility route as hard at k ≈ 50 | baseline |
| 1 | 2026-08-28 → 08-31 | Zhang 240 (Zenodo, AI-discovered, exact certificate); Stadlmann 240 (arXiv, no AI); independent | route credible |
| 2 | 2026-09-03 | Axiom Math 212, 45-tuple: draft says its prover produced a Lean certificate conditional on five analytic estimates and a variational certificate; not published | route credible |
| 3 | 2026-09-03 | OpenAI 186: paper, conditional Lean development, certificate program | admitted, conditional; four gaps opened |
| 4 | 2026-09-07 → 11-05 | Tao's optimization-problems page ("no bound was independently verified"), MathWorld, Science News, repo activity | no independent verification reported |
| 5 | 2026-11-07 | Nervous Machine checks C1–C3 (registered first) | all three pass |
| 6 | 2026-11-07 | Independent rerun, registered first (C4–C9): Lean build, Comparator + Nanoda + kernel, axiom print, stock FLINT fails regression (predicted), FLINT + fix passes, certificate passes | all predictions held |

## 5. What would settle it, in order

1. A number theorist reads the three goal statements in `Challenge.lean` (OpenAI's own metadata: "self-assessed, no
   independent human semantic review").
2. A referee report or an independent expert read of the paper.
3. Formalize the two classical bounds in Lean, or record that the field accepts them as standard.
4. Done 2026-11-07: independent rerun of the Lean build, Comparator and `prime_gap_186_certificate.py`. A second party
   repeating it would strengthen the record; the recipe is FLINT 3.6.0 + commit 7ad753d, python-flint 0.9.0 from source.

"If you think of any other questions, I'm just a call or text away."
