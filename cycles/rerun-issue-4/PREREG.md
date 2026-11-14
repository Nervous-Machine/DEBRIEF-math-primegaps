# Pre-registration: second independent rerun of openai/PrimeGaps186

Written 2026-11-13, before any step below was run. Party: Fredrik Prüzelius (with Claude Code).
Machine: isolated OrbStack VM, Ubuntu 24.04, aarch64, 16 vCPU, 36 GB RAM, on an Apple M5 Pro host (macOS).
Source: openai/PrimeGaps186 @ 61340d0b74163003b32756bb16e91d9209a5e330.
Our scripts were written independently from the DEBRIEF recipe (REPRODUCE.md was read; their shell scripts were not reused).
Only `probe_flint.py` (a verbatim copy of the certificate's own regression check) is taken from DEBRIEF.

| id | step | prediction |
|---|---|---|
| P0 | `Challenge.lean` sha256 = b99a403b…e1f0; certificate sha256 = 7f71bdef…5de4 | match |
| P1 | 40-tuple read from `Challenge.lean`: 40 distinct, diameter 186, admissible for all p ≤ 40 | pass |
| P4 | `lake exe cache get && lake build PrimeGaps186` | exit 0, 0 warnings, 0 errors; wall 8–20 min; peak RSS < 34 GB |
| P5a | Comparator (Nanoda + Lean kernel) on `comparator/main.json` | 3/3 matched, exit 0 |
| P5b | `#print axioms` on the three theorems | exactly the 6 permitted axioms |
| P6 | certificate regression on stock PyPI python-flint 0.9.0 | fail (first mismatch at index 15) |
| P8 | same regression on FLINT 3.6.0 + 7ad753d, python-flint 0.9.0 from source | pass |
| P9 | `prime_gap_186_certificate.py --workers 4` | `passed: true`; lower margin ≈ 2.336e-5 ≥ 2e-5, identical to DEBRIEF's receipt; wall 40–90 min |

A failure of any prediction is a result and will be reported as such.
