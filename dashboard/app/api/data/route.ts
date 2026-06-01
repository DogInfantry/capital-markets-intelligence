import { NextRequest, NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

function parseCSV(content: string) {
  const lines = content.trim().split('\n');
  if (lines.length < 2) return [];
  const headers = lines[0].split(',').map(h => h.trim().replace(/^"|"$/g, ''));
  return lines.slice(1).map(line => {
    const values: string[] = [];
    let current = '';
    let inQuotes = false;
    for (const char of line) {
      if (char === '"') { inQuotes = !inQuotes; }
      else if (char === ',' && !inQuotes) { values.push(current); current = ''; }
      else { current += char; }
    }
    values.push(current);
    const row: Record<string, string | number | null> = {};
    headers.forEach((h, i) => {
      const val = (values[i] || '').trim().replace(/^"|"$/g, '');
      const num = Number(val);
      row[h] = val === '' ? null : isNaN(num) ? val : num;
    });
    return row;
  });
}

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const file = searchParams.get('file');
  if (!file || file.includes('..')) {
    return NextResponse.json({ error: 'Invalid file' }, { status: 400 });
  }
  const dataDir = path.join(process.cwd(), 'public', 'data');
  const filePath = path.join(dataDir, file);
  try {
    const content = fs.readFileSync(filePath, 'utf-8');
    const data = parseCSV(content);
    return NextResponse.json(data);
  } catch {
    return NextResponse.json({ error: 'File not found' }, { status: 404 });
  }
}
