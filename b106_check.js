// b106_check.js — B106. "This model can be equipped with up to N of the following,
// but cannot take duplicates" — the addition shape, no `replaces`.
//
// The distinct/up-to mechanism landed under B101 for the REPLACEMENT case (a body of
// Chainswords, some swapped for one of a menu). The addition case is the same rule
// worn a little differently: pick up to N different weapons from a menu and add them
// to the model, no swap. Both Grey Knights Dreadknights carry this on a fixed-1
// model group and were the only residual _parser_flags entry in the faction at S206
// close; the shipped engine skipped a count option whose `replaces` was empty on
// that branch, so nothing was emitted.
//
// The fix reuses B101's helpers verbatim (loDistinctCap, loChoiceGroupCap,
// loDistinctPicks). Only loRollup's fixed-1 branch changed: a count option with no
// `replaces` but a `replacement_choices` list is now accepted as a pure addition,
// with the source-consumption bookkeeping skipped. The body branch already handled
// this shape because loSrcOnGroup treats an empty `replaces` as "nothing to
// replace" — that path is exercised here to pin its behaviour.
//
// Fixtures are synthetic. No shipped unit carries this shape yet (both Dreadknights
// wait on the parser turn that follows this session).
//
// Build-time only; not part of the served app.
// Usage: node b106_check.js [index.html]

const fs = require('fs');

function slice(lines, startNeedle, endNeedle) {
  const s = lines.findIndex(l => l.includes(startNeedle));
  const e = lines.findIndex(l => l.includes(endNeedle));
  if (s < 0 || e < 0 || e <= s) throw new Error(`slice failed: ${startNeedle} .. ${endNeedle}`);
  return lines.slice(s, e).join('\n');
}

function loadEngine(path) {
  const lines = fs.readFileSync(path, 'utf8').split('\n');
  const rollup = slice(lines, 'function loMaxCount', '// Unit Options UI for loadout-defined units.');
  const editor = slice(lines, 'function editLoadoutChoiceCount', 'function editLoadoutAdd');
  const prelude = `const PROFILE_SEP=/\\s[\u2013\\-\u00e2]\\s/;
function stripProfile(n){return String(n||'').split(PROFILE_SEP)[0].trim();}
function weaponBase(n){return stripProfile(n).toLowerCase();}
let wargearPoints = {};
let armyList = [];
function renderAll(){}`;
  return new Function(prelude + rollup + '\n' + editor +
    '\nreturn { loRollup, loMaxCount, loDistinctCap, loChoiceGroupCap, loDistinctPicks,' +
    ' editLoadoutChoiceCount, setList:(l)=>{armyList=l;}, getList:()=>armyList };')();
}

const E = loadEngine(process.argv[2] || 'index.html');

let fail = 0;
const ok = (cond, msg) => { if (!cond) { fail++; console.log('  FAIL ' + msg); } else console.log('  ok   ' + msg); };
const eq = (msg, got, want) => ok(got === want, `${msg}: got ${JSON.stringify(got)} want ${JSON.stringify(want)}`);

// ── fixtures ───────────────────────────────────────────────────────────────
// Shape of the real Nemesis Dreadknight option: 1-model group, add up to 2 of 3
// (or 4) distinct weapons. No `replaces`. Priced per pick (not modelled here — cost
// lives one layer up in wargearCostForRollup and reads the rollup we produce).
const RANGED3 = ['Gatling psilencer', 'Heavy incinerator', 'Heavy psycannon'];
const dkDef = (extra) => ({
  size_brackets: [1],
  model_groups: [
    { name: 'Nemesis Dreadknight', count: { fixed: 1 }, default_weapons: ['Dreadfists'] }
  ],
  options: [Object.assign({
    id: 'add_r', scope: 'Nemesis Dreadknight', group: 'Ranged Weapons', type: 'count',
    replacement_choices: RANGED3.slice(),
    distinct: true, max_total: 2
  }, extra || {})]
});
// The same option parked on a body group, to pin the other rollup branch. The body
// group already accepted an empty-`replaces` count option before B106 (loSrcOnGroup
// returned true), so this section is a regression pin — nothing should have moved.
const bodyDef = (extra) => ({
  size_brackets: [5, 10],
  model_groups: [
    { name: 'Champion', count: { fixed: 1 }, default_weapons: ['Bolt pistol', 'Chainsword'] },
    { name: 'Troopers', count: { fills_to_size: true, min: 4 }, default_weapons: ['Bolt pistol', 'Chainsword'] }
  ],
  options: [Object.assign({
    id: 'add_b', scope: 'Troopers', group: 'Special Weapons', type: 'count',
    replacement_choices: ['Flamer', 'Meltagun', 'Plasma gun'],
    distinct: true, max_total: 2
  }, extra || {})]
});
const sel = (counts) => ({ choiceById: {}, countById: counts || {}, addById: {} });
const w = (roll, name) => roll.weapons.get(name) || 0;

// ── 1. helpers behave the same on the no-`replaces` shape ──────────────────
console.log('B106 — B101 helpers are shape-agnostic re: `replaces`');
{
  // A distinct option with no `replaces` still shrinks its group cap to the number
  // of listed choices and still caps each choice at one.
  const noRepl = { distinct: true, replacement_choices: ['a', 'b'] };
  eq('per-choice cap', E.loDistinctCap(noRepl), 1);
  eq('group cap shrinks to listed choices', E.loChoiceGroupCap(noRepl, 5), 2);
  eq('cap is untouched when it already binds', E.loChoiceGroupCap(noRepl, 1), 1);
}

// ── 2. rollup, fixed-1 group: picks emit, default weapons stay ─────────────
console.log('B106 — fixed-1 distinct-add emits picks without consuming defaults');
{
  const def = dkDef();
  const r = E.loRollup(def, 1, sel({ add_r: { 'Heavy incinerator': 1 } }));
  eq('the pick lands on the model', w(r, 'Heavy incinerator'), 1);
  eq('the default Dreadfists survive', w(r, 'Dreadfists'), 1);
  eq('nothing else was added', r.weapons.size, 2);
}
{
  const def = dkDef();
  const r = E.loRollup(def, 1,
    sel({ add_r: { 'Gatling psilencer': 1, 'Heavy incinerator': 1 } }));
  eq('two different picks both survive (Gatling)', w(r, 'Gatling psilencer'), 1);
  eq('two different picks both survive (Incinerator)', w(r, 'Heavy incinerator'), 1);
  eq('Dreadfists still present', w(r, 'Dreadfists'), 1);
}
{
  // A stale duplicate — a saved list that asked for two of the same pick. Legal
  // total (2), illegal distribution. Only one survives; the freed slot is NOT
  // silently spent elsewhere.
  const def = dkDef();
  const r = E.loRollup(def, 1, sel({ add_r: { 'Heavy incinerator': 2 } }));
  eq('only one Incinerator survives', w(r, 'Heavy incinerator'), 1);
  eq('the freed slot did not manufacture a second pick', w(r, 'Gatling psilencer'), 0);
  eq('nor a third choice', w(r, 'Heavy psycannon'), 0);
  ok(!r.overAllocated, 'a clamped duplicate is corrected, not reported as over-allocation');
}
{
  // Three distinct picks against a max_total of 2 — the total ceiling still binds,
  // and it truncates in the option's own choice order rather than storage order.
  const def = dkDef();
  const r = E.loRollup(def, 1,
    sel({ add_r: { 'Heavy psycannon': 1, 'Heavy incinerator': 1, 'Gatling psilencer': 1 } }));
  eq('total across distinct picks is capped at max_total',
     w(r, 'Gatling psilencer') + w(r, 'Heavy incinerator') + w(r, 'Heavy psycannon'), 2);
  eq('truncation follows option choice order — Gatling kept', w(r, 'Gatling psilencer'), 1);
  eq('truncation follows option choice order — Incinerator kept', w(r, 'Heavy incinerator'), 1);
  eq('truncation follows option choice order — Psycannon dropped', w(r, 'Heavy psycannon'), 0);
  eq('Dreadfists always survive — the addition never consumes them', w(r, 'Dreadfists'), 1);
}
{
  // A 4-choice menu (the Grand Master's sublimator variant) with max_total 2 —
  // group cap still binds at 2, not at the number of listed choices.
  const def = dkDef({ replacement_choices: RANGED3.concat(['Sublimator']) });
  const r = E.loRollup(def, 1, sel({
    add_r: { 'Sublimator': 1, 'Heavy psycannon': 1, 'Heavy incinerator': 1, 'Gatling psilencer': 1 }
  }));
  const total = w(r, 'Sublimator') + w(r, 'Heavy psycannon')
              + w(r, 'Heavy incinerator') + w(r, 'Gatling psilencer');
  eq('four picks clamp to max_total 2', total, 2);
}
{
  // Empty selection: nothing added, Dreadfists intact. The default state of a fresh
  // Dreadknight — the option is genuinely optional, no free default.
  const def = dkDef();
  const r = E.loRollup(def, 1, sel({}));
  eq('no picks means no additions', r.weapons.size, 1);
  eq('and the model keeps its default', w(r, 'Dreadfists'), 1);
}

// ── 3. selection path: the duplicate is refused, not stored ────────────────
console.log('B106 — selection path refuses a second pick of the same choice');
{
  const entry = { listId: 1, wargear: {} };
  E.setList([entry]);
  // groupMax = 2 (the option's max_total), perMax = 1 (loDistinctCap).
  E.editLoadoutChoiceCount(1, 'add_r', 'Heavy incinerator', 1, 2, 1);
  eq('first Incinerator is taken', entry.wargear.add_r['Heavy incinerator'], 1);
  E.editLoadoutChoiceCount(1, 'add_r', 'Heavy incinerator', 1, 2, 1);
  eq('second Incinerator is refused', entry.wargear.add_r['Heavy incinerator'], 1);
  E.editLoadoutChoiceCount(1, 'add_r', 'Gatling psilencer', 1, 2, 1);
  eq('a DIFFERENT choice is still allowed', entry.wargear.add_r['Gatling psilencer'], 1);
  E.editLoadoutChoiceCount(1, 'add_r', 'Heavy psycannon', 1, 2, 1);
  ok(!entry.wargear.add_r['Heavy psycannon'], 'a third pick is refused — group cap binds');
  E.editLoadoutChoiceCount(1, 'add_r', 'Heavy incinerator', -1, 2, 1);
  ok(!entry.wargear.add_r['Heavy incinerator'], 'clearing a pick is always allowed');
  E.editLoadoutChoiceCount(1, 'add_r', 'Heavy psycannon', 1, 2, 1);
  eq('the freed slot can then be spent on something else',
     entry.wargear.add_r['Heavy psycannon'], 1);
}

// ── 4. rollup, body group: the pinned regression ─────────────────────────
console.log('B106 — body distinct-add: no regression against the same shape');
{
  const def = bodyDef();
  const r = E.loRollup(def, 10, sel({ add_b: { Flamer: 1, Meltagun: 1 } }));
  eq('two body picks land', w(r, 'Flamer') + w(r, 'Meltagun'), 2);
  // No source consumption — every Chainsword is still on the roster (9 Troopers +
  // 1 Champion). The addition NEVER swaps the default gear.
  eq('every default Chainsword survives (addition, not replacement)', w(r, 'Chainsword'), 10);
  eq('every default Bolt pistol survives', w(r, 'Bolt pistol'), 10);
}
{
  // A stale duplicate on a body group — the same clamp as the fixed-1 case.
  const def = bodyDef();
  const r = E.loRollup(def, 10, sel({ add_b: { Flamer: 2 } }));
  eq('only one Flamer survives on the body', w(r, 'Flamer'), 1);
  eq('the second slot is NOT spent elsewhere', w(r, 'Meltagun'), 0);
  eq('Chainswords are all still there — no consumption', w(r, 'Chainsword'), 10);
}

// ── 5. non-B106 count options behave exactly as before ─────────────────────
console.log('B106 — the replacement shape is byte-for-byte unchanged');
{
  // A count option WITH `replaces`, no distinct — a plain replacement. The B106
  // isAddOnly flag never trips; every existing arm still fires as it did.
  const def = {
    size_brackets: [5],
    model_groups: [
      { name: 'Champion', count: { fixed: 1 }, default_weapons: ['Bolt pistol', 'Chainsword'] },
      { name: 'Troopers', count: { fills_to_size: true, min: 4 }, default_weapons: ['Bolt pistol', 'Chainsword'] }
    ],
    options: [{
      id: 'cc_p', scope: 'Troopers', group: 'Chainsword Options', type: 'count',
      replaces: 'Chainsword', replacement_choices: ['Flamer', 'Meltagun', 'Plasma gun'],
      max_total_all: true, up_to: 2
    }]
  };
  const r = E.loRollup(def, 5, sel({ cc_p: { Flamer: 2 } }));
  eq('plain replacement still allows two of the same choice', w(r, 'Flamer'), 2);
  eq('and consumes two Chainswords', w(r, 'Chainsword'), 3);
}

console.log(fail === 0 ? 'all B106 checks pass' : `b106_check: ${fail} FAILED`);
process.exit(fail === 0 ? 0 : 1);
