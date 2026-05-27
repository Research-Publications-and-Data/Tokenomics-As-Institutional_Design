#!/usr/bin/env python3
"""Identify top funders via Subscan account-detail."""
import json, urllib.request, time

API_KEY = "c8625edf41b845a393ff24fe5d3bb132"
UA = "Mozilla/5.0"

clusters = json.load(open("/tmp/b2_phase4/dot_funding_clusters.json"))
top_funders = clusters["top_funders"][:15]

for f in top_funders:
    addr = f["funder"]
    # Look up account info
    url = "https://polkadot.api.subscan.io/api/v2/scan/search"
    body = json.dumps({"key": addr, "row": 1, "page": 0}).encode()
    req = urllib.request.Request(url, data=body, headers={
        "Content-Type": "application/json", "User-Agent": UA, "X-API-Key": API_KEY,
    }, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            d = json.load(r)
        if d.get("code") == 0:
            data = d.get("data", {})
            # Try multiple shapes
            display = ""
            ai = data.get("account") or {}
            if isinstance(ai, dict):
                ad = ai.get("account_display") or {}
                if isinstance(ad, dict):
                    p = ad.get("people") or {}
                    display = p.get("display") or ad.get("display", "")
                    if not display:
                        display = ad.get("display", "")
            
            # Also try data.account_display
            if not display:
                ad2 = data.get("account_display") or {}
                if isinstance(ad2, dict):
                    p = ad2.get("people") or {}
                    display = p.get("display") or ad2.get("display", "")
            
            print(f"  {addr[:30]}... funds {f['validator_count']:>3} validators ({f['total_stake_funded_dot']:>11,.0f} DOT) display='{display}'")
        time.sleep(0.3)
    except Exception as e:
        print(f"  {addr[:30]}: err {e}")
