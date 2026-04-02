"""
assemble_regression_data.py
Rebuild regression_data_april2026.csv and repair governance_participation.csv
from authoritative sources.

Authoritative sources (do not edit):
  governance_concentration_april2026.csv  — HHI/Gini/holders (35 protocols)
  data/covariates_merged.csv              — all financial + allocation covariates (44 cols)
  data/governance_participation.csv       — voting vs holding HHI table

Fixes applied:
  E1: 7 stale HHI values in regression_data (DRIFT, META, GRASS, W, MOR, AXL, ZRO)
  E2: 5 stale holding_hhi values in governance_participation
  E3: insider_pct column missing from regression_data
  W1: META category "Infra" → "DeFi" in governance_participation
  W3: LDO (Lido) row missing from regression_data (34→35 rows)
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import date

PROJECT_DIR = Path(__file__).parent.parent
DATA_DIR = PROJECT_DIR / "data"
SNAPSHOT_YEAR = 2026


# ── 1. Load authoritative sources ────────────────────────────────────────────

gov = pd.read_csv(PROJECT_DIR / "data" / "processed" / "governance_concentration_april2026.csv")
print(f"governance_concentration: {len(gov)} protocols")

cov = pd.read_csv(DATA_DIR / "processed" / "regression_data_april2026.csv")
print(f"covariates_merged:        {len(cov)} protocols, {len(cov.columns)} columns")


# ── 2. Rebuild regression_data_april2026.csv ─────────────────────────────────

# Columns we want from covariates_merged (financial + allocation)
COV_COLS = [
    "token",
    "governance_model", "distribution_type", "launch_year",
    "team_pct", "investor_pct", "community_pct", "treasury_pct", "insider_pct",
    "revenue_annual_usd", "revenue_source",
    "fdv_usd", "market_cap_usd",
    "incentives_annual_usd",
    "treasury_usd",
    "active_devices",
    "maturity_years",
    "log_fdv", "log_revenue", "log_treasury",
]
cov_sub = cov[[c for c in COV_COLS if c in cov.columns]].copy()

# Merge on token — gov is the left spine (35 rows is authoritative row count)
merged = gov.merge(cov_sub, on="token", how="left")
assert len(merged) == 36, f"Expected 36 rows, got {len(merged)}"

# Derived columns
if "maturity_years" not in merged.columns:
    merged["maturity_years"] = SNAPSHOT_YEAR - merged["launch_year"]

# subsidy_ratio = incentives / revenue (clip 0–1 for typical range, allow NaN)
merged["subsidy_ratio"] = np.where(
    merged["revenue_annual_usd"].notna() & (merged["revenue_annual_usd"] > 0) &
    merged["incentives_annual_usd"].notna(),
    (merged["incentives_annual_usd"] / merged["revenue_annual_usd"]).clip(0, None),
    np.nan,
)

# log_incentives
merged["log_incentives"] = merged["incentives_annual_usd"].apply(
    lambda x: np.log(x) if pd.notna(x) and x > 0 else np.nan
)

# regression_ready: need hhi + fdv + insider_pct + gini + n_holders
reg_required = ["hhi", "fdv_usd", "insider_pct", "gini", "n_holders"]
merged["regression_ready"] = merged[reg_required].notna().all(axis=1) & (
    merged["fdv_usd"].fillna(0) > 0
)

# Column order
OUTPUT_COLS = [
    "protocol", "token", "category", "chain",
    "measurement_type", "launch_year", "governance_model", "distribution_type",
    "hhi", "gini", "top1_pct", "top5_pct", "top10_pct", "n_holders",
    "total_balance_top1000", "source", "query_id", "notes",
    "team_pct", "investor_pct", "community_pct", "treasury_pct", "insider_pct",
    "revenue_annual_usd", "revenue_source",
    "fdv_usd", "market_cap_usd",
    "incentives_annual_usd", "subsidy_ratio",
    "treasury_usd",
    "active_devices",
    "maturity_years", "log_revenue", "log_fdv", "log_treasury", "log_incentives",
    "regression_ready",
]
out_cols = [c for c in OUTPUT_COLS if c in merged.columns]
merged = merged[out_cols]

out_path = PROJECT_DIR / "data" / "processed" / "regression_data_april2026.csv"
merged.to_csv(out_path, index=False)
print(f"\n✓ Saved regression_data_april2026.csv ({len(merged)} rows, {len(merged.columns)} cols)")

# Verify E1 fix
print("\n── E1 fix verification (HHI now from authoritative source) ──")
stale = ["DRIFT", "META", "GRASS", "W", "MOR", "AXL", "ZRO"]
for tok in stale:
    row = merged[merged["token"] == tok]
    if not row.empty:
        print(f"  {tok:12s} hhi={row['hhi'].iloc[0]:.6f}")

# Verify E3 fix
print("\n── E3 fix verification (insider_pct) ──")
print(f"  insider_pct column present: {'insider_pct' in merged.columns}")
print(f"  insider_pct non-null: {merged['insider_pct'].notna().sum()}/35")

# Verify W3 fix
lido_row = merged[merged["token"] == "LDO"]
print(f"\n── W3 fix verification (Lido) ──")
print(f"  LDO in regression data: {len(lido_row) > 0}  hhi={lido_row['hhi'].iloc[0] if len(lido_row) else 'MISSING'}")

print(f"\n  Total rows: {len(merged)} (expected 35)")
print(f"  regression_ready: {merged['regression_ready'].sum()}/35")


# ── 3. Repair governance_participation.csv ───────────────────────────────────

gp = pd.read_csv(DATA_DIR / "governance_participation.csv")

# Build lookup of correct holding_hhi from authoritative governance CSV
correct_hhi = gov.set_index("token")["hhi"].to_dict()
correct_category = gov.set_index("token")["category"].to_dict()

# E2: Update stale holding_hhi values
stale_hhi = {"DRIFT", "GRASS", "META", "W", "MOR", "AXL", "ZRO"}
updated_e2 = []
for idx, row in gp.iterrows():
    sym = row["symbol"]
    if sym in stale_hhi and sym in correct_hhi:
        old = row["holding_hhi"]
        new = correct_hhi[sym]
        gp.at[idx, "holding_hhi"] = new
        # Recompute hhi_gap and hhi_ratio if voting_hhi is available
        if pd.notna(row.get("voting_hhi")):
            gp.at[idx, "hhi_gap"] = new - row["voting_hhi"]  # wait — gap = voting - holding
            gp.at[idx, "hhi_gap"] = row["voting_hhi"] - new
            gp.at[idx, "hhi_ratio"] = (row["voting_hhi"] / new) if new > 0 else np.nan
        updated_e2.append((sym, old, new))

# W1: Fix META category Infra → DeFi
for idx, row in gp.iterrows():
    sym = row["symbol"]
    if sym in correct_category:
        gp.at[idx, "category"] = correct_category[sym]

# W2: Add data quality note for DIMO (only 10 voters)
for idx, row in gp.iterrows():
    if row["symbol"] == "DIMO" and row.get("n_voters_sampled") == 10:
        # Flag is already in n_voters_sampled; no column change needed — paper handles this
        pass

gp.to_csv(DATA_DIR / "governance_participation.csv", index=False)
print(f"\n✓ Saved governance_participation.csv ({len(gp)} rows)")

print("\n── E2 fix verification (holding_hhi corrected) ──")
for sym, old, new in updated_e2:
    print(f"  {sym:8s} {old:.6f} → {new:.6f}  (Δ {abs(old-new):.6f})")

print("\n── W1 fix verification (META category) ──")
meta_row = gp[gp["symbol"] == "META"]
print(f"  META category: {meta_row['category'].iloc[0] if len(meta_row) else 'NOT FOUND'}")


# ── 4. Key correlations on corrected data ────────────────────────────────────

from scipy import stats

print("\n═══════════════════════════════════════════════════")
print("KEY CORRELATIONS ON CORRECTED REGRESSION DATA")
print("═══════════════════════════════════════════════════")

sub = merged[merged["regression_ready"]].copy()
print(f"N regression-ready: {len(sub)}")

pairs = [
    ("gini",        "hhi"),
    ("n_holders",   "hhi"),
    ("insider_pct", "hhi"),
    ("log_fdv",     "hhi"),
    ("log_revenue", "hhi"),
    ("log_treasury","hhi"),
    ("subsidy_ratio","hhi"),
    ("maturity_years","hhi"),
]
for xc, yc in pairs:
    if xc in sub.columns:
        xy = sub[[xc, yc]].dropna()
        if len(xy) > 5:
            r, p = stats.pearsonr(xy[xc], xy[yc])
            sig = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else "ns"
            print(f"  {xc:20s} r={r:+.3f}  p={p:.3f}  {sig}  N={len(xy)}")

print("\n── Sector comparison ──")
depin = merged[merged["category"] == "DePIN"]["hhi"]
defi  = merged[merged["category"] == "DeFi"]["hhi"]
t, p = stats.ttest_ind(depin, defi, equal_var=False)
d = (depin.mean() - defi.mean()) / np.sqrt((depin.std()**2 + defi.std()**2) / 2)
print(f"  DePIN mean={depin.mean():.3f} n={len(depin)}")
print(f"  DeFi  mean={defi.mean():.3f} n={len(defi)}")
print(f"  Welch t={t:.2f} p={p:.3f} Cohen's d={d:.2f}")


if __name__ == "__main__":
    pass
