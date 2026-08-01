# Session handoff — Session 179

**Turn type:** UI-only (E27 shipped). `index.html` v6.13 → v6.14, `rules_assertions.py` +1
assertion, `pipeline_manifest.json` reissued. No data or engine-legality work.

## 1. Session open

- Baseline green with `--fetch`: **25/25 gates** (3 tier-B skipped, correct — UI turn, no
  `--data-turn`), 75/75 tier-A assertions. Repo matched the project area on all 131 guarded files —
  no staleness gap, no reconciliation needed.
- D269 confirmed via the local (fetch-verified) decision log before starting — all session-prompt
  claims about E26's shape matched the actual text.

## 2. What shipped (D270)

**`renderDetail`'s attach-panel section** (the "Leader Assignment" block) and **`leaderSectionHtml`'s
datasheet-modal section** both rewritten to read `leaderAbilityName` / `leader_ability_name` (Leader
or Support) instead of a hardcoded "Leader" string:

- The detail-panel heading is now `${abilityWord} Assignment`; the no-eligible-bodyguard hint now
  names the ability word too.
- The modal section heading (`leaderSectionHtml`) now derives from each entry's `abilityName`,
  captured off `mg.leader_ability_name`; a unit whose model groups disagree (verified none do,
  across all 131 model groups carrying a non-null value) falls back to "Leader" defensively.

**Two of the ticket's three named candidate sites investigated and found to need no change** — this
is a real finding, not a skip:
- The list-panel attached-unit row prints `${leader.unit_name} (${entry.unit_name})` — no role word
  anywhere.
- The JSON save/export schema (`serializeEntries` / `buildRecord`) carries no role field —
  `attached_to` is a listId reference only.

**Left deliberately untouched, and why it matters:** both modal builders' Rules-section dedup filter
checks the literal string `'Leader'` against each model group's `rule_names`, to avoid re-printing the
ability under the generic Rules list after it's already shown in the dedicated section. That filter
had to stay keyed on the literal string. Checked every model group carrying a non-null
`leader_ability_name` (131 total): the datasheet's own printed ability box is *always* literally
"Leader" (129 of 131 — the remaining 2, both Masters of the Maelstrom model groups, carry a bespoke
named ability with neither word), and the literal string "Support" appears **zero** times in any built
`rule_names` array. `leader_ability_name`'s Leader/Support split is sourced from the Munitorum Field
Manual's own LEADER/SUPPORT block headers (`mfm_points_parser.py`) — a real, official GW distinction,
but from a different document than the datasheet card. Confirmed via web search that 40k's core rules
print one ability named "Leader," with no separate "Support" ability text anywhere. Switching the
Rules-section filter to key on `leader_ability_name` instead would have double-printed the ability for
every Support-classified unit except MotM.

**Assertion E27 added** — structural shape only (no legality logic changed, so no behavioural cases
like E26's): confirms both the attach-panel heading/hint and the modal heading actually read the
ability-name field, and that the old hardcoded strings are gone, not merely shadowed by the new ones.

**76/76 tier-A assertions pass (113 total including 37 tier-B skipped).**

## 3. Decisions still waiting on Ryan

- **B70 (Wardens of Ultramar)** — unchanged. Not touched this session.

## 4. Process notes (not decisions, findings for the next tooling turn)

**`BACKLOG_ARCHIVE.md`** (repo-only) is missing full-history entries for **B73 (S176)** and **E26
(S178)** — the archive's most recent entry before this session was B76 (S174). E27's own entry was
appended this session (routine, since it's this session's own shipped ticket), but the B73/E26
backfill was left alone rather than done here, since backfilling two other sessions' archive entries
isn't part of E27's UI-only scope.

**`pipeline_manifest.py`'s `GUARDED` list has not been updated for the last three handoffs** —
`SESSION_HANDOFF_177.md`, `178.md`, and now `179.md` are absent from the hardcoded per-filename list
(it currently ends at `176.md`). This is the same failure class D256/B81 were built to catch: because
`--write` only records files named in `GUARDED`, none of these three handoffs have ever been covered
by the manifest's hash guard — not by `--freshness-check`, and not by the plain `pipeline_manifest.py`
gate baseline.sh runs every session. `--freshness-check` at the close of this session correctly fails
with `SESSION_HANDOFF_179.md not in pipeline_manifest.json`, and it will keep failing every session
until the list is caught up. Nothing else is at risk — this session's decision log and handoff are
genuinely the final committed text, this is a coverage gap, not a detected drift — but it is worth
fixing before it becomes a fourth or fifth silent gap. Root cause is the list's design: it requires a
literal per-filename addition every session, exactly the kind of written-checklist maintenance this
project has already been burned by twice per D251's own history. Recommend S180 be a short
tooling-only turn: back-add `177`/`178`/`179` to `GUARDED`, and consider replacing the static
per-filename list with the same `latest_handoff()` pattern the check already uses, so a future session
can't silently drop off the list again. E23's scoping turn (next in priority) can follow immediately
after in the same or a subsequent session.

## 5. Files

| File | Status | SHA-256 (first 12) |
|---|---|---|
| `index.html` | v6.13 → v6.14 (E27 UI) | `f90c1c474b54` |
| `rules_assertions.py` | +1 assertion (E27), +1 function (`e27_leader_support_wording`) | `dc969525d086` |
| `pipeline_manifest.json` | reissued at close (131 guarded files) | `8bbb3a561904` |
| `40K_Decision_Log.md` | D270 appended | `5c0e3716febf` |
| `DECISION_INDEX.md` | D270 index entry added | `931b02816f28` |
| `OPEN_ITEMS_BACKLOG.md` | E27 → Closed/Shipped; count 12 → 11 | `cc79da71cb5d` |
| `BACKLOG_ARCHIVE.md` | E27 full entry appended (repo-only; delivered for Ryan to push) | `012c2c1935ff` |
| `NEXT_SESSION_PROMPT.md` | overwritten (S180) | `cd0e36928269` |
| `SESSION_HANDOFF_179.md` | new (rolling) | — |

No GW-derived material in this set — all files are project docs and engine code. No data file changed.

## 6. Backlog

- **Beginning:** 12 open — B69, B70, B75, B85, B86, P2, P4, E23, B67b, E12, B17, E27
- **Resolved:** E27
- **Added:** none
- **Ending:** 11 open — B69, B70, B75, B85, B86, P2, P4, E23, B67b, E12, B17
