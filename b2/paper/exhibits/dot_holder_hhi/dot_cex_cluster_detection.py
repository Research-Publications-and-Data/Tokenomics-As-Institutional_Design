#!/usr/bin/env python3
"""Top-20 non-PCA whale investigation for additional CEX cluster detection.

Systematically queries each top-20 remaining non-PCA address for:
1. Activity profile (cold/hot/staking signature)
2. Outbound DOT transfers (recipient patterns; cluster identification)
3. Inbound DOT transfers (funding-source attribution)
4. Round-number transfer signatures (institutional behavior)
5. Cross-reference against confirmed Binance cluster
"""
import json
import os
import time
import urllib.request
import csv

API_KEY = os.environ.get("SUBSCAN_API_KEY", "")
BASE = "https://assethub-polkadot.api.subscan.io/api"

# Confirmed Binance cluster (for cross-reference)
BINANCE_CLUSTER = {
    "16ZL8yLyXv3V3L3z9ofR1ovFLziyXaN1DPq4yffMAZ9czzBD",
    "13vg3Mrxm3GL9eXxLsGgLYRueiwFCiMbkdHBL4ZN5aob5D4N",
    "12YfMjjeRPVHpytGSgdHH5iWnybxxuBdLuhjSuuYmrPjFT2H",
}

# Top-20 non-PCA whales (rank, address)
TOP_20_NON_PCA = [
    (2,  "13Z7KjGnzdAdMre9cqRwTZHR6F2p36gqBsaNmQwwosiPz8JT"),
    (5,  "12ouvKSvKnXAdXFR5oCL1vXimWrkDWG3joMNw3ETupTRs1ab"),
    (6,  "19KT274PAdSchBjDmnxh6vEMdy4QFU9Bo6jgMZhen3esYGG"),
    (7,  "112RLyVZhjjHMSdKsBA9jz6VLuZAxMh8CTLcXYiddWz5Xui"),
    (9,  "14iNNrvU5DCLZ67mBMjnXFHU1wW24XQBERnMa2ZvokTs5WYW"),
    (10, "165iwLPuPxtR4hkunhEBWvVMarh6gjbBeoBwPm3V13EZT4aC"),
    (11, "15DQVbbkBZoDZ8GFTw5qoSaFcGvtT22M7g9CaiihH15DiCzL"),
    (12, "1yEvPjUDp5V9YmBfjRiRotK7UPzq6EHmeRLfE8xxyJW8bzj"),
    (13, "15tkQXN8hj28sucMHYcGfMvyxWJqHtcVEDvj5jrNJ1TWSJyX"),
    (14, "1GVe7pAK2Pc4TVGuPBYbEU82VmaiQhKjFTzECpX7GGXgzBB"),
    (15, "12GQAfJAvMAMjxdweFfWP6UPE2dQ1UiodCh2RFgtpVQ59VmJ"),
    (16, "13Th6PcjJ468fy2cQeVDDdHE6ycJ3sFQ5S9wHiQRDkCKR6Tz"),
    (18, "13e9cUkCHDWuimeE5hYZRmZfDg3sgscsnAJTpN8buzPxVkd4"),
    (20, "14UpRGUeAfsSZHFN63t4ojJrLNupPApUiLgovXtm7ZiAHUDA"),
    (21, "14AoK8VSrHFxZijXhZGSUipHzZbUgo2AkmEaviD9yxTb1ScX"),
    (22, "11Q7ismkHUbbUexpQc4DgTvedfsh8jKMDV7jZZoQwv57NLS"),
    (23, "13SkL2uACPqBzpKBh3d2n5msYNFB2QapA5vEDeKeLjG2LS3Y"),
    (25, "15FZotswrG9r6KQvBPb5Y3ybs6CA5FLbFbyzhk4ABfgDup22"),
    (26, "16GMHo9HZv8CcJy4WLoMaU9qusgzx2wxKDLbXStEBvt5274B"),
    (27, "14gAowz3LaAqYkRjqUZkjZUxKFUzLtN2oZJSfr3ziHBRhwgc"),
]


def api_call(endpoint, body):
    """POST to Subscan API."""
    req = urllib.request.Request(
        f"{BASE}{endpoint}",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "X-API-Key": API_KEY},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.load(r)
    except Exception as e:
        return {"error": str(e)}


def profile(addr):
    """Get profile."""
    d = api_call("/v2/scan/search", {"key": addr})
    return d.get("data", {}).get("account", {})


def transfers(addr, direction):
    """Get DOT transfers in/out (direction: 'sent' or 'received')."""
    d = api_call("/v2/scan/transfers", {
        "row": 100, "page": 0, "address": addr, "direction": direction
    })
    transfers = d.get("data", {}).get("transfers") or []
    return [t for t in transfers if t.get("asset_symbol") == "DOT"]


# All outbound recipients (build recipient -> [senders] graph)
all_recipients = {}  # recipient_addr -> [(sender_addr, amount, block)]
all_senders = {}  # sender_addr -> [(recipient_addr, amount, block)]

results = []
for rank, addr in TOP_20_NON_PCA:
    print(f"\n=== rank {rank}: {addr[:20]}... ===", flush=True)
    p = profile(addr)
    bal = float(p.get("balance", 0) or 0)
    locked = float(p.get("lock", 0) or 0)
    bonded = float(p.get("bonded", 0) or 0)
    extr = p.get("count_extrinsic", 0)
    display = p.get("display", "") or "(no identity)"
    locked_pct = locked / bal * 100 if bal else 0
    
    # Classify signature
    if extr < 20 and locked == 0 and bonded == 0:
        sig = "COLD-STORAGE"
    elif extr > 10000 and locked == 0:
        sig = "HOT-WALLET"
    elif bonded > 0 and abs(bonded - bal*1e10) / (bal*1e10 + 1) < 0.05:
        sig = "100%-STAKED"
    elif locked_pct > 50:
        sig = "MOSTLY-STAKED"
    else:
        sig = "MIXED"
    
    # Get outbound DOT
    sent = transfers(addr, "sent")
    received = transfers(addr, "received")
    
    print(f"  bal={bal:,.0f}  extr={extr}  locked={locked_pct:.0f}%  sig={sig}  display={display[:40]}")
    print(f"  outbound DOT transfers: {len(sent)}")
    
    # Round-number signature: round to nearest 1M
    round_outbound = [t for t in sent if float(t.get("amount", 0)) >= 100000 and float(t.get("amount", 0)) % 100000 < 1000]
    
    # Track recipients + senders
    for t in sent:
        amount = float(t.get("amount", 0))
        if amount >= 100000:  # only large transfers
            recip = t.get("to", "")
            if recip not in all_recipients:
                all_recipients[recip] = []
            all_recipients[recip].append((addr, amount, t.get("block_num"), rank))
            if addr not in all_senders:
                all_senders[addr] = []
            all_senders[addr].append((recip, amount, t.get("block_num")))
    
    # Show recent outbound DOT
    large_sent = sorted([t for t in sent if float(t.get("amount", 0)) >= 100000], key=lambda x: -float(x.get("amount", 0)))[:5]
    if large_sent:
        print(f"  Top large outbound:")
        for t in large_sent[:5]:
            recip = t.get("to", "")[:48]
            amount = float(t.get("amount", 0))
            in_binance = "*BINANCE*" if recip in BINANCE_CLUSTER else ""
            print(f"    -> {recip}... {amount:,.0f} DOT blk {t.get('block_num')} {in_binance}")
    
    # Show funding source (large inbound)
    large_received = sorted([t for t in received if float(t.get("amount", 0)) >= 100000], key=lambda x: -float(x.get("amount", 0)))[:5]
    if large_received:
        print(f"  Top large inbound:")
        for t in large_received[:5]:
            sender = t.get("from", "")[:48]
            amount = float(t.get("amount", 0))
            in_binance = "*BINANCE*" if sender in BINANCE_CLUSTER else ""
            print(f"    <- {sender}... {amount:,.0f} DOT blk {t.get('block_num')} {in_binance}")
    
    results.append({
        "rank": rank,
        "address": addr,
        "balance": bal,
        "extrinsics": extr,
        "locked_pct": locked_pct,
        "signature": sig,
        "n_large_outbound": len([t for t in sent if float(t.get("amount", 0)) >= 100000]),
        "n_large_inbound": len([t for t in received if float(t.get("amount", 0)) >= 100000]),
        "display": display,
    })
    time.sleep(0.3)

# === Identify clusters via shared recipients ===
print(f"\n\n=== CLUSTER DETECTION: recipients receiving from 2+ top-20 senders ===")
shared_recipients = {r: senders for r, senders in all_recipients.items() if len(set(s[0] for s in senders)) >= 2}
for recip, senders in sorted(shared_recipients.items(), key=lambda x: -sum(s[1] for s in x[1])):
    total = sum(s[1] for s in senders)
    print(f"  {recip[:48]}...  RECEIVES from {len(set(s[0] for s in senders))} top-20 senders: {total:,.0f} DOT total")
    for sender, amount, block, rank in senders[:5]:
        print(f"    <- rank-{rank} {sender[:30]}... {amount:,.0f} DOT blk {block}")

# === Summary report ===
print(f"\n\n=== SUMMARY ===")
sig_counts = {}
for r in results:
    sig_counts[r["signature"]] = sig_counts.get(r["signature"], 0) + 1
for sig, count in sorted(sig_counts.items(), key=lambda x: -x[1]):
    print(f"  {sig}: {count}")

# Write summary CSV
with open("/tmp/dot_top20_nonpca_profile.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["rank", "address", "balance", "extrinsics", "locked_pct", "signature", "n_large_outbound", "n_large_inbound", "display"])
    w.writeheader()
    for r in results:
        w.writerow(r)
print(f"\nWrote: /tmp/dot_top20_nonpca_profile.csv")
