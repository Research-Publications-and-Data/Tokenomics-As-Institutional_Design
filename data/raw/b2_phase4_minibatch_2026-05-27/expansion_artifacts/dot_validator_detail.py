#!/usr/bin/env python3
"""Use correct field names for Subscan endpoints."""
import json, urllib.request
import os

API_KEY = os.environ["SUBSCAN_API_KEY"]
UA = "Mozilla/5.0"

test = "114SUbKCXjmb9czpWTtS3JANSmNRwVa4mmsMrWYpRG1kDH5"  # BINANCE_STAKE_9

# /api/scan/staking/validator with 'stash' parameter
print("=== /api/scan/staking/validator (stash=BINANCE_STAKE_9) ===")
body = json.dumps({"stash": test}).encode()
req = urllib.request.Request("https://polkadot.api.subscan.io/api/scan/staking/validator", data=body, headers={
    "Content-Type": "application/json", "User-Agent": UA, "X-API-Key": API_KEY,
}, method="POST")
with urllib.request.urlopen(req, timeout=15) as r:
    d = json.load(r)
print(json.dumps(d, default=str, indent=2)[:2500])

print("\n\n=== /api/scan/staking/nominators (address=BINANCE_STAKE_9) ===")
body2 = json.dumps({"address": test, "row": 200, "page": 0}).encode()
req2 = urllib.request.Request("https://polkadot.api.subscan.io/api/scan/staking/nominators", data=body2, headers={
    "Content-Type": "application/json", "User-Agent": UA, "X-API-Key": API_KEY,
}, method="POST")
with urllib.request.urlopen(req2, timeout=15) as r:
    d2 = json.load(r)
print(json.dumps(d2, default=str, indent=2)[:2500])
