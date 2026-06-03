#!/usr/bin/env python3
"""B2 thesis-strengthening: compute + LOCK the zero-new-data statistics (DO-NOW set).
Reproduces anchors first, then computes ROB-6 (N lock), ROB-2 (omnibus F), ROB-1 (TOST),
ROB-4 (retention triple + sector-partial), ROB-5 (influence diagnostics), NE-1 (temporal null).
All against committed in-repo inputs. No /tmp data dependency, no cross-clone path.

Run from anywhere:  python b2/paper/analysis_n52_2026-05-29/b2_strengthen_compute_2026-06-02.py
Reproduces (Section 4.4 / 4.6): allocation null r = 0.10, N = 50 (Spearman rho = 0.16);
TOST equivalence p = 0.02 within |r| = 0.38; launch-design omnibus F(3,41) = 0.66, p = 0.58
(R-squared 4.6 percent); insider-retention de-tautology rho = 0.54, N = 34 (bootstrap CI
[0.21, 0.80], permutation p = 0.001, LOO 34/34, sector-partial r = 0.47, p = 0.005);
Model 4 influence (all 50 LOO refits keep DePIN significant); NE-1 temporal endpoint null
(launch insider_pct vs 24-month governance-HHI, r = -0.11, N = 13)."""
import csv, math, os, sys
import numpy as np
from scipy import stats as ss

# Repo root resolved from this file's location (b2/paper/analysis_n52_2026-05-29/<file>):
SIB = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
FRAME = SIB + "/data/processed/regression_data_april2026.csv"
V3 = SIB + "/data/processed/insider_analysis_results_v3.csv"
PANEL = SIB + "/b2/paper/supplements/S7_hhi_panel/exhibit_k1_panel_full.csv"
SEC = {"DePIN": "DePIN", "DeFi": "DeFi", "L1_L2_Infra": "L1"}

def fnum(x):
    try:
        v = float(x); return v if not math.isnan(v) else None
    except Exception:
        return None

rows = list(csv.DictReader(open(FRAME)))
def col(r, c): return fnum(r.get(c))

print("="*78); print("ANCHOR: core null (insider_pct vs hhi), reproduce r=0.099/N=50"); print("="*78)
# governance + holder protocols in the 3 sectors with both fields present
def alloc_sample(include_social=False):
    out=[]
    for r in rows:
        cat=r["category"]
        if not include_social and cat not in SEC: continue
        if include_social and cat not in (set(SEC)|{"Social_Dead"}): continue
        ip=col(r,"insider_pct"); hh=col(r,"hhi")
        if ip is None or hh is None: continue
        out.append(r)
    return out
for inc,label in [(False,"sectors DePIN/DeFi/L1"),(True,"+ Social_Dead")]:
    S=alloc_sample(inc); ip=[col(r,"insider_pct") for r in S]; hh=[col(r,"hhi") for r in S]
    r_,p_=ss.pearsonr(ip,hh); rho,pr=ss.spearmanr(ip,hh)
    print(f"  [{label}] N={len(S)}  Pearson r={r_:.4f} p={p_:.4f}  Spearman rho={rho:.4f} p={pr:.4f}")
    if inc:
        social=[r['token'] for r in S if r['category']=="Social_Dead"]
        print(f"       Social_Dead row(s) in this sample: {social}")

print(); print("="*78); print("ROB-6: lock the core-null N (50 vs 51)"); print("="*78)
S50=alloc_sample(False); S51=alloc_sample(True)
swing=[r['token'] for r in S51 if r['token'] not in {x['token'] for x in S50}]
print(f"  N(sectors only)={len(S50)} ; N(+Social_Dead)={len(S51)} ; swing row(s)={swing}")
for nm,S in [("N=%d (sectors)"%len(S50),S50),("N=%d (+social)"%len(S51),S51)]:
    ip=[col(r,"insider_pct") for r in S]; hh=[col(r,"hhi") for r in S]
    r_,p_=ss.pearsonr(ip,hh)
    print(f"    {nm}: r={r_:.4f} (r={r_:.3f}) p={p_:.4f}")
mt={r['token']:r.get('measurement_type') for r in S50}
print(f"    measurement_type breakdown (sectors-only): "
      + str({k:sum(1 for r in S50 if r.get('measurement_type')==k) for k in set(mt.values())}))

print(); print("="*78); print("ROB-2: launch-design OMNIBUS joint F-test (hhi ~ launch-design block)"); print("="*78)
def omnibus(covs, sample):
    # rows needing all covs + hhi present
    D=[r for r in sample if all(col(r,c) is not None for c in covs) and col(r,"hhi") is not None]
    y=np.array([col(r,"hhi") for r in D]); n=len(D); k=len(covs)
    X=np.column_stack([np.ones(n)]+[[col(r,c) for r in D] for c in covs])
    beta,_,_,_=np.linalg.lstsq(X,y,rcond=None)
    yhat=X@beta; ssr=((y-yhat)**2).sum(); sst=((y-y.mean())**2).sum()
    r2=1-ssr/sst
    F=(r2/k)/((1-r2)/(n-k-1)); pF=1-ss.f.cdf(F,k,n-k-1)
    return n,k,r2,F,pF
for covs in [["team_pct","investor_pct","maturity_years"], ["team_pct","investor_pct","maturity_years","insider_pct"]]:
    n,k,r2,F,pF=omnibus(covs,S50)
    print(f"  covs={covs}")
    print(f"    N={n}  R2={r2:.4f} ({r2*100:.1f}% of HHI variance)  F({k},{n-k-1})={F:.3f}  p={pF:.4f}")

print(); print("="*78); print("ROB-1: TOST equivalence on the core null (bound |rho|<0.38)"); print("="*78)
def tost_corr(r_obs,n,bound=0.38,alpha=0.05):
    z=math.atanh(r_obs); se=1/math.sqrt(n-3); zb=math.atanh(bound)
    p_upper=ss.norm.cdf((z-zb)/se)        # H0: rho>=+bound
    p_lower=1-ss.norm.cdf((z+zb)/se)      # H0: rho<=-bound
    return max(p_upper,p_lower),p_upper,p_lower
for nm,S in [("N=%d"%len(S50),S50)]:
    ip=[col(r,"insider_pct") for r in S]; hh=[col(r,"hhi") for r in S]
    r_,_=ss.pearsonr(ip,hh)
    tp,pu,pl=tost_corr(r_,len(S))
    print(f"  {nm} r={r_:.4f}: TOST p=max({pu:.4f},{pl:.4f})={tp:.4f}  -> equivalence (|rho|<0.38) {'REJECTS null at .05 (EQUIVALENT)' if tp<0.05 else 'not concluded'}")

print(); print("="*78); print("ROB-4: insider-retention triple (bootstrap CI, permutation, LOO) + sector-partial"); print("="*78)
v3=list(csv.DictReader(open(V3)))
sectmap={r['token']:r['category'] for r in rows}
rec=[]
for r in v3:
    fr=fnum(r.get("insider_count_frac")); nh=fnum(r.get("non_insider_hhi_approx"))
    if fr is None or nh is None: continue
    rec.append((r['token'],fr,nh,sectmap.get(r['token'])))
x=np.array([a[1] for a in rec]); y=np.array([a[2] for a in rec]); N=len(rec)
rho0,p0=ss.spearmanr(x,y)
print(f"  de-tautology: Spearman rho={rho0:.4f} p={p0:.4f} N={N}")
# bootstrap CI on rho
rng=np.random.default_rng(7); bs=[]
for _ in range(10000):
    idx=rng.integers(0,N,N); rr,_=ss.spearmanr(x[idx],y[idx])
    if not math.isnan(rr): bs.append(rr)
lo,hi=np.percentile(bs,[2.5,97.5]); pctpos=100*np.mean(np.array(bs)>0)
print(f"  bootstrap 95% CI on rho = [{lo:.3f}, {hi:.3f}]  ({pctpos:.1f}% of replicates positive)")
# permutation p
rng=np.random.default_rng(42); c=0; obs=abs(rho0)
yp=y.copy()
for _ in range(100000):
    rng.shuffle(yp); rr,_=ss.spearmanr(x,yp)
    if abs(rr)>=obs: c+=1
print(f"  permutation p (100k, two-sided) = {c/100000:.5f}")
# LOO
loo=[]
for i in range(N):
    m=[j for j in range(N) if j!=i]; rr,_=ss.spearmanr(x[m],y[m]); loo.append(rr)
print(f"  LOO: {sum(1 for v in loo if v>0)}/{N} positive; rho range [{min(loo):.3f},{max(loo):.3f}]")
# sector-partial rank correlation (control for sector one-hot), N=34
secs=[a[3] for a in rec]; usec=sorted(set(secs))
def rank(a): return ss.rankdata(a)
rx=rank(x); ry=rank(y)
Dmat=np.column_stack([np.ones(N)]+[[1.0 if s==u else 0.0 for s in secs] for u in usec[1:]])
def resid(v):
    b,_,_,_=np.linalg.lstsq(Dmat,v,rcond=None); return v-Dmat@b
rxr=resid(rx); ryr=resid(ry); pr_,pp_=ss.pearsonr(rxr,ryr)
print(f"  sector-partial rank corr (control sector one-hot) r={pr_:.4f} p={pp_:.4f} N={N} sectors={usec}")

print(); print("="*78); print("ROB-5: Model 4 influence diagnostics (maturity-spec + retention-spec)"); print("="*78)
sys.path.insert(0,SIB)
import importlib.util
spec=importlib.util.spec_from_file_location("rep",SIB+"/reproduce.py")
rep=importlib.util.module_from_spec(spec); spec.loader.exec_module(rep)
frame, _v3, _n12 = rep.load_frame_and_retention()
def spec_loo(D, cols, label):
    b,se,p,r2=rep.ols_hc3(D,cols); base_p=p[1]
    worst=0; worst_tok=None; best=1; best_tok=None
    for i in range(len(D)):
        Dd=[D[j] for j in range(len(D)) if j!=i]
        bb,ss_,pp,_=rep.ols_hc3(Dd,cols); pv=pp[1]
        if pv>worst: worst=pv; worst_tok=D[i]["tok"]
        if pv<best: best=pv; best_tok=D[i]["tok"]
    print(f"  {label}: base DePIN p={base_p:.4f}  LOO worst p={worst:.4f} (drop {worst_tok})  best p={best:.4f} (drop {best_tok})  all-sig={'YES' if worst<0.05 else 'NO'}")
# build the two design sets exactly as reproduce.py main does
Dm=[d for d in frame if d["mat"] is not None]
Dr=[d for d in frame if d["ret"] is not None]
print(f"  (maturity-spec N={len(Dm)}; retention-spec N={len(Dr)}; keys={list(frame[0].keys())})")
spec_loo(Dm,[("sec","DePIN"),("sec","L1"),"ri","mat"],"maturity-spec")
spec_loo(Dr,[("sec","DePIN"),("sec","L1"),"ri","ret"],"retention-spec")

print(); print("="*78); print("NE-1: temporal endpoint null (launch insider_pct vs panel HHI)"); print("="*78)
panel=list(csv.DictReader(open(PANEL)))
# map panel protocol -> frame token
pmap={"MKR (MCD)":"MKR","MKR (TGE)":"MKR"}
def ptok(p): return pmap.get(p,p)
ins={r['token']:col(r,"insider_pct") for r in rows}
q1={}; q8={}
for r in panel:
    tok=ptok(r['protocol']); q=r['quarter']; h=fnum(r['gov_hhi'])
    if q=="Q1": q1[(r['protocol'])]=h
    if q=="Q8": q8[(r['protocol'])]=h
# join: use protocol label; need launch insider_pct from frame token
joined=[]
for r in panel:
    if r['quarter']!="Q8": continue
    prot=r['protocol']; tok=ptok(prot); ipv=ins.get(tok)
    # MKR dedup (shipped: N=13): MakerDAO appears as two panel vintages (MCD + TGE) at one
    # frame insider_pct; keep the TGE row (24mo-post-token-generation, apples-to-apples) and drop
    # MCD so the protocol is counted once. The null is INVARIANT across all four collapse choices
    # (both / keep-TGE / keep-MCD / drop-both: Q8 Pearson r in [-0.11, -0.06], all n.s.); see PAPER.md 4.4.
    if prot=="MKR (MCD)": continue
    h8=fnum(r['gov_hhi']); h1=q1.get(prot)
    if ipv is None or h8 is None: continue
    joined.append((prot,tok,ipv,h1,h8))
print(f"  joined protocols (insider_pct present): N={len(joined)}")
for prot,tok,ipv,h1,h8 in joined:
    print(f"    {prot:12s} tok={tok:6s} insider_pct={ipv:.3f}  Q1={h1}  Q8={h8}")
unmatched=[r['protocol'] for r in panel if r['quarter']=="Q8" and ins.get(ptok(r['protocol'])) is None]
print(f"  panel Q8 protocols with NO frame insider_pct (dropped): {unmatched}")
ipv=np.array([a[2] for a in joined]); h8=np.array([a[4] for a in joined])
h1=np.array([a[3] if a[3] is not None else np.nan for a in joined])
def corr_report(label,a,b):
    m=~np.isnan(a)&~np.isnan(b); a,b=a[m],b[m]
    rp,pp=ss.pearsonr(a,b); rs,ps=ss.spearmanr(a,b)
    print(f"  {label} N={len(a)}: Pearson r={rp:.4f} p={pp:.4f} | Spearman rho={rs:.4f} p={ps:.4f}")
corr_report("insider_pct vs Q8 (24mo endpoint)",ipv,h8)
corr_report("insider_pct vs Q1 (3mo)",ipv,h1)
decay=h1-h8
corr_report("insider_pct vs (Q1-Q8 decay)",ipv,decay)
# LOO dropping AAVE and CRV
keep=[i for i,a in enumerate(joined) if a[0] not in ("AAVE","CRV")]
corr_report("insider_pct vs Q8  [drop AAVE,CRV]",ipv[keep],h8[keep])
print("\n[done] all strengthening statistics computed.")
