"""
Subsidy multivariate sensitivity check: sub_OC preferred over sub_TT.

Mirrors subsidy_multivariate_2026-05-19.py except the field selection convention
is inverted: prefer subsidy_ratio_onchain (raw OC computation) over subsidy_ratio
(Token Terminal). For protocols without OC fields populated, fall back to TT.

Purpose: assess whether the headline Spec 4 finding (subsidy coefficient not
significant after sector control; DePIN sector membership absorbs the apparent
subsidy-HHI association) is robust to the field selection convention.

Outputs the 4-spec result table for direct comparison with the canonical
TT-preferred analysis.
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
            try:
                sub_tt = float(row.get("subsidy_ratio", "") or "nan")
            except ValueError:
                sub_tt = float("nan")
            try:
                sub_oc = float(row.get("subsidy_ratio_onchain", "") or "nan")
            except ValueError:
                sub_oc = float("nan")
            # OC-preferred convention (inversion of canonical script)
            if not np.isnan(sub_oc) and sub_oc != 0:
                sub = sub_oc
                source = "OC"
            elif not np.isnan(sub_tt) and sub_tt != 0:
                sub = sub_tt
                source = "TT"
            else:
                continue
            try:
                hhi = float(row["hhi"])
            except (ValueError, KeyError):
                continue
            rows.append({
                "protocol": row["protocol"],
                "category": row["category"],
                "subsidy": sub,
                "subsidy_source": source,
                "hhi": hhi,
                "depin_dummy": 1 if row["category"] == "DePIN" else 0,
            })

    print(f"Subsidy sample (OC-preferred convention, N = {len(rows)}):")
    for r in rows:
        print(f"  {r['protocol']:<20} sub={r['subsidy']:.4f} ({r['subsidy_source']}) hhi={r['hhi']:.5f} depin={r['depin_dummy']}")
    print()

    def fit_ols(X, y, names):
        Xc = sm.add_constant(X)
        model = sm.OLS(y, Xc).fit()
        return model

    subs = np.array([r["subsidy"] for r in rows])
    hhis = np.array([r["hhi"] for r in rows])
    depins = np.array([r["depin_dummy"] for r in rows])

    # Spec 1: HHI ~ subsidy (all)
    m1 = fit_ols(subs.reshape(-1, 1), hhis, ["sub"])
    print(f"=== Spec 1: HHI ~ subsidy_OC (all, N = {len(rows)}) ===")
    print(f"  beta = {m1.params[1]:.6f}, t = {m1.tvalues[1]:.3f}, p = {m1.pvalues[1]:.4f}, Adj R^2 = {m1.rsquared_adj:.3f}")
    print()

    # Spec 2: drop Livepeer
    mask_no_lpt = np.array([r["protocol"] != "Livepeer" for r in rows])
    m2 = fit_ols(subs[mask_no_lpt].reshape(-1, 1), hhis[mask_no_lpt], ["sub"])
    print(f"=== Spec 2: HHI ~ subsidy_OC (no Livepeer, N = {mask_no_lpt.sum()}) ===")
    print(f"  beta = {m2.params[1]:.6f}, t = {m2.tvalues[1]:.3f}, p = {m2.pvalues[1]:.4f}, Adj R^2 = {m2.rsquared_adj:.3f}")
    print()

    # Spec 3: + DePIN dummy
    X3 = np.column_stack([subs, depins])
    m3 = fit_ols(X3, hhis, ["sub", "depin"])
    print(f"=== Spec 3: HHI ~ subsidy_OC + DePIN (all, N = {len(rows)}) ===")
    print(f"  subsidy beta = {m3.params[1]:.6f}, t = {m3.tvalues[1]:.3f}, p = {m3.pvalues[1]:.4f}")
    print(f"  DePIN beta   = {m3.params[2]:.6f}, t = {m3.tvalues[2]:.3f}, p = {m3.pvalues[2]:.4f}")
    print(f"  Adj R^2 = {m3.rsquared_adj:.3f}")
    print()

    # Spec 4: + DePIN dummy, no LPT
    X4 = np.column_stack([subs[mask_no_lpt], depins[mask_no_lpt]])
    m4 = fit_ols(X4, hhis[mask_no_lpt], ["sub", "depin"])
    print(f"=== Spec 4: HHI ~ subsidy_OC + DePIN (no Livepeer, N = {mask_no_lpt.sum()}) ===")
    print(f"  subsidy beta = {m4.params[1]:.6f}, t = {m4.tvalues[1]:.3f}, p = {m4.pvalues[1]:.4f}")
    print(f"  DePIN beta   = {m4.params[2]:.6f}, t = {m4.tvalues[2]:.3f}, p = {m4.pvalues[2]:.4f}")
    print(f"  Adj R^2 = {m4.rsquared_adj:.3f}")
    print()

    print("=== Summary table (OC-preferred sensitivity) ===")
    print(f"Spec                                        subsidy_p    DePIN_p    AdjR2")
    print(f"1. Subsidy_OC only (all)                       {m1.pvalues[1]:.4f}      (n/a)    {m1.rsquared_adj:.3f}")
    print(f"2. Subsidy_OC only (no LPT)                    {m2.pvalues[1]:.4f}      (n/a)    {m2.rsquared_adj:.3f}")
    print(f"3. Subsidy_OC + DePIN (all)                    {m3.pvalues[1]:.4f}    {m3.pvalues[2]:.4f}     {m3.rsquared_adj:.3f}")
    print(f"4. Subsidy_OC + DePIN (no LPT)                 {m4.pvalues[1]:.4f}    {m4.pvalues[2]:.4f}     {m4.rsquared_adj:.3f}")


if __name__ == "__main__":
    main()
