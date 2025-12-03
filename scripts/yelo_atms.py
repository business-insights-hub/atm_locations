#!/usr/bin/env python3
"""
Yelo Bank ATM Location Scraper

This script scrapes ATM location data from Yelo Bank's website
and saves it to a CSV file. Coordinates are extracted from Google Maps links.
"""

import requests
import csv
import re
from typing import List, Dict
from html.parser import HTMLParser


class YeloATMParser(HTMLParser):
    """Custom HTML parser for Yelo Bank ATM data."""

    def __init__(self):
        super().__init__()
        self.atms = []
        self.current_atm = None
        self.in_b_tag = False
        self.in_pin_call = False
        self.in_pin_time = False
        self.in_metro = False
        self.current_text = []
        self.next_is_map_link = False

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        # Check if this is an ATM item (data-filter="pin1177")
        if tag == 'a' and 'data-filter' in attrs_dict:
            # If we have a previous ATM without coordinates, save it now
            if self.current_atm is not None and self.current_atm.get('name'):
                if self.current_atm['latitude'] or self.current_atm['address']:
                    self.atms.append(self.current_atm)

            if attrs_dict.get('data-filter') == 'pin1177':
                # This is an ATM
                self.current_atm = {
                    'id': attrs_dict.get('data-id', ''),
                    'name': '',
                    'metro': '',
                    'address': '',
                    'working_hours': '',
                    'latitude': '',
                    'longitude': ''
                }
            else:
                # This is a branch, skip it
                self.current_atm = None

        # Extract ATM name from <b> tag
        if tag == 'b' and self.current_atm is not None:
            self.in_b_tag = True
            self.current_text = []

        # Extract metro station
        if tag == 'span' and 'class' in attrs_dict:
            if attrs_dict['class'] == 'metro' and self.current_atm is not None:
                self.in_metro = True
                self.current_text = []

        # Extract address from li with class="pin_call"
        if tag == 'li' and 'class' in attrs_dict:
            if attrs_dict['class'] == 'pin_call' and self.current_atm is not None:
                self.in_pin_call = True
                self.current_text = []
            elif attrs_dict['class'] == 'pin_time' and self.current_atm is not None:
                self.in_pin_time = True
                self.current_text = []

        # Check for Google Maps link to extract coordinates
        if tag == 'a' and 'href' in attrs_dict:
            href = attrs_dict['href']
            if 'google.com/maps' in href and 'destination=' in href and self.current_atm is not None:
                # Extract coordinates from URL
                match = re.search(r'destination=([-\d.]+),([-\d.]+)', href)
                if match:
                    self.current_atm['latitude'] = match.group(1)
                    self.current_atm['longitude'] = match.group(2)

    def handle_endtag(self, tag):
        if tag == 'b' and self.in_b_tag:
            self.current_atm['name'] = ''.join(self.current_text).strip()
            self.in_b_tag = False
            self.current_text = []

        if tag == 'span' and self.in_metro:
            self.current_atm['metro'] = ''.join(self.current_text).strip()
            self.in_metro = False
            self.current_text = []

        if tag == 'li':
            if self.in_pin_call:
                self.current_atm['address'] = ''.join(self.current_text).strip()
                self.in_pin_call = False
                self.current_text = []
            elif self.in_pin_time:
                # Clean up working hours text
                hours_text = ''.join(self.current_text).strip()
                # Remove extra whitespace and normalize
                hours_text = re.sub(r'\s+', ' ', hours_text)
                self.current_atm['working_hours'] = hours_text
                self.in_pin_time = False
                self.current_text = []

        # Don't clear current_atm here - we need to keep it alive
        # to capture coordinates from the Google Maps link that comes after
        # The ATM will be saved when we start parsing the next ATM item or at the end

    def handle_data(self, data):
        if self.in_b_tag or self.in_pin_call or self.in_pin_time or self.in_metro:
            self.current_text.append(data)


def fetch_page_data(url: str) -> str:
    """
    Fetch the HTML page containing ATM data.

    Args:
        url: The URL to fetch

    Returns:
        HTML content as string
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text


def extract_atm_locations(html: str) -> List[Dict]:
    """
    Extract ATM location data from HTML.

    Args:
        html: HTML content

    Returns:
        List of dictionaries containing ATM information
    """
    parser = YeloATMParser()
    parser.feed(html)

    # Save the last ATM if it exists
    if parser.current_atm is not None and parser.current_atm.get('name'):
        if parser.current_atm['latitude'] or parser.current_atm['address']:
            parser.atms.append(parser.current_atm)

    print(f"Found {len(parser.atms)} ATM locations")

    return parser.atms


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
        'metro',
        'working_hours',
        'latitude',
        'longitude'
    ]

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(locations)

    print(f"Saved {len(locations)} ATM locations to {filename}")


def main():
    """Main function to orchestrate the scraping process."""
    print("Starting Yelo Bank ATM scraper...")

    # Yelo Bank ATMs and branches page
    url = "https://www.yelo.az/az/individuals/atms-and-branches/"

    try:
        # Fetch page data
        print(f"Fetching data from {url}...")
        html = fetch_page_data(url)

        # Extract ATM locations
        print("Extracting ATM location data...")
        locations = extract_atm_locations(html)

        # Save to CSV
        output_file = "../data/yelo_atms.csv"
        print(f"Saving to {output_file}...")
        save_to_csv(locations, output_file)

        # Print summary statistics
        print("\n=== Summary ===")
        print(f"Total ATMs: {len(locations)}")

        # Count ATMs with coordinates
        with_coords = len([loc for loc in locations if loc['latitude'] and loc['longitude']])
        print(f"ATMs with coordinates: {with_coords}")

        # Count ATMs with metro stations
        with_metro = len([loc for loc in locations if loc['metro']])
        print(f"ATMs near metro stations: {with_metro}")

        # Count by working hours availability
        with_hours = len([loc for loc in locations if loc['working_hours']])
        print(f"ATMs with working hours info: {with_hours}")

        print("\n✓ Yelo Bank scraping completed successfully!")

    except Exception as e:
        print(f"Error: {e}")
        raise


if __name__ == "__main__":
    main()
