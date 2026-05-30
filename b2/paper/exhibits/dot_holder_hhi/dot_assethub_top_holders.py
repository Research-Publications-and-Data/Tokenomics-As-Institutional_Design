#!/usr/bin/env python3
"""Pull DOT top-1000 holders from AssetHub Polkadot Subscan API.

Post-Polkadot-1.0 migration, DOT balances live primarily on AssetHub (system
parachain), not the relay chain. The relay-chain Subscan endpoint
(polkadot.api.subscan.io) returns post-migration relay-chain residual balances
only; the AssetHub endpoint (assethub-polkadot.api.subscan.io) returns the
canonical current DOT holder distribution.

Methodology: pull top-1000 by total balance, compute holder-HHI on top-1000
post-PCA-exclusion (sister to the 44-protocol cross-section methodology).
"""
import csv
import json
import os
import time
import urllib.request

API_KEY = os.environ.get("SUBSCAN_API_KEY", "")
URL = "https://assethub-polkadot.api.subscan.io/api/v2/scan/accounts"
PAGES = 10  # 10 * 100 = 1000 holders

all_holders = []
for page in range(PAGES):
    body = json.dumps({
        "row": 100,
        "page": page,
        "order": "desc",
        "order_field": "balance",  # AssetHub balance = total DOT balance per address
    }).encode()
    req = urllib.request.Request(URL, data=body, headers={
        "Content-Type": "application/json",
        "X-API-Key": API_KEY,
    }, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            d = json.load(r)
        if d.get("code") != 0:
            print(f"page {page}: code={d.get('code')}: {d.get('message', '')}")
            break
        accounts = d.get("data", {}).get("list", [])
        if not accounts:
            print(f"page {page}: empty list; stopping")
            break
        all_holders.extend(accounts)
        print(f"  page {page}: +{len(accounts)} accounts; cumulative: {len(all_holders)}")
        time.sleep(0.5)
    except Exception as e:
        print(f"page {page}: ERR {type(e).__name__}: {e}")
        break

print(f"\nTotal AssetHub DOT holders pulled: {len(all_holders)}")

# Save to CSV
out_path = "/tmp/dot_assethub_holders.csv"
with open(out_path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["rank", "address", "balance", "reserved", "lock", "display"])
    for i, h in enumerate(all_holders, 1):
        addr = h.get("address", "")
        bal = float(h.get("balance", 0) or 0)
        res = float(h.get("reserved", 0) or 0)
        lock = float(h.get("balance_lock", 0) or 0)
        display = h.get("account_display", {}).get("display", "")
        writer.writerow([i, addr, bal, res, lock, display])
print(f"Wrote: {out_path}")

# Compute HHI
print(f"\nTop-15 by Subscan AssetHub balance:")
print(f"{'rank':4} {'address':<50} {'balance':>16} {'reserved':>12} {'lock':>12} display")
for i, h in enumerate(all_holders[:15], 1):
    addr = h.get("address", "")
    bal = float(h.get("balance", 0) or 0)
    res = float(h.get("reserved", 0) or 0)
    lock = float(h.get("balance_lock", 0) or 0)
    display = h.get("account_display", {}).get("display", "")
    print(f"{i:4} {addr:<50} {bal:>15,.0f} {res:>11,.0f} {lock:>11,.0f} {display}")

# Raw HHI on top-1000
top1000 = all_holders[:1000]
balances = [float(h.get("balance", 0) or 0) for h in top1000]
total = sum(balances)
hhi = sum((b / total) ** 2 for b in balances)
print(f"\nRaw holder-HHI (top-{len(balances)}; no PCA exclusion): {hhi:.4f}")
print(f"Top-1000 total: {total:,.0f} DOT")
print(f"Top-1 share: {balances[0]/total*100:.2f}%")
print(f"Top-10 share: {sum(balances[:10])/total*100:.2f}%")
print(f"Top-100 share: {sum(balances[:100])/total*100:.2f}%")
