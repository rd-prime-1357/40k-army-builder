# NEXT SESSION PROMPT — Session 227

## Recommended turn type: engine-only (B113 — enforce detachment enhancement `LEADER:`
eligibility restrictions)

Read `SESSION_HANDOFF_226.md` first. Drukhari's units (D318), loadouts (D319), and detachments
(D320) are now all shipped — Drukhari was the last faction in the standing priority order, so
the faction-build sequence that has driven the last several sessions is complete. B113 is picked
as the next turn because it is small, ready (fully scoped at S217/D311), and closes a real D0 gap
that has been silently true across four shipped factions already.

Open with `./baseline.sh --fetch` (no `--data-turn` — this is an engine turn, GW sources are not
needed for the fix itself, though `rules_assertions.py`'s tier-all gates will still run if
sources happen to already be resident). Confirm clean before starting. If it fails, reconcile
before starting work — do not carry a failing gate forward in prose.

## The build

1. `detachment_parser.py`'s `MFM_BLOCK_NOISE` regex currently matches and silently drops any
   `^LEADER:` line inside a DETACHMENTS block. These lines restrict an enhancement to a leader
   attached to specific units. Confirmed count across shipped factions: Chaos Space Marines (2),
   Thousand Sons (1), Emperor's Children (1), World Eaters (2) — 6 total. Grey Knights, Chaos
   Daemons, and Drukhari all confirmed 0 further instances (Drukhari reconfirmed directly this
   session, S226).
2. Decide the parsing shape first: capture the `LEADER:` line's restricted-unit list instead of
   discarding it, thread it into the enhancement record in `detachments.json` (new field, e.g.
   `leader_restriction`), then enforce it at the point enhancements are assigned to a leader in
   `index.html` (the same E4b assignment-rules block D199 already governs).
3. Re-derive the exact 6 instances from source before writing any code — do not trust this
   prompt's count unchecked, per standing discipline.
4. This changes `detachments.json`'s schema (new optional field) — diff-guard carefully: every
   existing enhancement record must gain the field as `null`/absent-equivalent with 0 other
   changes, and only the 6 flagged enhancements should carry real restriction data.
5. New `rules_assertions.py` check pinning the 6-instance census, same shape as
   `e4b_name_collision_census` — a fact this legality-critical needs to be an executable check,
   not prose.
6. New engine-side enforcement: verify against a fixture (existing harness pattern, e.g. an
   `e4b`-adjacent check) that a leader outside the restricted-unit list cannot legally receive the
   enhancement, and one that is inside the list can.

## Also open, at your discretion

- **B114** — Chaos Daemons' `Shadow Legion` HERETIC ASTARTES unlock (`detachment_effects.json`) is
  recorded `enforced: false` on a now-stale premise. Needs its own scoping pass. Different turn
  type — do not fold in.
- **GK §6 / §7** — carried unchanged for several sessions now; still not investigated.
- **Repo push (Ryan's action)** — see Decisions/Ryan-action section of `SESSION_HANDOFF_226.md`;
  the pending push queue (S220 onward) is unchanged and still outstanding.

## Standing reminders

- Re-derive from source, don't trust prior-session prose — including this prompt's own numbers.
- Turn typing: this is an engine turn. No data regeneration beyond the `detachments.json` schema
  addition needed to carry the restriction data itself; no new faction work.

## Decisions waiting on Ryan

**B116** — unchanged. Whether/when to build Drukhari's Harlequins/Anhrathe cross-book
allied-inclusion mechanic (see `DRUKHARI_BUILD_SCOPE.md` §6). Recommendation is still to build it
as its own follow-on ticket once Ryan decides whether/how to admit a cross-book allied-inclusion
mechanic. Does not block anything already shipped.

**Next faction after Drukhari** — the documented priority order (all Adeptus Astartes, all
Heretic Astartes, Chaos Daemons, Drukhari) is now fully built. No faction is queued next.
Recommendation: hold faction work and clear the small backlog of engine/scoping items (B113,
B114, GK §6/§7) first, since none of them block on a product decision except B114 and B116 — then
revisit which faction (if any) comes after Drukhari. This is a genuine product-priority call and
belongs to Ryan whenever convenient; it does not block B113 from starting.

## Close

Produce the four documents, register `SESSION_HANDOFF_227.md` in `pipeline_manifest.py`'s GUARDED
list **before** running `--write`, and run `pipeline_manifest.py --freshness-check` as the
**last** command.
