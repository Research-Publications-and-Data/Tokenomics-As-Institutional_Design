#!/usr/bin/env python3
"""
B2 R3 Phase 4 mini-batch (EVM): FXS, SNX, GNO PCA-classification + HHI computation.

VERSION 2 (AUDITED): per "Audit confident-only exclusion HHI" directive 2026-05-27T17Z.
Reclassifications applied based on Etherscan public name tag verification (WebFetch) +
Nansen Address Labels API verification (POST /api/v1/profiler/address/labels).

Key changes vs v1:
  - FXS #1 (0x36cb65c...) promoted TENTATIVE -> CONFIRMED Class 4 (Etherscan public tag:
    "Fraxtal: Optimism Portal Proxy"; canonical Frax L2 bridge custody contract).
  - SNX #1 (0xffffff...) promoted TENTATIVE -> CONFIRMED Class 4 (Etherscan public tag:
    "Synthetix: Synthetix Core"; V3 protocol-controlled inflation/treasury contract).
  - FXS Comptroller promoted TENTATIVE -> CONFIRMED Class 2 (Etherscan: "Frax Finance: Comptroller").
  - GNO #4 promoted TENTATIVE -> CONFIRMED Class 2 (Etherscan: "Gnosis: Active Treasury Management").
  - GNO #8 LGNO promoted TENTATIVE -> CONFIRMED Class 3 (Etherscan: "Gnosis: LGNO Token"; locked-GNO
    staking aggregation, sister to veFXS pattern).
  - GNO #11 promoted TENTATIVE -> CONFIRMED Class 2 (Nansen: koeppelmann.eth, Gnosis co-founder Safe).
  - GNO #6 reclassified: was CONFIRMED Class 4 Mintr (INCORRECT); actual is Stefan George (Gnosis co-founder)
    Safe per Etherscan creator + Nansen "Proxy" tag. Now TENTATIVE Class 2 founder-personal custody.
  - NEW CONFIRMED Class 5 CEX additions per Nansen:
    * 0xedc6bacdc1e29d7c5fa6f6eca6fdd447b9c487c9 = Bitvavo (FXS + SNX + GNO 3-protocol)
    * 0xab782bc7d4a2b306825de5a7730034f8f63ee1bc = Bitvavo: Hot Wallet (SNX + GNO)
    * 0x3a5cc8689d1b0cef2c317bc5c0ad6ce88b27d597 = Luno: Wallet (SNX rank-4 3.87%)
    * 0xa023f08c70a23abc7edfc5b6b5e171d78dfc947e = Crypto.com 22 / Crypto.com: Hot Wallet (SNX + GNO)
    * 0x0529ea5885702715e83923c59746ae8734c553b7 = Bitpanda 18 (FXS + SNX) (Finding E in v1 INCORRECT;
      was attributed to Societe Generale based on EURCV holdings; actually Bitpanda CEX listing EURCV)
"""
import json, csv
from pathlib import Path
from dataclasses import dataclass

SCRIPT_DIR = Path("/Users/zach/Tokenomics-As-Institutional_Design/b2/paper/supplements")
RAW_DIR = Path("/tmp/b2_phase4")
DATE_STAMP = "2026-05-27"
VERSION = "v2_audited"

PROTOCOLS = {
    "FXS": {
        "contract": "0x3432B6A60D23Ca0dFCa7761B7ab56459D9C964D0",
        "project": "Frax Finance", "sector": "DeFi", "chain": "ethereum",
        "decimals": 18, "total_supply_raw": 99681495591133609740710857, "tge_year": 2020,
    },
    "SNX": {
        "contract": "0xC011a73ee8576Fb46F5E1c5751cA3B9Fe0af2a6F",
        "project": "Synthetix", "sector": "DeFi", "chain": "ethereum",
        "decimals": 18, "total_supply_raw": 344939867555663174515691674, "tge_year": 2018,
    },
    "GNO": {
        "contract": "0x6810e776880C02933D47DB1b9fc05908e5386b96",
        "project": "Gnosis", "sector": "DeFi", "chain": "ethereum",
        "decimals": 18, "total_supply_raw": 10000000000000000000000000, "tge_year": 2017,
    },
}

# AUDITED classifications (CONFIRMED set expanded based on Etherscan public name tags + Nansen API).
# Tuple: (address, class, label, confidence, source_doc)
PCA_CLASSIFICATIONS = {
    "FXS": [
        ("0x36cb65c1967a0fb0eee11569c51c2f2aa1ca6f6d", 4, "Fraxtal: Optimism Portal Proxy (Frax L2 bridge custody)",
         "CONFIRMED", "Etherscan public name tag retrieved 2026-05-27 via WebFetch: 'Fraxtal: Optimism Portal Proxy'"),
        ("0xc8418af6358ffdda74e09ca9cc3fe03ca6adc5b0", 3, "veFXS (vote-escrowed FXS staking aggregation)",
         "CONFIRMED", "Etherscan contract-source: Vyper_contract; documented at docs.frax.finance"),
        ("0x4a6d155df9ec9a1bb3639e6b7b99e46fb68d42f6", 4, "Fraxferry (Frax cross-chain bridge)",
         "CONFIRMED", "Etherscan contract-source: Fraxferry"),
        ("0x000000000004444c5dc75cb358380d2e3de08a90", 5, "Uniswap V4: Pool Manager (DEX trading-protocol custody)",
         "CONFIRMED", "Etherscan public name tag retrieved 2026-05-27 via WebFetch: 'Uniswap V4: Pool Manager'"),
        ("0x03b59bd1c8b9f6c265ba0c3421923b93f15036fa", 5, "FraxswapPair (Frax-native DEX liquidity pool custody)",
         "CONFIRMED", "Etherscan contract-source: FraxswapPair"),
        ("0xb1748c79709f4ba2dd82834b8c82d4a505003f27", 2, "Frax Finance: Comptroller (Foundation operational multisig)",
         "CONFIRMED", "Etherscan public name tag retrieved 2026-05-27 via WebFetch: 'Frax Finance: Comptroller'"),
        ("0xedc6bacdc1e29d7c5fa6f6eca6fdd447b9c487c9", 5, "Bitvavo CEX hot wallet (cross-protocol; also in SNX + GNO)",
         "CONFIRMED", "Nansen Address Labels API 2026-05-27: 'Bitvavo' / 'CEX' / 'Exchange' tags"),
    ],
    "SNX": [
        ("0xffffffaeff0b96ea8e4f94b2253f31abdd875847", 4, "Synthetix: Synthetix Core (V3 protocol-controlled inflation / treasury)",
         "CONFIRMED", "Etherscan public name tag retrieved 2026-05-27 via WebFetch: 'Synthetix: Synthetix Core'"),
        ("0x5fd79d46eba7f351fe49bff9e87cdea6c821ef9f", 4, "SynthetixBridgeEscrow (L1<->L2 bridge custody)",
         "CONFIRMED", "Etherscan contract-source: SynthetixBridgeEscrow; documented at docs.synthetix.io"),
        ("0xf977814e90da44bfa03b6295a0616a897441acec", 5, "Binance 8 (CEX hot wallet)",
         "CONFIRMED", "exclusions_log.csv precedent (LPT/OP/LDO/GMX); Nansen 'Binance' tag"),
        ("0x3a5cc8689d1b0cef2c317bc5c0ad6ce88b27d597", 5, "Luno: Wallet (CEX hot wallet)",
         "CONFIRMED", "Nansen Address Labels API 2026-05-27: 'Luno' / 'Luno: Wallet' / 'CEX' tags"),
        ("0xa9d1e08c7793af67e9d92fe308d5697fb81d3e43", 5, "Coinbase 10 (CEX hot wallet)",
         "CONFIRMED", "exclusions_log.csv precedent (AXL); Etherscan public name tag"),
        ("0x28c6c06298d514db089934071355e5743bf21d60", 5, "Binance 14 (CEX hot wallet)",
         "CONFIRMED", "exclusions_log.csv precedent (LDO); Etherscan public name tag"),
        ("0xa023f08c70a23abc7edfc5b6b5e171d78dfc947e", 5, "Crypto.com 22 / Crypto.com: Hot Wallet (cross-protocol; also in GNO)",
         "CONFIRMED", "Etherscan public name tag 'Crypto.com 22' + Nansen 'Crypto.com' / 'Crypto.com: Hot Wallet' / 'CEX' tags"),
        ("0x0529ea5885702715e83923c59746ae8734c553b7", 5, "Bitpanda 18 (CEX hot wallet; cross-protocol; also in FXS)",
         "CONFIRMED", "Etherscan public name tag retrieved 2026-05-27 via WebFetch: 'Bitpanda 18' / 'Beacon Depositor' / 'Exchange'"),
        ("0xedc6bacdc1e29d7c5fa6f6eca6fdd447b9c487c9", 5, "Bitvavo CEX (cross-protocol; also in FXS + GNO)",
         "CONFIRMED", "Nansen: Bitvavo / CEX / Exchange"),
        ("0xab782bc7d4a2b306825de5a7730034f8f63ee1bc", 5, "Bitvavo: Hot Wallet (cross-protocol; also in GNO)",
         "CONFIRMED", "Nansen: Bitvavo / Bitvavo: Hot Wallet / CEX"),
    ],
    "GNO": [
        ("0x0000000000000000000000000000000000000000", 1, "Null address (canonical burn destination)",
         "CONFIRMED", "Universal burn-address; 0x000...000 is canonical Ethereum burn destination"),
        ("0x88ad09518695c6c3712ac10a214be5109a655671", 4, "Gnosis Chain: ETH-xDAI Omni Bridge (bridge custody)",
         "CONFIRMED", "Etherscan public name tag retrieved 2026-05-27 via WebFetch: 'Gnosis Chain: ETH-xDAI Omni Bridge'"),
        ("0xec83f750adfe0e52a8b0dba6eeb6be5ba0bee535", 2, "Gnosis: Vesting (Foundation treasury vesting)",
         "CONFIRMED", "Etherscan public name tag retrieved 2026-05-27 via WebFetch: 'Gnosis: Vesting'"),
        ("0x604e4557e9020841f4e8eb98148de3d3cdea350c", 2, "GnosisDAO Disbursement (same creator/factory as Gnosis: Vesting)",
         "CONFIRMED", "Etherscan contract-source: Disbursement; same creator (0x12e9a5f7...) as Gnosis: Vesting"),
        ("0x849d52316331967b6ff1198e5e32a0eb168d039d", 2, "Gnosis: Active Treasury Management (Foundation treasury)",
         "CONFIRMED", "Etherscan public name tag retrieved 2026-05-27 via WebFetch: 'Gnosis: Active Treasury Management'"),
        ("0xae5fb390e5c4fa1962e39e98dbfb0ed8055ed7a9", 2, "koeppelmann.eth Safe (Martin Koppelmann; Gnosis co-founder personal custody)",
         "CONFIRMED", "Nansen Address Labels API: 'koeppelmann.eth*' social tag (Gnosis co-founder)"),
        ("0x4f8ad938eba0cd19155a835f617317a6e788c868", 3, "Gnosis: LGNO Token (Locked GNO staking aggregation contract; sister-pattern to veFXS)",
         "CONFIRMED", "Etherscan public name tag retrieved 2026-05-27 via WebFetch: 'Gnosis: LGNO Token'"),
        ("0xf977814e90da44bfa03b6295a0616a897441acec", 5, "Binance 8 (CEX hot wallet)",
         "CONFIRMED", "exclusions_log.csv precedent; Nansen 'Binance' tag"),
        ("0xa023f08c70a23abc7edfc5b6b5e171d78dfc947e", 5, "Crypto.com 22 / Crypto.com: Hot Wallet (cross-protocol; also in SNX)",
         "CONFIRMED", "Etherscan + Nansen consensus"),
        ("0xedc6bacdc1e29d7c5fa6f6eca6fdd447b9c487c9", 5, "Bitvavo CEX (cross-protocol; also in FXS + SNX)",
         "CONFIRMED", "Nansen: Bitvavo / CEX"),
        ("0xab782bc7d4a2b306825de5a7730034f8f63ee1bc", 5, "Bitvavo: Hot Wallet (cross-protocol; also in SNX)",
         "CONFIRMED", "Nansen: Bitvavo: Hot Wallet / CEX"),
        # TENTATIVE
        ("0x9d94ef33e7f8087117f85b3ff7b1d8f27e4053d5", 2, "Stefan George Safe (Gnosis co-founder personal custody; v1 mis-attributed as Mintr)",
         "TENTATIVE", "Etherscan creator: stefangeorge.eth (Gnosis co-founder) approximately 6 years ago; no public name tag; B2 §3.8 typology does not explicitly address founder-personal vs Foundation-operational custody distinction; classification depends on author decision on whether co-founder personal Safes count as Class 2 Foundation custody"),
        ("0xd2c8dfa974a8f6a5d25a45aa3ebf35b58c059185", 2, "GnosisSafeProxy (no public name tag; rank-17 at 0.12 percent)",
         "TENTATIVE", "Etherscan contract-source: GnosisSafeProxy; no public name tag retrieved"),
    ],
}


@dataclass
class HolderRow:
    rank: int
    address: str
    balance_raw: int
    share: float
    first_acquired: str


def load_holders(symbol: str):
    path = RAW_DIR / f"{symbol.lower()}_holders.json"
    d = json.load(open(path))
    raw = d.get("holders", [])
    parsed = sorted([
        {"address": r["wallet_address"].lower(), "balance_raw": int(r["balance"]),
         "first_acquired": r.get("first_acquired", "")}
        for r in raw
    ], key=lambda x: -x["balance_raw"])
    total = sum(x["balance_raw"] for x in parsed)
    return [HolderRow(rank=i+1, address=x["address"], balance_raw=x["balance_raw"],
                      share=x["balance_raw"]/total if total > 0 else 0.0,
                      first_acquired=x["first_acquired"]) for i, x in enumerate(parsed)], total


def compute_hhi(rows): return sum(r.share ** 2 for r in rows)


def compute_gini(rows):
    if not rows: return 0.0
    bals = sorted([r.balance_raw for r in rows])
    n = len(bals); cumsum = sum(i * b for i, b in enumerate(bals, 1))
    tot = sum(bals)
    return (2 * cumsum) / (n * tot) - (n + 1) / n if tot else 0.0


def exclude_and_renormalize(rows, excl):
    kept = [r for r in rows if r.address not in excl]
    new_total = sum(r.balance_raw for r in kept)
    if not new_total: return []
    return [HolderRow(rank=i+1, address=r.address, balance_raw=r.balance_raw,
                      share=r.balance_raw/new_total, first_acquired=r.first_acquired)
            for i, r in enumerate(kept)]


def topN_pct(rows, n): return 100.0 * sum(r.share for r in rows[:n])


# ============================================================
summary_rows, exclusion_rows, top20_rows = [], [], []

for sym, meta in PROTOCOLS.items():
    rows, total = load_holders(sym)
    hhi_pre = compute_hhi(rows); gini_pre = compute_gini(rows)
    classifications = PCA_CLASSIFICATIONS.get(sym, [])
    confirmed = {a.lower() for a, _, _, c, _ in classifications if c == "CONFIRMED"}
    tentative = {a.lower() for a, _, _, c, _ in classifications if c == "TENTATIVE"}

    rows_conf = exclude_and_renormalize(rows, confirmed)
    rows_full = exclude_and_renormalize(rows, confirmed | tentative)

    confirmed_share = 100.0 * sum(r.share for r in rows if r.address in confirmed)
    tentative_share = 100.0 * sum(r.share for r in rows if r.address in tentative)

    summary_rows.append({
        "symbol": sym, "project": meta["project"], "sector": meta["sector"],
        "chain": meta["chain"], "contract": meta["contract"],
        "n_holders_top1000": len(rows),
        "total_balance_top1000_units": f"{total / (10 ** meta['decimals']):.0f}",
        "tge_year": meta["tge_year"], "maturity_years": 2026 - meta["tge_year"],
        "hhi_pre": f"{hhi_pre:.6f}", "gini_pre": f"{gini_pre:.4f}",
        "top1_pct_pre": f"{topN_pct(rows, 1):.2f}",
        "top5_pct_pre": f"{topN_pct(rows, 5):.2f}",
        "top10_pct_pre": f"{topN_pct(rows, 10):.2f}",
        "n_pca_confirmed": len(confirmed), "confirmed_share_pct": f"{confirmed_share:.2f}",
        "hhi_confident": f"{compute_hhi(rows_conf):.6f}",
        "gini_confident": f"{compute_gini(rows_conf):.4f}",
        "top1_pct_confident": f"{topN_pct(rows_conf, 1):.2f}",
        "top5_pct_confident": f"{topN_pct(rows_conf, 5):.2f}",
        "top10_pct_confident": f"{topN_pct(rows_conf, 10):.2f}",
        "n_pca_full": len(confirmed | tentative), "tentative_share_pct": f"{tentative_share:.2f}",
        "hhi_full": f"{compute_hhi(rows_full):.6f}",
        "gini_full": f"{compute_gini(rows_full):.4f}",
        "top1_pct_full": f"{topN_pct(rows_full, 1):.2f}",
        "top5_pct_full": f"{topN_pct(rows_full, 5):.2f}",
        "top10_pct_full": f"{topN_pct(rows_full, 10):.2f}",
        "data_source": "Dune Sim API EVM token-holders endpoint",
        "data_pull_date": DATE_STAMP,
        "classification_audit_method": "Etherscan public name tag (WebFetch) + Nansen Address Labels API (POST /api/v1/profiler/address/labels)",
    })

    addr_to_class = {a.lower(): (c, lbl, conf) for a, c, lbl, conf, _ in classifications}
    for r in rows[:20]:
        cls = addr_to_class.get(r.address)
        top20_rows.append({
            "symbol": sym, "rank": r.rank, "address": r.address,
            "share_top1000_pct": f"{100.0*r.share:.4f}", "first_acquired": r.first_acquired,
            "pca_class": cls[0] if cls else "", "classification_label": cls[1] if cls else "",
            "confidence": cls[2] if cls else "",
        })
    for addr, cls, lbl, conf, src in classifications:
        a = addr.lower()
        rank = next((r.rank for r in rows if r.address == a), None)
        share = next((100.0*r.share for r in rows if r.address == a), 0.0)
        exclusion_rows.append({
            "symbol": sym, "address": a, "rank_in_top1000": rank,
            "share_top1000_pct": f"{share:.4f}", "pca_class": cls,
            "label": lbl, "confidence": conf, "source_doc": src, "chain": meta["chain"],
        })


# Write
for path, data in [
    (SCRIPT_DIR / f"phase4_evm_minibatch_{VERSION}_{DATE_STAMP}.csv", summary_rows),
    (SCRIPT_DIR / f"phase4_evm_minibatch_exclusions_{VERSION}_{DATE_STAMP}.csv", exclusion_rows),
    (SCRIPT_DIR / f"phase4_evm_minibatch_top20_{VERSION}_{DATE_STAMP}.csv", top20_rows),
]:
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(data[0].keys()))
        w.writeheader(); w.writerows(data)
    print(f"Wrote {path}")

print(f"\n{'='*110}\nPHASE 4 EVM MINI-BATCH (v2 AUDITED) HHI SUMMARY\n{'='*110}")
print(f"{'Sym':<5} {'HHI pre':>10} {'HHI conf':>10} {'HHI full':>10} {'top1 pre':>9} {'top1 conf':>10} {'top1 full':>10} {'PCA conf':>9} {'PCA full':>9} {'CONF shr':>9}")
for r in summary_rows:
    print(f"{r['symbol']:<5} {r['hhi_pre']:>10} {r['hhi_confident']:>10} {r['hhi_full']:>10} "
          f"{r['top1_pct_pre']:>9} {r['top1_pct_confident']:>10} {r['top1_pct_full']:>10} "
          f"{r['n_pca_confirmed']:>9} {r['n_pca_full']:>9} {r['confirmed_share_pct']:>9}")
print(f"\nTotal PCA candidates: {len(exclusion_rows)}")
print(f"  CONFIRMED: {sum(1 for r in exclusion_rows if r['confidence']=='CONFIRMED')}")
print(f"  TENTATIVE: {sum(1 for r in exclusion_rows if r['confidence']=='TENTATIVE')}")
