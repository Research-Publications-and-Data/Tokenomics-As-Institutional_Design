#!/usr/bin/env python3
"""ACQUISITION-SOURCE FETCH (2026-05-29). CoinGecko Pro /coins/<id> verbatim fetch for the 17 not-in-DefiLlama protocols (run via scripts/with_api_key.sh coingecko --)
Saves verbatim responses into acquisition_sources/ for reproducibility."""
import os, json, csv, subprocess, time
KEY=os.environ["COINGECKO_API_KEY"]
OUT="b2/paper/analysis_n52_2026-05-29/acquisition_sources"
# the 17 not-in-DefiLlama; token -> coingecko id
IDS={"ALGO":"algorand","ANYONE":"airtor-protocol","BONK":"bonk","DIMO":"dimo","GNO":"gnosis",
 "HONEY":"hivemapper","IO":"io","IOTX":"iotex","LPT":"livepeer","META":"meta-2-2","MKR":"maker",
 "POKT":"pocket-network","POL":"polygon-ecosystem-token","RENDER":"render-token","W":"wormhole",
 "WLFI":"world-liberty-financial","WXM":"weatherxm-network"}
def fetch(cid):
    url=f"https://pro-api.coingecko.com/api/v3/coins/{cid}?localization=false&tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=false"
    out=subprocess.run(["curl","-s",url,"-H",f"x-cg-pro-api-key: {KEY}"],capture_output=True,text=True,timeout=60).stdout
    return out
summary=[]
for tok,cid in IDS.items():
    raw=fetch(cid)
    try: d=json.loads(raw)
    except: print(f"  {tok:8} ({cid}) PARSE FAIL: {raw[:80]}"); continue
    if "error" in d or "id" not in d:
        print(f"  {tok:8} ({cid}) ERR: {str(d)[:80]}"); summary.append({"token":tok,"cg_id":cid,"status":"id-error","homepage":"","max_supply":"","total_supply":""}); time.sleep(1.5); continue
    open(f"{OUT}/{tok}_coingecko.json","w").write(raw)  # VERBATIM
    md=d.get("market_data",{}) or {}
    links=d.get("links",{}) or {}
    hp=(links.get("homepage") or [""])[0]
    wl=links.get("whitepaper") or ""
    repo=(links.get("repos_url",{}) or {}).get("github") or []
    summary.append({"token":tok,"cg_id":cid,"status":"ok","homepage":hp,"whitepaper":wl,
                    "max_supply":md.get("max_supply"),"total_supply":md.get("total_supply"),
                    "circulating_supply":md.get("circulating_supply"),"genesis_date":d.get("genesis_date"),
                    "github":repo[0] if repo else ""})
    print(f"  {tok:8} ({cid:24}) saved {len(raw)//1024}KB  max_supply={md.get('max_supply')}  hp={hp[:42]}")
    time.sleep(1.8)
json.dump(summary, open(f"{OUT}/_coingecko_summary.json","w"), indent=1)
print(f"\nsaved {sum(1 for s in summary if s['status']=='ok')}/{len(IDS)} verbatim CoinGecko coin records")
