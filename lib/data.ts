import fs from "node:fs/promises";
import path from "node:path";
import { LocationRecord } from "@/lib/types";

const ATM_TYPES = new Set(["ATM", "A", "atm", "network_atm"]);
const RETAIL_TYPES = new Set([
  "Branch",
  "branch",
  "Store",
  "store",
  "Ekspres",
  "Express",
  "Hiper",
  "Market",
  "Premium",
  "Super"
]);

function parseCsvLine(line: string): string[] {
  const out: string[] = [];
  let current = "";
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

    if (ch === "," && !inQuotes) {
      out.push(current);
      current = "";
      continue;
    }

    current += ch;
  }

  out.push(current);
  return out;
}

function coerceNumber(input: string): number {
  const value = Number(input);
  return Number.isFinite(value) ? value : NaN;
}

export async function loadCombinedDataset(): Promise<LocationRecord[]> {
  const filePath = path.join(process.cwd(), "data", "combined_locations.csv");
  const raw = await fs.readFile(filePath, "utf-8");
  const lines = raw.split(/\r?\n/).filter((line) => line.trim().length > 0);

  if (lines.length < 2) {
    return [];
  }

  const headers = parseCsvLine(lines[0]);
  const rows: LocationRecord[] = [];

  for (let i = 1; i < lines.length; i += 1) {
    const cols = parseCsvLine(lines[i]);
    const rec: Record<string, string> = {};

    headers.forEach((header, idx) => {
      rec[header] = (cols[idx] ?? "").trim();
    });

    const latitude = coerceNumber(rec.latitude ?? "");
    const longitude = coerceNumber(rec.longitude ?? "");

    if (!Number.isFinite(latitude) || !Number.isFinite(longitude)) {
      continue;
    }

    const normalizedSource = rec.source === "OBA Bank" ? "OBA Supermarket" : rec.source ?? "";

    rows.push({
      source: normalizedSource,
      type: rec.type ?? "",
      location_id: rec.location_id ?? "",
      name: rec.name ?? "",
      address: rec.address ?? "",
      city: rec.city ?? "",
      country: rec.country ?? "",
      latitude,
      longitude,
      phone: rec.phone ?? "",
      email: rec.email ?? "",
      website: rec.website ?? "",
      working_hours_weekday: rec.working_hours_weekday ?? "",
      working_hours_saturday: rec.working_hours_saturday ?? "",
      working_hours_sunday: rec.working_hours_sunday ?? "",
      cash_in: rec.cash_in ?? "",
      nfc: rec.nfc ?? "",
      twentyFourSeven: rec["24_7"] ?? "",
      work_on_weekend: rec.work_on_weekend ?? "",
      additional_info: rec.additional_info ?? ""
    });
  }

  return rows;
}

export function isAtm(record: LocationRecord): boolean {
  return ATM_TYPES.has(record.type);
}

export function isRetail(record: LocationRecord): boolean {
  return RETAIL_TYPES.has(record.type);
}
