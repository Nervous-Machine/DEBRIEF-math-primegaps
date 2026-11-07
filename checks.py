#!/usr/bin/env python3
"""Checks C1-C3 from prereg.yaml (registered 2026-11-07 before running). Writes results.json next to this file.

C1  the 40-tuple in PrimeGaps186.lean is admissible and has diameter 186
C2  |normalized Kl3(c; p)| <= 3 for nonzero c, primes p <= 97 (definition as in PrimeGaps186.lean)
C3  |sum_{t != 0,-1} K2(A/t) K2(B/(t+1))| <= 8 p sqrt(p) for nonzero A, B, primes p <= 61 (unnormalized K2, as in the Lean file)
C2 and C3 are numeric corroboration on small primes; they do not prove the axioms. C3 skips p = 2, where the sum is
empty and the bound holds trivially (amendment A1).

Provenance (amendment A1): the tuple and the two axiom statements are transcribed from openai/PrimeGaps186 at the commit
below. A verbatim copy of Challenge.lean is in ./source/. This script reads the tuple from that copy, checks the file hash
and the presence of the two axiom statements it transcribes, and fails if any of them differ from what was registered.
"""
import json, os, cmath, math, hashlib, re, sys

SOURCE = {"repo": "github.com/openai/PrimeGaps186", "commit": "61340d0b74163003b32756bb16e91d9209a5e330", "committed": "2026-09-02",
          "file": "Challenge.lean", "sha256": "b99a403b1946547ef1926cd43ebce717640f7f76fa7e1f8f5a4b19ac2e53e1f0", "fetched": "2026-11-07"}
AXIOM_TEXT = {"C2": "c ≠ 0 → ‖PrimeGap186.normalizedKloosterman3 p c‖ ≤ (3 : ℝ)", "C3": "8 * (p : ℝ) * Real.sqrt (p : ℝ)"}

H = [0, 2, 6, 12, 20, 26, 30, 32, 36, 42, 48, 50, 56, 60, 68, 72, 78, 86, 90, 92, 98, 102, 110, 116, 120, 126, 132, 138,
     140, 146, 152, 156, 158, 162, 168, 170, 176, 180, 182, 186]


def provenance():
    """Pin the inputs: the vendored Lean file must hash as registered, define the same 40-tuple as H, and contain the two
    axiom statements C2 and C3 transcribe. Any mismatch stops the run."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "source", SOURCE["file"])
    raw = open(path, "rb").read()
    digest = hashlib.sha256(raw).hexdigest()
    text = raw.decode("utf-8")
    m = re.search(r"def admissibleTuple : Finset ℕ :=\s*\{([^}]*)\}", text)
    tuple_in_source = [int(x) for x in m.group(1).replace("\n", " ").split(",")] if m else None
    axioms_present = {k: v in text for k, v in AXIOM_TEXT.items()}
    out = {**SOURCE, "sha256_observed": digest, "tuple_in_source": tuple_in_source, "tuple_matches_H": tuple_in_source == H, "axiom_text_present": axioms_present}
    if digest != SOURCE["sha256"] or tuple_in_source != H or not all(axioms_present.values()):
        sys.exit("provenance check failed: " + json.dumps(out))
    return out


def primes(n):
    return [p for p in range(2, n + 1) if all(p % q for q in range(2, int(p ** 0.5) + 1))]


def c1():
    k = len(H)
    misses = {}
    for p in primes(k):  # a k-tuple cannot cover all residues of a prime p > k
        used = {h % p for h in H}
        misses[p] = sorted(set(range(p)) - used)[:3]
    ok = len(set(H)) == 40 and max(H) - min(H) == 186 and all(misses[p] for p in misses)
    return {"pass": ok, "size": len(set(H)), "diameter": max(H) - min(H), "first_missed_residues": misses}


def roots(p):
    return [cmath.exp(2j * math.pi * k / p) for k in range(p)]


def c2(pmax=97):
    worst = {}
    for p in primes(pmax):
        R, inv = roots(p), [0] + [pow(a, p - 2, p) for a in range(1, p)]
        best = 0.0
        for c in range(1, p):
            s = 0j
            for u in range(1, p):
                cu = c * inv[u] % p
                for v in range(1, p):
                    s += R[(u + v + cu * inv[v]) % p]  # w = c / (u v)
            best = max(best, abs(s) / p)
        worst[p] = round(best, 6)
    return {"pass": all(v <= 3 + 1e-9 for v in worst.values()), "max_abs_by_prime": worst}


def c3(pmax=61):
    worst = {}
    for p in primes(pmax):
        if p < 3:
            continue
        R, inv = roots(p), [0] + [pow(a, p - 2, p) for a in range(1, p)]
        K2 = [sum(R[(u + c * inv[u]) % p] for u in range(1, p)) for c in range(p)]  # K2(c) = sum_u e((u + c/u)/p)
        ts = [t for t in range(1, p) if (t + 1) % p != 0]
        best = 0.0
        for A in range(1, p):
            ka = [K2[A * inv[t] % p] for t in ts]
            for B in range(1, p):
                s = sum(x * K2[B * inv[(t + 1) % p] % p] for x, t in zip(ka, ts))
                best = max(best, abs(s))
        bound = 8 * p * math.sqrt(p)
        worst[p] = {"max_abs": round(best, 3), "bound": round(bound, 3), "ratio": round(best / bound, 4)}
    return {"pass": all(v["max_abs"] <= v["bound"] for v in worst.values()), "by_prime": worst}


if __name__ == "__main__":
    out = {"registered": "prereg.yaml (2026-11-07); amendment A1 after the checks", "provenance": provenance(), "C1": c1(), "C2": c2(), "C3": c3()}
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results.json")
    json.dump(out, open(path, "w"), indent=1)
    print({k: out[k]["pass"] for k in ("C1", "C2", "C3")})
    print("C2 worst:", max(out["C2"]["max_abs_by_prime"].values()), " C3 worst ratio:", max(v["ratio"] for v in out["C3"]["by_prime"].values()))
