#!/usr/bin/env python3
"""B2 N=52 decision-ready re-analysis (HALT-A determination).
Read-only against clone A; writes nothing to canonical state.
Computes the headline DePIN-vs-DeFi concentration contrast at the N=40 paper
baseline and at the target sample under every open-decision scenario:
  FIL/POKT {in -> 52 / out -> 50} x GNO co-founder-Safe {excl 0.0425 / keep 0.0769} x TAO category {DePIN / Infra}
Also: per-category means, LOO robustness of the contrast, with/without-DOT sensitivity,
and the insider-allocation null (Pearson r).
"""
import csv
import numpy as np
from scipy import stats

CSV = "data/processed/regression_data_april2026.csv"
rows = list(csv.DictReader(open(CSV)))

def fnum(x):
    try: return float(x)
    except: return None

# --- base-40 (governance_token) + phase6-6 (holder), all from clone A ---
base = []
for r in rows:
    base.append({
        "protocol": r["protocol"],
        "cat": r["category"],
        "hhi": fnum(r["hhi"]),
        "insider": fnum(r.get("insider_pct")),
        "mtype": r.get("measurement_type", ""),
        "filpokt": r["protocol"] in ("Filecoin", "Pokt Network"),
    })

# --- the 6 new protocols (verified values; GNO + DOT + TAO parameterized) ---
NEW6_FIXED = [
    {"protocol": "Frax Finance", "cat": "DeFi", "hhi": 0.032411, "insider": 47.0},
    {"protocol": "Synthetix",    "cat": "DeFi", "hhi": 0.017075, "insider": 25.0},
    {"protocol": "Algorand",     "cat": "L1_L2_Infra", "hhi": 0.059096, "insider": 25.0},
]
GNO_LOW, GNO_HIGH = 0.042485, 0.076863     # co-founder Safe excluded / kept
DOT_HHI = 0.00525                          # post-PCA holder-HHI (canonical anchor)
TAO_HHI = 0.014                            # pre-excl conservative (post-excl <=)

def build(filpokt_in, gno, tao_cat, dot_hhi=DOT_HHI):
    pool = [dict(p) for p in base]
    if not filpokt_in:
        pool = [p for p in pool if not p["filpokt"]]
    pool += [dict(p) for p in NEW6_FIXED]
    pool.append({"protocol": "Gnosis",   "cat": "DeFi", "hhi": gno, "insider": 0.0})
    pool.append({"protocol": "Polkadot", "cat": "L1_L2_Infra", "hhi": dot_hhi, "insider": 11.4})
    pool.append({"protocol": "Bittensor","cat": tao_cat, "hhi": TAO_HHI, "insider": None})
    return pool

def cohend(a, b):
    a, b = np.array(a), np.array(b)
    na, nb = len(a), len(b)
    sp = np.sqrt(((na-1)*a.var(ddof=1) + (nb-1)*b.var(ddof=1)) / (na+nb-2))
    return (a.mean() - b.mean()) / sp if sp else float("nan")

def contrast(pool):
    """DePIN vs DeFi HHI: Mann-Whitney two-sided, Cohen's d, group stats."""
    depin = [p["hhi"] for p in pool if p["cat"] == "DePIN" and p["hhi"] is not None]
    defi  = [p["hhi"] for p in pool if p["cat"] == "DeFi"  and p["hhi"] is not None]
    u, p = stats.mannwhitneyu(depin, defi, alternative="two-sided")
    return {
        "n_depin": len(depin), "n_defi": len(defi),
        "mean_depin": np.mean(depin), "mean_defi": np.mean(defi),
        "median_depin": np.median(depin), "median_defi": np.median(defi),
        "U": u, "p": p, "d": cohend(depin, defi),
        "direction": "DePIN>DeFi" if np.median(depin) > np.median(defi) else "DeFi>=DePIN",
    }

def loo_pvals(pool):
    """Leave-one-out: drop each protocol, recompute the contrast p-value."""
    ps = []
    for i in range(len(pool)):
        sub = pool[:i] + pool[i+1:]
        ps.append((pool[i]["protocol"], contrast(sub)["p"]))
    return ps

def cat_means(pool):
    out = {}
    for cat in ("DeFi", "DePIN", "L1_L2_Infra", "Social_Dead"):
        v = [p["hhi"] for p in pool if p["cat"] == cat and p["hhi"] is not None]
        if v: out[cat] = (len(v), np.mean(v))
    return out

def insider_null(pool):
    xs = [(p["insider"], p["hhi"]) for p in pool if p["insider"] is not None and p["hhi"] is not None]
    x = [a for a, _ in xs]; y = [b for _, b in xs]
    r, p = stats.pearsonr(x, y)
    return len(xs), r, p

# ---- N=40 paper baseline (governance_token rows only; what the paper reports) ----
baseline_pool = [p for p in base if p["mtype"] == "governance_token"]
print("="*78)
print(f"BASELINE  N={len(baseline_pool)}  (paper-reported: 40 governance_token rows, incl FIL+POKT)")
c = contrast(baseline_pool)
print(f"  DePIN(n={c['n_depin']}) mean={c['mean_depin']:.4f} med={c['median_depin']:.4f} | "
      f"DeFi(n={c['n_defi']}) mean={c['mean_defi']:.4f} med={c['median_defi']:.4f}")
print(f"  Mann-Whitney p={c['p']:.4f}  Cohen's d={c['d']:.3f}  [{c['direction']}]")
n, r, p = insider_null(baseline_pool)
print(f"  insider-allocation null: Pearson r={r:.3f} p={p:.3f} (n={n})")
print(f"  category means: " + ", ".join(f"{k}={v[1]:.4f}(n{v[0]})" for k,v in cat_means(baseline_pool).items()))

# ---- scenario grid for the target sample ----
print("\n" + "="*78)
print("TARGET-SAMPLE SCENARIO GRID (headline DePIN-vs-DeFi contrast)")
print("="*78)
hdr = f"{'FIL/POKT':9} {'N':>3} {'GNO':>7} {'TAO':>5} | {'p(MW)':>7} {'d':>6} {'dir':>10} | {'meanDeP':>8} {'meanDeF':>8}"
print(hdr); print("-"*len(hdr))
results = {}
for filpokt_in in (True, False):
    for gno_name, gno in (("excl", GNO_LOW), ("keep", GNO_HIGH)):
        for tao_cat in ("DePIN", "Infra"):
            tcat = "DePIN" if tao_cat == "DePIN" else "L1_L2_Infra"
            pool = build(filpokt_in, gno, tcat)
            c = contrast(pool)
            N = len([p for p in pool if p["hhi"] is not None])
            key = (filpokt_in, gno_name, tao_cat)
            results[key] = (pool, c, N)
            print(f"{'IN(52)' if filpokt_in else 'OUT(50)':9} {N:>3} {gno_name:>7} {tao_cat:>5} | "
                  f"{c['p']:>7.4f} {c['d']:>6.3f} {c['direction']:>10} | {c['mean_depin']:>8.4f} {c['mean_defi']:>8.4f}")

# ---- deep dive on the primary scenario: FIL/POKT OUT (per EC-2026-05-27), GNO excl, TAO Infra ----
print("\n" + "="*78)
print("PRIMARY SCENARIO DEEP DIVE: FIL/POKT OUT (N=50), GNO Safe excluded, TAO=Infra")
print("="*78)
pool, c, N = results[(False, "excl", "Infra")]
print(f"  N={N}  Mann-Whitney p={c['p']:.4f}  Cohen's d={c['d']:.3f}  [{c['direction']}]")
print(f"  category means: " + ", ".join(f"{k}={v[1]:.4f}(n{v[0]})" for k,v in cat_means(pool).items()))
n, r, p = insider_null(pool)
print(f"  insider-allocation null: Pearson r={r:.3f} p={p:.3f} (n={n})")
# LOO
loo = loo_pvals(pool)
ps = [x[1] for x in loo]
print(f"  LOO contrast p-value range: min={min(ps):.4f} max={max(ps):.4f}  (all<0.05? {max(ps)<0.05})")
worst = sorted(loo, key=lambda x: -x[1])[:3]
print(f"  LOO most-influential (highest p when dropped): " + ", ".join(f"{a}:{b:.4f}" for a,b in worst))
# with/without DOT
pool_nodot = [p for p in pool if p["protocol"] != "Polkadot"]
c2 = contrast(pool_nodot)
print(f"  WITHOUT DOT: p={c2['p']:.4f} d={c2['d']:.3f}  (with DOT: p={c['p']:.4f} d={c['d']:.3f})")
# DOT value sensitivity (0.00525 vs raw 0.0139)
pool_dot_hi = build(False, GNO_LOW, "L1_L2_Infra", dot_hhi=0.0139)
c3 = contrast(pool_dot_hi)
print(f"  DOT at raw 0.0139 instead of 0.00525: p={c3['p']:.4f} d={c3['d']:.3f}")
