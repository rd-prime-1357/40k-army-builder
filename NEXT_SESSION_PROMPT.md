# NEXT SESSION PROMPT — Session 226

## Recommended turn type: data-only (Drukhari detachments — build `detachments.json` for the 9
detachments, including the deferred `detachment_parser.py` three-map registration)

Read `SESSION_HANDOFF_225.md` first, then `DRUKHARI_BUILD_SCOPE.md` §5 (still the authoritative
scoping writeup for the detachment shapes — nothing in it is known to have changed, but per
standing discipline re-derive the counts from source rather than trusting it unchecked, the same
way S225 found §7's loadout-authoring count was wrong). Drukhari's units and loadouts are both
shipped (D318, D319); this turn does not touch `units.json` or `unit_loadouts.json` at all.

Open with `./baseline.sh --fetch --data-turn`. Confirm clean before starting. If it fails,
reconcile before starting work — do not carry a failing gate forward in prose.

## The build

1. Register Drukhari in `detachment_parser.py`'s three maps (`ARMY_TO_MFM`, `MFM_SOURCE_NAME`,
   `ARMY_TO_WAHA_FACTION`) — this is safe to do now that `detachments.json` content is about to
   exist; it was deferred at S224 specifically because doing it early (before this turn) broke
   `detachments_repro_check`.
2. Run `detachment_parser.py` against `MFM_Drukhari_v1.1.txt` and build `detachments.json` for
   the 9 detachments. Re-derive the count and shape from source before banking — §5 states DP
   range 1–3, three shared Unique tags (COVENS, WYCH CULT, KABAL — each shared by two
   detachments, precedented mechanism, not new), 30 enhancements total, three detachments with a
   `FORCE DISPOSITION(S) CHANGED` tag between v1_0 and v1.1. Confirm all of this against a real
   parser run, not assumed from the scope doc.
3. Three detachments (Exhibition of Slaughter, Kabalite Agonysts, Tools of Torment) have no
   Wahapedia rule text at all — §5 says these ship with `text_source: "none"`, matching 25
   already-precedented instances. Confirm this is still true before banking.
4. One enhancement carries the `(Upgrade)` suffix (Tools of Torment's "Elixir of the Corpse
   Courts") — confirm `detachment_parser.py`'s existing `is_upgrade` stripping handles it, no new
   code needed.
5. Diff-guard `detachments.json` against committed, field-by-field, via
   `detachments_repro_check.py` — "ran clean" is not sufficient.
6. B113 gained 0 new instances for Drukhari at the S222 scoping pass (confirmed by direct text
   search of the Drukhari `DETACHMENTS` block) — re-confirm this against the real 9-detachment
   build rather than trusting the scoping-pass claim unchecked, same standing discipline as
   everything else this session.

## Also open, at your discretion

- **B113** — detachment enhancement `LEADER:` eligibility restriction discarded as parser noise (6
  instances across CSM/TS/EC/World Eaters; GK, CD, and Drukhari all confirmed to add 0 more —
  reconfirm Drukhari's 0 against the real build this session, per item 6 above). Engine turn,
  small, not urgent. Different turn type — do not fold in.
- **B114** — Chaos Daemons' `Shadow Legion` HERETIC ASTARTES unlock (`detachment_effects.json`) is
  recorded `enforced: false` on a now-stale premise. Needs its own scoping pass. Different turn
  type — do not fold in.
- **GK §6 / §7** — carried unchanged for several sessions now; still not investigated.
- **Repo push (Ryan's action)** — `OUTPUT_FORMAT_SPEC_for_project_instructions.md` and
  `Thousand_Sons_web.txt` (B108) both still outstanding. `pipeline_manifest.json` still
  outstanding from S223. This session adds S225's changed files to the same pending push (see
  `SESSION_HANDOFF_225.md`'s Ryan-action section) — `repo_check.py` will show `DIFFERS` findings
  until pushed; expected, not a new problem.

## Standing reminders

- Re-derive from source, don't trust prior-session prose — including this prompt's own numbers.
  S225 itself is a live example: the prior prompt's loadout-authoring count (9 units) turned out
  to be wrong once checked against the real pipeline (actual: 4 units needed authoring).
- Turn typing: this is a data turn. Detachments and the map registration only. No engine, no
  loadouts, no units work.

## Decisions waiting on Ryan

**B116** — unchanged. Whether/when to build Drukhari's Harlequins/Anhrathe cross-book
allied-inclusion mechanic (see `DRUKHARI_BUILD_SCOPE.md` §6). Recommendation is still to defer
past the initial Drukhari build. Does not block this session — Drukhari's own 9-detachment build
does not depend on this mechanic.

## Close

Produce the four documents, register `SESSION_HANDOFF_226.md` in `pipeline_manifest.py`'s GUARDED
list **before** running `--write`, and run `pipeline_manifest.py --freshness-check` as the
**last** command.
