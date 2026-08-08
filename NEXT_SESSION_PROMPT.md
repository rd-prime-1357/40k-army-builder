# NEXT SESSION PROMPT — Session 214

## Recommended turn type: engine-only (B109) or scoping-only (World Eaters)

Read `SESSION_HANDOFF_213.md` first. S213 closed B89 — both halves of the MFM v1.1 detachment
adoption arc are done for every currently-built faction except Chaos Daemons, which is blocked on
GW publication and now tracked separately as B112. Two candidates are ready with no scoping needed
for the first; pick per your own sequencing judgment (dev-manager call, not something to bring back
to Ryan).

## Candidate 1: B109 — "My Army Lists" page label fix

XS, engine-only, `index.html`'s `renderMyLists()`. The render site was located at S209: the line
`const tgt = r.points_target ? ('target ' + r.points_target) : '';`. One-line change to something
like `(r.points_target + ' Points')`. Still not touched after six sessions running. Doesn't block or
get blocked by anything else open.

## Candidate 2: World Eaters — scoping pass

Next faction in standard priority order (Heretic Astartes: Chaos Space Marines, Thousand Sons,
Death Guard, Emperor's Children all built; World Eaters is next before Chaos Daemons). Needs its
own scoping pass first, `CSM_BUILD_SCOPE.md`/`THOUSAND_SONS_BUILD_SCOPE.md`/
`EMPEROR_S_CHILDREN_BUILD_SCOPE.md` pattern — check current-edition datasheet count, points
coverage, any wargear or detachment gaps, before any data turn starts. Scoping-only turn, no
committed pipeline file touched.

## Also open, at your discretion

- **B110** — Grey Knights' `faction_taxonomy.json` flag stays `built: false` until it has
  detachments (`detachments.json` currently has zero Grey Knights entries). No new information since
  S211.
- **B111** — `mfm_points_parser.py`'s `WARGEAR_RE` regex doesn't match v1.1's bullet-less
  `WARGEAR OPTIONS` lines. Tooling turn; re-running the wargear pass afterward needs diff-guarding
  across every already-shipped faction, not just Emperor's Children's Defiler.
- **B112** — Chaos Daemons' LORDS OF THE WARP detachment disposition unverified against v1.1. Not
  actionable until GW publishes a v1.1 Chaos Daemons detachment file. No action needed each
  session — just check whether GW has published one before assuming this is still blocked.

## Standing reminders

- `./baseline.sh --fetch` at open (no `--data-turn` needed for either candidate — B109 is
  engine-only, World Eaters scoping doesn't touch committed pipeline files).
- All gates should be green at S213 close except `repo_check` (B108, Ryan action) — confirm before
  starting new work.
- Re-derive from source, don't trust prior-session prose — S211, S212, and S213 all caught real
  gaps or corrections by checking source directly rather than assuming an existing pattern held.
- Turn typing: B109 is engine-only (`index.html` only). A World Eaters scoping pass touches no
  committed pipeline file at all (new scope doc only). Do not combine either with a data turn.

## Close

Produce the four documents, register `SESSION_HANDOFF_214.md` in `pipeline_manifest.py`'s GUARDED
list **before** running `--write`, and run `pipeline_manifest.py --freshness-check` as the **last**
command.
