"use client";

import { useMemo, useState } from "react";
import { CoverageGap, DashboardMetrics, LocationRecord, RetailOpportunity } from "@/lib/types";
import { getDisplaySourceName } from "@/lib/display";

type Props = {
  data: LocationRecord[];
  metrics: DashboardMetrics;
  coverageGaps: CoverageGap[];
  retailOpportunities: RetailOpportunity[];
  roiTop: CoverageGap[];
};

type TabKey = "overview" | "coverage" | "retail" | "competitors" | "roi";

const tabLabels: Record<TabKey, string> = {
  overview: "Overview",
  coverage: "Coverage Gaps",
  retail: "Retail Opportunities",
  competitors: "Competitor Analysis",
  roi: "ROI Rankings"
};

function NumberCard({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="card metric-card">
      <p className="metric-label">{label}</p>
      <p className="metric-value">{value}</p>
    </div>
  );
}

function HorizontalBars({ data }: { data: Array<{ label: string; value: number }> }) {
  const max = Math.max(...data.map((d) => d.value), 1);

  return (
    <div className="card">
      <h3>ATM Distribution by Bank</h3>
      <div className="bars">
        {data.map((item) => (
          <div key={item.label} className="bar-row">
            <span className="bar-label">{item.label}</span>
            <div className="bar-track">
              <div className="bar-fill" style={{ width: `${(item.value / max) * 100}%` }} />
            </div>
            <span className="bar-value">{item.value}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

function DataTable({
  headers,
  rows
}: {
  headers: string[];
  rows: Array<Array<string | number>>;
}) {
  return (
    <div className="card table-wrap">
      <table>
        <thead>
          <tr>
            {headers.map((h) => (
              <th key={h}>{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, idx) => (
            <tr key={idx}>
              {row.map((cell, cellIdx) => (
                <td key={`${idx}-${cellIdx}`}>{cell}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default function Dashboard({
  data,
  metrics,
  coverageGaps,
  retailOpportunities,
  roiTop
}: Props) {
  const [activeTab, setActiveTab] = useState<TabKey>("overview");
  const [radiusKm, setRadiusKm] = useState(2);

  const bankCounts = useMemo(() => {
    const counts = new Map<string, number>();
    for (const row of data) {
      if (!["ATM", "A", "atm", "network_atm"].includes(row.type)) {
        continue;
      }
      counts.set(row.source, (counts.get(row.source) ?? 0) + 1);
    }

    return [...counts.entries()]
      .map(([label, value]) => ({ label, value }))
      .sort((a, b) => b.value - a.value);
  }, [data]);

  const filteredGaps = useMemo(() => coverageGaps.filter((gap) => gap.distance_to_bob > radiusKm), [coverageGaps, radiusKm]);

  const topRetail = useMemo(() => retailOpportunities.slice(0, 20), [retailOpportunities]);

  return (
    <main className="page">
      <header className="header">
        <h1>Bank of Baku ATM Strategy Dashboard</h1>
        <p>Next.js + TypeScript analytics dashboard for ATM expansion planning in Azerbaijan.</p>
      </header>

      <section className="tabs">
        {(Object.keys(tabLabels) as TabKey[]).map((tab) => (
          <button
            key={tab}
            className={tab === activeTab ? "tab active" : "tab"}
            onClick={() => setActiveTab(tab)}
          >
            {tabLabels[tab]}
          </button>
        ))}
      </section>

      {activeTab === "overview" && (
        <>
          <section className="grid metrics-grid">
            <NumberCard label="BOB ATMs" value={metrics.bobAtmCount} />
            <NumberCard label="Total Market ATMs" value={metrics.totalAtmCount} />
            <NumberCard label="Market Share" value={`${metrics.marketSharePct.toFixed(1)}%`} />
            <NumberCard label="Market Leader" value={`${metrics.leaderName} (${metrics.leaderCount})`} />
            <NumberCard label="Gap to Leader" value={metrics.gapToLeader} />
          </section>

          <section className="grid two-col">
            <HorizontalBars data={bankCounts} />
            <div className="card">
              <h3>Strategic Snapshot</h3>
              <ul className="insights">
                <li>Current BOB network remains significantly smaller than the top two competitors.</li>
                <li>Coverage gaps indicate many proven demand zones beyond BOB ATM radius.</li>
                <li>Retail partnership opportunities provide lower-cost expansion options.</li>
                <li>ROI scoring combines distance gap, competitor density, and retail proximity.</li>
              </ul>
            </div>
          </section>
        </>
      )}

      {activeTab === "coverage" && (
        <>
          <section className="card controls">
            <label htmlFor="radius">Coverage Radius (km): {radiusKm}</label>
            <input
              id="radius"
              type="range"
              min={1}
              max={5}
              step={1}
              value={radiusKm}
              onChange={(e) => setRadiusKm(Number(e.target.value))}
            />
          </section>

          <section className="grid metrics-grid">
            <NumberCard label="Total Gaps" value={filteredGaps.length} />
            <NumberCard
              label="Avg Distance to BOB"
              value={`${(filteredGaps.reduce((s, x) => s + x.distance_to_bob, 0) / Math.max(filteredGaps.length, 1)).toFixed(2)} km`}
            />
            <NumberCard
              label="Avg Competitor Density"
              value={(filteredGaps.reduce((s, x) => s + x.competitor_density, 0) / Math.max(filteredGaps.length, 1)).toFixed(1)}
            />
          </section>

          <DataTable
            headers={["Bank", "Address", "Distance to BOB (km)", "Competitors Nearby"]}
            rows={filteredGaps.slice(0, 30).map((g) => [
              g.source,
              g.address || "N/A",
              g.distance_to_bob.toFixed(2),
              g.competitor_density
            ])}
          />
        </>
      )}

      {activeTab === "retail" && (
        <>
          <section className="grid metrics-grid">
            <NumberCard label="Total Opportunities" value={retailOpportunities.length} />
            <NumberCard label="Top Chain" value={getDisplaySourceName(topRetail[0]?.source ?? "N/A")} />
            <NumberCard
              label="Top Score"
              value={topRetail[0] ? topRetail[0].opportunity_score.toFixed(1) : "0"}
            />
          </section>

          <DataTable
            headers={[
              "Retail Chain",
              "Address",
              "Distance to BOB (km)",
              "Competitors Nearby",
              "Opportunity Score"
            ]}
            rows={topRetail.map((x) => [
              getDisplaySourceName(x.source),
              x.address || "N/A",
              x.distance_to_bob.toFixed(2),
              x.competitor_density,
              x.opportunity_score.toFixed(1)
            ])}
          />
        </>
      )}

      {activeTab === "competitors" && (
        <>
          <HorizontalBars data={bankCounts} />
          <DataTable
            headers={["Rank", "Bank", "ATMs", "Market Share %"]}
            rows={bankCounts.map((entry, idx) => [
              idx + 1,
              entry.label,
              entry.value,
              ((entry.value / Math.max(metrics.totalAtmCount, 1)) * 100).toFixed(2)
            ])}
          />
        </>
      )}

      {activeTab === "roi" && (
        <DataTable
          headers={[
            "Rank",
            "Address",
            "Competitor Bank",
            "ROI Score",
            "Distance to BOB (km)",
            "Competitors Nearby"
          ]}
          rows={roiTop.slice(0, 50).map((x, idx) => [
            idx + 1,
            x.address || "N/A",
            x.source,
            (x.roi_score ?? 0).toFixed(1),
            x.distance_to_bob.toFixed(2),
            x.competitor_density
          ])}
        />
      )}
    </main>
  );
}
