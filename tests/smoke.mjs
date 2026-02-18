import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

function parseCsvLine(line) {
  const out = [];
  let current = '';
  let inQuotes = false;

  for (let i = 0; i < line.length; i += 1) {
    const ch = line[i];
    if (ch === '"') {
      if (inQuotes && line[i + 1] === '"') {
        current += '"';
        i += 1;
      } else {
        inQuotes = !inQuotes;
      }
      continue;
    }

    if (ch === ',' && !inQuotes) {
      out.push(current);
      current = '';
      continue;
    }

    current += ch;
  }

  out.push(current);
  return out;
}

function loadRows() {
  const raw = fs.readFileSync(path.join(process.cwd(), 'data', 'combined_locations.csv'), 'utf8');
  const lines = raw.split(/\r?\n/).filter(Boolean);
  const headers = parseCsvLine(lines[0]);

  return lines.slice(1).map((line) => {
    const cols = parseCsvLine(line);
    const rec = {};
    headers.forEach((h, i) => {
      rec[h] = cols[i] ?? '';
    });
    return rec;
  });
}

test('core nextjs files exist', () => {
  const required = [
    'app/page.tsx',
    'app/layout.tsx',
    'app/globals.css',
    'components/Dashboard.tsx',
    'lib/data.ts',
    'lib/analytics.ts',
    'package.json'
  ];

  for (const file of required) {
    assert.equal(fs.existsSync(path.join(process.cwd(), file)), true, `${file} missing`);
  }
});

test('combined data remains readable and non-empty', () => {
  const rows = loadRows();
  assert.ok(rows.length > 4000, 'expected >4000 combined rows');

  const bobAtms = rows.filter((r) => r.source === 'Bank of Baku' && ['ATM', 'A', 'atm', 'network_atm'].includes(r.type));
  assert.ok(bobAtms.length >= 30, 'expected >=30 BOB ATMs');
});

test('legacy python streamlit app file removed', () => {
  assert.equal(fs.existsSync(path.join(process.cwd(), 'app.py')), false);
});
