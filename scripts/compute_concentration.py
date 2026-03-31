"""
B2 Governance Concentration Metrics
Computes HHI, Gini, Top-1/5/10 from holder CSVs.
"""

import pandas as pd
import numpy as np
import json
import os
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent
HOLDER_DIR = PROJECT_DIR / "holder_lists"
OUTPUT_CSV = PROJECT_DIR / "governance_concentration_april2026.csv"
REGISTRY_PATH = PROJECT_DIR / "token_registry.json"

# Protocol-controlled addresses to exclude from governance concentration analysis.
# These are staking contracts, bridges, vaults, vesting locks, or minting contracts
# that hold tokens on behalf of users or for protocol operations — NOT individual holders.
# Exclusion verified via Blockscout contract labels (2026-03-30).
PROTOCOL_EXCLUSIONS = {
    "LPT": [
        "0xc20de37170b45774e6cd3d2304017fc962f27252",  # Livepeer Minter (Arbitrum) — inflation reserve
        "0xf977814e90da44bfa03b6295a0616a897441acec",  # Binance 8 exchange custodian
    ],
    "GMX": [
        "0x908c4d94d34924765f1edc22a1dd098397c59dd4",  # sGMX RewardTracker — staking contract
    ],
    "RPL": [
        "0x3bdc69c4e5e13e52a65f5583c23efb9636b469d6",  # RocketVault — Rocket Pool protocol treasury
    ],
    "ENS": [
        "0xd7a029db2585553978190db5e85ec724aa4df23f",  # TokenLock — vesting contract
    ],
    "LDO": [
        "0xf977814e90da44bfa03b6295a0616a897441acec",  # Binance 8 — exchange custodian
        "0x3e40d73eb977dc6a537af587d48316fee66e9c8c",  # Lido DAO Aragon Agent — protocol treasury (AppProxyUpgradeable → Agent)
        "0x945755de7eac99008c8c57bda96772d50872168b",  # GnosisSafe — Lido founding-period vesting multisig (created Dec 2020 by Lido deployer)
        "0x695c388153bea0fbe3e1c049c149bad3bc917740",  # GnosisSafe — Lido founding-period vesting multisig
        "0xa2dfc431297aee387c05beef507e5335e684fbcd",  # GnosisSafe — Lido founding-period vesting multisig
        "0x1597d19659f3de52abd475f7d2314dcca29359bd",  # GnosisSafe — Lido founding-period vesting multisig
        "0xb8d83908aab38a159f3da47a59d84db8e1838712",  # GnosisSafe — Lido founding-period vesting multisig
        "0x611f7bf868a6212f871e89f7e44684045ddfb09d",  # OKX Cold Wallet — exchange custodian
        "0x28c6c06298d514db089934071355e5743bf21d60",  # Binance 14 — exchange custodian
        "0xa9d1e08c7793af67e9d92fe308d5697fb81d3e43",  # Coinbase — exchange custodian
        "0xffffffffffffffffffffffffffffffffffffdead",  # burn-like address
    ],
    "WXM": [
        "0x93f1a412050bab0c317844361e4cc801ed5aca72",  # Unverified Arbitrum contract, likely WXM treasury/vesting
    ],
    "DIMO": [
        "0xc97bf974d6d4bab6e0f7641b7b37ec5b70922ce5",  # Unverified Polygon contract, likely DIMO Foundation
    ],
    "POL": [
        "0x5e3ef299fddf15eaa0432e6e66473ace8c13d908",  # Polygon StakeManagerProxy — PoS validator staking contract
        "0x401f6c983ea34274ec46f84d70b31c151321188b",  # Polygon DepositManagerProxy — Plasma Bridge contract
    ],
    "MPL_SYRUP": [
        "0x9c9499edd0cd2dcbc3c9dd5070baf54777ad8f2c",  # Syrup Migrator — MPL→SYRUP migration contract
        "0xc7e8b36e0766d9b04c93de68a9d47dd11f260b45",  # xMPL/stSYRUP — staked SYRUP vault (ERC-4626)
    ],
    "ZRO": [
        "0x8f6449530606a9efddac42e05612427ddeba449c",  # GnosisSafeProxy — LayerZero Foundation treasury multisig (created Jun 2024)
        "0x744dbc48d11415ec5cb2f78609dea5e1e738da24",  # GnosisSafeProxy — LayerZero Foundation/team multisig (created Jun 2024)
    ],
    "AXL": [
        "0xd2ff2d432a0078672cf4f9e2e97858a33cbdeebc",  # Unverified EOA — likely Axelar Foundation treasury (holds 43% of Ethereum axlAXL)
        "0x54d1774631980b22c85f13bfaf2f45291b22cbf9",  # Bithumb 148 — exchange custodian
        "0x377b8ce04761754e8ac153b47805a9cf6b190873",  # Upbit 59 — exchange custodian
    ],
    "MOR": [
        "0x000000000000000000000000000000000000dead",  # Burn address — burned MOR tokens
        "0xc0ed68f163d44b6e9985f0041fdf6f67c6bcff3f",  # ERC1967Proxy "BuildersV4" — Morpheus builders distribution contract
        "0xe5cf22ee4988d54141b77050967e1052bd9c7f7a",  # UniswapV3Pool — liquidity pool (not governance holder)
        "0xb1972e86b3380fd69dcb395f98d39fbf1a5f305a",  # Unverified Arbitrum contract — same balance as burn address, likely protocol distribution/lockup
    ],
    "W": [
        "7S7r1mnB9LsEywHnWK9WnLDP9tnmo69JT4TW3kHPoznq",  # Wormhole Foundation/DAO treasury — holds 49% of top-1000 W (unverified, likely vesting)
        "8X6MEdM5Rf2zZLjAbE3bwspNAn9aaQaodJ28mT14QR8b",  # Wormhole vesting/treasury — holds only W tokens (22%), consistent with lockup account
    ],
    # RENDER: Wormhole bridge exclusion is handled upstream in merge_multichain.py
    "META": [
        "CUPoiqkK4hxyCiJcLC4yE9AtJP1MoV1vFV2vx3jqwWeS",  # Futarchy conditional vault — holds META in escrow during live proposal (confirmed via tx analysis 2026-03-30)
    ],
}


def compute_concentration(holders_df: pd.DataFrame, known_total: float = None) -> dict:
    """
    Input: DataFrame with columns ['address', 'balance']
           known_total: if provided, use this as denominator for shares
                        (corrects for truncated holder lists where only top-N are available)
    Output: dict with HHI, Gini, Top1/5/10, N
    """
    df = holders_df.sort_values('balance', ascending=False).head(1000).copy()
    df = df[df['balance'] > 0].copy()
    total = df['balance'].sum()
    if total == 0 or len(df) == 0:
        return None

    # Use known_total if provided (corrects for truncated holder lists)
    share_denom = known_total if known_total and known_total > total else total
    df['share'] = df['balance'] / share_denom
    n = len(df)

    # HHI: sum of squared shares
    hhi = (df['share'] ** 2).sum()

    # Gini: standard formula using sorted ascending shares
    df_asc = df.sort_values('balance', ascending=True).reset_index(drop=True)
    df_asc['rank_asc'] = range(1, n + 1)
    gini = 1.0 - (2.0 / n) * (df_asc['rank_asc'] * df_asc['share']).sum() / df_asc['share'].sum() + 1.0 / n

    # Alternative Gini (more standard):
    # Using the relative mean absolute difference
    shares = df['share'].values
    abs_diffs = np.abs(shares[:, None] - shares[None, :]).sum()
    gini_alt = abs_diffs / (2 * n * shares.sum())

    # Top-N shares
    df_desc = df.sort_values('balance', ascending=False).reset_index(drop=True)
    top1 = df_desc['share'].iloc[0]
    top5 = df_desc['share'].iloc[:5].sum()
    top10 = df_desc['share'].iloc[:10].sum()

    return {
        'hhi': round(float(hhi), 6),
        'gini': round(float(gini_alt), 4),
        'top1_pct': round(float(top1 * 100), 2),
        'top5_pct': round(float(top5 * 100), 2),
        'top10_pct': round(float(top10 * 100), 2),
        'n_holders': n,
        'total_balance_top1000': round(float(total), 2),
    }


def load_registry() -> list:
    with open(REGISTRY_PATH) as f:
        return json.load(f)


def load_total_supply_corrections() -> dict:
    """Load known total supply corrections for truncated holder lists."""
    path = HOLDER_DIR / "total_supply_corrections.json"
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return {}


def process_all():
    registry = load_registry()
    results = []
    total_corrections = load_total_supply_corrections()

    for token in registry:
        symbol = token['symbol']
        holder_file = HOLDER_DIR / f"holders_{symbol}.csv"

        if not holder_file.exists():
            print(f"  SKIP {symbol}: no holder file at {holder_file}")
            continue

        print(f"  Processing {symbol}...")
        df = pd.read_csv(holder_file)

        # Normalize column names
        col_map = {}
        for c in df.columns:
            cl = c.lower().strip()
            if cl in ('address', 'wallet', 'account', 'holder'):
                col_map[c] = 'address'
            elif cl in ('balance', 'amount', 'token_balance', 'quantity'):
                col_map[c] = 'balance'
        df = df.rename(columns=col_map)

        if 'address' not in df.columns or 'balance' not in df.columns:
            print(f"  ERROR {symbol}: missing address/balance columns. Found: {list(df.columns)}")
            continue

        df['balance'] = pd.to_numeric(df['balance'], errors='coerce')
        df = df.dropna(subset=['balance'])
        df = df[df['balance'] > 0]

        # Exclude protocol-controlled addresses (staking contracts, bridges, vaults, etc.)
        exclusions = PROTOCOL_EXCLUSIONS.get(symbol, [])
        if exclusions:
            excl_lower = [a.lower() for a in exclusions]
            before = len(df)
            df = df[~df['address'].str.lower().isin(excl_lower)]
            removed = before - len(df)
            if removed > 0:
                print(f"    Excluded {removed} protocol-controlled address(es) for {symbol}")

        # Use known total supply correction if available (for truncated Dune exports)
        known_total = total_corrections.get(symbol, None)
        if known_total:
            print(f"    Using total supply correction: {known_total:.0f}")

        metrics = compute_concentration(df, known_total=known_total)
        if metrics is None:
            print(f"  ERROR {symbol}: no valid balances")
            continue

        row = {
            'protocol': token['name'],
            'token': symbol,
            'category': token['category'],
            'chain': token['chain'],
            'measurement_type': 'governance_token',
            'launch_year': token['launch_year'],
            'governance_model': token['governance_model'],
            'distribution_type': token['distribution_type'],
            **metrics,
            'source': 'Dune' if token['dune_table'] != 'N/A' else 'API',
            'query_id': '',
            'notes': token['notes'],
        }
        results.append(row)
        print(f"    HHI={metrics['hhi']:.4f} Gini={metrics['gini']:.2f} Top10={metrics['top10_pct']:.1f}%")

    results_df = pd.DataFrame(results)
    results_df.to_csv(OUTPUT_CSV, index=False)
    print(f"\nSaved {len(results_df)} protocols to {OUTPUT_CSV}")
    return results_df


def validate(results_df: pd.DataFrame):
    """Run validation checks per Step 8."""
    print("\n=== VALIDATION ===")
    print(f"Total protocols: {len(results_df)}")
    for cat in ['DePIN', 'DeFi', 'L1_L2_Infra', 'Social_Dead']:
        n = len(results_df[results_df.category == cat])
        print(f"  {cat}: {n}")

    # HHI range
    assert results_df.hhi.min() >= 0, "HHI below 0"
    assert results_df.hhi.max() <= 1, "HHI above 1"
    print(f"HHI range: {results_df.hhi.min():.4f} to {results_df.hhi.max():.4f}")

    # Gini range
    assert results_df.gini.min() >= 0, "Gini below 0"
    assert results_df.gini.max() <= 1, "Gini above 1"
    print(f"Gini range: {results_df.gini.min():.4f} to {results_df.gini.max():.4f}")

    # Missing values
    for col in ['hhi', 'gini', 'top1_pct', 'n_holders']:
        missing = results_df[col].isna().sum()
        if missing > 0:
            print(f"  WARNING: {col}: {missing} missing")

    # DePIN vs DeFi
    depin = results_df[results_df.category == 'DePIN']['hhi']
    defi = results_df[results_df.category == 'DeFi']['hhi']
    if len(depin) > 0 and len(defi) > 0:
        print(f"\nDePIN mean HHI: {depin.mean():.4f} (N={len(depin)})")
        print(f"DeFi mean HHI: {defi.mean():.4f} (N={len(defi)})")
        if defi.mean() > 0:
            print(f"Ratio: {depin.mean() / defi.mean():.1f}x")

    print("\nValidation PASSED")


if __name__ == "__main__":
    results = process_all()
    if len(results) > 0:
        validate(results)
