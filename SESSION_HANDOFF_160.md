# Session handoff — Session 160

**Type: data-only.** Thousand Sons turn C (detachments) shipped and banked. No engine change —
`index.html` untouched. Decisions recorded: **D248, D249.** Baseline closed **24/24**, assertions **109/109**.

---

## 1. Baseline-open reconciliation: a manifest custody gap spanning S158–S159 (D249)

`baseline.sh --fetch --data-turn` failed at open: `pipeline_manifest.json` carried stale hashes for
`40K_Decision_Log_v3_0.md` and `OPEN_ITEMS_BACKLOG.md` (both edited in S159's D243–D247, but `--write`
was never re-run against that content before the push), and `pipeline_manifest.py`'s `GUARDED` list had
not been extended past `SESSION_HANDOFF_157.md` — S158 and S159 both skipped the append-only step the
file's own docstring requires. This blocked the fetch-overlay from pulling in 36 repo-only files.

Reconciled, not worked around: appended `SESSION_HANDOFF_158.md`/`159.md` to `GUARDED`, regenerated
`pipeline_manifest.json` against verified current content (checked against the fetched repo tarball, not
assumed), reran the full baseline clean. Worth a periodic check: this is the second manifest-staleness
finding in two sessions (S159 found the repo-push gap, S160 found the guarded-list/hash gap) — both times
because `--write` and the `GUARDED` append were skipped at a prior close.

## 2. Thousand Sons has nine detachments, not seven (D248)

D245 (S159) said seven, "established from source." That was a regression: `THOUSAND_SONS_BUILD_SCOPE.md`
(S158, D241) had already worked out **9** correctly by diffing the MFM against Wahapedia — 3 MFM-only
(new in 11th Ed: Ritual of Regeneration, Sekhetar Cohort, Servants of Change), 3 Wahapedia-only (Boarding
Actions-only, dropped: Chosen Cabal, Devoted Thralls, Fateseekers), 6 in both. D245 re-derived from the
faction pack's page-1 contents list and page-9 errata alone, without checking the scope doc that had
already done this correctly, and missed Sekhetar Cohort and Servants of Change. Re-confirmed at S160 open
directly against `MFM_Thousand_Sons_v1_0.txt`: both missing detachments carry real DP costs and priced
enhancements there, and full Detachment Rules/Enhancements/Stratagems text on clean, non-SUSPECT pack pages.

**Better than D241 anticipated:** the scope doc expected the 3 MFM-only detachments to render prose-less
(no Wahapedia coverage, same shape as CSM's 2). They didn't need to — pages 2–4 of the pack are clean and
fully parseable. A new `parse_ts_pack()` (detachment_parser.py §3b-2) extracts them, reusing the Dark
Angels pack's `_da_consume` state machine unchanged; only new logic is an explicit page→detachment map
(this pack's stylized banner titles defeat DA's leading-heading auto-detect) and a line-splitter for this
pack's combined name+CP stratagem headers (`"RELENTLESS REBIRTH 1CP"` on one line, not two). All nine TS
detachments now carry real rule text — zero fall to `text_source: none`.

Verified: `detachments_repro_check.py` byte-identical; correct DP/disposition/unique_tag for all nine from
the MFM; the three pack-sourced ones' rule name, full rule text, both enhancement descriptions and all
three stratagems each checked by eye against the source pages. Two new assertions pin this: **TS-1**
(detachment count == 9) and **TS-2** (no TS detachment carries `text_source: none`).

## 3. Established from source: the Scintillating Legions allied unlock belongs to Changehost of Deceit (D248/E24)

Not a guess. Wahapedia's `Detachment_abilities.csv` ability `Infernal Pacts` (id `000010196`) is keyed
directly to detachment id `000001062` — Changehost of Deceit. Its text and points caps (500/1000/1500,
no-Warlord restriction) mirror Death Guard's Plague Legions clause under Tallyband Summoners exactly.
Shipped in `detachment_effects.json` as an `unlock` + `warlord(cannot_be)` pair, both `enforced: false`
with `unenforced_reason` recorded — turn A (which tags the six carrier units with `allied_group` on their
TS-priced `units.json` records) hasn't shipped, so nothing is reachable through the effect yet, same
reasoning as `Chaos Daemons|SHADOW LEGION`. `e21a_allied_targets`'s hardcoded expected-unenforced list is
extended to include both new keys.

## 4. B78 and B79 corrected while scoping the remaining turn-A work (D248)

Both were filed S159 assuming the underlying engine mechanism didn't exist. It does, in both cases:

- **B79 (tag exclusivity) is CLOSED.** `index.html`'s `uniqueTagConflicts()`/`canAddDetachment()` already
  read `unique_tag` straight off `detachments.json` and refuse a second same-tag detachment — shipped and
  tested (Blood Angels GRACE) before Thousand Sons existed. Death Guard's ENGINES/FLYBLOWN and CSM's
  NIGHTMARE tags were already enforced the same way. The moment turn C banked `detachments.json`,
  `SERVANTS OF CHANGE` and `WARPMELD PACT` (found this session — Wahapedia's rule text, not the pack,
  carries Warpmeld Pact's Battleline/MUTANT clause) both carry `unique_tag: "MUTANT"`, and the engine
  already refuses selecting both. Full history appended to `BACKLOG_ARCHIVE.md`.
- **B78 (Battleline grant) stays open, updated, blocked on turn A.** The `battleline` effect kind,
  `detachmentBattlelineNames()` and `effectiveUnitType()` are shipped and already elevate four units
  elsewhere (D204 ruling 2) — this needs two data rows, not new code. But it's **two** detachments needing
  one, not the one ticket named: `SERVANTS OF CHANGE` and `WARPMELD PACT`. Neither row can be added yet —
  `e21b_check.js`'s battleline sweep resolves every named unit against `units.json` unconditionally
  (`enforced` isn't checked), and no Tzaangor unit exists there until turn A. `rules_assertions.py`'s
  `e21a_coverage` (E21a-5) carries a small, self-checking `known_gap` allowlist naming exactly these two
  keys so the coverage gate passes without going silent; it fails loudly if the allowlist goes stale.

## 5. What was deliberately not attempted

The B61 census assertions (`b61_plague_legions_census` and its three siblings) were left untouched.
`NEXT_SESSION_PROMPT.md`'s turn-C scope item 3 listed extending them this session, but D245's own "what
turn A actually needs" framing is the accurate one — there is nothing to extend until turn A creates the
six TS-priced carrier records with `allied_group` set. `b61_no_other_army_carries_allied_group` correctly
asserts Death Guard is the only army carrying the field today; extending it now would assert units that
don't exist. This is turn A's work, not turn C's.

---

## 6. Files

| File | SHA-256 (first 12) | Status |
|---|---|---|
| `detachment_parser.py` | `75929a7fe4af` | updated — TS wiring + `parse_ts_pack()` (§3b-2) |
| `detachments.json` | `de9c4522e0ce` | updated — 160 → 169 detachments, 9 Thousand Sons |
| `detachment_effects.json` | `616dbaf0a137` | updated — Changehost of Deceit unlock+warlord (enforced:false) |
| `detachments_repro_check.py` | `94bb9f2f2238` | updated — TS inputs added to `REQUIRED` |
| `rules_assertions.py` | `3e3ccd244a31` | updated — E21a-4/E21a-5 extended, TS-1/TS-2 added |
| `pipeline_manifest.py` | `0b29a9b24278` | updated — GUARDED list extended (S158/159 handoffs) |
| `pipeline_manifest.json` | `e8d696c5e02f` | regenerated — 111 guarded files |
| `40K_Decision_Log_v3_0.md` | `dbb952354ae2` | updated (D248, D249) |
| `OPEN_ITEMS_BACKLOG.md` | `25f85e904aa6` | updated (B79 closed, B78/E24 updated) |
| `BACKLOG_ARCHIVE.md` | `3b0dda805f1d` | updated — B79 full history appended |
| `SESSION_HANDOFF_160.md` | (self) | new (rolling) |
| `NEXT_SESSION_PROMPT.md` | see next file | overwritten (S161) |

**Ryan cannot download from the project Files panel** (S159 finding, still true). All ten changed files
above are re-delivered as outputs this turn for repo push.

## 7. Backlog

- **Beginning:** 18 open — B69, B70, B71, B72, B73, B75, B76, B77, B78, B79, E24, P2, P4, B80, E23, B67b, E12, B17
- **Resolved:** 1 — B79 (premise was wrong; mechanism already shipped and generic)
- **Added:** 0
- **Ending:** 17 open — B69, B70, B71, B72, B73, B75, B76, B77, B78, E24, P2, P4, B80, E23, B67b, E12, B17
