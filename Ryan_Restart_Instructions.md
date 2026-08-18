# RYAN — RESTART INSTRUCTIONS

Written at Session 259, when the 40K army list builder was set aside.

This is the short personal note. The full orientation document is `PROJECT_COLD_STORAGE.md` in the
public repo — read that when you actually want to restart. This file exists to hold the two things
that are easy to lose and hard to reconstruct from memory.

---

## 1. The access token — the thing most likely to go missing

The private source repo `rd-prime-1357/rd-prime-1357-data-sources` holds every GW-derived source file
the data pipeline reads. It is reached with a read-only GitHub personal access token stored in a file
called `SOURCE_REPO_TOKEN.txt`.

**That file lives only in the project working area. It is deliberately never committed to either
repo.** If the project area is cleared, or the Claude subscription lapses, or enough time passes that
GitHub expires the token, it is gone.

This is recoverable but only if you remember what is needed. If the token is missing:

1. Sign in to GitHub as `rd-prime-1357`.
2. Settings → Developer settings → Personal access tokens → Fine-grained tokens → Generate new token.
3. Scope it to the `rd-prime-1357-data-sources` repository only, read-only contents access.
4. Save the token value into a plain text file named exactly `SOURCE_REPO_TOKEN.txt`, one line, no
   quotes or extra text.
5. Put that file in the same folder as `baseline.sh`.

**Do not paste the token value into this file, or into any file that goes to the public repo.**

You do not need the token to run the app. The deployed site works with no sources at all. You need it
only to regenerate the data files from source — which means only when adding a faction, adopting a new
Munitorum Field Manual, or proving the pipeline still reproduces the shipped data.

## 2. The five render checks — the outstanding work only you can do

Five UI checks were written and never run, because they need a human looking at the deployed app.
They take roughly twenty minutes in total. The full scripts are preserved in `NEXT_SESSION_PROMPT.md`
in the repo.

**Run S250's first.** It is the only case where the app changes a saved list without telling the
player: shrink an over-capped unit and it silently drops weapon picks, keeping the first two in the
option's listed order rather than the first two you clicked. If a warning banner appears at any point
during that check, that is a real defect and worth writing down.

The other four cover the enhancement picker's eligibility rules, the Marks of Chaos selector, and the
Tank Ace checkbox.

## 3. Restarting, in five steps

1. Clone `rd-prime-1357/40k-army-builder`.
2. Put `SOURCE_REPO_TOKEN.txt` next to `baseline.sh`.
3. Run `./baseline.sh --fetch --data-turn`. Expect 42 of 42. A single `repo_check` failure just means
   the working area is out of sync with the repo, which is normal after a gap.
4. Read `PROJECT_COLD_STORAGE.md`, then the last two or three session handoffs.
5. Decide which project you are restarting before picking any ticket — keeping twenty armies correct
   and current, or rebuilding rules-as-data so faction coverage becomes a data task. Section 7 of the
   cold-storage document lays out the difference. They are not the same job.

## 4. Where things are

- Public repo: `rd-prime-1357/40k-army-builder`. Holds the app, the data, the parsers, the gates, the
  documents and every session handoff. GitHub Pages serves `index.html` from it, currently v6.27, with
  no subscription or running service behind it.
- Private repo: `rd-prime-1357/rd-prime-1357-data-sources`. GW-derived source material only.
- The project working area inside Claude is a cache, never the record. Losing it costs nothing.
