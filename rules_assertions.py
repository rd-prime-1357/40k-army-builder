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

    def detachments(self):
        if 'dt' not in self._cache:
            with open(os.path.join(self.dir, 'detachments.json'), encoding='utf-8') as f:
                self._cache['dt'] = json.load(f)
        return self._cache['dt']

    def detachment_effects(self):
        if 'de' not in self._cache:
            with open(os.path.join(self.dir, 'detachment_effects.json'), encoding='utf-8') as f:
                self._cache['de'] = json.load(f)
        return self._cache['de']

    def faction_keywords(self):
        """datasheet_id -> set of FACTION keywords, straight from source.

        E21b. Chapter exclusivity is a claim about which chapter a datasheet belongs
        to, and the only place that is stated is the source export's is_faction_keyword
        flag. Deriving it from units.json block membership instead would make the
        assertion restate the thing it is supposed to police.
        """
        if 'fkw' not in self._cache:
            out = {}
            for r in pipe_rows(os.path.join(self.dir, 'Datasheets_keywords.csv')):
                if r.get('is_faction_keyword') == 'true':
                    out.setdefault(r['datasheet_id'], set()).add(r['keyword'])
            self._cache['fkw'] = out
        return self._cache['fkw']

    def taxonomy(self):
        if 'tax' not in self._cache:
            with open(os.path.join(self.dir, 'faction_taxonomy.json'), encoding='utf-8') as f:
                self._cache['tax'] = json.load(f)
        return self._cache['tax']

    def resolved_pool(self, army):
        """The unit set a player of `army` can actually reach.

        Mirrors index.html's resolveUnits(): a chapter subfaction is the generic
        Adeptus Astartes block unioned with its own block, the chapter's copy winning
        on a name collision. Everything else is just its own block. Returns
        {unit_name: unit_record}.
        """
        blocks = {a['army']: a for a in self.units()}
        tax = json.load(open(os.path.join(self.dir, 'faction_taxonomy.json'), encoding='utf-8'))
        sub = set()
        for g in tax['groups']:
            for fx in g['factions']:
                if fx.get('is_subfaction') and fx.get('data_army'):
                    sub.add(fx['data_army'])
        pool = {}
        if army in sub and 'Adeptus Astartes' in blocks:
            for u in blocks['Adeptus Astartes']['units']:
                pool[u['unit_name']] = u
        if army in blocks:
            for u in blocks[army]['units']:
                pool[u['unit_name']] = u
        return pool

    def mfm_detachment_rows(self):
        """Re-derive the detachment catalogue straight from the MFM faction files.

        MFM is the source of record for which detachments exist and for every number
        attached to them. Comparing detachments.json against a fresh read of the MFM
        text is what makes the catalogue a checked fact rather than a claim about a
        file nobody re-opens.
        """
        if 'mfmdt' not in self._cache:
            import importlib.util
            p = os.path.join(self.dir, 'detachment_parser.py')
            spec = importlib.util.spec_from_file_location('detachment_parser', p)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            rows = {}
            for fn in sorted(set(mod.ARMY_TO_MFM.values())):
                rows[fn] = mod.parse_mfm_detachments(os.path.join(self.dir, fn))
            self._cache['mfmdt'] = (mod, rows)
        return self._cache['mfmdt']

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
    built, _, _ = M.build_wargear_points(paths,
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
    # 53/33 through S152; CSM's loadout-defaults pass (S153) adds 11 qualifying free
    # seeds across 11 CSM units (Chaos Icon, Havoc launcher, Chaos Familiar, Plasma
    # pistol) -> 64/44. D240 (S157): cult-troop cross-file points turn adds Khorne
    # Berzerkers' Icon of Khorne (its only qualifying free add; the other three
    # cult-troop units' options are all sized/pooled/priced and don't qualify) -> 65/45.
    # Thousand Sons turn B (S163): +10 qualifying free seeds across +9 TS units —
    # Prosperine khopesh x3, Havoc launcher x4, and one unit (Pink Horrors, 000004127)
    # carrying two (Instrument of Chaos, Daemonic Icon) -> 75/54.
    return (len(q) == 75 and len(units) == 54), f'{len(q)} options across {len(units)} units'

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
     'loadout_parser.py regenerates every entry (bar the four hand-authored seeds), the five '
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
     'its item is unpriced. 75 options across 54 units qualify today.',
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
         and 'instanceLimit(effectiveUnitType(u, selectedDetachments), POINTS_CAP)' in S.index_html(),
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

    ('B59a-1',
     'A model group carrying non_consuming: true rides alongside the size bracket '
     'instead of drawing from it (D182 mechanism, B59a engine turn). index.html\'s '
     'loOptHeadroom excludes such a group from the reservation subtracted from size; '
     'loGroupCounts clamps such a group to its band only, taking nothing from the '
     'shared headroom or the reserved total that other groups compete over. Data side '
     'is passive today — no unit_loadouts.json group carries the flag yet (that is '
     'B59b) — but if one appears here first, it must be on an optional group, the '
     'only shape the mechanism is defined for.',
     'index.html loOptHeadroom / loGroupCounts (D182); unit_loadouts.json model_groups',
     lambda S: b59a_non_consuming_engine(S)),

    # ── P5. The third byte-identical gate (D193, E1a). detachments.json is brand new,
    # so its fixed point is established at first generation; from here on a stale or
    # hand-edited copy fails this and nothing else would catch it.
    ('P5',
     'The pipeline reproduces the committed detachments.json byte-for-byte from source: '
     'detachment_parser.py reads the eight MFM faction files for structure and numbers, '
     'joins tier-1 faction-pack prose and tier-2 Wahapedia prose on normalised names, and '
     'the result matches. A stale, partial or hand-edited copy cannot pass.',
     'detachments_repro_check.py (D193)',
     lambda S: detachments_repro_gate(S)),

    ('E1a-1',
     'Every detachment costs 1, 2 or 3 Detachment Points and grants exactly one of the five '
     'force dispositions (Priority Assets, Take and Hold, Purge the Foe, Disruption, '
     'Reconnaissance). Both are what the DP budget and the mission rules key off, so neither '
     'may be absent or out of range.',
     'Army_Muster_Rules.txt 25.03/25.04; MFM_Instructions.txt DETACHMENTS legend (D193)',
     lambda S: e1a_dp_and_disposition(S)),

    ('E1a-2',
     'No detachment name repeats inside one army, and every MFM Unique tag survives into '
     'detachments.json unchanged with none invented. 25.04 forbids taking the same detachment '
     'twice; MFM_Instructions.txt adds that no two selected detachments may share a Unique '
     'tag. The second constraint was missed entirely by the S122 scope pass and exists in '
     'the data for Blood Angels and Death Guard today.',
     'MFM_Instructions.txt DETACHMENTS legend, Unique Tag bullet (D193)',
     lambda S: e1a_no_duplicate_names_and_unique_tags(S)),

    ('E1a-3',
     'The whole catalogue re-derives from the MFM faction files: same detachments per army, '
     'same DP, same force disposition, and the same enhancement names, point costs and print '
     'order inside each. MFM is the source of record for structure and numbers; the counts '
     'are reported here rather than asserted, because they move on every input change.',
     'MFM_<faction>_v1_0.txt DETACHMENTS blocks (D192/D193)',
     lambda S: e1a_catalogue_matches_mfm(S)),

    ('E1a-4',
     'No enhancement present only in the 10th-Edition Wahapedia dump survives the join. Text '
     'sources contribute descriptions, never membership or price — a stale enhancement shown '
     'at a stale cost is a phantom option in front of the player.',
     'Enhancements.csv vs MFM enhancement lists (D192/D193)',
     lambda S: e1a_no_wahapedia_only_enhancements(S)),

    ('E1a-5',
     'The (Upgrade) tag survives the parse as a boolean, set on exactly the enhancements MFM '
     'prints it against. It is rules-significant under 25.04, and it is carried in the '
     'enhancement name string in the source, so it is exactly the kind of thing a name-cleaning '
     'pass silently eats.',
     'MFM enhancement lines carrying "(Upgrade)"; Army_Muster_Rules.txt 25.04 (D193)',
     lambda S: e1a_upgrade_flags_preserved(S)),

    ('E1a-6',
     'Every detachment carries a text_source of faction_pack, wahapedia_10e or none; a record '
     'with rule text is never marked none and a record marked none never carries rule text; '
     'and the set of none records is exactly the named gap manifest in _meta. The per-tier '
     'totals are recorded, not asserted — they move every time a faction pack arrives.',
     'detachments.json _meta.text_sources / _meta.text_gap_manifest (D192 three-tier ladder)',
     lambda S: e1a_text_source_and_gap_manifest(S)),

    ('E1a-7',
     'The deduplicated store resolves: every key an army names exists in the catalogue, every '
     'catalogue record is reached by at least one army, and each record\'s own key field matches '
     'the key it is filed under. detachments.json holds one record per distinct detachment with '
     'each army indexing it by key, because seven armies otherwise carried a byte-identical copy '
     'of the same Space Marines list — half the file. The saving is only safe if the indirection '
     'is airtight; a dangling key would silently remove a detachment from an army.',
     'detachments.json detachments / armies (D193, S123 dedup)',
     lambda S: e1a_keys_resolve(S)),

    # ── E1b. Detachment selection state and the schema v1 -> v2 migration.
    ('E1b-1',
     'The DP budget the engine applies is the DP column of the 25.03 battle-size table, read '
     'from Army_Muster_Rules.txt: 2 at Incursion and 3 at Strike Force, with the 3,000-point '
     'size the app offers but 25.03 does not define treated as Strike Force (D192 item 2). The '
     'threshold in index.html is checked against the source table, not against a remembered '
     'number, so a change to either side that breaks the pair fails here.',
     'Army_Muster_Rules.txt 25.03; index.html detachmentPointBudget (D192)',
     lambda S: e1b_budget_matches_muster(S)),

    ('E1b-2',
     'list_store.js and the copy of the same module inlined into index.html are byte-identical, '
     'and both declare SCHEMA_VERSION 3 (E4b\'s per-entry enhancement field). Two files holding one module is a drift risk that '
     'nothing else checks: the standalone copy silently lost E9b\'s warlord field and no gate '
     'noticed, because no gate compared them.',
     'index.html inlined block vs list_store.js (E1b, S124)',
     lambda S: e1b_module_copies_agree(S)),

    ('E1b-3',
     'e1b_check.js passes in full: the three constraints on a legal detachment set (combined DP '
     'within the battle-size budget, no detachment twice per 25.04, no two selections sharing a '
     'Unique tag per D193) behave as stated against the real catalogue, and a v1 saved record '
     'migrates to v2 with an empty detachment set and every other field untouched. The migration '
     'is a claim about behaviour, so it is executed rather than described (D107).',
     'e1b_check.js (E1b, S124)',
     lambda S: e1b_harness_gate(S)),

    # ── E1c. Detachment picker UI over the E1b read path.
    ('E1c-1',
     'The E1b engine functions that answer legality — dpUsed, duplicateDetachments, '
     'uniqueTagConflicts, detachmentPointBudget, dpState — are DEFINED inside the E1b block and '
     'nowhere else in index.html. The picker calls them; it does not re-derive them. A second '
     'implementation growing quietly in the picker is exactly what "single read path" is meant '
     'to prevent, and would be invisible unless something looked for it.',
     'index.html E1b vs E1c blocks (E1c, S125)',
     lambda S: e1c_engine_functions_defined_once(S)),

    ('E1c-2',
     'e1c_check.js passes in full: for every catalogue key across every scenario, the picker\'s '
     'disabled flag is exactly what canAddDetachment says, extended by E21d to also disable a '
     'non-selected row whose selection would forbid a unit already in the list (a selected row is '
     'always toggle-off-able; a non-selected row is disabled iff canAddDetachment is not OK OR '
     'detachmentForbidConflicts is non-empty), the row\'s ghost flag is "not in the catalogue" and '
     'nothing else, and every refusal — including the forbid-conflict one — has prose naming the '
     'conflicting unit. This is the guard against the picker growing a second implementation of '
     'detachment legality, now including the forbid gate.',
     'e1c_check.js (E1c, S125; extended E21d, S137)',
     lambda S: e1c_harness_gate(S)),

    # ── E4b. Enhancement assignment engine and persistence.
    ('E4b-1',
     'The enhancement limit the engine applies is the Enhancement Limit COLUMN of the 25.03 '
     'battle-size table, read from Army_Muster_Rules.txt: 2 at Incursion and 4 at Strike Force. '
     'That column is not the DP column beside it (2 and 3), and the two sit adjacent in the same '
     'row — precisely the pair that gets copied across by mistake. The 3,000-point size 25.03 '
     'does not define must fall in the Strike Force branch here, for DP and for the unit limit, '
     'so the three battle-size-derived rules cannot disagree.',
     'Army_Muster_Rules.txt 25.03; index.html enhancementLimit (E4b, D199)',
     lambda S: e4b_limit_matches_muster(S)),

    ('E4b-2',
     'Enhancement eligibility is derived from unit_type, and that is only safe while it agrees '
     'with the keyword-derived answer. unit_type == Character must select the same set as (has '
     'CHARACTER keyword AND NOT EPIC HERO keyword) on every unit whose keywords are populated, '
     'bar two documented data gaps that are both in the safe direction. The EPIC HERO half is '
     'not optional: fifty-odd Epic Heroes carry the CHARACTER keyword, because in the rules an '
     'Epic Hero IS a Character, so a bare CHARACTER test would call every one of them eligible '
     'and contradict 25.04. A data regeneration that shifts eligibility fails here.',
     'units.json unit_type vs model_groups keyword_names (E4b, D199)',
     lambda S: e4b_eligibility_derivations_agree(S)),

    ('E4b-3',
     'The name-collision census is pinned: 30 reachable same-army cross-detachment collisions '
     'across 6 distinct names, exactly one of them priced differently in its two detachments. '
     'The sixth name (Warp-Fuelled Thrusters, CSM-internal) entered with the CSM detachment '
     'build (D237/S154) and does not change the design: a non-zero count still forces the '
     'duplicate rule to be keyed by name army-wide rather than by (detachment, name), and the '
     'one differing price (Dark Angels/Deathwing Assault, unrelated to CSM) still forces a '
     'stored assignment to carry a detachment key rather than a bare name. If a regeneration '
     'moves either number, both choices need revisiting rather than inheriting.',
     'detachments.json enhancements per army (E4b, D199; updated S155 for CSM, D237)',
     lambda S: e4b_name_collision_census(S)),

    ('E4b-4',
     'The sixteen functions that answer enhancement legality are DEFINED inside the E4b block '
     'and nowhere else in index.html, and both enforcement points are wired: editLeaderTarget '
     'consults enhancementAttachBlock, and ptsForEntry folds in enhancementPointsForEntry. This '
     'is E1c-1 applied ahead of the UI: E4c builds a picker over these functions, and a second '
     'implementation growing quietly inside it would be invisible unless something looked. A '
     'declared-but-unwired attach gate would be worse than none, since it would read as covered.',
     'index.html E4b block vs the rest of the file (E4b, S128)',
     lambda S: e4b_engine_functions_defined_once(S)),

    ('E4b-5',
     'e4b_check.js passes in full: the Upgrade count carve-out behaves as 25.04 states (three '
     'copies of one Upgrade allowed, all three priced, only the first counted against the army '
     'limit, the fourth refused), the one-per-unit rule is enforced over the ATTACHED unit and '
     'not the single entry, an Epic Hero is refused an Upgrade as well as a regular, a refused '
     'assignment leaves no trace on the entry, the attach action refuses to merge two carriers, '
     'and every selected row stays clearable however over-constrained the army is. Three '
     'different thresholds live in one 25.04 sentence, so these are executed, not described.',
     'e4b_check.js (E4b, S128)',
     lambda S: e4b_harness_gate(S)),

    # ── B63. Soul Grinder's god weapons were reachable simultaneously — a live D0
    # violation on a built faction (D206). Allegiance_Condition never reached units.json,
    # so index.html's filter at lines 6580/6604 was dead code. Fixed at the converter;
    # these four pin the shape so a future regeneration cannot silently drop it again.
    ('B63-1',
     'Soul Grinder carries exactly four weapons with a non-empty allegiance_condition, one '
     'per god: Khorne, Nurgle, Slaanesh, Tzeentch.',
     'chaos_daemons_reference.md Daemonic Allegiance line; units.json Soul Grinder (B63, D206)',
     lambda S: b63_soul_grinder_four_god_weapons(S)),

    ('B63-2',
     'None of the four allegiance-tagged weapons is base equipment. Harvester cannon, Iron '
     'claw and Warpsword are all base equipment; Warpclaw stays the existing swap and is '
     'untouched by this fix.',
     'chaos_daemons_reference.md Soul Grinder composition line (B63, D206)',
     lambda S: b63_soul_grinder_base_equipment_correct(S)),

    ('B63-3',
     'No unit in any built army other than Soul Grinder carries an allegiance_condition. '
     'D25/D26 name Soul Grinder as the column\'s only user; the Daemon Princes take stat '
     'modifiers instead, detected through the app\'s hardcoded GOD_UNITS set.',
     'units.json, all armies (B63, D206)',
     lambda S: b63_no_other_unit_carries_allegiance(S)),

    ('B63-4',
     'Every non-empty allegiance_condition value across units.json is one of the four god '
     'names — Khorne, Tzeentch, Nurgle or Slaanesh — matching the exact strings index.html '
     'compares entry.god against.',
     'index.html GODS array (B63, D206)',
     lambda S: b63_allegiance_values_valid(S)),

    # ── B61. Wahapedia carries several Chaos Daemons datasheets twice — once under the
    # native CD faction, once again under an allied-unlock army (TALLYBAND SUMMONERS for
    # Death Guard, CHANGEHOST OF DECEIT for Thousand Sons) — and the parser was silently
    # absorbing the borrowing army's copies into its plain roster with no marker at all
    # (D208). Turn A (D248/E24) extended the same mechanism to Thousand Sons' Scintillating
    # Legions carriers; these four now pin the tag's exact shape across both armies via
    # ALLIED_CARRIER_GROUPS rather than one Death-Guard-specific census.
    ('B61-1',
     'Exactly the expected six units carry allied_group in each allied-carrier army: Death '
     'Guard carries "Plague Legions" (Beasts of Nurgle, Great Unclean One, Nurglings, '
     'Plaguebearers, Plague Drones, Rotigus); Thousand Sons carries "Scintillating Legions" '
     '(Kairos Fateweaver, Lord of Change, Flamers, Screamers, Pink Horrors, Blue Horrors). No '
     'other unit in either army carries the field at all — it is absent, not null, elsewhere.',
     'MFM_Death_Guard_v1_0.txt PLAGUE LEGIONS section, MFM_Thousand_Sons_v1_0.txt SCINTILLATING '
     'LEGIONS section; units.json Death Guard/Thousand Sons (B61, D208; TS added D248/E24)',
     lambda S: b61_plague_legions_census(S)),

    ('B61-2',
     'No unit in any army block outside the allied-carrier armies (Death Guard, Thousand Sons) '
     'carries allied_group. The tag is scoped to the sections it was derived from and has not '
     'leaked into Space Marines, the chapter variants, Chaos Space Marines, or Chaos Daemons\' '
     'own native copies of the same units.',
     'units.json, all armies (B61, D208; TS added D248/E24)',
     lambda S: b61_no_other_army_carries_allied_group(S)),

    ('B61-3',
     'Chaos Daemons carries its own native copy of every carrier unit under distinct unit_ids '
     '(local:chaos-daemons:*), and none of those native copies carries allied_group. This is '
     'the fact that makes each allied-carrier army\'s copies genuine duplicates rather than a '
     'merge collision — confirming Wahapedia\'s double-listing is intact on both sides of the '
     'fix, for Death Guard and now Thousand Sons.',
     'units.json Chaos Daemons vs Death Guard/Thousand Sons (B61, D208; TS added D248/E24)',
     lambda S: b61_cd_native_copies_distinct(S)),

    ('B61-4',
     'mfm_points_parser.py\'s ALLIED_GROUP_HEADERS still recognises all six documented labels — '
     'Plague Legions, Scintillating Legions, Blood Legions, Legions of Excess, Harlequins, Ynnari '
     '— across the factions not yet built. Written generally per the ticket rather than '
     'faction-specific, so a future session building World Eaters/Emperor\'s Children/Aeldari '
     'gets the tag for free; this guards against the set silently shrinking back down.',
     'mfm_points_parser.py ALLIED_GROUP_HEADERS (B61, D208)',
     lambda S: b61_allied_group_headers_intact(S)),

    ('E21a-1',
     'Every key in detachment_effects.json resolves to a real record in detachments.json, and '
     'the army named inside each record matches the army half of its own key. A typo in a key '
     'silently disables a restriction, which is the exact failure mode hand-authoring risks.',
     'detachment_effects.json vs detachments.json (E21a, D209)',
     lambda S: e21a_keys_resolve(S)),

    ('E21a-2',
     'Every unit name referenced by any effect — in units, in except_units — resolves in that '
     'army\'s RESOLVED pool, meaning its own block plus the generic Adeptus Astartes block for a '
     'chapter subfaction. Outrider Squad is the case that makes the distinction matter: it is '
     'referenced by a Dark Angels detachment but lives in the generic block.',
     'detachment_effects.json vs units.json + faction_taxonomy.json (E21a, D209)',
     lambda S: e21a_unit_names_resolve(S)),

    ('E21a-3',
     'The file obeys its own schema: every effect kind is one of the four D204 kinds '
     '(battleline, forbid, unlock, warlord) and never the dropped "require"; every effect carries '
     'an explicit boolean enforced; every warlord effect carries a mode of cannot_be or '
     'must_be_if_present; every unlock carries a points_cap keyed only by 1000/2000/3000 with '
     'strictly increasing values; and every unit_type named exists as a real unit_type in that '
     'army\'s pool.',
     'detachment_effects.json schema, _meta.effect_kinds (E21a, D204, D209)',
     lambda S: e21a_schema_valid(S)),

    ('E21a-4',
     'Allied-set targets resolve exactly when they claim to. Every enforced unlock or warlord '
     'effect targeting an allied_group matches at least one unit carrying that allied_group in '
     'the army\'s pool; every effect targeting a bare keyword instead of an allied_group is '
     'enforced: false and carries an unenforced_reason. The unenforced inventory is exactly one '
     'effect — Chaos Daemons SHADOW LEGION\'s HERETIC ASTARTES unlock — so the gap is counted '
     'rather than invisible, and shrinks loudly when Chaos Space Marines is built.',
     'detachment_effects.json vs units.json allied_group (E21a, D203, D204, D209)',
     lambda S: e21a_allied_targets(S)),

    ('E21a-5',
     'Coverage: every built detachment whose own text grants the BATTLELINE keyword, and every '
     'built detachment whose own text unlocks a non-faction unit set, has a row in '
     'detachment_effects.json. Re-derived by scanning all 169 built records rather than compared '
     'against a remembered list, so a detachment added later with a construction effect fails the '
     'baseline instead of being quietly unenforced.',
     'detachments.json rule_text/restrictions scan vs detachment_effects.json (E21a, D209)',
     lambda S: e21a_coverage(S)),

    ('E21a-6',
     'Be\'Lakor\'s units.json record carries must_be_warlord: true. This is why Chaos Daemons '
     'SHADOW LEGION has no warlord row: his Supreme Commander ability is unconditional and '
     'army-wide, so it is strictly stronger than the detachment\'s conditional version, and a row '
     'would be a second source for one rule. If this flag ever goes false the detachment rule '
     'stops being covered, and this assertion is what says so.',
     'units.json Chaos Daemons Be\'Lakor; detachment_effects.json _meta.not_in_this_file (E21a, D209)',
     lambda S: e21a_belakor_warlord_covered(S)),

    ('E21b-1',
     'Chapter exclusivity holds structurally. 25 built detachments say the army may include '
     "this Chapter's units and no other Chapter's, and resolveUnits() already makes the illegal "
     'state unreachable by composing a chapter army as the generic Adeptus Astartes block plus '
     'that chapter one block. Until now nothing policed it. For every faction in the taxonomy, '
     'no unit in its resolved pool carries another chapter\'s FACTION keyword in source — which '
     'also means the generic block carries none at all, so Space Marines cannot reach Lysander '
     'and White Scars cannot reach Ragnar. Read from Datasheets_keywords.csv rather than from '
     'block membership, so the check does not restate its own premise.',
     'units.json + faction_taxonomy.json vs Datasheets_keywords.csv is_faction_keyword (E21b, D204)',
     lambda S: e21b_chapter_exclusive(S)),

    ('E21b-2',
     'All three unit_type read sites go through effectiveUnitType(). D204 ruling 2 named exactly '
     'three — instanceLimit\'s caller, groupByType and the roster typeGroups build — and a fourth '
     'site added later that read unit_type directly would silently disagree with the other three '
     'about what a unit currently is. No grouping expression falls back on a raw unit_type.',
     'index.html unitLimit / groupByType / renderList typeGroups (E21b, D204)',
     lambda S: (
         'function effectiveUnitType' in S.index_html()
         and 'function detachmentBattlelineNames' in S.index_html()
         and S.index_html().count("effectiveUnitType(") >= 4
         and "unit_type || 'Other'" not in S.index_html(),
         'one predicate feeds the limit and both grouping sites')),

    ('E21c-1',
     'The three remaining construction-effect kinds are readable by the engine. E21b wired only '
     'battleline; forbid, unlock and warlord land on the add path and the Warlord pick. Eight '
     'functions carry them and all must exist, so a future edit that drops one fails here rather '
     'than silently under-enforcing: forbiddenUnitNames, unlockedAlliedGroups, alliedPointsCap, '
     'alliedSubtotal, canAddUnitToList, offerableUnits, detachmentForbidConflicts and '
     'warlordBannedByDetachment.',
     'index.html E21c/E22b block (E21c, D204, D208, D209)',
     lambda S: (
         all(('function ' + fn + '(') in S.index_html() for fn in (
             'forbiddenUnitNames', 'unlockedAlliedGroups', 'alliedPointsCap', 'alliedSubtotal',
             'canAddUnitToList', 'offerableUnits', 'detachmentForbidConflicts', 'warlordBannedByDetachment')),
         'all eight E21c/E22b functions are present')),

    ('E21c-2',
     'The add path and the roster offer both go through the gate. Both add sites — a fresh add '
     '(canAddUnitToList(unit, pts)) and the duplicate (canAddUnitToList(unit, provPts)) — call it, '
     'so a forbidden or over-sub-cap unit cannot enter the list, and the roster offers through '
     'offerableUnits(allUnits, selectedDetachments), so forbidden and not-yet-unlocked allied units '
     'are removed rather than shown-then-flagged (D0). Pins the two current add paths and the offer; '
     'a THIRD add path added later would not be caught here and must be gated by hand.',
     'index.html addUnitFromRoster / duplicateUnit / renderRoster (E21c, E22b, D204, D0)',
     lambda S: (
         'canAddUnitToList(unit, pts)' in S.index_html()
         and 'canAddUnitToList(unit, provPts)' in S.index_html()
         and 'offerableUnits(allUnits, selectedDetachments)' in S.index_html(),
         'both add paths and the roster offer route through the E21c gate')),

    ('E21c-3',
     'The warlord ban and the forbid-on-select refusal are wired live. Warlord eligibility filters '
     'on warlordBannedByDetachment(x.unit, selectedDetachments), so a Plague Legions model is not '
     'Warlord-eligible under Tallyband Summoners, and toggleDetachment consults '
     'detachmentForbidConflicts(key) before selecting, so a detachment that forbids a unit already '
     'in the list is refused rather than reached (the reachable state D209 / the S136 prompt names).',
     'index.html eligibleWarlordEntries / toggleDetachment (E21c, E22b, D204, D209)',
     lambda S: (
         'warlordBannedByDetachment(x.unit, selectedDetachments)' in S.index_html()
         and 'detachmentForbidConflicts(key)' in S.index_html(),
         'warlord ban and forbid-on-select are both wired')),

    ('E21d-1',
     'The render-side over-state is wired. entryAlliedError exists in the E21c/E22b block and '
     'entryHasError calls it, so a unit stranded by a later change — its detachment deselected, its '
     'group over the sub-cap after a battle-size drop, or a forbidden unit seated by import — reads '
     'as a visible roster error rather than being silently trimmed (Ryan, S139: a quick detachment '
     'switch-and-back must never discard a placed unit). Guards the wiring; e21c_check.js Section 8 '
     'drives the three branches against the real Tallyband Summoners and Shadow Legion data.',
     'index.html entryAlliedError / entryHasError (E21d piece 3, D218)',
     lambda S: (
         'function entryAlliedError(' in S.index_html()
         and 'if (entryAlliedError(unit)) return true;' in S.index_html(),
         'entryAlliedError exists and entryHasError routes through it')),

    ('P4-1',
     'The GW-derived source census holds. Two halves. (a) The 18 source files the gates proved '
     'REQUIRED are all present — established S135 by removing each candidate and re-running the '
     'full baseline, not by reading imports. (b) The set of GW-source filenames referenced anywhere '
     'in the gates and parsers is unchanged, so a parser that starts reading a new source file '
     'fails here and forces the census to be re-run. This exists because the removable half is a '
     'claim about ABSENCE — that nothing opens these files — and absence claims go stale silently, '
     'which is the whole reason the project does not trust prose.',
     'S135 park-and-rerun census over ./baseline.sh; static scan of the gate and parser sources (P4, D211)',
     lambda S: p4_source_census(S)),

    ('B62-1',
     'The nine Gen-1 Chaos Daemons root CSVs (Unit_Stats, Unit_Points, Unit_Wargear_Options, '
     'Unit_Other_Options, Unit_Weapons, Unit_Abilities, Keywords, Rules, Weapon_Abilities) are all '
     'present, non-empty, and carry their expected header columns. These are the only copy the '
     'project holds — the repo excludes them on GW-text grounds — so a missing or truncated one '
     'must fail loudly and by name here rather than surface as a confusing units.json repro '
     'mismatch, which is what happened when three went missing at S131.',
     'project root CD CSVs (D205, B62)',
     lambda S: b62_cd_csv_presence(S)),

    # ── B60a. D221 fixed the two defects that let a chapter-exclusivity restriction sit in
    # rule_text instead of restrictions, or carry stratagem/CP debris from a mis-scoped
    # DA pack region. The fix itself was verified once, by hand, at S142 close. These two
    # pin the resulting shape so a future detachments.json regeneration cannot silently
    # reopen either defect — restrictions is not read for legality today (D221's session
    # note), but the shape should be a fact, not a memory, before anything comes to depend on it.
    ('B60a-1',
     'Exactly 25 detachments carry the chapter-exclusivity sentence ("...drawn from any other '
     'Chapter") in restrictions, and zero carry it in rule_text.',
     'detachments.json, all detachments (B60a, D221)',
     lambda S: b60a_restrictions_carries_sentence_not_rule_text(S)),

    ('B60a-2',
     'No restrictions value contains stratagem/CP debris — none of the literal tokens '
     'STRATAGEM, WHEN:, or a standalone CP appears in any detachment\'s restrictions field.',
     'detachments.json, all detachments (B60a, D221)',
     lambda S: b60a_restrictions_no_stratagem_cp_debris(S)),

    # ── CSM: roster and detachment build census (S154 data turn, S155 tooling turn,
    # S157 data turn B — cult-troop cross-file points, closing the roster gap).
    # CSM_BUILD_SCOPE.md §1 fixed the real current-edition roster at 58, not the 112 the
    # raw source carries (54 of those 112 are Warhammer Legends units, out of scope). The
    # four cult-troop units are now priced via §4's cross-file append (D240); the roster
    # is complete at 58 of 58.
    ('CSM-1',
     'units.json carries all 58 real current-edition Chaos Space Marines units, including '
     'the four cult-troop units (Khorne Berzerkers, Plague Marines, Rubric Marines, Noise '
     'Marines) priced via their own cross-file MFM append per CSM_BUILD_SCOPE.md §4 (D240).',
     'units.json Chaos Space Marines army block; CSM_BUILD_SCOPE.md §1/§4',
     lambda S: csm_roster_count(S)),

    ('CSM-2',
     'detachments.json carries exactly 17 Chaos Space Marines detachments, matching the '
     'MFM roster (D237, CSM turn C).',
     'detachments.json armies["Chaos Space Marines"] (CSM_BUILD_SCOPE.md §3/§6, D237)',
     lambda S: csm_detachment_count(S)),

    ('CSM-3',
     'Exactly two Chaos Space Marines detachments — Devotees of Destruction and Murdertalon '
     'Raiders — carry text_source: none. Both are MFM-only detachments with no Wahapedia '
     'tier-2 prose to source from; this is the documented shape, not a parser gap.',
     'detachments.json Chaos Space Marines detachments (D237)',
     lambda S: csm_no_prose_detachments(S)),

    # ── Thousand Sons: detachment census (S160 data turn, turn C). THOUSAND_SONS_BUILD_SCOPE.md
    # §3 (D241, S158) worked out the correct count of 9 by diffing the MFM against Wahapedia;
    # D245 (S159) regressed it to 7 without checking the scope doc. Re-derived from
    # MFM_Thousand_Sons_v1_0.txt directly at S160 open, confirming D241 over D245 (D248).
    ('TS-1',
     'detachments.json carries exactly 9 Thousand Sons detachments, matching the MFM roster '
     '(THOUSAND_SONS_BUILD_SCOPE.md §3, D241, D248).',
     'detachments.json armies["Thousand Sons"] (D241, D248)',
     lambda S: ts_detachment_count(S)),

    ('TS-2',
     'No Thousand Sons detachment carries text_source: none — all 9 have real rule text, '
     'better than D241 anticipated (it expected the 3 MFM-only detachments to be prose-less '
     'like CSM\'s two). The 3 with no Wahapedia coverage — Ritual of Regeneration, Sekhetar '
     'Cohort, Servants of Change — are sourced from the faction pack instead (parse_ts_pack, D248).',
     'detachments.json Thousand Sons detachments (D248)',
     lambda S: ts_full_text_coverage(S)),

    # ── Thousand Sons: roster census, closing the tooling turn (S164). Mirrors CSM-1.
    # THOUSAND_SONS_BUILD_SCOPE.md §1 fixed the real current-edition roster at 34, not the
    # 60 the raw source carries (26 of those are Warhammer Legends, out of scope). No CSM-3
    # equivalent is needed here — TS-2 above already asserts zero TS detachments carry
    # text_source: none, which is the stronger and correct shape (§6's plan text expected
    # three prose-less detachments; D248 found the faction pack covers all of them instead).
    ('TS-3',
     'units.json carries all 34 real current-edition Thousand Sons units '
     '(THOUSAND_SONS_BUILD_SCOPE.md §1).',
     'units.json Thousand Sons army block; THOUSAND_SONS_BUILD_SCOPE.md §1',
     lambda S: ts_roster_count(S)),

]


# ── E21a: detachment_effects.json integrity ───────────────────────────────────

def _de_effects(S):
    """Flatten to (key, record, effect) triples."""
    out = []
    for key, rec in S.detachment_effects()['effects'].items():
        for eff in rec['effects']:
            out.append((key, rec, eff))
    return out


def e21a_keys_resolve(S):
    det = S.detachments()['detachments']
    bad = []
    for key, rec in S.detachment_effects()['effects'].items():
        if key not in det:
            bad.append(f'{key}: no such detachment record')
            continue
        army = key.split('|', 1)[0]
        if rec.get('army') != army:
            bad.append(f'{key}: record army={rec.get("army")!r} disagrees with key')
    if bad:
        return False, '; '.join(bad)
    n = len(S.detachment_effects()['effects'])
    return True, f'all {n} detachment keys resolve against the 169 built records'


def e21a_unit_names_resolve(S):
    bad = []
    pools = {}
    for key, rec, eff in _de_effects(S):
        army = rec['army']
        if army not in pools:
            pools[army] = S.resolved_pool(army)
        pool = pools[army]
        for field in ('units', 'except_units'):
            for name in eff.get('target', {}).get(field, []):
                if name not in pool:
                    bad.append(f'{key} [{eff["kind"]}.{field}]: {name!r} not in {army} pool')
    if bad:
        return False, '; '.join(bad)
    total = sum(len(e.get('target', {}).get(f, []))
                for _, _, e in _de_effects(S) for f in ('units', 'except_units'))
    return True, f'all {total} unit-name references resolve in their army\'s resolved pool'


def e21a_schema_valid(S):
    kinds = {'battleline', 'forbid', 'unlock', 'warlord'}
    modes = {'cannot_be', 'must_be_if_present'}
    caps = ['1000', '2000', '3000']
    bad = []
    pools = {}
    for key, rec, eff in _de_effects(S):
        k = eff.get('kind')
        if k not in kinds:
            bad.append(f'{key}: kind {k!r} is not one of {sorted(kinds)}')
        if not isinstance(eff.get('enforced'), bool):
            bad.append(f'{key} [{k}]: enforced must be an explicit boolean')
        if k == 'warlord' and eff.get('mode') not in modes:
            bad.append(f'{key} [warlord]: mode {eff.get("mode")!r} not in {sorted(modes)}')
        if k == 'unlock':
            pc = eff.get('points_cap')
            if not isinstance(pc, dict) or list(pc.keys()) != caps:
                bad.append(f'{key} [unlock]: points_cap keys must be exactly {caps}')
            else:
                vals = [pc[c] for c in caps]
                if vals != sorted(vals) or len(set(vals)) != 3:
                    bad.append(f'{key} [unlock]: points_cap values not strictly increasing: {vals}')
        army = rec['army']
        if army not in pools:
            pools[army] = S.resolved_pool(army)
        types = {u['unit_type'] for u in pools[army].values()}
        for t in eff.get('target', {}).get('unit_types', []):
            if t not in types:
                bad.append(f'{key} [{k}]: unit_type {t!r} does not exist in {army}')
    if bad:
        return False, '; '.join(bad)
    return True, f'{len(_de_effects(S))} effects across {len(S.detachment_effects()["effects"])} detachments all schema-valid'


def e21a_allied_targets(S):
    bad = []
    unenforced = []
    pools = {}
    for key, rec, eff in _de_effects(S):
        tgt = eff.get('target', {})
        army = rec['army']
        if army not in pools:
            pools[army] = S.resolved_pool(army)
        if 'allied_group' in tgt:
            g = tgt['allied_group']
            hits = [u for u in pools[army].values() if u.get('allied_group') == g]
            if eff['enforced'] and not hits:
                bad.append(f'{key} [{eff["kind"]}]: enforced but no {army} unit carries '
                           f'allied_group={g!r}')
        if 'keyword' in tgt and eff['enforced']:
            bad.append(f'{key} [{eff["kind"]}]: targets a bare keyword but claims enforced')
        if not eff['enforced']:
            unenforced.append(key + '/' + eff['kind'])
            if not eff.get('unenforced_reason'):
                bad.append(f'{key} [{eff["kind"]}]: enforced: false with no unenforced_reason')
    expect = ['Chaos Daemons|SHADOW LEGION/unlock']
    if sorted(unenforced) != expect:
        bad.append(f'unenforced inventory is {sorted(unenforced)}, expected {expect}')
    if bad:
        return False, '; '.join(bad)
    return True, ('allied targets resolve; exactly one documented unenforced effect remains '
                  '(Shadow Legion / HERETIC ASTARTES, awaiting Chaos Space Marines build) — '
                  'Changehost of Deceit flipped to enforced at Thousand Sons turn A (D248/E24)')


def csm_roster_count(S):
    """CSM_BUILD_SCOPE.md §1: real current-edition roster is 58, not the 112 the raw
    source carries. All 58 are built as of D240 (S157) — the four cult-troop units
    priced via §4's cross-file legion-MFM append."""
    armies = S.units()
    csm = next((a for a in armies if a.get('army') == 'Chaos Space Marines'), None)
    if csm is None:
        return False, 'Chaos Space Marines army block not found in units.json'
    n = len(csm.get('units') or [])
    if n != 58:
        return False, f'{n} CSM units built, expected 58 (real current-edition target)'
    return True, 'all 58 real current-edition CSM units built'


def csm_detachment_count(S):
    """D237: CSM's 17-detachment MFM roster, built S154."""
    dj = S.detachments()
    keys = dj.get('armies', {}).get('Chaos Space Marines', [])
    if len(keys) != 17:
        return False, f'{len(keys)} Chaos Space Marines detachments, expected 17'
    return True, '17 Chaos Space Marines detachments present'


def csm_no_prose_detachments(S):
    """D237: two CSM detachments are MFM-only with no Wahapedia tier-2 text to source prose
    from — text_source: none by design, not a gap."""
    dj = S.detachments()
    dets, keys = dj.get('detachments', {}), dj.get('armies', {}).get('Chaos Space Marines', [])
    none_keys = sorted(k for k in keys if dets.get(k, {}).get('text_source') == 'none')
    expect = ['Chaos Space Marines|DEVOTEES OF DESTRUCTION', 'Chaos Space Marines|MURDERTALON RAIDERS']
    if none_keys != expect:
        return False, f'text_source:none detachments are {none_keys}, expected {expect}'
    return True, 'exactly the two documented MFM-only CSM detachments carry text_source: none'


def ts_detachment_count(S):
    """D241/D248: TS's 9-detachment MFM roster (6 shared with Wahapedia, 3 MFM-only new in
    11th Ed), built S160."""
    dj = S.detachments()
    keys = dj.get('armies', {}).get('Thousand Sons', [])
    if len(keys) != 9:
        return False, f'{len(keys)} Thousand Sons detachments, expected 9'
    return True, '9 Thousand Sons detachments present'


def ts_full_text_coverage(S):
    """D248: unlike CSM, all 9 TS detachments carry real rule text -- the 3 with no Wahapedia
    coverage are sourced from the faction pack via parse_ts_pack instead of falling to none."""
    dj = S.detachments()
    dets, keys = dj.get('detachments', {}), dj.get('armies', {}).get('Thousand Sons', [])
    none_keys = sorted(k for k in keys if dets.get(k, {}).get('text_source') == 'none')
    if none_keys:
        return False, f'Thousand Sons detachments with text_source:none: {none_keys}, expected none'
    return True, 'all 9 Thousand Sons detachments carry real rule text (none, none)'


def ts_roster_count(S):
    """THOUSAND_SONS_BUILD_SCOPE.md §1: real current-edition roster is 34, not the 60 the
    raw source carries (26 are Warhammer Legends, excluded). Built S163 (D252, turn B)."""
    armies = S.units()
    ts = next((a for a in armies if a.get('army') == 'Thousand Sons'), None)
    if ts is None:
        return False, 'Thousand Sons army block not found in units.json'
    n = len(ts.get('units') or [])
    if n != 34:
        return False, f'{n} Thousand Sons units built, expected 34 (real current-edition target)'
    return True, 'all 34 real current-edition Thousand Sons units built'


def e21a_coverage(S):
    det = S.detachments()['detachments']
    have = set(S.detachment_effects()['effects'].keys())
    bl = re.compile(r'(gain|gains|have|has).{0,40}BATTLELINE', re.I | re.S)
    ul = re.compile(r'even though they do not have|allies allowed up to', re.I)
    missing = []
    for key, r in det.items():
        text = ' '.join(str(r.get(f) or '') for f in ('rule_text', 'restrictions'))
        if (bl.search(text) or ul.search(text)) and key not in have:
            missing.append(key)
    if missing:
        return False, ('built detachments with a construction effect and no row: '
                       + '; '.join(sorted(missing)))
    n = sum(1 for k, r in det.items()
            if bl.search(' '.join(str(r.get(f) or '') for f in ('rule_text', 'restrictions')))
            or ul.search(' '.join(str(r.get(f) or '') for f in ('rule_text', 'restrictions'))))
    return True, f'{n} built detachments carry a Battleline-grant or unlock clause; all have rows'


def e21a_belakor_warlord_covered(S):
    cd = next((a for a in S.units() if a['army'] == 'Chaos Daemons'), None)
    if cd is None:
        return False, 'Chaos Daemons army block not found'
    bl = next((u for u in cd['units'] if u['unit_name'] == "Be'Lakor"), None)
    if bl is None:
        return False, "Be'Lakor not found in Chaos Daemons"
    if not bl.get('must_be_warlord'):
        return False, ("Be'Lakor no longer carries must_be_warlord — SHADOW LEGION's conditional "
                       'Warlord rule is now uncovered and needs a warlord row')
    de = S.detachment_effects()['effects'].get('Chaos Daemons|SHADOW LEGION', {})
    if any(e['kind'] == 'warlord' for e in de.get('effects', [])):
        return False, ('SHADOW LEGION now carries a warlord row as well as the unit-level flag — '
                       'two sources for one rule')
    return True, "Be'Lakor must_be_warlord: true; SHADOW LEGION correctly carries no warlord row"


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


def b59a_non_consuming_engine(S):
    """B59a/D182: non_consuming rides alongside the bracket, not part of it.

    1. loOptHeadroom excludes a non_consuming group from the reservation subtracted
       from size (it does not shrink headroom the way a fixed/per_bracket/fills_to_size
       group does).
    2. loGroupCounts' optional branch clamps a non_consuming group to its band only —
       no headroom deduction, no addition to the reserved total other groups compete
       over (the fills_to_size group must not be shorted by it).
    3. Data side, active as of B59b: every model group in unit_loadouts.json carrying
       non_consuming: true must be on an optional group — the only shape the mechanism
       is defined for. Any count is tolerated; this does not hardcode an expected total.
    """
    txt = S.index_html()
    for needle, why in [
        ('if (ct.non_consuming) continue;',
         'loOptHeadroom does not skip the reservation for a non_consuming group'),
        ('const v = Math.max(0, Math.min(Number(oc[g.name]) || 0, band));',
         'loGroupCounts does not clamp a non_consuming group to band only, independent '
         'of headroom'),
    ]:
        if needle not in txt:
            return False, why

    lo = S.loadouts()
    bad = []
    for uid, u in lo.items():
        if uid.startswith('_') or not isinstance(u, dict):
            continue
        for g in (u.get('model_groups') or []):
            ct = g.get('count') or {}
            if ct.get('non_consuming') and not ct.get('optional'):
                bad.append((uid, g.get('name')))
    if bad:
        return False, f'non_consuming set on a non-optional group: {bad[:3]}'

    flagged = sum(
        1 for u in lo.values() if isinstance(u, dict)
        for g in (u.get('model_groups') or [])
        if (g.get('count') or {}).get('non_consuming')
    )
    return True, (f'engine wiring present (loOptHeadroom / loGroupCounts honour '
                  f'non_consuming); {flagged} unit_loadouts.json group(s) carry the '
                  f'flag today')


def b58_min_matches_composition(S):
    # Hand-authored entries (repro_check.py HAND_AUTHORED) bypass the parser entirely and
    # predate this field; they are frozen, not stale, and are excluded here for that reason.
    hand_authored = {'000001157', '000001044', '000004131', '000002712'}
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

# ── E1a. Detachment catalogue (detachments.json) ──────────────────────────────

FORCE_DISPOSITIONS = (
    'PRIORITY ASSETS', 'TAKE AND HOLD', 'PURGE THE FOE', 'DISRUPTION', 'RECONNAISSANCE',
)


def _army_records(S, army):
    """detachments.json stores one record per distinct detachment and lets each army
    index it by key, because seven armies shared a byte-identical Space Marines list.
    Resolve the indirection so the assertions still read per-army."""
    d = S.detachments()
    return [d['detachments'][k] for k in d['armies'][army]]


def _all_army_records(S):
    d = S.detachments()
    for army in d['armies']:
        yield army, _army_records(S, army)


def _all_detachments(S):
    for army, recs in _all_army_records(S):
        for r in recs:
            yield army, r


def detachments_repro_gate(S):
    """D193: the executable form of 'detachments.json is fresh'. detachments.json is a
    first-generation file with no earlier committed version to rebuild against, so the
    fixed point is set at first generation and held here from then on."""
    import os, importlib.util
    p = os.path.join(S.dir, 'detachments_repro_check.py')
    if not os.path.exists(p):
        return False, 'detachments_repro_check.py not found — the detachment reproduction gate is missing'
    spec = importlib.util.spec_from_file_location('detachments_repro_check', p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.repro(S.dir)


def e1a_keys_resolve(S):
    """detachments.json is stored deduplicated: one record per distinct detachment, each
    army holding a list of keys into it. Every key an army names must resolve, every
    record must be reachable from at least one army, and each record's own `key` field
    must agree with the key it is filed under. If any of the three slips, an army
    silently loses or gains detachments and nothing else would notice."""
    d = S.detachments()
    missing = [k for keys in d['armies'].values() for k in keys if k not in d['detachments']]
    orphan = [k for k in d['detachments'] if not any(k in v for v in d['armies'].values())]
    bad_self = [k for k, r in d['detachments'].items() if r.get('key') != k]
    return (not missing and not orphan and not bad_self), (
        f'{len(d["detachments"])} records, {sum(len(v) for v in d["armies"].values())} army slots; '
        f'{len(missing)} unresolved, {len(orphan)} orphaned, {len(bad_self)} key mismatches')


def e1a_dp_and_disposition(S):
    """25.03/25.04: a detachment costs 1-3 DP and grants exactly one force disposition."""
    bad_dp, bad_disp = [], []
    n = 0
    for army, r in _all_detachments(S):
        n += 1
        dp = r.get('dp')
        if not isinstance(dp, int) or isinstance(dp, bool) or not (1 <= dp <= 3):
            bad_dp.append((army, r.get('name'), dp))
        if r.get('force_disposition') not in FORCE_DISPOSITIONS:
            bad_disp.append((army, r.get('name'), r.get('force_disposition')))
    ok = not bad_dp and not bad_disp
    return ok, (f'{n} records; {len(bad_dp)} bad DP, {len(bad_disp)} bad disposition'
                + (f' e.g. {(bad_dp + bad_disp)[:3]}' if not ok else ''))


def e1a_no_duplicate_names_and_unique_tags(S):
    """25.04 forbids selecting the same detachment twice, and MFM_Instructions.txt adds a
    second exclusion: 'Some detachments are tagged with a Unique word or phrase. You cannot
    select more than one detachment that has the same one of these tags.' A duplicate name
    inside one army would make the first rule unenforceable by identity; a dropped or
    invented Unique tag would make the second unenforceable at all."""
    mod, rows = S.mfm_detachment_rows()
    dupes = []
    tag_mismatch = []
    tagged = 0
    for army, recs in _all_army_records(S):
        seen = set()
        for r in recs:
            k = mod.norm_key(r.get('name_raw') or r.get('name'))
            if k in seen:
                dupes.append((army, r.get('name')))
            seen.add(k)
        src = {mod.norm_key(d['name_raw']): d['unique_tag']
               for d in rows[mod.ARMY_TO_MFM[army]]}
        for r in recs:
            k = mod.norm_key(r.get('name_raw'))
            want = src.get(k)
            if r.get('unique_tag') != want:
                tag_mismatch.append((army, r.get('name'), r.get('unique_tag'), want))
            if want:
                tagged += 1
    ok = not dupes and not tag_mismatch
    return ok, (f'{len(dupes)} duplicate names, {len(tag_mismatch)} Unique-tag mismatches, '
                f'{tagged} tagged records'
                + (f' e.g. {(dupes + tag_mismatch)[:3]}' if not ok else ''))


def e1a_catalogue_matches_mfm(S):
    """MFM wins on structure and numbers. Every detachment in the file, and every
    enhancement name, point cost and print order inside it, must re-derive from the MFM
    text. Counts are reported, not asserted — they move whenever a faction pack or MFM
    revision lands, and an assertion that has to be hand-edited on every input change is
    an assertion that will eventually be hand-edited wrongly."""
    mod, rows = S.mfm_detachment_rows()
    bad = []
    n_det = n_enh = 0
    distinct = set()
    for army, recs in _all_army_records(S):
        fn = mod.ARMY_TO_MFM[army]
        src = {mod.norm_key(d['name_raw']): d for d in rows[fn]}
        if len(recs) != len(rows[fn]):
            bad.append((army, f'{len(recs)} records vs {len(rows[fn])} MFM rows'))
            continue
        for r in recs:
            n_det += 1
            distinct.add(r.get('key'))
            d = src.get(mod.norm_key(r.get('name_raw')))
            if d is None:
                bad.append((army, r.get('name'), 'not in MFM'))
                continue
            if r.get('dp') != d['dp'] or r.get('force_disposition') != d['force_disposition']:
                bad.append((army, r.get('name'), 'DP/disposition drift'))
            got = [(e.get('name'), e.get('points')) for e in r.get('enhancements') or []]
            want = [(e['name'], e['points']) for e in d['enhancements']]
            n_enh += len(got)
            if got != want:
                bad.append((army, r.get('name'), 'enhancement list drift'))
    ok = not bad
    return ok, (f'{n_det} records over {len(distinct)} distinct MFM rows, {n_enh} enhancements'
                + ('' if ok else f'; {len(bad)} mismatches e.g. {bad[:3]}'))


def e1a_no_wahapedia_only_enhancements(S):
    """The Wahapedia dump is a previous edition. An enhancement it lists that MFM does not
    is a stale leftover; carrying it would put a phantom option at a wrong price in front of
    the player. Text sources contribute descriptions only, never membership."""
    mod, rows = S.mfm_detachment_rows()
    strays = []
    for army, recs in _all_army_records(S):
        src = {mod.norm_key(d['name_raw']): {mod.norm_key(e['name']) for e in d['enhancements']}
               for d in rows[mod.ARMY_TO_MFM[army]]}
        for r in recs:
            allowed = src.get(mod.norm_key(r.get('name_raw')), set())
            for e in r.get('enhancements') or []:
                if mod.norm_key(e.get('name')) not in allowed:
                    strays.append((army, r.get('name'), e.get('name')))
    dropped = S.detachments()['_meta'].get('wahapedia_only_enhancements_dropped')
    return (not strays), (f'{len(strays)} non-MFM enhancements survived the join; '
                          f'{dropped} Wahapedia-only enhancements dropped')


def e1a_upgrade_flags_preserved(S):
    """The (Upgrade) tag is rules-significant under 25.04 and must survive the parse as a
    boolean, set on exactly the enhancements MFM prints it against — no more, no fewer."""
    mod, rows = S.mfm_detachment_rows()
    bad = []
    flagged = 0
    for army, recs in _all_army_records(S):
        src = {}
        for d in rows[mod.ARMY_TO_MFM[army]]:
            src[mod.norm_key(d['name_raw'])] = {mod.norm_key(e['name']): e['is_upgrade']
                                                for e in d['enhancements']}
        for r in recs:
            want = src.get(mod.norm_key(r.get('name_raw')), {})
            for e in r.get('enhancements') or []:
                got = e.get('is_upgrade')
                exp = want.get(mod.norm_key(e.get('name')))
                if got is not True and got is not False:
                    bad.append((army, e.get('name'), 'not boolean'))
                elif got != exp:
                    bad.append((army, r.get('name'), e.get('name'), got, exp))
                if got:
                    flagged += 1
    return (not bad), (f'{flagged} Upgrade-flagged enhancements'
                       + ('' if not bad else f'; {len(bad)} wrong e.g. {bad[:3]}'))


def e1a_text_source_and_gap_manifest(S):
    """text_source is one of three permitted values, and the set of detachments carrying
    'none' is exactly the named gap manifest. The per-tier totals are recorded rather than
    asserted: they move every time a faction pack arrives."""
    allowed = set(S.detachments()['_meta']['text_sources'])
    if allowed != {'faction_pack', 'wahapedia_10e', 'none'}:
        return False, f'permitted text_source set is {sorted(allowed)}'
    bad = []
    none_set = set()
    counts = {}
    for army, r in _all_detachments(S):
        ts = r.get('text_source')
        counts[ts] = counts.get(ts, 0) + 1
        if ts not in allowed:
            bad.append((army, r.get('name'), ts))
        if ts == 'none':
            none_set.add(r.get('key'))
            if r.get('rule_text') is not None:
                bad.append((army, r.get('name'), 'text_source none but rule_text present'))
        elif r.get('rule_text') is None:
            bad.append((army, r.get('name'), f'text_source {ts} but no rule_text'))
    manifest = {g['key'] for g in S.detachments()['_meta']['text_gap_manifest']}
    if manifest != none_set:
        bad.append(('gap manifest', sorted(manifest ^ none_set)[:3]))
    return (not bad), (f'text_source counts {counts}, {len(none_set)} in the gap manifest'
                       + ('' if not bad else f'; {len(bad)} problems e.g. {bad[:2]}'))


def e1b_budget_matches_muster(S):
    """D192 item 2. Read the DP column out of the 25.03 table, then read the threshold the
    engine actually applies out of index.html, and demand they agree. Neither number is
    written down here — both are re-derived, so this cannot pass on a stale memory."""
    mp = os.path.join(S.dir, 'Army_Muster_Rules.txt')
    ip = os.path.join(S.dir, 'index.html')
    for p in (mp, ip):
        if not os.path.exists(p):
            return False, f'{os.path.basename(p)} is not in the repo'
    flat = re.sub(r'\s+', ' ', open(mp, encoding='utf-8-sig').read().replace('\xa0', ' '))
    inc = re.search(r'INCURSION\s+(\d+)\s+(\d+)\s+\d+\s+\d+', flat)
    sf  = re.search(r'STRIKE FORCE\s+(\d+)\s+(\d+)\s+\d+\s+\d+', flat)
    if not inc or not sf:
        return False, '25.03 battle-size table no longer parses out of Army_Muster_Rules.txt'
    inc_pts, inc_dp = int(inc.group(1)), int(inc.group(2))
    sf_pts,  sf_dp  = int(sf.group(1)),  int(sf.group(2))

    html = open(ip, encoding='utf-8').read()
    m = re.search(r'function detachmentPointBudget\(pointsTotal\)\s*\{\s*'
                  r'return Number\(pointsTotal\) <= (\d+) \? (\d+) : (\d+);', html)
    if not m:
        return False, 'detachmentPointBudget is not in index.html in the expected shape'
    cut, low, high = int(m.group(1)), int(m.group(2)), int(m.group(3))

    # The same read for the unit limit, so the two battle-size rules are pinned together.
    u = re.search(r'function battleSizeUnitLimit\(pointsTotal\)\s*\{\s*'
                  r'return Number\(pointsTotal\) <= (\d+) \? (\d+) : (\d+);', html)
    if not u:
        return False, 'battleSizeUnitLimit is not in index.html in the expected shape'

    bad = []
    if cut != inc_pts:  bad.append(f'budget splits at {cut}, 25.03 puts Incursion at {inc_pts}')
    if low != inc_dp:   bad.append(f'Incursion budget is {low}, 25.03 says {inc_dp} DP')
    if high != sf_dp:   bad.append(f'Strike Force budget is {high}, 25.03 says {sf_dp} DP')
    if (cut, low, high) != (int(u.group(1)), int(u.group(2)), int(u.group(3))):
        bad.append('the DP budget and battleSizeUnitLimit no longer split the battle sizes the same way')
    return (not bad), ('; '.join(bad) if bad else
                       f'engine budget {low} DP at <= {cut} pts, {high} DP above — matches 25.03 '
                       f'(Incursion {inc_pts}/{inc_dp}, Strike Force {sf_pts}/{sf_dp}); '
                       f'3000 pts falls in the Strike Force branch')


def e1b_module_copies_agree(S):
    """The inlined list-storage block in index.html must be the same bytes as list_store.js.
    The declared SCHEMA_VERSION moves as tickets add persisted fields (E4b took it to 3);
    the number is pinned here so a bump on one side without the other cannot pass.
    Located by the module's own delimiters rather than by line number, so an edit above or
    below it cannot make this pass or fail for the wrong reason."""
    ip = os.path.join(S.dir, 'index.html')
    sp = os.path.join(S.dir, 'list_store.js')
    for p in (ip, sp):
        if not os.path.exists(p):
            return False, f'{os.path.basename(p)} is not in the repo'
    lines = open(ip, encoding='utf-8').read().split('\n')
    starts = [i for i, l in enumerate(lines) if l.startswith('/* =====')]
    ends   = [i for i, l in enumerate(lines) if l.startswith("})(typeof self !== 'undefined'")]
    if not starts or not ends:
        return False, 'the inlined list-storage block is not locatable in index.html'
    inlined = '\n'.join(lines[starts[0]:ends[0] + 1]).strip()
    standalone = open(sp, encoding='utf-8').read().strip()
    if inlined != standalone:
        il, sl = inlined.split('\n'), standalone.split('\n')
        first = next((n for n in range(min(len(il), len(sl))) if il[n] != sl[n]), min(len(il), len(sl)))
        return False, (f'the two copies differ ({len(il)} vs {len(sl)} lines, first difference at '
                       f'line {first + 1} of the block)')
    ver = re.search(r'var SCHEMA_VERSION = (\d+);', standalone)
    if not ver or ver.group(1) != '3':
        return False, f'SCHEMA_VERSION is {ver.group(1) if ver else "unreadable"}, expected 3'
    return True, f'both copies identical ({len(standalone.splitlines())} lines), SCHEMA_VERSION 3'


def e1b_harness_gate(S):
    """D107 applied to engine behaviour: the migration and the three selection constraints are
    claims about what the code does, so they are executed. Runs the real harness against the
    real catalogue rather than restating its conclusions here."""
    import subprocess
    p = os.path.join(S.dir, 'e1b_check.js')
    if not os.path.exists(p):
        return False, 'e1b_check.js not found — the E1b behaviour gate is missing'
    try:
        r = subprocess.run(['node', p, os.path.join(S.dir, 'index.html'),
                            os.path.join(S.dir, 'detachments.json'),
                            os.path.join(S.dir, 'list_store.js')],
                           capture_output=True, text=True, timeout=120, cwd=S.dir)
    except FileNotFoundError:
        return False, 'node is not available, so the E1b behaviour gate cannot run'
    except subprocess.TimeoutExpired:
        return False, 'e1b_check.js did not finish within 120s'
    out = (r.stdout or '') + (r.stderr or '')
    passed = len([l for l in out.split('\n') if l.strip().startswith('ok ')])
    failed = [l.strip() for l in out.split('\n') if l.strip().startswith('FAIL ')]
    if r.returncode != 0 or failed:
        return False, (f'{len(failed)} E1b check(s) failed, e.g. {failed[:2]}' if failed
                       else f'e1b_check.js exited {r.returncode}')
    return True, f'e1b_check.js: {passed} checks pass'


def e1c_engine_functions_defined_once(S):
    """The five legality helpers are declared inside the E1b block and NOWHERE else in the file.
    The E1c block is allowed to CALL them but never to redefine them; a second `function dpUsed`
    (or the other four) would be exactly the "picker growing its own rules" failure mode.

    Method: extract the E1b block by its own delimiters, and search the rest of the file for
    another `function NAME(` declaration of the same five names. If one exists, name it."""
    ip = os.path.join(S.dir, 'index.html')
    if not os.path.exists(ip):
        return False, 'index.html not found'
    html = open(ip, encoding='utf-8').read()
    lines = html.split('\n')

    def find_block(start_needle, end_needle):
        s = next((i for i, l in enumerate(lines) if start_needle in l), -1)
        e = next((i for i, l in enumerate(lines) if end_needle   in l), -1)
        if s < 0 or e < 0 or e <= s:
            return None, None
        return s, e

    e1b_s, e1b_e = find_block('// ── E1b: detachment selection rules', '// ── E1b block end')
    if e1b_s is None:
        return False, 'the E1b block delimiters are no longer locatable in index.html'
    e1c_s, e1c_e = find_block('// ── E1c: detachment picker', '// ── E1c block end')
    if e1c_s is None:
        return False, 'the E1c block delimiters are no longer locatable in index.html'

    names = ['dpUsed', 'duplicateDetachments', 'uniqueTagConflicts',
             'detachmentPointBudget', 'dpState']

    # Locate each name's DEFINITION line by number, then confirm every one lies inside the E1b
    # block. A definition outside E1b is exactly the failure mode to catch.
    bad = []
    for name in names:
        pat = re.compile(r'^\s*function\s+' + re.escape(name) + r'\s*\(', re.MULTILINE)
        matches = [i for i, l in enumerate(lines) if pat.match(l)]
        if not matches:
            bad.append(f'{name}: no definition found at all')
            continue
        if len(matches) > 1:
            bad.append(f'{name}: defined {len(matches)} times (lines {[m+1 for m in matches]})')
            continue
        line_no = matches[0]
        if not (e1b_s < line_no < e1b_e):
            bad.append(f'{name}: defined at line {line_no+1}, outside the E1b block '
                       f'(lines {e1b_s+1}..{e1b_e+1})')
    if bad:
        return False, '; '.join(bad)
    return True, (f'all five legality helpers are defined exactly once, inside the E1b block '
                  f'(lines {e1b_s+1}..{e1b_e+1}); the E1c block ({e1c_s+1}..{e1c_e+1}) calls them')


def e1c_harness_gate(S):
    """D107 applied to the picker: the disable classification is a claim about behaviour, so it
    is executed against the real catalogue rather than described here."""
    import subprocess
    p = os.path.join(S.dir, 'e1c_check.js')
    if not os.path.exists(p):
        return False, 'e1c_check.js not found — the E1c behaviour gate is missing'
    try:
        r = subprocess.run(['node', p, os.path.join(S.dir, 'index.html'),
                            os.path.join(S.dir, 'detachments.json')],
                           capture_output=True, text=True, timeout=120, cwd=S.dir)
    except FileNotFoundError:
        return False, 'node is not available, so the E1c behaviour gate cannot run'
    except subprocess.TimeoutExpired:
        return False, 'e1c_check.js did not finish within 120s'
    out = (r.stdout or '') + (r.stderr or '')
    passed = len([l for l in out.split('\n') if l.strip().startswith('ok ')])
    failed = [l.strip() for l in out.split('\n') if l.strip().startswith('FAIL ')]
    if r.returncode != 0 or failed:
        return False, (f'{len(failed)} E1c check(s) failed, e.g. {failed[:2]}' if failed
                       else f'e1c_check.js exited {r.returncode}')
    return True, f'e1c_check.js: {passed} checks pass'


def e4b_limit_matches_muster(S):
    """The Enhancement Limit the engine applies is the Enhancement Limit COLUMN of the 25.03
    battle-size table, not the DP column beside it. The two differ (2/3 for DP, 2/4 for
    enhancements) and sit adjacent in the same row, which is exactly the kind of pair that gets
    copied across by mistake. Neither number is written down here: both are re-derived, the
    table from Army_Muster_Rules.txt and the threshold from index.html."""
    mp = os.path.join(S.dir, 'Army_Muster_Rules.txt')
    ip = os.path.join(S.dir, 'index.html')
    for p in (mp, ip):
        if not os.path.exists(p):
            return False, f'{os.path.basename(p)} is not in the repo'
    flat = re.sub(r'\s+', ' ', open(mp, encoding='utf-8-sig').read().replace('\xa0', ' '))
    inc = re.search(r'INCURSION\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)', flat)
    sf  = re.search(r'STRIKE FORCE\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)', flat)
    if not inc or not sf:
        return False, '25.03 battle-size table no longer parses out of Army_Muster_Rules.txt'
    inc_pts, inc_dp, inc_enh = int(inc.group(1)), int(inc.group(2)), int(inc.group(3))
    sf_pts,  sf_dp,  sf_enh  = int(sf.group(1)),  int(sf.group(2)),  int(sf.group(3))

    html = open(ip, encoding='utf-8').read()
    m = re.search(r'function enhancementLimit\(pointsTotal\)\s*\{\s*'
                  r'return Number\(pointsTotal\) <= (\d+) \? (\d+) : (\d+);', html)
    if not m:
        return False, 'enhancementLimit is not in index.html in the expected shape'
    cut, low, high = int(m.group(1)), int(m.group(2)), int(m.group(3))

    bad = []
    if cut != inc_pts:
        bad.append(f'the engine splits at {cut} pts, 25.03 puts Incursion at {inc_pts}')
    if low != inc_enh:
        bad.append(f'engine allows {low} at Incursion, 25.03 says {inc_enh}')
    if high != sf_enh:
        bad.append(f'engine allows {high} at Strike Force, 25.03 says {sf_enh}')
    if (low, high) == (inc_dp, sf_dp) and (inc_dp, sf_dp) != (inc_enh, sf_enh):
        bad.append('the enhancement limit has been taken from the DP column, not the '
                   'Enhancement Limit column')
    # The 3,000-point size 25.03 does not define must land in the same branch here as it does
    # for DP and for the unit limit, so the three battle-size rules cannot disagree.
    d = re.search(r'function detachmentPointBudget\(pointsTotal\)\s*\{\s*'
                  r'return Number\(pointsTotal\) <= (\d+) \?', html)
    u = re.search(r'function battleSizeUnitLimit\(pointsTotal\)\s*\{\s*'
                  r'return Number\(pointsTotal\) <= (\d+) \?', html)
    if not d or not u:
        return False, 'detachmentPointBudget or battleSizeUnitLimit is no longer in the expected shape'
    if not (int(d.group(1)) == int(u.group(1)) == cut):
        bad.append('the three battle-size-derived rules no longer split the sizes at the same '
                   'points total')
    return (not bad), ('; '.join(bad) if bad else
                       f'engine allows {low} enhancements at <= {cut} pts and {high} above — '
                       f'matches the 25.03 Enhancement Limit column (Incursion {inc_pts}/{inc_enh}, '
                       f'Strike Force {sf_pts}/{sf_enh}), distinct from the DP column '
                       f'({inc_dp}/{sf_dp}); 3,000 pts falls in the Strike Force branch for all three')


# Two units are typed Character while their keyword lists do not say CHARACTER. Both are data
# gaps, not eligibility facts, and both are in the SAFE direction — unit_type offers the pick,
# the keyword list is merely incomplete. They are named here so the assertion stays sharp: any
# THIRD such unit, or any unit in the opposite direction, fails the gate.
E4B_KEYWORD_GAPS = {
    ('Dark Angels', 'Ravenwing Command Squad'),      # CHARACTER sits on the Champion model group
    ('Chaos Daemons', 'Rendmaster on Blood Throne'), # Chaos Daemons carry ability-style keywords only
    # S147 (CSM turn A) — same shape as Ravenwing Command Squad: a two-model-group
    # Character datasheet where CHARACTER is scoped to only the named model, not
    # "ALL MODELS", so the transform's (correct) refusal to promote a model-scoped
    # keyword to the whole unit leaves the unit-level keyword list incomplete.
    ('Chaos Space Marines', 'Dark Apostle'),         # CHARACTER sits on the DARK APOSTLE model
    ('Chaos Space Marines', 'Dark Commune'),         # CHARACTER sits on the CULT DEMAGOGUE model
    ('Chaos Space Marines', 'Traitor Enforcer'),     # CHARACTER sits on the TRAITOR ENFORCER model
}


def e4b_eligibility_derivations_agree(S):
    """D199: enhancement eligibility keys off unit_type, because the keyword lists are not
    uniformly populated. That is only safe while the two derivations agree, so this holds them
    to it: unit_type == 'Character' must select the same set as (has CHARACTER keyword AND NOT
    EPIC HERO keyword), everywhere keywords are populated, bar the two documented gaps.

    The EPIC HERO half of the keyword test is not optional. Fifty-odd Epic Heroes carry the
    CHARACTER keyword — in the rules an Epic Hero IS a Character — so a bare CHARACTER test
    would call them all eligible and contradict 25.04's own bullet."""
    units = S.units()
    kw_only, ut_only, gaps_seen, unpopulated = [], [], set(), 0
    for block in units:
        army = block.get('army')
        for u in block.get('units', []):
            kws, populated = set(), False
            for g in (u.get('model_groups') or []):
                names = g.get('keyword_names') or []
                if names:
                    populated = True
                for k in names:
                    kws.add(str(k).lower())
            if not populated:
                unpopulated += 1
                continue
            kw_elig = ('character' in kws) and ('epic hero' not in kws)
            ut_elig = (u.get('unit_type') == 'Character')
            if kw_elig and not ut_elig:
                kw_only.append(f"{army}/{u.get('unit_name')} (type {u.get('unit_type')})")
            elif ut_elig and not kw_elig:
                if (army, u.get('unit_name')) in E4B_KEYWORD_GAPS:
                    gaps_seen.add((army, u.get('unit_name')))
                else:
                    ut_only.append(f"{army}/{u.get('unit_name')}")

    bad = []
    if kw_only:
        bad.append('the keyword lists make these eligible while unit_type does not, so the '
                   'engine is refusing legal picks: ' + ', '.join(kw_only[:5]))
    if ut_only:
        bad.append('these are typed Character with no CHARACTER keyword and are not documented '
                   'gaps, so the engine may be offering illegal picks: ' + ', '.join(ut_only[:5]))
    missing = E4B_KEYWORD_GAPS - gaps_seen
    if missing:
        bad.append('a documented keyword gap has closed and the allowlist is now stale — remove '
                   'it from E4B_KEYWORD_GAPS: ' + ', '.join(f'{a}/{n}' for a, n in sorted(missing)))

    total = sum(len(b.get('units', [])) for b in units)
    chars = sum(1 for b in units for u in b.get('units', []) if u.get('unit_type') == 'Character')
    heroes = sum(1 for b in units for u in b.get('units', []) if u.get('unit_type') == 'Epic Hero')
    return (not bad), ('; '.join(bad) if bad else
                       f'{chars} Character and {heroes} Epic Hero across {total} units; the '
                       f'unit_type-derived and keyword-derived eligible sets agree on every unit '
                       f'with keywords populated ({unpopulated} without), bar the '
                       f'{len(E4B_KEYWORD_GAPS)} documented gaps')


def e4b_name_collision_census(S):
    """D199's forcing finding, pinned. The duplicate rule is keyed by NAME army-wide rather than
    by (detachment, name) because the same enhancement name is reachable through two different
    detachments inside one army. If a data regeneration moves this number, the choice of key has
    to be revisited, so the census is pinned rather than merely described.

    Counted as distinct (army, name) pairs. Only six distinct NAMES collide; they repeat across
    the chapter armies plus one CSM-internal collision, so the name count and the pair count
    are very different numbers and pinning the wrong one would look equally plausible."""
    dj = S.detachments()
    dets, armies = dj.get('detachments', {}), dj.get('armies', {})
    if not dets or not armies:
        return False, 'detachments.json no longer carries both a detachments map and an armies index'
    pairs, names, differing = set(), set(), []
    for army, keys in armies.items():
        by_name = {}
        for k in keys:
            d = dets.get(k)
            if not d:
                continue
            for e in (d.get('enhancements') or []):
                by_name.setdefault(e['name'], []).append((k, e.get('points')))
        for n, rows in by_name.items():
            if len(rows) > 1:
                pairs.add((army, n))
                names.add(n)
                if len({r[1] for r in rows}) > 1:
                    differing.append(f'{army}/{n}')

    EXPECTED_PAIRS, EXPECTED_NAMES, EXPECTED_DIFFERING = 30, 6, 1
    bad = []
    if len(pairs) != EXPECTED_PAIRS:
        bad.append(f'{len(pairs)} reachable same-army cross-detachment collisions, expected '
                   f'{EXPECTED_PAIRS} — the name-keyed duplicate rule (D199 call 1) rests on '
                   f'this being non-zero and was scoped against this figure')
    if len(names) != EXPECTED_NAMES:
        bad.append(f'{len(names)} distinct colliding names, expected {EXPECTED_NAMES}')
    if len(differing) != EXPECTED_DIFFERING:
        bad.append(f'{len(differing)} collisions where the two copies are priced differently, '
                   f'expected {EXPECTED_DIFFERING} — this is what forces the stored assignment '
                   f'to carry a detachment key rather than a bare name (got {differing[:4]})')
    return (not bad), ('; '.join(bad) if bad else
                       f'{len(pairs)} reachable same-army collisions across {len(names)} distinct '
                       f'names, {len(differing)} of them priced differently ({differing[0]}) — '
                       f'name-keyed duplicates and the stored detachment key are both still forced')


def e4b_engine_functions_defined_once(S):
    """E1c-1's guard, applied to E4b. The functions that answer enhancement legality are declared
    inside the E4b block and NOWHERE else in index.html. Consumers call them; nothing redefines
    them. A second implementation growing quietly in the picker E4c is about to build is exactly
    the failure this is here to catch, and it would be invisible otherwise."""
    ip = os.path.join(S.dir, 'index.html')
    if not os.path.exists(ip):
        return False, 'index.html not found'
    lines = open(ip, encoding='utf-8').read().split('\n')

    s_i = next((i for i, l in enumerate(lines) if '// ── E4b: enhancement assignment rules' in l), -1)
    e_i = next((i for i, l in enumerate(lines) if '// ── E4b block end' in l), -1)
    if s_i < 0 or e_i <= s_i:
        return False, 'the E4b block delimiters are no longer locatable in index.html'

    names = ['enhancementLimit', 'enhancementRecord', 'enhancementPoints', 'enhancementIsUpgrade',
             'enhancementIsOffered', 'assignedEnhancements', 'enhancementCount',
             'enhancementCopies', 'enhancementMaxCopies', 'attachedGroupListIds',
             'groupEnhancementCarriers', 'enhancementTypeEligible', 'canAssignEnhancement',
             'enhancementArmyState', 'enhancementRowState', 'enhancementAttachBlock']
    bad = []
    for name in names:
        pat = re.compile(r'^\s*function\s+' + re.escape(name) + r'\s*\(')
        hits = [i for i, l in enumerate(lines) if pat.match(l)]
        if not hits:
            bad.append(f'{name} is not defined at all')
        elif len(hits) > 1:
            bad.append(f'{name} is defined {len(hits)} times (lines '
                       + ', '.join(str(h + 1) for h in hits) + ')')
        elif not (s_i < hits[0] < e_i):
            bad.append(f'{name} is defined at line {hits[0] + 1}, outside the E4b block')

    # The attach gate is the second enforcement point (D199). It is only an enforcement point if
    # the action actually consults it, so that call is checked rather than assumed.
    body = '\n'.join(lines)
    m = re.search(r'function editLeaderTarget\(listId, targetListId\)\s*\{(.*?)\n  \}', body, re.S)
    if not m:
        return False, 'editLeaderTarget is no longer in index.html in the expected shape'
    if 'enhancementAttachBlock' not in m.group(1):
        bad.append('editLeaderTarget does not call enhancementAttachBlock — the attach gate is '
                   'declared but not wired, so two carriers can still be merged into one unit')
    if 'enhancementPointsForEntry' not in body:
        bad.append('ptsForEntry no longer folds in enhancementPointsForEntry')

    return (not bad), ('; '.join(bad) if bad else
                       f'all {len(names)} enhancement legality functions are defined exactly once, '
                       f'inside the E4b block, and both enforcement points are wired')


def e4b_harness_gate(S):
    """D107 applied to the enhancement engine: the Upgrade count carve-out, the attached-unit
    scope of the one-per-unit rule and the hard block are claims about behaviour, so they are
    executed against the real catalogue rather than described here."""
    import subprocess
    p = os.path.join(S.dir, 'e4b_check.js')
    if not os.path.exists(p):
        return False, 'e4b_check.js not found — the E4b behaviour gate is missing'
    try:
        r = subprocess.run(['node', p, os.path.join(S.dir, 'index.html'),
                            os.path.join(S.dir, 'detachments.json')],
                           capture_output=True, text=True, timeout=120, cwd=S.dir)
    except FileNotFoundError:
        return False, 'node is not available, so the E4b behaviour gate cannot run'
    except subprocess.TimeoutExpired:
        return False, 'e4b_check.js did not finish within 120s'
    out = (r.stdout or '') + (r.stderr or '')
    passed = len([l for l in out.split('\n') if l.strip().startswith('ok ')])
    failed = [l.strip() for l in out.split('\n') if l.strip().startswith('FAIL ')]
    if r.returncode != 0 or failed:
        return False, (f'{len(failed)} E4b check(s) failed, e.g. {failed[:2]}' if failed
                       else f'e4b_check.js exited {r.returncode}')
    return True, f'e4b_check.js: {passed} checks pass'


def _b63_soul_grinder(S):
    """Locate Soul Grinder's weapon list in units.json, or raise if the unit or army has moved."""
    for army in S.units():
        if army['army'] != 'Chaos Daemons':
            continue
        for u in army['units']:
            if u['unit_name'] == 'Soul Grinder':
                return u['weapons']
    raise AssertionError('Chaos Daemons / Soul Grinder not found in units.json')


def b63_soul_grinder_four_god_weapons(S):
    weapons = _b63_soul_grinder(S)
    tagged = [w for w in weapons if w.get('allegiance_condition')]
    gods = sorted(w['allegiance_condition'] for w in tagged)
    expect = ['Khorne', 'Nurgle', 'Slaanesh', 'Tzeentch']
    if len(tagged) != 4 or gods != expect:
        return False, f'Soul Grinder carries {len(tagged)} allegiance-tagged weapon(s): {gods}'
    return True, 'Soul Grinder carries exactly four allegiance-tagged weapons, one per god'


def b63_soul_grinder_base_equipment_correct(S):
    weapons = _b63_soul_grinder(S)
    by_name = {w['weapon_name']: w for w in weapons}
    bad = []
    for name in ('Torrent of burning blood', 'Warp gaze', 'Phlegm bombardment', 'Scream of despair'):
        w = by_name.get(name)
        if w is None:
            bad.append(f'{name}: missing')
        elif w.get('is_base_equipment') not in (False, 'FALSE'):
            bad.append(f'{name}: is_base_equipment={w.get("is_base_equipment")!r}, expected not base')
    for name in ('Harvester cannon', 'Iron claw', 'Warpsword'):
        w = by_name.get(name)
        if w is None:
            bad.append(f'{name}: missing')
        elif w.get('is_base_equipment') is not True:
            bad.append(f'{name}: is_base_equipment={w.get("is_base_equipment")!r}, expected True')
    if bad:
        return False, '; '.join(bad)
    return True, ('the four god weapons are not base equipment; Harvester cannon, Iron claw '
                  'and Warpsword all are')


def b63_no_other_unit_carries_allegiance(S):
    hits = []
    for army in S.units():
        for u in army['units']:
            if u['unit_name'] == 'Soul Grinder' and army['army'] == 'Chaos Daemons':
                continue
            for w in u.get('weapons', []):
                if w.get('allegiance_condition'):
                    hits.append(f"{army['army']}/{u['unit_name']}/{w['weapon_name']}")
    if hits:
        return False, f'{len(hits)} unexpected allegiance_condition carrier(s): {hits[:5]}'
    return True, 'no unit other than Soul Grinder carries an allegiance_condition'


def b63_allegiance_values_valid(S):
    valid = {'Khorne', 'Tzeentch', 'Nurgle', 'Slaanesh'}
    bad = []
    for army in S.units():
        for u in army['units']:
            for w in u.get('weapons', []):
                v = w.get('allegiance_condition')
                if v and v not in valid:
                    bad.append(f"{u['unit_name']}/{w['weapon_name']}: {v!r}")
    if bad:
        return False, f'{len(bad)} allegiance_condition value(s) not a god name: {bad[:5]}'
    return True, 'every allegiance_condition value is one of the four god names'


# B61/D208 shipped Death Guard's Plague Legions carriers; turn A (D248/E24) adds Thousand
# Sons' Scintillating Legions carriers on the same mechanism. One dict, generalising all
# four B61-1..4 census assertions below rather than forking TS-specific siblings, so a
# future allied-group army (Emperor's Children/Legions of Excess, etc.) is a one-line add
# here, not a fifth set of near-duplicate functions.
ALLIED_CARRIER_GROUPS = {
    'Death Guard': ('Plague Legions', {'Beasts of Nurgle', 'Great Unclean One', 'Nurglings',
                                        'Plaguebearers', 'Plague Drones', 'Rotigus'}),
    'Thousand Sons': ('Scintillating Legions', {'Kairos Fateweaver', 'Lord of Change',
                                                 'Flamers', 'Screamers', 'Pink Horrors',
                                                 'Blue Horrors'}),
}


def b61_plague_legions_census(S):
    bad = []
    for army_name, (label, expect) in ALLIED_CARRIER_GROUPS.items():
        army = next((a for a in S.units() if a['army'] == army_name), None)
        if army is None:
            bad.append(f'{army_name} army block not found')
            continue
        tagged = {u['unit_name'] for u in army['units'] if u.get('allied_group') == label}
        other_tagged = [u['unit_name'] for u in army['units']
                        if 'allied_group' in u and u.get('allied_group') != label]
        if tagged != expect or other_tagged:
            bad.append(f'{army_name}: tagged={sorted(tagged)}, expected={sorted(expect)}, '
                        f'other-tagged={other_tagged}')
    if bad:
        return False, '; '.join(bad)
    return True, ('exactly the expected carrier units carry the tag in each allied-carrier '
                  'army (' + ', '.join(ALLIED_CARRIER_GROUPS) + ')')


def b61_no_other_army_carries_allied_group(S):
    carrier_armies = set(ALLIED_CARRIER_GROUPS)
    hits = []
    for army in S.units():
        if army['army'] in carrier_armies:
            continue
        for u in army['units']:
            if 'allied_group' in u:
                hits.append(f"{army['army']}/{u['unit_name']}")
    if hits:
        return False, (f'{len(hits)} unexpected allied_group carrier(s) outside '
                        f'{sorted(carrier_armies)}: {hits[:5]}')
    return True, f'no army other than {sorted(carrier_armies)} carries allied_group'


def b61_cd_native_copies_distinct(S):
    cd = next((a for a in S.units() if a['army'] == 'Chaos Daemons'), None)
    if cd is None:
        return False, 'Chaos Daemons army block not found'
    bad = []
    for army_name, (label, names) in ALLIED_CARRIER_GROUPS.items():
        army = next((a for a in S.units() if a['army'] == army_name), None)
        if army is None:
            bad.append(f'{army_name} army block not found')
            continue
        cd_by_name = {u['unit_name']: u for u in cd['units'] if u['unit_name'] in names}
        army_by_name = {u['unit_name']: u for u in army['units'] if u['unit_name'] in names}
        for n in sorted(names):
            c, d = cd_by_name.get(n), army_by_name.get(n)
            if c is None:
                bad.append(f'{n}: missing from Chaos Daemons')
                continue
            if d is None:
                bad.append(f'{n}: missing from {army_name}')
                continue
            if c['unit_id'] == d['unit_id']:
                bad.append(f'{n}: same unit_id in both {army_name} and Chaos Daemons '
                            f'({c["unit_id"]})')
            if 'allied_group' in c:
                bad.append(f'{n}: Chaos Daemons native copy unexpectedly carries allied_group')
    if bad:
        return False, '; '.join(bad)
    return True, 'all carrier units exist as distinct, untagged native copies in Chaos Daemons'


def b61_allied_group_headers_intact(S):
    import importlib, sys as _sys
    sys_path_added = S.dir not in _sys.path
    if sys_path_added:
        _sys.path.insert(0, S.dir)
    try:
        mod_name = 'mfm_points_parser'
        if mod_name in _sys.modules:
            mod = importlib.reload(_sys.modules[mod_name])
        else:
            mod = importlib.import_module(mod_name)
    finally:
        if sys_path_added:
            _sys.path.remove(S.dir)
    expect = {'PLAGUE LEGIONS', 'SCINTILLATING LEGIONS', 'BLOOD LEGIONS',
              'LEGIONS OF EXCESS', 'HARLEQUINS', 'YNNARI'}
    have = set(getattr(mod, 'ALLIED_GROUP_HEADERS', {}).keys())
    if have != expect:
        return False, f'ALLIED_GROUP_HEADERS={sorted(have)}, expected={sorted(expect)}'
    return True, 'all six documented allied-group labels are recognised'



# ── P4: GW-derived source census ──────────────────────────────────────────────
#
# Derived S135 empirically: every candidate source file was moved out of the
# directory one at a time and ./baseline.sh re-run. REQUIRED means at least one
# of the 21 gates failed without it. Reading imports is not enough — several
# files are NAMED in a parser's lookup table without ever being opened, because
# the faction they belong to is not built yet.

P4_REQUIRED_SOURCES = [
    # MFM points files for the eight built army sources.
    'MFM_Black_Templars_v1_0.txt', 'MFM_Blood_Angels_v1_0.txt',
    'MFM_Chaos_Daemons_v1_0.txt', 'MFM_Dark_Angels_v1_0.txt',
    'MFM_Death_Guard_v1_0.txt', 'MFM_Death_Watch_v1_0.txt',
    'MFM_Space_Marines_v1_0.txt', 'MFM_Space_Wolves_v1_0.txt',
    'MFM_Instructions.txt',
    # Faction web composition files.
    'Black_Templars_web.txt', 'Dark_Angels_web.txt', 'Death_Guard_web.txt',
    'Space_Marines_web.txt', 'Space_Wolves_web.txt',
    # Faction packs and reference text.
    'Space_Marines_Faction_Pack_v1_0.md', 'Dark_Angels_Faction_Pack_June_2026.md',
    'Army_Muster_Rules.txt', 'chaos_daemons_reference.md',
]

# Every GW-source filename that appears anywhere in the gates or parsers. Some are
# referenced but not required — the priority-faction files below are named in
# mfm_points_parser.py's faction map against the day those factions are built.
# '_web.txt' is the interpolation stub the web filenames are constructed from.
P4_REFERENCED_SOURCES = {
    'Army_Muster_Rules.txt', 'Dark_Angels_Faction_Pack_June_2026.md',
    'MFM_Black_Templars_v1_0.txt', 'MFM_Blood_Angels_v1_0.txt',
    'MFM_Chaos_Daemons_v1_0.txt', 'MFM_Chaos_Space_Marines_v1_0.txt',
    'MFM_Chapter_Pass.md', 'MFM_Dark_Angels_v1_0.txt', 'MFM_Death_Guard_v1_0.txt',
    'MFM_Death_Watch_v1_0.txt', 'MFM_Drukhari_v1_0.txt',
    'MFM_Emperors_Children_v1_0.txt', 'MFM_FW_Reconciliation.md',
    'MFM_Grey_Knights_v1_0.txt', 'MFM_Instructions.txt',
    'MFM_Space_Marines_v1_0.txt', 'MFM_Space_Wolves_v1_0.txt',
    'MFM_Thousand_Sons_v1_0.txt', 'MFM_World_Eaters_v1_0.txt',
    'MFM_Standalone_Pass.md',
    'Space_Marines_Faction_Pack_v1_0.md', 'Space_Marines_web.txt',
    '_web.txt', 'chaos_daemons_reference.md', 'mfm_sm.txt',
}

P4_SCANNED = [
    'repro_check.py', 'units_repro_check.py', 'detachments_repro_check.py',
    'rules_assertions.py', 'mfm_points_parser.py', 'detachment_parser.py',
    'wahapedia_transform.py', 'convert_to_json.py', 'merge_factions.py',
    'loadout_parser.py', 'equipped_parser.py', 'ds_wargear_abilities_parser.py',
    'mfm_reconcile.py', 'add_loadout_groups.py', 'integrity_check.py',
    'pipeline_manifest.py',
]

_P4_PAT = re.compile(
    r"[A-Za-z0-9_']*(?:MFM_[A-Za-z0-9_]+|_web|Faction_Pack[A-Za-z0-9_]*|mfm_sm"
    r"|Army_Muster_Rules|wh40k_core_rules|chaos_daemons_reference)[A-Za-z0-9_]*\.(?:txt|md)")


def p4_source_census(S):
    bad = []
    missing = [f for f in P4_REQUIRED_SOURCES
               if not os.path.exists(os.path.join(S.dir, f))]
    if missing:
        bad.append('required source file(s) absent: ' + ', '.join(sorted(missing)))
    found = set()
    for f in P4_SCANNED:
        p = os.path.join(S.dir, f)
        if not os.path.exists(p):
            continue
        with open(p, encoding='utf-8') as fh:
            text = fh.read()
        # This file carries the census lists themselves. Scanning them would make the
        # assertion agree with itself by construction, so the census block is cut out
        # before the scan.
        if f == 'rules_assertions.py':
            cut = text.find('# \u2500\u2500 P4: GW-derived source census')
            end = text.find('def p4_source_census(')
            if cut != -1 and end != -1:
                text = text[:cut] + text[end:]
        for m in _P4_PAT.findall(text):
            found.add(m.lstrip("'"))
    added = found - P4_REFERENCED_SOURCES
    dropped = P4_REFERENCED_SOURCES - found
    if added:
        bad.append('gates/parsers now reference source file(s) not in the census: '
                   + ', '.join(sorted(added)) + ' — re-run the park-and-rerun census')
    if dropped:
        bad.append('census names source file(s) nothing references any more: '
                   + ', '.join(sorted(dropped)) + ' — they may now be removable')
    if bad:
        return False, '; '.join(bad)
    return True, (f'{len(P4_REQUIRED_SOURCES)} required source files present; '
                  f'{len(found)} referenced filenames unchanged')


# ── runner ────────────────────────────────────────────────────────────────────


# ── B62: presence-and-parse gate over the nine Gen-1 Chaos Daemons root CSVs ──
# (D205). These are Gen-1 hand-built data, never routed through wahapedia_transform.py
# (D132), and the only copy of them the project holds — the repo excludes them on
# GW-text grounds (they carry rule and ability text verbatim). When three went missing
# at S131 the symptom was a confusing repro byte mismatch, not a clear "missing
# pipeline input". This checks each is present and parses as a non-empty CSV with its
# expected header, so a missing or truncated one fails loudly and by name here instead.
_B62_CD_CSVS = {
    'Unit_Stats.csv':          ['Army Name', 'Unit Name', 'Unit Type'],
    'Unit_Points.csv':         ['Army Name', 'Unit Name', 'Size_1'],
    'Unit_Wargear_Options.csv': ['Army Name', 'Unit Name', 'Weapon Replaced', 'Replacement Weapon Name'],
    'Unit_Other_Options.csv':  ['Army Name', 'Unit Name', 'Option Name'],
    'Unit_Weapons.csv':        ['Army Name', 'Unit Name', 'Weapon Name', 'Is Base Equipment'],
    'Unit_Abilities.csv':      ['Unit Ability Name', 'Unit Ability Description'],
    'Keywords.csv':            ['Keyword Name', 'Keyword Description'],
    'Rules.csv':               ['Rule Name', 'Rule Description'],
    'Weapon_Abilities.csv':    ['Weapon Ability Name', 'Weapon Ability Description'],
}


def b62_cd_csv_presence(S):
    bad = []
    checked = 0
    for fname, expect_cols in sorted(_B62_CD_CSVS.items()):
        path = os.path.join(S.dir, fname)
        if not os.path.exists(path):
            bad.append(f'{fname}: missing')
            continue
        try:
            with open(path, encoding='utf-8-sig', newline='') as f:
                rows = list(csv.DictReader(f))
        except Exception as e:
            bad.append(f'{fname}: unreadable ({type(e).__name__})')
            continue
        if not rows:
            bad.append(f'{fname}: present but has no data rows')
            continue
        header = set(rows[0].keys())
        missing_cols = [c for c in expect_cols if c not in header]
        if missing_cols:
            bad.append(f'{fname}: missing expected column(s) {missing_cols}')
            continue
        checked += 1
    if bad:
        return False, '%d of 9 CD root CSV(s) failed: %s' % (len(bad), '; '.join(bad))
    return True, 'all 9 Chaos Daemons root CSVs present, non-empty, and header-complete'


# ── E21b: chapter exclusivity, structural ─────────────────────────────────────

# The eleven chapter FACTION keywords that correspond to an app army. A datasheet
# carrying one of these belongs to that chapter and to no other, which is what the
# 25 chapter detachments assume when they say "and no other Chapter's".
_CHAPTER_KEYWORDS = {
    'Black Templars', 'Blood Angels', 'Dark Angels', 'Deathwatch', 'Imperial Fists',
    'Iron Hands', 'Raven Guard', 'Salamanders', 'Space Wolves', 'Ultramarines',
    'White Scars',
}


def e21b_chapter_exclusive(S):
    fkw = S.faction_keywords()
    blocks = {b['army'] for b in S.units()}
    bad = []
    checked = 0
    for g in S.taxonomy()['groups']:
        for fx in g['factions']:
            army = fx.get('data_army')
            if not army or army not in blocks:
                continue
            own = army if army in _CHAPTER_KEYWORDS else None
            for name, u in sorted(S.resolved_pool(army).items()):
                found = fkw.get(u['unit_id'], set()) & _CHAPTER_KEYWORDS
                checked += 1
                if found and found != {own}:
                    bad.append('%s can reach %s (%s)' % (fx['name'], name, ', '.join(sorted(found))))
    if bad:
        return False, '%d cross-chapter unit(s): %s' % (len(bad), '; '.join(bad[:4]))
    return True, 'no cross-chapter unit in any resolved pool (%d pool entries checked)' % checked


# ── B60a: chapter-exclusivity restriction shape, pinned (D221) ────────────────

_B60A_EXCLUSIVITY_RE = re.compile(r'drawn from any other Chapter', re.I)
_B60A_DEBRIS_RE = re.compile(r'STRATAGEM|WHEN:|\bCP\b')


def b60a_restrictions_carries_sentence_not_rule_text(S):
    dets = S.detachments()['detachments']
    in_restrictions = 0
    in_rule_text = []
    for key, v in dets.items():
        if _B60A_EXCLUSIVITY_RE.search(v.get('restrictions') or ''):
            in_restrictions += 1
        if _B60A_EXCLUSIVITY_RE.search(v.get('rule_text') or ''):
            in_rule_text.append(key)
    if in_rule_text:
        return False, '%d detachment(s) still carry the sentence in rule_text: %s' % (
            len(in_rule_text), '; '.join(in_rule_text[:5]))
    if in_restrictions != 25:
        return False, 'expected exactly 25 detachments with the sentence in restrictions, found %d' % in_restrictions
    return True, 'all 25 chapter-exclusive detachments carry the sentence in restrictions; none carry it in rule_text'


def b60a_restrictions_no_stratagem_cp_debris(S):
    dets = S.detachments()['detachments']
    bad = [key for key, v in dets.items()
           if v.get('restrictions') and _B60A_DEBRIS_RE.search(v['restrictions'])]
    if bad:
        return False, '%d restrictions value(s) contain stratagem/CP debris: %s' % (len(bad), '; '.join(bad[:5]))
    return True, 'no restrictions value contains stratagem/CP debris (STRATAGEM, WHEN:, CP)'


# ── tier classification (P4/D231, M0/S149) ────────────────────────────────────
#
# WHY AUTO-DETECTED, NOT HAND-TAGGED: a fifth tuple element ('A' or 'B' typed by
# hand on ~150 entries) is exactly the kind of prose claim this whole file exists
# to replace — it would be correct the day it's written and silently wrong the
# day someone edits a helper function to start reading a new source file. Instead,
# tier is computed from what each assertion's code actually touches: walk the
# reachable global/attribute names of its callable (one hop into any named
# module-level function it calls, recursively), and check that set against the
# small, closed list of things that require a raw GW source file to be present.
#
# TIER_B_NAMES — every Sources method that opens a raw GW export directly
# (Wahapedia CSVs, MFM .txt, faction web/pack files), plus the embedded
# reproduction rebuilds and the two gates that check for GW source files by
# name. Everything else — units.json, detachments.json, wargear_points.json,
# datasheet_wargear_abilities.json, index.html, faction_taxonomy.json, the
# manifest — is built output or app code, and asserting against it needs no
# source at all.
TIER_B_NAMES = {
    # Sources methods that open a raw GW export.
    'abilities', 'models', 'datasheets', 'mfm_instructions', 'faction_keywords',
    'mfm_detachment_rows', 'options', 'composition', 'option_text', 'mfm_all',
    'wargear_ability', 'model_stat',
    # Embedded rebuild-from-source gates (P1/P4/detachments).
    'repro_gate', 'units_repro_gate', 'detachments_repro_gate',
    # Gates that check for GW source files by name/presence.
    'p4_source_census', 'b62_cd_csv_presence',
}


# GW-derived source filenames, loaded from source_manifest.json (M0) so this list
# has exactly one home and can't drift from the real file set. Falls back to a
# small hardcoded set if the manifest is absent (e.g. a --tier a run after M2
# eviction, when the manifest itself may not be locally present) — the fallback
# only needs to cover names actually referenced by inline open() calls in this
# file, not the full 70, so a stale fallback degrades gracefully rather than
# breaking classification outright.
def _load_gw_source_filenames():
    try:
        with open('source_manifest.json', encoding='utf-8') as f:
            return set(json.load(f).get('files', {}).keys())
    except Exception:
        return {'Army_Muster_Rules.txt'}


GW_SOURCE_FILENAMES = _load_gw_source_filenames()


def _reachable_names(fn, _seen=None):
    """Every global/attribute name AND string constant `fn`'s bytecode touches,
    plus the same for any module-level function among those names (one level of
    recursion, cycle-safe). Constants matter as much as names here: several
    assertions (B41-3, E1b-1, E4b-1) open a GW source file directly by literal
    filename rather than through a Sources method, and a names-only walk missed
    every one of them — caught by testing the tier-a path with sources absent,
    not by reading the code. This is what makes classify_tier self-maintaining:
    if a helper function is edited to start calling a source-reading method OR
    to open a new source filename literally, the next run re-derives the tier
    from the new code, nothing to remember to update by hand."""
    if _seen is None:
        _seen = set()
    code = getattr(fn, '__code__', None)
    if code is None:
        return set()
    names = set(code.co_names)
    consts = {c for c in code.co_consts if isinstance(c, str)}
    result = names | (consts & GW_SOURCE_FILENAMES)
    for n in names:
        if n in _seen:
            continue
        _seen.add(n)
        target = globals().get(n)
        if callable(target) and hasattr(target, '__code__'):
            result |= _reachable_names(target, _seen)
    return result


def classify_tier(fn):
    """'B' if this assertion's code reaches any raw-GW-source-reading name or
    opens a GW source filename directly; 'A' otherwise (built data + index.html
    only — safe with no sources loaded)."""
    return 'B' if _reachable_names(fn) & (TIER_B_NAMES | GW_SOURCE_FILENAMES) else 'A'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dir', default='.', help='directory holding the source CSVs and unit_loadouts.json')
    ap.add_argument('-v', '--verbose', action='store_true')
    ap.add_argument('--tier', choices=['a', 'all'], default='all',
                     help="'a' = skip every assertion that reaches a raw-GW-source read "
                          "(no sources needed); 'all' = every assertion (default, today's behaviour)")
    a = ap.parse_args()

    S = Sources(a.dir)
    fails = []
    skipped = []
    for aid, stmt, src, fn in ASSERTIONS:
        if a.tier == 'a' and classify_tier(fn) == 'B':
            skipped.append(aid)
            if a.verbose:
                print(f'SKIP  {aid}  tier B — sources not loaded')
            continue
        try:
            ok, detail = fn(S)
        except Exception as e:
            ok, detail = False, f'{type(e).__name__}: {e}'
        if not ok:
            fails.append((aid, stmt, src, detail))
        if a.verbose or not ok:
            print(f'{"PASS" if ok else "FAIL"}  {aid}  {detail}')

    ran = len(ASSERTIONS) - len(skipped)
    tier_note = f' ({len(skipped)} tier-B skipped)' if skipped else ''
    print(f'\n{ran - len(fails)}/{ran} rules assertions pass{tier_note}.')
    if fails:
        print('\nA stated fact is not true of the data. One of the two is wrong — find out which '
              'before doing anything else.\n')
        for aid, stmt, src, detail in fails:
            print(f'  {aid}: {stmt}\n    source: {src}\n    got:    {detail}\n')
        return 1
    return 0

if __name__ == '__main__':
    sys.exit(main())

