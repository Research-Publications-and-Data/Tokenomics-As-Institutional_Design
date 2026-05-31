#!/usr/bin/env python3
"""B2 full CEX-exclusion recompute + contrast re-run (READ-ONLY analysis; writes nothing canonical).
Validates each affected protocol reproduces the of-record frame with CURRENT exclusions,
then applies the new Nansen-confirmed CEX additions, then re-runs balanced-30 / full-frame /
3-class contrasts. As-of 2026-05-31."""
import csv, os, math
import numpy as np
from scipy import stats as ss

SIB = "/Users/zach/Tokenomics-As-Institutional_Design"
HLD = [os.path.join(SIB, "data/raw/holder_lists"), "/Users/zach/b2-governance-data/data/raw/holder_lists"]
FRAME = os.path.join(SIB, "data/processed/regression_data_april2026.csv")
ADIR = os.path.join(SIB, "b2/paper/analysis_n52_2026-05-29")
EXCL_SRCS = [
    (os.path.join(SIB, "data/processed/exclusions_log.csv"), "token", "address"),
    (os.path.join(ADIR, "new12_unified_exclusions_2026-05-29.csv"), "token", "address"),
    (os.path.join(ADIR, "b2_pca_exclusions_consolidated_2026-05-29.csv"), "token", "address"),
]

def load_holders(tok):
    for d in HLD:
        p = os.path.join(d, f"{tok}_holders.csv")
        if os.path.exists(p):
            return list(csv.DictReader(open(p)))
    return None

# current per-token exclusion union (lowercased)
cur = {}
for path, tcol, acol in EXCL_SRCS:
    if not os.path.exists(path):
        continue
    for r in csv.DictReader(open(path)):
        t = (r.get(tcol) or "").strip().upper()
        a = (r.get(acol) or "").strip().lower()
        if t and a:
            cur.setdefault(t, set()).add(a)

# frame
frame = {}
for r in csv.DictReader(open(FRAME)):
    frame[r["token"]] = r

def fnum(x):
    try: return float(x)
    except: return None

def hhi_topn(tok, extra_excl=frozenset()):
    rows = load_holders(tok)
    if not rows:
        return None
    ex = cur.get(tok, set()) | {a.lower() for a in extra_excl}
    surv = [(r["address"], float(r["balance"])) for r in rows if r["address"].strip().lower() not in ex]
    T = sum(b for _, b in surv)
    if T <= 0:
        return None
    shares = sorted((b / T for _, b in surv), reverse=True)
    hhi = sum(s * s for s in shares)
    return {"hhi": hhi, "top1": shares[0]*100, "top5": sum(shares[:5])*100,
            "top10": sum(shares[:10])*100, "n": len(surv), "n_excl": len(ex)}

# NEW Nansen-confirmed CEX additions: token -> [(addr, label)]
NEW_CEX = {
    # Solana
    "JUP": [("27b4PRN7K37rpTywq65t29rjuNfQkYpxZUjkbtHc5VvZ","Upbit"),
            ("43DbAvKxhXh1oSxkJSqGosNw3HpBnmsWiak6tB5wpecN","Backpack Exchange"),
            ("Gem2VAypSg7Ai7vjDKPTtqFahpoQWkfgVkyzx3rPoTka","Bybit Hot Wallet")],
    "DRIFT": [("FH9iLV5Z8EUEDMnW6CzUPkpDhWJCsHqJ5N4W23njNsUo","Upbit Internal"),
              ("EPpctwZpP7LE61Xkpbb9ixfxMFD8fFAxewe7dTk6dg1M","Coinbase Deposit"),
              ("5LZkATrLwHYCQj2YuVbjjgsDZzBk6YfL4pFQRJmtboT2","Bybit Hot Wallet [borderline]"),
              ("8Mm46CsqxiyAputDUp2cXHg41HE3BfynTeMBDwzrMZQH","Bithumb Hot Wallet")],
    "HNT": [("5LZkATrLwHYCQj2YuVbjjgsDZzBk6YfL4pFQRJmtboT2","Bybit Hot Wallet [borderline]"),
            ("22Wnk8PwyWZV7BfkZGJEKT9jGGdtvu7xY6EXeRh7zkBa","Crypto.com"),
            ("53unSgGWqEWANcPYRF35B2Bgf8BkszUtcccKiXwGGLyr","Binance US Hot Wallet"),
            ("EFE3j1pcSP1paUzA86zW7989ZjsFP2J7ginyUqo4ewqR","Kraken")],
    "HONEY": [("FsAA2JoVBLin4CbGk16eCjQM4Etixz9cbT1smJvfC6NQ","Coinbase Deposit"),
              ("3A6s38hSeXDrapWiAR7pRxyaJSiCbGLeKmEZSA9Tix4F","Coinbase Deposit"),
              ("5YMPkRAQN6S6sVw3hLwPGqg8w9ZDiVDwFdYNFK2QYJzp","Coinbase Deposit")],
    "RENDER": [("7TWnq4WeYcwQWBCwKeEX2Q9xqVtthPGkB7adNvueuVuh","Bitget Deposit")],
    "W": [("5LZkATrLwHYCQj2YuVbjjgsDZzBk6YfL4pFQRJmtboT2","Bybit Hot Wallet [borderline]"),
          ("8Mm46CsqxiyAputDUp2cXHg41HE3BfynTeMBDwzrMZQH","Bithumb Hot Wallet")],
    "IO": [("8Mm46CsqxiyAputDUp2cXHg41HE3BfynTeMBDwzrMZQH","Bithumb Hot Wallet [HOLDER LIST TRUNCATED]")],
    # EVM
    "AAVE": [("0x5a801a9418d036fd453078c3adcb761fdc5ae695","Upbit Hot Wallet")],
    "ANYONE": [("0x446b86a33e2a438f569b15855189e3da28d027ba","KuCoin"),
               ("0xaa10db8804d076601999c7cd769e02e44a99d5b2","KuCoin Deposit")],
    "ARB": [("0xee5b5b923ffce93a870b3104b7ca09c3db80047a","Bybit"),
            ("0x361ad597f6a0cf86f8ab14234ca17a5739a67458","Bithumb Wallet")],
    "ATH": [("0xaf8dcd50fdc14e413e5ef4468d4d21a961a7dcfd","Upbit Internal"),
            ("0x651641299c7ec0aa44ad7ed9b7e12702fed2022f","Bybit"),
            ("0x8714909ac67adb799df8901b1825234215c96e19","Bithumb Deposit")],
    "AXL": [("0xf42aac93ab142090db9fdc0bc86aab73cb36f173","Bybit Hot Wallet"),
            ("0xab782bc7d4a2b306825de5a7730034f8f63ee1bc","Bitvavo Hot Wallet")],
    "COMP": [("0x841ed663f2636863d40be4ee76243377dff13a34","Robinhood Hot Wallet"),
             ("0x6522b7f9d481eceb96557f44753a4b893f837e90","Bybit")],
    "CRV": [("0x88a1493366d48225fc3cefbdae9ebb23e323ade3","Bybit")],
    "ENS": [("0x498697892fd0e5e3a16bd40d7bf2644f33cbbbd4","Bithumb Hot Wallet"),
            ("0x187c9fbf5bd0f266883c03f320260c407c7b4100","Bybit")],
    "GRT": [("0x823fd1a44a37a4be35c3b0c8b11463cc4f27396c","Upbit"),
            ("0xeb8ee0503e0301720eb7616e0897f8ecdf751fc3","Bithumb Wallet")],
    "LDO": [("0x88a1493366d48225fc3cefbdae9ebb23e323ade3","Bybit"),
            ("0xffa8db7b38579e6a2d14f9b347a9ace4d044cd54","Bitget Deposit")],
    "MPL_SYRUP": [("0x517ce9b6d1fcffd29805c3e19b295247fcd94aef","FalconX Deposit"),
                  ("0x89860fbeab8d59858c57c920f39f5d7ba48d0722","Upbit Main Wallet")],
    "OP": [("0xb18fe4b95b7d633c83689b5ed3ac4ad0a857a2a7","Bithumb Wallet")],
    "POL": [("0x4c569c1e541a19132ac893748e0ad54c7c989ff4","Upbit MATIC Main Wallet")],
    "RPL": [("0x07a98956df1b3a555f8f8408e280d6342451daaa","Bithumb Wallet")],
}

print("="*120)
print("PER-PROTOCOL RECOMPUTE: validate current vs frame, then apply new CEX")
print("="*120)
print(f"{'tok':<10}{'cat':<6}{'frame_hhi':>11}{'recomp_cur':>12}{'val':>5}{'recomp_new':>12}{'delta':>10}{'t1_old':>8}{'t1_new':>8}{'n_new_cex':>10}")
newhhi = {}
validation_fail = []
for tok in sorted(NEW_CEX):
    fr = frame.get(tok)
    cat = fr["category"][:5] if fr else "?"
    fhhi = fnum(fr["hhi"]) if fr else None
    rc = hhi_topn(tok)               # current exclusions only
    rn = hhi_topn(tok, frozenset(a for a,_ in NEW_CEX[tok]))  # + new cex
    if rc is None:
        print(f"{tok:<10}{cat:<6}  NO HOLDER LIST")
        continue
    val = "OK" if (fhhi is not None and abs(rc["hhi"]-fhhi) < 2e-3) else "DIFF"
    if val == "DIFF":
        validation_fail.append((tok, fhhi, rc["hhi"]))
    delta = rn["hhi"]-fhhi if fhhi is not None else None
    newhhi[tok] = rn["hhi"]
    print(f"{tok:<10}{cat:<6}{fhhi if fhhi else 0:>11.6f}{rc['hhi']:>12.6f}{val:>5}{rn['hhi']:>12.6f}{(delta if delta is not None else 0):>+10.6f}{fr and fnum(fr['top1_pct']) or 0:>8.2f}{rn['top1']:>8.2f}{len(NEW_CEX[tok]):>10}")

print("\nVALIDATION FAILURES (current recompute != frame within 2e-3):", validation_fail if validation_fail else "NONE")

# ---- Build new frame HHI dict (affected -> new; else frame) ----
def cat_of(tok): return frame[tok]["category"]
def mtype(tok): return frame[tok]["measurement_type"]
def hhi_now(tok):
    return newhhi.get(tok, fnum(frame[tok]["hhi"]))

# IO: holder list truncated -> cannot recompute; keep frame value, FLAG.
if "IO" in newhhi:
    io_rn = hhi_topn("IO", frozenset(a for a,_ in NEW_CEX["IO"]))
    # truncated list -> unreliable; revert to frame for contrast, flag separately
    print(f"\n[IO FLAG] holder list truncated to {io_rn['n']} survivors; recompute UNRELIABLE. "
          f"Reverting IO to frame value {frame['IO']['hhi']} for contrasts; Bithumb 2.06% exclusion deferred.")
    newhhi.pop("IO")

def contrast(depin_toks, defi_toks, label):
    dep = [hhi_now(t) for t in depin_toks]
    df  = [hhi_now(t) for t in defi_toks]
    u,p = ss.mannwhitneyu(dep, df, alternative="two-sided")
    a,b = np.array(dep), np.array(df); na,nb=len(a),len(b)
    sp = math.sqrt(((na-1)*a.var(ddof=1)+(nb-1)*b.var(ddof=1))/(na+nb-2))
    d = (a.mean()-b.mean())/sp
    print(f"\n### {label}")
    print(f"  DePIN n={na} mean={a.mean():.4f} median={np.median(a):.4f}   DeFi n={nb} mean={b.mean():.4f} median={np.median(b):.4f}   ratio={a.mean()/b.mean():.2f}")
    print(f"  Mann-Whitney p={p:.4f}  Cohen d={d:+.3f}   [{'SIG' if p<0.05 else 'n.s.'}]")
    return p, d, a.mean(), b.mean()

# membership
depin15 = [t for t in frame if cat_of(t)=="DePIN" and mtype(t)=="governance_token"]
defi_gov15 = [t for t in frame if cat_of(t)=="DeFi" and mtype(t)=="governance_token" and t not in ("FXS","SNX","GNO")]
defi_all24 = [t for t in frame if cat_of(t)=="DeFi"]
defi18 = defi_gov15 + ["FXS","SNX","GNO"]

print("\n"+"="*120); print("CONTRAST RE-RUN (new HHIs)"); print("="*120)
print(f"DePIN-15: {sorted(depin15)}")
print(f"DeFi-gov-15: {sorted(defi_gov15)}")

print("\n----- BEFORE (frame of record) -----")
def contrast_frame(depin_toks, defi_toks, label):
    dep=[fnum(frame[t]['hhi']) for t in depin_toks]; df=[fnum(frame[t]['hhi']) for t in defi_toks]
    u,p=ss.mannwhitneyu(dep,df,alternative="two-sided")
    a,b=np.array(dep),np.array(df); na,nb=len(a),len(b)
    sp=math.sqrt(((na-1)*a.var(ddof=1)+(nb-1)*b.var(ddof=1))/(na+nb-2)); d=(a.mean()-b.mean())/sp
    print(f"  {label}: DePIN mean={a.mean():.4f} DeFi mean={b.mean():.4f} ratio={a.mean()/b.mean():.2f} p={p:.4f} d={d:+.3f}")
contrast_frame(depin15, defi_gov15, "balanced-30 (15v15)")
contrast_frame(depin15, defi_all24, "full-frame (15 DePIN vs 24 DeFi)")

print("\n----- AFTER (CEX-excluded) -----")
contrast(depin15, defi_gov15, "balanced-30 (15v15)  [HEADLINE; paper p=0.020 d=0.94]")
contrast(depin15, defi_all24, "full-frame (15 DePIN vs 24 DeFi)  [paper p=0.0234 d=0.939]")

# 3-class Kruskal + Dunn (DePIN15 / DeFi18 / L1-11)
l1_11 = [t for t in frame if cat_of(t)=="L1_L2_Infra"]
def kw3(label):
    g={"DePIN":[hhi_now(t) for t in depin15],"DeFi":[hhi_now(t) for t in defi18],"L1":[hhi_now(t) for t in l1_11]}
    H,p=ss.kruskal(*g.values())
    print(f"\n### {label}: KW H={H:.3f} p={p:.4f}")
    for k,v in g.items(): print(f"    {k:5} n={len(v)} mean={np.mean(v):.4f} median={np.median(v):.4f}")
    # DePIN vs DeFi Dunn-ish via mannwhitney for direction
    u,pp=ss.mannwhitneyu(g["DePIN"],g["DeFi"],alternative="two-sided")
    print(f"    DePIN-vs-DeFi (MW for direction) p={pp:.4f}")
kw3("3-class AFTER (DePIN15/DeFi18/L1-11)")

print("\n"+"="*120)
print("EXCLUSION-COUNT MAGNITUDE")
print("="*120)
new_rows = sum(len(v) for v in NEW_CEX.values())
new_unique = len({a.lower() for v in NEW_CEX.values() for a,_ in v})
prot_touched = len(NEW_CEX)
print(f"  New CEX exclusion rows added: {new_rows}  (unique addresses: {new_unique})  across {prot_touched} protocols")
print(f"  Current exclusions_log data rows: 168 across 44 tokens")
print(f"  -> new total ~ {168+new_rows} rows across ~{44 + len([t for t in NEW_CEX if t not in cur])} tokens (caption '133 exclusions / 38 protocols' changes)")
