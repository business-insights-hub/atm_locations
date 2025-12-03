#!/usr/bin/env python3
"""
Rabita Bank ATM Location Scraper

This script scrapes ATM location data from Rabita Bank's API
and saves it to a CSV file.
"""

import requests
import csv
import json
from typing import List, Dict


def fetch_atm_data(url: str) -> Dict:
    """
    Fetch ATM data from Rabita Bank API.

    Args:
        url: The API endpoint URL

    Returns:
        JSON response as dictionary
    """
    # Create a session to maintain cookies
    session = requests.Session()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'DNT': '1'
    }

    # First, visit the main page to establish a session and get cookies
    print("Establishing session...")
    main_page = "https://www.rabitabank.com/filial-ve-bankomatlar/filiallar"
    session.get(main_page, headers=headers)

    # Now make the API request with the session cookies
    api_headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Referer': 'https://www.rabitabank.com/filial-ve-bankomatlar/filiallar',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'DNT': '1'
    }

    # Get XSRF token from cookies if available
    if 'XSRF-TOKEN' in session.cookies:
        api_headers['X-XSRF-TOKEN'] = session.cookies['XSRF-TOKEN']

    # The API accepts a query parameter 'q' (empty for all ATMs)
    params = {'q': ''}

    response = session.get(url, headers=api_headers, params=params)
    response.raise_for_status()

    return response.json()


def extract_atm_locations(data: Dict) -> List[Dict]:
    """
    Extract ATM location data from API response.

    Args:
        data: JSON response from API

    Returns:
        List of dictionaries containing ATM information
    """
    locations = []

    # The Rabita Bank API returns: {"error": false, "data": [...]}
    atm_list = []

    if isinstance(data, dict) and 'data' in data:
        atm_list = data['data']
    elif isinstance(data, list):
        atm_list = data

    print(f"Found {len(atm_list)} ATM entries in response")

    for atm in atm_list:
        if not isinstance(atm, dict):
            continue

        # Extract coordinates from nested structure
        coords = atm.get('coordinates', {})
        latitude = coords.get('latitude', '') if isinstance(coords, dict) else ''
        longitude = coords.get('longitude', '') if isinstance(coords, dict) else ''

        # Extract location information
        location = {
            'id': atm.get('id', ''),
            'name': atm.get('title', ''),
            'address': atm.get('address', ''),
            'short_address': atm.get('short_address', ''),
            'latitude': latitude,
            'longitude': longitude,
            'type': atm.get('type', ''),
            'work_hours': atm.get('work_hours', ''),
            'work_hours_weekend': atm.get('work_hours_weekend', ''),
            'cash_in': 'Yes' if atm.get('cash_in') else 'No',
            'exchange': 'Yes' if atm.get('exchange') else 'No',
        }

        # Only add if we have at least coordinates or address
        if location['latitude'] or location['longitude'] or location['address']:
            locations.append(location)

    return locations


def save_to_csv(locations: List[Dict], filename: str) -> None:
    """
    Save ATM location data to CSV file.

    Args:
        locations: List of location dictionaries
        filename: Output CSV filename
    """
    if not locations:
        print("No locations to save")
        return

    # Define CSV columns
    fieldnames = [
        'id',
        'name',
        'address',
        'short_address',
        'latitude',
        'longitude',
        'type',
        'work_hours',
        'work_hours_weekend',
        'cash_in',
        'exchange'
    ]

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(locations)

    print(f"Saved {len(locations)} ATM locations to {filename}")


def main():
    """Main function to orchestrate the scraping process."""
    print("Starting Rabita Bank ATM scraper...")

    # Rabita Bank ATM API endpoint
    url = "https://www.rabitabank.com/filial-ve-bankomatlar/bankomatlar"

    try:
        # Fetch ATM data from API
        print(f"Fetching data from {url}...")
        data = fetch_atm_data(url)

        # Extract ATM locations
        print("Extracting ATM location data...")
        locations = extract_atm_locations(data)

        # Save to CSV
        output_file = "../data/rabita_atms.csv"
        print(f"Saving to {output_file}...")
        save_to_csv(locations, output_file)

        # Print summary statistics
        print("\n=== Summary ===")
        print(f"Total ATMs: {len(locations)}")

        # Count locations with coordinates
        with_coords = len([loc for loc in locations if loc['latitude'] and loc['longitude']])
        print(f"ATMs with coordinates: {with_coords}")

        # Count ATMs with cash-in capability
        cash_in_count = len([loc for loc in locations if loc.get('cash_in') == 'Yes'])
        print(f"ATMs with cash-in capability: {cash_in_count}")

        # Count ATMs with currency exchange
        exchange_count = len([loc for loc in locations if loc.get('exchange') == 'Yes'])
        print(f"ATMs with currency exchange: {exchange_count}")

        # Count 24/7 ATMs
        full_time = len([loc for loc in locations if loc.get('work_hours') == '24/7'])
        print(f"24/7 ATMs: {full_time}")

        print("\n✓ Rabita Bank scraping completed successfully!")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        raise
    except Exception as e:
        print(f"Error: {e}")
        raise


if __name__ == "__main__":
    main()
