#!/usr/bin/env python3
"""
Bravo Supermarket Branch Location Scraper

This script scrapes branch location data from Bravo Supermarket's website
and saves it to a CSV file. Coordinates are extracted from data attributes.
"""

import requests
import csv
import re
from typing import List, Dict
from html.parser import HTMLParser


class BravoBranchParser(HTMLParser):
    """Custom HTML parser for Bravo Supermarket branch data."""

    def __init__(self):
        super().__init__()
        self.branches = []
        self.current_branch = None
        self.in_h3 = False
        self.in_location_span = False
        self.in_phone_span = False
        self.in_address_span = False
        self.in_time_span = False
        self.current_text = []
        self.span_count = 0

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        # Check if this is a branch article with coordinates
        if tag == 'article' and 'data-lat' in attrs_dict and 'data-lng' in attrs_dict:
            # Save previous branch if exists
            if self.current_branch is not None and self.current_branch.get('name'):
                self.branches.append(self.current_branch)

            # Start new branch
            self.current_branch = {
                'latitude': attrs_dict.get('data-lat', ''),
                'longitude': attrs_dict.get('data-lng', ''),
                'name': '',
                'type': '',
                'phone': '',
                'address': '',
                'working_hours': ''
            }
            self.span_count = 0

        # Extract branch name from <h3> tag
        if tag == 'h3' and self.current_branch is not None:
            self.in_h3 = True
            self.current_text = []

        # Extract info from span tags inside li elements
        # The order is: type, phone, address, working hours
        if tag == 'span' and self.current_branch is not None:
            self.span_count += 1
            self.current_text = []

            if self.span_count == 1:
                self.in_location_span = True
            elif self.span_count == 2:
                self.in_phone_span = True
            elif self.span_count == 3:
                self.in_address_span = True
            elif self.span_count == 4:
                self.in_time_span = True

    def handle_endtag(self, tag):
        if tag == 'h3' and self.in_h3:
            self.current_branch['name'] = ''.join(self.current_text).strip()
            self.in_h3 = False
            self.current_text = []

        if tag == 'span':
            text = ''.join(self.current_text).strip()

            if self.in_location_span:
                self.current_branch['type'] = text
                self.in_location_span = False
            elif self.in_phone_span:
                self.current_branch['phone'] = text
                self.in_phone_span = False
            elif self.in_address_span:
                self.current_branch['address'] = text
                self.in_address_span = False
            elif self.in_time_span:
                self.current_branch['working_hours'] = text
                self.in_time_span = False

            self.current_text = []

    def handle_data(self, data):
        if (self.in_h3 or self.in_location_span or self.in_phone_span or
            self.in_address_span or self.in_time_span):
            self.current_text.append(data)


def fetch_page_data(url: str) -> str:
    """
    Fetch the HTML page containing branch data.

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


def extract_branch_locations(html: str) -> List[Dict]:
    """
    Extract branch location data from HTML.

    Args:
        html: HTML content

    Returns:
        List of dictionaries containing branch information
    """
    parser = BravoBranchParser()
    parser.feed(html)

    # Save the last branch if it exists
    if parser.current_branch is not None and parser.current_branch.get('name'):
        parser.branches.append(parser.current_branch)

    print(f"Found {len(parser.branches)} branch locations")

    return parser.branches


def save_to_csv(locations: List[Dict], filename: str) -> None:
    """
    Save branch location data to CSV file.

    Args:
        locations: List of location dictionaries
        filename: Output CSV filename
    """
    if not locations:
        print("No locations to save")
        return

    # Define CSV columns
    fieldnames = [
        'name',
        'type',
        'phone',
        'address',
        'working_hours',
        'latitude',
        'longitude'
    ]

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(locations)

    print(f"Saved {len(locations)} branch locations to {filename}")


def main():
    """Main function to orchestrate the scraping process."""
    print("Starting Bravo Supermarket branch scraper...")

    # Bravo Supermarket branches page
    url = "https://www.bravosupermarket.az/branches/"

    try:
        # Fetch page data
        print(f"Fetching data from {url}...")
        html = fetch_page_data(url)

        # Extract branch locations
        print("Extracting branch location data...")
        locations = extract_branch_locations(html)

        # Save to CSV
        output_file = "../data/bravo_branches.csv"
        print(f"Saving to {output_file}...")
        save_to_csv(locations, output_file)

        # Print summary statistics
        print("\n=== Summary ===")
        print(f"Total branches: {len(locations)}")

        # Count branches with coordinates
        with_coords = len([loc for loc in locations if loc['latitude'] and loc['longitude'] and
                          loc['latitude'] != '0.000000' and loc['longitude'] != '0.000000'])
        print(f"Branches with coordinates: {with_coords}")

        # Count by type
        types = {}
        for loc in locations:
            branch_type = loc.get('type', 'Unknown')
            types[branch_type] = types.get(branch_type, 0) + 1

        print("\nBy type:")
        for branch_type, count in sorted(types.items()):
            print(f"  {branch_type}: {count}")

        # Count 24/7 branches
        full_time = len([loc for loc in locations if '24/7' in loc.get('working_hours', '')])
        print(f"\n24/7 branches: {full_time}")

        print("\n✓ Bravo Supermarket scraping completed successfully!")

    except Exception as e:
        print(f"Error: {e}")
        raise


if __name__ == "__main__":
    main()
