# Next-session prompt — Session 129

Session 128 shipped **E4b** (engine + persistence) as **D200**. `index.html` is **6.4**,
`list_store.js` schema **3**, assertions **80/80**, baseline **20/20**. Read
`SESSION_HANDOFF_128.md`, then **D200** — it records a correction to D199 that matters if you
touch eligibility.

## Turn type

**UI.** E4c: the enhancement picker, the roster chip, and error rendering. No engine legality, no
data file changes, no parser changes. Every verdict E4c renders comes from `enhancementRowState`
and `enhancementRefusalText`; **assertion E4b-4 fails if E4c re-derives any of it.**

## Baseline at open

Run `./baseline.sh` (`--no-repo` if offline). **Run `repo_check.py` explicitly** — it was missing
from the project area in S128 and the custody check has not run since S127. Verify the twelve S128
hashes in `SESSION_HANDOFF_128.md`'s Files section before trusting the sync.

## The task: E4c — enhancement UI (per D199 call 4, as built by D200)

1. **Inline single-select row** in the unit's existing config panel in `renderDetail`, rendered
   only where `enhancementRowState(...).offered` gives rows the entry could hold. Name + points +
   detachment; illegal rows disabled and carrying `enhancementRefusalText`'s prose (a mute
   disabled row is the failure B47 exists to fix). A selected row is always clearable.
2. **Roster-level "Enhancements n/limit" chip** beside the DP display, off `enhancementArmyState`,
   mirroring how `renderSelectedDetachmentsHtml` renders the DP state.
3. **Error rendering** for the states only an import or a battle-size/detachment change can reach:
   `notOffered`, `wrongType`, `sharedUnits`, and `state === 'over'`. Visible, never trimmed.
   `entryHasError` already flags the carrying entry; the roster warning block is what's missing.
4. **An `e4c_check.js` harness** in the `e1c_check.js` mould — the picker's disabled flag is
   `canAssignEnhancement`'s answer for every offered row across scenarios, and nothing else.

**Version-bump `index.html`** and state the version when publishing.

## What is already done, so don't rebuild it

`offeredEnhancements()`, `enhancementRowState()`, `enhancementRefusalText()`,
`enhancementArmyState()`, `assignEnhancement()` and `clearEnhancement()` all exist, are exercised
by `e4b_check.js`, and currently have **no UI caller**. E4c is their consumer.

## Ryan's batched calls — check before building

D199's four calls are **still unreviewed** and E4b is built on all four. Calls 1 and 2 (name-keyed
duplicates, Epic-Hero-ban-on-Upgrades) are now load-bearing in shipped engine code and assertions.
Call 4 (inline config-panel picker vs. a modal) is the one E4c would act on and is still free — if
Ryan has said nothing, proceed on the inline recommendation.

## Backlog

**6 open:** P2, E21, E4c (this session), E12, B56, B17.

## Ground rules

* UI-only — engine legality, data files and parsers untouched.
* Do not rename anything — project name still unsettled.
* T2 hashes in this session's handoff Files section for S130 to verify.
* Manifest: regenerate `pipeline_manifest.json` (`--write`) at close after all gates pass, and add
  `e4c_check.js` to `pipeline_manifest.py` and `baseline.sh` when it exists.

## Standing inputs, neither blocking, worth more now

* Faction packs for **Black Templars, Blood Angels, Space Wolves, Death Guard** — still zeroes the
  nine-detachment no-text gap, and enhancement descriptions are about to become visible in the UI,
  which makes the 30 `none`-source and 265 `wahapedia_10e`-source descriptions more prominent than
  they have been.
* A **single-column re-extraction of the Space Marines pack** — still flips 15 detachments'
  stratagems to current text.
