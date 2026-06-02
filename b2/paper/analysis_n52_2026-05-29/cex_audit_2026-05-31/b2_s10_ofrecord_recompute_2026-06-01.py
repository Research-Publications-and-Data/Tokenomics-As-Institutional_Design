#!/usr/bin/env python3
"""S10 PCA-classification 5-spec robustness, recomputed on the POST-CEX-audit frame (2026-06-01).
READ-ONLY analysis; writes nothing canonical. Supersedes the pre-audit pca_classification_robustness_2026-05-22.py.

Of-record statistics: Mann-Whitney U two-sided (p); df-weighted pooled-SD Cohen's d (effect size);
IO held at of-record 0.040248 (IO holder list truncated/unreliable); balanced-30 sample
(15 governance-DePIN vs 15 governance-DeFi, excluding the three N=52 additions FXS/SNX/GNO).

Specs re-include PCA classes by the 5-class typology, from Spec A (exclude all 5 classes, the
canonical method) to Spec E (retain everything but Class-1 burn). Per-(token,address) class map:
explicit pca_class from the consolidated CSV takes priority; the blank-class rows from
exclusions_log get a class derived from exclusion_reason text by ordered keyword rules.

Reproduces the gate (Spec A p=0.0114, d=1.049) and the S10 table:
  A 0.011/1.05 | B 0.051/0.62 | C 0.135/0.40 | D 0.648/0.16 | E 0.561/0.43
"""
import csv, os, math, collections
import numpy as np
from scipy import stats as ss

SIB = os.path.abspath(__file__)
while SIB != os.path.dirname(SIB) and not os.path.exists(os.path.join(SIB, "reproduce.py")):
    SIB = os.path.dirname(SIB)
CEXDIR = os.path.join(SIB, "b2/paper/analysis_n52_2026-05-29/cex_audit_2026-05-31")
ADIR = os.path.join(SIB, "b2/paper/analysis_n52_2026-05-29")
CONS = os.path.join(ADIR, "b2_pca_exclusions_consolidated_2026-05-29.csv")
ELOG = os.path.join(SIB, "data/processed/exclusions_log.csv")

# of-record machinery (cur exclusion union, frame, load_holders, NEW_CEX)
ns = {'__file__': os.path.join(CEXDIR, "b2_full_cex_recompute.py")}
exec(open(os.path.join(CEXDIR, "b2_full_cex_recompute.py")).read().split('print("="*120)')[0], ns)
cur = ns['cur']; frame = ns['frame']; load_holders = ns['load_holders']; NEW_CEX = ns['NEW_CEX']; fnum = ns['fnum']

def low(a): return (a or "").strip().lower()
NAMED = ("binance","robinhood","bithumb","coinbase","bybit","kraken","mexc","kucoin","gate.io",
         "crypto.com","upbit","bitget","okx","htx","huobi","gemini","bitfinex","bitvavo","falconx","backpack")
classmap = {}
for r in csv.DictReader(open(CONS)):
    cl = (r.get("pca_class") or "").strip(); t = (r.get("token") or "").strip().upper(); a = low(r.get("address"))
    if cl and t and a: classmap[(t, a)] = int(cl)
def derive_class(reason):
    import re
    s = (reason or "").lower()
    m = re.search(r'class\s*([1-5])', s)
    if m: return int(m.group(1))
    if any(k in s for k in ("centralized-exchange","exchange custod","cex custody","exchange custodian",
                            "exchange deposit","hot wallet","deposit wallet","exchange")) or any(n in s for n in NAMED): return 5
    if any(k in s for k in ("burn","null","genesis","0x0000","dead address","incinerator")): return 1
    if any(k in s for k in ("bridge","migration","wormhole","portal","lock-mint","cross-chain")): return 4
    if any(k in s for k in ("staking","staked","validator","velocker","vote-escrow","vecrv","gauge","locker")): return 3
    return 2
for r in csv.DictReader(open(ELOG)):
    t = (r.get("token") or "").strip().upper(); a = low(r.get("address"))
    if not t or not a or (t, a) in classmap: continue
    classmap[(t, a)] = derive_class(r.get("exclusion_reason"))
newcex = collections.defaultdict(set)
for t, lst in NEW_CEX.items():
    for a, _ in lst:
        newcex[t.upper()].add(low(a)); classmap[(t.upper(), low(a))] = 5

def full_excl(tok): return set(cur.get(tok, set())) | newcex.get(tok, set())
def retain_for(tok, drop_classes):
    return {a for a in full_excl(tok) if classmap.get((tok, a)) in drop_classes}
def hhi_excl(tok, exclude):
    rows = load_holders(tok)
    if not rows: return None
    ex = {a.lower() for a in exclude}
    surv = [float(r["balance"]) for r in rows if r["address"].strip().lower() not in ex and float(r["balance"]) > 0]
    T = sum(surv)
    return sum((b/T)**2 for b in surv) if T > 0 else None
IO_OFRECORD = 0.040248
def hhi_for(tok, drop_classes):
    if tok == "IO": return IO_OFRECORD
    ex = full_excl(tok) - retain_for(tok, drop_classes)
    v = hhi_excl(tok, ex); return v if v is not None else fnum(frame[tok]["hhi"])
def dfw(a, b):
    a, b = np.array(a), np.array(b); n1, n2 = len(a), len(b)
    sp = math.sqrt(((n1-1)*a.var(ddof=1)+(n2-1)*b.var(ddof=1))/(n1+n2-2)); return (a.mean()-b.mean())/sp

cat = lambda t: frame[t]["category"]; mt = lambda t: frame[t]["measurement_type"]
toks = list(frame.keys())
depin15 = [t for t in toks if cat(t) == "DePIN" and mt(t) == "governance_token"]
defi15  = [t for t in toks if cat(t) == "DeFi" and mt(t) == "governance_token" and t not in ("FXS","SNX","GNO")]

SPECS = [("A", "exclude all 5 classes", set()),
         ("B", "drop Class 5 (retain CEX)", {5}),
         ("C", "drop Class 4+5", {4, 5}),
         ("D", "drop Class 3+4+5", {3, 4, 5}),
         ("E", "drop Class 2+3+4+5", {2, 3, 4, 5})]
print("=== S10 of-record sweep (post-CEX frame, balanced-30, MW2 two-sided + dfw Cohen d, IO=0.040248) ===")
for name, desc, drop in SPECS:
    dep = [hhi_for(t, drop) for t in depin15]; df = [hhi_for(t, drop) for t in defi15]
    p = ss.mannwhitneyu(dep, df, alternative="two-sided")[1]; d = dfw(dep, df)
    n_excl = sum(len((full_excl(t) - retain_for(t, drop)) & {r["address"].strip().lower() for r in (load_holders(t) or [])}) for t in depin15 + defi15)
    print(f"Spec {name} ({desc:<22}): excl={n_excl:>3}  MW2 p={p:.4f}  d={d:+.4f}  {'SIG' if p < 0.05 else 'n.s.'}")
print("\nSpec B narrow CEX definition (explicit class-5 + explicit-reason CEX + Nansen additions,")
print("excluding addresses tagged Class-5 only via generic exchange keywords) for breadth-contingency note:")
# narrow = consolidated explicit pca_class==5  UNION  log rows with an EXPLICIT cex-custody reason  UNION  NEW_CEX
_cex_consolidated = collections.defaultdict(set)
for r in csv.DictReader(open(CONS)):
    if (r.get("pca_class") or "").strip() == "5":
        _cex_consolidated[(r.get("token") or "").strip().upper()].add(low(r.get("address")))
_cex_log_explicit = collections.defaultdict(set)
for r in csv.DictReader(open(ELOG)):
    t = (r.get("token") or "").strip().upper(); a = low(r.get("address")); reason = (r.get("exclusion_reason") or "").lower()
    if not t or not a: continue
    if "centralized-exchange custody" in reason or "class 5" in reason or "exchange custodian" in reason or "cex custody" in reason:
        _cex_log_explicit[t].add(a)
def narrow_cex(tok):
    return (_cex_consolidated.get(tok, set()) | _cex_log_explicit.get(tok, set()) | newcex.get(tok, set())) & full_excl(tok)
dep = [IO_OFRECORD if t == "IO" else (hhi_excl(t, full_excl(t) - narrow_cex(t)) or fnum(frame[t]["hhi"])) for t in depin15]
df  = [IO_OFRECORD if t == "IO" else (hhi_excl(t, full_excl(t) - narrow_cex(t)) or fnum(frame[t]["hhi"])) for t in defi15]
print(f"Spec B (narrow): MW2 p={ss.mannwhitneyu(dep, df, alternative='two-sided')[1]:.4f}  d={dfw(dep, df):+.4f}")
