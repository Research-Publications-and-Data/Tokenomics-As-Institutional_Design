#!/usr/bin/env python3
"""Investigate the 186-validator cluster (~1.469M DOT each). Check funding source/controller patterns."""
import json, urllib.request, time

API_KEY = "c8625edf41b845a393ff24fe5d3bb132"
UA = "Mozilla/5.0"

d = json.load(open("/tmp/b2_phase4/dot_validators_classified.json"))
vals = d["validators"]

# Get the 1,469,000 bucket
cluster = [v for v in vals if v["operator_class"] == "Unverified" and 1_468_000 <= v["bonded_total_dot"] <= 1_470_000]
print(f"1,469,000 DOT cluster: {len(cluster)} validators")

# Get nominator counts
nom_dist = {}
for v in cluster:
    nc = v["count_nominators"]
    nom_dist[nc] = nom_dist.get(nc, 0) + 1
print(f"\nNominator-count distribution within cluster:")
for nc in sorted(nom_dist.keys()):
    print(f"  {nc:>4} nominators: {nom_dist[nc]} validators")

# Sample first 10 addresses for controller-pattern check via Subscan
print(f"\nSample 10 addresses from cluster (for controller-pattern inspection):")
for v in cluster[:10]:
    print(f"  {v['address']}  bonded_owner={v['bonded_owner_dot']:.2f}  n_noms={v['count_nominators']}")

# Try Subscan's account-detail endpoint for first cluster member to inspect controller / deposit source
print(f"\n=== Sample account detail (cluster member #1): ===")
addr = cluster[0]["address"]
url = "https://polkadot.api.subscan.io/api/v2/scan/search"
body = json.dumps({"key": addr, "row": 1, "page": 0}).encode()
req = urllib.request.Request(url, data=body, headers={
    "Content-Type": "application/json", "User-Agent": UA, "X-API-Key": API_KEY,
}, method="POST")
try:
    with urllib.request.urlopen(req, timeout=15) as r:
        result = json.load(r)
    print(json.dumps(result, indent=2, default=str)[:2000])
except Exception as e:
    print(f"  err: {e}")

# Also test the identity-of-account endpoint
print(f"\n=== Identity endpoint for cluster member #1: ===")
url2 = "https://polkadot.api.subscan.io/api/v2/scan/account/identity"
body2 = json.dumps({"address": addr}).encode()
req2 = urllib.request.Request(url2, data=body2, headers={
    "Content-Type": "application/json", "User-Agent": UA, "X-API-Key": API_KEY,
}, method="POST")
try:
    with urllib.request.urlopen(req2, timeout=15) as r:
        result = json.load(r)
    print(json.dumps(result, indent=2, default=str)[:1500])
except Exception as e:
    print(f"  err: {e}")

# Try /api/scan/account for batch identity resolution
print(f"\n=== Sample-10 batch identity resolution via /api/v2/scan/account: ===")
url3 = "https://polkadot.api.subscan.io/api/v2/scan/account"
for v in cluster[:5]:
    body = json.dumps({"address": v["address"]}).encode()
    req = urllib.request.Request(url3, data=body, headers={
        "Content-Type": "application/json", "User-Agent": UA, "X-API-Key": API_KEY,
    }, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            d = json.load(r)
        info = d.get("data", {})
        ad = info.get("account_display", {})
        display = ad.get("display", "") if isinstance(ad, dict) else ""
        people = ad.get("people", {}) if isinstance(ad, dict) else {}
        nansen_label = info.get("address_type", "")
        registrar = info.get("registrar_info", "")
        balance = info.get("balance", "?")
        derive = info.get("derive_token", "?")
        substrate = info.get("substrate_account", {})
        reg_judgements = (ad.get("people", {}) if isinstance(ad, dict) else {}).get("judgements", [])
        print(f"  {v['address'][:16]}... display='{display}' addr_type={nansen_label} reg_judgements={reg_judgements}")
        time.sleep(0.4)
    except Exception as e:
        print(f"  {v['address'][:16]}: err {e}")
