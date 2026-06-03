#!/usr/bin/env python3
"""B2 subsidy-to-concentration: ONE-COMMAND REPRODUCTION of the N=23 of-record
sample AND the N=35 sample-size-robustness extension.

    python b2_subsidy_n35_reproduce_2026-06-02.py

Reproduces, from the documented regression frame
(data/processed/regression_data_april2026.csv), the subsidy-ratio-vs-post-exclusion-
HHI bivariate correlation under two samples, with and without the single high-leverage
DePIN outlier (Livepeer), with no /tmp dependency and no live-API call:

  - N=23 OF-RECORD: subsidy_ratio non-null AND non-zero (sub_TT primary, sub_OC
    fallback for DePIN). This is the F-B2-4 of-record sample.
  - N=35 SAMPLE-SIZE-ROBUSTNESS: the non-zero filter relaxed to include the 12
    protocols with a genuine measured zero subsidy (revenue present, token
    incentives = 0: mature / buyback-only / no-fee-accrual tokens). Their zero is a
    substantive economic observation, not a data gap.

The point: the apparent positive subsidy-concentration correlation is single-outlier
(Livepeer) driven at BOTH sample sizes and collapses to a null when Livepeer is
removed, so the result is a demonstrated-fragile one, not a sample-size artifact that
more N would cure.

INPUT (committed; no /tmp): data/processed/regression_data_april2026.csv
"""
import csv
import math
from pathlib import Path

from scipy import stats as ss

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
DATA_PATH = REPO_ROOT / "data" / "processed" / "regression_data_april2026.csv"


def _f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return float("nan")


def load(include_zero):
    """Subsidy sample: sub_TT primary, sub_OC fallback. include_zero=False reproduces
    the N=23 of-record (non-zero filter); include_zero=True is the N=35 sample."""
    out = []
    with DATA_PATH.open() as fh:
        for row in csv.DictReader(fh):
            sub_tt = _f(row.get("subsidy_ratio", ""))
            sub_oc = _f(row.get("subsidy_ratio_onchain", ""))
            if not math.isnan(sub_tt) and (include_zero or sub_tt != 0):
                sub = sub_tt
            elif not math.isnan(sub_oc) and (include_zero or sub_oc != 0):
                sub = sub_oc
            else:
                continue
            hhi = _f(row.get("hhi", ""))
            if math.isnan(hhi):
                continue
            out.append({"protocol": row["protocol"], "category": row["category"],
                        "sub": sub, "hhi": hhi})
    return out


def battery(rows, label):
    sub = [r["sub"] for r in rows]
    hhi = [r["hhi"] for r in rows]
    pr = ss.pearsonr(sub, hhi)
    sp = ss.spearmanr(sub, hhi)
    no_lp = [r for r in rows if r["protocol"].upper() != "LIVEPEER"]
    sub2 = [r["sub"] for r in no_lp]
    hhi2 = [r["hhi"] for r in no_lp]
    pr2 = ss.pearsonr(sub2, hhi2)
    sp2 = ss.spearmanr(sub2, hhi2)
    print(f"\n=== {label}  (N = {len(rows)}) ===")
    print(f"  with Livepeer    : Pearson r = {pr.statistic:+.4f}, p = {pr.pvalue:.4f}; "
          f"Spearman rho = {sp.statistic:+.4f}, p = {sp.pvalue:.4f}")
    print(f"  without Livepeer : Pearson r = {pr2.statistic:+.4f}, p = {pr2.pvalue:.4f} "
          f"(N = {len(no_lp)}); Spearman rho = {sp2.statistic:+.4f}, p = {sp2.pvalue:.4f}")


def main():
    print("=" * 78)
    print("B2 subsidy-to-concentration: N=23 of-record vs N=35 sample-size-robustness")
    print("=" * 78)
    battery(load(include_zero=False), "OF-RECORD (non-zero subsidy filter; F-B2-4)")
    n35 = load(include_zero=True)
    battery(n35, "SAMPLE-SIZE-ROBUSTNESS (include 12 genuine-zero protocols)")
    zeros = [r["protocol"] for r in n35 if r["sub"] == 0]
    print(f"\n  12 genuine-zero protocols added (revenue present, incentives = 0): {zeros}")
    print("\n[done] subsidy N=23 vs N=35 reproduced; no /tmp, no live-API.")


if __name__ == "__main__":
    main()
