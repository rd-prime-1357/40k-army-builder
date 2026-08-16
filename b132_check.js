// b132_check.js — B132 (D342/D343). Loads the real applyChapterKeywordAdditions +
// applyChapterPointOverrides + resolveUnits out of index.html and proves the
// chapter-scoped keyword restoration is ISOLATED, not merely present:
//
//   1. The owning chapter's resolved pool carries the restored keyword on every
//      model group of every unit that carries the map.
//   2. NO other chapter's resolved pool carries it — the one that matters. The
//      generic unit object is shared by reference across every chapter's resolved
//      set, so an in-place push would leak Deathwing into Ultramarines.
//   3. The generic Space Marines pool (non-subfaction path) is unchanged, and the
//      underlying units.json objects are byte-identical after every resolve —
//      checked by deep-comparing a snapshot of the live block taken before any
//      resolve ran, which catches mutation no matter which pool it happened in.
//   4. Identity: an unaffected unit is returned by the SAME reference (no
//      gratuitous copying), and an affected unit is returned by a DIFFERENT
//      reference with a different model_groups array and different group objects.
//   5. Restoration is idempotent and dedupes — a chapter that natively carries
//      the keyword does not end up with it twice, and resolving twice is stable.
//   6. Order: an already-sorted keyword list stays sorted with the addition in
//      its alphabetical place; an unsorted list (Chaos-Daemons-shaped, source
//      order) is appended to, not reordered.
//   7. A unit carrying BOTH maps gets both effects (the two compose).
//   8. The 'complete' roster path never applies the map (structural isolation,
//      same tripwire shape as b90_check).
//
// Also run against the SHIPPED units.json: the 28 real records resolve for Dark
// Angels and for nobody else. Synthetic fixtures pin the mechanism; the live-data
// pass pins that the mechanism is actually reaching the real map.
//
// Build-time only; not part of the served app.
// Usage: node b132_check.js index.html
const fs = require('fs');

function slice(lines, startNeedle, endNeedle) {
  const s = lines.findIndex(l => l.includes(startNeedle));
  const e = lines.findIndex(l => l.includes(endNeedle));
  if (s < 0 || e < 0 || e <= s) throw new Error(`slice failed: ${startNeedle} .. ${endNeedle}`);
  return lines.slice(s, e).join('\n');
}

function load(path) {
  const lines = fs.readFileSync(path, 'utf8').split('\n');
  const mapsSrc    = slice(lines, 'function applyChapterPointOverrides', 'function resolveUnits');
  const resolveSrc = slice(lines, 'function resolveUnits', 'function setActiveUnits');
  const prelude = `
    let __kwCalls = 0;
    const __blocks = {};
    const unitsByArmy = __blocks;
    function setBlocks(b) { for (const k in __blocks) delete __blocks[k];
                            for (const k in b) __blocks[k] = b[k]; }
  `;
  const wrap = `
    const __origACKA = applyChapterKeywordAdditions;
    applyChapterKeywordAdditions = function (u, a) { __kwCalls++; return __origACKA(u, a); };
  `;
  return new Function(
    prelude + mapsSrc + '\n' + wrap + '\n' + resolveSrc + '\n' +
    'return { resolveUnits, setBlocks,' +
    ' kwCalls: () => __kwCalls, reset: () => { __kwCalls = 0; } };'
  )();
}

let fails = 0;
function ok(cond, msg) { if (!cond) { fails++; console.log('  FAIL: ' + msg); } }
const clone = o => JSON.parse(JSON.stringify(o));
const kwOf = (pool, name) => {
  const u = pool.find(x => x.unit_name === name);
  return u ? u.model_groups.map(g => g.keyword_names) : null;
};
const has = (pool, name, kw) =>
  (kwOf(pool, name) || []).some(list => list.indexOf(kw) >= 0);
const hasAny = (pool, kw) =>
  pool.some(u => (u.model_groups || []).some(g => (g.keyword_names || []).indexOf(kw) >= 0));

const E = load(process.argv[2] || 'index.html');

// ── synthetic fixtures ────────────────────────────────────────────────────────
// Shared generic units, exactly as units.json holds them: ONE object each, handed
// to every chapter's resolve. Sorted keyword lists (Astartes convention) except
// SourceOrder, which is deliberately unsorted (Chaos Daemons convention).
const generic = [
  { unit_name: 'Terminator Squad', unit_id: 'g1', points: {},
    chapter_keyword_additions: { 'Chapter A': ['Deathwing'] },
    model_groups: [
      { keyword_names: ['Imperium', 'Infantry', 'Terminator'] },
      { keyword_names: ['Character', 'Imperium', 'Infantry'] },
    ] },
  { unit_name: 'Outrider Squad', unit_id: 'g2', points: {},
    chapter_keyword_additions: { 'Chapter A': ['Ravenwing'] },
    model_groups: [{ keyword_names: ['Imperium', 'Mounted'] }] },
  { unit_name: 'Plain Marine', unit_id: 'g3', points: {},
    model_groups: [{ keyword_names: ['Imperium', 'Infantry'] }] },
  { unit_name: 'SourceOrder', unit_id: 'g4', points: {},
    chapter_keyword_additions: { 'Chapter A': ['Deathwing'] },
    model_groups: [{ keyword_names: ['Monster', 'Character', 'Imperium'] }] },
  { unit_name: 'Both Maps', unit_id: 'g5',
    points: { sizes: [{ size: 1, first_unit: 100 }] },
    chapter_keyword_additions: { 'Chapter A': ['Deathwing'] },
    chapter_point_overrides: { 'Chapter A': { sizes: [{ size: 1, first_unit: 140 }] } },
    model_groups: [{ keyword_names: ['Imperium', 'Vehicle'] }] },
  { unit_name: 'Already Has It', unit_id: 'g6', points: {},
    chapter_keyword_additions: { 'Chapter A': ['Deathwing'] },
    model_groups: [{ keyword_names: ['Deathwing', 'Imperium', 'Infantry'] }] },
];

const blocks = {
  'Adeptus Astartes': generic,
  'Chapter A': [{ unit_name: 'A Only', unit_id: 'a1', points: {},
                  model_groups: [{ keyword_names: ['Deathwing', 'Imperium'] }] }],
  'Chapter B': [{ unit_name: 'B Only', unit_id: 'b1', points: {},
                  model_groups: [{ keyword_names: ['Imperium'] }] }],
  'Chapter C': [],
};
E.setBlocks(blocks);

// Snapshot the live block BEFORE any resolve, for the mutation check (3).
const before = clone(generic);

const A = E.resolveUnits({ name: 'Chapter A', data_army: 'Chapter A', is_subfaction: true, roster_mode: 'union' });
const B = E.resolveUnits({ name: 'Chapter B', data_army: 'Chapter B', is_subfaction: true, roster_mode: 'union' });
const C = E.resolveUnits({ name: 'Chapter C', data_army: 'Chapter C', is_subfaction: true, roster_mode: 'union' });
const G = E.resolveUnits({ name: 'Space Marines', data_army: 'Adeptus Astartes', is_subfaction: false });

// 1 — the owning chapter gets the keyword, on EVERY model group.
ok(kwOf(A, 'Terminator Squad').every(l => l.indexOf('Deathwing') >= 0),
   'owning chapter did not get Deathwing on every model group: ' + JSON.stringify(kwOf(A, 'Terminator Squad')));
ok(has(A, 'Outrider Squad', 'Ravenwing'), 'owning chapter did not get Ravenwing');

// 2 — no other chapter, and no other unit, sees it. THE one that matters.
ok(!has(B, 'Terminator Squad', 'Deathwing'), 'Deathwing leaked into Chapter B');
ok(!has(C, 'Terminator Squad', 'Deathwing'), 'Deathwing leaked into Chapter C');
ok(!has(B, 'Outrider Squad', 'Ravenwing'),  'Ravenwing leaked into Chapter B');
ok(!has(A, 'Plain Marine', 'Deathwing'),    'Deathwing landed on a unit with no map entry');
ok(!hasAny(B, 'Ravenwing'), 'Ravenwing present anywhere in Chapter B pool');

// 3 — the generic pool is unchanged, and units.json itself was never mutated.
// (a natively-keyworded generic unit is allowed to keep its own keyword, so the
//  test is "identical to the pre-resolve snapshot", not "no Deathwing anywhere")
ok(JSON.stringify(G.map(u => u.model_groups)) === JSON.stringify(before.map(u => u.model_groups)),
   'the generic Space Marines pool gained or lost keywords');
ok(JSON.stringify(clone(generic)) === JSON.stringify(before),
   'the shared units.json objects were mutated by a resolve');

// 4 — identity: copy only where an addition applies.
const gPlain = generic.find(u => u.unit_name === 'Plain Marine');
ok(A.find(u => u.unit_name === 'Plain Marine') === gPlain,
   'an unaffected unit was needlessly copied');
ok(B.find(u => u.unit_name === 'Terminator Squad') === generic[0],
   'a non-owning chapter got a copy of an affected unit instead of the shared object');
const aTerm = A.find(u => u.unit_name === 'Terminator Squad');
ok(aTerm !== generic[0], 'the affected unit was returned by shared reference');
ok(aTerm.model_groups !== generic[0].model_groups, 'model_groups array was shared, not copied');
ok(aTerm.model_groups[0] !== generic[0].model_groups[0], 'a model group object was shared, not copied');
ok(aTerm.model_groups[0].keyword_names !== generic[0].model_groups[0].keyword_names,
   'keyword_names array was shared, not copied');

// 5 — dedupe + idempotence.
ok(kwOf(A, 'Already Has It')[0].filter(k => k === 'Deathwing').length === 1,
   'a natively-keyworded unit got the keyword twice');
const A2 = E.resolveUnits({ name: 'Chapter A', data_army: 'Chapter A', is_subfaction: true, roster_mode: 'union' });
ok(JSON.stringify(kwOf(A2, 'Terminator Squad')) === JSON.stringify(kwOf(A, 'Terminator Squad')),
   'resolving twice produced a different keyword set');

// 6 — order.
ok(JSON.stringify(kwOf(A, 'Terminator Squad')[0]) ===
   JSON.stringify(['Deathwing', 'Imperium', 'Infantry', 'Terminator']),
   'sorted list did not keep the addition in alphabetical place: ' + JSON.stringify(kwOf(A, 'Terminator Squad')[0]));
ok(JSON.stringify(kwOf(A, 'SourceOrder')[0]) ===
   JSON.stringify(['Monster', 'Character', 'Imperium', 'Deathwing']),
   'an unsorted (source-order) list was reordered: ' + JSON.stringify(kwOf(A, 'SourceOrder')[0]));

// 7 — the two maps compose on one unit.
const both = A.find(u => u.unit_name === 'Both Maps');
ok(both.points.sizes[0].first_unit === 140, 'point override lost when the keyword map also applied');
ok(both.model_groups[0].keyword_names.indexOf('Deathwing') >= 0,
   'keyword addition lost when the point override also applied');
ok(B.find(u => u.unit_name === 'Both Maps').points.sizes[0].first_unit === 100,
   'point override leaked to a non-owning chapter');

// 8 — the complete path never applies the map.
E.reset();
const K = E.resolveUnits({ name: 'Chapter A', data_army: 'Chapter A', is_subfaction: true, roster_mode: 'complete' });
ok(E.kwCalls() === 0, 'complete-mode called applyChapterKeywordAdditions (' + E.kwCalls() + ' calls)');
ok(K.length === 1 && K[0].unit_name === 'A Only', 'complete-mode roster wrong');

// ── live data ────────────────────────────────────────────────────────────────
// The mechanism is pinned above; this pins that it reaches the real 28 records.
if (fs.existsSync('units.json')) {
  const live = JSON.parse(fs.readFileSync('units.json', 'utf8'));
  const byArmy = {};
  for (const b of live) byArmy[b.army] = b.units;
  E.setBlocks(byArmy);

  const expect = {};
  for (const u of (byArmy['Adeptus Astartes'] || [])) {
    const m = u.chapter_keyword_additions;
    if (!m) continue;
    for (const army of Object.keys(m)) (expect[army] = expect[army] || []).push([u.unit_name, m[army]]);
  }
  const owners = Object.keys(expect);
  ok(owners.length > 0, 'no live unit carries chapter_keyword_additions — the map is gone from units.json');

  const tax = JSON.parse(fs.readFileSync('faction_taxonomy.json', 'utf8'));
  const subs = [];
  for (const g of tax.groups) for (const f of g.factions) if (f.is_subfaction && f.built) subs.push(f);

  for (const f of subs) {
    const pool = E.resolveUnits(f);
    const mine = expect[f.data_army] || [];
    for (const [name, kws] of mine) {
      for (const kw of kws) {
        ok((kwOf(pool, name) || []).every(l => l.indexOf(kw) >= 0),
           `${f.name}: ${name} missing restored keyword ${kw}`);
      }
    }
    // every keyword owned by SOMEONE ELSE must be absent from this pool unless
    // this chapter's own block natively carries it.
    for (const other of owners) {
      if (other === f.data_army) continue;
      for (const [name, kws] of expect[other]) {
        for (const kw of kws) {
          ok(!has(pool, name, kw), `${f.name}: ${kw} leaked onto ${name} (owned by ${other})`);
        }
      }
    }
  }

  const genericPool = E.resolveUnits({ name: 'Space Marines', data_army: 'Adeptus Astartes', is_subfaction: false });
  for (const army of owners) {
    for (const [name, kws] of expect[army]) {
      for (const kw of kws) {
        ok(!has(genericPool, name, kw), `generic Space Marines pool carries restored keyword ${kw} on ${name}`);
      }
    }
  }

  const total = owners.reduce((n, a) => n + expect[a].length, 0);
  console.log(`  live: ${total} record(s) across ${owners.length} owning army/armies, ${subs.length} chapters checked`);
}

if (fails === 0) console.log('all B132 checks pass');
else { console.log(fails + ' B132 check(s) failed'); process.exit(1); }
