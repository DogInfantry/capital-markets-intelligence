'use client';
import { useState, useEffect } from 'react';
import {
  AreaChart, Area, BarChart, Bar, LineChart, Line,
  RadarChart, Radar, PolarGrid, PolarAngleAxis,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  ResponsiveContainer, Cell, ReferenceLine, PieChart, Pie
} from 'recharts';
import {
  TrendingUp, Globe, Zap, Leaf, BarChart2, GitBranch,
  CheckCircle2, Activity, Shield, Target, ArrowUpRight,
  ArrowDownRight, ExternalLink, AlertCircle
} from 'lucide-react';

// ─── DATA ─────────────────────────────────────────────────────────────────────

const GREEN_BONDS = [
  { year: '2015', amount: 1000, type: 'psu' },
  { year: '2016', amount: 500,  type: 'bank' },
  { year: '2017', amount: 2300, type: 'psu' },
  { year: '2018', amount: 1400, type: 'corporate' },
  { year: '2019', amount: 1950, type: 'psu' },
  { year: '2020', amount: 1200, type: 'psu' },
  { year: '2021', amount: 700,  type: 'bank' },
  { year: '2022', amount: 2900, type: 'psu' },
  { year: '2023', amount: 26400, type: 'sovereign' },
  { year: '2024', amount: 26850, type: 'sovereign' },
];

const SECTOR_CAPITAL = [
  { sector: 'Utility Renewables', need: 32.0, color: '#10B981' },
  { sector: 'Grid & Transmission', need: 24.0, color: '#06B6D4' },
  { sector: 'Industrial Decarb',   need: 27.5, color: '#F59E0B' },
  { sector: 'EV & Fleet',          need: 14.8, color: '#0EA5E9' },
  { sector: 'Battery Storage',     need: 11.5, color: '#8B5CF6' },
  { sector: 'Green Buildings',     need: 8.2,  color: '#F97316' },
];

const EMISSIONS = [
  { sector: 'Power',       baseline: 1120, y2030: 860,  y2050: 210, lever: 'Renewables + Storage' },
  { sector: 'Steel',       baseline: 290,  y2030: 240,  y2050: 92,  lever: 'H₂-DRI + Scrap-EAF' },
  { sector: 'Transport',   baseline: 340,  y2030: 255,  y2050: 95,  lever: 'Fleet Electrification' },
  { sector: 'Agriculture', baseline: 410,  y2030: 372,  y2050: 250, lever: 'Methane Reduction' },
  { sector: 'Cement',      baseline: 210,  y2030: 176,  y2050: 78,  lever: 'Clinker Sub + CCUS' },
  { sector: 'Buildings',   baseline: 125,  y2030: 96,   y2050: 44,  lever: 'Efficiency + Cooling' },
];

const NET_ZERO_PATH = [
  { year: 2025, renewGW: 190,  evShare: 8,  emissionsRed: 10 },
  { year: 2030, renewGW: 500,  evShare: 30, emissionsRed: 28 },
  { year: 2040, renewGW: 1000, evShare: 70, emissionsRed: 52 },
  { year: 2050, renewGW: 1800, evShare: 95, emissionsRed: 73 },
  { year: 2070, renewGW: 2500, evShare: 100,emissionsRed: 100 },
];

const ESG_SCORES = [
  { ticker: 'INFY',     name: 'Infosys',      sector: 'IT',         E: 82, S: 80, G: 88, composite: 83.4, coal: 0 },
  { ticker: 'TCS',      name: 'TCS',           sector: 'IT',         E: 78, S: 82, G: 85, composite: 81.4, coal: 0 },
  { ticker: 'WIPRO',    name: 'Wipro',         sector: 'IT',         E: 80, S: 75, G: 82, composite: 79.1, coal: 0 },
  { ticker: 'HCLTECH',  name: 'HCL Tech',      sector: 'IT',         E: 76, S: 72, G: 80, composite: 76.2, coal: 0 },
  { ticker: 'HDFCBANK', name: 'HDFC Bank',     sector: 'Financials', E: 62, S: 70, G: 80, composite: 70.0, coal: 0 },
  { ticker: 'ICICIBNK', name: 'ICICI Bank',    sector: 'Financials', E: 58, S: 65, G: 78, composite: 66.5, coal: 0 },
  { ticker: 'MARUTI',   name: 'Maruti Suzuki', sector: 'Con. Disc.', E: 52, S: 62, G: 74, composite: 61.4, coal: 0 },
  { ticker: 'LT',       name: 'L&T',           sector: 'Industrials',E: 50, S: 60, G: 75, composite: 60.5, coal: 0 },
  { ticker: 'RELIANCE', name: 'Reliance',      sector: 'Energy',     E: 42, S: 55, G: 68, composite: 52.6, coal: 5 },
  { ticker: 'TATASTL',  name: 'Tata Steel',    sector: 'Materials',  E: 40, S: 58, G: 72, composite: 52.0, coal: 0 },
  { ticker: 'JSWSTL',   name: 'JSW Steel',     sector: 'Materials',  E: 35, S: 50, G: 66, composite: 46.8, coal: 0 },
  { ticker: 'ULTRACM',  name: 'UltraTech',     sector: 'Materials',  E: 32, S: 52, G: 68, composite: 46.4, coal: 0 },
  { ticker: 'NTPC',     name: 'NTPC',          sector: 'Utilities',  E: 30, S: 55, G: 65, composite: 45.5, coal: 85 },
  { ticker: 'COALIND',  name: 'Coal India',    sector: 'Energy',     E: 18, S: 52, G: 58, composite: 36.2, coal: 98 },
];

const DEAL_ECONOMICS = [
  { sector: 'Utility RE',    deals: 18, ticket: 1450, feeBps: 85,  feePool: 221.9 },
  { sector: 'Grid & Tx',     deals: 9,  ticket: 2800, feeBps: 52,  feePool: 131.0 },
  { sector: 'Indus. Decarb', deals: 13, ticket: 2350, feeBps: 105, feePool: 320.8 },
  { sector: 'Battery',       deals: 11, ticket: 1180, feeBps: 95,  feePool: 123.3 },
  { sector: 'Green Bldg',    deals: 24, ticket: 265,  feeBps: 115, feePool: 73.1  },
  { sector: 'EV & Fleet',    deals: 21, ticket: 180,  feeBps: 140, feePool: 52.9  },
];

const RADAR_DATA = [
  { sector: 'IT',          E: 79, S: 77, G: 84 },
  { sector: 'Financials',  E: 58, S: 66, G: 78 },
  { sector: 'Materials',   E: 37, S: 53, G: 69 },
  { sector: 'Energy',      E: 30, S: 54, G: 63 },
  { sector: 'Industrials', E: 50, S: 60, G: 75 },
];

const ISSUES = [
  { id: 16, title: 'Companion notebooks for src/ modules',    labels: ['documentation', 'notebook'] },
  { id: 15, title: 'RBI climate-risk capital impact model',   labels: ['model-needed', 'policy'] },
  { id: 14, title: 'State-level ESG readiness overlay',       labels: ['data-gap', 'research-gap'] },
  { id: 13, title: 'Green buildings & municipal finance',     labels: ['sector-expansion'] },
  { id: 12, title: 'Green MSME & fintech archetypes',         labels: ['data-gap', 'sector-expansion'] },
  { id: 10, title: 'BRSR disclosure quality overlay',         labels: ['good first issue', 'data-gap'] },
  { id: 8,  title: 'SGrB yield & greenium module',            labels: ['data-gap', 'model-needed'] },
];

const COMMITS = [
  { sha: '73cad19', msg: 'Add missing synthetic data files', date: 'May 25' },
  { sha: 'c04f10e', msg: 'docs: unified README combining research + commercial layer', date: 'Apr 7' },
  { sha: '762657c', msg: 'Add CONTRIBUTING.md, issue templates, missing core models', date: 'Apr 7' },
  { sha: 'ed69893', msg: 'docs: overhaul README with clean structure and key findings', date: 'Apr 5' },
  { sha: 'a1b2c3d', msg: 'feat: merge React dashboard into main', date: 'Jun 3' },
];

const POLICIES = [
  { body: 'SEBI',     instrument: 'BRSR Core Mandate',        year: 2023, status: 'Active',        impact: 'High',   desc: 'Top 150 listed cos — mandatory sustainability reporting' },
  { body: 'SEBI',     instrument: 'Green/SLB Framework',      year: 2021, status: 'Active',        impact: 'High',   desc: 'Listing reqs for labelled bonds; use-of-proceeds + SPT disclosures' },
  { body: 'RBI',      instrument: 'Climate Risk Framework',   year: 2023, status: 'Consultation',  impact: 'Medium', desc: 'Draft guidance on climate-related financial risks; capital impact TBD' },
  { body: 'GoI',      instrument: 'Sovereign Green Bonds',    year: 2023, status: 'Active',        impact: 'High',   desc: '₹44,000Cr issued — establishes sovereign green yield curve' },
  { body: 'NITI',     instrument: 'Low Carbon Dev. Strategy', year: 2022, status: 'Published',     impact: 'Medium', desc: 'Net Zero 2070 roadmap with sectoral pathways & investment needs' },
  { body: 'MoEFCC',   instrument: 'Carbon Credit Trading',    year: 2023, status: 'Developing',    impact: 'High',   desc: 'CCTS domestic carbon market; BEE-linked credit issuance' },
];

const PRODUCTS = [
  { name: 'Green Project Finance',    family: 'Use of Proceeds', tenor: '10–18yr', h2a: 'Medium', color: '#10B981' },
  { name: 'Green Corporate Term Loan',family: 'Use of Proceeds', tenor: '3–7yr',   h2a: 'Medium', color: '#06B6D4' },
  { name: 'Green Bond',               family: 'Use of Proceeds', tenor: '5–12yr',  h2a: 'Low',    color: '#0EA5E9' },
  { name: 'Sustainability-Linked Loan',family: 'SLL',            tenor: '3–7yr',   h2a: 'High',   color: '#F59E0B' },
  { name: 'Transition Finance Loan',  family: 'Transition',      tenor: '5–12yr',  h2a: 'High',   color: '#F97316' },
  { name: 'Blended Finance (DFI+)',   family: 'Blended',         tenor: '7–15yr',  h2a: 'High',   color: '#8B5CF6' },
  { name: 'Carbon / Results-Based',   family: 'Carbon',          tenor: '1–10yr',  h2a: 'High',   color: '#EF4444' },
  { name: 'Green Securitisation',     family: 'Structured',      tenor: '3–8yr',   h2a: 'Low',    color: '#38BDF8' },
];

// ─── TABS ─────────────────────────────────────────────────────────────────────

const TABS = [
  { id: 'overview',   label: 'Overview',   Icon: Activity },
  { id: 'capital',    label: 'Capital',    Icon: BarChart2 },
  { id: 'emissions',  label: 'Emissions',  Icon: Globe },
  { id: 'esg',        label: 'ESG',        Icon: Leaf },
  { id: 'products',   label: 'Products',   Icon: Shield },
  { id: 'policy',     label: 'Policy',     Icon: CheckCircle2 },
  { id: 'repo',       label: 'Repo',       Icon: GitBranch },
];

// ─── TOOLTIP ─────────────────────────────────────────────────────────────────

function CT({ active, payload, label }: { active?: boolean; payload?: { name: string; value: number; color: string }[]; label?: string }) {
  if (!active || !payload?.length) return null;
  return (
    <div className="bg-[#080F18] border border-[#1A2A3A] rounded-lg p-3 text-xs font-mono shadow-xl">
      <div className="text-[#7A9BBE] mb-2">{label}</div>
      {payload.map((p, i) => (
        <div key={i} style={{ color: p.color }} className="mt-1">
          {p.name}: <span className="text-[#E2EAF4]">{typeof p.value === 'number' ? p.value.toLocaleString() : p.value}</span>
        </div>
      ))}
    </div>
  );
}

// ─── KPI CARD ─────────────────────────────────────────────────────────────────

function KpiCard({ label, value, sub, Icon, color = '#10B981', delta }: {
  label: string; value: string; sub?: string; Icon: React.ElementType; color?: string; delta?: number;
}) {
  return (
    <div className="bg-[#0B1420] border border-[#1A2A3A] rounded-xl p-5 flex flex-col gap-2 hover:border-[#1E3A5F] transition-colors">
      <div className="flex justify-between items-start">
        <span className="font-mono text-[10px] text-[#3D5A7A] uppercase tracking-widest">{label}</span>
        <Icon size={14} color={color} />
      </div>
      <div className="font-['Syne'] text-3xl font-extrabold leading-none" style={{ color }}>{value}</div>
      {sub && <div className="font-mono text-[10px] text-[#3D5A7A]">{sub}</div>}
      {delta !== undefined && (
        <div className="flex items-center gap-1">
          {delta >= 0 ? <ArrowUpRight size={11} color="#10B981" /> : <ArrowDownRight size={11} color="#EF4444" />}
          <span className="font-mono text-[10px]" style={{ color: delta >= 0 ? '#10B981' : '#EF4444' }}>
            {Math.abs(delta)}% YoY
          </span>
        </div>
      )}
    </div>
  );
}

// ─── SECTION COMPONENTS ───────────────────────────────────────────────────────

function OverviewSection() {
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        <KpiCard label="Green Bond Issuance" value="₹65K Cr" sub="2015–2024 cumulative" Icon={TrendingUp} color="#10B981" delta={41} />
        <KpiCard label="Annual Capital Need" value="$118B" sub="6 priority sectors" Icon={Target} color="#06B6D4" />
        <KpiCard label="Est. Fee Pool" value="₹923Cr" sub="illustrative annual" Icon={BarChart2} color="#F59E0B" />
        <KpiCard label="Net Zero Target" value="2070" sub="India NDC pathway" Icon={Globe} color="#0EA5E9" />
        <KpiCard label="2030 RE Target" value="500 GW" sub="under India NZ scenario" Icon={Zap} color="#8B5CF6" />
        <KpiCard label="Open Issues" value="14" sub="v1.1 → v2.0 roadmap" Icon={GitBranch} color="#EF4444" />
      </div>

      <div className="bg-[#0B1420] border border-[#1A2A3A] rounded-xl p-5">
        <div className="font-['Syne'] font-semibold text-sm text-[#E2EAF4] mb-4">
          India Green Bond Issuance Timeline (₹ Crore)
        </div>
        <ResponsiveContainer width="100%" height={240}>
          <AreaChart data={GREEN_BONDS}>
            <defs>
              <linearGradient id="gbg" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#10B981" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#10B981" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#1A2A3A" />
            <XAxis dataKey="year" stroke="#3D5A7A" tick={{ fontSize: 11, fontFamily: 'monospace', fill: '#3D5A7A' }} />
            <YAxis stroke="#3D5A7A" tick={{ fontSize: 11, fontFamily: 'monospace', fill: '#3D5A7A' }} tickFormatter={v => `₹${(v/1000).toFixed(0)}K`} />
            <Tooltip content={<CT />} />
            <Area type="monotone" dataKey="amount" name="₹ Crore" stroke="#10B981" fill="url(#gbg)" strokeWidth={2} dot={{ fill: '#10B981', r: 3 }} />
          </AreaChart>
        </ResponsiveContainer>
        <div className="flex gap-4 mt-3 flex-wrap">
          {[['Sovereign', '#0EA5E9'], ['PSU', '#10B981'], ['Corporate', '#F59E0B'], ['Bank', '#8B5CF6']].map(([l, c]) => (
            <div key={l} className="flex items-center gap-1.5">
              <div className="w-2 h-2 rounded-full" style={{ background: c as string }} />
              <span className="font-mono text-[10px] text-[#3D5A7A]">{l}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function CapitalSection() {
  return (
    <div className="space-y-4">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <div className="bg-[#0B1420] border border-[#1A2A3A] rounded-xl p-5">
          <div className="font-['Syne'] font-semibold text-sm text-[#E2EAF4] mb-4">Annual Capital Need by Subsector (USD Bn)</div>
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={SECTOR_CAPITAL} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="#1A2A3A" />
              <XAxis type="number" stroke="#3D5A7A" tick={{ fontSize: 11, fontFamily: 'monospace', fill: '#3D5A7A' }} unit="B" />
              <YAxis type="category" dataKey="sector" width={140} tick={{ fontSize: 11, fontFamily: 'monospace', fill: '#7A9BBE' }} />
              <Tooltip content={<CT />} />
              <Bar dataKey="need" name="USD Bn" radius={[0, 4, 4, 0]}>
                {SECTOR_CAPITAL.map((d, i) => <Cell key={i} fill={d.color} />)}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-[#0B1420] border border-[#1A2A3A] rounded-xl p-5">
          <div className="font-['Syne'] font-semibold text-sm text-[#E2EAF4] mb-4">Fee Pool (₹Cr) vs Deal Count</div>
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={DEAL_ECONOMICS}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1A2A3A" />
              <XAxis dataKey="sector" tick={{ fontSize: 10, fontFamily: 'monospace', fill: '#3D5A7A' }} angle={-20} textAnchor="end" height={50} />
              <YAxis yAxisId="l" tick={{ fontSize: 10, fontFamily: 'monospace', fill: '#3D5A7A' }} />
              <YAxis yAxisId="r" orientation="right" tick={{ fontSize: 10, fontFamily: 'monospace', fill: '#3D5A7A' }} />
              <Tooltip content={<CT />} />
              <Legend wrapperStyle={{ fontFamily: 'monospace', fontSize: 10, color: '#7A9BBE' }} />
              <Bar yAxisId="l" dataKey="feePool" name="Fee Pool ₹Cr" fill="#F59E0B" opacity={0.85} radius={[4, 4, 0, 0]} />
              <Bar yAxisId="r" dataKey="deals" name="Deals" fill="#0EA5E9" opacity={0.7} radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="bg-[#0B1420] border border-[#1A2A3A] rounded-xl p-5 overflow-x-auto">
        <div className="font-['Syne'] font-semibold text-sm text-[#E2EAF4] mb-4">Deal Economics — Full Matrix</div>
        <table className="w-full font-mono text-xs border-collapse min-w-[600px]">
          <thead>
            <tr>
              {['Subsector', 'Deals/yr', 'Avg Ticket ₹Cr', 'Fee (bps)', 'Fee Pool ₹Cr', 'Risk Profile'].map(h => (
                <th key={h} className="text-left py-2 px-3 text-[#3D5A7A] border-b border-[#1A2A3A] font-normal">{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {DEAL_ECONOMICS.map((d, i) => {
              const cap = SECTOR_CAPITAL[i];
              return (
                <tr key={i} className="border-b border-[#1A2A3A] hover:bg-[#0F1C2E] transition-colors">
                  <td className="py-2.5 px-3 text-[#E2EAF4]">{d.sector}</td>
                  <td className="py-2.5 px-3 text-[#7A9BBE]">{d.deals}</td>
                  <td className="py-2.5 px-3 text-[#7A9BBE]">₹{d.ticket.toLocaleString()}</td>
                  <td className="py-2.5 px-3 text-[#F59E0B]">{d.feeBps} bps</td>
                  <td className="py-2.5 px-3 text-[#10B981]">₹{d.feePool}</td>
                  <td className="py-2.5 px-3">
                    <span className="px-2 py-0.5 rounded text-[10px]" style={{ background: (cap?.color || '#10B981') + '20', color: cap?.color || '#10B981' }}>
                      Core+
                    </span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function EmissionsSection() {
  return (
    <div className="space-y-4">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <div className="bg-[#0B1420] border border-[#1A2A3A] rounded-xl p-5">
          <div className="font-['Syne'] font-semibold text-sm text-[#E2EAF4] mb-4">Sector Emissions: Baseline → 2030 → 2050 (MtCO₂e)</div>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={EMISSIONS}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1A2A3A" />
              <XAxis dataKey="sector" tick={{ fontSize: 10, fontFamily: 'monospace', fill: '#3D5A7A' }} />
              <YAxis tick={{ fontSize: 10, fontFamily: 'monospace', fill: '#3D5A7A' }} unit=" Mt" />
              <Tooltip content={<CT />} />
              <Legend wrapperStyle={{ fontFamily: 'monospace', fontSize: 10, color: '#7A9BBE' }} />
              <Bar dataKey="baseline" name="2024 Baseline" fill="#EF4444" opacity={0.8} radius={[3, 3, 0, 0]} />
              <Bar dataKey="y2030"    name="2030 Target"   fill="#F59E0B" opacity={0.8} radius={[3, 3, 0, 0]} />
              <Bar dataKey="y2050"    name="2050 Target"   fill="#10B981" opacity={0.9} radius={[3, 3, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-[#0B1420] border border-[#1A2A3A] rounded-xl p-5">
          <div className="font-['Syne'] font-semibold text-sm text-[#E2EAF4] mb-4">Net Zero 2070 — Key Milestones</div>
          <ResponsiveContainer width="100%" height={180}>
            <LineChart data={NET_ZERO_PATH}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1A2A3A" />
              <XAxis dataKey="year" tick={{ fontSize: 10, fontFamily: 'monospace', fill: '#3D5A7A' }} />
              <YAxis tick={{ fontSize: 10, fontFamily: 'monospace', fill: '#3D5A7A' }} />
              <Tooltip content={<CT />} />
              <Legend wrapperStyle={{ fontFamily: 'monospace', fontSize: 10, color: '#7A9BBE' }} />
              <Line type="monotone" dataKey="renewGW"      name="Renew. GW"    stroke="#10B981" strokeWidth={2} dot={{ r: 3 }} />
              <Line type="monotone" dataKey="emissionsRed" name="Emissions ↓%" stroke="#EF4444" strokeWidth={2} dot={{ r: 3 }} />
              <Line type="monotone" dataKey="evShare"      name="EV Share %"   stroke="#0EA5E9" strokeWidth={2} dot={{ r: 3 }} />
            </LineChart>
          </ResponsiveContainer>

          <div className="mt-4 space-y-2">
            {[{ p: '2025–30', need: 180 }, { p: '2030–40', need: 260 }, { p: '2040–50', need: 300 }].map(d => (
              <div key={d.p} className="flex justify-between items-center bg-[#080F18] rounded-lg px-3 py-2">
                <span className="font-mono text-[10px] text-[#3D5A7A]">{d.p}</span>
                <div className="flex items-center gap-3">
                  <div className="h-1 rounded-full bg-[#1A2A3A] w-20 overflow-hidden">
                    <div className="h-full rounded-full bg-[#10B981]" style={{ width: `${(d.need / 300) * 100}%` }} />
                  </div>
                  <span className="font-mono text-xs text-[#10B981] font-semibold">${d.need}B/yr</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
        {EMISSIONS.map(d => {
          const pct = Math.round(((d.baseline - d.y2050) / d.baseline) * 100);
          return (
            <div key={d.sector} className="bg-[#0B1420] border border-[#1A2A3A] rounded-xl p-4">
              <div className="flex justify-between items-center mb-2">
                <span className="font-['Syne'] text-xs font-semibold text-[#E2EAF4]">{d.sector}</span>
                <span className="font-mono text-xs text-[#10B981]">−{pct}%</span>
              </div>
              <div className="h-1 bg-[#1A2A3A] rounded-full mb-2 overflow-hidden">
                <div className="h-full bg-[#10B981] rounded-full" style={{ width: `${pct}%` }} />
              </div>
              <div className="font-mono text-[10px] text-[#3D5A7A]">
                {d.baseline} → {d.y2050} Mt · <span className="text-[#06B6D4]">{d.lever}</span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

function ESGSection() {
  const [filter, setFilter] = useState('All');
  const sectors = ['All', ...Array.from(new Set(ESG_SCORES.map(d => d.sector)))];
  const filtered = filter === 'All' ? ESG_SCORES : ESG_SCORES.filter(d => d.sector === filter);
  const sorted = [...filtered].sort((a, b) => b.composite - a.composite);

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="lg:col-span-2 bg-[#0B1420] border border-[#1A2A3A] rounded-xl p-5">
          <div className="flex flex-wrap justify-between items-center gap-3 mb-4">
            <div className="font-['Syne'] font-semibold text-sm text-[#E2EAF4]">Composite ESG Score — Nifty 50 Sample</div>
            <div className="flex gap-2 flex-wrap">
              {sectors.map(s => (
                <button key={s} onClick={() => setFilter(s)}
                  className="font-mono text-[10px] px-2.5 py-1 rounded transition-all"
                  style={{
                    background: filter === s ? '#10B981' : '#1A2A3A',
                    color: filter === s ? '#050A0F' : '#7A9BBE',
                    border: 'none', cursor: 'pointer'
                  }}>
                  {s}
                </button>
              ))}
            </div>
          </div>
          <ResponsiveContainer width="100%" height={320}>
            <BarChart data={sorted} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="#1A2A3A" />
              <XAxis type="number" domain={[0, 100]} tick={{ fontSize: 10, fontFamily: 'monospace', fill: '#3D5A7A' }} />
              <YAxis type="category" dataKey="ticker" width={76} tick={{ fontSize: 11, fontFamily: 'monospace', fill: '#7A9BBE' }} />
              <Tooltip content={<CT />} />
              <ReferenceLine x={60} stroke="rgba(16,185,129,0.3)" strokeDasharray="4 4" />
              <Bar dataKey="composite" name="ESG Score" radius={[0, 4, 4, 0]}>
                {sorted.map((d, i) => (
                  <Cell key={i} fill={d.composite >= 70 ? '#10B981' : d.composite >= 55 ? '#F59E0B' : '#EF4444'} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="space-y-4">
          <div className="bg-[#0B1420] border border-[#1A2A3A] rounded-xl p-5">
            <div className="font-['Syne'] font-semibold text-sm text-[#E2EAF4] mb-3">E / S / G by Sector</div>
            <ResponsiveContainer width="100%" height={200}>
              <RadarChart data={RADAR_DATA}>
                <PolarGrid stroke="#1A2A3A" />
                <PolarAngleAxis dataKey="sector" tick={{ fontFamily: 'monospace', fontSize: 9, fill: '#7A9BBE' }} />
                <Radar name="E" dataKey="E" stroke="#10B981" fill="#10B981" fillOpacity={0.15} />
                <Radar name="S" dataKey="S" stroke="#0EA5E9" fill="#0EA5E9" fillOpacity={0.1} />
                <Radar name="G" dataKey="G" stroke="#F59E0B" fill="#F59E0B" fillOpacity={0.1} />
                <Legend wrapperStyle={{ fontFamily: 'monospace', fontSize: 10, color: '#7A9BBE' }} />
              </RadarChart>
            </ResponsiveContainer>
          </div>

          <div className="bg-[#0B1420] border border-[#1A2A3A] rounded-xl p-5">
            <div className="font-['Syne'] font-semibold text-sm text-[#E2EAF4] mb-3">Coal Exposure Flags</div>
            {ESG_SCORES.filter(d => d.coal > 0).map(d => (
              <div key={d.ticker} className="flex justify-between items-center py-2 border-b border-[#1A2A3A]">
                <div>
                  <span className="font-mono text-xs text-[#E2EAF4]">{d.ticker}</span>
                  <span className="font-mono text-[10px] text-[#3D5A7A] ml-2">{d.name}</span>
                </div>
                <span className="font-mono text-xs" style={{ color: d.coal > 90 ? '#EF4444' : '#F59E0B' }}>
                  {d.coal}% coal
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

function ProductsSection() {
  return (
    <div className="space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
        {PRODUCTS.map(p => (
          <div key={p.name} className="bg-[#0B1420] border border-[#1A2A3A] rounded-xl p-4 hover:border-[#1E3A5F] transition-colors"
            style={{ borderLeft: `3px solid ${p.color}` }}>
            <div className="flex justify-between items-start mb-2">
              <span className="font-['Syne'] text-sm font-semibold text-[#E2EAF4] leading-tight">{p.name}</span>
            </div>
            <span className="font-mono text-[10px] px-2 py-0.5 rounded" style={{ background: p.color + '20', color: p.color }}>
              {p.family}
            </span>
            <div className="flex gap-3 mt-3">
              <span className="font-mono text-[10px] text-[#3D5A7A]">Tenor: <span className="text-[#7A9BBE]">{p.tenor}</span></span>
              <span className="font-mono text-[10px] text-[#3D5A7A]">H2A: <span style={{ color: p.h2a === 'High' ? '#F59E0B' : '#3D5A7A' }}>{p.h2a}</span></span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function PolicySection() {
  const statusColor: Record<string, string> = { Active: '#10B981', Consultation: '#F59E0B', Developing: '#0EA5E9', Published: '#06B6D4' };
  const impactColor: Record<string, string> = { High: '#10B981', Medium: '#F59E0B', Low: '#3D5A7A' };
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {POLICIES.map(p => (
        <div key={p.instrument} className="bg-[#0B1420] border border-[#1A2A3A] rounded-xl p-4 hover:border-[#1E3A5F] transition-colors">
          <div className="flex justify-between items-start mb-2">
            <div>
              <span className="font-mono text-[10px] text-[#3D5A7A] mr-2">{p.body} ·</span>
              <span className="font-['Syne'] text-sm font-semibold text-[#E2EAF4]">{p.instrument}</span>
            </div>
            <span className="font-mono text-[10px] px-2 py-0.5 rounded shrink-0"
              style={{ background: statusColor[p.status] + '20', color: statusColor[p.status] }}>
              {p.status}
            </span>
          </div>
          <p className="font-mono text-[10px] text-[#3D5A7A] leading-relaxed mb-3">{p.desc}</p>
          <div className="flex items-center gap-3">
            <span className="font-mono text-[10px] text-[#3D5A7A]">Since {p.year}</span>
            <span className="font-mono text-[10px]" style={{ color: impactColor[p.impact] }}>● {p.impact} Impact</span>
          </div>
        </div>
      ))}
    </div>
  );
}

function RepoSection() {
  const labelColor: Record<string, string> = {
    documentation: '#0EA5E9', notebook: '#8B5CF6', 'good first issue': '#10B981',
    'model-needed': '#F59E0B', 'data-gap': '#F97316', policy: '#06B6D4',
    'research-gap': '#EF4444', 'sector-expansion': '#10B981',
  };
  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
      <div className="bg-[#0B1420] border border-[#1A2A3A] rounded-xl p-5">
        <div className="flex justify-between items-center mb-4">
          <span className="font-['Syne'] font-semibold text-sm text-[#E2EAF4]">Open Issues</span>
          <a href="https://github.com/DogInfantry/sustainable-finance-india-transition/issues"
            target="_blank" rel="noreferrer"
            className="flex items-center gap-1 font-mono text-[10px] text-[#10B981] hover:text-[#06B6D4] transition-colors no-underline">
            GitHub <ExternalLink size={10} />
          </a>
        </div>
        <div className="space-y-2">
          {ISSUES.map(issue => (
            <div key={issue.id} className="bg-[#080F18] rounded-lg p-3 border-l-2 border-[#10B981]/30">
              <div className="flex gap-2 mb-1.5">
                <span className="font-mono text-[10px] text-[#3D5A7A]">#{issue.id}</span>
                <span className="font-mono text-xs text-[#E2EAF4]">{issue.title}</span>
              </div>
              <div className="flex gap-1.5 flex-wrap">
                {issue.labels.map(l => (
                  <span key={l} className="font-mono text-[10px] px-1.5 py-0.5 rounded"
                    style={{ color: labelColor[l] || '#7A9BBE', background: (labelColor[l] || '#7A9BBE') + '18' }}>
                    {l}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="space-y-4">
        <div className="bg-[#0B1420] border border-[#1A2A3A] rounded-xl p-5">
          <div className="font-['Syne'] font-semibold text-sm text-[#E2EAF4] mb-4">Recent Commits</div>
          <div className="space-y-2">
            {COMMITS.map(c => (
              <div key={c.sha} className="flex gap-3 py-2 border-b border-[#1A2A3A]">
                <span className="font-mono text-xs text-[#10B981] shrink-0">{c.sha}</span>
                <div>
                  <div className="font-mono text-xs text-[#E2EAF4]">{c.msg}</div>
                  <div className="font-mono text-[10px] text-[#3D5A7A] mt-0.5">{c.date}</div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-[#0B1420] border border-[#1A2A3A] rounded-xl p-5">
          <div className="font-['Syne'] font-semibold text-sm text-[#E2EAF4] mb-3">Repository Topics</div>
          <div className="flex gap-2 flex-wrap">
            {['carbon-markets', 'climate-finance', 'climate-policy', 'esg', 'green-bonds-analysis',
              'india-energy-transition', 'sustainable-finance', 'taxonomy'].map(t => (
              <span key={t} className="font-mono text-[10px] px-2.5 py-1 rounded-full border border-[#1E3A5F] text-[#10B981]">
                {t}
              </span>
            ))}
          </div>
        </div>

        <div className="bg-[#0B1420] border border-[#1A2A3A] rounded-xl p-5">
          <div className="font-['Syne'] font-semibold text-sm text-[#E2EAF4] mb-3">Repository Structure</div>
          {[
            { path: 'src/', desc: 'ESG spread, VaR, DCF, taxonomy models', icon: '⚙️', color: '#06B6D4' },
            { path: 'data/', desc: 'Synthetic: green bonds, ESG scores, climate scenarios', icon: '📊', color: '#10B981' },
            { path: 'reports/', desc: 'Roadmap, product mapping, bank views', icon: '📄', color: '#0EA5E9' },
            { path: 'notebooks/', desc: 'Jupyter notebooks (v1.1+ planned)', icon: '📓', color: '#8B5CF6' },
            { path: 'tests/', desc: 'pytest coverage for core models', icon: '🧪', color: '#F59E0B' },
          ].map(item => (
            <div key={item.path} className="flex gap-3 py-2 border-b border-[#1A2A3A] last:border-0 items-start">
              <span>{item.icon}</span>
              <div>
                <span className="font-mono text-xs" style={{ color: item.color }}>{item.path}</span>
                <div className="font-mono text-[10px] text-[#3D5A7A] mt-0.5">{item.desc}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

// ─── MAIN PAGE ────────────────────────────────────────────────────────────────

export default function SfinPage() {
  const [tab, setTab] = useState('overview');
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const h = () => setScrolled(window.scrollY > 20);
    window.addEventListener('scroll', h);
    return () => window.removeEventListener('scroll', h);
  }, []);

  return (
    <div className="min-h-screen" style={{ background: '#050A0F', color: '#E2EAF4' }}>
      {/* NAV */}
      <header className={`sticky top-0 z-50 px-6 transition-all duration-300 ${scrolled ? 'bg-[#050A0F]/95 backdrop-blur-md border-b border-[#1A2A3A]' : 'bg-transparent border-b border-transparent'}`}>
        <div className="max-w-[1400px] mx-auto flex items-center gap-6 h-14">
          <div className="flex items-center gap-2.5">
            <div className="w-7 h-7 rounded-md flex items-center justify-center" style={{ background: 'linear-gradient(135deg, #10B981, #06B6D4)' }}>
              <Leaf size={13} color="#050A0F" />
            </div>
            <div>
              <div className="font-['Syne'] text-sm font-bold text-[#E2EAF4] leading-none">India Transition Finance</div>
              <div className="font-mono text-[9px] text-[#3D5A7A] leading-none mt-0.5">DogInfantry / sustainable-finance-india-transition</div>
            </div>
          </div>

          <nav className="flex gap-1 ml-4 flex-1 overflow-x-auto">
            {TABS.map(({ id, label, Icon }) => {
              const active = tab === id;
              return (
                <button key={id} onClick={() => setTab(id)}
                  className="flex items-center gap-1.5 px-3 py-1.5 rounded-md transition-all whitespace-nowrap font-mono text-[10px]"
                  style={{
                    background: active ? '#1A2A3A' : 'transparent',
                    color: active ? '#10B981' : '#3D5A7A',
                    border: 'none', cursor: 'pointer'
                  }}>
                  <Icon size={11} /> {label}
                </button>
              );
            })}
          </nav>

          <a href="https://github.com/DogInfantry/sustainable-finance-india-transition"
            target="_blank" rel="noreferrer"
            className="flex items-center gap-1 font-mono text-[10px] text-[#3D5A7A] hover:text-[#10B981] transition-colors no-underline shrink-0">
            <ExternalLink size={11} /> GitHub
          </a>
        </div>
      </header>

      {/* HERO */}
      <div className="border-b border-[#1A2A3A] px-6 pt-8 pb-6" style={{ background: 'linear-gradient(180deg, rgba(16,185,129,0.04) 0%, transparent 100%)' }}>
        <div className="max-w-[1400px] mx-auto">
          <div className="font-mono text-[10px] text-[#10B981] tracking-[0.15em] uppercase mb-2">
            Research Dashboard · v1.0 · Synthetic Data · India Climate Finance
          </div>
          <h1 className="font-['Syne'] font-extrabold text-3xl md:text-4xl text-[#E2EAF4] leading-tight tracking-tight mb-3 max-w-2xl">
            India&apos;s Sustainable Finance<br />
            <span style={{ color: '#10B981' }}>Transition</span> — Data &amp; Frameworks
          </h1>
          <p className="font-mono text-xs text-[#7A9BBE] max-w-xl leading-relaxed">
            Green bonds · ESG integration · SEBI/RBI policy frameworks ·
            Climate risk in Indian capital markets · Transition finance for hard-to-abate sectors
          </p>
        </div>
      </div>

      {/* CONTENT */}
      <main className="max-w-[1400px] mx-auto px-6 py-8">
        {tab === 'overview'  && <OverviewSection />}
        {tab === 'capital'   && <CapitalSection />}
        {tab === 'emissions' && <EmissionsSection />}
        {tab === 'esg'       && <ESGSection />}
        {tab === 'products'  && <ProductsSection />}
        {tab === 'policy'    && <PolicySection />}
        {tab === 'repo'      && <RepoSection />}
      </main>

      {/* FOOTER */}
      <footer className="border-t border-[#1A2A3A] px-6 py-5">
        <div className="max-w-[1400px] mx-auto flex justify-between items-center flex-wrap gap-3">
          <span className="font-mono text-[10px] text-[#3D5A7A]">
            © 2026 · Anklesh Rawat · IIM Bodh Gaya MBA · MIT License · All data is synthetic / illustrative
          </span>
          <span className="font-mono text-[10px] text-[#3D5A7A]">
            Next.js + Recharts + Tailwind · Deployed on Vercel
          </span>
        </div>
      </footer>
    </div>
  );
}
