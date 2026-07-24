# Next-session prompt — Session 137

Session 136 shipped **E21c/E22b** (**D214**): forbid, allied unlock with a battle-size points
sub-cap, and the detachment-scoped Warlord ban are all live in `index.html` at **6.7**, in one
sliceable `E21c / E22b` block. Assertions **100/100**, baseline **23/23**. Read
`SESSION_HANDOFF_136.md`, then **D214**, then **D204** (rulings 1–3) and **D212** (the E21b block E21d
renders on top of). E22 is closed; **E21 stays open on E21d**, which closes it.

## Turn type

**UI-only.** `index.html` only, plus harnesses and assertions if a rendered behaviour needs pinning.
No parser, no converter, no data file, no JSON regeneration. `detachment_effects.json` is a
hand-authored **input** — never edit it. E21c's engine predicates already decide legality; E21d only
renders what they already know.

## Baseline at open

Run `./baseline.sh` (`--no-repo` if offline) — **23 gates now**, including `e21c_check`. Verify the
S136 hashes in `SESSION_HANDOFF_136.md`'s Files section before trusting the sync.
`detachment_effects.json` is unchanged and its hash is still `e38c38dcef31`.

## The task: E21d — the UI layer that closes E21

Three pieces, all presentation over predicates that already exist:

**1. Refusal prose.** The add path refuses through `canAddUnitToList` → `addRefusalText`, and the
detachment picker refuses a forbid-on-select through `detachmentForbidConflicts`. `addRefusalText` is
functional, not polished — bring it up to `enhancementRefusalText`'s standard (it already names the
unit, the group and the sub-cap numbers in the reason object). Wire the disabled picker row and its
reason off `detachmentForbidConflicts(key)`: today the click is refused with a banner but the row is
not visibly disabled, so extend `detachmentPickerRowState` — and note that doing so changes what
**E1c-1** asserts about `disabled` (currently "disabled iff `canAddDetachment` is not OK"); update the
assertion to include the forbid gate rather than loosening it.

**2. Battleline indicator.** A detachment-elevated unit renders under Battleline (E21b) but nothing
tells the player *why* it moved. Add the indicator D204 ruling 2 asked for.

**3. The stranded-allied residual — the one product call in this session.** Deselecting or switching
away from Tallyband Summoners while Plague Legions units are in the list strands them: the engine
rejects them (`offerableUnits`, `canAddUnitToList`) but the roster shows no error. The recommendation
in D214 is to **flag them as a visible error**, the enhancement over-state treatment — never a silent
trim, and **not** by blocking the deselect (that would contradict flag-don't-drop). **Confirm this
direction with Ryan before building it**, since it sets a precedent for how the tool treats a legal
list that a later detachment change makes illegal. The engine predicate is already there; only the
render is new.

## Ground rules

* UI-only. `index.html`, harnesses, assertions. No data file touched.
* Do not rename anything — project name still unsettled.
* The render still needs Ryan's eyeball — Claude cannot see the DOM. Say so; do not claim a visual is
  correct.

## After E21d

* **S138 — data-only.** P4 step 2. Decision rule fixed in D213: minify `unit_loadouts.json` alone
  (77 KB), re-bank its fixed point, reissue the manifest, then read the percentage. If ~77 KB moves
  the display ~0.6 points, step 3 minifies `units.json` and `detachments.json`; if it does not move,
  step 3 is cancelled.
* **E23** — scoping turn, unsequenced. Headhunter Task Force's Tank Ace → Character grant. A fifth
  effect kind (muster-time keyword grant, count-limited, player-chosen recipients), player state
  rather than a static row; lands on E4's enhancement eligibility and E9's Warlord eligibility.
  Over-restriction, not a D0 violation.
* **B62** — the `FALSE` string-literal quirk and the missing presence-and-parse assertion over the
  nine CD CSVs. Open and untouched since D205.
* Then the faction priority order resumes: Chaos Space Marines next (it unblocks Shadow Legion's
  HERETIC ASTARTES unlock, still `enforced: false`).

## Standing inputs

* **A local backup folder** for the GW-derived files — the nine Chaos Daemons CSVs, the Wahapedia
  export, the MFM `.txt` files, the faction web and pack files, `Army_Muster_Rules.txt` and
  `wh40k_core_rules.md` (139 KB, opened by nothing — the obvious first tenant). The repo cannot hold
  them; S131 lost three and rebuilt them only because `units.json` happened to carry enough.
* Faction packs for **Black Templars, Blood Angels, Space Wolves, Death Guard**.
* A **single-column re-extraction of the Space Marines pack** — still flips 15 detachments'
  stratagems to current text.
* **D199's four batched calls remain unreviewed — since S127, now ten sessions.**
* **New files and project-area capacity (92%).** S136 added one harness (~10 KB) — noise against a
  ~12 MB area. The lever remains moving the GW-derived source files to local backup, not refusing to
  add checks.

## Effort

**Mostly mechanical with one product call.** The rendering is UI plumbing over predicates that already
decide legality — moderate effort. The stranded-allied direction (piece 3) is a lasting precedent and
must reach Ryan before it is built; do not decide it silently.

## Backlog

**8 open:** B62, P2, P4, E21 (E21a/b/c shipped; E21d remains), E23, B60, E12, B17.
