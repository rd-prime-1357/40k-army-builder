// e4b_check.js — E4b. Loads the real enhancement engine out of index.html and
// exercises it against the real detachment catalogue. Per D107 these are claims
// about BEHAVIOUR, so they are executed rather than described in prose.
//
// What it holds:
//   1. the battle-size enhancement limit (25.03 table, Enhancement column)
//   2. eligibility: Character only, Epic Hero never, Upgrades to anyone but an
//      Epic Hero
//   3. the one-per-unit rule over an ATTACHED unit, not a single entry
//   4. name-keyed duplicates army-wide, three copies for an Upgrade
//   5. the count arithmetic — the 2nd and 3rd copy of an Upgrade are priced but
//      not counted, which is the single easiest thing in E4 to get wrong
//   6. hard block: a refused assignment leaves no trace on the entry
//   7. the attach gate, the second enforcement point
//   8. flag-don't-drop: a stale or over-limit state stays visible and exitable
//
// Build-time only; not part of the served app.
// Usage: node e4b_check.js index.html detachments.json
const fs = require('fs');

function slice(lines, startNeedle, endNeedle) {
  const s = lines.findIndex(l => l.includes(startNeedle));
  const e = lines.findIndex(l => l.includes(endNeedle));
  if (s < 0 || e < 0 || e <= s) throw new Error(`slice failed: ${startNeedle} .. ${endNeedle}`);
  return lines.slice(s, e).join('\n');
}

function loadEngine(path, defs) {
  const lines = fs.readFileSync(path, 'utf8').split('\n');
  const e4b = slice(lines, '// ── E4b: enhancement assignment rules', '// ── E4b block end');
  const src = 'let detachmentDefs = DEFS; let selectedDetachments = []; '
            + 'let armyList = []; let POINTS_CAP = 2000; '
            + 'function renderAll(){}\n'
            + e4b
            + '\nreturn { enhancementLimit, enhancementRecord, enhancementPoints, '
            + 'enhancementIsUpgrade, enhancementIsOffered, offeredEnhancements, '
            + 'assignedEnhancements, enhancementCount, enhancementCopies, '
            + 'enhancementMaxCopies, attachedGroupListIds, groupEnhancementCarriers, '
            + 'enhancementTypeEligible, canAssignEnhancement, enhancementArmyState, '
            + 'enhancementRowState, enhancementRefusalText, enhancementAttachBlock, '
            + 'enhancementPointsForEntry, assignEnhancement, clearEnhancement, '
            + 'setArmy: (a) => { armyList = a; }, '
            + 'setDetachments: (d) => { selectedDetachments = d; }, '
            + 'setCap: (p) => { POINTS_CAP = p; }, '
            + 'army: () => armyList };';
  return new Function('DEFS', src)(defs);
}

const idxPath = process.argv[2] || 'index.html';
const detPath = process.argv[3] || 'detachments.json';

const DJ = JSON.parse(fs.readFileSync(detPath, 'utf8'));
const E  = loadEngine(idxPath, DJ.detachments);

let fail = 0;
const ok = (cond, msg) => { if (!cond) { fail++; console.log('  FAIL ' + msg); } else console.log('  ok   ' + msg); };
const eq = (a, b, msg) => ok(JSON.stringify(a) === JSON.stringify(b), `${msg} (got ${JSON.stringify(a)})`);

// ── fixtures, all resolved out of the real catalogue ─────────────────────────
// Chosen because between them they exercise every refusal type and both sides
// of the Upgrade carve-out against records that actually exist.
const K_ICTF = 'Dark Angels|INNER CIRCLE TASK FORCE';   // Deathwing Assault @ 30
const K_WOTR = 'Dark Angels|WRATH OF THE ROCK';         // Deathwing Assault @ 15
const K_FIRE = 'Space Marines|FIRESTORM ASSAULT FORCE'; // Adamantine Mantle @ 20
const K_FORG = "Space Marines|FORGEFATHER'S SEEKERS";   // Adamantine Mantle @ 20
const K_FULG = 'Space Marines|FULGURIS TASK FORCE';     // Bellicose Weapon Spirits — Upgrade @ 15

const N_DWA  = 'Deathwing Assault';
const N_ADAM = 'Adamantine Mantle';
const N_BWS  = 'Bellicose Weapon Spirits';

function entry(listId, unitType, name, opts) {
  return Object.assign({
    listId: listId, unit_name: name || ('U' + listId), unit_type: unitType,
    enhancement: null, attachedToListId: null, unresolved: false
  }, opts || {});
}
function assign(e, name, key) { e.enhancement = { name: name, detachment_key: key }; return e; }

// Pick a second regular (non-Upgrade) enhancement off FIRESTORM so limit tests
// have distinct names to fill with, rather than hard-coding more literals.
const fireRegulars = (DJ.detachments[K_FIRE].enhancements || [])
  .filter(e => !e.is_upgrade).map(e => e.name);
const forgRegulars = (DJ.detachments[K_FORG].enhancements || [])
  .filter(e => !e.is_upgrade).map(e => e.name);

// ── 0. the fixtures are what the harness thinks they are ─────────────────────
// If the data moves under it, every scenario below would still "pass" while
// testing nothing. Assert the fixture facts first.
console.log('E4b — fixtures resolve against the real catalogue');
ok(E.enhancementPoints(N_DWA, K_ICTF) === 30 && E.enhancementPoints(N_DWA, K_WOTR) === 15,
   'the same enhancement name carries two different prices in two detachments (30 / 15)');
ok(E.enhancementIsUpgrade(N_BWS, K_FULG) === true, 'the Upgrade fixture is flagged is_upgrade');
ok(E.enhancementIsUpgrade(N_ADAM, K_FIRE) === false, 'the regular fixture is not flagged is_upgrade');
ok(fireRegulars.length >= 3 && forgRegulars.length >= 3,
   'both fixture detachments carry enough regular enhancements to fill a Strike Force limit');

// ── 1. the battle-size limit ─────────────────────────────────────────────────
// 25.03 Enhancement Limit column: Incursion 2, Strike Force 4. NOT the same as
// the DP column (2/3), which is why this is its own function.
console.log('E4b — the enhancement limit is the 25.03 Enhancement column');
ok(E.enhancementLimit(1000) === 2, 'Incursion (1000 pts) allows 2');
ok(E.enhancementLimit(2000) === 4, 'Strike Force (2000 pts) allows 4');
ok(E.enhancementLimit(3000) === 4, '3,000 pts falls in the Strike Force branch, as DP and unit limits do');
ok(E.enhancementLimit(999) === 2, 'below Incursion still reads as Incursion');

// ── 2. eligibility by unit_type ──────────────────────────────────────────────
console.log('E4b — eligibility: Character only, Epic Hero never, Upgrades wider');
ok(E.enhancementTypeEligible('Character', false) === true,  'a Character may take a regular enhancement');
ok(E.enhancementTypeEligible('Infantry', false) === false,  'a non-Character may not');
ok(E.enhancementTypeEligible('Epic Hero', false) === false, 'an Epic Hero may not');
ok(E.enhancementTypeEligible('Infantry', true) === true,    'a non-Character MAY take an Upgrade');
ok(E.enhancementTypeEligible('Vehicle', true) === true,     'so may a Vehicle');
ok(E.enhancementTypeEligible('Epic Hero', true) === false,
   'but an Epic Hero may NOT take an Upgrade — the Upgrade bullets lift the CHARACTER rule, not the EPIC HERO ban');

E.setDetachments([K_FIRE, K_FULG]);
{
  const hero = entry(1, 'Epic Hero'), inf = entry(2, 'Infantry'), chr = entry(3, 'Character');
  E.setArmy([hero, inf, chr]);
  eq(E.canAssignEnhancement(hero, N_ADAM, K_FIRE, 2000).reason, 'unit_type', 'Epic Hero + regular refuses on unit_type');
  eq(E.canAssignEnhancement(hero, N_BWS, K_FULG, 2000).reason, 'unit_type', 'Epic Hero + Upgrade refuses on unit_type');
  eq(E.canAssignEnhancement(inf, N_ADAM, K_FIRE, 2000).reason, 'unit_type', 'Infantry + regular refuses on unit_type');
  ok(E.canAssignEnhancement(inf, N_BWS, K_FULG, 2000).ok === true, 'Infantry + Upgrade is allowed');
  ok(E.canAssignEnhancement(chr, N_ADAM, K_FIRE, 2000).ok === true, 'Character + regular is allowed');
}

// ── 3. one per unit, where "unit" means the attached unit ────────────────────
console.log('E4b — one enhancement per unit, counted over the attached unit');
{
  const bg     = entry(1, 'Infantry', 'Bodyguard');
  const leadA  = entry(2, 'Character', 'Leader A', { attachedToListId: 1 });
  const leadB  = entry(3, 'Character', 'Leader B', { attachedToListId: 1 });
  const lone   = entry(4, 'Character', 'Lone');
  E.setArmy([bg, leadA, leadB, lone]);
  eq(E.attachedGroupListIds(2).sort(), [1, 2, 3], 'the cluster is the bodyguard plus everything attached to it');
  eq(E.attachedGroupListIds(4), [4], 'an unattached entry is its own cluster');

  assign(leadA, N_ADAM, K_FIRE);
  eq(E.canAssignEnhancement(leadB, fireRegulars.find(n => n !== N_ADAM), K_FIRE, 2000).reason, 'unit_has_one',
     'a co-leader in the same attached unit is refused on unit_has_one');
  eq(E.canAssignEnhancement(bg, N_BWS, K_FULG, 2000).reason, 'unit_has_one',
     'the bodyguard of that attached unit is refused too, even for an Upgrade');
  ok(E.canAssignEnhancement(lone, fireRegulars.find(n => n !== N_ADAM), K_FIRE, 2000).ok === true,
     'a separate unit elsewhere in the army is unaffected');
  ok(E.canAssignEnhancement(leadA, N_ADAM, K_FIRE, 2000).ok === true,
     're-picking the row the entry already holds is never self-blocking');
}

// ── 4. duplicates are name-keyed army-wide, across detachments ───────────────
// The 29-collision finding is the reason. Two detachments both offering
// Adamantine Mantle must still allow only one in the army.
console.log('E4b — duplicates are name-keyed army-wide, not per detachment');
E.setDetachments([K_FIRE, K_FORG, K_FULG]);
{
  const a = assign(entry(1, 'Character'), N_ADAM, K_FIRE);
  const b = entry(2, 'Character');
  E.setArmy([a, b]);
  eq(E.canAssignEnhancement(b, N_ADAM, K_FORG, 2000).reason, 'duplicate',
     'the same name from a DIFFERENT detachment is still a duplicate');
  ok(E.canAssignEnhancement(b, N_ADAM, K_FIRE, 2000).reason === 'duplicate',
     'and so is the same name from the same detachment');
}

// ── 5. Upgrades: three copies, and the count carve-out ───────────────────────
// The rule: "You can include up to three of the same Upgrade in your army (the
// second and third instances do not count towards the total number of
// enhancements in your army, but you must still spend the stated points cost
// each time)." Three thresholds live in this one paragraph and they differ.
console.log('E4b — Upgrades: three copies allowed, only the first counts');
E.setDetachments([K_FIRE, K_FULG]);
{
  const mk = (id) => assign(entry(id, 'Infantry'), N_BWS, K_FULG);
  const one   = [mk(1)];
  const two   = [mk(1), mk(2)];
  const three = [mk(1), mk(2), mk(3)];
  E.setArmy(one);   eq(E.enhancementCount(E.assignedEnhancements()), 1, 'one copy of an Upgrade counts 1');
  E.setArmy(two);   eq(E.enhancementCount(E.assignedEnhancements()), 1, 'two copies still count 1');
  E.setArmy(three); eq(E.enhancementCount(E.assignedEnhancements()), 1, 'three copies still count 1');

  // ...but every copy is still paid for.
  const paid = three.reduce((s, e) => s + E.enhancementPointsForEntry(e), 0);
  eq(paid, 45, 'all three copies are priced (3 x 15 pts), even though only one counts');

  // The fourth is refused.
  E.setArmy(three.concat([entry(4, 'Infantry')]));
  eq(E.canAssignEnhancement(E.army()[3], N_BWS, K_FULG, 2000).reason, 'duplicate',
     'a fourth copy of the same Upgrade is refused');
  eq(E.canAssignEnhancement(E.army()[3], N_BWS, K_FULG, 2000).max, 3,
     'and the refusal names three as the ceiling');

  // Two copies at Incursion, where the limit is 2: the second copy must not
  // consume the second slot, so a regular still fits alongside.
  E.setArmy([mk(1), mk(2), entry(3, 'Character')]);
  eq(E.enhancementCount(E.assignedEnhancements()), 1, 'two Upgrade copies read as 1 against an Incursion limit of 2');
  ok(E.canAssignEnhancement(E.army()[2], N_ADAM, K_FIRE, 1000).ok === true,
     'so a regular enhancement still fits at Incursion alongside two copies of an Upgrade');
}

// ── 6. the army limit ────────────────────────────────────────────────────────
console.log('E4b — the army limit blocks the (limit + 1)th distinct enhancement');
E.setDetachments([K_FIRE, K_FORG]);
{
  const names = Array.from(new Set(fireRegulars.concat(forgRegulars)));
  const keyFor = (n) => fireRegulars.indexOf(n) >= 0 ? K_FIRE : K_FORG;

  // Fill to the Incursion limit of 2, then probe.
  const filled2 = [assign(entry(1, 'Character'), names[0], keyFor(names[0])),
                   assign(entry(2, 'Character'), names[1], keyFor(names[1]))];
  const probe = entry(3, 'Character');
  E.setArmy(filled2.concat([probe]));
  eq(E.enhancementCount(E.assignedEnhancements()), 2, 'two regulars count 2');
  eq(E.canAssignEnhancement(probe, names[2], keyFor(names[2]), 1000).reason, 'army_limit',
     'a third is refused at Incursion');
  ok(E.canAssignEnhancement(probe, names[2], keyFor(names[2]), 2000).ok === true,
     'the same pick is allowed at Strike Force, where the limit is 4');

  const st = E.enhancementArmyState(1000);
  eq([st.used, st.limit, st.state, st.legal], [2, 2, 'at', true],
     'the army state reads at-limit and still legal');
}

// ── 7. hard block — a refusal leaves no trace ────────────────────────────────
// D0: illegal states are unreachable, not flagged. The action is the gate.
console.log('E4b — a refused assignment is a no-op, not an accepted-then-flagged pick');
E.setDetachments([K_FIRE, K_FULG]);
{
  const hero = entry(1, 'Epic Hero');
  E.setArmy([hero]);
  E.assignEnhancement(1, N_ADAM, K_FIRE);
  ok(hero.enhancement === null, 'assigning to an Epic Hero leaves the entry untouched');

  const chr = entry(2, 'Character');
  E.setArmy([chr]);
  E.assignEnhancement(2, N_ADAM, K_FIRE);
  eq(chr.enhancement, { name: N_ADAM, detachment_key: K_FIRE }, 'a legal assignment lands with its detachment key');
  E.assignEnhancement(2, N_ADAM, K_FIRE);
  ok(chr.enhancement === null, 'picking the same row again clears it');

  // An unoffered pick is refused even when the record exists in the catalogue.
  E.setDetachments([K_FIRE]);
  const chr2 = entry(3, 'Character');
  E.setArmy([chr2]);
  eq(E.canAssignEnhancement(chr2, N_DWA, K_WOTR, 2000).reason, 'not_offered',
     'an enhancement from an unselected detachment is not offered');
  E.assignEnhancement(3, N_DWA, K_WOTR);
  ok(chr2.enhancement === null, 'and the action refuses it');
}

// ── 8. the attach gate — the second enforcement point ────────────────────────
console.log('E4b — the attach action refuses to merge two carriers into one unit');
E.setDetachments([K_FIRE, K_FORG]);
{
  const bg   = assign(entry(1, 'Infantry', 'Bodyguard'), N_BWS, K_FULG);
  const lead = assign(entry(2, 'Character', 'Leader'), N_ADAM, K_FIRE);
  E.setArmy([bg, lead]);
  ok(E.enhancementAttachBlock(2, 1) !== null, 'attaching a carrier to a carrier is blocked');
  eq(E.enhancementAttachBlock(2, 1).carrier, 'Bodyguard', 'and the block names the other carrier');
  ok(E.enhancementAttachBlock(2, null) === null, 'detaching is always allowed');

  bg.enhancement = null;
  ok(E.enhancementAttachBlock(2, 1) === null, 'once the bodyguard is clear, the attach is allowed');
  lead.enhancement = null;
  bg.enhancement = { name: N_BWS, detachment_key: K_FULG };
  ok(E.enhancementAttachBlock(2, 1) === null, 'a leader with no enhancement may join a carrier');
}

// ── 9. flag-don't-drop: stale and over states stay visible and exitable ──────
console.log("E4b — stale and over-limit states stay visible, and stay exitable");
E.setDetachments([K_FIRE]);
{
  // An assignment out of a detachment that is no longer selected.
  const stale = assign(entry(1, 'Character'), N_DWA, K_WOTR);
  E.setArmy([stale]);
  const st = E.enhancementArmyState(2000);
  eq(st.notOffered.length, 1, 'a stale assignment is reported, not deleted');
  ok(st.legal === false, 'and the army reads illegal while it is there');
  ok(E.enhancementPointsForEntry(stale) === 15,
     'it is still priced from the catalogue record while that record resolves');

  // A key that no longer resolves at all prices at 0 rather than guessing.
  const ghost = assign(entry(2, 'Character'), 'No Such Enhancement', 'Space Marines|GONE');
  E.setArmy([ghost]);
  ok(E.enhancementPointsForEntry(ghost) === 0, 'an unresolvable assignment contributes 0 points');
  ok(E.enhancementIsUpgrade('No Such Enhancement', 'Space Marines|GONE') === false,
     'and reads as a regular, so it cannot buy Upgrade headroom');
  eq(E.enhancementArmyState(2000).notOffered.length, 1, 'and it is still surfaced');

  // Over-limit by battle-size change: four legal picks at Strike Force, then
  // the player drops to Incursion. Every row must stay clearable.
  const names = Array.from(new Set(fireRegulars.concat(forgRegulars)));
  E.setDetachments([K_FIRE, K_FORG]);
  const keyFor = (n) => fireRegulars.indexOf(n) >= 0 ? K_FIRE : K_FORG;
  const four = names.slice(0, 4).map((n, i) => assign(entry(i + 1, 'Character'), n, keyFor(n)));
  E.setArmy(four);
  eq(E.enhancementArmyState(1000).state, 'over', 'dropping to Incursion leaves the army over the limit');
  ok(E.enhancementArmyState(1000).legal === false, 'which reads as illegal');
  for (const e of four) {
    const rs = E.enhancementRowState(e, e.enhancement.name, e.enhancement.detachment_key, 1000);
    ok(rs.selected === true && rs.disabled === false,
       `the selected row on ${e.unit_name} stays enabled so the state can be exited`);
  }
  E.clearEnhancement(1);
  eq(E.enhancementArmyState(1000).used, 3, 'and clearing one brings the count down');
}

// ── 10. the row classifier is canAssignEnhancement, not a second copy ────────
// The E1c-1 story applied to E4b: for a non-selected row, disabled must be
// exactly !canAssignEnhancement(...).ok, for every offered row in every
// scenario. If that ever stops holding, a second implementation of the five
// rules is living in the classifier.
console.log('E4b — the row classifier is the read path, not a second copy of it');
{
  const scenarios = [
    { name: 'empty army, Strike Force', dets: [K_FIRE, K_FORG, K_FULG], pts: 2000,
      army: () => [entry(1, 'Character'), entry(2, 'Infantry'), entry(3, 'Epic Hero')] },
    { name: 'one regular assigned, Incursion', dets: [K_FIRE, K_FORG, K_FULG], pts: 1000,
      army: () => [assign(entry(1, 'Character'), N_ADAM, K_FIRE), entry(2, 'Character'), entry(3, 'Vehicle')] },
    { name: 'at the Incursion limit', dets: [K_FIRE, K_FORG, K_FULG], pts: 1000,
      army: () => {
        const n = Array.from(new Set(fireRegulars.concat(forgRegulars)));
        const keyFor = (x) => fireRegulars.indexOf(x) >= 0 ? K_FIRE : K_FORG;
        return [assign(entry(1, 'Character'), n[0], keyFor(n[0])),
                assign(entry(2, 'Character'), n[1], keyFor(n[1])),
                entry(3, 'Character')];
      } },
    { name: 'attached unit already carrying one', dets: [K_FIRE, K_FULG], pts: 2000,
      army: () => [entry(1, 'Infantry', 'BG'),
                   assign(entry(2, 'Character', 'L1', { attachedToListId: 1 }), N_ADAM, K_FIRE),
                   entry(3, 'Character', 'L2', { attachedToListId: 1 })] },
    { name: 'two Upgrade copies down', dets: [K_FULG, K_FIRE], pts: 2000,
      army: () => [assign(entry(1, 'Infantry'), N_BWS, K_FULG),
                   assign(entry(2, 'Infantry'), N_BWS, K_FULG),
                   entry(3, 'Infantry'), entry(4, 'Character')] },
  ];

  let rows = 0, mismatches = 0;
  for (const sc of scenarios) {
    E.setDetachments(sc.dets);
    const army = sc.army();
    E.setArmy(army);
    for (const e of army) {
      for (const off of E.offeredEnhancements()) {
        const rs = E.enhancementRowState(e, off.name, off.detachment_key, sc.pts);
        const ca = E.canAssignEnhancement(e, off.name, off.detachment_key, sc.pts);
        rows++;
        const expected = rs.selected ? false : !ca.ok;
        if (rs.disabled !== expected) {
          mismatches++;
          if (mismatches <= 3)
            console.log(`       ${sc.name} / ${e.unit_name} / ${off.name}: disabled=${rs.disabled} expected=${expected}`);
        }
        if (!ca.ok && !E.enhancementRefusalText(ca)) {
          mismatches++;
          if (mismatches <= 3) console.log(`       mute refusal: ${ca.reason}`);
        }
      }
    }
  }
  ok(rows >= 100, `the sweep covered a meaningful number of rows (${rows})`);
  ok(mismatches === 0, `every row's disabled flag is canAssignEnhancement's answer, and no refusal is mute (${mismatches} mismatches)`);
}

console.log(fail === 0 ? '\nall E4b checks pass' : `\n${fail} E4b check(s) FAILED`);
process.exit(fail === 0 ? 0 : 1);
