# Next-session prompt — Session 128

Session 127 was an **analysis/scoping session**: E4 designed end-to-end as **D199**, the planned
E4a data turn cancelled (data verified clean), E4 split into E4b (this session) and E4c (S129).
Read `SESSION_HANDOFF_127.md`, then **D199** in full — it is the build spec. `index.html` did not
change — still 6.3.

## Turn type

**Engine-only.** E4b: enhancement state, persistence, validation and points math. No data file
changes, no parser changes. The UI (E4c) is S129 — this session may add the minimal render hooks
the assertions need, but the picker/chip/error rendering is out of scope; stop cleanly at the
engine seam.

## Baseline at open

Run `./baseline.sh` (use `--no-repo` if offline). **Known S127 finding:** if this sandbox loads
from the Claude Project store, `repro_check.py` and `pipeline_manifest.py` may be missing and
`pipeline_manifest.json` stale — pull the three from the GitHub repo if Ryan has not re-uploaded
them yet. The repo versions are correct; S127 verified them against the S126 hashes.

**Verify the S127 hashes** in `SESSION_HANDOFF_127.md`'s Files section before trusting the sync.

## The task: E4b — enhancement engine + persistence (per D199)

Build exactly what D199 specifies:

1. **Per-entry field** `enhancement: { name, detachment_key }` beside `god`/`wargear`/`otherOptions`.
2. **`list_store.js` schema v2 → v3.** v2 records load with `enhancement: null` on every entry.
   Flag-don't-drop on load: unresolvable detachment key or name is kept, flagged, priced from the
   catalogue when resolvable and 0 when not (the `detachmentDp()` pattern).
3. **One read-path function** answering every legality question with ok/blocked-with-reason:
   wrong unit type (regular → Character only; Upgrade → any type except Epic Hero), duplicate
   (name-keyed army-wide; Upgrades block at the third copy), unit/attached-group already has one,
   army limit reached (2 at ≤1000 pts else 4; first Upgrade copy counts, second/third do not),
   not-offered (stale/import only). Hard block per D114/D115; over states from import or
   battle-size/detachment change stay visible errors.
4. **Attach-action gate**: refuse merging two enhancement carriers into one attached group.
5. **Points math** through the existing recompute — entry points, army total, cap, `points_cache`.
6. **Assertions** (rules_assertions.py or a new e4b harness — your call, note it in the handoff):
   eligibility-set match (unit_type-derived vs keyword-derived wherever keywords are populated);
   single-call-site guard on the read-path function (E1c-1 pattern); count arithmetic including
   the Upgrade carve-out; name-collision census pinned at **29** so a data regeneration that moves
   it resurfaces the duplicate-identity question.

**Version-bump `index.html`** and state the version when publishing.

## Ryan's batched calls (D199) — check before building on them

Four recommendations are pending Ryan's review: name-keyed duplicates, Epic-Hero-ban-on-Upgrades,
free-text restrictions displayed-not-enforced, inline config-panel UI. If he has overruled any,
the design adjusts before E4b builds; if silent, proceed on the recommendations as recorded.

## Backlog

**7 open:** P2, E21, E4b (this session), E4c, E12, B56, B17.

## Ground rules

* Engine-only — data files and parsers untouched.
* Do not rename anything — project name still unsettled.
* T2 hashes in this session's handoff Files section for S129 to verify.
* Manifest: `index.html` and `list_store.js` are guarded — regenerate `pipeline_manifest.json`
  (`--write`) at close after all gates pass.

## Standing inputs, neither blocking, worth more now

* Faction packs for **Black Templars, Blood Angels, Space Wolves, Death Guard** — unchanged from
  the S127 prompt; still zeroes the nine-detachment no-text gap.
* A **single-column re-extraction of the Space Marines pack** — still flips 15 detachments'
  stratagems to current text.
