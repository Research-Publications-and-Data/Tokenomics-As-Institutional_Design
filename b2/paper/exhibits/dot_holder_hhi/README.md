# DOT Holder-HHI Exhibits

**Captured 2026-05-27** | **45th protocol; sister to 44-protocol cross-section**

## Purpose

Compute Polkadot (DOT) holder-balance HHI on top-1000 AssetHub addresses after Protocol-Controlled-Address (PCA) exclusion, placing DOT in the cross-section as a 45th holder-HHI observation. Distinct from validator-stake HHI (mechanically near-zero under NPoS Phragmen equalization at 0.0017); the holder-balance axis is comparable to the 44 EVM/Solana protocols in the main cross-section.

## Data source

**AssetHub Polkadot Subscan API** (`assethub-polkadot.api.subscan.io`). Post-Polkadot-1.0 migration, DOT balances live primarily on AssetHub (system parachain); the relay-chain endpoint returns only residual post-migration balances. AssetHub Subscan reports 1,781,108 total holders; we pull the top-1000 by balance.

## Scripts (reproducibility)

1. `dot_assethub_top_holders.py`: pulls top-1000 holders via Subscan AssetHub `/api/v2/scan/accounts` endpoint (10 pages of 100). Requires `SUBSCAN_API_KEY` environment variable (free tier).
2. `dot_pca_refined.py`: applies refined PCA classification by cross-referencing top-1000 against (a) Polkawatch operator_id registry (91 institutional staking providers controlling 275 validators), (b) multi-funder cluster identification (45 addresses that fund multiple validators), and (c) a Class 5 CEX-cluster registry (Binance cluster confirmed via SubSquare governance-forum ground-truth plus on-chain extrinsic verification 2026-05-27; see the Substrate-analog CEX-cluster finding below). The Polkawatch and funding-cluster inputs are the sample-expansion artifacts in `data/raw/`. Outputs PCA exclusions CSV + post-exclusion HHI.

## Results (2026-05-27 capture)

Two reportable values bracketing methodology completeness:

| Metric | Refined baseline (Classes 2+3 only) | With Class 5 Binance cluster |
|---|---|---|
| Total AssetHub holders | 1,781,108 | 1,781,108 |
| Top-1000 captured | 1,418,857,215 DOT (~92% of supply) | 1,418,857,215 DOT |
| Raw holder-HHI (no exclusion) | 0.0090 | 0.0090 |
| **Post-PCA-exclusion HHI** | **0.0093** | **0.0052** |
| PCAs identified | 10 (5 Class 2 + 5 Class 3) | 13 (5 Class 2 + 5 Class 3 + 3 Class 5) |
| PCA balance excluded | 54,659,790 DOT | 179,769,675 DOT |
| Top-1 (post-exclusion) | 16ZL8yLyXv3V... @ 94.1M (6.90%) | 13Z7KjGn... @ 40.3M (3.25%) |
| Top-10 (post-exclusion) share | 18.33% | 12.85% |
| Top-100 (post-exclusion) share | 61.78% | 58.85% |
| Cross-section placement | Compound 0.009 / Optimism 0.009 / Uniswap 0.010 peer group | below Lido 0.008; tightest in cross-section |

**Recommended primary**: 0.0052 (with Binance cluster excluded; ground-truth attributed) per cross-protocol consistency with the EVM sample-expansion findings that classify confirmed CEX hot, cold, and staking addresses as Class 5. Report 0.0093 as the **methodology-completeness sensitivity** ("if Class 5 attribution is rejected on academic-source-quality grounds"). The 44.4% gap between values is itself a finding about Substrate-chain CEX-attribution gap relative to EVM/Solana.

**Extended sensitivity** (per `dot_top20_investigation_2026-05-27.md`): a third scenario C-narrow (HHI = **0.0043**) includes rank-2 (40.3M; multi-depositor + bidirectional cluster with 13fKwtY... at $15M+ cumulative flow; LIKELY-CEX distinct from Binance) and rank-5 (16.2M; zero extrinsics; pure cold-storage; POSSIBLE-CEX). The Coinbase / Kraken / OKX / Bybit / KuCoin enumeration generalizes beyond Binance; ground-truth attribution for those custodians remains pending. The 0.0043 to 0.0093 range (2x band) reflects the cross-architecture CEX-attribution methodology gap on Substrate chains.

## PCA classification (refined; 10 of top-1000)

**Class 2 (Treasury/pallet; 5 accounts; pattern-matched via `modlpy/*` display)**:

| Rank | Address | Balance (DOT) | Display |
|---|---|---|---|
| 3 | 13UVJyLnbVp9...JVPhFsTB | 23,187,996 | modlpy/trsry |
| 320 | 13UVJyLnbVp9...H73FXaR6esrd | 676,380 | modlpy/trsrybt$ |
| 462 | 13UVJyLnbVp9...vEDeKeLjG2LS3Y | 386,986 | modlpy/trsrybt |
| 554 | 13UVJyLnbVp9...AADCmw9XQWvYW | 297,639 | modlpy/xcmch |
| 956 | 13UVJyLnbVp9...wSnqb3yanRjB | 114,205 | modlpy/trsrybt@ |

**Class 3 (Institutional staking-provider warm wallets + multi-funder clusters; 5 accounts; identified via Polkawatch operator_id cross-reference)**:

| Rank | Address | Balance (DOT) | Rationale |
|---|---|---|---|
| 17 | 13KJ3t8w1CKM...rCBTvojmM | 10,000,073 | Polkawatch operator_id (pos.dog; controls 38 validators) |
| 19 | 13E7LXW3NGYA...buzPxVkd4 | 10,000,023 | Multi-funder cluster (funds 2 validators) |
| 24 | 15j4dg5GzsL1...vLjvDCK | 9,137,211 | Multi-funder cluster (funds 3 validators) |
| 319 | 1qnJN7FViy3HZ...Caox4t8GT7 | 677,561 | Multi-funder cluster (funds 5 validators) |
| 735 | 15UHvPeMjYLv...ijzGPM3p9 | 181,715 | Polkawatch operator_id (Novasama; controls 4 validators) |

**Class 5 (CEX custody Binance cluster; 3 accounts; ground-truth attributed via SubSquare governance-forum + on-chain extrinsic verification)**:

| Rank | Address | Balance (DOT) | Architecture role | Evidence |
|---|---|---|---|---|
| 1 | 16ZL8yLyXv3V... | 94,103,159 | Binance cold storage | 5 extrinsics; pre-AssetHub-migration origin; only outbound DOT ever = 12M to confirmed Binance cluster (8M to hot + 4M to staking) |
| 4 | 13vg3Mrxm3GL... | 16,956,385 | Binance hot wallet (CONFIRMED) | SubSquare hydration-forum testimony (user zengsw 2025) + extrinsic `0x51bc6c61d67afa916163b22653750537554005b2448a19728bed52528f4eb186` block 8156083 verifies `balances.transfer_keep_alive` FROM 13vg3M... matching narrative (5-minute auto-rotation pattern; exact-amount Jose test 1.355049 DOT) |
| 8 | 12YfMjjeRPVH... | 14,000,258 | Binance staking position | 100% bonded; 2 extrinsics; only inbound DOT ever was 4M from confirmed Binance cold wallet (top-1 16ZL8y...) |

**Total Binance cluster: 125,059,802 DOT (~9.2% of top-1000 supply; ~8.8% of total AssetHub supply)**.

## Substrate-analog CEX-cluster finding (2026-05-27)

A parallel EVM finding documents Foundation cross-chain duplication (OP and ARB Foundation GnosisSafes hold tokens on both the L1 home chain and the L2 native chain; exclusion lists capture only the L1 side). Investigating the DOT top-1 attribution gap (16ZL8yLyXv3V... at 94.1M DOT, initially unattributed) surfaced a Substrate analog at a different mechanism: an intra-AssetHub same-custodian CEX cluster (cold plus hot plus staking architecture) that the identity-pallet plus Polkawatch operator-registry attribution stack does not detect on its own.

Investigation chain:

1. Top-1 (16ZL8y...) Subscan profile: 94.1M DOT fully transferable, zero locks/reserved/bonded, only 5 extrinsics, no identity, `assets_tag: "Whale"`. Cold-storage signature.
2. Outbound transfer audit: only 2 outbound DOT transfers ever (8M to rank-4 13vg3M... + 4M to rank-8 12YfMj...). Round-number signature suggesting institutional cold-to-hot rotation.
3. Rank-4 (13vg3M...) profile: 17.0M DOT, 66,628 extrinsics, high-velocity small-value rotation. Hot-wallet signature.
4. Rank-8 (12YfMj...) profile: 14.0M DOT, 100% bonded, only 2 extrinsics, only inbound DOT ever was 4M from cluster cold-storage. Same-cluster staking-position signature.
5. Same-cluster confirmation via outflow-graph: all 3 addresses converge to single custodian architecture.
6. Ground-truth attribution: SubSquare hydration governance forum post by user zengsw ([hydration.subsquare.io/posts/230](https://hydration.subsquare.io/posts/230)) explicitly states "the hot wallet 13vg3Mrxm3GL9eXxLsGgLYRueiwFCiMbkdHBL4ZN5aob5D4N. It has actually been marked as strongly associated with Binance" and describes 5-minute auto-rotation pattern with 3 on-chain extrinsic proofs.
7. Independent on-chain verification: extrinsic `0x51bc6c61d67afa916163b22653750537554005b2448a19728bed52528f4eb186` (block 8156083) verifies `balances.transfer_keep_alive` FROM 13vg3M... TO Jose's test address for exact random amount 1.355049 DOT (matches SubSquare narrative).
8. Cluster classification as Class 5 (CEX custody) per B2 §3.8 typology.

**Methodological implication**: identity-pallet + Polkawatch operator-registry attribution alone undercount Substrate-chain custodial concentration. Outflow-graph analysis combined with cold/hot/staking activity-pattern triangulation surfaces same-custodian clusters that don't appear in voluntary attestation registries. This is the Substrate analog of the EVM Foundation cross-chain duplication finding at a different mechanism (intra-chain custodian cluster vs cross-chain Foundation duplication); both reflect the structural limitation of self-reported on-chain attribution for institutional concentration measurement.

## Cross-section placement

Two reportable values reflecting methodology completeness:

**Primary (Class 5 Binance cluster excluded)**: DOT post-exclusion holder-HHI = **0.0052** places DOT as the **lowest-concentration observation** in the 45-protocol cross-section:

- Below Lido 0.008 (previously tightest)
- Lido 0.008 / Compound 0.009 / Optimism 0.009 / Uniswap 0.010 peer group is the next tier above
- Distinct from high-concentration DePIN tail: DRIFT 0.053 / GMX 0.065 / HNT 0.075 / JUP 0.096 / WeatherXM 0.148 / Livepeer 0.199

**Methodology-completeness sensitivity (Class 5 cluster not excluded)**: DOT post-exclusion holder-HHI = **0.0093** places DOT in the Compound 0.009 / Optimism 0.009 / Uniswap 0.010 peer group, bracketed by Lido 0.008 (lower) and Aave 0.013 (higher).

The 44.4% gap between values reflects the structural Substrate-chain CEX-attribution gap relative to EVM/Solana (Etherscan + Nansen labels yield ~95% high-share holder attribution on EVM; Helius + Sim API yield ~80% on Solana; Substrate AssetHub at ground-truth Class 5 attribution requires governance-forum + extrinsic verification work because Subscan public tags do not include CEX custody attributions). This is itself a finding for §5.7 cross-architecture methodology limitations.

## Caveats

1. **Class 5 ground-truth completeness**: only Binance cluster confirmed via SubSquare + extrinsic verification (3 addresses; 125.1M DOT). Other major CEX custodians (Coinbase, Kraken, OKX, Bybit, KuCoin) likely also operate AssetHub custody at similar scale but require separate ground-truth attribution work. Top-20 non-PCAs show 10-40M DOT each with cold-storage / mixed-activity signatures suggestive of additional custodial clusters (e.g., 13Z7KjGn... at 40.3M; 12ouvKS... at 16.2M with zero extrinsics; 112RLy... at 15.2M).
2. **Top-1000 coverage**: 92% of supply captured; long-tail residual (~8%) does not materially affect HHI under squared-share dominance.
3. **Class 3 completeness**: depends on Polkawatch operator registry coverage (91 operators / 275 validators of ~600 active validators). Operators NOT in Polkawatch's registry would slip the Class 3 net. Sister manual-review pass on top-20 non-PCAs (matching lock+reserved=balance pattern indicating 100% staked) flagged for future refinement.
4. **Methodology mismatch with validator-stake HHI**: holder-balance HHI (this artifact) is comparable to the cross-section; validator-stake HHI (0.0017 under NPoS Phragmen) is mechanically near-zero and not directly comparable. Paper §4.5.5 treats these as sister axes.

## Files

- `dot_assethub_holders_2026-05-27.csv`: top-1000 AssetHub holders (rank, address, balance, reserved, lock, display)
- `dot_pca_exclusions_2026-05-27.csv`: 13 PCAs (5 Class 2 + 5 Class 3 + 3 Class 5 Binance) with rationale
- `dot_pca_refined.py`: PCA classification + post-exclusion HHI computation (includes Class 5 Binance cluster registry with attribution evidence)
- `dot_cluster_sensitivity.py`: Substrate-analog CEX-cluster sensitivity computation (Scenarios A / B / C)
- `dot_cex_cluster_detection.py`: top-20 non-PCA whale systematic investigation (outflow-graph + activity-pattern + funding-source analysis)
- `dot_top20_investigation_2026-05-27.md`: top-20 whale investigation report (per-address findings + rank-2 LIKELY-CEX cluster + 163egH5d staking-rewards-pattern downgrade + three-scenario sensitivity band + Coinbase/Kraken/OKX/Bybit/KuCoin enumeration caveat)
- `dot_top20_nonpca_profile.csv`: per-address signature classification (rank, address, balance, extrinsics, locked_pct, signature, n_large_outbound, n_large_inbound, display)
- `dot_assethub_top_holders.py`: Subscan AssetHub puller (requires SUBSCAN_API_KEY env var)

## Reproduction

```bash
export SUBSCAN_API_KEY="<your-key>"
python3 dot_assethub_top_holders.py     # pulls fresh top-1000; saves CSV to /tmp
python3 dot_pca_refined.py              # applies refined PCA exclusion; computes HHI
python3 dot_cex_cluster_detection.py    # systematic top-20 whale investigation
python3 dot_cluster_sensitivity.py      # three-scenario sensitivity band
```
