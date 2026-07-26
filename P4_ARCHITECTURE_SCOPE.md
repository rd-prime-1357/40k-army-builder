# P4 — Project-area long-term architecture (scoping note, S148)

**Status: design for Ryan's approval. Nothing here is built.** Direction approved in shape at S147's
close (log removal was the accidental prototype); this note works out the details. Numbers below were
measured this session unless marked otherwise.

---

## 1. The problem, sized

The project area holds 11.75 MB across 146 files today, at or near 100% of capacity. It breaks down:

- **GW-derived source — 7.28 MB (62%), 71 files.** The Wahapedia CSV export (~5.3 MB), the MFM `.txt`
  files, the `_web.txt` composition files, the faction packs, `Army_Muster_Rules.txt`, the reference
  markdowns, and the pipeline-intermediate CSVs that carry GW text verbatim. None of this may ever
  reach the public repo.
- **Built outputs — 3.11 MB (26%).** `units.json` (2.03 MB), `detachments.json` (0.79 MB), and the
  eleven smaller JSONs. All already live in the repo — they are the deployed app's data.
- **`index.html` — 0.34 MB.** The product.
- **Everything else — ~1 MB.** Parsers, harnesses, fixtures, checks, docs. All already repo-resident.

At the honest near-term scope (SM family + CSM variants + Daemons + Drukhari), built data alone
roughly triples — `units.json` heads toward 5–6 MB. At the eventual goal of **all 40K factions**,
built JSON plausibly reaches 15–20 MB, larger than the entire area. So the design target is not
"fit the next few factions with headroom." It is: **the area's size must be independent of faction
count.** The area holds the per-session working set; content growth lands somewhere that doesn't care.

## 2. Target state — three homes

**The public repo** (already true today, verified current this session — `units.json`, `index.html`,
`unit_loadouts.json`, `detachments.json` all hash-match the area byte-for-byte): built outputs,
parsers, pipeline scripts, harnesses, fixtures, all reference docs, the decision log, the backlog
archive, the full handoff chain. 102 files today. Nothing about any file's public status changes —
this plan only moves where sessions read files from, never what is published. The custody line stays
exactly where practice has it: the 71-file area-only set is the never-commit set. (Audited this
session: the area-minus-repo delta is exactly those 71 files; zero GW source in the repo.)

**A second, private GitHub repo** (`rd-prime-1357/40k-sources`, or similar): the 71 GW source files.
Private so GW-derived text never sits on a public server. Fetched into the session workspace on data
turns with a read-only token; that token lives in the project area under a fixed name, hard-guarded
out of the public repo by the custody check. Section 5 is the full design, including how the token
works and the zip that stays as an offline fallback.

**The project area** — the permanent working set, about 450 KB (~4% of today):

- `NEXT_SESSION_PROMPT.md`
- the latest session handoff (older handoffs live in the repo, as they already do — the area holds
  only 147 today)
- `OPEN_ITEMS_BACKLOG.md`
- `DECISION_INDEX.md`
- `index.html`
- `pipeline_manifest.json` — the trust anchor (extended, section 3)
- `baseline.sh` (grows the fetch-and-verify open, section 3) and the instructions-support doc
- `SOURCE_REPO_TOKEN.txt` — the read-only token for the private sources repo (section 5). Persistent
  so no per-session paste is needed; hard-guarded out of the public repo by the custody check.

These are the files every session must read before it can do anything, plus the anchor that lets it
trust everything it fetches. Everything else arrives in the workspace at open.

## 3. The session open, redesigned

Today's open assumes every file is local. The new open assembles the workspace, verifies it, then
gates it:

1. **Read** the prompt and latest handoff from the area, verify area-file hashes against the handoff
   (unchanged from today).
2. **Fetch** the whole repo as one tarball (`codeload.github.com/.../tar.gz/main` — tested this
   session: one request, 1.07 MB, all 102 files) and unpack into the workspace.
3. **Verify** every fetched file against `pipeline_manifest.json`, which M0 extends from its current
   41 pipeline outputs to every repo-resident file a session consumes. The area-resident manifest is
   the anchor; a fetched tree that doesn't match it is a blocking finding, exactly like a bad hash
   today. No commit SHAs needed — the manifest-in-the-area *is* the pin.
4. **Overlay** the dual-resident working set (the section-2 area list) — the area copy wins.
   Authority rule for any area/repo mismatch on those files: if the area copy matches the handoff
   hash and the repo copy doesn't, the repo is simply a batch behind (note it, proceed); if the
   *area* copy fails the handoff hash, that is the bad-sync alarm regardless of what the repo says.
   Same semantics as today, extended.
5. **Fetch sources** on data turns: read `SOURCE_REPO_TOKEN.txt` from the area, fetch the private
   sources repo as a tarball with the token in the auth header, unpack into the workspace, and verify
   every file against `source_manifest.json` (section 5). If the token is absent or the fetch fails,
   fall back to the attached `gw_sources.zip`; if neither is present, tier-B gates skip and a data
   turn refuses to start (section 4).
6. **Run the gates**, tiered (section 4).

**Fallback when GitHub is unreachable:** the session is blocked from most work — accepted, because
if GitHub is down the deployed app is down too. Escape hatch: Ryan attaches any needed file directly;
the manifest verifies it identically, so the trust story doesn't change.

**Close protocol changes:** the handoff's Files section works as today (per-changed-file hashes) plus
one new line — the hash of the updated `pipeline_manifest.json`. Ryan's per-session upload burden
*drops*: after a data turn he pushes to git (which he already does) and re-uploads only the small
working-set files that changed, not multi-MB JSONs. One removal: the handoff stops hashing
`NEXT_SESSION_PROMPT.md`. It is consumed once, overwritten, git-historied, and — as this session's
open showed — legitimately edited after the handoff is finalized, so its hash can only ever match by
luck or false-alarm. (Finding from this open: the prompt's hash didn't match S147's handoff; all ten
substantive files did. Not a bad sync — the prompt post-dates the handoff, it documents the log
removal and drops the archive-split idea the handoff still recommends.)

## 4. Gates, tiered — where the fixed-point discipline moves

Three of today's gates rebuild outputs from GW sources and byte-compare (`repro_check`,
`units_repro_check`, `detachments_repro`), and rules_assertions both embeds one of those rebuilds and
reads a dozen-plus source files for its source-first assertions. Once sources leave the area, those
can't run at every open. The split:

- **Tier A — every session open, no sources needed:** area-hash check, fetch-verify against the
  manifest, all eighteen JS harnesses, `bundle_check`, `pipeline_manifest`, the repo custody check,
  and rules_assertions in a new `--tier a` mode (the source-reading assertions and the embedded
  rebuild are tagged out; everything against built data and `index.html` still runs).
- **Tier B — whenever sources are loaded, and mandatorily at every data turn's open *and* close:**
  the three full repro rebuilds and the source-first assertion set.

Two rules make this safe rather than a quiet weakening:

**Skips are loud and counted.** `baseline.sh` detects whether the source set is present. Absent, every
tier-B gate prints a visible `SKIP (tier B — sources not loaded)` line and the summary reads like
"OK 20/20 tier-A gates pass, 4 tier-B skipped." A skip is never silence, and never an exit-zero-and-
forget — a data turn with sources absent refuses to start.

**The fixed point is pinned continuously and recomputed at every point it could move.** Between data
turns, nothing legitimate can change an output; illegitimate change (hand-edit, bad sync) trips the
manifest at the very next open — same-day detection, same as today. The byte-identical rebuild still
runs at every moment an output actually changes. What moves: detection of a silently corrupted
*source* file shifts from "next repro run" to "next time sources are loaded" — which is the first
moment it could matter, and `source_manifest.json` (below) closes even that gap by hash-pinning the
sources themselves. Net: no protection is lost; one detection latency moves to exactly the point of
use.

A recovered gate, for free: `repo_check.py` has been absent from the area since before S147 (every
recent baseline ran `--no-repo`) — but it turns out to live in the repo. The fetch-open brings it
into every workspace, and custody checking comes back as a standing tier-A gate, run against the
fetched tree.

## 5. GW-source custody — the crux

The sources can never touch the *public* repo, so they can't use the public repo's fetch pattern.
**Decision (this session): they live in a second, private GitHub repo** — GW-derived text stays off
any public server, sources sync by `git push` like everything else, and a session fetches them into
the workspace on data turns. No zip to build and maintain, no per-file area uploads. Flat, original
filenames in the repo root — parsers' and repro checks' `REQUIRED` lists keep working with zero path
changes.

This is a deliberate accept-some-risk posture for the pre-release window (Ryan's call, recorded):
GW points and rules text are copyrighted regardless of being published, so a private repo under
Ryan's account is a real, if small, exposure. It is judged acceptable while the tool is
personal-use-only and non-commercial. **When the tool opens to other people, this decision is
revisited** — that is the trigger to reconsider whether sources stay in a private repo, move fully
local, or the custody question changes shape entirely. Noted here so a future session treats the
public-launch moment as a custody checkpoint, not a silent continuation.

**The token — how a private fetch authenticates.** A private repo only answers requests that prove
they're allowed; the proof is a GitHub personal access token. It is *not* an in-conversation approval
or a login prompt — GitHub has no knowledge of the session. Ryan creates the token once on GitHub's
site and it lives in the project area as `SOURCE_REPO_TOKEN.txt`. The open reads it and puts it in the
fetch's auth header; it is never committed, never written to any output, never carried into a handoff.

- **Creating it (once, on the record for future sessions):** GitHub → Settings → Developer settings →
  Personal access tokens → Fine-grained tokens → Generate new token. Name it; set an expiry (a year is
  fine); Repository access → Only select repositories → the private sources repo alone; Permissions →
  Contents → **Read-only**. Generate, copy the `github_pat_…` string, paste it into
  `SOURCE_REPO_TOKEN.txt` in the project area. Read-only-single-repo scoping is the safety property:
  the worst case if the string ever leaked is that someone could read GW points files they could
  mostly get from Wahapedia anyway, and Ryan can revoke and reissue in seconds from GitHub settings.
- **Why the area, not a per-session paste:** Ryan's call, and sound for this threat model. The real
  risk isn't an attacker (GW will not be hunting a token) — it's the one accident that the area syncs
  to the *public* repo, so a token file could ride along into a public commit. That is defused by a
  **hard custody gate, not a prose reminder** (below). With that gate in place, the area token gives
  zero-friction data turns and never needs re-pasting until it expires.
- **The hard guard.** `repo_check.py` (recovered as a standing gate, section 4) gains an explicit
  fail-loud rule: if `SOURCE_REPO_TOKEN.txt` — or anything matching a token filename pattern — ever
  appears in a public-repo-bound file list, the custody gate fails the session. Same discipline as
  everything else here: the protection is executable, checked every open, not a note someone has to
  remember. A one-line `.gitignore` entry backs it up at the git layer.
- **Integrity as an executable check:** a new `source_manifest.json` — filename and hash for all 71
  sources — lives in the *public* repo (it's only hashes; nothing GW-derived in it). The open verifies
  every fetched source file against it. When GW publishes new points and Ryan pushes an updated source
  file, the same data turn that consumes it updates the manifest — a source change is always a
  visible, hashed, logged event, never a quiet drift. This converts "the sources are right" from trust
  into a gate, and it protects both the private-repo fetch and the zip fallback identically.

**The offline fallback — the zip.** `gw_sources.zip`, one flat archive of the same 71-file set, stays
defined as the no-credential, no-network-to-the-private-repo path: if the token is absent, the private
fetch fails, or Ryan simply prefers not to have a live credential in play for a given turn, he attaches
the zip and the open unpacks and verifies it against the identical `source_manifest.json`. Same D226
attach rhythm as data work already uses. It is the fallback, not the primary — but it means no single
point of failure gates data work, and it's the escape hatch if the token approach ever feels wrong.

Rejected outright: encrypting the sources into the *public* repo. Ciphertext of GW's text, publicly
hosted, is a legally murkier object than a private repo, for no gain. Also considered and dropped:
the earlier zip-as-primary design (S148 mid-session) — the private repo removes the per-turn attach
step for the same custody outcome, so the zip is demoted to fallback rather than the main path.

## 6. Migration order

**M0 — build the new open (tooling turn, nothing evicted).** Extend `pipeline_manifest.py` to full
public-repo coverage; add the fetch-unpack-verify-overlay stage to `baseline.sh`, including the
token-authed private-source fetch with zip fallback; tier-tag `rules_assertions.py` and the three
repro gates; create `source_manifest.json`; wire the fetched `repo_check.py` back in as a standing
gate **and add its `SOURCE_REPO_TOKEN.txt` fail-loud rule**; codify the close-protocol changes
(manifest-pin line, prompt dropped from the hash list). Exit test: old open and new open both fully
green in the same session — tier B green too, since sources are still in the area. Rollback: none
needed; nothing moved.

**M1 — evict the repo-resident set (Ryan, ~10 minutes, no session needed).** Delete from the area
everything that is in the repo except the section-2 working set: the built JSONs, parsers, pipeline
scripts, harnesses, fixtures, and cold docs. Pre-conditions: M0's exit test passed, and the repo is
hash-current (true today; re-verified at the moment of eviction). Verification: full file-list
screenshots before and after — a proposed amendment to the deletion rule, which was written for
one-off deletions and doesn't scale to a ~70-file batch — then the next session opens on the fetch
path and comes back green. Frees ~3.9 MB (33%). Rollback: re-upload from the repo.

**M2 — evict the GW sources.** Ryan does the one-time setup: create the private sources repo, push
the 71-file set (provided list from the M2 turn), create the read-only token and paste it into
`SOURCE_REPO_TOKEN.txt` in the area, and — as belt-and-braces — build `gw_sources.zip` once so the
fallback exists. `source_manifest.json` is committed to the public repo. Before any deletion: the next
data turn (CSM turn B) runs entirely from the token-fetched private copy *while the area copies still
exist*, outputs byte-compared as usual — a full dress rehearsal of the real fetch path with a trivial
rollback. Only after that turn banks clean does Ryan delete the 71 from the area (same screenshot
protocol). Frees ~7.3 MB (62%). Rollback: the area copies, or the zip, or re-fetch.

**M3 — steady state.** Area ≈ 450 KB and stays there regardless of faction count. Data-turn prompts
say "confirm the source token is in the area" instead of naming a file to attach. The old all-local
open path is retired.

**Sequencing against the live queue (my call as dev manager):** M0 next session, then M1 the same
day, then B68 (engine turn), then CSM turn B as the M2 dress rehearsal, M2 eviction, CSM turn C. One
added session total (M0); every migration step after it rides work already queued. Doing M0 before
the remaining CSM turns matters because the area is at capacity *now* — CSM turns B/C add ~140 KB,
and after M1 that growth lands in the repo where it belongs instead of against the ceiling.

## 7. Costs accepted, eyes open

- **Network dependence at open.** Every session needs one public-repo fetch; data turns add the
  private-repo fetch. Mitigated by the zip fallback for sources; and a GitHub outage already takes
  down the deployed app.
- **A live credential in the area.** `SOURCE_REPO_TOKEN.txt` is a real token sitting in the working
  set. Scoped read-only to one low-stakes repo, hard-guarded out of the public repo by the custody
  gate, revocable in seconds. The accepted risk is deliberate (section 5); the zip fallback is the
  no-credential path for anyone uneasy with it on a given turn.
- **A private repo holds GW-derived text.** The pre-release accept-risk posture (section 5), to be
  revisited at public launch. Not zero exposure — a conscious, time-boxed call.
- **Source-corruption detection latency** moves to point-of-use, closed by `source_manifest.json`.
- **Upkeep** — one private repo to push source updates to (which Ryan already does for the public
  repo), one token to reissue ~yearly, and the fallback zip to refresh when sources change. Lighter
  than today's per-file area uploads.
- **Two-place edits for the working set** — the dual-resident files can drift between area and repo
  intraday. Already true today; the open's authority rule (section 3) makes the drift visible and
  ordered instead of ambiguous.

## 8. Decisions — settled this session, and what's left

**Settled (S148, Ryan's calls — recorded here so M0 builds against them):**

1. **GW-source home:** a private GitHub repo, not the zip. Zip demoted to offline fallback.
2. **Accept-risk posture:** GW-derived text in a private repo is acceptable for the pre-release,
   non-commercial, personal-use window, to be revisited at public launch (the launch is a custody
   checkpoint, section 5).
3. **Token in the area:** the read-only token lives in `SOURCE_REPO_TOKEN.txt` in the project area
   (no per-session paste), made safe by a hard custody gate that fails the session if the token
   filename ever reaches the public repo.

**Still needs your yes before M0 is built:**

1. **The shape overall** (sections 2–4, 6–7): area as working set, public repo as the fetch-on-demand
   home for everything public, private repo for sources, tiered gates, the M0–M3 order. M0 is not
   built until this is a yes.
2. **Bulk-deletion verification amendment** (section 6, M1): full file-list screenshots before and
   after each eviction batch, in place of per-file cards, for migration steps only.

One product decision confirmed and folded in, needing nothing further: whole-project-single-repo vs.
app-public/sources-private — you chose app stays in the current public repo, sources go in a new
private one, revisit at public launch.
