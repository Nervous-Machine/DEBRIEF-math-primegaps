# Independent reruns of openai/PrimeGaps186 at commit 61340d0

One row per party. "Build" is C4, "Comparator" is C5 (statements matched, Nanoda, Lean kernel, exactly six axioms),
"Certificate" is C9 on FLINT 3.6.0 + 7ad753d. Report what you saw, including failures.

| date | party | machine | build | comparator | certificate (wall, margin) | record |
|---|---|---|---|---|---|---|
| 2026-11-07 | Nervous Machine | Ubuntu VM, aarch64, 20 cores, 98 GB, on Apple silicon | pass, 9:32.68, 28.5 GB, 0 warnings | pass, 6:38, six axioms | pass, 1:03:48, 4 workers, 2.336e-5 ≥ 2e-5 | `cycle6/results_cycle6.json` |

## Adding a row

1. Follow `REPRODUCE.md`. Keep every log. Record wall time, peak memory, exit codes, tool versions and commits.
2. Write down what you expect before each step, if you want your row to carry the same weight as ours. It is not
   required.
3. Open an issue titled `Rerun: <machine>` with your results JSON and the receipt, or send a pull request that adds a
   row here and a directory `reruns/<date>-<party>/` with your logs. Paths with usernames can be replaced; say so.
4. If a step fails, that is the result. Put it in the row.

Most useful next: an x86-64 machine, and any machine with a different Lean or FLINT build path (for example, a
distribution FLINT package once a release contains PR 2790).
