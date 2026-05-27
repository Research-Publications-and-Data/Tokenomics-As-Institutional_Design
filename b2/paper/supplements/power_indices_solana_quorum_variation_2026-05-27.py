"""
B2 R3 Phase 1 closure: Solana SS (JUP from Dune setvote; HNT/DRIFT from holder-proxy)
+ quorum-variation extension 0.33-0.75 across full N=14.

Inputs:
- /tmp/jup_voters_2026-05-27.json: 100 JUP voters with max_weight from
  jupiter_solana.govern_call_setvote 12-month window (Dune query 7585115)
- data/raw/holder_lists/HNT_holders.csv (top-100 by balance; VSR-unmultiplied proxy)
- data/raw/holder_lists/DRIFT_holders.csv (top-100; VSR-unmultiplied proxy)
- data/raw/tally_delegates.csv (7 protocols: AAVE, COMP, UNI, ARB, OP, GMX, ENS)
- data/raw/snapshot_votes.csv (6 protocols: UNI, COMP, LDO, DIMO, WXM, ARB)

Methodology notes:
- JUP: per-signer max-weight aggregation across all setvote calls in 12-month window;
  consistent with S11/S14 Snapshot methodology
- HNT, DRIFT: top-100 token holder balance used as SS input weight (VSR-unmultiplied
  baseline; actual VSR weight = balance × lockup_multiplier where multiplier ranges
  1-4x per S12 methodology). This UNDERESTIMATES SS amplification compared to actual
  VSR-multiplier-applied weights. Documented as approximation pending Helius RPC
  VSR position-state parsing (next-cycle work; Helius API key provided 2026-05-27).
- Quorum-variation: 0.33, 0.40, 0.50, 0.60, 0.67, 0.75 (S11 quorum_variation precedent)

Outputs:
- power_indices_n14_full_2026-05-27.csv: per-protocol per-quorum SS-HHI
- power_indices_quorum_variation_n14_2026-05-27.csv: quorum × protocol matrix

Author: Claude Code session 2026-05-27 (PID 4300).
"""

import csv
import json
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy import stats

REPO = Path("/Users/zach/Tokenomics-As-Institutional_Design")
DATA_RAW = REPO / "data/raw"
OUT_DIR = REPO / "b2/paper/supplements"


def load_tally():
    delegates = defaultdict(list)
    with (DATA_RAW / "tally_delegates.csv").open() as f:
        for row in csv.DictReader(f):
            sym = row["symbol"]
            try:
                votes = float(row["votes_count"])
            except (ValueError, KeyError):
                continue
            if votes > 0:
                delegates[sym].append((row["address"], votes))
    return delegates


def load_snapshot():
    voter_max = defaultdict(lambda: defaultdict(float))
    with (DATA_RAW / "snapshot_votes.csv").open() as f:
        for row in csv.DictReader(f):
            sym = row["symbol"]
            voter = row["voter"]
            try:
                vp = float(row["voting_power"])
            except (ValueError, KeyError):
                continue
            if vp > voter_max[sym][voter]:
                voter_max[sym][voter] = vp
    return {s: [(v, w) for v, w in m.items() if w > 0] for s, m in voter_max.items()}


def load_jup():
    with open("/tmp/jup_voters_2026-05-27.json") as f:
        rows = json.load(f)
    return [(r["voter"], r["max_weight"]) for r in rows if r["max_weight"] > 0]


def load_holder_as_voter_proxy(token):
    """Use token holder balance as SS voter weight (VSR-unmultiplied proxy)."""
    path = DATA_RAW / "holder_lists" / f"{token}_holders.csv"
    if not path.exists():
        return []
    out = []
    with path.open() as f:
        for row in csv.DictReader(f):
            addr = row.get("address") or row.get("owner")
            try:
                bal = float(row.get("balance", 0) or 0)
            except (ValueError, KeyError):
                bal = 0
            if bal > 0:
                out.append((addr, bal))
    out.sort(key=lambda x: -x[1])
    return out[:100]


def ss_montecarlo(weights, n_perms=20000, quorum=0.5, seed=42):
    weights = np.array(weights, dtype=float)
    threshold = weights.sum() * quorum
    n = len(weights)
    pivotal = np.zeros(n, dtype=int)
    rng = np.random.default_rng(seed=seed)
    for _ in range(n_perms):
        perm = rng.permutation(n)
        c = 0.0
        for idx in perm:
            c += weights[idx]
            if c >= threshold:
                pivotal[idx] += 1
                break
    return pivotal / n_perms


def bz_montecarlo(weights, n_samples=5000, quorum=0.5, seed=42):
    weights = np.array(weights, dtype=float)
    threshold = weights.sum() * quorum
    n = len(weights)
    swing = np.zeros(n, dtype=int)
    rng = np.random.default_rng(seed=seed + 1)
    for _ in range(n_samples):
        mask = rng.integers(0, 2, size=n).astype(bool)
        cw = weights[mask].sum()
        for i in range(n):
            if mask[i]:
                if cw >= threshold and (cw - weights[i]) < threshold:
                    swing[i] += 1
            else:
                if cw < threshold and (cw + weights[i]) >= threshold:
                    swing[i] += 1
    t = swing.sum()
    return swing / t if t > 0 else np.zeros(n)


def main():
    tally = load_tally()
    snap = load_snapshot()
    jup_voters = load_jup()
    hnt_proxy = load_holder_as_voter_proxy("HNT")
    drift_proxy = load_holder_as_voter_proxy("DRIFT")

    # Build full N=14 list
    protocols = []
    for sym in ["AAVE", "COMP", "UNI", "ARB", "OP", "GMX", "ENS"]:
        weights = [w for _, w in tally.get(sym, [])][:100]
        if weights:
            protocols.append((sym, "tally", weights))
    for sym in ["UNI", "COMP", "LDO", "DIMO", "WXM", "ARB"]:
        vlist = sorted(snap.get(sym, []), key=lambda x: -x[1])[:100]
        weights = [w for _, w in vlist]
        if len(weights) >= 2:
            protocols.append((sym, "snapshot", weights))
    # Solana
    protocols.append(("JUP", "solana_setvote", [w for _, w in jup_voters][:100]))
    protocols.append(("HNT", "solana_holder_proxy", [w for _, w in hnt_proxy]))
    protocols.append(("DRIFT", "solana_holder_proxy", [w for _, w in drift_proxy]))

    print(f"Total protocols computed: {len(protocols)}")
    print()

    # First: 0.50 quorum baseline (full N=14)
    print("=" * 90)
    print(f"Baseline (quorum=0.50) full N={len(protocols)}")
    print("=" * 90)
    print(f"{'Protocol':<22} {'N':<5} {'Share_HHI':<10} {'SS_HHI':<10} {'BZ_HHI':<10} {'SS_top1':<10} {'SS-share_pp':<12}")
    print("-" * 90)

    baseline_results = []
    for sym, source, weights in protocols:
        if len(weights) < 2:
            print(f"{sym} ({source}): TOO_FEW")
            continue
        ss = ss_montecarlo(weights, n_perms=20000, quorum=0.5)
        bz = bz_montecarlo(weights, n_samples=5000, quorum=0.5)
        share = np.array(weights, dtype=float)
        share = share / share.sum()
        r = {
            "protocol": sym, "source": source, "n": len(weights),
            "share_hhi": float((share * share).sum()),
            "ss_hhi": float((ss * ss).sum()),
            "bz_hhi": float((bz * bz).sum()),
            "ss_top1": float(ss.max()),
            "share_top1": float(share.max()),
            "ss_share_pp": float((ss.max() - share.max()) * 100),
        }
        baseline_results.append(r)
        label = f"{sym} ({source[:12]})"
        print(f"{label:<22} {r['n']:<5} {r['share_hhi']:<10.5f} {r['ss_hhi']:<10.5f} "
              f"{r['bz_hhi']:<10.5f} {r['ss_top1']:<10.5f} {r['ss_share_pp']:+12.2f}")

    # Correlation
    share_h = [r["share_hhi"] for r in baseline_results]
    ss_h = [r["ss_hhi"] for r in baseline_results]
    bz_h = [r["bz_hhi"] for r in baseline_results]
    ps = stats.pearsonr(share_h, ss_h)
    sp = stats.spearmanr(share_h, ss_h)
    pb = stats.pearsonr(share_h, bz_h)
    print()
    print(f"=== N={len(baseline_results)} extended sample (7 Tally + 6 Snapshot + 3 Solana) ===")
    print(f"  Pearson r (Share-HHI vs SS-HHI): {ps.statistic:.4f} (p={ps.pvalue:.2e})")
    print(f"  Spearman rho:                    {sp.statistic:.4f} (p={sp.pvalue:.2e})")
    print(f"  Pearson r (Share-HHI vs BZ-HHI): {pb.statistic:.4f}")
    print(f"  Acceptance threshold > 0.95: {'PASS' if ps.statistic > 0.95 else 'FAIL'}")

    # Write baseline CSV
    with (OUT_DIR / "power_indices_n14_full_2026-05-27.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["protocol", "source", "n", "share_hhi", "share_top1", "ss_hhi",
                    "ss_top1", "bz_hhi", "ss_share_pp"])
        for r in baseline_results:
            w.writerow([r["protocol"], r["source"], r["n"],
                        f"{r['share_hhi']:.6f}", f"{r['share_top1']:.6f}",
                        f"{r['ss_hhi']:.6f}", f"{r['ss_top1']:.6f}",
                        f"{r['bz_hhi']:.6f}", f"{r['ss_share_pp']:+.4f}"])

    # QUORUM VARIATION: 0.33-0.75 across all protocols
    print()
    print("=" * 90)
    print(f"Quorum-variation across N={len(protocols)} (SS-HHI per quorum threshold)")
    print("=" * 90)
    quorums = [0.33, 0.40, 0.50, 0.60, 0.67, 0.75]
    print(f"{'Protocol':<22} " + " ".join(f"{f'q={q}':<10}" for q in quorums))
    print("-" * (22 + 11 * len(quorums)))

    quorum_results = []
    for sym, source, weights in protocols:
        if len(weights) < 2:
            continue
        row = {"protocol": sym, "source": source, "n": len(weights)}
        for q in quorums:
            ss = ss_montecarlo(weights, n_perms=10000, quorum=q, seed=42 + int(q * 100))
            row[f"ss_hhi_q{q}"] = float((ss * ss).sum())
            row[f"ss_top1_q{q}"] = float(ss.max())
        quorum_results.append(row)
        label = f"{sym} ({source[:12]})"
        vals = " ".join(f"{row[f'ss_hhi_q{q}']:<10.5f}" for q in quorums)
        print(f"{label:<22} {vals}")

    # Write quorum variation CSV
    with (OUT_DIR / "power_indices_quorum_variation_n14_2026-05-27.csv").open("w", newline="") as f:
        w = csv.writer(f)
        cols = ["protocol", "source", "n"]
        for q in quorums:
            cols.extend([f"ss_hhi_q{q}", f"ss_top1_q{q}"])
        w.writerow(cols)
        for row in quorum_results:
            out = [row["protocol"], row["source"], row["n"]]
            for q in quorums:
                out.extend([f"{row[f'ss_hhi_q{q}']:.6f}", f"{row[f'ss_top1_q{q}']:.6f}"])
            w.writerow(out)

    # Rank-stability analysis: how does the rank-order of protocols change across quorums?
    print()
    print("=== Rank stability across quorum thresholds ===")
    for q in quorums:
        ranked = sorted(quorum_results, key=lambda r: -r[f"ss_hhi_q{q}"])
        ordering = [f"{r['protocol']}-{r['source'][:3]}" for r in ranked[:5]]
        print(f"  q={q}: top-5 SS-HHI: {' > '.join(ordering)}")

    print(f"\nWrote: power_indices_n14_full_2026-05-27.csv ({len(baseline_results)} rows)")
    print(f"Wrote: power_indices_quorum_variation_n14_2026-05-27.csv ({len(quorum_results)} rows × {len(quorums)} quorums)")


if __name__ == "__main__":
    main()
