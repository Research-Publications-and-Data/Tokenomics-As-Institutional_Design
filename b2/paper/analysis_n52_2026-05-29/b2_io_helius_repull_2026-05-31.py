import os, json, urllib.request, csv, time
key=os.environ["HELIUS_API_KEY"]
mint="BZLbGTNCSFfoth2GYDtwr7e4imWzpR5jqcUuGEwr646K"
url=f"https://mainnet.helius-rpc.com/?api-key={key}"
from collections import defaultdict
owner_bal=defaultdict(int)
page=1; total_accts=0
while page<=200:
    body=json.dumps({"jsonrpc":"2.0","id":"1","method":"getTokenAccounts",
        "params":{"mint":mint,"page":page,"limit":1000}}).encode()
    req=urllib.request.Request(url,data=body,headers={"Content-Type":"application/json"})
    for attempt in range(3):
        try:
            r=json.load(urllib.request.urlopen(req,timeout=60)); break
        except Exception as e:
            if attempt==2: raise
            time.sleep(2)
    ta=r.get("result",{}).get("token_accounts",[])
    if not ta: break
    for a in ta:
        owner_bal[a["owner"]] += int(a["amount"])
    total_accts+=len(ta)
    if len(ta)<1000: break
    page+=1
print(f"pages={page} token_accounts={total_accts} distinct_owners={len(owner_bal)}")
ranked=sorted(owner_bal.items(), key=lambda x:-x[1])
top=ranked[:1000]
# write snapshot
out="/tmp/IO_holders_repull_2026-05-31.csv"
total_all=sum(v for _,v in ranked)          # total over ALL owners
total_top1000=sum(v for _,v in top)
with open(out,"w",newline="") as f:
    w=csv.writer(f); w.writerow(["address","balance","rank","share","token"])
    for i,(o,b) in enumerate(top,1):
        w.writerow([o, b, i, b/total_top1000, "IO"])
print("wrote", out)
# raw HHI over top-1000 (paper convention: renormalize over top-1000)
sh=[b/total_top1000 for _,b in top]
hhi=sum(s*s for s in sh)
print(f"IO RAW (repull, top-1000): HHI={hhi:.6f} top1={sh[0]*100:.2f}% top5={sum(sh[:5])*100:.2f}% top10={sum(sh[:10])*100:.2f}% n=1000")
print(f"(frame of-record IO: 0.125136 / t1=33.47 / t5=51.34 / t10=61.16)")
print("\nTop 15 owners (address, balance, share):")
for i,(o,b) in enumerate(top[:15],1):
    print(f"  {i:>2} {o} {b} {b/total_top1000*100:.2f}%")
