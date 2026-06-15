#!/usr/bin/env python3
"""B2 explanatory-model AUTHORITATIVE REPRODUCTION (2026-05-29, post-missed-PCA-correction).

Re-establishes the powered explanatory-model numbers from PERSISTED data after the
original /tmp run scripts evaporated (artifact-retention gap). READ-ONLY against
clone-A regression_data_april2026.csv (current; corrected ENA/WLFI HHIs in place).

Reproduces what persisted data supports:
  - M0: log-HHI ~ sector (DePIN/L1; DeFi=ref)         [headline, no controls]
  - M1: log-HHI ~ sector + log(rev-intensity) + maturity   [POWERED; obs/pred ~12.5]
  - raw-HHI versions of both (Table-5 coefficient comparability to published Models 1-3)
  - HC3 robust SE (matches Table 5 published spec)
  - mediation: DePIN coef M0 -> M1 (does architecture survive controls?)
  - VIF
  - original-sample retention de-tautology from insider_analysis_results_v3.csv:
        non-insider-HHI ~ retention (Spearman + OLS), N as covered

NOT reproducible here (flagged): the N=49 model WITH insider-RETENTION for all sectors,
because the new-12 retention frame (FXS/SNX/GNO/WLFI/ENA/PUMP/JTO/BONK/KMNO/DOT/TAO/ALGO)
was assembled at run-time and not persisted. The retention TERM at the expanded N requires
re-deriving insider_count_frac for those 12 from the persisted holder-lists + the session's
Nansen/Blockscout/Helius classifications. Headline (DePIN robust) does NOT depend on it.
"""
import csv, math, numpy as np
import scipy.stats as ss

C="data/processed/regression_data_april2026.csv"
rows=list(csv.DictReader(open(C)))
def f(x):
    try: return float(x)
    except: return None

SEC={'DePIN':'DePIN','DeFi':'DeFi','L1_L2_Infra':'L1'}
D=[]
for r in rows:
    if r.get('category') not in SEC: continue
    hhi=f(r['hhi']); rev=f(r.get('revenue_annual_usd')); fdv=f(r.get('fdv_usd')) or f(r.get('market_cap_usd'))
    mat=f(r.get('maturity_years'))
    if hhi is None or rev is None or fdv is None or mat is None or fdv<=0: continue
    ri=rev/fdv
    D.append({'p':r['protocol'],'tok':r.get('token',''),'sec':SEC[r['category']],
              'hhi':hhi,'y':math.log(hhi),'ri':math.log10(ri+1e-7),'mat':mat})
from collections import Counter
N=len(D)
print(f"=== MODEL FRAME N={N} | sectors {dict(Counter(d['sec'] for d in D))} ===")

def ols_hc3(y, cols, D):
    """cols: list of ('sec',label) for dummy, or plain key for continuous."""
    X=np.column_stack([np.ones(N)]+[
        np.array([(1.0 if d['sec']==c[1] else 0.0) if isinstance(c,tuple) else d[c] for d in D])
        for c in cols])
    b,_,_,_=np.linalg.lstsq(X,y,rcond=None); e=y-X@b; n,k=X.shape
    XtXi=np.linalg.inv(X.T@X); H=X@XtXi@X.T; h=np.diag(H)
    # HC3
    omega=np.diag((e**2)/((1-h)**2))
    cov=XtXi@(X.T@omega@X)@XtXi; se=np.sqrt(np.diag(cov)); t=b/se
    p=[2*(1-ss.t.cdf(abs(tt),n-k)) for tt in t]
    r2=1-(e@e)/(((y-y.mean())**2).sum()); adj=1-(1-r2)*(n-1)/(n-k)
    return b,se,p,r2,adj

names_m0=['(int)','DePIN','L1']; cols_m0=[('sec','DePIN'),('sec','L1')]
names_m1=['(int)','DePIN','L1','log_revint','maturity']; cols_m1=[('sec','DePIN'),('sec','L1'),'ri','mat']

for dv,lbl in (('y','log-HHI'),('hhi','raw-HHI')):
    y=np.array([d[dv] for d in D])
    print(f"\n########## DV = {lbl} ##########")
    b,se,p,r2,adj=ols_hc3(y,cols_m0,D)
    print(f"-- M0 (sector only): N={N} --")
    for nm,bb,ss_,pp in zip(names_m0,b,se,p): print(f"   {nm:12} b={bb:+.4f} se={ss_:.4f} p={pp:.4f}{' *' if pp<0.05 else ''}")
    print(f"   adjR2={adj:.3f}  DePIN(uncontrolled)={b[1]:+.4f}")
    dep0=b[1]
    b,se,p,r2,adj=ols_hc3(y,cols_m1,D)
    print(f"-- M1 (POWERED: sector + log(rev-int) + maturity): N={N}, obs/pred={N/4:.1f} --")
    for nm,bb,ss_,pp in zip(names_m1,b,se,p): print(f"   {nm:12} b={bb:+.4f} se={ss_:.4f} p={pp:.4f}{' *' if pp<0.05 else ''}")
    print(f"   adjR2={adj:.3f}  DePIN(controlled)={b[1]:+.4f}  p={p[1]:.4f}")
    att=(1-b[1]/dep0)*100 if dep0 else 0
    print(f"   MEDIATION: DePIN {dep0:+.4f} -> {b[1]:+.4f} ({'attenuates '+f'{att:.0f}%' if abs(b[1])<abs(dep0) else 'NO attenuation / strengthens'})")

# VIF (continuous predictors in M1)
print("\n=== VIF (M1 predictors) ===")
for c,nm in (('ri','log_revint'),('mat','maturity')):
    yi=np.array([d[c] for d in D])
    Xo=np.column_stack([np.ones(N)]+[np.array([1.0 if d['sec']==s else 0.0 for d in D]) for s in('DePIN','L1')]
                       +[np.array([d[c2] for d in D]) for c2 in('ri','mat') if c2!=c])
    bb,_,_,_=np.linalg.lstsq(Xo,yi,rcond=None); ri_=yi-Xo@bb; r2i=1-(ri_@ri_)/(((yi-yi.mean())**2).sum())
    print(f"   {nm:12} VIF={1/(1-r2i):.2f}")

# ---- original-sample retention de-tautology (PERSISTED: v3) ----
print("\n=== RETENTION de-tautology (original sample; insider_analysis_results_v3.csv) ===")
v3=list(csv.DictReader(open("data/processed/insider_analysis_results_v3.csv")))
ret=[]
for r in v3:
    frac=f(r.get('insider_count_frac')); nih=f(r.get('non_insider_hhi_approx'))
    full=f(r.get('full_hhi'))
    if frac is not None and full is not None:
        ret.append({'tok':r['token'],'frac':frac,'nih':nih,'full':full})
fr=np.array([r['frac'] for r in ret]); fu=np.array([r['full'] for r in ret])
rho,pr=ss.spearmanr(fr,fu)
print(f"   retention vs FULL-HHI: Spearman rho={rho:.3f} p={pr:.4f} N={len(ret)} (the published rho=0.48 check)")
ret_n=[r for r in ret if r['nih'] is not None]
if ret_n:
    frn=np.array([r['frac'] for r in ret_n]); nih=np.array([r['nih'] for r in ret_n])
    rho2,pr2=ss.spearmanr(frn,nih)
    print(f"   retention vs NON-INSIDER-HHI (de-tautologized): Spearman rho={rho2:.3f} p={pr2:.4f} N={len(ret_n)}")
    # OLS non-insider-HHI ~ retention
    X=np.column_stack([np.ones(len(ret_n)),frn]); b,_,_,_=np.linalg.lstsq(X,nih,rcond=None)
    e=nih-X@b; n,k=X.shape; XtXi=np.linalg.inv(X.T@X); h=np.diag(X@XtXi@X.T)
    cov=XtXi@(X.T@np.diag((e**2)/((1-h)**2))@X)@XtXi; se=np.sqrt(np.diag(cov))
    pp=2*(1-ss.t.cdf(abs(b[1]/se[1]),n-k))
    print(f"   OLS non-insider-HHI ~ retention: beta={b[1]:+.4f} se={se[1]:.4f} p={pp:.4f} N={n}")
print("\n[done] persisted reproduction; new-12 retention frame still needs re-derivation for the N~49 retention TERM.")
