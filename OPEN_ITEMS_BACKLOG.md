# Open Items Backlog

Originally logged Session 18; reorganised **S126 (T5)** — closed/shipped ticket bodies moved in
full to `BACKLOG_ARCHIVE.md`. Each keeps a one-line pointer here (ID, title, closing session,
decision reference). The Open Items section below is the only section awaiting work; if it is
not here, it isn't open. **12 open** as of S169: B69, B70, B73, B75, B76, B77, P2, P4, E23, B67b, E12, B17. B72 and B80
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

### B70 — Wardens of Ultramar cannot be attached to a unit — **NEW, Ryan-reported; S**
The detachment enhancement/unit "Wardens of Ultramar" cannot currently be attached to any unit in the
app. Ryan points to the "Heroes of Ultramar" ability as the source of the eligible-unit list and to a
Leader restriction that should apply. Needs the eligibility rule traced from that ability's rules text
into whatever governs attachment, likely a Leader-restriction gap similar to prior Leader-eligibility
bugs.

### B73 — Ultramarine Leader abilities list units outside their actual 40k eligibility — **NEW, Ryan-reported; M; likely spans multiple leaders**
Uriel Ventris's Leader ability text lists eligible units (Deathwatch, Crusaders, Kill Teams, etc.) that
are not valid attachments in a 40k Matched Play list — likely a case where the source ability text
covers eligibility across multiple game modes/contexts and the app is surfacing all of it rather than
filtering to what's legal in this app's scope. Ryan suspects this is not unique to Uriel and other
Ultramarine (and possibly other) Leaders carry the same over-broad list. Needs a source-level audit of
Leader eligibility text against actual Matched Play legality before scoping a fix.


### B75 — Faction pack Rules Updates pages: column resolution fails, text interleaves — **NEW S159 (D244); M**
`faction_pack_transform.py` resolves every datasheet and detachment page correctly (stat tables intact,
verified on Thousand Sons and Death Guard packs) but cannot resolve the portrait **Rules Updates** pages,
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

### B76 — Rolling documents carry frozen version numbers in their filenames — **NEW S159 (D246); S; clarity not safety**
Five docs carry `_vN_M` labels that have never incremented: the decision log has 29 commits under
`v3_0`, and no predecessor volume exists in repo history. Cost real time this session — a backup copy of
`40K_Data_Pipeline_Process_v0_6.md` was 16 lines short (missing Step 2b / B56a chapter-points procedure)
under an identical version string.
Rename to drop versions: `40K_Decision_Log.md`, `40K_Data_Pipeline_Process.md`, `40K_Functional_Spec.md`,
`40K_Architecture_Overview.md`, `40K_Data_Dictionary.md`. Cost: each name is referenced in 3–6 other
files, all five are manifest-keyed, historical handoffs keep pointing at old names (and stay untouched —
they are the record), and the repo needs a delete-plus-add the web uploader cannot do in one step.
Content identity is already handled by the manifest hash, so this adds no safety. Sequenced behind the
Thousand Sons build.

### B77 — `SCINTILLATING LEGIONS` keyword absent from our data — **NEW S159 (D245); S**
Thousand Sons Rituals and stratagems target "THOUSAND SONS **or SCINTILLATING LEGIONS**" units, but the
keyword exists nowhere in our data: zero hits in `keywords.json`, and the six carrier units have an
empty `keywords` list with `allied_group: "Scintillating Legions"` standing in. Any TS rule naming the
keyword has nothing to match against. Parser fix (never hand-edit output). Note `allied_group` must be
**retained** — it is B61's shipped mechanism feeding E22b's gate, not a placeholder to be replaced.

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
- **Not yet attempted: splitting `40K_Decision_Log_v3_0.md`.** Original step-1 plan (D211) included
  moving the log's archive half (~400 KB, out of 660 KB now) to a repo-only file the way
  `BACKLOG_ARCHIVE.md` was split off, with `DECISION_INDEX.md` preserving lookup. Deferred, not
  ruled out — the next candidate if capacity is still tight after `wh40k_core_rules.md`'s removal
  lands, though it is a bigger move (a new archive file, a cut-line decision) than the file removals
  done so far.

**Unknown, do not assume:** whether the displayed percentage is against the base ceiling or the
RAG-expanded one.


### E23 — `HEADHUNTER TASK FORCE`: the Tank Ace Character keyword grant — **NEW S134 (D209); M**

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

**Why it is not folded into `detachment_effects.json` as-is.** It is a **fifth effect kind** — a
muster-time keyword grant with a per-list count limit and a player choice of which units receive it.
That is player state, not a static table row: the selection has to be stored on the list, survive
save/load, and be re-validated when the detachment is deselected. It also lands on two pieces of
shipped code at once (E4's enhancement eligibility and E9's Warlord eligibility). Scope it properly
before touching the schema.

**First step is a scoping turn**, in D199's and D203's mould: confirm the Tank Ace keyword definition
against source for all six copies, decide where the selection lives in the list record, and decide
whether the grant is modelled as a sixth effect kind or as its own mechanism.


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
