"""
Shapley-Shubik power indices (Item 1) for Table 7 voting-layer protocols.

Inputs:
- data/raw/tally_delegates.csv: delegate-by-delegate voting weights for
  Tally-sourced protocols (AAVE, COMP, UNI, ARB, OP, MKR, ENS).
- data/raw/voting_hhi.csv: voting concentration metrics.

Method:
- Monte Carlo Shapley-Shubik computation: for each of 10,000 random
  permutations of voters, find the pivotal voter (the voter whose
  addition first crosses the simple-majority quorum). Each voter's
  Shapley-Shubik power index = fraction of permutations in which
  they are pivotal.
- Use top-100 delegates per protocol (matches voting_hhi.csv top-N).

Outputs:
- power_indices_2026-05-19.csv: per-voter Shapley-Shubik values
- Summary statistics for paragraph integration:
    Pearson r between top-1 SS power and HHI
    Spearman rho between rank-order SS and HHI

Single threshold: simple majority (50% + 1).
"""

import csv
from collections import defaultdict
from pathlib import Path
import numpy as np
from scipy import stats


REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
DATA_DIR = REPO_ROOT / "data" / "raw"


def load_tally_delegates():
    """Return dict: protocol -> list of (address, votes_count_int)."""
    delegates = defaultdict(list)
    with (DATA_DIR / "tally_delegates.csv").open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            sym = row["symbol"]
            try:
                votes = int(row["votes_count"])
            except (ValueError, KeyError):
                continue
            if votes > 0:
                delegates[sym].append((row["address"], votes))
    return delegates


def load_voting_hhi():
    """Return dict: protocol -> (source, voting_hhi, voting_top1_pct)."""
    hhi = {}
    with (DATA_DIR / "voting_hhi.csv").open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            sym = row["symbol"]
            src = row["source"]
            # Prefer tally source where both exist
            if sym in hhi and hhi[sym][0] == "tally":
                continue
            hhi[sym] = (src, float(row["voting_hhi"]), float(row["voting_top1_pct"]))
    return hhi


def shapley_shubik_montecarlo(weights, n_perms=10000, quorum=0.5):
    """Monte Carlo Shapley-Shubik power indices.
    weights: list of voter weights
    quorum: fraction of total weight needed to win (default 50%+).
    Returns: list of power indices (same length as weights)."""
    weights = np.array(weights, dtype=float)
    total = weights.sum()
    threshold = total * quorum
    n = len(weights)
    pivotal_counts = np.zeros(n, dtype=int)
    rng = np.random.default_rng(seed=42)
    for _ in range(n_perms):
        perm = rng.permutation(n)
        cumsum = 0.0
        for idx in perm:
            cumsum += weights[idx]
            if cumsum > threshold:
                pivotal_counts[idx] += 1
                break
    return (pivotal_counts / n_perms).tolist()


def main():
    delegates = load_tally_delegates()
    voting_hhi = load_voting_hhi()

    print(f"Protocols with delegate data: {sorted(delegates.keys())}")
    print(f"Protocols with voting HHI data: {sorted(voting_hhi.keys())}")
    print()

    results = []
    rows = []
    for protocol in sorted(delegates.keys()):
        delegs = sorted(delegates[protocol], key=lambda x: -x[1])
        # Use top-100 (Tally's typical N)
        delegs_top = delegs[:100]
        addresses = [d[0] for d in delegs_top]
        weights = [d[1] for d in delegs_top]
        ss_powers = shapley_shubik_montecarlo(weights, n_perms=20000)
        # Sort by SS power desc
        ranked = sorted(zip(addresses, weights, ss_powers), key=lambda x: -x[2])
        top1_ss = ranked[0][2]
        # HHI of SS powers (concentration of power)
        ss_arr = np.array(ss_powers)
        ss_hhi = float(np.sum(ss_arr ** 2))
        # Voting HHI for comparison
        src, vhhi, vtop1 = voting_hhi.get(protocol, ("none", 0.0, 0.0))
        results.append((protocol, src, vhhi, vtop1, top1_ss, ss_hhi))
        print(f"{protocol:6s} | voting HHI (top-100, {src}): {vhhi:.4f}; top-1 weight: {vtop1:.2f}% | SS-HHI: {ss_hhi:.4f}; top-1 SS: {top1_ss*100:.2f}%")

        # Per-voter rows
        for addr, w, ss in ranked[:10]:
            rows.append({
                "protocol": protocol,
                "source": src,
                "address": addr,
                "votes_count": w,
                "weight_pct": w / sum(weights) * 100,
                "shapley_shubik_power": ss,
            })

    # Correlation: voting HHI vs SS-HHI
    arr_vhhi = np.array([r[2] for r in results])
    arr_sshhi = np.array([r[5] for r in results])
    arr_top1_voting = np.array([r[3] for r in results])
    arr_top1_ss = np.array([r[4] for r in results]) * 100

    r_hhi, p_hhi = stats.pearsonr(arr_vhhi, arr_sshhi)
    rho_hhi, prho_hhi = stats.spearmanr(arr_vhhi, arr_sshhi)
    r_top1, p_top1 = stats.pearsonr(arr_top1_voting, arr_top1_ss)
    rho_top1, prho_top1 = stats.spearmanr(arr_top1_voting, arr_top1_ss)

    print(f"\n=== Voting HHI vs Shapley-Shubik HHI (N = {len(results)}) ===")
    print(f"Pearson r = {r_hhi:.4f} (p = {p_hhi:.4f})")
    print(f"Spearman rho = {rho_hhi:.4f} (p = {prho_hhi:.4f})")
    print(f"\n=== Top-1 voting share vs Top-1 SS power ===")
    print(f"Pearson r = {r_top1:.4f} (p = {p_top1:.4f})")
    print(f"Spearman rho = {rho_top1:.4f} (p = {prho_top1:.4f})")

    out_csv = Path(__file__).parent / "power_indices_2026-05-19.csv"
    with out_csv.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["protocol", "source", "address", "votes_count", "weight_pct", "shapley_shubik_power"])
        w.writeheader()
        for row in rows:
            w.writerow(row)
    print(f"\nWrote: {out_csv}")

    summary_csv = Path(__file__).parent / "power_indices_summary_2026-05-19.csv"
    with summary_csv.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["protocol", "source", "voting_hhi", "voting_top1_pct", "shapley_shubik_top1", "shapley_shubik_hhi"])
        for protocol, src, vhhi, vtop1, top1_ss, ss_hhi in results:
            w.writerow([protocol, src, f"{vhhi:.4f}", f"{vtop1:.2f}", f"{top1_ss:.4f}", f"{ss_hhi:.4f}"])
    print(f"Wrote: {summary_csv}")


if __name__ == "__main__":
    main()
