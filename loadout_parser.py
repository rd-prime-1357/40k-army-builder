#!/usr/bin/env python3
"""
loadout_parser.py  —  Prose-to-structured-loadout parser for 40K Army Builder.

Reads Datasheets_options.csv + pipeline units.json output, emits unit_loadouts.json
keyed by unit_id.  Flags any sentence it can't cleanly map to a known pattern.

Usage:
  python3 loadout_parser.py \
    --options   Datasheets_options.csv \
    --units-dir _work/deploy \
    --comp      Datasheets_unit_composition.csv \
    --cost      Datasheets_models_cost.csv \
    --datasheets Datasheets.csv \
    --factions  SM DG \
    --existing  _work/unit_loadouts.json \
    --out       _work/unit_loadouts.json \
    --report    _work/parser_report.md
"""

import argparse, csv, json, re, os
from collections import defaultdict, OrderedDict

# ── helpers ──────────────────────────────────────────────────────────────────
def strip_html(t):
    return re.sub(r'<[^>]+>', ' ', t or '')

def clean(t):
    t = strip_html(t)
    t = t.replace('\u2019', "'").replace('\u2018', "'") \
         .replace('\u201c', '"').replace('\u201d', '"') \
         .replace('\u2013', '-').replace('\u2014', '-') \
         .replace('\u2010', '-').replace('\u2011', '-') \
         .replace('\u2012', '-').replace('\u2015', '-')
    return re.sub(r'\s+', ' ', t).strip()

def base_name(n):
    """Strip profile suffix: 'Plasma pistol – standard' → 'plasma pistol'."""
    n = re.sub(r'\s+[–-]\s+\S.*$', '', n).strip()
    return n.lower()

def qty_name(text):
    """'1 bolt rifle' → 'bolt rifle'; '1 Plasma pistol – standard' → 'plasma pistol'."""
    t = re.sub(r'^\d+\s+', '', text.strip())
    return base_name(t)

def find_weapon(raw, unit_weapons_base, unit_weapons_full):
    """Match a freetext weapon name to a canonical weapon name in the unit's weapon list.
    Returns the canonical name or None."""
    r = base_name(raw)
    if r in unit_weapons_base:
        return unit_weapons_base[r]   # exact base match -> canonical
    # partial: the raw name is a prefix of a canonical base
    for b, canon in unit_weapons_base.items():
        if b.startswith(r) or r.startswith(b):
            return canon
    return None

# ── composition parser ────────────────────────────────────────────────────────
def is_comp_annotation(text):
    """True for composition lines that are notes, not model groups.
    e.g. '10 MODELS MAXIMUM' — a size annotation Wahapedia lists as a comp line."""
    t = text.strip()
    if re.match(r'^\d+\s+models?\s+maximum$', t, re.I):
        return True
    return False

def parse_comp_row(text):
    """'1 Intercessor Sergeant' -> fixed 1
       '4-9 Intercessors'      -> fills_to_size (body range, low >= 1)
       '0-1 Chapter Ancient'   -> optional, min 0, max 1 (build-choice toggle)
       '0-6 Hunting Wolves'    -> optional, min 0, max 6
    Returns a group dict, or None if the line isn't a countable model group."""
    m = re.match(r'^(\d+)(?:-(\d+))?\s+(.+)$', text.strip())
    if not m:
        return None
    lo = int(m.group(1))
    hi = int(m.group(2)) if m.group(2) is not None else None
    name = m.group(3).strip()
    g = {'name': name, 'fixed': None, 'fills': False, 'optional': False, 'max': None}
    if hi is None:
        g['fixed'] = lo                    # single integer -> fixed count
    elif lo == 0:
        g['optional'] = True; g['max'] = hi  # '0-N' -> optional group (toggle / capped)
    else:
        g['fills'] = True                  # 'A-B', A>=1 -> body, fills to size
    return g

# ── sentence classifiers ──────────────────────────────────────────────────────
# Each returns a list of option dicts (possibly empty), or None if no match.

def _choices_from_list(text, sep=r'\s+(?=\d+\s)'):
    """'1 bolt pistol 1 chainsword 1 plasma gun' -> ['bolt pistol','chainsword','plasma gun']"""
    # split on whitespace followed by a digit (new item)
    parts = re.split(r'\s+(?=\d+\s)', text.strip())
    return [qty_name(p) for p in parts if p.strip()]

def classify_sgl_choice(text, unit_name):
    """'The <group>'s <weapon> can be replaced with one of the following: <list>'"""
    m = re.match(
        r"The (?P<model>.+?)'s (?P<repl>.+?) can be replaced with one of the following[:\s]+(?P<list>.+)",
        text, re.I)
    if not m:
        return None
    model = m.group('model').strip()
    replaces = qty_name(m.group('repl'))
    choices_raw = m.group('list').strip()
    choices = _choices_from_list(choices_raw)
    if not choices:
        return None
    return [{'_type': 'choice', '_scope_hint': model, 'replaces': replaces, 'choices': choices}]

def classify_sgl_single(text, unit_name):
    """'The <group>'s <weapon> can be replaced with <single>'"""
    m = re.match(
        r"The (?P<model>.+?)'s (?P<repl>.+?) can be replaced with (?P<rep>\d+\s+\S.*?)$",
        text, re.I)
    if not m:
        return None
    model = m.group('model').strip()
    replaces = qty_name(m.group('repl'))
    replacement = qty_name(m.group('rep'))
    return [{'_type': 'single', '_scope_hint': model, 'replaces': replaces, 'replacement': replacement}]

def classify_per_n(text, unit_name):
    """'For every N models …  X can be replaced with …'"""
    m = re.match(
        r"For every (?P<n>\d+) models? in this unit[,.]?\s+(?P<rest>.+)",
        text, re.I)
    if not m:
        return None
    per_n = int(m.group('n'))
    rest = m.group('rest').strip()
    # replaced with one of the following
    m2 = re.match(
        r"(?:\d+\s+)?(?P<model>.+?)'s? (?P<repl>.+?) can be replaced with one of the following[:\s]+(?P<list>.+)",
        rest, re.I)
    if m2:
        scope_hint = m2.group('model').strip()
        replaces = qty_name(m2.group('repl'))
        choices = _choices_from_list(m2.group('list'))
        if choices:
            return [{'_type': 'count_choice', '_scope_hint': scope_hint,
                     'replaces': replaces, 'replacement_choices': choices,
                     'per_n_models': per_n, 'max_per_n': 1}]
    # replaced with single
    m3 = re.match(
        r"(?:\d+\s+)?(?:model|(?P<model>.+?))'s? (?P<repl>.+?) can be replaced with (?P<rep>\d+\s+\S.*?)$",
        rest, re.I)
    if m3:
        scope_hint = (m3.group('model') or 'body').strip()
        replaces = qty_name(m3.group('repl'))
        replacement = qty_name(m3.group('rep'))
        return [{'_type': 'count', '_scope_hint': scope_hint,
                 'replaces': replaces, 'replacement': replacement,
                 'per_n_models': per_n, 'max_per_n': 1}]
    # equipped with (add)
    m4 = re.match(
        r"(?:\d+\s+)?(?:model|(?P<model>.+?)) can be equipped with (?P<what>\d+\s+\S.*?)$",
        rest, re.I)
    if m4:
        scope_hint = (m4.group('model') or 'body').strip()
        what = qty_name(m4.group('what'))
        return [{'_type': 'add', '_scope_hint': scope_hint,
                 'adds': what, 'per_n_models': per_n, 'max_per_n': 1}]
    return None

def classify_any_number(text, unit_name):
    """'Any number of models …' or 'All models …' or 'Up to N models …'"""
    m = re.match(
        r"(?:Any number of (?:(?P<model>\w[\w\s\-]+?) )?(?:models?|units?)"
        r"|All (?:(?P<model2>\w[\w\s\-]+?) )?(?:models?)"
        r"|Up to \d+ (?:(?P<model3>\w[\w\s\-]+?) )?(?:models?))"
        r"(?:\s+in this unit)?"
        r" can (?:each )?have their (?P<repl>.+?) replaced with"
        r"(?: one of the following[:\s]+(?P<list>.+)|(?P<rep>\d+\s+\S.*?)$)",
        text, re.I)
    if not m:
        return None
    scope_hint = (m.group('model') or m.group('model2') or m.group('model3') or 'body').strip()
    replaces = qty_name(m.group('repl'))
    if m.group('list'):
        choices = _choices_from_list(m.group('list'))
        if choices:
            return [{'_type': 'any_count_choice', '_scope_hint': scope_hint,
                     'replaces': replaces, 'replacement_choices': choices}]
    elif m.group('rep'):
        replacement = qty_name(m.group('rep'))
        return [{'_type': 'any_count', '_scope_hint': scope_hint,
                 'replaces': replaces, 'replacement': replacement}]
    return None

def classify_add(text, unit_name):
    """'This model can be equipped with …'  /  'This unit …'"""
    m = re.match(
        r"(?:This (?:model|unit)|These models?) can be equipped with (?P<what>\d+\s+\S.*?)(?:\.|$)",
        text, re.I)
    if not m:
        return None
    what = qty_name(m.group('what'))
    return [{'_type': 'add', '_scope_hint': 'body', 'adds': what, 'max_total': 1}]


def classify_this_model_choice(text, unit_name):
    """'This model's X can be replaced with one of the following: …'
       'This model's X can be replaced with <single>'"""
    m = re.match(
        r"This model's (?P<repl>.+?) can be replaced with one of the following[:\s]+(?P<list>.+)",
        text, re.I)
    if m:
        choices = _choices_from_list(m.group('list'))
        if choices:
            return [{'_type': 'choice', '_scope_hint': 'single',
                     'replaces': qty_name(m.group('repl')), 'choices': choices}]
    m2 = re.match(
        r"This model's (?P<repl>.+?) can be replaced with (?P<rep>\d+\s+\S.*?)(?:\.|$)",
        text, re.I)
    if m2:
        return [{'_type': 'single', '_scope_hint': 'single',
                 'replaces': qty_name(m2.group('repl')),
                 'replacement': qty_name(m2.group('rep'))}]
    return None

def classify_this_model_add_choice(text, unit_name):
    """'This model can be equipped with one of the following: …'"""
    m = re.match(
        r"This (?:model|unit) can be equipped with one of the following[:\s]+(?P<list>.+)",
        text, re.I)
    if m:
        choices = _choices_from_list(m.group('list'))
        if choices:
            return [{'_type': 'add_choice', '_scope_hint': 'single',
                     'choices': choices}]
    return None

def classify_n_model_swap(text, unit_name):
    """'1 Tactical Marine's boltgun can be replaced with one of the following: …'
       'N <model>'s X can be replaced with …'"""
    m = re.match(
        r"\d+\s+(?P<model>.+?)'s? (?P<repl>.+?) can be replaced with"
        r"(?: one of the following[:\s]+(?P<list>.+)|(?P<rep>\d+\s+\S.*?)(?:\.|$))",
        text, re.I)
    if not m: return None
    scope = m.group('model').strip()
    replaces = qty_name(m.group('repl'))
    if m.group('list'):
        choices = _choices_from_list(m.group('list'))
        if choices:
            return [{'_type': 'count_choice', '_scope_hint': scope,
                     'replaces': replaces, 'replacement_choices': choices,
                     'per_n_models': 5, 'max_per_n': 1}]
    elif m.group('rep'):
        return [{'_type': 'count', '_scope_hint': scope,
                 'replaces': replaces, 'replacement': qty_name(m.group('rep')),
                 'per_n_models': 5, 'max_per_n': 1}]
    return None

NOTE_PAT = re.compile(
    r'^\*|cannot be taken|only if one|only one|^note:|^designer', re.I)

CLASSIFIERS = [
    classify_sgl_choice,
    classify_sgl_single,
    classify_per_n,
    classify_any_number,
    classify_add,
    classify_this_model_choice,
    classify_this_model_add_choice,
    classify_n_model_swap,
]

def parse_sentence(text, unit_name):
    """Return (list_of_raw_ops, flag_reason).  flag_reason is None if parsed cleanly."""
    t = clean(text)
    if not t or t.lower() == 'none' or NOTE_PAT.search(t):
        return [], None   # skip gracefully
    for fn in CLASSIFIERS:
        res = fn(t, unit_name)
        if res is not None:
            return res, None
    return [], f'UNMATCHED: {t[:120]}'

# ── scope resolver ────────────────────────────────────────────────────────────
_LEADER_WORDS = ('sergeant', 'champion', 'superior', 'sarge', 'leader', 'alpha', 'prime')

def _sing(w):
    return w[:-1] if len(w) > 3 and w.endswith('s') else w

def _scope_words(s):
    return set(_sing(w) for w in re.findall(r"[a-z0-9]+", s.lower()))

def resolve_scope(scope_hint, model_groups):
    """Match a scope_hint from option text to one of the unit's parsed model group names.

    Word-based, singular-normalised scoring. A plain body-model hint (e.g.
    'Sternguard Veteran') must resolve to the body group ('Sternguard Veterans'),
    NOT to a leader group whose name merely contains it ('Sternguard Veteran
    Sergeant'). Substring matching got this wrong; scoring by word overlap plus a
    leader/body preference gets it right.
    """
    sh = scope_hint.lower().strip()
    if not model_groups:
        return 'All'
    fills = [g for g in model_groups if g.get('fills')]
    fixed = [g for g in model_groups if g.get('fixed') == 1]
    if sh == 'single':
        return fixed[0]['name'] if fixed else model_groups[0]['name']
    if sh in ('body', 'all', ''):
        return fills[0]['name'] if fills else model_groups[-1]['name']

    hw = _scope_words(sh)
    hint_is_leader = any(w in hw for w in _LEADER_WORDS)
    best, best_score = None, -1
    for g in model_groups:
        gw = _scope_words(g['name'])
        if not gw:
            continue
        if hw == gw:
            score = 100
        elif hw <= gw:
            score = 80 - (len(gw) - len(hw))      # fewer extra words in group = closer
        elif gw <= hw:
            score = 70 - (len(hw) - len(gw))
        else:
            overlap = len(hw & gw)
            if not overlap:
                continue
            score = 40 + overlap - len(gw - hw)
        is_leader_group = (g.get('fixed') == 1)
        if hint_is_leader == is_leader_group:      # leader hint→leader group, body hint→body group
            score += 5
        if score > best_score:
            best_score, best = score, g['name']
    if best is not None:
        return best
    return fills[0]['name'] if fills else (model_groups[-1]['name'] if model_groups else 'All')

# ── weapon normaliser ─────────────────────────────────────────────────────────
def build_weapon_index(unit_weapons_list):
    """base_name -> first canonical full name from unit's weapon list."""
    idx = {}
    for w in unit_weapons_list:
        b = base_name(w)
        if b not in idx:
            idx[b] = w
    return idx

def normalise_weapon(raw, idx, global_idx=None):
    """Map a parsed weapon name to canonical form. Falls back to global index then strips plural s."""
    b = base_name(raw)
    if b in idx:
        return idx[b], True
    # prefix fallback within unit
    for k, canon in idx.items():
        if k.startswith(b) or b.startswith(k):
            return canon, True
    # global index fallback
    if global_idx:
        if b in global_idx:
            return global_idx[b], True
        # strip trailing s (lascannons -> lascannon)
        bs = b.rstrip('s')
        if bs and bs in global_idx:
            return global_idx[bs], True
        # prefix fallback in global
        for k, canon in global_idx.items():
            if k.startswith(b) or b.startswith(k):
                return canon, True
    return raw.title(), False

# ── OR alternative-profile merge ────────────────────────────────────────────────
def _norm_group_key(name):
    """Normalise a group name for cross-profile alignment: lowercase, strip a
    trailing footnote marker, and singular/plural-fold the last word incl. the
    irregular -ves plural (wolves -> wolf)."""
    n = re.sub(r'[\*\u2020\u2021]+$', '', name.strip()).lower()
    words = n.split()
    if words:
        last = words[-1]
        if last.endswith('ves'):
            last = last[:-3] + 'f'
        elif last.endswith('s') and len(last) > 1:
            last = last[:-1]
        words[-1] = last
    return ' '.join(words)

def merge_or_profiles(profiles, size_brackets, flags):
    """Fold N alternative composition profiles (split on a bare 'OR' line) into
    one group list. Profile i maps to size bracket i. A group whose count is the
    same across all profiles becomes a fixed count; a group whose count varies
    becomes a per-bracket count keyed by bracket size. This is more faithful to
    the rules than a fills-to-size body: in an OR unit each bracket is one exact
    legal composition."""
    lengths = {len(p) for p in profiles}
    if len(lengths) != 1:
        flags.append(f'OR_PROFILE_SHAPE_MISMATCH: profiles have group counts {sorted(len(p) for p in profiles)}; using first profile only')
        return profiles[0]
    ngroups = lengths.pop()
    if len(profiles) != len(size_brackets):
        flags.append(f'OR_PROFILE_BRACKET_MISMATCH: {len(profiles)} profiles vs {len(size_brackets)} brackets')
    # canonical name per position: from the profile with the largest total count
    totals = [sum((g.get('fixed') or 0) for g in p) for p in profiles]
    canon_idx = totals.index(max(totals))
    # sanity: each profile's total should equal its bracket
    for i, p in enumerate(profiles):
        if i < len(size_brackets) and totals[i] != size_brackets[i]:
            flags.append(f'OR_PROFILE_SUM_MISMATCH: profile {i} sums {totals[i]} != bracket {size_brackets[i]}')
    merged = []
    for j in range(ngroups):
        keys = {_norm_group_key(profiles[i][j]['name']) for i in range(len(profiles))}
        if len(keys) != 1:
            flags.append(f'OR_PROFILE_NAME_MISMATCH at position {j}: {[profiles[i][j]["name"] for i in range(len(profiles))]}')
        name = profiles[canon_idx][j]['name']
        counts = [profiles[i][j].get('fixed') for i in range(len(profiles))]
        g = {'name': name, 'fixed': None, 'fills': False, 'optional': False, 'max': None, 'per_bracket': None}
        if len(set(counts)) == 1:
            g['fixed'] = counts[0]
        else:
            g['per_bracket'] = {str(size_brackets[i]): counts[i] for i in range(len(profiles)) if i < len(size_brackets)}
        merged.append(g)
    return merged

# ── main per-unit assembler ────────────────────────────────────────────────────
def build_loadout(unit_id, unit_name, comp_rows, size_brackets, weapons_list, option_texts, global_idx=None):
    flags = []
    # model groups — split composition into alternative profiles on a bare 'OR',
    # skipping annotation lines ('N MODELS MAXIMUM').
    profiles = [[]]
    for row in comp_rows:
        if row.strip().upper() == 'OR':
            profiles.append([])
            continue
        if is_comp_annotation(row):
            continue
        p = parse_comp_row(row)
        if p:
            profiles[-1].append(p)
        else:
            flags.append(f'COMP_PARSE_FAIL: {row}')
    profiles = [p for p in profiles if p]
    if not profiles:
        flags.append('NO_MODEL_GROUPS')
        return None, flags
    if len(profiles) == 1:
        model_groups = profiles[0]
    else:
        model_groups = merge_or_profiles(profiles, size_brackets, flags)
    if not model_groups:
        flags.append('NO_MODEL_GROUPS')
        return None, flags

    weapon_idx = build_weapon_index(weapons_list)

    # default_weapons: base-equipment weapons per group
    # For now assign all base weapons to all groups; the parser can't reliably
    # split defaults per group without per-model data, so we mark that for review.
    base_weapons = list(weapons_list[:0])   # start empty; filled from is_base in pipeline

    options = []
    opt_id_counter = [0]
    def new_id(prefix):
        opt_id_counter[0] += 1
        return f'{prefix}_{opt_id_counter[0]}'

    for raw_text in option_texts:
        raw_ops, flag = parse_sentence(raw_text, unit_name)
        if flag:
            flags.append(flag)
            continue
        for op in raw_ops:
            ot = op['_type']
            scope = resolve_scope(op.get('_scope_hint', 'body'), model_groups)
            # single-model scope: ensure only fixed=1 groups are targeted
            single_group = next((g for g in model_groups if g['name'] == scope and g.get('fixed') == 1), None)
            if ot == 'choice':
                repl, ok = normalise_weapon(op['replaces'], weapon_idx, global_idx)
                if not ok: flags.append(f'WEAPON_NOT_FOUND: {op["replaces"]} (choice.replaces) on {unit_name}')
                choices_out = []
                for c in op['choices']:
                    cn, cok = normalise_weapon(c, weapon_idx, global_idx)
                    if not cok: flags.append(f'WEAPON_NOT_FOUND: {c} (choice) on {unit_name}')
                    choices_out.append(cn)
                options.append({'id': new_id('cho'), 'scope': scope, 'group': repl.title() + ' Options',
                                'type': 'choice', 'replaces': repl, 'choices': choices_out})
            elif ot == 'single':
                repl, ok = normalise_weapon(op['replaces'], weapon_idx, global_idx)
                if not ok: flags.append(f'WEAPON_NOT_FOUND: {op["replaces"]} (single.replaces) on {unit_name}')
                rep, ok2 = normalise_weapon(op['replacement'], weapon_idx, global_idx)
                if not ok2: flags.append(f'WEAPON_NOT_FOUND: {op["replacement"]} (single.replacement) on {unit_name}')
                options.append({'id': new_id('sng'), 'scope': scope, 'group': repl.title() + ' Options',
                                'type': 'choice', 'replaces': repl, 'choices': [rep]})
            elif ot in ('count', 'count_choice', 'any_count', 'any_count_choice'):
                repl, ok = normalise_weapon(op['replaces'], weapon_idx, global_idx)
                if not ok: flags.append(f'WEAPON_NOT_FOUND: {op["replaces"]} (count.replaces) on {unit_name}')
                per_n = op.get('per_n_models')
                max_pn = op.get('max_per_n', 1)
                is_choice = 'choice' in ot
                if is_choice:
                    choices_out = []
                    for c in op['replacement_choices']:
                        cn, cok = normalise_weapon(c, weapon_idx, global_idx)
                        if not cok: flags.append(f'WEAPON_NOT_FOUND: {c} (count_choice) on {unit_name}')
                        choices_out.append(cn)
                    entry = {'id': new_id('cc'), 'scope': scope, 'group': 'Special Weapon',
                             'type': 'count', 'replaces': repl, 'replacement_choices': choices_out}
                else:
                    rep, ok2 = normalise_weapon(op['replacement'], weapon_idx, global_idx)
                    if not ok2: flags.append(f'WEAPON_NOT_FOUND: {op["replacement"]} (count.rep) on {unit_name}')
                    entry = {'id': new_id('cnt'), 'scope': scope, 'group': 'Special Weapon',
                             'type': 'count', 'replaces': repl, 'replacement': rep}
                if per_n:
                    entry['per_n_models'] = per_n; entry['max_per_n'] = max_pn
                else:
                    # 'any number' / 'all' — use unit size as total max; mark for review
                    entry['max_total_all'] = True
                    flags.append(f'REVIEW_MAX_TOTAL: {unit_name} — "any/all" scope needs max_total set')
                options.append(entry)
            elif ot == 'add_choice':
                # "equipped with one of the following" — treated as a single-model choice
                # (no replaces; user picks which to add)
                choices_out = []
                for c in op['choices']:
                    cn, cok = normalise_weapon(c, weapon_idx, global_idx)
                    if not cok: flags.append(f'WEAPON_NOT_FOUND: {c} (add_choice) on {unit_name}')
                    choices_out.append(cn)
                options.append({'id': new_id('ach'), 'scope': scope, 'group': 'Wargear',
                                'type': 'choice', 'replaces': None, 'choices': choices_out,
                                '_note': 'add_choice: no base weapon replaced; pick one to add'})
            elif ot == 'add':

                what, ok = normalise_weapon(op['adds'], weapon_idx, global_idx)
                if not ok: flags.append(f'WEAPON_NOT_FOUND: {op["adds"]} (add) on {unit_name}')
                per_n = op.get('per_n_models')
                entry = {'id': new_id('add'), 'scope': scope, 'group': what.title(),
                         'type': 'add', 'adds_weapon': what}
                if per_n:
                    entry['per_n_models'] = per_n; entry['max_per_n'] = op.get('max_per_n', 1)
                else:
                    entry['max_total'] = op.get('max_total', 1)
                options.append(entry)

    def emit_count(g):
        if g.get('per_bracket'):
            return {'per_bracket': g['per_bracket']}
        if g.get('optional'):
            return {'optional': True, 'max': g.get('max')}
        if g.get('fixed') is not None:
            return {'fixed': g['fixed']}
        return {'fills_to_size': True}

    defn = {
        'size_brackets': size_brackets,
        'model_groups': [
            {'name': g['name'],
             'count': emit_count(g),
             'default_weapons': []}   # populated below from pipeline's is_base field
            for g in model_groups
        ],
        'options': options,
        '_parser_flags': flags,
    }
    return defn, flags

# ── entry point ────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--options', required=True)
    ap.add_argument('--units-dir', required=True)
    ap.add_argument('--comp', required=True)
    ap.add_argument('--cost', required=True)
    ap.add_argument('--datasheets', required=True)
    ap.add_argument('--factions', nargs='+', default=['SM', 'DG'])
    ap.add_argument('--existing', default=None)
    ap.add_argument('--out', required=True)
    ap.add_argument('--report', default='parser_report.md')
    args = ap.parse_args()

    fac_ids = set(args.factions)
    ds_fac = {}; ds_name = {}; ds_by_name = defaultdict(list)
    for r in csv.reader(open(args.datasheets), delimiter='|'):
        if len(r) > 2:
            ds_fac[r[0]] = r[2]; ds_name[r[0]] = r[1]; ds_by_name[r[1]].append(r[0])

    # composition
    comp = defaultdict(list)
    for r in csv.reader(open(args.comp), delimiter='|'):
        if len(r) >= 3 and ds_fac.get(r[0]) in fac_ids:
            t = clean(r[2])
            if t: comp[r[0]].append(t)

    # size brackets
    sizes = defaultdict(list)
    for r in csv.reader(open(args.cost), delimiter='|'):
        if len(r) >= 3 and ds_fac.get(r[0]) in fac_ids:
            m = re.search(r'(\d+)', r[2])
            if m:
                s = int(m.group(1))
                if s not in sizes[r[0]]: sizes[r[0]].append(s)

    # option texts per datasheet
    opts_by_ds = defaultdict(list)
    for r in csv.reader(open(args.options), delimiter='|'):
        if len(r) >= 4 and ds_fac.get(r[0]) in fac_ids:
            t = clean(r[3])
            if t and t.lower() != 'none': opts_by_ds[r[0]].append(t)

    # weapons + base flags from pipeline units.json
    unit_weapons = {}  # unit_id -> [weapon_name, ...]
    unit_base_weapons = {}  # unit_id -> [base_weapon_name, ...]
    units_json = os.path.join(args.units_dir, 'units.json')
    if os.path.exists(units_json):
        data = json.load(open(units_json))
        for blk in data:
            for u in blk['units']:
                uid = u.get('unit_id')
                if uid:
                    unit_weapons[uid] = [w['weapon_name'] for w in u.get('weapons', [])]
                    unit_base_weapons[uid] = [w['weapon_name'] for w in u.get('weapons', []) if w.get('is_base_equipment')]

    # load existing hand-authored definitions (preserve them; parser only adds new ones)
    existing = {}
    if args.existing and os.path.exists(args.existing):
        raw_existing = json.load(open(args.existing))
        for k, v in raw_existing.items():
            if k.startswith('_'): continue
            existing[k] = v

    out = OrderedDict()
    out['_schema'] = ('Structured loadout definitions keyed by unit_id. '
                      'Hand-authored entries are preserved. Parser-generated entries carry '
                      '_parser_flags listing any sentences that were unmatched or need review.')
    out.update(existing)

    all_flags = []
    parsed = 0; skipped = 0; preserved = 0

    target_ids = [uid for uid, fid in ds_fac.items() if fid in fac_ids]
    # Global weapon index: base_name -> canonical name, across ALL units in pipeline output
    global_weapon_idx = {}
    if os.path.exists(units_json):
        data2 = json.load(open(units_json))
        for blk in data2:
            for u in blk['units']:
                for w in u.get('weapons', []):
                    b = base_name(w['weapon_name'])
                    if b not in global_weapon_idx:
                        global_weapon_idx[b] = w['weapon_name']

    for uid in sorted(target_ids):
        name = ds_name.get(uid, '')
        if uid in existing:
            preserved += 1
            continue
        if not opts_by_ds.get(uid) and not comp.get(uid):
            skipped += 1
            continue
        weapons_list = unit_weapons.get(uid, [])
        base_ws = unit_base_weapons.get(uid, [])
        sz = sizes.get(uid, [])
        defn, flags = build_loadout(
            uid, name, comp.get(uid, []), sz, weapons_list, opts_by_ds.get(uid, []),
            global_idx=global_weapon_idx)
        if defn:
            # fill default_weapons from pipeline base flags
            for g in defn['model_groups']:
                g['default_weapons'] = base_ws  # same set for all groups (review flag set if needed)
            out[uid] = defn
            if flags:
                all_flags.append((uid, name, flags))
            parsed += 1

    json.dump(out, open(args.out, 'w'), indent=2, ensure_ascii=False)

    # report
    with open(args.report, 'w') as f:
        f.write(f'# Loadout Parser Report\n\n')
        f.write(f'Preserved (hand-authored): {preserved}  \n')
        f.write(f'Parsed: {parsed}  \n')
        f.write(f'Skipped (no data): {skipped}  \n')
        f.write(f'Units with flags needing review: {len(all_flags)}  \n\n')
        if all_flags:
            f.write('## Flagged units\n\n')
            for uid, name, flags in all_flags:
                f.write(f'### {name} ({uid})\n')
                for fl in flags:
                    f.write(f'- {fl}\n')
                f.write('\n')

    print(f'Done. Preserved: {preserved} | Parsed: {parsed} | Skipped: {skipped}')
    print(f'Flagged for review: {len(all_flags)} units — see {args.report}')

if __name__ == '__main__':
    main()
