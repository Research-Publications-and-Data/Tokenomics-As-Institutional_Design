# Supplementary File S16c: Polkadot fifth-protocol closure (AssetHub Polkadot Subscan)

**Companion to:** S16b (`S16_phase4_minibatch_2026-05-27.md`; FXS, SNX, GNO, TAO pre-exclusion baseline).

**Capture:** 2026-05-27 (AssetHub Polkadot Subscan).

**Data source:** AssetHub Polkadot Subscan API (`assethub-polkadot.api.subscan.io`). Top-1000 holders by balance; total holders 1,781,108; top-1000 captures approximately 92 percent of total DOT supply (1,418,857,215 DOT).

**Exhibits and reproduction artifacts:** [`exhibits/dot_holder_hhi/`](../exhibits/dot_holder_hhi/README.md) (README, holder CSVs, PCA-exclusions CSV, Subscan puller, refined PCA classifier).

---

## Canonical-source note

The current DOT holder distribution is measured on AssetHub, not the relay chain. After the Polkadot 1.0 migration (2024), DOT balances live primarily on the AssetHub system parachain; the relay-chain endpoint returns only residual post-migration balances and protocol-controlled accounts. A relay-chain-only snapshot (for example, the Dune `polkadot.balances` namespace, last updated 2025-07-23) therefore misrepresents the current distribution. The canonical source is the AssetHub Polkadot Subscan endpoint, which reports 1,781,108 total holders; this addendum measures the top-1000 by balance.

---

## Results (2026-05-27 capture)

Two reportable values bracket methodology completeness, depending on whether the confirmed Class 5 (centralized-exchange custody) Binance cluster is excluded:

| Metric | Refined baseline (Classes 2+3) | Primary (with Class 5 Binance cluster) |
|---|---:|---:|
| Total AssetHub holders | 1,781,108 | 1,781,108 |
| Top-1000 captured | 1,418,857,215 DOT (~92% of supply) | 1,418,857,215 DOT |
| Raw holder-HHI (no exclusion) | 0.0090 | 0.0090 |
| **Post-PCA-exclusion holder-HHI** | **0.0093** | **0.0052** |
| PCAs identified | 10 (5 Class 2 + 5 Class 3) | 13 (5 Class 2 + 5 Class 3 + 3 Class 5) |
| PCA balance excluded | 54,659,790 DOT | 179,769,675 DOT |
| Top-1 post-exclusion | `16ZL8yLyXv3V...` at 94.1M (6.90%) | `13Z7KjGn...` at 40.3M (3.25%) |
| Top-10 post-exclusion share | 18.33% | 12.85% |
| Top-100 post-exclusion share | 61.78% | 58.85% |
| Cross-section placement | Compound 0.009 / Optimism 0.009 / Uniswap 0.010 peer group | below Lido 0.008; tightest in cross-section |

**Recommended primary: 0.0052** (with the Binance cluster excluded, ground-truth attributed), for cross-protocol consistency with the EVM and Solana sample-expansion findings that classify confirmed CEX hot, cold, and staking addresses as Class 5. **Report 0.0093 as the methodology-completeness sensitivity** (the value if Class 5 attribution is rejected on academic-source-quality grounds). The 44.4 percent gap between the two values is itself a finding about the Substrate-chain CEX-attribution gap relative to EVM and Solana (Section 5.7).

**Direction-of-shift note.** The refined-baseline post-exclusion HHI (0.0093) shifts upward from the raw HHI (0.0090) because the excluded Class 3 institutional staking-provider warm wallets (5 accounts at 10 to 15M DOT each) were proportionally larger than the average remaining holder, so re-normalization to the smaller denominator inflates the squared-share dominance of the remaining large holders. The pattern is mechanically expected when high-share addresses are excluded from a long-tail distribution. Excluding the additional Class 5 Binance cluster (the single largest holders) then pulls the HHI down to 0.0052.

---

## PCA classification (13 of top-1000)

### Class 2 (Treasury/pallet; 5 accounts; pattern-matched via `modlpy/*` display field)

| Rank | Address | Balance (DOT) | Display |
|---:|---|---:|---|
| 3 | `13UVJyLnbVp9...JVPhFsTB` | 23,187,996 | `modlpy/trsry` |
| 320 | `13UVJyLnbVp9...H73FXaR6esrd` | 676,380 | `modlpy/trsrybt$` |
| 462 | `13UVJyLnbVp9...vEDeKeLjG2LS3Y` | 386,986 | `modlpy/trsrybt` |
| 554 | `13UVJyLnbVp9...AADCmw9XQWvYW` | 297,639 | `modlpy/xcmch` |
| 956 | `13UVJyLnbVp9...wSnqb3yanRjB` | 114,205 | `modlpy/trsrybt@` |

The Treasury account (`modlpy/trsry`) is the canonical Polkadot Treasury pallet account. The sub-pallets (`modlpy/trsrybt`, `modlpy/trsrybt$`, `modlpy/trsrybt@`) are Bounty pallet sub-accounts; `modlpy/xcmch` is the XCM channel pallet account. All five are protocol-controlled by the Polkadot runtime; standard Class 2 (Foundation/treasury) classification applies.

### Class 3 (Institutional staking-provider; 5 accounts; Polkawatch operator-registry + multi-funder cluster identification)

| Rank | Address | Balance (DOT) | Rationale |
|---:|---|---:|---|
| 17 | `13KJ3t8w1CKM...rCBTvojmM` | 10,000,073 | Polkawatch operator (pos.dog; controls 38 validators) |
| 19 | `13E7LXW3NGYA...buzPxVkd4` | 10,000,023 | Multi-funder cluster (funds 2 validators) |
| 24 | `15j4dg5GzsL1...vLjvDCK` | 9,137,211 | Multi-funder cluster (funds 3 validators) |
| 319 | `1qnJN7FViy3HZ...Caox4t8GT7` | 677,561 | Multi-funder cluster (funds 5 validators) |
| 735 | `15UHvPeMjYLv...ijzGPM3p9` | 181,715 | Polkawatch operator (Novasama; controls 4 validators) |

Class 3 (staking-aggregation) classification extends to Substrate-native institutional staking-provider warm wallets per the Section 3.8 typology (sister to the EVM SPL stake-pool and Lido stETH Class 3 pattern). The Polkawatch operator-registry (91 institutional staking providers; 275 of approximately 600 active validators attributed) and multi-funder cluster identification (45 addresses funding multiple validators) jointly provide the Class 3 methodology for Substrate-native protocols.

### Class 5 (CEX custody; Binance cluster; 3 accounts; ground-truth attributed)

| Rank | Address | Balance (DOT) | Architecture role | Evidence |
|---:|---|---:|---|---|
| 1 | `16ZL8yLyXv3V...` | 94,103,159 | Binance cold storage | 5 extrinsics; pre-migration origin; only outbound DOT ever was 12M to the confirmed cluster (8M to the hot wallet, 4M to the staking position) |
| 4 | `13vg3Mrxm3GL...` | 16,956,385 | Binance hot wallet | Governance-forum testimony (SubSquare hydration forum, user zengsw, 2025) plus on-chain extrinsic `0x51bc6c...` (block 8156083) verifying a `balances.transfer_keep_alive` from this address matching the narrative (5-minute auto-rotation; exact-amount test transfer 1.355049 DOT) |
| 8 | `12YfMjjeRPVH...` | 14,000,258 | Binance staking position | 100 percent bonded; 2 extrinsics; only inbound DOT ever was 4M from the cluster cold wallet (rank 1) |

**Total Binance cluster: 125,059,802 DOT (~9.2 percent of top-1000 supply).** The cluster was surfaced by outflow-graph analysis combined with cold/hot/staking activity-pattern triangulation: the three addresses converge on a single custodian architecture (cold storage rank 1, hot wallet rank 4, staking position rank 8), confirmed by governance-forum ground-truth and independent on-chain extrinsic verification. The Class 5 classification follows the Section 3.8 typology.

### Class 1 and Class 4 in top-1000

- Class 1 (burn destinations): 0. Polkadot has no native burn convention (slashed funds route to the Treasury).
- Class 4 (bridge custody): 0 in top-1000. Cross-parachain bridge custody (XCM channel accounts on other parachains) would require a separate XCM channel registry cross-reference; deferred (see Outstanding gaps).

---

## A methodological finding on Substrate CEX attribution

The identity-pallet plus Polkawatch operator-registry attribution stack does not, on its own, detect the intra-AssetHub same-custodian CEX cluster (cold plus hot plus staking architecture) documented above: the cold-storage and staking addresses carry no identity and do not appear in the operator registry, and only the hot wallet is attributable through governance-forum ground-truth. Outflow-graph analysis combined with cold/hot/staking activity-pattern triangulation surfaces the same-custodian cluster that voluntary attestation registries miss. This is a Substrate-side instance of the broader pattern that self-reported on-chain attribution undercounts institutional concentration, and it motivates the methodology-completeness sensitivity band reported above. An extended sensitivity scenario adds two further likely-CEX whales (rank 2 at 40.3M and rank 5 at 16.2M, distinct from the Binance cluster) and yields a third value of 0.0043; the 0.0043 to 0.0093 band reflects the cross-architecture CEX-attribution gap on Substrate chains, where ground-truth attribution requires governance-forum plus extrinsic verification because public Subscan tags do not include CEX custody attributions.

---

## Cross-section placement

**Primary (Class 5 Binance cluster excluded): DOT post-exclusion holder-HHI = 0.0052** places DOT as the lowest-concentration observation in the 45-protocol cross-section, below the previously tightest Lido (0.008), with the Lido 0.008 / Compound 0.009 / Optimism 0.009 / Uniswap 0.010 peer group as the next tier and the high-concentration DePIN tail (DRIFT 0.053, GMX 0.065, HNT 0.075, JUP 0.096, WeatherXM 0.148, Livepeer 0.199) far above.

**Methodology-completeness sensitivity (Class 5 cluster not excluded): DOT post-exclusion holder-HHI = 0.0093** places DOT in the Compound 0.009 / Optimism 0.009 / Uniswap 0.010 peer group, bracketed by Lido 0.008 below and Aave 0.013 above.

Either placement is consistent with Polkadot's mature L1 architecture (five-year operating history; broad nominator-validator distribution under NPoS) and the absence of a dominant Foundation/treasury concentration pattern at the holder-balance axis (the Treasury account holds 23.2M DOT, approximately 1.6 percent of supply, excluded as a Class 2 PCA).

**Methodology mismatch with validator-stake HHI.** The holder-balance HHI reported here is comparable to the cross-section's 44 EVM and Solana protocols. The validator-stake HHI of 0.0017 reported in Section 4.5.5 is a separate axis measuring NPoS bonded-stake concentration across the active validator set under Phragmen equalization; it is mechanically near-zero by design and is not directly comparable. Section 4.5.5 treats holder-balance HHI and validator-stake HHI as parallel-but-distinct concentration axes for Substrate NPoS protocols.

---

## Outstanding gaps

1. **Other CEX custodians.** Only the Binance cluster is ground-truth confirmed (3 addresses; 125.1M DOT). Other major CEX custodians (Coinbase, Kraken, OKX, Bybit, KuCoin) likely also operate AssetHub custody at similar scale but require separate ground-truth attribution work; the top-20 non-PCAs show 10 to 40M DOT each with cold-storage or mixed-activity signatures suggestive of additional custodial clusters.
2. **Class 3 completeness.** Class 3 coverage depends on the Polkawatch operator-registry (91 providers; 275 of approximately 600 active validators). Operators not indexed by Polkawatch slip the Class 3 net; manual review of the top-20 non-PCAs surfaces additional 100-percent-staked candidates. Continuation work: cross-reference top-50 non-PCAs against direct on-chain nominator-validator-stake patterns.
3. **Cross-parachain DOT custody.** Web3 Foundation and the Polkadot Treasury hold DOT across multiple parachains via XCM-transferred reserve accounts in addition to AssetHub; the current capture does not cross-check parachain reserve accounts. Continuation work: enumerate parachain reserve accounts via the XCM channel registry and cross-reference top balances per parachain against the AssetHub top-1000.

---

## Section 3.8 PCA typology: Substrate-native extensions

| Class | Substrate-native extension | DOT anchor |
|---|---|---|
| Class 1 (burns) | No native burn convention (slashed funds route to Treasury) | none |
| Class 2 (Foundation/treasury) | Runtime pallets via `modlpy/*` display pattern (Treasury, Bounty, XCM channels) | 5 accounts |
| Class 3 (staking-aggregation) | Polkawatch operator-registry plus multi-funder cluster identification | 5 accounts (pos.dog, Novasama, 3 multi-funder clusters) |
| Class 4 (bridge custody) | XCM channel registry (cross-parachain); deferred | out of scope this cycle |
| Class 5 (CEX) | Outflow-graph plus cold/hot/staking triangulation plus governance-forum and extrinsic ground-truth | 3-account Binance cluster (125.1M DOT) |

Substrate-native Class 2, Class 3, and Class 5 methodology now anchors the Section 3.8 typology's cross-architecture coverage (EVM via Etherscan plus Nansen; Solana via Helius DAS plus Sim API; Substrate via Polkawatch operator-registry, `modlpy/*` display matching, and outflow-graph CEX-cluster triangulation).

---

## Cross-references

- S16b: Phase 4 cycle 1 sample-expansion batch (FXS, SNX, GNO, TAO pre-exclusion baseline).
- S18: EVM sample-expansion PCA classification with two-layer audit.
- S19: Polkadot validator-set five-axis attribution methodology (sister axis, distinct from the holder-balance HHI reported here).
- S20: Polkadot Subscan refresh finding (methodology validation; sister to the AssetHub canonical-source note above).
- Exhibits: [`exhibits/dot_holder_hhi/`](../exhibits/dot_holder_hhi/README.md) (README, holder CSVs, PCA-exclusions CSV, Subscan puller, refined PCA classifier, top-20 whale investigation).
- B2 PAPER.md Section 3.8 (five-class PCA typology; Substrate-native extensions), Section 4.3 (sector contrast), Section 4.5.5 (validator-set attribution), and Section 5.7 (cross-architecture attribution-coverage limitation).
