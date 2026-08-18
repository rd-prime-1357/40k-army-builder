# NEXT SESSION PROMPT — Session 260 (only if the project is picked up again)

## Read first

The project was set aside at S259. **Read `PROJECT_COLD_STORAGE.md` before this file and before
anything else.** It is written for a reader with no context and replaces reading back through the
handoff chain. This file only covers what that document deliberately leaves out: the mechanics of
opening a session, and the render checks.

`SESSION_HANDOFF_259.md` is the last handoff. Do not trust remembered session numbers, version
strings or decision numbers — re-derive them. `index.html` is at **v6.27**, `rules_assertions.py` at
**139**, the decision log through **D356**, the backlog at **23 open**.

## Session open

Clone the public repo. Put `SOURCE_REPO_TOKEN.txt` next to `baseline.sh`. Run
`./baseline.sh --fetch --data-turn`.

Expect **42/42**, or 41/42 if the project file area is out of sync with the repo — that is
`repo_check` telling you about the area, not about the repo, and it is normal after a gap. A tier-A
run without sources gives 35/35 with 5 tier-B gates skipped.

If any other gate is red, reconcile it before starting work. Do not work around it and carry the
explanation forward in prose; that is how manifest work was reverted twice without anyone noticing.

Verify the hashes in `SESSION_HANDOFF_259.md`'s Files table against the clone.

**Take `detachments_repro_check.py` from the repo, always.** The project-area copy has been stale
three times running. D355 settled this.

## Before choosing work

Section 7 of `PROJECT_COLD_STORAGE.md` frames the real choice: keep twenty armies correct and current,
or rebuild rules-as-data to make faction coverage a data task. Those are different projects. Decide
which one you are doing before picking a ticket, because the answer changes whether the backlog is a
work queue or a specification.

If the answer is "keep twenty armies correct", the order is: run the render checks below; then **B90**
(the union-vs-complete chapter roster bug — the largest live D0 violation, five chapters affected);
then **B127** (source acquisition for the 74 enhancement records with no rule text, which blocks four
other tickets and cannot be built around).

Turn typing still applies: engine-only, data-only, or tooling-only, never mixed.

## Session close

Add `SESSION_HANDOFF_260.md` to `GUARDED` **before** `--write` (FILES-TABLE ORDERING, S257 — the
handoff's own hash is a row in its own table). Then `pipeline_manifest.py --write` followed
immediately by `pipeline_manifest.py --freshness-check` as the literal last two commands. Produce the
handoff, the decision log entry and the backlog update as usual.

---

## Standing item: the render checks, seven sessions deep

Four scripts, reproduced here in full so this file is self-contained and no handoff lookup is needed.
Run them against the deployed app. **S250's is the one that matters** — it is the only one that edits
a saved list without telling the player.
Four scripts, reproduced here in full so this file is self-contained and no handoff lookup is needed.
Run them against the deployed app. **S250's is the one that matters** — it is the only one that edits
a saved list without telling the player.

**S250 — silent over-cap truncation.** Create a **Grey Knights** list. Add a **Purifier Squad** at
**10 models**. Open its wargear pane and fill the psycannon/psilencer/incinerator option to its ceiling
of 4. Note the unit's points. Change the size to **5 models**. Expect: points fall, the stepper shows
**2** picks rather than 4, and **no warning banner appears** — the correction is silent by design.
Reopen the pane and confirm the two surviving picks are the first two in the option's listed order,
not the first two you clicked. If a "Too many weapon swaps for this unit size" banner appears at any
point, that is a real defect.

**S256 — enhancement picker eligibility.** Build a **Space Marines** list on **Headhunter Task
Force**. Add a Captain and a Rhino. On the Captain, open the enhancement section: all four
enhancements should be **visible but disabled**, each reading "Adeptus Astartes Vehicle model only."
On the Rhino, check **Select as Tank Ace**, then open its enhancement section: the same four should
now be **enabled**. Uncheck Tank Ace and confirm they return to disabled. Then switch to **Thousand
Sons / Warpmeld Pact** and confirm `Bray Lord` is offered on `Sorcerer`, `Infernal Master` **and**
`Sorcerer In Terminator Armour`, and disabled on any other Character.

**S249 — Marks of Chaos.** Create a **Chaos Space Marines** list, select **Pactbound Zealots**, add
Legionaries and a Chaos Lord. Both should show "! Choose Mark of Chaos" and a five-chip selector. Pick
Khorne on both, attach the Lord — the attach should be offered. Change the Legionaries to Nurgle: the
change must be **allowed**, and both entries must then flag the mismatch. Change the Lord to Nurgle
and confirm both clear with no detach. Add a **Dark Commune** and confirm only four chips render, with
Khorne absent. Add **Khorne Berzerkers** and confirm no selector appears and "Khorne" shows on its
roster line. Deselect Pactbound Zealots and confirm the picks are kept but flagged; reselect and
confirm they revive with no re-click.

**S248 — Tank Ace.** Open a **Space Marines** list, select **Headhunter Task Force**, add a qualifying
Vehicle. Confirm the "Tank Ace" pill shows in the datasheet modal and the checkbox appears in the
config panel. Check it, and confirm the Enhancement section and Warlord picker both pick the entry up.
Add three more qualifying Vehicles and confirm the 4th checkbox is disabled with a cap message.
Uncheck one and confirm it re-enables.
