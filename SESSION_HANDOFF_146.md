# Session Handoff 146

## Baseline at open

S145's six hashes matched byte-for-byte. `./baseline.sh --no-repo` passed 23/23 gates, 104/104
assertions — clean, unchanged from S145's close. `repo_check.py` is absent from the mount (as since
S141/S142), so the repo gate was skipped; no committed file was touched this turn, so custody is
unaffected.

## What happened — D227, tooling-only (CSM build scoped, not built)

Scoping-only turn. No committed data, engine, or parser file changed. Dry-run transforms wrote only to
a throwaway temp dir. Full plan in the net-new `CSM_BUILD_SCOPE.md`; the load-bearing findings:

**Roster is 58, not 112.** The 112 is a raw `faction_id == CSM` row count; 54 are Warhammer Legends
(edition 0) and are correctly dropped by the transform's existing filter. The dry-run transform selects
58, matching `MFM_Standalone_Pass.md`. CSM is a clean Death-Guard-shaped build — no chapter split, no
allied codex, no new engine or UI mechanism, no `index.html` change.

**Marks of Chaos need no new mechanism.** Zero "Mark of …" option rows; marks are baked-in god
keywords plus three E4-handled enhancements. The biggest potential complication is ruled out.

**Detachments reconcile to 17 under D192** (engineering rule, not a Ryan call). MFM-only (kept):
Devotees of Destruction, Murdertalon Raiders. Wahapedia-only (dropped as stale 10th-ed leftovers):
Champions of Chaos, Infernal Reavers, Underdeck Uprising. `detachment_parser.py` already works this
way; three config lines only.

**Four cult-troop units are priced in sibling MFMs** — Khorne Berzerkers (WE), Plague Marines (DG),
Rubric Marines (TS), Noise Marines (EC), all confirmed present. They must be priced. The existing
`--append --scope-to-army` machinery covers it, with a relabel wrinkle. This is the only part of the
build with a real chance of running deep; if so, it stays its own turn.

**Build sequenced as three data turns + one tooling turn, strictly separated** (scope §8). Real
project-area growth is ~540 KB across the three regenerated outputs. Turn A is next session.

## Decisions needed

**D228 (precedent-setting; build proceeds on recommendation unless Ryan says otherwise).** The two new
detachments have no held rule/enhancement/stratagem prose in any source. Recommendation: build them
selectable but prose-incomplete — suppressing legal current-edition detachments breaks the tool's core
promise, and it mirrors E1's prose-incomplete handling. Reversible (one inclusion flag). Explicit
yes/no wanted because it sets a precedent for all future factions.

Also still open, carried forward: D199's four batched calls (unreviewed since S127, twenty sessions,
three load-bearing); the `_web.txt` regeneration plan (D226 — pause and ask before each); B67b.

## Shipped / changed

Docs only. `CSM_BUILD_SCOPE.md` written (net-new). `40K_Decision_Log_v3_0.md` — D227, D228 appended.
`DECISION_INDEX.md` — both indexed. `NEXT_SESSION_PROMPT.md` — rewritten for S147 (CSM build turn A).
`OPEN_ITEMS_BACKLOG.md` — header session marker moved to S146, CSM-scoping note added; no ticket
opened or closed.

### Net New Files
- `CSM_BUILD_SCOPE.md` — the build-scope document. New name; "scope document" is a role the project
  has held before (`E1_DETACHMENT_SCOPE.md`), so under the project's own rule this is arguably an
  update-class file. Listed here as net-new because it is a distinct, standalone artifact the S147
  build turn consumes; flagging the ambiguity rather than hiding it.

### Files (SHA-256, first 12 chars)
- `CSM_BUILD_SCOPE.md` — `2701d61e56e5`
- `40K_Decision_Log_v3_0.md` — `9910c67a14bd`
- `DECISION_INDEX.md` — `4680c7ee3180`
- `NEXT_SESSION_PROMPT.md` — `1e11c33a6727`
- `OPEN_ITEMS_BACKLOG.md` — `3e1f2ac1edc8`

**Repo custody:** all five files are project-generated prose. `CSM_BUILD_SCOPE.md` names detachment,
unit, and enhancement titles and points but reproduces no GW rule/ability prose — repo-eligible, same
class as the other scope docs and the decision log. No GW-derived source is introduced. Belongs in the
next batch upload alongside this handoff. Excluded as always: the Wahapedia CSV export, the MFM `.txt`
files, the faction web/pack files.

## Backlog summary

- **Beginning (7 open):** P2, P4, E23, E12, B17, B61, B67b
- **Resolved (0):** none
- **Added (0):** none
- **Ending (7 open):** P2, P4, E23, E12, B17, B61, B67b
