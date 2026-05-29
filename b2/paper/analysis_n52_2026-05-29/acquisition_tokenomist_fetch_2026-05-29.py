#!/usr/bin/env python3
"""ACQUISITION-SOURCE FETCH (2026-05-29). tokenomist.ai/<slug> verbatim HTML fetch (the unlock/vesting/allocation source; curl, embeds data in the Next.js RSC payload)
Saves verbatim responses into acquisition_sources/ for reproducibility."""
import subprocess, os, re
OUT="b2/paper/analysis_n52_2026-05-29/acquisition_sources"
# token -> candidate tokenomist slugs (try in order)
CAND={
 "ALGO":["algorand"],"ANYONE":["anyone-protocol","ator","anyone"],"BONK":["bonk"],"DIMO":["dimo"],
 "GNO":["gnosis"],"HONEY":["hivemapper","honey"],"IO":["io-net","ionet","io"],"IOTX":["iotex"],
 "LPT":["livepeer"],"META":["metadao","meta-dao","metadao-fi"],"MKR":["maker","makerdao","sky"],
 "POKT":["pocket-network","pokt"],"POL":["polygon","polygon-ecosystem-token","matic-network"],
 "RENDER":["render","render-token","render-network"],"W":["wormhole"],
 "WLFI":["world-liberty-financial","wlfi","worldliberty"],"WXM":["weatherxm","weatherxm-network"]}
def get(slug):
    r=subprocess.run(["curl","-s","-w","\n%{http_code}","https://tokenomist.ai/"+slug,"-H","User-Agent: Mozilla/5.0"],capture_output=True,text=True,timeout=60).stdout
    body,_,code=r.rpartition("\n")
    return body,code.strip()
import time
ok=0
for tok,cands in CAND.items():
    saved=False
    for slug in cands:
        body,code=get(slug)
        # valid if 200, has tokenomics data, and looks like the right token (symbol or allocation present)
        if code=="200" and len(body)>50000 and re.search(r'(allocation|unlock|vesting|Participation|Investors|Treasury)', body, re.I):
            open(f"{OUT}/{tok}_tokenomist_{slug}.html","w").write(body)  # VERBATIM
            # extract allocation/vesting snippets
            allocs=re.findall(r'([A-Z][A-Za-z &/]{2,40}) (?:at )?([0-9]{1,2}\.?[0-9]{0,2})%', body)
            allocs=[(a.strip(),p) for a,p in allocs if 0<float(p)<=100][:8]
            print(f"  {tok:8} slug={slug:26} OK {len(body)//1024}KB  allocs={allocs[:5]}")
            saved=True; ok+=1; break
        time.sleep(0.8)
    if not saved: print(f"  {tok:8} NO valid tokenomist page (tried {cands})")
    time.sleep(0.6)
print(f"\nsaved {ok}/{len(CAND)} verbatim tokenomist pages")
