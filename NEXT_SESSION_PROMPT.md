# Next-session prompt — Session 150

Session 149 built and proved M0 (D232) — the new fetch-open, tiered gates, `source_manifest.json`,
and the token custody guard. Nothing was evicted. Read `SESSION_HANDOFF_149.md` and `D232_entry.md`
before starting.

## Step 1 — confirm M0 for real, at open

S149's exit test proved the mechanism correct by simulation but could not get a literal green
`--fetch` run, because the real public repo hadn't received S149's push yet. That push should have
landed by now. Open with:

    ./baseline.sh --fetch --no-repo

Expect `fetch-verify` to PASS this time (101/101 guarded files match) — if it still reports files
missing from the manifest, the push didn't land as expected; stop and reconcile before doing anything
else, don't route around it. `repo_check.py` is skipped by `--no-repo` here deliberately — check it
separately once M1 has run (see Step 2), since right now it would still show S149's now-pushed files
as "differs" against whatever Ryan's git history looks like mid-push.

Verify carried-forward hashes match S149's handoff: units.json `eb370386ccf7`, abilities.json
`051bdd9ceb08`, rules.json `b347222a3bc9`, weapon_abilities.json `ff4379837df4`,
datasheet_wargear_abilities.json `af5be2824e54`, units_repro_check.py `81cb0f825727`.

## Step 2 — M1, if not already done

M1 is Ryan's task, not a session (~10 minutes, screenshot-verified per the amendment D231/D232
settled). If the area is still near 100% capacity, M1 hasn't happened yet — ask Ryan to run it
before this session does substantive work, rather than opening a data/engine turn against a
capacity-constrained area. If the area is already slim (~450 KB), M1 is done; open on the new
`--fetch` path as the default going forward and confirm `repo_check.py` comes back clean too.

## Step 3 — B68 (engine turn)

Per D231's migration sequence, B68 is next: `loadout_parser.py`/`equipped_parser.py` resolve by unit
name, not army+unit_id, so Death Guard and Chaos Space Marines' seven shared generic Chaos vehicle
names bleed across factions. Full detail in `OPEN_ITEMS_BACKLOG.md`'s B68 entry and D230. This is an
engine/parser turn — per turn typing, it must not mix with any data change. Fix: rekey the relevant
lookup(s) to (army, unit name) or unit_id outright; re-run the full production chain; diff-trace
against the currently-committed `unit_loadouts.json` to confirm the only changes are the seven known
unit_ids resolving correctly, nothing else drifting.

**Do not start CSM turn B** (the M2 dress rehearsal) until B68 is closed — it's the next item in the
same sequence, not this session's work unless B68 finishes with room to spare.

## Turn type

**Engine-only** (B68), once Steps 1–2 confirm M0/M1 are genuinely settled. If M1 hasn't happened yet,
this session's real job is coordinating that with Ryan, not B68 — don't force an engine turn onto a
still-capacity-constrained area.
