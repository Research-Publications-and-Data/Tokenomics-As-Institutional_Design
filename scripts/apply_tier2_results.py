#!/usr/bin/env python3
"""
Apply Tier 2 Blockscout results to insider_classification.csv.
Reads a JSON file of Blockscout lookup results and updates the CSV.
Usage: python3 scripts/apply_tier2_results.py data/tier2_results.json
"""
import pandas as pd
import json
import sys
import os

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

results_file = sys.argv[1] if len(sys.argv) > 1 else 'data/tier2_results.json'

with open(results_file) as f:
    results = json.load(f)

df = pd.read_csv('data/insider_classification.csv')

# Ensure string columns are string type (not float from NaN)
str_cols = ['tier1_label', 'tier2_label', 'tier3_label', 'final_classification',
            'classification_source', 'confidence', 'vesting_status', 'notes']
for col in str_cols:
    if col in df.columns:
        df[col] = df[col].fillna('').astype(str)

updated = 0
for r in results:
    addr = r['address'].lower()
    name = r.get('name', '')
    is_contract = r.get('is_contract', False)
    tags = r.get('tags', [])
    classification = r.get('classification', 'unknown')
    notes = r.get('notes', '')

    if not name and not tags and classification == 'unknown':
        continue  # Nothing useful from Blockscout

    # Update all rows with this address (may appear for multiple tokens)
    mask = df['address'] == addr
    if not mask.any():
        continue

    label = name if name else ', '.join(tags) if tags else ''

    for idx in df[mask].index:
        if df.at[idx, 'final_classification'] != '':
            continue  # Already classified by Tier 1

        df.at[idx, 'tier2_label'] = label
        if classification != 'unknown':
            df.at[idx, 'final_classification'] = classification
            df.at[idx, 'classification_source'] = 'tier2_blockscout'
            df.at[idx, 'confidence'] = 'high' if name else 'medium'
        elif is_contract:
            df.at[idx, 'final_classification'] = 'contract'
            df.at[idx, 'classification_source'] = 'tier2_blockscout'
            df.at[idx, 'confidence'] = 'medium'

        if notes:
            df.at[idx, 'notes'] = notes
        updated += 1

df.to_csv('data/insider_classification.csv', index=False)

total = len(df)
classified = len(df[df['final_classification'].notna() & (df['final_classification'] != '')])
print(f"Applied {updated} updates from {len(results)} Blockscout results")
print(f"Total classified: {classified} / {total} ({100*classified/total:.0f}%)")
print(f"Remaining: {total - classified}")
