# Next-session prompt — Session 180

**Assigned: tooling-only — close the `pipeline_manifest.py` `GUARDED`-list gap on the last three
session handoffs.** Found at S179 close: `SESSION_HANDOFF_177.md`, `178.md`, and `179.md` are all
absent from the hardcoded `GUARDED` list (it currently ends at `176.md`), so none of the three has
ever been covered by the manifest hash guard — not by the plain `pipeline_manifest.py` gate baseline.sh
runs every session, and not by `--freshness-check`. This is the same failure class D256/B81 were built
to catch. **11 open items — this fix is not itself a backlog ticket, just close-out debt; do not open
one for it, just fix it.**

## Open at session start

Read `SESSION_HANDOFF_179.md` first (section 4 has the full finding), then `40K_Decision_Log.md` D270.
Do not trust any session/version/decision number from memory.

Run the full baseline: `./baseline.sh --fetch`. Expect the plain `pipeline_manifest.py` gate to pass
(it only checks files actually in `GUARDED`) but `--freshness-check` to fail on `SESSION_HANDOFF_179.md`
— that is the known, already-diagnosed problem this session fixes, not a new gate failure to reconcile
before starting.

## The fix

1. Add `'SESSION_HANDOFF_177.md'`, `'SESSION_HANDOFF_178.md'`, and `'SESSION_HANDOFF_179.md'` to
   `GUARDED` in `pipeline_manifest.py`.
2. Consider replacing the static per-filename list for session handoffs with the same
   `latest_handoff()` discovery pattern `freshness_check` already uses (highest-numbered
   `SESSION_HANDOFF_*.md` present), so `GUARDED` can't silently fall behind again — dev-manager's call
   on whether that refactor is worth it now or whether re-adding the three names and moving on is
   enough for this turn. If deferred, say so explicitly and file it rather than letting it recur
   silently a fourth time.
3. Run `python3 pipeline_manifest.py --write`, then `python3 pipeline_manifest.py --freshness-check`
   to confirm it passes clean with `SESSION_HANDOFF_180.md` once that's written.
4. `BACKLOG_ARCHIVE.md` (repo-only) is also missing full entries for B73 (S176) and E26 (S178) — if
   time allows in this same tooling turn, backfill them from `40K_Decision_Log.md` D267/D269 and the
   old Open-Items ticket bodies (already in git history via the handoffs); otherwise leave noted for a
   later tooling pass.

## After this

**E23 — `HEADHUNTER TASK FORCE` Tank Ace Character keyword grant, scoping turn (analysis-only).**
Ticket text (`OPEN_ITEMS_BACKLOG.md`, filed S134/D209): `HEADHUNTER TASK FORCE` exists in six built
armies (Space Marines, Black Templars, Blood Angels, Dark Angels, Deathwatch, Space Wolves) and grants
the Vehicle keyword Tank Ace to most Adeptus Astartes Vehicles, then in the Muster Armies step lets the
player select up to three Tank Ace units to gain the Character keyword — making them Enhancement- and
Warlord-eligible. `index.html` currently gates both on `unit_type === 'Character'` and refuses
everything else, an over-restriction (refuses something legal), not a D0 violation, on up to three
vehicles per list. Needs GW sources loaded (`--data-turn`) to confirm the keyword text across all six
armies, a decision on where the per-list selection lives in the list record (player state, must
survive save/load), and a decision on mechanism (sixth `detachment_effects.json` effect kind vs. its
own mechanism) — it touches E4's enhancement eligibility and E9's Warlord eligibility.

Other candidates after that, by priority:
- **B69** (select-N ability pools) — needs a data + engine arc, M-sized.
- **B70** (Wardens of Ultramar join mechanic) — still waiting on Ryan's MFM-vs-datasheet reconcile.
- **B75/B85** — blocked on real PDF access from Ryan.
- Remaining faction builds per the priority order.

## Close protocol

Produce the four documents: `SESSION_HANDOFF_180.md`, overwrite `NEXT_SESSION_PROMPT.md`, append the
decision log + `DECISION_INDEX.md` (a short D271 covering the GUARDED fix is enough — no ticket to move
in the backlog since this was never a ticket), update `OPEN_ITEMS_BACKLOG.md` only if the archive
backfill happened. Every changed and net-new file carries a SHA-256 (first 12) in the handoff Files
section. Reissue `pipeline_manifest.json` at close — this session's whole point is making that reissue
trustworthy again. Repo is public and flat — no GW-derived material committed; state the exclusions
when listing files for the repo.
