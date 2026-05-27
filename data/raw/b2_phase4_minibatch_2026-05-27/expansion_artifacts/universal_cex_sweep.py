#!/usr/bin/env python3
"""Universal CEX-sweep: scan existing N=40 protocol holder lists for 5 newly-confirmed CEX hot wallets."""
import csv, glob, json
from pathlib import Path
from collections import defaultdict

HOLDER_DIR = Path("/Users/zach/Tokenomics-As-Institutional_Design/data/raw/holder_lists")
OUT_DIR = Path("/Users/zach/Tokenomics-As-Institutional_Design/b2/paper/supplements")
EXCL_LOG = Path("/Users/zach/Tokenomics-As-Institutional_Design/data/processed/exclusions_log.csv")
REG_DATA = Path("/Users/zach/Tokenomics-As-Institutional_Design/data/processed/regression_data_april2026.csv")
DATE = "2026-05-27"

# 5 newly-confirmed CEX hot wallets from Phase 4 audit
NEW_CEX = {
    "0xa023f08c70a23abc7edfc5b6b5e171d78dfc947e": ("Crypto.com 22", "Crypto.com Hot Wallet"),
    "0x0529ea5885702715e83923c59746ae8734c553b7": ("Bitpanda 18", "Bitpanda Exchange"),
    "0xedc6bacdc1e29d7c5fa6f6eca6fdd447b9c487c9": ("Bitvavo", "Bitvavo CEX"),
    "0xab782bc7d4a2b306825de5a7730034f8f63ee1bc": ("Bitvavo Hot Wallet", "Bitvavo Hot Wallet"),
    "0x3a5cc8689d1b0cef2c317bc5c0ad6ce88b27d597": ("Luno Wallet", "Luno Exchange Hot Wallet"),
}

# Already-known Binance/Coinbase patterns to also sweep for cross-reference
KNOWN_CEX = {
    "0xf977814e90da44bfa03b6295a0616a897441acec": ("Binance 8", "known precedent"),
    "0x28c6c06298d514db089934071355e5743bf21d60": ("Binance 14", "known precedent"),
    "0xa9d1e08c7793af67e9d92fe308d5697fb81d3e43": ("Coinbase 10", "known precedent"),
    "0x5a52e96bacdabb82fd05763e25335261b270efcb": ("Binance 19", "known precedent"),
}
ALL_CEX = {**NEW_CEX, **KNOWN_CEX}

# Load existing exclusions to avoid double-adding
existing_exclusions = set()
with open(EXCL_LOG) as f:
    reader = csv.DictReader(f)
    for r in reader:
        existing_exclusions.add((r.get("token", "").upper(), r.get("address", "").lower()))

# Load existing exclusions per protocol -> already-excluded address set
proto_excl = defaultdict(set)
with open(EXCL_LOG) as f:
    for r in csv.DictReader(f):
        proto_excl[r.get("token", "").upper()].add(r.get("address", "").lower())

# Sweep each holder file
results = []
holder_files = sorted(glob.glob(str(HOLDER_DIR / "*_holders.csv")))

for hf in holder_files:
    sym = Path(hf).stem.replace("_holders", "")
    with open(hf) as f:
        # Auto-detect schema: address could be in col 0 (AAVE-style) or col 2 (HONEY-style)
        first_line = f.readline().strip().lower()
        f.seek(0)
        reader = csv.DictReader(f)
        # Address column name
        addr_col = None
        for c in reader.fieldnames or []:
            if c.lower() == "address":
                addr_col = c
                break
        if not addr_col:
            continue
        # Balance column
        bal_col = None
        for c in reader.fieldnames or []:
            if c.lower() in ("balance", "amount"):
                bal_col = c
                break
        # Share column (some files have pre-computed share)
        share_col = None
        for c in reader.fieldnames or []:
            if c.lower() in ("share", "share_pct", "pct"):
                share_col = c
                break

        holders = []
        for r in reader:
            addr = (r.get(addr_col) or "").lower()
            if not addr:
                continue
            try:
                bal = float(r.get(bal_col, 0) or 0)
            except (ValueError, TypeError):
                bal = 0.0
            holders.append({"address": addr, "balance": bal, "rank": len(holders) + 1})
    
    if not holders:
        continue

    total = sum(h["balance"] for h in holders)
    if total == 0:
        continue

    # Scan for CEX hot wallets in this protocol's top-1000
    hits = []
    for h in holders[:1000]:
        if h["address"] in ALL_CEX:
            cex_name, _ = ALL_CEX[h["address"]]
            is_new = h["address"] in NEW_CEX
            already_excluded = h["address"] in proto_excl.get(sym.upper(), set())
            share = h["balance"] / total
            hits.append({
                "symbol": sym,
                "address": h["address"],
                "cex_name": cex_name,
                "rank": h["rank"],
                "share_top1000_pct": 100.0 * share,
                "is_new_cex_from_phase4": is_new,
                "already_in_exclusions_log": already_excluded,
            })
    
    if hits:
        # Compute pre/post-exclusion HHI for this protocol (only the new-CEX additions if not already excluded)
        existing_exclusions_for_sym = proto_excl.get(sym.upper(), set())
        new_cex_to_add = [h for h in hits if h["address"] in NEW_CEX and not h["already_in_exclusions_log"]]
        
        # Pre = current state with existing exclusions already applied
        # We don't have the pre-exclusion HHI per protocol cached, so compute on this file's raw data
        hhi_pre = sum((h["balance"] / total) ** 2 for h in holders)
        hhi_pre_with_existing_excl = None
        if existing_exclusions_for_sym:
            kept = [h for h in holders if h["address"] not in existing_exclusions_for_sym]
            new_total = sum(h["balance"] for h in kept)
            if new_total > 0:
                hhi_pre_with_existing_excl = sum((h["balance"] / new_total) ** 2 for h in kept)
        
        # Post = add new CEX exclusions on top
        all_excl = existing_exclusions_for_sym | {h["address"] for h in new_cex_to_add}
        kept_post = [h for h in holders if h["address"] not in all_excl]
        new_total_post = sum(h["balance"] for h in kept_post)
        hhi_post = sum((h["balance"] / new_total_post) ** 2 for h in kept_post) if new_total_post > 0 else None
        
        for hit in hits:
            hit["hhi_protocol_raw_pre"] = f"{hhi_pre:.6f}"
            hit["hhi_with_existing_excl"] = f"{hhi_pre_with_existing_excl:.6f}" if hhi_pre_with_existing_excl else ""
            hit["hhi_post_new_cex_excl"] = f"{hhi_post:.6f}" if hhi_post else ""
            hit["hhi_shift_from_new_cex"] = f"{(hhi_post - (hhi_pre_with_existing_excl or hhi_pre)):+.6f}" if hhi_post else ""
            hit["existing_exclusion_count"] = len(existing_exclusions_for_sym)
            hit["new_cex_to_add_count"] = len(new_cex_to_add)
        
        results.extend(hits)
        
        if any(h["address"] in NEW_CEX and not h["already_in_exclusions_log"] for h in hits):
            print(f"  {sym:<10}: {len(hits)} CEX hits ({sum(1 for h in hits if h['address'] in NEW_CEX)} from new Phase 4 set; {sum(1 for h in hits if h['already_in_exclusions_log'])} already excluded)")

# Write results
out_csv = OUT_DIR / f"universal_cex_sweep_phase4_new_{DATE}.csv"
if results:
    with open(out_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(results[0].keys()))
        w.writeheader()
        w.writerows(results)
    print(f"\nWrote {out_csv}: {len(results)} total hits")
else:
    print("No hits found")

# Summary
print("\n=== Summary by CEX address ===")
by_cex = defaultdict(list)
for r in results:
    by_cex[(r["address"], r["cex_name"])].append(r)
for (addr, name), hits in sorted(by_cex.items(), key=lambda x: -len(x[1])):
    is_new = addr in NEW_CEX
    new_marker = " [NEW PHASE 4]" if is_new else ""
    syms = [h["symbol"] for h in hits if not h["already_in_exclusions_log"]]
    excl_syms = [h["symbol"] for h in hits if h["already_in_exclusions_log"]]
    print(f"  {name:<22} ({addr[:10]}...){new_marker}")
    print(f"    in N={len(hits)} protocols; {len(syms)} not-yet-excluded; {len(excl_syms)} already-excluded")
    if syms:
        print(f"    NEW hits: {sorted(syms)[:15]}")
