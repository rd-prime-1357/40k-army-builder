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
import json, re, unicodedata, argparse


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
WILDCARD = re.compile(r'\b(this|every|all|each)\s+models?\b', re.I)
END_COMP = re.compile(r'^\s*(\d+\s+models?\b|keywords\b|faction\s+keywords\b|attached\s+units\b|leader\b)', re.I)
EQUIP = re.compile(r'\b(is|are)\s+equipped\s+with\b', re.I)


def strip_determiners(s):
    prev = None
    while prev != s:
        prev = s
        s = DETERMINERS.sub('', s).strip()
    return s


def match_group(frag, gnames):
    p = norm(strip_determiners(frag))
    for g in gnames:
        if norm(g) == p:
            return g
    for g in gnames:
        if norm(g).rstrip('s') == p.rstrip('s'):
            return g
    return None


def parse_equipped_line(line):
    m = re.search(r'(.*?)\b(?:is|are)\s+equipped\s+with\s*:?\s*(.*)$', line, re.I)
    if not m:
        return None
    subject = m.group(1).strip()
    rest = m.group(2).strip().rstrip('.')
    tokens = [t.strip() for t in re.split(r'[;,]', rest) if t.strip()]
    return subject, tokens


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
    """Return list of (index, uid) for lines that are datasheet titles:
    a roster-name line whose next non-blank line is the stat header 'M'."""
    titles = []
    for i, ln in enumerate(lines):
        key = norm_name(ln)
        if key not in name2id:
            continue
        j = i + 1
        while j < len(lines) and not lines[j].strip():
            j += 1
        if j < len(lines) and '\u2300' in lines[j]:      # skip one base-size "(⌀..)" line
            j += 1
            while j < len(lines) and not lines[j].strip():
                j += 1
        if j < len(lines) and lines[j].strip().upper() == 'M':   # must reach stat header
            titles.append((i, name2id[key]))
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
                uid = tuid
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--composition', required=True)
    ap.add_argument('--units', required=True)
    ap.add_argument('--loadouts', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--report', required=True)
    ap.add_argument('--no-prune', action='store_true')
    args = ap.parse_args()

    name2id, ex_by_id, ba_by_id, roster_ids, g_ex, g_ba = load_roster(args.units)
    ld = json.load(open(args.loadouts))
    text = open(args.composition, encoding='utf-8').read()
    owner_lines, dropped_lines = segment(text, name2id)

    updated, group_sets = 0, 0
    wargear_routed, unmatched_groups, multi_count = [], [], []

    for uid, elines in owner_lines.items():
        if uid not in ld or not isinstance(ld[uid], dict):
            continue
        groups = ld[uid].get('model_groups', [])
        gnames = [g.get('name', '') for g in groups]
        acc = {g.get('name'): {'w': [], 'g': []} for g in groups}
        touched = False
        for ln in elines:
            parsed = parse_equipped_line(ln)
            if not parsed:
                continue
            subject, tokens = parsed
            if WILDCARD.search(subject):
                targets = gnames
            else:
                targets = []
                for frag in re.split(r'\band\b', subject, flags=re.I):
                    frag = frag.strip()
                    if not frag:
                        continue
                    g = match_group(frag, gnames)
                    (targets.append(g) if g else unmatched_groups.append((uid, frag)))
            if not targets:
                continue
            ex, ba = ex_by_id.get(uid, {}), ba_by_id.get(uid, {})
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
                if acc[nm]['g']:
                    g['default_wargear'] = acc[nm]['g']
                group_sets += 1
        ld[uid]['_defaults_source'] = 'equipped'
        updated += 1

    pruned = []
    if not args.no_prune:
        for k in [k for k, v in ld.items() if isinstance(v, dict) and k not in roster_ids]:
            pruned.append(k); del ld[k]

    json.dump(ld, open(args.out, 'w'), indent=2, ensure_ascii=False)

    with open(args.report, 'w') as f:
        f.write('# Equipped-With Parser Report\n\n')
        f.write(f'Units updated with per-group defaults: {updated}\n')
        f.write(f'Model-group default sets written: {group_sets}\n')
        f.write(f'Orphan loadout entries pruned: {len(pruned)}\n')
        f.write(f'Equipped-with lines on dropped (non-roster) datasheets: {dropped_lines}\n\n')
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
          f'wargear_routed={len(set(wargear_routed))} unmatched_groups={len(unmatched_groups)} '
          f'dropped_lines={dropped_lines}')


if __name__ == '__main__':
    main()
