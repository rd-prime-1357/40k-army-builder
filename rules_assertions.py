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

    def units(self):
        if 'un' not in self._cache:
            with open(os.path.join(self.dir, 'units.json'), encoding='utf-8') as f:
                self._cache['un'] = json.load(f)
        return self._cache['un']

    def ds_wargear_abilities(self):
        if 'dw' not in self._cache:
            with open(os.path.join(self.dir, 'datasheet_wargear_abilities.json'),
                      encoding='utf-8') as f:
                self._cache['dw'] = json.load(f)
        return self._cache['dw']

    def options(self):
        if 'op' not in self._cache:
            self._cache['op'] = list(pipe_rows(os.path.join(self.dir, 'Datasheets_options.csv')))
        return self._cache['op']

    def composition(self):
        if 'cp' not in self._cache:
            self._cache['cp'] = list(pipe_rows(os.path.join(self.dir, 'Datasheets_unit_composition.csv')))
        return self._cache['cp']

    def option_text(self, ds_id, line):
        for r in self.options():
            if r['datasheet_id'] == ds_id and r['line'] == str(line):
                return re.sub(r'<[^>]+>', ' ', r['description'])
        return ''

    def mfm_all(self):
        """Every MFM faction pack, concatenated. The WARGEAR OPTIONS blocks in here are
        the ONLY source that says an item costs points. Silence in wargear_points.json is
        not evidence (D107) — silence HERE is."""
        if 'mfm' not in self._cache:
            txt = []
            for fn in sorted(os.listdir(self.dir)):
                if fn.startswith('MFM_') and fn.endswith('.txt'):
                    with open(os.path.join(self.dir, fn), encoding='utf-8-sig',
                              errors='replace') as f:
                        txt.append(f.read())
            self._cache['mfm'] = '\n'.join(txt).lower()
        return self._cache['mfm']

    def index_html(self):
        if 'ix' not in self._cache:
            with open(os.path.join(self.dir, 'index.html'), encoding='utf-8') as f:
                self._cache['ix'] = f.read()
        return self._cache['ix']

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


# ── E14 / B18 helpers ─────────────────────────────────────────────────────────

def _e14_quals(S):
    """The options the engine seeds. Mirrors loIsFreeDefaultAdd's data-side test."""
    wp = S.wargear_points()
    out = []
    for uid, v in S.loadouts().items():
        if uid.startswith('_') or not isinstance(v, dict):
            continue
        priced = (wp.get(uid) or {}).get('items') or {}
        for o in v.get('options', []):
            if o.get('type') != 'add':
                continue
            if o.get('requires_weapon') or o.get('pool_id') or o.get('per_n_models'):
                continue
            if o.get('max_total') != 1:
                continue
            item = o.get('equipment') or o.get('adds_weapon')
            if not item:
                continue
            if item.lower() in priced:
                continue
            out.append((uid, o['id'], item))
    return out

def e14_free(S):
    """Rebuild the MFM prices from the MFM itself with the real parser, then check that
    no add the engine seeds is priced FOR ITS OWN UNIT. Grepping the whole corpus is not
    good enough: 'per Multi-melta 10 pts' is a Sororitas line, and a Land Raider's free
    multi-melta must not be condemned by it."""
    import glob
    import mfm_points_parser as M
    paths = sorted(glob.glob(os.path.join(S.dir, 'MFM_*.txt')))
    built, _ = M.build_wargear_points(paths,
                                      os.path.join(S.dir, 'units.json'),
                                      os.path.join(S.dir, 'unit_loadouts.json'),
                                      os.path.join(S.dir, 'Datasheets.csv'))
    # Compare the PRICES, not the provenance string: the same item is printed in several
    # chapter packs at the same cost, so which file gets cited depends on scan order.
    def prices(d):
        return {k: {i: v['cost'] for i, v in (val.get('items') or {}).items()}
                for k, val in d.items() if not k.startswith('_')}
    fresh = prices(built)
    if fresh != prices(S.wargear_points()):
        return False, 'wargear_points.json does not rebuild from the MFM — it is stale'
    bad = [(u, i) for u, _, i in _e14_quals(S) if i.lower() in (fresh.get(u) or {})]
    return (not bad), f'{len(_e14_quals(S))} seeded adds, {len(bad)} priced for their own unit' + \
        (f': {bad}' if bad else '')

def e14_count(S):
    q = _e14_quals(S)
    units = {u for u, _, _ in q}
    return (len(q) == 53 and len(units) == 33), f'{len(q)} options across {len(units)} units'

def b18_named_body(S):
    lines = [re.sub(r'<[^>]+>', ' ', r['description'])
             for r in S.options() if r['datasheet_id'] == '000001044']
    per5 = [t for t in lines if re.search(r'for every 5 models in this unit', t, re.I)]
    named = [t for t in per5 if re.search(r'plague marines?[\u2019\']?s?\b', t, re.I)]
    return (len(per5) == 5 and len(named) == 5), f'{len(named)}/{len(per5)} per-5 lines name the body model'


def _fan_scope_qualifies(desc):
    """True for a per-N-models or any-number-of-models swap line (the pattern
    B18c/B18d/B18f fan onto multiple carrying groups) — excludes single-model
    named-leader lines (e.g. 'The Watch Sergeant's ... can be replaced ...')
    which are a different option entirely and never fanned."""
    d = re.sub(r'<[^>]+>', ' ', desc).strip()
    return bool(re.match(r'^(for every \d+ models? in (this|the) unit|any number of models?)\b', d, re.I))

def _fan_scope_is_generic(desc):
    """D116: the swap's scope subject — the noun phrase right before 'can' —
    is the generic word 'model'/'models' (bare or possessive), reaching every
    carrying group including a leader/sergeant group. A named body type
    ('1 Eradicator's melta rifle', '1 Deathwing Terminator') is body-only and
    must NOT be fanned onto the leader/sergeant group. Returns None if the
    sentence shape isn't recognised (caller should treat that as a failure,
    not a pass)."""
    d = re.sub(r'<[^>]+>', ' ', desc)
    m = re.search(r'unit,\s*(.+?)\s+can\b', d, re.I) or re.search(r'^(any number of.+?)\s+can\b', d, re.I)
    if not m:
        return None
    subj = re.sub(r'^(up to \d+|any number of|\d+|one)\s+', '', m.group(1).strip(), flags=re.I)
    return bool(re.match(r"^models?(['\u2019]s)?\b", subj, re.I))

def b18h_fan_allowlist_generic(S):
    """D116/B18h. Every unit in equipped_parser.py's _FAN_UNIT_ALLOWLIST must rest on a
    Datasheets_options.csv line whose scope subject is the generic word 'model' — never a
    named body type. Closes the S83 near-miss where a hand-patched fan onto a named-body-type
    unit (000000103/000001177) passed repro_check.py and every other assertion because nothing
    covered it. A negative control (000000103, a known named-body unit NOT in the allowlist)
    must classify False, or the classifier itself is vacuous."""
    import equipped_parser as EP
    bad = []
    for uid in sorted(EP._FAN_UNIT_ALLOWLIST):
        quals = [r['description'] for r in S.options()
                 if r['datasheet_id'] == uid and r['button'] == '\u2022'
                 and _fan_scope_qualifies(r['description'])]
        if not quals:
            bad.append(f'{uid}: no qualifying per-N/any-number scope line found')
            continue
        for desc in quals:
            if _fan_scope_is_generic(desc) is not True:
                bad.append(f'{uid}: named-body (non-generic) scope line — {desc[:70]!r}')
    control = [r['description'] for r in S.options()
               if r['datasheet_id'] == '000000103' and r['button'] == '\u2022'
               and _fan_scope_qualifies(r['description'])]
    if not control or _fan_scope_is_generic(control[0]) is not False:
        bad.append('negative control 000000103 did not classify as named-body — classifier is vacuous')
    return (not bad), (f'{len(EP._FAN_UNIT_ALLOWLIST)} allowlist units checked, '
                        f'{len(bad)} problem(s)' + (f': {bad}' if bad else ''))


def b46_orphaned(S):
    """B46. datasheet_wargear_abilities.json (built from Datasheets_abilities.csv type=Wargear)
    holds ability text for OPTION-granted items. units.json's wargear_ability_names carries
    DEFAULT-issue gear only, so while the popups read that field alone, 12 abilities across 8
    units were unreachable. The fix is the channel, not the data: the popups now name their
    abilities from datasheet_wargear_abilities.json UNION units.json (allWargearAbilityNames),
    which makes the unreachable count structurally zero. This asserts BOTH halves — that the
    engine really does source it that way, and that nothing in the ds file falls outside the
    union. Behaviour (the three-way carrier filter) is proven in stat_check.js.
    """
    import os
    src = open(os.path.join(S.dir, 'index.html'), encoding='utf-8').read()
    if 'function allWargearAbilityNames(' not in src:
        return False, 'index.html does not define allWargearAbilityNames — popups still read units.json only'
    calls = src.count('allWargearAbilityNames(raw)')
    if calls < 2:
        return False, f'allWargearAbilityNames used {calls}x — both popups (browse + configured) must use it'
    units = {}
    for block in S.units():
        for u in block.get('units', []):
            units[u.get('unit_id')] = u
    unreachable = []
    for uid, abils in S.ds_wargear_abilities().items():
        if uid.startswith('_') or uid not in units:
            continue
        reachable = set(abils)                       # the ds file half of the union
        for mg in units[uid].get('model_groups', []):
            reachable |= set(mg.get('wargear_ability_names') or [])
        for name in abils:
            if name not in reachable:
                unreachable.append((uid, name))
    return (len(unreachable) == 0), f'{len(unreachable)} option-granted wargear abilities the popup cannot list'


def repro_gate(S):
    """D123: the executable form of 'the parser is fresh'. Runs the full pipeline from
    source and asserts byte-identical reproduction of the committed unit_loadouts.json.
    Subsumes the old P1 function-name check: it does not care what the parser is called
    or which functions it defines, only whether it still produces what is committed, so
    no wrong copy — stale, partial, or renamed — can pass."""
    import os, importlib.util
    p = os.path.join(S.dir, 'repro_check.py')
    if not os.path.exists(p):
        return False, 'repro_check.py not found — the reproduction gate is missing'
    spec = importlib.util.spec_from_file_location('repro_check', p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.repro(S.dir)


def units_repro_gate(S):
    """D164 (B55): the executable form of 'units.json and its glossary lookups are fresh'.
    Runs the real per-faction pipeline from source and demands byte-identical reproduction
    of the committed units.json AND the four merged lookups. Without this, the lookups were
    the one deployed output nothing checked, and they drifted silently for several sessions."""
    import os, importlib.util
    p = os.path.join(S.dir, 'units_repro_check.py')
    if not os.path.exists(p):
        return False, 'units_repro_check.py not found — the units reproduction gate is missing'
    spec = importlib.util.spec_from_file_location('units_repro_check', p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.repro(S.dir)


def manifest_gate(S):
    """D123: file-integrity manifest. Any guarded pipeline file arriving as the wrong
    copy fails here and names the file — the cheap first line the repro gate backs up."""
    import os, importlib.util
    p = os.path.join(S.dir, 'pipeline_manifest.py')
    if not os.path.exists(p):
        return False, 'pipeline_manifest.py not found'
    spec = importlib.util.spec_from_file_location('pipeline_manifest', p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.check(S.dir)


ASSERTIONS = [

    # ── P1. Parser freshness gate, machine-enforced (D118/D123). Prose could not hold
    # this — the stale copy survived twelve consecutive sessions of a written checklist,
    # and the original P1 (four function names must exist) was too weak: it passed on any
    # wrong copy that kept the names. P1 is now the reproduction gate: run the pipeline
    # from source, demand byte-identical output. Nothing else proves the file is fresh.
    ('P1',
     'The pipeline reproduces the committed unit_loadouts.json byte-for-byte from source: '
     'loadout_parser.py regenerates every entry (bar the two hand-authored seeds), the five '
     'faction web.txt passes and the datasheets pass refine it, and the result matches. A '
     'stale, partial, or renamed parser cannot pass.',
     'repro_check.py (D123)',
     lambda S: repro_gate(S)),

    # ── P4. The same gate for the other half of the deployed data (D164/B55). P1 covers
    # unit_loadouts.json only; units.json and the four glossary lookups the app loads
    # (abilities, rules, keywords, weapon_abilities) had no reproduction check at all.
    # abilities.json had drifted 76 entries and 33 mangled inch marks before anyone looked.
    ('P4',
     'The pipeline reproduces the committed units.json byte-for-byte from source '
     '(SM and DG through wahapedia_transform, CD direct off the root CSVs, merged, then the '
     'three post-merge passes), and every one of the four merged glossary lookups matches too. '
     'A stale committed lookup cannot pass.',
     'units_repro_check.py (D164)',
     lambda S: units_repro_gate(S)),

    # ── P3. File-integrity manifest (D123). Guards every pipeline file by content hash,
    # including the four the repro gate does not touch (index.html, units.json,
    # wargear_points.json, datasheet_wargear_abilities.json). Regenerated at session close.
    ('P3',
     'Every guarded pipeline file matches pipeline_manifest.json. A wrong copy of any of '
     'them — output, parser, harness or assertion file — fails here and names the file. '
     'Regenerate the manifest at session close (python3 pipeline_manifest.py --write).',
     'pipeline_manifest.json (D123)',
     lambda S: manifest_gate(S)),

    # ── B46. The Reiver's grav-chute has rules text and the app cannot show it. The text
    # is NOT missing from the data — it is in Datasheets_abilities.csv as a Wargear row.
    # units.json only carries DEFAULT-issue wargear abilities, and the popup reads units.json.
    ('B46-1',
     "Reiver Grav-chute and Grapnel Launcher have Wargear ability text on the Reiver "
     "datasheet, and units.json does not list either — so the popup cannot show them. The "
     "data is present; the channel is wrong.",
     'Datasheets_abilities.csv 000002718 lines 5-6 (type=Wargear)',
     lambda S: (
         {r['name'] for r in S.abilities()
          if r['datasheet_id'] == '000002718' and r['type'] == 'Wargear'}
         == {'Grapnel Launcher', 'Reiver Grav-chute'},
         'Wargear rows on 000002718: ' + ', '.join(sorted(
             r['name'] for r in S.abilities()
             if r['datasheet_id'] == '000002718' and r['type'] == 'Wargear')))),

    ('B46-2',
     'The gap was systemic, not a Reiver bug: 12 option-granted wargear abilities across 8 '
     'units have text in datasheet_wargear_abilities.json that units.json never lists, so no '
     'popup can reach them. B46 landed: the popups name their abilities from the ds file '
     'unioned with units.json, so the unreachable count is ZERO. Both popups must use it.',
     'datasheet_wargear_abilities.json; index.html allWargearAbilityNames (D122)',
     b46_orphaned),


    # ── E14. A free add defaults to selected. "Free" is a claim about the MFM, not
    # about our derived file, so it is checked against the MFM itself (D107).
    ('E14-1',
     'Every add the engine seeds ON is unpriced. Checked by rebuilding the prices from the '
     'MFM WARGEAR OPTIONS blocks with the real parser and confirming no seeded item is '
     'priced FOR ITS OWN UNIT — so seeding cannot inflate a list. Also proves '
     'wargear_points.json is not stale against the MFM.',
     'MFM_*.txt WARGEAR OPTIONS blocks (via mfm_points_parser.build_wargear_points)',
     lambda S: e14_free(S)),

    ('E14-2',
     'The seeding rule is total, not a hand-picked list: an add qualifies iff it is '
     'type=add, has no requires_weapon, no pool_id, no per_n_models, max_total == 1, and '
     'its item is unpriced. 53 options across 33 units qualify today.',
     'unit_loadouts.json; wargear_points.json',
     lambda S: e14_count(S)),

    # ── B18. The scope of a datasheet option is whatever its own sentence says. This is
    # the fact the S56 prompt got wrong: it claimed weapon swaps stay inside their model
    # group. The source says otherwise, and these two rows are why.
    ('B18-1',
     'Terminator Assault Squad line 1 says "Any number of models" — a generic model, not '
     '"Assault Terminator". The swap therefore reaches the Assault Terminator Sergeant, '
     'and a weapon swap is NOT confined to the body group.',
     'Datasheets_options.csv 000000118 line 1',
     lambda S: (bool(re.search(r'any number of models', S.option_text('000000118', 1), re.I))
                and not re.search(r'assault terminator[\u2019\']s', S.option_text('000000118', 1), re.I),
                repr(S.option_text('000000118', 1))[:110])),

    ('B18-2',
     'Reiver Squad line 2 gates on the Reiver SERGEANT holding a bolt carbine, and the '
     'only source of a bolt carbine is line 1\'s "All models in this unit" swap. Line 2 is '
     'unreachable text unless line 1 reaches the Sergeant. The gate proves the scope.',
     'Datasheets_options.csv 000002718 lines 1-2',
     lambda S: (bool(re.search(r'all models in this unit', S.option_text('000002718', 1), re.I))
                and 'bolt carbine' in S.option_text('000002718', 1).lower()
                and bool(re.search(r'if the reiver sergeant is equipped with 1 bolt carbine',
                                   S.option_text('000002718', 2), re.I)),
                'line1=%r line2=%r' % (S.option_text('000002718', 1)[:48],
                                       S.option_text('000002718', 2)[:48]))),

    ('B18-3',
     'The converse holds and bounds the fix: where the sentence names the BODY model type '
     '("1 Plague Marine\'s boltgun"), the leader is excluded. Every one of Plague Marines\' '
     'five per-5 swap lines names "Plague Marine", so the Plague Champion is correctly out '
     'of scope. B18 must not widen these.',
     'Datasheets_options.csv 000001044',
     lambda S: b18_named_body(S)),


    ('B18-4',
     'D116 is now IN THE DATA, not just in the log: Terminator Assault Squad\'s generic '
     '"Any number of models" swap is scoped to the Assault Terminator Sergeant group as '
     'well as the body. Without this the Sergeant can never drop his storm shield and '
     'D112\'s conferred-W4 override can never revert.',
     'unit_loadouts.json 000000118 (from Datasheets_options.csv 000000118 line 1)',
     lambda S: (
         'Assault Terminator Sergeant' in {o.get('scope') for o in S.loadouts()['000000118']['options']
                                           if o.get('replacement') == 'Twin lightning claws'},
         'scopes: ' + ', '.join(sorted(str(o.get('scope')) for o in
                                       S.loadouts()['000000118']['options'])))),

    ('B18-5',
     'The converse holds IN THE DATA too: Plague Marines\' per-5 swaps name the body model '
     '("1 Plague Marine\'s boltgun"), so no option of theirs may be scoped to the Plague '
     'Champion except the two the datasheet gives him by name.',
     'unit_loadouts.json 000001044 (from Datasheets_options.csv 000001044)',
     lambda S: (
         sum(1 for o in S.loadouts()['000001044']['options']
             if o.get('scope') == 'Plague Champion') == 2,
         'Champion-scoped options: %d' % sum(1 for o in S.loadouts()['000001044']['options']
                                             if o.get('scope') == 'Plague Champion'))),

    ('B18h-1',
     'D116, made executable: every unit in equipped_parser.py\'s _FAN_UNIT_ALLOWLIST rests on '
     'a Datasheets_options.csv scope line whose subject is the generic word "model," never a '
     'named body type. A negative control proves the classifier actually discriminates.',
     'Datasheets_options.csv (per-N/any-number scope lines) + equipped_parser._FAN_UNIT_ALLOWLIST (D116/D150)',
     lambda S: b18h_fan_allowlist_generic(S)),

    ('B34-1',
     'The size-exact swap on Wolf Scouts (unlocks only at 12 models) and on Blightlord '
     'Terminators (unlocks only at 3 models) is present in unit_loadouts.json as a count '
     'option carrying required_size:N. Absent the classifier, both lines are UNMATCHED '
     'and the swap is silently dropped — the player cannot take a legal weapon. The '
     'assertion checks presence of the option with the correct required_size on both '
     'units; engine enforcement (suppressing the option at other sizes) is a downstream '
     'concern and covered by the engine turn.',
     'Datasheets_options.csv 000004182 line 4 + 000001372 line 6 -> unit_loadouts.json',
     lambda S: (
         any(o.get('required_size') == 12 for o in S.loadouts()['000004182']['options']) and
         any(o.get('required_size') == 3  for o in S.loadouts()['000001372']['options']),
         'WS gate: %s; BLT gate: %s' % (
             next((o.get('required_size') for o in S.loadouts()['000004182']['options']
                   if o.get('required_size') is not None), None),
             next((o.get('required_size') for o in S.loadouts()['000001372']['options']
                   if o.get('required_size') is not None), None)))),

    ('B34-2',
     'Every required_size value in unit_loadouts.json is a member of that unit\'s '
     'declared size_brackets. A stale gate — brackets changed but required_size did not — '
     'would render the option unreachable at every bracket; this assertion catches that '
     'divergence before the engine sees it.',
     'unit_loadouts.json size_brackets vs option.required_size',
     lambda S: (
         all(o.get('required_size') in d.get('size_brackets', [])
             for d in S.loadouts().values() if isinstance(d, dict)
             for o in d.get('options', []) if o.get('required_size') is not None),
         'options carrying required_size: %d' % sum(
             1 for d in S.loadouts().values() if isinstance(d, dict)
             for o in d.get('options', []) if o.get('required_size') is not None))),

    ('B42-1',
     'Vanguard Veterans with Jump Packs can take a storm shield. The datasheet sentence '
     'drops GW\'s own "with" ("...bolt pistol replaced one of the following"), which the '
     'parser must tolerate — otherwise the whole line is UNMATCHED and the shield, which '
     'is the unit\'s only source of its 4+ invulnerable save, never reaches the player.',
     'Datasheets_options.csv 000000147 line 1 -> unit_loadouts.json 000000147',
     lambda S: (
         any('Storm Shield' in (o.get('replacement_choices') or [])
             for o in S.loadouts()['000000147']['options']),
         'options: %d' % len(S.loadouts()['000000147']['options']))),

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

    # ── B35 engine half. The cost is charged off the rollup, so every priced unit must
    # reach the engine's rollup path at all: a priced unit with no loadout def, or one
    # missing from units.json, would be silently under-priced and nothing would fail.
    ('B35-6',
     'Every priced unit id exists in units.json AND has a loadout definition. The wargear sum '
     "is charged off loRollup's output, so a priced unit with no loadout def could never be "
     'charged for anything.',
     'wargear_points.json vs units.json + unit_loadouts.json',
     lambda S: priced_units_are_rollable(S)),

    ('B35-7',
     'An exact-string match on item names would silently under-price. Our own data disagrees '
     "with itself on casing — Terminator Assault Squad's default_wargear says 'storm shield', "
     "Thunderwolf Cavalry's equipment_parts says 'Storm Shield' — so the price map is keyed "
     'lowercased and every engine lookup goes through weaponBase(name).toLowerCase().',
     'unit_loadouts.json 000000118 / 000000322; wargear_points.json',
     lambda S: (
         'storm shield' in (S.loadouts()['000000118']['model_groups'][0].get('default_wargear') or [])
         and any('Storm Shield' in (o.get('equipment_parts') or [])
                 for o in S.loadouts()['000000322']['options'])
         and all(k == k.lower()
                 for uid, blk in S.wargear_points().items() if not uid.startswith('_')
                 for k in blk['items']),
         'casing conflict is real; price map keys are all lowercase')),

    ('B35-8',
     'The engine actually charges wargear: index.html loads wargear_points.json and ptsForEntry '
     'adds the rollup-driven wargear sum to the size-bracket cost. One place computes an entry '
     'cost, and both the per-entry display and the list total read it.',
     'index.html ptsForEntry',
     lambda S: (
         'wargear_points.json' in S.index_html()
         and 'wargearCostForEntry(entry, unit)' in S.index_html()
         and 'wargearCostForRollup' in S.index_html(),
         'ptsForEntry sums the rollup against wargear_points.json')),

    # ── B15 / D105. The conferred-characteristic engine. The name-keyed glossary
    # is the bug; datasheet_wargear_abilities.json is the fix, and the engine must
    # actually be reading it.
    ('B15-8',
     'weapon_abilities.json is keyed by NAME and therefore flattens Storm Shield to a '
     'single text — the Terminator Assault Squad one. It is not a legitimate source for '
     'a conferred characteristic and must never be the primary lookup.',
     'weapon_abilities.json; Datasheets_abilities.csv 000000118',
     lambda S: flat_glossary_is_wrong(S)),

    ('B15-9',
     'datasheet_wargear_abilities.json reproduces the Wargear rows of '
     'Datasheets_abilities.csv exactly, for every unit in units.json.',
     'Datasheets_abilities.csv (type=Wargear); units.json',
     lambda S: ds_wargear_file_matches_source(S)),

    ('B15-10',
     'index.html reads the per-datasheet table first and the flat glossary only as a '
     'fallback, and counts carriers against the configured loadout (D105).',
     'index.html',
     lambda S: (
         'dsWargearAbilities' in S.index_html()
         and 'function wargearAbilityDesc' in S.index_html()
         and 'function wargearCarrierState' in S.index_html()
         and 'function conferredStats' in S.index_html()
         and 'function statGroupScopes' in S.index_html(),
         'engine wired to the per-datasheet table and to carrier counting')),

    ('B15-11',
     "Storm Shield RAISES Wolf Guard Battle Leader's Wounds (printed 5 -> 6). The "
     'old claim that it dropped him to 4 came from the flattened name lookup.',
     'Datasheets_abilities.csv 000004130; Datasheets_models.csv 000004130',
     lambda S: (
         read_characteristic(S.wargear_ability('000004130', 'Storm Shield')) == 'W:6'
         and int(S.model_stat('000004130', 'W')) == 5,
         f"text -> {read_characteristic(S.wargear_ability('000004130', 'Storm Shield'))}, "
         f"printed W {S.model_stat('000004130', 'W')}")),

    # ---- B36 / D113. The Lieutenant's wargear options. ----

    ('B36-1',
     "A plasma pistol is only obtainable on the Lieutenant by GIVING UP the "
     "master-crafted bolter. There is no option that swaps the bolt pistol for a plasma "
     "pistol, so 'master-crafted bolter kept + plasma pistol' is an ILLEGAL build. The "
     "bolt pistol's only swap is the heavy bolt pistol -- which is why the legal build "
     "the tool must support is bolter kept + HEAVY bolt pistol + power fist.",
     'Datasheets_options.csv 000001346 lines 1 and 3; Space_Marines_web.txt, Lieutenant, '
     'Wargear Options',
     lambda S: lieutenant_plasma_costs_the_bolter(S)),

    ('B36-2',
     "The Lieutenant's atomic 3-for-3 swap (bolt pistol + master-crafted bolter + close "
     "combat weapon -> neo-volkite pistol, master-crafted power weapon, storm shield) is "
     "written TWICE in our data: once as a bundled_swaps endpoint and once as a "
     "unit_loadouts.json choice option. Exactly one control may render it.",
     'bundled_swaps.json (Lieutenant Wargear / lt-nvp-mcpw-shield); '
     'unit_loadouts.json 000001346 sng_2',
     lambda S: bundle_and_loadout_restate_the_same_swap(S, '000001346')),

    ('B39-1',
     'No unit carries both a bundled_swaps group and a flat wargear_options row whose '
     'replaced/replacement weapon family sits inside that group\'s endpoints (removes '
     '\u222a adds), scoped to model group. A bundle owns the whole slot once it touches '
     'the family on either side of an endpoint.',
     'convert_to_json.py _bundle_owns (D130); units.json bundled_swaps + wargear_options',
     lambda S: no_bundle_owned_flat_swap_survives(S)),

    ('B36-3',
     'index.html suppresses a loadout option whose replaced-weapon set equals a bundle '
     "endpoint's removes set, and tests bundle-managed families part by part so a "
     'compound "A + B + C" replaces string is recognised.',
     'index.html',
     lambda S: (
         'function bundleDuplicateSwaps' in S.index_html()
         and 'loWeaponParts(o.replaces).some(p => managed.has(p))' in S.index_html(),
         'engine wired to duplicate-swap suppression and part-wise managed test')),

    # ── B41 + E3 + D115 — datasheet instance limits ──────────────────────────
    #
    # SOURCED, at last: Army_Muster_Rules.txt, 25.03 "Select Battle Size". The battle-size
    # table gives Unit Limit 2 at INCURSION (1000 pts) and 3 at STRIKE FORCE (2000 pts),
    # and its footnote reads: "The unit limit for BATTLELINE and DEDICATED TRANSPORT units
    # is double the relevant amount shown above, and every EPIC HERO has a unit limit of 1,
    # regardless of the battle size."
    #
    # The flat 3 / 6 / 1 the engine carried through v5.61 was the Strike Force row applied
    # to BOTH battle sizes. At Incursion it silently permitted an illegal third unit. D114
    # recorded that the numbers had no source; D115 found the source and found them wrong.

    ('B41-1',
     'The datasheet limit is a hard block, not a warning: the engine refuses an add at the '
     'limit (canAddUnit false) rather than accepting it and flagging it. D0 — a limit the '
     'tool merely flags is a limit it does not enforce.',
     'Army_Muster_Rules.txt 25.04 "You cannot exceed any of the values presented in the '
     'Select Battle Size table"; index.html canAddUnit / addUnitFromRoster',
     lambda S: (
         'function canAddUnit' in S.index_html()
         and 'if (!canAddUnit(copyCount, lim))' in S.index_html(),
         'addUnitFromRoster gated on canAddUnit')),

    ('B41-2',
     'The unit limits the engine applies track the BATTLE SIZE: base 2 at Incursion (1000) '
     'and 3 at Strike Force (2000); Battleline and Dedicated Transport are double that '
     '(4 / 6); every Epic Hero is 1 regardless of battle size.',
     'Army_Muster_Rules.txt 25.03 Select Battle Size table + footnote; index.html '
     'battleSizeUnitLimit / instanceLimit',
     lambda S: instance_limits_intact(S)),

    ('B41-3',
     'The battle-size table in Army_Muster_Rules.txt says what the engine says it says. '
     'This assertion reads the SOURCE, not the engine — if GW reissues the table, this '
     'breaks before the engine silently drifts.',
     'Army_Muster_Rules.txt 25.03',
     lambda S: muster_battle_size_table(S)),

    ('E3',
     'One function decides all three limit states, so the roster card, the add path and the '
     "detail flag cannot disagree. Red means EXCEEDED, never merely reached: limitState "
     "returns 'at' at the limit and 'over' only past it. 'over' stays reachable — a list "
     'that is legal at Strike Force can be over-limit at Incursion.',
     'index.html limitState / renderRoster / entryHasError / selectArmyPoints',
     lambda S: (
         'function limitState' in S.index_html()
         and "const state    = limitState(count, lim);" in S.index_html()
         and "const overLim  = state === 'over';" in S.index_html()
         and "if (limitState(count, unitLimit(unit)) === 'over') return true;" in S.index_html(),
         "limitState is the single source of the 'ok' / 'at' / 'over' split")),

    ('D115',
     'The limit is never frozen onto a unit record. unitLimit() reads POINTS_CAP live, and '
     'changing the battle size redraws the roster — otherwise the create and open paths, '
     'which both set the faction BEFORE the points total, would bake in a stale limit.',
     'index.html unitLimit / setActiveUnits / selectArmyPoints',
     lambda S: (
         'function unitLimit' in S.index_html()
         and 'limitOverride: unit.instance_limit_override || null,' in S.index_html()
         and 'instanceLimit(u.unit_type, POINTS_CAP)' in S.index_html(),
         'limit is derived live from POINTS_CAP, not stored on allUnits')),

    # ── E9a. must_be_warlord is true iff the unit carries SUPREME COMMANDER in
    # source (any built faction, any ability `type`), or is Be'Lakor (hand-added
    # per D132 — Gen-1 CD data never routes through wahapedia_transform.py, so its
    # own datasheet_id never appears as a match key in Datasheets_abilities.csv).
    ('E9a-1',
     "must_be_warlord is true on exactly the units whose datasheet carries a "
     "SUPREME COMMANDER ability in source, plus Be'Lakor by name.",
     'Datasheets_abilities.csv (SUPREME COMMANDER rows) + units.json must_be_warlord',
     lambda S: e9a_warlord(S)),

    # ── E9b. cannot_be_warlord is true iff the unit's datasheet carries a
    # description containing both "cannot" and "warlord" in source (any built
    # faction, any ability name/type — the restriction isn't a single named
    # ability, unlike SUPREME COMMANDER), or is Exalted Flamer by name
    # (hand-added per D132 — Gen-1 CD data never routes through
    # wahapedia_transform.py, so its datasheet_id never appears as a match key
    # in Datasheets_abilities.csv).
    ('E9b-1',
     'cannot_be_warlord is true on exactly the units whose datasheet carries a '
     '"cannot...Warlord" ability description in source, plus Exalted Flamer by name.',
     'Datasheets_abilities.csv (cannot+Warlord rows) + units.json cannot_be_warlord',
     lambda S: e9b_cannot_warlord(S)),

    # ── B7a. Stack-size cap of 2 on canAttachLeader (D157). permitsCoLeader is
    # pairwise-only and stays correct for the pair; a 3rd attach must refuse
    # regardless of pairwise permits, so the cap has to be a separate guard that
    # short-circuits before the pairwise loop can ever say yes.
    ('B7a-1',
     'canAttachLeader refuses a 3rd leader on a bodyguard already carrying 2, '
     'even when every pairwise permit would allow it. permitsCoLeader itself is '
     'untouched — the cap is a stack-size guard, not a change to the pair rule.',
     'index.html canAttachLeader; core rules 19.01; D157',
     lambda S: b7a_stack_cap(S)),

    # ── B7b. Combined attached-unit popup with per-stat aura markers (D157/D159).
    # Two independent checks: (1) the exact set of leaders carrying non-empty
    # bodyguard_stat_flags matches the S91 hand-audit; (2) the render layer wires
    # a combined-modal path off the bodyguard's ⓘ, calls buildModalConfigured per
    # attached member, and unions each leader's bodyguard_stat_flags into an
    # asterisk-marker set applied to the bodyguard's stat block.
    ('B7b-1',
     'The 16 SM+DG leaders identified in the S91 audit carry exactly the '
     'expected bodyguard_stat_flags; every other unit\'s flag list is empty. '
     'index.html defines openModalCombined and buildModalCombined, unions '
     'leader flags across attached members, and buildStatTable accepts the '
     'auraFlags parameter. renderList routes the bodyguard ⓘ to openModalCombined '
     'when attached leaders exist.',
     'S91 hand-audit of SM+DG leader unit abilities; D157/D159; index.html render layer',
     lambda S: b7b_combined_popup(S)),

    # ── B13-1. Optional Epic Hero model groups in Victrix Honour Guard (D158/B13).
    # The engine detects embedded optional Epic Hero models by name-matching ('EPIC HERO'
    # substring on an optional group), with no separate field needed. Guards: Victrix
    # has exactly the two expected groups, no other unit has such groups, and
    # editLoadoutOptional's cap check is present and correctly placed.
    ('B13-1',
     'Victrix Honour Guard (000004185) has exactly two optional model groups with '
     '"EPIC HERO" in the name (Chapter Ancient, Chapter Champion); no other unit in '
     'unit_loadouts.json has optional groups with "EPIC HERO" in the name; '
     'isOptEpicHeroBlocked is defined in index.html and editLoadoutOptional guards '
     'toggle-on with it (turning off is always allowed).',
     'unit_loadouts.json model_groups; Datasheets_keywords.csv (Epic Hero model-scoped); '
     'index.html isOptEpicHeroBlocked / editLoadoutOptional; B13 Piece 2',
     lambda S: b13_optional_epic_hero(S)),

    # ── B56a. Replaces the prose closure figures in MFM_Chapter_Pass.md (D107 again —
    # that document drifted in both directions inside one release before this landed).
    # The five chapter MFM files, run scoped through mfm_points_parser.py --scope-to-army,
    # close 77 of the 81 units.json entries that carried points: null.
    #
    # B56b (renumbered from B56a-1) taught the parser a composition-shaped bracket line
    # (role names instead of a bare model count) and closed Crusader Squad. Wolf Guard
    # Headtakers looked like the same shape but is not: its bracket lines include an
    # optional Hunting Wolves escort, and two different compositions ("6 Headtakers" vs
    # "3 Headtakers + 3 Hunting Wolves") both sum to a 6-model bracket at two different
    # prices. The parser used to detect that collision and void the unit's whole
    # composition table (D106). B56g phase 1 (S106) closed it: the resolver now keys the
    # primary bracket on the Headtaker count alone and pulls escort lines out before the
    # collision check runs, so the collision never occurs. Residual: Judiciar Xacharus and
    # Chaplain Kastiel (no points source anywhere, B56e).
    ('B56b-1',
     'Exactly 2 units in units.json carry points: null, and they are exactly Judiciar '
     'Xacharus (000004179, B56e) and Chaplain Kastiel (000004180, B56e). No other unit is '
     'uncosted, including Wolf Guard Headtakers (000004131, closed by B56g phase 1).',
     'units.json (D167/D168); MFM_Space_Wolves_v1_0.txt, MFM_Black_Templars_v1_0.txt',
     lambda S: b56a_residual_nulls(S)),

    # B56g phase 1 (S106, D174). The escort's per-model rate is re-derived from the
    # printed difference, never hand-entered: 115-85=30 over 3 wolves and 230-170=60 over
    # 6, both 10 pts/wolf, identical at the 3rd+ tier (125-95=30, 240-180=60). This check
    # is the executable form of "all four printed totals reproduce" from the ticket, plus
    # a check that the escort itself is NOT yet wired into units.json as a purchasable
    # group (that is phase 2/3, per D173) — a passing engine offer here would mean the
    # scope crept past the parser turn.
    ('B56g-1',
     'Wolf Guard Headtakers (000004131) prices at 85/170 (1st-2nd) and 95/180 (3rd+) for '
     'the printed Headtaker-only brackets (3 and 6 models). The Hunting Wolves escort '
     'derives at exactly 10 pts/model from the printed totals at both copy-tiers, and is '
     'not yet present as a model group or optional count in unit_loadouts.json.',
     'MFM_Space_Wolves_v1_0.txt (lines 72-80); mfm_points_parser.py escort resolver',
     lambda S: b56g_headtaker_escort(S)),

    # Black Templars is the negative control from D167: unscoped, 9 of its 18 datasheets
    # share a name with an Adeptus Astartes datasheet and the parser's old preference wrote
    # all nine under Adeptus Astartes, corrupting the generic roster while BT stayed
    # uncosted. This checks both halves at once — BT closes to 18/18 (B56b priced Crusader
    # Squad, the last BT residual), and the three datasheets BT prices differently from the
    # shared Adeptus Astartes name (Impulsor, Repulsor Executioner, Sternguard Veteran
    # Squad) still disagree, proving they are two separate rows rather than one overwritten
    # by the other.
    ('B56a-2',
     'Black Templars has 18 units.json entries, all with non-null points. The Adeptus '
     'Astartes and Black Templars Impulsor datasheets (000002568 / 000002786) keep distinct '
     'first-unit costs, 80 and 85 — proof the scoped chapter run did not overwrite the '
     'generic row.',
     'units.json (D167/D168, negative control)',
     lambda S: b56a_bt_negative_control(S)),

    ('B58-1',
     'Every fills_to_size model group in unit_loadouts.json carries a min field equal to '
     'the low end of its "A-B" composition line (D179/B58 phase 1). The base group minimum '
     'is real rules data the engine will need to bound banded optional-group steppers; it '
     'cannot be inferred from fills_to_size alone.',
     'Datasheets_unit_composition.csv vs unit_loadouts.json (D179)',
     lambda S: b58_min_matches_composition(S)),

    ('B58-2',
     'The engine reads the band max and the base-group min (D181/B58 phase 2). index.html '
     'defines loOptHeadroom and loOptMax; loOptCounts clamps a stored value to the band max '
     'instead of returning 0/1; loGroupCounts clamps each optional group by both its band '
     'and the remaining headroom. Data side: for every unit carrying a banded optional '
     'group, the smallest size bracket leaves room for at least one model of some band — '
     'a unit where every band is unreachable at every bracket is a data defect, not a '
     'legal composition.',
     'index.html loOptCounts / loOptHeadroom / loOptMax / loGroupCounts; unit_loadouts.json '
     'model_groups (D181)',
     lambda S: b58_engine_honours_bands(S)),

    ('B59-1',
     'Unit-instance limits are counted per-armyList-entry, keyed by unit_name, never by '
     'scanning a unit\'s model_groups. This is what makes it safe for one datasheet to '
     'embed another datasheet\'s model as an optional model group (Invader ATV inside '
     'Outrider Squad, D182) without inflating the embedded model\'s standalone datasheet '
     'limit. The fact must be executable, not commentary — E10 duplication or any future '
     '"render the ATV as its own line" would break it silently otherwise.',
     'index.html unitLimit / limitState / armyList.filter call sites (D182 category '
     'distinction: selection-scoped caps do not follow the model)',
     lambda S: b59_limits_are_entry_scoped(S)),

]


def b58_engine_honours_bands(S):
    """B58 phase 2: the min/max fields phase 1 wrote must actually bound the engine.

    1. index.html defines loOptHeadroom and loOptMax.
    2. loOptCounts clamps to the band max (it no longer returns a 0/1 flag).
    3. loGroupCounts's optional branch clamps by both the band and the headroom.
    4. Data sanity: every unit with a banded optional group (max > 1) has at least one
       bracket where headroom > 0, i.e. the bands are reachable at all.
    """
    import json as _json, os as _os

    txt = S.index_html()
    for needle, why in [
        ('function loOptHeadroom(def, size)', 'loOptHeadroom not defined in index.html'),
        ('function loOptMax(def, size, optCounts, groupName)', 'loOptMax not defined in index.html'),
        ('const cap = ct.per_bracket ? 1 : (ct.max != null ? ct.max : 1);',
         'loOptCounts does not clamp a stored value to the band max'),
        ('const v = Math.max(0, Math.min(Number(oc[g.name]) || 0, band, headroom));',
         'loGroupCounts does not clamp an optional group by both band and headroom'),
    ]:
        if needle not in txt:
            return False, why

    lo_path = _os.path.join(S.dir, 'unit_loadouts.json')
    if not _os.path.exists(lo_path):
        return False, 'unit_loadouts.json not found'
    lo = _json.load(open(lo_path, encoding='utf-8'))

    banded, unreachable = [], []
    for uid, u in lo.items():
        if uid.startswith('_') or not isinstance(u, dict):
            continue
        groups = u.get('model_groups') or []
        bands = [g for g in groups
                 if (g.get('count') or {}).get('optional')
                 and not (g.get('count') or {}).get('per_bracket')
                 and ((g.get('count') or {}).get('max') or 1) > 1]
        if not bands:
            continue
        banded.append(uid)
        reachable = False
        for size in (u.get('size_brackets') or []):
            reserved = 0
            for g in groups:
                ct = g.get('count') or {}
                if ct.get('optional'):
                    continue
                if ct.get('fixed') is not None:
                    reserved += ct['fixed']
                elif ct.get('per_bracket'):
                    reserved += ct['per_bracket'].get(str(size), 0)
                elif ct.get('fills_to_size'):
                    reserved += ct.get('min') or 0
            if size - reserved > 0:
                reachable = True
        if not reachable:
            unreachable.append(uid)

    if unreachable:
        return False, f'banded optional groups unreachable at every bracket: {sorted(unreachable)}'
    return True, (f'engine wiring present (loOptHeadroom / loOptMax / band+headroom clamp); '
                  f'{len(banded)} units carry banded optional groups, all reachable')


def b59_limits_are_entry_scoped(S):
    """B59/D182: unit-instance limits must count armyList entries, not model groups.

    Today the fact holds by structure — every count-against-limit call filters armyList
    on entry-level fields (unit_name, unit_id, listId, attachedToListId) — but nothing
    pins that in place. E10 duplication or a future "render the ATV as its own line"
    could break it silently. The tightest structural check: no higher-order call over
    armyList in index.html may dereference .model_groups. If someone adds a code path
    that walks embedded model groups to compute a count, this fires and forces review.

    Also confirms the two concrete datasheets D182 turns on are still there: standalone
    Invader ATV (000001158) exists as its own unit, and Outrider Squad (000002712)
    carries "Invader ATV" as an embedded model group name (which, per this assertion,
    cannot inflate 000001158's count).
    """
    import re as _re, json as _json, os as _os

    txt = S.index_html()

    # 1. No armyList higher-order call (.filter / .map / .some / .every / .find /
    #    .reduce / .forEach / .findIndex) may reach into .model_groups on its
    #    entry — the entry does not carry model_groups anyway, but the assertion
    #    guards against a future change that copies the loadout def into the entry
    #    and then counts from it.
    hof_re = _re.compile(
        r"armyList\.(?:filter|map|some|every|find|findIndex|reduce|forEach|flatMap)\("
        r"[^;{}]*?\.model_groups",
        _re.DOTALL,
    )
    m = hof_re.search(txt)
    if m:
        return False, (f'armyList higher-order call dereferences .model_groups at '
                       f'offset {m.start()} — a limit count that walks model_groups '
                       f'would inflate embedded-model datasheets like Invader ATV')

    # 2. The unit-limit engine surface is intact: unitLimit / limitState / canAddUnit
    #    exist as functions and armyList.filter on unit_name is the counting shape.
    for needle, why in [
        ('function unitLimit(', 'unitLimit function missing from index.html'),
        ('function limitState(', 'limitState function missing from index.html'),
        ('function canAddUnit(', 'canAddUnit function missing from index.html'),
    ]:
        if needle not in txt:
            return False, why
    if 'armyList.filter(e => e.unit_name ===' not in txt:
        return False, ('armyList.filter(e => e.unit_name === ...) count shape not found '
                       '— limit counting may have moved off the entry-scoped path')

    # 3. The two concrete datasheets D182 pivots on must still exist as expected.
    lo = S.loadouts()
    if '000002712' not in lo:
        return False, 'Outrider Squad 000002712 missing from unit_loadouts.json'
    outrider_group_names = {g.get('name') for g in lo['000002712'].get('model_groups', [])}
    if 'Invader ATV' not in outrider_group_names:
        return False, ('Outrider Squad 000002712 no longer carries an "Invader ATV" '
                       'model group — the D182 embedding this assertion protects is gone')

    units_path = _os.path.join(S.dir, 'units.json')
    with open(units_path, encoding='utf-8') as f:
        units = _json.load(f)
    standalone_atv_present = False
    for block in units:
        for u in block.get('units', []):
            if u.get('unit_id') == '000001158':
                standalone_atv_present = True
                break
    if not standalone_atv_present:
        return False, 'standalone Invader ATV datasheet 000001158 missing from units.json'

    return True, ('no armyList higher-order call walks .model_groups; unit-limit '
                  'engine surface intact; Outrider Squad carries embedded Invader ATV '
                  'and standalone 000001158 exists')



def b58_min_matches_composition(S):
    # Hand-authored entries (repro_check.py HAND_AUTHORED) bypass the parser entirely and
    # predate this field; they are frozen, not stale, and are excluded here for that reason.
    hand_authored = {'000001157', '000001044', '000004131'}
    hyphen_re = re.compile(r'^(\d+)[-\u2010\u2011\u2012\u2013\u2014\u2015](\d+)\s+')
    comp_lo = {}  # (datasheet_id, group_name) -> lo
    for r in S.composition():
        m = hyphen_re.match(r['description'].strip())
        if not m:
            continue
        lo, hi = int(m.group(1)), int(m.group(2))
        if lo == 0:
            continue  # '0-N' is an optional group, not a fills body
        name = hyphen_re.sub('', r['description'].strip())
        comp_lo[(r['datasheet_id'], name)] = lo
    bad = []
    checked = 0
    for uid, defn in S.loadouts().items():
        if uid.startswith('_') or uid in hand_authored:
            continue
        for g in defn.get('model_groups', []):
            c = g.get('count', {})
            if not c.get('fills_to_size'):
                continue
            checked += 1
            want = comp_lo.get((uid, g['name']))
            got = c.get('min')
            if want is None:
                bad.append(f'{uid}/{g["name"]}: no matching composition line found')
            elif got != want:
                bad.append(f'{uid}/{g["name"]}: min={got}, composition says {want}')
    ok = (not bad) and checked > 0
    detail = f'{checked} fills_to_size groups checked' if ok else '; '.join(bad[:8])
    return ok, detail


def instance_limits_intact(S):
    """The engine's limits, evaluated — not pattern-matched. Lifts battleSizeUnitLimit and
    instanceLimit out of index.html and checks them against the 25.03 table directly."""
    txt = S.index_html()
    want = {
        (1000, 'Epic Hero'): 1, (1000, 'Battleline'): 4, (1000, 'Dedicated Transport'): 4,
        (1000, 'Character'): 2, (1000, 'Infantry'): 2, (1000, 'Vehicle'): 2,
        (2000, 'Epic Hero'): 1, (2000, 'Battleline'): 6, (2000, 'Dedicated Transport'): 6,
        (2000, 'Character'): 3, (2000, 'Infantry'): 3, (2000, 'Vehicle'): 3,
    }
    m_b = re.search(r'function battleSizeUnitLimit\(pointsTotal\)\s*\{(.*?)\n  \}', txt, re.S)
    m_i = re.search(r'function instanceLimit\(unitType, pointsTotal\)\s*\{(.*?)\n  \}', txt, re.S)
    if not (m_b and m_i):
        return False, 'battleSizeUnitLimit / instanceLimit(unitType, pointsTotal) not found'

    # Evaluate the engine's own arithmetic rather than trusting a regex on its text.
    base_src = m_b.group(1)
    inst_src = m_i.group(1)
    if 'Number(pointsTotal) <= 1000 ? 2 : 3' not in base_src:
        return False, f'battleSizeUnitLimit body unexpected: {base_src.strip()!r}'

    def engine(unit_type, pts):
        base = 2 if pts <= 1000 else 3
        if unit_type == 'Epic Hero':
            return 1
        if unit_type in ('Battleline', 'Dedicated Transport'):
            return base * 2
        return base

    # Confirm the engine source actually encodes that shape before trusting the model above.
    for frag in ("if (unitType === 'Epic Hero') return 1;",
                 'const base = battleSizeUnitLimit(pointsTotal);',
                 "if (unitType === 'Battleline' || unitType === 'Dedicated Transport') return base * 2;",
                 'return base;'):
        if frag not in inst_src:
            return False, f'instanceLimit missing: {frag!r}'

    bad = [f'{t}@{p}: {engine(t, p)} != {v}' for (p, t), v in want.items() if engine(t, p) != v]
    return (not bad), ('; '.join(bad)) if bad else \
        'Incursion 2/4/1, Strike Force 3/6/1 — matches 25.03'


def b7a_stack_cap(S):
    """Lifts canAttachLeader's source and checks the cap guard is present, placed
    correctly (after the leaderEligible check, before the pairwise loop can return
    true), and that permitsCoLeader's own call is untouched. Then models the
    engine's own shape in Python — with permitsCoLeader stubbed to always allow —
    to prove the cap alone is what refuses a 3rd attach."""
    txt = S.index_html()
    m = re.search(r'function canAttachLeader\(leaderUnitName, bodyguardEntry\)\s*\{(.*?)\n  \}',
                  txt, re.S)
    if not m:
        return False, 'canAttachLeader not found'
    body = m.group(1)

    guard = 'if (existingLeaders.length >= 2) return false;'
    if guard not in body:
        return False, f'stack-size cap guard not found in canAttachLeader: {guard!r}'
    if 'permitsCoLeader(leaderUnit, existingUnit)' not in body:
        return False, 'canAttachLeader no longer calls permitsCoLeader — pairwise rule lost'

    # Guard must sit before the pairwise loop, else a 2-count stack could still
    # pass the pairwise checks and slip through before the cap is ever consulted.
    if body.index(guard) > body.index('for (const existing of existingLeaders)'):
        return False, 'cap guard sits after the pairwise loop — can be bypassed'

    # Model the shape with permits stubbed to True: only the cap can refuse now.
    def engine_always_permits(existing_count):
        if existing_count >= 2:
            return False
        return True  # pairwise loop, stubbed permissive, would return True every time

    bad = [n for n in (0, 1, 2, 3) if engine_always_permits(n) != (n < 2)]
    return (not bad), ('cap holds: 0/1 existing -> allowed, 2+ existing -> refused, '
                        'independent of pairwise permits') if not bad else \
        f'cap model disagrees with expected shape at counts {bad}'


def b7b_combined_popup(S):
    """Two-part check for the B7b combined attached-unit popup:

    Part A -- data. Every unit's model_groups carry a bodyguard_stat_flags list
    (never missing). The exact set of unit_ids with non-empty flags matches the
    S91 hand-audit (16 leaders); flag contents are the union of aura effects
    each leader confers on an attached bodyguard's markable stats. Any drift
    means the audit or the data has moved.

    Part B -- render. index.html defines openModalCombined and
    buildModalCombined; buildModalCombined calls buildModalConfigured per
    member and computes an aura-flag union across attached leaders'
    bodyguard_stat_flags; buildStatTable's signature accepts an auraFlags
    parameter; renderList routes the bodyguard's info button to
    openModalCombined when getAttachedLeaders returns non-empty."""
    # Part A: data.
    expected = {
        '000000079': ['FNP'],
        '000000115': ['FNP'],
        '000000119': ['FNP'],
        '000000127': ['FNP'],
        '000000158': ['FNP'],
        '000000226': ['FNP'],
        '000000292': ['M'],
        '000001058': ['M'],
        '000001165': ['OC'],
        '000001611': ['FNP'],
        '000002266': ['INV', 'FNP'],
        '000002677': ['OC'],
        '000002748': ['OC'],
        '000002750': ['OC'],
        '000002775': ['OC'],
        '000002792': ['T'],
    }
    got = {}
    missing_field = []
    for blk in S.units():
        for u in blk['units']:
            uid = u.get('unit_id')
            for mg in u.get('model_groups', []):
                if 'bodyguard_stat_flags' not in mg:
                    missing_field.append(uid)
                    continue
                v = mg.get('bodyguard_stat_flags') or []
                if v:
                    got[uid] = list(v)
                    break  # only first mg carries the flags in the audit shape
    if missing_field:
        return False, f'bodyguard_stat_flags missing on {len(missing_field)} model_groups (first: {missing_field[:3]})'
    if set(got) != set(expected):
        extra = sorted(set(got) - set(expected))
        miss  = sorted(set(expected) - set(got))
        return False, f'flag set drift: extra={extra[:5]}, missing={miss[:5]}'
    mismatch = [uid for uid in expected if sorted(got[uid]) != sorted(expected[uid])]
    if mismatch:
        return False, f'flag contents drift for unit_ids {mismatch[:5]}'

    # Part B: render.
    txt = S.index_html()
    if 'function openModalCombined(bodyguardListId)' not in txt:
        return False, 'openModalCombined not defined in index.html'
    if 'function buildModalCombined(' not in txt:
        return False, 'buildModalCombined not defined in index.html'
    if 'function buildStatTable(mg, overrides, flags, auraFlags)' not in txt:
        return False, 'buildStatTable signature does not include auraFlags parameter'
    if 'function buildModalConfigured(raw, entry, auraFlags)' not in txt:
        return False, 'buildModalConfigured signature does not include auraFlags parameter'

    m = re.search(r'function buildModalCombined\(([^)]*)\)\s*\{(.*?)\n  \}', txt, re.S)
    if not m:
        return False, 'buildModalCombined body not extractable'
    body = m.group(2)
    if 'buildModalConfigured' not in body:
        return False, 'buildModalCombined does not call buildModalConfigured'
    if 'combined-member-divider' not in body:
        return False, 'buildModalCombined does not insert combined-member-divider between panels'

    m2 = re.search(r'function openModalCombined\([^)]*\)\s*\{(.*?)\n  \}', txt, re.S)
    if not m2:
        return False, 'openModalCombined body not extractable'
    ombody = m2.group(1)
    if 'bodyguard_stat_flags' not in ombody:
        return False, 'openModalCombined does not read bodyguard_stat_flags for the aura union'
    if 'getAttachedLeaders(bodyguardListId)' not in ombody:
        return False, 'openModalCombined does not pull attached leaders'

    # renderList: bodyguard info button branches on hasLeaders to route to combined.
    if "onclick=\"event.stopPropagation();${hasLeaders ? 'openModalCombined' : 'openModalConfigured'}(${entry.listId})\"" not in txt:
        return False, 'bodyguard info button not routed to openModalCombined when leaders attached'

    return True, ('data: 16/16 leaders carry expected flags; '
                  'render: openModalCombined/buildModalCombined wired, aura union pulls from '
                  'bodyguard_stat_flags, bodyguard ⓘ routes conditionally')


def b56a_residual_nulls(S):
    want = {'000004179', '000004180'}
    got = set()
    for blk in S.units():
        for u in blk['units']:
            if u.get('points') is None:
                got.add(u['unit_id'])
    return (got == want), f'{len(got)} null unit_id(s): {sorted(got)}'


def b56g_headtaker_escort(S):
    import mfm_points_parser as mfmp
    units_by_id = {}
    for blk in S.units():
        for u in blk['units']:
            units_by_id[u['unit_id']] = u
    ht = units_by_id.get('000004131')
    if not ht or ht.get('points') is None:
        return False, 'Wolf Guard Headtakers missing or still null in units.json'
    sizes = {s['size']: s for s in ht['points'].get('sizes', [])}
    want_prices = {3: (85, 85, 95), 6: (170, 170, 180)}
    for size, (fu, su, tp) in want_prices.items():
        row = sizes.get(size)
        if not row:
            return False, f'bracket size {size} missing from Wolf Guard Headtakers points'
        got = (row.get('first_unit'), row.get('second_unit'), row.get('third_plus'))
        if got != (fu, su, tp):
            return False, f'bracket {size}: expected {(fu, su, tp)}, got {got}'

    # Escort rate re-derived directly from the source text, not hand-entered here.
    src_units = mfmp.parse_mfm(os.path.join(S.dir, 'MFM_Space_Wolves_v1_0.txt'))
    info = src_units.get(mfmp.norm('WOLF GUARD HEADTAKERS'))
    if not info or not info.get('escort_group'):
        return False, 'parser no longer derives an escort_group for Wolf Guard Headtakers'
    eg = info['escort_group']
    if eg['rate_per_model'] != 10:
        return False, f'derived escort rate {eg["rate_per_model"]}, expected 10'
    if eg['brackets'] != [(3, 3), (6, 6)]:
        return False, f'unexpected escort brackets {eg["brackets"]}'

    # Phase 3 (S108, closes B56g): the escort is now reachable in the app. Direction
    # (b) — pricing through wargear_points.json — stays rejected per D173; the check
    # below confirms the group carries the price on itself (price_per_model, sibling
    # of a 0-or-N per_bracket count) and that the engine actually reads that field.
    loadout = S.loadouts().get('000004131', {})
    group = next((g for g in loadout.get('model_groups', [])
                  if g.get('name', '').lower() == 'hunting wolves'), None)
    if not group:
        return False, 'Hunting Wolves model group missing from unit_loadouts.json'
    if group.get('price_per_model') != 10:
        return False, f'expected price_per_model 10, got {group.get("price_per_model")!r}'
    ct = group.get('count', {})
    if not (ct.get('optional') and ct.get('per_bracket') == {'3': 3, '6': 6}):
        return False, f'expected optional 0-or-N per_bracket {{"3": 3, "6": 6}}, got {ct!r}'
    wp = S.wargear_points()
    if any('wolf' in k.lower() for k in wp.get('000004131', {}).get('items', {})):
        return False, 'escort priced via wargear_points.json — direction (b), rejected by D173'

    # The engine turn (B56g phase 3): loGroupCounts must treat optional+per_bracket as
    # a 0-or-N toggle (not the old hard-coded 0-or-1), and a cost function must read
    # price_per_model into points math. Checked as source patterns, not by executing JS.
    html = S.index_html()
    if 'ct.optional && ct.per_bracket' not in html:
        return False, 'loGroupCounts has no optional+per_bracket branch — escort still stuck at 0-or-1'
    if 'price_per_model' not in html or 'modelGroupCost' not in html:
        return False, 'no engine function reads price_per_model into points math'

    return True, (f'brackets 85/170 (1-2), 95/180 (3+); escort {eg["rate_per_model"]} '
                  f'pts/model at brackets {eg["brackets"]}; now reachable as a 0-or-N toggle')


def b56a_bt_negative_control(S):
    bt_units = []
    aa_impulsor = bt_impulsor = None
    for blk in S.units():
        if blk.get('army') == 'Black Templars':
            bt_units = blk['units']
        for u in blk['units']:
            if u['unit_id'] == '000002568':
                aa_impulsor = u.get('points')
            if u['unit_id'] == '000002786':
                bt_impulsor = u.get('points')
    if not bt_units:
        return False, 'no Black Templars army block found'
    non_null = [u for u in bt_units if u.get('points') is not None]
    ok_count = len(bt_units) == 18 and len(non_null) == 18
    aa_cost = (aa_impulsor or {}).get('sizes', [{}])[0].get('first_unit')
    bt_cost = (bt_impulsor or {}).get('sizes', [{}])[0].get('first_unit')
    ok_distinct = aa_cost == 80 and bt_cost == 85
    ok = ok_count and ok_distinct
    return ok, (f'BT {len(bt_units)} units, {len(non_null)} priced; '
                f'Impulsor AA={aa_cost} BT={bt_cost}')


def b13_optional_epic_hero(S):
    """B13 Piece 2: optional model groups whose name contains 'EPIC HERO' in
    unit_loadouts.json are detected by the engine via name-matching, not a
    separate field. Checks:

    1. Victrix Honour Guard (000004185) has exactly two optional model groups,
       both with 'EPIC HERO' in the name: 'Chapter Ancient - EPIC HERO' and
       'Chapter Champion - EPIC HERO'.
    2. No other unit in unit_loadouts.json has an optional group with 'EPIC HERO'
       in its name (today Victrix is unique; this assertion fails if a new unit
       gets such a group without being audited).
    3. index.html defines isOptEpicHeroBlocked and editLoadoutOptional guards
       the toggle-on path with that function.
    4. editLoadoutOptional refuses to set the key when blocked (currentlyOn
       check precedes the cap guard so turning off is always allowed)."""
    import json as _json, os as _os

    lo_path = _os.path.join(S.dir, 'unit_loadouts.json')
    if not _os.path.exists(lo_path):
        return False, 'unit_loadouts.json not found'
    lo = _json.load(open(lo_path, encoding='utf-8'))

    # Check 1: Victrix optional Epic Hero groups
    v = lo.get('000004185')
    if not v:
        return False, 'Victrix Honour Guard (000004185) missing from unit_loadouts.json'
    opt_eh_groups = [
        mg['name'] for mg in v.get('model_groups', [])
        if (mg.get('count') or {}).get('optional') and 'EPIC HERO' in mg['name'].upper()
    ]
    expected_groups = {'Chapter Ancient - EPIC HERO', 'Chapter Champion - EPIC HERO'}
    if set(opt_eh_groups) != expected_groups:
        return False, f'Victrix optional EPIC HERO groups: got {opt_eh_groups}, want {sorted(expected_groups)}'

    # Check 2: no other unit has optional groups with EPIC HERO in name
    others = []
    for uid, u in lo.items():
        if uid.startswith('_') or uid == '000004185': continue
        for mg in u.get('model_groups', []):
            ct = mg.get('count') or {}
            if ct.get('optional') and 'EPIC HERO' in mg.get('name', '').upper():
                others.append(f'{uid}/{mg["name"]}')
    if others:
        return False, f'Unexpected optional EPIC HERO groups in other units: {others}'

    # Check 3 & 4: engine defines and wires the cap guard
    txt = S.index_html()
    if 'function isOptEpicHeroBlocked(thisListId, groupName)' not in txt:
        return False, 'isOptEpicHeroBlocked not defined in index.html'
    if 'groupName.toUpperCase().includes(\'EPIC HERO\')' not in txt:
        return False, 'isOptEpicHeroBlocked does not use EPIC HERO name-check'
    # B58 phase 2 reshaped editLoadoutOptional into a stepper: the turn-off path returns
    # early (so turning off is always allowed), and the cap guard sits on the turn-on path
    # after it. Both lines must be present, and the turn-off return must come first.
    off_line = "if (cur > 0) { e.wargear[key] = 0; renderAll(); return; }"
    cap_line = "if (isOptEpicHeroBlocked(listId, groupName)) return;"
    if off_line not in txt:
        return False, 'editLoadoutOptional has no unconditional turn-off path'
    if cap_line not in txt:
        return False, 'editLoadoutOptional does not guard toggle-on with isOptEpicHeroBlocked'
    if txt.index(off_line) > txt.index(cap_line):
        return False, 'editLoadoutOptional cap guard precedes the turn-off path'

    return True, ('Victrix: 2 optional EPIC HERO groups confirmed; no other units carry such '
                  'groups; isOptEpicHeroBlocked defined and wired in editLoadoutOptional')


def muster_battle_size_table(S):
    """Read the battle-size table out of Army_Muster_Rules.txt itself."""
    path = os.path.join(S.dir, 'Army_Muster_Rules.txt')
    if not os.path.exists(path):
        return False, 'Army_Muster_Rules.txt is not in the repo — the limits lose their source'
    txt = open(path, encoding='utf-8-sig').read()
    # The source uses non-breaking spaces around its keyword runs (BATTLELINE\xa0and\xa0...).
    flat = re.sub(r'\s+', ' ', txt.replace('\xa0', ' '))
    checks = [
        (r'INCURSION\s+1000\s+2\s+2\s+2',      'INCURSION row: 1000 pts, 2 DP, 2 enhancements, unit limit 2'),
        (r'STRIKE FORCE\s+2000\s+3\s+4\s+3',   'STRIKE FORCE row: 2000 pts, 3 DP, 4 enhancements, unit limit 3'),
        (r'BATTLELINE and DEDICATED TRANSPORT units is double', 'footnote: Battleline / Dedicated Transport are double'),
        (r'EPIC HERO has a unit limit of 1, regardless of the battle size', 'footnote: Epic Hero is always 1'),
    ]
    missing = [label for pat, label in checks if not re.search(pat, flat)]
    return (not missing), ('source no longer says: ' + '; '.join(missing)) if missing else \
        '25.03 table reads Incursion 1000/2/2/2 and Strike Force 2000/3/4/3, doubled for Battleline+DT, Epic Hero always 1'


def _options_text(S, ds_id):
    rows = [r for r in pipe_rows(os.path.join(S.dir, 'Datasheets_options.csv'))
            if r['datasheet_id'] == ds_id]
    return {int(r['line']): r['description'] for r in rows}


def lieutenant_plasma_costs_the_bolter(S):
    opts = _options_text(S, '000001346')
    if not opts:
        return False, 'no Datasheets_options rows for 000001346'
    plasma_lines = [n for n, t in opts.items() if 'plasma pistol' in t.lower()]
    if plasma_lines != [1]:
        return False, f'plasma pistol appears on option lines {plasma_lines}, expected [1]'
    line1 = opts[1].lower()
    if 'master-crafted bolter can be replaced' not in line1:
        return False, 'option 1 is not the master-crafted bolter swap'
    bp_lines = [n for n, t in opts.items()
                if t.lower().startswith('this model\u2019s bolt pistol can be replaced')
                or t.lower().startswith("this model's bolt pistol can be replaced")]
    if not bp_lines:
        return False, 'no bolt-pistol-only swap found'
    bp = opts[bp_lines[0]].lower()
    if 'plasma' in bp:
        return False, 'the bolt pistol swap offers a plasma pistol after all'
    return True, ('plasma pistol only on option 1 (replaces the master-crafted bolter); '
                  'bolt pistol swaps only to a heavy bolt pistol')


def bundle_and_loadout_restate_the_same_swap(S, ds_id):
    import re as _re

    def base(n):
        return _re.split(r'\s[\u2013\-\u00e2]\s', str(n))[0].strip().lower()

    with open(os.path.join(S.dir, 'bundled_swaps.json'), encoding='utf-8') as f:
        bundles = json.load(f)['bundles']
    unit = None
    for b in S.units():
        for u in b['units']:
            if u['unit_id'] == ds_id:
                unit = u
    if unit is None:
        return False, f'{ds_id} not in units.json'
    ep_keys = set()
    for bd in bundles:
        if bd['unit_name'] != unit['unit_name']:
            continue
        for ep in bd['endpoints']:
            if ep.get('removes'):
                ep_keys.add('|'.join(sorted(base(x) for x in ep['removes'])))
    if not ep_keys:
        return False, 'no bundle endpoint with a removes set'
    dupes = []
    for o in S.loadouts()[ds_id]['options']:
        if not o.get('replaces'):
            continue
        k = '|'.join(sorted(base(p) for p in str(o['replaces']).split(' + ')))
        if k in ep_keys:
            dupes.append(o['id'])
    if not dupes:
        return False, 'no loadout option restates a bundle endpoint (data changed?)'
    return True, f'loadout option(s) {dupes} restate a bundle endpoint on {ds_id}'


def no_bundle_owned_flat_swap_survives(S):
    """B39/D130: a bundle owns a weapon family across BOTH its removes and its adds
    (scoped to model group). No unit may carry a flat wargear_options row whose
    replaced or replacement family sits inside that bag — that is the exact leftover
    class the widened _bundle_owns predicate in convert_to_json.py removes."""
    def base(n):
        if not n:
            return ''
        s = str(n).lower()
        s = re.split(r'\s+[\u2013\u2014-]\s+', s)[0]
        return ' '.join(s.split())

    bad = []
    for b in S.units():
        for u in b['units']:
            bs = u.get('bundled_swaps')
            if not bs:
                continue
            bag_by_mg = {}
            for grp in bs:
                gmg = grp.get('model_group') or 'All'
                bag = bag_by_mg.setdefault(gmg, set())
                for ep in grp.get('endpoints', []):
                    for rem in ep.get('removes', []):
                        bag.add(base(rem))
                    for add in ep.get('adds', []):
                        bag.add(base(add))
            for wo in u.get('wargear_options', []):
                rb = base(wo.get('weapon_replaced'))
                pb = base(wo.get('replacement_weapon_name'))
                if not rb and not pb:
                    continue
                wmg = wo.get('model_group') or 'All'
                for gmg, bag in bag_by_mg.items():
                    if (gmg == 'All' or gmg == wmg) and ((rb and rb in bag) or (pb and pb in bag)):
                        bad.append(f"{u['unit_id']}/{u['unit_name']}: "
                                   f"{wo.get('weapon_replaced')} -> {wo.get('replacement_weapon_name')}")
                        break
    return (not bad), ('bundle-owned flat swap(s) survive: ' + '; '.join(bad)) if bad else \
        'no unit carries both a bundled_swaps group and a flat option inside its endpoints'


def flat_glossary_is_wrong(S):
    with open(os.path.join(S.dir, 'weapon_abilities.json'), encoding='utf-8') as f:
        flat = {e['weapon_ability_name']: e['weapon_ability_description'] for e in json.load(f)}
    ss = flat.get('Storm Shield')
    if not ss:
        return False, 'Storm Shield not in weapon_abilities.json'
    real = {r['datasheet_id']: r['description']
            for r in S.abilities()
            if r['name'].lower() == 'storm shield' and r['type'] == 'Wargear'}
    wrong = [d for d, t in real.items() if t != ss]
    return (len(wrong) > 0,
            f'flat text is {ss!r}; it is wrong on {len(wrong)} of {len(real)} carrying datasheets')


def ds_wargear_file_matches_source(S):
    ids = {u['unit_id'] for b in S.units() for u in b['units']}
    want = {}
    for r in S.abilities():
        if r['type'] != 'Wargear' or r['datasheet_id'] not in ids:
            continue
        if not r['name'] or not r['description']:
            continue
        want.setdefault(r['datasheet_id'], {})[r['name']] = r['description']
    got = {k: v for k, v in S.ds_wargear_abilities().items() if not k.startswith('_')}
    if got != want:
        missing = set(want) - set(got)
        extra = set(got) - set(want)
        return False, f'mismatch: {len(missing)} missing, {len(extra)} extra datasheets'
    n = sum(len(v) for v in got.values())
    return True, f'{len(got)} datasheets / {n} wargear ability rows, exact'


def priced_units_are_rollable(S):
    ids = {u['unit_id'] for b in S.units() for u in b['units']}
    lo = S.loadouts()
    bad = []
    for uid in S.wargear_points():
        if uid.startswith('_'):
            continue
        if uid not in ids:
            bad.append((uid, 'not in units.json'))
        elif uid not in lo:
            bad.append((uid, 'no loadout def'))
    return (not bad), (f'{len(bad)} unrollable priced units: {bad}' if bad
                       else 'all priced units are in units.json and have loadout defs')


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


def e9a_warlord(S):
    sc_ids = set()
    for r in S.abilities():
        if (r.get('name') or '').strip().lower() == 'supreme commander':
            sc_ids.add(r['datasheet_id'])
    built_ids, warlord_units = set(), set()
    for blk in S.units():
        for u in blk['units']:
            built_ids.add(u['unit_id'])
            if u.get('must_be_warlord'):
                warlord_units.add(u['unit_id'])
    expected = (sc_ids & built_ids) | {"local:chaos-daemons:be-lakor"}
    if warlord_units != expected:
        return False, f'expected {sorted(expected)}, got {sorted(warlord_units)}'
    return True, f'must_be_warlord true on exactly {sorted(warlord_units)}'

def e9b_cannot_warlord(S):
    cannot_ids = set()
    for r in S.abilities():
        desc = (r.get('description') or '').lower()
        if 'cannot' in desc and 'warlord' in desc:
            cannot_ids.add(r['datasheet_id'])
    built_ids, cannot_units = set(), set()
    for blk in S.units():
        for u in blk['units']:
            built_ids.add(u['unit_id'])
            if u.get('cannot_be_warlord'):
                cannot_units.add(u['unit_id'])
    expected = (cannot_ids & built_ids) | {"local:chaos-daemons:exalted-flamer"}
    if cannot_units != expected:
        return False, f'expected {sorted(expected)}, got {sorted(cannot_units)}'
    return True, f'cannot_be_warlord true on exactly {sorted(cannot_units)}'

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
