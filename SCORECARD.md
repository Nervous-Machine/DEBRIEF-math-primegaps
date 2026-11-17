# The claim that primes come within 186 of each other infinitely often

In early September, OpenAI posted a proof credited to its model GPT 6 Astra that infinitely many pairs of primes are at most one hundred and eighty six apart, beating the 2014 record of two hundred and forty six. The same week, Hanxin Zhang and Julia Stadlmann each reached two hundred and forty and Axiom Math announced two hundred and twelve by related routes, so the approach is credible. The logic of OpenAI's proof is fully machine-checked in Lean, but it rests on three inputs that were taken as given: two classical bounds on exponential sums, and one hundred and fifty two numerical bounds computed by a separate program. Nervous Machine checked what can be checked directly. The forty-number list is correct, and the two classical bounds hold with room to spare on every small prime tested. Nervous Machine then reran OpenAI's own checks: the Lean build, the Comparator match and both kernel checks all passed, and the numerical certificate ran to completion and passed on a publicly buildable library. What is still open is human: no number theorist has publicly confirmed the formal statements say what the paper claims, and the written proof has not been refereed. My read: conditionally supported, with the computation independently reproduced; not yet settled.

_Rendered from the briefing record. Items marked internal in the ledger (how the framework works, the state of the record) stay in `ledger.json` and are not shown here._

Record quality: reconstructed. Replayed from the public record, dated by first public posting; Nervous Machine's own checks were registered before they ran.

**Standing.** Certified 5. Accepted 5. Refuted 0. Open gaps 3. An open gap is an input or question nobody has settled; it is not a finding and has no standing.

## Findings

| id | kind | standing | basis | cycles |
|---|---|---|---|---|
| P1 | learned | **certified** | checked by direct computation under a rule written down first, on the tuple read from the pinned Lean source | 5, rerun-4 |
| P2 | learned | **certified** | formally checked by the authors' toolchain, and rerun by Nervous Machine on November seventh: the Lean build, Comparator, the Nanoda kernel and Lean's kernel all passed, with exactly the six permitted axioms | 3, 6, rerun-4 |
| P3 | learned | **accepted** | published, refereed results | 0, 3 |
| P4 | learned | **accepted** | standard results in the literature, supported by spot checks on small primes | 3, 5 |
| P5 | discovery | **accepted** | three independent groups, none refereed; Axiom's Lean certificate is described in its draft and is not public | 1, 2 |
| P7 | correction | **accepted** | dated public deposits | 1 |
| P6 | correction | **accepted** | the repository lists them | 3 |
| P10 | learned | **certified** | deterministic text comparison registered before it ran | 7 |
| P8 | correction | **certified** | deterministic checks registered before they ran | 6, rerun-4 |
| P9 | learned | **certified** | independent rerun of the certificate under a rule written first | 6, rerun-4 |

## Cycles, in order

| cycle | dated | by | kind | written first | verdict |
|---|---|---|---|---|---|
| 0 | 2014-2015 |  | replay | no | learned |
| 1 | 2026-08-28 to 2026-08-31 |  | replay | no | classified |
| 2 | 2026-09-03 |  | replay | no | classified |
| 3 | 2026-09-03 |  | replay | no | admitted |
| 4 | 2026-09-07 to 2026-11-05 |  | replay | no | unavailable |
| 5 | 2026-11-07 | Nervous Machine (Heidi Bennett; Claude Code as the operating agent) | rerun | yes | confirmed |
| 6 | 2026-11-07 | Nervous Machine (Heidi Bennett; Claude Code as the operating agent) | rerun | yes | confirmed |
| 7 | 2026-11-08 | Nervous Machine (Heidi Bennett; Claude Code as the operating agent) | trace | yes | confirmed |
| rerun-4 | 2026-11-14 | Fredrik Prüzelius (with Claude Code) | rerun | no | confirmed |
| external-2026-11-17 | 2026-11-17 | None | replay | no | admitted |

## Gaps, in the order that would settle things fastest

| priority | gap | status | closes with | who could act | signal expected | resolution by |
|---|---|---|---|---|---|---|
| 1 | The one hundred and fifty two numerical integral bounds | resolved learned | an independent rerun of the numerical certificate | any group: FLINT 3.6.0 plus public upstream fix 7ad753d, python-flint 0.9.0 built from source |  |  |
| 2 | Do the formal statements say what a mathematician means? | proposed | a number theorist reads the definitional trace against the formal file and the paper and signs its checklist | an independent number theorist | two read cycles, by named people who are not authors of the claim, each signing every item of the trace's checklist; one refusal reopens it | none registered |
| 3 | The two classical exponential-sum bounds are assumed in Lean | proposed | formalize the two bounds in Lean, or accept them as standard literature | the Lean community | either a Lean formalization of the two bounds accepted into the development, or a cited statement from the field that they are standard | none registered |
| 4 | No independent review of the written proof | proposed | referee or independent expert review of the paper | a journal or independent experts | a referee report, or a public account by an independent expert of having read the proof through | none registered |

## Corrections, retractions, ruled out

- **P7** (correction): An earlier draft of this briefing called Stadlmann's two hundred and forty the first improvement in more than a decade. Hanxin Zhang's two hundred and forty was deposited three days earlier, on August twenty eighth, with the discovery credited to an AI model. They are independent proofs of the same bound.
- **P6** (correction): Some descriptions say the proof rests on six assumptions. Three of those are the standard rules of Lean's logic that every Lean proof uses. The claim rests on three.
- **P8** (correction): Earlier this briefing said the numerical certificate needed a library build OpenAI had not published. The missing piece is public: one upstream fix to the FLINT library, merged in August and in no release yet. The stock library fails the certificate's own startup test; FLINT three point six with that one fix passes it.

_Generated by DEBRIEF tools/render.py from ledger.json; protocol 0.1.0._
