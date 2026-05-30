#!/usr/bin/env python3
"""Refined PCA exclusion for DOT top-1000 holders.

Cross-references Subscan AssetHub holder data with parallel-session Polkawatch
operator registry + funding-cluster identification to surface institutional
staking-provider warm wallets (Class 3 PCAs) beyond the pattern-matched
Treasury/pallet accounts (Class 2 PCAs). Adds Class 5 (CEX custody) for
Binance cluster confirmed via SubSquare governance-forum ground-truth + on-chain
extrinsic verification (Substrate-analog CEX-cluster finding 2026-05-27).

PCA classification per B2 §3.8 five-class typology:
- Class 1: burns (Polkadot has no burn convention; zero on-chain)
- Class 2: Treasury/pallet (modlpy/* pattern; caught by string match)
- Class 3: Institutional staking-provider operator_id wallets (Polkawatch registry)
- Class 4: Bridge custody (XCM channels; cross-chain bridge custody;
  modlpy/xcmch pattern caught at Class 2 since it's pallet-managed)
- Class 5: CEX custody (Binance cluster confirmed via SubSquare hydration-forum
  zengsw testimony + extrinsic 0x51bc6c... verification 2026-05-27;
  intra-AssetHub cold + hot + staking architecture)
"""
import csv
import json
from pathlib import Path

# Load Subscan AssetHub holders (top-1000)
holders = []
with open("/tmp/dot_assethub_holders.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        holders.append({
            "rank": int(row["rank"]),
            "address": row["address"],
            "balance": float(row["balance"]),
            "reserved": float(row["reserved"]),
            "lock": float(row["lock"]),
            "display": row["display"],
        })

# Load Polkawatch validator->operator mapping
with open("data/raw/b2_phase4_minibatch_2026-05-27/expansion_artifacts/pw_full_mapping.json") as f:
    pw = json.load(f)
v2o = pw.get("validator_to_operator", {})

# Build operator_id -> {name, validator_count} map
operator_ids = {}  # operator_id (warm wallet address) -> operator_name
for v_addr, info in v2o.items():
    op_id = info.get("operator_id")
    op_name = info.get("operator_name", "")
    if op_id:
        if op_id not in operator_ids:
            operator_ids[op_id] = {"name": op_name, "n_validators": 0}
        operator_ids[op_id]["n_validators"] += 1

print(f"=== Polkawatch operators ===")
print(f"Total operator_ids: {len(operator_ids)}")

# Load funding clusters (multi-funder top addresses)
with open("data/raw/b2_phase4_minibatch_2026-05-27/expansion_artifacts/dot_funding_clusters.json") as f:
    funding = json.load(f)
top_funders = funding.get("top_funders", [])
funder_addrs = {f["funder"]: f for f in top_funders}
print(f"Multi-funder addresses: {len(funder_addrs)}")

# === Class 5 CEX cluster registry (Binance; ground-truth verified 2026-05-27) ===
# Evidence: SubSquare hydration governance forum post by user zengsw at
# https://hydration.subsquare.io/posts/230 documenting Binance auto-routing
# through hot wallet 13vg3M... within 5 min after deposit. On-chain extrinsic
# 0x51bc6c61d67afa916163b22653750537554005b2448a19728bed52528f4eb186 (block
# 8156083; balances.transfer_keep_alive FROM 13vg3M... TO Jose's test address
# for exact random amount 1.355049 DOT) verifies the auto-rotation pattern.
#
# Cluster construction: 16ZL8y... (top-1 cold; 94.1M; 5 extrinsics; sent only
# 8M+4M = 12M DOT ever, both to confirmed-Binance addresses) + 13vg3M... (hot;
# confirmed-Binance; 17.0M; 66,628 extrinsics; small-value rotation pattern)
# + 12YfMj... (staking; 14.0M; 2 extrinsics; received 4M from cold; 100%
# bonded; same-cluster signature: only inbound DOT ever was from confirmed
# cluster member 16ZL8y...).
CEX_CLUSTER_BINANCE = {
    "16ZL8yLyXv3V3L3z9ofR1ovFLziyXaN1DPq4yffMAZ9czzBD": "cold-storage; 5 extrinsics; only outbound 12M DOT to confirmed Binance cluster members 13vg3M (8M) + 12YfMj (4M)",
    "13vg3Mrxm3GL9eXxLsGgLYRueiwFCiMbkdHBL4ZN5aob5D4N": "Binance hot wallet (CONFIRMED via SubSquare hydration-forum zengsw + extrinsic 0x51bc6c... block 8156083 auto-rotation pattern)",
    "12YfMjjeRPVHpytGSgdHH5iWnybxxuBdLuhjSuuYmrPjFT2H": "staking position; 100% bonded; only inbound DOT ever was 4M from confirmed cluster member 16ZL8y... (top-1 cold)",
}
print(f"Class 5 Binance cluster: {len(CEX_CLUSTER_BINANCE)} addresses; ground-truth via SubSquare + extrinsic verification")
print()

# === Apply PCA classification ===

PALLET_PATTERNS = ("modlpy/", "modl/")

def classify(holder):
    """Return (is_pca, class_number, rationale)."""
    display = holder.get("display", "").strip()
    addr = holder["address"]

    # Class 5: CEX cluster (highest-priority; ground-truth verified)
    if addr in CEX_CLUSTER_BINANCE:
        return (True, 5, f"Binance cluster ({CEX_CLUSTER_BINANCE[addr]})")

    # Class 2: Treasury/pallet
    for p in PALLET_PATTERNS:
        if display.startswith(p):
            return (True, 2, f"pallet-managed account ({display})")
    if display.startswith("para:"):
        return (True, 3, f"parachain slot reserve ({display})")

    # Class 3: Polkawatch operator_id (institutional staking provider warm wallet)
    if addr in operator_ids:
        op = operator_ids[addr]
        return (True, 3, f"Polkawatch operator_id ({op['name']}; controls {op['n_validators']} validators)")

    # Class 3 sister: multi-funder top address (funds multiple validators; institutional)
    if addr in funder_addrs:
        f = funder_addrs[addr]
        return (True, 3, f"Multi-funder cluster (funds {f.get('validator_count', '?')} validators)")

    return (False, None, None)

n_by_class = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
total_pca_balance = 0
total_by_class = {1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0, 5: 0.0}
pca_rows = []
non_pca = []
for h in holders:
    is_pca, cls, rationale = classify(h)
    if is_pca:
        n_by_class[cls] += 1
        total_by_class[cls] += h["balance"]
        total_pca_balance += h["balance"]
        pca_rows.append((h, cls, rationale))
    else:
        non_pca.append(h)

print(f"=== Refined + Class 5 PCA classification (top-1000) ===")
print(f"Class 1 (burns):                         {n_by_class[1]} (Polkadot has no burn convention)")
print(f"Class 2 (Treasury/pallet):               {n_by_class[2]:>3} ({total_by_class[2]:>14,.0f} DOT)")
print(f"Class 3 (Polkawatch/multi-funder):       {n_by_class[3]:>3} ({total_by_class[3]:>14,.0f} DOT)")
print(f"Class 4 (bridge custody):                {n_by_class[4]} (no separate XCM addresses in top-1000; XCM-channel caught at Class 2)")
print(f"Class 5 (CEX custody Binance cluster):   {n_by_class[5]:>3} ({total_by_class[5]:>14,.0f} DOT)  <-- Substrate-analog CEX-cluster finding")
print(f"Total PCAs:                              {len(pca_rows)}")
print(f"Total PCA balance:                       {total_pca_balance:,.0f} DOT")
print()
print(f"PCAs identified (top 20 by balance):")
pca_rows.sort(key=lambda x: -x[0]["balance"])
print(f"{'rank':>4} {'class':>5} {'address':<48} {'balance':>14} rationale")
for h, cls, rationale in pca_rows[:20]:
    print(f"{h['rank']:>4} {cls:>5} {h['address']:<48} {h['balance']:>13,.0f} {rationale[:80]}")

# Post-exclusion HHI
non_pca.sort(key=lambda h: -h["balance"])
top_n = non_pca  # all remaining holders
total_post = sum(h["balance"] for h in top_n)
hhi_post = sum((h["balance"] / total_post) ** 2 for h in top_n)

print(f"\n=== Post-PCA-exclusion HHI (with Class 5 Binance cluster) ===")
print(f"Remaining non-PCA holders: {len(top_n)}")
print(f"Post-exclusion total: {total_post:,.0f} DOT")
print(f"Post-exclusion holder-HHI: {hhi_post:.4f}")
print(f"Top-1 (post-exclusion) share: {top_n[0]['balance']/total_post*100:.2f}%  ({top_n[0]['address']})")
print(f"Top-10 (post-exclusion) share: {sum(h['balance'] for h in top_n[:10])/total_post*100:.2f}%")
print(f"Top-100 (post-exclusion) share: {sum(h['balance'] for h in top_n[:100])/total_post*100:.2f}%")

print()
print(f"=== Cross-section placement (with Binance cluster excluded) ===")
print(f"DOT post-cluster-exclusion HHI {hhi_post:.4f}:")
if hhi_post < 0.008:
    print(f"  -> below Lido 0.008; tightest cross-section observation")
elif hhi_post < 0.010:
    print(f"  -> Lido 0.008 / Compound 0.009 / Optimism 0.009 peer group")
elif hhi_post < 0.014:
    print(f"  -> Uniswap 0.010 / Aave 0.013 peer group")

# Show top-20 remaining non-PCAs for review (potential additional CEX/institutional)
print(f"\n=== Top-20 remaining non-PCAs (potential additional Class 5/institutional) ===")
print(f"{'rank':>4} {'address':<50} {'balance':>14} share")
for h in top_n[:20]:
    share = h["balance"] / total_post * 100
    print(f"{h['rank']:>4} {h['address']:<50} {h['balance']:>13,.0f} {share:>5.2f}%")

# Write refined PCA list to CSV
out_path = "dot_pca_exclusions_2026-05-27.csv"
with open(out_path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["rank", "class", "address", "balance", "display", "rationale"])
    for h, cls, rationale in pca_rows:
        writer.writerow([h["rank"], cls, h["address"], h["balance"], h["display"], rationale])
print(f"\nWrote PCA exclusions: {out_path}")
