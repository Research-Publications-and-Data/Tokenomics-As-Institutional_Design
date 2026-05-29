#!/usr/bin/env python3
"""CORRECTED post-exclusion top-10 for the new-12, merging ALL exclusion sources:
  - data/processed/exclusions_log.csv                              (main; WLFI/ENA/Solana)
  - b2/paper/supplements/phase4_evm_minibatch_exclusions_v2_audited_2026-05-27.csv  (FXS/SNX/GNO)
The earlier precompute used only the main log and kept addresses that the v2-audited
EVM minibatch excludes (FXS r1 Fraxtal bridge, SNX r1 Synthetix Core, GNO null-burn +
co-founder Safes), so its post-exclusion top-10 was wrong for FXS/SNX/GNO. This corrects it.
DOT/TAO/ALGO exclusions live in per-protocol artifacts (dot_pca_refined / tao_pca / ALGO json);
their retention is low-confidence (older L1; flagged, not classified here). READ-ONLY.
"""
import csv, os, json

CLONE_A="/Users/zach/Tokenomics-As-Institutional_Design"
CLONE_B="/Users/zach/b2-governance-data"
HL=[os.path.join(CLONE_A,"data/raw/holder_lists"), os.path.join(CLONE_B,"data/raw/holder_lists")]

# --- assemble exclusion address sets per symbol from BOTH sources ---
excl={}   # symbol -> {addr_lower: label}
def add(sym, addr, label):
    excl.setdefault(sym.upper(), {})[addr.strip().lower()] = label

for r in csv.DictReader(open(os.path.join(CLONE_A,"data/processed/exclusions_log.csv"))):
    add(r["token"], r["address"], (r.get("identity","")+" | "+r.get("exclusion_reason","")).strip())
for r in csv.DictReader(open(os.path.join(CLONE_A,"b2/paper/supplements/phase4_evm_minibatch_exclusions_v2_audited_2026-05-27.csv"))):
    add(r["symbol"], r["address"], f"[Class {r.get('pca_class','?')}] {r.get('label','')}")

NEW12={"FXS":"ethereum","SNX":"ethereum","GNO":"ethereum","WLFI":"ethereum","ENA":"ethereum",
       "PUMP":"solana","JTO":"solana","BONK":"solana","KMNO":"solana",
       "DOT":"polkadot","TAO":"bittensor","ALGO":"algorand"}

def load(tok):
    for b in HL:
        p=os.path.join(b,f"{tok}_holders.csv")
        if os.path.exists(p): return list(csv.DictReader(open(p)))
    return None

out={}
for tok,chain in NEW12.items():
    rows=load(tok)
    if not rows: out[tok]={"error":"no holder list"}; continue
    ex=excl.get(tok,{})
    survivors=[r for r in rows if r["address"].strip().lower() not in ex]
    top10=survivors[:10]
    out[tok]={"chain":chain,"n_excluded":len(rows)-len(survivors),
              "top10":[{"rank_orig":r.get("rank"),"address":r["address"].strip(),"share_orig":r.get("share")} for r in top10]}
    print(f"\n### {tok} ({chain}) | excluded={len(rows)-len(survivors)} | CORRECTED post-exclusion top-10:")
    for r in top10:
        print(f"   orig_r{r.get('rank'):>4} {r['address']:46} share={r.get('share')}")

json.dump(out, open(os.path.join(CLONE_A,"b2/paper/analysis_n52_2026-05-29/new12_CORRECTED_top10.json"),"w"), indent=1)
print("\n[written] new12_CORRECTED_top10.json")
