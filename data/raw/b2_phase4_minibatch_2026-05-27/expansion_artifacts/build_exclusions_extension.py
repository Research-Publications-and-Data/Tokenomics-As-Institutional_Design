#!/usr/bin/env python3
"""Build exclusions_log.csv extension rows for:
  (a) 28 CONFIRMED + 2 TENTATIVE Phase 4 PCAs (FXS + SNX + GNO)
  (b) 89 universal-sweep CEX hot wallet hits across existing N=40 sample
"""
import csv
from pathlib import Path

SCHEMA = ["token", "address", "identity", "exclusion_reason", "chain", "hhi_before", "hhi_after", "source"]
OUT_CSV = Path("/Users/zach/Tokenomics-As-Institutional_Design/b2/paper/supplements/phase4_exclusions_log_extension_2026-05-27.csv")

new_rows = []

# Phase 4 PCAs per S18 v2 audited classifications
PHASE4 = [
    # FXS
    ("FXS", "0x36cb65c1967a0fb0eee11569c51c2f2aa1ca6f6d", "Fraxtal: Optimism Portal Proxy", "Frax L2 bridge custody (Optimism Portal pattern for Fraxtal); 52.48% of top-1000 share; verified Etherscan public name tag 2026-05-27 via WebFetch (Class 4)", "ethereum", 0.261654, 0.032411, "Etherscan public name tag + S18 v2 audit"),
    ("FXS", "0xc8418af6358ffdda74e09ca9cc3fe03ca6adc5b0", "veFXS (vote-escrow staking aggregation)", "Frax vote-escrowed FXS contract; Vyper contract verified Etherscan source; sister-pattern to veCRV (Class 3)", "ethereum", 0.261654, 0.032411, "Etherscan contract source"),
    ("FXS", "0x4a6d155df9ec9a1bb3639e6b7b99e46fb68d42f6", "Fraxferry (Frax cross-chain bridge)", "Frax cross-chain bridge custody (Class 4); Etherscan source verified", "ethereum", 0.261654, 0.032411, "Etherscan contract source"),
    ("FXS", "0x000000000004444c5dc75cb358380d2e3de08a90", "Uniswap V4: Pool Manager", "DEX trading-protocol liquidity custody (Class 5); Etherscan public name tag verified", "ethereum", 0.261654, 0.032411, "Etherscan public name tag"),
    ("FXS", "0x03b59bd1c8b9f6c265ba0c3421923b93f15036fa", "FraxswapPair", "Frax-native DEX liquidity pool (Class 5); Etherscan contract source verified", "ethereum", 0.261654, 0.032411, "Etherscan contract source"),
    ("FXS", "0xb1748c79709f4ba2dd82834b8c82d4a505003f27", "Frax Finance: Comptroller", "Foundation operational multisig (Class 2); Etherscan public name tag verified", "ethereum", 0.261654, 0.032411, "Etherscan public name tag"),
    ("FXS", "0xedc6bacdc1e29d7c5fa6f6eca6fdd447b9c487c9", "Bitvavo CEX hot wallet", "Cross-protocol CEX custody; verified Nansen Address Labels API; also in SNX + GNO (Class 5)", "ethereum", 0.261654, 0.032411, "Nansen Address Labels API"),
    # SNX
    ("SNX", "0xffffffaeff0b96ea8e4f94b2253f31abdd875847", "Synthetix: Synthetix Core", "V3 protocol-controlled inflation / treasury contract (Class 4); 38.07% of top-1000; verified Etherscan public name tag", "ethereum", 0.164252, 0.017075, "Etherscan public name tag"),
    ("SNX", "0x5fd79d46eba7f351fe49bff9e87cdea6c821ef9f", "SynthetixBridgeEscrow", "L1<->L2 bridge custody (Class 4); Etherscan source verified", "ethereum", 0.164252, 0.017075, "Etherscan contract source"),
    ("SNX", "0xf977814e90da44bfa03b6295a0616a897441acec", "Binance 8", "CEX hot wallet (Class 5); existing exclusions_log precedent (LPT/OP/LDO/GMX)", "ethereum", 0.164252, 0.017075, "Etherscan + Nansen + existing precedent"),
    ("SNX", "0x3a5cc8689d1b0cef2c317bc5c0ad6ce88b27d597", "Luno Wallet", "CEX hot wallet (Class 5); Nansen verified Luno exchange tag", "ethereum", 0.164252, 0.017075, "Nansen Address Labels API"),
    ("SNX", "0xa9d1e08c7793af67e9d92fe308d5697fb81d3e43", "Coinbase 10", "CEX hot wallet (Class 5); existing exclusions_log precedent (AXL)", "ethereum", 0.164252, 0.017075, "Etherscan public name tag + precedent"),
    ("SNX", "0x28c6c06298d514db089934071355e5743bf21d60", "Binance 14", "CEX hot wallet (Class 5); existing exclusions_log precedent (LDO)", "ethereum", 0.164252, 0.017075, "Etherscan public name tag + precedent"),
    ("SNX", "0xa023f08c70a23abc7edfc5b6b5e171d78dfc947e", "Crypto.com 22 / Hot Wallet", "Cross-protocol CEX hot wallet (Class 5); Etherscan + Nansen verified; also in GNO + 12 others (universal sweep)", "ethereum", 0.164252, 0.017075, "Etherscan public name tag + Nansen"),
    ("SNX", "0x0529ea5885702715e83923c59746ae8734c553b7", "Bitpanda 18", "Cross-protocol CEX hot wallet (Class 5); Etherscan public name tag verified; also in FXS + 18 others", "ethereum", 0.164252, 0.017075, "Etherscan public name tag"),
    ("SNX", "0xedc6bacdc1e29d7c5fa6f6eca6fdd447b9c487c9", "Bitvavo", "Cross-protocol CEX (Class 5); also in FXS + GNO; Nansen verified", "ethereum", 0.164252, 0.017075, "Nansen Address Labels API"),
    ("SNX", "0xab782bc7d4a2b306825de5a7730034f8f63ee1bc", "Bitvavo Hot Wallet", "Cross-protocol CEX (Class 5); also in GNO; Nansen verified", "ethereum", 0.164252, 0.017075, "Nansen Address Labels API"),
    # GNO
    ("GNO", "0x0000000000000000000000000000000000000000", "Null address (canonical burn)", "Canonical Ethereum burn destination (Class 1); 31.48% of top-1000", "ethereum", 0.272764, 0.042485, "Universal burn-address convention"),
    ("GNO", "0x88ad09518695c6c3712ac10a214be5109a655671", "Gnosis Chain: ETH-xDAI Omni Bridge", "Gnosis Chain bridge custody (Class 4); 13.99% of top-1000; Etherscan public name tag verified", "ethereum", 0.272764, 0.042485, "Etherscan public name tag"),
    ("GNO", "0xec83f750adfe0e52a8b0dba6eeb6be5ba0bee535", "Gnosis: Vesting", "Foundation treasury vesting (Class 2); 38.52% of top-1000; Etherscan public name tag verified", "ethereum", 0.272764, 0.042485, "Etherscan public name tag"),
    ("GNO", "0x604e4557e9020841f4e8eb98148de3d3cdea350c", "Gnosis Disbursement-2", "Foundation treasury vesting (Class 2); 3.60% of top-1000; same creator (0x12e9a5f7...) as Gnosis: Vesting", "ethereum", 0.272764, 0.042485, "Etherscan contract source + creator pattern"),
    ("GNO", "0x849d52316331967b6ff1198e5e32a0eb168d039d", "Gnosis: Active Treasury Management", "Foundation treasury operational multisig (Class 2); 4.15% of top-1000; Etherscan public name tag verified", "ethereum", 0.272764, 0.042485, "Etherscan public name tag"),
    ("GNO", "0xae5fb390e5c4fa1962e39e98dbfb0ed8055ed7a9", "koeppelmann.eth Safe (Martin Koppelmann; Gnosis co-founder)", "Co-founder personal custody (Class 2 tentative-foundation; sub-class pending DEC on cofounder-personal-Safe policy); Nansen koeppelmann.eth social tag verified", "ethereum", 0.272764, 0.042485, "Nansen Address Labels API"),
    ("GNO", "0x4f8ad938eba0cd19155a835f617317a6e788c868", "Gnosis: LGNO Token (Locked GNO staking aggregation)", "Staking aggregation contract (Class 3); sister-pattern to veFXS; Etherscan public name tag verified", "ethereum", 0.272764, 0.042485, "Etherscan public name tag"),
    ("GNO", "0xf977814e90da44bfa03b6295a0616a897441acec", "Binance 8", "CEX hot wallet (Class 5); existing precedent + Nansen", "ethereum", 0.272764, 0.042485, "existing precedent"),
    ("GNO", "0xa023f08c70a23abc7edfc5b6b5e171d78dfc947e", "Crypto.com 22 / Hot Wallet", "CEX cross-protocol (Class 5); also in SNX + 12 others", "ethereum", 0.272764, 0.042485, "Etherscan + Nansen"),
    ("GNO", "0xedc6bacdc1e29d7c5fa6f6eca6fdd447b9c487c9", "Bitvavo", "CEX cross-protocol (Class 5); also in FXS + SNX", "ethereum", 0.272764, 0.042485, "Nansen Address Labels API"),
    ("GNO", "0xab782bc7d4a2b306825de5a7730034f8f63ee1bc", "Bitvavo Hot Wallet", "CEX cross-protocol (Class 5); also in SNX", "ethereum", 0.272764, 0.042485, "Nansen Address Labels API"),
    # TENTATIVE
    ("GNO", "0x9d94ef33e7f8087117f85b3ff7b1d8f27e4053d5", "Stefan George Safe (Gnosis co-founder personal custody; TENTATIVE)", "Co-founder personal custody; deployed by stefangeorge.eth; classification depends on DEC for cofounder-personal-Safe policy (Class 2 tentative)", "ethereum", 0.272764, 0.076863, "Etherscan creator (stefangeorge.eth) + S18 v2 audit (TENTATIVE)"),
    ("GNO", "0xd2c8dfa974a8f6a5d25a45aa3ebf35b58c059185", "GnosisSafeProxy (TENTATIVE; rank-17 0.12 percent)", "Unverified Foundation multisig; no public name tag (Class 2 tentative)", "ethereum", 0.272764, 0.076863, "Etherscan contract source (TENTATIVE)"),
]

# Universal sweep extensions (new CEX hot wallets across existing protocols)
import csv as csvmod
with open("/Users/zach/Tokenomics-As-Institutional_Design/b2/paper/supplements/universal_cex_sweep_phase4_new_2026-05-27.csv") as f:
    sweep = list(csvmod.DictReader(f))

UNIVERSAL = []
for h in sweep:
    if h["is_new_cex_from_phase4"] != "True" or h["already_in_exclusions_log"] == "True":
        continue
    sym = h["symbol"]
    addr = h["address"]
    cex = h["cex_name"]
    share = float(h["share_top1000_pct"])
    hhi_before = float(h.get("hhi_with_existing_excl") or h["hhi_protocol_raw_pre"])
    hhi_after = float(h.get("hhi_post_new_cex_excl") or 0)
    UNIVERSAL.append((sym, addr, cex, f"CEX cross-protocol hot wallet (Class 5); Phase 4 universal-sweep ship 2026-05-27; {share:.4f} percent of {sym} top-1000", "ethereum", hhi_before, hhi_after, f"Phase 4 universal sweep ({cex})"))

# Write
ALL = PHASE4 + UNIVERSAL
with open(OUT_CSV, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=SCHEMA)
    w.writeheader()
    for row in ALL:
        w.writerow(dict(zip(SCHEMA, row)))

print(f"Wrote {OUT_CSV}")
print(f"  Phase 4 PCA rows:        {len(PHASE4)}")
print(f"  Universal-sweep rows:    {len(UNIVERSAL)}")
print(f"  Total new rows:          {len(ALL)}")

# Summary by protocol of universal-sweep impact
from collections import defaultdict
by_sym = defaultdict(list)
for row in UNIVERSAL:
    by_sym[row[0]].append(row)
print(f"\nUniversal-sweep hits by protocol ({len(by_sym)} affected):")
for sym, rows in sorted(by_sym.items()):
    if rows:
        # Use the worst (largest shift) row
        max_shift = max(float(r[6]) - float(r[5]) for r in rows)
        print(f"  {sym:<10}: {len(rows)} new exclusions; max HHI shift {max_shift:+.6f}")
