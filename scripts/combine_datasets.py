#!/usr/bin/env python3
"""
Combined Dataset Generator

This script combines all individual bank/store location datasets into one
comprehensive CSV file with normalized columns.

Output: data/combined_locations.csv
"""

import csv
from typing import List, Dict, Optional


def read_csv(filename: str) -> List[Dict[str, str]]:
    """
    Read a CSV file and return list of dictionaries.

    Args:
        filename: Path to CSV file

    Returns:
        List of row dictionaries
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return []


def normalize_abb_atms(rows: List[Dict]) -> List[Dict]:
    """Normalize ABB Bank ATM data."""
    normalized = []
    for row in rows:
        normalized.append({
            "source": "ABB Bank",
            "type": "ATM",
            "location_id": row.get("ext_id", ""),
            "name": row.get("name", ""),
            "address": row.get("address", ""),
            "city": "",
            "country": "Azerbaijan",
            "latitude": row.get("lat", ""),
            "longitude": row.get("lon", ""),
            "phone": row.get("phone", ""),
            "email": "",
            "website": "",
            "working_hours_weekday": row.get("weekdays", ""),
            "working_hours_saturday": row.get("saturdays", ""),
            "working_hours_sunday": "",
            "cash_in": row.get("atm_cash_in", ""),
            "nfc": "",
            "24_7": row.get("full_day", ""),
            "work_on_weekend": row.get("work_on_weekend", ""),
            "additional_info": f"Status: {row.get('status', '')}, Type: {row.get('type', '')}",
        })
    return normalized


def normalize_bazarstore_branches(rows: List[Dict]) -> List[Dict]:
    """Normalize Bazarstore branch data."""
    normalized = []
    for row in rows:
        normalized.append({
            "source": "Bazarstore",
            "type": "Store",
            "location_id": row.get("id", ""),
            "name": row.get("name", ""),
            "address": row.get("address", ""),
            "city": row.get("city", ""),
            "country": row.get("country", ""),
            "latitude": row.get("latitude", ""),
            "longitude": row.get("longitude", ""),
            "phone": row.get("phone", ""),
            "email": row.get("email", ""),
            "website": row.get("website", ""),
            "working_hours_weekday": "",
            "working_hours_saturday": "",
            "working_hours_sunday": "",
            "cash_in": "",
            "nfc": "",
            "24_7": "",
            "work_on_weekend": "",
            "additional_info": f"Image: {row.get('image_url', '')}, Description: {row.get('description', '')}",
        })
    return normalized


def normalize_bob_atms(rows: List[Dict]) -> List[Dict]:
    """Normalize Bank of Baku ATM data."""
    normalized = []
    for row in rows:
        address = row.get("api_address") or row.get("predefined_address", "")
        normalized.append({
            "source": "Bank of Baku",
            "type": "ATM",
            "location_id": "",
            "name": row.get("name", ""),
            "address": address,
            "city": "",
            "country": "Azerbaijan",
            "latitude": row.get("lat", ""),
            "longitude": row.get("lon", ""),
            "phone": "",
            "email": "",
            "website": "",
            "working_hours_weekday": "",
            "working_hours_saturday": "",
            "working_hours_sunday": "",
            "cash_in": "",
            "nfc": "",
            "24_7": "",
            "work_on_weekend": "",
            "additional_info": f"Services: {row.get('service_names', '')}, Matched: {row.get('matched', '')}",
        })
    return normalized


def normalize_br_atms(rows: List[Dict]) -> List[Dict]:
    """Normalize Bank Respublika ATM data."""
    normalized = []
    for row in rows:
        normalized.append({
            "source": "Bank Respublika",
            "type": row.get("type", "ATM"),
            "location_id": row.get("id", ""),
            "name": row.get("title", ""),
            "address": row.get("info", ""),
            "city": row.get("city_location", ""),
            "country": "Azerbaijan",
            "latitude": row.get("latitude", ""),
            "longitude": row.get("longitude", ""),
            "phone": "",
            "email": "",
            "website": "",
            "working_hours_weekday": "",
            "working_hours_saturday": "",
            "working_hours_sunday": "",
            "cash_in": row.get("cash_in", ""),
            "nfc": "",
            "24_7": "",
            "work_on_weekend": "",
            "additional_info": f"Currencies: {row.get('atm_currencies', '')}, Categories: {row.get('categories', '')}",
        })
    return normalized


def normalize_bravo_branches(rows: List[Dict]) -> List[Dict]:
    """Normalize Bravo Supermarket branch data."""
    normalized = []
    for row in rows:
        normalized.append({
            "source": "Bravo Supermarket",
            "type": row.get("type", "Store"),
            "location_id": "",
            "name": row.get("name", ""),
            "address": row.get("address", ""),
            "city": "",
            "country": "Azerbaijan",
            "latitude": row.get("latitude", ""),
            "longitude": row.get("longitude", ""),
            "phone": row.get("phone", ""),
            "email": "",
            "website": "",
            "working_hours_weekday": row.get("working_hours", ""),
            "working_hours_saturday": "",
            "working_hours_sunday": "",
            "cash_in": "",
            "nfc": "",
            "24_7": "",
            "work_on_weekend": "",
            "additional_info": "",
        })
    return normalized


def normalize_kb_atms(rows: List[Dict]) -> List[Dict]:
    """Normalize Kapital Bank ATM data."""
    normalized = []
    for row in rows:
        normalized.append({
            "source": "Kapital Bank",
            "type": row.get("type", "ATM"),
            "location_id": row.get("id", ""),
            "name": row.get("name", ""),
            "address": row.get("address", ""),
            "city": "",
            "country": "Azerbaijan",
            "latitude": row.get("lat", ""),
            "longitude": row.get("lng", ""),
            "phone": "",
            "email": "",
            "website": "",
            "working_hours_weekday": row.get("work_hours_week", ""),
            "working_hours_saturday": row.get("work_hours_saturday", ""),
            "working_hours_sunday": row.get("work_hours_sunday", ""),
            "cash_in": row.get("cash_in", ""),
            "nfc": row.get("is_nfc", ""),
            "24_7": "",
            "work_on_weekend": row.get("working_weekends", ""),
            "additional_info": f"Digital: {row.get('is_digital', '')}, Open: {row.get('is_open', '')}, Notes: {row.get('notes', '')}",
        })
    return normalized


def normalize_oba_branches(rows: List[Dict]) -> List[Dict]:
    """Normalize OBA Bank branch data."""
    normalized = []
    for row in rows:
        normalized.append({
            "source": "OBA Bank",
            "type": "Branch",
            "location_id": row.get("branch_id", ""),
            "name": row.get("name", ""),
            "address": row.get("address", ""),
            "city": "",
            "country": "Azerbaijan",
            "latitude": row.get("latitude", ""),
            "longitude": row.get("longitude", ""),
            "phone": "",
            "email": "",
            "website": "",
            "working_hours_weekday": "",
            "working_hours_saturday": "",
            "working_hours_sunday": "",
            "cash_in": "",
            "nfc": "",
            "24_7": "",
            "work_on_weekend": "",
            "additional_info": f"Distance: {row.get('distance_km', '')} km",
        })
    return normalized


def normalize_rabita_atms(rows: List[Dict]) -> List[Dict]:
    """Normalize Rabita Bank ATM data."""
    normalized = []
    for row in rows:
        normalized.append({
            "source": "Rabita Bank",
            "type": row.get("type", "ATM"),
            "location_id": row.get("id", ""),
            "name": row.get("name", ""),
            "address": row.get("address", ""),
            "city": "",
            "country": "Azerbaijan",
            "latitude": row.get("latitude", ""),
            "longitude": row.get("longitude", ""),
            "phone": "",
            "email": "",
            "website": "",
            "working_hours_weekday": row.get("work_hours", ""),
            "working_hours_saturday": "",
            "working_hours_sunday": row.get("work_hours_weekend", ""),
            "cash_in": row.get("cash_in", ""),
            "nfc": "",
            "24_7": "",
            "work_on_weekend": "",
            "additional_info": f"Exchange: {row.get('exchange', '')}",
        })
    return normalized


def normalize_xb_atms(rows: List[Dict]) -> List[Dict]:
    """Normalize Xalq Bank ATM data."""
    normalized = []
    for row in rows:
        normalized.append({
            "source": "Xalq Bank",
            "type": "ATM",
            "location_id": row.get("id", ""),
            "name": row.get("title", ""),
            "address": row.get("address", ""),
            "city": "",
            "country": "Azerbaijan",
            "latitude": row.get("lat", ""),
            "longitude": row.get("lon", ""),
            "phone": row.get("phone", ""),
            "email": "",
            "website": "",
            "working_hours_weekday": row.get("working_hours", ""),
            "working_hours_saturday": "",
            "working_hours_sunday": "",
            "cash_in": "",
            "nfc": "",
            "24_7": "",
            "work_on_weekend": "",
            "additional_info": "",
        })
    return normalized


def normalize_yelo_atms(rows: List[Dict]) -> List[Dict]:
    """Normalize Yelo Bank ATM data."""
    normalized = []
    for row in rows:
        normalized.append({
            "source": "Yelo Bank",
            "type": "ATM",
            "location_id": row.get("id", ""),
            "name": row.get("name", ""),
            "address": row.get("address", ""),
            "city": "",
            "country": "Azerbaijan",
            "latitude": row.get("latitude", ""),
            "longitude": row.get("longitude", ""),
            "phone": "",
            "email": "",
            "website": "",
            "working_hours_weekday": row.get("working_hours", ""),
            "working_hours_saturday": "",
            "working_hours_sunday": "",
            "cash_in": "",
            "nfc": "",
            "24_7": "",
            "work_on_weekend": "",
            "additional_info": f"Metro: {row.get('metro', '')}",
        })
    return normalized


def main():
    """Main execution function."""
    print("Combining all datasets...")

    all_locations = []

    # Process each dataset
    datasets = [
        ("data/abb_atms.csv", normalize_abb_atms, "ABB Bank ATMs"),
        ("data/bazarstore_branches.csv", normalize_bazarstore_branches, "Bazarstore branches"),
        ("data/bob_atms.csv", normalize_bob_atms, "Bank of Baku ATMs"),
        ("data/br_atms.csv", normalize_br_atms, "Bank Respublika ATMs"),
        ("data/bravo_branches.csv", normalize_bravo_branches, "Bravo branches"),
        ("data/kb_atms.csv", normalize_kb_atms, "Kapital Bank ATMs"),
        ("data/oba_branches.csv", normalize_oba_branches, "OBA Bank branches"),
        ("data/rabita_atms.csv", normalize_rabita_atms, "Rabita Bank ATMs"),
        ("data/xb_atms.csv", normalize_xb_atms, "Xalq Bank ATMs"),
        ("data/yelo_atms.csv", normalize_yelo_atms, "Yelo Bank ATMs"),
    ]

    for filename, normalizer, description in datasets:
        rows = read_csv(filename)
        if rows:
            normalized = normalizer(rows)
            all_locations.extend(normalized)
            print(f"  Added {len(normalized)} locations from {description}")

    # Save combined dataset
    if all_locations:
        fieldnames = [
            "source", "type", "location_id", "name", "address", "city", "country",
            "latitude", "longitude", "phone", "email", "website",
            "working_hours_weekday", "working_hours_saturday", "working_hours_sunday",
            "cash_in", "nfc", "24_7", "work_on_weekend", "additional_info"
        ]

        output_file = "data/combined_locations.csv"
        try:
            with open(output_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(all_locations)

            print(f"\nSuccessfully created combined dataset: {output_file}")
            print(f"Total locations: {len(all_locations)}")

            # Print summary by source
            print("\nBreakdown by source:")
            sources = {}
            for loc in all_locations:
                source = loc["source"]
                sources[source] = sources.get(source, 0) + 1

            for source, count in sorted(sources.items()):
                print(f"  {source}: {count}")

        except IOError as e:
            print(f"Error writing combined dataset: {e}")
    else:
        print("No data to combine")


if __name__ == "__main__":
    main()
