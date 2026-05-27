#!/usr/bin/env python3
"""Nominator-overlap clustering with correct endpoint."""
import json, urllib.request, time
from collections import defaultdict

API_KEY = "c8625edf41b845a393ff24fe5d3bb132"
UA = "Mozilla/5.0"
URL = "https://polkadot.api.subscan.io/api/scan/staking/nominators"

d = json.load(open("/tmp/b2_phase4/dot_validators_classified.json"))
unverif = [v for v in d["validators"] if v["operator_class"] == "Unverified"]
unverif.sort(key=lambda x: -x["bonded_total_dot"])

# Sample top-25 unverified + top-15 Binance + top-10 institutional for cross-comparison
sample = unverif[:25]
# Also include verified for control
binance = [v for v in d["validators"] if v["operator_class"] == "CEX:Binance"]
inst = [v for v in d["validators"] if v["operator_class"].startswith("Institutional:")]
sample = sample + binance[:10] + inst[:10]

addr_to_nominators = {}
addr_to_meta = {}
print(f"Pulling nominator lists for {len(sample)} validators (top-25 unverified + 10 Binance + 10 Institutional)...")
for i, v in enumerate(sample, 1):
    addr = v["address"]
    body = json.dumps({"address": addr, "is_validator": True, "row": 100, "page": 0}).encode()
    req = urllib.request.Request(URL, data=body, headers={
        "Content-Type": "application/json", "User-Agent": UA, "X-API-Key": API_KEY,
    }, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            resp = json.load(r)
        if resp.get("code") == 0:
            data = resp.get("data", {})
            count = data.get("count", 0)
            noms = data.get("list", []) or []
            nom_addrs = [n.get("nominator_stash", "") for n in noms]
            addr_to_nominators[addr] = set(filter(None, nom_addrs))
            addr_to_meta[addr] = {"class": v["operator_class"], "display": v["display"], "stake": v["bonded_total_dot"], "n_pulled": len(noms), "n_total": count}
            if i <= 5 or v["operator_class"] != "Unverified":
                print(f"  #{i:>2}  {v['display'][:25]:<25} cls={v['operator_class'][:25]:<25} pulled={len(noms)}/{count}")
        time.sleep(0.3)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")[:80] if hasattr(e, "read") else ""
        print(f"  #{i} HTTP {e.code}: {body}")
    except Exception as e:
        print(f"  #{i} err: {e}")

# Pairwise overlap
print(f"\n=== Pairwise nominator-overlap (>=5 shared nominators) ===")
addrs = list(addr_to_nominators.keys())
overlap_pairs = []
for i in range(len(addrs)):
    for j in range(i+1, len(addrs)):
        a, b = addrs[i], addrs[j]
        sh = addr_to_nominators[a] & addr_to_nominators[b]
        if len(sh) >= 5:
            overlap_pairs.append((a, b, len(sh)))
overlap_pairs.sort(key=lambda x: -x[2])
print(f"Found {len(overlap_pairs)} pairs with >=5 shared nominators")
for a, b, n in overlap_pairs[:30]:
    ma = addr_to_meta[a]
    mb = addr_to_meta[b]
    print(f"  shared={n:>3}  {ma['display'][:20] or a[:20]:<20} [{ma['class'][:15]:<15}]  <->  {mb['display'][:20] or b[:20]:<20} [{mb['class'][:15]}]")

# Union-find clustering
parent = {a: a for a in addrs}
def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]; x = parent[x]
    return x
def union(a, b):
    ra, rb = find(a), find(b)
    if ra != rb: parent[ra] = rb

for a, b, _ in overlap_pairs:
    union(a, b)

clusters = defaultdict(list)
for a in addrs:
    clusters[find(a)].append(a)
multi = [(r, m) for r, m in clusters.items() if len(m) >= 2]
multi.sort(key=lambda x: -len(x[1]))

print(f"\n=== Operator-cluster connected components ({len(multi)} multi-validator clusters) ===")
for root, members in multi:
    total_stake = sum(addr_to_meta[m]["stake"] for m in members)
    classes = set(addr_to_meta[m]["class"] for m in members)
    displays = [addr_to_meta[m]["display"] or "Unverified" for m in members]
    print(f"\n  Cluster of {len(members)} validators ({total_stake:,.0f} DOT total; classes={classes}):")
    for m in members:
        meta = addr_to_meta[m]
        print(f"    {meta['display'][:30] or m[:24]:<32} cls={meta['class'][:20]:<20} stake={meta['stake']:>10,.0f}  noms_total={meta['n_total']}")

# Save
with open("/tmp/b2_phase4/dot_nominator_overlap_v2.json", "w") as f:
    json.dump({
        "n_sampled": len(sample),
        "overlap_pairs": [(a, b, n) for a, b, n in overlap_pairs],
        "clusters": [{"root": r, "members": m, "total_stake_dot": sum(addr_to_meta[mm]["stake"] for mm in m)} for r, m in multi],
    }, f, default=str, indent=2)
