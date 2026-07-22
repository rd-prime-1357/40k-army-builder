#!/usr/bin/env python3
"""
equipped_parser.py

Recovers per-model weapon attribution from a pasted Wahapedia composition file
and writes authoritative per-group default_weapons / default_wargear into
unit_loadouts.json, as an override over the flat-pool baseline.

Source of truth: the datasheet UNIT COMPOSITION "... is equipped with:" wording,
which the Wahapedia CSV export drops. Keyed to the curated roster (units.json);
datasheets not in the roster are dropped and orphan loadout entries pruned.

Ownership is resolved by datasheet TITLE (a roster-name line immediately followed
by the stat block, i.e. a lone 'M' line) so that roster names appearing inside
"can be attached to the following units" lists are ignored. Each composition
region is bounded to the block between UNIT COMPOSITION and the points line, so
a neighbouring datasheet's wargear-option text cannot leak in.
"""
import json, re, unicodedata, argparse, csv


def norm(s):
    s = unicodedata.normalize('NFKD', s).replace('\u2019', "'").replace('\u2018', "'")
    s = s.replace('\u2013', '-').replace('\u2014', '-')
    return re.sub(r'\s+', ' ', s).strip().lower()


def norm_name(s):
    return re.sub(r'[^a-z0-9 ]', '', norm(s)).strip()


def base(n):
    # strip weapon variant suffix, e.g. "plasma incinerator - standard" -> "plasma incinerator"
    return re.split(r'\s+-\s+', n)[0].strip()


def variants(tok):
    n = norm(tok)
    words = n.split()
    out = [n]
    if words:
        last = words[-1]
        out.append(' '.join(words[:-1] + [last + 's']))            # add plural
        if last.endswith('s'):
            out.append(' '.join(words[:-1] + [last[:-1]]))          # strip plural
    seen, uniq = set(), []
    for c in out:
        if c not in seen:
            seen.add(c); uniq.append(c)
    return uniq


DETERMINERS = re.compile(r'^\s*(the|an|a|every|each|all|one|two|three|1|2|3)\s+', re.I)
SINGLE = re.compile(r'^\s*(one|an|a|1)\s+', re.I)  # "One Company Veteran ..." = a single model
WILDCARD = re.compile(r'\b(this|every|all|each)\s+models?\b', re.I)
OTHER = re.compile(r'\b(every|all|each)\s+other\s+models?\b', re.I)
END_COMP = re.compile(r'^\s*(\d+\s+models?\b|keywords\b|faction\s+keywords\b|attached\s+units\b|leader\b)', re.I)
EQUIP = re.compile(r'\b(is|are)\s+equipped\s+with\b', re.I)


def strip_determiners(s):
    prev = None
    while prev != s:
        prev = s
        s = DETERMINERS.sub('', s).strip()
    return s


def group_key(g):
    # Normalize a group name for matching: drop the " - ROLE" suffix and any
    # trailing datasheet footnote marker (e.g. "Cenobyte Servitors*").
    gb = re.split(r'\s+-\s+', norm(g))[0].strip()
    return re.sub(r'[\*\u2020\u2021]+$', '', gb).strip()


def sing_forms(s):
    # Candidate singular/plural forms for tolerant group matching, incl. the
    # irregular -ves plural (wolves -> wolf/wolfe).
    out = {s}
    if s.endswith('ves'):
        out.add(s[:-3] + 'f'); out.add(s[:-3] + 'fe')
    if s.endswith('es'):
        out.add(s[:-2])
    if s.endswith('s'):
        out.add(s[:-1])
    return out


def _sing_word(w):
    # Singularize one word for the loose (per-word) fallback below. Deliberately
    # conservative: strip a single trailing "s" (rifles -> rifle), map -ves/-ies,
    # leave -ss words (e.g. "cutlass") alone. Applied to BOTH sides, so words that
    # aren't true plurals (e.g. "occulus" -> "occulu") still collapse identically.
    if w.endswith('ies') and len(w) > 3:
        return w[:-3] + 'y'
    if w.endswith('ves') and len(w) > 3:
        return w[:-3] + 'fe'
    if w.endswith('ss'):
        return w
    if w.endswith('s') and len(w) > 1:
        return w[:-1]
    return w


def loose_key(s):
    # Whole-phrase key with every word singularized, so a plural that sits
    # MID-phrase matches its singular ("... Intercessor with plasma incinerator"
    # vs group "... Intercessors with plasma incinerators"). sing_forms only
    # normalizes the trailing word, which binds base groups but misses variant
    # sub-groups (B17 true-1b).
    p = re.sub(r'\s+models?$', '', norm(strip_determiners(s))).strip()
    return ' '.join(_sing_word(w) for w in p.split())


def match_group(frag, gnames):
    p = norm(strip_determiners(frag))
    # "Each <group> model is equipped with" leaves a trailing "model(s)" on the
    # subject after the leading determiner is stripped; drop it so the subject
    # matches the group name (e.g. "victrix honour guard model" -> "...guard").
    p = re.sub(r'\s+models?$', '', p).strip()
    pf = sing_forms(p)
    for g in gnames:
        if sing_forms(group_key(g)) & pf:
            return g
    # Fallback: per-word-singularized whole-phrase equality, accepted only when
    # exactly one group matches (no ambiguity). Catches variant sub-groups whose
    # only difference from the subject is a mid-phrase plural.
    fk = loose_key(frag)
    hits = [g for g in gnames if loose_key(g) == fk]
    if len(hits) == 1:
        return hits[0]
    return None


def parse_equipped_line(line):
    m = re.search(r'(.*?)\b(?:is|are)\s+equipped\s+with\s*:?\s*(.*)$', line, re.I)
    if not m:
        return None
    subject = m.group(1).strip()
    rest = m.group(2).strip().rstrip('.')
    tokens = [t.strip() for t in re.split(r'[;,]', rest) if t.strip()]
    return subject, tokens


# ── Datasheets.csv loadout-column adapter (gap-fill source) ────────────────────
# The pasted *_web.txt composition dumps are incomplete (whole datasheets missing),
# so segment() leaves those units with the flat all-groups baseline. The
# Datasheets.csv `loadout` column carries the same "... is equipped with:" prose
# for every unit, in HTML. This adapter turns that prose into the same per-clause
# equipped lines segment() would have produced, so the existing partition machinery
# can consume it unchanged. Used only to fill gaps (web.txt takes precedence).
_TAG = re.compile(r'<[^>]+>')
_CLAUSE = re.compile(r'<b>\s*(.*?is\s+equipped\s+with:?)\s*</b>\s*(.*?)(?=<b>|$)', re.I | re.S)


def _detag(t):
    return re.sub(r'\s+', ' ', _TAG.sub(' ', t or '')).strip()


def loadout_lines_from_datasheets(path):
    """uid -> [equipped-line string]. Each <b>Subject is equipped with:</b> weapons
    clause becomes one 'Subject is equipped with: weapons' line for parse_equipped_line."""
    out = {}
    for r in csv.reader(open(path), delimiter='|'):
        if len(r) < 7:
            continue
        uid, prose = r[0], r[6]
        lines = []
        for m in _CLAUSE.finditer(prose or ''):
            subj = _detag(m.group(1))
            weps = _detag(m.group(2)).rstrip('.')
            if subj and weps:
                lines.append(f'{subj} {weps}')
        if lines:
            out[uid] = lines
    return out


def load_roster(units_path):
    data = json.load(open(units_path))
    name2id, exact_by_id, base_by_id, roster_ids = {}, {}, {}, set()
    g_exact, g_base = {}, {}
    for blk in data:
        for u in blk['units']:
            uid = u['unit_id']
            roster_ids.add(uid)
            name2id[norm_name(u['unit_name'])] = uid
            ex, ba = {}, {}
            for w in u.get('weapons', []):
                nm = w['weapon_name']; n = norm(nm)
                ex[n] = nm
                ba.setdefault(base(n), [])
                if nm not in ba[base(n)]:
                    ba[base(n)].append(nm)
                g_exact.setdefault(n, nm)
                g_base.setdefault(base(n), [])
                if nm not in g_base[base(n)]:
                    g_base[base(n)].append(nm)
            exact_by_id[uid] = ex; base_by_id[uid] = ba
    return name2id, exact_by_id, base_by_id, roster_ids, g_exact, g_base


def resolve(tok, ex, ba, g_ex, g_ba):
    for cand in variants(tok):
        if cand in ex:
            return [ex[cand]]
        if base(cand) in ba:
            return ba[base(cand)]
    for cand in variants(tok):
        if cand in g_ex:
            return [g_ex[cand]]
        if base(cand) in g_ba:
            return g_ba[base(cand)]
    return []


def find_titles(lines, name2id):
    """Return list of (index, uid) for every datasheet title block in the file:
    a name line whose next non-blank line (past an optional base-size '(⌀..)' line)
    is the stat header 'M'. uid is the roster id, or None for a datasheet that is
    not on the roster (Legends/Forge World entries). Off-roster blocks must still
    be listed: they own their own UNIT COMPOSITION anchors, and if they are invisible
    the anchor is attributed to the previous roster unit and its equipped line bleeds
    into that unit's defaults (B27 — the Whirlwind picked up the Astraeus and the
    Thunderhawk this way)."""
    titles = []
    for i, ln in enumerate(lines):
        if not ln.strip() or '\u2300' in ln:   # blank, or the base-size "(⌀..)" line
            continue
        j = i + 1
        while j < len(lines) and not lines[j].strip():
            j += 1
        if j < len(lines) and '\u2300' in lines[j]:      # skip one base-size "(⌀..)" line
            j += 1
            while j < len(lines) and not lines[j].strip():
                j += 1
        if j < len(lines) and lines[j].strip().upper() == 'M':   # must reach stat header
            titles.append((i, name2id.get(norm_name(ln))))
    return titles


def segment(text, name2id):
    lines = text.splitlines()
    titles = find_titles(lines, name2id)
    anchors = [i for i, ln in enumerate(lines) if re.match(r'\s*unit\s+composition\s*$', ln, re.I)]
    owner_seen, dropped = {}, 0
    for a in anchors:
        # owner = nearest preceding title
        uid = None
        for idx, tuid in titles:
            if idx < a:
                uid = tuid          # may be None: an off-roster datasheet owns this anchor
            else:
                break
        # bounded region: anchor -> first composition-end line
        end = len(lines)
        for k in range(a + 1, len(lines)):
            if END_COMP.match(lines[k]):
                end = k; break
        elines = [lines[k].strip() for k in range(a, end) if EQUIP.search(lines[k])]
        if uid:
            owner_seen.setdefault(uid, []).extend(elines)
        else:
            dropped += len(elines)
    return owner_seen, dropped


# ── weapon-family normalisation (B24) ─────────────────────────────────────────
# A multi-profile weapon is stored in units.json as one row per profile
# ("Plasma pistol – standard" / "– supercharge"). The app treats the FAMILY, not
# the profile, as the unit of selection, replacement and display: every consumer
# of the loadout rollup looks weapons up by base name. So every weapon name held
# in unit_loadouts.json — default_weapons, default_weapon_counts keys, and the
# option replaces/replacement/choices fields — must be the base name. A profile
# suffix left in place makes a swap consume only one profile of the weapon it
# replaces (the sibling profile stays on the model) and makes the weapon vanish
# from the unit's weapon table. This runs over the whole file on every pass, so
# the invariant holds regardless of when an entry was parsed.
_PROFILE_SUFFIX = re.compile(r'\s+[\u2013\u2014-]\s+\S.*$')

def strip_profile(name):
    return _PROFILE_SUFFIX.sub('', (name or '')).strip()

def _fold_compound(name):
    """Base-name each part of a compound ('A – x + B – y' -> 'A + B')."""
    if not isinstance(name, str):
        return name
    return ' + '.join(strip_profile(p) for p in name.split(' + ') if p.strip())

def _dedupe(seq):
    out, seen = [], set()
    for x in seq:
        if x not in seen:
            seen.add(x); out.append(x)
    return out

# B18c — fan a capped generic per-N weapon swap onto every model group that
# actually carries the source weapon, sharing one unit-wide pool_id so the cap
# is drawn across the whole unit (D116: a generic "1 model" phrase reaches every
# carrying group, including a leader/sergeant group).
#
# This runs on the final --datasheets pass only, after per-group default_weapons
# are authoritative, so "which groups carry the weapon" is answerable.
#
# Scope is an EXPLICIT unit allowlist, not a structural gate. S63 found the
# structural gate ("uncontested + 2+ carriers") is unsafe: it matches 8 units,
# and two of them (Terminators 000001183 / 000004138) carry a per-model
# restriction — "* this model's storm bolter cannot be replaced" — that lives in
# a datasheet footnote, not in the option structure, so a structural fan would
# hand those sergeants an ILLEGAL swap. Until that per-model-restriction signal
# is parsed and applied, only hand-verified units are fanned. Add a unit id here
# only after confirming it has no such footnote and no same-slot contest.
_FAN_UNIT_ALLOWLIST = {'000000241', '000002748'}

def _wbase(name):
    return strip_profile(name).strip().lower()

def _slug(s):
    return re.sub(r'_+', '_', re.sub(r'[^a-z0-9]+', '_', str(s).lower())).strip('_')

def fan_pooled_swaps(ld):
    for uid in _FAN_UNIT_ALLOWLIST:
        entry = ld.get(uid)
        if not isinstance(entry, dict):
            continue
        groups = entry.get('model_groups', [])
        opts = entry.get('options', [])
        # weapons replaced by ANY option — used to skip same-slot contests.
        contest = {}
        for o in opts:
            r = o.get('replaces')
            if r:
                contest[_wbase(r)] = contest.get(_wbase(r), 0) + 1
        new_opts = []
        for o in opts:
            new_opts.append(o)
            if o.get('type') != 'count' or not o.get('per_n_models'):
                continue
            w = o.get('replaces')
            if not w or contest.get(_wbase(w), 0) > 1:
                continue  # contested slot — do not fan
            carriers = [g['name'] for g in groups
                        if any(_wbase(dw) == _wbase(w) for dw in g.get('default_weapons', []))]
            if len(carriers) < 2:
                continue  # single carrier already correct
            pool = _slug(strip_profile(w))
            o['pool_id'] = pool  # original keeps its id; gains the shared pool
            have = {o.get('scope')}
            existing_ids = {x.get('id') for x in opts}
            for gname in carriers:
                if gname in have:
                    continue
                cid = o['id'] + '__' + _slug(gname)
                if cid in existing_ids:
                    continue
                copy = {k: v for k, v in o.items()}
                copy['id'] = cid
                copy['scope'] = gname
                copy['pool_id'] = pool
                new_opts.append(copy)
                have.add(gname)
        entry['options'] = new_opts

def normalise_profiles(ld):
    for uid, entry in ld.items():
        if not isinstance(entry, dict):
            continue
        for g in entry.get('model_groups', []):
            if isinstance(g.get('default_weapons'), list):
                g['default_weapons'] = _dedupe(strip_profile(w) for w in g['default_weapons'])
            dwc = g.get('default_weapon_counts')
            if isinstance(dwc, dict):
                folded = {}
                for k, v in dwc.items():
                    b = strip_profile(k)
                    folded[b] = max(folded.get(b, 0), v)   # profiles of one weapon share a count
                g['default_weapon_counts'] = folded
            if isinstance(g.get('default_wargear'), list):
                g['default_wargear'] = _dedupe(strip_profile(w) for w in g['default_wargear'])
        for opt in entry.get('options', []):
            for f in ('replaces', 'replacement', 'adds_weapon', 'requires_weapon'):
                if isinstance(opt.get(f), str):
                    opt[f] = _fold_compound(opt[f])
            for f in ('choices', 'replacement_choices'):
                if isinstance(opt.get(f), list):
                    opt[f] = [_fold_compound(c) for c in opt[f]]


def load_wargear_allowlist(path):
    """Canonical wargear item names (weapon_abilities.json) -> normalised set."""
    try:
        rows = json.load(open(path))
    except Exception:
        return set()
    out = set()
    for r in rows:
        nm = r.get('weapon_ability_name') if isinstance(r, dict) else None
        if nm:
            out.add(norm_name(re.sub(r'\s*\([^)]*\)\s*$', '', nm)))
    return out


def _names_wargear(elines, ex, ba, g_ex, g_ba, allow):
    """True when a datasheet loadout clause names an item that is not a weapon but is
    a known wargear item."""
    if not allow:
        return False
    for ln in elines:
        parsed = parse_equipped_line(ln)
        if not parsed:
            continue
        for tok in parsed[1]:
            core = re.sub(r'^\d+\s+', '', tok).strip()
            if resolve(core, ex, ba, g_ex, g_ba):
                continue
            if norm_name(core) in allow:
                return True
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--composition', required=True)
    ap.add_argument('--units', required=True)
    ap.add_argument('--loadouts', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--report', required=True)
    ap.add_argument('--no-prune', action='store_true')
    ap.add_argument('--wargear-allowlist', default='weapon_abilities.json')
    ap.add_argument('--datasheets', default=None,
                    help='Datasheets.csv; gap-fills the loadout partition for multi-group '
                         'units the web.txt composition dump misses (web.txt takes precedence).')
    args = ap.parse_args()

    name2id, ex_by_id, ba_by_id, roster_ids, g_ex, g_ba = load_roster(args.units)
    ld = json.load(open(args.loadouts))
    text = open(args.composition, encoding='utf-8').read()
    owner_lines, dropped_lines = segment(text, name2id)

    # Gap-fill from Datasheets.csv loadout prose. Only multi-group units the web.txt
    # dump didn't cover: single-group units are already correct (flat == the one group),
    # and web.txt-covered units are left untouched so nothing regresses.
    allow = load_wargear_allowlist(args.wargear_allowlist)
    ds_filled = []
    if args.datasheets:
        ds_lines = loadout_lines_from_datasheets(args.datasheets)
        for uid, elines in ds_lines.items():
            if uid in owner_lines:
                continue
            entry = ld.get(uid)
            if not isinstance(entry, dict):
                continue
            if entry.get('_defaults_source') == 'equipped':
                continue  # already partitioned by a web.txt pass — don't re-touch
            if len(entry.get('model_groups', [])) < 2 and not _names_wargear(
                    elines, ex_by_id.get(uid, {}), ba_by_id.get(uid, {}), g_ex, g_ba, allow):
                # Single-group units are already correct on the weapon side (flat == the
                # one group). Admit one only when its loadout prose names a real wargear
                # ITEM (allowlist) that no weapon lookup can resolve — otherwise the group
                # would carry no gear and a gear-sourced swap could never fire (B28b).
                continue
            owner_lines[uid] = elines
            ds_filled.append(uid)

    updated, group_sets = 0, 0
    wargear_routed, unmatched_groups, multi_count = [], [], []

    for uid, elines in owner_lines.items():
        if uid not in ld or not isinstance(ld[uid], dict):
            continue
        groups = ld[uid].get('model_groups', [])
        gnames = [g.get('name', '') for g in groups]
        acc = {g.get('name'): {'w': [], 'g': [], 'c': {}} for g in groups}
        ex, ba = ex_by_id.get(uid, {}), ba_by_id.get(uid, {})
        # Pre-pass: classify each line and collect explicitly-named groups, so an
        # "every other model" line can target the complement (all groups not named
        # by a specific line, e.g. Ravenwing Command: Champion named -> other =
        # Apothecary + Ancient).
        plines, named, singleflags = [], set(), []
        for ln in elines:
            parsed = parse_equipped_line(ln)
            if not parsed:
                continue
            subject, tokens = parsed
            if OTHER.search(subject):
                plines.append(('other', None, tokens)); singleflags.append(False)
            elif WILDCARD.search(subject):
                plines.append(('all', gnames, tokens)); singleflags.append(False)
            else:
                tg = []
                for frag in re.split(r'\band\b', subject, flags=re.I):
                    frag = frag.strip()
                    if not frag:
                        continue
                    g = match_group(frag, gnames)
                    if g:
                        tg.append(g); named.add(g)
                    else:
                        unmatched_groups.append((uid, frag))
                plines.append(('specific', tg, tokens))
                singleflags.append(bool(SINGLE.match(subject)) and len(tg) == 1)

        # Heterogeneous fixed-group split (B9). A group of N identical models
        # breaks when the composition gives DIFFERENT weapons to individual models
        # via repeated singular lines ("One Company Veteran ... heavy bolter" /
        # "One ... bolt rifle"). Kept as one group, the rollup multiplies every
        # listed weapon by N, doubling the per-model weapons. When a fixed-N group
        # gets exactly N such singular lines and carries no scoped options, split
        # it into N one-model sub-groups, each with its own weapons, named by its
        # distinguishing weapon. Guarded to fire only on that exact shape.
        opt_scopes = {o.get('scope') for o in ld[uid].get('options', [])}

        def _fixedN(c):
            return c.get('fixed') if isinstance(c, dict) and isinstance(c.get('fixed'), int) else None

        single_idx = {}
        for i, (kind, tgt, toks) in enumerate(plines):
            if kind == 'specific' and singleflags[i] and len(tgt) == 1:
                single_idx.setdefault(tgt[0], []).append(i)
        for gname, idxs in single_idx.items():
            gc = next((g.get('count', {}) for g in groups if g['name'] == gname), {})
            n = _fixedN(gc)
            if not n or n < 2 or len(idxs) != n or gname in opt_scopes:
                continue
            # resolve each singular line's weapons; find its distinguishing weapon
            resolved = []
            for i in idxs:
                names = []
                for tok in plines[i][2]:
                    mnum = re.match(r'^(\d+)\s+(.*\S)$', tok)
                    core = mnum.group(2) if mnum else tok
                    names.append((core, resolve(core, ex, ba, g_ex, g_ba),
                                  int(mnum.group(1)) if mnum else 1))
                resolved.append(names)
            common = None
            for names in resolved:
                s = {w for _, ws, _ in names for w in ws}
                common = s if common is None else (common & s)
            gidx = next(k for k, g in enumerate(groups) if g['name'] == gname)
            template = groups[gidx]
            base_name = re.split(r'\s+-\s+', gname)[0].strip()
            base_name = re.sub(r'[\*\u2020\u2021]+$', '', base_name).strip()
            singular = base_name[:-1] if base_name.endswith('s') and not base_name.endswith('ss') else base_name
            subgroups = []
            for j, i in enumerate(idxs):
                distinguishing = next((w for _, ws, _ in resolved[j] for w in ws if w not in common), None)
                label = f"{singular} ({distinguishing})" if distinguishing else f"{singular} {j + 1}"
                ng = dict(template)
                ng['name'] = label
                ng['count'] = {'fixed': 1}
                ng.pop('default_weapons', None); ng.pop('default_weapon_counts', None); ng.pop('default_wargear', None)
                w, gw, c = [], [], {}
                for core, ws, cnt in resolved[j]:
                    if ws:
                        for nm2 in ws:
                            if nm2 not in w:
                                w.append(nm2)
                            if cnt > 1:
                                c[nm2] = cnt
                    elif core not in gw:
                        gw.append(core); wargear_routed.append((uid, core))
                if w:
                    ng['default_weapons'] = w
                if gw:
                    ng['default_wargear'] = gw
                if c:
                    ng['default_weapon_counts'] = c
                subgroups.append(ng)
            groups[gidx:gidx + 1] = subgroups
            gnames = [g['name'] for g in groups]
            acc = {g['name']: acc.get(g['name'], {'w': [], 'g': [], 'c': {}}) for g in groups}
            # drop the singular lines for this group so the normal pass skips them
            plines = [pl for k, pl in enumerate(plines) if k not in idxs]
            singleflags = [singleflags[k] for k in range(len(singleflags)) if k not in idxs]
            group_sets += len(subgroups)

        touched = False
        for kind, tg, tokens in plines:
            targets = [g for g in gnames if g not in named] if kind == 'other' else tg
            if not targets:
                continue
            for tok in tokens:
                cnt, core = 1, tok
                mnum = re.match(r'^(\d+)\s+(.*\S)$', tok)
                if mnum:
                    cnt, core = int(mnum.group(1)), mnum.group(2)
                names = resolve(core, ex, ba, g_ex, g_ba)
                if cnt > 1 and names:
                    multi_count.append((uid, core, cnt))
                for g in targets:
                    if names:
                        for nm in names:
                            if nm not in acc[g]['w']:
                                acc[g]['w'].append(nm)
                            if cnt > 1:
                                acc[g]['c'][nm] = cnt
                    else:
                        if core not in acc[g]['g']:
                            acc[g]['g'].append(core)
                if not names:
                    wargear_routed.append((uid, core))
            touched = True
        if not touched:
            continue
        for g in groups:
            nm = g.get('name')
            if acc.get(nm) and (acc[nm]['w'] or acc[nm]['g']):
                g['default_weapons'] = acc[nm]['w']
                g.pop('default_wargear', None); g.pop('default_weapon_counts', None)
                if acc[nm]['g']:
                    g['default_wargear'] = acc[nm]['g']
                if acc[nm]['c']:
                    g['default_weapon_counts'] = acc[nm]['c']
                group_sets += 1
        ld[uid]['_defaults_source'] = 'equipped'
        updated += 1

    pruned = []
    if not args.no_prune:
        for k in [k for k, v in ld.items() if isinstance(v, dict) and k not in roster_ids]:
            pruned.append(k); del ld[k]

    normalise_profiles(ld)

    if args.datasheets:
        fan_pooled_swaps(ld)

    json.dump(ld, open(args.out, 'w'), indent=2, ensure_ascii=False)

    with open(args.report, 'w') as f:
        f.write('# Equipped-With Parser Report\n\n')
        f.write(f'Units updated with per-group defaults: {updated}\n')
        f.write(f'Model-group default sets written: {group_sets}\n')
        f.write(f'Orphan loadout entries pruned: {len(pruned)}\n')
        f.write(f'Multi-group units gap-filled from Datasheets.csv: {len(ds_filled)}\n')
        f.write(f'Equipped-with lines on dropped (non-roster) datasheets: {dropped_lines}\n\n')
        if ds_filled:
            f.write('## Gap-filled from Datasheets.csv loadout prose\n')
            for uid in sorted(ds_filled):
                f.write(f'- {uid}\n')
            f.write('\n')
        if wargear_routed:
            f.write('## Tokens routed to default_wargear (verify: real wargear vs missing weapon)\n')
            for uid, tok in sorted(set(wargear_routed)):
                f.write(f'- {uid}: {tok}\n')
            f.write('\n')
        if multi_count:
            f.write('## Weapons with quantity >1 (count not yet represented in name-list schema)\n')
            for uid, nm, cnt in sorted(set(multi_count)):
                f.write(f'- {uid}: {nm} x{cnt}\n')
            f.write('\n')
        if unmatched_groups:
            f.write('## Subject fragments that did not map to a model group\n')
            for uid, frag in unmatched_groups:
                f.write(f'- {uid}: {frag!r}\n')
            f.write('\n')

    print(f'updated={updated} group_sets={group_sets} pruned={len(pruned)} '
          f'ds_filled={len(ds_filled)} '
          f'wargear_routed={len(set(wargear_routed))} unmatched_groups={len(unmatched_groups)} '
          f'dropped_lines={dropped_lines}')


if __name__ == '__main__':
    main()
