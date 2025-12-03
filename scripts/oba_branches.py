#!/usr/bin/env python3
"""
OBA Bank Branch Location Scraper

This script scrapes branch location data from OBA Bank's website (oba.az).
The data is embedded in the page as a JavaScript array variable 'my_Coords'.

Data extracted:
- Branch ID
- Branch name
- Latitude and longitude coordinates
- Distance from reference point
"""

import csv
import json
import re
import requests
from typing import List, Dict, Optional


def fetch_oba_branches() -> Optional[str]:
    """
    Fetch the OBA branches webpage containing embedded JavaScript data.

    Returns:
        HTML content as string, or None if request fails
    """
    url = "https://oba.az/branches/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "az,en-US;q=0.7,en;q=0.3",
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching OBA branches: {e}")
        return None


def extract_coordinates_from_html(html_content: str) -> List[List]:
    """
    Extract the my_Coords JavaScript array from HTML content.

    Args:
        html_content: Raw HTML content from the webpage

    Returns:
        List of branch data arrays, each containing:
        [latitude, longitude, branch_id, branch_name, distance]
    """
    # Pattern to match: var my_Coords = [[...], [...], ...];
    pattern = r'var\s+my_Coords\s*=\s*(\[[\s\S]*?\]);'

    match = re.search(pattern, html_content)
    if not match:
        print("Could not find my_Coords variable in HTML")
        return []

    try:
        # Extract the array string and parse as JSON
        coords_str = match.group(1)
        coords_data = json.loads(coords_str)
        return coords_data
    except (json.JSONDecodeError, AttributeError) as e:
        print(f"Error parsing coordinates data: {e}")
        return []


def parse_branch_data(coords_data: List[List]) -> List[Dict[str, str]]:
    """
    Convert raw coordinate arrays into structured branch dictionaries.

    Args:
        coords_data: List of arrays with branch data

    Returns:
        List of dictionaries with structured branch information
    """
    branches = []

    for item in coords_data:
        if len(item) >= 5:
            branch = {
                "name": item[3],  # Branch name
                "branch_id": item[2],  # Branch ID
                "address": item[3],  # Using name as address since no separate address field
                "latitude": str(item[0]),
                "longitude": str(item[1]),
                "distance_km": str(item[4])
            }
            branches.append(branch)

    return branches


def save_to_csv(branches: List[Dict[str, str]], filename: str = "data/ob_branches.csv") -> None:
    """
    Save branch data to CSV file.

    Args:
        branches: List of branch dictionaries
        filename: Output CSV filename
    """
    if not branches:
        print("No branch data to save")
        return

    fieldnames = ["name", "branch_id", "address", "latitude", "longitude", "distance_km"]

    try:
        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(branches)

        print(f"Successfully saved {len(branches)} branches to {filename}")
    except IOError as e:
        print(f"Error writing to CSV: {e}")


def main():
    """Main execution function."""
    print("Fetching OBA branch data...")

    # Fetch the webpage
    html_content = fetch_oba_branches()
    if not html_content:
        print("Failed to fetch webpage")
        return

    # Extract coordinates array from JavaScript
    coords_data = extract_coordinates_from_html(html_content)
    if not coords_data:
        print("Failed to extract coordinate data")
        return

    print(f"Found {len(coords_data)} branches")

    # Parse into structured data
    branches = parse_branch_data(coords_data)

    # Save to CSV
    save_to_csv(branches)


if __name__ == "__main__":
    main()
