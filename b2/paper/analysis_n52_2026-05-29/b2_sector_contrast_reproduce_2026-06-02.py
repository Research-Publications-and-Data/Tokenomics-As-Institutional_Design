#!/usr/bin/env python3
"""B2 sector contrast (DePIN vs DeFi): ONE-COMMAND REPRODUCTION of the three
staking-treatment effect sizes that anchor the of-record headline.

    python b2_sector_contrast_reproduce_2026-06-02.py

Reproduces, from the committed balanced-30 per-protocol holding-HHI vectors
(sector_contrast_hhi_vectors_2026-06-02.csv), the Section 4.6.2 staking-treatment
triple, with no /tmp dependency and no cross-clone or live-API call:

  - HEADLINE  voter-inclusive staking pass-through : Cohen's d = 0.65, Mann-Whitney
              p = 0.028; all 30 leave-one-out folds significant; the mean-based
              permutation is marginal (p approximately 0.08), the heavy-tail
              signature of the single concentrated DeFi-side vote-escrow bloc (CRV)
  - ROBUSTNESS uniform staking-aggregation exclusion: Cohen's d = 0.75, Mann-Whitney
              p = 0.018, label-permutation p = 0.009, all 30 leave-one-out folds
              significant (per-fold p 0.006 to 0.031, d 0.68 to 0.92), bootstrap d
              95% interval [0.40, 1.52]
  - INFLATED  earlier inconsistent (complete-CEX) treatment, reported as inflated
              rather than as the headline: Cohen's d = 1.05, Mann-Whitney p = 0.011

INPUT (committed; no /tmp, no Nansen label list):
  sector_contrast_hhi_vectors_2026-06-02.csv
    Per-protocol post-exclusion holding HHI for the balanced 15-DePIN / 15-DeFi
    governance-token sample under each of the three staking treatments. These are
    aggregate per-protocol statistics of the same class as the published Table 3
    HHIs (the pass-through column differs from Table 3 only in that staking-
    aggregation contracts are re-attributed to their measured underlying stakers
    rather than excluded). The upstream derivation of these HHIs from raw top-1000
    holder lists plus the protocol-controlled-address exclusion typology (which uses
    third-party entity labels under their terms of use) is documented in Section 3.8
    and Supplementary File S13; this script reproduces the sector-level statistics
    from the per-protocol HHIs.

Outputs a reconciliation table against the of-record values.
"""
import csv
import math
import os

import numpy as np
from scipy import stats as ss

HERE = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.join(HERE, "sector_contrast_hhi_vectors_2026-06-02.csv")

TREATMENTS = [
    ("hhi_passthrough", "HEADLINE  voter-inclusive pass-through", "d=0.65 p=0.028 perm~0.08"),
    ("hhi_uniform_exclusion", "ROBUSTNESS uniform staking-agg exclusion", "d=0.75 p=0.018 perm=0.009"),
    ("hhi_inflated_completecex", "INFLATED  complete-CEX (not the headline)", "d=1.05 p=0.011"),
]


def cohens_d(a, b):
    n1, n2 = len(a), len(b)
    sp = math.sqrt(((n1 - 1) * np.var(a, ddof=1) + (n2 - 1) * np.var(b, ddof=1)) / (n1 + n2 - 2))
    return (np.mean(a) - np.mean(b)) / sp


def load():
    depin, defi = {}, {}
    with open(CSV) as fh:
        for r in csv.DictReader(fh):
            (depin if r["sector"] == "DePIN" else defi)[r["token"]] = r
    assert len(depin) == 15 and len(defi) == 15, (len(depin), len(defi))
    return depin, defi


def battery(depin, defi, col):
    A = [float(r[col]) for r in depin.values()]
    B = [float(r[col]) for r in defi.values()]
    u, p = ss.mannwhitneyu(A, B, alternative="two-sided")
    d = cohens_d(A, B)
    # leave-one-out over all 30 protocols
    tokvals = [(t, float(r[col]), "DePIN") for t, r in depin.items()] + \
              [(t, float(r[col]), "DeFi") for t, r in defi.items()]
    loo_p, loo_d = [], []
    for drop, _, _ in tokvals:
        aa = [v for t, v, s in tokvals if s == "DePIN" and t != drop]
        bb = [v for t, v, s in tokvals if s == "DeFi" and t != drop]
        _, pp = ss.mannwhitneyu(aa, bb, alternative="two-sided")
        loo_p.append(pp); loo_d.append(cohens_d(aa, bb))
    # label-permutation on the mean difference (seed 42, 100k), matches the battery
    rng = np.random.default_rng(42)
    pool = np.array(A + B); n1 = len(A); obs = abs(np.mean(A) - np.mean(B)); cnt = 0
    for _ in range(100000):
        rng.shuffle(pool)
        cnt += abs(np.mean(pool[:n1]) - np.mean(pool[n1:])) >= obs
    perm = cnt / 100000
    # bootstrap d 95% percentile interval (seed 7, 10k), matches the battery
    rng = np.random.default_rng(7); ds = []
    for _ in range(10000):
        aa = rng.choice(A, len(A), replace=True); bb = rng.choice(B, len(B), replace=True)
        sp = math.sqrt(((len(aa) - 1) * np.var(aa, ddof=1) + (len(bb) - 1) * np.var(bb, ddof=1)) / (len(aa) + len(bb) - 2))
        if sp > 0: ds.append((np.mean(aa) - np.mean(bb)) / sp)
    lo, hi = np.percentile(ds, [2.5, 97.5])
    return dict(p=p, d=d, depin_mean=np.mean(A), defi_mean=np.mean(B),
                loo_sig=sum(1 for x in loo_p if x < 0.05), loo_n=len(loo_p),
                loo_p=(min(loo_p), max(loo_p)), loo_d=(min(loo_d), max(loo_d)),
                perm=perm, boot=(lo, hi))


def main():
    depin, defi = load()
    print("=" * 78)
    print("B2 sector contrast (balanced 15 DePIN vs 15 DeFi) reproduced from committed HHI vectors")
    print("=" * 78)
    for col, label, expect in TREATMENTS:
        r = battery(depin, defi, col)
        print(f"\n{label}   (expect {expect})")
        print(f"  DePIN mean={r['depin_mean']:.4f}  DeFi mean={r['defi_mean']:.4f}  ratio={r['depin_mean']/r['defi_mean']:.2f}")
        print(f"  Mann-Whitney p={r['p']:.4f}   Cohen d={r['d']:+.3f}")
        print(f"  LOO: {r['loo_sig']}/{r['loo_n']} significant at p<0.05; "
              f"p range [{r['loo_p'][0]:.4f}, {r['loo_p'][1]:.4f}]; d range [{r['loo_d'][0]:.3f}, {r['loo_d'][1]:.3f}]")
        print(f"  label-permutation p (mean diff, 100k) = {r['perm']:.4f}")
        print(f"  bootstrap d 95% interval (10k) = [{r['boot'][0]:.3f}, {r['boot'][1]:.3f}]")
    print("\n[done] sector-contrast triple reproduced; no /tmp, no cross-clone, no live-API.")


if __name__ == "__main__":
    main()
