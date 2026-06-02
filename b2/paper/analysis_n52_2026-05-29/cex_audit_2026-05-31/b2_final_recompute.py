import csv, os, math
import numpy as np
from scipy import stats as ss
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "b2_full_cex_recompute.py")).read().split("print(\"=\"*120)")[0])  # reuse loaders, cur, frame, NEW_CEX, hhi_topn (loader promoted from /tmp to in-repo sibling)
# Build final new HHIs from holder-list recompute (all NEW_CEX), then override IO with fresh pull value
newh={}
for tok in NEW_CEX:
    if tok=="IO": continue
    rn=hhi_topn(tok, frozenset(a for a,_ in NEW_CEX[tok]))
    if rn: newh[tok]=rn["hhi"]
IO_VALUES={"frame_0.125":0.125136, "cex_only_0.163":0.162915, "cex_plus_vault_0.040":0.040248}

def hnow(tok, io_val):
    if tok=="IO": return io_val
    return newh.get(tok, float(frame[tok]["hhi"]))
def cat(t): return frame[t]["category"]
def mt(t): return frame[t]["measurement_type"]
depin15=[t for t in frame if cat(t)=="DePIN" and mt(t)=="governance_token"]
defi15=[t for t in frame if cat(t)=="DeFi" and mt(t)=="governance_token" and t not in("FXS","SNX","GNO")]
defi24=[t for t in frame if cat(t)=="DeFi"]
def contr(depin,defi,io_val):
    dep=[hnow(t,io_val) for t in depin]; df=[hnow(t,io_val) for t in defi]
    u,p=ss.mannwhitneyu(dep,df,alternative="two-sided")
    a,b=np.array(dep),np.array(df);na,nb=len(a),len(b)
    sp=math.sqrt(((na-1)*a.var(ddof=1)+(nb-1)*b.var(ddof=1))/(na+nb-2));d=(a.mean()-b.mean())/sp
    return p,d,a.mean(),b.mean()
print("FINAL recompute (full 52-protocol CEX audit). IO-treatment sensitivity:")
print(f"{'IO treatment':<22}{'bal30_p':>9}{'bal30_d':>9}{'DePINmean':>10}{'DeFimean':>10}{'ratio':>7}{'full_p':>9}{'full_d':>9}")
for name,io in IO_VALUES.items():
    p,d,dm,fm=contr(depin15,defi15,io)
    fp,fd,_,_=contr(depin15,defi24,io)
    print(f"{name:<22}{p:>9.4f}{d:>+9.3f}{dm:>10.4f}{fm:>10.4f}{dm/fm:>7.2f}{fp:>9.4f}{fd:>+9.3f}")
print("\npaper of-record: balanced-30 p=0.020 d=0.94 ratio=2.3 ; full-frame p=0.0234 d=0.939")
# Final per-protocol table (IO = cex_only 0.163)
print("\nFINAL per-protocol HHI (token: frame -> new):")
io=0.162915
allchg=sorted(set(list(newh)+["IO"]))
for t in allchg:
    print(f"  {t:<10} {float(frame[t]['hhi']):.6f} -> {hnow(t,io):.6f}  ({cat(t)[:5]})")
# 3-class
l1=[t for t in frame if cat(t)=="L1_L2_Infra"]; defi18=defi15+["FXS","SNX","GNO"]
g={"DePIN":[hnow(t,io) for t in depin15],"DeFi":[hnow(t,io) for t in defi18],"L1":[hnow(t,io) for t in l1]}
H,pk=ss.kruskal(*g.values())
print(f"\n3-class KW: H={H:.3f} p={pk:.4f}  DePIN mean={np.mean(g['DePIN']):.4f} DeFi={np.mean(g['DeFi']):.4f} L1={np.mean(g['L1']):.4f}")
# exclusion count
nrows=sum(len(v) for v in NEW_CEX.values())-1+23  # minus IO's 1 placeholder + 23 actual IO CEX
print(f"\nExclusion magnitude: ~{sum(len(v) for v in NEW_CEX.values())-1}+23(IO) = ~{sum(len(v) for v in NEW_CEX.values())-1+23} new CEX rows across ~21 protocols")
