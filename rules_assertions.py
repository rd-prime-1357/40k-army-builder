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
]

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
