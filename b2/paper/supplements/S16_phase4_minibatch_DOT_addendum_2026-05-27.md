# Supplementary File S16c: Polkadot fifth-protocol closure (AssetHub Polkadot Subscan)

**Companion to:** `S16_phase4_minibatch_2026-05-27.md` (PID 4300 cycle 1; FXS, SNX, GNO, TAO pre-exclusion baseline).

**Capture:** 2026-05-27 (AssetHub Polkadot Subscan).

**Data source:** AssetHub Polkadot Subscan API (`assethub-polkadot.api.subscan.io`). Top-1000 holders by balance; total holders 1,781,108; top-1000 captures approximately 92 percent of total DOT supply (1,418,857,215 DOT of approximately 1.55B circulating).

**Exhibits + reproduction artifacts:** [`exhibits/dot_holder_hhi/`](../exhibits/dot_holder_hhi/README.md) (README + CSVs + Subscan puller + refined PCA classifier).

---

## Methodology-of-record correction (supersedes prior PID 4300 cycle 1 DOT addendum)

The initial Phase 4 cycle 1 DOT addendum (PID 4300; 2026-05-27 first capture) reported DOT holder-HHI = 0.014 via Dune `polkadot.balances` namespace (2025-07-23 snapshot, approximately 10 months stale). That source was incorrect for the post-Polkadot-1.0 era: the Dune `polkadot.balances` namespace returns relay-chain account balances only, but post-Polkadot-1.0 migration (2024) DOT balances live primarily on the AssetHub system parachain, with the relay chain holding only residual post-migration balances and protocol-controlled accounts. The relay-chain snapshot therefore misrepresents the current DOT holder distribution.

The canonical source for current DOT holder distribution is the AssetHub Polkadot Subscan endpoint (`assethub-polkadot.api.subscan.io`), which indexes AssetHub balances. AssetHub Subscan reports 1,781,108 total holders versus the smaller relay-chain residual; the top-1000 by balance captures approximately 92 percent of total DOT supply. This addendum supersedes the cycle 1 Dune-sourced finding (HHI = 0.014; stale relay-chain snapshot) with the AssetHub-Subscan capture (post-PCA-exclusion HHI = 0.0093; 2026-05-27).

The supersession is methodology-of-record (sister to S20 Subscan-refresh-finding documentation pattern); the cycle 1 finding is retained in commit history as audit-trail-of-record of the canonical-source evolution from Polkadot relay chain (pre-Polkadot-1.0) to AssetHub system parachain (post-Polkadot-1.0). An EC entry covers the canonical-source correction in `docs/ERROR_CORRECTION_LOG.md`.

---

## Results (canonical 2026-05-27 capture)

| Metric | Value |
|---|---:|
| Total AssetHub holders | 1,781,108 |
| Top-1000 captured balance | 1,418,857,215 DOT (approximately 92 percent of supply) |
| Raw holder-HHI (top-1000; no exclusion) | 0.0090 |
| **Post-PCA-exclusion holder-HHI** | **0.0093** |
| PCAs identified | 10 (5 Class 2 + 5 Class 3) |
| PCA balance excluded | 54,659,790 DOT |
| Top-1 post-exclusion share | 6.90 percent (`16ZL8yLyXv3V...` at 94.1M DOT; UNATTRIBUTED) |
| Top-10 post-exclusion share | 18.33 percent |
| Top-100 post-exclusion share | 61.78 percent |

**Direction-of-shift note.** Post-PCA-exclusion HHI (0.0093) shifts UPWARD from raw HHI (0.0090) because the excluded Class 3 institutional staking-provider warm wallets (5 accounts at 10-15M DOT each) were proportionally larger than the average remaining holder, so re-normalization to the smaller denominator inflates the squared-share dominance of remaining large holders. The pattern is mechanically expected when high-share addresses are excluded from a long-tail distribution; sister to the counterintuitive INCREASE pattern surfaced in S18 v1 for FXS + SNX before the audit-cycle resolution.

---

## PCA classification (refined; 10 of top-1000)

### Class 2 (Treasury/pallet; 5 accounts; pattern-matched via `modlpy/*` display field)

| Rank | Address | Balance (DOT) | Display |
|---:|---|---:|---|
| 3 | `13UVJyLnbVp9...JVPhFsTB` | 23,187,996 | `modlpy/trsry` |
| 320 | `13UVJyLnbVp9...H73FXaR6esrd` | 676,380 | `modlpy/trsrybt$` |
| 462 | `13UVJyLnbVp9...vEDeKeLjG2LS3Y` | 386,986 | `modlpy/trsrybt` |
| 554 | `13UVJyLnbVp9...AADCmw9XQWvYW` | 297,639 | `modlpy/xcmch` |
| 956 | `13UVJyLnbVp9...wSnqb3yanRjB` | 114,205 | `modlpy/trsrybt@` |

Treasury account (`modlpy/trsry`) is the canonical Polkadot Treasury pallet account. Sub-pallets (`modlpy/trsrybt`, `modlpy/trsrybt$`, `modlpy/trsrybt@`) are Bounty pallet sub-accounts (treasury bounties subsystem); `modlpy/xcmch` is the XCM channel pallet account. All five are protocol-controlled by the Polkadot runtime; standard Class 2 (Foundation/treasury) PCA classification applies.

### Class 3 (Institutional staking-provider; 5 accounts; identified via Polkawatch operator_id cross-reference + multi-funder cluster identification)

| Rank | Address | Balance (DOT) | Rationale |
|---:|---|---:|---|
| 17 | `13KJ3t8w1CKM...rCBTvojmM` | 10,000,073 | Polkawatch operator_id: `pos.dog` (controls 38 validators in active set) |
| 19 | `13E7LXW3NGYA...buzPxVkd4` | 10,000,023 | Multi-funder cluster (funds 2 validators) |
| 24 | `15j4dg5GzsL1...vLjvDCK` | 9,137,211 | Multi-funder cluster (funds 3 validators) |
| 319 | `1qnJN7FViy3HZ...Caox4t8GT7` | 677,561 | Multi-funder cluster (funds 5 validators) |
| 735 | `15UHvPeMjYLv...ijzGPM3p9` | 181,715 | Polkawatch operator_id: Novasama (controls 4 validators in active set) |

Class 3 (staking-aggregation) PCA classification extended to Substrate-native institutional staking-provider warm wallets per the §3.8 typology Substrate extension (sister to EVM SPL stake-pool / Lido stETH Class 3 pattern). The Polkawatch operator-registry (91 institutional staking providers indexed; 275 of approximately 600 active validators attributed) and multi-funder cluster identification (45 addresses funding multiple validators) jointly provide the Class 3 attribution methodology for Substrate-native protocols; sister to the S19 5-axis validator-set attribution methodology.

### Class 1, 4, 5 in top-1000

- Class 1 (burn destinations): 0. Polkadot has no native burn convention (slashed funds route to Treasury rather than burn addresses).
- Class 4 (bridge custody): 0 in top-1000. Cross-parachain bridge custody (XCM channel accounts on Acala, Moonbeam, etc.) would require separate XCM channel registry cross-reference; deferred (see Outstanding Gaps below).
- Class 5 (CEX): 0 directly identified in top-1000 via Polkawatch + multi-funder methodology. Top-1 holder remains unattributed (see Outstanding Gaps below); likely Class 5 (CEX cold wallet) or Class 2 (Web3 Foundation cold storage) per qualitative inspection.

---

## Cross-section placement

DOT post-PCA-exclusion holder-HHI = **0.0093** places among the lowest-concentration protocols in the 45-protocol cross-section:

- **Sister anchors at similar HHI:** Compound (0.009), Optimism (0.009), Uniswap (0.010).
- **Bracketed by:** Lido (0.008; lower) and Aave (0.013; higher).
- **Distinct from high-concentration DePIN tail:** DRIFT (0.053), GMX (0.065), HNT (0.075), JUP (0.096), WeatherXM (0.148), Livepeer (0.199).

The placement is consistent with Polkadot's mature L1 architecture (5-year operating history; broad nominator-validator distribution under NPoS) and the absence of a dominant Foundation/treasury concentration pattern at the holder-balance axis (Treasury account holds 23.2M DOT or approximately 1.6 percent of supply, excluded as Class 2 PCA).

**Methodology mismatch with validator-stake HHI.** The holder-balance HHI reported here (0.0093) is comparable to the cross-section's 44 EVM and Solana protocols. The validator-stake HHI of 0.0017 reported in §4.5.5 is a separate axis measuring NPoS bonded-stake concentration across the active validator set under Phragmen equalization; it is mechanically near-zero by NPoS design and is not directly comparable to holder-balance HHI across the broader cross-section. The paper §4.5.5 treats holder-balance HHI and validator-stake HHI as parallel-but-distinct concentration axes for Substrate NPoS protocols.

---

## Outstanding gaps (flagged for KNOWN_UNKNOWNS)

### Gap 1: Top-1 attribution

The rank-1 holder `16ZL8yLyXv3V3L3z9ofR1ovFLziyXaN1DPq4yffMAZ9czzBD` at 94,117,720 DOT (6.90 percent of top-1000 post-exclusion) is unattributed in both the Subscan display field and the Polkawatch operator registry. Likely candidates: (a) Class 5 CEX cold wallet (Coinbase Custody is a known DOT institutional custody provider); (b) Class 2 Web3 Foundation cold storage; (c) institutional custody pattern outside both registries. If the attribution resolves to Class 5 or Class 2, post-PCA-exclusion HHI drops materially (top-1 squared-share at 6.90 percent contributes approximately 0.0048 to HHI of 0.0093, or roughly 51 percent of the total). Investigation deferred to a continuation cycle; the paper acknowledges as a sensitivity point per the addendum's caveat section.

### Gap 2: Class 3 completeness

Class 3 attribution coverage depends on the Polkawatch operator-registry coverage (91 institutional staking providers / 275 validators of approximately 600 active validators). Operators not indexed by Polkawatch slip the Class 3 net. Manual review of the top-20 non-PCAs surfaces multiple addresses with `lock + reserved = balance` pattern (indicating 100 percent staked), 10-15M DOT balance, behavior consistent with additional Class 3 candidates that are not in the Polkawatch registry. Continuation cycle work: cross-reference top-50 non-PCAs against direct on-chain nominator-validator-stake patterns (Substrate `Staking.nominators` storage queries) to surface Class 3 misses.

### Gap 3: Cross-parachain DOT custody (Substrate analog of EVM L1/L2 Foundation duplication)

Web3 Foundation and Polkadot Treasury hold DOT positions across multiple parachains via XCM-transferred reserve accounts (Acala, Moonbeam, Astar, etc.) in addition to AssetHub. The current Phase 4 capture does not cross-check parachain reserve accounts; sister to the EVM L1/L2 Foundation duplication finding (F-6 in the cross-protocol holder-axis sister analysis) where Foundation positions on Optimism / Arbitrum / Base were double-counted in early Phase 1 analysis. Continuation cycle work: enumerate parachain reserve accounts via Polkadot Asset Hub XCM channel registry; cross-reference top-100 DOT balances per parachain against the AssetHub top-1000 to identify cross-parachain Foundation positions.

---

## §3.8 PCA typology, Substrate-native extensions

The Phase 4 cycle 1 + DOT addendum jointly establish the Substrate-native PCA typology extensions:

| Class | Substrate-native extension | Phase 4 anchor |
|---|---|---|
| Class 1 (burns) | Substrate has no native burn convention (slashed funds route to Treasury) | DOT |
| Class 2 (Foundation/treasury) | Substrate runtime pallets via `modlpy/*` display pattern (Treasury + Bounty pallets + XCM channels) | DOT (5 accounts); TAO Bittensor Foundation candidate (pending) |
| Class 3 (staking-aggregation) | Polkawatch operator_id cross-reference + multi-funder cluster identification | DOT (pos.dog + Novasama + 3 multi-funder clusters) |
| Class 4 (bridge custody) | XCM channel registry (cross-parachain bridge custody); deferred | DOT (out of scope this cycle) |
| Class 5 (CEX) | CEX cold wallet identification via Polkawatch + manual qualitative review | DOT top-1 candidate (unattributed; pending) |

Substrate-native Class 2 + Class 3 methodology now anchors the §3.8 typology cross-architecture coverage (EVM via Etherscan + Nansen; Solana via Helius DAS + Sim API; Substrate via Polkawatch operator-registry + `modlpy/*` display pattern matching). Cross-architecture coverage closes the §5.7 third-limitation gap (asymmetric attribution coverage across chain architectures) at the Substrate axis pending DOT top-1 attribution + Class 3 completeness refinement.

---

## Cross-references

- **S16b** (`S16_phase4_minibatch_2026-05-27.md`): Phase 4 cycle 1; FXS + SNX + GNO + TAO pre-exclusion baseline.
- **S18 + S18 audit addendum**: Phase 4 EVM mini-batch PCA classification + 2-layer audit (FXS + SNX + GNO post-exclusion HHI 0.032/0.017/0.042).
- **S19 cluster**: Polkadot validator-set 5-axis attribution methodology (Subscan Identity Pallet + Polkawatch DDP API + Web3 Foundation TVP + L2 funding-source + display-name; 53 percent attribution coverage at validator-set layer).
- **S20**: Polkadot Subscan refresh finding (Phase 4 methodology validation; sister to the AssetHub canonical-source supersession in this addendum).
- **Exhibits**: [`research_content/papers/B2_governance_concentration/exhibits/dot_holder_hhi/`](../exhibits/dot_holder_hhi/README.md) (README + CSVs + Subscan puller + refined PCA classifier).
- **B2 PAPER.md §3.8** (Five-class PCA typology; Substrate-native Class 2 + Class 3 extensions per this addendum).
- **B2 PAPER.md §4.3** (DePIN-vs-DeFi sector contrast; DOT joins low-concentration L1 cluster).
- **B2 PAPER.md §4.5.5** (Validator-set 5-axis attribution; sister axis distinct from holder-balance HHI reported here).
- **B2 PAPER.md §5.7 #2 + §5.8 #2** (Sample-expansion limitation + future-research; CLOSED by Phase 4 N=45 mini-batch).
- **B2 PAPER.md §5.7 #3** (Asymmetric attribution coverage across chain architectures; partially closed at Substrate axis by this addendum's `modlpy/*` + Polkawatch methodology).
- **`docs/ERROR_CORRECTION_LOG.md`** (canonical-source correction entry: Dune polkadot.balances stale-relay-chain-only vs AssetHub Polkadot Subscan post-Polkadot-1.0 canonical).
- **`docs/KNOWN_UNKNOWNS.md`** (3 gap entries: top-1 attribution; Class 3 completeness; cross-parachain DOT custody).

---

## Author note

DOT 5th mini-batch closure shipped with AssetHub Polkadot Subscan as canonical source for current DOT holder distribution (supersedes the cycle 1 Dune polkadot.balances stale-relay-chain capture). Phase 4 mini-batch N=45 holder-HHI sample target structurally MET; the cross-section now reports 45 protocols at the holder-balance HHI axis. Continuation-cycle work flagged for top-1 attribution resolution + Class 3 completeness refinement + cross-parachain DOT custody enumeration (3 entries in `docs/KNOWN_UNKNOWNS.md`).

Workflow clone `/Users/zach/Tokenization_Systems_Website` (designated workflow clone post-2026-04-26 partition per DEC-117); sibling replication clone `/Users/zach/Tokenomics-As-Institutional_Design` (mirror to be propagated via cross-clone supplement-sync cycle).
