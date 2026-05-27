#!/usr/bin/env python3
"""Funding-source clustering: for each validator stash, pull first incoming transfers.
Group validators by common source-address to identify operator-co-controlled validators."""
import json, urllib.request, time
from collections import defaultdict

API_KEY = "c8625edf41b845a393ff24fe5d3bb132"
UA = "Mozilla/5.0"
URL = "https://polkadot.api.subscan.io/api/v2/scan/transfers"

our = json.load(open("/tmp/b2_phase4/dot_validators_classified.json"))
validators = our["validators"]
total_stake = our["total_bonded_dot"]

# Focus on Unverified to maximize newly-resolved attribution
# (verified ones already classified)
unverified = [v for v in validators if v["operator_class"] == "Unverified"]
unverified.sort(key=lambda x: -x["bonded_total_dot"])

# Optionally exclude already-resolved via TVP
tvp = json.load(open("/tmp/b2_phase4/dot_tvp_crossref.json"))
tvp_resolved_addrs = set(v["address"] for v in tvp.get("matched_validators", []))
still_unverif = [v for v in unverified if v["address"] not in tvp_resolved_addrs]
print(f"Unverified validators after TVP cross-ref: {len(still_unverif)}")

# Pull first 10 incoming transfers for each (top-100 by stake to start; expandable)
print(f"\nPulling funding-source transfers for top-150 still-unverified by stake...")
addr_to_sources = {}

for i, v in enumerate(still_unverif[:150], 1):
    addr = v["address"]
    body = json.dumps({
        "address": addr,
        "row": 10,
        "page": 0,
        "direction": "received",  # incoming transfers
    }).encode()
    req = urllib.request.Request(URL, data=body, headers={
        "Content-Type": "application/json", "User-Agent": UA, "X-API-Key": API_KEY,
    }, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            resp = json.load(r)
        if resp.get("code") != 0:
            continue
        transfers = resp.get("data", {}).get("transfers", []) or []
        sources = []
        for t in transfers:
            src = t.get("from") or (t.get("from_account_display") or {}).get("address", "")
            amt = t.get("amount", "0")
            sources.append({"from": src, "amount_raw": amt, "block_timestamp": t.get("block_timestamp")})
        addr_to_sources[addr] = sources
        if i % 20 == 0:
            print(f"  {i}/150 processed")
        time.sleep(0.3)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")[:80] if hasattr(e, "read") else ""
        if i <= 5:
            print(f"  #{i} HTTP {e.code}: {body}")
    except Exception as e:
        if i <= 5:
            print(f"  #{i} ERR: {e}")

# Build source → recipients map
source_to_validators = defaultdict(list)
for addr, sources in addr_to_sources.items():
    seen_sources = set()
    for s in sources:
        src = s.get("from", "")
        if src and src not in seen_sources:
            source_to_validators[src].append(addr)
            seen_sources.add(src)

# Find sources funding multiple validators
multi_funder = {src: vs for src, vs in source_to_validators.items() if len(vs) >= 2}
print(f"\n=== Funding sources that fund >= 2 of the 150 unverified validators ===")
sorted_funders = sorted(multi_funder.items(), key=lambda x: -len(x[1]))
print(f"Total multi-validator funders: {len(multi_funder)}")
print(f"Top-30 funders by validator-count:")
val_lookup = {v["address"]: v for v in validators}
for src, vs in sorted_funders[:30]:
    total_stake_funded = sum(val_lookup[a]["bonded_total_dot"] for a in vs)
    print(f"  funder={src[:24]}... funds {len(vs):>2} validators ({total_stake_funded:>11,.0f} DOT total)")

# Cross-reference top funders against well-known accounts
# Web3 Foundation accounts, Treasury, well-known operators
known_funders = {
    # Polkadot Treasury parachain account
    "13UVJyLnbVp9RBZYFwHYxaAHz2wUWeAdAFbgn94o6M77nAZw": "Polkadot Treasury Parachain",
}
print(f"\nCheck top funders against known-accounts:")
for src, vs in sorted_funders[:30]:
    if src in known_funders:
        print(f"  {src[:24]}... = {known_funders[src]} funds {len(vs)} validators")

# Save
with open("/tmp/b2_phase4/dot_funding_clusters.json", "w") as f:
    json.dump({
        "n_processed": len(addr_to_sources),
        "multi_funder_count": len(multi_funder),
        "top_funders": [
            {
                "funder": src,
                "validator_count": len(vs),
                "validator_addresses": vs,
                "total_stake_funded_dot": sum(val_lookup[a]["bonded_total_dot"] for a in vs),
            }
            for src, vs in sorted_funders[:50]
        ],
    }, f, default=str, indent=2)
