# Next-session prompt — Session 134

Session 133 shipped **B61** (**D208**): Plague Legions units are now tagged `allied_group: "Plague
Legions"` at the parser via a known-label lookup (`ALLIED_GROUP_HEADERS`), `units.json` re-banked
(exactly the six units changed, one new key each), four assertions filed. `index.html` stays at
**6.5**, assertions **88/88**, baseline **21/21**. Read `SESSION_HANDOFF_133.md`, then **D208**.

**Tagged, not gated.** The six units are still selectable under any detachment or none, with no
points sub-cap and Rotigus still Warlord-eligible. That gate is E22b, sequenced into S136 with E21c —
not this session's work.

## Turn type

**Data-only.** `detachment_effects.json` (net new), hand-authored. No parser, no converter, no engine,
no `index.html`.

## Baseline at open

Run `./baseline.sh` (`--no-repo` if offline). Verify the four S133 hashes in `SESSION_HANDOFF_133.md`'s
Files section before trusting the sync.

## The task: E21a — `detachment_effects.json`

Author a hand-built table of detachment-driven army-construction effects, keyed `Army|DETACHMENT`,
covering the six live cases D203 found plus the two unlock cases D204 resolved:

- **Battleline elevation** — Blood Angels|THE LOST BRETHREN (Death Company Marines ×2), Dark
  Angels|COMPANY OF HUNTERS (Outrider Squad), Death Guard|SHAMBLEROT VECTORIUM (Poxwalkers).
- **Forbid / conditional Warlord** — Chaos Daemons|SHADOW LEGION (Be'Lakor optional; if included must
  be Warlord — not a require, per D204's correction to the faction-pack paraphrase).
- **Unlock** — Death Guard|TALLYBAND SUMMONERS (Plague Legions, `enforced: true` — B61 already landed
  the marking this reads); Chaos Daemons|SHADOW LEGION (HERETIC ASTARTES, `enforced: false` — no CSM
  units are built yet, ships as a documented gap, not a silent omission).

Effect kinds are `battleline` | `forbid` | `unlock` | `warlord` (D204 — `require` is dropped; no built
detachment needs it).

**Author from the rules, not from `rule_text`.** D203 gives three reasons and D204 a fourth: `rule_text`
spans three fidelity tiers including a paraphrase that disagrees with actual rule content (Shadow
Legion's Be'Lakor line); nine built detachments carry no rule text at all; the prose names don't match
`units.json`'s names (`Daemon Prince` vs. **Daemon Prince of Chaos**, `Be'lakor` vs. **Be'Lakor**); and
the faction-pack paraphrase inverted Shadow Legion's actual constraint (conditional Warlord, not
unconditional inclusion) — a parser trusting the prose would have shipped the wrong rule with full
confidence. Hand-author against the faction packs / MFM text directly, then add referential-integrity
assertions (every unit name resolves in `units.json`, every army|detachment key resolves in
`detachments.json`) so a typo fails loudly rather than silently.

**25 of 143 built detachments carrying chapter-exclusivity text need no entry.** `resolveUnits()`
already composes a chapter army as the generic pool plus that chapter's own units, so no foreign-chapter
unit is ever reachable — D0 satisfied by construction. E21b adds the structural assertion; this session
doesn't need a row for it.

## Ground rules

* Data-only. No parser, no converter, no engine, no `index.html`.
* `detachment_effects.json` is genuinely net new — no file has played this role before.
* Do not rename anything — project name still unsettled.

## After E21a

* **S135 — engine-only.** E21b: `effectiveUnitType()` feeding `instanceLimit()` and both grouping
  sites, plus the chapter-exclusivity structural assertion.
* **S136 — engine-only.** E21c with E22b — Shadow Legion's forbid/conditional-Warlord path, Death
  Guard's Plague Legions unlock gate (consuming B61's `allied_group` tag), points sub-cap, Warlord ban.
* **S137 — UI-only.** E21d: refusal prose, roster warnings, Battleline indicator.

## Backlog

**7 open:** B62, P2, E21 (scoped a/b/c/d), E22 (E22a done, E22b remains), B60, E12, B17.

## Standing inputs, neither blocking, worth more now than before

* **A local backup folder** for the GW-derived and GW-text-carrying files — the nine Chaos Daemons
  CSVs, the Wahapedia export, the MFM `.txt` files, the faction web and pack files. The repo cannot
  hold them; S131 lost three and rebuilt them only because `units.json` happened to carry enough.
* Faction packs for **Black Templars, Blood Angels, Space Wolves, Death Guard** — this session's
  Battleline-elevation rows (THE LOST BRETHREN, SHAMBLEROT VECTORIUM) are exactly the kind of fact
  these would let you author with more confidence than the MFM text alone gives.
* A **single-column re-extraction of the Space Marines pack** — still flips 15 detachments'
  stratagems to current text.
* **D199's four batched calls remain unreviewed — since S127, now seven sessions.** Worth a look
  purely on staleness grounds even though nothing this session depends on them.
* **B62** — the `FALSE` string-literal quirk and missing presence-and-parse assertion over the nine
  CD CSVs — still open, untouched since D205.
