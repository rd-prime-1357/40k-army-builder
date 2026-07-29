# Session Handoff 154

## Baseline at open

Read `SESSION_HANDOFF_153.md` and `NEXT_SESSION_PROMPT.md` (S154 header) as instructed. Found a real
mount anomaly before starting: `40K_Decision_Log_v3_0.md`, which S153 recorded as workspace-resident and
holding D236, is absent from the mounted project area this session, and `D231_entry.md`–`D234_entry.md`
— which S153 recorded deleting — are still present there. Read as the project-area mount going stale
after S153's uploads (it is a point-in-time snapshot, not authoritative for presence/absence, per
standing constraint), not a real regression. Not acted on beyond flagging: D237 below is banked as a
standalone entry rather than appended to a log file I can't verify is genuinely gone or genuinely
present. Ryan: if `40K_Decision_Log_v3_0.md` is intact in your local copy or the repo, fold D237 in
directly — same treatment D231–D234 got at S153. If it's genuinely missing, a fresh upload will confirm
that and next session can rebuild the workspace-resident copy properly.

Ran the turn's own gate — `detachments_repro_check.py` — against a from-source rebuild rather than the
full `baseline.sh` (that needs the whole project tree; this session only pulled the detachment-build
input set). It passed clean; see below.

## What shipped — D237, CSM turn C (data-only), closing the CSM detachment build

Per `CSM_BUILD_SCOPE.md` §3/§6 and the S154 prompt.

**`detachment_parser.py`** gained CSM's three config lines: `ARMY_TO_MFM` ("Chaos Space Marines" →
`MFM_Chaos_Space_Marines_v1_0.txt`), `MFM_SOURCE_NAME` (that file → "Chaos Space Marines"), and
`ARMY_TO_WAHA_FACTION` ("Chaos Space Marines" → "CSM"). **`detachments_repro_check.py`** gained the CSM
MFM file in its required-inputs list.

**`detachments.json` regenerated: +17 CSM detachments** (143 → 160 records, 14 → 15 armies, 275 → 292
army-detachment slots, 515 → 577 enhancements). Diff-traced key-by-key against the previously-committed
file: every added key belongs to Chaos Space Marines, zero existing records changed, zero removed, and
no other army's own detachment-slot list moved. Matches D192/§3: MFM is the source of record for the
17-detachment roster; the two MFM-only detachments (Devotees of Destruction, Murdertalon Raiders) came
through with no rule prose, enhancement names/points only (`text_source: none`); the other 15 sourced
their prose from Wahapedia's tier-2 text (CSM has no faction-pack tier-1 source, so all 15 read
`wahapedia_10e`); the three Wahapedia-only detachments were dropped as stale, per scope.
`detachments_repro_check.py` reproduces the result byte-for-byte from a clean rebuild.

Per the standing sequence, **M2 (Ryan, evict the 71 GW sources) is now unblocked** — this was the last
piece of CSM build work gating it.

**Two real gaps surfaced, both filed for the tooling turn, neither touched this session (turn-typing:
config lines plus the regeneration they drive only — no assertion or effects-file edit):**

- **E4b-3's pinned literal is stale.** The same-army enhancement-name collision census moved 29 → 30
  reachable collisions (5 → 6 distinct names) now that CSM's own enhancements are in `detachments.json`.
  The underlying rule (name-keyed duplicate detection, army-wide) is unaffected; only the number needs
  updating, alongside the other CSM assertions already scoped for the tooling turn.
- **New ticket B74.** CSM's Chaos Cult detachment grants TRAITOR GUARDSMEN SQUAD units the BATTLELINE
  keyword — a real construction effect with no row in `detachment_effects.json`. `rules_assertions.py`'s
  E21a-5 fails correctly the instant `detachments.json` carries this text; that's the assertion working
  as designed, not a false positive. Filed as its own small data turn against `detachment_effects.json`,
  to run once the tooling turn's CSM assertions are in.

`index.html` untouched — CSM's detachment picker needs no new mechanism, matching CSM_BUILD_SCOPE.md
§6's expectation.

## Decisions needed

None. The mount anomaly above is a reconciliation note for Ryan to confirm, not a choice; the two
surfaced gaps are sequencing calls (deferred to the tooling turn / a follow-up data turn), not
product or legality questions.

## Net New Files

- `D237_entry.md` — standalone decision-log entry, reviving the pre-S152 fallback pattern because
  `40K_Decision_Log_v3_0.md` is unreachable in the mount this session. Net new only in the sense that no
  file named exactly this exists yet; the *role* (a standalone D-entry awaiting fold-in) has existed
  before (D231–D234) and was retired at S153 — reviving it, not inventing it.

All other touched files are updates to existing parsers, regenerated outputs, or rolling documents.

## Files (SHA-256, first 12 chars)

- `detachment_parser.py` — `98183c6bdb5d`
- `detachments_repro_check.py` — `c0424dab7f71`
- `detachments.json` — `d556b96ea775`
- `DECISION_INDEX.md` — `07979be6f1db`
- `OPEN_ITEMS_BACKLOG.md` — `c537425bc8ed`
- `D237_entry.md` — `8432371b7803` (net new)
- `SESSION_HANDOFF_154.md` — self-referential; hash after upload for the manifest
- `NEXT_SESSION_PROMPT.md` — hash after upload for the manifest
