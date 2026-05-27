#!/usr/bin/env python3
"""Audit confident-only exclusion HHI: trace math + classification basis."""
import json
from pathlib import Path

PROTOCOLS = {
    "FXS": "/tmp/b2_phase4/fxs_holders.json",
    "SNX": "/tmp/b2_phase4/snx_holders.json",
    "GNO": "/tmp/b2_phase4/gno_holders.json",
}

# CONFIRMED exclusions per S18 classification
CONFIRMED = {
    "FXS": [
        ("0xc8418af6358ffdda74e09ca9cc3fe03ca6adc5b0", "veFXS Vyper"),
        ("0x4a6d155df9ec9a1bb3639e6b7b99e46fb68d42f6", "Fraxferry"),
        ("0x000000000004444c5dc75cb358380d2e3de08a90", "Uniswap v4 PoolManager"),
        ("0x03b59bd1c8b9f6c265ba0c3421923b93f15036fa", "FraxswapPair"),
    ],
    "SNX": [
        ("0x5fd79d46eba7f351fe49bff9e87cdea6c821ef9f", "SynthetixBridgeEscrow"),
        ("0xf977814e90da44bfa03b6295a0616a897441acec", "Binance 8"),
        ("0xa9d1e08c7793af67e9d92fe308d5697fb81d3e43", "Coinbase 10"),
        ("0x28c6c06298d514db089934071355e5743bf21d60", "Binance 14"),
    ],
    "GNO": [
        ("0x0000000000000000000000000000000000000000", "null burn"),
        ("0x88ad09518695c6c3712ac10a214be5109a655671", "Omnibridge EternalStorageProxy"),
        ("0xec83f750adfe0e52a8b0dba6eeb6be5ba0bee535", "GnosisDAO Disbursement"),
        ("0x604e4557e9020841f4e8eb98148de3d3cdea350c", "GnosisDAO Disbursement-2"),
        ("0x9d94ef33e7f8087117f85b3ff7b1d8f27e4053d5", "Mintr / migration proxy"),
        ("0xf977814e90da44bfa03b6295a0616a897441acec", "Binance 8"),
    ],
}

# TENTATIVE exclusions
TENTATIVE = {
    "FXS": [
        ("0x36cb65c1967a0fb0eee11569c51c2f2aa1ca6f6d", "Frax v3 migration Proxy", 0.5248),
        ("0xb1748c79709f4ba2dd82834b8c82d4a505003f27", "Frax Comptroller multisig", 0.0069),
    ],
    "SNX": [
        ("0xffffffaeff0b96ea8e4f94b2253f31abdd875847", "Synthetix V3 Migrator proxy", 0.3845),
    ],
    "GNO": [
        ("0x849d52316331967b6ff1198e5e32a0eb168d039d", "GnosisDAO Safe-1", 0.0417),
        ("0xae5fb390e5c4fa1962e39e98dbfb0ed8055ed7a9", "PayingProxy", 0.0034),
        ("0xd2c8dfa974a8f6a5d25a45aa3ebf35b58c059185", "GnosisSafeProxy-3", 0.0012),
        ("0x4f8ad938eba0cd19155a835f617317a6e788c868", "TransparentUpgradeableProxy", 0.0052),
    ],
}


def hhi(rows, denom):
    return sum((r["balance_raw"] / denom) ** 2 for r in rows)


for sym, path in PROTOCOLS.items():
    d = json.load(open(path))
    rows = [{"address": r["wallet_address"].lower(), "balance_raw": int(r["balance"])} for r in d.get("holders", [])]
    rows.sort(key=lambda x: -x["balance_raw"])

    total = sum(r["balance_raw"] for r in rows)
    h_pre = hhi(rows, total)
    confirmed_addrs = {a for a, _ in CONFIRMED[sym]}
    tentative_addrs = {a for a, _, _ in TENTATIVE[sym]}

    # After confirmed exclusion
    kept_conf = [r for r in rows if r["address"] not in confirmed_addrs]
    total_conf = sum(r["balance_raw"] for r in kept_conf)
    h_conf = hhi(kept_conf, total_conf)

    # After full exclusion
    kept_full = [r for r in rows if r["address"] not in (confirmed_addrs | tentative_addrs)]
    total_full = sum(r["balance_raw"] for r in kept_full)
    h_full = hhi(kept_full, total_full)

    # Trace: what's the new top-1 share + contribution after confident exclusion?
    new_top1_conf = kept_conf[0]
    new_top1_share_conf = new_top1_conf["balance_raw"] / total_conf
    new_top1_contrib_conf = new_top1_share_conf ** 2

    new_top1_full = kept_full[0]
    new_top1_share_full = new_top1_full["balance_raw"] / total_full
    new_top1_contrib_full = new_top1_share_full ** 2

    confirmed_excluded_share_pre = sum(r["balance_raw"] for r in rows if r["address"] in confirmed_addrs) / total

    print(f"\n=== {sym} HHI AUDIT ===")
    print(f"  Top-1000 base                = {total:.0f}")
    print(f"  Pre-exclusion HHI            = {h_pre:.6f}")
    print(f"    -> top-1 share-of-1000    = {rows[0]['balance_raw']/total:.4f}")
    print(f"    -> top-1 HHI contribution = {(rows[0]['balance_raw']/total)**2:.6f}")
    print(f"  CONFIRMED-only base          = {total_conf:.0f} ({100*total_conf/total:.1f}% of original)")
    print(f"    CONFIRMED excluded share  = {confirmed_excluded_share_pre:.4f} of pre-base")
    print(f"    New top-1 = {new_top1_conf['address']} share={new_top1_share_conf:.4f} contrib={new_top1_contrib_conf:.6f}")
    print(f"  HHI confident-only           = {h_conf:.6f}  ({'INCREASED' if h_conf>h_pre else 'DECREASED'} {(h_conf-h_pre):+.6f})")
    print(f"  HHI full                     = {h_full:.6f}")
    print(f"    New top-1 = {new_top1_full['address']} share={new_top1_share_full:.4f}")
    print()
    print(f"  Direction-of-shift root cause check:")
    print(f"    is top-1 (rank-1 of original top-1000) IN confirmed-set?  {rows[0]['address'] in confirmed_addrs}")
    print(f"    is top-1 IN tentative-set?                                 {rows[0]['address'] in tentative_addrs}")
    if rows[0]['address'] in tentative_addrs:
        print(f"    ==> direction-of-shift INCREASED is because top-1 is TENTATIVE (kept in confident-only set)")
        print(f"        Re-normalization: top-1 share rises from {rows[0]['balance_raw']/total:.4f} to {new_top1_share_conf:.4f}")
        print(f"        ==> contribution rises from {(rows[0]['balance_raw']/total)**2:.6f} to {new_top1_contrib_conf:.6f}")
