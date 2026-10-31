// Replays the Python engine's results through the page's JavaScript engine and compares them.
//   python artifact/build.py --out /tmp/page.html --expected /tmp/expected.json
//   node artifact/verify_engine.js /tmp/page.html /tmp/expected.json
const fs = require('fs');
const crypto = require('crypto');
const assert = require('assert');

const [, , htmlPath, expectedPath] = process.argv;
const html = fs.readFileSync(htmlPath, 'utf8');
const engineSrc = html.slice(html.indexOf('/*ENGINE-START*/'), html.indexOf('/*ENGINE-END*/'));
const dataLine = html.split('\n').find(l => l.startsWith('const DEMO = '));
const DEMO = JSON.parse(dataLine.slice('const DEMO = '.length).replace(/;$/, ''));
const E = new Function(engineSrc + `; return { parseReport, prepClient, proposeFromRules, mockLines, buildJournal, runChecks, exportJournal, buildModelPayload,
  allPassed, sha256, plain, verifyChain, entryHash, parseMoney, parseDate, splitAmount, GENESIS };`)();
const expected = JSON.parse(fs.readFileSync(expectedPath, 'utf8'));

let failures = 0, checks = 0;
const eq = (label, a, b) => {
  checks++;
  try { assert.deepStrictEqual(a, b); } catch (e) {
    failures++;
    console.log(`  MISMATCH ${label}\n    js:     ${JSON.stringify(a).slice(0, 300)}\n    python: ${JSON.stringify(b).slice(0, 300)}`);
  }
};

// ---- sha256 against Node's implementation (multi-block, multibyte, empty, exactly 55/56/64 bytes)
for (const s of ['', 'abc', 'é'.repeat(40), 'x'.repeat(55), 'x'.repeat(56), 'x'.repeat(64), 'x'.repeat(1000), JSON.stringify(DEMO.files[0])]) {
  eq(`sha256(${s.length} chars)`, E.sha256(s), crypto.createHash('sha256').update(s, 'utf8').digest('hex'));
}

// ---- money / date parsing parity with app/money.py
const money = { '1234.5': 123450, '$1,234.56': 123456, '(12.00)': -1200, '-5': -500, '12-': -1200, '0': 0, ' 7 ': 700, '.5': 50, '0.005': 1, '0.004': 0, '2.675': 268 };
for (const [raw, cents] of Object.entries(money)) eq(`parseMoney(${raw})`, E.parseMoney(raw), cents);
for (const raw of ['', 'abc', '1e5', 'NaN', 'Infinity', '10/15/2026', '1.2.3', 'E1001', null]) eq(`parseMoney(${raw}) is null`, E.parseMoney(raw), null);
for (const raw of ['2026-10-15', '10/15/2026', '10/15/26', '2026-10-15 00:00:00']) eq(`parseDate(${raw})`, E.parseDate(raw), '2026-10-15');
eq('parseDate(garbage)', E.parseDate('soon'), null);
eq('parseDate(2026-02-30)', E.parseDate('2026-02-30'), null);

// ---- largest-remainder split property check vs. exact arithmetic
let rng = 12345; const rand = n => { rng = (rng * 1103515245 + 12345) & 0x7fffffff; return rng % n; };
for (let i = 0; i < 2000; i++) {
  const cents = rand(20000001) - 10000000, a = rand(101), b = rand(101 - a);
  const w = [{ code: 'A', pct: a }, { code: 'B', pct: b }, { code: 'C', pct: 100 - a - b }];
  const parts = E.splitAmount(cents, w);
  if (Object.values(parts).reduce((x, y) => x + y, 0) !== cents) { failures++; console.log('  split lost a cent', cents, w); break; }
}
checks++;

// ---- full cases
for (const c of expected) {
  const before = failures;
  const client = E.prepClient(DEMO.clients.find(x => x.id === c.clientId));
  const text = DEMO.files.find(f => f.filename === c.file).csv;
  const report = E.parseReport(text);
  eq(`${c.name}: headers`, report.headers, c.headers);
  let lines;
  if (c.how === 'rules') lines = E.proposeFromRules(report, client);
  else if (c.how === 'mock') lines = E.mockLines(report, client);
  else lines = DEMO.saved.find(m => m.version === +c.how.slice(-1)).lines;
  const keys = ['source_column', 'role', 'line_type', 'side', 'gl_account', 'offset_account', 'entity', 'fund', 'memo', 'origin', 'confidence', 'rationale', 'reviewed'];
  eq(`${c.name}: mapping lines`, lines.map(l => keys.map(k => l[k])), c.mapping.map(l => keys.map(k => l[k])));

  const j = E.buildJournal(report, lines, client, { start: c.start, end: c.end, allocate: c.allocate, target: c.target });
  eq(`${c.name}: journal lines`, j.lines.map(l => [l.line_no, l.account_no, l.entity, l.fund, E.plain(l.debit), E.plain(l.credit), l.memo, l.kind]), c.lines);
  eq(`${c.name}: reference/description`, [j.reference, j.description, E.plain(j.debits), E.plain(j.credits)], [c.reference, c.description, c.debits, c.credits]);
  const { checks: ck, tie } = E.runChecks(report, lines, client, j, c.start, c.end);
  eq(`${c.name}: checks (id, status, message)`, ck.map(x => [x.id, x.status, x.detail]), c.checks);
  eq(`${c.name}: tie-out`, tie.map(r => [r.column, E.plain(r.source), r.stated === null ? null : E.plain(r.stated), E.plain(r.journal), r.note]), c.tie);
  if (c.csv === null) { eq(`${c.name}: export blocked`, E.allPassed(ck), false); }
  else { eq(`${c.name}: export csv (byte for byte)`, E.exportJournal(j).csv, c.csv); eq(`${c.name}: export allowed`, E.allPassed(ck), true); }
  const red = E.buildModelPayload(report);
  eq(`${c.name}: redacted sample rows`, red.payload.sample_rows, c.payload_rows);
  eq(`${c.name}: redacted columns`, red.columns, c.columns_redacted);
  console.log(`${failures === before ? 'ok  ' : 'FAIL'} ${c.name} (${j.lines.length} lines, ${c.csv === null ? 'export blocked' : 'exportable'})`);
}

// ---- audit chain: valid, then detects an edit
const mk = (prev, n) => { const e = { ts: 't' + n, actor_email: 'a', actor_name: 'A', actor_roles: 'r', action: 'x' + n, client_id: null, job_id: null, mapping_version: null, file_sha256: null, details: '{}', prev }; e.hash = E.entryHash(prev, e); return e; };
const chain = []; let prev = E.GENESIS; for (let i = 0; i < 4; i++) { const e = mk(prev, i); chain.push(e); prev = e.hash; }
eq('audit chain verifies', E.verifyChain(chain).ok, true);
chain[1].actor_email = 'mallory'; eq('audit tamper detected at entry 2', E.verifyChain(chain), { ok: false, n: 4, brokenAt: 2 });

console.log(`\n${checks} comparisons, ${failures} mismatch(es)`);
process.exit(failures ? 1 : 0);
