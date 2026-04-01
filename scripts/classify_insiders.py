#!/usr/bin/env python3
"""
Insider Classification — Steps 1 & 2 (Automated Tiers)
Build post-exclusion top-10 holder lists and classify via cross-reference.
"""
import pandas as pd
import os
import glob

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ── Step 1: Build post-exclusion top-10 lists ──────────────────────────────

gov = pd.read_csv('governance_concentration_april2026.csv')
token_chain_map = dict(zip(gov['token'], gov['chain']))
gov_tokens = set(gov['token'])

exclusions = pd.read_csv('data/exclusions_log.csv')
excluded_addrs_by_token = {}
for token, group in exclusions.groupby('token'):
    excluded_addrs_by_token[token] = set(group['address'].str.lower())

# Map governance tokens to holder files
# Most are holders_{TOKEN}.csv; special cases handled explicitly
TOKEN_FILE_MAP = {t: f'holder_lists/holders_{t}.csv' for t in gov_tokens}
# Verify files exist and warn if not
for t, fp in list(TOKEN_FILE_MAP.items()):
    if not os.path.exists(fp):
        print(f"WARNING: No holder file for {t} at {fp}")
        del TOKEN_FILE_MAP[t]

results = []
for token, filepath in sorted(TOKEN_FILE_MAP.items()):
    holders = pd.read_csv(filepath)

    # Add token column if missing
    if 'token' not in holders.columns:
        holders['token'] = token

    # Normalize address column to lowercase
    holders['address'] = holders['address'].str.lower()

    # Compute share if missing
    if 'share' not in holders.columns:
        total = holders['balance'].sum()
        holders['share'] = holders['balance'] / total if total > 0 else 0

    # Remove excluded addresses
    excluded = excluded_addrs_by_token.get(token, set())
    clean = holders[~holders['address'].isin(excluded)].copy()
    clean = clean.sort_values('balance', ascending=False).head(10)
    clean['post_exclusion_rank'] = range(1, len(clean) + 1)

    chain = token_chain_map.get(token, 'unknown')

    for _, row in clean.iterrows():
        results.append({
            'token': token,
            'chain': chain,
            'address': row['address'],
            'balance': row['balance'],
            'share': row['share'],
            'post_exclusion_rank': row['post_exclusion_rank'],
            'tier1_label': '',
            'tier2_label': '',
            'tier3_label': '',
            'final_classification': '',
            'classification_source': '',
            'confidence': '',
            'vesting_status': '',
            'notes': '',
        })

top10_df = pd.DataFrame(results)
print(f"Step 1: Built top-10 lists — {len(top10_df)} entries ({len(top10_df) // 10} protocols × 10)")

# Verify no excluded addresses leaked through
for token in excluded_addrs_by_token:
    if token not in TOKEN_FILE_MAP:
        continue
    token_rows = top10_df[top10_df['token'] == token]
    leaked = token_rows[token_rows['address'].isin(excluded_addrs_by_token[token])]
    if len(leaked) > 0:
        print(f"  ERROR: {len(leaked)} excluded addresses in {token} top-10!")

# ── Step 2: Tier 1 — Cross-reference known addresses ──────────────────────

# Build global excluded-address → label mapping
all_excluded_labels = dict(zip(
    exclusions['address'].str.lower(),
    exclusions['identity']
))

# Known exchange addresses (common across tokens)
KNOWN_EXCHANGES = {
    '0xf977814e90da44bfa03b6295a0616a897441acec': 'Binance 8',
    '0x28c6c06298d514db089934071355e5743bf21d60': 'Binance 14',
    '0x21a31ee1afc51d94c2efccaa2092ad1028285549': 'Binance 15',
    '0xdfd5293d8e347dfe59e90efd55b2956a1343963d': 'Binance 16',
    '0x56eddb7aa87536c09ccc2793473599fd21a8b17f': 'Binance 17',
    '0x503828976d22510aad0201ac7ec88293211d23da': 'Coinbase',
    '0xa9d1e08c7793af67e9d92fe308d5697fb81d3e43': 'Coinbase 10',
    '0x0d0707963952f2fba59dd06f2b425ace40b492fe': 'Gate.io',
    '0x1ab4973a48dc892cd9971ece8e01dcc7688f8f23': 'Kraken 4',
    '0x2910543af39aba0cd09dbb2d50200b3e800a63d2': 'Kraken 13',
    '0xbe0eb53f46cd790cd13851d5eff43d12404d33e8': 'Binance 7',
    '0x5a52e96bacdabb82fd05763e25335261b270efcb': 'Binance Hot',
    '0x835678a611b28684005a5e2233695fb6cbbb0007': 'OKX',
    '0x6cc5f688a315f3dc28a7781717a9a798a59fda7b': 'OKX 2',
    '0xa7efae728d2936e78bda97dc267687568dd593f3': 'OKX 3',
    '0x40ec5b33f54e0e8a33a975908c5ba1c14e5bbbdf': 'Polygon Bridge',
    '0xe92d1a43df510f82c66382592a047d288f85226f': 'WazirX',
}

for idx, row in top10_df.iterrows():
    addr = row['address']

    # Check 1: Is this address excluded for a DIFFERENT token?
    if addr in all_excluded_labels:
        label = all_excluded_labels[addr]
        top10_df.at[idx, 'tier1_label'] = f"Excluded elsewhere: {label}"
        label_lower = label.lower()
        if any(x in label_lower for x in ['exchange', 'binance', 'coinbase', 'kraken', 'okx', 'gate']):
            top10_df.at[idx, 'final_classification'] = 'exchange'
        elif any(x in label_lower for x in ['team', 'investor', 'founder', 'vest', 'foundation',
                                              'treasury', 'multisig', 'deployer', 'grant']):
            top10_df.at[idx, 'final_classification'] = 'insider'
        elif any(x in label_lower for x in ['bridge', 'escrow', 'gateway', 'locker', 'minter',
                                              'staking', 'comptroller', 'timelock', 'governor',
                                              'migrator', 'distributor', 'reservoir']):
            top10_df.at[idx, 'final_classification'] = 'protocol_contract'
        top10_df.at[idx, 'classification_source'] = 'tier1_exclusion_crossref'
        top10_df.at[idx, 'confidence'] = 'high'

    # Check 2: Known exchange addresses
    if not top10_df.at[idx, 'final_classification'] and addr in KNOWN_EXCHANGES:
        top10_df.at[idx, 'tier1_label'] = KNOWN_EXCHANGES[addr]
        top10_df.at[idx, 'final_classification'] = 'exchange'
        top10_df.at[idx, 'classification_source'] = 'tier1_known_exchange'
        top10_df.at[idx, 'confidence'] = 'high'

classified_t1 = len(top10_df[top10_df['final_classification'] != ''])
print(f"Step 2: Tier 1 classified {classified_t1} / {len(top10_df)} ({100*classified_t1/len(top10_df):.0f}%)")

# ── Save intermediate results ─────────────────────────────────────────────

top10_df.to_csv('data/insider_classification.csv', index=False)
print(f"\nSaved: data/insider_classification.csv")

# Summary by token
print(f"\n{'Token':<12} {'Chain':<16} {'Classified':<12} {'Remaining'}")
print("-" * 55)
for token in sorted(top10_df['token'].unique()):
    t = top10_df[top10_df['token'] == token]
    chain = t['chain'].iloc[0]
    n_done = len(t[t['final_classification'] != ''])
    n_left = 10 - n_done
    print(f"{token:<12} {chain:<16} {n_done:<12} {n_left}")

# List unclassified addresses for Tier 2
unclassified = top10_df[top10_df['final_classification'] == '']
evm_unclassified = unclassified[~unclassified['chain'].isin(['solana', 'filecoin_native', 'pokt_native'])]
non_evm = unclassified[unclassified['chain'].isin(['solana', 'filecoin_native', 'pokt_native'])]

print(f"\n=== TIER 2 QUEUE ===")
print(f"EVM addresses for Blockscout lookup: {len(evm_unclassified)}")
print(f"Non-EVM (straight to manual review): {len(non_evm)}")
print(f"Total unclassified: {len(unclassified)}")
