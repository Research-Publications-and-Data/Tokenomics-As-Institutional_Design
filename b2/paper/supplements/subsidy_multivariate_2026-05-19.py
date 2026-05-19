"""
Item 5: Subsidy multivariate with sector control.

Tests whether subsidy-to-concentration correlation (Section 3.4 + 3.7
Livepeer-outlier result) persists when controlling for DePIN sector
membership.

Inputs:
- data/processed/regression_data_april2026.csv

Specifications:
1. Univariate: HHI ~ subsidy_ratio (all protocols with non-null subsidy)
2. Univariate without Livepeer: HHI ~ subsidy_ratio (excluding Livepeer outlier)
3. Multivariate with DePIN dummy: HHI ~ subsidy_ratio + DePIN_dummy
4. Multivariate without Livepeer: HHI ~ subsidy_ratio + DePIN_dummy

Hypothesis: Section 3.4 + 3.7 documents subsidy effect is Livepeer-driven.
Test: under sector control (DePIN dummy), does subsidy coefficient remain
significant after Livepeer exclusion? Predicted: no (sector membership
absorbs the apparent subsidy-HHI association).
"""

import csv
from pathlib import Path
import numpy as np
import statsmodels.api as sm


REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
DATA_PATH = REPO_ROOT / "data" / "processed" / "regression_data_april2026.csv"


def main():
    rows = []
    with DATA_PATH.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Use subsidy_ratio first; fallback to subsidy_ratio_onchain (DePIN subsidies)
            try:
                sub_tt = float(row.get("subsidy_ratio", "") or "nan")
            except ValueError:
                sub_tt = float("nan")
            try:
                sub_oc = float(row.get("subsidy_ratio_onchain", "") or "nan")
            except ValueError:
                sub_oc = float("nan")
            # Prefer Token Terminal value; fall back to on-chain
            if not np.isnan(sub_tt) and sub_tt != 0:
                sub = sub_tt
            elif not np.isnan(sub_oc) and sub_oc != 0:
                sub = sub_oc
            else:
                continue
            try:
                hhi = float(row["hhi"])
            except (ValueError, KeyError):
                continue
            rows.append({
                "protocol": row["protocol"],
                "category": row["category"],
                "hhi": hhi,
                "subsidy_ratio": sub,
            })

    protocols = [r["protocol"] for r in rows]
    print(f"Subsidy sample (non-null, non-zero subsidy): N = {len(rows)}")
    print(f"Protocols: {protocols}")
    print()

    # Spec 1: Univariate HHI ~ subsidy (all)
    X1 = sm.add_constant([r["subsidy_ratio"] for r in rows])
    y1 = [r["hhi"] for r in rows]
    m1 = sm.OLS(y1, X1).fit(cov_type="HC3")
    print(f"=== Spec 1: HHI ~ subsidy_ratio (all, N = {len(rows)}) ===")
    print(f"  beta = {m1.params[1]:.6f}, t = {m1.tvalues[1]:.3f}, p = {m1.pvalues[1]:.4f}, Adj R^2 = {m1.rsquared_adj:.3f}")

    # Spec 2: Univariate without Livepeer
    rows_no_lp = [r for r in rows if r["protocol"].upper() != "LIVEPEER"]
    X2 = sm.add_constant([r["subsidy_ratio"] for r in rows_no_lp])
    y2 = [r["hhi"] for r in rows_no_lp]
    m2 = sm.OLS(y2, X2).fit(cov_type="HC3")
    print(f"\n=== Spec 2: HHI ~ subsidy_ratio (without Livepeer, N = {len(rows_no_lp)}) ===")
    print(f"  beta = {m2.params[1]:.6f}, t = {m2.tvalues[1]:.3f}, p = {m2.pvalues[1]:.4f}, Adj R^2 = {m2.rsquared_adj:.3f}")

    # Spec 3: Multivariate with DePIN dummy (all)
    X3 = np.column_stack([
        [r["subsidy_ratio"] for r in rows],
        [1 if r["category"] == "DePIN" else 0 for r in rows],
    ])
    X3 = sm.add_constant(X3)
    y3 = y1
    m3 = sm.OLS(y3, X3).fit(cov_type="HC3")
    print(f"\n=== Spec 3: HHI ~ subsidy_ratio + DePIN_dummy (all, N = {len(rows)}) ===")
    print(f"  subsidy beta = {m3.params[1]:.6f}, t = {m3.tvalues[1]:.3f}, p = {m3.pvalues[1]:.4f}")
    print(f"  DePIN beta   = {m3.params[2]:.6f}, t = {m3.tvalues[2]:.3f}, p = {m3.pvalues[2]:.4f}")
    print(f"  Adj R^2 = {m3.rsquared_adj:.3f}")

    # Spec 4: Multivariate without Livepeer
    X4 = np.column_stack([
        [r["subsidy_ratio"] for r in rows_no_lp],
        [1 if r["category"] == "DePIN" else 0 for r in rows_no_lp],
    ])
    X4 = sm.add_constant(X4)
    y4 = y2
    m4 = sm.OLS(y4, X4).fit(cov_type="HC3")
    print(f"\n=== Spec 4: HHI ~ subsidy_ratio + DePIN_dummy (without Livepeer, N = {len(rows_no_lp)}) ===")
    print(f"  subsidy beta = {m4.params[1]:.6f}, t = {m4.tvalues[1]:.3f}, p = {m4.pvalues[1]:.4f}")
    print(f"  DePIN beta   = {m4.params[2]:.6f}, t = {m4.tvalues[2]:.3f}, p = {m4.pvalues[2]:.4f}")
    print(f"  Adj R^2 = {m4.rsquared_adj:.3f}")

    # Spec 5: Multivariate including log_fdv as additional control
    X5 = np.column_stack([
        [r["subsidy_ratio"] for r in rows_no_lp],
        [1 if r["category"] == "DePIN" else 0 for r in rows_no_lp],
    ])
    X5 = sm.add_constant(X5)
    print(f"\n=== Summary table ===")
    print(f"{'Spec':40s} {'subsidy_p':>12s} {'DePIN_p':>10s} {'AdjR2':>8s}")
    print(f"{'1. Subsidy only (all, N={len(rows)})':40s} {m1.pvalues[1]:>12.4f} {'(n/a)':>10s} {m1.rsquared_adj:>8.3f}")
    print(f"{'2. Subsidy only (no LPT, N=' + str(len(rows_no_lp)) + ')':40s} {m2.pvalues[1]:>12.4f} {'(n/a)':>10s} {m2.rsquared_adj:>8.3f}")
    print(f"{'3. Subsidy + DePIN (all, N=' + str(len(rows)) + ')':40s} {m3.pvalues[1]:>12.4f} {m3.pvalues[2]:>10.4f} {m3.rsquared_adj:>8.3f}")
    print(f"{'4. Subsidy + DePIN (no LPT, N=' + str(len(rows_no_lp)) + ')':40s} {m4.pvalues[1]:>12.4f} {m4.pvalues[2]:>10.4f} {m4.rsquared_adj:>8.3f}")

    out_csv = Path(__file__).parent / "subsidy_multivariate_2026-05-19.csv"
    with out_csv.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["spec", "N", "subsidy_beta", "subsidy_t", "subsidy_p", "depin_beta", "depin_t", "depin_p", "adj_r2"])
        w.writerow(["1. Subsidy only (all)", len(rows), f"{m1.params[1]:.6f}", f"{m1.tvalues[1]:.3f}", f"{m1.pvalues[1]:.4f}", "", "", "", f"{m1.rsquared_adj:.4f}"])
        w.writerow(["2. Subsidy only (no LPT)", len(rows_no_lp), f"{m2.params[1]:.6f}", f"{m2.tvalues[1]:.3f}", f"{m2.pvalues[1]:.4f}", "", "", "", f"{m2.rsquared_adj:.4f}"])
        w.writerow(["3. Subsidy + DePIN (all)", len(rows), f"{m3.params[1]:.6f}", f"{m3.tvalues[1]:.3f}", f"{m3.pvalues[1]:.4f}", f"{m3.params[2]:.6f}", f"{m3.tvalues[2]:.3f}", f"{m3.pvalues[2]:.4f}", f"{m3.rsquared_adj:.4f}"])
        w.writerow(["4. Subsidy + DePIN (no LPT)", len(rows_no_lp), f"{m4.params[1]:.6f}", f"{m4.tvalues[1]:.3f}", f"{m4.pvalues[1]:.4f}", f"{m4.params[2]:.6f}", f"{m4.tvalues[2]:.3f}", f"{m4.pvalues[2]:.4f}", f"{m4.rsquared_adj:.4f}"])
    print(f"\nWrote: {out_csv}")


if __name__ == "__main__":
    main()
