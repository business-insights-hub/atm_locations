#!/usr/bin/env python3
"""
Script to fetch Bank of Baku ATM locations and save to CSV
"""

import requests
import csv
import json
import re
from typing import List, Dict, Optional
import os


# Predefined list of ATMs with addresses
ATM_DATA = [
    {"name": "Baş İdarə ATM", "address": "Atatürk pr. 40/42, Bakı"},
    {"name": "Azneft filialının ATM-i", "address": "Neftçilər pr. 65, Bakı"},
    {"name": "Bakıxanov filialının ATM-i", "address": "Gənclər küç. 4081-ci məh., Bakı"},
    {"name": "Əməliyyat mərkəzidə ATM", "address": "A. Neymətulla küç. 63/65, Bakı"},
    {"name": "Əhmədli filialının ATM-i", "address": "Sarayevo küç. 23/65-ci məh., Bakı"},
    {"name": "Həzi Aslanov filialının ATM-i", "address": "Məhəmməd Hadi küçəsi, 152C, Bakı"},
    {"name": "Mərkəz filialının ATM-i", "address": "Azərbaycan pr. 3, Bakı"},
    {"name": "Mərdəkan filialının ATM-i", "address": "Xəzər r-nu, Mərdəkan qəsəbəsinin girişi, Bakı"},
    {"name": "Nəsimi filialındakı ATM", "address": "A. Məhərrəmov küçəsi, 34A, Bakı"},
    {"name": "Neftçilər filialının ATM-i", "address": "Q. Qarayev, 59, Bakı"},
    {"name": "Otoplaza filialının ATM-i", "address": "Z. Bünyadov 118, Bakı"},
    {"name": "Səməd Vurğun filialının ATM-i", "address": "AZ 1010, Nəsimi rayonu, Puşkin küç., 12/14, Bakı"},
    {"name": "Yasamal filialının ATM-i", "address": "N. Hikmət küç., 32C, Bakı"},
    {"name": "Nərimanov filialının ATM-i", "address": "Ağa Nemətulla 76H, Nərimanov, Bakı"},
    {"name": "Xırdalan filialının ATM-i", "address": "Xırdalan ş., H. Əliyev küç. 39, Xırdalan Mədəniyyət evi ilə üzbəüz"},
    {"name": "Gəncə filialının ATM-i", "address": "Cavadxan 38, Gəncə"},
    {"name": "Yeni Gəncə filialının ATM-i", "address": "Kəpəz rayonu, N. Nərimanov pr-ti, 42C, Gəncə"},
    {"name": "Lənkəran filialının ATM-i", "address": "H. Aslanov 1, Lənkəran"},
    {"name": "Sumqayıt filialının ATM-i", "address": "Sumqayıt ş., Z. Hacıyev küç. 183"},
    {"name": "Şəki filialının ATM-i", "address": "Məmməd Əmin Rəsulzadə 149B, Şəki"},
    {"name": "Şirvan filialının ATM-i", "address": "M. Rəsulzadə küç. 33, Şirvan"},
    {"name": "Xaçmaz filialının ATM-i", "address": "H. Əliyev küç. 30, Xaçmaz"},
    {"name": "Park Bulvar ATM", "address": "Ticarət mərkəzi, Neftçilər pr., Dənizkənarı Milli Park, Bakı"},
    {"name": "28 Mall ATM", "address": "\"28 mall\" ticarət mərkəzi, Azadlıq 27, Nəsimi, Bakı"},
    {"name": "Favorit Market ATM", "address": "Mir Cəlal 59, Binəqədi, Bakı"},
    {"name": "Baku Electronics ATM (Ə.Naxçıvani)", "address": "Əcəmi Naxçıvani 3066, Binəqədi, Bakı"},
    {"name": "Improtex Travel ATM", "address": "Nizami 63, Nəsimi, Bakı"},
    {"name": "Demirchi Tower ATM", "address": "Xocalı pr-ti 37, Xətai, Bakı"},
    {"name": "Memarlıq Universiteti ATM", "address": "Ayna Sultanova 11, Yasamal, Bakı"},
    {"name": "Nizami Mall ATM", "address": "Şıxəli Qurbanov, Yasamal, Bakı"},
    {"name": "Qəbələ Futbol Akademiyası ATM", "address": "Qəbələ rayonu, 28 May küç."},
    {"name": "EmbaFinans ATM", "address": "Akim Abbasov 73E, Yasamal, Bakı"},
    {"name": "İnşaatçılar Filialı ATM", "address": "Abbas Mirzə Şərifzadə küçəsi, 560B"},
    {"name": "Baku Tobacco ATM", "address": "1-ci Köndələn 21, Nizami, Bakı"},
    {"name": "Metro Park TM ATM", "address": "Təbriz küç. 44, Bakı"}
]


def fetch_service_network_data(url: str) -> Dict:
    """
    Fetch service network data from Bank of Baku API

    Args:
        url: API endpoint URL

    Returns:
        API response dictionary
    """
    print(f"Fetching data from {url}...")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'https://www.bankofbaku.com',
        'Referer': 'https://www.bankofbaku.com/'
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    data = response.json()
    print(f"Successfully fetched data")

    return data


def clean_html_title(html_str: str) -> str:
    """
    Extract text from HTML table in title field

    Args:
        html_str: HTML string containing title

    Returns:
        Clean text without HTML tags
    """
    if not html_str:
        return ""

    # Simple HTML tag removal
    # Remove HTML tags
    clean = re.sub(r'<[^>]+>', '', html_str)
    # Clean up whitespace
    clean = ' '.join(clean.split())
    return clean.strip()


def extract_atm_locations(data: Dict) -> List[Dict]:
    """
    Extract ATM locations from API response

    Args:
        data: API response dictionary

    Returns:
        List of ATM location dictionaries
    """
    atm_locations = []

    payload = data.get('payload', {})

    # Navigate through the structure: payload -> pages -> informationGroup -> listGroup
    pages = payload.get('pages', [])

    for page in pages:
        # Check if this is an ATM page
        if page.get('serviceNetworkType') == 'atm':
            information_groups = page.get('informationGroup', [])

            for info_group in information_groups:
                # Get listGroup array
                list_groups = info_group.get('listGroup', [])

                for list_group in list_groups:
                    # Get location at the group level
                    group_location_str = list_group.get('location', '')
                    lat, lon = None, None

                    if group_location_str:
                        try:
                            parts = group_location_str.split(',')
                            if len(parts) == 2:
                                lat = float(parts[0].strip())
                                lon = float(parts[1].strip())
                        except (ValueError, AttributeError):
                            pass

                    # Get lists array
                    lists = list_group.get('lists', [])

                    for item in lists:
                        # Filter for Azerbaijani language entries
                        if item.get('language') == 'az':
                            # Clean the HTML from title
                            raw_title = item.get('title', '')
                            clean_title = clean_html_title(raw_title)

                            atm_locations.append({
                                'title': clean_title,
                                'address': item.get('address'),
                                'service_names': item.get('serviceNames'),
                                'lat': lat,
                                'lon': lon,
                                'position_order': list_group.get('positionOrder')
                            })

    print(f"Extracted {len(atm_locations)} locations from API")
    return atm_locations


def normalize_string(s: str) -> str:
    """
    Normalize string for fuzzy matching by removing special characters

    Args:
        s: Input string

    Returns:
        Normalized string
    """
    if not s:
        return ""

    import html
    # Decode HTML entities first
    s = html.unescape(s)

    # Remove quotes and special characters
    s = s.replace('«', '').replace('»', '').replace('"', '').replace("'", '').replace('&laquo;', '').replace('&raquo;', '')

    # Remove punctuation for better matching
    s = s.replace('.', '').replace(',', '').replace('-', ' ').replace('(', '').replace(')', '')

    # Normalize spaces
    s = ' '.join(s.split())

    # Convert to lowercase
    s = s.lower().strip()

    # Normalize Turkish/Azeri characters (ı to i)
    s = s.replace('ı', 'i')

    return s


def match_atms(atm_data: List[Dict], api_locations: List[Dict]) -> List[Dict]:
    """
    Match predefined ATM data with API locations

    Args:
        atm_data: List of ATM dictionaries with name and address
        api_locations: List of locations from API

    Returns:
        List of matched ATM dictionaries
    """
    matched_atms = []

    print("\nMatching ATMs...")

    for atm in atm_data:
        atm_name = atm.get('name', '')
        atm_address = atm.get('address', '')
        normalized_name = normalize_string(atm_name)
        normalized_address = normalize_string(atm_address)

        # Try to find a match in API locations
        matched = False
        for location in api_locations:
            location_title = normalize_string(location.get('title', ''))
            location_address = normalize_string(location.get('address', ''))

            # Check if the normalized titles match (fuzzy) or addresses match
            if (location_title and (normalized_name in location_title or location_title in normalized_name)) or \
               (location_address and normalized_address and (normalized_address in location_address or location_address in normalized_address)):
                matched_atms.append({
                    'name': atm_name,
                    'predefined_address': atm_address,
                    'api_title': location.get('title'),
                    'api_address': location.get('address'),
                    'service_names': location.get('service_names'),
                    'lat': location.get('lat'),
                    'lon': location.get('lon'),
                    'position_order': location.get('position_order'),
                    'matched': True
                })
                matched = True
                print(f"✓ Matched: {atm_name}")
                break

        if not matched:
            # Add ATM without coordinates if not found
            matched_atms.append({
                'name': atm_name,
                'predefined_address': atm_address,
                'api_title': None,
                'api_address': None,
                'service_names': None,
                'lat': None,
                'lon': None,
                'position_order': None,
                'matched': False
            })
            print(f"✗ Not matched: {atm_name}")

    matched_count = sum(1 for atm in matched_atms if atm['matched'])
    print(f"\nMatched {matched_count}/{len(atm_data)} ATMs")

    return matched_atms


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

    # Define fieldnames
    fieldnames = ['name', 'predefined_address', 'api_title', 'api_address', 'service_names', 'lat', 'lon', 'position_order', 'matched']

    print(f"\nWriting {len(data)} records to {output_path}...")

    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    print(f"Successfully saved data to {output_path}")


def save_basic_data(atm_data: List[Dict], output_path: str):
    """
    Save basic ATM data to CSV without API matching

    Args:
        atm_data: List of ATM dictionaries
        output_path: Path to output CSV file
    """
    if not atm_data:
        print("No data to save")
        return

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Define fieldnames
    fieldnames = ['name', 'address']

    print(f"Writing {len(atm_data)} records to {output_path}...")

    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(atm_data)

    print(f"Successfully saved data to {output_path}")


def main():
    """Main function"""
    # API endpoint
    api_url = "https://site-api.bankofbaku.com/categories/serviceNetwork/individual"

    # Output path
    output_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'data',
        'bob_atms.csv'
    )

    try:
        # Try to fetch data from API
        try:
            api_data = fetch_service_network_data(api_url)
            api_locations = extract_atm_locations(api_data)

            if len(api_locations) > 0:
                # If API returns data, match and save
                matched_atms = match_atms(ATM_DATA, api_locations)
                save_to_csv(matched_atms, output_path)
                print(f"\nDone!")
                print(f"Total ATMs: {len(matched_atms)}")
            else:
                # If API returns no data, save basic data
                print("\nAPI returned no location data. Saving predefined data...")
                save_basic_data(ATM_DATA, output_path)
                print("\nDone!")
                print(f"Total ATMs: {len(ATM_DATA)}")
        except Exception as api_error:
            print(f"\nAPI error: {api_error}")
            print("Saving predefined data...")
            save_basic_data(ATM_DATA, output_path)
            print("\nDone!")
            print(f"Total ATMs: {len(ATM_DATA)}")

    except Exception as e:
        print(f"Error: {e}")
        raise


if __name__ == "__main__":
    main()
