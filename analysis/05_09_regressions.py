"""
B2 Full Recomputation — 40 Protocols, Clean Regressions
========================================================
Produces authoritative data/regression_results.json from the N=40 dataset.
Uses subsidy_ratio_onchain (NOT legacy subsidy_ratio).

Run: python3 scripts/recompute_regressions.py
"""

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

PROJECT_DIR = Path(__file__).parent.parent
CONC_CSV = PROJECT_DIR / "data" / "processed" / "governance_concentration_april2026.csv"
REG_CSV = PROJECT_DIR / "data" / "processed" / "regression_data_april2026.csv"
OUTPUT_JSON = PROJECT_DIR / "outputs" / "regression_results.json"

# Old values for before/after comparison
OLD = {
    "n_concentration": 39,
    "sector_mw_p": 0.072,
    "cross_pearson_r": 0.58,
    "cross_pearson_p": 0.007,
    "cross_spearman_rho": 0.157,
    "cross_spearman_p": 0.508,
    "cross_log_r": 0.234,
    "cross_log_p": 0.35,
    "excl_livepeer_r": 0.128,
    "excl_livepeer_p": 0.601,
    "depin_pearson_r": 0.525,
    "depin_pearson_p": 0.098,
    "depin_spearman_rho": 0.027,
    "depin_spearman_p": 0.937,
    "defi_pearson_r": -0.26,
    "defi_pearson_p": 0.499,
}


def validate_dataset(conc: pd.DataFrame, reg: pd.DataFrame):
    """Assert dataset integrity before computation."""
    # Concentration universe = 40
    assert len(conc) == 40, f"Concentration CSV: expected 40, got {len(conc)}"

    # Regression file = 40
    assert len(reg) == 40, f"Regression CSV: expected 40, got {len(reg)}"

    # All 5 new protocols present in both files
    required = ["Aethir", "Hivemapper", "io.net", "Hyperliquid", "Balancer"]
    for name in required:
        conc_match = conc[conc["protocol"].str.contains(name, case=False, na=False)]
        reg_match = reg[reg["protocol"].str.contains(name, case=False, na=False)]
        assert len(conc_match) == 1, f"{name} missing/dup in concentration (found {len(conc_match)})"
        assert len(reg_match) == 1, f"{name} missing/dup in regression (found {len(reg_match)})"

    # Spot-check HHI values
    hype = reg[reg["protocol"].str.contains("Hyperliquid", case=False)].iloc[0]
    assert abs(hype["hhi"] - 0.004526) < 0.001, f"HYPE HHI wrong: {hype['hhi']}"

    bal = reg[reg["protocol"].str.contains("Balancer", case=False)].iloc[0]
    assert abs(bal["hhi"] - 0.027673) < 0.005, f"BAL HHI wrong: {bal['hhi']}"

    # No duplicates
    assert reg["protocol"].nunique() == 40, f"Duplicate protocols in regression"
    assert conc["protocol"].nunique() == 40, f"Duplicate protocols in concentration"

    # HHI present for all 40
    assert reg["hhi"].notna().sum() == 40, f"Missing HHI values"

    print("Dataset integrity: PASS (N=40, all 5 new protocols, no duplicates)")


def summary_stats(df: pd.DataFrame):
    """Print and return summary statistics."""
    print("\n" + "=" * 60)
    print("SUMMARY STATISTICS")
    print("=" * 60)

    print(f"\nFull sample (N={len(df)}):")
    print(f"  Mean HHI:   {df['hhi'].mean():.4f}")
    print(f"  Median HHI: {df['hhi'].median():.4f}")
    print(f"  Std HHI:    {df['hhi'].std():.4f}")
    min_row = df.loc[df["hhi"].idxmin()]
    max_row = df.loc[df["hhi"].idxmax()]
    print(f"  Min: {df['hhi'].min():.4f} ({min_row['protocol']})")
    print(f"  Max: {df['hhi'].max():.4f} ({max_row['protocol']})")

    sector_stats = {}
    for sector in sorted(df["category"].unique()):
        sub = df[df["category"] == sector]
        s = {
            "n": len(sub),
            "mean": sub["hhi"].mean(),
            "median": sub["hhi"].median(),
            "std": sub["hhi"].std(),
        }
        sector_stats[sector] = s
        print(f"\n{sector} (N={s['n']}):")
        print(f"  Mean HHI:   {s['mean']:.4f}")
        print(f"  Median HHI: {s['median']:.4f}")
        print(f"  Std HHI:    {s['std']:.4f}")

    return sector_stats


def sector_comparison(df: pd.DataFrame):
    """DePIN vs DeFi comparison tests."""
    print("\n" + "=" * 60)
    print("SECTOR COMPARISON: DePIN vs DeFi")
    print("=" * 60)

    depin_hhi = df[df["category"] == "DePIN"]["hhi"].values
    defi_hhi = df[df["category"] == "DeFi"]["hhi"].values

    # Welch's t-test
    t_stat, t_p = stats.ttest_ind(depin_hhi, defi_hhi, equal_var=False)

    # Mann-Whitney U
    mw_stat, mw_p = stats.mannwhitneyu(depin_hhi, defi_hhi, alternative="two-sided")

    # Cohen's d
    pooled_std = np.sqrt((depin_hhi.std() ** 2 + defi_hhi.std() ** 2) / 2)
    cohens_d = (depin_hhi.mean() - defi_hhi.mean()) / pooled_std if pooled_std > 0 else 0

    print(f"  DePIN: N={len(depin_hhi)}, mean={depin_hhi.mean():.4f}")
    print(f"  DeFi:  N={len(defi_hhi)}, mean={defi_hhi.mean():.4f}")
    print(f"  Welch t-test: t={t_stat:.3f}, p={t_p:.4f}")
    print(f"  Mann-Whitney: U={mw_stat:.0f}, p={mw_p:.4f}")
    print(f"  Cohen's d:    {cohens_d:.3f}")

    return {
        "depin_n": len(depin_hhi),
        "defi_n": len(defi_hhi),
        "depin_mean_hhi": round(float(depin_hhi.mean()), 4),
        "defi_mean_hhi": round(float(defi_hhi.mean()), 4),
        "welch_t": round(float(t_stat), 4),
        "welch_p": round(float(t_p), 4),
        "mw_U": round(float(mw_stat), 1),
        "mw_p": round(float(mw_p), 4),
        "cohens_d": round(float(cohens_d), 3),
    }


def insider_regression(df: pd.DataFrame):
    """Insider allocation vs HHI."""
    print("\n" + "=" * 60)
    print("INSIDER ALLOCATION REGRESSION")
    print("=" * 60)

    reg_df = df.dropna(subset=["hhi", "insider_pct"])
    print(f"  N = {len(reg_df)}")

    r, p = stats.pearsonr(reg_df["insider_pct"], reg_df["hhi"])
    rho, rho_p = stats.spearmanr(reg_df["insider_pct"], reg_df["hhi"])

    print(f"  Pearson:  r = {r:+.4f}, p = {p:.4f}")
    print(f"  Spearman: rho = {rho:+.4f}, p = {rho_p:.4f}")

    return {
        "n": len(reg_df),
        "pearson_r": round(float(r), 4),
        "pearson_p": round(float(p), 4),
        "spearman_rho": round(float(rho), 4),
        "spearman_p": round(float(rho_p), 4),
    }


def subsidy_regression(df: pd.DataFrame):
    """Subsidy ratio (onchain) vs HHI — cross-sector and within-sector."""
    print("\n" + "=" * 60)
    print("SUBSIDY REGRESSION (subsidy_ratio_onchain)")
    print("=" * 60)

    sub_df = df.dropna(subset=["hhi", "subsidy_ratio_onchain"])
    print(f"  Cross-sector N = {len(sub_df)}")

    results = {"n": len(sub_df)}

    # Cross-sector Pearson & Spearman
    r, p = stats.pearsonr(sub_df["subsidy_ratio_onchain"], sub_df["hhi"])
    rho, rho_p = stats.spearmanr(sub_df["subsidy_ratio_onchain"], sub_df["hhi"])
    print(f"  Cross Pearson:  r = {r:+.4f}, p = {p:.4f}")
    print(f"  Cross Spearman: rho = {rho:+.4f}, p = {rho_p:.4f}")
    results["cross_pearson_r"] = round(float(r), 4)
    results["cross_pearson_p"] = round(float(p), 4)
    results["cross_spearman_rho"] = round(float(rho), 4)
    results["cross_spearman_p"] = round(float(rho_p), 4)

    # Log-transformed (exclude zero subsidy)
    log_sub = sub_df[sub_df["subsidy_ratio_onchain"] > 0].copy()
    if len(log_sub) >= 3:
        log_sub["log_subsidy"] = np.log(log_sub["subsidy_ratio_onchain"])
        r_log, p_log = stats.pearsonr(log_sub["log_subsidy"], log_sub["hhi"])
        print(f"  Log Pearson: r = {r_log:+.4f}, p = {p_log:.4f} (N={len(log_sub)})")
        results["cross_log_r"] = round(float(r_log), 4)
        results["cross_log_p"] = round(float(p_log), 4)
        results["cross_log_n"] = len(log_sub)

    # Excluding Livepeer (outlier check)
    excl_lvp = sub_df[~sub_df["protocol"].str.contains("Livepeer", case=False)]
    if len(excl_lvp) >= 3:
        r_ex, p_ex = stats.pearsonr(excl_lvp["subsidy_ratio_onchain"], excl_lvp["hhi"])
        print(f"  Excl Livepeer: r = {r_ex:+.4f}, p = {p_ex:.4f} (N={len(excl_lvp)})")
        results["excl_livepeer_r"] = round(float(r_ex), 4)
        results["excl_livepeer_p"] = round(float(p_ex), 4)
        results["excl_livepeer_n"] = len(excl_lvp)

    # Within DePIN
    depin_sub = sub_df[sub_df["category"] == "DePIN"]
    results["n_depin"] = len(depin_sub)
    if len(depin_sub) >= 5:
        r_dp, p_dp = stats.pearsonr(depin_sub["subsidy_ratio_onchain"], depin_sub["hhi"])
        rho_dp, rho_p_dp = stats.spearmanr(depin_sub["subsidy_ratio_onchain"], depin_sub["hhi"])
        print(f"  DePIN Pearson:  r = {r_dp:+.4f}, p = {p_dp:.4f} (N={len(depin_sub)})")
        print(f"  DePIN Spearman: rho = {rho_dp:+.4f}, p = {rho_p_dp:.4f}")
        results["depin_pearson_r"] = round(float(r_dp), 4)
        results["depin_pearson_p"] = round(float(p_dp), 4)
        results["depin_spearman_rho"] = round(float(rho_dp), 4)
        results["depin_spearman_p"] = round(float(rho_p_dp), 4)

    # Within DeFi
    defi_sub = sub_df[sub_df["category"] == "DeFi"]
    results["n_defi"] = len(defi_sub)
    if len(defi_sub) >= 5:
        r_df, p_df = stats.pearsonr(defi_sub["subsidy_ratio_onchain"], defi_sub["hhi"])
        rho_df, rho_p_df = stats.spearmanr(defi_sub["subsidy_ratio_onchain"], defi_sub["hhi"])
        print(f"  DeFi Pearson:  r = {r_df:+.4f}, p = {p_df:.4f} (N={len(defi_sub)})")
        print(f"  DeFi Spearman: rho = {rho_df:+.4f}, p = {rho_p_df:.4f}")
        results["defi_pearson_r"] = round(float(r_df), 4)
        results["defi_pearson_p"] = round(float(p_df), 4)
        results["defi_spearman_rho"] = round(float(rho_df), 4)
        results["defi_spearman_p"] = round(float(rho_p_df), 4)

    # Within L1_L2_Infra
    infra_sub = sub_df[sub_df["category"] == "L1_L2_Infra"]
    results["n_infra"] = len(infra_sub)
    if len(infra_sub) >= 3:
        r_inf, p_inf = stats.pearsonr(infra_sub["subsidy_ratio_onchain"], infra_sub["hhi"])
        print(f"  Infra Pearson:  r = {r_inf:+.4f}, p = {p_inf:.4f} (N={len(infra_sub)})")
        results["infra_pearson_r"] = round(float(r_inf), 4)
        results["infra_pearson_p"] = round(float(p_inf), 4)

    return results


def robustness_correlations(df: pd.DataFrame):
    """HHI vs Gini correlation."""
    print("\n" + "=" * 60)
    print("ROBUSTNESS: METRIC CORRELATIONS")
    print("=" * 60)

    results = {}

    valid = df.dropna(subset=["hhi", "gini"])
    if len(valid) >= 3:
        r_gini, p_gini = stats.pearsonr(valid["hhi"], valid["gini"])
        print(f"  HHI-Gini: r = {r_gini:+.4f}, p = {p_gini:.4f} (N={len(valid)})")
        results["hhi_gini_r"] = round(float(r_gini), 4)
        results["hhi_gini_p"] = round(float(p_gini), 4)
        results["hhi_gini_n"] = len(valid)

    return results


def print_comparison(results: dict):
    """Print before/after comparison table."""
    print("\n" + "=" * 60)
    print("BEFORE -> AFTER COMPARISON")
    print("=" * 60)
    print(f"{'Metric':<30} {'Old (stale)':>12} {'New (clean)':>12} {'Delta':>10}")
    print("-" * 64)

    comparisons = [
        ("Concentration N", OLD["n_concentration"], results["n_concentration"], ""),
        ("Subsidy N", 20, results["n_subsidy"], ""),
        ("Sector MW p", OLD["sector_mw_p"], results["sector_mw_p"], ""),
        ("Cross Pearson r", OLD["cross_pearson_r"], results["cross_pearson_r"], ""),
        ("Cross Pearson p", OLD["cross_pearson_p"], results["cross_pearson_p"], ""),
        ("Cross Spearman rho", OLD["cross_spearman_rho"], results["cross_spearman_rho"], ""),
        ("Cross Spearman p", OLD["cross_spearman_p"], results["cross_spearman_p"], ""),
        ("Cross Log r", OLD["cross_log_r"], results["cross_log_r"], ""),
        ("Excl Livepeer r", OLD["excl_livepeer_r"], results["excl_livepeer_r"], ""),
        ("Excl Livepeer p", OLD["excl_livepeer_p"], results["excl_livepeer_p"], ""),
        ("DePIN Pearson r", OLD["depin_pearson_r"], results["depin_pearson_r"], ""),
        ("DePIN Pearson p", OLD["depin_pearson_p"], results["depin_pearson_p"], ""),
        ("DePIN Spearman rho", OLD["depin_spearman_rho"], results.get("depin_spearman_rho", "N/A"), ""),
        ("DeFi Pearson r", OLD["defi_pearson_r"], results["defi_pearson_r"], ""),
        ("DeFi Pearson p", OLD["defi_pearson_p"], results["defi_pearson_p"], ""),
        ("DePIN mean HHI", "?", results["depin_mean_hhi"], ""),
        ("DeFi mean HHI", "?", results["defi_mean_hhi"], ""),
        ("Full mean HHI", "?", results["full_mean_hhi"], ""),
    ]

    for label, old, new, _ in comparisons:
        if isinstance(old, str) or isinstance(new, str):
            delta = ""
        else:
            delta = f"{new - old:+.4f}"
        old_s = f"{old}" if isinstance(old, str) else f"{old:.4f}"
        new_s = f"{new}" if isinstance(new, str) else f"{new:.4f}"
        print(f"{label:<30} {old_s:>12} {new_s:>12} {delta:>10}")


def main():
    print("B2 Full Recomputation — 40 Protocols")
    print("=" * 60)

    # Load data
    conc = pd.read_csv(CONC_CSV)
    reg = pd.read_csv(REG_CSV)

    # Validate
    validate_dataset(conc, reg)

    # Use regression_data as the authoritative merged source
    df = reg.copy()

    # Summary stats
    sector_stats = summary_stats(df)

    # Sector comparison
    sector = sector_comparison(df)

    # Insider allocation regression
    insider = insider_regression(df)

    # Subsidy regression
    subsidy = subsidy_regression(df)

    # Robustness
    robustness = robustness_correlations(df)

    # Assemble output JSON
    results = {
        # Sample sizes
        "n_concentration": 40,
        "n_total": 40,
        "n_regression_ready": int((df["regression_ready"] == True).sum()),
        "n_subsidy": subsidy["n"],
        "n_depin_subsidy": subsidy["n_depin"],
        "n_defi_subsidy": subsidy["n_defi"],
        "n_infra_subsidy": subsidy["n_infra"],
        "subsidy_col": "subsidy_ratio_onchain",

        # Full-sample stats
        "full_mean_hhi": round(float(df["hhi"].mean()), 4),
        "full_median_hhi": round(float(df["hhi"].median()), 4),
        "full_std_hhi": round(float(df["hhi"].std()), 4),

        # Sector means
        "depin_mean_hhi": sector["depin_mean_hhi"],
        "defi_mean_hhi": sector["defi_mean_hhi"],

        # Sector comparison
        "sector_welch_t": sector["welch_t"],
        "sector_welch_p": sector["welch_p"],
        "sector_mw_U": sector["mw_U"],
        "sector_mw_p": sector["mw_p"],
        "sector_cohens_d": sector["cohens_d"],

        # Insider allocation
        "insider_pearson_r": insider["pearson_r"],
        "insider_pearson_p": insider["pearson_p"],
        "insider_spearman_rho": insider["spearman_rho"],
        "insider_spearman_p": insider["spearman_p"],
        "insider_n": insider["n"],

        # Subsidy cross-sector
        "cross_pearson_r": subsidy["cross_pearson_r"],
        "cross_pearson_p": subsidy["cross_pearson_p"],
        "cross_spearman_rho": subsidy["cross_spearman_rho"],
        "cross_spearman_p": subsidy["cross_spearman_p"],
        "cross_log_r": subsidy.get("cross_log_r"),
        "cross_log_p": subsidy.get("cross_log_p"),

        # Subsidy excl Livepeer
        "excl_livepeer_r": subsidy.get("excl_livepeer_r"),
        "excl_livepeer_p": subsidy.get("excl_livepeer_p"),

        # Subsidy within-DePIN
        "depin_pearson_r": subsidy.get("depin_pearson_r"),
        "depin_pearson_p": subsidy.get("depin_pearson_p"),
        "depin_spearman_rho": subsidy.get("depin_spearman_rho"),
        "depin_spearman_p": subsidy.get("depin_spearman_p"),

        # Subsidy within-DeFi
        "defi_pearson_r": subsidy.get("defi_pearson_r"),
        "defi_pearson_p": subsidy.get("defi_pearson_p"),
        "defi_spearman_rho": subsidy.get("defi_spearman_rho"),
        "defi_spearman_p": subsidy.get("defi_spearman_p"),

        # Robustness
        "hhi_gini_r": robustness.get("hhi_gini_r"),
        "hhi_gini_p": robustness.get("hhi_gini_p"),

        # BAL fix
        "bal_in_concentration": True,
        "bal_vetoken_caveat": "veBAL; raw token HHI reported, not voting power",
        "crv_vetoken_caveat": "veCRV; raw token HHI reported, not voting power",

        # Exclusion status
        "exclusion_pending": ["ATH", "HONEY", "IO"],

        # Metadata
        "_note": "Clean recomputation 2026-04-01. All 40 protocols in concentration universe. BAL included (was regression-only, now fixed). subsidy_ratio_onchain is authoritative. Protocol team/investor wallets excluded per exclusion registry. ATH/HONEY/IO exclusion verification deferred to next session.",
        "_replaces": "regression_results.json from prior session (stale, coefficients not recomputed after expansion)",
        "_timestamp": "2026-04-01",
    }

    # Write output
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_JSON, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nOutput written: {OUTPUT_JSON}")

    # Comparison table
    print_comparison(results)

    print("\nDone.")
    return results


if __name__ == "__main__":
    main()
