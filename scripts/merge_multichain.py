"""
Merge multi-chain/multi-token holder lists for:
1. MPL + SYRUP → Maple Finance (normalize SYRUP by /100)
2. RENDER (Solana) + RNDR (Ethereum) → Render Network
"""

import pandas as pd
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent
HOLDER_DIR = PROJECT_DIR / "holder_lists"


def merge_maple():
    """
    Merge MPL and SYRUP holder lists.
    SYRUP was 1 MPL = 100 SYRUP, so divide SYRUP balances by 100.
    Since addresses are on same chain (Ethereum), can merge by address.
    """
    mpl_path = HOLDER_DIR / "holders_MPL.csv"
    syrup_path = HOLDER_DIR / "holders_SYRUP.csv"
    out_path = HOLDER_DIR / "holders_MPL_SYRUP.csv"

    dfs = []
    if mpl_path.exists():
        mpl = pd.read_csv(mpl_path)
        mpl = mpl[['address', 'balance']].copy()
        mpl['balance'] = pd.to_numeric(mpl['balance'], errors='coerce')
        print(f"  MPL: {len(mpl)} holders, total {mpl['balance'].sum():,.0f} MPL")
        dfs.append(mpl)
    else:
        print(f"  WARNING: {mpl_path} not found")

    if syrup_path.exists():
        syrup = pd.read_csv(syrup_path)
        syrup = syrup[['address', 'balance']].copy()
        syrup['balance'] = pd.to_numeric(syrup['balance'], errors='coerce')
        # Normalize: 100 SYRUP = 1 MPL
        syrup['balance'] = syrup['balance'] / 100.0
        print(f"  SYRUP: {len(syrup)} holders, total {syrup['balance'].sum():,.0f} MPL-equivalent")
        dfs.append(syrup)
    else:
        print(f"  WARNING: {syrup_path} not found")

    if not dfs:
        print("  ERROR: No data to merge for Maple")
        return

    # Concatenate and group by address (same-chain merge)
    merged = pd.concat(dfs).groupby('address', as_index=False)['balance'].sum()
    merged = merged[merged['balance'] > 0].sort_values('balance', ascending=False).reset_index(drop=True)
    merged = merged.head(1000)

    merged.to_csv(out_path, index=False)
    print(f"  Merged Maple: {len(merged)} unique holders → {out_path}")


def merge_render():
    """
    Merge Solana RENDER and Ethereum RNDR holder lists.
    Both are 1:1 the same token on different chains.
    Addresses are different formats (base58 vs hex) so no address overlap.
    Simple concatenation of top holders.
    """
    sol_path = HOLDER_DIR / "holders_RENDER_SOL.csv"
    eth_path = HOLDER_DIR / "holders_RNDR_ETH.csv"
    out_path = HOLDER_DIR / "holders_RENDER.csv"

    dfs = []
    if sol_path.exists():
        sol = pd.read_csv(sol_path)
        sol = sol[['address', 'balance']].copy()
        sol['balance'] = pd.to_numeric(sol['balance'], errors='coerce')
        print(f"  RENDER (Solana): {len(sol)} holders, total {sol['balance'].sum():,.0f}")
        dfs.append(sol)
    else:
        print(f"  WARNING: {sol_path} not found")

    if eth_path.exists():
        eth = pd.read_csv(eth_path)
        eth = eth[['address', 'balance']].copy()
        eth['balance'] = pd.to_numeric(eth['balance'], errors='coerce')
        # Exclude Wormhole Token Bridge (0x3ee1...): holds ~86% of Ethereum RNDR because
        # RENDER migrated to Solana. The bridge is not a governance holder.
        wormhole_bridge = "0x3ee18b2214aff97000d974cf647e7c347e8fa585"
        eth = eth[eth['address'].str.lower() != wormhole_bridge.lower()]
        print(f"  RNDR (Ethereum, ex-Wormhole bridge): {len(eth)} holders, total {eth['balance'].sum():,.0f}")
        dfs.append(eth)
    else:
        print(f"  WARNING: {eth_path} not found")

    if not dfs:
        print("  ERROR: No data to merge for Render")
        return

    # Cross-chain: addresses are different formats, no overlap expected
    merged = pd.concat(dfs)
    merged = merged[merged['balance'] > 0].sort_values('balance', ascending=False).reset_index(drop=True)
    merged = merged.head(1000)

    merged.to_csv(out_path, index=False)
    print(f"  Merged Render: {len(merged)} holders → {out_path}")


def main():
    print("=== Merging multi-chain/multi-token holder lists ===\n")

    print("1. Maple Finance (MPL + SYRUP):")
    merge_maple()

    print("\n2. Render Network (RENDER + RNDR):")
    merge_render()

    print("\nDone. Run compute_concentration.py next.")


if __name__ == "__main__":
    main()
