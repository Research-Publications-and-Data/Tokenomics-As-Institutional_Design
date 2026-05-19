"""
Extended power-indices analysis (2026-05-19 future-work fill-in):

1. Banzhaf power index (Banzhaf 1965) via Monte Carlo for Tally-sourced
   voting-layer protocols, complementing the Shapley-Shubik analysis
   in power_indices_2026-05-19.py.

2. Shapley-Shubik under varying quorum thresholds (33%, 50%, 60%, 67%,
   75%) to test the theoretical prediction in Section 4.8 that pivotal-
   power concentration diverges from voting-HHI under non-simple-
   majority quorum rules that bind near the median of the delegate-
   weight distribution.

Method:
- Banzhaf via Monte Carlo: for each of 20K random subsets of voters
  (each voter independently included w.p. 0.5), find swing voters
  (voters whose removal would flip the coalition's win/loss state).
  A voter's Banzhaf power = fraction of subsets in which they are
  swing. Normalize so power-indices sum to 1.
- Shapley-Shubik under varying quorum (20K permutations per quorum).
- Computed for 5 Tally protocols: AAVE, ARB, COMP, OP, UNI.

Outputs:
- banzhaf_indices_2026-05-19.csv: per-voter Banzhaf values
- power_indices_quorum_variation_2026-05-19.csv: SS power per
  protocol across 5 quorum thresholds

Run: python3 power_indices_extended_2026-05-19.py
"""

import csv
from collections import defaultdict
from pathlib import Path
import numpy as np
from scipy import stats


REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
DATA_DIR = REPO_ROOT / "data" / "raw"


def load_tally_delegates():
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
    hhi = {}
    with (DATA_DIR / "voting_hhi.csv").open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            sym = row["symbol"]
            src = row["source"]
            if sym in hhi and hhi[sym][0] == "tally":
                continue
            hhi[sym] = (src, float(row["voting_hhi"]), float(row["voting_top1_pct"]))
    return hhi


def shapley_shubik_montecarlo(weights, n_perms=20000, quorum=0.5, seed=42):
    """Monte Carlo Shapley-Shubik. Returns per-voter power indices."""
    weights = np.array(weights, dtype=float)
    total = weights.sum()
    threshold = total * quorum
    n = len(weights)
    pivotal_counts = np.zeros(n, dtype=int)
    rng = np.random.default_rng(seed=seed)
    for _ in range(n_perms):
        perm = rng.permutation(n)
        cumsum = 0.0
        for idx in perm:
            cumsum += weights[idx]
            if cumsum > threshold:
                pivotal_counts[idx] += 1
                break
    return (pivotal_counts / n_perms).tolist()


def banzhaf_montecarlo(weights, n_subsets=20000, quorum=0.5, seed=42):
    """Monte Carlo Banzhaf. Each voter is a swing voter in a subset if
    removing them flips the coalition's win/loss state. Banzhaf power =
    fraction of subsets in which voter is swing. Normalized so sum = 1."""
    weights = np.array(weights, dtype=float)
    total = weights.sum()
    threshold = total * quorum
    n = len(weights)
    swing_counts = np.zeros(n, dtype=int)
    rng = np.random.default_rng(seed=seed)
    for _ in range(n_subsets):
        inclusion = rng.random(n) < 0.5
        coalition_sum = float((weights * inclusion).sum())
        coalition_wins = coalition_sum > threshold
        for i in range(n):
            if inclusion[i]:
                if (coalition_sum - weights[i]) <= threshold and coalition_wins:
                    swing_counts[i] += 1
            else:
                if (coalition_sum + weights[i]) > threshold and not coalition_wins:
                    swing_counts[i] += 1
    raw = swing_counts.astype(float)
    s = raw.sum()
    if s > 0:
        return (raw / s).tolist()
    return raw.tolist()


def hhi_of_distribution(values):
    """Herfindahl of normalized distribution."""
    arr = np.array(values, dtype=float)
    s = arr.sum()
    if s == 0:
        return 0.0
    shares = arr / s
    return float(np.sum(shares ** 2))


def main():
    delegates = load_tally_delegates()
    voting_hhi = load_voting_hhi()

    summary_quorum = []
    banzhaf_rows = []

    for protocol in sorted(delegates.keys()):
        delegs = sorted(delegates[protocol], key=lambda x: -x[1])[:100]
        addresses = [d[0] for d in delegs]
        weights = [d[1] for d in delegs]
        src, vhhi, vtop1 = voting_hhi.get(protocol, ("none", 0.0, 0.0))

        # Shapley-Shubik at varying quorum thresholds
        quorum_results = {}
        for q in [0.33, 0.50, 0.60, 0.67, 0.75]:
            ss = shapley_shubik_montecarlo(weights, n_perms=20000, quorum=q, seed=42)
            ss_hhi = hhi_of_distribution(ss)
            top1_ss = float(max(ss)) if ss else 0.0
            quorum_results[q] = (ss_hhi, top1_ss)
            summary_quorum.append({
                "protocol": protocol,
                "quorum": q,
                "ss_hhi": f"{ss_hhi:.4f}",
                "ss_top1_pct": f"{top1_ss*100:.2f}",
                "voting_hhi": f"{vhhi:.4f}",
                "voting_top1_pct": f"{vtop1:.2f}",
                "ratio_ss_to_voting_hhi": f"{ss_hhi/vhhi:.3f}" if vhhi > 0 else "n/a",
            })
        print(f"\n{protocol} (voting HHI {vhhi:.4f}, top-1 voting share {vtop1:.2f}%):")
        for q in [0.33, 0.50, 0.60, 0.67, 0.75]:
            ss_hhi, top1_ss = quorum_results[q]
            ratio = ss_hhi/vhhi if vhhi > 0 else 0
            print(f"  quorum={q:.2f}: SS-HHI={ss_hhi:.4f}, top-1 SS={top1_ss*100:.2f}%, ratio SS/voting-HHI={ratio:.3f}")

        # Banzhaf at simple-majority quorum
        bz = banzhaf_montecarlo(weights, n_subsets=20000, quorum=0.5, seed=42)
        bz_hhi = hhi_of_distribution(bz)
        bz_top1 = float(max(bz)) if bz else 0.0
        print(f"  Banzhaf (q=0.50): BZ-HHI={bz_hhi:.4f}, top-1 BZ={bz_top1*100:.2f}%")

        ranked = sorted(zip(addresses, weights, bz), key=lambda x: -x[2])
        for addr, w, p in ranked[:10]:
            banzhaf_rows.append({
                "protocol": protocol,
                "address": addr,
                "votes_count": w,
                "banzhaf_power": p,
            })

    # Aggregate analysis: does SS-HHI / voting-HHI ratio diverge from 1.0
    # as quorum moves away from 0.50?
    print("\n=== Ratio SS-HHI / voting-HHI by quorum (mean across 5 protocols) ===")
    by_quorum = defaultdict(list)
    for r in summary_quorum:
        if r["ratio_ss_to_voting_hhi"] != "n/a":
            by_quorum[r["quorum"]].append(float(r["ratio_ss_to_voting_hhi"]))
    for q, ratios in sorted(by_quorum.items()):
        print(f"  quorum={q:.2f}: mean ratio = {np.mean(ratios):.3f}, range [{min(ratios):.3f}, {max(ratios):.3f}]")

    # Write outputs
    out_quorum = Path(__file__).parent / "power_indices_quorum_variation_2026-05-19.csv"
    with out_quorum.open("w", newline="") as f:
        if summary_quorum:
            w = csv.DictWriter(f, fieldnames=list(summary_quorum[0].keys()))
            w.writeheader()
            for r in summary_quorum:
                w.writerow(r)
    print(f"\nWrote: {out_quorum}")

    out_bz = Path(__file__).parent / "banzhaf_indices_2026-05-19.csv"
    with out_bz.open("w", newline="") as f:
        if banzhaf_rows:
            w = csv.DictWriter(f, fieldnames=list(banzhaf_rows[0].keys()))
            w.writeheader()
            for r in banzhaf_rows:
                w.writerow(r)
    print(f"Wrote: {out_bz}")


if __name__ == "__main__":
    main()
