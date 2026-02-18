"use client";

import { useEffect, useMemo, useState } from "react";
import dynamic from "next/dynamic";
import { CoverageGap, DashboardMetrics, LocationRecord, RetailOpportunity } from "@/lib/types";
import { getDisplaySourceName } from "@/lib/display";

type Props = {
  data: LocationRecord[];
  metrics: DashboardMetrics;
  coverageGaps: CoverageGap[];
  retailOpportunities: RetailOpportunity[];
  roiTop: CoverageGap[];
};

type TabKey = "overview" | "coverage" | "retail" | "competitors" | "roi" | "map";
type MapFilter = "all" | "bob" | "competitors" | "retail";

const CoordinateMap = dynamic(() => import("@/components/CoordinateMap"), {
  ssr: false
});

const tabLabels: Record<TabKey, string> = {
  overview: "Overview",
  coverage: "Coverage Gaps",
  retail: "Retail Opportunities",
  competitors: "Competitor Analysis",
  roi: "ROI Rankings",
  map: "Map View"
};

function formatInt(value: number): string {
  return new Intl.NumberFormat("en-US").format(value);
}

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
  title,
  headers,
  rows
}: {
  title?: string;
  headers: string[];
  rows: Array<Array<string | number>>;
}) {
  return (
    <div className="card table-wrap">
      {title ? <h3 className="table-title">{title}</h3> : null}
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
  const [mapFilter, setMapFilter] = useState<MapFilter>("all");
  const [mapLimit, setMapLimit] = useState(800);
  const [selectedSources, setSelectedSources] = useState<string[]>([]);
  const [mapSourcesInitialized, setMapSourcesInitialized] = useState(false);

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
  const roiTop50 = useMemo(() => roiTop.slice(0, 50), [roiTop]);

  const sourceMix = useMemo(() => {
    const counts = new Map<string, number>();
    for (const row of data) {
      counts.set(row.source, (counts.get(row.source) ?? 0) + 1);
    }
    return [...counts.entries()]
      .map(([source, count]) => ({ source, count }))
      .sort((a, b) => b.count - a.count);
  }, [data]);

  const allSources = useMemo(() => sourceMix.map((x) => x.source), [sourceMix]);

  useEffect(() => {
    if (!mapSourcesInitialized && allSources.length > 0) {
      setSelectedSources(allSources);
      setMapSourcesInitialized(true);
    }
  }, [allSources, mapSourcesInitialized]);

  const geoBounds = useMemo(() => {
    const lats = data.map((x) => x.latitude);
    const lons = data.map((x) => x.longitude);
    return {
      minLat: Math.min(...lats),
      maxLat: Math.max(...lats),
      minLon: Math.min(...lons),
      maxLon: Math.max(...lons)
    };
  }, [data]);

  const roiSummary = useMemo(() => {
    const excellent = roiTop50.filter((x) => (x.roi_score ?? 0) >= 90).length;
    const good = roiTop50.filter((x) => (x.roi_score ?? 0) >= 70 && (x.roi_score ?? 0) < 90).length;
    const fair = roiTop50.filter((x) => (x.roi_score ?? 0) >= 50 && (x.roi_score ?? 0) < 70).length;
    return { excellent, good, fair };
  }, [roiTop50]);

  const mapPoints = useMemo(() => {
    const source = data.filter((row) => {
      if (mapFilter === "all") {
        return true;
      }
      if (mapFilter === "bob") {
        return row.source === "Bank of Baku";
      }
      if (mapFilter === "competitors") {
        return row.source !== "Bank of Baku" && ["ATM", "A", "atm", "network_atm"].includes(row.type);
      }
      return !["ATM", "A", "atm", "network_atm"].includes(row.type);
    });
    const sourceFiltered = source.filter((row) => selectedSources.includes(row.source));
    return sourceFiltered.slice(0, mapLimit);
  }, [data, mapFilter, mapLimit, selectedSources]);

  return (
    <main className="page">
      <header className="header">
        <p className="eyebrow">ATM Expansion Intelligence</p>
        <h1>Bank of Baku Strategy Dashboard</h1>
        <p>
          Responsive Next.js + TypeScript analytics workspace for nationwide ATM coverage,
          competitor pressure, retail partnerships, and ROI prioritization.
        </p>
        <div className="pill-row">
          <span className="pill">Total Locations: {formatInt(data.length)}</span>
          <span className="pill">Banks: {formatInt(bankCounts.length)}</span>
          <span className="pill">Coverage Radius: {radiusKm} km</span>
        </div>
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
            <NumberCard label="Total Market ATMs" value={formatInt(metrics.totalAtmCount)} />
            <NumberCard label="Market Share" value={`${metrics.marketSharePct.toFixed(1)}%`} />
            <NumberCard label="Market Leader" value={`${metrics.leaderName} (${metrics.leaderCount})`} />
            <NumberCard label="Gap to Leader" value={formatInt(metrics.gapToLeader)} />
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

          <section className="grid two-col">
            <div className="card">
              <h3>Dataset Detail</h3>
              <div className="detail-grid">
                <div>
                  <p className="detail-label">Latitude Range</p>
                  <p className="detail-value">
                    {geoBounds.minLat.toFixed(3)} to {geoBounds.maxLat.toFixed(3)}
                  </p>
                </div>
                <div>
                  <p className="detail-label">Longitude Range</p>
                  <p className="detail-value">
                    {geoBounds.minLon.toFixed(3)} to {geoBounds.maxLon.toFixed(3)}
                  </p>
                </div>
                <div>
                  <p className="detail-label">Retail Opportunities</p>
                  <p className="detail-value">{formatInt(retailOpportunities.length)}</p>
                </div>
                <div>
                  <p className="detail-label">ROI Candidates</p>
                  <p className="detail-value">{formatInt(roiTop.length)}</p>
                </div>
              </div>
            </div>
            <div className="card">
              <h3>Source Mix</h3>
              <div className="mix-list">
                {sourceMix.slice(0, 6).map((entry) => (
                  <div key={entry.source} className="mix-row">
                    <span>{entry.source}</span>
                    <strong>{formatInt(entry.count)}</strong>
                  </div>
                ))}
              </div>
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
            <NumberCard label="Total Gaps" value={formatInt(filteredGaps.length)} />
            <NumberCard
              label="Avg Distance to BOB"
              value={`${(filteredGaps.reduce((s: number, x: CoverageGap) => s + x.distance_to_bob, 0) / Math.max(filteredGaps.length, 1)).toFixed(2)} km`}
            />
            <NumberCard
              label="Avg Competitor Density"
              value={(filteredGaps.reduce((s: number, x: CoverageGap) => s + x.competitor_density, 0) / Math.max(filteredGaps.length, 1)).toFixed(1)}
            />
          </section>

          <DataTable
            title="Top Coverage Gaps"
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
            <NumberCard label="Total Opportunities" value={formatInt(retailOpportunities.length)} />
            <NumberCard label="Top Chain" value={getDisplaySourceName(topRetail[0]?.source ?? "N/A")} />
            <NumberCard
              label="Top Score"
              value={topRetail[0] ? topRetail[0].opportunity_score.toFixed(1) : "0"}
            />
          </section>

          <DataTable
            title="Top 20 Retail Partnership Targets"
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
            title="Market Share Breakdown"
            headers={["Rank", "Bank", "ATMs", "Market Share %"]}
            rows={bankCounts.map((entry, idx) => [
              idx + 1,
              entry.label,
              formatInt(entry.value),
              ((entry.value / Math.max(metrics.totalAtmCount, 1)) * 100).toFixed(2)
            ])}
          />
        </>
      )}

      {activeTab === "roi" && (
        <>
          <section className="grid metrics-grid">
            <NumberCard label="Excellent (>=90)" value={roiSummary.excellent} />
            <NumberCard label="Good (70-89)" value={roiSummary.good} />
            <NumberCard label="Fair (50-69)" value={roiSummary.fair} />
            <NumberCard label="Top 50 Mean ROI" value={(roiTop50.reduce((s: number, x: CoverageGap) => s + (x.roi_score ?? 0), 0) / Math.max(roiTop50.length, 1)).toFixed(1)} />
          </section>
          <DataTable
            title="Top 50 ROI-Ranked Locations"
            headers={[
              "Rank",
              "Address",
              "Competitor Bank",
              "ROI Score",
              "Distance to BOB (km)",
              "Competitors Nearby"
            ]}
            rows={roiTop50.map((x, idx) => [
              idx + 1,
              x.address || "N/A",
              x.source,
              (x.roi_score ?? 0).toFixed(1),
              x.distance_to_bob.toFixed(2),
              x.competitor_density
            ])}
          />
        </>
      )}

      {activeTab === "map" && (
        <>
          <section className="card controls">
            <label htmlFor="map-filter">Dataset</label>
            <select
              id="map-filter"
              value={mapFilter}
              onChange={(e) => setMapFilter(e.target.value as MapFilter)}
            >
              <option value="all">All Locations</option>
              <option value="bob">Bank of Baku Only</option>
              <option value="competitors">Competitor ATMs</option>
              <option value="retail">Retail Chains</option>
            </select>

            <label htmlFor="map-limit">Points</label>
            <input
              id="map-limit"
              type="range"
              min={200}
              max={2000}
              step={200}
              value={mapLimit}
              onChange={(e) => setMapLimit(Number(e.target.value))}
            />
            <span className="range-value">{formatInt(mapLimit)}</span>
          </section>

          <section className="card">
            <h3 className="table-title">Source Filter</h3>
            <div className="source-actions">
              <button className="tab" onClick={() => setSelectedSources(allSources)}>Select All</button>
              <button className="tab" onClick={() => setSelectedSources([])}>Clear All</button>
            </div>
            <div className="source-grid">
              {allSources.map((source) => {
                const checked = selectedSources.includes(source);
                return (
                  <label key={source} className="source-item">
                    <input
                      type="checkbox"
                      checked={checked}
                      onChange={(e) => {
                        if (e.target.checked) {
                          setSelectedSources(Array.from(new Set([...selectedSources, source])));
                        } else {
                          setSelectedSources(selectedSources.filter((s) => s !== source));
                        }
                      }}
                    />
                    <span>{source}</span>
                  </label>
                );
              })}
            </div>
          </section>

          <section className="grid metrics-grid">
            <NumberCard label="Visible Points" value={formatInt(mapPoints.length)} />
            <NumberCard label="Filter" value={mapFilter.toUpperCase()} />
            <NumberCard label="BOB Coordinates" value={formatInt(data.filter((x) => x.source === "Bank of Baku").length)} />
            <NumberCard label="Competitor/ Retail Mix" value={`${formatInt(data.length - metrics.bobAtmCount)} / ${formatInt(data.length)}`} />
          </section>

          <div className="card">
            <h3 className="table-title">Interactive Coordinate Map</h3>
            <CoordinateMap points={mapPoints} />
          </div>
        </>
      )}
    </main>
  );
}
