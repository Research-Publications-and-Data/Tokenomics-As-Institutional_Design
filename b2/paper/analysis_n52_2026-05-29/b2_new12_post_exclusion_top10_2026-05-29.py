#!/usr/bin/env python3
"""Precompute post-exclusion top-10 for the new-12 (retention re-fetch inputs).
For each protocol: holder list minus PCA-excluded addresses (exclusions_log.csv,
token-matched) -> top-10 survivors, with any exclusions-log identity annotation
carried for context. Pure data; no external API. Output drives the classification
workflow (classify each survivor insider/not -> insider_count_frac).
READ-ONLY against persisted holder lists + exclusions log.
"""
import csv, os, json

CLONE_A="/Users/zach/Tokenomics-As-Institutional_Design"
CLONE_B="/Users/zach/b2-governance-data"
HL_A=os.path.join(CLONE_A,"data/raw/holder_lists")
HL_B=os.path.join(CLONE_B,"data/raw/holder_lists")
EXCL=os.path.join(CLONE_A,"data/processed/exclusions_log.csv")

PROTOS=["FXS","SNX","GNO","WLFI","ENA","PUMP","JTO","BONK","KMNO","DOT","TAO","ALGO"]
CHAIN={"FXS":"ethereum","SNX":"ethereum","GNO":"ethereum","WLFI":"ethereum","ENA":"ethereum",
       "PUMP":"solana","JTO":"solana","BONK":"solana","KMNO":"solana",
       "DOT":"polkadot","TAO":"bittensor","ALGO":"algorand"}

# load exclusions, keyed by (token, lowercased address)
excl={}
for r in csv.DictReader(open(EXCL)):
    excl.setdefault(r["token"].upper(), {})[r["address"].strip().lower()] = (r.get("identity","")+" || "+r.get("exclusion_reason","")).strip()

def load_holders(tok):
    for base in (HL_A, HL_B):
        p=os.path.join(base, f"{tok}_holders.csv")
        if os.path.exists(p):
            return list(csv.DictReader(open(p))), p
    return None, None

out={}
for tok in PROTOS:
    rows, path = load_holders(tok)
    if rows is None:
        out[tok]={"error":"holder list not found"}; print(f"{tok}: NOT FOUND"); continue
    ex = excl.get(tok, {})
    survivors=[]
    n_excluded=0
    for r in rows:
        addr=r["address"].strip()
        if addr.lower() in ex:
            n_excluded+=1; continue
        survivors.append(r)
    # survivors are already rank-sorted in the source; take top-10
    top10=survivors[:10]
    out[tok]={"chain":CHAIN[tok], "n_holders_listed":len(rows), "n_excluded_matched":n_excluded,
              "top10":[{"rank_orig":r.get("rank"), "address":r["address"].strip(),
                        "share_orig":r.get("share"), "balance":r.get("balance")} for r in top10]}
    print(f"\n### {tok} ({CHAIN[tok]}) | listed={len(rows)} excluded_matched={n_excluded} | post-exclusion top-10:")
    for r in top10:
        a=r["address"].strip()
        note = ""  # survivors are NOT excluded; show if any excl-log entry exists for context (should be none)
        print(f"   r{r.get('rank'):>3} {a:46} share={r.get('share')}")

with open(os.path.join(CLONE_A,"b2/paper/analysis_n52_2026-05-29/new12_post_exclusion_top10.json"),"w") as f:
    json.dump(out,f,indent=1)
print("\n[written] new12_post_exclusion_top10.json")
