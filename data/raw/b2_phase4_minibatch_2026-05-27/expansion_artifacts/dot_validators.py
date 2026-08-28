#!/usr/bin/env python3
"""Pull DOT validators (staking aggregation concentration; sister to veCRV in EVM)."""
import json, urllib.request, time
import os

API_KEY = os.environ["SUBSCAN_API_KEY"]
UA = "Mozilla/5.0"
URL = "https://polkadot.api.subscan.io/api/scan/staking/validators"

all_validators = []
for page in range(0, 10):  # Up to 1000 validators (Polkadot has ~297 active + waiting set)
    body = json.dumps({"row": 100, "page": page}).encode()
    req = urllib.request.Request(URL, data=body, headers={
        "Content-Type": "application/json", "User-Agent": UA, "X-API-Key": API_KEY,
    }, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            d = json.load(r)
        if d.get("code") != 0:
            print(f"page {page}: code={d.get('code')}: {d.get('message')}")
            break
        vals = d.get("data", {}).get("list", [])
        if not vals:
            break
        all_validators.extend(vals)
        print(f"  page {page}: {len(vals)} validators; total: {len(all_validators)}")
        time.sleep(0.5)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")[:120] if hasattr(e, "read") else ""
        print(f"page {page}: HTTP {e.code} {body}")
        break

# Parse balances (planks = 10^-10 DOT)
PLANCK_PER_DOT = 10**10
parsed = []
for v in all_validators:
    bn = int(v.get("bonded_nominators", "0") or "0")
    bo = int(v.get("bonded_owner", "0") or "0")
    total_bonded = bn + bo
    addr = v.get("stash_account_display", {}).get("address", "")
    display = v.get("stash_account_display", {}).get("people", {}).get("display", "") or v.get("stash_account_display", {}).get("display", "")
    n_nom = v.get("count_nominators", 0)
    parsed.append({
        "address": addr, "display": display, "bonded_total_plancks": total_bonded,
        "bonded_total_dot": total_bonded / PLANCK_PER_DOT,
        "bonded_owner_plancks": bo, "bonded_nominators_plancks": bn,
        "count_nominators": n_nom,
    })

# Sort by total bonded
parsed.sort(key=lambda x: -x["bonded_total_plancks"])
print(f"\nTotal validators: {len(parsed)}")
print(f"\nTop-15 by bonded stake:")
for i, v in enumerate(parsed[:15], 1):
    print(f"  #{i:>3}  {v['display'][:35]:<35} {v['bonded_total_dot']:>14,.0f} DOT  ({v['count_nominators']} nominators)")

# Compute HHI on validator concentration
total_bonded = sum(v["bonded_total_plancks"] for v in parsed)
print(f"\nTotal bonded across all validators: {total_bonded / PLANCK_PER_DOT:,.0f} DOT")

if total_bonded > 0:
    shares = [v["bonded_total_plancks"] / total_bonded for v in parsed]
    hhi = sum(s**2 for s in shares)
    top1_pct = 100 * shares[0]
    top5_pct = 100 * sum(shares[:5])
    top10_pct = 100 * sum(shares[:10])
    print(f"HHI (bonded-stake basis):  {hhi:.6f}")
    print(f"top1_pct: {top1_pct:.2f}%   top5_pct: {top5_pct:.2f}%   top10_pct: {top10_pct:.2f}%")

# Save
with open("/tmp/b2_phase4/dot_validators.json", "w") as f:
    json.dump({"validators": parsed, "total_bonded_plancks": total_bonded, "hhi": hhi if total_bonded else None, "n": len(parsed)}, f, default=str)
