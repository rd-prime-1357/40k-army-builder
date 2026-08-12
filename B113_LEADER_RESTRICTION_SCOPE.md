# B113 — Detachment enhancement `LEADER:` line: scope / diagnosis (S227)

**Status: build stopped cleanly at open. The feature as scoped in the S227 prompt (and in the
original B113 backlog entry / D311) rests on a wrong model of what the `LEADER:` line means, and
building it would make the affected enhancements assignable to nobody. B113 is re-scoped here and
now carries a product/rules-legality decision for Ryan. No engine, data, or assertion change was
shipped this turn.**

This turn was typed engine-only. The diagnosis found there is no correct engine change to make
until Ryan settles the mechanic, so the turn's real output is scoping. Flagging the type change
rather than forcing a half-built engine change to fit the original type.

---

## 1. The two source-derived corrections

### 1a. The census is 8, not 6

Every prior statement of this census — the S227 prompt, the B113 backlog entry, D311 — says 6
instances: Chaos Space Marines ×2, Thousand Sons ×1, Emperor's Children ×1, World Eaters ×2.

Re-derived directly this session against the v1.1 MFM files the parser actually consumes (the
files named in `detachment_parser.py`'s `ARMY_TO_MFM`), reading each line exactly as the parser
does (`clean_chars` + strip + the v1.1 DETACHMENTS-block normalisation), the true count is **8**.
The two that every prior statement missed are both **Space Wolves**, a faction that shipped after
B113 was opened at S217:

- Saga of the Beastslayer → Wolf-touched → `LEADER:WULFEN, WULFEN WITH STORM SHIELDS`
- Saga of the Great Wolf → Grimnar's Mark → `LEADER:WOLF GUARD TERMINATORS`

The v1_0 files and unbuilt factions (Sororitas, Astra Militarum, Necrons, Orks) also carry
`LEADER:` lines, but those files are not referenced by `ARMY_TO_MFM` and do not reach
`detachments.json`, so they are correctly out of scope.

### 1b. The binding was mis-stated too

The original B113 entry gives World Eaters' second instance as "Khorne Daemonkin's **Icon of
War**". That is wrong. The `LEADER:` line binds to the enhancement **immediately above it**, and
in Khorne Daemonkin that is **Disciple of Khorne** — Icon of War is the line *after* the `LEADER:`
line and carries no restriction. The `LEADER:` line is frequently mid-list, not at the end of the
ENHANCEMENTS block (e.g. CSM Murdertalon Raiders restricts Pact of Cursed Pinions but leaves
Shadowcowl Talisman, printed directly below it, unrestricted). Binding to "the last enhancement"
or "the whole detachment" would both be wrong.

The immediately-preceding-enhancement binding is confirmed independently by the 10e rules text we
already hold in `detachments.json`: Sorrowscent Vulture's text names "a Warp Talons unit", Disciple
of Khorne's names "a Bloodcrushers or Flesh Hounds unit", Butcher Lord's names "a Jakhals or
Goremongers unit" — each matching the `LEADER:` line printed under it, and each leaving the *other*
enhancements in the same detachment (including the one printed directly above, e.g. Greyveil Hex
above Sorrowscent Vulture) untouched.

### The corrected, complete census

| Faction | Detachment | Bound enhancement | Pts | `LEADER:` target unit(s) | Bearer restriction (from rules text) |
|---|---|---|---|---|---|
| Space Wolves | Saga of the Beastslayer | Wolf-touched | 15 | Wulfen, Wulfen with Storm Shields | Space Wolves model only |
| Space Wolves | Saga of the Great Wolf | Grimnar's Mark | 20 | Wolf Guard Terminators | Adeptus Astartes Terminator Captain model only |
| Chaos Space Marines | Murdertalon Raiders | Pact of Cursed Pinions | 20 | Warp Talons | *(no rules text in source)* |
| Chaos Space Marines | Nightmare Hunt | Sorrowscent Vulture | 35 | Warp Talons | Chaos Lord w/ Jump Pack model only |
| Thousand Sons | Warpmeld Pact | Bray Lord | 15 | Tzaangors | Sorcerer or Infernal Master model only |
| Emperor's Children | Court of the Phoenician | Exalted Patron | 15 | Flawless Blades | Lord Exultant model only |
| World Eaters | Cult of Blood | Butcher Lord | 10 | Goremongers, Jakhals | World Eaters Infantry model only |
| World Eaters | Khorne Daemonkin | Disciple of Khorne | 15 | Bloodcrushers, Flesh Hounds | Lord on Juggernaut model only |

The comma-separated target list reads as "or" (one of these units), confirmed by the rules text in
every case that has text.

---

## 2. The decisive finding: `LEADER:` is an attach-ENABLER, not an assignment restriction

The S227 prompt scopes B113 as: capture the `LEADER:` unit list, thread it into the enhancement
record, and enforce at assignment time so that "a leader outside the restricted-unit list cannot
legally receive the enhancement, and one that is inside the list can." That is the E4b
canAssignEnhancement gate with a new `leader_restriction` reason.

That model is backwards, for a concrete reason grounded in the data:

**The units named on the `LEADER:` line are bodyguard units the bearer normally CANNOT lead.** The
enhancement is precisely what grants the attachment. Checked against the app's own attach model
(`leaderEligible` / `canAttachLeader`, sourced from each unit's `leader_eligible_units`):

- Warp Talons (CSM): **0** leaders can attach normally. Sorrowscent Vulture's bearer, Chaos Lord
  with Jump Pack, attaches to Raptors — not Warp Talons.
- Wulfen / Wulfen with Storm Shields (SW): **0** leaders can attach normally.
- Jakhals, Goremongers, Bloodcrushers, Flesh Hounds (WE): **0** leaders can attach normally. The
  Lord on Juggernaut (Disciple of Khorne's bearer) attaches to Eightbound / Exalted Eightbound /
  Khorne Berzerkers — none of the four.
- Flawless Blades (EC), Tzaangors (TS), Wolf Guard Terminators (SW): a small number of *other*
  leaders can attach, but not the enhancement's intended bearer.

So for six of the eight targets, **no leader in the faction can attach to the named unit at all**,
and for the intended bearer in every case the named unit is not in its normal attach list.

**Consequence:** implementing the prompt's enforcement — refuse the enhancement unless the leader
is already attached to the named unit — would make these enhancements assignable to **nobody**,
because the app will not permit the prerequisite attachment in the first place. That is strictly
worse than today's state (today the enhancement is over-permissively assignable to any Character;
the prompt's change would flip it to assignable to no one). It is the opposite of D0.

The rules text confirms the direction: "During the Declare Battle Formations step, the bearer
**can** be attached to a [named] unit." The `LEADER:` line grants an attachment the bearer
otherwise lacks. It does not describe a precondition on the bearer.

---

## 3. What the enhancement actually is (two parts)

Each of these eight enhancements bundles two distinct rules:

1. **A bearer restriction** — "X model only" (e.g. *Lord on Juggernaut model only*, *Chaos Lord
   with Jump Pack model only*). This is the rule that actually makes an illegal army reachable
   today: right now any Character in the detachment can take Disciple of Khorne, when only a Lord
   on Juggernaut should. This restriction lives in the enhancement **description prose**, **not**
   on the `LEADER:` line.

2. **An attach enablement** — the `LEADER:` line — which grants the (already-restricted) bearer
   the ability to attach to a unit it normally cannot lead. Optional in the rules ("can be
   attached"): a legal army may include the enhancement on its eligible bearer without ever making
   the attachment.

B113's data capture (the `LEADER:` line alone) therefore captures only the *second, optional*
part, and not the *first, legality-meaningful* part. Capturing `leader_restriction` and enforcing
it as an assignment gate would enforce the wrong half of the rule, in the wrong direction.

---

## 4. Options for the correct mechanic (decision for Ryan)

This is a product / rules-legality call with lasting precedent — it is the first
enhancement-conditional attachment mechanic in the tool, and it sets how the tool treats
"enhancement grants an attachment" and whether such attachments are ever mandatory. It belongs to
Ryan, not to the build. Options, with trade-offs:

- **(A) Enforce the bearer restriction only.** Restrict each of the 8 enhancements to its named
  bearer unit(s) — the change that genuinely makes illegal armies unreachable (the wrong Character
  can no longer take it). Needs per-enhancement bearer data. Seven of eight have it in the
  description prose ("X model only"); one (Pact of Cursed Pinions) has no source text and would
  need a hand-supplied bearer. Prose parsing of "X model only" is not clean, so this likely means a
  small curated, asserted 8-row bearer map. Medium engine change, in the E4b gate — but note the
  bearer text is not uniformly single-unit ("Space Wolves model only", "Sorcerer or Infernal
  Master model only"), so the data shape is per-enhancement, not one keyword.
  **This is my recommendation for what to enforce** — it is the part that maps to a reachable
  illegal state.

- **(B) Full attach-enablement.** Model the `LEADER:` line properly: when the enhancement is on its
  eligible bearer, expand that bearer's `leaderEligible` to include the named unit(s), and make the
  resulting attachment legal only while the enhancement is held (removing it must break the
  attachment). Correct and complete, but a real change to the attachment-eligibility model
  (`canAttachLeader` / `leaderEligible`), order-dependent, and it still needs the bearer data from
  (A) to know whose eligibility to expand. Largest of the three. Best done *after* (A), if at all.

- **(C) Capture-only, defer enforcement.** Add `leader_restriction` to the schema as inert data now
  and enforce nothing until (A)/(B) is scoped. Smallest, but ships no legality gain and risks the
  field ossifying at a shape the real mechanic doesn't want.

Recommendation: re-scope B113 to **(A)** — enforce the bearer restriction, which is the reachable
illegal state — and treat the `LEADER:` attach-enablement (B) as a separate, later item that (A)
does not block. Do **not** build the prompt's assignment-restriction-on-attach-target enforcement
under any option; it is incorrect regardless.

Whichever way Ryan calls it, the corrected 8-instance census (§1) and the binding rule (§1b) are
the settled, source-derived inputs the build will start from, and should land as an executable
assertion in `rules_assertions.py` at the top of that build so the scope cannot silently drift
again the way the "6" did.

---

## 5. What was verified this session, and how

- Census of 8 and the two Space Wolves instances: re-derived by parsing every `ARMY_TO_MFM` v1.1
  file with the parser's own line handling and normalisation; counted `LEADER:` lines inside the
  DETACHMENTS→LEGENDS slice.
- Binding to the immediately-preceding enhancement: read the full detachment blocks; confirmed the
  `LEADER:` line is mid-list in most cases; cross-checked against the 10e rules text already in
  `detachments.json`, which names the same target unit under the same enhancement.
- Attach-enabler finding: checked the target units against every faction leader's
  `leader_eligible_units` in `units.json`, and checked the intended bearers' own attach lists —
  the named targets are absent from both.

All figures above come from command output in this session, not from prior-session prose.
