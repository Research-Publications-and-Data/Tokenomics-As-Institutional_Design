#!/usr/bin/env python3
"""Probe alternative Subscan endpoints for meaningful DOT top-holder distribution."""
import json, urllib.request, time

API_KEY = "c8625edf41b845a393ff24fe5d3bb132"
UA = "Mozilla/5.0"

BASE = "https://polkadot.api.subscan.io"

# Try several endpoints
candidates = [
    # Staking-related
    ("POST", "/api/scan/staking/validators", {"row": 100, "page": 0}),
    ("POST", "/api/v2/scan/staking/nominators", {"row": 100, "page": 0, "order": "desc", "order_field": "bonded"}),
    ("POST", "/api/scan/nomination_pools", {"row": 100, "page": 0}),
    # Total bonded
    ("POST", "/api/scan/staking/era_stat", {"row": 10, "page": 0}),
    # Top holders (different terminology)
    ("POST", "/api/v2/scan/accounts", {"row": 100, "page": 0, "order": "desc", "order_field": "balance_total"}),
    ("POST", "/api/v2/scan/accounts", {"row": 100, "page": 0, "order": "desc", "order_field": "free"}),
    # Treasury
    ("POST", "/api/scan/treasury/proposals", {"row": 10}),
]

for method, path, payload in candidates:
    url = BASE + path
    body = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=body, headers={
        "Content-Type": "application/json",
        "User-Agent": UA,
        "X-API-Key": API_KEY,
    }, method=method)
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            d = json.load(r)
        code = d.get("code", "?")
        msg = d.get("message", "")
        data = d.get("data", {})
        if isinstance(data, dict):
            keys = list(data.keys())
            list_key = next((k for k in keys if isinstance(data[k], list)), None)
            count = len(data[list_key]) if list_key else 0
            sample = data[list_key][0] if (list_key and data[list_key]) else None
        else:
            count = 0; sample = None
        print(f"  {path}  code={code} msg='{msg[:40]}' count={count}")
        if sample:
            print(f"    sample[0]: {json.dumps(sample, default=str)[:400]}")
        time.sleep(0.5)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")[:120] if hasattr(e, "read") else ""
        print(f"  {path}: HTTP {e.code} {body[:100]}")
    except Exception as e:
        print(f"  {path}: ERR {e}")
