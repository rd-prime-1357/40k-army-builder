// b103_check.js — B103. A non-distinct `replacement_choices` tally must never roll
// up past its cap, and must never be left sitting over the cap in storage.
//
// The defect (v6.25 and earlier): `loRollup`'s MULTI-MODEL branch pushed every
// tallied pick into `emit` in full and clamped only the running total afterwards.
// Two consequences, both live on shipped data:
//
//   1. more replacement weapons were emitted — and priced — than the cap allows;
//   2. `chargeSource` was handed the CLAMPED total, so the per-source-weapon check
//      below it never saw the overrun and `overAllocated` stayed false. The list
//      read clean while being wrong.
//
// The FIXED-1 branch clamped differently again (it bounded each pick against the
// remaining cap as it went), so the two branches disagreed on the same shape.
//
// Reachability matters and is pinned here: `editLoadoutChoiceCount` refuses to step
// past the cap, so the UI cannot build an over-cap tally. `editSizeIdx` moves the
// size bracket, recalculates points and never touches `entry.wargear` — and a
// `per_n_models` cap scales with the bracket. Build big, fill to the ceiling, shrink:
// that is the whole population, and it is why this ticket moves the points of
// already-saved lists.
//
// Three things are gated:
//
//   * both rollup branches now bound each pick against the remaining cap, and both
//     truncate in the OPTION'S OWN choice order — not storage insertion order, which
//     is click order and is not stable across an export/reimport round trip. Same
//     reasoning as `loDistinctPicks`.
//   * a tally that FITS its cap is untouched by all of this. That is the safety
//     property the whole ticket rests on and it is asserted directly, on every
//     shipped option at every bracket.
//   * `loHealChoiceTallies` removes the over-cap state from storage rather than
//     leaving it there to be clamped on the way out (D0). Without it the stepper —
//     which reads `entry.wargear` raw — would show more picks than the rollup
//     honours.
//
// Clamping is SILENT. `overAllocated` is not fired: under D0 the state was never
// legal, so there is nothing to warn about, and that flag's message is about
// same-source contention. The precedent is B34, whose size-gated picks are already
// cleared silently on a size change.
//
// Build-time only; not part of the served app.
// Usage: node b103_check.js [index.html] [unit_loadouts.json] [units.json] [wargear_points.json]

const fs = require('fs');

function slice(lines, startNeedle, endNeedle) {
  const s = lines.findIndex(l => l.includes(startNeedle));
  const e = lines.findIndex(l => l.includes(endNeedle));
  if (s < 0 || e < 0 || e <= s) throw new Error(`slice failed: ${startNeedle} .. ${endNeedle}`);
  return lines.slice(s, e).join('\n');
}

function loadEngine(path) {
  const lines = fs.readFileSync(path, 'utf8').split('\n');
  // The rollup block carries loMaxCount, loDistinctPicks, loHealChoiceTallies,
  // loGroupCounts and loRollup itself.
  const rollup = slice(lines, 'function loMaxCount', '// Unit Options UI for loadout-defined units.');
  const cost   = slice(lines, 'function wargearCostForRollup', 'function ptsForEntry');
  const editor = slice(lines, 'function editLoadoutChoiceCount', 'function editLoadoutAdd');
  const prelude = `const PROFILE_SEP=/\\s[\u2013\\-\u00e2]\\s/;
function stripProfile(n){return String(n||'').split(PROFILE_SEP)[0].trim();}
function weaponBase(n){return stripProfile(n).toLowerCase();}
let wargearPoints = {};
let armyList = [];
function renderAll(){}`;
  return new Function(prelude + cost + '\n' + rollup + '\n' + editor +
    '\nreturn { loRollup, loMaxCount, loGroupCounts, loDistinctCap, loChoiceGroupCap,' +
    ' loHealChoiceTallies, wargearCostForRollup, editLoadoutChoiceCount,' +
    ' setWP:(w)=>{wargearPoints=w;}, setList:(l)=>{armyList=l;} };')();
}

const E     = loadEngine(process.argv[2] || 'index.html');
const LO    = JSON.parse(fs.readFileSync(process.argv[3] || 'unit_loadouts.json', 'utf8'));
const UNITS = JSON.parse(fs.readFileSync(process.argv[4] || 'units.json', 'utf8'));
const WP    = JSON.parse(fs.readFileSync(process.argv[5] || 'wargear_points.json', 'utf8'));
E.setWP(WP);

let fail = 0;
const ok = (cond, msg) => { if (!cond) { fail++; console.log('  FAIL ' + msg); } else console.log('  ok   ' + msg); };
const eq = (msg, got, want) => ok(got === want, `${msg}: got ${JSON.stringify(got)} want ${JSON.stringify(want)}`);

const sel = (counts) => ({ choiceById: {}, countById: counts || {}, addById: {} });
const w   = (roll, name) => (roll.weapons.get(name) || 0) + (roll.equipment.get(name) || 0);
const dump = (roll) => JSON.stringify([[...roll.weapons].sort(), [...roll.equipment].sort()]);
const sum = (t) => Object.keys(t || {}).reduce((a, k) => a + Math.max(0, Number(t[k]) | 0), 0);

// ── fixtures ───────────────────────────────────────────────────────────────
// A 3-choice swap on a body group, capped 1 per 5 models: cap 2 at size 10, cap 1
// at size 5. That is the real shape of Terminator Squad cc_1, Strike Squad cc_1 and
// twenty-odd others — build at 10, fill to 2, drop to 5.
const CH3 = ['Alpha', 'Bravo', 'Charlie'];
const bodyDef = (extra) => ({
  size_brackets: [5, 10],
  model_groups: [
    { name: 'Sergeant', count: { fixed: 1 }, default_weapons: ['Bolt pistol', 'Chainsword'] },
    { name: 'Troopers', count: { fills_to_size: true, min: 4 }, default_weapons: ['Bolt pistol', 'Chainsword'] }
  ],
  options: [Object.assign({
    id: 'cc_b', scope: 'Troopers', group: 'Chainsword Options', type: 'count',
    replaces: 'Chainsword', replacement_choices: CH3.slice(), per_n_models: 5
  }, extra || {})]
});
// The same option parked on the fixed-1 group — the other branch entirely.
const leaderDef = (extra) => ({
  size_brackets: [5, 10],
  model_groups: [
    { name: 'Sergeant', count: { fixed: 1 }, default_weapons: ['Bolt pistol', 'Chainsword'] },
    { name: 'Troopers', count: { fills_to_size: true, min: 4 }, default_weapons: ['Bolt pistol', 'Chainsword'] }
  ],
  options: [Object.assign({
    id: 'cc_l', scope: 'Sergeant', group: 'Chainsword Options', type: 'count',
    replaces: 'Chainsword', replacement_choices: CH3.slice(), max_total_all: true, up_to: 3
  }, extra || {})]
});

// ── 1. the defect itself, multi-model branch ───────────────────────────────
console.log('B103 — an over-cap tally is clamped on the multi-model branch');
{
  const def = bodyDef();
  const stale = { cc_b: { Alpha: 1, Bravo: 1 } };      // legal at 10 (cap 2), not at 5 (cap 1)
  const big = E.loRollup(def, 10, sel(stale));
  eq('cap 2 at size 10 — both picks survive', w(big, 'Alpha') + w(big, 'Bravo'), 2);

  const small = E.loRollup(def, 5, sel(stale));
  eq('cap 1 at size 5 — exactly one pick survives', w(small, 'Alpha') + w(small, 'Bravo'), 1);
  eq('truncation follows the option choice order — Alpha kept', w(small, 'Alpha'), 1);
  eq('truncation follows the option choice order — Bravo dropped', w(small, 'Bravo'), 0);
  // 4 Troopers, one Chainsword consumed -> 3 remain, plus the Sergeant's = 4.
  eq('exactly one Chainsword is consumed, matching what was emitted', w(small, 'Chainsword'), 4);
  ok(!small.overAllocated, 'the clamp is silent — overAllocated does NOT fire');
}
{
  // The pre-fix shape: everything piled on one choice. The old code emitted all of
  // it and clamped only the source charge, so this is the case that hid best.
  const def = bodyDef();
  const r = E.loRollup(def, 5, sel({ cc_b: { Charlie: 4 } }));
  eq('a single over-stacked choice is clamped to the cap', w(r, 'Charlie'), 1);
  eq('and consumes exactly one Chainsword', w(r, 'Chainsword'), 4);
  ok(!r.overAllocated, 'still silent');
}
{
  // A cap that has fallen to zero. Grey Knights Paladin Squad and Brotherhood
  // Terminator Squad both do this at their 4-model bracket (1 per 5 models).
  const def = bodyDef();
  const r = E.loRollup(def, 4, sel({ cc_b: { Alpha: 2 } }));
  eq('a cap of zero emits nothing at all', w(r, 'Alpha'), 0);
  eq('and consumes no Chainsword', w(r, 'Chainsword'), 4);
}

// ── 2. the two branches now agree ──────────────────────────────────────────
console.log('B103 — the fixed-1 and multi-model branches truncate identically');
{
  // A fixed-1 group can never take more than its one model, whatever the option's
  // own ceiling says, so the shared cap to compare the branches at is 1.
  const stale = { Charlie: 1, Alpha: 1, Bravo: 1 };    // stored in a deliberately odd order
  const body = E.loRollup(bodyDef(), 5, sel({ cc_b: stale }));       // cap 1
  const lead = E.loRollup(leaderDef(), 5, sel({ cc_l: stale }));     // cap 1
  eq('body branch keeps Alpha',   w(body, 'Alpha'), 1);
  eq('body branch drops Bravo',   w(body, 'Bravo'), 0);
  eq('body branch drops Charlie', w(body, 'Charlie'), 0);
  eq('fixed-1 branch keeps Alpha',   w(lead, 'Alpha'), 1);
  eq('fixed-1 branch drops Bravo',   w(lead, 'Bravo'), 0);
  eq('fixed-1 branch drops Charlie', w(lead, 'Charlie'), 0);
  ok(!body.overAllocated && !lead.overAllocated, 'neither branch reports over-allocation');
}
{
  // Storage order must not decide the outcome. Two tallies with the same contents
  // written in different orders have to roll up the same way.
  const def = bodyDef();
  const a = E.loRollup(def, 5, sel({ cc_b: { Alpha: 1, Charlie: 1 } }));
  const b = E.loRollup(def, 5, sel({ cc_b: { Charlie: 1, Alpha: 1 } }));
  eq('insertion order does not change the result', dump(a), dump(b));
}
{
  // A key that is not a listed choice is ignored, not emitted and not charged.
  const def = bodyDef();
  const r = E.loRollup(def, 10, sel({ cc_b: { Delta: 2, Alpha: 1 } }));
  eq('an unlisted key emits nothing', w(r, 'Delta'), 0);
  eq('and does not consume the listed pick\'s slot', w(r, 'Alpha'), 1);
}

// ── 3. a tally within its cap is untouched ─────────────────────────────────
// The whole ticket rests on this: the fix must move ONLY lists that were already
// illegal. If a legal list re-prices, the fix is wrong.
console.log('B103 — a tally that fits its cap is unaffected');
{
  const def = bodyDef();
  const r10 = E.loRollup(def, 10, sel({ cc_b: { Alpha: 1, Bravo: 1 } }));
  eq('both picks emitted at the bracket they were made at', w(r10, 'Alpha') + w(r10, 'Bravo'), 2);
  eq('two Chainswords consumed', w(r10, 'Chainsword'), 8);   // 1 Sergeant + 9 Troopers - 2
  const r5 = E.loRollup(def, 5, sel({ cc_b: { Bravo: 1 } }));
  eq('a single pick at cap 1 survives whichever choice it is', w(r5, 'Bravo'), 1);
  ok(!r10.overAllocated && !r5.overAllocated, 'no flag on a legal list');
}

// ── 4. overAllocated still fires for genuine same-source contention ────────
// The clamp must not have swallowed the flag's real job: two options eating the
// same source weapon on more models than the group has.
console.log('B103 — genuine same-source contention still reports over-allocation');
{
  const def = {
    size_brackets: [5],
    model_groups: [
      { name: 'Troopers', count: { fills_to_size: true, min: 5 }, default_weapons: ['Chainsword'] }
    ],
    options: [
      { id: 'a1', scope: 'Troopers', group: 'g', type: 'count', replaces: 'Chainsword',
        replacement_choices: ['Alpha'], max_total_all: true, up_to: 5 },
      { id: 'a2', scope: 'Troopers', group: 'g', type: 'count', replaces: 'Chainsword',
        replacement_choices: ['Bravo'], max_total_all: true, up_to: 5 }
    ]
  };
  const r = E.loRollup(def, 5, sel({ a1: { Alpha: 4 }, a2: { Bravo: 4 } }));
  eq('both options emit up to their own caps', w(r, 'Alpha') + w(r, 'Bravo'), 8);
  ok(r.overAllocated, 'eight swaps of one weapon across five models is flagged');
}

// ── 5. the selection path cannot create an over-cap tally ─────────────────
console.log('B103 — the UI cannot build an over-cap tally in the first place');
{
  const entry = { listId: 1, wargear: {} };
  E.setList([entry]);
  E.editLoadoutChoiceCount(1, 'cc_b', 'Alpha', 1, 1);
  E.editLoadoutChoiceCount(1, 'cc_b', 'Bravo', 1, 1);
  eq('the group cap refuses the second pick', sum(entry.wargear.cc_b), 1);
}

// ── 6. loHealChoiceTallies: the state is removed, not just ignored ────────
console.log('B103 — an over-cap saved tally is healed out of storage');
{
  const def = bodyDef();
  const entry = { listId: 1, wargear: { cc_b: { Alpha: 1, Bravo: 1 } } };
  const healedAt10 = E.loHealChoiceTallies(def, 10, entry, {}, null);
  eq('nothing to heal at the bracket it was built at', healedAt10.length, 0);
  eq('and the tally is left exactly as stored', sum(entry.wargear.cc_b), 2);

  const healedAt5 = E.loHealChoiceTallies(def, 5, entry, {}, null);
  eq('the option is healed after the size drops', healedAt5.join(','), 'cc_b');
  eq('the tally is truncated to the live cap', sum(entry.wargear.cc_b), 1);
  eq('in the option\'s own choice order', JSON.stringify(entry.wargear.cc_b), '{"Alpha":1}');
}
{
  // The heal and the rollup must agree — otherwise the stepper and the points table
  // tell the player different stories.
  const def = bodyDef();
  const raw = { Bravo: 2, Charlie: 1 };
  const entry = { listId: 1, wargear: { cc_b: JSON.parse(JSON.stringify(raw)) } };
  const before = E.loRollup(def, 5, sel({ cc_b: raw }));
  E.loHealChoiceTallies(def, 5, entry, {}, null);
  const after = E.loRollup(def, 5, sel({ cc_b: entry.wargear.cc_b }));
  eq('rolling up the healed tally gives the same answer as clamping the raw one',
     dump(after), dump(before));
}
{
  const def = bodyDef({ distinct: true });
  const entry = { listId: 1, wargear: { cc_b: { Alpha: 3 } } };
  E.loHealChoiceTallies(def, 10, entry, {}, null);
  eq('the per-choice cap on a distinct option is honoured by the heal',
     JSON.stringify(entry.wargear.cc_b), '{"Alpha":1}');
}
{
  const def = bodyDef();
  const entry = { listId: 1, wargear: { cc_b: { Delta: 2 } } };
  E.loHealChoiceTallies(def, 10, entry, {}, null);
  eq('a key that is not a listed choice is dropped', JSON.stringify(entry.wargear.cc_b), '{}');
}
{
  const def = bodyDef();
  const entry = { listId: 1, wargear: { cc_b: { Alpha: 1, Bravo: 1 } } };
  const healed = E.loHealChoiceTallies(def, 5, entry, {}, (o) => o.id === 'cc_b');
  eq('a suppressed option is left alone — its own clearing pass owns it', healed.length, 0);
  eq('and its tally is untouched', sum(entry.wargear.cc_b), 2);
}
{
  const def = bodyDef();
  const entry = { listId: 1, wargear: { cc_b: 3 } };   // a plain count, not a tally
  const healed = E.loHealChoiceTallies(def, 5, entry, {}, null);
  eq('a non-object value is not a tally and is skipped', healed.length, 0);
  eq('and is left as it was', entry.wargear.cc_b, 3);
}

// ── 7. the shipped population, re-derived from the real data ─────────────
// Not remembered numbers: the census is recomputed here from unit_loadouts.json
// through the engine's own loMaxCount/loGroupCounts, so a data change that widens
// the affected population fails this gate instead of passing silently.
console.log('B103 — the shipped population, re-derived');
const meta = {};
for (const a of UNITS) for (const u of a.units)
  meta[u.unit_id] = { army: a.army, name: u.unit_name,
                      sizes: ((u.points || {}).sizes || []).map(s => s.size) };

let nRC = 0, nMultiPlain = 0, nShrink = 0, capZero = [];
const shrinkers = [];
for (const uid of Object.keys(LO)) {
  if (uid === '_schema') continue;
  const def = LO[uid], m = meta[uid];
  if (!m) continue;
  const groups = {};
  for (const g of def.model_groups || []) groups[g.name] = g;
  for (const o of def.options || []) {
    if (o.type !== 'count' || !Array.isArray(o.replacement_choices)) continue;
    nRC++;
    const g = groups[o.scope];
    const isFixed1 = !!(g && g.count && g.count.fixed === 1);
    if (isFixed1 || o.distinct) continue;
    nMultiPlain++;
    const caps = {};
    for (const s of (m.sizes.length ? m.sizes : (def.size_brackets || []))) {
      if (o.required_size != null && o.required_size !== s) continue;
      caps[s] = E.loChoiceGroupCap(o, E.loMaxCount(o, s, E.loGroupCounts(def, s, {})[o.scope]));
    }
    const vals = Object.values(caps);
    if (!vals.length) continue;
    if (Math.max(...vals) !== Math.min(...vals)) {
      nShrink++;
      shrinkers.push({ uid, o, def, caps, m });
      if (Math.min(...vals) === 0) capZero.push(`${m.army}|${m.name}|${o.id}`);
    }
  }
}
eq('count options carrying replacement_choices', nRC, 64);
eq('of those, multi-model and non-distinct — the branch this ticket fixes', nMultiPlain, 49);
eq('of those, with a cap that shrinks between size brackets', nShrink, 30);
capZero.sort();
eq('the two options whose cap falls to zero at their smallest bracket',
   capZero.join(' ; '),
   'Grey Knights|Brotherhood Terminator Squad|cc_1 ; Grey Knights|Paladin Squad|cc_1');

// For every shrinking option: build a full-cap tally at its largest bracket, then
// view it at every smaller one. The heal and the rollup must agree, the healed tally
// must fit the cap, and nothing may be emitted that the cap does not allow.
let checked = 0, disagreed = 0, overCap = 0;
for (const s of shrinkers) {
  const brackets = Object.keys(s.caps).map(Number).sort((a, b) => a - b);
  const big = brackets[brackets.length - 1];
  const capBig = s.caps[big];
  const tally = {};
  let left = capBig;
  for (const c of s.o.replacement_choices) { if (left <= 0) break; tally[c] = 1; left--; }
  if (left > 0) tally[s.o.replacement_choices[0]] += left;
  for (const view of brackets) {
    if (view === big) continue;
    const entry = { listId: 1, wargear: { [s.o.id]: JSON.parse(JSON.stringify(tally)) } };
    const rawRoll = E.loRollup(s.def, view, sel({ [s.o.id]: tally }));
    E.loHealChoiceTallies(s.def, view, entry, {}, null);
    const healedRoll = E.loRollup(s.def, view, sel({ [s.o.id]: entry.wargear[s.o.id] }));
    checked++;
    if (dump(rawRoll) !== dump(healedRoll)) { disagreed++; console.log(`    ${s.m.name} ${s.o.id} @${view}: heal and rollup disagree`); }
    if (sum(entry.wargear[s.o.id]) > s.caps[view]) { overCap++; console.log(`    ${s.m.name} ${s.o.id} @${view}: healed tally still over cap`); }
  }
}
ok(checked > 0, `every shrinking option exercised at every smaller bracket (${checked} cases)`);
eq('heal and rollup agree on every one', disagreed, 0);
eq('no healed tally is left over its cap', overCap, 0);

// A tally that FITS is untouched at its own bracket — asserted across the whole
// shipped population, not on the fixtures alone.
let legalTouched = 0;
for (const s of shrinkers) {
  for (const b of Object.keys(s.caps).map(Number)) {
    const cap = s.caps[b];
    if (cap <= 0) continue;
    const tally = {};
    let left = cap;
    for (const c of s.o.replacement_choices) { if (left <= 0) break; tally[c] = 1; left--; }
    if (left > 0) tally[s.o.replacement_choices[0]] += left;
    const entry = { listId: 1, wargear: { [s.o.id]: JSON.parse(JSON.stringify(tally)) } };
    E.loHealChoiceTallies(s.def, b, entry, {}, null);
    if (JSON.stringify(entry.wargear[s.o.id]) !== JSON.stringify(tally)) {
      legalTouched++;
      console.log(`    ${s.m.name} ${s.o.id} @${b}: a legal tally was altered`);
    }
  }
}
eq('a tally built at its own bracket is never altered', legalTouched, 0);

// ── 8. the points that actually move ─────────────────────────────────────
// Pinned by name and by figure. These are the only shipped units whose saved lists
// re-price, and they can only ever fall — a clamp removes weapons, never adds them.
console.log('B103 — the seven units whose saved lists re-price');
{
  const moved = [];
  let rose = 0, cases = 0;
  for (const s of shrinkers) {
    const brackets = Object.keys(s.caps).map(Number).sort((a, b) => a - b);
    const big = brackets[brackets.length - 1];
    const cap = s.caps[big];
    const choices = s.o.replacement_choices;
    // Three ways to spend the same cap. Which picks a player made decides whether a
    // priced one is the one that gets truncated, so a single fill would under-count
    // the affected units.
    const fills = [];
    { const t = {}; let left = cap; for (const c of choices) { if (left <= 0) break; t[c] = 1; left--; }
      if (left > 0) t[choices[0]] += left; if (cap > 0) fills.push(t); }
    if (cap > 0 && !s.o.distinct) fills.push({ [choices[0]]: cap });
    if (cap > 0 && !s.o.distinct) fills.push({ [choices[choices.length - 1]]: cap });
    for (const tally of fills) {
      for (const view of brackets) {
        if (view === big) continue;
        const pNow  = E.wargearCostForRollup(s.uid, E.loRollup(s.def, view, sel({ [s.o.id]: tally })));
        // What the pre-fix engine emitted at the smaller bracket: every pick, in
        // full — which is exactly what the fixed engine emits at the bracket the
        // tally was built at, where it still fits.
        const pThen = E.wargearCostForRollup(s.uid, E.loRollup(s.def, big, sel({ [s.o.id]: tally })));
        cases++;
        if (pNow > pThen) { rose++; console.log(`    ${s.m.name} @${view}: points ROSE ${pThen} -> ${pNow}`); }
        if (pNow !== pThen) moved.push(`${s.m.army}|${s.m.name}`);
      }
    }
  }
  ok(cases > 0, `every shrinking option priced across three fills (${cases} cases)`);
  eq('a clamp removes weapons, so wargear points never rise', rose, 0);
  const names = [...new Set(moved)].sort();
  eq('exactly seven shipped units re-price', names.length, 7);
  eq('and they are these',
     names.join(' ; '),
     "Adeptus Astartes|Centurion Devastator Squad ; Deathwatch|Deathwatch Terminator Squad ; " +
     "Drukhari|Talos ; Grey Knights|Brotherhood Terminator Squad ; Grey Knights|Paladin Squad ; " +
     "Grey Knights|Purifier Squad ; Space Wolves|Thunderwolf Cavalry");
}

console.log(fail === 0 ? 'all B103 checks pass' : `b103_check: ${fail} FAILED`);
process.exit(fail === 0 ? 0 : 1);
