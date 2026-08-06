# SESSION HANDOFF 200

**Turn type:** scoping-only (analysis). `GREY_KNIGHTS_BUILD_SCOPE.md` produced (net-new). No committed
data, parser or engine file changed. `index.html` untouched, stays v6.16.

## What happened
1. **Baseline opened 30/31 with one expected failure.** `repo_check` red on exactly the seven files
   S199 produced and predicted would drift until pushed — nothing unexpected. Every other gate green,
   118/118 assertions. Note the gate count reads 31 rather than 32 because `source-fetch` correctly
   skips when sources are already local from a prior fetch; that is by design, not a skipped check.
2. **Ryan set a standing rule (D293): always build from the newest MFM available**, units and
   detachments alike, for new builds as well as migrations. This had never been written down — B89's
   arc is v1.1 adoption in spirit, but D288–D291 each explicitly deferred the detachments side and
   left `detachments.json` at v1_0. For an already-built faction that deferral is coherent; for a
   **new** faction there is nothing to defer, so building detachments at v1_0 would mean authoring
   knowingly-stale values on first build. Accepted consequence: Grey Knights becomes the first army
   with v1.1 detachments while the other sixteen stay v1_0.
3. **Scoped Grey Knights from source, not from prior-session prose.** Full dry runs of
   `wahapedia_transform.py`, `mfm_points_parser.py`, `convert_to_json.py`, `loadout_parser.py` and
   `detachment_parser.py` (the last via a throwaway copy with Grey Knights registered in its three
   maps), all into temp dirs. Headline: **25 current-edition datasheets, not the raw 31** — the
   smallest faction build the project has done, fully self-sourced, pipeline runs it end to end today
   with no code changes.
4. **Verified the six exclusions against the MFM itself, not just Wahapedia.**
   `MFM_Grey_Knights_v1.1.txt` carries an explicit `LEGENDS` section header at line 279 with Draigo,
   Stern, the Grey Knights Dreadnought, the Relic Razorback and Servitors beneath it. Both sources
   agree. Worth knowing because Draigo's absence will look like a bug to anyone who doesn't check.
5. **Separated "excluded" from "unbuildable."** The Grey Knights Thunderhawk Gunship is priced
   *inline* in the MFM's main list (Matched Play legal per GW) but Wahapedia's Forge World source is
   edition `0` — no datasheet, no stats, nothing to build from. Not a rules judgement, a data gap,
   and it already applies to every built faction since every Forge World source except Adeptus
   Titanicus is edition `0`. Recorded, not fixed; does not block the build.
6. **Retired B94's open Grey Knights concern.** S194 recorded that Brotherhood Terminator Squad was
   mis-parsed by the `1ST TO 3RD` / `4TH +` copy-tier shape and was never fixed because Grey Knights
   was not a built army. That shape is present in v1_0 and **gone in v1.1** — the source carries an
   explicit `REQUISITION THRESHOLDS REMOVED` note and the unit is now a plain composition-bracket
   unit. Building from v1.1 sidesteps it rather than relying on B87's `esc4` reader.
7. **Found two defects, neither Grey Knights' fault, both opened as tickets.**
   - **B101 (engine, live D0 gap):** `loMaxCount` caps the total picks for a `max_total_all`/`up_to`
     option but nothing enforces that the picks differ. Three **already-shipped** Chaos Space Marines
     units carry the no-duplicate rule only as a literal string inside `replacement_choices` — so an
     illegal duplicate is reachable today, and the rule text renders as a fake selectable option.
     Grey Knights forces the issue: both Nemesis Dreadknights depend on it and cannot be authored
     around it.
   - **B102 (tooling, XS):** `detachment_parser.py --report` dies with a `KeyError` on any gap —
     records carry `source_faction`, the report writer reads `g["army"]`. Latent because no gate
     passes `--report`; a build or scoping session does, which is how it surfaced. Eleven gaps
     already exist across built factions.
8. `SESSION_HANDOFF_200.md` and `GREY_KNIGHTS_BUILD_SCOPE.md` registered in `pipeline_manifest.py`'s
   GUARDED list, manifest regenerated with `--write`, `--freshness-check` run last.
9. Decision log (D293) and its index entry, and backlog (B100 scoped; B101, B102 opened) updated.

## What's explicitly not done
No build work started — this was a scoping pass and it stops at the scope document, per the CSM and
Thousand Sons precedent. The two Nemesis Dreadknights cannot be authored until B101 lands, so the
Grey Knights units data turn is blocked behind an engine turn.

## One open question left deliberately unanswered
There is no `Grey_Knights_web.txt`, and `repro_check.py` requires one file per `WEB_PASSES` entry.
Chaos Daemons is precedent for a built faction in neither `WEB_PASSES` nor `FACTIONS`, and the
loadout run produced complete results for all 25 units with no web pass — so one is probably
unnecessary. But the web passes exist to supply *equipped* defaults and that has not been
demonstrated for Grey Knights. Left as the build turn's first check rather than assumed either way.

## State
- Baseline: 30/31 at open; `repo_check` red on S199's seven unpushed files only.
- `index.html`: untouched, **v6.16**.
- `units.json`, `detachments.json`, all parsers, `rules_assertions.py`: untouched — scoping only.
- `OPEN_ITEMS_BACKLOG.md`: **22 open** (up from 20 — new B101, B102). B100 scoped and now blocked on
  B101.
- `pipeline_manifest.json`: regenerated at close, 160 guarded files (`SESSION_HANDOFF_200.md` and
  `GREY_KNIGHTS_BUILD_SCOPE.md` added).
- `repo_check` will show drift until pushed — S199's seven files **plus** this session's:
  `GREY_KNIGHTS_BUILD_SCOPE.md` (net-new), `40K_Decision_Log.md`, `DECISION_INDEX.md`,
  `OPEN_ITEMS_BACKLOG.md`, `pipeline_manifest.py`, `pipeline_manifest.json`,
  `NEXT_SESSION_PROMPT.md`, `SESSION_HANDOFF_200.md` (net-new).

## Ryan action required
1. **Push the Calgar missing-comma fix** to the private repo's `MFM_Space_Marines_v1.1.txt` — still
   outstanding since S198, re-confirmed missing by direct fetch in S199. Not re-checked this session.
2. Push S199's and this session's public-repo changes — two sessions' worth now pending.
3. No file-list screenshot needed; nothing this session turned on project-area presence or absence.

## Decisions still waiting on Ryan
None. D293 was Ryan's call and is recorded. The B101-before-B100 sequencing is a development call
made under standing authority, not a product question — the scope document explains the reasoning
and Ryan can overrule it if he'd rather ship the Dreadknights capped-but-not-distinct.

## Files (SHA-256, first 12)
| file | sha256:12 | note |
|------|-----------|------|
| `GREY_KNIGHTS_BUILD_SCOPE.md` | 4108c81f5a57 | **net-new** — the session's deliverable |
| `40K_Decision_Log.md` | 4975982e82c6 | D293 appended |
| `DECISION_INDEX.md` | f9da595dea3e | D293 index entry |
| `OPEN_ITEMS_BACKLOG.md` | 29e8b8fde315 | B100 scoped; B101, B102 opened; 22 open |
| `pipeline_manifest.py` | 1ba68cc581dc | handoff 200 + scope doc registered in GUARDED |
| `pipeline_manifest.json` | (not self-guarded) | `--write`, 160 guarded files |
| `NEXT_SESSION_PROMPT.md` | 9f0fa7f11b2b | (unguarded by design) S201 |
| `SESSION_HANDOFF_200.md` | (this file) | net-new; hash banked in the manifest by `--write` |

## Backlog
22 open, up from 20 at S199. Beginning: B99, B98, B97, E28, B93, B90, B94, B89, B100, B85, B86, B69,
B70, B75, P2, P4, E23, B67b, E12, B17 (20). Resolved: none. Added: B101 (no-duplicate wargear
unenforced), B102 (`detachment_parser.py --report` crash). Ending: B99, B98, B97, B101, E28, B93,
B90, B94, B89, B100, B102, B85, B86, B69, B70, B75, P2, P4, E23, B67b, E12, B17 (22). B100 advanced
from unscoped to scoped-and-blocked-on-B101; B94's last open Grey Knights item retired inside the
scoping work.
