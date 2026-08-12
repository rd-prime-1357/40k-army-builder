# NEXT SESSION PROMPT — Session 228

## Recommended turn type: depends on Ryan's B113 call (see below). Absent that, engine/scoping —
## B114 scoping, or GK §6/§7.

Read `SESSION_HANDOFF_227.md` first, then `B113_LEADER_RESTRICTION_SCOPE.md`. S227 opened B113 as
an engine turn, diagnosed it, and **stopped the build cleanly** — the scoped mechanic was wrong.
Nothing engine/data/assertion shipped. B113 stays open, re-scoped, and now carries a decision for
Ryan.

Open with `./baseline.sh --fetch`. If zero GW source files are resident in the workspace (they were
not at S227 open), a turn that needs to re-parse MFM will require `--fetch --data-turn` to fetch and
verify sources — S227 did this and noted it; do the same if the turn needs sources. Confirm clean
before starting; reconcile any failing gate before working, do not carry it forward.

## The B113 decision (blocks the B113 build, nothing else)

`B113_LEADER_RESTRICTION_SCOPE.md` §4 lays out the call. In short: the `LEADER:` line is an
attach-enabler, not an assignment restriction, so the S227 prompt's "refuse the enhancement unless
the leader is attached to the named unit" is wrong and would make 6 of 8 enhancements assignable to
nobody. The reachable illegal state is the "X model only" **bearer restriction** (in the
description prose, not the `LEADER:` line). Options:

- **(A) enforce the bearer restriction only** — recommended. A small curated, asserted
  per-enhancement bearer map (8 rows; 7 bearers are in the prose, Pact of Cursed Pinions needs one
  supplied). Enforced in the E4b `canAssignEnhancement` gate as a new reason. Medium engine turn.
- **(B) full attach-enablement** — expand `leaderEligible` while the enhancement is held. Larger,
  order-dependent, needs (A)'s data first. A separate later item, not a first step.
- **(C) capture-only, defer** — schema field now, no enforcement. Smallest, no legality gain.

If Ryan has picked, build accordingly. If not, do not build B113 — pick up B114 or GK §6/§7 below.
Under every option, do **not** implement the prompt-style attach-target assignment gate.

Settled inputs the build starts from, whichever option (source-derived S227, in the scope doc):
the corrected **8-instance** census (incl. the two Space Wolves cases), and the rule that the
`LEADER:` line binds to the enhancement **immediately above** it. Land these as a
`rules_assertions.py` census check (same shape as `e4b_name_collision_census`) at the top of the
build so scope cannot drift again.

## Also open, at your discretion

- **B114** — Chaos Daemons' `Shadow Legion` HERETIC ASTARTES unlock recorded `enforced: false` on a
  now-stale premise. Needs its own scoping pass. Different turn type from any B113 build — do not
  fold in.
- **GK §6 / §7** — carried unchanged for several sessions; still not investigated.
- **Repo push (Ryan's action)** — the pending push queue (S220 onward) is unchanged and still
  outstanding; S227's files add to it (see the handoff's Ryan-action section).

## Standing reminders

- Re-derive from source, don't trust prior-session prose — including this prompt's numbers. S227 is
  the case in point: the "6" was wrong for three sessions running.
- Turn typing stays strict. A B113 build (any option) is an engine turn; B114 is scoping; don't mix.

## Decisions waiting on Ryan

- **B113 mechanic** — the (A)/(B)/(C) call above. Recommended: (A).
- **B116** — unchanged. Drukhari's Harlequins/Anhrathe cross-book allied-inclusion mechanic (see
  `DRUKHARI_BUILD_SCOPE.md` §6). Build as its own follow-on ticket once Ryan decides whether/how to
  admit a cross-book allied-inclusion mechanic. Does not block anything shipped.
- **Next faction after Drukhari** — the documented priority order is fully built; no faction is
  queued. Recommendation stands: clear the small engine/scoping backlog (B113, B114, GK §6/§7)
  before revisiting which faction, if any, comes next. A genuine product-priority call, Ryan's,
  whenever convenient.

## Close

Produce the four documents, register `SESSION_HANDOFF_228.md` in `pipeline_manifest.py`'s GUARDED
list **before** running `--write`, and run `pipeline_manifest.py --freshness-check` as the **last**
command — S227's open found S226 had let a post-`--write` handoff edit slip past exactly this
check, so run it last and act on a red.
