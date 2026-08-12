# B114 — Chaos Daemons' Shadow Legion HERETIC ASTARTES unlock: scope / diagnosis (S229)

**Status: scoping only, no build. The stored effect's premise (flip `enforced: true` once CSM
ships) is not simply stale — the effect's `target` shape is one the engine has never had code to
consume at all, and the rule text's actual unlockable set is materially narrower than a literal
reading of "HERETIC ASTARTES keyword" would suggest. Recommends re-shaping the data onto the
existing, already-tested `allied_group` mechanism (Plague Legions / Scintillating Legions
precedent) rather than building new keyword-based unlock logic.**

---

## 1. Why "flip the flag" was never going to work

`detachment_effects.json`'s `Chaos Daemons|SHADOW LEGION` entry stores the HERETIC ASTARTES unlock
as `target: {"keyword": "HERETIC ASTARTES"}`, `enforced: false`, reasoned (D204 ruling 3, B112
finding) as "nothing is currently reachable through this effect [because CSM isn't built], it
becomes enforceable the session CSM lands."

CSM landed at S212 (D307). But `index.html`'s `unlockedAlliedGroups`/`alliedPointsCap` — the only
engine code that reads an `unlock`-kind effect at all — filters exclusively on
`eff.target.allied_group` (index.html, ~line 2593, comment confirms this explicitly: "Only
allied_group unlocks are handled; the keyword-targeted unlock (Shadow Legion's HERETIC ASTARTES)
is enforced:false until CSM is built and is skipped by the same guard"). There is no code path that
reads `target.keyword` at all — flipping `enforced: true` today would change nothing, because
nothing consumes that field. The B112/D204 premise wasn't "the flag is stale," it's "the flag was
never wired to any mechanism in the first place." This needed a scoping pass, not a one-line fix,
independent of the CSM-shipped question.

## 2. The real unlockable set is not "every CSM unit with the HERETIC ASTARTES keyword"

Pulled the actual Wahapedia ability text this session (`Detachment_abilities.csv` id `000009976`,
"Thralls of the First Prince" — the ability `detachments.json`'s paraphrased `rule_text` summarizes
as "Heretic Astartes allies allowed up to..."). The ability names an **explicit 15-item list**, not
a bare keyword:

> Chaos Lord, Chaos Lord in Terminator Armour, Chaos Lord with Jump Pack, Chaos Terminator Squad,
> Chosen, **Damned units**, Dark Apostle, Havocs, Legionaries, Master of Possession, Possessed,
> Raptors, Sorcerer, Sorcerer in Terminator Armour, Warp Talons

14 of these are literal datasheet names; **"Damned units" is itself a Wahapedia keyword group**, not
a single datasheet — it covers 17 distinct datasheets across Wahapedia's export (Cultist Mob,
Cultist Firebrand, Fellgor Beastmen, Dark Commune, Traitor Enforcer, Accursed Cultists, Traitor
Guardsmen Squad, Cultist Mob with Firearms, Gellerpox Infected, Mutoid Vermin, Negavolt Cultists,
Renegade Enforcer, Renegade Heavy Weapons Squad, Renegade Ogryn Beast Handler, Renegade Ogryn
Brutes, Renegade Plague Ogryns, Rogue Psyker), checked directly against `Datasheets_keywords.csv`.

**If a future engine change unlocked "every unit carrying the HERETIC ASTARTES keyword" as a bare
keyword filter, that would be over-permissive — a live D0 violation the moment it shipped.** CSM's
58-unit built roster includes Epic Heroes and named characters (Abaddon, Cypher, Fabius Bile, Huron
Blackheart, Vashtorr the Arkifane, Kravek Morne, Haarken Worldclaimer, and others) that almost
certainly carry the HERETIC ASTARTES keyword but are nowhere on Thralls of the First Prince's list
and are not legally includable under Shadow Legion. This is exactly the failure shape B113 found in
a different rule (a broad-sounding label that is not the actual reachable legal set) — worth
flagging on the same grounds even though the mechanism here is unrelated to B113's.

### The actually-buildable set, checked against the shipped CSM roster

All 14 named datasheets, and 7 of the 17 "Damned"-keyword datasheets, are already in CSM's shipped
58-unit roster (`units.json`), all sourced from CSM's own Codex (Wahapedia `source_id 000000012`,
the same source the shipped roster was built from) and all carry a priced entry:

| Named directly (14) | "Damned"-keyword, built (7) | "Damned"-keyword, NOT built (10) |
|---|---|---|
| Chaos Lord | Cultist Mob | Cultist Mob with Firearms |
| Chaos Lord In Terminator Armour | Cultist Firebrand | Gellerpox Infected |
| Chaos Lord with Jump Pack | Fellgor Beastmen | Mutoid Vermin |
| Chaos Terminator Squad | Dark Commune | Negavolt Cultists |
| Chosen | Traitor Enforcer | Renegade Enforcer |
| Dark Apostle | Accursed Cultists | Renegade Heavy Weapons Squad |
| Havocs | Traitor Guardsmen Squad | Renegade Ogryn Beast Handler |
| Legionaries | | Renegade Ogryn Brutes |
| Master Of Possession | | Renegade Plague Ogryns |
| Possessed | | Rogue Psyker |
| Raptors | | |
| Sorcerer | | |
| Sorcerer In Terminator Armour | | |
| Warp Talons | | |

The 10 unbuilt "Damned"-keyword datasheets carry Wahapedia `source_id 000000355` — a Faction Pack
shared across Chaos Daemons, Chaos Space Marines, Death Guard and (Questor Traitoris, tag `QT`) —
not CSM's own Codex, and (checked directly) none of the 10 appear in CSM's own MFM file, so they
have no points and were correctly out of `CSM_BUILD_SCOPE.md`'s 58-unit build regardless of this
ticket. Leaving them out of Shadow Legion's unlock is under-enforcement (a legal option the tool
doesn't yet offer), the established safe direction (E21b's degrade rule, same convention as several
other rows in this file) — not a reachable illegal state. **Recommend leaving them out of this
build**, revisited only if/when there's reason to build the Chaos Cult source pack generally.

Total buildable unlock set: **21 units** (14 named + 7 already-shipped "Damned" units).

## 3. Recommended mechanism: reuse `allied_group`, don't build a keyword-unlock engine

The project already has a tested, shipping mechanism for exactly this rule shape — "a detachment
grants a points-capped allowance of units the army doesn't natively include" — used by Death
Guard's Plague Legions (`Rotigus`, `Great Unclean One`, `Plaguebearers`, `Plague Drones`, `Beasts of
Nurgle`, `Nurglings`, all tagged `allied_group: "Plague Legions"` in `units.json`) and Thousand
Sons' Scintillating Legions. `unlockedAlliedGroups`, `alliedPointsCap`, `alliedSubtotal`,
`canAddUnitToList`, `offerableUnits`, `detachmentForbidConflicts` and the stranded-unit handling
(E21d) all already work correctly against this shape. Building a second, keyword-based unlock
mechanism to enforce the same rule family would duplicate all of that for one detachment, with no
existing test coverage and no other consumer.

**Recommendation:** tag the 21 units above with a new `allied_group` value (e.g.
`"Shadow Legion Thralls"`) in `units.json`, and change `detachment_effects.json`'s Shadow Legion
unlock `target` from `{"keyword": "HERETIC ASTARTES"}` to `{"allied_group": "Shadow Legion
Thralls"}`, `enforced: true`. The existing `points_cap` table (500/1000/1500) is already correct
and unchanged since D204 — it matches the ability text pulled directly this session. This is a
data-only change to `units.json` and `detachment_effects.json` plus flipping the one flag; no new
engine code.

**One difference from the Plague Legions/Scintillating Legions precedent, checked rather than
assumed:** neither "Thralls of the First Prince" nor the rest of the Shadow Legion detachment rule
bans allied HERETIC ASTARTES/Damned units from being Warlord (unlike Plague Legions' explicit "No
PLAGUE LEGIONS model from your army can be your WARLORD" clause). **Do not add a matching `warlord`
effect** — that would be inventing a restriction the source text doesn't state.

## 4. What was verified this session, and how

- Engine consumption: read `index.html`'s `unlockedAlliedGroups`/`alliedPointsCap` and their
  callers directly; confirmed by the function's own comment that only `allied_group` is read.
- The 15-item named list: pulled directly from `Detachment_abilities.csv` id `000009976`
  ("Thralls of the First Prince"), not from the paraphrased `detachments.json` `rule_text` or the
  `chaos_daemons_reference.md` summary (both omit the explicit list).
- The "Damned" keyword group and its 17 members: `Datasheets_keywords.csv`, filtered on
  `keyword == 'Damned'`, resolved to names via `Datasheets.csv`.
- The 21-unit buildable overlap and the 14/7 split: cross-referenced directly against
  `units.json`'s shipped Chaos Space Marines block (58 units); all 21 confirmed present and priced.
- The unbuilt 10's exclusion reason: confirmed their Wahapedia `source_id` (`000000355`) differs
  from the 14 named units' and the 7 built "Damned" units' source (`000000012`, CSM's own Codex).
- The Warlord-ban difference from Plague Legions: read the full "Thralls of the First Prince"
  ability text directly; no Warlord clause present.

## 5. Not a decision for Ryan

No lasting-precedent or rules-ambiguity call here — the mechanism to use is a straight reuse of an
existing, already-decided pattern (Plague Legions/Scintillating Legions), and the buildable set is
fully determined by source data, not a judgment call. This is a "how it gets built" question,
proceeding under standing dev-manager authority. Recommend building next as a data-only turn:
tag the 21 units, retarget the effect, flip `enforced: true`, add a pinned assertion (same shape as
`e4b_name_collision_census`/B113's E4b-6/E4b-7) checking the 21-unit set against source so a future
MFM or Wahapedia regeneration can't silently drift it.
