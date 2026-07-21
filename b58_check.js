// b58_check.js — B58 phase 2. Pulls loOptCounts / loOptHeadroom / loOptMax /
// loGroupCounts straight out of index.html and checks the banded optional model
// groups resolve to a legal mix at every reachable step.
// Usage: node b58_check.js index.html unit_loadouts.json
const fs = require('fs');
const src = fs.readFileSync(process.argv[2] || 'index.html', 'utf8');
const lines = src.split('\n');
function slice(a, b) {
  const s = lines.findIndex(l => l.includes(a));
  const e = lines.findIndex((l, i) => i > s && l.includes(b));
  return lines.slice(s, e).join('\n');
}
const block = slice('function loOptCounts', 'requires_weapon: carrier counting');
const E = new Function(block + '\nreturn {loOptCounts,loOptHeadroom,loOptMax,loGroupCounts};')();
const L = JSON.parse(fs.readFileSync(process.argv[3] || 'unit_loadouts.json', 'utf8'));

let pass = 0, fail = 0;
function check(label, got, want) {
  const ok = JSON.stringify(got) === JSON.stringify(want);
  if (ok) pass++; else { fail++; console.log('FAIL', label, 'got', JSON.stringify(got), 'want', JSON.stringify(want)); }
}
const entry = w => ({ wargear: w });

// ── 1. headroom = size - fixed - base min, for the four D179 kill teams ──
check('fortis headroom @10',     E.loOptHeadroom(L['000002780'], 10), 7);
check('spectrus headroom @10',   E.loOptHeadroom(L['000002779'], 10), 7);
check('indomitor headroom @10',  E.loOptHeadroom(L['000002781'], 10), 7);
check('talonstrike headroom @10',E.loOptHeadroom(L['000003874'], 10), 7);

// ── 2. loOptCounts returns a count, clamped to the band max ──
{
  const def = L['000002780'];
  const oc = E.loOptCounts(def, entry({
    'opt_Kill Team Intercessors with plasma incinerators': 3,
    'opt_Kill Team Intercessors with superfrag rocket launchers': 9  // band max 2
  }));
  check('band count kept',    oc['Kill Team Intercessors with plasma incinerators'], 3);
  check('band max clamps',    oc['Kill Team Intercessors with superfrag rocket launchers'], 2);
  check('unset band is 0',    oc['Kill Team Intercessors with pyreblasters'], 0);
}

// ── 3. a legal Fortis mix resolves, body group never falls under its minimum ──
{
  const def = L['000002780'];
  const oc = E.loOptCounts(def, entry({
    'opt_Kill Team Intercessors with plasma incinerators': 4,
    'opt_Kill Team Intercessors with heavy bolt pistols': 3
  }));
  const c = E.loGroupCounts(def, 10, oc);
  check('fortis sergeant', c['Kill Team Sergeant'], 1);
  check('fortis plasma',   c['Kill Team Intercessors with plasma incinerators'], 4);
  check('fortis hbp',      c['Kill Team Intercessors with heavy bolt pistols'], 3);
  check('fortis body @min', c['Kill Team Intercessors'], 2);
  const total = def.model_groups.reduce((a, g) => a + c[g.name], 0);
  check('fortis total = 10', total, 10);
}

// ── 4. over-spent bands are trimmed in order; body never drops below min ──
{
  const def = L['000002780'];
  const oc = E.loOptCounts(def, entry({
    'opt_Kill Team Intercessors with plasma incinerators': 4,
    'opt_Kill Team Intercessors with heavy bolt pistols': 4,
    'opt_Kill Team Intercessors with pyreblasters': 4,
    'opt_Kill Team Intercessors with superfrag rocket launchers': 2
  }));
  const c = E.loGroupCounts(def, 10, oc);
  const total = def.model_groups.reduce((a, g) => a + c[g.name], 0);
  check('overspend total = 10', total, 10);
  check('overspend body >= min', c['Kill Team Intercessors'] >= 2, true);
  check('overspend first band full', c['Kill Team Intercessors with plasma incinerators'], 4);
  check('overspend second band trimmed', c['Kill Team Intercessors with heavy bolt pistols'], 3);
  check('overspend third band zero', c['Kill Team Intercessors with pyreblasters'], 0);
}

// ── 5. loOptMax narrows as siblings fill up ──
{
  const def = L['000002780'];
  check('plasma max, nothing taken',
    E.loOptMax(def, 10, {}, 'Kill Team Intercessors with plasma incinerators'), 4);
  check('plasma max, 5 taken elsewhere',
    E.loOptMax(def, 10, { 'Kill Team Intercessors with heavy bolt pistols': 5 },
               'Kill Team Intercessors with plasma incinerators'), 2);
  check('plasma max, 7 taken elsewhere',
    E.loOptMax(def, 10, { 'Kill Team Intercessors with heavy bolt pistols': 4,
                          'Kill Team Intercessors with pyreblasters': 3 },
               'Kill Team Intercessors with plasma incinerators'), 0);
}

// ── 6. every band at its own max is still legal for Talonstrike (band binds, not headroom) ──
{
  const def = L['000003874'];
  const oc = E.loOptCounts(def, entry({ 'opt_Kill Team Heavy Intercessors with Jump Packs': 5 }));
  const c = E.loGroupCounts(def, 10, oc);
  check('talonstrike variant', c['Kill Team Heavy Intercessors with Jump Packs'], 5);
  check('talonstrike body', c['Kill Team Intercessors with Jump Packs'], 4);
}

// ── 7. B13 regression — Victrix Honour Guard, two one-band Epic Heroes ──
{
  const def = L['000004185'];
  const oc = E.loOptCounts(def, entry({
    'opt_Chapter Ancient - EPIC HERO': 1, 'opt_Chapter Champion - EPIC HERO': 1 }));
  const c = E.loGroupCounts(def, 3, oc);
  check('victrix ancient @3', c['Chapter Ancient - EPIC HERO'], 1);
  check('victrix champion @3', c['Chapter Champion - EPIC HERO'], 1);
  check('victrix body @3', c['Victrix Honour Guard'], 1);
  const c6 = E.loGroupCounts(def, 6, oc);
  check('victrix body @6', c6['Victrix Honour Guard'], 4);
}

// ── 8. B56g regression — Hunting Wolves escort rides alongside the bracket ──
{
  const def = L['000004131'];
  const on = E.loOptCounts(def, entry({ 'opt_Hunting Wolves': 1 }));
  check('escort flag stays 1', on['Hunting Wolves'], 1);
  const c3 = E.loGroupCounts(def, 3, on);
  check('hunting wolves on @3', c3['Hunting Wolves'], 3);
  check('headtakers unchanged @3', c3['Wolf Guard Headtakers'], 3);
  const c6 = E.loGroupCounts(def, 6, on);
  check('hunting wolves on @6', c6['Hunting Wolves'], 6);
  check('headtakers unchanged @6', c6['Wolf Guard Headtakers'], 6);
  const off = E.loGroupCounts(def, 3, E.loOptCounts(def, entry({})));
  check('hunting wolves off @3', off['Hunting Wolves'], 0);
}

// ── 9. Invader ATV — non_consuming, rides alongside the bracket, never
// competes for headroom (B59b/D182). Reachable at EVERY bracket, not gated to
// the top bracket the way a per_bracket escort would be — the withdrawn
// per_bracket shape this section previously pinned would have kept the ATV
// wrongly unreachable at size 3 (headroom there is 0, fully claimed by the
// Outriders fills_to_size minimum); non_consuming is exactly what fixes that.
{
  const def = L['000002712'];
  check('ATV headroom @3', E.loOptHeadroom(def, 3), 0);
  check('ATV headroom @6', E.loOptHeadroom(def, 6), 3);
  const oc = E.loOptCounts(def, entry({ 'opt_Invader ATV': 1 }));
  check('ATV reachable @3', E.loGroupCounts(def, 3, oc)['Invader ATV'], 1);
  check('ATV reachable @6', E.loGroupCounts(def, 6, oc)['Invader ATV'], 1);
  check('outriders @3 respect min', E.loGroupCounts(def, 3, oc)['Outriders'], 2);
  check('outriders @6 unaffected by ATV', E.loGroupCounts(def, 6, oc)['Outriders'], 5);
}

// ── 10. global: no unit, at any bracket, with every band maxed, produces a body
// group below its composition minimum or a total over the bracket size ──
for (const uid of Object.keys(L)) {
  const def = L[uid];
  if (!def || !def.model_groups) continue;
  const opts = def.model_groups.filter(g => (g.count || {}).optional);
  if (!opts.length) continue;
  for (const size of (def.size_brackets || [])) {
    const w = {};
    for (const g of opts) w['opt_' + g.name] = 99;
    const c = E.loGroupCounts(def, size, E.loOptCounts(def, entry(w)));
    let total = 0;
    for (const g of def.model_groups) {
      const ct = g.count || {};
      total += (ct.optional && (ct.per_bracket || ct.non_consuming)) ? 0 : c[g.name];
      if (ct.fills_to_size && ct.min != null)
        check(`${uid}@${size} ${g.name} >= min`, c[g.name] >= ct.min, true);
    }
    check(`${uid}@${size} total = size`, total, size);
  }
}

console.log(`b58_check: ${pass} pass, ${fail} fail`);
process.exit(fail ? 1 : 0);
