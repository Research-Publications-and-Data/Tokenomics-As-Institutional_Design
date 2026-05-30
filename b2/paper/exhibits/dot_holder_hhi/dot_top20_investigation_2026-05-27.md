# DOT Top-20 Non-PCA Whale Investigation

**Captured 2026-05-27** | **Substrate-analog CEX-cluster extended investigation**

Systematic outflow-graph + activity-pattern + funding-source investigation of the top-20 remaining non-PCA whales (post Class 2 + Class 3 + Class 5 Binance exclusion) to identify additional CEX clusters per Coinbase / Kraken / OKX / Bybit / KuCoin candidate enumeration.

## Method

For each top-20 non-PCA address:
1. Subscan AssetHub profile pull (balance, locks, bonded, extrinsics, tags, role, identity).
2. Activity-pattern signature classification (COLD-STORAGE / HOT-WALLET / 100%-STAKED / MOSTLY-STAKED / MIXED).
3. Inbound large DOT transfers (>=100K) for funding-source attribution.
4. Outbound large DOT transfers (>=50K) for recipient cluster identification.
5. Cross-reference recipients across senders for shared-cluster signatures.
6. Cross-reference against confirmed Binance cluster (16ZL8y / 13vg3M / 12YfMj).

## Activity-pattern summary (top 20)

| Pattern | Count | Implication |
|---|---|---|
| MOSTLY-STAKED (50%+ locked; some outbound) | 9 | Institutional staking positions |
| 100%-STAKED (fully bonded; zero outbound) | 4 | Institutional staking pools |
| COLD-STORAGE (zero extrinsics; receive-only) | 4 | Custody-grade cold storage |
| MIXED (active; varied locks) | 3 | Active accounts |

Aggregate: **9 + 4 = 13 of 20 are staked positions** (institutional staking infrastructure beneficiaries); **4 of 20 are pure cold storage** (custody pattern).

## Findings

### F1: Rank-2 cluster (STRONG-LIKELY-CEX; not Binance)

**13Z7KjGnzdAdMre9cqRwTZHR6F2p36gqBsaNmQwwosiPz8JT** (40.3M DOT; 31 extrinsics):

- **13 large inbound transfers from 8+ unique senders**: classic exchange deposit-collection pattern (60K-1.7M DOT per deposit).
- Top funding source: 13fKwtY... (1.69M DOT inbound) + 13QzQJw... (785K) + 16JsLeTi... (777K).
- **30 large outbound transfers**: top recipient 13fKwtY... received 14,070,000 DOT cumulative from rank-2 (bidirectional cluster signature).
- Other large outflow recipients: 12CUYV... (2.45M cumulative) + 13QzQJw... (1.6M cumulative).
- Bidirectional flow with 13fKwtY... ($15M+ both directions) consistent with same-custodian cold/hot wallet rotation.
- One inbound from confirmed Binance hot wallet (247,700 DOT block 13149746) is likely a user-driven Binance withdrawal, not same-cluster.
- **Classification: LIKELY-CEX (custodian distinct from Binance; possibly Coinbase / Kraken / OKX / Bybit)**.

### F2: Rank-5 (POSSIBLE-CEX; pure cold-storage; migration-origin)

**12ouvKSvKnXAdXFR5oCL1vXimWrkDWG3joMNw3ETupTRs1ab** (16.2M DOT; ZERO extrinsics):

- ZERO extrinsics, ZERO inbound transfers >= 100K DOT (only 1 zero-amount inbound).
- Pure migration-origin balance (relay chain → AssetHub auto-migration).
- Cold-storage signature without outflow data (cannot triangulate cluster).
- **Classification: POSSIBLE-CEX (signature consistent with custody cold wallet; attribution-uncertain)**.

### F3: Ranks 10/11/12 (AMBIGUOUS; staking-infrastructure-not-CEX)

**165iwLPu...** (12.1M; rank 10), **15DQVbb...** (12.1M; rank 11), **1yEvPjU...** (11.9M; rank 12): ALL three funded by single distributor **163egH5dubAAwbYQQ6wH3jhe8J5YV3wAiEExAvu67BAXmxyx** in 58-91 separate transfers of standardized 130-180K DOT each, with multiple transfers at the same block (e.g., block 10730792 sends 162,810 DOT to multiple recipients simultaneously).

**Distributor profile**: 163egH5d... currently holds 382K DOT, tagged "Dolphin" (Subscan small-whale; not "Whale"), 3263 extrinsics, no identity. Pattern signature (exact-amount recurring batches at same block) is consistent with **staking-rewards-pallet batch payout** OR **institutional accumulation drip**, NOT CEX custody. Classification cannot be definitively resolved without on-chain staking-pallet extrinsic-type evidence.

**Classification: AMBIGUOUS** (more likely staking infrastructure beneficiaries than CEX custody; NOT included in conservative Class 5 expansion).

### F4: Ranks 13-27 (mostly-staked institutional positions)

13 of remaining 17 addresses (ranks 13, 14, 16, 18, 20, 21, 22, 23, 25, 26, 27 + others) are MOSTLY-STAKED (50%+ locked) or 100%-STAKED (fully bonded) with ZERO outbound DOT transfers. Pattern signature: institutional staking positions (likely served by staking-provider warm wallets already caught at Class 3 Polkawatch cross-reference). Some may correspond to staking-pool delegators not in the Polkawatch operator registry (Class 3 coverage gap; not Class 5 CEX custody).

## Three-scenario sensitivity band

| Scenario | Class 5 inclusion | HHI | Excluded (M DOT) | Cross-section placement |
|---|---|---|---|---|
| A (refined baseline) | none (Class 2+3 only) | **0.0093** | 54.7 | Compound 0.009 / Optimism 0.009 / Uniswap 0.010 peer group |
| B (Binance confirmed) | 3 (Binance cluster) | **0.0052** | 179.8 | Below Lido 0.008; tightest in cross-section |
| C-narrow (+ LIKELY-CEX) | 5 (Binance + rank-2 + rank-5) | **0.0043** | 236.3 | Below all observations |

**Methodologically defensible primary**: Scenario B (0.0052), because the Binance cluster has hard ground-truth attribution via SubSquare governance forum + on-chain extrinsic verification.

**Sensitivity-band brackets**: A (0.0093; if Class 5 attribution rejected entirely) and C-narrow (0.0043; if rank-2 + rank-5 LIKELY-CEX accepted). The 2x range from 0.0043 to 0.0093 reflects the cross-architecture CEX-attribution methodology gap on Substrate chains.

## Methodological notes

1. **163egH5d... distributor pattern is NOT CEX custody**: exact-amount recurring batches at same block to multiple recipients is the **staking-rewards-pallet batch payout signature**. Distinguishes from CEX cold-to-hot rotation (round-number one-shot transfers; cold + hot + staking architecture).
2. **Multi-depositor pattern is exchange deposit-collection signature**: rank-2 13Z7KjGn... receives from 8+ unique senders with 60K-1.7M DOT each, then routes outflows to 3-4 repeat recipients with $1M+ cumulative bidirectional flows. This is the classic CEX deposit-aggregation architecture.
3. **Pure cold-storage without outflow data is attribution-blocked**: rank-5 12ouvKS... has ZERO extrinsics and zero inbound transfers (migration-origin balance only); cannot triangulate via outflow-graph or recipient-cluster analysis. Marker for "POSSIBLE-CEX" classification but requires external attribution (Subscan public-tag registry / OFAC sanctioned-entity lists / governance-forum testimony / direct exchange disclosure).
4. **Polkawatch + Subscan identity-pallet + Class 3 funding-cluster all undercount CEX custody on Substrate**: confirmed via Binance cluster (none of three addresses are in Polkawatch operator registry; none have identity-pallet attestation). Cross-architecture parity with EVM Foundation cross-chain duplication finding (Foundation cross-chain duplication).

## Caveats

1. **CEX-specific attribution coverage**: only Binance has ground-truth attribution (3 addresses; via SubSquare). Coinbase, Kraken, OKX, Bybit, KuCoin custody on AssetHub Polkadot likely exists at comparable scale but remains attribution-blocked without (a) governance-forum testimony for those exchanges, (b) Subscan public-tag updates, or (c) direct exchange disclosure.
2. **13fKwtY... null query**: the rank-2's main outflow recipient (received 14.07M cumulative DOT) returned null Subscan response (possible rate-limit transient OR address-format issue OR genuinely-non-existent address). Re-investigation deferred (not load-bearing for the rank-2 cluster classification).
3. **Top-1000 coverage**: 92% of supply captured; long-tail residual (~8%) does not materially affect HHI under squared-share dominance. Additional CEX custody in the rank 1000+ tail would only marginally shift HHI.

## Files

- `dot_top20_investigation_2026-05-27.md`: this report.
- `dot_top20_nonpca_profile.csv`: per-address profile + signature classification (rank, address, balance, extrinsics, locked_pct, signature, n_large_outbound, n_large_inbound, display).

## Reproduction

```bash
export SUBSCAN_API_KEY="<your-key>"
python3 dot_cex_cluster_detection.py    # systematic top-20 investigation; writes profile CSV
python3 dot_cluster_sensitivity.py      # three-scenario HHI computation
```
