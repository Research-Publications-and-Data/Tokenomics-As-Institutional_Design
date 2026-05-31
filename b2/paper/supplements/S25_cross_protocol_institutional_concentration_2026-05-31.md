# Supplementary File S25: Cross-Protocol Institutional Concentration (Fifth-Axis Evidence)

This file is the reviewer-facing home for the cross-protocol institutional-concentration evidence previewed in Section 4.5.5 of the main text. It documents, in three parts: (1) the voter-axis institutional-delegate pattern at Snapshot and Tally depth (the professional governance firms that aggregate delegated voting power across multiple protocols); (2) the holder-axis cross-protocol CEX-overlap pattern (the EVM universal hot-wallet sweep and the Solana candidate-address verification); and (3) the Substrate validator-set CEX-attribution pattern on Polkadot. The unifying claim is that a fifth concentration axis, cross-protocol institutional concentration, is load-bearing for the cross-section's concentration story and is not captured by any per-protocol HHI metric. The axis is descriptive and orthogonal to the paper's four empirical contributions; full development to additional governance surfaces remains future work (Section 5.8).

The cross-section is 52 protocols. All values below are point-in-time measurements consistent with the main-text snapshot discipline (March 2026 base; May 2026 Tally and Snapshot replication for added protocols).

---

## Part 1: Voter-axis institutional-delegate pattern (Snapshot and Tally)

### 1.1 Snapshot voter-pool aggregation

The Snapshot voter-pool extension to 13 protocols aggregated 11,077 unique voter addresses across the cross-section (UNI, COMP, LDO, DIMO, WXM, ARB, BAL, GTC, MPL_SYRUP, POKT, AAVE, ENS, GMX). Of these, 1,801 voters (16.3 percent) participate in 2 or more protocols' Snapshot governance. A small institutional-governance-investor class (approximately 10 to 50 addresses) participates in 6 or more protocols' delegate programs simultaneously.

The top three institutional cross-protocol delegators collectively exert 17.0 percent combined Snapshot voting power across the L1 DeFi suite:

| Firm | Address | ENS name | DAOs | DAOs participated | Combined summed Snapshot share |
|---|---|---|---|---|---|
| PGov | `0x3fb19771...` | pgov.eth | 7 | ARB, COMP, ENS, GMX, GTC, LDO, UNI | 10.16 percent |
| Tane Governance | `0xb79294d0...` | tanegov.eth | 6 | (six DAOs) | 4.83 percent |
| Arana Digital | `0x0579a616...` | aranadigital.eth | 6 | (six DAOs) | 2.04 percent |

These are professional governance firms whose business model is providing cross-protocol delegation services to token-holders who do not vote directly; the firms aggregate delegated voting power across multiple protocols simultaneously.

### 1.2 Tally-side audit (all-delegates depth)

The pattern is not Snapshot-specific. A parallel Tally-side audit across the four EVM Tally protocols at all-delegates depth (AAVE N = 150,911; COMP N = 18,627; UNI N = 48,707; ARB N = 437,453) confirms PGov, Tane Governance, and Arana Digital all appear in the Tally delegate registries with substantial cross-protocol presence: combined summed share of 8.11 percent across ARB + COMP + UNI delegate weight.

The Tally audit also surfaces seven additional institutional governance firms operating cross-protocol at material delegated weight: Blockworks Advisory, Wintermute Governance, L2BEAT, Humpy, Gauntlet, GFX Labs, and olimpio. These firms operate as professional-delegate service providers whose business model is cross-protocol delegation aggregation rather than single-protocol participation. The Tally-side and Snapshot-side audits jointly establish the cross-protocol institutional pattern across both major EVM-governance surfaces in the cross-section.

### 1.3 Why per-protocol metrics miss it

The pattern is invisible to per-protocol concentration metrics. The predominant-amplification finding (Section 4.5) addresses delegation amplification within a single protocol (delegated voting power exceeds post-exclusion holding HHI); it does not address whether the same set of institutional delegates appears across multiple protocols. Token-holders who delegate to professional firms acquire delegated representation across multiple protocols simultaneously; the firms' decisions affect governance outcomes in all protocols where they hold delegated weight, creating correlated voting patterns invisible to per-protocol Mann-Whitney or Cohen's d analysis. A single entity (PGov) operating across 7 Snapshot DAOs plus at least 3 of the 4 Tally protocols audited represents a meaningfully concentrated cross-protocol governance position that no per-protocol HHI metric captures.

---

## Part 2: Holder-axis cross-protocol CEX-overlap pattern (EVM and Solana)

The voter-axis cross-protocol pattern documented in Part 1 has a structural-mechanical counterpart at the holder-axis surface.

### 2.1 EVM universal CEX hot-wallet sweep

The EVM-side universal CEX hot-wallet sweep across the EVM cross-section identifies 89 cross-protocol holder-address hits across 21 protocols, with 8 producing material post-exclusion HHI shifts above 0.0005 (largest: Aethir +0.0033). The Bitpanda hot wallet `0x18...` appears in 20 protocols, the most widespread cross-protocol CEX presence in the cross-section. Full per-protocol breakdown is reported in the S19 phase-4 scope-expansion materials.

### 2.2 Solana candidate-address verification

An initial cross-protocol Solana candidate-address verification (Sim API balance plus token-portfolio analysis on 7 candidate addresses; 6 classified as CEX hot wallet and 1 as institutional investor) is reported in the S13 Solana PCA audit addendum.

### 2.3 Relationship to the voter-axis pattern

The holder-axis CEX pattern is structurally distinct from the voter-axis pattern: PGov, Tane, Arana, and the other Tally firms are professional governance firms whose business model is deliberate cross-protocol delegation, whereas CEX hot wallets are mechanical custody routing that produces cross-protocol address overlap without coordinated governance intent. The two patterns share the structural-mechanical character: per-protocol HHI metrics undercount the cross-protocol-aggregated concentration that emerges when the same operator (a PGov-class governance firm or exchange-custody routing) holds material weight at multiple protocols simultaneously. Both patterns converge on the same conclusion: a fifth concentration axis (cross-protocol institutional concentration, covering both governance-coordination and custody-routing mechanisms) is load-bearing for the cross-section's concentration story and is not captured by any per-protocol HHI metric.

---

## Part 3: Substrate validator-set CEX-attribution pattern (Polkadot)

A second, structurally-distinct evidence path converges on the cross-protocol CEX-mediated concentration pattern at the Substrate validator-set layer.

On Polkadot (Nominated Proof-of-Stake), the validator-set HHI is 0.0017, mechanically equalized by the Phragmen election design and distinct from Polkadot's post-PCA holder-balance HHI of 0.0052 (a genuinely low but real holder distribution computed the same way as every other protocol in the cross-section). The validator-set and operator-attribution layer, not the holder layer, is where Polkadot concentration manifests.

A five-axis operator-attribution methodology combining Subscan Identity Pallet plus Web3 Foundation Thousand Validators Programme registry plus Layer-2 funding-source clustering plus Polkawatch display-name matching plus direct Polkawatch DDP API access lifts cumulative attribution from 16 percent of bonded stake (Identity Pallet baseline) to 53 percent (300 of 600 validators attributed). It surfaces:

| CEX | Validators | Bonded-stake share | On-chain visibility |
|---|---|---|---|
| Binance | 15 | 3.72 percent | Visible |
| Coinbase | 12 | (not separately reported) | Invisible to all four on-chain attribution axes |
| EXNESS | 6 | (not separately reported) | Invisible to all four on-chain attribution axes |

The latter two operate via relay-mixing funding patterns. Combined CEX-validator footprint is at least 27 validators across the Polkadot active set, a 69 percent increase in counted CEX presence relative to on-chain-only verification.

The Polkadot evidence demonstrates that the EVM universal CEX-sweep pattern is not EVM-specific: cross-protocol CEX-mediated concentration generalizes to Substrate NPoS chains under appropriate methodology adaptation. Sister-context: TAO (Bittensor), a Substrate base-layer L1, enters the holding cross-section at a post-PCA holder-balance HHI of 0.0075 (principal-exclusion adjusting for confirmed CEX coldkeys); its subnet-validator-layer concentration is a coverage-gap item deferred to future work, so TAO is analyzed on the holder-balance axis alongside the other L1 protocols rather than via validator-network attribution.

The CEX-validator concentration findings are reported as lower bounds for Substrate NPoS protocols, because operator-attribution coverage on Substrate (53 percent, with a residual approximately 47 percent structural ceiling for voluntary-identity-pallet protocols) is below the near-complete coverage on EVM (roughly 95 percent) and Solana (roughly 80 percent). The EVM and Solana CEX-overlap findings use near-complete-coverage attribution data and are not lower bounds. Section 5.7 documents the cross-architecture attribution-coverage asymmetry as a methodological limitation.

---

## Part 4: Cross-references and reproduction

Full per-axis detail for the materials summarized here is reported in the following supplements:

- Voter-axis institutional-delegate audit (Snapshot 13-protocol pool plus Tally all-delegates audit): this file, Part 1.
- EVM universal CEX hot-wallet sweep (per-protocol breakdown; 89 hits across 21 protocols): S19 phase-4 scope-expansion materials.
- Solana candidate-address verification (7 addresses): S13 Solana PCA audit addendum.
- Polkadot five-axis operator-attribution methodology, per-axis attribution decomposition, 47 percent structural attribution ceiling discussion, per-operator stake breakdown, and the operator-infrastructure-axis candidate (Hetzner, AWS, colocation, self-hosted classification via the Polkawatch LastNetwork field): S16c DOT addendum, S19 verification execution, S19 Polkawatch synthesis, S19 Polkawatch API discovery, and S20 Subscan refresh finding.

The Snapshot signer-side institutional-provider dual-account class (institutional staking providers such as Blockdaemon, KILN, pos.dog, Iceberg Nodes, and ParaNodes register Subscan Identity Pallet attestation on funding warm-wallet accounts but not on validator stash accounts) is documented in Section 4.6.1 of the main text as a voting-HHI methodology-robustness item; Layer-2 funding-source clustering is the productive cross-surface verification method for that class.