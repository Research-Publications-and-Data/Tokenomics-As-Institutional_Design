#!/usr/bin/env python3
"""Check Polkadot governance/council/OpenGov for top validators' presence."""
import json, urllib.request, time

API_KEY = "c8625edf41b845a393ff24fe5d3bb132"
UA = "Mozilla/5.0"
BASE = "https://polkadot.api.subscan.io"

# 1) Council members (current and historical)
print("=== Council members (treasury/governance council) ===")
url = BASE + "/api/scan/council/members"
req = urllib.request.Request(url, data=json.dumps({"row": 100, "page": 0}).encode(), headers={
    "Content-Type": "application/json", "User-Agent": UA, "X-API-Key": API_KEY,
}, method="POST")
try:
    with urllib.request.urlopen(req, timeout=15) as r:
        d = json.load(r)
    print(f"  Status code: {d.get('code')}; msg: {d.get('message', '')}")
    council = d.get("data", {})
    if isinstance(council, dict):
        members = council.get("list", []) or council.get("members", [])
    else:
        members = []
    print(f"  Found: {len(members)} council members")
    for m in members[:10]:
        print(f"    {json.dumps(m, default=str)[:200]}")
except urllib.error.HTTPError as e:
    body = e.read().decode("utf-8")[:200] if hasattr(e, "read") else ""
    print(f"  HTTP {e.code}: {body}")
except Exception as e:
    print(f"  ERR: {e}")

# 2) OpenGov referendum participation top voters (latest few referenda)
print("\n=== OpenGov referendum list ===")
url2 = BASE + "/api/scan/referenda/referendums"
req2 = urllib.request.Request(url2, data=json.dumps({"row": 5, "page": 0}).encode(), headers={
    "Content-Type": "application/json", "User-Agent": UA, "X-API-Key": API_KEY,
}, method="POST")
try:
    with urllib.request.urlopen(req2, timeout=15) as r:
        d = json.load(r)
    print(f"  Status: {d.get('code')}")
    refs = d.get("data", {}).get("list", [])[:5]
    for ref in refs:
        print(f"    referendum_index: {ref.get('referendum_index')} status: {ref.get('status')} created: {ref.get('created_block')}")
except urllib.error.HTTPError as e:
    body = e.read().decode("utf-8")[:200] if hasattr(e, "read") else ""
    print(f"  HTTP {e.code}: {body}")

# 3) Tech committee / Fellowship
print("\n=== Fellowship (technical committee) ===")
url3 = BASE + "/api/scan/fellowship/members"
req3 = urllib.request.Request(url3, data=json.dumps({"row": 50, "page": 0}).encode(), headers={
    "Content-Type": "application/json", "User-Agent": UA, "X-API-Key": API_KEY,
}, method="POST")
try:
    with urllib.request.urlopen(req3, timeout=15) as r:
        d = json.load(r)
    print(f"  Status: {d.get('code')}; msg: {d.get('message', '')}")
    members = d.get("data", {}).get("list", []) or d.get("data", {}).get("members", [])
    print(f"  Found {len(members)} fellowship members")
    for m in members[:5]:
        print(f"    {json.dumps(m, default=str)[:200]}")
except urllib.error.HTTPError as e:
    body = e.read().decode("utf-8")[:200] if hasattr(e, "read") else ""
    print(f"  HTTP {e.code}: {body}")

# 4) Top accounts by total stake (alt endpoint)
print("\n=== Top by total bonded (incl. nominators not via validators) ===")
# This requires querying staking-related accounts
url4 = BASE + "/api/v2/scan/staking/nominator"
req4 = urllib.request.Request(url4, data=json.dumps({"row": 20, "page": 0}).encode(), headers={
    "Content-Type": "application/json", "User-Agent": UA, "X-API-Key": API_KEY,
}, method="POST")
try:
    with urllib.request.urlopen(req4, timeout=15) as r:
        d = json.load(r)
    print(f"  Status: {d.get('code')}; msg: {d.get('message', '')}")
    noms = d.get("data", {}).get("list", [])
    print(f"  Found {len(noms)} nominators (top)")
    for n in noms[:5]:
        print(f"    {json.dumps(n, default=str)[:300]}")
except urllib.error.HTTPError as e:
    body = e.read().decode("utf-8")[:200] if hasattr(e, "read") else ""
    print(f"  HTTP {e.code}: {body}")
