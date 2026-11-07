# Pinned source for checks C1-C3

`Challenge.lean` is a verbatim copy from github.com/openai/PrimeGaps186, default branch `main`,
commit `61340d0b74163003b32756bb16e91d9209a5e330` (committed 2026-09-02), fetched 2026-11-07.

sha256 `b99a403b1946547ef1926cd43ebce717640f7f76fa7e1f8f5a4b19ac2e53e1f0`

It holds the 40-element `admissibleTuple` and the three project axioms (`kloosterman3_bound`,
`kloosterman2_correlation_bound`, `physical_integral_bounds`) whose definitions C1-C3 transcribe. Its header says
the axiom and definition bodies are copied from `PrimeGaps186.lean`. `checks.py` reads the tuple from this file,
checks the hash, and fails if either differs from what was registered.

Licence: Apache-2.0 (copy in `LICENSE-openai-PrimeGaps186`). Not modified.
