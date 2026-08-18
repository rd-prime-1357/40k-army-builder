# NEXT SESSION PROMPT — Session 259

## Read first

`SESSION_HANDOFF_258.md` and this file are the only authority on current state. Do not trust
remembered session numbers, version strings or decision numbers — re-derive them.

This is a **wind-down session**, not a feature session. The project is being set aside. S258 confirmed
custody is complete: the public repo plus the private sources repo hold a self-reproducing record.
S259's whole job is the cold-storage document.

## Session open

Run `./baseline.sh --fetch`. Expect 35/35 with 5 tier-B gates skipped; `--fetch --data-turn` gives
42/42. This turn touches no data, so tier-A is sufficient.

**Take `detachments_repro_check.py` from the repo, always.** Do not ask Ryan to re-upload it. The
project-area copy is stale and the repo copy is the newer, authoritative one — D355 settled this after
three sessions asked for the re-upload backwards.

Verify the four hashes in S258's Files table against a fresh clone.

## Turn type: documentation

No engine, data, parser or assertion change. If the work starts pulling toward a code change, stop and
bank it — the point of this session is a durable record, not a fix.

## The assigned work — `PROJECT_COLD_STORAGE.md` (net new)

One document, written for a reader who has none of this context: a future Ryan returning after a long
gap, or a future model opening the repo cold. It replaces reading back through 133 handoffs. Plain
prose, no assumed knowledge, no padding.

It must cover:

**What the thing is.** A browser-based Warhammer 40,000 11th Edition Matched Play list builder,
single-file `index.html`, deployed on GitHub Pages, currently **v6.27**. Its differentiator is D0 —
illegal army states must be unreachable, not merely flagged. That one principle explains most of the
architecture, including why rules live in engine code rather than in a data schema.

**What actually works today.** Twenty factions built: twelve Adeptus Astartes, five Heretic Astartes,
Chaos Daemons, Drukhari. Say plainly what a user can and cannot do end to end.

**What the pipeline is.** Private GW sources → parsers → JSON data files → single-file app, with
`baseline.sh` as the one command that checks everything. Name the gates and what each protects. Make
clear the private sources repo is required to regenerate but not to run.

**What is broken or missing.** The 23 open tickets grouped by meaning, not listed by ID. Call out the
live D0 gaps specifically — B93's remaining turn, B90's union-vs-complete roster bug, B135's
unmodelled transports, B120, E23 — because those are places the app is confidently wrong rather than
merely incomplete. Note that B116 was resolved by Aeldari going out of scope: Drukhari ships without
Harlequin and Anhrathe allied units.

**The traps.** The things that cost multiple sessions each and would cost them again: the project-area
mount is not evidence of what exists; a census result that looks small is usually an unread field;
scope-document instructions can be superseded by later decisions; hand-edited output files are lost on
the next regeneration; GW-derived material must never reach the public repo, tested by content and not
by author.

**Why it was set aside, and what a revival faces.** Be straight. Rules are encoded as engine code plus
curated tables, which is what makes D0 achievable and also what caps throughput at one maintainer's
rate — the 26 sessions from S232 to S257 closed 24 tickets and opened 23, a steady state rather than a
queue draining. A revival that fixes throughput is a rules-as-data rebuild, not a continuation of this
backlog. Say that plainly rather than implying the project is nearly finished.

**Where everything lives.** Public repo `rd-prime-1357/40k-army-builder`; private sources repo
`rd-prime-1357/rd-prime-1357-data-sources` with the read-only token at `SOURCE_REPO_TOKEN.txt`; which
documents are living and which are archival; the fact that `SESSION_HANDOFF_203.md` is missing from an
otherwise unbroken 125–257 chain.

## Also this session

Nothing else. Do not start a ticket.

## Session close

Add `SESSION_HANDOFF_259.md` to `GUARDED` **before** `--write` (FILES-TABLE ORDERING, S257). Then
`pipeline_manifest.py --write` followed immediately by `pipeline_manifest.py --freshness-check` as the
literal last two commands. Produce the handoff, the decision log entry and the backlog update as
usual — the chain stays unbroken even on the last session.

Push after close: `PROJECT_COLD_STORAGE.md`, `40K_Decision_Log.md`, `DECISION_INDEX.md`,
`OPEN_ITEMS_BACKLOG.md`, `pipeline_manifest.py`, `pipeline_manifest.json`,
`SESSION_HANDOFF_259.md`, `NEXT_SESSION_PROMPT.md`.

---

## Standing item: the render checks, six sessions deep

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
