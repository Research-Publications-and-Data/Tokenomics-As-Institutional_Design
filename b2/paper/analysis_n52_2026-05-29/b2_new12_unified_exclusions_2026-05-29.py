#!/usr/bin/env python3
"""DETERMINISTIC PREP for the new-12 retention re-fetch: unify every exclusion source
into one consistent set + recompute the correct post-exclusion top-10, so the fresh
reproduction-pipeline session classifies survivors against a clean base (no API, no
insider-judgment here -- pure data assembly).

Sources unified (EVM-5 + Solana-4, the new-cohort where retention/channel-shift is the story):
  - data/processed/exclusions_log.csv                                 (WLFI/ENA/PUMP/JTO/BONK/KMNO)
  - b2/paper/supplements/phase4_evm_minibatch_exclusions_v2_audited_2026-05-27.csv  (FXS/SNX/GNO)
  - 3 DECIDED corrections missing from the canonical log (HHIs already reflect them;
    recorded here with provenance to close the gap surfaced 2026-05-29).

DOT/TAO/ALGO (older L1; retention low-confidence ~0): exclusions live in per-protocol
artifacts (tao_pca.py + tao_exchange_coldkeys.json; dot_pca_refined in the sibling site
clone exhibits, commit d3a28a97; ALGO_holding_hhi_2026-04-30.json). Flagged for the fresh
session to extract; not assembled here. READ-ONLY against persisted data.
"""
import csv, os, json

import os as _os_anchor
_RR = _os_anchor.path.dirname(_os_anchor.path.abspath(__file__))
while _RR != _os_anchor.path.dirname(_RR) and not _os_anchor.path.exists(_os_anchor.path.join(_RR, "reproduce.py")):
    _RR = _os_anchor.path.dirname(_RR)
A=_RR
B="/Users/zach/b2-governance-data"
HL=[os.path.join(A,"data/raw/holder_lists"), os.path.join(B,"data/raw/holder_lists")]

excl={}   # SYMBOL -> {addr_lower: {"class":..,"label":..,"source":..}}
def add(sym, addr, cls, label, source):
    excl.setdefault(sym.upper(), {})[addr.strip().lower()] = {"class":cls,"label":label,"source":source}

# source 1: main exclusions log
for r in csv.DictReader(open(os.path.join(A,"data/processed/exclusions_log.csv"))):
    lbl=(r.get("identity","")+" | "+r.get("exclusion_reason","")).strip(" |")
    # main log embeds [Class N] in the reason text; leave class blank if not parseable
    cls=""
    import re
    m=re.search(r"\[Class\s*(\d)\]", lbl)
    if m: cls=m.group(1)
    add(r["token"], r["address"], cls, lbl, "exclusions_log.csv")

# source 2: phase4 EVM v2-audited (FXS/SNX/GNO)
for r in csv.DictReader(open(os.path.join(A,"b2/paper/supplements/phase4_evm_minibatch_exclusions_v2_audited_2026-05-27.csv"))):
    add(r["symbol"], r["address"], r.get("pca_class",""), r.get("label",""), "phase4_evm_minibatch_exclusions_v2_audited_2026-05-27.csv")

# source 3: the 3 DECIDED corrections missing from the canonical log (HHIs already reflect them)
CORR=[
 ("ENA","0x8be3460a480c80728a8c4d7a5d5303c85ba7b3b9","3","Ethena Staked ENA (sENA) staking aggregation","CORRECTED 2026-05-29; missing from canonical log; HHI 0.0467->0.0472"),
 ("WLFI","0x003ca23fd5f0ca87d01f6ec6cd14a8ae60c2b97d","5","DolomiteMargin (DeFi protocol custody)","CORRECTED 2026-05-29; HHI 0.1265->0.1557"),
 ("WLFI","0xc785d05961b3c537cac11f1d496876a255f6d650","4","LockReleaseTokenPool (CCIP bridge)","CORRECTED 2026-05-29; HHI 0.1265->0.1557"),
]
for sym,a,cls,lbl,src in CORR: add(sym,a,cls,lbl,src)

NEW9={"FXS":"ethereum","SNX":"ethereum","GNO":"ethereum","WLFI":"ethereum","ENA":"ethereum",
      "PUMP":"solana","JTO":"solana","BONK":"solana","KMNO":"solana"}

def load(tok):
    for b in HL:
        p=os.path.join(b,f"{tok}_holders.csv")
        if os.path.exists(p): return list(csv.DictReader(open(p)))
    return None

# write unified exclusions CSV (provenance-tracked)
unified_rows=[]
for tok in NEW9:
    for addr,meta in excl.get(tok.upper(),{}).items():
        unified_rows.append({"token":tok,"address":addr,"pca_class":meta["class"],"label":meta["label"][:120],"source":meta["source"]})
outdir=os.path.join(A,"b2/paper/analysis_n52_2026-05-29")
with open(os.path.join(outdir,"new12_unified_exclusions_2026-05-29.csv"),"w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=["token","address","pca_class","label","source"]); w.writeheader(); w.writerows(unified_rows)

# recompute correct post-exclusion top-10
top10={}
for tok,chain in NEW9.items():
    rows=load(tok)
    if not rows: top10[tok]={"error":"no holder list"}; continue
    ex=excl.get(tok.upper(),{})
    survivors=[r for r in rows if r["address"].strip().lower() not in ex]
    t10=survivors[:10]
    top10[tok]={"chain":chain,"n_excluded_unified":len(rows)-len(survivors),
                "top10":[{"orig_rank":r.get("rank"),"address":r["address"].strip(),"share_orig":r.get("share")} for r in t10]}
    print(f"{tok:5} ({chain:8}) excluded={len(rows)-len(survivors):2}  survivor-top1 share={t10[0].get('share') if t10 else 'NA'}")
top10["_DOT_TAO_ALGO_NOTE"]="exclusions in per-protocol artifacts (tao_pca.py + tao_exchange_coldkeys.json; dot_pca_refined @ site-clone exhibits d3a28a97; ALGO_holding_hhi_2026-04-30.json); retention low-confidence ~0; fresh session extracts + classifies best-effort."
json.dump(top10, open(os.path.join(outdir,"new12_unified_post_exclusion_top10_2026-05-29.json"),"w"), indent=1)

print(f"\n[written] new12_unified_exclusions_2026-05-29.csv ({len(unified_rows)} exclusion rows, EVM-5 + Solana-4)")
print(f"[written] new12_unified_post_exclusion_top10_2026-05-29.json")
print("DOT/TAO/ALGO: flagged (per-protocol artifacts; retention low-confidence ~0).")
