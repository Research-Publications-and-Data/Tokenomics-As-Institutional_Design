#!/usr/bin/env python3
"""B2 voting-HHI full-history + trajectory: ONE-COMMAND REPRODUCTION of Table 6b and the
Section 4.5.4.2 trajectory mini-table / Figure 7.

    python3 b2_voting_timeseries_reproduce_2026-06-03.py

Self-contained: reads the committed source files in this directory (no /tmp, no live API).

Reproduces:
  (1) TABLE 6b: for the 12 Table-6 protocols with a same-surface full-history pool, the
      full-history pooled voting HHI from voting_hhi_full_history_2026-05-28.csv (Snapshot
      pooled column for the 7 Snapshot-surfaced protocols; Tally-delegate column for the 5
      Tally-surfaced) paired with the published 12-month Table-6 value, the per-protocol
      delta, the Spearman rank correlation, and the amplify/disperse-flip check.
  (2) SECTION 4.5.4.2 TRAJECTORY: per-period HHI min/median/max for ALGO (15 governance
      periods), GEOD (9 GIPs), HNT (47 proposals, pre/post HIP-141), and the DRIFT
      cross-sectional median (no dated series).

INPUTS (committed alongside this script):
  voting_hhi_full_history_2026-05-28.csv   34-protocol same-surface pooled voting HHI
  ALGO_voting_hhi_series.json              15 governance periods (commitment-weight HHI)
  GEOD_voting_hhi_series.json              9 GIPs (veNFT vote-weight HHI)
  HNT_per_proposal_turnout.csv             47 proposals (per-owner HHI; era pre/post HIP-141)
  DRIFT_full_corpus_onchain.json           10 substantive proposals (cross-sectional)
"""
import csv
import json
import math
import os
import statistics as st

HERE = os.path.dirname(os.path.abspath(__file__))

# Published Table 6 12-month voting HHI + the CSV surface to source the full-history value.
TABLE6 = {
    "DIMO": (0.228, "snapshot"), "Lido": (0.050, "snapshot"), "WeatherXM": (0.556, "snapshot"),
    "Compound": (0.089, "snapshot"), "Arbitrum": (0.038, "snapshot"), "Gnosis": (0.104, "snapshot"),
    "Synthetix": (0.095, "snapshot"),
    "Aave": (0.058, "tally_delegate"), "Uniswap": (0.027, "tally_delegate"),
    "Optimism": (0.033, "tally_delegate"), "GMX": (0.057, "tally_delegate"), "ENS": (0.022, "tally_delegate"),
}
# CSV row symbol per protocol
SYM = {"DIMO": "DIMO", "Lido": "LDO", "WeatherXM": "WXM", "Compound": "COMP", "Arbitrum": "ARB",
       "Gnosis": "GNO", "Synthetix": "SNX", "Aave": "AAVE", "Uniswap": "UNI", "Optimism": "OP",
       "GMX": "GMX", "ENS": "ENS"}
# Holding HHI (Table 3) for the amplify/disperse-flip check, derived from the Table 6 ratios
HOLDING = {"DIMO": 0.0251, "Lido": 0.0079, "WeatherXM": 0.146, "Compound": 0.0090, "Arbitrum": 0.0123,
           "Gnosis": 0.0400, "Synthetix": 0.0170, "Aave": 0.0132, "Uniswap": 0.0100, "Optimism": 0.0089,
           "GMX": 0.0655, "ENS": 0.0489}


def spearman(a, b):
    def ranks(x):
        order = sorted(range(len(x)), key=lambda i: x[i])
        r = [0] * len(x)
        for rank, i in enumerate(order):
            r[i] = rank + 1
        return r
    ra, rb = ranks(a), ranks(b)
    n = len(a)
    dsq = sum((ra[i] - rb[i]) ** 2 for i in range(n))
    return 1 - 6 * dsq / (n * (n * n - 1))


def table6b():
    rows = {r["symbol"]: r for r in csv.DictReader(open(os.path.join(HERE, "voting_hhi_full_history_2026-05-28.csv")))}
    print("=" * 78)
    print("TABLE 6b: full-history pooled voting HHI vs 12-month (same surface)")
    print("=" * 78)
    print(f"  {'protocol':10} {'surface':15} {'12mo':>8} {'full-hist':>10} {'delta':>8}  class")
    twelve, full = [], []
    flips = 0
    for p, (v12, surf) in TABLE6.items():
        r = rows[SYM[p]]
        col = "snapshot_pooled_hhi" if surf == "snapshot" else "tally_delegate_hhi"
        vf = round(float(r[col]), 4)
        twelve.append(v12); full.append(vf)
        c12 = "amplify" if v12 / HOLDING[p] > 1.0 else "disperse"
        cf = "amplify" if vf / HOLDING[p] > 1.0 else "disperse"
        flips += (c12 != cf)
        print(f"  {p:10} {surf:15} {v12:>8.3f} {vf:>10.4f} {vf-v12:>+8.4f}  {cf}{'  FLIP!' if c12!=cf else ''}")
    rho = spearman(twelve, full)
    mad = st.mean(abs(f - t) for f, t in zip(full, twelve))
    print(f"\n  Spearman rho (12mo vs full-history, n={len(twelve)}) = {rho:.3f}")
    print(f"  mean |delta| = {mad:.4f}; amplify/disperse flips = {flips}")
    print("  6 protocols with NO same-surface full-history pool: DRIFT, HNT, JUP (Solana surface);")
    print("  Bittensor, Polkadot, Livepeer (structurally point-in-time). Retain Table 6 classification.")


def trajectory():
    print("\n" + "=" * 78)
    print("SECTION 4.5.4.2: per-period voting-HHI trajectories")
    print("=" * 78)
    algo = [r["hhi_commitment_weight"] for r in json.load(open(os.path.join(HERE, "ALGO_voting_hhi_series.json")))["per_period_hhi_series"]]
    geod = [r["hhi"] for r in json.load(open(os.path.join(HERE, "GEOD_voting_hhi_series.json")))["per_proposal_hhi_series"]]
    hnt = []
    for r in csv.DictReader(open(os.path.join(HERE, "HNT_per_proposal_turnout.csv"))):
        try:
            h = float(r.get("per_owner_hhi_markers_only", "") or "nan"); nv = int(float(r.get("n_distinct_voters", "") or 0))
        except ValueError:
            continue
        if h == h and nv >= 5:
            hnt.append((h, r.get("era", "")))
    hnt_pre = [h for h, e in hnt if "post" not in e.lower()]
    hnt_post = [h for h, e in hnt if "post" in e.lower()]
    for name, s in (("ALGO", algo), ("GEOD", geod)):
        print(f"  {name:6} N={len(s):2}  min={min(s):.4f}  median={st.median(s):.4f}  max={max(s):.4f}")
    print(f"  HNT    N={len(hnt)}  pre-HIP-141 (n={len(hnt_pre)}): median={st.median(hnt_pre):.4f}, min={min(hnt_pre):.4f}, max={max(hnt_pre):.4f}")
    print(f"               post-HIP-141 (n={len(hnt_post)}): median={st.median(hnt_post):.4f} (turnout-collapse artifact)")
    drift = json.load(open(os.path.join(HERE, "DRIFT_full_corpus_onchain.json")))
    print(f"  DRIFT  aggregated per-signer HHI = {drift.get('aggregated_hhi_max_weight','n/a')} (cross-sectional; no dated series; per-proposal median 0.266)")


def main():
    table6b()
    trajectory()
    print("\n[done] Table 6b + trajectory reproduced; no /tmp, no live-API.")


if __name__ == "__main__":
    main()
