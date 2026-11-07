# DEBRIEF ledger — schema v1 (draft, 2026-10-07)

The debrief agent speaks from this ledger and from nothing else. One database (`nm_debrief`), seven collections.
Edge vectors stay where they are (`nm.edges`); the ledger points at them and does not copy them.

Conventions follow `nm-graph-v1`: every document carries `mission_id`, `pod`, `schema_version: "nm-debrief-v1"`,
`created_by`, `created_at`, and a `provenance` object. Text meant to be said aloud lives in a field called `spoken`
(plain prose, no symbols). Anything not in the ledger does not get said.

## Collections

| collection | one document is | the agent uses it for |
|---|---|---|
| `missions` | a mission (a domain worked over a period) | the opening, the short version, scope limits, record quality |
| `cycles` | one learning cycle: what was written down first, what happened | recounting the mission in order; "the reasoning" |
| `findings` | one thing learned, retracted, ruled out or discovered | "what was learned"; "what it changes" |
| `gaps` | one open or closed unknown, with its history and what would close it | "what was escalated", "what gaps still exist", "what needs your attention" |
| `anomalies` | one event that disagreed with a trusted expectation | outstanding anomalies; immediate alerts |
| `background` | one concept explained, kept apart from results | teaching ("what is a Forbush decrease?") |
| `sessions` | one debrief call: who, what was asked, what the team proposed | follow-ups; what the team does not yet understand; ideas to test |

## Fields

**missions** — `mission_id`, `title`, `pods[]`, `began`, `status` (active | closed), `record_quality`
(`full_ledger` | `reconstructed`) with `record_note`, `scope_limits[]`, `opening.spoken`, `short_version.spoken`,
`what_happened.spoken`, `implications` {`rely_on[]`, `do_not_rely_on[]`, `stop[]`, `new[]`, each {`spoken`,
`finding_ids[]`}}, `certainty_statement.spoken`, `sources[]` {`kind`, `ref`}.

**cycles** — `cycle` (number or label), `dated`, `preregistered` {`question`, `rule`, `predictions[]`, `commit`,
`before_data` (true | false | unknown)}, `outcome` {`verdict`, `numbers{}`}, `spoken`, `finding_ids[]`, `gap_ids[]`.
`verdict` is one of: `admitted`, `not_admitted`, `confirmed`, `refuted`, `unavailable`, `corrected`,
`withdrawn`, `classified`, `learned`, `mixed`.

**findings** — `finding_id`, `kind` (`learned` | `retracted` | `ruled_out` | `discovery` | `correction`),
`spoken`, `evidence` {`numbers{}`, `cycles[]`, `confirmed_by[]`}, `standing` {`status`, `basis`, `note`},
`certainty` {`earned`: true | false | null, `note`}, `edge_refs[]` {`pod`, `edge_id`}.

`standing.status` is the outcome of the hypothesis test (Heidi, 2026-10-07): what was tried, what was refuted,
what earned structure and sign. A finding is a tested hypothesis; a count or a measurement is not a finding (it
lives in `what_happened` or in an anomaly's evidence). Record completeness is a property of the mission
(`record_quality`), not of the standing.

| status | means |
|---|---|
| `accepted` | the hypothesis passed its test and made it into the prior with a sign, but has not properly earned certainty (clamp, structural limits, sparse event data — reasons still being worked out). |
| `certified` | accepted, **and** certainty (Z) was earned under a settled rule. Requires `certainty.earned: true`. |
| `refuted` | the hypothesis did not stand. |

`basis` says how it was accepted or refuted, in words the agent can say aloud.

### Audit missions (added 2026-11-07; first used by `prime-gaps-186-2026-11`)

A mission can also keep score of a claim made by someone else, with no learning kernel and no Z. The same three
statuses apply, read against the mission's pre-registration (for example `primegaps/prereg.yaml`) instead of the
kernel's certainty rule:

| status | means in an audit mission |
|---|---|
| `certified` | a deterministic check Nervous Machine ran under a rule written down first, or a formal check rerun by a party independent of the authors. `certainty.earned: true` here records that the check is deterministic and reproducible; it is not a Z value. |
| `accepted` | a published, refereed theorem; a formal check reported by the authors' own toolchain; or a step inside a formally checked deduction. `basis` must say which of these it is. |
| `refuted` | a counterexample, a failed check, or a published objection the authors have not answered. |

An input nobody independent has checked is not a finding with a standing; it is a gap, with `closes_with` naming
what would settle it. The knowledge base's standing line reports open gaps next to the finding counts, so
"Certified 1, Accepted 5, Refuted 0" cannot be read as six of six. Numeric spot checks corroborate a literature
input but never raise its standing. Anything a check transcribes from the claim (a tuple, a definition) is pinned
to a source commit and file hash in the mission's `provenance` and in the check's results; the check fails if the
pinned source no longer matches the transcription. The pre-registration is not edited after the checks run;
later changes go in a dated amendment inside it.

**gaps** — `gap_id`, `title`, `spoken`, `status` (`proposed` | `in_cycle` | `resolved_learned` |
`resolved_refuted` | `immovable`), `opened_cycle`, `history[]` {`cycle`, `hypothesis`, `before_data`, `result`},
`closes_with[]` {`what`, `kind`: `data_release` | `measurement` | `research` | `decision` | `rerun`, `external`
(bool), `who_could_act`}, `ask.spoken`, `priority` (1 = first).

**anomalies** — `anomaly_id`, `when`, `node`, `spoken`, `status` (`open` | `explained` | `confirmed`), `urgency`
(`immediate` | `daily`), `from_trusted_node` (true | false | unknown), `evidence{}`, `gap_id`, `alert` {`sent`,
`channel`, `at`}.

**background** — `term`, `also_called[]`, `spoken` (the plain explanation), `source` (`general` | `literature`
with `citation`), `mission_tie.spoken` (what this mission saw; optional).

**sessions** — `session_id`, `at`, `audience`, `questions[]` {`text`, `answered_from[]` (ids) or
`"not_in_record"`}, `ideas[]` {`text`, `already_tried` (gap or cycle id, or null), `follow_up`}, `asks_accepted[]`.

**audience** (findings, gaps, cycles, and each implication) — `briefing` or `internal`. Internal means how the
framework works or the state of the record: how certainty is scored, controls on the learning rule, lost or
recovered files. The mission document keeps `record_note`, `record_limits[]`, `certainty_statement` and
`internal_prose[]` (passages marked `[[internal: ...]]` in the source prose) for the same purpose. The agent's
knowledge base is rendered from briefing items only; internal items go to `debrief/internal/`, which the agent is
not given (Heidi, 2026-10-08: a briefing is about what was found; framework problems get fixed, not briefed).

## Rules the ledger enforces

1. A finding names the cycles it came from, or says the cycle record is not available.
2. Every finding has a standing with a basis, and certainty is recorded separately. `certified` is not allowed
   unless certainty was earned.
3. A gap is not `immovable` unless `closes_with` names something outside the campaign's reach.
4. Background never carries a result; a result never lives in background.
5. An anomaly alerts immediately only if `from_trusted_node` is true.
6. Nothing is deleted. A correction is a new finding of kind `correction` that names what it replaces.
7. Leaving something out of the briefing is done by marking it `internal`, never by removing it from the ledger.

## A third mission (for example an enterprise agent audit) has to supply

A mission document; at least one cycle with something written down before it was scored; findings with their
standing and basis; gaps with what would close each one; and background for any term its team may not know.
Where there is no outcome to check against, that is a gap, with `closes_with.kind: measurement`.
