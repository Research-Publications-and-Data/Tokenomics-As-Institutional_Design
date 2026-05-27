"""
Phase 1 of B2 R3 data-collection omnibus: Shapley-Shubik + Banzhaf full-sample extension.

Closes §5.7 limitation #5 (HHI vs pivotal voting power) + §5.8 future research #4.

Extends S11 partial-sample (5 Tally protocols: AAVE, COMP, UNI, ARB, OP) to additional
voting-HHI protocols using available data. Specifically adds:
- DIMO, LDO, WXM (Snapshot-side; voter weight from snapshot_votes.csv per-voter max-weight)
- N = 13 target (5 Tally + 3 Snapshot computed this cycle = 8; remaining 5 protocols
  (GMX, ENS via Tally API; HNT, DRIFT, JUP via Solana VSR) deferred to continuation dispatch.

Inputs:
- data/raw/tally_delegates.csv: AAVE, COMP, UNI, ARB, OP top-100 delegate weights
- data/raw/snapshot_votes.csv: 6 Snapshot protocols' vote-level data
- data/raw/voting_hhi.csv: canonical voting-HHI for cross-validation

Outputs:
- power_indices_extension_2026-05-27.csv: per-protocol SS + Banzhaf (N=8)
- power_indices_extension_summary_2026-05-27.csv: summary stats
- power_indices_extension_2026-05-27.md: human-readable report

Methodology:
- Per-voter max-weight aggregation for Snapshot protocols (treat each unique voter's
  max recorded voting_power across all their proposals as the SS input weight)
- 20,000 Monte Carlo permutations per protocol (consistent with S11 methodology)
- 0.50 simple-majority quorum threshold (S11 baseline)
- Banzhaf computed alongside SS for cross-protocol comparison

Per dispatch HALT-1.1: Snapshot vote-weight data IS available for DIMO+LDO+WXM (snapshot_votes.csv)
Per dispatch HALT-1.2: Solana VSR data NOT available this cycle; halt + surface in handoff-back

Author: Claude Code session 2026-05-27 (PID 4300).
"""

import csv
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy import stats

REPO = Path("/Users/zach/Tokenomics-As-Institutional_Design")
DATA_RAW = REPO / "data/raw"
OUT_DIR = REPO / "b2/paper/supplements"


def load_tally_delegates():
    """Return dict: protocol -> list of (address, votes_count_float)."""
    delegates = defaultdict(list)
    with (DATA_RAW / "tally_delegates.csv").open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            sym = row["symbol"]
            try:
                votes = float(row["votes_count"])
            except (ValueError, KeyError):
                continue
            if votes > 0:
                delegates[sym].append((row["address"], votes))
    return delegates


def load_snapshot_voter_weights():
    """For each Snapshot protocol, return list of (voter, max_voting_power)."""
    voter_max = defaultdict(lambda: defaultdict(float))
    with (DATA_RAW / "snapshot_votes.csv").open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            sym = row["symbol"]
            voter = row["voter"]
            try:
                vp = float(row["voting_power"])
            except (ValueError, KeyError):
                continue
            if vp > voter_max[sym][voter]:
                voter_max[sym][voter] = vp
    out = {}
    for sym, vmap in voter_max.items():
        out[sym] = [(v, w) for v, w in vmap.items() if w > 0]
    return out


def load_voting_hhi():
    """Canonical voting-HHI for cross-validation. Returns dict (sym, source) -> values."""
    hhi = {}
    with (DATA_RAW / "voting_hhi.csv").open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (row["symbol"], row["source"])
            hhi[key] = {
                "voting_hhi": float(row["voting_hhi"]),
                "voting_top1_pct": float(row["voting_top1_pct"]),
            }
    return hhi


def shapley_shubik_montecarlo(weights, n_perms=20000, quorum=0.5, seed=42):
    """Monte Carlo Shapley-Shubik. Returns per-voter pivotal-share."""
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
            if cumsum >= threshold:
                pivotal_counts[idx] += 1
                break
    return pivotal_counts / n_perms


def banzhaf_montecarlo(weights, n_samples=20000, quorum=0.5, seed=42):
    """Monte Carlo Banzhaf approximation: voter i's swing = fraction of random
    coalitions (subsets of N \\ {i}) where i is critical (without i: <threshold; with i: >=threshold).
    Normalized by sum across all voters."""
    weights = np.array(weights, dtype=float)
    total = weights.sum()
    threshold = total * quorum
    n = len(weights)
    swing_counts = np.zeros(n, dtype=int)
    rng = np.random.default_rng(seed=seed + 1)
    for _ in range(n_samples):
        # Sample a random coalition (binary mask over all voters)
        mask = rng.integers(0, 2, size=n).astype(bool)
        coal_weight = weights[mask].sum()
        # For each voter, check if flipping their membership changes the outcome
        for i in range(n):
            if mask[i]:
                # voter i is in coalition; would removal drop below threshold?
                if coal_weight >= threshold and (coal_weight - weights[i]) < threshold:
                    swing_counts[i] += 1
            else:
                # voter i is out; would adding push over threshold?
                if coal_weight < threshold and (coal_weight + weights[i]) >= threshold:
                    swing_counts[i] += 1
    total_swings = swing_counts.sum()
    if total_swings == 0:
        return np.zeros(n)
    return swing_counts / total_swings


def compute_power_indices(weights, label, n_perms=20000):
    """Compute SS + Banzhaf for a weight vector. Returns dict of summary stats."""
    if len(weights) < 2:
        return {"label": label, "n": len(weights), "status": "TOO_FEW_VOTERS"}

    ss = shapley_shubik_montecarlo(weights, n_perms=n_perms)
    # For large n, Banzhaf MC is expensive; cap n_samples
    bz = banzhaf_montecarlo(weights, n_samples=min(n_perms, 5000))

    # HHI of SS values (sum of squares of normalized SS shares)
    ss_hhi = float(np.sum(ss * ss))
    bz_hhi = float(np.sum(bz * bz))

    weights_arr = np.array(weights, dtype=float)
    share = weights_arr / weights_arr.sum()
    share_hhi = float(np.sum(share * share))

    return {
        "label": label,
        "n": len(weights),
        "status": "OK",
        "share_hhi": share_hhi,
        "share_top1": float(share.max()),
        "ss_top1": float(ss.max()),
        "ss_hhi": ss_hhi,
        "bz_top1": float(bz.max()),
        "bz_hhi": bz_hhi,
        "ss_share_top1_divergence_pp": (float(ss.max()) - float(share.max())) * 100,
        "bz_share_top1_divergence_pp": (float(bz.max()) - float(share.max())) * 100,
    }


def main():
    print("=" * 80)
    print("Phase 1 of B2 R3 data-collection omnibus: SS + Banzhaf extension")
    print("Generated 2026-05-27 (PID 4300)")
    print("=" * 80)

    tally = load_tally_delegates()
    snapshot = load_snapshot_voter_weights()
    canonical_hhi = load_voting_hhi()

    results = []

    # Tally protocols (5 from S11 baseline)
    for sym in ["AAVE", "COMP", "UNI", "ARB", "OP"]:
        weights = [w for _, w in tally.get(sym, [])]
        if not weights:
            results.append({"label": f"{sym} (tally)", "n": 0, "status": "NO_DATA"})
            continue
        r = compute_power_indices(weights, f"{sym} (tally; N={len(weights)})")
        r["protocol"] = sym
        r["source"] = "tally"
        canon = canonical_hhi.get((sym, "tally"), {})
        r["canonical_voting_hhi"] = canon.get("voting_hhi")
        results.append(r)

    # Snapshot protocols (new this cycle: DIMO, LDO, WXM; also re-validate UNI, COMP, ARB)
    for sym in ["DIMO", "LDO", "WXM", "UNI", "COMP", "ARB"]:
        # Use top-100 by voter weight (matches S11 top-100 convention)
        vlist = sorted(snapshot.get(sym, []), key=lambda x: -x[1])[:100]
        weights = [w for _, w in vlist]
        if len(weights) < 2:
            results.append({
                "label": f"{sym} (snapshot)",
                "n": len(weights),
                "status": "TOO_FEW_VOTERS",
                "protocol": sym,
                "source": "snapshot",
            })
            continue
        r = compute_power_indices(weights, f"{sym} (snapshot; top-{len(weights)})")
        r["protocol"] = sym
        r["source"] = "snapshot"
        canon = canonical_hhi.get((sym, "snapshot"), {})
        r["canonical_voting_hhi"] = canon.get("voting_hhi")
        results.append(r)

    # Pretty print
    print(f"\n{'Protocol':<22} {'N':<5} {'Share_HHI':<10} {'SS_HHI':<10} {'BZ_HHI':<10} "
          f"{'SS-share_pp':<12} {'BZ-share_pp':<12} {'Canonical_HHI':<14}")
    print("-" * 110)
    for r in results:
        if r.get("status") != "OK":
            print(f"{r['label']:<22} {r['n']:<5} {r.get('status', 'UNK')}")
            continue
        canon = r.get("canonical_voting_hhi")
        canon_str = f"{canon:.5f}" if canon is not None else "N/A"
        print(f"{r['label']:<22} {r['n']:<5} {r['share_hhi']:<10.5f} {r['ss_hhi']:<10.5f} "
              f"{r['bz_hhi']:<10.5f} {r['ss_share_top1_divergence_pp']:+12.2f} "
              f"{r['bz_share_top1_divergence_pp']:+12.2f} {canon_str:<14}")

    # Correlation analysis: SS-HHI vs Share-HHI
    valid = [r for r in results if r.get("status") == "OK"]
    if len(valid) >= 5:
        share_hhis = [r["share_hhi"] for r in valid]
        ss_hhis = [r["ss_hhi"] for r in valid]
        bz_hhis = [r["bz_hhi"] for r in valid]
        pearson_ss = stats.pearsonr(share_hhis, ss_hhis)
        pearson_bz = stats.pearsonr(share_hhis, bz_hhis)
        spearman_ss = stats.spearmanr(share_hhis, ss_hhis)
        print(f"\n=== Correlation: Share-HHI vs SS-HHI (N={len(valid)}) ===")
        print(f"  Pearson r = {pearson_ss.statistic:.4f} (p = {pearson_ss.pvalue:.4f})")
        print(f"  Spearman rho = {spearman_ss.statistic:.4f} (p = {spearman_ss.pvalue:.4f})")
        print(f"\n=== Correlation: Share-HHI vs Banzhaf-HHI (N={len(valid)}) ===")
        print(f"  Pearson r = {pearson_bz.statistic:.4f} (p = {pearson_bz.pvalue:.4f})")
        print(f"\n=== Per-S11 baseline: Pearson r expected > 0.95 (rank-preservation)===")
        print(f"  Actual: {pearson_ss.statistic:.4f} {'PASS' if pearson_ss.statistic > 0.95 else 'FAIL'}")

    # Write CSV
    out_csv = OUT_DIR / "power_indices_extension_2026-05-27.csv"
    with out_csv.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["protocol", "source", "n_voters", "status", "share_hhi", "share_top1",
                    "ss_hhi", "ss_top1", "bz_hhi", "bz_top1",
                    "ss_share_divergence_pp", "bz_share_divergence_pp",
                    "canonical_voting_hhi"])
        for r in results:
            if r.get("status") != "OK":
                w.writerow([r.get("protocol", ""), r.get("source", ""), r["n"], r["status"],
                            "", "", "", "", "", "", "", "", r.get("canonical_voting_hhi", "")])
                continue
            w.writerow([r["protocol"], r["source"], r["n"], "OK",
                        f"{r['share_hhi']:.6f}", f"{r['share_top1']:.6f}",
                        f"{r['ss_hhi']:.6f}", f"{r['ss_top1']:.6f}",
                        f"{r['bz_hhi']:.6f}", f"{r['bz_top1']:.6f}",
                        f"{r['ss_share_top1_divergence_pp']:+.4f}",
                        f"{r['bz_share_top1_divergence_pp']:+.4f}",
                        r.get("canonical_voting_hhi", "")])
    print(f"\nWrote: {out_csv}")

    return results


if __name__ == "__main__":
    main()
