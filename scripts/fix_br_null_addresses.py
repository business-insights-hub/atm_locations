#!/usr/bin/env python3
"""
Fix Bank Respublika ATM records with null addresses
"""

import pandas as pd

# Read the Bank Respublika data
print("Reading br_atms.csv...")
df = pd.read_csv('data/br_atms.csv')
print(f"Total records: {len(df)}")

# Check for null/empty addresses in the 'info' field
null_addresses = df[df['info'].isna() | (df['info'] == '')]
print(f"\nFound {len(null_addresses)} records with null/empty addresses:")
print(null_addresses[['id', 'title', 'info', 'city_location']])

# Fix null addresses by using title + city location
for idx, row in null_addresses.iterrows():
    if pd.isna(row['info']) or row['info'] == '':
        # Create address from title and city_location
        address = f"{row['title']}, {row['city_location']}"
        df.at[idx, 'info'] = f"Address: {address}"
        print(f"\nFixed record {row['id']}:")
        print(f"  Title: {row['title']}")
        print(f"  New address: {address}")

# Save the updated file
df.to_csv('data/br_atms.csv', index=False)
print(f"\n✅ Saved updated br_atms.csv with {len(df)} records")

# Verify fix
updated_null = df[df['info'].isna() | (df['info'] == '')]
print(f"\nRemaining null addresses: {len(updated_null)}")
