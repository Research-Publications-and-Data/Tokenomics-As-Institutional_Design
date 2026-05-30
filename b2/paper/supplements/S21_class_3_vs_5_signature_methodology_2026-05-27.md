# Supplementary File S21: Class 3 versus Class 5 Disambiguation via Transaction-Pattern Signatures

## Purpose

The five-class protocol-controlled-address (PCA) typology in Section 3.8 distinguishes Class 3 (staking-aggregation contracts) from Class 5 (centralized-exchange custody). Both classes share a surface-level behavioral signal of many small transfers, which makes them difficult to separate whenever explicit entity attribution (Etherscan public name tags, the Nansen Address Labels API, the Polkawatch operator registry) is unavailable. This supplement specifies a transaction-pattern signature that recovers the distinction from on-chain behavior alone. It is the recovery layer for the lower-attribution-coverage chains noted in the Section 5.7 attribution-coverage limitation. The disambiguation is consequential for the concentration measure: misclassifying a Class 3 staking-aggregation address as Class 5 (or the reverse) changes whether the address is excluded, and therefore the post-exclusion HHI.

## The two signatures

The two classes separate on four transaction-pattern properties: flow directionality, rotation cadence, balance steady state, and the ratio of lifetime cumulative inflow to current balance.

### Class 5: the deposit-collection signature (centralized-exchange custody)

1. **Directionality.** Many small inbound transfers from independent, unrelated counterparty addresses, funneling to a single outbound consolidation. The flow is convergent: many senders, one collector.
2. **Rotation cadence.** Rapid turnover, minutes to hours, frequently on an automated rotation schedule. The canonical Binance and Coinbase hot-wallet rotation patterns are diagnostic.
3. **Balance steady state.** Low, because balances are swept to cold storage or to the next address in the rotation shortly after arrival.
4. **Inflow-to-balance ratio.** Lifetime cumulative inflow to current balance commonly exceeds 10x, reflecting high throughput against a low standing balance.

### Class 3: the batch-payout signature (staking-aggregation contract)

1. **Directionality.** Many small outbound transfers from a single protocol-controlled inbound source, the staking-rewards distribution mechanism. The flow is divergent: one distributor, many recipients. This is the opposite of the Class 5 pattern.
2. **Rotation cadence.** Slow, matching the protocol's reward-distribution cadence (per-epoch, per-era, or per-period).
3. **Balance steady state.** High, because reward pools accumulate between distribution events.
4. **Inflow-to-balance ratio.** Lifetime cumulative inflow to current balance typically falls below 5x, reflecting accumulation rather than throughput.

## Diagnostic decision matrix

| Property | Class 5 (CEX custody) | Class 3 (staking aggregation) |
|---|---|---|
| Flow directionality | convergent (many senders to one collector) | divergent (one distributor to many recipients) |
| Rotation cadence | rapid (minutes to hours; auto-rotation) | slow (reward-distribution cadence) |
| Balance steady state | low (swept) | high (accumulating pool) |
| Lifetime-inflow to current-balance | commonly above 10x | typically below 5x |

A candidate address is classified Class 5 when the convergent-flow, rapid-rotation, low-balance, high-ratio pattern holds, and Class 3 when the divergent-flow, slow-rotation, high-balance, low-ratio pattern holds. The four properties are mutually reinforcing. Flow directionality and the inflow-to-balance ratio are the most diagnostic; rotation cadence and balance steady state serve as confirming evidence.

## Cross-architecture application

The signature is architecture-agnostic. It operates on flow structure rather than on chain-specific address formats, and applies uniformly across the three architectures in the cross-section.

- **EVM.** Class 3 staking-aggregation contracts include stkAAVE, Lido stETH, and Rocket Pool minipool contracts; Class 5 hot wallets follow the Binance and Coinbase rotation patterns.
- **Solana.** SPL stake-pool accounts (Marinade msol, Jito jitoSOL) exhibit the batch-payout signature; centralized-exchange deposit addresses exhibit the deposit-collection signature. Supplementary File S13 applies the Class 5 deposit-collection signature to the Solana cross-section.
- **Substrate.** Polkawatch-attributed institutional staking-provider accounts and protocol-pallet reward distributions exhibit the batch-payout signature; centralized-exchange deposit accounts on AssetHub Polkadot exhibit the deposit-collection signature.

## Worked examples: the Polkadot cycle

The Polkadot cycle established the canonical worked examples on AssetHub Polkadot, where the Polkawatch operator registry did not cover the relevant accounts and the transaction-pattern signature was the only available basis for classification.

- **Reclassified to Class 5, excluded.** The rank-2 holder (`13Z7KjGn...`) and the rank-5 holder (`12ouvKS...`) were classified as likely centralized-exchange custody via the deposit-collection signature. Excluding them yields a post-exclusion HHI of 0.0043 (the narrow Scenario C disposition).
- **Preserved as Class 3, retained.** The ranks 10, 11, and 12 holders (`163egH5d...` and the adjacent distributed staking-infrastructure beneficiaries) were preserved as legitimate Class 3 via the batch-payout signature. Distributed staking-infrastructure beneficiaries are not protocol-controlled custody, and excluding them would understate the participating-holder distribution.

## Audit framework

For systematic application across the cross-section (the N = 45 PCA-audited cohort), each candidate PCA address whose class is ambiguous under explicit attribution is evaluated against the four-property matrix in the following order: (1) flow directionality, which separates convergent from divergent flow; (2) the lifetime-inflow-to-current-balance ratio, which separates throughput from accumulation; then (3) rotation cadence and (4) balance steady state as confirming evidence. An address is reclassified only when at least the two most-diagnostic properties (directionality and the inflow-to-balance ratio) agree. Addresses for which the signature is indeterminate are retained at their pre-signature classification, the conservative disposition that avoids over-exclusion. The framework is applied uniformly across the EVM, Solana, and Substrate cohorts.
