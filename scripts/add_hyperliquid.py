"""
Add Hyperliquid (HYPE) as 36th protocol to B2 governance concentration dataset.
Verifies HHI, creates holder list, appends to all CSVs, reruns regressions.
"""

import csv
import json
import math
import os
import sys
from pathlib import Path

import numpy as np
from scipy import stats

PROJECT_DIR = Path(__file__).parent.parent
OUTPUT_DIR = Path.home() / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

HOLDER_CSV = Path.home() / "HYPE_2026-04-01T20_53_51.692Z.csv"

EXCLUDE_ADDRS = {
    "0xfefefefefefefefefefefefefefefefefefefefe",
    "0x2222222222222222222222222222222222222222",
    "0x43e9abea1910387c4292bca4b94de81462f8a251",
    "0xd57ecca444a9acb7208d286be439de12dd09de5d",
    "0x393d0b87ed38fc779fd9611144ae649ba6082109",
}

EXCLUSION_DETAILS = [
    ("0xfefefefefefefefefefefefefefefefefefefefe", "Assistance Fund (system address)", "CONFIRMED_DOCS", "Hyperliquid docs"),
    ("0x2222222222222222222222222222222222222222", "Burn address", "CONFIRMED_PATTERN", "Standard burn pattern"),
    ("0x43e9abea1910387c4292bca4b94de81462f8a251", "Community rewards treasury", "HIGH_ALLOCATION_MATH", "Allocation math verification"),
    ("0xd57ecca444a9acb7208d286be439de12dd09de5d", "Hyper Foundation treasury", "HIGH_ALLOCATION_MATH", "Allocation math verification"),
    ("0x393d0b87ed38fc779fd9611144ae649ba6082109", "Staking manager (system address)", "CONFIRMED_LABEL", "Hypurrscan label"),
]

progress = {}

def save_progress(step, data):
    progress[step] = data
    with open(OUTPUT_DIR / "progress.json", "w") as f:
        json.dump(progress, f, indent=2, default=str)


# ── Step 1: Load and verify HHI ──────────────────────────────────────────────
print("=" * 60)
print("STEP 1: Verify HHI from holder CSV")
print("=" * 60)

holders = []
with open(HOLDER_CSV, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        amount = float(row["amount"])
        if amount > 0:
            holders.append({"address": row["address"].lower(), "amount": amount})

print(f"  Loaded {len(holders)} holders with amount > 0")

# Compute raw HHI (before exclusions)
raw_total = sum(h["amount"] for h in holders)
raw_shares = [h["amount"] / raw_total for h in holders]
hhi_raw = sum(s ** 2 for s in raw_shares)
print(f"  Raw HHI (before exclusions): {hhi_raw:.6f}")

# Identify excluded amounts
excluded_amounts = {}
for h in holders:
    if h["address"] in EXCLUDE_ADDRS:
        excluded_amounts[h["address"]] = h["amount"]
total_excluded = sum(excluded_amounts.values())
print(f"  Excluded {len(excluded_amounts)} addresses totaling {total_excluded:,.0f} tokens")
for addr, amt in sorted(excluded_amounts.items(), key=lambda x: -x[1]):
    print(f"    {addr}: {amt:,.2f}")

# Filter
filtered = [h for h in holders if h["address"] not in EXCLUDE_ADDRS]
filtered.sort(key=lambda x: -x["amount"])
total = sum(h["amount"] for h in filtered)
shares = [h["amount"] / total for h in filtered]
n_holders = len(filtered)

# HHI
hhi = sum(s ** 2 for s in shares)
print(f"\n  Post-exclusion HHI: {hhi:.6f}")
print(f"  Post-exclusion holders: {n_holders}")
assert abs(hhi - 0.0045) < 0.001, f"HHI mismatch: {hhi:.6f} (expected ~0.0045)"
assert n_holders == 1886, f"Holder count mismatch: {n_holders} (expected 1886)"

# Gini (Brown's formula)
sorted_shares = sorted(shares)
n = len(sorted_shares)
cumulative = np.cumsum(sorted_shares)
gini = 1 - (2 / n) * (n - np.sum(np.arange(1, n + 1) * sorted_shares / cumulative[-1]))
# More standard: gini = (2 * sum(i * x_i) / (n * sum(x_i))) - (n + 1) / n
sorted_amounts = sorted([h["amount"] for h in filtered])
gini = (2 * sum((i + 1) * sorted_amounts[i] for i in range(n)) / (n * sum(sorted_amounts))) - (n + 1) / n

# Top 1/5/10 %
top1_pct = round(shares[0] * 100, 2)
top5_pct = round(sum(shares[:5]) * 100, 2)
top10_pct = round(sum(shares[:10]) * 100, 2)

# Entropy
entropy = -sum(s * math.log2(s) for s in shares if s > 0)

# Total balance (for top-1000 field: we have 1886, report sum of top 1000)
top1000_balance = sum(h["amount"] for h in filtered[:1000])

print(f"  Gini: {gini:.4f}")
print(f"  Entropy: {entropy:.4f}")
print(f"  Top 1%: {top1_pct}%, Top 5%: {top5_pct}%, Top 10%: {top10_pct}%")
print(f"  Total balance (post-exclusion): {total:,.2f}")
print(f"  Top-1000 balance: {top1000_balance:,.2f}")

save_progress("step1_verify", {
    "hhi_raw": round(hhi_raw, 6),
    "hhi_post_exclusion": round(hhi, 6),
    "n_holders_post_exclusion": n_holders,
    "n_exclusions": len(excluded_amounts),
    "total_excluded_tokens": round(total_excluded, 0),
    "gini": round(gini, 4),
    "entropy": round(entropy, 4),
    "top1_pct": top1_pct,
    "top5_pct": top5_pct,
    "top10_pct": top10_pct,
    "VERIFIED": True,
})
print("  ✓ VERIFIED")


# ── Step 2: Save holder list ─────────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 2: Save holder list to replication package")
print("=" * 60)

holder_path = PROJECT_DIR / "holder_lists" / "holders_HYPE.csv"
with open(holder_path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["address", "balance", "rank", "share", "token"])
    for i, h in enumerate(filtered):
        writer.writerow([h["address"], h["amount"], i + 1, shares[i], "HYPE"])

print(f"  Saved {n_holders} rows to {holder_path}")
save_progress("step2_holder_list", {"path": str(holder_path), "rows": n_holders})


# ── Step 3: Append to governance_concentration_april2026.csv ─────────────────
print("\n" + "=" * 60)
print("STEP 3: Append to governance_concentration_april2026.csv")
print("=" * 60)

conc_path = PROJECT_DIR / "governance_concentration_april2026.csv"
with open(conc_path, "r") as f:
    reader = csv.DictReader(f)
    old_rows = list(reader)
    cols = reader.fieldnames

old_rows = [r for r in old_rows if r.get("protocol", "").strip()]
old_count = len(old_rows)
print(f"  Existing protocols: {old_count}")

# Check not already present
assert not any(r["protocol"] == "Hyperliquid" for r in old_rows), "Hyperliquid already in concentration CSV"

new_row = {
    "protocol": "Hyperliquid",
    "token": "HYPE",
    "category": "DeFi",
    "chain": "hyperliquid_l1",
    "measurement_type": "governance_token",
    "launch_year": "2024",
    "governance_model": "token_weighted",
    "distribution_type": "airdrop",
    "hhi": str(round(hhi, 6)),
    "gini": str(round(gini, 4)),
    "top1_pct": str(top1_pct),
    "top5_pct": str(top5_pct),
    "top10_pct": str(top10_pct),
    "n_holders": str(n_holders),
    "total_balance_top1000": str(round(top1000_balance, 2)),
    "source": "Hypurrscan",
    "query_id": "",
    "notes": "0% VC; 31% community airdrop; deflationary buyback; Hyperliquid L1 native token",
}

with open(conc_path, "a", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=cols)
    writer.writerow(new_row)

print(f"  Appended Hyperliquid row (old count: {old_count})")
save_progress("step3_concentration", {"appended": True})


# ── Step 4: Append to exclusions_log.csv ─────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 4: Append to exclusions_log.csv")
print("=" * 60)

excl_path = PROJECT_DIR / "exclusions_log.csv"
with open(excl_path, "r") as f:
    reader = csv.DictReader(f)
    excl_cols = reader.fieldnames

# token,address,identity,exclusion_reason,chain,hhi_before,hhi_after,source
for addr, identity, reason, source in EXCLUSION_DETAILS:
    row = {
        "token": "HYPE",
        "address": addr,
        "identity": identity,
        "exclusion_reason": reason,
        "chain": "Hyperliquid L1",
        "hhi_before": str(round(hhi_raw, 6)),
        "hhi_after": str(round(hhi, 6)),
        "source": source,
    }
    with open(excl_path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=excl_cols)
        writer.writerow(row)

print(f"  Appended 5 exclusion rows for HYPE")
save_progress("step4_exclusions", {"appended": 5})


# ── Step 5: Append to data/covariates_merged.csv ─────────────────────────────
print("\n" + "=" * 60)
print("STEP 5: Append to covariates_merged.csv")
print("=" * 60)

cov_path = PROJECT_DIR / "data" / "covariates_merged.csv"
with open(cov_path, "r") as f:
    reader = csv.DictReader(f)
    cov_cols = reader.fieldnames

log_hhi = math.log(hhi)
log_fdv = math.log(35e9)

cov_row = {col: "" for col in cov_cols}
cov_row.update({
    "protocol": "Hyperliquid",
    "token": "HYPE",
    "category": "DeFi",
    "launch_year": "2024",
    "governance_model": "token_weighted",
    "distribution_type": "airdrop",
    "hhi": str(round(hhi, 6)),
    "gini": str(round(gini, 4)),
    "top1_pct": str(top1_pct),
    "top5_pct": str(top5_pct),
    "top10_pct": str(top10_pct),
    "n_holders": str(n_holders),
    "market_cap_usd": "9300000000.0",
    "fdv_usd": "35000000000.0",
    "team_pct": "29.8",
    "investor_pct": "0.0",
    "community_pct": "31.0",
    "treasury_pct": "39.2",
    "other_pct": "0.0",
    "insider_pct": "29.8",
    "maturity_years": "2",
    "log_hhi": str(log_hhi),
    "log_fdv": str(log_fdv),
    "regression_ready": "True",
    "source": "Hypurrscan",
})

with open(cov_path, "a", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=cov_cols)
    writer.writerow(cov_row)

print(f"  Appended Hyperliquid to covariates_merged.csv")
save_progress("step5_covariates", {"appended": True})


# ── Step 6: Append to data/full_merged_dataset.csv ───────────────────────────
print("\n" + "=" * 60)
print("STEP 6: Append to full_merged_dataset.csv")
print("=" * 60)

fmd_path = PROJECT_DIR / "data" / "full_merged_dataset.csv"
with open(fmd_path, "r") as f:
    reader = csv.DictReader(f)
    fmd_cols = reader.fieldnames

fmd_row = {col: "" for col in fmd_cols}
fmd_row.update({
    "protocol": "Hyperliquid",
    "token": "HYPE",
    "category": "DeFi",
    "chain": "hyperliquid_l1",
    "measurement_type": "governance_token",
    "hhi": str(round(hhi, 6)),
    "gini": str(round(gini, 4)),
    "top1_pct": str(top1_pct),
    "top5_pct": str(top5_pct),
    "top10_pct": str(top10_pct),
    "n_holders": str(n_holders),
    "total_balance_top1000": str(round(top1000_balance, 2)),
    "source": "Hypurrscan",
    "team_pct": "29.8",
    "investor_pct": "0.0",
    "community_pct": "31.0",
    "treasury_pct": "39.2",
    "insider_pct": "29.8",
    "fdv_usd": "35000000000.0",
    "market_cap_usd": "9300000000.0",
    "maturity_years": "2",
    "log_fdv": str(log_fdv),
    "regression_ready": "True",
    "symbol": "HYPE",
    "governance_model": "token_weighted",
    "other_pct": "0.0",
})

with open(fmd_path, "a", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fmd_cols)
    writer.writerow(fmd_row)

print(f"  Appended Hyperliquid to full_merged_dataset.csv")
save_progress("step6_full_merged", {"appended": True})


# ── Step 7: Append to regression_data_april2026.csv ──────────────────────────
print("\n" + "=" * 60)
print("STEP 7: Append to regression_data_april2026.csv")
print("=" * 60)

reg_path = PROJECT_DIR / "regression_data_april2026.csv"
with open(reg_path, "r") as f:
    reader = csv.DictReader(f)
    reg_cols = reader.fieldnames

reg_row = {col: "" for col in reg_cols}
reg_row.update({
    "protocol": "Hyperliquid",
    "token": "HYPE",
    "category": "DeFi",
    "chain": "hyperliquid_l1",
    "measurement_type": "governance_token",
    "hhi": str(round(hhi, 6)),
    "gini": str(round(gini, 4)),
    "top1_pct": str(top1_pct),
    "top5_pct": str(top5_pct),
    "top10_pct": str(top10_pct),
    "n_holders": str(n_holders),
    "total_balance_top1000": str(round(top1000_balance, 2)),
    "source": "Hypurrscan",
    "team_pct": "29.8",
    "investor_pct": "0.0",
    "community_pct": "31.0",
    "treasury_pct": "39.2",
    "insider_pct": "29.8",
    "fdv_usd": "35000000000.0",
    "market_cap_usd": "9300000000.0",
    "maturity_years": "2",
    "log_fdv": str(log_fdv),
    "regression_ready": "True",
})

with open(reg_path, "a", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=reg_cols)
    writer.writerow(reg_row)

print(f"  Appended Hyperliquid to regression_data_april2026.csv")
save_progress("step7_regression_data", {"appended": True})


# ── Step 8: Rerun regressions ────────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 8: Rerun statistical tests")
print("=" * 60)

# Load updated full_merged_dataset
import pandas as pd

df = pd.read_csv(fmd_path)
df = df[df["regression_ready"] == True]
df["hhi"] = pd.to_numeric(df["hhi"], errors="coerce")
df["insider_pct"] = pd.to_numeric(df["insider_pct"], errors="coerce")
df["subsidy_ratio"] = pd.to_numeric(df["subsidy_ratio"], errors="coerce")

new_n = len(df)
print(f"  Total regression-ready protocols: {new_n}")
print(f"  Category breakdown:")
print(df["category"].value_counts().to_string())

defi = df[df["category"] == "DeFi"]["hhi"].dropna()
depin = df[df["category"] == "DePIN"]["hhi"].dropna()
infra = df[df["category"] == "L1_L2_Infra"]["hhi"].dropna()

print(f"\n  DeFi N={len(defi)}, DePIN N={len(depin)}, Infra N={len(infra)}")

# --- Wilcoxon rank-sum: DePIN vs DeFi ---
stat_dd, p_dd = stats.mannwhitneyu(depin, defi, alternative="two-sided")
# Cohen's d
d_dd = (depin.mean() - defi.mean()) / np.sqrt((depin.std()**2 + defi.std()**2) / 2)
print(f"\n  DePIN vs DeFi Wilcoxon: U={stat_dd}, p={p_dd:.4f}, d={d_dd:.4f}")

# --- Wilcoxon rank-sum: DePIN vs Infra ---
stat_di, p_di = stats.mannwhitneyu(depin, infra, alternative="two-sided")
d_di = (depin.mean() - infra.mean()) / np.sqrt((depin.std()**2 + infra.std()**2) / 2)
print(f"  DePIN vs Infra Wilcoxon: U={stat_di}, p={p_di:.4f}, d={d_di:.4f}")

# --- Insider allocation correlation ---
alloc_df = df[["insider_pct", "hhi"]].dropna()
alloc_n = len(alloc_df)
r_alloc, p_alloc = stats.pearsonr(alloc_df["insider_pct"], alloc_df["hhi"])
print(f"\n  Insider allocation ~ HHI: r={r_alloc:.4f}, p={p_alloc:.4f}, N={alloc_n}")

# --- Summary statistics ---
defi_old_hhis = defi.drop(defi[df[df["category"]=="DeFi"]["protocol"] == "Hyperliquid"].index, errors="ignore")
# Easier: just compute with and without Hyperliquid
all_defi_mask = df["category"] == "DeFi"
hype_mask = df["protocol"] == "Hyperliquid"

defi_new = df[all_defi_mask]["hhi"]
defi_old = df[all_defi_mask & ~hype_mask]["hhi"]
full_new = df["hhi"]
full_old = df[~hype_mask]["hhi"]

print(f"\n  DeFi HHI (old N={len(defi_old)}): mean={defi_old.mean():.6f}, median={defi_old.median():.6f}, std={defi_old.std():.6f}")
print(f"  DeFi HHI (new N={len(defi_new)}): mean={defi_new.mean():.6f}, median={defi_new.median():.6f}, std={defi_new.std():.6f}")
print(f"  Full sample HHI (old N={len(full_old)}): mean={full_old.mean():.6f}, median={full_old.median():.6f}")
print(f"  Full sample HHI (new N={len(full_new)}): mean={full_new.mean():.6f}, median={full_new.median():.6f}")

# Subsidy regression check
subsidy_df = df[df["subsidy_ratio"].notna() & (df["subsidy_ratio"] > 0)]
print(f"\n  Subsidy regression N: {len(subsidy_df)} (Hyperliquid excluded: subsidy=NaN)")
assert "Hyperliquid" not in subsidy_df["protocol"].values, "Hyperliquid should not be in subsidy regression"

# --- Build results JSON ---
results = {
    "hhi_verified": True,
    "hhi_raw": round(hhi_raw, 6),
    "hhi_post_exclusion": round(hhi, 6),
    "new_sample_size": int(new_n),
    "defi_sample_size": int(len(defi_new)),
    "depin_sample_size": int(len(depin)),
    "sector_pvalue_depin_defi": round(p_dd, 4),
    "sector_pvalue_depin_defi_old": 0.20,
    "sector_effect_d_depin_defi": round(d_dd, 4),
    "sector_pvalue_depin_infra": round(p_di, 4),
    "sector_pvalue_depin_infra_old": 0.038,
    "sector_effect_d_depin_infra": round(d_di, 4),
    "allocation_r": round(r_alloc, 4),
    "allocation_p": round(p_alloc, 4),
    "allocation_n": int(alloc_n),
    "allocation_r_old": 0.08,
    "allocation_p_old": 0.64,
    "defi_mean_hhi_old": round(defi_old.mean(), 6),
    "defi_mean_hhi_new": round(defi_new.mean(), 6),
    "defi_median_hhi_old": round(defi_old.median(), 6),
    "defi_median_hhi_new": round(defi_new.median(), 6),
    "full_sample_mean_hhi_old": round(full_old.mean(), 6),
    "full_sample_mean_hhi_new": round(full_new.mean(), 6),
    "full_sample_median_hhi_old": round(full_old.median(), 6),
    "full_sample_median_hhi_new": round(full_new.median(), 6),
    "subsidy_regression_n": int(len(subsidy_df)),
    "hyperliquid_in_subsidy": False,
    "n_exclusions": 5,
    "total_excluded_tokens": round(total_excluded, 0),
    "gini": round(gini, 4),
    "entropy": round(entropy, 4),
    "top1_pct": top1_pct,
    "top5_pct": top5_pct,
    "top10_pct": top10_pct,
}

results_path = OUTPUT_DIR / "results_hyperliquid_addition.json"
with open(results_path, "w") as f:
    json.dump(results, f, indent=2)
print(f"\n  Saved results to {results_path}")

save_progress("step8_regressions", results)

# ── Verification summary ─────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("VERIFICATION SUMMARY")
print("=" * 60)
checks = [
    ("HHI ≈ 0.0045", abs(hhi - 0.0045) < 0.001),
    ("5 exclusions", len(excluded_amounts) == 5),
    ("Post-exclusion holders = 1886", n_holders == 1886),
    (f"Regression-ready N = {new_n} (old + 1)", new_n == len(full_old) + 1),
    (f"DeFi count = {len(defi_new)} (old + 1)", len(defi_new) == len(defi_old) + 1),
    ("Sector p > 0.10", p_dd > 0.10),
    ("Allocation |r| < 0.20", abs(r_alloc) < 0.20),
    ("Hyperliquid not in subsidy regression", "Hyperliquid" not in subsidy_df["protocol"].values),
]

all_pass = True
for desc, passed in checks:
    status = "✓" if passed else "✗"
    print(f"  {status} {desc}")
    if not passed:
        all_pass = False

if all_pass:
    print("\n  ALL CHECKS PASSED")
else:
    print("\n  SOME CHECKS FAILED")
    sys.exit(1)
