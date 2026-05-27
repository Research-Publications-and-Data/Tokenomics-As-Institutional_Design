#!/usr/bin/env python3
"""Check for cross-protocol holder overlap across FXS/SNX/GNO (sister to S13 Finding C)."""
import json
from collections import defaultdict

PROTOCOLS = {
    "FXS": "/tmp/b2_phase4/fxs_holders.json",
    "SNX": "/tmp/b2_phase4/snx_holders.json",
    "GNO": "/tmp/b2_phase4/gno_holders.json",
}

# Load top-100 for each
addr_to_protocols = defaultdict(list)
for sym, path in PROTOCOLS.items():
    d = json.load(open(path))
    for i, r in enumerate(d.get("holders", [])[:100], 1):
        addr_to_protocols[r["wallet_address"].lower()].append((sym, i, r["first_acquired"][:10], int(r["balance"])))

# Find cross-protocol (2+ presence)
print("=== Cross-protocol holders (top-100 in 2+ of FXS/SNX/GNO) ===")
multi = {a: pres for a, pres in addr_to_protocols.items() if len(pres) >= 2}
for addr, presences in sorted(multi.items(), key=lambda x: -len(x[1])):
    presence_str = ", ".join(f"{s}#{r}({d})" for s, r, d, _ in presences)
    print(f"  {addr}  [{len(presences)}-protocol]  {presence_str}")
print(f"\nTotal cross-protocol addresses (top-100, 2+ protocols): {len(multi)}")
print(f"Total cross-protocol addresses (top-100, 3+ protocols): {sum(1 for a, p in multi.items() if len(p) >= 3)}")
