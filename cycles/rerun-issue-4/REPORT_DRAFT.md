# Rerun: OrbStack Ubuntu VM, aarch64, 16 vCPU, 36 GB, on Apple M5 Pro (DRAFT, not posted)

Second independent rerun of openai/PrimeGaps186 @ 61340d0b74163003b32756bb16e91d9209a5e330.
Pre-registration: `PREREG.md` (written before any step was run). Our scripts (`run.sh`, `run_cont.sh`) were written
independently from REPRODUCE.md; only `probe_flint.py` is a verbatim copy of the certificate's regression check.

## Proposed RESULTS.md row

| date | party | machine | build | comparator | certificate (wall, margin) | record |
|---|---|---|---|---|---|---|
| 2026-11-14 | F. Prüzelius (with Claude Code) | OrbStack Ubuntu 24.04 VM, aarch64, 16 vCPU, 36 GB, on Apple M5 Pro | pass, 15:43, 23.3 GB, 0 warnings | pass, 9:56, six axioms | pass, 2:09:50, 4 workers, 2.336e-5 ≥ 2e-5 | `reruns/2026-11-14-pruzelius/` |

## Predictions vs outcomes

| id | prediction | outcome |
|---|---|---|
| P0 | sha256 Challenge.lean b99a403b…e1f0, certificate 7f71bdef…5de4 | match |
| P1 | 40 distinct, diameter 186, admissible | pass |
| P4 | build exit 0, 0 warnings, 0 errors; 8–20 min; RSS < 34 GB | pass: rc 0, 0 errors, 0 warnings (our grep counted 2, both are the module name `Cache.Warning`), 15:43, 23.3 GB |
| P5a | Comparator 3/3, exit 0 | pass: Nanoda and the Lean kernel accept, exit 0, 9:56. The `sorry` warnings come only from `Challenge.lean`, as intended |
| P5b | exactly the six permitted axioms | pass: propext, Quot.sound, Classical.choice, kloosterman2_correlation_bound, kloosterman3_bound, physical_integral_bounds |
| P6 | stock python-flint 0.9.0 fails at index 15 | pass (fails at index 15, degree_got 30) |
| P8 | FLINT 3.6.0 + 7ad753d passes | pass, after deviation D1 (below) |
| P9 | passed: true, margin ≈ 2.336e-5, identical to DEBRIEF receipt, 40–90 min | passed: true, margin 69162467338708766984467/2960664736250000000000000000 ≈ 2.33605e-5, **identical** to `cycle6/prime_gap_186_fresh.json` in every field except `elapsed_seconds`. **Wall time missed the prediction: 2:09:50** (user 30 875 s, peak RSS 9.3 GB). The host was running other heavy exact-arithmetic jobs at the same time, so this says nothing about the certificate |

## Deviations

- D1: the first C8 attempt failed because building python-flint from source needs `python3-dev`, which our provisioning
  had not installed. We installed it and rebuilt python-flint 0.9.0 against the same FLINT 3.6.0 + 7ad753d build. No
  other change.
- The Mac-side `orb` client that followed the run was stopped by the host during C9 (memory pressure from other jobs). The
  VM process was not affected: exit status 0, signals delivered 0, so `progress.log` lacks the END line for C9 and
  there is no `C9_certificate.rc`; the exit status is from `/usr/bin/time -v`.

## Files

`progress.log`, `environment.txt`, `S*/C*.{log,rc,time}`, `C9_certificate.log`, `prime_gap_186_fresh.json`,
`PREREG.md`, `run.sh`, `run_cont.sh`. Home paths in logs are `/home/pruzze/...`.
