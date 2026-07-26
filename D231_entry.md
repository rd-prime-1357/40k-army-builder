## D231 — P4 scoped: area as working set, public repo fetch, private sources repo with token-in-area; Ryan's custody calls settled (S148)

P4 stops being a whitespace/eviction firefight (D211/D213/D219/D220) and becomes a target
architecture. Scoping note only — `P4_ARCHITECTURE_SCOPE.md` delivered, nothing built, no app/data/
gate touched this session. The problem restated at the right size: the project area cannot be the
long-term home for built data or GW sources, because at the full-faction goal built JSON alone
plausibly exceeds the entire area. The design target is therefore that **the area's size is
independent of faction count** — it holds only the per-session working set; everything else is
fetch-on-demand or regenerated into the workspace.

**Three homes.** (1) The public repo (`rd-prime-1357/40k-army-builder`) — built outputs, parsers,
harnesses, fixtures, all docs, the decision log, the handoff chain; already true today, verified this
session (units.json / index.html / unit_loadouts.json / detachments.json all hash-match the area
byte-for-byte). (2) A new private repo (`rd-prime-1357/data-sources`, created by Ryan this session) —
the 71 GW-derived source files, fetched into the workspace on data turns. (3) The area — a ~450 KB
working set: the prompt, the latest handoff, the backlog, DECISION_INDEX, index.html,
pipeline_manifest.json (the trust anchor), baseline.sh + support doc, and the source-repo token.

**The open, redesigned.** Read+verify the area against the handoff → fetch the public repo as one
tarball and verify every file against an extended `pipeline_manifest.json` (the area-resident manifest
is the pin; no commit SHAs needed) → overlay the dual-resident working set (area copy wins) → on data
turns, fetch the private sources repo with the token and verify against a new `source_manifest.json`
→ run the gates, tiered. Proven feasible this session: one codeload tarball request pulls all 102
public-repo files (1.07 MB).

**Gates tiered.** Tier A (every open, no sources): area-hash check, fetch-verify, all JS harnesses,
bundle_check, pipeline_manifest, repo custody check, and rules_assertions in a new `--tier a` mode.
Tier B (whenever sources are loaded; mandatory at every data-turn open and close): the three full
repro rebuilds and the source-first assertions. Skips are loud and counted; a data turn with sources
absent refuses to start. Net effect on the fixed-point discipline: no protection lost — the only
change is that detection of a silently corrupted *source* file moves from "next repro run" to "next
time sources load," which `source_manifest.json` closes by hash-pinning the sources themselves.

**Recovered gate.** `repo_check.py` — absent from the area since before S147, every recent baseline
run `--no-repo` — lives in the repo; the fetch-open brings it back as a standing tier-A gate.

**Ryan's custody calls, settled this session (the reason this is a decision entry, not just a note):**
- **Accept-risk posture.** GW-derived text in a *private* repo is acceptable for the pre-release,
  non-commercial, personal-use window. GW points/rules text is copyrighted regardless of being
  published, so this is a real, small, deliberate exposure — worst realistic case is a takedown
  notice. **Public launch is the custody checkpoint** where this is revisited (private repo vs. fully
  local vs. a changed posture). Recorded so a future session treats launch as a decision point, not a
  silent continuation.
- **Private repo, not the earlier zip-on-machine recommendation.** Removes the per-turn attach step
  for the same custody outcome; sources sync by push like everything else. The zip (`gw_sources.zip`,
  same 71 files, same `source_manifest.json`) is demoted to the offline/no-credential fallback, so no
  single point of failure gates data work.
- **Token lives in the area.** A fine-grained, read-only, single-repo personal access token in
  `SOURCE_REPO_TOKEN.txt` — persistent, so no per-session paste. Ryan's threat-model reasoning
  accepted: the real risk is not an attacker (GW will not hunt a token) but the one accident that the
  area syncs to the *public* repo and carries the token in. Defused by a **hard custody gate**, not a
  prose reminder: `repo_check.py` gains a fail-loud rule that fails the session if the token filename
  (or a token-pattern match) ever appears in a public-repo-bound file list, backed by a `.gitignore`
  line. Read-only-single-repo scoping means a leak exposes only GW points files (mostly gettable from
  Wahapedia anyway) and is revocable in seconds.
- **Product call folded in:** app stays in the current public repo (open/forkable path preserved),
  only GW sources go private. Whole-project-private was considered and rejected.

**Rejected:** encrypting sources into the public repo (ciphertext of GW's text, publicly hosted, is
legally murkier for no gain); a token pasted per-session (more friction, same or worse exposure than
the guarded area file for this threat model).

**Migration M0–M3, sequenced (dev-manager call):** M0 next session (tooling-only — extend the
manifest to full public-repo coverage; add fetch-unpack-verify-overlay + token-authed private fetch
with zip fallback to baseline.sh; tier-tag rules_assertions and the three repro gates; create
source_manifest.json; wire repo_check.py back in with its token guard; codify close-protocol changes.
Exit test: old and new open both green same session, tier B green since sources still local. No
eviction, no rollback needed). Then M1 (Ryan evicts the repo-resident set from the area, ~3.9 MB,
screenshot-verified), B68 (engine turn), CSM turn B doubling as the M2 dress rehearsal (runs from the
token-fetched private copy while area copies still exist), M2 eviction of the 71 sources (~7.3 MB),
CSM turn C. One added session total; every migration step after M0 rides queued work. M0 goes before
the remaining CSM turns because the area is at capacity now.

**Close-protocol changes recorded for M0 to implement:** the handoff Files section gains a line for
the updated `pipeline_manifest.json` hash, and **drops `NEXT_SESSION_PROMPT.md` from the hash list** —
this session's own open confirmed the prompt is legitimately edited after the handoff is finalized
(its S147 hash didn't match while all ten substantive files did; not a bad sync, the prompt documents
the log removal and post-dates the handoff), so its hash can only ever false-alarm.

**Amendment, for Ryan's confirmation:** for migration eviction batches only (M1, M2), verification is
full file-list screenshots before and after, in place of the per-file card the one-off deletion rule
calls for — that rule doesn't scale to ~70-file batches.
