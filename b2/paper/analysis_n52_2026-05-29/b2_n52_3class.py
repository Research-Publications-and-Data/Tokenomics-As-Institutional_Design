#!/usr/bin/env python3
"""B2 N=52 three-class sector analysis (the author-chosen design, D1).
Kruskal-Wallis omnibus + Dunn post-hoc (Holm) across governance-token
{DePIN, DeFi, L1} ; keeps the published balanced-30 binary as of-record.
Read-only; writes nothing to canonical state.
Verified inputs: DOT=0.0052 (primary; per dot_pca_refined.py README),
GNO=0.042485 (S18 Safe-excluded primary), TAO=0.014 (raw, PCA pending; L1, non-headline).
"""
import csv, numpy as np
from scipy import stats

CSV = "data/processed/regression_data_april2026.csv"
rows = list(csv.DictReader(open(CSV)))
def fnum(x):
    try: return float(x)
    except: return None

# governance-token protocols by category, from clone A (the measurement-consistent class)
G = {"DePIN": [], "DeFi": [], "L1_L2_Infra": [], "Social_Dead": []}
for r in rows:
    if r.get("measurement_type") != "governance_token":  # 6 holder phase6 stay out of the contrast
        continue
    c = r["category"]
    if c in G:
        G[c].append((r["protocol"], fnum(r["hhi"])))

# new governance-token additions per the decided design
NEW = {
    "DeFi": [("Frax Finance", 0.032411), ("Synthetix", 0.017075), ("Gnosis", 0.042485)],
    "L1_L2_Infra": [("Polkadot", 0.0052), ("Algorand", 0.059096), ("Bittensor", 0.014)],
}

def cohend(a, b):
    a, b = np.array(a), np.array(b); na, nb = len(a), len(b)
    sp = np.sqrt(((na-1)*a.var(ddof=1)+(nb-1)*b.var(ddof=1))/(na+nb-2))
    return (a.mean()-b.mean())/sp if sp else float("nan")
def cliffs_delta(a, b):
    gt = sum(1 for x in a for y in b if x > y); lt = sum(1 for x in a for y in b if x < y)
    return (gt-lt)/(len(a)*len(b))

def dunn_holm(groups):
    """groups: dict name->list. Returns omnibus KW + Holm-adjusted pairwise Dunn p."""
    names = list(groups)
    allvals = [v for g in groups.values() for v in g]
    N = len(allvals)
    ranks = stats.rankdata(allvals)
    # tie correction factor for Dunn SE
    _, counts = np.unique(allvals, return_counts=True)
    ties = sum(t**3 - t for t in counts)
    # mean rank per group
    idx = 0; mr = {}; n = {}
    for nm in names:
        k = len(groups[nm]); mr[nm] = ranks[idx:idx+k].mean(); n[nm] = k; idx += k
    H, p_kw = stats.kruskal(*[groups[nm] for nm in names])
    eps2 = (H - len(names) + 1) / (N - len(names))  # epsilon-squared effect size
    sigma2 = (N*(N+1)/12) - ties/(12*(N-1))
    pairs = []
    for i in range(len(names)):
        for j in range(i+1, len(names)):
            a, b = names[i], names[j]
            se = np.sqrt(sigma2 * (1/n[a] + 1/n[b]))
            z = (mr[a]-mr[b]) / se
            p = 2*(1-stats.norm.cdf(abs(z)))
            pairs.append([f"{a} vs {b}", z, p])
    # Holm across the pairwise set
    order = sorted(range(len(pairs)), key=lambda k: pairs[k][2])
    m = len(pairs)
    for rank, k in enumerate(order):
        pairs[k].append(min(1.0, pairs[k][2]*(m-rank)))
    return H, p_kw, eps2, pairs, mr, n

def run(label, depin, defi, l1):
    groups = {"DePIN": [h for _,h in depin], "DeFi": [h for _,h in defi], "L1": [h for _,h in l1]}
    H, p_kw, eps2, pairs, mr, n = dunn_holm(groups)
    print(f"\n### {label}")
    print(f"  n: DePIN={n['DePIN']} DeFi={n['DeFi']} L1={n['L1']}  (total {sum(n.values())})")
    for nm in ("DePIN","DeFi","L1"):
        v = groups[nm]
        print(f"    {nm:5} mean={np.mean(v):.4f} median={np.median(v):.4f} range=[{min(v):.4f},{max(v):.4f}]")
    print(f"  Kruskal-Wallis H={H:.3f} p={p_kw:.4f}  epsilon^2={eps2:.3f}")
    print(f"  Dunn post-hoc (Holm-adjusted):")
    for name, z, p, padj in pairs:
        flag = "  <-- HEADLINE" if name=="DePIN vs DeFi" else ""
        sig = "SIG" if padj < 0.05 else "n.s."
        print(f"    {name:18} z={z:+.3f} p={p:.4f} p_adj={padj:.4f} [{sig}]{flag}")
    # DePIN-DeFi pairwise effect sizes (compare to published d=0.94)
    dep=[h for _,h in depin]; df=[h for _,h in defi]
    print(f"  DePIN-vs-DeFi effect: Cohen d={cohend(dep,df):.3f}  Cliff delta={cliffs_delta(dep,df):+.3f}")
    return pairs

print("="*78)
print("BALANCED-30 OF-RECORD PRIMARY (published; preserved): governance DePIN(15) vs DeFi(15)")
u,p = stats.mannwhitneyu([h for _,h in G['DePIN']],[h for _,h in G['DeFi']],alternative='two-sided')
print(f"  Mann-Whitney p={p:.4f}  Cohen d={cohend([h for _,h in G['DePIN']],[h for _,h in G['DeFi']]):.3f}  (paper: p=0.020 d=0.94)")

print("\n" + "="*78)
print("THREE-CLASS DESIGN (D1): primary + sensitivities")
print("="*78)
depin_full = G["DePIN"]                                   # 15 incl FIL/POKT
depin_xfp  = [x for x in G["DePIN"] if x[0] not in ("Filecoin","Pokt Network")]  # 13
defi18 = G["DeFi"] + NEW["DeFi"]
l1_11  = G["L1_L2_Infra"] + NEW["L1_L2_Infra"]

run("PRIMARY: DePIN15 / DeFi18 / L1-11 (TAO in L1; DOT=0.0052; GNO=0.0425; FIL/POKT in)",
    depin_full, defi18, l1_11)

# sensitivity: TAO -> DePIN
run("SENS-A: TAO moved to DePIN (16) / DeFi18 / L1-10",
    depin_full + [("Bittensor",0.014)], defi18,
    G["L1_L2_Infra"] + [("Polkadot",0.0052),("Algorand",0.059096)])

# sensitivity: FIL/POKT out
run("SENS-B: FIL/POKT excluded from DePIN (13) / DeFi18 / L1-11",
    depin_xfp, defi18, l1_11)

# sensitivity: DOT=0.0093, GNO=0.0769
defi18_hi = G["DeFi"] + [("Frax",0.032411),("Synthetix",0.017075),("Gnosis",0.076863)]
l1_11_hi  = G["L1_L2_Infra"] + [("Polkadot",0.0093),("Algorand",0.059096),("Bittensor",0.014)]
run("SENS-C: DOT=0.0093 (Class5-rejected) + GNO=0.0769 (Safe kept)",
    depin_full, defi18_hi, l1_11_hi)

# LOO on the DePIN-DeFi pairwise within the 3-class design (primary)
print("\n" + "="*78)
print("LOO robustness of the DePIN-DeFi Dunn p_adj (PRIMARY 3-class design)")
print("="*78)
pool = [("DePIN",p,h) for p,h in depin_full] + [("DeFi",p,h) for p,h in defi18] + [("L1",p,h) for p,h in l1_11]
padjs = []
for i in range(len(pool)):
    sub = pool[:i]+pool[i+1:]
    g = {"DePIN":[h for c,_,h in sub if c=="DePIN"],"DeFi":[h for c,_,h in sub if c=="DeFi"],"L1":[h for c,_,h in sub if c=="L1"]}
    _,_,_,pr,_,_ = dunn_holm(g)
    pd_ = [p for nm,z,p,padj in pr if nm=="DePIN vs DeFi"][0]
    padj_ = [padj for nm,z,p,padj in pr if nm=="DePIN vs DeFi"][0]
    padjs.append((pool[i][1], padj_))
ps=[x[1] for x in padjs]
print(f"  DePIN-DeFi Dunn p_adj range: min={min(ps):.4f} max={max(ps):.4f}  all<0.05? {max(ps)<0.05}")
worst=sorted(padjs,key=lambda x:-x[1])[:4]
print(f"  most-influential (highest p_adj when dropped): "+", ".join(f"{a}:{b:.4f}" for a,b in worst))
