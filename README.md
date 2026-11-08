# An independent rerun of openai/PrimeGaps186

**Status, 7 November 2026.** OpenAI's conditional Lean development for the bound "infinitely many pairs of primes are at
most 186 apart" rebuilds from the pinned sources, passes its own checkers (Comparator, the Nanoda kernel and Lean's
kernel) on exactly the six permitted axioms, and its numerical certificate runs to completion and passes, on one
machine, run by one party independent of the authors. Every check was written down with a prediction before it ran,
and every prediction held. The logs are in this repository.

**What this does not say.** It does not say 186 is a theorem. The Lean development takes three inputs as axioms: two
classical exponential-sum bounds and 152 numerical bounds. The rerun reproduces the computation behind the third and
the deduction from all three. Whether the three formal goal statements in `Challenge.lean` say what the paper claims is
a human judgment that, by the repository's own metadata, nobody independent has made ("self-assessed", "No independent
human semantic review"). The paper has not been refereed. Our read: **conditionally supported, with the computation
independently reproduced; not yet settled.**

**What we are asking for** is at the end: a second rerun on different hardware, and a number theorist's reading of
three Lean statements. The second is worth more than the first.

## Results at a glance

| check | what | result | wall | peak memory |
|---|---|---|---|---|
| C1 | the 40-number list spans 186 and is admissible | pass | seconds | |
| C2 | normalized hyper-Kloosterman bound, all nonzero c, primes ≤ 97 | pass, max 2.351 against 3 | seconds | |
| C3 | Kloosterman correlation bound, all nonzero A, B, primes ≤ 61 | pass, never above 0.458 of the limit | seconds | |
| C4 | `lake exe cache get && lake build PrimeGaps186`, pinned toolchain | exit 0, 0 error lines, 0 warning lines | 9:32.68 | 28.5 GB |
| C5 | `lake exe comparator comparator/main.json` in the README's systemd sandbox | 3 of 3 statements matched; Nanoda accepts; Lean kernel accepts | 6:38 | 8 GB |
| C5 | `#print axioms` on the three theorems | exactly `kloosterman3_bound`, `kloosterman2_correlation_bound`, `physical_integral_bounds`, `propext`, `Quot.sound`, `Classical.choice` | | |
| C6 | certificate's startup regression on the stock python-flint 0.9.0 wheel | fails at coefficient 15, as predicted | seconds | |
| C8 | same regression on FLINT 3.6.0 + upstream commit 7ad753d, python-flint built from source | pass | | |
| C9 | `prime_gap_186_certificate.py --workers 4` on that build | receipt `passed: true`, 97 components; lower margin 2.336e-5 against required 2e-5 | 1:03:48 | 9.7 GB |

Machine: a Linux virtual machine (Ubuntu, kernel 7.0, aarch64, 20 cores, 98 GB) on an Apple-silicon host. Nothing
from the repository ran on the host. Full numbers: `cycle6/results_cycle6.json`.

## What was run, in order

**The source.** `github.com/openai/PrimeGaps186` at commit `61340d0b74163003b32756bb16e91d9209a5e330` (2 September
2026, the repository's only commit). `Challenge.lean` at that commit has sha256
`b99a403b1946547ef1926cd43ebce717640f7f76fa7e1f8f5a4b19ac2e53e1f0`; a verbatim copy is in `source/` and every script
that reads the tuple or the axiom statements checks that hash first.

**Checks we wrote ourselves (C1–C3, `prereg.yaml`, `checks.py`).** The 40-element tuple is read from the pinned
`Challenge.lean`. C1 confirms 40 distinct entries, diameter 186, and that for every prime p ≤ 40 the residues mod p
miss at least one class. C2 computes the normalized rank-3 hyper-Kloosterman sum exactly as the Lean file defines it
and confirms the norm is at most 3 for every nonzero c and every prime up to 97. C3 computes the shifted rank-2
correlation exactly as the Lean file defines it and confirms it is at most 8·p·√p for every nonzero A, B and every
prime up to 61. C2 and C3 are corroboration on small primes. They support the two literature inputs; they do not prove
them, and under our rules they never raise an input's standing.

**The authors' own checks, rerun (C4–C9, `prereg_cycle6.yaml`, `cycle6/`).**

- C4: install the pinned toolchain through elan (`leanprover/lean4:v4.34.0-rc2`), fetch the Mathlib cache, build.
  The README claims a warning-free build; it was.
- C5: build `lean4export` and `comparator` from the repository's own lake dependencies, build `landrun` and
  `nanoda_bin` from their upstream sources (commits recorded), and run Comparator inside the systemd wrapper the
  README recommends, with `--pipe --wait` in place of `--pty` because there is no terminal. Comparator exports the
  three theorems, replays them through Nanoda and through Lean's kernel, and matches each statement to
  `Challenge.lean`. Then `#print axioms` on each theorem.
- C6: install `python-flint==0.9.0` from PyPI and run the certificate's own startup regression,
  `check_flint_signed_fft`, reproduced verbatim. OpenAI's README says the certificate needs a "custom FLINT 3.6.0
  build" with corrected signed convolution that is not bundled. We predicted the stock wheel would fail. It did.
- Amendment A1, written after C6 and before anything else ran: OpenAI's numerics paper identifies the custom build.
  It is FLINT 3.6.0 plus upstream commit `7ad753d51c82fdec115cb179b41d0e581f1cb0ec`, pull request 2790, "Fix fft
  conversion bug causing rare incorrect results in fmpz_poly_mul_SS", merged to FLINT main on 11 August 2026 and in
  no FLINT release (latest release v3.6.0, 29 June 2026). So the certificate is reproducible from public sources.
  A1 added C8 and C9 with predictions.
- C8: clone FLINT, check out v3.6.0, cherry-pick 7ad753d (applies cleanly), build, build python-flint 0.9.0 from
  source against it, run the same regression. Pass.
- C9: run `prime_gap_186_certificate.py` (sha256 `7f71bdef…`) on that build. The receipt is
  `cycle6/prime_gap_186_fresh.json`.

## Deviations, recorded against ourselves

- The pre-registration said `--workers 20`. The script accepts only 1 or 4. We reran with 4. The failed launch is
  `cycle6/C9.attempt1.*`.
- The first FLINT build fell back to FLINT main (3.7.0-dev) because git had no committer identity for the
  cherry-pick, and python-flint's build gate rejects anything at or above 3.7. That attempt is `cycle6/C8.log`; the
  one that counts is `cycle6/C8b.log`.
- C3 as run skips p = 2, where the sum is empty and the bound holds trivially. The rule said primes ≤ 61.
- The VM user's home path in the logs was replaced with `/home/runner` before publication, by string substitution.
  Nothing else in the logs was edited (`cycle6/NOTE-paths.md`).

## How the ledger was built

This rerun is the sixth cycle of a scorecard that Nervous Machine keeps with a tool called DEBRIEF. The scorecard
itself is `ledger/primegaps.json`, its schema is `ledger/SCHEMA.md`, and a readable rendering is `SCORECARD.md`.
The rules that produced it:

**Replay with no look-ahead.** The public record is replayed as dated cycles. Each cycle sees only what was public
by its date, dated by first public posting. Cycle 0 is Polymath 8 (246, 2014). Cycle 1 is the two independent 240s:
Hanxin Zhang's (Zenodo, 28 August, discovery credited to an AI model, with an exact-arithmetic certificate) and
Julia Stadlmann's (arXiv, 31 August, no AI). Cycle 2 is Axiom Math's 212 (3 September; its draft describes a Lean
certificate that has not been published). Cycle 3 is OpenAI's 186. Cycle 4 is the public record of review through
5 November: Terence Tao's optimization-problems page ("no bound was independently verified"), MathWorld's table
("conditional Lean proof, no independent verification reported"), Science News, and the repository's activity (one
commit, no issues, no pull requests). Cycles 5 and 6 are ours.

**The proof as a graph of steps.** Before any check ran, the argument was split into nine steps (S1–S9 in
`prereg.yaml`): the tuple, the Polymath 8a estimates, Stadlmann's bilinear estimate as adapted, the new factorization
conditions, the sieve evaluation, the two Kloosterman inputs, the 152 numerical bounds, and the semantic question of
whether `Challenge.lean` states the claim as a mathematician would. Each step was assigned how it could be checked:
computation, literature, formal-conditional, rerun-of-certificate, or human-semantic-review.

**Standing.** Every finding carries one of four words. *Certified*: a deterministic check we ran under a rule
written first, or a formal check rerun by a party independent of the authors. *Accepted*: a refereed theorem, a
formal check reported by the authors' own toolchain, or a step inside a formally checked deduction. *Refuted*: a
counterexample, a failed check, or a published objection the authors have not answered. *Open*: an input nobody
independent has checked; it is a gap, not a finding, and it carries no standing. Numeric spot checks on small cases
corroborate a literature input but never raise its standing.

**The claim rule.** The whole claim is called verified only if every step is certified or accepted from refereed
literature and the formal deduction has been rerun independently. Otherwise it is called conditionally supported and
each open input is named. The second condition is now met. The first is not: the two Kloosterman inputs are accepted
from the literature, and the semantic step is open.

**Pre-registration.** Each check and its predicted outcome were written down before the check ran. Later changes go
in dated amendments appended to the file, never into the body. `prereg_cycle6.sha256` holds two hashes: the file as
first written and the file after amendment A1. (The path in that file is from the parent repository; the hashes are of
the file as it stands here.) Standing consequences were also written in advance: what moves if C4 and C5 pass, what
happens if C6 passes unexpectedly, what gets recorded as an anomaly if C9 fails.

**What moved.** The Lean deduction moved from accepted (the authors' toolchain) to certified (rerun independently).
The 152 numerical bounds moved from open to certified. Three corrections were recorded: an earlier draft called
Stadlmann's 240 the first improvement in a decade, when Zhang's 240 was deposited three days earlier; an earlier
draft said the certificate needed a library OpenAI had not published, when the missing piece is a public, unreleased
upstream fix; and descriptions counting six assumptions were replaced with three, since `propext`, `Quot.sound` and
`Classical.choice` are Lean's standard rules. Final standing: certified 4, accepted 5, refuted 0, open 3.

**Who did the work.** Nervous Machine, with Claude Code as the operating agent that wrote the pre-registrations,
scripts and ledger entries and ran them. The agent did not read the proof and makes no claim about the mathematics
beyond what the checks establish. Everything it did is in the logs.

## What remains open, in the order that would settle the claim fastest

1. **Do the three goal statements in `Challenge.lean` say what the paper claims?** Comparator confirms the proofs
   reach their stated goals. It cannot confirm the goals are the right ones. The repository's `formalization.yaml`
   records the review status as self-assessed with no independent human semantic review. This is a reading task for
   a number theorist, of three statements, and it is the step that decides whether "conditionally supported" becomes
   something stronger.
2. **Refereeing**, or an independent expert read of the written proof. None has been reported.
3. **The two classical bounds** (Deligne's hyper-Kloosterman bound; Fouvry, Kowalski and Michel's correlation bound)
   are axioms in the Lean development. Either formalize them or record that the field accepts them as standard.

## The ask

**A second rerun, on x86.** Ours was on aarch64. The FLINT bug that the certificate guards against is in the FFT
multiplication path, so architecture is a real variable here. `REPRODUCE.md` is the recipe; it took about two hours
of machine time on 20 cores plus setup. Open an issue titled "Rerun: <your machine>" with your `results_cycle6.json`
equivalent, or send a pull request adding a row to `RESULTS.md`. A failed check is as welcome as a pass; say what
failed.

**A human read of `Challenge.lean`.** Start with `trace/DEFINITIONAL-TRACE.md`. It quotes each of the three goals and
three axioms verbatim, traces every definition down to Mathlib with file and line, gives a plain-language rendering,
names the paper location to compare against (Theorem 1.1, Corollary 1.2, Lemma A.4; (2.30)–(2.33) of the numerics
note), and ends with a sign-off checklist. Parts A and B take under an hour. The renderings are ours and carry no
standing; a reviewer's signature would. Open an issue titled "Semantic read" and say what you found, in either
direction. That one issue would close the biggest open item on this scorecard.

## Cycle 7: the definitional trace (8 November 2026)

Pre-registered in `prereg_cycle7.yaml` before the paper was read. `trace/DEFINITIONAL-TRACE.md` is the result.
Alongside it, `cycle7/compare_tables.py` compared every number in `Challenge.lean` with the numerics paper: the 77
trial coefficients, all 97 component rows, the mask caps, the shared constants, the three scalar bounds, and the
budget and margin arithmetic in exact rationals. All match (`cycle7/table_compare.json`). One discrepancy was found,
in `formalization.yaml`, which labels the lim inf statement "Theorem 1.1" where the paper and the Lean docstring say
Corollary 1.2. No discrepancy affecting content was seen by the agent. The trace changed no standing: the semantic
gap stays open until a person signs the checklist.

## Layout

```
README.md               this file
prereg_cycle7.yaml      pre-registration for the trace, with its hash alongside
trace/                  DEFINITIONAL-TRACE.md, the reading guide for a semantic reviewer
cycle7/                 lean_statements.txt, declarations.tsv, compare_tables.py, table_compare.json
RESULTS.md              one row per independent rerun; how to add yours
REPRODUCE.md            the recipe, step by step, from a fresh Ubuntu machine
SCORECARD.md            the human-readable scorecard, as briefed on 7 November 2026
prereg.yaml             pre-registration for cycles 0–5 and checks C1–C3, with amendment A1
prereg_cycle6.yaml      pre-registration for the rerun, C4–C7, with amendment A1 adding C8–C9
prereg_cycle6.sha256    hashes of that file before and after the amendment
checks.py, results.json C1–C3 and their output (python3 -I checks.py reruns them in seconds)
source/                 Challenge.lean at the pinned commit, verbatim, with its Apache-2.0 licence
cycle6/                 every log, the receipt, environment, tool commits, the scripts, collect.py, results_cycle6.json
ledger/                 the DEBRIEF ledger for this mission and its schema
```

## Provenance and licences

`source/Challenge.lean` is OpenAI's, unmodified, under Apache-2.0 (`source/LICENSE-openai-PrimeGaps186`). The
certificate program is not vendored; the recipe fetches it at the pinned commit and records its hash. Everything
else in this repository is by Nervous Machine under Apache-2.0 (`LICENSE`). References: the OpenAI paper and
numerics note in the pinned repository; Zhang, Zenodo, 28 August 2026; Stadlmann, arXiv 2608.31126; Axiom Math,
3 September 2026 announcement and draft; FLINT pull request 2790.
