"use client";

import { useMemo } from "react";
import { MapContainer, TileLayer, CircleMarker, Popup } from "react-leaflet";
import { LocationRecord } from "@/lib/types";

type Props = {
  points: LocationRecord[];
};

const SOURCE_COLORS: Record<string, string> = {
  "Bank of Baku": "#0f5fa8",
  "Kapital Bank": "#d44f3a",
  "ABB Bank": "#8e4dcf",
  "Xalq Bank": "#f08c00",
  "Bank Respublika": "#2f8f83",
  "Rabita Bank": "#b82f6c",
  "Yelo Bank": "#caa000",
  "OBA Supermarket": "#0b9c7b",
  "Bravo Supermarket": "#2a9d5b",
  Bazarstore: "#1e7f5e"
};

const FALLBACK_COLORS = ["#1f77b4", "#ff7f0e", "#2ca02c", "#9467bd", "#17becf", "#e377c2", "#8c564b", "#bcbd22", "#d62728"];

function normalizeSource(source: string): string {
  const s = source.trim();
  if (s === "OBA Bank") {
    return "OBA Supermarket";
  }
  return s;
}

function fallbackColor(source: string): string {
  let hash = 0;
  for (let i = 0; i < source.length; i += 1) {
    hash = (hash * 31 + source.charCodeAt(i)) >>> 0;
  }
  return FALLBACK_COLORS[hash % FALLBACK_COLORS.length];
}

function markerRadius(source: string): number {
  if (source === "Bank of Baku") {
    return 7;
  }
  if (source.includes("Supermarket") || source === "Bazarstore") {
    return 5;
  }
  return 5.5;
}

export default function CoordinateMap({ points }: Props) {
  const centerLat = points.length
    ? points.reduce((sum, p) => sum + p.latitude, 0) / points.length
    : 40.38;
  const centerLon = points.length
    ? points.reduce((sum, p) => sum + p.longitude, 0) / points.length
    : 49.89;

  const sourcesInView = useMemo(
    () => Array.from(new Set(points.map((point) => normalizeSource(point.source)))).sort(),
    [points]
  );

  const colorBySource = useMemo(() => {
    const out: Record<string, string> = {};
    sourcesInView.forEach((source, idx) => {
      out[source] = SOURCE_COLORS[source] ?? FALLBACK_COLORS[idx % FALLBACK_COLORS.length] ?? fallbackColor(source);
    });
    return out;
  }, [sourcesInView]);

  const resolveColor = (source: string): string => {
    return colorBySource[normalizeSource(source)] ?? "#6f7f97";
  };

  return (
    <div className="map-shell">
      <div className="map-legend">
        {sourcesInView.map((source) => (
          <div key={source} className="legend-item">
            <span className="legend-dot" style={{ backgroundColor: resolveColor(source) }} />
            <span>{source}</span>
          </div>
        ))}
      </div>
      <MapContainer center={[centerLat, centerLon]} zoom={8} scrollWheelZoom className="map-view">
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {points.map((point, idx) => (
          <CircleMarker
            key={`${point.source}-${point.latitude}-${point.longitude}-${idx}`}
            center={[point.latitude, point.longitude]}
            radius={markerRadius(point.source)}
            pathOptions={{
              color: resolveColor(point.source),
              fillColor: resolveColor(point.source),
              fillOpacity: 0.85,
              weight: 1.2
            }}
          >
            <Popup>
              <div>
                <strong>{point.source}</strong>
                <br />
                {point.address || "No address"}
                <br />
                {point.latitude.toFixed(5)}, {point.longitude.toFixed(5)}
              </div>
            </Popup>
          </CircleMarker>
        ))}
      </MapContainer>
    </div>
  );
}
