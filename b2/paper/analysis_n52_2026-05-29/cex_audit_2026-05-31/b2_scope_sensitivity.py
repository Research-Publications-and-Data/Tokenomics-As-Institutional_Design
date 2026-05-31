import csv, os, math
import numpy as np
from scipy import stats as ss
SIB="/Users/zach/Tokenomics-As-Institutional_Design"
HLD=[os.path.join(SIB,"data/raw/holder_lists"),"/Users/zach/b2-governance-data/data/raw/holder_lists"]
FRAME=os.path.join(SIB,"data/processed/regression_data_april2026.csv")
ADIR=os.path.join(SIB,"b2/paper/analysis_n52_2026-05-29")
SRCS=[(os.path.join(SIB,"data/processed/exclusions_log.csv"),"token","address"),
      (os.path.join(ADIR,"new12_unified_exclusions_2026-05-29.csv"),"token","address"),
      (os.path.join(ADIR,"b2_pca_exclusions_consolidated_2026-05-29.csv"),"token","address")]
def loadh(t):
    for d in HLD:
        p=os.path.join(d,f"{t}_holders.csv")
        if os.path.exists(p): return list(csv.DictReader(open(p)))
    return None
cur={}
for path,tc,ac in SRCS:
    if not os.path.exists(path): continue
    for r in csv.DictReader(open(path)):
        t=(r.get(tc)or"").strip().upper(); a=(r.get(ac)or"").strip().lower()
        if t and a: cur.setdefault(t,set()).add(a)
frame={r["token"]:r for r in csv.DictReader(open(FRAME))}
def fnum(x):
    try:return float(x)
    except:return None
def hhi(t,extra=frozenset()):
    rows=loadh(t)
    if not rows: return None
    ex=cur.get(t,set())|{a.lower() for a in extra}
    surv=[float(r["balance"]) for r in rows if r["address"].strip().lower() not in ex]
    T=sum(surv)
    return sum((b/T)**2 for b in surv) if T>0 else None

# full new-cex set (token->addrs)
FULL={
 "JUP":["27b4PRN7K37rpTywq65t29rjuNfQkYpxZUjkbtHc5VvZ","43DbAvKxhXh1oSxkJSqGosNw3HpBnmsWiak6tB5wpecN","Gem2VAypSg7Ai7vjDKPTtqFahpoQWkfgVkyzx3rPoTka"],
 "DRIFT":["FH9iLV5Z8EUEDMnW6CzUPkpDhWJCsHqJ5N4W23njNsUo","EPpctwZpP7LE61Xkpbb9ixfxMFD8fFAxewe7dTk6dg1M","5LZkATrLwHYCQj2YuVbjjgsDZzBk6YfL4pFQRJmtboT2","8Mm46CsqxiyAputDUp2cXHg41HE3BfynTeMBDwzrMZQH"],
 "HNT":["5LZkATrLwHYCQj2YuVbjjgsDZzBk6YfL4pFQRJmtboT2","22Wnk8PwyWZV7BfkZGJEKT9jGGdtvu7xY6EXeRh7zkBa","53unSgGWqEWANcPYRF35B2Bgf8BkszUtcccKiXwGGLyr","EFE3j1pcSP1paUzA86zW7989ZjsFP2J7ginyUqo4ewqR"],
 "HONEY":["FsAA2JoVBLin4CbGk16eCjQM4Etixz9cbT1smJvfC6NQ","3A6s38hSeXDrapWiAR7pRxyaJSiCbGLeKmEZSA9Tix4F","5YMPkRAQN6S6sVw3hLwPGqg8w9ZDiVDwFdYNFK2QYJzp"],
 "RENDER":["7TWnq4WeYcwQWBCwKeEX2Q9xqVtthPGkB7adNvueuVuh"],
 "W":["5LZkATrLwHYCQj2YuVbjjgsDZzBk6YfL4pFQRJmtboT2","8Mm46CsqxiyAputDUp2cXHg41HE3BfynTeMBDwzrMZQH"],
 "AAVE":["0x5a801a9418d036fd453078c3adcb761fdc5ae695"],
 "ANYONE":["0x446b86a33e2a438f569b15855189e3da28d027ba","0xaa10db8804d076601999c7cd769e02e44a99d5b2"],
 "ARB":["0xee5b5b923ffce93a870b3104b7ca09c3db80047a","0x361ad597f6a0cf86f8ab14234ca17a5739a67458"],
 "ATH":["0xaf8dcd50fdc14e413e5ef4468d4d21a961a7dcfd","0x651641299c7ec0aa44ad7ed9b7e12702fed2022f","0x8714909ac67adb799df8901b1825234215c96e19"],
 "AXL":["0xf42aac93ab142090db9fdc0bc86aab73cb36f173","0xab782bc7d4a2b306825de5a7730034f8f63ee1bc"],
 "COMP":["0x841ed663f2636863d40be4ee76243377dff13a34","0x6522b7f9d481eceb96557f44753a4b893f837e90"],
 "CRV":["0x88a1493366d48225fc3cefbdae9ebb23e323ade3"],
 "ENS":["0x498697892fd0e5e3a16bd40d7bf2644f33cbbbd4","0x187c9fbf5bd0f266883c03f320260c407c7b4100"],
 "GRT":["0x823fd1a44a37a4be35c3b0c8b11463cc4f27396c","0xeb8ee0503e0301720eb7616e0897f8ecdf751fc3"],
 "LDO":["0x88a1493366d48225fc3cefbdae9ebb23e323ade3","0xffa8db7b38579e6a2d14f9b347a9ace4d044cd54"],
 "MPL_SYRUP":["0x517ce9b6d1fcffd29805c3e19b295247fcd94aef","0x89860fbeab8d59858c57c920f39f5d7ba48d0722"],
 "OP":["0xb18fe4b95b7d633c83689b5ed3ac4ad0a857a2a7"],
 "POL":["0x4c569c1e541a19132ac893748e0ad54c7c989ff4"],
 "RPL":["0x07a98956df1b3a555f8f8408e280d6342451daaa"],
}
BORDERLINE={"5lzkatrlwhycqj2yuvbjjgsdzzbk6yfl4pfqrjmtbot2","gem2vaypsg7ai7vjdkpttqfahpoqwkfgvkyzx3rpotka"}

depin15=[t for t in frame if frame[t]["category"]=="DePIN" and frame[t]["measurement_type"]=="governance_token"]
defi15=[t for t in frame if frame[t]["category"]=="DeFi" and frame[t]["measurement_type"]=="governance_token" and t not in("FXS","SNX","GNO")]
defi24=[t for t in frame if frame[t]["category"]=="DeFi"]

def scope_hhi(scope):
    # scope: dict token-> list addrs (subset of FULL)
    out={}
    for t in frame:
        extra=scope.get(t,[])
        if extra:
            v=hhi(t,frozenset(extra))
            out[t]= v if v is not None else fnum(frame[t]["hhi"])
        else:
            out[t]=fnum(frame[t]["hhi"])
    # IO truncated -> always keep frame
    out["IO"]=fnum(frame["IO"]["hhi"])
    return out

def contr(hd, depin, defi):
    dep=[hd[t] for t in depin]; df=[hd[t] for t in defi]
    u,p=ss.mannwhitneyu(dep,df,alternative="two-sided")
    a,b=np.array(dep),np.array(df);na,nb=len(a),len(b)
    sp=math.sqrt(((na-1)*a.var(ddof=1)+(nb-1)*b.var(ddof=1))/(na+nb-2));d=(a.mean()-b.mean())/sp
    return p,d,a.mean(),b.mean()

scopes={
 "0 current (frame)": {},
 "A JUP-only {Upbit,Backpack,Bybit}": {"JUP":FULL["JUP"]},
 "A' JUP {Upbit,Backpack} only (live-confirmed)": {"JUP":["27b4PRN7K37rpTywq65t29rjuNfQkYpxZUjkbtHc5VvZ","43DbAvKxhXh1oSxkJSqGosNw3HpBnmsWiak6tB5wpecN"]},
 "B JUP+cycle3-HNT (min Cycle-6 closeout)": {"JUP":["27b4PRN7K37rpTywq65t29rjuNfQkYpxZUjkbtHc5VvZ","43DbAvKxhXh1oSxkJSqGosNw3HpBnmsWiak6tB5wpecN"],"HNT":["22Wnk8PwyWZV7BfkZGJEKT9jGGdtvu7xY6EXeRh7zkBa","53unSgGWqEWANcPYRF35B2Bgf8BkszUtcccKiXwGGLyr"]},
 "C full 52-protocol audit (42 wallets)": FULL,
 "C- full minus borderline (5LZk,Gem2VAyp)": {t:[a for a in v if a.lower() not in BORDERLINE] for t,v in FULL.items()},
}
print(f"{'scope':<48}{'bal30_p':>9}{'bal30_d':>9}{'bal_ratio':>10}{'full_p':>9}{'full_d':>9}")
for name,sc in scopes.items():
    hd=scope_hhi(sc)
    p,d,dm,fm=contr(hd,depin15,defi15)
    fp,fd,_,_=contr(hd,depin15,defi24)
    print(f"{name:<48}{p:>9.4f}{d:>+9.3f}{dm/fm:>10.2f}{fp:>9.4f}{fd:>+9.3f}")
print("\npaper of-record: balanced-30 p=0.020 d=0.94 ratio=2.3 ; full-frame p=0.0234 d=0.939")
