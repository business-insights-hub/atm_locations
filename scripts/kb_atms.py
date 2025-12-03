#!/usr/bin/env python3
"""
Script to fetch Kapital Bank ATM locations and save to CSV
"""

import requests
import csv
import json
from typing import List, Dict
import os


def fetch_atm_data(url: str) -> List[Dict]:
    """
    Fetch ATM location data from Kapital Bank API

    Args:
        url: API endpoint URL

    Returns:
        List of ATM location dictionaries
    """
    print(f"Fetching data from {url}...")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Accept': '*/*',
        'X-Requested-With': 'XMLHttpRequest'
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    data = response.json()
    print(f"Successfully fetched {len(data)} locations")

    return data


def flatten_location_data(locations: List[Dict]) -> List[Dict]:
    """
    Flatten the location data for CSV export

    Args:
        locations: List of location dictionaries

    Returns:
        Flattened list of dictionaries
    """
    flattened = []

    for location in locations:
        # Create base record
        base_record = {
            'id': location.get('id'),
            'name': location.get('name'),
            'slug': location.get('slug'),
            'type': location.get('type'),
            'address': location.get('address'),
            'city_id': location.get('city_id'),
            'lat': location.get('lat'),
            'lng': location.get('lng'),
            'is_open': location.get('is_open'),
            'is_nfc': location.get('is_nfc'),
            'cash_in': location.get('cash_in'),
            'working_weekends': location.get('working_weekends'),
            'is_digital': location.get('is_digital'),
            'work_hours_week': location.get('work_hours_week'),
            'work_hours_saturday': location.get('work_hours_saturday'),
            'work_hours_sunday': location.get('work_hours_sunday'),
            'notes': location.get('notes')
        }

        flattened.append(base_record)

    return flattened


def save_to_csv(data: List[Dict], output_path: str):
    """
    Save data to CSV file

    Args:
        data: List of dictionaries to save
        output_path: Path to output CSV file
    """
    if not data:
        print("No data to save")
        return

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Get all fieldnames from data
    fieldnames = list(data[0].keys())

    print(f"Writing {len(data)} records to {output_path}...")

    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    print(f"Successfully saved data to {output_path}")


def main():
    """Main function"""
    # API endpoint
    api_url = "https://www.kapitalbank.az/locations/region?is_nfc=false&weekend=false&specialdays=false&type=atm"

    # Output path
    output_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'data',
        'kb_atms.csv'
    )

    try:
        # Fetch data
        locations = fetch_atm_data(api_url)

        # Flatten data
        flattened_data = flatten_location_data(locations)

        # Save to CSV
        save_to_csv(flattened_data, output_path)

        print("\nDone!")
        print(f"Total locations: {len(flattened_data)}")

    except Exception as e:
        print(f"Error: {e}")
        raise


if __name__ == "__main__":
    main()
