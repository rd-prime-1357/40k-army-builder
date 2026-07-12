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

def base_display(name):
    """Option-facing display form of a matched weapon: drop a ' – <profile>' /
    ' - <profile>' suffix so a multi-profile weapon (e.g. 'Astartes grenade
    launcher – frag') is conferred/gated as the whole weapon ('Astartes grenade
    launcher'), matching the hand-authored convention. Title-case is preserved."""
    return re.sub(r'\s+[–-]\s+\S.*$', '', name).strip()

def qty_name(text):
    """'1 bolt rifle' → 'bolt rifle'; '1 Plasma pistol – standard' → 'plasma pistol'."""
    t = re.sub(r'^\d+\s+', '', text.strip())
    t = t.strip(' .,;')            # drop stray list punctuation ('frag cannon.' -> 'frag cannon')
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

def _is_exact_weapon(raw, idx, global_idx=None):
    """True only if the WHOLE name is an exact base key in the unit or global weapon
    index. Deliberately does NOT use the loose prefix fallback, so 'combi-bolter and
    power fist' is NOT mistaken for 'combi-bolter' — but a real 'and'-named weapon
    like 'Teeth and claws' IS recognised as a single weapon and won't be split."""
    b = base_name(raw)
    if b in idx:
        return True
    if global_idx and b in global_idx:
        return True
    return False

def split_compound_source(raw, idx, global_idx=None):
    """Split a replaced-weapon phrase into parts. 'storm bolter and power fist' ->
    ['storm bolter', 'power fist']; 'Teeth and claws' (a real weapon) -> ['teeth and
    claws']. Only splits when the whole phrase is not itself a known weapon."""
    if _is_exact_weapon(raw, idx, global_idx):
        return [base_name(raw)]
    parts = [p.strip() for p in re.split(r'\s+and\s+', raw.strip()) if p.strip()]
    if len(parts) > 1:
        return [base_name(p) for p in parts]
    return [base_name(raw)]

def split_compound_replacement(raw):
    """Split a replacement phrase into parts. '1 auto boltstorm gauntlets and 1
    fragstorm grenade launcher' -> ['auto boltstorm gauntlets', 'fragstorm grenade
    launcher']. Only splits on ' and ' when every part is count-led ('N weapon'),
    so a single 'and'-named weapon ('1 Slaughter and Carnage - strike') is kept
    whole."""
    parts = [p.strip(' ,') for p in re.split(r'\s*,\s*|\s+and\s+', raw.strip()) if p.strip(' ,')]
    if len(parts) > 1 and all(re.match(r'^\d+\s+\S', p) for p in parts):
        return [qty_name(p) for p in parts]
    return [qty_name(raw)]

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

def _strip_footnote(s):
    return re.sub(r'[\*\u2020\u2021]+', '', s or '')

def _choices_from_list(text, sep=r'\s+(?=\d+\s)'):
    """Split a 'one of the following' list into choices. An item written
    'X and 1 Y' is a compound pick (two weapons at once) and is kept as one
    choice, rendered 'X + Y' -- not split into two bogus single choices."""
    text = _strip_footnote(text)
    # drop a trailing rules note in parentheses, e.g.
    # '... 1 cyclone missile launcher (this model's storm bolter cannot be replaced)'
    text = re.sub(r'\s*\([^)]*\)\s*$', '', text)
    parts = re.split(r'\s+(?=\d+\s)', text.strip())
    merged = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        if merged and re.search(r'\band$', merged[-1]):
            merged[-1] = re.sub(r'\s+and$', '', merged[-1]) + ' + ' + p
        elif merged and merged[-1].endswith(','):
            # '1 boltgun, 1 Astartes shield and 1 close combat weapon' is ONE choice
            # of three weapons, not a choice of 'boltgun' plus something else.
            merged[-1] = merged[-1][:-1].strip() + ' + ' + p
        else:
            merged.append(p)
    out = []
    for item in merged:
        if ' + ' in item:
            out.append(' + '.join(qty_name(w) for w in item.split(' + ')))
        else:
            out.append(qty_name(item))
    return out

def classify_sgl_choice(text, unit_name):
    """'The <group>'s <weapon> can be replaced with one of the following: <list>'"""
    m = re.match(
        r"The (?P<model>.+?)'s (?P<repl>.+?) can be replaced with (?:one|1) of the following[:\s]+(?P<list>.+)",
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
        r"For every (?P<n>\d+) models? in (?:this|the) unit[,.]?\s+(?P<rest>.+)",
        text, re.I)
    if not m:
        return None
    per_n = int(m.group('n'))
    rest = m.group('rest').strip()
    # A conditional per-model scope ('1 model equipped with a bolt rifle can be
    # equipped with ...') carries a requires_weapon gate. Handle the two shapes we
    # see (add / replace); if it's a conditional shape we don't recognise, flag it
    # (return None) rather than fall through to the generic matchers, which would
    # mis-scope 'model equipped with a <weapon>' as the model-group name.
    if re.search(r'\bequipped with an?\b', rest, re.I):
        mc = re.match(
            r"(?:\d+\s+)?models?\s+equipped with an?\s+(?P<req>.+?)\s+"
            r"can be equipped with\s+(?P<what>\d+\s+\S.*?)(?:\.|$)",
            rest, re.I)
        if mc:
            return [{'_type': 'add', '_scope_hint': 'body',
                     'adds': qty_name(mc.group('what')),
                     'per_n_models': per_n, 'max_per_n': 1,
                     'requires_weapon': mc.group('req').strip()}]
        mcr = re.match(
            r"(?:\d+\s+)?models?\s+equipped with an?\s+(?P<req>.+?)\s+"
            r"can replace (?:its|their)\s+(?P<repl>.+?)\s+with\s+(?P<rep>\d+\s+\S.*?)(?:\.|$)",
            rest, re.I)
        if mcr:
            return [{'_type': 'count', '_scope_hint': 'body',
                     'replaces': qty_name(mcr.group('repl')),
                     'replacement': qty_name(mcr.group('rep')),
                     'per_n_models': per_n, 'max_per_n': 1,
                     'requires_weapon': mcr.group('req').strip()}]
        return None
    # passive: '[up to N] <model>'s <weapon> can be replaced with one of the following: <list>'
    m2 = re.match(
        r"(?:up to \d+\s+)?(?:\d+\s+)?(?P<model>.+?)'s? (?P<repl>.+?) can be replaced with (?:one|1) of the following[:\s]+(?P<list>.+)",
        rest, re.I)
    if m2:
        scope_hint = m2.group('model').strip()
        replaces = qty_name(m2.group('repl'))
        choices = _choices_from_list(m2.group('list'))
        if choices:
            return [{'_type': 'count_choice', '_scope_hint': scope_hint,
                     'replaces': replaces, 'replaces_raw': m2.group('repl').strip(),
                     'replacement_choices': choices,
                     'per_n_models': per_n, 'max_per_n': 1}]
    # active: '[up to N] <model> can replace its <weapon> with one of the following: <list>'
    m2a = re.match(
        r"(?:up to \d+\s+)?(?:\d+\s+)?(?P<model>.+?) can replace (?:its|their) (?P<repl>.+?) with (?:one|1) of the following[:\s]+(?P<list>.+)",
        rest, re.I)
    if m2a:
        scope_hint = m2a.group('model').strip()
        replaces = qty_name(m2a.group('repl'))
        choices = _choices_from_list(m2a.group('list'))
        if choices:
            return [{'_type': 'count_choice', '_scope_hint': scope_hint,
                     'replaces': replaces, 'replaces_raw': m2a.group('repl').strip(),
                     'replacement_choices': choices,
                     'per_n_models': per_n, 'max_per_n': 1}]
    # passive single: '[up to N] <model>'s <weapon> can be replaced with <single>'
    m3 = re.match(
        r"(?:up to \d+\s+)?(?:\d+\s+)?(?:model|(?P<model>.+?))'s? (?P<repl>.+?) can be replaced with (?P<rep>\d+\s+\S.*?)$",
        rest, re.I)
    if m3:
        scope_hint = (m3.group('model') or 'body').strip()
        replaces = qty_name(m3.group('repl'))
        replacement = qty_name(m3.group('rep'))
        return [{'_type': 'count', '_scope_hint': scope_hint,
                 'replaces': replaces, 'replaces_raw': m3.group('repl').strip(),
                 'replacement': replacement, 'replacement_raw': m3.group('rep').strip(),
                 'per_n_models': per_n, 'max_per_n': 1}]
    # active single: '[up to N] <model> can replace its <weapon> with <single>'
    m3a = re.match(
        r"(?:up to \d+\s+)?(?:\d+\s+)?(?P<model>.+?) can replace (?:its|their) (?P<repl>.+?) with (?P<rep>\d+\s+\S.*?)$",
        rest, re.I)
    if m3a:
        scope_hint = m3a.group('model').strip()
        replaces = qty_name(m3a.group('repl'))
        replacement = qty_name(m3a.group('rep'))
        return [{'_type': 'count', '_scope_hint': scope_hint,
                 'replaces': replaces, 'replaces_raw': m3a.group('repl').strip(),
                 'replacement': replacement, 'replacement_raw': m3a.group('rep').strip(),
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
    """'Any number of models …' / 'All [of the] models …' / 'Up to N models …',
    including the named-model forms ('Any number of Sternguard Veterans …').
    The scope between the lead-in and 'can … have their' is captured verbatim and
    resolved to a model group later; it need not be the literal word 'models'.
    Source and replacement are passed as raw text so build_loadout can split
    compound weapons ('A and B') with the unit's weapon index in hand."""
    m = re.match(
        r"(?:Any number of|All of the|All|Up to (?P<upto>\d+))\s+"
        r"(?P<scope>.+?)"
        r"(?:\s+in this unit)?"
        r" can (?:each )?(?:have their (?P<repl>.+?) replaced with|replace their (?P<repl2>.+?) with)\s+"
        r"(?:(?:one|1) of the following[:\s]+(?P<list>.+)|(?P<rep>\d+\s+\S.*?)(?:\.|$))",
        text, re.I)
    if not m:
        return None
    up_to = int(m.group('upto')) if m.group('upto') else None
    scope_raw = m.group('scope').strip()
    if re.fullmatch(r'(?:of the |the )?models?|units?', scope_raw, re.I):
        scope_hint = 'body'
    else:
        # tolerate a trailing 'models'/'units' after a named model, if present
        scope_hint = re.sub(r'\s+(?:models?|units?)$', '', scope_raw, flags=re.I).strip() or 'body'
    repl_raw = (m.group('repl') or m.group('repl2') or '').strip()
    if m.group('list'):
        choices = _choices_from_list(m.group('list'))
        if choices:
            return [{'_type': 'any_count_choice', '_scope_hint': scope_hint,
                     'replaces': qty_name(repl_raw), 'replaces_raw': repl_raw,
                     'up_to': up_to, 'replacement_choices': choices}]
    elif m.group('rep'):
        rep_raw = m.group('rep').strip()
        return [{'_type': 'any_count', '_scope_hint': scope_hint,
                 'replaces': qty_name(repl_raw), 'replaces_raw': repl_raw,
                 'up_to': up_to,
                 'replacement': qty_name(rep_raw), 'replacement_raw': rep_raw}]
    return None

def classify_active_swap(text, unit_name):
    """Active-voice replacement (mirror of the passive '<weapon> can be replaced with'):
       'The Kill Team Sergeant can replace its X with one of the following: <list>'
       'The Kill Team Sergeant with Jump Pack can replace its X with 1 Y'
    Only the DEFINITE lead-in ('The'/'This') is handled — that scopes to a named,
    single model (typically the sergeant/leader group), where a plain 'choice'/'single'
    is exactly right. Indefinite single-model swaps ('One model / 1 model can replace
    its X …') need a 1-model cap and are left for a follow-up shape; a conditional
    per-model scope ('One model equipped with a …') is a requires-weapon shape and is
    likewise left for that pass."""
    m = re.match(
        r"(?:The|This)\s+(?P<model>.+?) can replace (?:its|their) (?P<repl>.+?) with"
        r"(?: (?:one|1) of the following[:\s]+(?P<list>.+)|\s+(?P<rep>\d+\s+\S.*?)(?:\.|$))",
        text, re.I)
    if not m:
        return None
    model = m.group('model').strip()
    if re.search(r'\bequipped with a\b', model, re.I):
        return None
    replaces = qty_name(m.group('repl'))
    if m.group('list'):
        choices = _choices_from_list(m.group('list'))
        if not choices:
            return None
        return [{'_type': 'choice', '_scope_hint': model, 'replaces': replaces, 'choices': choices}]
    return [{'_type': 'single', '_scope_hint': model, 'replaces': replaces,
             'replacement': qty_name(m.group('rep'))}]

def classify_one_model_swap(text, unit_name):
    """Indefinite single-model swaps that need a 1-model cap:
       'One model can replace its X with 1 Y'   /   '1 model can replace its X with 1 Y'
    and the conditional (requires-weapon) variant:
       'One model equipped with a W can replace its X with 1 Y'
    A plain choice/count without a cap would let the whole body swap; these are
    capped at exactly one model via max_total:1. The 'equipped with a W' clause is
    carried as requires_weapon — a dormant gate until the engine honours it on
    count options (banked engine turn)."""
    m = re.match(
        r"(?:One|1)\s+model(?:\s+equipped with an?\s+(?P<req>.+?))?"
        r"\s+can replace (?:its|their)\s+(?P<repl>.+?)\s+with\s+(?P<rep>\d+\s+\S.*?)(?:\.|$)",
        text, re.I)
    if not m:
        return None
    op = {'_type': 'count', '_scope_hint': 'body',
          'replaces': qty_name(m.group('repl')),
          'replacement': qty_name(m.group('rep')),
          'max_total': 1}
    if m.group('req'):
        op['requires_weapon'] = m.group('req').strip()
    return [op]

def classify_conditional_add_choice(text, unit_name):
    """'One model equipped with a <weapon> can be equipped with one of the following: …'
    An exclusive one-model equipment choice gated on the bearer still carrying <weapon>.
    Emits one capped add (max_total:1) per list item; all items in the sentence share a
    pool (assigned in build_loadout) so picking one locks out the others, and each carries
    requires_weapon so the whole choice disappears if the bearer weapon is swapped away."""
    m = re.match(
        r"(?:One|1)\s+model\s+equipped with an?\s+(?P<req>.+?)\s+"
        r"can be equipped with (?:one|1) of the following[:\s]+(?P<list>.+)",
        text, re.I)
    if not m:
        return None
    choices = _choices_from_list(m.group('list'))
    if not choices:
        return None
    req = m.group('req').strip()
    return [{'_type': 'add', '_scope_hint': 'body', 'adds': c,
             'requires_weapon': req, 'max_total': 1, '_pool': True}
            for c in choices]

def classify_conditional_add(text, unit_name):
    """'If the <model> is equipped with <req>, it can be equipped with <what>.'
    A single-model conditional add gated on the bearer still carrying <req>. Emits
    one capped add (max_total:1) scoped to <model>, carrying requires_weapon so the
    add disappears if the gate weapon is not present. (Reiver Sergeant: keeps a
    combat knife only when it took the bolt carbine.)"""
    m = re.match(
        r"If (?:the )?(?P<model>.+?) is equipped with (?P<req>\d+\s+\S.*?),?\s+"
        r"it can be equipped with (?P<what>\d+\s+\S.*?)(?:\.|$)",
        text, re.I)
    if not m:
        return None
    return [{'_type': 'add', '_scope_hint': m.group('model').strip(),
             'adds': qty_name(m.group('what')),
             'requires_weapon': qty_name(m.group('req')),
             'max_total': 1}]

def classify_all_models_add(text, unit_name):
    """'All models in this unit can each be equipped with 1 <item>.'
    A unit-wide, per-model item add: every model may independently take one. Emits
    one per-model add per model group (fanned out in build_loadout via _all_groups),
    each capped at one per model (per_n_models 1 / max_per_n 1) so the cap follows
    each group's own size. Separate option lines are independent (not mutually
    exclusive)."""
    m = re.match(
        r"All models in this unit can each be equipped with (?P<what>\d+\s+\S.*?)(?:\.|$)",
        text, re.I)
    if not m:
        return None
    return [{'_type': 'add', '_all_groups': True,
             'adds': qty_name(m.group('what')),
             'per_n_models': 1, 'max_per_n': 1}]

def classify_one_model_add(text, unit_name):
    """'One model can be equipped with N <item>.'  /  '1 model can be equipped with N <item>.'
    An indefinite single-model item add: exactly one model in the unit may take it.
    Body-scoped, capped at one model via max_total:1. Same emission path as classify_add;
    build_loadout resolves <item> to an equipment add when it's a known wargear item
    (e.g. 'Sanguinary Banner') or to a weapon add otherwise. Distinct from
    classify_one_model_swap (verb 'replace', not 'be equipped with')."""
    m = re.match(
        r"(?:One|1)\s+model can be equipped with (?P<what>\d+\s+\S.*?)(?:\.|$)",
        text, re.I)
    if not m:
        return None
    what = qty_name(m.group('what'))
    return [{'_type': 'add', '_scope_hint': 'body', 'adds': what, 'max_total': 1}]

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
        r"This model's (?P<repl>.+?) can be replaced with (?:one|1) of the following[:\s]+(?P<list>.+)",
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
        r"This (?:model|unit) can be equipped with (?:one|1) of the following[:\s]+(?P<list>.+)",
        text, re.I)
    if m:
        choices = _choices_from_list(m.group('list'))
        if choices:
            return [{'_type': 'add_choice', '_scope_hint': 'single',
                     'choices': choices}]
    return None

def classify_n_model_swap(text, unit_name):
    """'1 Tactical Marine's boltgun can be replaced with one of the following: …'
       'N <model>'s X can be replaced with N Y'
       'N of this model's X can be replaced with …'

    N counts models IN THE UNIT, not an allowance per 5 models: a 10-model Tactical
    Squad still gets exactly one special and one heavy weapon. The old form emitted
    per_n_models 5 / max_per_n 1, which doubled every such slot at size 10 and (on a
    1-model unit like the Helbrute) computed zero. Now emits a fixed cap of N via
    max_total, keeping the 'Special Weapon' heading these slots had.

    A compound source ('X and Y can be replaced with…') is carried through as
    replaces_raw and split into a compound 'A + B' source by build_loadout (B23)."""
    m = re.match(
        r"(?P<n>\d+)\s+(?:of\s+)?(?P<model>.+?)'s? (?P<repl>.+?) can be replaced with"
        r"(?: (?:one|1) of the following[:\s]+(?P<list>.+)|\s+(?P<rep>\d+\s+\S.*?)(?:\.|$))",
        text, re.I)
    if not m: return None
    repl_raw = m.group('repl').strip()
    n = int(m.group('n'))
    model = m.group('model').strip().lower()
    if model in ('model', 'models'):
        scope = 'body'
    elif model in ('this model', 'these models'):
        scope = 'single'
    else:
        scope = m.group('model').strip()
    replaces = qty_name(repl_raw)
    if m.group('list'):
        choices = _choices_from_list(m.group('list'))
        if choices:
            return [{'_type': 'count_choice', '_scope_hint': scope,
                     'replaces': replaces, 'replaces_raw': repl_raw,
                     'replacement_choices': choices,
                     'max_total': n, '_special_slot': True}]
    elif m.group('rep'):
        rep_raw = m.group('rep').strip()
        return [{'_type': 'count', '_scope_hint': scope,
                 'replaces': replaces, 'replaces_raw': repl_raw,
                 'replacement': qty_name(rep_raw), 'replacement_raw': rep_raw,
                 'max_total': n, '_special_slot': True}]
    return None

NOTE_PAT = re.compile(
    r'^\*|cannot be taken|only if one|only one|^note:|^designer', re.I)

CLASSIFIERS = [
    classify_conditional_add,
    classify_all_models_add,
    classify_one_model_add,
    classify_sgl_choice,
    classify_sgl_single,
    classify_per_n,
    classify_any_number,
    classify_active_swap,
    classify_one_model_swap,
    classify_conditional_add_choice,
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

def _squash(s):
    return re.sub(r'[^a-z0-9]', '', (s or '').lower())

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
    # squashed fallback: ignore spaces/hyphens ('powerfist' -> 'power fist')
    sq = _squash(b)
    if sq:
        for k, canon in idx.items():
            if _squash(k) == sq:
                return canon, True
        for k, canon in (global_idx or {}).items():
            if _squash(k) == sq:
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
def build_loadout(unit_id, unit_name, comp_rows, size_brackets, weapons_list, option_texts, global_idx=None, equipment_items=None):
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
        # _all_groups ops ('All models in this unit can each be equipped with X')
        # fan out to one per-model add per model group, each scoped to that group so
        # its cap follows the group's own size.
        _expanded = []
        for o in raw_ops:
            if o.get('_all_groups'):
                for g in model_groups:
                    o2 = dict(o); o2.pop('_all_groups'); o2['_scope_hint'] = g['name']
                    _expanded.append(o2)
            else:
                _expanded.append(o)
        raw_ops = _expanded
        # ops flagged _pool from one sentence share a single unit-wide pool cap.
        if any(o.get('_pool') for o in raw_ops):
            _pid = new_id('pool')
            for o in raw_ops:
                if o.get('_pool'):
                    o['pool_id'] = _pid
        for op in raw_ops:
            ot = op['_type']
            scope = resolve_scope(op.get('_scope_hint', 'body'), model_groups)
            # single-model scope: ensure only fixed=1 groups are targeted
            single_group = next((g for g in model_groups if g['name'] == scope and g.get('fixed') == 1), None)
            if ot in ('choice', 'single'):
                # The engine keys a choice's source by exact weapon name, so it cannot
                # yet consume a compound source ('A and B can be replaced with C').
                # Flag it and act on the first weapon only (B23b, engine turn).
                src_parts = split_compound_source(op.get('replaces_raw', op['replaces']), weapon_idx, global_idx)
                if len(src_parts) > 1:
                    flags.append(f'COMPOUND_SOURCE_UNSUPPORTED: {op.get("replaces_raw", op["replaces"])} on {unit_name}')
                repl, ok = normalise_weapon(op['replaces'], weapon_idx, global_idx)
                if not ok: flags.append(f'WEAPON_NOT_FOUND: {op["replaces"]} ({ot}.replaces) on {unit_name}')
                repl = base_display(repl)
                raw_choices = op['choices'] if ot == 'choice' else [op['replacement']]
                choices_out = []
                for c in raw_choices:
                    parts = []
                    for w in c.split(' + '):
                        wn, wok = normalise_weapon(w, weapon_idx, global_idx)
                        if not wok: flags.append(f'WEAPON_NOT_FOUND: {w} ({ot}.choices) on {unit_name}')
                        parts.append(base_display(wn))
                    choices_out.append(' + '.join(parts))
                options.append({'id': new_id('cho' if ot == 'choice' else 'sng'), 'scope': scope,
                                'group': repl.title() + ' Options',
                                'type': 'choice', 'replaces': repl, 'choices': choices_out})
            elif ot in ('count', 'count_choice', 'any_count', 'any_count_choice'):
                is_any = ot.startswith('any_')
                def _norm_parts(parts, ctx):
                    out = []
                    for p in parts:
                        pn, pok = normalise_weapon(p, weapon_idx, global_idx)
                        if not pok: flags.append(f'WEAPON_NOT_FOUND: {p} ({ctx}) on {unit_name}')
                        out.append(base_display(pn))
                    return ' + '.join(out)
                # source (replaces): compound-aware for the whole count family (B23).
                # The engine splits a compound source (' + ') only on multi-model
                # groups; on a fixed-1 group it keys the source by exact name, so a
                # compound there is flagged and reduced to its first weapon.
                src_parts = split_compound_source(op.get('replaces_raw', op['replaces']), weapon_idx, global_idx)
                if len(src_parts) > 1 and single_group:
                    flags.append(f'COMPOUND_SOURCE_ON_SINGLE_GROUP: {op.get("replaces_raw")} on {unit_name}')
                    src_parts = src_parts[:1]
                repl = _norm_parts(src_parts, 'count.replaces')
                per_n = op.get('per_n_models')
                max_pn = op.get('max_per_n', 1)
                is_choice = 'choice' in ot
                # per-N replacements are the datasheet's "special weapon" slot; any-number
                # swaps are their own thing (e.g. power fist -> chainfist), so they get a
                # source-derived heading instead of sharing 'Special Weapon'.
                grp_label = 'Special Weapon' if ((per_n or op.get('_special_slot')) and not is_any) \
                            else (repl.split(' + ')[0].title() + ' Options')
                if is_choice:
                    choices_out = []
                    for c in op['replacement_choices']:
                        choices_out.append(_norm_parts(c.split(' + '), 'count_choice'))
                    entry = {'id': new_id('cc'), 'scope': scope, 'group': grp_label,
                             'type': 'count', 'replaces': repl, 'replacement_choices': choices_out}
                else:
                    rep = _norm_parts(split_compound_replacement(op.get('replacement_raw', op['replacement'])), 'count.rep')
                    entry = {'id': new_id('cnt'), 'scope': scope, 'group': grp_label,
                             'type': 'count', 'replaces': repl, 'replacement': rep}
                if per_n:
                    entry['per_n_models'] = per_n; entry['max_per_n'] = max_pn
                elif op.get('max_total') is not None:
                    # indefinite single-model swap — a fixed cap of exactly N models
                    # ('One model can replace its X with 1 Y').
                    entry['max_total'] = op['max_total']
                else:
                    # 'any number' / 'all' / 'up to N' — cap resolves at render time
                    # to the scoped group's model count (min with up_to when present).
                    entry['max_total_all'] = True
                    if op.get('up_to') is not None:
                        entry['up_to'] = op['up_to']
                if op.get('requires_weapon'):
                    rw, _rwok = normalise_weapon(op['requires_weapon'], weapon_idx, global_idx)
                    entry['requires_weapon'] = base_display(rw)
                options.append(entry)
            elif ot == 'add_choice':
                # "equipped with one of the following" — treated as a single-model choice
                # (no replaces; user picks which to add)
                choices_out = []
                for c in op['choices']:
                    cn, cok = normalise_weapon(c, weapon_idx, global_idx)
                    if not cok: flags.append(f'WEAPON_NOT_FOUND: {c} (add_choice) on {unit_name}')
                    choices_out.append(base_display(cn))
                options.append({'id': new_id('ach'), 'scope': scope, 'group': 'Wargear',
                                'type': 'choice', 'replaces': None, 'choices': choices_out,
                                '_note': 'add_choice: no base weapon replaced; pick one to add'})
            elif ot == 'add':

                what, ok = normalise_weapon(op['adds'], weapon_idx, global_idx)
                # A non-weapon wargear item (e.g. 'Watcher in the Dark') that fails the
                # weapon lookup but is a known equipment/ability item is added as gear,
                # not flagged as a missing weapon.
                as_equipment = (not ok) and equipment_items is not None \
                    and base_name(op['adds']) in equipment_items
                if as_equipment:
                    item = equipment_items[base_name(op['adds'])]
                    entry = {'id': new_id('add'), 'scope': scope, 'group': item,
                             'type': 'add', 'equipment': item}
                    per_n = op.get('per_n_models')
                    if per_n:
                        entry['per_n_models'] = per_n; entry['max_per_n'] = op.get('max_per_n', 1)
                    else:
                        entry['max_total'] = op.get('max_total', 1)
                    if op.get('pool_id'): entry['pool_id'] = op['pool_id']
                    if op.get('requires_weapon'):
                        rw, _rwok = normalise_weapon(op['requires_weapon'], weapon_idx, global_idx)
                        entry['requires_weapon'] = base_display(rw)
                    options.append(entry)
                    continue
                if not ok: flags.append(f'WEAPON_NOT_FOUND: {op["adds"]} (add) on {unit_name}')
                if ok: what = base_display(what)
                per_n = op.get('per_n_models')
                entry = {'id': new_id('add'), 'scope': scope, 'group': what.title(),
                         'type': 'add', 'adds_weapon': what}
                if per_n:
                    entry['per_n_models'] = per_n; entry['max_per_n'] = op.get('max_per_n', 1)
                else:
                    entry['max_total'] = op.get('max_total', 1)
                if op.get('pool_id'): entry['pool_id'] = op['pool_id']
                if op.get('requires_weapon'):
                    rw, _rwok = normalise_weapon(op['requires_weapon'], weapon_idx, global_idx)
                    entry['requires_weapon'] = base_display(rw)
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

    # Equipment allowlist: wargear items that confer abilities but are not weapons
    # (e.g. 'Watcher in the Dark'). base_name -> canonical display name. Sourced from
    # weapon_abilities.json next to this script when present.
    equipment_items = {}
    wa_path = os.path.join(os.path.dirname(os.path.abspath(args.datasheets)) or '.', 'weapon_abilities.json')
    if not os.path.exists(wa_path):
        wa_path = 'weapon_abilities.json'
    if os.path.exists(wa_path):
        try:
            for row in json.load(open(wa_path)):
                nm = row.get('weapon_ability_name') if isinstance(row, dict) else None
                if nm:
                    equipment_items[base_name(nm)] = nm
        except Exception:
            pass

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
            global_idx=global_weapon_idx, equipment_items=equipment_items)
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
