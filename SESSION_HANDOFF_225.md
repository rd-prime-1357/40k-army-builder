# SESSION HANDOFF 225

**Turn type:** tooling-only (Drukhari loadouts — author the flagged wargear-option groups).
`unit_loadouts.json`, `wargear_points.json`, `repro_check.py`, `rules_assertions.py` changed.
`units.json`, `detachments.json`, `detachment_parser.py`, `index.html` untouched. Closes no
numbered backlog ticket — Drukhari's build is part of the standing faction-priority-order
sequence, not its own item. See D319.

## What happened

1. **Open-time baseline clean.** `./baseline.sh --fetch --data-turn`: 34/34 gates, 85 source
   files verified.

2. **§7's carried-forward numbers did not match live output — re-derived from the real pipeline
   before authoring anything, not trusted unchecked.** Ran `loadout_parser.py --factions ... DRU`
   + `equipped_parser.py --datasheets` for real (scratch dir first, then the actual regen). The
   real flagged set is 8 units, not 9, and only partially overlaps `DRUKHARI_BUILD_SCOPE.md` §7's
   named list:
   - 4 of §7's named units (Razorwing Jetfighter, Voidraven Bomber, Scourges with Heavy Weapons,
     Scourges with Shardcarbines) resolve automatically with zero authoring — same
     datasheets-gap-fill precedent as Grey Knights. §7's "13 groups / 9 units" figure
     over-counted these.
   - 3 units the real parser flags were absent from §7 entirely: Kabalite Warriors, Reavers,
     Cronos.
   - Of the real 8, only 4 needed `unit_loadouts.json` authoring. Kabalite Warriors, Reavers,
     Hellions, and Hand of the Archon each carry only an "equipped with one of the following:
     [non-weapon item]" line pointing at `units.json`'s own `other_options` (Kabalite
     Icon/Phantasm Grenade Launcher/Cluster Caltrops/Grav-talon). Confirmed by grep that
     `index.html` renders `other_options` directly, independent of `unit_loadouts.json` — same
     shape already shipped and left `UNMATCHED` for Incursor Squad's Haywire Mine (000001159).
     These stay `UNMATCHED`, correctly.

3. **4 units hand-authored: Wracks (000000650), Talos (000000663), Cronos (000000664), Ravager
   (000000665).** Added to `repro_check.py`'s `HAND_AUTHORED` and `DRU` added to `FACTIONS`.
   - Wracks: the auto-parser's own Acothyst swap was correct as-is; added (a) a second
     alternative in the same `choice` list for the conditional "if not equipped with a power
     weapon" line — verified verbatim against the official rule text via search, not a Wahapedia
     artifact — and (b) a 4-way "for every 5 models" compound special-weapon group scoped to the
     regular `Wracks` model group.
   - Talos: two "replace one of their macro-scalpels" groups authored as `count` type against
     the single shared `Macro-scalpel` weapon row, same shape as the unit's own auto-parsed
     Twin splinter cannon options.
   - Cronos: simple `add` for Spirit vortex, `max_total_all: true`.
   - Ravager: `count`-type replace of `Dark lance` → `Disintegrator cannon`, `max_total_all: true`
     (three physical dark lances share one profile row, same shape as Talos's macro-scalpels).

4. **Diff-guarded, not just "ran clean."** Full regen via the real pipeline (all 8 factions incl.
   `DRU`, 11-id hand-authored seed) reproduces the new committed `unit_loadouts.json`
   byte-for-byte (`repro_check.py` OK). Field-by-field diff against the pre-session file: +23
   keys (exactly Drukhari's 23 units), 0 removed, 0 existing units changed.

5. **`wargear_points.json` rebuilt via the canonical `mfm_points_parser.py --wargear MFM_*.txt`
   path.** Exactly the 4 forecasted Drukhari items populate: Ravager's Dark lance (+5), Scourges
   with Heavy Weapons' Haywire blaster (+5) and Dark lance (+5), Talos's Twin haywire blaster
   (+5). 0 removed, 0 unrelated changes — confirmed by key-level diff, not assumed.

6. **E14 literal updated in `rules_assertions.py`, verified by full per-army breakdown before
   changing the number.** The auto-parsed Voidraven Bomber `Voidraven missiles` add
   (max_total:1, unpriced) is a new qualifying free seed. Confirmed every non-DRU faction's count
   unchanged at 108/75 before updating the literal to 109/76.

7. **Full baseline re-run with all changes in place.** `repro_check`, `units_repro_check`,
   `detachments_repro_check` all byte-identical to committed; `rules_assertions` 121/122 (the one
   red is the expected P3 manifest-drift for the four edited files, cleared by `--write` below);
   every harness clean — zero regression to any already-built faction.

## Not investigated this session

B113, B114, GK §6/§7 untouched — different turn types, not mixed per the standing rule.
Detachments (§5, 9 detachments) and the deferred `detachment_parser.py` three-map registration
are the next Drukhari turn, per `DRUKHARI_BUILD_SCOPE.md` §8's sequencing — not started this
session.

## State at close

- `unit_loadouts.json`: +23 units (Drukhari). 19 auto-parsed, 4 hand-authored (Wracks, Talos,
  Cronos, Ravager). 0 existing units changed.
- `wargear_points.json`: +4 items, all Drukhari, purely additive.
- `repro_check.py`: `FACTIONS` now includes `DRU`; `HAND_AUTHORED` extended with the 4 new ids
  and an explanatory comment recording this session's re-derived findings.
- `rules_assertions.py`: E14 literal 108/75 → 109/76, with a dated comment.
- `units.json`, `detachments.json`, `detachment_parser.py`, `index.html`: untouched.
- `40K_Decision_Log.md`: D319 appended. `DECISION_INDEX.md`: D319 one-liner appended.
- `OPEN_ITEMS_BACKLOG.md`: ledger header updated to S225, count unchanged at 23 (no ticket
  closes or opens — Drukhari's loadouts build isn't a numbered backlog item).

## Ryan action required

1. **B108 — remove `Thousand_Sons_web.txt` from the public repo** (still outstanding, unchanged).
2. **Push `OUTPUT_FORMAT_SPEC_for_project_instructions.md` to the public repo** (still outstanding
   from S220).
3. **Push `pipeline_manifest.json`** — still outstanding from S223's open-time reconciliation.
4. Push this session's new/changed files to the public repo: `unit_loadouts.json`,
   `wargear_points.json`, `repro_check.py`, `rules_assertions.py`, `40K_Decision_Log.md`,
   `DECISION_INDEX.md`, `OPEN_ITEMS_BACKLOG.md`, `pipeline_manifest.py`/`.json`, this handoff,
   `NEXT_SESSION_PROMPT.md`. This adds to the same pending push queue as S223/S224's files —
   `repo_check.py` will keep showing `DIFFERS` findings until pushed; expected, not a new problem.

## Decisions waiting on Ryan

**B116** — unchanged (Drukhari's Harlequins/Anhrathe allied-inclusion mechanic; see
`DRUKHARI_BUILD_SCOPE.md` §6). Not touched this session.

## Files (SHA-256, first 12)

Verify these at S226 open.

| file | sha256:12 | note |
|------|-----------|------|
| `unit_loadouts.json` | (computed by `--write`) | +23 Drukhari units |
| `wargear_points.json` | (computed by `--write`) | +4 Drukhari items, additive |
| `repro_check.py` | (computed by `--write`) | DRU in FACTIONS, 4 ids added to HAND_AUTHORED |
| `rules_assertions.py` | (computed by `--write`) | E14 literal 108/75 → 109/76 |
| `40K_Decision_Log.md` | (computed by `--write`) | D319 appended |
| `DECISION_INDEX.md` | (computed by `--write`) | D319 one-liner appended |
| `OPEN_ITEMS_BACKLOG.md` | (computed by `--write`) | ledger header S225, count unchanged (23) |
| `pipeline_manifest.py` | (hash not self-referential) | `SESSION_HANDOFF_225.md` appended to GUARDED |
| `pipeline_manifest.json` | (hash not self-referential) | regenerated by `--write` at close |
| `NEXT_SESSION_PROMPT.md` | (informational only, never guarded) | S226 |
| `SESSION_HANDOFF_225.md` | (this file, hash not self-referential) | |

## Net New Files

None this session. `unit_loadouts.json` and `wargear_points.json` are updates to existing,
versioned files (new faction data inside them, not new files). `repro_check.py` and
`rules_assertions.py` are updates to existing harnesses/checks.

## Backlog

23 open at S224 close; **23 open at S225 close** (unchanged — Drukhari's loadouts build advances
the standing faction-priority-order sequence but isn't its own backlog ticket; nothing closed,
nothing opened).

Beginning: B116, B114, B113, B108, B99, B98, B97, B103, E28, B93, B90, B94, B85, B86, B69, B70,
B75, P2, P4, E23, B67b, E12, B17 (23). Resolved: none (0). Added: none (0). Ending: B116, B114,
B113, B108, B99, B98, B97, B103, E28, B93, B90, B94, B85, B86, B69, B70, B75, P2, P4, E23, B67b,
E12, B17 (23).
