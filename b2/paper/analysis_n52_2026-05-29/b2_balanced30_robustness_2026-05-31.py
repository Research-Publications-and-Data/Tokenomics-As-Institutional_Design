import csv, math, itertools, random
import numpy as np
from scipy import stats as ss
random.seed(42); np.random.seed(42)
frame={r['token']:r for r in csv.DictReader(open("data/processed/regression_data_april2026.csv"))}
def cat(t):return frame[t]['category']
def mt(t):return frame[t]['measurement_type']
def hh(t):return float(frame[t]['hhi'])
depin=[hh(t) for t in frame if cat(t)=="DePIN" and mt(t)=="governance_token"]
defi=[hh(t) for t in frame if cat(t)=="DeFi" and mt(t)=="governance_token" and t not in("FXS","SNX","GNO")]
def cohend(a,b):
    a,b=np.array(a),np.array(b);na,nb=len(a),len(b)
    sp=math.sqrt(((na-1)*a.var(ddof=1)+(nb-1)*b.var(ddof=1))/(na+nb-2));return (a.mean()-b.mean())/sp
u,p=ss.mannwhitneyu(depin,defi,alternative="two-sided")
print(f"balanced-30: DePIN n={len(depin)} mean={np.mean(depin):.4f} | DeFi n={len(defi)} mean={np.mean(defi):.4f} | ratio={np.mean(depin)/np.mean(defi):.2f}")
print(f"  MW p={p:.4f}  Cohen d={cohend(depin,defi):.3f}")
# overlap: DePIN protocols within DeFi range
dmin,dmax=min(defi),max(defi)
overlap=sum(1 for x in depin if dmin<=x<=dmax)
print(f"  DePIN within DeFi range [{dmin:.4f},{dmax:.4f}]: {overlap} of {len(depin)}")
# LOO: 30 iterations (drop each of the 30 protocols)
pool=[("DePIN",x) for x in depin]+[("DeFi",x) for x in defi]
ps=[];ds=[]
for i in range(len(pool)):
    sub=pool[:i]+pool[i+1:]
    dp=[x for c,x in sub if c=="DePIN"];df=[x for c,x in sub if c=="DeFi"]
    _,pp=ss.mannwhitneyu(dp,df,alternative="two-sided");ps.append(pp);ds.append(cohend(dp,df))
print(f"  LOO p range: {min(ps):.4f} to {max(ps):.4f} (all<0.05? {max(ps)<0.05})")
print(f"  LOO Cohen d range: {min(ds):.2f} to {max(ds):.2f}")
# permutation: 100,000 label reassignments, two-sided on mean diff
obs=abs(np.mean(depin)-np.mean(defi)); allv=np.array(depin+defi);n1=len(depin);cnt=0;NP=100000
for _ in range(NP):
    np.random.shuffle(allv)
    if abs(allv[:n1].mean()-allv[n1:].mean())>=obs:cnt+=1
print(f"  permutation p (100k, two-sided mean diff): {cnt/NP:.4f}")
# bootstrap: 10,000 resamples, 95% percentile interval of mean diff + Cohen d CI
NB=10000;diffs=[];dds=[]
for _ in range(NB):
    bd=np.random.choice(depin,len(depin),replace=True);bf=np.random.choice(defi,len(defi),replace=True)
    diffs.append(bd.mean()-bf.mean());dds.append(cohend(list(bd),list(bf)))
print(f"  bootstrap 95% mean-diff PI: [{np.percentile(diffs,2.5):.3f}, {np.percentile(diffs,97.5):.3f}]")
print(f"  bootstrap Cohen d 95% CI: [{np.percentile(dds,2.5):.2f}, {np.percentile(dds,97.5):.2f}]")
