#!/usr/bin/env python3
"""Characterize cross-protocol unclassified top-holders via Sim API EVM balances.
Reuses S13 cycle's CEX-vs-institutional heuristic: 500+ token balances = CEX hot wallet."""
import json, subprocess, time

CANDIDATES = [
    "0xd2dd7b597fd2435b6db61ddf48544fd931e6869f",  # 3-protocol; 2025-09-21 same-day
    "0x7dafba1d69f6c01ae7567ffd7b046ca03b706f83",  # 3-protocol; 2025-09-20 same-day
    "0xedc6bacdc1e29d7c5fa6f6eca6fdd447b9c487c9",  # 3-protocol; older
    "0x0529ea5885702715e83923c59746ae8734c553b7",  # 2-protocol; FXS+SNX
    "0xab782bc7d4a2b306825de5a7730034f8f63ee1bc",  # 2-protocol; SNX+GNO same-day
    "0xa023f08c70a23abc7edfc5b6b5e171d78dfc947e",  # 2-protocol; SNX+GNO same-day
    "0x7bf3cc3130d0efee990b0905540f982571e9205c",  # 2-protocol; SNX+GNO same-day
]

for addr in CANDIDATES:
    print(f"\n=== {addr} ===")
    try:
        r = subprocess.run(
            ["dune", "sim", "evm", "balances", addr, "--chain-ids", "1", "-o", "json"],
            capture_output=True, text=True, timeout=30
        )
        d = json.loads(r.stdout)
        balances = d.get("balances", [])
        n_tokens = len(balances)
        # Get total USD if available
        total_usd = sum(b.get("value_usd") or 0 for b in balances)
        # Major-asset (top-3 by USD)
        sorted_bals = sorted([b for b in balances if b.get("value_usd")], key=lambda x: -(x.get("value_usd") or 0))
        major = sorted_bals[:5]
        print(f"  n_tokens: {n_tokens}; total_USD: ${total_usd:,.0f}")
        print(f"  top-5 by USD:")
        for b in major:
            sym = b.get("symbol") or "?"
            amt = b.get("amount") or "?"
            usd = b.get("value_usd") or 0
            print(f"    {sym:>8}  ${usd:>14,.0f}  {amt}")
        # Pattern classification heuristic
        if n_tokens >= 500:
            pattern = "CEX-pattern (500+ tokens; memecoin-dust + major-asset mix)"
        elif n_tokens <= 100 and all(b.get("value_usd", 0) for b in major if major):
            pattern = "INSTITUTIONAL-pattern (<100 tokens; major-assets-only)"
        else:
            pattern = "MIXED / unclear"
        print(f"  pattern: {pattern}")
        time.sleep(0.5)
    except Exception as e:
        print(f"  ERR: {e}")
