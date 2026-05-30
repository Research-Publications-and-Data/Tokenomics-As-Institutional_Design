#!/usr/bin/env python3
"""Substrate-analog CEX-cluster sensitivity: three-scenario CEX-cluster exclusion band.

Computes the DOT post-PCA-exclusion HHI under three Class 5 inclusion scenarios:

  A. Refined Class 2+3 only (baseline; no Class 5)
  B. + Binance CONFIRMED cluster (3 addresses; ground-truth via SubSquare
     hydration-forum zengsw + extrinsic 0x51bc6c... block 8156083
     auto-rotation pattern verification)
  C-narrow. + Binance + rank-2 13Z7KjGn... STRONG-LIKELY-CEX
            (multi-depositor exchange-collection pattern + bidirectional
            cluster with 13fKwtY... at $15M+ cumulative)
            + rank-5 12ouvKS... POSSIBLE-CEX (pure cold-storage; zero
            extrinsics; migration-origin)

Scenario B is the recommended primary (hard ground-truth attribution).
Scenarios A and C-narrow bracket the methodology-completeness uncertainty.

NOT included in C-narrow per F4 downgrade (ranks 10/11/12 funded by
163egH5d... distributor; exact-amount recurring batches at same block is
staking-rewards-pallet batch payout signature, NOT CEX custody).
"""
import csv

# === Class 2 + Class 3 refined exclusion set (10 PCAs) ===
EXISTING_PCAS = {
    # Class 2 Treasury/pallet (5; modlpy/* pattern match)
    "13UVJyLnbVp9RBZYFwFGyDvVd1y27Tt8tkntv6Q7JVPhFsTB",  # modlpy/trsry; 23.2M DOT
    "13UVJyLnbVp9RBZYFwHYxaAqqaywnygJs1K8H73FXaR6esrd",  # modlpy/trsrybt$
    "13UVJyLnbVp9RBZYFwHYxa8HBg7kUjxSv9yjwwATVqdrarwV",  # modlpy/trsrybt
    "13UVJyLnbVp9x5XDyJv8g8r3UddNwBrdaH7AADCmw9XQWvYW",  # modlpy/xcmch
    "13UVJyLnbVp9RBZYFwHYxaFy9QiLRT82khytwSnqb3yanRjB",  # modlpy/trsrybt@
    # Class 3 institutional staking-provider (5; Polkawatch operator_id + multi-funder)
    "13KJ3t8w1CKMkXCmZ6s3VwdWo4h747kXE88ZNh6rCBTvojmM",  # pos.dog (38 validators)
    "13E7LXW3NGYAJGKugiEitKZ4XjR4MXBs4ZhE1bkwBAaAoBCn",  # multi-funder (2 validators)
    "15j4dg5GzsL1bw2U2AWgeyAk6QTxq43V7ZPbXdAmbVLjvDCK",  # multi-funder (3 validators)
    "1qnJN7FViy3HZaxZK9tGAA71zxHSBeUweirKqCaox4t8GT7",   # multi-funder (5 validators)
    "15UHvPeMjYLvMLqh6bWLxAP3MbqjjsMXFWToJKCijzGPM3p9",  # Novasama (4 validators)
}

# === Class 5 Binance CONFIRMED cluster (3 addresses) ===
# Ground-truth via SubSquare hydration governance forum + extrinsic verification
BINANCE_CLUSTER = {
    "16ZL8yLyXv3V3L3z9ofR1ovFLziyXaN1DPq4yffMAZ9czzBD",  # cold (94.1M)
    "13vg3Mrxm3GL9eXxLsGgLYRueiwFCiMbkdHBL4ZN5aob5D4N",  # hot CONFIRMED (17.0M)
    "12YfMjjeRPVHpytGSgdHH5iWnybxxuBdLuhjSuuYmrPjFT2H",  # staking (14.0M)
}

# === Class 5 LIKELY-CEX expansion (rank-2 + rank-5; non-Binance) ===
# Per top-20 non-PCA investigation (dot_top20_investigation_2026-05-27.md)
LIKELY_CEX_NARROW = {
    # rank-2 (40.3M; 31 extrinsics; 13 large inbounds from 8+ unique senders =
    # exchange deposit-collection pattern; 30 large outbounds with bidirectional
    # cluster signature with 13fKwtY... at $15M+ cumulative both directions)
    "13Z7KjGnzdAdMre9cqRwTZHR6F2p36gqBsaNmQwwosiPz8JT",
    # rank-5 (16.2M; ZERO extrinsics; zero large inbounds; migration-origin;
    # pure cold-storage signature; attribution-blocked without external evidence)
    "12ouvKSvKnXAdXFR5oCL1vXimWrkDWG3joMNw3ETupTRs1ab",
}

# Load top-1000 holders
holders = []
with open("/tmp/dot_assethub_holders.csv") as f:
    for row in csv.DictReader(f):
        holders.append({
            "rank": int(row["rank"]),
            "address": row["address"],
            "balance": float(row["balance"]),
        })


def compute_hhi(pca_set):
    """Return (n_remaining, total_remaining, hhi, top_1_addr, top_1_share)."""
    non_pca = [h for h in holders if h["address"] not in pca_set]
    total = sum(h["balance"] for h in non_pca)
    hhi = sum((h["balance"] / total) ** 2 for h in non_pca)
    non_pca.sort(key=lambda h: -h["balance"])
    top_1 = non_pca[0]
    return len(non_pca), total, hhi, top_1["address"], top_1["balance"] / total * 100


def classify(hhi):
    if hhi < 0.005:
        return "below all cross-section observations (extreme low-concentration)"
    elif hhi < 0.008:
        return "below Lido 0.008 (tightest in cross-section)"
    elif hhi < 0.010:
        return "Compound 0.009 / Optimism 0.009 / Uniswap 0.010 peer group"
    elif hhi < 0.014:
        return "Aave 0.013 / CRV 0.014 mid-range"
    return "high-concentration tail"


scenarios = [
    ("A", "refined Class 2+3 only", EXISTING_PCAS),
    ("B", "+ Binance CONFIRMED (primary)", EXISTING_PCAS | BINANCE_CLUSTER),
    ("C-narrow", "+ Binance + rank-2 + rank-5 LIKELY-CEX", EXISTING_PCAS | BINANCE_CLUSTER | LIKELY_CEX_NARROW),
]

print("=== Substrate-analog CEX-cluster sensitivity: three-scenario band ===\n")
print(f"{'Scenario':<12} {'PCAs':>4} {'Remaining':>9} {'Excluded(M)':>11} {'HHI':>8}  Cross-section placement")
print("-" * 105)
results = []
for name, label, pca_set in scenarios:
    n_rem, total_rem, hhi, top_1_addr, top_1_share = compute_hhi(pca_set)
    excluded_total = sum(h["balance"] for h in holders if h["address"] in pca_set)
    print(f"{name:<12} {len(pca_set):>4} {n_rem:>9} {excluded_total/1e6:>11.1f} {hhi:>8.4f}  {classify(hhi)}")
    results.append((name, label, hhi, n_rem, total_rem, excluded_total, top_1_addr, top_1_share))

print()
print("=== Sensitivity band summary ===")
print(f"Range: {results[2][2]:.4f} (C-narrow upper-bound exclusion) to {results[0][2]:.4f} (A lower-bound exclusion)")
range_pct = (results[0][2] - results[2][2]) / results[0][2] * 100
print(f"Width: {results[0][2] - results[2][2]:.4f} ({range_pct:.1f}% of upper value); reflects cross-architecture")
print(f"  CEX-attribution methodology gap on Substrate chains (vs EVM ~95% / Solana ~80%).")
print()
print(f"PRIMARY (recommended for paper): Scenario B = {results[1][2]:.4f}")
print(f"  Binance cluster has hard ground-truth attribution (SubSquare + on-chain extrinsic).")
print()
print(f"Per-scenario top-1 remaining holder:")
for name, label, hhi, n_rem, total_rem, excluded, top_1_addr, top_1_share in results:
    print(f"  {name}: {top_1_addr[:32]}... @ {top_1_share:.2f}%")

print()
print("=== Class 5 cluster compositions ===")
print(f"Binance CONFIRMED: 3 addresses; 125.1M DOT")
print(f"  16ZL8y... 94.1M (cold; 5 extrinsics; pre-migration origin)")
print(f"  13vg3M... 17.0M (hot CONFIRMED via SubSquare; 66,628 extrinsics)")
print(f"  12YfMj... 14.0M (staking; 100% bonded; received 4M from cluster cold)")
print()
likely_total = sum(h["balance"] for h in holders if h["address"] in LIKELY_CEX_NARROW)
print(f"LIKELY-CEX NARROW expansion: 2 addresses; {likely_total/1e6:.1f}M DOT")
print(f"  13Z7Kj... 40.3M (rank-2; multi-depositor + bidirectional $15M cluster with 13fKwtY...)")
print(f"  12ouvK... 16.2M (rank-5; pure cold-storage; zero extrinsics)")
print()
print("DOWNGRADED from Class 5 (per F4 in dot_top20_investigation_2026-05-27.md):")
print("  ranks 10/11/12 (12.1M + 12.1M + 11.9M; funded by 163egH5d... distributor)")
print("  exact-amount recurring batches at same block = staking-rewards-pallet payout pattern")
print("  classification: institutional staking infrastructure beneficiaries, NOT CEX custody")
