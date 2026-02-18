"use client";

import { MapContainer, TileLayer, CircleMarker, Popup } from "react-leaflet";
import { LocationRecord } from "@/lib/types";

type Props = {
  points: LocationRecord[];
};

function markerColor(source: string): string {
  if (source === "Bank of Baku") {
    return "#0f5fa8";
  }
  if (source.includes("Supermarket") || source.includes("Bazarstore") || source.includes("OBA")) {
    return "#0b9c7b";
  }
  return "#d35454";
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
      <MapContainer center={[centerLat, centerLon]} zoom={8} scrollWheelZoom className="map-view">
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {points.map((point, idx) => (
          <CircleMarker
            key={`${point.source}-${point.latitude}-${point.longitude}-${idx}`}
            center={[point.latitude, point.longitude]}
            radius={5}
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
