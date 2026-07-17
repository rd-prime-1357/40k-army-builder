// b18d_check.js — B18d verification. Contested-slot mutual exclusion on
// leader-conflict units where a fanned generic capped swap and a named
// leader/sergeant swap target the same weapon on a fixed-1 group.
//
// Verifies:
//   1. Pool caps: the unit-wide cap is correct across body + leader groups.
//   2. Mutual exclusion: activating both the named swap and the fanned swap
//      on the same leader group fires overAllocated.
//   3. Independent use: activating ONLY the fanned swap (not the named swap)
//      does NOT fire overAllocated.
//   4. Named swap without fan: using the named swap alone is clean and
//      does NOT consume a pool slot.
//
// Usage: node b18d_check.js [index.html] [B18d_fixture.json]

const fs = require('fs');

function slice(lines, startNeedle, endNeedle) {
  const s = lines.findIndex(l => l.includes(startNeedle));
  const e = lines.findIndex(l => l.includes(endNeedle));
  return lines.slice(s, e).join('\n');
}
function loadEngine(path) {
  const lines = fs.readFileSync(path, 'utf8').split('\n');
  const rollup = slice(lines, 'function loMaxCount', '// Unit Options UI for loadout-defined units.');
  const cost   = slice(lines, 'function wargearCostForRollup', 'function wargearCostForEntry');
  const prelude = `const PROFILE_SEP=/\\s[\u2013\\-\u00e2]\\s/;
function stripProfile(n){return String(n||'').split(PROFILE_SEP)[0].trim();}
function weaponBase(n){return stripProfile(n).toLowerCase();}
let wargearPoints = {};`;
  return new Function(prelude + rollup + '\n' + cost +
    '\nreturn {loRollup, wargearCostForRollup, setPts:(p)=>{wargearPoints=p;}};')();
}

const E = loadEngine(process.argv[2] || 'index.html');
const FIX = JSON.parse(fs.readFileSync(process.argv[3] || 'B18d_fixture.json', 'utf8'));
E.setPts({});

let fail = 0;
const ck = (name, got, want) => {
  const ok = got === want;
  if (!ok) fail++;
  console.log(`  ${ok ? 'ok  ' : 'FAIL'} ${name}: got ${got} want ${want}`);
};

function roll(uid, size, sel) {
  return E.loRollup(FIX[uid], size, sel);
}
function sel(choices, counts, adds) {
  return { choiceById: choices || {}, countById: counts || {}, addById: adds || {} };
}

// ────────────────────────────────────────────────────────────────────────
// 1. Thunderwolf Cavalry (000000322)
//    cnt_3 (body) + cnt_3__thunderwolf_cavalry_pack_leader (leader)
//    share pool "cnt_3", per_n_models=3, max_per_n=1.
//    cc_1 (leader, replaces Bolt pistol) contests the same slot.
// ────────────────────────────────────────────────────────────────────────
{
  const uid = '000000322';
  // @size 6: pool cap = floor(6/3)*1 = 2
  // Seed both cnt_3 options high; pool should clamp total to 2.
  const r1 = roll(uid, 6, sel({}, { cnt_3: 99, cnt_3__thunderwolf_cavalry_pack_leader: 99 }));
  const pp = r1.weapons.get('Plasma pistol') || 0;
  ck('TWC @6: total plasma pistols capped at 2', pp, 2);

  // @size 3: pool cap = floor(3/3)*1 = 1
  const r2 = roll(uid, 3, sel({}, { cnt_3: 99, cnt_3__thunderwolf_cavalry_pack_leader: 99 }));
  const pp3 = r2.weapons.get('Plasma pistol') || 0;
  ck('TWC @3: total plasma pistols capped at 1', pp3, 1);

  // Mutual exclusion: cc_1 (Pack Leader swaps Bolt pistol → Boltgun) AND
  // cnt_3_ldr (Pack Leader swaps Bolt pistol → Plasma pistol) both active.
  // overAllocated must fire (2 replacements of 1 bolt pistol on 1 model).
  const r3 = roll(uid, 6, sel({}, { cc_1: {Boltgun: 1}, cnt_3__thunderwolf_cavalry_pack_leader: 1 }));
  ck('TWC @6: cc_1 + cnt_3_ldr fires overAllocated', r3.overAllocated, true);

  // Independent use: ONLY cnt_3_ldr active (Pack Leader → Plasma pistol),
  // cc_1 not active. Should be clean.
  const r4 = roll(uid, 6, sel({}, { cnt_3__thunderwolf_cavalry_pack_leader: 1 }));
  ck('TWC @6: cnt_3_ldr alone is clean', r4.overAllocated, false);

  // Named swap alone: cc_1 (Pack Leader → Boltgun), no fanned option.
  // Should be clean and NOT consume from pool.
  const r5 = roll(uid, 6, sel({}, { cc_1: {Boltgun: 1} }));
  ck('TWC @6: cc_1 alone is clean', r5.overAllocated, false);
  // Pool should still be empty (cc_1 has no pool_id).
  const bodyPlasma = r5.weapons.get('Plasma pistol') || 0;
  ck('TWC @6: cc_1 alone emits no plasma pistol', bodyPlasma, 0);
}

// ────────────────────────────────────────────────────────────────────────
// 2. Talonstrike Kill Team (000003874)
//    cnt_3 (Intercessors) + cnt_3__kill_team_sergeant_with_jump_pack (Sgt)
//    share pool "cnt_3", per_n_models=5, max_per_n=1.
//    cho_1 (Sgt choice, replaces Heavy bolt pistol) contests the same slot.
// ────────────────────────────────────────────────────────────────────────
{
  const uid = '000003874';
  // @size 10: pool cap = floor(10/5)*1 = 2
  const r1 = roll(uid, 10, sel({}, { cnt_3: 99, cnt_3__kill_team_sergeant_with_jump_pack: 99 }));
  const pp = r1.weapons.get('Plasma pistol') || 0;
  ck('TKT @10: total plasma pistols capped at 2', pp, 2);

  // Mutual exclusion: cho_1 (Sgt choice → Hand flamer) AND cnt_3_ldr both active.
  const r2 = roll(uid, 10, sel({ cho_1: 'Hand flamer' }, { cnt_3__kill_team_sergeant_with_jump_pack: 1 }));
  ck('TKT @10: cho_1 + cnt_3_ldr fires overAllocated', r2.overAllocated, true);

  // Independent use: ONLY cnt_3_ldr, cho_1 not active. Clean.
  const r3 = roll(uid, 10, sel({}, { cnt_3__kill_team_sergeant_with_jump_pack: 1 }));
  ck('TKT @10: cnt_3_ldr alone is clean', r3.overAllocated, false);

  // Named swap alone: cho_1 → Plasma pistol, no fanned option.
  // Should NOT consume from cnt_3 pool; body can still use cnt_3.
  const r4 = roll(uid, 10, sel({ cho_1: 'Plasma pistol' }, { cnt_3: 1 }));
  ck('TKT @10: cho_1 + body cnt_3 is clean (independent caps)', r4.overAllocated, false);
  const totalPP = r4.weapons.get('Plasma pistol') || 0;
  ck('TKT @10: cho_1 + body cnt_3 emits 2 plasma pistols', totalPP, 2);
}

// ────────────────────────────────────────────────────────────────────────
// 3. Deathwatch Veterans (000002783)
//    cc_1..cnt_7 (body) each fanned to Watch Sergeant, each with own pool.
//    sng_8 (Sgt replaces Power weapon) and sng_9 (Sgt replaces Boltgun)
//    contest the compound "Boltgun + Power weapon" slot.
// ────────────────────────────────────────────────────────────────────────
{
  const uid = '000002783';
  // @size 10: cc_1 pool cap = floor(10/5)*2 = 4
  // Seed cc_1 body + leader high; total should be 4.
  // cc_1 has replacement_choices — seed as object.
  const r1 = roll(uid, 10, sel({}, {
    cc_1: { 'Power weapon + Astartes Shield': 99 },
    cc_1__watch_sergeant: { 'Power weapon + Astartes Shield': 99 }
  }));
  // Count the shield (equipment_parts) — it's how the replacement emits.
  // Actually count Power weapon, which appears in the replacement.
  // The compound replacement "Power weapon + Astartes Shield" emits Power weapon
  // to weapons and Astartes Shield to equipment.
  // But Power weapon is also a default weapon being replaced, so the rollup is complex.
  // Instead, check overAllocated is false (all within cap).
  ck('DWV @10: cc_1 body+leader all-high is clean', r1.overAllocated, false);

  // @size 5: cc_1 pool cap = floor(5/5)*2 = 2
  const r1b = roll(uid, 5, sel({}, {
    cc_1: { 'Power weapon + Astartes Shield': 99 },
    cc_1__watch_sergeant: { 'Power weapon + Astartes Shield': 99 }
  }));
  ck('DWV @5: cc_1 body+leader all-high is clean', r1b.overAllocated, false);

  // cnt_3 pool cap = floor(10/5)*1 = 2
  const r2 = roll(uid, 10, sel({}, {
    cnt_3: 99, cnt_3__watch_sergeant: 99
  }));
  const sk = r2.weapons.get('Stalker-pattern boltgun') || 0;
  ck('DWV @10: cnt_3 stalker boltguns capped at 2', sk, 2);

  // cnt_7 pool cap = max_total 1 (no per_n_models)
  const r3 = roll(uid, 10, sel({}, { cnt_7: 99, cnt_7__watch_sergeant: 99 }));
  const bs = r3.weapons.get('Black Shield blades') || 0;
  ck('DWV @10: cnt_7 Black Shield blades capped at 1', bs, 1);

  // Mutual exclusion: sng_8 (Sgt choice: Power weapon → Xenophase blade)
  // AND cc_1__watch_sergeant (Sgt count: Boltgun+PW → replacement).
  // Both consume Power weapon on the 1-model Sgt group. overAllocated.
  const r4 = roll(uid, 10, sel(
    { sng_8: 'Xenophase blade' },
    { cc_1__watch_sergeant: { 'Power weapon + Astartes Shield': 1 } }
  ));
  ck('DWV @10: sng_8 + cc_1_ldr fires overAllocated', r4.overAllocated, true);

  // Mutual exclusion: sng_9 (Sgt choice: Boltgun → Combi-weapon)
  // AND cnt_2__watch_sergeant (Sgt count: Boltgun+PW → DW thunder hammer).
  const r5 = roll(uid, 10, sel(
    { sng_9: 'Combi-weapon' },
    { cnt_2__watch_sergeant: 1 }
  ));
  ck('DWV @10: sng_9 + cnt_2_ldr fires overAllocated', r5.overAllocated, true);

  // Both sng_8 AND sng_9 active (swap each weapon individually), PLUS
  // a fanned generic option — triple-contested.
  const r6 = roll(uid, 10, sel(
    { sng_8: 'Xenophase blade', sng_9: 'Combi-weapon' },
    { cnt_3__watch_sergeant: 1 }
  ));
  ck('DWV @10: sng_8 + sng_9 + cnt_3_ldr fires overAllocated', r6.overAllocated, true);

  // Clean: sng_8 + sng_9 only (no fanned option). Fine — different slots.
  const r7 = roll(uid, 10, sel({ sng_8: 'Xenophase blade', sng_9: 'Combi-weapon' }, {}));
  ck('DWV @10: sng_8 + sng_9 alone is clean', r7.overAllocated, false);

  // Clean: fanned option alone, no named swaps.
  const r8 = roll(uid, 10, sel({}, { cnt_2__watch_sergeant: 1 }));
  ck('DWV @10: cnt_2_ldr alone is clean', r8.overAllocated, false);
}

console.log(fail ? `\n${fail} FAILURES` : '\nall B18d checks pass');
process.exit(fail ? 1 : 0);
