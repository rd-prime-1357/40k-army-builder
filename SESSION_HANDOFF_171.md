# Session handoff — Session 171

**Type: audit-only** (no `index.html` change, no parser change, no data change). Decision recorded:
**D261.** B77 audited and closed as already-resolved — its S159 diagnosis no longer matches the data.

---

## 1. Baseline at session open

`./baseline.sh --fetch --data-turn` ran clean: 29/29 gates pass, sources loaded. No reconciliation
needed at open. Assertion count is 110/110 (the S170 handoff's own count was accurate; a stale figure
of 75/75 had been circulating in earlier chat context and should not be trusted going forward — always
read the live baseline output, not a remembered number).

## 2. Why this was an audit, not a build

S170's next-session prompt named B77 as the one pick that didn't need Ryan first — a small, self-
contained parser fix. Before starting the fix, the ticket's own claim (six carrier units have an empty
keyword list, `keywords.json` has zero hits) was checked against the current committed `units.json`
rather than taken on faith, per standing practice. It was false. Building the "fix" would have been
redundant work against a problem that no longer exists.

## 3. Finding (D261)

All six Scintillating Legions carriers (Kairos Fateweaver, Lord of Change, Flamers, Screamers, Pink
Horrors, Blue Horrors) already carry `"Scintillating Legions"` in `model_groups[].faction_keyword_names`.
That field is sourced directly from Wahapedia's `Datasheets_keywords.csv` via `convert_to_json.py` — real
source data, not something synthesized from `allied_group`. `index.html` already renders it as a
`Faction: Scintillating Legions` pill, the same code path used for every other faction keyword (e.g.
`Adeptus Astartes`).

`keywords.json` genuinely has no `Scintillating Legions` entry, but that's correct, not a gap: that file
is a tooltip-description glossary for plain `keyword_names` (Fly, Infantry, etc.). Faction keywords render
as a plain `Faction: X` line with no lookup against `keywords.json` at all — confirmed directly in
`index.html`'s keyword-rendering block.

All actual list-building legality already runs off `allied_group` (the offer filter and Warlord ban
shipped under B61/E22b — D208, D214, D245, D248), which this audit did not touch. The ticket's underlying
concern — TS Rituals/stratagems that target "THOUSAND SONS or SCINTILLATING LEGIONS" units — is in-game
ability targeting, not list-construction legality, and was never something the tool needed to resolve at
muster time.

**Closed on standing authority.** This is a data-verification finding, not a product or rules-legality
call, so it was closed without waiting on Ryan, per the project's own routing rule (only "how it works"
questions reach Ryan). Recorded for the record in D261 and the backlog rather than surfaced as a
question.

## 4. B70 and B73 — unchanged, still blocked on Ryan

Not touched this session. Same two decisions from S170 remain open — see D260 and the prior next-session
prompt. Nothing new to add; re-derivation is done, only the scope call is outstanding.

## 5. Decisions needed (Ryan)

1. **B70 (Wardens of Ultramar)** — close as not-a-bug, or scope the "join another unit" mechanic as new
   M/L work? Recommendation: close, unless Wardens-as-originally-imagined is specifically wanted.
2. **B73 (Leader lists carry out-of-chapter units)** — MFM's `LEADER` list authoritative wherever both
   exist (recommended), or does Ryan trust Wahapedia's broader list instead? Roster-wide, precedent-
   setting — held for Ryan per S170's own routing.

Nothing new needs Ryan from this session; B77 was resolved without a question reaching him.

## 6. What's next

11 open, down from 12: B69, B70, B73, B75, B76, P2, P4, E23, B67b, E12, B17. B70/B73 still blocked on
Ryan's two decisions above. Next viable pick without waiting on Ryan: **B76** (rolling-doc filename
cleanup — small, low-risk, tooling-only). B75 stays blocked on Ryan's flag-count report. B69 stays
blocked on Ryan's six-vs-one scope choice (D259).

**P4 note:** Ryan confirmed project-area capacity at 79% full this session (previously last reported at
S166/167, unconfirmed since). Still watch-not-blocking per D231/D232's M2 sequencing, but worth carrying
forward without needing to ask again next time.

## 7. Files

| File | SHA-256 (first 12) | Status |
|---|---|---|
| `40K_Decision_Log_v3_0.md` | (see manifest) | updated (D261) |
| `DECISION_INDEX.md` | (see manifest) | updated — D261 one-liner |
| `OPEN_ITEMS_BACKLOG.md` | (see manifest) | updated — B77 moved to Closed/Shipped; open count 12 → 11 |
| `NEXT_SESSION_PROMPT.md` | (see manifest) | overwritten (S172) — not guarded, by design (D231) |
| `SESSION_HANDOFF_171.md` | (self) | new (rolling) |
| `pipeline_manifest.json` | (issued last — see §8) | regenerated, reflects the files this session changed |

**Net New Files:** none. This session touched only rolling documents (decision log, decision index,
backlog, handoff, next-session prompt) — no harness, parser, or data file was created. `index.html`,
`units.json`, and every pipeline script are byte-identical to S170.

**Ryan cannot download from the project Files panel** (S159 finding). All changed files are delivered
as outputs this turn for repo push and project-area upload.

## 8. Manifest reissued last, per D251's ordering rule — checked by `--freshness-check`

`pipeline_manifest.py --write` then `pipeline_manifest.py --freshness-check` are the literal last two
commands, after this handoff's text and D261's decision-log entry were finalized.

## 9. Backlog

- **Beginning:** 12 open — B69, B70, B73, B75, B76, B77, P2, P4, E23, B67b, E12, B17
- **Resolved:** 1 — B77 (closed, already-resolved, no build)
- **Added:** 0
- **Ending:** 11 open — B69, B70, B73, B75, B76, P2, P4, E23, B67b, E12, B17
