"use client";

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

function markerColor(source: string): string {
  return SOURCE_COLORS[source] ?? "#6f7f97";
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

  return (
    <div className="map-shell">
      <div className="map-legend">
        {Object.entries(SOURCE_COLORS).map(([source, color]) => (
          <div key={source} className="legend-item">
            <span className="legend-dot" style={{ backgroundColor: color }} />
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
            pathOptions={{ color: markerColor(point.source), fillOpacity: 0.7, weight: 1.2 }}
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
