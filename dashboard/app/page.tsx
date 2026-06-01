'use client';
import { useState, useEffect, useCallback } from 'react';
import {
  LineChart, Line, AreaChart, Area, BarChart, Bar, ScatterChart, Scatter,
  XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine,
  RadarChart, Radar, PolarGrid, PolarAngleAxis, Cell, ComposedChart
} from 'recharts';

// ─────────────────────────────────────────────
// TYPES
// ─────────────────────────────────────────────
type Row = Record<string, string | number | null>;

interface AllData {
  yieldCurve: Row[];
  regime: Row[];
  marketRates: Row[];
  ipoRaw: Row[];
  ipoEvents: Row[];
  mnaRaw: Row[];
  dealScreening: Row[];
  dealFeatures: Row[];
  caseStudies: Row[];
  sovereignRisk: Row[];
  stressTest: Row[];
  sovereignIssuance: Row[];
  fxRates: Row[];
  worldbank: Row[];
}

// ─────────────────────────────────────────────
// HELPERS
// ─────────────────────────────────────────────
async function fetchCSV(file: string): Promise<Row[]> {
  try {
    const res = await fetch(`/api/data?file=${file}`);
    if (!res.ok) return [];
    return await res.json();
  } catch { return []; }
}

const fmt = (v: number | null | undefined, decimals = 2, suffix = '') => {
  if (v == null || isNaN(Number(v))) return '—';
  return `${Number(v).toFixed(decimals)}${suffix}`;
};
const fmtBn = (v: number | null | undefined) => {
  if (v == null) return '—';
  const n = Number(v);
  if (n >= 1000) return `$${(n / 1000).toFixed(1)}T`;
  if (n >= 1) return `$${n.toFixed(1)}B`;
  return `$${(n * 1000).toFixed(0)}M`;
};
const fmtPct = (v: number | null | undefined) => fmt(v, 2, '%');

const REGIME_COLORS: Record<string, string> = {
  'Risk-On': '#10B981',
  'Neutral': '#F59E0B',
  'Risk-Off': '#EF4444',
};
const RISK_COLORS: Record<string, string> = {
  'Low Risk': '#10B981',
  'Moderate Risk': '#F59E0B',
  'Elevated Risk': '#F97316',
  'High Risk': '#EF4444',
  'Critical': '#F87171',
};
const CURVE_COLORS: Record<string, string> = {
  'Inverted': '#EF4444',
  'Flat': '#F59E0B',
  'Normal': '#10B981',
  'Steep': '#0EA5E9',
};

interface TooltipPayloadItem { color?: string; name?: string; value?: number | string; }
const CustomTooltip = ({ active, payload, label }: { active?: boolean; payload?: TooltipPayloadItem[]; label?: string }) => {
  if (!active || !payload || !payload.length) return null;
  return (
    <div style={{ background: '#0B1420', border: '1px solid #1A2A3A', borderRadius: 6, padding: '8px 12px', fontFamily: 'DM Mono, monospace', fontSize: 12 }}>
      {label && <div style={{ color: '#7A9BBE', marginBottom: 4 }}>{String(label)}</div>}
      {payload.map((p, i) => (
        <div key={i} style={{ color: p.color || '#E2EAF4' }}>
          {p.name}: <span style={{ color: '#E2EAF4' }}>{typeof p.value === 'number' ? p.value.toFixed(3) : String(p.value)}</span>
        </div>
      ))}
    </div>
  );
};

// ─────────────────────────────────────────────
// STAT CARD
// ─────────────────────────────────────────────
function StatCard({ label, value, sub, color = '#0EA5E9', trend }: {
  label: string; value: string; sub?: string; color?: string; trend?: 'up' | 'down' | 'neutral';
}) {
  return (
    <div className="card" style={{ padding: '16px 20px' }}>
      <div style={{ color: 'var(--text-muted)', fontSize: 11, fontFamily: 'DM Mono, monospace', letterSpacing: '0.08em', textTransform: 'uppercase', marginBottom: 8 }}>{label}</div>
      <div className="stat-value" style={{ color }}>{value}</div>
      {sub && (
        <div style={{ color: trend === 'up' ? '#10B981' : trend === 'down' ? '#EF4444' : 'var(--text-secondary)', fontSize: 12, marginTop: 4 }}>
          {trend === 'up' ? '↑ ' : trend === 'down' ? '↓ ' : ''}{sub}
        </div>
      )}
    </div>
  );
}

// ─────────────────────────────────────────────
// NAV
// ─────────────────────────────────────────────
const TABS = [
  { id: 'overview', label: 'Overview' },
  { id: 'yield', label: 'Yield Curve' },
  { id: 'regime', label: 'Market Regime' },
  { id: 'ipo', label: 'IPO Markets' },
  { id: 'mna', label: 'M&A Screening' },
  { id: 'sovereign', label: 'Sovereign Risk' },
];

// ─────────────────────────────────────────────
// SECTION: OVERVIEW
// ─────────────────────────────────────────────
function OverviewSection({ data }: { data: AllData }) {
  const latestYield = data.yieldCurve[data.yieldCurve.length - 1];
  const latestRegime = data.regime[data.regime.length - 1];
  const latestMarket = data.marketRates[data.marketRates.length - 1];
  const totalMnAValue = data.mnaRaw.reduce((s, r) => s + Number(r.deal_value_usd_bn || 0), 0);
  const completedDeals = data.mnaRaw.filter(r => r.status === 'Completed').length;
  const avgIPOReturn = data.ipoRaw.reduce((s, r) => s + Number(r.first_day_return_pct || 0), 0) / (data.ipoRaw.length || 1);
  const highRiskCountries = data.sovereignRisk.filter(r => String(r.risk_tier).includes('High') || String(r.risk_tier).includes('Critical')).length;

  const recentRegime = data.regime.slice(-60).map((r, i) => ({
    i,
    score: Number(r.regime_score),
    regime: r.regime,
    date: String(r.date).slice(5),
  }));

  const yieldTrend = data.yieldCurve.slice(-90).map(r => ({
    date: String(r.date).slice(5),
    '3M': Number(r.yield_3M),
    '10Y': Number(r.yield_10Y),
    '30Y': Number(r.yield_30Y),
    slope: Number(r.slope_10y_3m),
  }));

  const regimeColor = latestRegime?.regime === 'Risk-On' ? '#10B981' : latestRegime?.regime === 'Risk-Off' ? '#EF4444' : '#F59E0B';
  const curveColor = CURVE_COLORS[String(latestYield?.curve_regime)] || '#0EA5E9';

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
      {/* Hero strip */}
      <div style={{ background: 'linear-gradient(135deg, #0B1420 0%, #060D16 100%)', border: '1px solid #1A2A3A', borderRadius: 10, padding: '20px 28px', position: 'relative', overflow: 'hidden' }}>
        <div style={{ position: 'absolute', top: 0, right: 0, width: 300, height: '100%', background: 'radial-gradient(ellipse at right, rgba(14,165,233,0.08) 0%, transparent 70%)', pointerEvents: 'none' }} />
        <div style={{ fontSize: 11, fontFamily: 'DM Mono', letterSpacing: '0.1em', color: '#3D5A7A', textTransform: 'uppercase', marginBottom: 8 }}>Capital Markets Intelligence Platform</div>
        <h1 style={{ fontSize: 'clamp(1.4rem, 3vw, 2rem)', fontWeight: 800, color: '#E2EAF4', margin: 0, marginBottom: 8, fontFamily: 'Syne' }}>
          Real-Time Market Intelligence
        </h1>
        <p style={{ color: '#7A9BBE', fontSize: 13, maxWidth: 600, margin: 0 }}>
          Institutional-grade analytics across IPO markets, sovereign risk, M&A deal screening, and cross-asset regime detection. Modeled on Goldman Sachs GIR · J.P. Morgan · D.E. Shaw · PwC Deals.
        </p>
        <div style={{ display: 'flex', gap: 12, marginTop: 16, flexWrap: 'wrap' }}>
          {[
            { label: 'Data Vintage', val: '2024–2026' },
            { label: 'Trading Days', val: '501' },
            { label: 'Models', val: '6 Proprietary' },
            { label: 'Zero API Keys', val: 'Open Data' },
          ].map(({ label, val }) => (
            <div key={label} style={{ background: 'rgba(14,165,233,0.06)', border: '1px solid rgba(14,165,233,0.15)', borderRadius: 4, padding: '4px 12px' }}>
              <span style={{ color: '#3D5A7A', fontFamily: 'DM Mono', fontSize: 10, letterSpacing: '0.06em' }}>{label}: </span>
              <span style={{ color: '#0EA5E9', fontFamily: 'DM Mono', fontSize: 11, fontWeight: 500 }}>{val}</span>
            </div>
          ))}
        </div>
      </div>

      {/* KPI Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: 12 }}>
        <StatCard label="Market Regime" value={String(latestRegime?.regime || '—')} sub={`Score: ${fmt(latestRegime?.regime_score as number, 1)}`} color={regimeColor} />
        <StatCard label="Curve Regime" value={String(latestYield?.curve_regime || '—')} sub={`Slope 10Y-3M: ${fmt(latestYield?.slope_10y_3m as number, 2)}%`} color={curveColor} />
        <StatCard label="10Y Treasury" value={`${fmt(latestYield?.yield_10Y as number, 2)}%`} sub={`30Y: ${fmt(latestYield?.yield_30Y as number, 2)}%`} color="#0EA5E9" />
        <StatCard label="S&P 500" value={latestMarket ? Number(latestMarket['^GSPC']).toFixed(0) : '—'} sub={`VIX: ${fmt(latestMarket?.['^VIX'] as number, 1)}`} color="#8B5CF6" />
        <StatCard label="M&A Pipeline" value={fmtBn(totalMnAValue)} sub={`${completedDeals}/${data.mnaRaw.length} completed`} color="#F59E0B" />
        <StatCard label="IPO Avg Day-1" value={fmtPct(avgIPOReturn)} sub={`${data.ipoRaw.length} IPOs tracked`} trend={avgIPOReturn > 0 ? 'up' : 'down'} color={avgIPOReturn > 0 ? '#10B981' : '#EF4444'} />
        <StatCard label="High-Risk Countries" value={String(highRiskCountries)} sub={`of ${data.sovereignRisk.length} sovereigns`} color="#EF4444" />
        <StatCard label="Sovereign Issuances" value={`$${data.sovereignIssuance.reduce((s, r) => s + Number(r.issue_size_usd_bn || 0), 0).toFixed(0)}B`} sub={`${data.sovereignIssuance.length} bond issuances`} color="#06B6D4" />
      </div>

      {/* Two charts side by side */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
        <div className="card" style={{ padding: 20 }}>
          <div style={{ marginBottom: 12 }}>
            <div style={{ fontFamily: 'Syne', fontWeight: 700, fontSize: 14, color: '#E2EAF4' }}>Yield Curve — 90 Day Trend</div>
            <div style={{ color: '#3D5A7A', fontSize: 11, fontFamily: 'DM Mono' }}>3M / 10Y / 30Y Yields</div>
          </div>
          <ResponsiveContainer width="100%" height={200}>
            <LineChart data={yieldTrend}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1A2A3A" />
              <XAxis dataKey="date" tick={{ fill: '#3D5A7A', fontSize: 10, fontFamily: 'DM Mono' }} interval={19} />
              <YAxis tick={{ fill: '#3D5A7A', fontSize: 10, fontFamily: 'DM Mono' }} domain={['auto', 'auto']} tickFormatter={v => `${v}%`} />
              <Tooltip content={<CustomTooltip />} />
              <Line dataKey="3M" stroke="#EF4444" dot={false} strokeWidth={1.5} />
              <Line dataKey="10Y" stroke="#0EA5E9" dot={false} strokeWidth={1.5} />
              <Line dataKey="30Y" stroke="#8B5CF6" dot={false} strokeWidth={1.5} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="card" style={{ padding: 20 }}>
          <div style={{ marginBottom: 12 }}>
            <div style={{ fontFamily: 'Syne', fontWeight: 700, fontSize: 14, color: '#E2EAF4' }}>Market Regime Score — 60 Days</div>
            <div style={{ color: '#3D5A7A', fontSize: 11, fontFamily: 'DM Mono' }}>–2 Risk-Off → +2 Risk-On</div>
          </div>
          <ResponsiveContainer width="100%" height={200}>
            <AreaChart data={recentRegime}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1A2A3A" />
              <XAxis dataKey="date" tick={{ fill: '#3D5A7A', fontSize: 10, fontFamily: 'DM Mono' }} interval={14} />
              <YAxis tick={{ fill: '#3D5A7A', fontSize: 10, fontFamily: 'DM Mono' }} domain={[-2.5, 2.5]} />
              <Tooltip content={<CustomTooltip />} />
              <ReferenceLine y={0} stroke="#3D5A7A" strokeDasharray="4 4" />
              <Area dataKey="score" stroke="#0EA5E9" fill="rgba(14,165,233,0.08)" strokeWidth={1.5} />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Sovereign risk mini-table */}
      <div className="card" style={{ padding: 20 }}>
        <div style={{ fontFamily: 'Syne', fontWeight: 700, fontSize: 14, color: '#E2EAF4', marginBottom: 14 }}>Sovereign Risk — Top 10 by Risk Score</div>
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontFamily: 'DM Mono', fontSize: 12 }}>
            <thead>
              <tr style={{ borderBottom: '1px solid #1A2A3A' }}>
                {['Country', 'ISO', 'Risk Score', 'Risk Tier', 'GDP Growth', 'Inflation', 'Debt/GDP'].map(h => (
                  <th key={h} style={{ padding: '6px 12px', color: '#3D5A7A', textAlign: 'left', fontSize: 10, letterSpacing: '0.06em', textTransform: 'uppercase' }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {[...data.sovereignRisk].sort((a, b) => Number(b.risk_index_0_100) - Number(a.risk_index_0_100)).slice(0, 10).map((row, i) => {
                const tier = String(row.risk_tier);
                const color = tier.includes('High') ? '#EF4444' : tier.includes('Elevated') ? '#F97316' : tier.includes('Moderate') ? '#F59E0B' : '#10B981';
                return (
                  <tr key={i} style={{ borderBottom: '1px solid rgba(26,42,58,0.5)' }}>
                    <td style={{ padding: '8px 12px', color: '#E2EAF4' }}>{String(row.country_name)}</td>
                    <td style={{ padding: '8px 12px', color: '#7A9BBE' }}>{String(row.country_code)}</td>
                    <td style={{ padding: '8px 12px', color: '#E2EAF4', fontWeight: 500 }}>{fmt(row.risk_index_0_100 as number, 1)}</td>
                    <td style={{ padding: '8px 12px' }}><span style={{ color, background: `${color}18`, border: `1px solid ${color}40`, borderRadius: 3, padding: '2px 8px', fontSize: 10 }}>{tier}</span></td>
                    <td style={{ padding: '8px 12px', color: Number(row['GDP growth (annual %)']) > 0 ? '#10B981' : '#EF4444' }}>{fmtPct(row['GDP growth (annual %)'] as number)}</td>
                    <td style={{ padding: '8px 12px', color: '#F59E0B' }}>{fmtPct(row['Inflation (CPI, annual %)'] as number)}</td>
                    <td style={{ padding: '8px 12px', color: '#7A9BBE' }}>{fmtPct(row['Central govt debt (% of GDP)'] as number)}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────
// SECTION: YIELD CURVE
// ─────────────────────────────────────────────
function YieldSection({ data }: { data: AllData }) {
  const fullHistory = data.yieldCurve.map(r => ({
    date: String(r.date).slice(0, 7),
    '3M': Number(r.yield_3M),
    '5Y': Number(r.yield_5Y),
    '10Y': Number(r.yield_10Y),
    '30Y': Number(r.yield_30Y),
    slope: Number(r.slope_10y_3m),
    level: Number(r.level),
    curvature: Number(r.curvature),
    regime: String(r.curve_regime),
    levelZ: Number(r.level_zscore),
    slopeZ: Number(r.slope_10y_3m_zscore),
  }));

  // Deduplicate to monthly for spread chart
  const monthly: typeof fullHistory = [];
  const seen = new Set<string>();
  for (const r of fullHistory) {
    if (!seen.has(r.date)) { seen.add(r.date); monthly.push(r); }
  }

  const last30 = data.yieldCurve.slice(-1)[0];
  const regimeCounts = data.yieldCurve.reduce((acc, r) => {
    const k = String(r.curve_regime);
    acc[k] = (Number(acc[k]) || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  // Latest term structure snapshot
  const termStructure = last30 ? [
    { tenor: '3M', yield: Number(last30.yield_3M) },
    { tenor: '5Y', yield: Number(last30.yield_5Y) },
    { tenor: '10Y', yield: Number(last30.yield_10Y) },
    { tenor: '30Y', yield: Number(last30.yield_30Y) },
  ] : [];

  const slopeHistory = data.yieldCurve.slice(-120).map((r, i) => ({
    i,
    date: String(r.date).slice(5),
    slope: Number(r.slope_10y_3m),
    regime: String(r.curve_regime),
  }));

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))', gap: 12 }}>
        <StatCard label="3M Yield" value={`${fmt(last30?.yield_3M as number, 2)}%`} color="#EF4444" />
        <StatCard label="5Y Yield" value={`${fmt(last30?.yield_5Y as number, 2)}%`} color="#F97316" />
        <StatCard label="10Y Yield" value={`${fmt(last30?.yield_10Y as number, 2)}%`} color="#0EA5E9" />
        <StatCard label="30Y Yield" value={`${fmt(last30?.yield_30Y as number, 2)}%`} color="#8B5CF6" />
        <StatCard label="10Y–3M Slope" value={`${fmt(last30?.slope_10y_3m as number, 2)}%`} color={Number(last30?.slope_10y_3m) < 0 ? '#EF4444' : '#10B981'} />
        <StatCard label="Curve Regime" value={String(last30?.curve_regime || '—')} color={CURVE_COLORS[String(last30?.curve_regime)] || '#0EA5E9'} />
        <StatCard label="Level Z-Score" value={fmt(last30?.level_zscore as number, 2)} color="#F59E0B" />
        <StatCard label="Slope Z-Score" value={fmt(last30?.slope_10y_3m_zscore as number, 2)} color="#06B6D4" />
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
        {/* Current term structure */}
        <div className="card" style={{ padding: 20 }}>
          <div style={{ fontFamily: 'Syne', fontWeight: 700, fontSize: 14, color: '#E2EAF4', marginBottom: 4 }}>Current Term Structure</div>
          <div style={{ color: '#3D5A7A', fontSize: 11, fontFamily: 'DM Mono', marginBottom: 14 }}>Latest snapshot — US Treasury</div>
          <ResponsiveContainer width="100%" height={220}>
            <AreaChart data={termStructure}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1A2A3A" />
              <XAxis dataKey="tenor" tick={{ fill: '#7A9BBE', fontSize: 11, fontFamily: 'DM Mono' }} />
              <YAxis tick={{ fill: '#3D5A7A', fontSize: 10, fontFamily: 'DM Mono' }} tickFormatter={v => `${v}%`} domain={['auto', 'auto']} />
              <Tooltip content={<CustomTooltip />} />
              <Area dataKey="yield" stroke="#0EA5E9" fill="rgba(14,165,233,0.1)" strokeWidth={2} dot={{ fill: '#0EA5E9', r: 4 }} />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* Slope history */}
        <div className="card" style={{ padding: 20 }}>
          <div style={{ fontFamily: 'Syne', fontWeight: 700, fontSize: 14, color: '#E2EAF4', marginBottom: 4 }}>10Y–3M Slope — 120 Days</div>
          <div style={{ color: '#3D5A7A', fontSize: 11, fontFamily: 'DM Mono', marginBottom: 14 }}>Inversion signal (negative = inverted curve)</div>
          <ResponsiveContainer width="100%" height={220}>
            <ComposedChart data={slopeHistory}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1A2A3A" />
              <XAxis dataKey="date" tick={{ fill: '#3D5A7A', fontSize: 10, fontFamily: 'DM Mono' }} interval={29} />
              <YAxis tick={{ fill: '#3D5A7A', fontSize: 10, fontFamily: 'DM Mono' }} tickFormatter={v => `${v}%`} />
              <Tooltip content={<CustomTooltip />} />
              <ReferenceLine y={0} stroke="#EF4444" strokeDasharray="4 2" strokeWidth={1} label={{ value: 'Inversion', fill: '#EF4444', fontSize: 10, fontFamily: 'DM Mono' }} />
              <Area dataKey="slope" stroke="#10B981" fill="rgba(16,185,129,0.08)" strokeWidth={1.5} />
            </ComposedChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Full history */}
      <div className="card" style={{ padding: 20 }}>
        <div style={{ fontFamily: 'Syne', fontWeight: 700, fontSize: 14, color: '#E2EAF4', marginBottom: 4 }}>Full Yield History — All Tenors</div>
        <div style={{ color: '#3D5A7A', fontSize: 11, fontFamily: 'DM Mono', marginBottom: 14 }}>Monthly aggregation · 501 trading days</div>
        <ResponsiveContainer width="100%" height={240}>
          <LineChart data={monthly}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1A2A3A" />
            <XAxis dataKey="date" tick={{ fill: '#3D5A7A', fontSize: 10, fontFamily: 'DM Mono' }} interval={3} />
            <YAxis tick={{ fill: '#3D5A7A', fontSize: 10, fontFamily: 'DM Mono' }} tickFormatter={v => `${v}%`} />
            <Tooltip content={<CustomTooltip />} />
            <Line dataKey="3M" stroke="#EF4444" dot={false} strokeWidth={1.5} />
            <Line dataKey="5Y" stroke="#F97316" dot={false} strokeWidth={1.5} />
            <Line dataKey="10Y" stroke="#0EA5E9" dot={false} strokeWidth={2} />
            <Line dataKey="30Y" stroke="#8B5CF6" dot={false} strokeWidth={1.5} />
          </LineChart>
        </ResponsiveContainer>
        <div style={{ display: 'flex', gap: 16, marginTop: 12, flexWrap: 'wrap' }}>
          {[['3M', '#EF4444'], ['5Y', '#F97316'], ['10Y', '#0EA5E9'], ['30Y', '#8B5CF6']].map(([k, c]) => (
            <div key={k} style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: 11, fontFamily: 'DM Mono', color: '#7A9BBE' }}>
              <div style={{ width: 20, height: 2, background: c }} />
              {k}
            </div>
          ))}
        </div>
      </div>

      {/* Regime distribution */}
      <div className="card" style={{ padding: 20 }}>
        <div style={{ fontFamily: 'Syne', fontWeight: 700, fontSize: 14, color: '#E2EAF4', marginBottom: 14 }}>Curve Regime Distribution — {data.yieldCurve.length} Days</div>
        <div style={{ display: 'flex', gap: 16, flexWrap: 'wrap' }}>
          {Object.entries(regimeCounts).map(([regime, count]) => (
            <div key={regime} style={{ flex: 1, minWidth: 120, background: 'rgba(14,165,233,0.04)', border: '1px solid #1A2A3A', borderRadius: 6, padding: 16, textAlign: 'center' }}>
              <div style={{ fontSize: 24, fontFamily: 'DM Mono', fontWeight: 500, color: CURVE_COLORS[regime] || '#0EA5E9' }}>{count}</div>
              <div style={{ fontSize: 11, color: '#7A9BBE', fontFamily: 'DM Mono', marginTop: 4 }}>{regime}</div>
              <div style={{ fontSize: 10, color: '#3D5A7A', fontFamily: 'DM Mono' }}>{((Number(count) / data.yieldCurve.length) * 100).toFixed(1)}%</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────
// SECTION: MARKET REGIME
// ─────────────────────────────────────────────
function RegimeSection({ data }: { data: AllData }) {
  const regimeHistory = data.regime.slice(-180).map((r, i) => ({
    i,
    date: String(r.date).slice(5),
    score: Number(r.regime_score),
    ma: Number(r.regime_score_5d_ma),
    regime: String(r.regime),
    curve: Number(r.curve_signal),
    fxVol: Number(r.fx_vol_signal),
  }));

  const sp500History = data.marketRates.slice(-180).map(r => ({
    date: String(r.date).slice(5),
    sp500: Number(r['^GSPC']),
    vix: Number(r['^VIX']),
    gold: Number(r['GC=F']),
    oil: Number(r['CL=F']),
  }));

  const regimeCounts = data.regime.reduce((acc, r) => {
    const k = String(r.regime);
    acc[k] = (Number(acc[k]) || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  const latestRegime = data.regime[data.regime.length - 1];
  const latestMarket = data.marketRates[data.marketRates.length - 1];

  // FX rates recent
  const fxRecent = data.fxRates.slice(-60).map(r => ({
    date: String(r.date).slice(5),
    INR: Number(r['USDINR=X']),
    BRL: Number(r['USDBRL=X']),
    TRY: Number(r['USDTRY=X']),
    JPY: Number(r['USDJPY=X']),
    EUR: Number(r['EURUSD=X']),
  }));

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))', gap: 12 }}>
        <StatCard label="Current Regime" value={String(latestRegime?.regime || '—')} color={REGIME_COLORS[String(latestRegime?.regime)] || '#F59E0B'} />
        <StatCard label="Regime Score" value={fmt(latestRegime?.regime_score as number, 1)} color="#0EA5E9" />
        <StatCard label="VIX Level" value={fmt(latestMarket?.['^VIX'] as number, 1)} color={Number(latestMarket?.['^VIX']) > 25 ? '#EF4444' : Number(latestMarket?.['^VIX']) > 18 ? '#F59E0B' : '#10B981'} />
        <StatCard label="S&P 500" value={Number(latestMarket?.['^GSPC']).toFixed(0)} color="#8B5CF6" />
        <StatCard label="Gold (USD/oz)" value={`$${Number(latestMarket?.['GC=F']).toFixed(0)}`} color="#F59E0B" />
        <StatCard label="WTI Oil" value={`$${Number(latestMarket?.['CL=F']).toFixed(1)}`} color="#F97316" />
        <StatCard label="Risk-On Days" value={String(regimeCounts['Risk-On'] || 0)} sub={`${(((Number(regimeCounts['Risk-On'] || 0) / data.regime.length)) * 100).toFixed(0)}% of period`} color="#10B981" />
        <StatCard label="Risk-Off Days" value={String(regimeCounts['Risk-Off'] || 0)} sub={`${(((Number(regimeCounts['Risk-Off'] || 0) / data.regime.length)) * 100).toFixed(0)}% of period`} color="#EF4444" />
      </div>

      {/* Regime score timeline */}
      <div className="card" style={{ padding: 20 }}>
        <div style={{ fontFamily: 'Syne', fontWeight: 700, fontSize: 14, color: '#E2EAF4', marginBottom: 4 }}>6-Signal Regime Score — 180 Days</div>
        <div style={{ color: '#3D5A7A', fontSize: 11, fontFamily: 'DM Mono', marginBottom: 14 }}>VIX · S&P Trend · Gold · Yield Curve · EM FX Vol · Momentum</div>
        <ResponsiveContainer width="100%" height={220}>
          <ComposedChart data={regimeHistory}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1A2A3A" />
            <XAxis dataKey="date" tick={{ fill: '#3D5A7A', fontSize: 10, fontFamily: 'DM Mono' }} interval={29} />
            <YAxis tick={{ fill: '#3D5A7A', fontSize: 10, fontFamily: 'DM Mono' }} domain={[-2.5, 2.5]} />
            <Tooltip content={<CustomTooltip />} />
            <ReferenceLine y={0.5} stroke="#10B981" strokeDasharray="4 2" />
            <ReferenceLine y={-0.5} stroke="#EF4444" strokeDasharray="4 2" />
            <ReferenceLine y={0} stroke="#3D5A7A" />
            <Area dataKey="score" stroke="#0EA5E9" fill="rgba(14,165,233,0.08)" strokeWidth={0} />
            <Line dataKey="score" stroke="#0EA5E9" dot={false} strokeWidth={1.5} />
            <Line dataKey="ma" stroke="#F59E0B" dot={false} strokeWidth={1.5} strokeDasharray="4 2" />
          </ComposedChart>
        </ResponsiveContainer>
      </div>

      {/* SP500 + VIX */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
        <div className="card" style={{ padding: 20 }}>
          <div style={{ fontFamily: 'Syne', fontWeight: 700, fontSize: 14, color: '#E2EAF4', marginBottom: 14 }}>S&P 500 — 180 Days</div>
          <ResponsiveContainer width="100%" height={200}>
            <AreaChart data={sp500History}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1A2A3A" />
              <XAxis dataKey="date" tick={{ fill: '#3D5A7A', fontSize: 10, fontFamily: 'DM Mono' }} interval={29} />
              <YAxis tick={{ fill: '#3D5A7A', fontSize: 10, fontFamily: 'DM Mono' }} domain={['auto', 'auto']} />
              <Tooltip content={<CustomTooltip />} />
              <Area dataKey="sp500" stroke="#8B5CF6" fill="rgba(139,92,246,0.08)" strokeWidth={1.5} />
            </AreaChart>
          </ResponsiveContainer>
        </div>
        <div className="card" style={{ padding: 20 }}>
          <div style={{ fontFamily: 'Syne', fontWeight: 700, fontSize: 14, color: '#E2EAF4', marginBottom: 14 }}>VIX Fear Index — 180 Days</div>
          <ResponsiveContainer width="100%" height={200}>
            <AreaChart data={sp500History}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1A2A3A" />
              <XAxis dataKey="date" tick={{ fill: '#3D5A7A', fontSize: 10, fontFamily: 'DM Mono' }} interval={29} />
              <YAxis tick={{ fill: '#3D5A7A', fontSize: 10, fontFamily: 'DM Mono' }} />
              <Tooltip content={<CustomTooltip />} />
              <ReferenceLine y={20} stroke="#F59E0B" strokeDasharray="4 2" />
              <ReferenceLine y={30} stroke="#EF4444" strokeDasharray="4 2" />
              <Area dataKey="vix" stroke="#EF4444" fill="rgba(239,68,68,0.08)" strokeWidth={1.5} />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* FX rates */}
      <div className="card" style={{ padding: 20 }}>
        <div style={{ fontFamily: 'Syne', fontWeight: 700, fontSize: 14, color: '#E2EAF4', marginBottom: 4 }}>EM FX Rates vs USD — 60 Days</div>
        <div style={{ color: '#3D5A7A', fontSize: 11, fontFamily: 'DM Mono', marginBottom: 14 }}>INR · BRL · TRY · JPY | EUR (inverted)</div>
        <ResponsiveContainer width="100%" height={200}>
          <LineChart data={fxRecent}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1A2A3A" />
            <XAxis dataKey="date" tick={{ fill: '#3D5A7A', fontSize: 10, fontFamily: 'DM Mono' }} interval={14} />
            <YAxis yAxisId="em" tick={{ fill: '#3D5A7A', fontSize: 9, fontFamily: 'DM Mono' }} domain={['auto', 'auto']} />
            <YAxis yAxisId="jpy" orientation="right" tick={{ fill: '#3D5A7A', fontSize: 9, fontFamily: 'DM Mono' }} domain={['auto', 'auto']} />
            <Tooltip content={<CustomTooltip />} />
            <Line yAxisId="em" dataKey="INR" stroke="#10B981" dot={false} strokeWidth={1.5} />
            <Line yAxisId="em" dataKey="BRL" stroke="#F59E0B" dot={false} strokeWidth={1.5} />
            <Line yAxisId="em" dataKey="TRY" stroke="#EF4444" dot={false} strokeWidth={1.5} />
            <Line yAxisId="jpy" dataKey="JPY" stroke="#0EA5E9" dot={false} strokeWidth={1.5} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────
// SECTION: IPO
// ─────────────────────────────────────────────
function IpoSection({ data }: { data: AllData }) {
  const ipos = data.ipoEvents.length > 0 ? data.ipoEvents : data.ipoRaw;

  const avgDay1 = ipos.reduce((s, r) => s + Number(r.first_day_return_pct || 0), 0) / (ipos.length || 1);
  const totalMLOT = ipos.reduce((s, r) => s + Number(r.money_left_on_table_usd || 0), 0);
  const underpriced = ipos.filter(r => String(r.pricing_assessment || '').includes('Underpriced')).length;
  const totalDealSize = ipos.reduce((s, r) => s + Number(r.deal_size_usd || 0), 0);

  // Scatter: offer price vs first day return
  const scatterData = ipos.map(r => ({
    company: String(r.company || r.ticker),
    offer: Number(r.offer_price),
    return: Number(r.first_day_return_pct),
    size: Math.sqrt(Number(r.deal_size_usd || 1e8) / 1e8) * 4,
    sector: String(r.sector || '').split(' ')[0],
  })).filter(r => !isNaN(r.offer) && !isNaN(r.return));

  // Bar: first day returns
  const returnsBar = [...ipos].sort((a, b) => Number(b.first_day_return_pct) - Number(a.first_day_return_pct)).map(r => ({
    company: String(r.ticker || r.company).slice(0, 6),
    return: Number(r.first_day_return_pct),
    color: Number(r.first_day_return_pct) > 0 ? '#10B981' : '#EF4444',
  }));

  // Sector breakdown
  const bySector = ipos.reduce((acc, r) => {
    const s = String(r.sector || 'Other').split(' ')[0];
    if (!acc[s]) acc[s] = { count: 0, totalReturn: 0 };
    acc[s].count++;
    acc[s].totalReturn += Number(r.first_day_return_pct || 0);
    return acc;
  }, {} as Record<string, { count: number; totalReturn: number }>);

  const sectorData = Object.entries(bySector).map(([sector, d]) => ({
    sector,
    count: d.count,
    avgReturn: d.totalReturn / d.count,
  }));

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))', gap: 12 }}>
        <StatCard label="IPOs Tracked" value={String(ipos.length)} sub="7 countries" color="#0EA5E9" />
        <StatCard label="Avg Day-1 Return" value={fmtPct(avgDay1)} trend={avgDay1 > 0 ? 'up' : 'down'} color={avgDay1 > 0 ? '#10B981' : '#EF4444'} />
        <StatCard label="Total Deal Size" value={fmtBn(totalDealSize / 1e9)} color="#8B5CF6" />
        <StatCard label="Money Left on Table" value={fmtBn(totalMLOT / 1e9)} color="#F97316" />
        <StatCard label="Underpriced IPOs" value={`${underpriced}/${ipos.length}`} sub={`${((underpriced / ipos.length) * 100).toFixed(0)}% of cohort`} color="#F59E0B" />
        <StatCard label="Largest IPO" value={fmtBn(Math.max(...ipos.map(r => Number(r.deal_size_usd || 0))) / 1e9)} color="#06B6D4" />
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
        {/* Day-1 returns bar */}
        <div className="card" style={{ padding: 20 }}>
          <div style={{ fontFamily: 'Syne', fontWeight: 700, fontSize: 14, color: '#E2EAF4', marginBottom: 4 }}>Day-1 Returns by IPO</div>
          <div style={{ color: '#3D5A7A', fontSize: 11, fontFamily: 'DM Mono', marginBottom: 14 }}>Sorted high → low, % vs offer price</div>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={returnsBar} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="#1A2A3A" horizontal={false} />
              <XAxis type="number" tick={{ fill: '#3D5A7A', fontSize: 10, fontFamily: 'DM Mono' }} tickFormatter={v => `${v}%`} />
              <YAxis type="category" dataKey="company" tick={{ fill: '#7A9BBE', fontSize: 9, fontFamily: 'DM Mono' }} width={40} />
              <Tooltip content={<CustomTooltip />} />
              <ReferenceLine x={0} stroke="#3D5A7A" />
              <Bar dataKey="return" radius={[0, 2, 2, 0]}>
                {returnsBar.map((entry, i) => <Cell key={i} fill={entry.color} />)}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Scatter */}
        <div className="card" style={{ padding: 20 }}>
          <div style={{ fontFamily: 'Syne', fontWeight: 700, fontSize: 14, color: '#E2EAF4', marginBottom: 4 }}>Offer Price vs Day-1 Return</div>
          <div style={{ color: '#3D5A7A', fontSize: 11, fontFamily: 'DM Mono', marginBottom: 14 }}>Bubble size = deal size</div>
          <ResponsiveContainer width="100%" height={220}>
            <ScatterChart>
              <CartesianGrid strokeDasharray="3 3" stroke="#1A2A3A" />
              <XAxis dataKey="offer" name="Offer Price" tick={{ fill: '#3D5A7A', fontSize: 10, fontFamily: 'DM Mono' }} tickFormatter={v => `$${v}`} label={{ value: 'Offer $', fill: '#3D5A7A', fontSize: 10, position: 'insideBottom', offset: -5 }} />
              <YAxis dataKey="return" name="Day-1 Return" tick={{ fill: '#3D5A7A', fontSize: 10, fontFamily: 'DM Mono' }} tickFormatter={v => `${v}%`} />
              <Tooltip cursor={{ stroke: '#1A2A3A' }} content={({ payload }) => {
                if (!payload?.length) return null;
                const d = payload[0].payload as typeof scatterData[0];
                return (
                  <div style={{ background: '#0B1420', border: '1px solid #1A2A3A', borderRadius: 6, padding: '8px 12px', fontFamily: 'DM Mono', fontSize: 12 }}>
                    <div style={{ color: '#E2EAF4', fontWeight: 500 }}>{d.company}</div>
                    <div style={{ color: '#7A9BBE' }}>Offer: ${d.offer}</div>
                    <div style={{ color: d.return > 0 ? '#10B981' : '#EF4444' }}>Return: {d.return.toFixed(2)}%</div>
                  </div>
                );
              }} />
              <ReferenceLine y={0} stroke="#EF4444" strokeDasharray="4 2" />
              <Scatter data={scatterData} fill="#0EA5E9" opacity={0.8} />
            </ScatterChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Sector avg returns */}
      <div className="card" style={{ padding: 20 }}>
        <div style={{ fontFamily: 'Syne', fontWeight: 700, fontSize: 14, color: '#E2EAF4', marginBottom: 14 }}>Avg Day-1 Return by Sector</div>
        <ResponsiveContainer width="100%" height={180}>
          <BarChart data={sectorData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1A2A3A" />
            <XAxis dataKey="sector" tick={{ fill: '#7A9BBE', fontSize: 10, fontFamily: 'DM Mono' }} />
            <YAxis tick={{ fill: '#3D5A7A', fontSize: 10, fontFamily: 'DM Mono' }} tickFormatter={v => `${v}%`} />
            <Tooltip content={<CustomTooltip />} />
            <ReferenceLine y={0} stroke="#3D5A7A" />
            <Bar dataKey="avgReturn" radius={[3, 3, 0, 0]}>
              {sectorData.map((e, i) => <Cell key={i} fill={e.avgReturn > 0 ? '#10B981' : '#EF4444'} />)}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* IPO table */}
      <div className="card" style={{ padding: 20 }}>
        <div style={{ fontFamily: 'Syne', fontWeight: 700, fontSize: 14, color: '#E2EAF4', marginBottom: 14 }}>IPO Database — Full Cohort</div>
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontFamily: 'DM Mono', fontSize: 11 }}>
            <thead>
              <tr style={{ borderBottom: '1px solid #1A2A3A' }}>
                {['Company', 'Ticker', 'IPO Date', 'Country', 'Offer $', 'Day-1 %', 'Total %', 'Deal Size', 'Assessment', 'MLOT'].map(h => (
                  <th key={h} style={{ padding: '6px 10px', color: '#3D5A7A', textAlign: 'left', fontSize: 10, textTransform: 'uppercase', letterSpacing: '0.05em', whiteSpace: 'nowrap' }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {ipos.map((row, i) => {
                const d1 = Number(row.first_day_return_pct);
                const total = Number(row.total_return_pct);
                const assessment = String(row.pricing_assessment || '—');
                const assessColor = assessment.includes('Significantly') ? '#F97316' : assessment.includes('Moderately') ? '#F59E0B' : assessment.includes('Fairly') ? '#10B981' : '#7A9BBE';
                return (
                  <tr key={i} style={{ borderBottom: '1px solid rgba(26,42,58,0.5)' }}>
                    <td style={{ padding: '8px 10px', color: '#E2EAF4', whiteSpace: 'nowrap' }}>{String(row.company || '').slice(0, 20)}</td>
                    <td style={{ padding: '8px 10px', color: '#0EA5E9' }}>{String(row.ticker)}</td>
                    <td style={{ padding: '8px 10px', color: '#7A9BBE', whiteSpace: 'nowrap' }}>{String(row.ipo_date || '').slice(0, 10)}</td>
                    <td style={{ padding: '8px 10px', color: '#7A9BBE' }}>{String(row.country)}</td>
                    <td style={{ padding: '8px 10px', color: '#E2EAF4' }}>${Number(row.offer_price).toFixed(2)}</td>
                    <td style={{ padding: '8px 10px', color: d1 > 0 ? '#10B981' : '#EF4444' }}>{d1.toFixed(2)}%</td>
                    <td style={{ padding: '8px 10px', color: total > 0 ? '#10B981' : '#EF4444' }}>{isNaN(total) ? '—' : `${total.toFixed(2)}%`}</td>
                    <td style={{ padding: '8px 10px', color: '#7A9BBE', whiteSpace: 'nowrap' }}>{fmtBn(Number(row.deal_size_usd) / 1e9)}</td>
                    <td style={{ padding: '8px 10px' }}><span style={{ color: assessColor, fontSize: 10 }}>{assessment.replace(' Priced', '')}</span></td>
                    <td style={{ padding: '8px 10px', color: '#F97316' }}>{fmtBn(Number(row.money_left_on_table_usd) / 1e9)}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────
// SECTION: M&A
// ─────────────────────────────────────────────
function MnaSection({ data }: { data: AllData }) {
  const deals = data.dealScreening.length > 0 ? data.dealScreening : data.mnaRaw;
  const completed = deals.filter(r => Number(r.completed) === 1 || r.status === 'Completed').length;
  const totalValue = data.mnaRaw.reduce((s, r) => s + Number(r.deal_value_usd_bn || 0), 0);
  const crossBorder = data.mnaRaw.filter(r => r.cross_border === 'True' || String(r.cross_border) === 'true').length;
  const avgProb = data.dealScreening.reduce((s, r) => s + Number(r.completion_probability_pct || 0), 0) / (data.dealScreening.length || 1);

  // Feature importance
  const features = data.dealFeatures.map(r => ({
    feature: String(r.feature).replace('is_', '').replace('_', ' '),
    correlation: Number(r.correlation),
    abs: Math.abs(Number(r.correlation)),
    direction: String(r.direction),
  })).sort((a, b) => b.abs - a.abs);

  // Sector breakdown
  const sectorDeals = data.mnaRaw.reduce((acc, r) => {
    const s = String(r.sector || 'Other');
    if (!acc[s]) acc[s] = { count: 0, value: 0 };
    acc[s].count++;
    acc[s].value += Number(r.deal_value_usd_bn || 0);
    return acc;
  }, {} as Record<string, { count: number; value: number }>);

  const sectorArr = Object.entries(sectorDeals).map(([sector, d]) => ({ sector: sector.slice(0, 15), count: d.count, value: d.value }));

  const PALETTE = ['#0EA5E9', '#10B981', '#F59E0B', '#8B5CF6', '#EF4444', '#06B6D4', '#F97316'];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))', gap: 12 }}>
        <StatCard label="Total M&A Value" value={fmtBn(totalValue)} color="#F59E0B" />
        <StatCard label="Deals Tracked" value={String(data.mnaRaw.length)} color="#0EA5E9" />
        <StatCard label="Completed" value={`${completed}/${deals.length}`} sub={`${((completed / (deals.length || 1)) * 100).toFixed(0)}% completion rate`} color="#10B981" />
        <StatCard label="Cross-Border" value={`${crossBorder}/${data.mnaRaw.length}`} color="#8B5CF6" />
        <StatCard label="Avg Completion Prob" value={fmtPct(avgProb)} color="#06B6D4" />
        <StatCard label="Largest Deal" value={fmtBn(Math.max(...data.mnaRaw.map(r => Number(r.deal_value_usd_bn || 0))))} color="#F97316" />
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
        {/* Feature importance */}
        <div className="card" style={{ padding: 20 }}>
          <div style={{ fontFamily: 'Syne', fontWeight: 700, fontSize: 14, color: '#E2EAF4', marginBottom: 4 }}>Deal Screening — Feature Importance</div>
          <div style={{ color: '#3D5A7A', fontSize: 11, fontFamily: 'DM Mono', marginBottom: 14 }}>Point-biserial correlation vs completion</div>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={features} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="#1A2A3A" horizontal={false} />
              <XAxis type="number" tick={{ fill: '#3D5A7A', fontSize: 10, fontFamily: 'DM Mono' }} />
              <YAxis type="category" dataKey="feature" tick={{ fill: '#7A9BBE', fontSize: 10, fontFamily: 'DM Mono' }} width={80} />
              <Tooltip content={<CustomTooltip />} />
              <ReferenceLine x={0} stroke="#3D5A7A" />
              <Bar dataKey="correlation" radius={[0, 2, 2, 0]}>
                {features.map((e, i) => <Cell key={i} fill={e.direction === 'Positive' ? '#10B981' : '#EF4444'} />)}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Sector value */}
        <div className="card" style={{ padding: 20 }}>
          <div style={{ fontFamily: 'Syne', fontWeight: 700, fontSize: 14, color: '#E2EAF4', marginBottom: 4 }}>M&A Value by Sector</div>
          <div style={{ color: '#3D5A7A', fontSize: 11, fontFamily: 'DM Mono', marginBottom: 14 }}>Total deal value in $B</div>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={sectorArr}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1A2A3A" />
              <XAxis dataKey="sector" tick={{ fill: '#7A9BBE', fontSize: 9, fontFamily: 'DM Mono' }} angle={-25} textAnchor="end" height={50} />
              <YAxis tick={{ fill: '#3D5A7A', fontSize: 10, fontFamily: 'DM Mono' }} tickFormatter={v => `$${v}B`} />
              <Tooltip content={<CustomTooltip />} />
              <Bar dataKey="value" radius={[3, 3, 0, 0]}>
                {sectorArr.map((_, i) => <Cell key={i} fill={PALETTE[i % PALETTE.length]} />)}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Completion probability scatter */}
      <div className="card" style={{ padding: 20 }}>
        <div style={{ fontFamily: 'Syne', fontWeight: 700, fontSize: 14, color: '#E2EAF4', marginBottom: 4 }}>Deal Completion Probability Model</div>
        <div style={{ color: '#3D5A7A', fontSize: 11, fontFamily: 'DM Mono', marginBottom: 14 }}>Screened probability vs deal value</div>
        <ResponsiveContainer width="100%" height={200}>
          <ScatterChart>
            <CartesianGrid strokeDasharray="3 3" stroke="#1A2A3A" />
            <XAxis dataKey="dealVal" name="Deal Value ($B)" tick={{ fill: '#3D5A7A', fontSize: 10, fontFamily: 'DM Mono' }} label={{ value: 'Deal Value ($B)', fill: '#3D5A7A', fontSize: 10, position: 'insideBottom', offset: -5 }} />
            <YAxis dataKey="prob" name="Completion %" tick={{ fill: '#3D5A7A', fontSize: 10, fontFamily: 'DM Mono' }} tickFormatter={v => `${v}%`} />
            <Tooltip cursor={{ stroke: '#1A2A3A' }} content={({ payload }) => {
              if (!payload?.length) return null;
              const d = payload[0].payload as { acquirer: string; target: string; dealVal: number; prob: number };
              return (
                <div style={{ background: '#0B1420', border: '1px solid #1A2A3A', borderRadius: 6, padding: '8px 12px', fontFamily: 'DM Mono', fontSize: 11 }}>
                  <div style={{ color: '#E2EAF4' }}>{d.acquirer} → {d.target}</div>
                  <div style={{ color: '#7A9BBE' }}>Value: ${d.dealVal}B</div>
                  <div style={{ color: '#0EA5E9' }}>Prob: {d.prob?.toFixed(1)}%</div>
                </div>
              );
            }} />
            <Scatter
              data={data.dealScreening.map(r => ({
                dealVal: Number(r.deal_value_usd_bn),
                prob: Number(r.completion_probability_pct),
                acquirer: String(r.acquirer).slice(0, 15),
                target: String(r.target).slice(0, 15),
                completed: Number(r.completed),
              }))}
              fill="#0EA5E9"
            >
              {data.dealScreening.map((r, i) => <Cell key={i} fill={Number(r.completed) === 1 ? '#10B981' : '#EF4444'} opacity={0.85} />)}
            </Scatter>
          </ScatterChart>
        </ResponsiveContainer>
        <div style={{ display: 'flex', gap: 16, marginTop: 8 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: 11, fontFamily: 'DM Mono', color: '#7A9BBE' }}><div style={{ width: 10, height: 10, borderRadius: '50%', background: '#10B981' }} /> Completed</div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: 11, fontFamily: 'DM Mono', color: '#7A9BBE' }}><div style={{ width: 10, height: 10, borderRadius: '50%', background: '#EF4444' }} /> Pending / Failed</div>
        </div>
      </div>

      {/* M&A Deal Table */}
      <div className="card" style={{ padding: 20 }}>
        <div style={{ fontFamily: 'Syne', fontWeight: 700, fontSize: 14, color: '#E2EAF4', marginBottom: 14 }}>M&A Deal Database</div>
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontFamily: 'DM Mono', fontSize: 11 }}>
            <thead>
              <tr style={{ borderBottom: '1px solid #1A2A3A' }}>
                {['Acquirer', 'Target', 'Value ($B)', 'Status', 'Sector', 'Type', 'X-Border', 'Completion %'].map(h => (
                  <th key={h} style={{ padding: '6px 10px', color: '#3D5A7A', textAlign: 'left', fontSize: 10, textTransform: 'uppercase', letterSpacing: '0.05em', whiteSpace: 'nowrap' }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {data.dealScreening.map((row, i) => {
                const status = String(row.status || '');
                const statusColor = status.includes('Completed') ? '#10B981' : status.includes('Pending') ? '#F59E0B' : '#EF4444';
                return (
                  <tr key={i} style={{ borderBottom: '1px solid rgba(26,42,58,0.5)' }}>
                    <td style={{ padding: '8px 10px', color: '#E2EAF4', whiteSpace: 'nowrap' }}>{String(row.acquirer || '').slice(0, 20)}</td>
                    <td style={{ padding: '8px 10px', color: '#7A9BBE', whiteSpace: 'nowrap' }}>{String(row.target || '').slice(0, 18)}</td>
                    <td style={{ padding: '8px 10px', color: '#F59E0B' }}>${Number(row.deal_value_usd_bn).toFixed(1)}B</td>
                    <td style={{ padding: '8px 10px' }}><span style={{ color: statusColor, fontSize: 10 }}>{status.slice(0, 18)}</span></td>
                    <td style={{ padding: '8px 10px', color: '#7A9BBE', whiteSpace: 'nowrap' }}>{String(row.sector || '').slice(0, 18)}</td>
                    <td style={{ padding: '8px 10px', color: '#7A9BBE' }}>{String(row.deal_type || '').slice(0, 16)}</td>
                    <td style={{ padding: '8px 10px', color: (row.cross_border === 'True' || row.is_cross_border === 1) ? '#8B5CF6' : '#3D5A7A' }}>
                      {(row.cross_border === 'True' || row.is_cross_border === 1) ? 'Yes' : 'No'}
                    </td>
                    <td style={{ padding: '8px 10px', color: Number(row.completion_probability_pct) > 50 ? '#10B981' : '#EF4444' }}>
                      {fmtPct(row.completion_probability_pct as number)}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────
// SECTION: SOVEREIGN RISK
// ─────────────────────────────────────────────
function SovereignSection({ data }: { data: AllData }) {
  const countries = data.sovereignRisk;
  const sorted = [...countries].sort((a, b) => Number(b.risk_index_0_100) - Number(a.risk_index_0_100));

  // Stress test scenarios
  const scenarios = ['Base Case', 'Fed Hawkish Surprise', 'Global Recession', 'EM Currency Crisis', 'Oil Price Shock'];
  const stressData = scenarios.map(scenario => {
    const rows = data.stressTest.filter(r => r.scenario === scenario);
    const avgRisk = rows.reduce((s, r) => s + Number(r.risk_score || 0), 0) / (rows.length || 1);
    const avgYield = rows.reduce((s, r) => s + Number(r.stressed_yield_pct || 0), 0) / (rows.length || 1);
    return { scenario: scenario.replace('Fed Hawkish Surprise', 'Fed Hawkish').replace('EM Currency Crisis', 'EM FX Crisis'), avgRisk, avgYield };
  });

  // Risk score distribution
  const riskDist = sorted.slice(0, 15).map(r => ({
    country: String(r.country_code),
    score: Number(r.risk_index_0_100),
    tier: String(r.risk_tier),
  }));

  // Macro scatter
  const macroScatter = countries.map(r => ({
    gdp: Number(r['GDP growth (annual %)']),
    inflation: Number(r['Inflation (CPI, annual %)']),
    risk: Number(r.risk_index_0_100),
    country: String(r.country_code),
    tier: String(r.risk_tier),
  })).filter(r => !isNaN(r.gdp) && !isNaN(r.inflation));

  // Issuance by region
  const byRegion = data.sovereignIssuance.reduce((acc, r) => {
    const k = String(r.region || 'Other');
    if (!acc[k]) acc[k] = { count: 0, value: 0 };
    acc[k].count++;
    acc[k].value += Number(r.issue_size_usd_bn || 0);
    return acc;
  }, {} as Record<string, { count: number; value: number }>);
  const regionArr = Object.entries(byRegion).map(([region, d]) => ({ region, count: d.count, value: d.value }));

  const avgRisk = countries.reduce((s, r) => s + Number(r.risk_index_0_100 || 0), 0) / (countries.length || 1);
  const highRisk = countries.filter(r => String(r.risk_tier).includes('High')).length;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))', gap: 12 }}>
        <StatCard label="Sovereigns Tracked" value={String(countries.length)} color="#0EA5E9" />
        <StatCard label="Avg Risk Score" value={fmt(avgRisk, 1)} color="#F59E0B" />
        <StatCard label="High/Critical Risk" value={String(highRisk)} color="#EF4444" />
        <StatCard label="Total Issuance" value={`$${data.sovereignIssuance.reduce((s, r) => s + Number(r.issue_size_usd_bn || 0), 0).toFixed(0)}B`} color="#8B5CF6" />
        <StatCard label="IG Issuances" value={String(data.sovereignIssuance.filter(r => r.investment_grade === 'True' || String(r.investment_grade) === 'true').length)} color="#10B981" />
        <StatCard label="Stress Scenarios" value="60" sub="12 countries × 5 scenarios" color="#06B6D4" />
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
        {/* Risk score bar */}
        <div className="card" style={{ padding: 20 }}>
          <div style={{ fontFamily: 'Syne', fontWeight: 700, fontSize: 14, color: '#E2EAF4', marginBottom: 4 }}>Sovereign Risk Index — Top 15</div>
          <div style={{ color: '#3D5A7A', fontSize: 11, fontFamily: 'DM Mono', marginBottom: 14 }}>Composite score 0–100 (higher = riskier)</div>
          <ResponsiveContainer width="100%" height={240}>
            <BarChart data={riskDist} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="#1A2A3A" horizontal={false} />
              <XAxis type="number" tick={{ fill: '#3D5A7A', fontSize: 10, fontFamily: 'DM Mono' }} domain={[0, 100]} />
              <YAxis type="category" dataKey="country" tick={{ fill: '#7A9BBE', fontSize: 10, fontFamily: 'DM Mono' }} width={32} />
              <Tooltip content={<CustomTooltip />} />
              <Bar dataKey="score" radius={[0, 2, 2, 0]}>
                {riskDist.map((e, i) => <Cell key={i} fill={RISK_COLORS[e.tier] || '#F59E0B'} />)}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Stress scenarios */}
        <div className="card" style={{ padding: 20 }}>
          <div style={{ fontFamily: 'Syne', fontWeight: 700, fontSize: 14, color: '#E2EAF4', marginBottom: 4 }}>Macro Stress Test — 5 Scenarios</div>
          <div style={{ color: '#3D5A7A', fontSize: 11, fontFamily: 'DM Mono', marginBottom: 14 }}>Avg risk score delta + stressed yield</div>
          <ResponsiveContainer width="100%" height={240}>
            <BarChart data={stressData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1A2A3A" />
              <XAxis dataKey="scenario" tick={{ fill: '#7A9BBE', fontSize: 9, fontFamily: 'DM Mono' }} angle={-20} textAnchor="end" height={60} />
              <YAxis yAxisId="risk" tick={{ fill: '#3D5A7A', fontSize: 10, fontFamily: 'DM Mono' }} />
              <YAxis yAxisId="yield" orientation="right" tick={{ fill: '#3D5A7A', fontSize: 10, fontFamily: 'DM Mono' }} tickFormatter={v => `${v}%`} />
              <Tooltip content={<CustomTooltip />} />
              <Bar yAxisId="risk" dataKey="avgRisk" fill="#EF4444" opacity={0.7} radius={[3, 3, 0, 0]} name="Avg Risk Score" />
              <Bar yAxisId="yield" dataKey="avgYield" fill="#0EA5E9" opacity={0.7} radius={[3, 3, 0, 0]} name="Avg Stressed Yield" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* GDP vs inflation macro scatter */}
      <div className="card" style={{ padding: 20 }}>
        <div style={{ fontFamily: 'Syne', fontWeight: 700, fontSize: 14, color: '#E2EAF4', marginBottom: 4 }}>Macro Positioning — GDP Growth vs Inflation</div>
        <div style={{ color: '#3D5A7A', fontSize: 11, fontFamily: 'DM Mono', marginBottom: 14 }}>Colored by risk tier</div>
        <ResponsiveContainer width="100%" height={220}>
          <ScatterChart>
            <CartesianGrid strokeDasharray="3 3" stroke="#1A2A3A" />
            <XAxis dataKey="gdp" name="GDP Growth %" tick={{ fill: '#3D5A7A', fontSize: 10, fontFamily: 'DM Mono' }} label={{ value: 'GDP Growth %', fill: '#3D5A7A', fontSize: 10, position: 'insideBottom', offset: -5 }} />
            <YAxis dataKey="inflation" name="Inflation %" tick={{ fill: '#3D5A7A', fontSize: 10, fontFamily: 'DM Mono' }} label={{ value: 'Inflation %', fill: '#3D5A7A', fontSize: 10, angle: -90, position: 'insideLeft' }} />
            <Tooltip cursor={{ stroke: '#1A2A3A' }} content={({ payload }) => {
              if (!payload?.length) return null;
              const d = payload[0].payload as typeof macroScatter[0];
              return (
                <div style={{ background: '#0B1420', border: '1px solid #1A2A3A', borderRadius: 6, padding: '8px 12px', fontFamily: 'DM Mono', fontSize: 11 }}>
                  <div style={{ color: '#E2EAF4', fontWeight: 500 }}>{d.country}</div>
                  <div style={{ color: '#7A9BBE' }}>GDP: {d.gdp?.toFixed(2)}%</div>
                  <div style={{ color: '#F59E0B' }}>Inflation: {d.inflation?.toFixed(2)}%</div>
                  <div style={{ color: RISK_COLORS[d.tier] || '#0EA5E9' }}>Risk: {d.risk?.toFixed(1)}</div>
                </div>
              );
            }} />
            <ReferenceLine x={0} stroke="#3D5A7A" strokeDasharray="4 2" />
            <ReferenceLine y={5} stroke="#F59E0B" strokeDasharray="4 2" />
            <Scatter data={macroScatter}>
              {macroScatter.map((e, i) => <Cell key={i} fill={RISK_COLORS[e.tier] || '#0EA5E9'} opacity={0.8} />)}
            </Scatter>
          </ScatterChart>
        </ResponsiveContainer>
      </div>

      {/* Issuance by region */}
      <div className="card" style={{ padding: 20 }}>
        <div style={{ fontFamily: 'Syne', fontWeight: 700, fontSize: 14, color: '#E2EAF4', marginBottom: 14 }}>Sovereign Issuance by Region</div>
        <ResponsiveContainer width="100%" height={160}>
          <BarChart data={regionArr}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1A2A3A" />
            <XAxis dataKey="region" tick={{ fill: '#7A9BBE', fontSize: 10, fontFamily: 'DM Mono' }} />
            <YAxis tick={{ fill: '#3D5A7A', fontSize: 10, fontFamily: 'DM Mono' }} tickFormatter={v => `$${v}B`} />
            <Tooltip content={<CustomTooltip />} />
            <Bar dataKey="value" fill="#0EA5E9" opacity={0.8} radius={[3, 3, 0, 0]} name="Value ($B)" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────
// MAIN APP
// ─────────────────────────────────────────────
export default function Home() {
  const [activeTab, setActiveTab] = useState('overview');
  const [data, setData] = useState<AllData | null>(null);
  const [loading, setLoading] = useState(true);

  const loadAll = useCallback(async () => {
    setLoading(true);
    const [
      yieldCurve, regime, marketRates, ipoRaw, ipoEvents, mnaRaw,
      dealScreening, dealFeatures, caseStudies, sovereignRisk,
      stressTest, sovereignIssuance, fxRates, worldbank
    ] = await Promise.all([
      fetchCSV('processed/yield_curve_analysis.csv'),
      fetchCSV('processed/regime_indicators.csv'),
      fetchCSV('raw/market_rates.csv'),
      fetchCSV('raw/ipo_data_raw.csv'),
      fetchCSV('processed/ipo_event_study.csv'),
      fetchCSV('raw/mna_data_raw.csv'),
      fetchCSV('processed/deal_screening_model.csv'),
      fetchCSV('processed/deal_feature_importance.csv'),
      fetchCSV('processed/case_studies.csv'),
      fetchCSV('processed/sovereign_risk_index.csv'),
      fetchCSV('processed/stress_test_results.csv'),
      fetchCSV('raw/sovereign_issuance_raw.csv'),
      fetchCSV('raw/fx_rates.csv'),
      fetchCSV('raw/worldbank_indicators.csv'),
    ]);
    setData({ yieldCurve, regime, marketRates, ipoRaw, ipoEvents, mnaRaw, dealScreening, dealFeatures, caseStudies, sovereignRisk, stressTest, sovereignIssuance, fxRates, worldbank });
    setLoading(false);
  }, []);

  useEffect(() => { loadAll(); }, [loadAll]);

  const now = new Date();

  return (
    <div style={{ minHeight: '100vh', background: 'var(--bg-primary)', display: 'flex', flexDirection: 'column' }}>
      {/* Top bar */}
      <header style={{ background: 'rgba(8,15,24,0.95)', borderBottom: '1px solid #1A2A3A', padding: '0 24px', height: 56, display: 'flex', alignItems: 'center', justifyContent: 'space-between', position: 'sticky', top: 0, zIndex: 100, backdropFilter: 'blur(12px)' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <div style={{ width: 28, height: 28, background: 'linear-gradient(135deg, #0EA5E9, #8B5CF6)', borderRadius: 6, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
              <polyline points="22 7 13.5 15.5 8.5 10.5 2 17" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
              <polyline points="16 7 22 7 22 13" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
          </div>
          <div>
            <div style={{ fontFamily: 'Syne', fontWeight: 700, fontSize: 14, color: '#E2EAF4', lineHeight: 1.2 }}>Capital Markets Intelligence</div>
            <div style={{ fontFamily: 'DM Mono', fontSize: 10, color: '#3D5A7A', letterSpacing: '0.06em' }}>DogInfantry · Production Platform</div>
          </div>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
            <div className="pulse-dot" style={{ width: 6, height: 6, borderRadius: '50%', background: '#10B981' }} />
            <span style={{ fontFamily: 'DM Mono', fontSize: 10, color: '#3D5A7A', letterSpacing: '0.04em' }}>LIVE</span>
          </div>
          <div style={{ fontFamily: 'DM Mono', fontSize: 10, color: '#3D5A7A' }}>
            {now.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
          </div>
        </div>
      </header>

      {/* Nav tabs */}
      <nav style={{ background: 'rgba(8,15,24,0.9)', borderBottom: '1px solid #1A2A3A', padding: '0 24px', display: 'flex', gap: 0, overflowX: 'auto', backdropFilter: 'blur(8px)' }}>
        {TABS.map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className="nav-item"
            style={{
              padding: '14px 18px',
              background: 'none',
              border: 'none',
              borderBottom: activeTab === tab.id ? '2px solid #0EA5E9' : '2px solid transparent',
              color: activeTab === tab.id ? '#0EA5E9' : '#3D5A7A',
              cursor: 'pointer',
              whiteSpace: 'nowrap',
              transition: 'all 0.2s ease',
            }}
          >
            {tab.label}
          </button>
        ))}
      </nav>

      {/* Main content */}
      <main style={{ flex: 1, padding: '24px', maxWidth: 1400, width: '100%', margin: '0 auto' }}>
        {loading ? (
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '60vh', gap: 16 }}>
            <div style={{ width: 40, height: 40, border: '2px solid #1A2A3A', borderTop: '2px solid #0EA5E9', borderRadius: '50%', animation: 'spin 1s linear infinite' }} />
            <div style={{ fontFamily: 'DM Mono', fontSize: 12, color: '#3D5A7A', letterSpacing: '0.08em' }}>LOADING MARKET DATA...</div>
            <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
          </div>
        ) : data && (
          <div className="animate-in">
            {activeTab === 'overview' && <OverviewSection data={data} />}
            {activeTab === 'yield' && <YieldSection data={data} />}
            {activeTab === 'regime' && <RegimeSection data={data} />}
            {activeTab === 'ipo' && <IpoSection data={data} />}
            {activeTab === 'mna' && <MnaSection data={data} />}
            {activeTab === 'sovereign' && <SovereignSection data={data} />}
          </div>
        )}
      </main>

      {/* Footer */}
      <footer style={{ borderTop: '1px solid #1A2A3A', padding: '16px 24px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: 8 }}>
        <div style={{ fontFamily: 'DM Mono', fontSize: 10, color: '#3D5A7A' }}>
          © 2026 DogInfantry · Capital Markets Intelligence Platform · MIT License
        </div>
        <div style={{ display: 'flex', gap: 16 }}>
          {['Yahoo Finance', 'World Bank', 'SEC EDGAR'].map(s => (
            <span key={s} style={{ fontFamily: 'DM Mono', fontSize: 10, color: '#3D5A7A' }}>{s}</span>
          ))}
        </div>
      </footer>
    </div>
  );
}
