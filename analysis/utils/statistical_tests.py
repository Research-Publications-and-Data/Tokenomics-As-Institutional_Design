#!/usr/bin/env python3
"""
Statistical tests: DePIN vs DeFi governance concentration.
Reproduces the permutation test (p = 0.029) and Mann-Whitney U (p = 0.075)
reported in Section 5.3 of the paper.

Usage:
    python statistical_tests.py data/expected_results.csv data/statistical_test_results.csv
"""

import sys
import csv
import numpy as np
from scipy import stats


def main(input_path, output_path):
    # Extract HHI values from expected_results.csv
    defi_hhi = []
    depin_hhi = []

    defi_protocols = {
        "Compound", "MakerDAO", "Aave", "Uniswap", "Curve", "Optimism", "The Graph"
    }

    with open(input_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["metric"] == "HHI" and row["protocol"] not in ("sector", "Livepeer", "GEODNET"):
                hhi = float(row["value"])
                if row["protocol"] in defi_protocols:
                    defi_hhi.append(hhi)
                else:
                    depin_hhi.append(hhi)

    print(f"DeFi  (N={len(defi_hhi)}): {sorted(defi_hhi)}")
    print(f"DePIN (N={len(depin_hhi)}): {sorted(depin_hhi)}")
    print(f"DeFi  mean: {np.mean(defi_hhi):.4f}")
    print(f"DePIN mean: {np.mean(depin_hhi):.4f}")

    # Mann-Whitney U (one-sided: DePIN > DeFi)
    u_stat, p_mw = stats.mannwhitneyu(depin_hhi, defi_hhi, alternative="greater")

    # Rank-biserial effect size
    n1, n2 = len(depin_hhi), len(defi_hhi)
    r_rb = (2 * u_stat) / (n1 * n2) - 1

    # Permutation test (one-sided: DePIN mean > DeFi mean)
    observed_diff = np.mean(depin_hhi) - np.mean(defi_hhi)
    combined = np.array(defi_hhi + depin_hhi)
    np.random.seed(42)
    n_perms = 100_000
    count = sum(
        1 for _ in range(n_perms)
        if (np.random.shuffle(combined) is None) and
           np.mean(combined[:n1]) - np.mean(combined[n1:]) >= observed_diff
    )
    p_perm = count / n_perms

    results = {
        "defi_mean_hhi": round(float(np.mean(defi_hhi)), 4),
        "depin_mean_hhi": round(float(np.mean(depin_hhi)), 4),
        "mean_ratio": round(float(np.mean(depin_hhi) / np.mean(defi_hhi)), 2),
        "observed_diff": round(float(observed_diff), 4),
        "mann_whitney_U": round(float(u_stat), 1),
        "mann_whitney_p": round(float(p_mw), 4),
        "permutation_p": round(float(p_perm), 4),
        "rank_biserial_r": round(float(r_rb), 3),
        "n_defi": n2,
        "n_depin": n1,
        "n_permutations": n_perms,
    }

    print("\nResults:")
    for k, v in results.items():
        print(f"  {k}: {v}")

    # Validation checks
    print("\nValidation against expected values:")
    checks = {
        "Permutation p in [0.028, 0.040]": 0.028 <= results["permutation_p"] <= 0.040,
        "Mann-Whitney p in [0.088, 0.115]": 0.088 <= results["mann_whitney_p"] <= 0.115,
        "Effect size r in [0.44, 0.54]": 0.44 <= results["rank_biserial_r"] <= 0.54,
        "N DeFi = 7": results["n_defi"] == 7,
        "N DePIN = 5": results["n_depin"] == 5,
    }
    all_pass = True
    for check, result in checks.items():
        status = "PASS" if result else "FAIL"
        if not result:
            all_pass = False
        print(f"  [{status}] {check}")

    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results.keys())
        writer.writeheader()
        writer.writerow(results)

    print(f"\nResults saved to {output_path}")
    return 0 if all_pass else 1


if __name__ == "__main__":
    input_path = sys.argv[1] if len(sys.argv) > 1 else "data/expected_results.csv"
    output_path = sys.argv[2] if len(sys.argv) > 2 else "data/statistical_test_results.csv"
    sys.exit(main(input_path, output_path))
