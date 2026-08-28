#!/usr/bin/env python3
"""Check referendum vote concentration (governance axis)."""
import json, urllib.request, time
from collections import defaultdict
import os

API_KEY = os.environ["SUBSCAN_API_KEY"]
UA = "Mozilla/5.0"

# Get recent executed referendums
url = "https://polkadot.api.subscan.io/api/scan/referenda/votes"

# Sample a recent executed referendum: 1777
for ref_idx in [1777, 1776, 1775]:
    print(f"\n=== Referendum #{ref_idx} votes (top by conviction-weighted DOT) ===")
    body = json.dumps({"referendum_index": ref_idx, "row": 50, "page": 0, "order": "desc", "order_field": "amount"}).encode()
    req = urllib.request.Request(url, data=body, headers={
        "Content-Type": "application/json", "User-Agent": UA, "X-API-Key": API_KEY,
    }, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            d = json.load(r)
        if d.get("code") != 0:
            print(f"  err code={d.get('code')} msg={d.get('message')}")
            continue
        votes = d.get("data", {}).get("list", [])
        count = d.get("data", {}).get("count", 0)
        print(f"  Total votes on ref #{ref_idx}: {count}; sample top 50 returned")
        # Compute vote concentration
        if votes:
            amounts = []
            for v in votes[:50]:
                amt = float(v.get("amount", 0) or 0) / 1e10  # planck → DOT
                addr = v.get("account", {}).get("address", "")
                display = v.get("account", {}).get("display", "")
                conv = v.get("conviction", "0")
                vote = v.get("vote", "")
                amounts.append((amt, addr, display, conv, vote))
            print(f"  Top-10 voters by amount:")
            for amt, addr, display, conv, vote in amounts[:10]:
                print(f"    {amt:>11,.0f} DOT  conv={conv} vote={vote}  '{display}' {addr[:20]}...")
        time.sleep(0.7)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")[:200] if hasattr(e, "read") else ""
        print(f"  HTTP {e.code}: {body[:120]}")
    except Exception as e:
        print(f"  ERR: {e}")
