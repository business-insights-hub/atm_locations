#!/usr/bin/env python3
"""
Deduplicate Bank Respublika ATM data
Removes duplicate entries keeping the most complete/recent record
"""

import pandas as pd
import sys

# Read the original data
print("Reading br_atms.csv...")
df = pd.read_csv('data/br_atms.csv')
print(f"Original records: {len(df)}")

# Show duplicates
duplicates = df[df.duplicated(subset=['id'], keep=False)].sort_values('id')
if len(duplicates) > 0:
    print(f"\nFound {len(duplicates)} duplicate records based on ID:")
    print(duplicates[['id', 'title', 'type']].to_string())

# Remove duplicates - keep first occurrence
df_dedup = df.drop_duplicates(subset=['id'], keep='first')
print(f"\nAfter deduplication: {len(df_dedup)} records")
print(f"Removed {len(df) - len(df_dedup)} duplicate records")

# Count ATMs vs branches
atm_count = len(df_dedup[df_dedup['type'] == 'atm'])
branch_count = len(df_dedup[df_dedup['type'] == 'branch'])
print(f"\nFinal counts:")
print(f"  ATMs: {atm_count}")
print(f"  Branches: {branch_count}")
print(f"  Total: {len(df_dedup)}")

# Save deduplicated data
output_file = 'data/br_atms.csv'
df_dedup.to_csv(output_file, index=False)
print(f"\nSaved deduplicated data to {output_file}")

# Show some sample titles
print("\nSample ATM titles:")
for title in df_dedup[df_dedup['type'] == 'atm']['title'].head(10):
    print(f"  - {title}")
