# Open Items Backlog

Originally logged Session 18; reorganised **S126 (T5)** — closed/shipped ticket bodies moved in
full to `BACKLOG_ARCHIVE.md`. Each keeps a one-line pointer here (ID, title, closing session,
decision reference). The Open Items section below is the only section awaiting work; if it is
not here, it isn't open. **24 open** as of S212 (unchanged from S211 — nothing closed, nothing
new opened; B89 advanced but did not close): B111, B110, B109, B108, B99, B98, B97, B103, E28,
B93, B90, B94, B89, B85, B86, B69, B70, B75, P2, P4, E23, B67b, E12, B17.
Data-only turn (D306): `detachment_parser.py`'s `ARMY_TO_MFM`/`MFM_SOURCE_NAME` re-pointed Chaos
Space Marines, Death Guard, and Thousand Sons at their v1.1 MFM files, mirroring Emperor's
Children. `detachments.json` +0/-0 records, 7 changed (Hexwarp Thrallband 2 DP to 3 DP, six
disposition corrections, Soulforged Warpack's Tempting Addendum 25 to 40 pts), diff-guarded exact
match against the D305 finding's predicted list. `detachment_effects.json` and
`rules_assertions.py` checked directly, both unaffected. **B89 still open**: the same v1_0
detachment-sourcing gap applies to the six-file Space Marines group (base Adeptus Astartes, Black
Templars, Blood Angels, Dark Angels, Deathwatch, Space Wolves) — noted since D291 but not yet
confirmed/quantified by direct diff — recommended as B89's next data turn.

**24 open** as of S211 (unchanged from S210 — nothing closed, nothing
new opened; B89 gained confirmed evidence, not a new ticket): B111, B110, B109, B108, B99, B98,
B97, B103, E28, B93, B90, B94, B89, B85, B86, B69, B70, B75, P2, P4, E23, B67b, E12, B17.
Data-only turn (Emperor's Children detachments, D305). `EC` registered in `detachment_parser.py`'s
three maps, built from v1.1 per D293. `detachments.json` +10 EC detachments (179 total, 17
armies), diff-guarded 0 changed/removed elsewhere, byte-identical repro. `detachment_effects.json`
+1 entry (Carnival of Excess's Legions of Excess unlock + Warlord restriction), diff-guarded 0
changed/removed elsewhere. `faction_taxonomy.json`: EC's `built` flag flipped to `true`,
`data_army` added — Emperor's Children is now fully built (units + detachments both complete).
**B89 gained confirmed evidence, not closed**: direct parse-and-diff found Chaos Space Marines,
Death Guard, and Thousand Sons' detachments are still sourced from v1_0 MFM text, with real
already-shipped errors (a DP-cost bug, an enhancement-price bug, six disposition mismatches) — see
B89's body below for detail. Recommended as B89's next data turn, not opened as a new ticket.

**24 open** as of S210 (up from 23 at S209 — B111 opened, nothing
closed; B110 corrected in place, not closed): B111, B110, B109, B108, B99, B98, B97, B103, E28,
B93, B90, B94, B89, B85, B86, B69, B70, B75, P2, P4, E23, B67b, E12, B17. Data-only turn
(Emperor's Children units, D304). `units.json` +23 EC units, `unit_loadouts.json` +23 EC entries
(21 auto-parsed + 2 hand-authored), `wargear_points.json` +1 unit, `datasheet_wargear_abilities
.json` +5 units — all diff-guarded, 0 changed/removed elsewhere in each. New structural assertion
`EC-DATA`. Found and opened **B111** (v1.1 MFM files' `WARGEAR OPTIONS` format broke
`mfm_points_parser.py`'s `--wargear` pass project-wide, not EC-specific — surfaced by EC's
Defiler, the first case where the resulting stale v1_0 pricing is actually wrong). **Corrected
B110** (not executed): Grey Knights has zero detachments in `detachments.json`, so flipping
`built: true` per the original wording would be premature — flagged for Ryan rather than done.

**23 open** as of S209 (up from 22 at S208 — B110 opened, nothing closed):
B110, B109, B108, B99, B98, B97, B103, E28, B93, B90, B94, B89, B85, B86, B69, B70, B75, P2, P4, E23,
B67b, E12, B17. Scoping-only turn (Emperor's Children, D303). No committed file changed.
`EMPEROR'S_CHILDREN_BUILD_SCOPE.md` written — 23 datasheets, zero LEGENDS exclusions, zero engine
gaps found (a first). Loadout parser flagged 2 units, both the same already-solved free-item shape.
Detachments: 10, no unique tags, 4 force-disposition changes v1_0→v1.1. Found and logged **B110**
(`faction_taxonomy.json` stale Grey Knights `built` flag) and located but did not fix B109's
`index.html` render site (would mix engine work into this scoping turn).

**22 open** as of S208 (unchanged count from S207 — B100 closed, B109
opened): B108, B99, B98, B97, B103, E28, B93, B90, B94, B89, B85, B86, B69, B70, B75, P2, P4, E23,
B67b, E12, B17, B109. Data+parser turn (B106-DATA). Both Grey Knights Dreadknights' ranged-weapon
options authored — new classifier `classify_this_model_add_count_choice` in `loadout_parser.py`,
`unit_loadouts.json` and `wargear_points.json` regenerated and diff-guarded (2 units changed in each,
0 elsewhere), new structural assertion `B106-DATA` re-derived from source. **B100 (Grey Knights)
CLOSED — faction fully complete, 25/25 units, zero residual `_parser_flags`.** Baseline reconciliation
at open fixed a stale manifest hash on `SESSION_HANDOFF_207.md` (same self-referential-hash problem as
prior manifest gaps, different symptom). B108's private-repo-push half now confirmed done; public-repo
removal half still outstanding, B108 stays open. Faction-priority census corrected by reading
`units.json` directly: all twelve Adeptus Astartes chapters are already built — Emperor's Children is
the correct next faction, not "the next Adeptus Astartes faction" as the prior two sessions' prompts
assumed. Also logged Ryan's change request as **B109** (My Army Lists page label copy).
**22 open** as of S207 (unchanged count from S206 — B106 closed, B108 opened):
B108, B99, B98, B97, B103, E28, B93, B90, B94, B89, B100, B85, B86, B69, B70, B75, P2, P4, E23, B67b,
E12, B17. Engine-only turn (B106). `index.html` v6.17 → v6.18: `loRollup`'s fixed-1 branch now accepts
a `count` option with `distinct: true`, `replacement_choices` and no `replaces` as a pure addition,
reusing the B101 machinery. Net-new `b106_check.js` (32 assertions), gated in `baseline.sh` and
`pipeline_manifest.py`. Grey Knights fully unblocked — parser change + Dreadknight regeneration next
session. Also this session: baseline reconciled at open found `Thousand_Sons_web.txt` committed to the
public repo (verbatim GW datasheet material, standing-constraint violation) and still absent from the
private source repo — the S206 Ryan action went to the wrong repo. Opened as B108. Cannot fix from
this session (public-repo push scope + read-only private token).
**22 open** as of S206 (down from 23 at S205 — B105 closed; B107 opened
and closed same session, never counted as open): B106, B99, B98, B97, B103, E28, B93, B90, B94, B89,
B100, B85, B86, B69, B70, B75, P2, P4, E23, B67b, E12, B17. Tooling+data turn. B105 (passive
single-model swap classifier) and B107 (new — wargear-allowlist quote-normalisation fix, found
verifying B105's target units) both shipped. `GK` added to `repro_check.py`'s `FACTIONS`;
`unit_loadouts.json` regenerated (25 GK units added, 0 changed elsewhere; repro_check byte-identical).
`wargear_points.json` regenerated using the canonical `FACTION_BY_MFM` file order (4 GK units added, 0
changed elsewhere — a naive alphabetical order was tried first and discarded, same provenance-drift
trap D236 documented for CSM). `E14-2` census updated 75/54 → 90/61. B100 substantially closed; B106
(Dreadknights, engine-scoped) remains open, untouched, correctly the only residual flag left on Grey
Knights. Also this session: resolved a manifest gap (`SESSION_HANDOFF_203.md` confirmed genuinely
unrecoverable, removed from `GUARDED`) and found a second, related gap (`Thousand_Sons_web.txt` never
added to the private source repo's census — Ryan action needed, token is read-only).
**23 open** as of S205 (down from 24 at S204 — B104 closed): B105, B106,
B99, B98, B97, B103, E28, B93, B90, B94, B89, B100, B85, B86, B69, B70, B75, P2, P4, E23, B67b,
E12, B17. Tooling-only turn (B104). `equipped_parser.py`'s `scoped_name2id` rewritten with scope-alias
+ parent-army fallback + propagation. Fixes the insertion-order-dependent `cands[-1]` fallback (D298).
Also corrects a pre-existing gap: 7 AA generic vehicles now gain correct `equipped` composition data.
`unit_loadouts.json` regenerated (no GK in FACTIONS); repro_check byte-identical. B104 assertion added
to `rules_assertions.py`. B100 still blocked on B105/B106 for its loadouts half.
**24 open** as of S204 (up from 21 at S203 — three new tickets opened,
B100 stays open but its units half closed): B104, B105, B106, B99, B98, B97, B103, E28, B93, B90, B94,
B89, B100, B85, B86, B69, B70, B75, P2, P4, E23, B67b, E12, B17. Data-only turn (B100, units half).
`units.json` regenerated with Grey Knights (25 units), diff-guarded at key level against committed —
exactly 25 added, nothing else moved; `abilities.json`/`weapon_abilities.json` regenerated as part of
the same fixed point; `datasheet_wargear_abilities.json` regenerated separately (2 datasheets added).
Confirmed by direct pipeline run (not assumed from the S200 scope doc) that Grey Knights needs no
`Grey_Knights_web.txt` — its six multi-group units gap-fill completely from the final `--datasheets`
pass alone. **Opened B104**: registering Grey Knights exposed a real, pre-existing bug in
`equipped_parser.py`'s `scoped_name2id` — an ambiguous, insertion-order-dependent fallback that
silently corrupted 8 unrelated, already-shipped vehicles (Land Raider and its variants, Rhino,
Razorback, Stormhawk/Stormtalon/Stormraven) the moment Grey Knights' same-named vehicles were appended
after them in `units.json`. `unit_loadouts.json` was **not** regenerated this session — `repro_check`
is deliberately left red, tracing to exactly this one documented cause, until B104 ships. Also opened
**B105** (a passive single-model swap sentence shape `loadout_parser.py` doesn't classify) and **B106**
(a fixed-1-group pure-addition "up to N distinct picks" shape `index.html`'s B101 `distinct` support
doesn't cover) — both found while attempting to author Grey Knights' four flagged units' loadouts;
both left as residual `UNMATCHED` flags, same precedent as Raptors'/Legionaries' pre-B101 residuals.
B100 stays open, now blocked on B104/B105/B106 for its loadouts half; its units half is done.
**23 open** as of S201 (up from 22 at S200 — B101's engine half shipped and
closed, but its data half was split out as B101-data, and B103 was opened): B99, B98, B97, B101-data,
B103, E28, B93, B90, B94, B89, B100, B102, B85, B86, B69, B70, B75, P2, P4, E23, B67b, E12, B17.
Engine-only turn. `index.html` v6.16 → **v6.17**: the new `distinct` flag makes
"you cannot select the same option more than once" enforceable, held at three places (selection path,
renderer, and both `loRollup` branches) so no single omission becomes the hole. Net-new
`b101_check.js`, registered in `baseline.sh` and `pipeline_manifest.py`, with each enforcement point
mutation-tested. **The engine can now express the rule and nothing uses it** — no shipped option
carries the flag, so the three CSM units are as wrong for a player at v6.17 as at v6.16; that is
B101-data (parser emits the flag, then regenerate). Found while looking: selecting the marker string
does not merely look wrong, it adds a weapon named after the rules sentence to the unit (points
unaffected — a rules sentence never matches a priced item). S200's table corrected against the data:
Legionaries `cc_5` is `per_n_models: 5 / max_per_n: 1`, not uncapped. B103 opened for a looser
pre-existing defect deliberately left alone. B100 still blocked, now on B101-data rather than B101.
**22 open** as of S200 (up from 20 at S199 — new B101, B102): B99, B98,
B97, B101, E28, B93, B90, B94, B89, B100, B102, B85, B86, B69, B70, B75, P2, P4, E23, B67b, E12,
B17. Grey Knights scoped (D293, `GREY_KNIGHTS_BUILD_SCOPE.md`) — 25 datasheets, the smallest build
yet, fully self-sourced, only four units needing loadout authoring. D293 also set a standing rule:
always build from the newest MFM available, units and detachments alike. Two defects found while
scoping, neither Grey Knights' fault: B101 (no-duplicate wargear unenforced — live D0 gap in three
shipped CSM units) and B102 (`detachment_parser.py --report` crashes on any gap). Verification-only
session: confirmed the Calgar comma fix has not landed (direct private-repo fetch, not the local copy)
and Chaos Space Marines stays blocked on World Eaters/Emperor's Children. Corrected Grey Knights off
B89's candidate list — it has zero built units at any version, so nothing to migrate — and opened B100
to track its net-new build (needs its own scoping pass first, per the CSM/TS precedent). No data,
parser, or engine files changed this session.
**19 open** as of S197 (unchanged from S196 — B89 advanced, did not close):
B99, B98, B97, E28, B93, B90, B94, B89, B85, B86, B69, B70, B75, P2, P4, E23, B67b, E12, B17. Chaos
Daemons migrated to MFM v1.1 (D290) — B89's third migration, first via direct hand-edit of the Gen-1
root `Unit_Points.csv` rather than a source-file swap (6 points changes: Beasts of Nurgle,
Bloodcrushers, Fluxmaster, Kairos Fateweaver, Lord of Change, Shalaxi Helbane). B94 untouched — none of
CD's six changed units are esc4-shaped. Ticket stays open for the remaining priority-order factions.
`source_manifest.json` needs Ryan to push the matching `Unit_Points.csv` edit to the private
`rd-prime-1357-data-sources` repo (Claude's token there is read-only) — not itself a new backlog item,
but noted as a required action carried forward.
**19 open** as of S196 (unchanged from S195 — B94 and B89 both advanced
but neither closed): B99, B98, B97, E28, B93, B90, B94, B89, B85, B86, B69, B70, B75, P2, P4, E23,
B67b, E12, B17. Death Guard migrated to MFM v1.1 (D289) — B94's second faction (Chaos Rhino now
carries `fourth_plus`) and B89's second migration (5 points changes). Both tickets stay open for the
remaining priority-order factions.
**20 open** as of pre-S194 (up from 17 at S193): B69, B70, B75, B85, B86,
P2, P4, E23, B67b, E12, B17, B89, B90, E28, B93, B94, B96, B97, B98, B99. B97/B98/B99 logged from
Ryan screenshots ahead of S194 (not yet triaged into a decision-log entry): a Grand Coven rule-text
run-on render; B98 — root cause confirmed same session after Ryan corrected an initial mis-scope — a
two-record `unit_loadouts.json` typo ("heliforged" for "Hellforged") on both Daemon Prince of
Tzeentch sizes breaks melee-weapon resolution, data-only fix, XS; and a confirmed engine gap — no
enhancement anywhere modifies a bearer's displayed weapon Strength/Damage, found while checking
Eldritch Vortex of E'Taph specifically.
**17 open** as of S193 (up from 16 at S192): B69, B70, B75, B85, B86,
P2, P4, E23, B67b, E12, B17, B89, B90, E28, B93, B94, B96. B94's **engine turn shipped** (D286,
engine-only): added an optional `fourth_plus` copy-tier and routed all three points sites through
one shared `copyTierPts` helper (≥4th copy → `fourth_plus`, fallback `third_plus`); byte-identical
on current data; Python mirror + assertion `B94-1` pin it single-source (118 assertions, was 117);
`index.html` v6.16. B94 **stays open** — its data turn (fold into B89) and data-side assertion turn
remain. B96 opened (D286): `b87_check`/`b88_check` sit in `baseline.sh`'s always-run block but need
GW sources, so they crash rather than SKIP on an engine-only open without `--data-turn`.
**16 open** as of S192 (down from 17 at S191): B69, B70, B75, B85, B86,
P2, P4, E23, B67b, E12, B17, B89, B90, E28, B93, B94. B95 closed (D285, data+tooling turn):
`faction_taxonomy.json`'s `built` flag was stale for CSM/Thousand Sons and both were missing
`data_army` entirely — both gaps closed together, new assertion `B95-1` added. B94 also decided
this session (Ryan: add the real 4th copy-tier) — stays open, engine turn queued for S193.
**17 open** as of S191 (unchanged count from S190): B69, B70, B75, B85,
B86, P2, P4, E23, B67b, E12, B17, B89, B90, E28, B93, B94, B95. B88 closed (D284, tooling/analysis
turn): `detachment_parser.py` now reads the MFM v1.1 DETACHMENTS layout via the same sniff +
normalization pattern B87 used for points (all 15 v1.1 files parse cleanly, 0 before; v1_0 output
byte-identical); `mfm_reconcile.py` generalized into a real per-faction delta tool across the 10
built-army MFM file pairs (189 adopt-mechanically, 71 investigate-first — `MFM_v1_1_Reconciliation.md`
is B89's work order). B95 opened (D284): `faction_taxonomy.json`'s `built` flag disagrees with
`units.json` for Chaos Space Marines and Thousand Sons.

**17 open** as of S190 (unchanged count from S189): B69, B70, B75, B85, B86, P2, P4, E23, B67b, E12,
B17, B88, B89, B90, E28, B93, B94. B87 closed (D283, tooling turn): mfm_points_parser.py now reads
the MFM v1.1 layout via a per-file sniff + normalization pass, all 15 v1.1 files cost fully (179/179
for SM, 0 before), v1_0 output byte-identical except the two units B87 corrected. B94 added (D283):
the deferred copy-4 tier-schema decision for the 34 units using the
1st-to-3rd/4th+ shape in v1.1 — a "how it behaves" product/schema call plus its engine+data work.
B90's last sub-question answered this session (D283): Legends/Forge-World datasheets a chapter's own
current MFM prices ARE legal roster members — B90 turn 2 now fully unblocked (runs after B88/B89 per
D274 sequencing). One shipped points bug fixed in-flight this turn: Rubric Marines (CSM + TS) was
overcharging every 1st-3rd copy at the 4th+ price (110/200); corrected to 100/190.
**17 open** as of S189 (down from 19 at S188): B69, B70, B75, B85, B86, P2, P4, E23, B67b, E12,
B17, B87, B88, B89, B90, E28, B93. B91 and B92 closed (D282, tooling/doc turn): the two decision-log
files merged into one canonical `40K_Decision_Log.md` (byte-diffed first, every D-number 0–281
confirmed present exactly once); B90's roster mechanism confirmed against `MFM_Black_Templars_v1.1.txt`
directly; B92 closed as a duplicate of D274's already-decided MFM edition policy, with B87 now
confirmed as the real next unblocked step. B90 still has one open sub-question (Legends/Forge-World
datasheets counting as legal roster members).
**19 open** as of S188 (up from 17 at S187): B69, B70, B75, B85, B86, P2, P4, E23, B67b, E12,
B17, B87, B88, B89, B90, B91, B92, E28, B93. Two tickets logged from Ryan reports (D281, doc-only,
no build): E28 (Detachment selection UI placement — right panel, click-to-configure) and B93
(Enhancement/Upgrade eligibility doesn't read the Enhancement's own qualification text; two records
found with no usable qualification text yet). Neither B90 blocker (D279) nor B91 was answered.
**17 open** as of S187 (unchanged from S186): B69, B70, B75, B85, B86, P2, P4, E23, B67b, E12,
B17, B87, B88, B89, B90, B91, B92. Neither B90 blocker (D279) nor B91 was answered, so both stayed
untouched; E23 was the only unblocked, fully-scoped item — its data turn shipped (D280):
`detachment_effects.json`'s fifth kind (`tank_ace`) and six rows, re-verified from source (caught
and fixed a real army-resolution bug in the process), two new assertions. Ticket stays open; the
engine turn (list_store.js state, index.html eligibility hooks) is separate work, not attempted.
**17 open** as of S186 (up from 16 at S185): B69, B70, B75, B85, B86, P2, P4, E23, B67b, E12,
B17, B87, B88, B89, B90, B91, B92. S186 (data turn) banked only an open-reconciliation — `faction_taxonomy.json`
re-serialised to canonical form to clear a red baseline (D278, S185's engine-turn hand-edit left a stray
trailing newline). B90 turn 2 was deferred (D279): source shows it is a pipeline build with a target
contradicted by D276 (source BT=90, not 76) and blocked on the v1_0/v1.1 points-edition question →
**B92 opened** (MFM v1.1 adoption / points currency). Both are Ryan decisions. B90 stays open.
**16 open** as of S185 (up from 15 at S184): B69, B70, B75, B85, B86, P2, P4, E23, B67b, E12,
B17, B87, B88, B89, B90, B91. B90 turn 1 of 3 (engine) shipped S185 (D277): `resolveUnits()` two-tier
mechanism + `roster_mode` flag landed, all eleven chapters flagged `'union'` for now (live behavior
unchanged, still union-leaked); the five Tier-2 chapters flip to `'complete'` in the B90 data turn,
because their `units.json` blocks are source-verified deltas, not baked unions. B91 opened S185 (D277):
decision-log integrity gap — the guarded `40K_Decision_Log.md` is stale (no D276), the live `_v3_0` is
unguarded and diverged. **15 open** as of S184 (up from 14 at S183): B69, B70, B75, B85, B86, P2, P4, E23, B67b, E12,
B17, B87, B88, B89, B90. SM-family chapter roster bug found and scoped S184 (D276, Ryan-flagged):
`resolveUnits()` unions the generic Adeptus Astartes pool into all `is_subfaction` chapters without
distinguishing vanilla (correct) from dedicated-MFM (wrong) chapters — five chapters currently leak
illegal units (BT alone: 90, including every Librarian and 11 other-chapter characters). B90 opened
ahead of all further faction work; priority order otherwise unchanged. **14 open** as of S183 (up from 11 at S182): B69, B70, B75, B85, B86, P2, P4, E23, B67b, E12,
B17, B87, B88, B89. MFM v1.1 intake S183 (D274, doc-only): GW published a points update; 15 v1.1
captures banked in the private repo (all built armies + Emperor's Children + four extra), custody
checked. The current parser reads zero costs from the new layout, so a refresh arc is opened — B87
(parser v1.1 layout, tooling) → B88 (reconciliation reports) → B89 (per-faction adoption) — and
sequenced ahead of the E23 build turn, whose D273 pool counts get re-verified after adoption. Intake
policy (GW-version filenames, keep all versions, targeted capture, manifest-recorded per-faction
versions, format-sniff parser) recorded in D274. **11 open** as of S182 (unchanged from S181): B69, B70, B75, B85, B86, P2,
P4, E23, B67b, E12, B17. E23 data turn done S182 (D273, data-only): all four source facts confirmed
across all six armies — wording identical (one shared SM detachment), carve-out is a precise
`Fly`/`Walker`/`Drop Pod`/`Fortification` exclusion predicate (not "most Vehicles"), "up to three" cap
holds, six keys confirmed; per-army eligible pools resolved (Blood Angels 17, the other five 16). E23
no longer blocked — build turn next. E23 scoped S181 (D272, analysis-only): mechanism decided (fifth
`detachment_effects.json` kind for the detachment-scoped facts + a purely-additive `list_store.js`
pick array for player selections, no version bump), revalidation decided by `recomputeWarlord()`
precedent (continuous silent drop, no Muster-phase gate). Corrected an inherited miscount — the
schema has four effect kinds today, not the "sixth" a prior document claimed; Tank Ace would be the
fifth. Still blocked on a data turn to confirm exact wording/cap across all six armies. No ticket
closed — scoping only. **11 open** as of S179 (down from 12 at S178): B69, B70, B75, B85, B86, P2,
P4, E23, B67b, E12, B17. E27 shipped S179 (D270, UI-only): `renderDetail`'s attach-panel heading/hint
and `leaderSectionHtml`'s modal heading now read `leaderAbilityName` instead of a hardcoded "Leader"
string; two other candidate sites (list-panel row, JSON export) checked and found to need no change.
`index.html` v6.13 → v6.14. **12 open** as of S178 (down from 13 at S177): B69, B70, B75, B85, B86, P2,
P4, E23, B67b, E12, B17, E27. E26 shipped S178 (D269, engine-only): `permitsCoLeader` rewritten to
enforce one-Leader-one-Support stacking with the four D268 requirements (bare CHARACTER Support pairs
with any Leader; DG `co_leader_any` second-Leader path; Huron→MotM cross-reference; same-type cap).
`leaderAbilityName` added to the allUnits view object. Assertion E26 added (75/75 tier-A, 112 total).
`index.html` v6.12 → v6.13. **13 open** as of S177 (unchanged from S176): B69, B70, B75, B85, B86, P2,
P4, E23, B67b, E12, B17, E26, E27. S177 (D268, analysis-only) re-scoped E26 from source — no ship,
no data change: the CSM "data gap" the S176 handoff implied does not exist (MoE correctly typed Support
per D192+D267's MFM-wins rule, footer cleared by B73), so E26 is now **engine-only, no data dependency**;
the deferred D144 CSM `co_leader_any` population resolves as unnecessary. E26 count unchanged (re-scoped
in place). **13 open** as of S176 (up from 12 at S175): B69, B70, B75, B85, B86, P2,
P4, E23, B67b, E12, B17, E26, E27. B73 shipped S176 (D267, data-only) — MFM made source of truth for
attach eligibility; two S175 assumptions corrected against source before building (Support is the
same attach mechanic as Leader; the engine gates on the eligible list, not the ability name). Ryan's
three stipulations became new engine/UI tickets E26 (one-Leader-one-Support stacking + exceptions)
and E27 (popup/output Leader-vs-Support wording). Wardens of Ultramar carved out of B73 as the first
MFM/datasheet conflict (MFM 6 vs printed 3), handed to B70. **12 open** as of S175 (unchanged from S174):
B69, B70, B73, B75, B85,
B86, P2, P4, E23, B67b, E12, B17. B70/B73 decided by Ryan S175 (D266) — no longer blocked on a
product call, but re-deriving B73's mechanism from source found the fix bigger than S170's audit
assumed (the parser has no `LEADER`-block handling at all today); both need a scoping/build turn,
not a same-session patch. **12 open** as of S174 (down from 13 at S173): B69, B70, B73, B75, B85,
B86, P2, P4, E23, B67b, E12, B17. B76 shipped S174 (D265, tooling) — five versioned docs renamed,
content unchanged. A manifest-hash mismatch on `SESSION_HANDOFF_172.md` was also found and
reconciled at open (D264) — not a backlog ticket, recorded in the decision log only.

**13 open** as of S173 (down from 14 at S172): B69, B70, B73, B75, B76,
B85, B86, P2, P4, E23, B67b, E12, B17. B84 closed S173 (D263, tooling, shipped) — the converter's
KNOWN LIMITATION note no longer names a page type it doesn't own. B85 not closed — a diagnostic
was added but the root cause needs a real converter run to confirm; still open.

**14 open** as of S172 (up from 11 at S171): B69, B70, B73, B75, B76, B84, B85, B86, P2, P4, E23,
B67b, E12, B17. B75 resized and its diagnosis corrected (D262); B84/B85/B86 filed as new tickets
from the same full-pack-run finding.

**11 open** as of S171 (down from 12 at S169/S170): B69, B70, B73, B75,
B76, P2, P4, E23, B67b, E12, B17. B77 closed S171 (D261, audit-only, no code/data shipped) — its
S159 diagnosis was already stale: the six Scintillating Legions carriers already carry the faction
keyword in `units.json` and it already renders in the UI, so there was nothing to build.

**12 open** as of S170 (unchanged from S169): B69, B70, B73, B75, B76,
B77, P2, P4, E23, B67b, E12, B17. B70/B73 audited S170 (D260, audit-only, no code/data shipped):
one root mechanism found in `mfm_points_parser.py`'s Leader-list backfill (blind to the MFM's
own LEADER vs. SUPPORT distinction, plus a one-line block-boundary over-read). B70 looks like
not-a-bug — Wardens of Ultramar has no Leader ability anywhere in source; its real ability is an
unbuilt "join" mechanic, not Leader-attach. B73 confirmed systemic across all 13 built LEADER-
typed Epic Heroes, same cross-chapter pattern on every one; whether Wahapedia's broader
per-character list or the MFM's narrower current list should govern is a roster-wide
rules-legality call, left to Ryan. Neither ticket closed; both need a scope decision before any
build. **12 open** as of S169: B69, B70, B73, B75, B76, B77, P2, P4, E23, B67b, E12, B17. B72 and B80
shipped S169 (D258, engine-only): `index.html` v6.11 → v6.12. B72 — the Outrider Squad's Invader ATV
(the only `non_consuming` optional model group in the data) was offered only at size 6 because
`loOptMax` ran the headroom clamp on it; headroom is 0 at the 3-model bracket. Fixed to exempt
`non_consuming` groups, matching the exemption `loGroupCounts`/`loOptHeadroom` already carry. B80 —
the combined attached-unit popup rendered `buildModalConfigured` twice with hardcoded section IDs, so
the bodyguard's chevron toggled the leader's section; fixed with a per-member `idScope`. `b72_check.js`
added (21 checks) and guarded; `rules_assertions.py`'s B7b render assertion updated to the new
signature and extended to police the scoping. **14 open** as of S168: B69, B70, B72, B73, B75, B76, B77, P2, P4,
B80, E23, B67b, E12, B17. B81 shipped S168 (D257, tooling-only): `pipeline_manifest.py` gained
`--freshness-check`, verifying only the decision log and the latest handoff against the manifest as
the last command of session close, converting D251's ordering rule into an automated check rather
than a remembered one. **15 open** as of S167: B69, B70, B72, B73, B75, B76, B77, B81, P2, P4,
B80, E23, B67b, E12, B17. B81 opened S167 (D256, tooling-only): manifest hashes for two guarded
files went stale between write and session-close text finalization, third occurrence of the same
defect class as D239; content unaffected, manifest reissued clean, ticket filed to automate the
check. **16 open** as of S164: B69, B70, B71, B72, B73, B75, B76, B77, E25,
P2, P4, B80, E23, B67b, E12, B17. Thousand Sons tooling turn shipped S164 (D253, tooling-only):
`TS-3` added to `rules_assertions.py`, asserting `units.json` carries all 34 real current-edition
Thousand Sons units, mirroring `CSM-1`. No `CSM-3` equivalent added — `TS-2` (S160/D248) already
asserts zero TS detachments carry `text_source: none`, the stronger and correct shape given the
faction pack covers all three MFM-only detachments' text. No backlog ticket opened or closed; this
closes the Thousand Sons build (`THOUSAND_SONS_BUILD_SCOPE.md` turns A/B/C/tooling all shipped).
Thousand Sons turn B shipped S163 (D252, data-only):
`unit_loadouts.json` +34 TS entries (309 total, additive-only, diff-traced clean), `wargear_points.json`
+1 entry (TS's own Defiler, `000001030` — same class of gap D236 found for CSM: an MFM-priced wargear
swap silently free until a loadout entry exists). `repro_check.py` registered TS (`FACTIONS`,
`WEB_PASSES`), mirroring the other six factions. `E14-2`'s stale hardcoded count corrected 65/45 ->
75/54 to reflect the new qualifying free-add seeds TS's roster surfaces. No backlog ticket opened or
closed; TS build progress is tracked in `THOUSAND_SONS_BUILD_SCOPE.md`, same convention as CSM's build.
E25 (Force Disposition selection) designed and filed S162 (D251,
doc-only turn) — data already fully retained, engine work only. Thousand Sons turn A shipped S161 (D250, data-only): `units.json` +34
(362 total), the six Scintillating Legions carriers TS-priced and tagged; closes **E24** (allied
unlock now enforced) and **B78** (both Battleline rows shipped, scoped to the sole TZAANGORS-
keyword datasheet). B61's four census assertions generalised to cover both Death Guard and
Thousand Sons rather than forked into TS-specific siblings.
**12 open** as of S157: P2, P4, E23, E12, B17, B61, B67b, B69, B70, B71, B72, B73 —
B69–B73 logged Ryan-side S152, not yet scoped or reproduced by Claude. CSM cult-troop cross-file
points shipped S157 (D240, data-only): `units.json` +4 (58/58 roster complete), `unit_loadouts.json`
+4, `CSM-1`/`E14-2` updated; closes `CSM_BUILD_SCOPE.md` §4 — CSM's build is now complete except for
M2 (Ryan, no Claude action). B74 CLOSED S156 (D239) — Chaos
Cult BATTLELINE grant now has its `detachment_effects.json` row; closes the CSM tooling arc from
`CSM_BUILD_SCOPE.md` §8 in full, full body moved to `BACKLOG_ARCHIVE.md`. CSM tooling turn shipped S155
(D238, tooling-only): three new CSM census assertions (roster 54/58, detachment count 17, no-prose
detachments), E4b-3's collision census corrected 29/5 → 30/6 (CSM's Warp-Fuelled Thrusters), manifest
reissued. CSM detachment build shipped S154 (D237, data-only):
`detachments.json` +17 CSM detachments (160 total), diff-traced clean against the committed file;
closes the CSM build arc and unblocks M2. CSM loadout defaults shipped S153
(D236, data-only): `unit_loadouts.json` +54 CSM entries, `wargear_points.json` +2 entries (a second gap
surfaced by the first); nothing else moved. B68 closed S152 (D235, engine); S150 confirmed `--fetch` live-green
against the real repo (D233, tooling-only, verification only); nothing closed or added, M1 unblocked.
Thousand Sons build scoped S158 (D241, tooling/scoping-only): `THOUSAND_SONS_BUILD_SCOPE.md` written
— 34-unit current roster, 9 current detachments, fully self-sourced points (no cross-file gap, unlike
CSM), one blocking gap (no `Thousand_Sons_web.txt` for loadout defaults — needs Ryan to source it).
No backlog ticket opened or closed; the build itself is tracked in the scope doc, same convention as
CSM. Also fixed a real B15-9 drift found at baseline open: S157 added 4 units to `units.json` but
never regenerated `datasheet_wargear_abilities.json` against them — reran the parser, +3 entries,
additive only, no ticket needed (a session-open reconciliation, not a standing bug).
M2 dress rehearsal shipped S158 (D242, same session): Ryan's private sources repo and read-only token
verified live — full fetch/unpack/byte-compare of all 70 files against `source_manifest.json` passed
clean. Found and fixed a real bug: `baseline.sh`'s private-fetch URL was hardcoded to a nonexistent
repo name. Deletion of the 71 area-resident source files is Ryan's remaining step (screenshot-verified
protocol), not yet done.
S149 was M0 (D232, tooling-only): the new fetch-open path built and proven; nothing closed or added. S147 was
CSM turn A (D229, data-only): 54 self-priced units shipped, diff-traced clean. It also opened B68
(D230): building the CSM loadout-defaults pass surfaced a real parser bug (name-keyed matching bleeds
across Death Guard/CSM's seven shared generic Chaos vehicle names), deferred to its own engine/parser
turn — `unit_loadouts.json` and `repro_check.py` deliberately untouched. CSM is faction-priority
roadmap work tracked in `CSM_BUILD_SCOPE.md`, not a backlog ticket in its own right. B67 CLOSED S145
(D225) — both GW-derived files confirmed removed from the repo's HEAD; D223's "single commit" premise
was wrong (249 commits), so a full history purge is a separate, optional action, filed as B67b.
S145 also regenerated `unit_loadouts.json` (D225) after verifying a Dark Angels data fix and a new
Space Wolves file against the real pipeline — no ticket, routine data maintenance.
B61 logged Ryan-side (combined-popup expand arrow, see below). E21 closed S139 (D218) — piece 3, the
stranded-allied roster warning, shipped.

## Open Items


### B110 — `faction_taxonomy.json` still shows Grey Knights as `built: false` — **NEW S209; data; XS**
Found while scoping Emperor's Children. `units.json` confirms Grey Knights is fully built (25/25
units) and B100 closed at S208, but `faction_taxonomy.json`'s Imperium group still carries
`{'name': 'Grey Knights', 'built': False}` — nobody flipped the flag when the faction shipped. Not
currently causing a visible bug (checked: no UI or check harness was found reading this field to
gate Grey Knights specifically), but it's a stale data point that could produce a false-negative in
some future faction census the way S206/S207's stale "next Adeptus Astartes faction" prose did. Fix
is a one-line flag flip; can ride with any other data turn.

**Correction, S210:** the S209 claim above ("no UI... was found reading this field to gate Grey
Knights specifically") was checked incompletely. `index.html` reads `f.built` generically to gate
every faction's selectability (`opt.disabled = !f.built`), so it DOES gate Grey Knights the same as
any other faction — that part of the original investigation missed the actual read site. More to
the point: `detachments.json` was checked directly this session and has **zero** Grey Knights
entries. Flipping `built: true` now, as the ticket originally recommended, would let a player select
Grey Knights and reach an empty detachment picker — a broken list-building state, not a cosmetic
stale flag. **Not a one-line flip.** This ticket is correct that the flag is stale, but the fix is
blocked on Grey Knights getting its own detachments build, not just a data toggle. Left open,
`built: false` unchanged, until detachments ship.

### B111 — `mfm_points_parser.py`'s `--wargear` pass is blind to v1.1 `WARGEAR OPTIONS` text
— **NEW S210; tooling/engine; found while building Emperor's Children units**
Sourcing EC's Defiler wargear from `MFM_Emperors_Children_v1.1.txt` (per D293's "build from newest
MFM" rule) returned zero items. Root cause, confirmed directly against multiple files: every v1.1
MFM file dropped the leading bullet character (`•`) from `WARGEAR OPTIONS` lines that v1_0 files
have (checked `MFM_Grey_Knights_v1.1.txt`, `MFM_Death_Guard_v1.1.txt`, `MFM_Thousand_Sons_v1.1.txt`,
`MFM_Chaos_Space_Marines_v1.1.txt` — all bullet-less, universal not EC-specific).
`mfm_points_parser.py`'s `WARGEAR_RE` regex hard-requires that leading bullet, so the `--wargear`
pass has been silently unable to read v1.1 wargear pricing for every faction since the v1.1
migration. Harmless everywhere else purely by coincidence — every other faction's wargear item
happens to cost the same in v1_0 and v1.1, so the stale v1_0 sourcing still produces the right
number. EC's Defiler is the first case where the two versions genuinely disagree (10 vs 15 pts per
item), which is what surfaced the gap. S210 shipped EC's Defiler wargear at the stale v1_0 price (10
pts), consistent with its already-shipped siblings (DG/TS/CSM Defilers, all currently also stuck at
v1_0 pricing for this same pre-existing reason), rather than leaving the items unpriced or
hand-patching a number outside the pipeline. Fix: update `WARGEAR_RE` to accept both the bulleted
v1_0 format and the bullet-less v1.1 format. After the regex fix, the wargear pass should be re-run
across every already-shipped faction (not just EC) and diff-guarded, in case another v1.1-only price
change is hiding behind the same gap elsewhere — don't assume EC's Defiler is the only casualty.

### B109 — "My Army Lists" page: replace "target ####" label with "#### Points" — **NEW S208
(Ryan-reported); engine; XS; render site now located**
Render site found (S209): `index.html`'s `renderMyLists()`, the line
`const tgt = r.points_target ? ('target ' + r.points_target) : '';`. One-line change to
`(r.points_target + ' Points')` (or similar). Not made this session — would mix an engine edit into
a scoping-typed turn. Standalone engine-only turn, or ride with the Emperor's Children detachments
build.

### B108 — `Thousand_Sons_web.txt` committed to the public repo (GW-derived) AND still absent from the private source repo — **NEW S207 (D301); RYAN ACTION; CRITICAL (compliance)**
`repo_check.py` at S207 open flagged `Thousand_Sons_web.txt` in the public repo. Verified against a
direct fetch of the public tarball (`codeload.github.com/rd-prime-1357/40k-army-builder/tar.gz/main`):
the file is genuinely in the repo. Content is verbatim GW datasheet material — unit profiles, weapons,
abilities — the same class the standing constraint excludes ("faction web composition files"). Also
verified against the private repo via the read-only token: the file is still not there,
`source_manifest.json` still doesn't list it, so S206's Ryan action (push to the private repo) was
not completed and the file appears to have gone to the public repo instead. Two distinct actions
required, both by Ryan (private-repo token is read-only, public-repo push isn't in Claude's scope):
(1) remove `Thousand_Sons_web.txt` from the public repo — at minimum from HEAD; ideally scrub git
history via `git filter-repo` since the content shouldn't have been public; (2) push
`Thousand_Sons_web.txt` to the private `rd-prime-1357-data-sources` repo and regenerate
`source_manifest.json`. Until (1) lands, `repo_check` will keep flagging CRITICAL on every session
open; until (2) lands, any data-turn `--fetch --data-turn` open will fall back on the same
project-mount-only stopgap S206 and S207 both used.

### B99 — Enhancement "Eldritch Vortex of E'Taph" (+1 Strength/Damage to bearer's Psychic weapons) has no effect on displayed weapon stats — **NEW (Ryan-reported, pre-S194); engine/data; scope TBD; live D0-adjacent gap**
Ryan-reported via screenshot (Daemon Prince of Tzeentch with Wings). Checked before logging:
`detachments.json` confirms the enhancement's text is present and correctly captured — Thousand
Sons | Grand Coven, 35 points, "Add 1 to the Strength and Damage characteristics of Psychic weapons
equipped by the bearer." `detachment_effects.json`'s own `_meta` block states its five effect kinds
(`battleline`, `forbid`, `unlock`, `warlord`, `tank_ace`) are muster-time army-construction effects
only — none of them represent an equipped item modifying a weapon's printed characteristics.
Searched `index.html` directly for any site that reads an enhancement and adjusts a weapon's
strength/damage field: none found. This is not a one-off miss on this one enhancement — no
stat-bonus-to-equipped-weapon enhancement is wired into the engine at all, so any other army with a
similarly-shaped enhancement almost certainly shares the same gap. Needs a scoping turn: a census of
how many built armies carry a stat-modifying enhancement, whether this becomes a new
`detachment_effects.json` kind or its own table, and how the weapon-profile popup should read a
live-computed value against the base printed one.

### B98 — Daemon Prince of Tzeentch (both sizes): melee weapons don't render at all; a mismatched wargear label shows instead — **NEW (Ryan-reported, pre-S194); data; XS; root cause confirmed**
Ryan-reported via screenshot (Daemon Prince of Tzeentch with Wings) and corrected my first pass at
this ticket — the melee-weapons-as-table format is the app's normal, working pattern (Tzaangors'
popup shows it correctly), so this was never a design question. Checked source directly: the unit
does carry two melee weapon profiles in `units.json` — "Hellforged weapons – strike" and "Hellforged
weapons – sweep" — but `unit_loadouts.json`'s `default_wargear` for this unit reads `"heliforged
weapons"` (missing the second L, lower case, no "– strike"/"– sweep" suffix). That string doesn't
match either weapon name, so nothing resolves to the MELEE WEAPONS table; instead the popup falls
back to showing the unresolved string as a generic Other Wargear line, which is exactly the
"Heliforged weapons ×1" line in the screenshot. Confirmed scope: exactly two records carry the typo
— `000001036` (Daemon Prince of Tzeentch) and `000004120` (Daemon Prince of Tzeentch with Wings);
the other four Hellforged-weapons-bearing records in `unit_loadouts.json` spell it correctly. **Fix
is data-only**: correct both `default_wargear` entries to `"Hellforged weapons"` (or however the
resolver expects multi-profile melee defaults to be named — check a correctly-working record, e.g.
the non-Thousand-Sons Daemon Prince variants, for the exact convention before writing the fix) and
re-verify against the parser, not hand-edited.

### B97 — Grand Coven detachment rule text renders as a run-on wall of text — **NEW (Ryan-reported, pre-S194); engine/UI or data; scope TBD**
Ryan-reported via screenshot. Confirmed in `detachments.json`: the `Thousand Sons|GRAND COVEN`
`rule_text` field concatenates its three named sub-abilities directly against the surrounding
sentence with no delimiter — "...once per battle.Imbued ManifestationAdd 6\" to the Range..." and
"...Range characteristic...Psychic MaelstromEach time..." both run name-into-text and
text-into-name with no space or line break. Any renderer that does not insert its own break where
the sub-ability names sit reproduces exactly the wall-of-text look in the screenshot. Root cause
(source text lacking separators vs. a renderer that should be inserting breaks and isn't) not yet
diagnosed. Also not yet checked: whether other WHEN/TARGET/EFFECT- or multi-option-style rule texts
elsewhere in the file share the same missing-separator pattern — worth a scan across all `rule_text`
and stratagem `description` fields in the same turn rather than fixing this one row in isolation.

### E28 — Detachment selection: move from centre-list widget to right-panel configuration (Force Disposition included) — **NEW S188 (D281); Ryan-raised; engine/UI; M**
Ryan's question: selected Detachments and Force Disposition currently render as an always-visible
block inside the centre "Army List" panel (`renderSelectedDetachmentsHtml`, the `fdisp-picker`
element), rather than through the click-to-configure pattern used for every unit (left panel picks
it, centre lists it, right "Unit Options" panel configures it once clicked). He asked whether
Detachments should follow that same pattern, with Force Disposition "listed and selected under the
Detachments."

Checked against the original UI decision before answering (D192 item 5, `E1_DETACHMENT_SCOPE.md`
§5): the plan was left-panel picker (unchanged), centre-list rows (unchanged), and **an info
control per row opening rule text/enhancements/stratagems as collapsible detail** — closer to a
click-to-expand pattern than what shipped. E25 (Force Disposition, D251/D254) added its own
always-on selector at the top of the centre list instead of using that info-control path, which is
why today's layout doesn't match either the original plan or the unit mechanic.

**Recommendation given to Ryan: yes, move it, with one adjustment.** Keep detachment rows in the
centre list — name and DP cost need to stay visible without a click, which is the one thing the
current widget gets right. Clicking a detachment row switches the right panel to a "Detachment
Options" view, the same way `selectListEntry` does for units; that view is where Force Disposition,
rule text, and enhancement browsing live. The one departure from "listed and selected under the
Detachments" as literally stated: Force Disposition is a single value governing the whole
detachment *selection*, not a per-row property (two detachments can be selected at once; one Force
Disposition applies to both) — so the selector should attach to a "Detachments" group-level
header/state, not repeat under each individual row, or it will read as belonging to whichever
detachment happens to be clicked. Everything else in Ryan's framing holds.

**Mechanism note, not yet designed in detail:** the right panel currently switches on a numeric
`listId` (`selectListEntry`); detachment rows are keyed by string (`army|name`), so this needs new
selection state distinguishing "a unit is selected" from "the Detachments group is selected," plus
a render branch in the right-panel path. Comparable in size to E1c's original build. A scoping
session should confirm whether per-unit enhancement assignment (unaffected by this move) needs any
UI adjustment once Detachments get their own detail view.

### B93 — Enhancement/Upgrade eligibility: engine checks Character-vs-not, not the Enhancement's own qualification requirement — **NEW S188 (D281); Ryan-flagged; engine+data; L; spans sessions; live D0 gap**
Ryan's report: every Enhancement's description begins with the specific unit/keyword requirement to
take it (e.g. a Phobos-armoured Character, "any Adeptus Astartes Character," "any Adeptus Astartes
Vehicle"), and by rule an Enhancement can only be taken by a Character unless stated otherwise.
`enhancementTypeEligible()` (`index.html`) does not read that requirement at all — it hard-codes
two cases: `is_upgrade === true` → eligible for **any** unit type with no further check,
`is_upgrade === false` → eligible only if `unit_type === 'Character'`. Checked against
`detachments.json` (607 enhancement records) before logging: the type-vs-Character split is right
as a default, but the specific qualification is real, present in the data, and unenforced in both
directions —

1. **Upgrades (`is_upgrade: true`) currently have zero type restriction.** Example: Fulguris Task
   Force's *Bellicose Weapon Spirits* names "SPEEDER unit only" in its own text, but the engine's
   `isUpgrade ? true : …` allows it on any unit in the army. This is the wider of the two gaps — it
   is live and reachable today, not gated behind unbuilt work.
2. **Regular Enhancements narrow past "any Character."** Several name a specific keyword,
   sub-type, or even a single named unit rather than "any Character" — Anvil Siege Force's
   *Indomitable Fury* ("GRAVIS model only"), Death Guard's *Cornucophagus* ("Lord of Poxes only"),
   Space Wolves' *Iron Resolve* ("ADEPTUS ASTARTES TERMINATOR model only"). The blanket Character
   check currently over-admits all of these to any Character in the army, not just the named one.

**Correction to the reported pattern, checked before scoping further:** the qualification clause is
not reliably the first sentence of `description`. Sampled records show it typically follows one
sentence of flavour text (`Bellicose Weapon Spirits`, `Blackwing Shroud`, `Bombast Omnivox` all
follow this shape), and two records currently carry no usable qualification text at all:
`Thousand Sons | RUBRICAE PHALANX | Stave Abominus` has an **empty** `description`, and
`Chaos Daemons | SHADOW LEGION | Leaping Shadows`'s description is just the enhancement's own name
repeated, with no rule text. A first-sentence parsing heuristic would misfire on real records today
— a source pass across all 607 is needed before either gap is built.

**Not scoped for build.** This needs an analysis turn across the full record set before a
mechanism is chosen — likely a new structured field (qualification keyword/unit-type/unit-name,
captured at the pipeline stage the description text already goes through) plus an `index.html`
change to `enhancementTypeEligible()`/`canAssignEnhancement()` to consume it. Sized L, spans
sessions, same shape as the B70/B73 and B90 clusters. Priority relative to the current faction-build
queue is a sequencing call, not made here.

### B90 — SM-family chapter rosters: fix the union-vs-complete bug — **NEW S184 (D276); Ryan-flagged; engine+data; L; spans sessions; blocks further faction work**
`resolveUnits()` in `index.html` unions the full generic Adeptus Astartes pool into every
`is_subfaction` chapter, with no distinction between the six vanilla chapters (no dedicated MFM,
union is correct) and the five dedicated-MFM chapters — Black Templars, Blood Angels, Dark Angels,
Deathwatch, Space Wolves — whose own MFM file is a complete, self-contained roster that should never
be unioned with generic. Confirmed directly against `MFM_Black_Templars_v1.1.txt`: 76 units total,
including generic units BT can still field at BT's own prices, with no reference back to
`MFM_Space_Marines.txt`. Current behaviour leaks 90 generic units into BT alone that its own MFM
excludes — every Librarian variant (Black Templars take no Psykers) and 11 other-chapter named
characters (Tigurius, Vulkan He'stan, Shrike, Kor'sarro Khan, and others). A live D0 violation: these
are currently selectable in list building. The other four dedicated-MFM chapters are assumed to
share the same complete-file shape by construction but each gets confirmed against its own MFM
during the rebuild, not assumed from the BT case.

**Scope, three turns, strictly separated per turn-typing:**
1. **Engine turn:** add a `roster_mode` (or equivalent) flag per chapter distinguishing `'complete'`
   (the five) from `'union'` (the six vanilla + generic); `resolveUnits()` branches on it instead of
   unioning unconditionally.
2. **Data turn:** rebuild the five Tier-2 chapters in `units.json` directly from their own MFM files
   (Black Templars, Blood Angels, Dark Angels, Deathwatch, Space Wolves) rather than as override
   deltas against generic; re-verify `unit_loadouts.json` and `wargear_points.json` entries for any
   unit whose leader/support attach list or wargear changes shape once sourced natively.
3. **Assertion turn:** pin the fix — no Tier-2 chapter roster contains a unit absent from its own
   MFM file; existing chapter-exclusivity assertions (D221/D222 pattern) extended to cover roster
   membership, not just detachment restrictions.

Acceptance: all five Tier-2 chapters' rosters match their MFM files exactly (unit-for-unit); the six
vanilla chapters and generic Space Marines unchanged; baseline stays green; new assertion in the
tier-A set. D276 has full source verification detail for Black Templars; the other four are checked
fresh at rebuild time.

**PROGRESS — turn 1 of 3 shipped S185 (D277).** The engine mechanism is in: `resolveUnits()` branches
on `roster_mode`, `'complete'` returns the chapter's own block only (structurally isolated from the
generic pool and the point-override map — proven by `b90_check.js`), everything else takes the
unchanged union path. `roster_mode` added to all twelve Adeptus Astartes taxonomy records; presence
pinned by `rules_assertions.py` B90-1 (tier A). index.html v6.14 → v6.15.
**Correction to the turn plan:** turn 1 flags **all eleven** chapters `'union'`, not the five
`'complete'`. Their `units.json` blocks are source-verified deltas (BT 18, BA 15, DA 16, DW 10, SW 21),
not baked unions, so `'complete'` now would strip the generic units they legitimately field. The five
flip to `'complete'` in **turn 2 (data)**, atomically with the MFM-complete rebuild — so the flag flip
moves from turn 1 into turn 2. Turn 2 must also update `resolved_pool()` in `rules_assertions.py` (the
Python mirror of `resolveUnits()`, still union-only) to add complete-mode, or the mirror silently
diverges from the engine. Turn 3 (assertion) unchanged. Live behavior after turn 1: still union-leaked,
unregressed — the D0 gap persists exactly as before until turn 2.

**TURN 2 DEFERRED — S186 (D279); BLOCKED on two Ryan decisions.** Turn 2 was scoped as a mechanical
data rebuild; source check this session shows it is a pipeline build with an ill-defined target, so it
was not attempted (no half-build). Two blockers, both points-legality precedent (Ryan): (1) **points
edition** — the pipeline pins v1_0 MFMs, but unadopted v1.1 files carry corrected points (rosters are
identical across versions; only points differ), so the tool ships stale points; a rebuild bakes in one
edition's points and adopting v1.1 is a faction-wide refresh → **B92**. (2) **roster target** — direct
source count is BT=**90** (18 chapter-specific + 72 curated-generic), not the **76** D276/the prompt
state; the acceptance figure is contradicted by source and must be corrected before an assertion pins
it. Source *does* confirm D276's legality model (BT lists 0 Librarians; chapter rosters genuinely
differ). Also noted: no existing pipeline path emits a complete per-chapter roster — turn 2 needs a new
build path, not a data edit. Turn 2 resumes once both decisions are settled; turn 3 (assertion) follows.

**MECHANISM CONFIRMED AGAINST SOURCE — S189 (D282).** Read `MFM_Black_Templars_v1.1.txt` directly:
its unit list carries no Librarian entry at all — not "no BT override of the generic one," genuinely
absent. Confirms the turn-2 plan is right and rules out a tempting shortcut: a build that unions the
full generic pool and swaps in named overrides would still leak the generic Librarian in, since
there's no BT-specific entry to override it with. Each Tier-2 chapter's `units.json` block must be
built as exactly what its own MFM lists, with no reference to the generic pool. **Ryan confirmed
S189:** roster target is the source-verified count (~90 for BT, not 76) and MFM edition should never
lock to one version — both already match D274's intake policy and this turn's rebuild target.
**Still open:** whether Legends/Forge-World datasheets present in a chapter's MFM (Astraeus,
Thunderhawk for BT) count as legal matched-play roster members — **ANSWERED S190 (D283): yes.**
Legends/Forge-World datasheets that a chapter's own current MFM prices ARE legal roster members for
that chapter, sourced from the current MFM (never locked to one edition). Verified against source:
Astraeus and Thunderhawk Gunship are priced identically to ordinary units in all five Tier-2 chapter
MFMs, with no distinguishing marker. Note for the turn-2 build: both are currently excluded app-wide
by `wahapedia_transform.py`'s `source_is_excluded` (their Wahapedia source is tagged "…(Forge
World)", which the exclusion bundles with genuine Legends content — two different source categories
the code cannot currently tell apart). Turn 2 must carve these out of that exclusion for the five
chapters. B90 turn 2 is now fully unblocked on decisions; it still runs after B88/B89 per D274's
sequencing.

### B94 — copy-4 tier schema: represent "1st-to-3rd / 4th+" pricing — **NEW S190 (D283); DECIDED S192 (D285): add the real tier; ENGINE TURN SHIPPED S193 (D286); PIPELINE-EMIT TURN SHIPPED S194 (D287); DATA TURN 1/N SHIPPED S195 (D288); DATA TURN 2/N SHIPPED S196 (D289); product+engine+data; M; data turn folds into B89**

**Data turn, second faction, shipped S196 (D289).** Death Guard regenerated from `_v1.1.txt` with
`--emit-fourth-plus`: Chaos Rhino (1 of the scope's 34 units) now carries a real `fourth_plus` value in
committed `units.json` (75/85). 31 units across the remaining priority-order factions still need their
own migration turn before this ticket's data half closes; the data-side assertion (below) still needs
writing once more factions have landed.

**Data turn, first faction, shipped S195 (D288).** Thousand Sons regenerated from `_v1.1.txt` with
`--emit-fourth-plus`: Rubric Marines and Chaos Rhino (2 of the scope's 34 units) now carry real
`fourth_plus` values in committed `units.json` (110/200 and 90 respectively).

**Engine turn shipped S193 (D286).** Added an optional `fourth_plus` tier to `points.sizes[*]` and
routed all three points sites (`ptsForEntry`, `addUnitFromRoster`, size-selector) through one shared
`copyTierPts(sizeEntry, prior)` helper: copies 1–3 → first/second/third_plus; the 4th copy onward →
`fourth_plus` when present, falling back to `third_plus` when absent. Byte-identical on the current
3-tier data (no committed row carries `fourth_plus` yet) — verified by executing the real JS helper.
Python mirror `Sources.copy_tier_pts` + assertion `B94-1` pin the ladder single-source and hold JS↔
Python in lockstep (118 assertions). `index.html` v6.16.

**Pipeline-emit turn shipped S194 (D287).** `mfm_points_parser.py`'s `to_points_row` now emits the
captured `_esc4_fourth_plus` tier into three new `Points_1-4`/`Points_2-4`/`Points_3-4` CSV columns
(unconditional — populated on the 34 esc4 units, blank everywhere else, same convention as every other
`Points_b-t` column). `convert_to_json.py` carries this into `points.sizes[*].fourth_plus`, but only
when called with a new opt-in `--emit-fourth-plus` flag (default off) — every existing call site,
including `units_repro_check.py`'s real-source run, stays byte-identical to committed `units.json`.
Verified three ways without touching committed data: an isolated synthetic-CSV round trip, the real
parser against `MFM_Thousand_Sons_v1.1.txt` (Rubric Marines' row carries 110/200, Castellan's stays
blank), and a full-CLI Thousand Sons build diffed flag-off vs flag-on (only Rubric Marines + Chaos Rhino
change, correctly). `b87_check.js` extended with a 4th fact pinning the row-level carry-through.

**Remaining turn (still open):**
1. **Data** — regenerate the 34 affected units by running the pipeline with `--emit-fourth-plus`, so
   their rows carry the real `fourth_plus` value, diff-guarded (only those 34 units' points move,
   `fourth_plus` added, all else byte-identical). Folds into B89's adoption arc per D283 so the units
   migrate once. Followed by a data-side assertion pinning the 34 units' correct `fourth_plus` value,
   re-derived from the MFM source.

**Scope of the shape (v1.1):** 34 units across the 15 files — Rhino, Razorback, Drop Pod, Impulsor
(loyalist transports), Chaos Rhino (Chaos transports), Raider, Venom (Drukhari), plus Rubric Marines.
Rare in v1_0 (only Rubric Marines + Brotherhood Terminator Squad), widespread in v1.1.

### B89 — MFM v1.1 adoption arc — **NEW S183 (D274); FIRST FACTION SHIPPED S195 (D288); data; L; depends B88; spans sessions**
Per-faction data-only turns: regenerate points from the v1_1 file, full pipeline through convert and
merge, key-level diff against the committed output — expected diffs are points values only, any
structural diff investigated before acceptance. Assertions pinning points values are reconciled
against the new source, never loosened. `source_manifest.json` updated per faction as it migrates.
Standard priority order. E23's D273 per-army pool counts re-verified after the six Astartes armies
migrate. The v1_0 layout reader retires when the last faction leaves it.

**Thousand Sons migrated S195 (D288)**, first of the arc — chosen over Death Guard per the S195
prompt's own recommendation (fully self-sourced, no chapter points). 12 units' points changed
(11 real re-prices, matching `MFM_v1_1_Reconciliation.md`'s adopt-mechanically list exactly, plus
Rubric Marines' `fourth_plus` under B94); all other 15 armies byte-identical. No points-value
assertions needed reconciling — none exist for this faction. `source_manifest.json` needed no change
(both source files already correctly hashed). **Left open for Thousand Sons**, tracked in the
reconciliation report, not new tickets: a Defiler wargear removal (`wargear_points.json`, Hades
lascannon/Heavy reaper autocannon) and 3 detachment force-disposition/unique-tag changes
(`detachments.json`) — both outside a units-only data turn's scope. **Death Guard migrated S196
(D289)**, second of the arc: 5 points changes (Plague Marines, Chaos Rhino [also gains `fourth_plus`
under B94], Deathshroud Terminators, Mortarion, Defiler), all other 15 armies byte-identical.
Reconciliation report found wrong on Defiler's wargear (repriced, not removed as the report states) —
flagged, not corrected, since `wargear_points.json` is untouched by a units-only turn.

**Chaos Daemons migrated S197 (D290)**, third of the arc and the first via a different mechanism: CD's
Gen-1 root `Unit_Points.csv` has no source-file-swap path (no `_v1_0.txt`/`_v1.1.txt` selection —
there is only the one hand-authored file), so this migration is a direct hand-edit of the 6 changed
values, decided this session as the correct precedented mechanism (see D290 for the full reasoning; a
`mfm_points_parser.py`-against-CD path exists in principle but is unvalidated new tooling, deferred).
6 units changed (Beasts of Nurgle, Bloodcrushers, Fluxmaster, Kairos Fateweaver, Lord of Change,
Shalaxi Helbane), all confined to `points`, all other 15 armies and all four merged lookups
byte-identical. `source_manifest.json`'s `Unit_Points.csv` hash updated to match — **Ryan action
required**: push the same edit to the private `rd-prime-1357-data-sources` repo, since Claude's token
there is read-only. Reconciliation report found wrong twice for CD: 3 enhancement re-prices
misattributed to SCINTILLATING LEGION instead of SHADOW LEGION (flagged for whoever migrates CD's
`detachments.json`), and a PLAGUE LEGION force-disposition banner that checked out as unchanged
(`TAKE AND HOLD` both versions) — not a missed item. CD's own investigate-first item (LORDS OF THE WARP
force disposition, PURGE THE FOE→TAKE AND HOLD) stays tracked for the detachments migration, out of
scope here.

**The six-file Space Marines group (base + Black Templars, Blood Angels, Dark Angels, Deathwatch,
Space Wolves) migrated together S198 (D291)**, fourth of the arc and the first multi-file atomic
migration: `add_chapter_point_overrides.py` compares each chapter's shared-unit prices against the
*current* generic base price on every build, so this group cannot split faction-by-faction like
CD/DG/TS — confirmed from source, not new tooling, just a synchronized filename swap across
`units_repro_check.py` and `add_chapter_point_overrides.py` (see D291). 47 units changed (14 Adeptus
Astartes, 8 Ultramarines, 9 Dark Angels, 7 Space Wolves, 1 White Scars, 8 Black Templars): `points` on
all 47, `chapter_point_overrides` on 2 (Inceptor Squad newly gains four chapter overrides; Vanguard
Veteran Squad With Jump Packs' existing Blood Angels override re-prices), `model_groups` on 1 (Uriel
Ventris legitimately gains Victrix Honour Guard as an attach option in v1.1). All ten other armies and
all four merged lookups byte-identical. One pinned `rules_assertions.py` value reconciled
(`b56a_bt_negative_control`, Impulsor AA/BT 80/85 -> 70/75).

**Found and stopgap-fixed a genuine source-text defect** (not a reconciliation-report error this
time — a raw MFM transcription defect): `MFM_Space_Marines_v1.1.txt`'s Marneus Calgar LEADER line is
missing a comma between "ERADICATOR SQUAD" and "STERNGUARD VETERAN SQUAD", gluing them into one
unresolvable token and silently dropping both legal units from his attach list. Scanned all six
SM-family files' validation reports for the same pattern (a dropped attach-list token that splits
cleanly into two-or-three known unit names) — isolated to this one instance, not systemic. Fixed via a
narrow, filename-and-substring-scoped correction table in `mfm_points_parser.py`
(`_KNOWN_SOURCE_FIXES`) that fails loudly if the source text changes underneath it. **Ryan action
required**: push the missing-comma fix to the private repo's `MFM_Space_Marines_v1.1.txt`, then this
dict entry can be removed. Detachments scope (Black Templars gains a new VENGEFUL HOSTS detachment,
several enhancement re-prices) untouched, tracked separately per convention.

**S199 (D292): checked both open fronts, neither is actionable right now.** The Calgar comma fix has
not landed in the private repo (verified via a direct fetch, not the local copy — still glued at
`MFM_Space_Marines_v1.1.txt` line 538); stopgap unchanged. Chaos Space Marines re-confirmed blocked:
`units.json` has no World Eaters or Emperor's Children entries. **Grey Knights corrected off this
list** — it was never a migration candidate. `units.json` has zero Grey Knights units at any version
(matches the standing "GK is not a built army" note from B94/S194), so there is nothing to migrate.
Building it is a net-new faction build (own scoping pass first, `CSM_BUILD_SCOPE.md`/
`THOUSAND_SONS_BUILD_SCOPE.md` precedent — no such doc exists yet for GK) and does not belong under
B89's definition. Tracked separately below as a new ticket. B89 itself has **no remaining in-scope
candidate** until either a Grey Knights build lands or World Eaters/Emperor's Children unblocks CSM.

**S211: confirmed and quantified the detachments-side gap this ticket already flagged for TS/DG/CD.**
Registering Emperor's Children in `detachment_parser.py` surfaced that `ARMY_TO_MFM` still points
Chaos Space Marines, Death Guard, and Thousand Sons at their v1_0 MFM files for detachments, even
though all three factions' `units.json` migrated to v1.1 under this ticket. Direct parse-and-diff of
each registered v1_0 file against its v1.1 counterpart confirms real, already-shipped errors, not just
the disposition drift this ticket already expected: Thousand Sons' Hexwarp Thrallband is priced 2 DP
(should be 3), Chaos Space Marines' Soulforged Warpack enhancement Tempting Addendum is priced 25 pts
(should be 40), plus six force-disposition mismatches across the three factions (TS: Ritual of
Regeneration, Sekhetar Cohort, Warpforged Cabal; CSM: Murdertalon Raiders, Soulforged Warpack; DG:
Contagion Engines). Chaos Daemons has no v1.1 detachment file to compare against, so its already-noted
LORDS OF THE WARP item stays unverified by this pass. Not fixed this session — three different
factions' committed `detachments.json`/`detachment_effects.json` data, out of scope for an
Emperor's-Children-only data turn. **Recommended as the next data turn under this ticket**, now that
Emperor's Children's own detachments (D305) are the one item that was blocking a clean sequencing
choice.

**S212 (D306): fixed the CSM/Death Guard/Thousand Sons portion of the gap.** `ARMY_TO_MFM`
re-pointed all three factions at their v1.1 files, mirroring Emperor's Children. Regenerated and
diff-guarded at record-key level: 0 keys added/removed (179 total unchanged), exactly the 7
predicted records changed — Hexwarp Thrallband's DP fix, the six disposition corrections, and
Soulforged Warpack's enhancement price fix, matching the S211 finding item for item. One extra,
harmless diff: Death Guard's Contagion Engines enhancement gained a hyphen in its v1.1 name
("Parasitic Woe reaper" to "Parasitic Woe-reaper"), a text correction with no points/legality
effect. `detachment_effects.json` (Death Guard's, Chaos Space Marines', and Thousand Sons' entries)
and `rules_assertions.py` (CSM-3, TS-2, both pin `text_source` only) checked directly against the 7
changed keys — neither needed reconciling. `detachments_repro_check.py` passes byte-identical.
**Ticket stays open**: the same v1_0-detachment-sourcing pattern applies to the six-file Space
Marines group (base Adeptus Astartes, Black Templars, Blood Angels, Dark Angels, Deathwatch, Space
Wolves) — flagged since D291 (Black Templars gains a new Vengeful Hosts detachment in v1.1, several
enhancement re-prices) but not yet confirmed/quantified by a direct parse-and-diff the way this
session did for CSM/DG/TS. **Recommended as B89's next data turn.** Chaos Daemons remains blocked
— no v1.1 detachment file exists to diff against, so its LORDS OF THE WARP item stays unverified.

### B100 — CLOSED S208 (D302); pointer only — full body in Closed / Shipped
Build Grey Knights faction. CLOSED S208: B106-DATA (both Dreadknights' ranged-weapon
options) shipped; faction fully complete, 25/25 units, zero residual `_parser_flags`.

### B109 — "My Army Lists" page: replace "Target ####" label with "#### Points" — **NEW S208 (D302); Ryan-reported; UI copy only; XS**
Ryan's change request, logged verbatim. Not yet scoped against `index.html` — needs the render site for
the "My Army Lists" page's list-row label found and the copy changed. No rules content, no data or
parser involvement; pure UI-text turn.

### B103 — Non-distinct `replacement_choices` rollup emits past its cap and hides the over-allocation — **NEW S201 (D294); engine; M; affects shipped lists' points**
Found while landing B101 and deliberately left alone there. In `loRollup`'s multi-model body branch, a
`replacement_choices` option pushes **every** tallied pick into `emit` and only then clamps the total
for the source charge (`used = Math.min(used, cap)`). Two consequences: more replacement weapons can
be emitted than the cap allows, and because the *source* charge is the clamped figure, the
per-source-weapon check never sees the overrun, so `overAllocated` does not fire — the list looks
clean while being wrong. The fixed-1 branch clamps differently again (it bounds each pick against the
remaining cap as it goes), so the two branches disagree on the same shape.

Not fixed inside B101 on purpose: the emitted weapons feed `wargearCostForRollup`, so tightening this
changes the **points** of already-saved lists across shipped factions. That needs its own turn, its
own before/after census of which shipped units can actually reach an over-cap tally, and a decision on
whether the correct behaviour is to clamp silently or to clamp *and* fire `overAllocated`. My reading
is that a saved list that exceeds a cap should be corrected silently (D0 — the state was never legal,
so there is nothing to warn about) and that `overAllocated` should stay reserved for genuine
same-source contention, but that is a product call and belongs to Ryan, not to the fix.

### B85 — Converter's faction-keyword detector is noise, not signal — **NEW S172 (D262); diagnostic added S173 (D263), not yet fixed; S**
`FACTION_KEYWORD_RE` captures the preceding line, so it reports unit names glued to the real keyword:
"Skarbrand Legiones Daemonica", "Kairos Fateweaver Legiones Daemonica". Chaos Daemons reports ~34
"faction keywords", Space Marines ~33 — roughly one per datasheet.
Worse than cosmetic: the false positives sit directly beside the KNOWN LIMITATION notes and train the
reader to skim past them, undermining the loud-failure design that justified stopping the build in D244.
**S173: not fixed blind.** No PDF access this session — the private source repo holds only already-
converted `.md` output for two packs, never the raw PDFs, and a synthetic string built to reproduce the
reported bleed ("Skarbrand FACTION KEYWORDS: Legiones Daemonica" on one line) did **not** reproduce it —
the regex correctly captured only "Legiones Daemonica" in that shape, so the real cause is something
other than same-line adjacency and guessing at it risks a third wrong diagnosis of this exact area (D262
already corrected two). Added a stdout-only diagnostic instead: each match now prints 30 characters of
raw context immediately before it, so Ryan's next real run against the actual packs shows the true
bleed pattern instead of speculation. Does not touch committed `.md` output, no determinism risk. Fix
still needs that real-run output before it can be written correctly.

### B86 — Chaos Daemons faction pack p13 has no extractable text — **NEW S172 (D262); XS; may be nothing**
Image-only page; the converter flags it. Needs an eye to confirm whether it carries rules. If it does,
OCR is required, which is a larger question than this ticket.

### B69 — "Select N abilities" datasheet pools render with no link to their selector — **Ryan-reported S152; corrected + generalized S169 (D259); was S, now M**
**Corrected intent (Ryan, S169):** remove the "(see left)" cue from Roboute Guilliman's *Author of the
Codex* entirely (not rewrite it to "(see below)"), and render the abilities it grants directly beneath
the *Author of the Codex* rule, visually grouped, so the user associates them with it.

**Generalized S169.** This is not a Guilliman one-off. The same shape — a short "select N [X] abilities"
ability whose "(see left)"/"(see above)" cue points to a boxed pool printed elsewhere on the datasheet —
appears on **six units across four factions**: Roboute Guilliman (*Author of the Codex* → Primarch of
the XIII (Aura), Master of Battle, Supreme Strategist), Chaplain Grimaldus (*Temple Relics*), Mortarion
(*Lord of the Death Guard*), Abaddon the Despoiler (*The Warmaster*), Magnus the Red (*Unearthly Power*),
Ulrik the Slayer (*Oathbound*, "(see above)"). All show the same defect: the pool abilities render as
plain sibling rows in the flat ability list with nothing tying them to their selector.

**Why it is not a quick engine strip.** The association is absent from our data — `abilities.json` is
name+description only, `units.json` ability entries are bare names. The source carried the pool via its
left/right-column ability typing ("левая колонка"), which the parser collapsed (B4/D155). For Guilliman
the pool is the trailing three abilities, but that ordering is not a rule that holds for the other five.
Also, a blanket cue-strip is unsafe: the 28 "(see below)" cues (Nurgle's Gift on 30+ Death Guard units,
Blessings of Khorne) sit on long descriptions whose referenced content is *inside the same text block* —
those cues are correct and must be left untouched.

**Correct build shape (dev-manager call, pending Ryan's scope choice):** a **data turn** — re-capture each
selector's ability pool from the source column-typing (parser fix, never hand-edit `units.json`), backed
by an assertion listing the six selector→pool maps — then an **engine turn** that renders each pool nested
under its selector and drops the resolved "(see left)/(see above)" cue while leaving "(see below)" alone.
Open decision for Ryan: fix all six at once (recommended) or Guilliman-only as a stopgap. Not started.

### B70 — Wardens of Ultramar cannot be attached to a unit — **DECIDED S175 (D266): build the join/Starting-Strength mechanic; needs a scoping turn**
Audited S170 (D260): Wardens has zero rows in `Datasheets_leader.csv` and no Core-typed "Leader"
ability — `leader_ability_name` is correctly null in both sources. Its real ability, `HEROES OF
ULTRAMAR`, is a distinct "this unit joins another unit, increasing its Starting Strength" mechanic,
not the Leader-attach mechanic, and the engine has no code for it. The engine's refusal to attach it
as a Leader is therefore correct as filed — not a bug. Ryan confirmed S175: build the join mechanic.
New scope, sizing TBD (D260 estimated M/L; not resized yet). Needs a scoping turn before build — an
analysis turn, not mechanical, since it sets how "join and increase Starting Strength" works
generally, not just for Wardens. **Updated S176 (D267):** B73 shipped and carved Wardens out —
`leader_eligible_units` is now empty and `leader_ability_name` null (the old glued 6-unit `SUPPORT`
backfill is gone). B73 also surfaced a conflict B70 must reconcile: the MFM tags Wardens `SUPPORT`
with **six** units (Assault Intercessor Squad, Assault Squad, Bladeguard Veteran Squad, Intercessor
Squad, Sternguard Veteran Squad, Vanguard Veteran Squad), but the printed `HEROES OF ULTRAMAR`
ability lists only **three** (Assault Intercessor Squad, Bladeguard Veteran Squad, Intercessor
Squad). MFM-as-source-of-truth vs. the datasheet text is the first identified MFM/pack conflict —
B70 decides which list governs the join. Not started.

### B75 — Faction pack pages that cannot be resolved into columns — **S159 (D244); resized + diagnosis corrected S172 (D262); L**
**Corrected S172 (D262): the original diagnosis below was wrong on both scale and scope.**
`faction_pack_transform.py` resolves *most* datasheet and detachment pages (stat tables intact) but
**not all** — Thousand Sons p1 (cover) and p5 (Hexwarp Thrallband, a **detachment** page) both fail. The
original claim that only the portrait Rules Updates pages fail is false. It cannot resolve pages that
which mix a full-width title and intro with columns starting at different heights. Those pages extract
full-width and the two columns interleave mid-sentence: "Each time a PLAGUE LEGIONS unit from your
**this PSYKER) and roll one D6**". Threshold tuning is exhausted — five values swept, none fixed Death
Guard p7 while keeping Thousand Sons correct, and one attempt regressed TS while fixing DG.
The converter now flags these pages (`single-SUSPECT` + a KNOWN LIMITATION note naming page numbers), so
the failure is loud, not silent. **Do not parse flagged pages.** This matters because Rules Updates
pages carry the keyword changes.
Recommended fix: cluster words into columns by x-position per row band, which handles ragged column
starts. Cheaper alternative Ryan may prefer: hand-correct the ~1 page per pack, at the cost of breaking
determinism. Awaiting Ryan's flag-count report across the full pack set to size the work.

**Sized S172 (D262) from a full 11-pack run: 64 flagged pages of 635 (~10%).** Range 3–16 per pack;
Black Templars is 3 of its 5. The original estimate — roughly one page per pack — came from a two-pack
sample. **Hand-correction is therefore not viable**: 64 pages of manual work that permanently breaks
determinism. Cluster words into columns by x-position per row band. Do B85 in the same pass so
the flags stay trustworthy (B84 shipped S173, no longer bundled here).

**S173: still blocked on real PDF access, not a product decision.** The private source repo carries only
already-converted `.md` output for two packs (Dark Angels, Space Marines), never the raw PDFs — Ryan's
local machine is the only place they exist. A column-clustering rewrite designed and shipped without
testing it against the actual flagged pages is exactly how B75's diagnosis got corrected twice already
(D262). Needs either the flagged pages themselves (screenshot or a small PDF excerpt) or a Ryan-run
diagnostic dump (word text + x0/x1/top per row on 2-3 representative flagged pages, e.g. Thousand Sons
p1/p5) before the rewrite can be designed on real evidence instead of guessed.

### P2 — `loadout_parser.py` custody — **NEW S58; PROCESS; softened by D123 (S59)**
The durable fix — commit the parser to the GitHub repo as canonical, mirror to project knowledge — is still
Ryan's call. But the pipeline is now self-defending regardless of where the parser lives: a stale or wrong copy
fails P1 (reproduction) and P3 (manifest) on the baseline run and by name, so a bad copy can no longer cost a
whole session's work silently. See **D119, D123**.


### P4 — Project-area capacity → long-term architecture — **NEW S134 (D211); STEPS 1–3 (D213/D219/D220); SCOPED S148 (D231); M0 BUILT S149 (D232); M1 DONE; B68 CLOSED S152 (D235); PROCESS; M2 NEXT**

**M0 built and proven S149 (D232).** `pipeline_manifest.py` extended 41 → 101 guarded files (full
public-repo coverage; fixed a pre-existing gap where it never guarded itself). `baseline.sh` gained
`--fetch` (tarball fetch-verify-overlay against the manifest) and `--data-turn` (token-authed
private-source fetch, zip fallback, refuses to start with neither). `rules_assertions.py` gained
`--tier a`, auto-classified per assertion (reachable-code walk against source-reading names AND
literal GW filenames — the filename half was a real gap the sources-absent simulation caught: three
assertions open `Army_Muster_Rules.txt` directly, missed by a names-only first pass). `repo_check.py`
gained the `SOURCE_REPO_TOKEN.txt` custody guard (live clone + bound-file-lists + content scan).
`source_manifest.json` created, 70 entries, confirmed against Ryan's real file-list screenshots. Exit test:
mechanism proven correct by simulation (fetch-verify passes against a simulated post-push tree; a
literal live-green run of `--fetch` against the real remote is blocked until tonight's push lands,
an inherent one-session chicken-and-egg, not a bug — noted for S150 to confirm for real at open).

**S150 (D233): `--fetch` confirmed live-green.** The live repo's `pipeline_manifest.py` carries the
101-file guarded set; a fresh tarball fetch-verify against it fails only one file
(`40K_Data_Pipeline_Process_v0_6.md`) — hash-confirmed as the pre-existing area-ahead-of-repo drift
D232 already named, not a new problem. **M1 is unblocked.**

**S151 (D234): M1 confirmed already run; fetch-verify design gap fixed.** Session open found 27
repo-resident guarded files absent from the area — M1 had run. The fetch-open's own verify step was
blocking their recovery: it checked the whole fetched tree unconditionally, so area-ahead-of-repo drift
on two unrelated files (`DECISION_INDEX.md`/`OPEN_ITEMS_BACKLOG.md`, edited S150 without a manifest
refresh) blocked pulling in files that had nothing to do with the mismatch. `pipeline_manifest.py`
gained `check_overlay()`/`--overlay-check`, scoping verification to only files absent locally, per the
"area copy wins" rule. Also closed a manifest gap: `SESSION_HANDOFF_149.md`/`.150.md` were never
appended to `GUARDED` (S149 missed its own append step). Manifest regenerated, 104 guarded files. Full
baseline clean except the carried-forward B68 failure and three known push-pending files
(`baseline.sh`, `pipeline_manifest.py`, `pipeline_manifest.json`, plus the pre-existing
`40K_Data_Pipeline_Process_v0_6.md` drift).

**Migration M0–M3 (dev-manager sequence):** M0 and M1 done. B68 closed S152. CSM turn B (loadout
defaults, the M2 dress rehearsal) shipped S153 (D236) → M2 (Ryan, evict the 71 sources) → CSM turn C
(detachment build).

---

**Step 3 cancelled (D220).** Step 2's 77 KB whitespace removal did not move the displayed
percentage at all (92% before, 92% after) — not even the fraction of a point the ~0.6-point
prediction called for. Per D213's rule, fixed before the read: no movement means whitespace prices
far below prose, near-free to the tokeniser. Minifying `units.json` and `detachments.json` for a
further ~720 KB, at the cost of three re-banked fixed points, is cancelled — the whitespace line of
P4 is done.

**`wh40k_core_rules.md` removed and confirmed (S142).** 139 KB, GW text, already flagged below as
"nothing opens it. Largest single removable file." Verified safe by static scan (absent from
`P4_REQUIRED_SOURCES`; the one filename match in `rules_assertions.py` is P4-1's own naming-pattern
regex, not a file open) and park-and-rerun (23/23 gates pass without it). Delivered to Ryan for local
backup — GW text, never repo-eligible regardless of project-area location. **Ryan deleted it S142:
92% → 90%, a 2-point move for 139 KB** — close to the ~123 KB/point rate found in step 1
(`BACKLOG_ARCHIVE.md`, 174 KB → also 2 points), so prose keeps pricing consistently regardless of
which file it's in.

**Step 1 result (D213): 94% → 92% on removing `BACKLOG_ARCHIVE.md` (174 KB).** The metric responds
to volume. Display rounds to whole points, so the true move is 1.1–2.9 against a 1.4 linear
prediction — consistent with linear. Roughly 123 KB of prose per displayed point. `BACKLOG_ARCHIVE.md`
is out of the project area, held in the repo and in Ryan's local backup; `OPEN_ITEMS_BACKLOG.md`'s
six pointer lines preserve lookup. Verified safe before deletion by park-and-rerun (22/22 gates pass
without it) and by a static scan finding no code reference and no manifest entry.

**Do NOT extrapolate 797 KB × linear = 6.5 points.** Prose tokenises at ~4 bytes/token; runs of
identical space characters compress far harder, plausibly 10–20. Step 1 proved volume matters, not
that all volume costs the same.

**Step 2 result (D219): `unit_loadouts.json` minified, 201,999 → 124,652 bytes (77,347 removed),
matching the 77 KB estimate.** `equipped_parser.py`'s terminal writer switched to compact separators;
fixed point re-banked, manifest reissued, 23/23 gates and 102/102 assertions hold. **Percentage read
(S141): 92% before, 92% after — no movement, step 3 cancelled per the pre-set rule (D220).**

The project area reads **90% as of S142**, after `wh40k_core_rules.md`'s removal.

**CSM sized S143, unblocked S144.** 112 datasheets (vs. Death Guard's 71 — CSM is roughly 1.5x DG's
build), 18 detachments, `MFM_Chaos_Space_Marines_v1_0.txt` present (499 lines). `Chaos_Space_Marines_web.txt`
supplied S144 (8,337 lines, 58 UNIT COMPOSITION anchors, structurally sound — D224). CSM itself is
fully unblocked: nothing left to source, only the build. The metric is **tokens, not bytes**
(Anthropic support docs: project knowledge capacity relates to context limits, with RAG expanding
it). So file *count* is irrelevant — only total content volume matters — and byte size is a proxy
rather than a linear measure.

**S145: reads 96%.** Since S144's read, Ryan replaced `Dark_Angels_web.txt` (was incomplete) and
`Space_Wolves_web.txt` (was missing entirely, now complete), on top of `Chaos_Space_Marines_web.txt`
landing S144. All three verified against the real pipeline (D225) — no break, one genuine Dark Angels
data bug fixed in the process. Ryan has a script (used for the new Space Wolves file) he intends to
use to regenerate the remaining hand-sourced `_web.txt` files (Black Templars, Death Guard, and a
rerun of Space Marines) for consistency and some further capacity relief. **Recommendation: not as
one batch.** Each of those files is load-bearing for a built faction's committed data; regenerating
several at once means a script quirk on any one faction shows up smeared across all of them at once
instead of pointed at one. Do them one at a time, each its own verified data-only turn, the way Dark
Angels and Space Wolves were handled in S145. Expected capacity return from this alone is modest — the
new script drops Windows line endings for plain ones, roughly a byte a line, well under what moved
the needle in steps 1 and 2 below. **The decision-log archive split (next paragraph) is very likely
the bigger lever and hasn't been tried yet.**

**Established by measurement, not by reading imports.** Every candidate source file was moved out and
`./baseline.sh` re-run. Results are pinned in assertion **P4-1**.

- **Built factions pin their sources permanently.** All eight built-faction MFM files, all five
  `_web.txt` files, both faction packs, `MFM_Instructions.txt`, `Army_Muster_Rules.txt` and
  `chaos_daemons_reference.md` each fail three or four gates when absent. Sources can be swapped in for
  an unbuilt faction; they can never be swapped back out once it is built.
- **Pruning sources: ~317 KB total was identified removable (~2.6%), six of those files are priority
  factions we'd have to re-source.** Of the ~285 KB genuinely free, `wh40k_core_rules.md` (139 KB) is
  out as of S141 (D220) — roughly 178 KB of identified prose remains a candidate if the next
  percentage read shows it's still worth pursuing.
- **The whitespace lever is done, and returned less than prose.** Compact separators on
  `unit_loadouts.json` (77 KB) moved the display by 0 points (D220) — the opposite of D213's ~0.6-point
  prediction. `units.json` (650 KB) and `detachments.json` (70 KB) stay pretty-printed; minifying them
  is not expected to be worth three re-banked fixed points given step 2's result.
- **Not yet attempted: splitting `40K_Decision_Log.md`.** Original step-1 plan (D211) included
  moving the log's archive half (~400 KB, out of 660 KB now) to a repo-only file the way
  `BACKLOG_ARCHIVE.md` was split off, with `DECISION_INDEX.md` preserving lookup. Deferred, not
  ruled out — the next candidate if capacity is still tight after `wh40k_core_rules.md`'s removal
  lands, though it is a bigger move (a new archive file, a cut-line decision) than the file removals
  done so far.

**Unknown, do not assume:** whether the displayed percentage is against the base ceiling or the
RAG-expanded one.


### E23 — `HEADHUNTER TASK FORCE`: the Tank Ace Character keyword grant — **NEW S134 (D209); scoped S181 (D272); data confirmed S182 (D273); data authored S187 (D280); engine build turn next; M**

**Data turn done S187 (D280).** `detachment_effects.json` carries all six rows (`tank_ace` kind,
`enforced: false`), re-verified from source rather than trusted from D273 — a real bug caught in
the process (the generic key's `army` field pointed at the unresolvable label `Space Marines`
instead of its true seven owning armies; fixed with a new `_owning_armies()` helper, general
enough to cover any future shared generic-key row). Two new assertions (`E23-1` coverage, `E23-2`
pool counts) pin the six pools at 16/16/17/16/16/16 and the Hammerfall Bunker Fortification
carve-out. What remains is the engine turn below — untouched this session.

Found by re-deriving E21's survey from source instead of trusting D203's list. `HEADHUNTER TASK FORCE`
exists in **six built armies** — Space Marines, Black Templars, Blood Angels, Dark Angels, Deathwatch,
Space Wolves — and grants the Vehicle keyword Tank Ace to most Adeptus Astartes Vehicles, then in the
Muster Armies step lets the player select **up to three** Tank Ace units to gain the **Character**
keyword. Its own Designer's Note confirms the consequence: those units can be given Enhancements, and
one of them can be the Warlord.

**The app currently gets this wrong.** Enhancement eligibility in `index.html` tests
`unit_type === 'Character'` and refuses everything else with *"Only Characters can be given this
enhancement."* Under this detachment that refusal is wrong on up to three vehicles per list.

**Direction of the error: over-restriction, not a D0 violation.** The tool refuses something legal
rather than permitting something illegal, so this does not outrank the enforcement work already
sequenced behind E21b/c/d and E22b. It is still a real rule the app does not know about, on six built
armies.

**Scoped S181 (D272). It is a fifth effect kind, not the sixth an earlier prompt miscounted** —
`detachment_effects.json` carries exactly four kinds today (`battleline`, `forbid`, `unlock`,
`warlord`); nothing shipped a fifth between D209 (S134) and now.

**The real complexity: E4 and E9 test Character status two different ways, and neither has a
per-list-entry hook.** E9's `isCharacter` (`eligibleWarlordEntries()`) is computed once per unique
`unit_name` and shared by every copy of that unit in the list. E4 (`enhancementTypeEligible`, three
call sites: index.html ~3194, ~3375, ~3689) reads the raw `unit_type` field copied onto the list entry
at six construction sites, never through `effectiveUnitType()` (D204's overlay function, which exists
only for the blanket battleline grant and isn't consulted by any enhancement code path). Tank Ace's
grant is neither a per-name nor a per-detachment blanket — it's up to three **player-picked
instances** — so this cannot be done as a pure data change or by extending either existing mechanism
as-is. Checked for overlap risk: none of the 28 Vehicle-type units in the generic Adeptus Astartes
block are already `unit_type: Character`, so no reconciliation case exists there.

**Mechanism decided (dev-manager call, reversible):** hybrid, not a pure effect-kind row. (1) A new
declarative `detachment_effects.json` kind carries the detachment-scoped static facts — eligible
unit_types/exceptions and the count cap (3) — the same shape `unlock`'s numeric `points_cap` already
uses. (2) The player's actual picks are new, purely-additive `list_store.js` state — an array of
`listId`s, capped at the detachment's grant — added the same way `warlord_entry_id` (v1) and
`force_disposition` (v3) were: absence reads as "none elevated," exactly what an older record already
meant, so **no schema version bump**.

**Storage/reset behaviour decided by existing precedent, not escalated to Ryan.** Continuously
re-validated, the same shape as `recomputeWarlord()`: any picked `listId` that stops being eligible
(leaves the list, its detachment is deselected, the cap is exceeded) is silently dropped on every
recompute — no confirmation dialog. Checked for a modelled "Muster" phase to gate against: none exists
— `index.html` mentions "Muster" only in rules-citation comments — so picks stay editable continuously,
identical to Warlord and Enhancement selection today.

**Engine touch points for the build turn:** `eligibleWarlordEntries()` needs an OR against the new
per-entry pick array alongside `x.unit.isCharacter`; `canAssignEnhancement`/`enhancementTypeEligible`'s
three call sites need an effective per-entry type (raw `unit_type`, or `'Character'` when the entry's
`listId` is a live pick) in place of the raw field — mirroring `effectiveUnitType()`'s "compute an
overlay, never touch the raw record" shape, but at per-entry rather than per-detachment granularity,
since no existing function does that today.

**Data turn done — all four facts confirmed from source (S182, D273); no longer blocked.** (1) Grant
wording is **identical across all six** because it is a single Space Marines detachment, not six copies:
verbatim only in the SM Faction Pack v1.0 and Wahapedia `Detachment_abilities.csv` (`faction_id=SM`),
which agree word-for-word; `detachments.json` `rule_text` is byte-identical in all six records (SHA-256
`cadd53c18131`). (2) The carve-out is **not "most Vehicles" — it is a precise predicate**: Adeptus
Astartes Vehicle *excluding Fortifications, Drop Pods, Walkers and units that can Fly*, all computable
from built `keyword_names` (`Fly`/`Walker`/`Drop Pod`) plus `unit_type` (`Fortification`). (3) The
**"up to three" cap holds in all six**. (4) Keys confirmed: `<Army>|HEADHUNTER TASK FORCE` for Space
Marines / Black Templars / Blood Angels / Dark Angels / Deathwatch / Space Wolves, each `dp:2`,
`PRIORITY ASSETS`.

**Per-army eligible pool (resolved from source, ground truth for the build's assertion):** generic
Adeptus Astartes block is 28 Vehicle-type units → **16 eligible** (Firestrike Servo-turrets, both
Gladiators×3, Impulsor, the three Land Raiders, both Predators, Razorback, both Repulsors, Rhino,
Vindicator, Whirlwind), 12 carved out (5 Walker Dreadnoughts, 6 flyers, Drop Pod). Resolved per army:
**SM 16, Black Templars 16, Blood Angels 17 (adds Baal Predator), Dark Angels 16, Deathwatch 16, Space
Wolves 16 — Blood Angels is the only army that is not 16.** No eligible unit is already a
Character/Epic Hero in any pool, so the grant is never a no-op.

**Build-turn design notes (dev-manager calls):** (a) base eligibility on the Vehicle **keyword**, not
`unit_type: Vehicle`, so the "excluding Fortifications" clause does real work — it catches Hammerfall
Bunker (Vehicle keyword, `unit_type: Fortification`), the only Adeptus Astartes case; (b) author the
carve-out as a **per-entry exclusion predicate** on the effect row, not a per-detachment name list, and
evaluate it on each list entry's own keywords; (c) the "Adeptus Astartes" qualifier is satisfied by
pool construction today, not a keyword test — add an assertion that no non-Adeptus-Astartes vehicle can
enter these pools and silently become Tank Ace-eligible.


### B67b — Optional: purge `Unit_Weapons.csv` / `wh40k_core_rules.md` from git history — **NEW S145 (D225); Ryan action; low priority, not time-sensitive**
Both files are confirmed gone from the repo's HEAD (B67 closed S145). D223's belief that the repo was
a single commit was wrong — 249 commits — so the two commits that originally added these files are
still reachable in history even though neither file has been touched since; `git filter-repo` or BFG
plus a force-push would be needed for a full purge. Bigger and more disruptive than the HEAD-level
fix already done. Precedent: the repo already has an early batch of `_web.txt` files committed by
mistake and deleted the same HEAD-only way, still sitting in that old history today, apparently
without incident. Ryan's call whether this is worth doing at all.


### E12 — User accounts (login/passwords) — **OPEN; DEFERRED S121 (Ryan: hold until near the end); L; architectural**
Biggest lift by far — moves the app from static GitHub Pages + local storage to
something with a backend/auth. Flag: this reshapes hosting and data storage and
should be scoped on its own, well apart from the list-builder work. Ryan has
deferred this to late in the roadmap, after the list-builder feature set is otherwise done.


### B17 — Loadout completeness gaps — **PARTS 1–2 + ENGINE TURN DONE (Sessions 24–26, D79/D80/D81); remainder S–M.**
Part 1 (option-parser gaps) shipped: `loadout_parser.py` now handles per-N clauses with
"in the unit" / "up to N" / active voice, active-voice definite (sergeant) swaps,
active-voice "any number / all" swaps, and by-name equipment adds (Watcher in the Dark).
Five units fully or partly cleared — Talonstrike (3→0 flags), Decimus (4→0), Deathwing
Terminator Squad (2→0, incl. the storm-bolter swap group + Watcher), Fortis (5→3),
Spectrus (4→2). Data-only, `index.html` still v5.45.

**Part 2 (Session 25, D80) — DONE (four of five flags):** indefinite single-model swap
(`count` + `max_total:1`) and conditional per-model scope (`requires_weapon`) now parse.
Cleared: Fortis vengor, Fortis plasma-pistol (dormant gate), Fortis grenade-launcher per-5
(live gate), Spectrus instigator. Fortis 3→0, Spectrus 2→1. Data-only, `index.html` still v5.45.

**Engine turn (Session 26, D81) — DONE.** `index.html` **5.45 → 5.46**. Count path now honours
`requires_weapon` (rollup skip + clear-on-lose + disabled "needs `<weapon>`" render) — the
Fortis plasma-pistol gate is live (harmless today; nothing removes the incinerator). Shared-pool
cap now also seeds from `max_total` members (bounded by the largest member; `per_n_models` keeps
precedence). New `classify_conditional_add_choice` handles "One model equipped with a `<weapon>`
can be equipped with one of the following: …" → capped adds sharing a per-sentence `pool_id`.
Spectrus helix/comms modelled as two `max_total:1` equipment adds, shared pool (cap 1),
`requires_weapon` marksman bolt carbine → exclusive one-model choice. **Spectrus 1→0 flags.**
Splice was one unit, `options`/`_parser_flags` only; `model_groups` byte-identical; fixed point
holds; CD verbatim. Render states unverified in-DOM.

**Variant sub-group DEFAULT weapons (true 1b) — DONE (Session 28, D83).** Root cause was a
`match_group` gap, not merged-list synthesis: the per-variant "…with `<weapon>` is equipped
with: …" lines already exist in prose but failed to bind because the singularizer only
normalized the trailing word (the plural sat mid-phrase). Added a per-word-singularized
unique-equality fallback to `match_group`; re-derived the three affected units (Spectrus,
Fortis, Heavy-Intercessor team `000002781`), correcting ten variant groups' `default_weapons`
to their authoritative loadouts. Only those units changed; base groups/options/flags/counts
byte-identical; fixed point re-established; CD verbatim. Data-only, `index.html` v5.47.

**Still open in B17 (banked with reason):**
- **Reiver Squad** — **DONE (D84, S29).** Two new classifiers (`classify_conditional_add`,
  `classify_all_models_add`): Sergeant conditional combat-knife add gated on bolt carbine
  (reuses `requires_weapon`); grav-chute + grapnel as independent per-model equipment adds
  fanned across both model groups. Only `000002718` changed; fixed point re-established; CD
  verbatim; v5.47.
- **Sanguinary Guard** — "One model can be equipped with 1 Sanguinary banner" (max-1 add)
  + confirm the 3/6 size selector surfaces from `size_brackets [3,6]`. **S–M.**
Fix parsers, not output; the five-unit change reached the preserved file via strip-from-
existing → re-parse → splice options/flags, keeping B16 `default_weapons` byte-identical.


## Closed / Shipped — pointers

- **B106** — B101's `distinct` engine support didn't cover a fixed-1-group pure-addition
  "up to N, no duplicates" option — **NEW S204 (D297); CLOSED S207 (D301); ENGINE.** Fix reuses the
  existing B101 machinery: a `count` option with `distinct: true`, `replacement_choices: [...]`,
  `max_total: N` and no `replaces` now rides the same `loDistinctCap` / `loChoiceGroupCap` /
  `loDistinctPicks` path as the swap case. `loRollup`'s fixed-1 branch changed: a two-line guard
  accepts the no-`replaces` shape, and `chargeF` skips source-consumption for it. Body-group branch
  needed no change — `loSrcOnGroup` already returned true for empty `replaces` (verified against
  source, then pinned by the harness). `add`+`pool_id` was rejected because its cap is `max` of
  member caps, not a sum. Net-new `b106_check.js` (32 assertions), gated in `baseline.sh` and
  `pipeline_manifest.py`. `index.html` v6.17 → v6.18. Grey Knights fully unblocked for the
  Dreadknight parser + regeneration turn.

- **B106-DATA** — the parser/data half of B106 — **NEW S208 (D302); CLOSED S208 (D302); DATA+PARSER.**
  New classifier `classify_this_model_add_count_choice` in `loadout_parser.py` matches "This model can
  be equipped with up to N of the following, but cannot take duplicates" (N always spelled as a word in
  source — confirmed across the full corpus, 22 "two" + 5 "three", never a digit), emitting `type:
  'count'`, `distinct: true`, `replacement_choices`, `max_total`, no `replaces` — exactly the shape
  B106's engine fix was built to accept. Regression-checked against the full options corpus: only the
  two Grey Knights Dreadknights match this classifier's lead-in; four more raw-text matches (all Tau)
  use a different lead-in ("Any number of models…") and are out of scope regardless (not currently
  built). `unit_loadouts.json` regenerated via the seven-pass chain, seeded with only the four
  `HAND_AUTHORED` entries — 2 units changed, 0 elsewhere, `repro_check` byte-identical.
  `wargear_points.json` regenerated via the canonical `FACTION_BY_MFM` order — 2 units added, 0
  elsewhere. New structural assertion `B106-DATA`, re-derived from source, not pinned to unit IDs.

- **B100** — Build Grey Knights faction — **NEW S199 (D292); scoped S200 (D293); units half shipped
  S204; loadouts half shipped S206; CLOSED S208 (D302) once B106-DATA shipped the two Dreadknights'
  ranged-weapon options.** Full original body below, kept intact for the scoping/build history.

  Adeptus Astartes priority-order faction with zero built units at any version. Both
  `MFM_Grey_Knights_v1_0.txt` and `_v1.1.txt` are present and already mapped in `mfm_points_parser.py`'s
  `FACTION_BY_MFM`, and it was never part of the SM chapter-override chain (`add_chapter_point_overrides.py`'s
  `CHAPTERS` list holds only the five named chapters), so nothing blocks a build from a tooling
  standpoint.

  **SCOPED S200 (D293)** — `GREY_KNIGHTS_BUILD_SCOPE.md` written (net-new). 25 current-edition
  datasheets, not the raw 31; the smallest faction build the project has done. Fully self-sourced: no
  cross-file points append, not part of the `add_chapter_point_overrides.py` chain, so D291's
  version-mismatch hazard doesn't apply. Mirrors the Death Guard / Thousand Sons blocks in
  `units_repro_check.py` exactly. Full pipeline dry run clean (transform -> points -> convert, 25
  units, Gate of Infinity correctly routed as an army-level ability). Points coverage complete: 0
  datasheets unpriced, 0 unparsable costs, 0 bracket collisions, 0 dropped attach-list entries. Six
  exclusions verified against the MFM's own `LEGENDS` header — Draigo's absence is correct, not a bug.
  The Thunderhawk Gunship is unbuildable rather than excluded (Wahapedia's Forge World source is
  edition `0`, no datasheet exists); same silent gap applies to every built faction, recorded not
  fixed. **B94's open Grey Knights concern retires** — the `1ST TO 3RD`/`4TH +` copy-tier shape is gone
  in v1.1 (`REQUISITION THRESHOLDS REMOVED`). Loadouts need only four units authored, in two shapes:
  compound "weapon and banner" replacements plus a narthecium upgrade (no new schema — Sanguinary
  Guard's banner and Tzaangors' Herd Banner/Brayhorn are shipped precedents), and the two Nemesis
  Dreadknights' pick-two-distinct constraint, which depends on **B101-data turn 2** (turn 1 shipped
  S202/D295). Nine detachments, 28 enhancements, no unique tags; v1_0 vs v1.1 differ only in three force
  dispositions. Build from `_v1.1.txt` per D293.

  **UNITS HALF SHIPPED S204.** Registered Grey Knights in `units_repro_check.py` (mirrors the
  Thousand Sons block exactly). `units.json` regenerated and diff-guarded: exactly 25 units added,
  nothing else changed. Demonstrated directly (not assumed from the scope doc) that Grey Knights needs
  no dedicated composition-paste file — its six multi-group units gap-fill completely and correctly
  from the final `--datasheets` pass alone, since each one's groups carry identical default gear per
  the datasheet's own "Every model is equipped with" wording. `repro_check.py`'s `FACTIONS` list does
  **not** yet include `GK` — see below.

  **LOADOUTS HALF BLOCKED — three gaps found while attempting to author the four flagged units,
  tracked as their own tickets so the loadouts half can ship independently once each is resolved:**
  - **B104** (serious, blocks any `unit_loadouts.json` regeneration while Grey Knights exists in
    `units.json`, not just its own loadouts): registering Grey Knights exposed a real, pre-existing
    ambiguous-fallback bug in `equipped_parser.py`'s `scoped_name2id` that silently corrupts 8
    unrelated, already-shipped generic-vehicle units the moment Grey Knights' same-named vehicles
    (Land Raider, Land Raider Crusader, Land Raider Redeemer, Rhino, Razorback, Stormhawk Interceptor,
    Stormtalon Gunship, Stormraven Gunship) are appended after them. See B104's own entry for the
    full root cause.
  - **B105**: the narthecium sentence ("1 Terminator can have its storm bolter replaced with 1
    Apothecary's narthecium") uses passive phrasing no classifier in `loadout_parser.py` matches.
    Confirmed data-only-fixable pieces first: added `Ancient's Banner` and `Apothecary's Narthecium`
    wargear-ability text via `ds_wargear_abilities_parser.py`'s regeneration — the SAME "compound
    weapon + banner" option (Brotherhood Terminator Squad / Paladin Squad's `cc_2`) is already
    correctly classified by the existing parser and needs no code change once B104 is fixed and a
    clean regeneration lands it with its display name resolved. Only the standalone narthecium
    sentence needs a new classifier.
  - **B106**: both Dreadknights' "up to two of the following, but cannot take duplicates" line (no
    `replaces` — a pure addition, not a swap) is a genuinely untested shape: traced the actual
    `loRollup` code in `index.html` and confirmed the shipped B101 `distinct` support only covers
    options with a real source weapon on a fixed-1 group. This needs new engine support, not just a
    parser regex, before it can ship.

  Sequencing recommendation (mine, proceeding on it): fix B104 first — it blocks the whole
  `unit_loadouts.json` gate regardless of Grey Knights' own loadouts and risks silently corrupting
  other factions' data on any future data turn if left alone. Then B105 (parser-only, small). B106
  (engine + tooling + data) can follow on its own schedule since it only blocks the two Dreadknights,
  not the rest of the roster. Once all three ship, re-add `GK` to `repro_check.py`'s `FACTIONS` list
  and regenerate `unit_loadouts.json` for real, re-verifying the 8 previously-affected vehicles resolve
  correctly alongside Grey Knights' own 25 units.

  **CLOSED S208 (D302):** B106-DATA shipped both Dreadknights' ranged-weapon options — see B106-DATA's
  own entry above for the classifier, regeneration, and assertion detail. Grey Knights is now fully
  complete: 25/25 units built, zero residual `_parser_flags` anywhere in the faction.
- **B105** — `loadout_parser.py` doesn't classify a passive single-model swap sentence ("N `<model>`
  can have its X replaced with Y") — **NEW S204 (D297); CLOSED S206 (D300); TOOLING.** Added
  `classify_one_model_passive_swap`, mirroring `classify_one_model_swap`'s active-voice shape but for
  the passive "can have its X replaced with Y" form with a named model group. Regression-checked
  against the full options corpus before regenerating: 13 sentences match, all previously unclassified,
  only 2 (Brotherhood Terminator Squad, Paladin Squad) belong to a currently-built unit. The backlog's
  own claim that the sibling "compound weapon + banner" sentence needed no code change once B104
  shipped was checked against source and found wrong — see B107.
- **B107** — `weapon_abilities.json`'s raw punctuation vs. `loadout_parser.py`'s cleaned option text:
  quote-normalisation mismatch drops equipment resolution — **NEW S206; CLOSED S206 (D300); TOOLING;
  found and fixed same session.** `equipment_items` (the wargear allowlist) was built directly from
  `weapon_abilities.json`'s raw JSON values, never passed through the same curly-to-straight
  normalisation `clean()` applies to option text before matching. Two Grey Knights datasheets disagree
  on curly vs. straight apostrophe for the same item names; "Ancient's Banner" only had a curly-quote
  entry, so it silently failed to resolve, fell back to a bad-cased placeholder, and dropped
  `equipment_parts` — while "Apothecary's Narthecium" happened to resolve, by coincidence, because
  `weapon_abilities.json` holds duplicate entries for it in both punctuation styles. Fixed by running
  `nm` through `clean()` before keying the allowlist. Diff-guarded: touches only Grey Knights' two
  affected units, zero change elsewhere.

- **B104** — `equipped_parser.py`'s `scoped_name2id` ambiguous-candidate fallback silently corrupts
  unrelated units — **NEW S204 (D297); CLOSED S205 (D298).** Fixed with scope-alias + parent-army
  fallback from `faction_taxonomy.json`, plus propagation of composition data to all same-named
  candidates. Also corrected a pre-existing gap: 7 AA generic vehicles gained correct `equipped`
  composition data. Synthetic B104 assertion added to `rules_assertions.py`.
- **B101-data** — The no-duplicate rule was expressible (B101 engine half) but nothing authored it; the
  marker string shipped as a fake option — **NEW S201 (D294); TURN 1 (TOOLING) SHIPPED S202 (D295);
  TURN 2 (DATA) SHIPPED S203 (D296); CLOSED S203.** Three Chaos Space Marines options held GW's
  no-duplicate restriction as a literal string sitting in the choices array instead of the `distinct`
  flag B101's engine half enforces: Raptors `cc_6`, Legionaries `cc_5`, Traitor Guardsmen Squad `cc_1`.
  Turn 1 (S202): `_choices_from_list` recognises the marker at the start of the captured list text and
  returns `(choices, distinct)`; all ten call sites updated, plus a second copy-through in
  `build_loadout`'s entry rebuild. Turn 2 (S203): ran the real pipeline in a scratch dir, diff-guarded
  at key level against committed — exactly the three predicted units changed, nothing else across 305
  parsed units; `unit_loadouts.json` banked, `repro_check` passes. Added `rules_assertions.py`
  **B101-DATA**: rather than pinning the three known IDs, scans `Datasheets_options.csv` for the marker
  across all rows and checks every currently-built, successfully-classified hit — a structural check
  that will catch the same GW phrasing on a future faction's datasheet rather than staying silent on it.
  Scoping found one more marked datasheet in scope (Nemesis Claw `000003876`, CSM) whose row is
  `UNMATCHED` (marker text never reaches output) — a separate, pre-existing parser gap, correctly
  excluded. Negative-controlled against the pre-regen file pulled from the repo (fails, names the three
  units) and against the regenerated file (passes). 119 assertions (was 118). Three residual `UNMATCHED`
  flags (Raptors' 10-model-bonus sentence; Legionaries' two spelled-out "One Legionary's..." lines)
  confirmed unrelated and left open, not folded in. B100 (Grey Knights) no longer blocked.

- **B102** — `detachment_parser.py --report` crashes on any gap — **NEW S200 (D293); CLOSED S202
  (D295); TOOLING.** Gap records are built with keys `key` / `source_faction` / `detachment` / `dp`,
  but the report writer read `g["army"]`, so any run with `--report` that produced at least one gap
  died with a `KeyError` after the JSON had already been written. Latent because
  `detachments_repro_check.py` never passes `--report`. One-line fix (`g["source_faction"]`); proven
  directly against real sources — all 11 known gaps across built factions now render correctly, and
  `detachments.json`'s own output confirmed byte-identical, so only the report writer changed.

- **B101 (engine half)** — "Cannot take duplicates" wargear rule was not enforced — **NEW S200
  (D293); engine half CLOSED S201 (D294); ENGINE.** `loMaxCount` capped the total picks for a
  `replacement_choices` option but nothing anywhere enforced that the picks differ, so an illegal
  duplicate was reachable in three shipped Chaos Space Marines units and both Grey Knights Nemesis
  Dreadknights could not be authored at all. Fixed by a per-option `distinct` boolean held at three
  independent enforcement points — the selection path (`editLoadoutChoiceCount` gains a `perMax`
  argument), the renderer (the `+` disables rather than being offered-and-rejected), and the rollup
  (`loDistinctPicks`, in **both** `loRollup` branches, so a list saved before the flag cannot roll up
  illegal weapons or their points). Derived ceiling `loChoiceGroupCap`: a distinct option can never
  take more picks than it lists choices. Over-selection truncates in `replacement_choices` order, so
  it is deterministic. `index.html` v6.17; net-new `b101_check.js` with synthetic fixtures by design
  (nothing shipped carries the flag yet, so real-data assertions would pin nothing) and each
  enforcement point mutation-tested. **The authoring half is not closed** — it needs a parser change
  then a regeneration and is tracked separately as B101-data, which is what B100 now waits on.

- **B96** — `b87_check`/`b88_check` crashed instead of SKIP when GW sources are absent — **NEW S193
  (D286); CLOSED S194 (D287); TOOLING.** Both harnesses invoke the parsers directly against raw GW MFM
  source files but sat in `baseline.sh`'s always-run block rather than the sources-required block, so a
  legitimate sources-absent open got two `FileNotFoundError` crashes indistinguishable from real
  failures. Folded into B94's S194 tooling session (two tooling items, one tooling turn — turn-
  consistent). Fix: moved both gates into the `if [ "$SOURCES_OK" -eq 1 ]` block alongside the three
  repro checks; they now `SKIP` cleanly when sources are absent.

- **B95** — `faction_taxonomy.json`'s `built` flag disagrees with `units.json` for CSM and Thousand Sons — **NEW S191 (D284); CLOSED S192 (D285); DATA + TOOLING.** Both factions were fully built by every measure every other built faction is (CSM 58/58 units + 17 detachments + CSM-1/2/3 passing; Thousand Sons 34/34 units + 9 detachments + TS-1/2/3 passing, `Thousand_Sons_web.txt` now present resolving the old loadout-defaults blocker) — the `built: false` flag was simply stale. But checking `index.html`'s consumers of the flag before flipping it found a bigger gap: neither faction's taxonomy entry carried a `data_army` key, which `resolveUnits`/`resolveDetachments` require — missing it means a silent fallback to the generic Adeptus Astartes pool (units) or an empty list (detachments), not a clean failure. Both `built: true` and the correct `data_army` added together. New assertion `B95-1` pins the contract (every built, non-subfaction faction carries a valid `data_army`) so the same silent-fallback shape can't recur on a future faction. 117 assertions (was 116).
- **B88** — MFM v1.1 reconciliation reports + detachment-layout parsing — **NEW S183 (D274); CLOSED S191 (D284); TOOLING/ANALYSIS.** Extended `detachment_parser.py` with the same sniff-and-normalize pattern B87 used for the points file: v1.1 splits `NAME<n>DP`/bulleted-enhancement lines across two physical lines (name, then a bare `<n>DP` or `<n> pts` line) and drops the same `UPDATED`/`FORCE DISPOSITION(S) CHANGED` notes as noise — normalization rejoins the DETACHMENTS...LEGENDS/EOF slice back into the exact v1_0 shape so the existing reader runs unmodified. Two DETACHMENTS-only quirks not present in the points file, both verified against source: a bare `▲` marker with no parenthesised delta on a DP line (Thousand Sons' Hexwarp Thrallband, 2DP→3DP) and a `UNIQUE TAG REMOVED` note (World Eaters — missed on a first pass keyed only off the Space Marines file, caught once World Eaters was actually parsed, then confirmed complete by an exhaustive all-caps-line sweep of all 15 files' DETACHMENTS blocks). v1_0 output proven byte-identical on all 10 files in `ARMY_TO_MFM`; all 15 v1.1 files now parse their DETACHMENTS block cleanly (0 before). Net-new `b88_check.js` pins all of it; `rules_assertions.py`'s P4 source census updated for the new report filename. Generalized `mfm_reconcile.py` from the old one-off SM-vs-`mfm_sm.txt` pass into a real per-faction tool: for the 10 built-army MFM file pairs, diffs points, roster, wargear, attach lists (including Leader/Support flips), and detachment fields/enhancements between v1_0 (what the app is built from) and v1.1 (the newest capture), classifying every delta adopt-mechanically vs investigate-first. Caught and fixed a real bug in the first draft before shipping: force-disposition and unique-tag changes on an otherwise-matched detachment were being counted as adopt-mechanically — they're a rules-shape property, not a value, so they were moved to investigate-first. Final: 189 adopt-mechanically, 71 investigate-first across the 10 factions; report banked as `MFM_v1_1_Reconciliation.md`. Output is B89's work order. **B95 opened**, incidental: `faction_taxonomy.json` marks Chaos Space Marines and Thousand Sons `built: false` though `units.json` holds real data for both — found while scoping this report to "built" factions.
- **B87** — `mfm_points_parser` cannot read the MFM v1.1 page layout — **NEW S183 (D274); CLOSED S190 (D283); TOOLING (+ one coupled 2-value data correction).** Added a per-file v1.1 sniff (keyed on the ▲/▼ change markers, absent from every v1_0 file) and a normalization pass that rewrites each v1.1-exclusive quirk into the exact v1_0 line shape the existing readers already parse: drops the leading `UNITS` header, the standalone `▲`/`▼`/`▲▼` markers, and the `UPDATED`/`REQUISITION THRESHOLDS REMOVED`/`FORCE DISPOSITION(S) CHANGED` notes; strips the inline `▼ (-10)` / `▲ (+10)` cost annotations leaving the final printed value intact. Cost lines made bullet-optional so one reader serves both editions. Result: all 15 v1.1 files cost fully (SM 179/179; 0 before), every v1_0 file byte-identical **except** the two units B87 corrected. **In-flight bug found and fixed:** the tier shape `1ST TO 3RD / 4TH+` had no reader — the parser fell through to single-mode and kept the pricier 4th+ line, so Rubric Marines (CSM 000003583, TS 000001020) shipped every 1st-3rd copy at 110/200 instead of the correct 100/190. B87 added a reader for the shape (`esc4` mode) that emits the 1st-to-3rd price across the 3-tier schema and captures the un-representable 4th+ tier for B94; the two Rubric Marines values were regenerated through the real pipeline (units_repro_check green). The v1.1 DETACHMENTS-parsing clause was rescoped out to B88 (detachments have their own parser). 15 v1.1 files registered in `source_manifest.json`. Net-new `b87_check.js` pins all three facts. **B94 opened** for the deferred copy-4 schema decision.

- **B91** — Decision-log & versioned-doc canonical reconciliation — **NEW S185 (D277); CLOSED S189 (D282); TOOLING/DOC.** The unversioned name was already canonical (decided at D265/S174); sessions had drifted back to a resurrected `40K_Decision_Log_v3_0.md` without anyone noticing, since the manifest only checks that its guarded target hasn't changed, not that it's the one being written to. Byte-diffed both files before merging: agreed everywhere except D264–D275 (guarded-only) and D276–D281 (versioned-only, D276 additionally misplaced beside D42). Merged into one `40K_Decision_Log.md`, every D-number 0–281 present exactly once, D276 relocated to its correct position. The four sibling version-suffixed doc pairs confirmed byte-identical to their renamed counterparts by direct fetch, not size — safe to delete outright. Five old-named files need deleting from the repo by Ryan.
- **B92** — MFM v1.1 edition adoption / points currency — **NEW S186 (D279); CLOSED S189 (D282), duplicate.** Already decided at D274/S183 (keep every version, adopt per-faction as versions bump); B87/B88/B89 are the tickets that execute it, opened the same session and still open. B92 restated the same question without being checked against the earlier decision; Ryan reconfirmed the same direction independently this session. B87 is the actual next unblocked step.
- **E27** — State Leader vs Support correctly in popups and exported output — **SHIPPED S179 (D270); UI.** `renderDetail`'s attach-panel section heading and hint, and `leaderSectionHtml`'s datasheet-modal heading, both now read `leaderAbilityName`/`leader_ability_name` instead of a hardcoded "Leader" string. Investigated and ruled out during the build: the two other "likely sites" the ticket named — the list-panel attached-unit row and the JSON save/export schema — neither actually hardcodes the word "Leader" anywhere, so nothing changed at either. Also confirmed the Rules-section dedup filter (checks the literal string `'Leader'` against `rule_names`) had to stay untouched: the datasheet's own ability box is always literally printed "Leader" (129 of 129 checked instances) regardless of `leader_ability_name`'s Leader/Support classification — that classification comes from the MFM's own LEADER/SUPPORT block headers, a different source document, not the datasheet card. Assertion E27 added (structural shape only, no legality change). `index.html` v6.13 → v6.14.
- **E26** — Enforce one-Leader-one-Support stacking — **SHIPPED S178 (D269); ENGINE.** `permitsCoLeader` rewritten with four D268 requirements: (R1) bare CHARACTER Support pairs with any Leader by the base rule; (R2) DG `co_leader_any` second-Leader path kept; (R3) Leader cross-reference (Huron→MotM, sole instance across 16 factions); (R4) same-type cap refuses two Supports or two non-`co_leader_any` Leaders, actively overriding the stale Apothecary→Lieutenant cross-listing. `leaderAbilityName` added to the allUnits view object. Named `co_leader_eligible_with` lists preserved as the datasheet combination restriction. Assertion E26 added (10 legality cases with symmetry, plus 9 structural shape fragments). `index.html` v6.12 → v6.13.
- **B73** — Ultramarine (and roster-wide) Leader abilities listed units outside their actual eligibility — **DECIDED S175 (D266); SHIPPED S176 (D267); DATA.** MFM made source of truth for attach eligibility. `mfm_points_parser.py` rewritten to capture `LEADER` and `SUPPORT` blocks (one line each — fixes the D260 over-read), replace the stale 10th-ed Wahapedia ability/list wherever the MFM has a block, drop any entry that resolves to no datasheet, and clear the footer on Support overrides. `units.json` regenerated through the full pipeline; diff-guard clean (43 units, only `leader_eligible_units`/`leader_ability_name`/`leader_footer`). Ancient/Apothecary/Lieutenant → Support; Epic Heroes narrowed to MFM lists; Wardens carved out (MFM/datasheet conflict → B70). Assertion `B73` added (111 total). Corrected two S175 assumptions before building: Support is the same attach mechanic as Leader (not B70's join mechanic), and the engine gates on the list not the ability name — so both lists live in one field with the distinction in `leader_ability_name`, reversing the S175 "separate field" plan (confirmed with Ryan). Ryan's stipulations became E26 (stacking enforcement) and E27 (popup/output wording).
- **B76** — Rolling documents carried frozen version numbers in their filenames — **NEW S159 (D246); SHIPPED S174 (D265); TOOLING, clarity not safety.** Renamed all five (`40K_Decision_Log.md`, `40K_Data_Pipeline_Process.md`, `40K_Functional_Spec.md`, `40K_Architecture_Overview.md`, `40K_Data_Dictionary.md`) — content unchanged. `pipeline_manifest.py`, `repo_check.py`, `DECISION_INDEX.md`, and the P4 backlog entry updated to the new names; every historical decision-log entry, closed-backlog history, and session handoff left untouched, per the ticket's own scoping note. Delivered for Ryan to push, with the five old-named files to be deleted from the repo once the new ones land.
- **B84** — Converter's KNOWN LIMITATION note names the wrong page type — **NEW S172 (D262); SHIPPED S173 (D263); TOOLING.** The note ended "In these packs that is the Rules Updates page," which is false (Thousand Sons p1 is cover/contents, p5 is the Hexwarp Thrallband detachment page). Sentence dropped; the note now stops at the page numbers it already prints. Pure string edit in `faction_pack_transform.py`, verified by code inspection and a synthetic `_find_anomalies` run — no PDF needed for this one.
- **B77** — `SCINTILLATING LEGIONS` keyword absent from our data — **NEW S159 (D245); CLOSED S171 (D261),
  already-resolved, no build.** The S159 diagnosis (zero hits in `keywords.json`, carrier units carry an
  empty keyword list) does not match the current `units.json`: all six carriers (Kairos Fateweaver, Lord
  of Change, Flamers, Screamers, Pink Horrors, Blue Horrors) already carry `"Scintillating Legions"` in
  `faction_keyword_names`, sourced from Wahapedia's own `Datasheets_keywords.csv`, and `index.html`
  already renders it as a `Faction: Scintillating Legions` pill. `keywords.json`'s absence of an entry is
  correct — that file is a tooltip glossary for plain `keyword_names` only; faction keywords never look
  it up. `allied_group` (B61's mechanism) is untouched and still drives all real legality. No parser,
  engine, or data change made.
- **B72** — Outrider Squad ATV gated on wrong squad size — CLOSED S169 (D258); engine-only; `loOptMax` now exempts `non_consuming` optional groups from the headroom clamp so the Invader ATV is offered at every legal size; `index.html` v6.12
- **B80** — Combined popup: bodyguard's expand arrow opened the leader's section — CLOSED S169 (D258); engine-only; per-member `idScope` on `buildModalConfigured` so stacked panels no longer share section IDs; `b72_check.js` added; `index.html` v6.12

Full history for every one of these lives in `BACKLOG_ARCHIVE.md`, in the same order.
**`BACKLOG_ARCHIVE.md` is intentionally repo-only, not project-area resident (D217) — nothing in
the pipeline or gates reads it, so it does not sit in `/mnt/project`. Its absence from the mount is
not loss; fetch the current copy from
`https://raw.githubusercontent.com/rd-prime-1357/40k-army-builder/main/BACKLOG_ARCHIVE.md` before
appending to it, and hand the updated file back for Ryan to commit.

- **B81** — Manifest write could run before the decision log/handoff reached final text — SHIPPED S168 (D257); TOOLING. Third occurrence of the D239 defect class. `pipeline_manifest.py --freshness-check` added: re-hashes only the decision log and the latest session handoff against the manifest, run as the last command of session close after `--write`. Verified both directions (clean pass, then a deliberate edit made it fail with the file named, then reverted and passed again). Standing convention from S168: session close ends with `--write` then `--freshness-check`.
- **E21** — Detachment-driven army-construction effects (battleline / forbid / unlock / warlord) — CLOSED S139 (D218); E21a data (D209), E21b engine (D212), E21c engine + E22b (D214), E21d UI pieces 1-2 (D215) and piece 3 — the stranded-allied roster warning (`entryAlliedError`, D218) — all shipped. Full history in D203/D204/D209/D212/D214/D215/D218
- **B62** — `FALSE` string literal in Is Base Equipment (a real latent bug, not inert as first assumed), and no presence gate on the CD root CSVs — SHIPPED S138 (D216)
- **B60** — `detachment_parser.py`: `restrictions` populated inconsistently — CLOSED S142 (D221); DATA. Two root causes fixed (Wahapedia folding the restriction into `rule_text` in two shapes; DA pack bleeding stratagem clauses in where page-collated CP tokens defeat stratagem recognition). All 25 chapter-exclusive detachments now carry the restriction in `restrictions`, none in `rule_text`; 16 records changed, restrictions/rule_text only. Assertion follow-up split off as B60a
- **B60a** — Pin the `restrictions` consistency as an assertion — SHIPPED S143 (D222); TOOLING. Two new assertions in `rules_assertions.py`: 25 detachments carry the chapter-exclusivity sentence in `restrictions` and 0 in `rule_text`; no `restrictions` value carries stratagem/CP debris. 104/104 assertions pass
- **B67** — Two GW-derived files (`Unit_Weapons.csv`, `wh40k_core_rules.md`) removed from the public repo — CLOSED S145 (D225); Ryan deleted both, confirmed gone from HEAD via the API. D223's "single commit" premise corrected (249 commits); full history purge is a separate optional action, filed as B67b
- **B68** — `equipped_parser.py` resolved web-composition titles through a flat name→unit_id map (last-write-wins), misrouting Death Guard's seven shared generic Chaos vehicle equipped lines to their CSM twins once both factions co-existed in `units.json` — CLOSED S152 (D235); ENGINE. Diagnosis corrected: bug was in `equipped_parser.py` alone, not `loadout_parser.py`. Fixed with army-scoped title resolution (`scoped_name2id()`, scope inferred from the composition filename); no caller edit, pure engine turn. `repro_check` byte-identical, no data regenerated, durable for the future CSM web pass. Unblocks CSM turn B
- **B79** — Detachment tag exclusivity — CLOSED S160 (D248); premise was wrong, not a gap: `index.html`'s `uniqueTagConflicts()`/`canAddDetachment()` already read `unique_tag` straight off `detachments.json` and refuse a second same-tag detachment, shipped generically (tested against Blood Angels' GRACE tag) before Thousand Sons existed. Death Guard's `ENGINES`/`FLYBLOWN` and CSM's `NIGHTMARE` tags were already enforced the same way. Confirmed live for Thousand Sons the moment turn C banked `detachments.json`: `SERVANTS OF CHANGE` and `WARPMELD PACT` both carry `unique_tag: "MUTANT"` and the engine already refuses selecting both
- **E24** — Thousand Sons allied unlock: gate the six Scintillating Legions carriers — CLOSED S161 (D250); turn A tagged the six carrier records in `units.json` with `allied_group: "Scintillating Legions"`, TS-priced (Pink Horrors 115, Blue Horrors 90, not the CD 150/125); `Changehost of Deceit`'s unlock + warlord-ban flipped `enforced: true` in `detachment_effects.json`; `e21a_allied_targets`'s expected-unenforced list trimmed to the one remaining Chaos Space Marines gap (Shadow Legion / HERETIC ASTARTES)
- **B78** — Thousand Sons Battleline grant needs two `detachment_effects.json` rows — CLOSED S161 (D250); both rows shipped once turn A landed a Tzaangor unit: `Servants of Change` and `Warpmeld Pact` each target only `Tzaangors` (unit_id `000001034`), the sole TS datasheet carrying the TZAANGORS keyword — Tzaangor Shaman and both Tzaangor Enlightened datasheets carry their own distinct keywords and are correctly not elevated. `e21a_coverage`'s `known_gap` allowlist removed (no longer needed); `e21b_check.js`'s pinned battleline-table count updated 5 → 7
- **E25** — Force Disposition selection: one required per army list — CLOSED S165 (D254); ENGINE. All seven spec points shipped: deduplicated list-tolerant derivation (`[].concat(...)`), auto-select on a singleton set, additive `force_disposition` field inside the unbumped schema (mirrors `warlord_entry_id`), invalidation on detachment change, missing-selection flag-and-warn (found no existing missing-warlord precedent to mirror — built on the real `det-list-warning` pattern instead), a `fdisp-picker` control next to the warlord picker, and the Army List output line (`det-list-info` when resolved, `det-list-warning` when not). New `e25_check.js`, 25/25 checks pass, added to `baseline.sh` and `pipeline_manifest.py`
- **B71** — Config panel: expanded options collapsed on any selection, not just the toggle icon — CLOSED S166 (D255); ENGINE. Root cause: `mkDetail()`'s expander ids were assigned from a per-render sequence counter, so an id (and thus "open" state) could not survive the rebuild a selection elsewhere in the group triggers. Fixed by keying expanders on a stable string (entry id + option/group identity) hashed into the DOM id, with a persistent `openDetailIds` Set read at render time; only `toggleDetail()` (the icon click) changes membership. All 20 call sites across the enhancement picker, wargear swap/indep/bundle groups, unit options, and the main loadout modal updated with real stable keys. New `b71_check.js`, 9/9 checks pass, added to `baseline.sh` and `pipeline_manifest.py`

- **H3** — `pipeline_manifest.py` custody — CLOSED S126 (D198); `repo_check.py` confirms the script is present and byte-identical in the public repo
- **H4** — Ryan's per-session repo refresh becoming routine — CLOSED S126 (D198); repo_check.py found the bulk upload had happened and 67/67 shared files matched
- **T1** — `repo_check.py` (net new) — CLOSED S126 (D198)
- **T2** — SHA-256 hash convention in handoffs — CLOSED S126 (D198)
- **T3** — `baseline.sh` (net new) — CLOSED S126 (D198)
- **T4** — known-failure allowlist in `bundle_check.js` — CLOSED S126 (D198)
- **T5** — backlog/decision-log split (`BACKLOG_ARCHIVE.md`, `DECISION_INDEX.md`, both net new) — CLOSED S126 (D198)
- **T6** — module-extraction policy — CLOSED S126 (D197)

- **B1** — Ability-description collision (SYSTEMIC) — AUDITED S76 (D141), residual risk (B1b) SHIPPED S77.
- **B2** — "Leader" rule shows the game Leadership rule, not the unit's Leader ability — CLOSED (audited S78, D143)
- **B3** — Wrong faction assignment: Chaplain Kastiel & Judiciar Xacharus — CLOSED (already resolved)
- **B4** — Roboute Guilliman missing abilities — SHIPPED S87 (D155)
- **B5** — SM Lieutenant weapon swap wrong (all-three-at-once) — SHIPPED (v5.41)
- **B6** — Captain weapon swap wrong (one-of-the-following) — SHIPPED (v5.41)
- **B7** — Multi-leader attachment not supported — CLOSED S89 (D157) — mechanic already shipped in B38 cluster; residuals reshaped into B7a and B7b
- **B7a** — leader-stack cap semantics (engine) — CLOSED S90 (D158)
- **B7b** — combined attached-unit popup with per-stat aura markers — CLOSED S91 (D159); cluster: leader system
- **B8** — Unit classification mis-buckets multi-model units — CLOSED (D71, v5.36→v5.37) — backlog entry was stale, corrected S92
- **B9** — Company Heroes weapon counts (heterogeneous fixed group) — SHIPPED
- **B13** — Victrix embedded Epic Heroes: optional-model toggle + 1-per-army cap — CLOSED (D158 Piece 1 v5.79 S92; D159 Piece 2 v5.80 S93)
- **B10** — DW Decimus Kill Team: no config options / not attachable — CLOSED (stale; corrected S92)
- **B11** — SV/LD data carries a trailing "+" while INV/FNP are bare — CLOSED S109 (D177)
- **B12** — Wargear stat effects not applied to the statline — CLOSED (v5.39–v5.42)
- **B15** — Conferred always-on wargear characteristics not on the statline (broad pass) — CLOSED S53 (D112, v5.59)
- **B14** — Optional per-model wargear matcher ("1 X can be equipped with…") — DONE (SM), D76
- **B14b** — Mixed weapon+item exclusive group (Impulsor group C) — CLOSED (D99, S44)
- **B18a** — option scope: generic "models" means EVERY model group (uncapped shapes) — CLOSED S58 (D120)
- **B18b** — pooled cap on `count` options — CLOSED S61 (D126); index.html v5.66
- **B18c** — fan the capped generic swaps (two clean units) — CLOSED S65; DATA; `unit_loadouts.json` 217 units / 327 options
- **B18d** — capped generic swaps on leader-conflict units — CLOSED S82 (D149); equipped_parser.py + unit_loadouts.json 217/336
- **B18e** — engine: enforce shared `pool_id` cap on the weapon rollup — CLOSED S64 (D129); index.html v5.67
- **B18f** — general capped-generic fan for remaining under-grant units — CLOSED S83 (D150) — no defect; candidate list rested on a D116 misreading
- **B18g** — Decimus Kill Team infernus heavy bolter: generic swap under-granted to a second body group — CLOSED S86 (D153)
- **B18h** — executable D116 guard on the fan allowlist — CLOSED S84 (D151)
- **None** — ### B18 (original) — CLOSED S99 — every sub-item shipped; header was stale
- **SG1** — Sanguinary Guard banner (one-model item add) — DONE (D85, S30)
- **B14c** — Bearer-qualified adds ("1 model equipped with a <weapon> can…") — CLOSED S99 — all three parts shipped; header was stale
- **B14c(b)** — bearer-gated adds, data half — DONE (Session 37, D92)
- **B19** — `requires_weapon` gate: carrier counting (engine) — DONE (Session 36, D91, v5.52)
- **B20** — `count` swaps scoped to a single-model group are silently ignored (engine + data) — CLOSED (D93 engine S38, D94 parser+data S39; stale entry corrected S92)
- **B21** — Options mis-scoped to the base group when the required weapon lives in a variant group — CLOSED S114 (D182)
- **B58** — banded optional model groups (0-N) are treated as 0-or-1 toggles — CLOSED S113 (phase 1 D180 / phase 2 D181)
- **B59** — Invader ATV should ride alongside the Outrider Squad and its +60 is uncharged — CLOSED S116 (D182/D183/D184); SHIPPED ACROSS B59a + B59b
- **B59a** — Engine: `non_consuming` handling in `loOptHeadroom` / `loGroupCounts` — CLOSED S115 (D183); ENGINE-ONLY; M
- **B59b** — Data / parser: MFM additive-line parser + Outriders group flip — CLOSED S116 (D184); DATA-ONLY; M
- **B63** — Soul Grinder shipped all four god weapons at once, live D0 violation — SHIPPED S132 (D207); `Allegiance_Condition` restored, `units.json` re-banked, four assertions (B63-1..4) pin the shape; render not yet eyeballed by Ryan
- **B61** — Plague Legions units offered to every Death Guard army, ungated — SHIPPED S133 (D208); `mfm_points_parser.py` tags via a known-label lookup, `units.json` re-banked (exactly six units gained one key), four assertions (B61-1..4) pin the census; selection-time gate is E22b (S136), not this ticket
- **E22** — Detachment ally unlocks, points sub-caps and Warlord bans — CLOSED S136 (D214); E22a shipped as B61 (D208, allied_group tag), E22b shipped S136 as the engine gate (offer filter + battle-size points sub-cap + detachment-scoped Warlord ban) alongside E21c. Death Guard | TALLYBAND SUMMONERS fully enforced; Chaos Daemons | SHADOW LEGION HERETIC ASTARTES unlock stays enforced:false in detachment_effects.json until CSM is built. Full history in D203/D204/D208/D214
- **B64** — Detachment (i) opened detail inline in the left panel — SHIPPED S137 (D215); now opens the shared centered modal, same treatment as the unit full-datasheet popup; row keeps only name/battle trait/DP
- **B65** — Over-DP-budget detachment rows rendered their refusal in red — SHIPPED S137 (D215); red now reserved for the forbid-conflict case (a real D0 guard), budget/duplicate/tag-clash/unknown use a new muted `.det-refusal-neutral` style, per E3/D114's convention
- **B66** — Config-panel single-item detail button used an eye icon — SHIPPED S137 (D215); `infoBtn()` is the one shared renderer for every configurable item across the panel, so the glyph swap (eye → info-circle) fixed it project-wide in one place
- **B32** — engine: `requires_weapon` with more than one weapon — CLOSED S49 (v5.57)
- **B33** — negated gates — CLOSED S50 (data)
- **B35** — paid wargear options — CLOSED (data half S51, engine half S52)
- **B34** — Size-gated wargear swaps (`required_size`) — CLOSED S95 (D160 + D161)
- **B42** — Vanguard Veterans' storm shield is missing from the loadout def — CLOSED S58
- **B43** — Wardens of Ultramar: Refractor Field has no carrier — CLOSED S58 as a duplicate of B44 (D121)
- **B44** — statline groups and loadout groups have no shared key — CLOSED S72 (D135 data half, D136 engine half)
- **B36** — Lieutenant wargear options are wrong — CLOSED S54 (D113), `index.html` v5.60
- **P3** — file-integrity manifest + reproduction gate — DONE (Session 59, D123)
- **B37** — Captain wargear panes are mislabelled — CLOSED S88 (D156), no build needed
- **B38** — a second leader on one unit (co-leader) — CLOSED S81 — B38-engine SHIPPED S79 (D145); B38a SHIPPED S80 (D146); B38b SHIPPED S81 (D147)
- **B39** — Bloodthirster options lock each other out wrongly — CLOSED S67 (D131)
- **B39b** — Audit the whole bundle queue for the same leftover-flat-swap class — CLOSED S67 (D131)
- **P4** — RESOLVED S68 (D132). units.json rebuild fixed point re-established for all 14 blocks.
- **B40** — Bloodmaster is missing its Leader rule — CLOSED S69 (D133), not a bug
- **B41** — Epic Heroes: adding past the limit should be blocked, not flagged — CLOSED S55 (D114 + D115)
- **B45** — army-level legality rules — CLOSED S100 — header retired S73 (D137), fully re-homed; kept surfacing as a candidate pick
- **E14** — Free, unconditional adds default to selected — CLOSED S56 (D117, v5.63)
- **B46** — wargear abilities granted by an OPTION never reach the popup — DONE (Session 59, D122; index.html v5.64)
- **B47** — information buttons on every configurable item and every option group (Configuration Panel) — DONE (Session 60, D124). v5.64 → v5.65
- **B48** — Corvus Blackstar renders two controls for the same wargear — DONE (Session 60, D125). Rode with B47
- **B49** — Leader section: show the character's attachment rule, not the generic core "Leader" blurb — CLOSED S70 (D134)
- **E15** — "Transport" as an ability, not just a keyword — CLOSED S97 (D163)
- **E16** — Sort control on "My Army Lists" page — DONE (Session 32, D87)
- **E17** — Asterisk on statline stats that have a non-representable rule benefit — DONE (D89, v5.51); SUPERSEDED S53 (D112)
- **E2** — Collapsible/expandable left-panel sections — SHIPPED S117 (D185)
- **E3** — Left-panel unit counts: red only when EXCEEDED, not when max is met — CLOSED S55 (D114)
- **E1** — Detachment selection system — CLOSED S125 (D196); parent over E1a/E1b/E1c/E1e; all four shipped
- **E1a** — Detachment data turn: parser + `detachments.json` — CLOSED S123 (D193/D194); DATA-ONLY; `detachments.json` 14 armies / 143 distinct records / 275 army slots / 515 enhancements / 797 KB
- **E1b** — Detachment state + persistence — CLOSED S124 (D195); ENGINE-ONLY; `index.html` 6.1 → 6.2
- **E1c** — Detachment picker + detail UI — CLOSED S125 (D196); ENGINE-ONLY; `index.html` 6.2 → 6.3
- **H2** — Retire three superseded Wahapedia join tables from the project file area — CLOSED S124 (D195); housekeeping
- **E1e** — Enforce detachment Unique-tag exclusivity — CLOSED S125 (D196); engine + UI
- **E5** — Rename banner "List Points" → "LIST POINTS" with two figures — SHIPPED S87 (D154)
- **E6** — Affordability cue on left-panel units — SHIPPED S118 (D187)
- **E7** — More spacing between points / info / x in the center panel — SHIPPED S87 (D154)
- **E8** — Delete safety — SHIPPED S87 (D154)
- **E9** — Warlord selection — DONE (Sessions 75–76, D139, D140)
- **E4** — Detachment enhancement assignment — CLOSED S129 (D199 scope, D200 engine, D201 UI); full body in `BACKLOG_ARCHIVE.md`
- **B50** — off-by-one column index in `wahapedia_transform.py` post-processing — DONE (Session 74, D138)
- **B51** — Blue Horrors' abilities/rules/keywords were miscolumned in the CD source — DONE (Session 75, D139)
- **B52** — `Sullen Malevolence (Aura)`'s ability description is truncated in the CD source — SHIPPED S77
- **B53** — Combined attached-unit popup renders bodyguard on top, leader on bottom — should be leader first — **CLOSED S96 (D162); `index.html` v5.81 → v5.82
- **B56a** — chapter Unit_Points rows (scoped) — SHIPPED S101 (D168)
- **B56b** — parser: composition-shaped size-bracket lines — SHIPPED S102 (D170) — Crusader Squad only
- **B56g** — Wolf Guard Headtakers: Hunting Wolves escort is an optional priced model group — CLOSED S108 (D174, D175, D176)
- **B56** — 81 built units carry no points (cluster header) — CLOSED S129 (D202); verified against `units.json` directly — 270 units total, exactly 2 null-points (Judiciar Xacharus, Chaplain Kastiel, both retired by Ryan's S121 call, B56e) — header was stale, all sub-items had already shipped; full body in `BACKLOG_ARCHIVE.md`
- **B57** — in-between unit sizes are not offered anywhere — CLOSED S118 (D186); no build needed
- **B56c** — derive the per-chapter points override map — SHIPPED S103 (D171)
- **B56d** — engine: apply the chapter override at selection — SHIPPED S104 (D172)
- **B56e** — Judiciar Xacharus & Chaplain Kastiel have no points source — RETIRED S121 (Ryan: disregard these characters)
- **B56f** — Venerable Dreadnought priced twice, generic and chapter disagree — CLOSED S101 (D169)
- **B54** — Be'Lakor's Shadow Form ability shows the rule name but not the pickable abilities — CLOSED S110 (D178)
- **B55** — `abilities.json` has drifted from what the pipeline currently produces — CLOSED S98 (D164)
- **E10** — Duplicate unit in center panel — DONE (S81, D148)
- **E11** — Light/dark background toggle — SHIPPED S120 (D190); closed
- **E20** — Visual polish, phase 2 (deferred items from E11's pass) — CLOSED S121 (Ryan: not pursuing)
- **E19** — Move Configured/Remaining points next to Army Points in the banner — SHIPPED S119 (D188)
- **E13** — Drop "Keep" prefix from default swap-option labels — CLOSED S84 (D151)
- **E18** — JSON export / import (list portability + data-loss recovery) — DONE (Session 27, D82).
- **B16** — Per-model-group default weapons (weapon-count fix) — DONE (Session 23, D78).** Fixed in equipped_parser.py via a Datasheets.csv loadout-column gap-filler; 19 units repartitioned, 0 regressions.
- **B22** — "1 model's X can be replaced" is parsed as a per-5-models allowance (parser + data) — CLOSED (D94, S39)
- **B23** — compound "A and B can be replaced with C" — `count` family CLOSED (D95, S40)
- **B23b** — compound source on a `choice` option (engine + parser) — CLOSED (engine D97/v5.54 S42; parser D98 S43)
- **B26** — per-N "up to N models can each have their X replaced with Y" — CLOSED (D96, S41)
- **B20** — CLOSED (engine half D93/v5.53; parser half D94/S39)
- **B24** — profile-pinned `replaces` / `replacement` — CLOSED (D95, S40)
- **B27** — Whirlwind's `default_weapons` contain weapons the unit does not have — CLOSED (D96, S41)
- **B25** — two `choice` options in one single-model group replace the same weapon (engine/UI) — CLOSED (D97, v5.54, S42)
- **None** — ### B23b (parser half) — stop reducing a compound source — **CLOSED (D98, S43)
- **B30** — the replacement side of a `single` swap isn't split on " and " — CLOSED S45 (D100)
- **B31** — an "A or B and C" source — CLOSED S99 (D165); DATA; `bundled_swaps.json` + `units.json`
- **B28** — a swap whose source is a wargear *item*, not a weapon — CLOSED (D101 engine S46, D102 data S47; header corrected S92)
- **B29** — "Additional Combi-Bolter" isn't normalised to a weapon — CLOSED (D98, S43)
- **P1** — `loadout_parser.py` stale-copy failure — CLOSED S57 (D118)

## Cross-cutting notes

- **Combinatorial-swap cluster** (B5, B6, plus the banked Devastator Sergeant
  "pick two"): all need one shared design decision on the control model —
  mutually-exclusive option *sections* where picking one atomic multi-weapon swap
  locks the others. Design this once, apply to all three.
- **Leader-system cluster** (originally B7 multi-leader, E9 Warlord, plus the banked attached-unit
  combined popup): substantially shipped. B38 cluster (D144–D147) shipped the multi-leader mechanic;
  E9 shipped (D139/D140); B7 closed S89 (D157) with residuals reshaped into B7a and B7b. B7a (stack
  cap engine refinement) shipped S90 (D158). B7b (combined popup with aura markers) closed S91 (D159).
  The cluster is fully shipped. *(This note said B7b was still open until S124; it had been closed for
  thirty-odd sessions — the exact drift D107 warns about, in the document meant to track what is open.)*
- **Detachment cluster** (E1a→E1b→E1c, then E4 and E21; E5's "Remaining" total feeds off the same
  points math): scoped S122 (D192), authoritative write-up in `E1_DETACHMENT_SCOPE.md`. Build order
  is fixed and not open for re-litigation — E1a is a data-only turn, E1b and E1c are engine-only
  turns, and they cannot be merged without breaking the never-mix rule. The new pipeline path is
  MFM-first (11th Ed, authoritative on DP and points) with the 10th-Ed Wahapedia dump joined in for
  description text only. E21 (require/forbid, unit unlocks, Battleline elevation) is deliberately
  downstream of E1c, not part of it.
- **Sequencing intuition** (for discussion, not committed): B1 first (credibility —
  wrong rule text is worse than a missing feature), then the quick UI wins
  (E3, E7, E2, E5), then the detachment foundation (E1→E4→E6), with the
  combinatorial-swap and leader-system clusters slotted per your priority.
