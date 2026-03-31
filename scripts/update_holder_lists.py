"""
Update holder_lists from Helius CSV data and recompute HHI from Dune execution results.
Run: python3 scripts/update_holder_lists.py
"""
import pandas as pd
import numpy as np
from pathlib import Path
import os

PROJECT_DIR = Path(__file__).parent.parent
HOLDER_DIR = PROJECT_DIR / "holder_lists"
DATA_DIR = PROJECT_DIR / "data"

# === Step 1: Convert Helius CSVs to holder_lists format ===
HELIUS_TOKENS = {
    "META": "METAwkXcqyXKy1AtsSgJ8JiUHwGCafnZL38n3vYmeta",
    "DRIFT": "DriFtupJYLTosbwoN8koMbEYSx54aFAVLddWsbksjwg7",
    "GRASS": "Grass7B4RdKfBCjTKgSqnXkqjwiGvQyFbuSCUJr3XXjs",
    "W": "85VBFQZC9TZkfaptBWjvUw7YbZjy52A6mjtPGjstQAmQ",
}

# Token decimals for converting raw balances
DECIMALS = {
    "META": 9,  # Solana SPL
    "DRIFT": 6,
    "GRASS": 9,
    "W": 6,
}

def convert_helius_to_holder_list(token: str):
    """Convert Helius holder data to standard holder_lists format."""
    helius_file = DATA_DIR / f"holders_helius_{token}.csv"
    if not helius_file.exists():
        print(f"  SKIP {token}: no Helius file at {helius_file}")
        return

    df = pd.read_csv(helius_file)
    print(f"  {token}: {len(df)} holders from Helius")

    # Helius data has: owner, balance (raw integer amounts)
    df = df.rename(columns={"owner": "address"})

    # Convert from raw integer to human-readable
    decimals = DECIMALS.get(token, 9)
    df["balance"] = df["balance"].astype(float) / (10 ** decimals)

    # Remove zero balances
    df = df[df["balance"] > 0].copy()

    # Sort by balance descending, take top 1000
    df = df.sort_values("balance", ascending=False).head(1000).reset_index(drop=True)

    # Compute rank and share
    df["rank"] = range(1, len(df) + 1)
    total = df["balance"].sum()
    df["share"] = df["balance"] / total
    df["token"] = token

    # Save
    output_file = HOLDER_DIR / f"holders_{token}.csv"
    df[["token", "address", "balance", "rank", "share"]].to_csv(output_file, index=False)

    # Quick HHI
    hhi = (df["share"] ** 2).sum()
    top1 = df["share"].iloc[0] * 100
    print(f"    Saved {len(df)} rows. HHI={hhi:.4f}, Top1={top1:.1f}%, Total={total:.0f}")


def main():
    print("=== Converting Helius data to holder_lists ===")
    for token in HELIUS_TOKENS:
        convert_helius_to_holder_list(token)

    print("\n=== Done ===")
    print("Now run: python3 scripts/compute_concentration.py")


if __name__ == "__main__":
    main()
