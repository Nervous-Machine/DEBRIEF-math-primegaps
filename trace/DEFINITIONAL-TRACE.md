# Definitional trace of `Challenge.lean` (openai/PrimeGaps186 at commit 61340d0)

**For:** a number theorist who is willing to spend an hour, not a day, deciding whether the three formal goal statements
and the three axioms in OpenAI's Lean development say what the paper "Improved short gaps between primes" claims.

**What this is.** For each of the six statements: the Lean text verbatim, every definition it depends on down to Mathlib
with file and line, a plain-language rendering, the place in the paper to compare against, and the specific points
to confirm. The renderings are the reading of the operating agent (Claude Code, for Nervous Machine) on 8 November
2026. They are an aid, not a check. Where the agent did not trace something to the bottom, it says so.

**What this is not.** It is not an independent human semantic review, and it does not change the standing of
anything. The repository's own `formalization.yaml` records review status "self-assessed", "No independent human
semantic review". That stays true until a human signs the checklist at the end.

**Sources, pinned.** `Challenge.lean`, sha256 `b99a403b1946547ef1926cd43ebce717640f7f76fa7e1f8f5a4b19ac2e53e1f0`
(verbatim copy in `source/`). Mathlib at the revision pinned by the repository's `lake-manifest.json` (rev `bbcd1968`).
Main paper: `short_gaps.pdf` from cdn.openai.com, sha256 `456f05e0a3ef589ebb0e9abcfd31f140f3c945adbf6950e00ef371a3c88b0930`,
dated 30 August 2026. Numerics paper: `short_gaps_numerics.pdf` in the repository, sha256 `79190b2c…`. Machine
transcripts: `cycle7/lean_statements.txt` (the statements and definitions as the built development prints them),
`cycle7/table_compare.json` (every number table compared mechanically), `cycle7/declarations.tsv` (all 77 declarations
in the file with their docstrings). Pre-registration for this trace: `prereg_cycle7.yaml`.

**Time.** Part A (the three goals): 30 to 45 minutes. Part B (the two Kloosterman axioms): 20 minutes. Part C (the
numerical axiom): 30 minutes for its shape; the meaning of its left-hand sides is the one open-ended task, and is
marked as such.

---

## 0. Mathlib conventions a reviewer has to know

These are the places where Lean's meaning differs from the blackboard's. Each is used below.

| convention | where | what it means here |
|---|---|---|
| Division by zero is zero | all Lean fields, including `ZMod p`, `ℚ`, `ℝ` | `x / 0 = 0`. Every division in the axioms is guarded (B2), so this never bites, but check it. |
| `Nat.Prime p` is `Irreducible p` in ℕ | `Mathlib/Data/Nat/Prime/Defs.lean` l.42 | a natural number ≥ 2 whose only factorizations are trivial (`Nat.prime_def` gives the textbook form) |
| `Nat.nth p n` is 0-indexed | `Mathlib/Data/Nat/Nth.lean` l.60 | `nth Nat.Prime 0 = 2`, `nth Nat.Prime 1 = 3` (Mathlib lemmas `nth_prime_zero_eq_two`, `nth_prime_one_eq_three`). For a finite predicate it falls back to a sorted list with default 0; the primes are infinite in Mathlib, so here it is the genuine n-th prime. |
| `Int.toNat` sends negatives to 0 | Lean core `Init/Data/Int/Basic.lean` | so `(n + h).toNat.Prime` means "n + h is a positive prime" |
| `Filter.liminf u atTop = sSup {a ∣ ∀ᶠ n, a ≤ u n}` | `Mathlib/Order/LiminfLimsup.lean` l.60, l.70 | the supremum of all a such that eventually u n ≥ a. In `EReal`, a complete lattice, this is the classical lim inf. |
| `ZMod p` for prime p is the field F_p; `(ZMod p)ˣ` its units | Mathlib | — |
| `ZMod.stdAddChar j = exp(2πi j / p)` | `Mathlib/Analysis/SpecialFunctions/Complex/CircleAddChar.lean` l.83, lemma `stdAddChar_coe` l.86 | the paper's e_p |
| `‖z‖` on ℂ | Mathlib | the modulus |
| `Finset.filter`, `Finset.card`, `Set.Infinite` | Mathlib | the obvious meanings; a `Finset` has distinct elements |

---

## Part A. The three goals

### A1. `dhl_40_2` ↔ Theorem 1.1

Lean (`Challenge.lean` l.948–954):
```lean
/-- Theorem 1.1 of the main paper: every admissible integer 40-tuple has two-prime translates. -/
theorem dhl_40_2
    (H : Finset ℤ) (hcard : H.card = 40)
    (hadm : ∀ p : ℕ, p.Prime → ∃ a : ZMod p, ∀ h ∈ H, (h : ZMod p) ≠ a) :
    Set.Infinite {n : ℤ | 2 ≤ (H.filter (fun h => (n + h).toNat.Prime)).card}
```
Paper (p.1): "A set of distinct integers is admissible if it omits a residue class modulo every prime. Following
Polymath [16, Claim 3.1], write DHL[k, j] for the assertion that every admissible k-tuple has infinitely many
translates containing at least j primes. **Theorem 1.1.** The assertion DHL[40, 2] holds."

Depends on: `Finset ℤ`, `Finset.card`, `Nat.Prime`, `ZMod p` and the cast ℤ → `ZMod p`, `Int.toNat`, `Finset.filter`,
`Set.Infinite`. Nothing project-specific.

Agent's rendering: *For every set H of 40 distinct integers such that, for every prime p, some residue class mod p
contains no element of H, there are infinitely many integers n for which at least two of the numbers n + h (h ∈ H)
are positive primes.*

Points to confirm:
1. `hadm` is admissibility: for every prime p there is a residue `a` that no `h ∈ H` hits. (The quantifier runs over
   all primes, including p > 40 where it is automatic.)
2. "Distinct integers", "40 of them": `Finset ℤ` with `card = 40`.
3. "Infinitely many translates containing at least two primes": infinitely many `n` with at least two `h` such that
   `n + h` is prime. Distinct `n` give distinct translates, so counting `n` is counting translates.
4. `Int.toNat`: a negative `n + h` becomes 0, which is not prime. So the predicate is "n + h is a prime", with primes
   positive, as in the paper.
5. The paper's proof says "by translation, assume h_i ≥ 0"; the Lean statement does not assume it. That is the
   stronger (correct) statement of DHL[40,2].

Agent's verdict: matches, with no convention surprise beyond item 4.

### A2. `infinite_two_prime_translates_admissibleTuple` ↔ equation (1.3) and the sentence after it

Lean (l.937–941, 956–959):
```lean
def admissibleTuple : Finset ℕ :=
  {0, 2, 6, 12, 20, 26, 30, 32, 36, 42, 48, 50, 56, 60, 68, 72, 78, 86, 90, 92,
    98, 102, 110, 116, 120, 126, 132, 138, 140, 146, 152, 156, 158, 162,
    168, 170, 176, 180, 182, 186}

theorem infinite_two_prime_translates_admissibleTuple :
    Set.Infinite {n : ℕ | 2 ≤ (admissibleTuple.filter (fun h => (n + h).Prime)).card}
```
Paper (p.1): "The 40-element set H := {0, 2, 6, …, 182, 186} (1.3) is admissible and has diameter 186, so
Theorem 1.1 implies the following."

Agent's rendering: *There are infinitely many natural numbers n such that at least two of n + h, for h in the
explicit 40-element list, are prime.*

Points to confirm:
1. The list equals (1.3) element by element. Checked mechanically (`results.json`, check C1; the list is read from
   this file). Its 40 entries are distinct, span 0 to 186, and miss a residue class for every prime ≤ 40.
2. `n : ℕ` rather than `ℤ`. Infinitely many natural n is what the paper needs; the integer version (A1 applied to
   this H) implies it, since for n < −186 every n + h is negative and at most 186 negative n can qualify.

Agent's verdict: matches. The docstring calls it a "supporting conclusion in the proof of Corollary 1.2", which is
what the paper's sentence is.

### A3. `primeGapLiminf_le_186` ↔ Corollary 1.2

Lean (l.943–947, 962–964):
```lean
/-- The extended-real liminf of consecutive prime gaps; `Nat.nth Nat.Prime 0 = 2`. -/
noncomputable def primeGapLiminf : EReal :=
  Filter.liminf
    (fun n : ℕ =>
      (Nat.nth Nat.Prime (n + 1) : EReal) - (Nat.nth Nat.Prime n : EReal))
    Filter.atTop

theorem primeGapLiminf_le_186 : primeGapLiminf ≤ (186 : EReal)
```
Paper (p.1): "Write H_m := lim inf_{n→∞} (p_{n+m} − p_n), where p_n is the nth prime. … **Corollary 1.2.** We have
H_1 ≤ 186."

Depends on: `Nat.nth` (0-indexed n-th prime), `EReal` and the casts ℕ → `EReal`, `Filter.liminf`, `Filter.limsInf`,
`Filter.atTop`, `Filter.Eventually`, `sSup` in `EReal`.

Agent's rendering: *Write q_n for the n-th prime counting from q_0 = 2. The lower limit, as n → ∞, of q_{n+1} − q_n,
taken in the extended reals, is at most 186.*

Points to confirm:
1. `Nat.nth Nat.Prime` is the genuine enumeration of primes: the primes are an infinite set in Mathlib, so `nth` is
   the order isomorphism ℕ ≃ primes, not the finite fallback. `q_n = p_{n+1}` in the paper's indexing; a shift of
   index does not change a lim inf.
2. Mathlib's `liminf` in `EReal` is the classical one: the supremum of all a such that eventually the gap is ≥ a.
   Since gaps are integers: lim inf ≤ 186 ⟺ it is not the case that eventually gap ≥ 187 ⟺ gap ≤ 186 for infinitely
   many n. That is "infinitely many pairs of consecutive primes at most 186 apart", which is H_1 ≤ 186.
3. The cast to `EReal` and the subtraction are on finite values, so no ⊤/⊥ arithmetic is involved.

Agent's verdict: matches. Note the paper defines H_m in the extended sense implicitly; Lean makes it explicit with
`EReal`.

---

## Part B. The two exponential-sum axioms ↔ Lemma A.4

Paper, Appendix A.3 (p.32):
> We use the normalization Kl_3(c; m) := (1/m) Σ_{x_1,x_2,x_3 mod m, x_1x_2x_3 = c mod m} e_m(x_1 + x_2 + x_3), also for
> composite m. For a prime p, put K_2(c; p) := Σ_{u ∈ F_p^×} e_p(u + c/u); this second sum is unnormalized.
>
> **Lemma A.4 (Prime-field inputs).** For every prime p and nonzero c, A, B ∈ F_p,
> |Kl_3(c; p)| ≤ 3,   |Σ_{t ∈ F_p∖{0,−1}} K_2(A/t; p) K_2(B/(t+1); p)| ≤ 8p√p.   (A.6)
>
> Proof. The first estimate is [10, Thm. 4.1.1(1)–(2), p. 49]: rank three and weight two give the unnormalized bound
> 3p. For the second, substitute u ↦ u^{−1} in [5, Prop. 2]. Its normalized sum is K_2(c;p)/√p, so its bound 8√p gives
> the displayed bound. The two excluded poles are retained in both statements.

([10] is Katz, *Gauss sums, Kloosterman sums, and monodromy groups*; [5] is Fouvry, Kowalski and Michel, *The
Friedlander–Iwaniec character sum*, 2013.) The paper's text on p.1 says the repository states "the precise
exponential-sum bounds of Lemma A.4 … as explicit assumptions."

### B1. `kloosterman3_bound` ↔ Lemma A.4, first bound

Lean (l.26–35, 48–50):
```lean
noncomputable def normalizedKloosterman3 (p : ℕ) [Fact p.Prime] (c : ZMod p) : ℂ :=
  (p : ℂ)⁻¹ *
    ∑ u : ZMod p, ∑ v : ZMod p, ∑ w : ZMod p,
      if u * v * w = c then ZMod.stdAddChar (u + v + w) else 0

axiom PrimeGap186.kloosterman3_bound :
  ∀ (p : ℕ) [Fact p.Prime] (c : ZMod p),
    c ≠ 0 → ‖PrimeGap186.normalizedKloosterman3 p c‖ ≤ (3 : ℝ)
```
Correspondence, term by term:

| Lean | paper | note |
|---|---|---|
| `(p : ℂ)⁻¹ *` | 1/m with m = p | same normalization |
| triple sum over `ZMod p` with `if u*v*w = c` | Σ over x_1,x_2,x_3 mod p with x_1x_2x_3 = c | Lean sums over all of F_p including 0; with c ≠ 0 a zero factor never satisfies the condition, exactly as in the paper |
| `ZMod.stdAddChar (u+v+w)` | e_p(x_1+x_2+x_3) | `stdAddChar_coe`: exp(2πi j/p) |
| `c ≠ 0` | nonzero c | — |
| `‖·‖ ≤ 3` | ≤ 3 | same constant |

Agent's rendering: *For every prime p and every nonzero c in F_p, the rank-three hyper-Kloosterman sum, normalized
by 1/p, has modulus at most 3.*

Agent's verdict: the axiom is Lemma A.4's first bound, verbatim in meaning, with the same normalization. Whether
Lemma A.4's first bound is a correct statement of Deligne's theorem as given in Katz is the reviewer's judgment;
this trace does not make it (pre-registration rule R4). Numerically it holds for all primes ≤ 97 with maximum
2.351 (`results.json`, C2).

### B2. `kloosterman2_correlation_bound` ↔ Lemma A.4, second bound

Lean (l.37–45, 52–57):
```lean
noncomputable def unnormalizedKloosterman2 (p : ℕ) [Fact p.Prime] (c : ZMod p) : ℂ :=
  ∑ u : (ZMod p)ˣ,
    ZMod.stdAddChar ((u : ZMod p) + c / (u : ZMod p))

axiom PrimeGap186.kloosterman2_correlation_bound :
  ∀ (p : ℕ) [Fact p.Prime] (A B : ZMod p),
    A ≠ 0 → B ≠ 0 →
      ‖∑ t : ZMod p, if t ≠ 0 ∧ t ≠ -1 then
        PrimeGap186.unnormalizedKloosterman2 p (A / t) *
          PrimeGap186.unnormalizedKloosterman2 p (B / (t + 1)) else 0‖ ≤
        8 * (p : ℝ) * Real.sqrt (p : ℝ)
```
Correspondence:

| Lean | paper | note |
|---|---|---|
| `∑ u : (ZMod p)ˣ` | Σ_{u ∈ F_p^×} | units of F_p |
| `(u : ZMod p) + c / (u : ZMod p)` | u + c/u | u is a unit, so the division is a genuine field division (convention 0 never triggers) |
| no normalization | "this second sum is unnormalized" | — |
| `if t ≠ 0 ∧ t ≠ -1 then … else 0` | Σ_{t ∈ F_p ∖ {0, −1}} | same index set |
| `A / t`, `B / (t + 1)` | A/t, B/(t+1) | t ≠ 0 and t ≠ −1, so both denominators are nonzero |
| `A ≠ 0 → B ≠ 0 →` | nonzero A, B | — |
| `8 * p * Real.sqrt p` | 8p√p | same constant |

Agent's rendering: *For every prime p and nonzero A, B in F_p, the sum over t ≠ 0, −1 of K_2(A/t) · K_2(B/(t+1)),
with K_2 the unnormalized classical Kloosterman sum, has modulus at most 8 p^{3/2}.*

Agent's verdict: the axiom is Lemma A.4's second bound, verbatim in meaning. For p = 2 the index set is empty and
the bound is trivial, which is why the spot check C3 skips it. Numerically it holds for all primes ≤ 61 with the
ratio to the bound never above 0.458 (`results.json`, C3). Whether the bound follows from Fouvry–Kowalski–Michel
Proposition 2 as the paper says is the reviewer's judgment.

---

## Part C. The numerical axiom ↔ the numerics paper

### C1. Shape of the axiom

Lean (l.896–933), compressed:
```lean
axiom PrimeGap186.physical_integral_bounds :
  (∀ j : Fin outerOrderTwoBounds.length,
     physicalSourceOuterRoot 0 j / (23685317816 / 10^24) ≤ (outerOrderTwoBounds.get j).2.1 / 10^18 ∧
     physicalSourceOuterFace 0 j / (23685317816 / 10^24) ≤ (outerOrderTwoBounds.get j).2.2.1 / 10^18) ∧
  (∀ j : Fin outerOrderFiveHalvesBounds.length,  … same with group 1 and that table …) ∧
  (∀ j : Fin innerBaseOrderTwoBounds.length,
     physicalSourceInnerMass 2 j / (23685317816 / 10^24) ≤ (innerBaseOrderTwoBounds.get j).1 / 10^18) ∧
  (∀ j : Fin innerBaseOrderFiveHalvesBounds.length,     … group 3 …) ∧
  (∀ j : Fin innerEnlargedOrderTwoBounds.length,        … group 4 …) ∧
  (∀ j : Fin innerEnlargedOrderFiveHalvesBounds.length, … group 5 …) ∧
  23685317816 / 10^24 ≤ trialIH ∧ trialIH ≤ 23685317890 / 10^24 ∧
  90248755123 / 10^24 ≤ trialJLambdaH
```
Numerics paper, §2.4 and §2.5:
> For an outer component their integers q, A, B, E mean c := q/10^6, R/I_H^− ≤ A/10^18, V/I_H^− ≤ B/10^18,
> cA/10^18 + B/(10^18 c) ≤ E/10^12. (2.30)
> For an inner component the recorded A, E mean β_G/I_H^− ≤ A/10^18, κ_G A/10^18 ≤ E/10^12. (2.31)
> **Lemma 2.5.** 23685317816·10^−24 ≤ I_H ≤ 23685317890·10^−24, J_{λ,H} ≥ 90248755123·10^−24. (2.33)

with I_H^− := 23685317816·10^−24 (the lower endpoint), R_j and V_j "the positive upper forms in (2.17) and (2.21)",
β_G the inner failure masses of (1.30), κ_G = d_0 for the old (base) inner groups and 1 − b_h for the new (enlarged).

What the axiom asserts: for each of the 17 + 35 outer rows, the two inequalities R/I_H^− ≤ A/10^18 and
V/I_H^− ≤ B/10^18; for each of the 7 + 10 + 11 + 17 inner rows, β/I_H^− ≤ A/10^18; and the three scalar bounds of
Lemma 2.5. That is 2·52 + 45 + 3 = 152 inequalities, which is the "152 numerical bounds" of the ledger.

What the axiom does **not** assert, and therefore what Lean proves from the data: the budget inequalities (the last
clauses of (2.30) and (2.31)), the group totals (2.32), and the final margin (2.35). Columns q and E in the Lean
tables are proof data for those steps. Our script checked that they hold exactly in rational arithmetic
(`table_compare.json`: `budget_inequalities_2_30_2_31_hold_exactly`, `grand_total_696075110`,
`corollary_2_6_margin_exact` = 230382667/10^13 ≈ 2.30·10^−5 > 1/50000). That is a consistency check on the tables;
Lean's kernel is what checked the proof.

Points to confirm (shape): the division by the lower endpoint I_H^− on every component, as in (2.30)–(2.31); the
`.2.1` / `.2.2.1` projections pick A and B out of the (q, A, B, E) row and `.1` picks A out of (A, E); the group
indices 0..5 are (outer order 2, outer order 5/2, base inner 2, base inner 5/2, enlarged inner 2, enlarged inner 5/2),
matching the paper's O_2, O_{5/2}, I_2^old, I_{5/2}^old, I_2^new, I_{5/2}^new (the `physicalSourceGroup` docstring,
l.626, and `physicalSourceInnerMass`, which uses the base mask for groups < 4 and the enlarged mask otherwise).

### C2. The data

Every number in the statement file was compared with the numerics paper (`cycle7/compare_tables.py`, output
`cycle7/table_compare.json`). All match:

| Lean | numerics paper | rows |
|---|---|---|
| `trialCoefficientInteger` | Table 1.1 (the 77 integers C_{σ,d}, c_{σ,d} = 10^−10 C_{σ,d}) | 11 × 7 |
| `trialAngularSignature` | (1.6): ∅, (2), (3), (4), (5), (6), (2,2), (2,3), (2,4), (3,3), (2,2,2) | 11 |
| `outerOrderTwoBounds` | Table 2.1 (q, A, B, E) | 17 |
| `outerOrderFiveHalvesBounds` | Table 2.2 | 35 |
| `innerBaseOrderTwoBounds` | Table 2.3 (A, E) | 7 |
| `innerBaseOrderFiveHalvesBounds` | Table 2.4 | 10 |
| `innerEnlargedOrderTwoBounds` | Table 2.5 | 11 |
| `innerEnlargedOrderFiveHalvesBounds` | Table 2.6 | 17 |
| the three scalars in the axiom | Lemma 2.5, (2.33) | 3 |
| mask caps in `trialOuterMask`, `trialBaseMask`, `trialEnlargedMask`, `trialFullMask` | (1.5): index ranges and z/h values 68225, 49152, 46580, 44781, 35265, 44976, 35419 | — |
| `trialMesh = (2742997/2624989)/98304` | h = S/N, S = 2742997/2624989, N = 98304 (1.1), (1.3) | — |
| `trialProfile` | g(t) = (21/200)/(1 + t/100) + (179/200)/(1 + (907/5) t) (1.7) | — |
| `trialProfileNormalizer = Σ_{j<98264} g(t°_j)²` | Z = Σ_{j<n} g(t°_j)², n = N − 40 = 98264 | — |
| `physicalSourceRho = 262499/10^6` | ρ = 1/4 + Ω_o = 262499/10^6 (1.13) | — |
| coefficients in `trialJLambdaH`: 2479900401/2500000000 + (−843183/10^9), and −843183/10^9 | a_h + b_h and b_h, (1.28)–(1.29) | — |
| `trialLargestCap = 68225 · h` | ζ = 19037/(10^5 ρ) = 190370/262499, "rounded down to a multiple of h" (§1.1); ζ/h = 68225.10…, floor 68225 | — |

### C3. The meaning of the left-hand sides (the open-ended part)

The right-hand sides are numbers. The left-hand sides, `physicalSourceOuterRoot g j`, `physicalSourceOuterFace g j`,
`physicalSourceInnerMass g j`, `trialIH`, `trialJLambdaH`, are real numbers defined by about 830 lines of Lean
(l.60–895) in measure theory on `FiniteMeasure ℝ`. The question for the reviewer is whether those Lean reals are the
paper's I_H, J_{λ,H}, R_j, V_j and β_G. The certificate program computes rigorous enclosures of the paper's
quantities; the axiom asserts the same inequalities about the Lean-defined quantities. If the two sets of definitions
diverge, the certificate's pass says nothing about the axiom.

The agent traced the chain below from the Lean docstrings and the numerics paper's §1. It did **not** trace the
source-support and covering definitions (`PhysicalSourceRowData` through `physicalSourceCover`, l.468–850) against
the paper's §1.3–§2.2; those are listed by name only.

**The fragment measure (traced).**

| Lean (line) | docstring, abridged | paper |
|---|---|---|
| `weightedEmpirical` (66) | atomic measure giving weight max(x_i, 0) at each sample x_i | a fragment configuration X as a weighted multiset |
| `finitePoissonLaw` (76) | Poisson count of mean μ.mass, locations from μ.normalize, weighted empirical measure | L(Π_c) restricted to a band |
| `cappedDyadicIntensity` (87) | density 1/u on (0, ζ] ∩ (2^k, 2^{k+1}] | the intensity dv/v of Π_c, cut into dyadic bands so each piece is finite |
| `finiteFragments` (114) | sum of the band measures when finite, else 0 | reassembling the bands |
| `fragmentLaw` (123) | "the probability law of the finite weighted fragment measure … The paper's measure ν_ζ is exp(γ)·ζ times this law" | ν_c := e^γ c L(Π_c), numerics §1 |
| `trialPhysicalMeasure` (309) | ofReal(e^γ · 68225h) • fragmentLaw(68225h) | ν = ν_ζ with ζ rounded down to the grid |

Reviewer question: is `fragmentLaw ζ` the law of a Poisson process on (0, ζ] with intensity dv/v, viewed as a random
finite measure with atoms weighted by their locations? The docstrings say so; the dyadic cut-and-reassemble is the
part to check.

**The trial function (traced).**

| Lean (line) | paper |
|---|---|
| `trialCellIndex X = ⌊X.mass / h⌋₊` (317) | cell C_j = [jh, (j+1)h) of the coordinate total t_i = |X_i| (1.3) |
| `trialCellMidpoint j = (j + ½) h` (321) | t°_j |
| `trialProfile`, `trialProfileValue`, `trialProfileNormalizer` (327–334) | g, g(t°_j), Z |
| `trialRadialPolynomial s` (286) | Σ_d c_{σ,d} X^d with the Table 1.1 coefficients |
| `angularMonomial σ t` (293) | P_σ(t) = Π_{j∈σ} Σ_i t_i^j, P_∅ = 1 |
| `trialOuterMask` (341) | 1_{H_O}: index sum ≤ 98263 and the per-shell cap from (1.5) |
| `trialCore X t` (396) | F̃(X) = 1_{H_O}(X) Π_i g(t_i) Σ_σ Σ_d c_{σ,d} (s − 9/10)^d P_σ(t), (1.8), with s = Σ t_i |
| `trialStepFunction X` (403) | F: F̃ evaluated at cell midpoints. Σ_i (j_i + ½)h = (r + 20)h, the paper's radial argument (r + 20)h − 9/10 |
| `trialMarginal i Y` (406) | V_i = E_i F = ∫ F(Y ⊕_i X) dν(X) |
| `trialBaseMask`, `trialEnlargedMask`, `trialFullMask` (355–395) | 1_{H_0}, 1_{H_1}, 1_{H_f} from (1.5) |
| `trialPhysicalNormalizer = (h Z)^40` (414) | the common normalization (hZ)^{−40} of §1.1 |
| `trialIH` (421) | I_H = ‖F‖_2^2 / (hZ)^40 |
| `trialJ0`, `trialJPlus`, `trialJTail` (429–457) | J_0, J_+, J_t of (1.9)–(1.10); J_+ uses mask 1_{H_1}(1 − 1_{H_0}) = 1_{H_1∖H_0}, J_t uses 1_{H_f}(1 − 1_{H_1}) |
| `trialJLambdaH` (459) | J_{λ,H} = J_0 + (a_h + b_h) J_+ + b_h J_t, (1.29) |

**The source components (listed, not traced).** `PhysicalSourceRowData` (468), `physicalSourceRho` (509),
`physicalSourceOuterRadius` (512), `physicalSourceInnerRadius` (515), `physicalSourceAdvance` (522),
`physicalSourceOrder` (528), `physicalSourceAffine` (535), `physicalSourceOmegaPrefix` (547), `physicalSourceRow`
(562), `PhysicalSourceGroupData` (584), `physicalSourceGroup` (626), `physicalSourceRows` (663),
`physicalSourceLowBoundaries` (676), `physicalSourceRankFractions` (694), `physicalSourceLowCount` (704),
`physicalSourceRankCount` (709), `physicalSourceRowCount` (715), `physicalSourceComponentKind` (722),
`physicalSourceComponentEndpoints` (730), `physicalSourceTheta` (746), `physicalSourceLowClipping` (758),
`physicalSourceAlignedCapIndex` (778), `physicalSourceRadialMask` (790), `physicalSourceCountMeasure` (809),
`physicalSourceCover` (819), `physicalSourceFaceWeight` (851). These implement the paper's source supports (§1.3,
(1.12)–(1.26)) and the covering functions and face-coefficient envelope of §2 ((2.17), (2.19), (2.21)). Then:

| Lean (line) | paper |
|---|---|
| `physicalSourceOuterRoot g j` (865) | R_j, "the normalized outer-component integral of the squared trial function, summed over all 40 faces and weighted by the covering function and face-coefficient envelope" |
| `physicalSourceOuterFace g j` (876) | V_j, the same with the squared face marginal `trialMarginal i (i.removeNth X)` in place of F² |
| `physicalSourceInnerMass g j` (887) | β_G component: covering-weighted squared marginal on the base mask (groups 2, 3) or enlarged mask (groups 4, 5) |

The docstring of `PhysicalSourceGroupData` (l.584) says "In both TeX documents, `cap` is the group cap z_G and
`split` is p_G", which tells the reviewer the Lean was written against the TeX of both papers and which symbols to
look for.

Reviewer task for C3, honestly stated: read l.468–895 against numerics §1.3–§2.4. The agent estimates this at
several hours for someone who knows the sieve, and it is the only part of the whole file that is.

---

## D. Discrepancies and observations

Pre-registration rule R3: anything the agent can see that differs between the formal text and the paper is recorded,
harmless or not.

| id | what | kind | effect |
|---|---|---|---|
| D1 | `formalization.yaml` aligns `primeGapLiminf_le_186` to "Theorem 1.1 (consecutive-prime gap liminf)". The paper states that as **Corollary 1.2**, and the Lean docstring (l.962) also says Corollary 1.2. | labeling, in the metadata file only | none on content; the yaml should say Corollary 1.2 |
| D2 | `Nat.nth Nat.Prime` is 0-indexed (q_0 = 2); the paper's p_n is 1-indexed (p_1 = 2). | index convention | none; a lim inf is shift-invariant |
| D3 | `dhl_40_2` uses `(n + h).toNat.Prime`; negative n + h map to 0. | Lean convention | none; 0 is not prime, so the predicate is "n + h is a positive prime" as intended |
| D4 | `infinite_two_prime_translates_admissibleTuple` quantifies n over ℕ; the paper's translates range over ℤ. | strengthening in the statement | none; the ℕ statement follows from the ℤ one and is what Corollary 1.2 needs |
| D5 | `trialLargestCap = 68225·h` while the paper's ζ = 190370/262499; ζ/h = 68225.103… | rounding | consistent with the paper's own rule "round the fragment cap down to a multiple of h" (§1.1); Lean encodes the rounded value directly |
| D6 | d_0 = 44415113/5·10^9 of (1.28) does not appear in `Challenge.lean`. | absence | expected: d_0 only enters the budgets E, which are already multiplied through in Tables 2.3–2.4 |
| D7 | The axiom asserts the A and B columns and the three scalars only; q, E, the budget inequalities, the totals and the margin are proof data. | scope | expected; Lean's kernel checked those steps, and they hold exactly by our script |

No discrepancy affecting mathematical content was found by the agent. That sentence is the agent's, and it is the
sentence this trace exists to let a human replace with their own.

Pre-registered predictions (`prereg_cycle7.yaml`): P1 held (goals render to Theorem 1.1 and Corollary 1.2 without a
constant or convention mismatch); P2 held, and the normalizations are identical, not merely equivalent; P3 held (all
numbers verbatim); P4 held (D1 found; nothing affecting content found).

---

## E. Sign-off checklist

For a reviewer who is prepared to put their name to a reading. Each line is a yes/no.

- [ ] A1: `dhl_40_2` states DHL[40,2] as defined on p.1 of the paper.
- [ ] A2: `admissibleTuple` is (1.3), and the theorem states that it has infinitely many two-prime translates.
- [ ] A3: `primeGapLiminf_le_186` states H_1 ≤ 186, with `Nat.nth Nat.Prime` the enumeration of primes and Mathlib's
      `liminf` in `EReal` the classical lim inf.
- [ ] B1: `kloosterman3_bound` is Lemma A.4's first bound with the paper's normalization.
- [ ] B2: `kloosterman2_correlation_bound` is Lemma A.4's second bound with the paper's index set and constant.
- [ ] B (judgment): Lemma A.4 is a correct statement of what Katz [10] and Fouvry–Kowalski–Michel [5] prove.
- [ ] C1: `physical_integral_bounds` has the shape of (2.30), (2.31), (2.33), 152 inequalities, each divided by I_H^−.
- [ ] C2: the numbers are the paper's (the script says so; the reviewer may spot-check).
- [ ] C3 (the long one): `trialIH`, `trialJLambdaH`, `physicalSourceOuterRoot`, `physicalSourceOuterFace` and
      `physicalSourceInnerMass` denote the paper's I_H, J_{λ,H}, R_j, V_j, β_G under ν_ζ.

A reviewer who signs A1–A3 and B1–B2 has closed the semantic question for the conclusion and for the shape of the
exponential-sum inputs. A reviewer who signs C3 has closed it for the numerical input. Either is a public first.
Send it as an issue titled "Semantic read" on github.com/Nervous-Machine/primegaps-186-rerun, or anywhere public;
the ledger will record it by date.
