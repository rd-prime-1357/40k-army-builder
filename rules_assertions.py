#!/usr/bin/env python3
"""
rules_assertions.py — executable rules facts.

Prose drifts. A handoff can carry a false claim for a dozen sessions and nothing
will stop it. An assertion cannot: it runs, and it passes or it fails.

Every rules or design fact that a session is allowed to ACT on must be either
(a) re-derived from source this session, or (b) asserted here. Nothing gets to be
true just because a previous handoff said so.

Run at session start, alongside the baseline check:

    python3 rules_assertions.py --dir .

Exit code 0 = all pass. Non-zero = a stated fact is not true of the data. Stop
and find out which one is wrong, the assertion or the data.

Adding a fact: append to the ASSERTIONS list with the source it was derived from.
An assertion with no source is not a fact, it is a guess, and does not belong here.
"""

import argparse, csv, json, os, re, sys

# ── source loaders ────────────────────────────────────────────────────────────

def pipe_rows(path):
    """Wahapedia CSVs are pipe-delimited with a trailing empty field."""
    with open(path, encoding='utf-8-sig') as f:
        head = f.readline().rstrip('\r\n').split('|')
        for line in f:
            parts = line.rstrip('\r\n').split('|')
            if len(parts) < len(head):
                continue
            yield dict(zip(head, parts))

class Sources:
    def __init__(self, d):
        self.dir = d
        self._cache = {}

    def abilities(self):
        if 'ab' not in self._cache:
            self._cache['ab'] = list(pipe_rows(os.path.join(self.dir, 'Datasheets_abilities.csv')))
        return self._cache['ab']

    def models(self):
        if 'md' not in self._cache:
            self._cache['md'] = list(pipe_rows(os.path.join(self.dir, 'Datasheets_models.csv')))
        return self._cache['md']

    def datasheets(self):
        if 'ds' not in self._cache:
            self._cache['ds'] = {r['id']: r['name']
                                 for r in pipe_rows(os.path.join(self.dir, 'Datasheets.csv'))}
        return self._cache['ds']

    def wargear_points(self):
        if 'wp' not in self._cache:
            with open(os.path.join(self.dir, 'wargear_points.json'), encoding='utf-8') as f:
                self._cache['wp'] = json.load(f)
        return self._cache['wp']

    def mfm_instructions(self):
        if 'mi' not in self._cache:
            with open(os.path.join(self.dir, 'MFM_Instructions.txt'), encoding='utf-8-sig') as f:
                self._cache['mi'] = f.read()
        return self._cache['mi']

    def loadouts(self):
        if 'lo' not in self._cache:
            with open(os.path.join(self.dir, 'unit_loadouts.json'), encoding='utf-8') as f:
                self._cache['lo'] = json.load(f)
        return self._cache['lo']

    def wargear_ability(self, ds_id, name):
        """The ability text on ONE datasheet. This is the only legitimate lookup —
        never key on the ability name alone (D70)."""
        for r in self.abilities():
            if r['datasheet_id'] == ds_id and r['name'].lower() == name.lower():
                return r['description']
        return None

    def model_stat(self, ds_id, stat, group=None):
        for r in self.models():
            if r['datasheet_id'] != ds_id:
                continue
            if group and r['name'] != group:
                continue
            return r[stat]
        return None

# ── assertion helpers ─────────────────────────────────────────────────────────

def confers(S, ds_id, item, expect):
    """The named wargear on THIS datasheet confers exactly `expect`
    ('inv:4', 'W:6', ...). Derived from Datasheets_abilities.csv."""
    txt = S.wargear_ability(ds_id, item)
    if txt is None:
        return False, f'{item} not found on {ds_id}'
    got = read_characteristic(txt)
    ok = (got == expect)
    return ok, f'{S.datasheets().get(ds_id, ds_id)} / {item}: expected {expect}, data says {got or "nothing"} ({txt})'

def read_characteristic(txt):
    """The reader from D75, restated. An absolute SET, never a modifier."""
    t = txt or ''
    m = re.search(r'(\d)\+ invulnerable save', t, re.I)
    if m: return f'inv:{m.group(1)}'
    m = re.search(r'Wounds characteristic of (\d+)', t, re.I)
    if m: return f'W:{m.group(1)}'
    m = re.search(r'Save characteristic of (\d)\+', t, re.I)
    if m: return f'SV:{m.group(1)}'
    m = re.search(r'Feel No Pain (\d)\+', t, re.I)
    if m: return f'FNP:{m.group(1)}'
    return None

def printed_stat(S, ds_id, stat, expect, group=None):
    got = S.model_stat(ds_id, stat, group)
    return (str(got) == str(expect)), f'{S.datasheets().get(ds_id, ds_id)} printed {stat}: expected {expect}, data says {got}'

# ── the facts ─────────────────────────────────────────────────────────────────
# Each entry: (id, one-line statement, source, callable(S) -> (ok, detail))

ASSERTIONS = [

    # ── D70 / B15. The fact that was false in the handoff for a dozen sessions.
    # An identically-named wargear item confers DIFFERENT things on different
    # datasheets. Any lookup keyed on the item name alone is provably wrong.
    ('B15-1',
     'Storm Shield does not mean one thing. Across datasheets it confers at least '
     'three different effects, so no name-keyed lookup can be correct.',
     'Datasheets_abilities.csv',
     lambda S: (
         len({read_characteristic(r['description'])
              for r in S.abilities() if r['name'].lower() == 'storm shield'}) >= 3,
         'distinct Storm Shield effects: ' + ', '.join(sorted(
             str(x) for x in {read_characteristic(r['description'])
                              for r in S.abilities() if r['name'].lower() == 'storm shield'})))),

    ('B15-2',
     'Wolf Guard Battle Leader: storm shield sets Wounds to 6. It does NOT set 4. '
     'The claim that it regresses him W5 -> W4 blocked the invuln pass from S37 to S49 '
     'and was never true.',
     'Datasheets_abilities.csv 000004130 (confirmed against the printed card)',
     lambda S: confers(S, '000004130', 'Storm Shield', 'W:6')),

    ('B15-3',
     'Wolf Guard Battle Leader printed Wounds is 5, so the shield is +1 and never a regression.',
     'Datasheets_models.csv 000004130',
     lambda S: printed_stat(S, '000004130', 'W', '5')),

    ('B15-4',
     'Wolf Guard: storm shield confers a 4+ invulnerable save (no Wounds change). '
     'Same item name as the Battle Leader, different datasheet, different effect.',
     'Datasheets_abilities.csv 000000315 (confirmed against the printed card)',
     lambda S: confers(S, '000000315', 'Storm Shield', 'inv:4')),

    ('B15-4b',
     'Wolf Guard printed Wounds is 2 and it has no printed invulnerable save, so the shield '
     'is the only source of the 4+ — and only for the models that took one.',
     'Datasheets_models.csv 000000315 (confirmed against the printed card)',
     lambda S: printed_stat(S, '000000315', 'W', '2')),

    ('B15-5',
     'Terminator Assault Squad: storm shield sets Wounds to 4 (printed W3). This is where '
     'the "4" in the false B15 claim actually came from.',
     'Datasheets_abilities.csv 000000118',
     lambda S: confers(S, '000000118', 'Storm Shield', 'W:4')),

    ('B15-6',
     'Terminator Assault Squad printed Wounds is 3.',
     'Datasheets_models.csv 000000118',
     lambda S: printed_stat(S, '000000118', 'W', '3')),

    ('B15-7',
     'Ancient in Terminator Armour: the item is named Terminator Storm Shield and sets Wounds to 6. '
     'Item names are not stable across datasheets either.',
     'Datasheets_abilities.csv 000002677',
     lambda S: confers(S, '000002677', 'Terminator Storm Shield', 'W:6')),

    # ── D95. No weapon or item name anywhere carries a profile suffix.
    ('D95',
     'No weapon or item name in unit_loadouts.json carries a profile suffix.',
     'unit_loadouts.json',
     lambda S: d95(S)),

    # ── D103 / B32. The compound gate exists and is still compound.
    ('B32',
     "Captain with Jump Pack's relic shield is gated on BOTH the heavy bolt pistol and the "
     'Astartes chainsword. If this collapses to one weapon, a Captain could take a power fist '
     'AND a relic shield.',
     'unit_loadouts.json 000000083 add_4 (D103)',
     lambda S: compound_gate(S)),

    # ── D106 / B33. A negated gate is a PER-MODEL exclusion, not a unit-level one.
    # Each Plaguebearer sentence forbids ONE MODEL holding both items; neither forbids
    # the UNIT holding both. The body group has 9 (Plaguebearers) / 2-5 (Plague Drones)
    # models, so the two adds can never be forced onto the same model and no exclusion
    # pool is needed. A pooled mutual exclusion here would make a legal list unbuildable.
    ('B33-1',
     'Plaguebearers and Plague Drones each offer BOTH a daemonic icon and an instrument '
     'of Chaos, as two independent single-model adds. Neither carries a gate or a pool.',
     'Datasheets_options.csv 000004113 / 000004114; unit_loadouts.json',
     lambda S: (
         all(sorted(o.get('equipment') for o in S.loadouts()[u]['options'])
                 == ['Daemonic Icon', 'Instrument of Chaos']
             and all(o['type'] == 'add' and o.get('max_total') == 1
                     and not o.get('requires_weapon') and not o.get('pool_id')
                     for o in S.loadouts()[u]['options'])
             for u in ('000004113', '000004114')),
         'icon/instrument on 000004113 + 000004114: two ungated, unpooled, capped adds each')),

    # ── D104 guard, still live: the classifiers must refuse a negated gate.
    ('B33-2',
     'No option carries a requires_weapon naming an icon or an instrument — the D104 '
     'inversion bug (reading "not equipped with X" as "requires X") stays dead.',
     'unit_loadouts.json',
     lambda S: (
         not [o for u in S.loadouts() if not u.startswith('_')
              for o in S.loadouts()[u].get('options', [])
              if 'icon' in str(o.get('requires_weapon', '')).lower()
              or 'instrument' in str(o.get('requires_weapon', '')).lower()],
         'no inverted icon/instrument gates')),

    # ── B32 + bearer gate: a compound gate names every weapon the bearer must hold.
    ('B33-3',
     'Captain with Jump Pack: the relic shield add is gated on BOTH the heavy bolt '
     'pistol and the Astartes chainsword, written as one compound gate.',
     'Datasheets_options.csv 000000083; unit_loadouts.json',
     lambda S: (
         any(o.get('requires_weapon') == 'Heavy bolt pistol + Astartes chainsword'
             for o in S.loadouts()['000000083']['options']),
         'compound gate present on 000000083')),

    # ── D107 / B35. Wargear is NOT free, and the pricing rule is stated in source.
    # These four exist because the previous claim ("every wargear option is free")
    # was read off our own derived data, which had simply thrown the costs away.
    ('B35-1',
     "The MFM's own instructions state the pricing rule: wargear costs are charged per "
     'item TAKEN and are applied ON TOP of the unit\'s main points cost. This is the whole '
     'basis of the engine\'s points sum, so it is asserted rather than remembered.',
     'MFM_Instructions.txt, UNITS > Wargear',
     lambda S: (
         'per item taken' in S.mfm_instructions().lower()
         and "on top of the unit's main points cost" in S.mfm_instructions().lower().replace('\u2019', "'"),
         'MFM_Instructions.txt states per-item-taken, on top of the unit cost')),

    ('B35-2',
     'A default-issue item IS a taken item, so the base cost does NOT already include it. '
     "Terminator Assault Squad's thunder hammer is priced at 5 and can only ever be swapped "
     'AWAY (it appears as a default weapon and as a swap source, never as an add or a '
     'replacement), so the 5 pts can only be pricing the default loadout.',
     'MFM_Space_Marines_v1_0.txt:373; unit_loadouts.json 000000118',
     lambda S: (
         '000000118' in S.wargear_points()
         and 'thunder hammer' in S.wargear_points()['000000118']['items']
         and all('Thunder hammer' in (g.get('default_weapons') or [])
                 for g in S.loadouts()['000000118']['model_groups'])
         and not any(o.get('adds_weapon') == 'Thunder hammer'
                     or o.get('replacement') == 'Thunder hammer'
                     or 'Thunder hammer' in (o.get('choices') or [])
                     or 'Thunder hammer' in (o.get('replacement_choices') or [])
                     for o in S.loadouts()['000000118']['options']),
         'TAS thunder hammer is priced and is default-only — it cannot be added')),

    ('B35-3',
     'A wargear price keyed by unit NAME alone is provably wrong: "Defiler" is five separate '
     'datasheets across five factions. The price map is keyed by datasheet id, faction-resolved '
     'from the MFM file it came from.',
     'Datasheets.csv',
     lambda S: (
         len([1 for r in pipe_rows(os.path.join(S.dir, 'Datasheets.csv'))
              if r['name'] == 'Defiler']) >= 5,
         'Defiler datasheet ids: ' + ', '.join(sorted(
             r['id'] + '/' + r['faction_id']
             for r in pipe_rows(os.path.join(S.dir, 'Datasheets.csv'))
             if r['name'] == 'Defiler')))),

    ('B35-4',
     'The same item name is priced on one datasheet and free on another, so cost cannot hang '
     "off the item name globally: Wolf Guard Terminators' storm shield costs 5, Terminator "
     "Assault Squad's storm shield costs nothing.",
     'MFM_Space_Wolves_v1_0.txt:89; MFM_Space_Marines_v1_0.txt:372-373',
     lambda S: (
         S.wargear_points()['000000318']['items'].get('storm shield', {}).get('cost') == 5
         and 'storm shield' not in S.wargear_points()['000000118']['items'],
         'storm shield: 5 on 000000318, unpriced on 000000118')),

    ('B35-5',
     'Every priced item name resolves, case-insensitively, into the reachable item set of its '
     'own unit in unit_loadouts.json. Nothing is priced that the unit cannot carry.',
     'wargear_points.json vs unit_loadouts.json',
     lambda S: wargear_names_resolve(S)),

]


def wargear_names_resolve(S):
    bad = []
    for uid, blk in S.wargear_points().items():
        if uid.startswith('_'):
            continue
        lo = S.loadouts().get(uid)
        if not lo:
            bad.append(uid + ': no loadout')
            continue
        reach = set()
        def put(n):
            for p in str(n or '').split(' + '):
                if p.strip():
                    reach.add(p.strip().lower())
        for g in lo.get('model_groups', []):
            for w in (g.get('default_weapons') or []) + (g.get('default_wargear') or []):
                put(w)
        for o in lo.get('options', []):
            for k in ('adds_weapon', 'adds_wargear', 'replaces', 'replacement'):
                put(o.get(k))
            for k in ('choices', 'replacement_choices', 'equipment_parts', 'equipment_choices'):
                for c in (o.get(k) or []):
                    put(c)
        for item in blk['items']:
            if item not in reach:
                bad.append(uid + ': ' + item)
    return (not bad), ('unresolved priced items: ' + '; '.join(bad)) if bad else \
        'all priced items reachable in their own unit'


def d95(S):
    bad = []
    for uid, v in S.loadouts().items():
        if uid.startswith('_'):
            continue
        names = []
        for g in v.get('model_groups', []):
            names += (g.get('default_weapons') or []) + (g.get('default_wargear') or [])
        for o in v.get('options', []):
            for f in ('replaces', 'replacement', 'requires_weapon', 'adds_weapon', 'equipment'):
                if isinstance(o.get(f), str):
                    names.append(o[f])
            names += [c for c in (o.get('choices') or []) if isinstance(c, str)]
            names += list(o.get('equipment_parts') or [])
        for n in names:
            if re.search(r'\s[\u2013-]\s', n):
                bad.append((uid, n))
    return (not bad), f'{len(bad)} profile-suffixed names' + (f' e.g. {bad[:3]}' if bad else '')

def compound_gate(S):
    d = S.loadouts().get('000000083', {})
    for o in d.get('options', []):
        if o.get('id') == 'add_4':
            gate = o.get('requires_weapon', '')
            parts = [p.strip() for p in gate.split(' + ') if p.strip()]
            ok = len(parts) == 2 and {p.lower() for p in parts} == {
                'heavy bolt pistol', 'astartes chainsword'}
            return ok, f'gate = {gate!r} ({len(parts)} part(s))'
    return False, 'add_4 not found on 000000083'

# ── runner ────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dir', default='.', help='directory holding the source CSVs and unit_loadouts.json')
    ap.add_argument('-v', '--verbose', action='store_true')
    a = ap.parse_args()

    S = Sources(a.dir)
    fails = []
    for aid, stmt, src, fn in ASSERTIONS:
        try:
            ok, detail = fn(S)
        except Exception as e:
            ok, detail = False, f'{type(e).__name__}: {e}'
        if not ok:
            fails.append((aid, stmt, src, detail))
        if a.verbose or not ok:
            print(f'{"PASS" if ok else "FAIL"}  {aid}  {detail}')

    print(f'\n{len(ASSERTIONS) - len(fails)}/{len(ASSERTIONS)} rules assertions pass.')
    if fails:
        print('\nA stated fact is not true of the data. One of the two is wrong — find out which '
              'before doing anything else.\n')
        for aid, stmt, src, detail in fails:
            print(f'  {aid}: {stmt}\n    source: {src}\n    got:    {detail}\n')
        return 1
    return 0

if __name__ == '__main__':
    sys.exit(main())
