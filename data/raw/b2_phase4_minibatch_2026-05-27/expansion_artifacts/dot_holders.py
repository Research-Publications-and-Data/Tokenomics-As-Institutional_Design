#!/usr/bin/env python3
"""Pull DOT top holders via Subscan API with API key."""
import json, urllib.request, time
import os

API_KEY = os.environ["SUBSCAN_API_KEY"]
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_6) AppleWebKit/605.1.15"
URL = "https://polkadot.api.subscan.io/api/v2/scan/accounts"

all_holders = []
for page in range(0, 10):  # 10 pages * 100 = 1000 holders
    body = json.dumps({
        "row": 100,
        "page": page,
        "order": "desc",
        "order_field": "balance",
    }).encode()
    req = urllib.request.Request(URL, data=body, headers={
        "Content-Type": "application/json",
        "User-Agent": UA,
        "Accept": "application/json",
        "X-API-Key": API_KEY,
    }, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            d = json.load(r)
        if d.get("code") != 0:
            print(f"page {page}: code={d.get('code')}: {d.get('message', '')}")
            break
        data = d.get("data", {})
        accounts = data.get("list", [])
        if not accounts:
            break
        all_holders.extend(accounts)
        print(f"  page {page}: {len(accounts)} accounts; total: {len(all_holders)}")
        time.sleep(0.7)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")[:200] if hasattr(e, "read") else ""
        print(f"page {page}: HTTP {e.code}  {body[:200]}")
        break
    except Exception as e:
        print(f"page {page}: ERR {type(e).__name__}: {e}")
        break

with open("/tmp/b2_phase4/dot_holders.json", "w") as f:
    json.dump({"holders": all_holders, "count": len(all_holders)}, f, default=str)
print(f"\nTotal DOT holders pulled: {len(all_holders)}")
if all_holders:
    print(f"Top-15 sample:")
    for i, h in enumerate(all_holders[:15], 1):
        addr = h.get("address", "?")
        bal_raw = h.get("balance", "0")
        try:
            bal = float(bal_raw) if not isinstance(bal_raw, (int, float)) else bal_raw
        except:
            bal = 0
        identity = (h.get("account_display") or {}).get("identity") or {}
        display = (h.get("account_display") or {}).get("display") or ""
        merkle = (h.get("merkle") or {}).get("tag_name", "")
        print(f"  #{i}: {addr[:24]}... bal={bal:>18,.0f} DOT  display='{display}' merkle='{merkle}'")
