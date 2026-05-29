#!/usr/bin/env python3
"""Merge the 6 new protocols into clone-A regression_data at N=52.
Backs up first. Verified HHIs (this cycle). FXS/SNX/GNO from S18 phase4 rows;
ALGO from holding-HHI json; DOT new holder-HHI row (0.0052, NOT the validator-set row);
TAO new principal-excluded row (0.0075). All measurement_type=governance_token so the
3-class sector contrast picks them up. Covariate-incomplete rows -> regression_ready=False
(per HALT-C; regression subset is a separate covariate-completion track).
"""
import csv, json, shutil, os
DATA = "/Users/zach/Tokenomics-As-Institutional_Design"
CSV = f"{DATA}/data/processed/regression_data_april2026.csv"
BAK = CSV + ".pre_n52_merge_2026-05-29"

def hhi_topN(bals):
    tot = sum(bals)
    s = sorted(bals, reverse=True)
    return (sum((b/tot)**2 for b in bals), tot,
            s[0]/tot*100, sum(s[:5])/tot*100, sum(s[:10])/tot*100)

# --- backup ---
if not os.path.exists(BAK):
    shutil.copy2(CSV, BAK)
    print(f"backup -> {BAK}")
rows = list(csv.DictReader(open(CSV)))
header = list(rows[0].keys())
existing = {r["protocol"] for r in rows}
print(f"clone-A before merge: {len(rows)} rows")

def blank_row():
    return {k: "" for k in header}

new_rows = []

# 1) FXS/SNX/GNO from the S18 phase4 regression rows (already schema-aligned)
phase4 = {r["protocol"]: r for r in csv.DictReader(
    open(f"{DATA}/b2/paper/supplements/phase4_minibatch_regression_rows_2026-05-27.csv"))}
for proto in ("Frax Finance", "Synthetix", "Gnosis"):
    src = phase4[proto]
    assert src["category"] == "DeFi" and src["measurement_type"] == "governance_token", proto
    r = blank_row()
    for k in header:
        r[k] = src.get(k, "")
    new_rows.append(r)

# 2) ALGO from holding-HHI json (clone B)
algo = json.load(open("/Users/zach/b2-governance-data/data/processed/ALGO_holding_hhi_2026-04-30.json"))
r = blank_row()
r.update({
    "protocol": "Algorand", "token": "ALGO", "category": "L1_L2_Infra", "chain": "algorand",
    "measurement_type": "governance_token", "hhi": f"{algo['hhi_post_pca']:.6f}",
    "gini": f"{algo['gini_post_pca']:.4f}", "top1_pct": f"{algo['top1_pct']*100:.2f}",
    "top5_pct": f"{algo['top5_pct']*100:.2f}", "top10_pct": f"{algo['top10_pct']*100:.2f}",
    "n_holders": str(algo["eligible_n_holders"]), "insider_pct": "25.0",
    "source": "AlgoNode indexer v2 top-1000 + behavioral-signature PCA (DEC-203 S21)",
    "query_id": "ALGO_holding_hhi_2026-04-30", "regression_ready": "False",
    "notes": "N=52 expansion (L1); post-PCA 36 excluded (31 Class2 treasury + 5 Class5 CEX); behavioral-signature classification (explorer labels unavailable); covariates partial -> not regression-ready",
})
new_rows.append(r)

# 3) DOT new holder-HHI row (0.0052 primary; NOT the validator-set 0.0017 row)
dot_excl = {x["address"] for x in csv.DictReader(open(
    f"/Users/zach/Tokenization_Systems_Website/research_content/papers/B2_governance_concentration/exhibits/dot_holder_hhi/dot_pca_exclusions_2026-05-27.csv"))}
dot_h = list(csv.DictReader(open(f"{DATA}/data/raw/holder_lists/DOT_holders.csv")))
dot_kept = [float(x["balance"]) for x in dot_h if x["address"] not in dot_excl]
_, _, d1, d5, d10 = hhi_topN(dot_kept)
r = blank_row()
r.update({
    "protocol": "Polkadot", "token": "DOT", "category": "L1_L2_Infra", "chain": "polkadot_assethub",
    "measurement_type": "governance_token", "hhi": "0.0052",
    "top1_pct": f"{d1:.2f}", "top5_pct": f"{d5:.2f}", "top10_pct": f"{d10:.2f}",
    "n_holders": str(len(dot_kept)), "insider_pct": "11.4",
    "source": "Subscan AssetHub top-1000 + dot_pca_refined (Binance-cluster Class5 ground-truth excluded)",
    "query_id": "dot_pca_refined_2026-05-27", "regression_ready": "False",
    "notes": "N=52 expansion (L1); holder-HHI post-PCA 0.0052 primary (Binance cluster excluded, SubSquare+extrinsic ground-truth) / 0.0093 sensitivity (Class5-rejected). DISTINCT from validator-set HHI 0.0017 (Phragmen, F-B2-29). covariates partial -> not regression-ready",
})
new_rows.append(r)

# 4) TAO new principal-excluded row (0.0075)
tao_h = list(csv.DictReader(open(f"{DATA}/data/raw/holder_lists/TAO_holders.csv")))
tao_reg = {x["coldkey"] for x in json.load(open("/Users/zach/b2-governance-data/data/processed/tao_exchange_coldkeys.json"))}
tao_kept = [float(x["balance"]) for x in tao_h if x["address"] not in tao_reg]
_, _, t1, t5, t10 = hhi_topN(tao_kept)
r = blank_row()
r.update({
    "protocol": "Bittensor", "token": "TAO", "category": "L1_L2_Infra", "chain": "bittensor",
    "measurement_type": "governance_token", "hhi": "0.007486",
    "top1_pct": f"{t1:.2f}", "top5_pct": f"{t5:.2f}", "top10_pct": f"{t10:.2f}",
    "n_holders": str(len(tao_kept)),
    "source": "TAOSTATS top-1000 coldkey + principal-exclusion PCA (registry CEX coldkeys)",
    "query_id": "tao_pca_2026-05-29", "regression_ready": "False",
    "notes": "N=52 expansion (L1); principal-excluded holder-HHI 0.0075 (6 registry CEX/bridge excluded, 12.6% top-1000) / 0.014 raw. Opentensor-foundation + subnet-staking long-tail deferred (Substrate CEX-attribution gap). category L1 primary; TAO-as-DePIN sensitivity reported. covariates absent -> not regression-ready",
})
new_rows.append(r)

# --- guard: no dup protocols ---
for r in new_rows:
    assert r["protocol"] not in existing, f"DUP {r['protocol']}"

# --- write ---
out = rows + new_rows
with open(CSV, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=header)
    w.writeheader(); w.writerows(out)
print(f"clone-A after merge: {len(out)} rows  (+{len(new_rows)})")
print("new rows:")
for r in new_rows:
    print(f"  {r['protocol']:14} {r['category']:12} {r['measurement_type']:16} hhi={r['hhi']:9} "
          f"top1={r['top1_pct']:6} reg_ready={r['regression_ready']}")
