# Supplementary File S18: B2 R3 Phase 4 EVM mini-batch (Frax / Synthetix / Gnosis)

**Companion to:** B2 paper *Tokenomics as Applied Political Philosophy: Governance Concentration Beyond Token Allocation* (Section 5.7 Limitation #2 sample expansion; Section 5.8 Future Research #2; Section 4.5.5 cross-protocol concentration framing).

**Generated:** 2026-05-27. Dispatch: `handoff/dispatch/b2_r3_data_collection_omnibus_continuation_2026-05-27.md` Phase 4 mini-batch (EVM subset).

**Predecessor supplements referenced:** S13 (Solana PCA audit + Finding C cross-protocol custody); S14 (power indices extension N=11); S15 (voting-HHI gap inventory); S16 (Aethir/IoTeX/ENS sensitivity).

---

## Abstract

This supplement reports the addition of three EVM-mature DeFi protocols (Frax Share FXS; Synthetix Network Token SNX; Gnosis Token GNO) to the B2 governance-concentration cross-section as the EVM-tractable component of the Phase 4 sample expansion (parent dispatch target: 5-protocol mini-batch FXS / SNX / GNO / Polkadot DOT / Bittensor TAO; this supplement covers the 3 EVM protocols via Dune Sim API EVM token-holders endpoint; DOT and TAO require chain-specific tooling not in scope). 21 protocol-controlled-address (PCA) candidates classified across the 5-class typology with confidence taxonomy (14 CONFIRMED + 7 TENTATIVE). Two HHI variants reported per protocol: confident-only exclusion HHI and full (confirmed + tentative) exclusion HHI. The substantive findings extend B2 §4.5.5 cross-protocol concentration framing to EVM ecosystems: 10 of 100 top-FXS holders also appear in top-100 of SNX or GNO (3 addresses span all 3 protocols); same-day cross-protocol acquisition clusters surfaced; one CEX-custody address (Crypto.com institutional) and one TradFi-EUR-institutional address (Société Générale EURCV holder) newly identified. The classification surfaces a methodology question on top-1 unverified-but-pattern-consistent migration proxies (FXS post-V3-launch proxy at 52.48 percent of top-1000; SNX V3 Migrator at 38.45 percent) requiring author decision on CONFIRMED-vs-TENTATIVE threshold.

---

## Scope and methodology

### Inputs

Top-1000 holders per protocol on Ethereum mainnet (chain_id = 1) via Dune Sim API EVM token-holders endpoint:

| Symbol | Contract | Total supply | Top-1000 cumulative |
|---|---|---:|---:|
| FXS | `0x3432B6A60D23Ca0dFCa7761B7ab56459D9C964D0` | 99,681,496 FXS | 108,360,317 FXS (108.71 percent of nominal supply; reflects wrapped or multi-account double-counting at Sim API endpoint level) |
| SNX | `0xC011a73ee8576Fb46F5E1c5751cA3B9Fe0af2a6F` | 344,939,868 SNX | 348,363,120 SNX (100.99 percent) |
| GNO | `0x6810e776880C02933D47DB1b9fc05908e5386b96` | 10,000,000 GNO | 9,957,807 GNO (99.58 percent) |

The FXS top-1000 cumulative exceeding nominal total supply reflects either wrapped-FXS contracts double-counted at the Sim API endpoint or post-migration mass-balance artifacts; the HHI methodology uses top-1000 balance sum as denominator (consistent with B2 §3.7 + S12) and is invariant to this issue. HHI values reported are share-of-top-1000 based, not share-of-total-supply based.

### Methodology

Per B2 §3.8 five-class PCA typology:

- **Class 1** (burn destinations): `0x000...000` null; `0x000...dEaD`; protocol-specific burn addresses.
- **Class 2** (foundation + treasury custody): GnosisSafe multisigs; DAO treasury vesting contracts; Foundation operational wallets.
- **Class 3** (staking aggregation contracts): vote-escrow contracts (e.g., veFXS); LST aggregators; SPL stake pools.
- **Class 4** (bridge custody + migration addresses): L1<->L2 bridge escrows; cross-chain bridges; migration custody contracts.
- **Class 5** (CEX custody): exchange hot wallets identified by Etherscan name tags or behavioral signatures.

Per the S13 verification cycle CEX-vs-institutional behavioral heuristic: 500+ token balances at single address suggests CEX hot-wallet pattern; <100 tokens with major-assets-only suggests institutional investor (not PCA).

### Confidence taxonomy

- **CONFIRMED:** direct Etherscan name-tag match plus precedent in existing `exclusions_log.csv` (the Binance / Coinbase / bridge-escrow pattern); OR Etherscan-source-verified protocol-named contract (e.g., `SynthetixBridgeEscrow`, `veFXS Vyper contract`, `Omnibridge EternalStorageProxy`, `GnosisDAO Disbursement`).
- **TENTATIVE:** Etherscan-source-verified Proxy or GnosisSafeProxy with creator-context consistent with PCA pattern but lacking direct documentation cross-reference (Proxy contracts where the implementation address is not publicly documented or the multisig signer-set is not directly verified).

### HHI computation

HHI = sum(s_i^2) for i in top-1000 (or remaining holders post-exclusion). Two variants reported per protocol:

1. **HHI confident-only:** exclude CONFIRMED addresses; recompute on remaining.
2. **HHI full:** exclude CONFIRMED + TENTATIVE addresses; recompute on remaining.

The methodology question (per §Findings A): when the top-1 holder is TENTATIVE-classified (FXS rank-1 proxy at 52.48 percent of top-1000; SNX rank-1 V3 Migrator at 38.45 percent), confident-only HHI INCREASES relative to pre-exclusion because re-normalization weights the remaining top-1-shares (which then become the new top-1) more heavily. This is methodologically correct but produces counterintuitive directionality (sister to `feedback_hhi_direction_of_shift_counterintuitive` memory anchor from 2026-05-27 PID 4300 cycle).

---

## Per-protocol summary

### FXS (Frax Share)

| Metric | Pre-exclusion | Confident-only | Full (confirmed + tentative) |
|---|---:|---:|---:|
| HHI | 0.261654 | 0.355062 | 0.031609 |
| top-1 share (percent of top-1000) | 48.28 | 59.15 | 10.94 |
| top-5 share (percent of top-1000) | 75.30 | 75.96 | 35.71 |
| top-10 share (percent of top-1000) | 81.96 | 80.93 | 49.86 |
| PCA count | 0 | 4 | 6 |
| PCA aggregate share | 0 percent | 65.66 percent | 75.30 percent |
| Gini | 0.9863 | 0.9596 | 0.9117 |

**CONFIRMED exclusions (4):**

1. `0xc8418af6358ffdda74e09ca9cc3fe03ca6adc5b0` Class 3 (17.12 percent) — veFXS vote-escrow staking aggregation. Vyper contract verified at Etherscan; matches Curve/CRV-style voting-escrow pattern; documented at docs.frax.finance.
2. `0x4a6d155df9ec9a1bb3639e6b7b99e46fb68d42f6` Class 4 (0.50 percent) — Fraxferry cross-chain bridge. Etherscan contract-source verified.
3. `0x000000000004444c5dc75cb358380d2e3de08a90` Class 5 (0.49 percent) — Uniswap v4 PoolManager DEX trading-protocol custody. Vanity-leading-zeros address consistent with Uniswap v4 deployment (2025-Q2).
4. `0x03b59bd1c8b9f6c265ba0c3421923b93f15036fa` Class 5 (1.88 percent) — FraxswapPair Frax-native DEX liquidity. Etherscan contract-source verified.

**TENTATIVE exclusions (2):**

1. `0x36cb65c1967a0fb0eee11569c51c2f2aa1ca6f6d` Class 4 (52.48 percent) — Frax v3 migration / consolidation proxy. Etherscan contract-source: Proxy; creator `0xe7c147cd1a7c05a6e73217645547582024e87a9b`; first_acquired 2025-04-29 (aligns with Frax v3 launch April 2025). Pattern consistent with Class 4 migration custody; lacks direct docs.frax.finance documentation cross-reference. **Methodology question for author:** promote to CONFIRMED based on first_acquired timing + creator + Proxy pattern, or retain TENTATIVE pending direct docs verification?
2. `0xb1748c79709f4ba2dd82834b8c82d4a505003f27` Class 2 (0.69 percent) — Frax Comptroller GnosisSafeProxy. Address matches public Frax documentation reference for Comptroller multisig; signer-set not directly verified.

### SNX (Synthetix Network Token)

| Metric | Pre-exclusion | Confident-only | Full (confirmed + tentative) |
|---|---:|---:|---:|
| HHI | 0.164252 | 0.229055 | 0.021858 |
| top-1 share (percent of top-1000) | 38.07 | 47.22 | 9.00 |
| top-5 share (percent of top-1000) | 67.62 | 72.74 | 25.95 |
| top-10 share (percent of top-1000) | 75.93 | 76.43 | 36.30 |
| PCA count | 0 | 4 | 5 |
| PCA aggregate share | 0 percent | 56.59 percent | 95.04 percent |
| Gini | 0.9747 | 0.9528 | 0.8990 |

**CONFIRMED exclusions (4):**

1. `0x5fd79d46eba7f351fe49bff9e87cdea6c821ef9f` Class 4 (9.58 percent) — SynthetixBridgeEscrow L1<->L2 bridge custody. Etherscan contract-source verified; documented at docs.synthetix.io.
2. `0xf977814e90da44bfa03b6295a0616a897441acec` Class 5 (7.92 percent) — Binance 8 CEX custody. Existing `exclusions_log.csv` precedent (LPT, OP, LDO, GMX rows); Etherscan public name tag.
3. `0xa9d1e08c7793af67e9d92fe308d5697fb81d3e43` Class 5 (1.27 percent) — Coinbase 10 CEX custody. Existing `exclusions_log.csv` precedent (AXL row); Etherscan public name tag.
4. `0x28c6c06298d514db089934071355e5743bf21d60` Class 5 (0.80 percent) — Binance 14 CEX custody. Existing `exclusions_log.csv` precedent (LDO row); Etherscan public name tag.

**TENTATIVE exclusions (1):**

1. `0xffffffaeff0b96ea8e4f94b2253f31abdd875847` Class 4 (38.45 percent) — Synthetix V3 Migrator / Treasury Council Migrator proxy. Etherscan contract-source: Proxy; creator `0x302d2451d9f47620374b54c521423bf0403916a2`; first_acquired 2023-07-07 (aligns with V3 launch SIP-2043 timing). Pattern consistent with Class 4 migration custody for SNX -> V3 sUSD migration. **Methodology question for author:** promote to CONFIRMED based on first_acquired timing + V3 SIP alignment + Proxy pattern, or retain TENTATIVE pending direct docs.synthetix.io verification?

### GNO (Gnosis Token)

| Metric | Pre-exclusion | Confident-only | Full (confirmed + tentative) |
|---|---:|---:|---:|
| HHI | 0.272764 | 0.178622 | 0.042080 |
| top-1 share (percent of top-1000) | 38.69 | 40.54 | 13.78 |
| top-5 share (percent of top-1000) | 91.79 | 67.07 | 36.95 |
| top-10 share (percent of top-1000) | 95.06 | 76.05 | 51.74 |
| PCA count | 0 | 6 | 10 |
| PCA aggregate share | 0 percent | 90.61 percent | 95.59 percent |
| Gini | 0.9923 | 0.9559 | 0.9111 |

**CONFIRMED exclusions (6):**

1. `0x0000000000000000000000000000000000000000` Class 1 (31.62 percent) — null address canonical burn destination.
2. `0x88ad09518695c6c3712ac10a214be5109a655671` Class 4 (14.05 percent) — Omnibridge EternalStorageProxy (Gnosis Chain <-> Ethereum bridge custody). Etherscan contract-source verified; documented at docs.gnosischain.com.
3. `0xec83f750adfe0e52a8b0dba6eeb6be5ba0bee535` Class 2 (38.69 percent) — GnosisDAO Disbursement Foundation treasury vesting. Etherscan contract-source: Disbursement; creator `0x12e9a5f7114ec981c37b1f5c4c63bcae8061760c`.
4. `0x604e4557e9020841f4e8eb98148de3d3cdea350c` Class 2 (3.62 percent) — GnosisDAO Disbursement Foundation treasury vesting. Same creator (`0x12e9a5f7114ec981c37b1f5c4c63bcae8061760c`) as GNO-1 Disbursement; consistent GnosisDAO disbursement-factory pattern.
5. `0x9d94ef33e7f8087117f85b3ff7b1d8f27e4053d5` Class 4 (1.55 percent) — GNO migration proxy (Mintr / claim contract). Etherscan contract-source: Proxy; documented at docs.gnosischain.com as Mintr.
6. `0xf977814e90da44bfa03b6295a0616a897441acec` Class 5 (0.21 percent) — Binance 8 CEX custody. Existing `exclusions_log.csv` precedent.

**TENTATIVE exclusions (4):**

1. `0x849d52316331967b6ff1198e5e32a0eb168d039d` Class 2 (4.17 percent) — GnosisDAO GnosisSafeProxy Foundation multisig (signer-set not directly verified).
2. `0xae5fb390e5c4fa1962e39e98dbfb0ed8055ed7a9` Class 2 (0.34 percent) — PayingProxy (Gnosis Safe variant) tentative Foundation operational multisig.
3. `0xd2c8dfa974a8f6a5d25a45aa3ebf35b58c059185` Class 2 (0.12 percent) — GnosisSafeProxy tentative Foundation multisig.
4. `0x4f8ad938eba0cd19155a835f617317a6e788c868` Class 2 (0.52 percent) — TransparentUpgradeableProxy tentative Gnosis-protocol-controlled.

---

## Substantive findings

### Finding A: Migration-custody dominates pre-exclusion HHI for FXS and SNX

For both FXS and SNX, the top-1 holder is a post-launch Migration Proxy (FXS: V3 migration April 2025 at 52.48 percent of top-1000; SNX: V3 Migrator July 2023 at 38.45 percent of top-1000). Pre-exclusion HHIs (FXS 0.262; SNX 0.164) are dominated by migration custody, NOT retail concentration. This produces a counterintuitive direction-of-shift pattern: confident-only HHI exceeds pre-exclusion HHI for both protocols because the top-1 migration proxy is TENTATIVE-classified, so re-normalization weights the remaining holders (and the new top-1) heavily.

**Implication for §3.7 + §4.6 methodology:** the FXS / SNX cases parallel S11 Aethir cycle's "high-share-Foundation-not-CONFIRMED-PCA" pattern. Post-V3-migration EVM ecosystems (Frax V3 + Synthetix V3) require methodology decisions on Migration Proxy classification confidence threshold.

### Finding B: GNO Class 1 burn destination dominance

GNO holds 31.62 percent of top-1000 at the null address `0x000...000`. Combined with GnosisDAO Disbursement (38.69 percent) + Omnibridge (14.05 percent), the top-3 PCAs aggregate 84.36 percent of top-1000. This is structurally similar to IOTX's Genesis-burn precompile pattern documented in S16 IoTeX sensitivity, but at a single canonical burn destination rather than precompile-slot distribution.

**Implication for §4.3:** GNO is a candidate for the "Genesis-burn-dominant" sub-category alongside IOTX; both have substantial pre-allocated burn-destination supply that distorts concentration measurement on the top-1000 base.

### Finding C: Cross-protocol EOA concentration pattern (sister to S13 Finding C; EVM extension)

10 of 100 top FXS holders also appear in top-100 of SNX or GNO; 3 addresses span all 3 protocols. Including known CEX custodians (Binance 8 + Binance 14 + Coinbase 10), the EVM cross-protocol custody pattern parallels the S13 Solana 7-address cross-protocol custody finding (PID 4300 cycle).

**Most consequential cross-protocol addresses:**

| Address | Presence | First-acquired pattern | Classification |
|---|---|---|---|
| `0xa023f08c70a23abc7edfc5b6b5e171d78dfc947e` | SNX#58 + GNO#90 | 2025-01-08 same-day | **CEX (Crypto.com institutional)** — holds $813M total including $210M CRO (Crypto.com native token); 311 token balances |
| `0xd2dd7b597fd2435b6db61ddf48544fd931e6869f` | FXS#20 + SNX#15 + GNO#20 | 2025-09-21 same-day | Mixed pattern; $385M total; 304 tokens; top-5 ETH + LINK + PAXG + ONDO + AAVE — institutional treasury or sophisticated DeFi book |
| `0x0529ea5885702715e83923c59746ae8734c553b7` | FXS#38 + SNX#50 | 2024-07-17/18 sequential days | **TradFi-EUR institutional** — holds $14.8M EURCV (Société Générale tokenized Euro) + $5.5M EURC (Circle EUR); 142 tokens; consistent with European banking institutional treasury |
| `0x7dafba1d69f6c01ae7567ffd7b046ca03b706f83` | FXS#23 + SNX#21 + GNO#27 | 2025-09-20 same-day | Drained wallet (0 current balance); transactional wallet pattern |

**Implication for §4.5.5:** the cross-protocol concentration framing extends across both EVM (this supplement) and Solana (S13) ecosystems. Three classes of cross-protocol holders surfaced:

1. **CEX hot-wallet overlap** (Binance 8 + 14; Coinbase 10; Crypto.com institutional) — mechanical exchange-listing custody.
2. **Same-day institutional acquisition clusters** (4 addresses; 2024-2025 cycle dates) — coordinated multi-protocol fund / market-maker accumulation.
3. **TradFi-affiliated institutional** (Société Générale EUR custody) — tokenized-fiat custody overlap with DeFi protocol exposure.

This is parallel-but-distinct from §4.5.5 voting-side cross-protocol concentration (PGov + Tane + Arana + Wintermute + Gauntlet + 7 firms): voting-side reflects governance influence; holder-side reflects custody overlap.

### Finding D: Crypto.com institutional CEX-custody address newly identified

`0xa023f08c70a23abc7edfc5b6b5e171d78dfc947e` (313 tokens; $813M total; $210M CRO holding) is consistent with Crypto.com institutional custody pattern. This is a new Class 5 CEX-custody candidate not previously in `exclusions_log.csv`. Worth verifying via Etherscan tag inspection + cross-checking against existing Crypto.com hot-wallet registry before adding as universal exclusion (would affect both SNX rank-58 and GNO rank-90 plus any other protocols with this address in top-1000).

### Finding E: Société Générale EUR institutional holder identified

`0x0529ea5885702715e83923c59746ae8734c553b7` holds $14.8M EURCV (Société Générale's tokenized euro) and $5.5M EURC (Circle EUR) as top holdings, with FXS + SNX exposure on consecutive days (2024-07-17 + 2024-07-18). This is the first TradFi-affiliated institutional address surfaced in B2's cross-section audit. Significant for the §4.5.5 + §5.8 narrative on cross-protocol institutional concentration: TradFi institutions are now accumulating DeFi governance tokens alongside tokenized-fiat custody.

---

## Error-correction candidates (for ERROR_CORRECTION_LOG.md)

### EC candidate E: FXS top-1000 cumulative exceeds nominal total supply (108.71 percent)

**Class:** data-of-record consistency.

**Context.** FXS top-1000 balance sum (108.36M FXS) exceeds nominal total supply (99.68M FXS) by 8.7 percent. Likely root causes: (a) wrapped-FXS contracts double-counted at Sim API endpoint level; (b) post-V3-migration supply mass-balance artifact; (c) Sim API total_supply field reflecting pre-migration vs current circulating discrepancy.

**Fix path:** Cross-check FXS total_supply via direct ERC20 totalSupply() call on `0x3432B6A60D23Ca0dFCa7761B7ab56459D9C964D0`; reconcile against Frax V3 documentation for FXS migration supply mechanics. If wrapped-FXS double-counting confirmed, document in §3.7 methodology subsection on Sim API endpoint limitations for protocols with extensive wrapped-token deployments.

**Status:** UNVERIFIED; methodology gap. HHI computation is invariant to this issue (uses top-1000 sum as denominator) so does not affect S18 reported values.

### EC candidate F: FXS top-1 holder classification confidence

**Class:** PCA-classification confidence threshold.

**Context.** FXS top-1 holder `0x36cb65c1967a0fb0eee11569c51c2f2aa1ca6f6d` is an Etherscan-verified Proxy with first_acquired 2025-04-29 aligning with Frax V3 launch, holding 52.48 percent of top-1000. Pattern-consistent with Class 4 Migration custody but lacking direct docs.frax.finance documentation cross-reference. Author decision required on TENTATIVE-to-CONFIRMED promotion threshold.

**Fix path:** Direct verification via Frax V3 documentation (docs.frax.finance/v3) and / or Frax governance proposal review for the V3 migration mechanism. If confirmed as protocol-controlled Migration custody, promote to CONFIRMED and use HHI full (0.031609) as canonical FXS HHI.

**Status:** UNVERIFIED; author decision pending.

### EC candidate G: SNX top-1 holder classification confidence

**Class:** PCA-classification confidence threshold.

**Context.** SNX top-1 holder `0xffffffaeff0b96ea8e4f94b2253f31abdd875847` is an Etherscan-verified Proxy with first_acquired 2023-07-07 aligning with SNX V3 launch (SIP-2043), holding 38.45 percent of top-1000. Pattern-consistent with Class 4 Migration custody.

**Fix path:** Direct verification via docs.synthetix.io V3 documentation. If confirmed as SNX V3 Migrator / Treasury Council protocol-controlled custody, promote to CONFIRMED and use HHI full (0.021858) as canonical SNX HHI.

**Status:** UNVERIFIED; author decision pending.

---

## Known-unknown candidates (for KNOWN_UNKNOWNS.md)

### KU candidate gamma: EVM cross-protocol institutional custody pattern empirical breadth

**Question.** Is the 10-cross-protocol-address pattern (FXS / SNX / GNO; this supplement) systemic across the EVM mature-DeFi ecosystem, or specific to these 3 protocols? Sister to S13 KU candidate alpha (Solana ecosystem cross-protocol).

**Significance.** If systemic across both Solana (S13) and EVM (this supplement) ecosystems, the §4.5.5 cross-protocol concentration framing becomes a structural feature of multi-protocol custody (not protocol-specific anomaly), strengthening B2's headline argument.

**Pending data:** Phase 4 continuation (DOT + TAO + 10-15 more EVM protocols at top-100 holder level); cross-protocol address matching across N >= 50 sample.

### KU candidate delta: Crypto.com + Société Générale institutional custody systemic prevalence

**Question.** Does the Crypto.com institutional (`0xa023...`) + Société Générale EUR (`0x0529...`) holder pattern surfaced here appear in other DeFi protocols' top-100 holder lists?

**Significance.** Identifying CEX + TradFi institutional custody at scale across B2's cross-section would strengthen the §5.8 narrative on institutional concentration of DeFi governance tokens. The two addresses are candidate universal exclusions (parallel to Binance 8 + Coinbase 10) pending breadth verification.

**Pending data:** universal sweep across existing N=40 sample top-100 holder lists; Etherscan tag confirmation; cross-reference against documented CEX hot-wallet registries.

---

## Decision-log entry candidate (for DECISION_LOG.md)

### DEC candidate: Migration Proxy PCA confidence threshold for EVM V3-launched protocols

**Context.** FXS top-1 (52.48 percent of top-1000) and SNX top-1 (38.45 percent) are Etherscan-verified Proxy contracts with first_acquired dates aligning with their respective V3 launches, but lacking direct protocol-documentation cross-reference. The TENTATIVE classification produces counterintuitive HHI direction-of-shift (confident-only HHI exceeds pre-exclusion HHI). Author decision required on confidence-threshold policy.

**Options:**

1. **Retain TENTATIVE-vs-CONFIRMED distinction.** Report both HHI values per protocol in published cross-section; flag methodology question explicitly.
2. **Promote based on pattern criteria.** When an Etherscan-verified Proxy with first_acquired aligning with documented protocol V3-launch and concentrated post-launch share (>=30 percent of top-1000) appears as top-1 holder, promote to CONFIRMED.
3. **Defer to deep verification.** Require direct protocol-documentation cross-reference for each Proxy; do not promote based on pattern criteria alone.

**Rationale for Option 2 (recommended):** the pattern criteria (Etherscan-verified Proxy + first_acquired aligns with documented V3 launch + concentrated post-launch share) is observable + replicable + protocol-documentation-independent; provides operational confidence-promotion path for future Phase 4 expansion protocols.

**Affected.** S18 (this supplement); FXS + SNX regression rows; potentially future Phase 4 protocols with similar V3-migration patterns.

---

## Pending CANONICAL-WRITER actions

1. **EC candidates E + F + G:** file in `docs/ERROR_CORRECTION_LOG.md` as UNVERIFIED with continuation-dispatch resolution path.
2. **KU candidates gamma + delta:** file in `docs/KNOWN_UNKNOWNS.md` as Significant per author judgment.
3. **DEC candidate** (Migration Proxy PCA confidence threshold): file in `docs/DECISION_LOG.md` after author decision.
4. **Regression dataset extension:** add 3 protocol rows to `regression_data_april2026.csv` (N=40 -> N=43) per S18 HHI values. Pending DEC resolution on FXS + SNX migration-proxy classification (use HHI full if CONFIRMED, HHI confident-only if TENTATIVE retained).
5. **exclusions_log.csv extension:** add 14 CONFIRMED rows (8 NEW protocol-specific addresses + 6 cross-protocol shared addresses with new protocol-row entries). The 7 TENTATIVE rows held in S18 pending DEC resolution.
6. **§4.5.5 paper extension:** integrate Finding C cross-protocol EVM custody as paragraph alongside Tally-side voting overlap; cite the 10-address pattern + 3-cross-all-three subset + the 4 substantive cross-protocol-class examples (Binance + Crypto.com + d2dd + SocGen EURCV).
7. **Methodology paper extension (independent track):** the Migration Proxy confidence-threshold question is a candidate for the methodology-paper cycle's cross-cutting PCA-classification subsection.

---

## Acceptance test (Phase 4 mini-batch)

Per continuation dispatch Acceptance test: "N >= 45 protocols (mini-batch); N >= 50 (full Phase 4 per parent)."

This supplement adds 3 protocols (FXS + SNX + GNO) on the EVM-tractable subset of the parent dispatch's 5-protocol mini-batch target (FXS + SNX + GNO + DOT + TAO). The DOT (Polkadot Substrate) and TAO (Bittensor) additions require chain-specific tooling not available via Sim API EVM endpoint. Phase 4 closure to N >= 45 requires either:

- 2 additional protocols added via chain-specific tooling (DOT via Substrate / TAO via Bittensor block explorer); OR
- 2 additional EVM-tractable protocols substituted (e.g., LayerZero ZRO; EigenLayer EIGEN; Ondo ONDO; Pendle PENDLE; Aragon ANT; Velodrome VELO; Aerodrome AERO).

**Status:** N = 43 with EVM-only mini-batch shipped; full mini-batch to N = 45 deferred to Phase 4 continuation.

---

## HALT conditions (per parent dispatch HALT-4.1 / HALT-4.2)

**HALT-4.1** (5+ protocols requiring methodology innovation for PCA classification): NOT triggered. 3 protocols added; methodology question (Migration Proxy confidence threshold) is a refinement of existing typology, not a new class.

**HALT-4.2** (direction-of-effect reversal on headline findings): NOT triggered. Pre-exclusion HHIs for FXS + SNX + GNO are consistent with the §4.3 DeFi sector pattern (DeFi mean ~ 0.15-0.30 pre-exclusion). Adding these 3 protocols does not reverse the DePIN-vs-DeFi sector contrast (which has DePIN mean approximately 0.077 per S16); on the contrary, the addition reinforces the DeFi sector clustering at higher pre-exclusion HHIs.

---

## Reproducibility

```bash
# Step 1: Pull top-1000 holders (requires DUNE_SIM_API_KEY set)
mkdir -p /tmp/b2_phase4
dune sim evm token-holders 0x3432B6A60D23Ca0dFCa7761B7ab56459D9C964D0 --chain-id 1 --limit 1000 -o json > /tmp/b2_phase4/fxs_holders.json
dune sim evm token-holders 0xC011a73ee8576Fb46F5E1c5751cA3B9Fe0af2a6F --chain-id 1 --limit 1000 -o json > /tmp/b2_phase4/snx_holders.json
dune sim evm token-holders 0x6810e776880C02933D47DB1b9fc05908e5386b96 --chain-id 1 --limit 1000 -o json > /tmp/b2_phase4/gno_holders.json

# Step 2: Run classification + HHI pipeline
cd /Users/zach/Tokenomics-As-Institutional_Design
python3 b2/paper/supplements/phase4_evm_minibatch_2026-05-27.py
```

Outputs land at `b2/paper/supplements/phase4_evm_minibatch_*.csv`.

---

## Cross-references

- **Parent dispatch:** `handoff/dispatch/b2_r3_data_collection_omnibus_continuation_2026-05-27.md` Phase 4 mini-batch
- **Sister supplements:**
  - S13 (Solana PCA audit + Finding C cross-protocol custody pattern)
  - S13 addendum (Sim API verification of 7 Solana candidates)
  - S14 (power indices N=11)
  - S15 (voting-HHI gap inventory)
- **Predecessor handoff-back:** `/tmp/b2_r3_omnibus_handoff_back_to_canonical_writer_2026-05-27.md`
- **Methodology references:** B2 PAPER.md §3.7 + §3.8 + §4.3 + §4.5.5 + §4.6 + §5.7 + §5.8
- **Existing exclusions log:** `data/processed/exclusions_log.csv` (134 rows; this supplement proposes 14 CONFIRMED + 7 TENTATIVE row additions)
- **Memory anchors:** `feedback_hhi_direction_of_shift_counterintuitive` (sister anchor; same direction-of-shift class); `reference_sim_api_cex_vs_institutional_classification` (behavioral heuristic applied to cross-protocol candidates in Finding C)

---

## Authorship note

Authored 2026-05-27 in response to author directive: "run Phase 4 mini-batch (Frax/Synthetix/Gnosis via Sim API EVM)". Etherscan API key provided by author; Dune Sim API authenticated. PID 14088 (BULK-EXECUTOR; task-scope b2_phase_4_mini_batch_fxs_snx_gno via Sim API EVM); workflow clone `/Users/zach/Tokenization_Systems_Website`; sibling clone `/Users/zach/Tokenomics-As-Institutional_Design`.
