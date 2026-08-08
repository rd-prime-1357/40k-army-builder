# NEXT SESSION PROMPT — Session 215

## Recommended turn type: scoping-only (World Eaters) or tooling-only (B111)

Read `SESSION_HANDOFF_214.md` first. S214 closed B109 (engine-only, `index.html` v6.18 → v6.19).
23 open items remain. Two candidates ready; pick per your own sequencing judgment (dev-manager
call, not something to bring back to Ryan).

## Candidate 1: World Eaters — scoping pass

Next faction in standard priority order (Heretic Astartes: Chaos Space Marines, Thousand Sons,
Death Guard, Emperor's Children all built; World Eaters is next before Chaos Daemons). Needs its
own scoping pass first, `CSM_BUILD_SCOPE.md`/`THOUSAND_SONS_BUILD_SCOPE.md`/
`EMPEROR_S_CHILDREN_BUILD_SCOPE.md` pattern — check current-edition datasheet count, points
coverage, any wargear or detachment gaps, before any data turn starts. Scoping-only turn, no
committed pipeline file touched.

## Candidate 2: B111 — WARGEAR_RE regex gap

Tooling turn. `mfm_points_parser.py`'s `WARGEAR_RE` doesn't match v1.1's bullet-less
`WARGEAR OPTIONS` lines (only the bulleted v1_0 format). After the regex fix, the wargear pass
needs re-running across every already-shipped faction, not just Emperor's Children's Defiler, and
diff-guarded in case another v1.1-only price change is hiding behind the same gap elsewhere — don't
assume EC's Defiler is the only casualty.

## Also open, at your discretion

- **B110** — Grey Knights' `faction_taxonomy.json` flag stays `built: false` until it has
  detachments (`detachments.json` currently has zero Grey Knights entries). No new information since
  S211.
- **B112** — Chaos Daemons' LORDS OF THE WARP detachment disposition unverified against v1.1. Not
  actionable until GW publishes a v1.1 Chaos Daemons detachment file. No action needed each
  session — just check whether GW has published one before assuming this is still blocked.

## Standing reminders

- `./baseline.sh --fetch` at open (`--data-turn` not needed for either candidate — World Eaters
  scoping and B111's regex fix don't require a data-turn open; B111's subsequent re-run across
  shipped factions will).
- All gates should be green at S214 close except `repo_check` (B108, Ryan action) — confirm before
  starting new work.
- Re-derive from source, don't trust prior-session prose — S211, S212, and S213 all caught real
  gaps or corrections by checking source directly rather than assuming an existing pattern held.
- Turn typing: World Eaters scoping touches no committed pipeline file at all (new scope doc only).
  B111's regex fix is tooling-only; the subsequent multi-faction wargear re-run is data-only and
  belongs in a separate turn. Do not combine either with the other candidate.

## Close

Produce the four documents, register `SESSION_HANDOFF_215.md` in `pipeline_manifest.py`'s GUARDED
list **before** running `--write`, and run `pipeline_manifest.py --freshness-check` as the **last**
command.
