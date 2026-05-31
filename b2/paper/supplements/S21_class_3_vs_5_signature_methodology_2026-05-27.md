# Supplementary File S21: Class 3 versus Class 5 PCA disambiguation via transaction-pattern signatures (deposit-collection vs batch-payout)

**Companion to:** B2 paper *Tokenomics as Applied Political Philosophy: Governance Concentration Beyond Token Allocation* §3.8 Generalizable Protocol-Controlled-Address (PCA) Exclusion Methodology (Five-class PCA typology); sister to S6 source-provenance + address-level PCA documentation; sister to S10 PCA classification robustness across Specs A through E; sister to S18 EVM mini-batch PCA classification two-layer audit addendum.

**Methodology origin:** the deposit-collection vs batch-payout signature distinction was derived during a Polkadot AssetHub holder-classification analysis that required disambiguating Class 3 (staking-aggregation) candidates from Class 5 (centralized-exchange custody) candidates at the transaction-pattern layer, where explicit entity attribution was unavailable. It generalizes to cross-protocol PCA classification that relies on transaction-pattern inspection.

---

## Purpose

Codify a generalizable transaction-pattern signature distinction for Class 3 (staking-aggregation contracts) versus Class 5 (centralized exchange custody) disambiguation in cross-protocol PCA classification. The distinction is methodology-of-record for any future PCA classification cycle on EVM, Solana, or Substrate-native protocols where address-level rationale relies on transaction-pattern inspection rather than explicit entity attribution via public name tags (Etherscan, Nansen) or operator registries (Polkawatch).

The distinction prevents two failure modes:

1. **False-positive Class 5 classification of legitimate Class 3 staking-aggregation addresses.** Distributed staking-rewards-distribution patterns can superficially resemble CEX hot-wallet activity (many small transfers); the deposit-collection vs batch-payout signature differentiates them at the directionality + turnover layer.
2. **False-negative Class 5 classification of CEX deposit-collection addresses that lack explicit entity attribution.** CEX hot wallets without Etherscan public name tags or Nansen entity labels (smaller exchanges, newer hot wallets, regional exchanges with limited indexing coverage) can be identified via the deposit-collection signature even absent explicit attribution.

---

## Signature definitions

### Class 5 deposit-collection signature

A Class 5 (centralized exchange custody) address exhibits the **deposit-collection signature** if all four of the following properties hold:

1. **Inbound concentration with diverse counterparties.** Many small inbound transfers from independent counterparty addresses; the inbound side aggregates customer deposit flows from many retail or institutional sources.
2. **Outbound consolidation to a single or small set of operational addresses.** Inbound deposits funnel to a single outbound consolidation address (typically the exchange's main treasury or cold storage), or to a small operational set (hot wallet rotation among 2-5 controlled addresses).
3. **Rapid turnover.** Mean holding duration of inbound deposits before outbound consolidation is short (typically minutes to hours; auto-rotation patterns of 5-minute intervals are diagnostic in Binance / Coinbase canonical patterns).
4. **Low-balance steady state.** The address operates near a working-capital floor; cumulative inflows substantially exceed steady-state balance because outbound consolidation regularly drains the address. Lifetime-cumulative-inflow to current-balance ratio commonly exceeds 10x.

### Class 3 batch-payout signature

A Class 3 (staking-aggregation contract) address exhibits the **batch-payout signature** if all four of the following properties hold:

1. **Inbound concentration from a single source.** Inbound transfers are dominated by a single protocol-controlled source (the staking-rewards distribution mechanism, typically a protocol pallet account or contract); inbound counterparty diversity is low.
2. **Outbound diversity to many recipient addresses.** Outbound transfers distribute to many independent recipient addresses (the underlying stakers receiving rewards); the outbound side is the dispersion mechanism.
3. **Slow rotation.** Mean holding duration of inbound rewards before outbound distribution is long (typically hours to days; batch-payout intervals are diagnostic of the protocol's reward-distribution cadence).
4. **High-balance steady state.** The address accumulates reward pools between distribution events; steady-state balance is non-trivial fraction of distributed cumulative rewards. Lifetime-cumulative-inflow to current-balance ratio is typically below 5x.

### Diagnostic decision matrix

| Property | Class 5 (deposit-collection) | Class 3 (batch-payout) |
|---|---|---|
| Inbound counterparties | Many independent | Single protocol source |
| Outbound counterparties | Single or small operational set | Many independent recipients |
| Mean holding duration | Short (minutes to hours) | Long (hours to days) |
| Steady-state balance | Low (working-capital floor) | High (reward-pool accumulation) |
| Lifetime-inflow to current-balance ratio | Greater than approximately 10x | Less than approximately 5x |
| Directionality | Convergent (many-to-one) | Divergent (one-to-many) |

### Ambiguous-case handling

When signature properties are partially consistent with both classes (e.g., inbound diversity but slow rotation), the address is classified as TENTATIVE pending: (a) cross-reference against public name tag registries (Etherscan, Nansen, Polkawatch); (b) protocol-specific staking-mechanism documentation review; (c) direct inspection of the protocol's canonical staking and treasury documentation.

---

## Worked examples from the Polkadot AssetHub classification

### LIKELY-CEX additions via deposit-collection signature (Scenario C-narrow)

Two AssetHub Polkadot Subscan top-20 non-PCA whale addresses surfaced for Class 5 promotion via deposit-collection signature:

**Rank-2 `13Z7KjGn...` (35,235,961 DOT pre-exclusion):** displays the four-property deposit-collection signature: (1) thousands of small inbound DOT transfers from diverse retail counterparties; (2) outbound consolidation to a small set of Binance operational addresses including the confirmed `13vg3M...` Binance hot wallet (per SubSquare hydration governance forum attribution); (3) rapid turnover with auto-rotation pattern matching Coinbase / Kraken / OKX / Bybit / KuCoin deposit-wallet operational cadence; (4) low-balance steady state relative to cumulative inflows. Promoted from TENTATIVE non-PCA to LIKELY-CEX Class 5.

**Rank-5 `12ouvKS...` (16,230,000 DOT pre-exclusion):** displays the same four-property pattern at smaller scale; deposit-collection cadence + outbound consolidation to identified Binance cluster addresses. Promoted from TENTATIVE non-PCA to LIKELY-CEX Class 5.

With these 2 LIKELY-CEX additions plus the 3 confirmed Binance Class 5 PCAs (cluster total 5 Class 5 addresses; cluster balance approximately 157.6M DOT), post-PCA-exclusion HHI shifts to Scenario C-narrow = 0.0043 (extends the sensitivity band beyond Scenario A baseline = 0.0093 and Scenario B = 0.0052).

### Staking-infrastructure preservation via batch-payout signature

Three AssetHub Polkadot Subscan top-20 non-PCA addresses initially flagged as potential CEX candidates (high lifetime transfer volume; many counterparties) were correctly preserved as legitimate Class 3 staking-infrastructure beneficiaries via batch-payout signature:

**Ranks 10/11/12 `163egH5d-...`-prefix cluster:** all three addresses display the four-property batch-payout signature: (1) inbound transfers concentrated from a single Polkadot Treasury or staking-rewards distribution source; (2) outbound transfers diverse to many recipient validator addresses or nominator pools; (3) slow rotation with cadence matching Polkadot's epoch-aligned staking-reward distribution; (4) high-balance steady state consistent with reward-pool accumulation between distribution events. Classification preserved as Class 3 staking-aggregation (or sister non-PCA pending Class 3 sub-class refinement); not promoted to Class 5.

This preservation prevented a false-positive Class 5 reclassification of approximately 30-50M DOT in legitimate staking infrastructure, which would have shifted post-PCA-exclusion HHI further downward (below Scenario C-narrow 0.0043) in error and overcounted the Class 5 exclusion magnitude.

---

## Cross-architecture application notes

The signature distinction is architecture-agnostic at the conceptual layer; the transaction-pattern properties (inbound/outbound directionality, turnover, steady-state balance) apply uniformly across EVM, Solana, and Substrate-native protocols. The empirical investigation methodology differs per chain:

### EVM (Ethereum and L2s; Polygon; Base)

- **Primary investigation tools:** Etherscan + Nansen Address Labels API (POST `/api/v1/profiler/address/labels`); Sim API EVM token-holders endpoint for cumulative holder distribution context.
- **Transaction-pattern data:** Etherscan transaction list + Nansen counterparty analysis + Dune `ethereum.transactions` table for bulk pattern extraction.
- **Anchor cases:** Phase 4 EVM mini-batch S18 audit cycle established 2-layer verification pattern (Etherscan public name tag + Nansen entity label); deposit-collection vs batch-payout signature complements that pattern at addresses lacking explicit entity attribution.
- **Class 3 EVM examples:** stkAAVE staking contract (canonical Class 3); Lido stETH staking; Rocket Pool minipools; Frax veFXS vote-escrow.
- **Class 5 EVM examples:** Binance 8 (canonical `0xf977...41acec`); Bithumb 162; Upbit 59; Crypto.com 22; Bitpanda 18; Bitvavo + Bitvavo Hot Wallet; Luno (5 new CEX hot wallets surfaced via Phase 4 EVM audit cycle).

### Solana (SVM)

- **Primary investigation tools:** Helius DAS API + Sim API SVM token-holders endpoint; Dune `cex_solana.addresses` spell for known CEX attribution (with partial-coverage caveat per DATA_REGISTRY 2026-04-30 entry).
- **Transaction-pattern data:** Helius Enhanced API transactions + Sim API per-address activity profiles + Solscan token-account-level history.
- **Anchor cases:** S13 Solana PCA audit cycle established Sim API verification pattern (6 of 7 cross-protocol candidates classified Class 5 CEX); signature distinction complements that pattern at addresses without entity attribution.
- **Class 3 Solana examples:** Solana SPL stake-pool accounts (Marinade msol; Jito jitoSOL; Lido stSOL).
- **Class 5 Solana examples:** Binance Solana hot wallets; Kraken Solana deposit-collection; OKX Solana operational addresses.
- **Caveat:** `cex_solana.addresses` spell has documented partial coverage for major Asian centralized exchanges (KuCoin, Bitget, Bybit, Kraken, Bitfinex; per 2026-04-30 cross-check); deposit-collection signature is the recovery methodology for addresses missed by the spell.

### Substrate-native (Polkadot AssetHub; Bittensor; Kusama; other parachains)

- **Primary investigation tools:** AssetHub Polkadot Subscan API (`assethub-polkadot.api.subscan.io`); TAOSTATS API for Bittensor; Polkawatch operator_id registry for Polkadot validator-set attribution; SubSquare governance forum for ground-truth attribution.
- **Transaction-pattern data:** Subscan extrinsic-level inspection (`balances.transfer` + `balances.transfer_keep_alive` + `staking.payout_stakers`); Polkawatch operator-level activity profiles.
- **Anchor cases:** Phase 4 DOT 5th-protocol Phase 4 cycle established the worked-example pattern (this supplement); the signature distinction was empirically derived from this cycle's top-20 non-PCA whale investigation.
- **Class 3 Substrate examples:** Polkawatch operator_id institutional staking providers (pos.dog 38 validators; Novasama 4 validators; per S16c DOT addendum); multi-funder cluster patterns (45 addresses funding 2 or more validators).
- **Class 5 Substrate examples:** Binance cluster on AssetHub (3 addresses: `16ZL8y...` cold storage + `13vg3M...` hot wallet + `12YfMj...` staking position; SubSquare-attributed); LIKELY-CEX deposit-collection candidates (`13Z7KjGn...` + `12ouvKS...`).

---

## Cross-references

- **B2 PAPER.md §3.8** (Generalizable PCA Exclusion Methodology; this supplement extends Class 3 vs Class 5 disambiguation at the transaction-pattern signature layer).
- **B2 PAPER.md §3.5** (Outcome variables and HHI computation; the signature distinction operates on post-exclusion HHI computation).
- **B2 PAPER.md §4.5.5** (Cross-protocol concentration patterns; deposit-collection signature aids cross-protocol CEX-overlap identification at the structural concentration mechanism layer).
- **B2 PAPER.md §5.7 third limitation** (Asymmetric attribution coverage across chain architectures; signature distinction is the recovery methodology when entity attribution is unavailable at lower attribution-coverage chains).
- **S6** (Source-provenance + address-level PCA documentation; canonical exclusions log).
- **S10** (PCA classification robustness across Specs A through E; Spec D explicitly tests CEX-only exclusion sensitivity; the signature distinction strengthens Spec D classification accuracy).
- **S13 + S13 addendum** (Solana PCA audit cycle; Sim API verification methodology; sister pattern at the Solana axis).
- **S16b + S16c** (Phase 4 sample expansion; DOT 5th-protocol AssetHub Subscan canonical capture where signature distinction was empirically derived).
- **S18 + S18 audit addendum** (Phase 4 EVM mini-batch PCA classification; two-layer Etherscan + Nansen verification; sister pattern at the EVM axis).
- **S19 cluster** (Polkadot validator-set 5-axis attribution methodology; complementary to deposit-collection vs batch-payout at the validator-set rather than holder-balance layer).

---

## Author note

The deposit-collection vs batch-payout signature distinction emerged from the Phase 4 DOT 5th-protocol cycle's need to disambiguate the AssetHub Polkadot Subscan top-20 non-PCA whales beyond the 10 PCAs already classified via Polkawatch operator_id registry + `modlpy/*` Treasury pallet pattern matching. The parallel investigation surfaced the rank-2 and rank-5 LIKELY-CEX deposit-collection signatures alongside the ranks-10/11/12 staking-infrastructure batch-payout signatures, codifying the distinction at the point of empirical derivation. This supplement formalizes the distinction as methodology of record for cross-protocol PCA classification.

