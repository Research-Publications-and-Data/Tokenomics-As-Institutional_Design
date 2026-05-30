# Supplementary File S12: PCA-symmetric robustness check

**Companion to:** B2 paper *Tokenomics as Applied Political Philosophy: Governance Concentration Beyond Token Allocation* (Section 4.6.1 Voting-HHI methodology robustness). Generated 2026-05-22; refreshed for the final-version sample.

---

## Abstract

This supplement tests whether the predominant-amplification finding in Section 4.5 of the main paper (delegation amplifies voting concentration above holding concentration in thirteen of eighteen protocols with comparable voting data; five protocols disperse) is robust to applying protocol-controlled-address (PCA) exclusion symmetrically: that is, excluding foundation, treasury, and aggregation-related governance addresses from voting HHI as the paper excludes the corresponding custody addresses from holding HHI. The asymmetric approach used in Section 4.5 follows established delegation-HHI literature (Fritsch et al., 2024) by including all delegates with non-zero voting power regardless of whether the delegate is a protocol-controlled entity. The symmetric robustness check tests the alternative methodology, and the qualitative amplification finding holds under it.

## Cross-reference

This supplement supports the Section 4.6.1 voting-HHI methodology robustness paragraph. Main paper retains a summary of the three methodology axes (Tally delegate-sample depth, symmetric PCA exclusion on Snapshot, and proper-weight versus vote-count methodology on Solana); this supplement reports the per-protocol signer-side functional-PCA results and the surface-class distinctions that make symmetric exclusion non-mechanical on the voting side.

## Why symmetric exclusion is not a simple mirror of the holder side

Applying PCA exclusion symmetrically on the voting side requires distinguishing three structurally distinct surface classes:

- **Holder-side custody addresses.** Treasury safes, vesting multisigs, foundation cold wallets, staking-aggregation contracts, CEX hot wallets, and burn destinations. These are the addresses excluded from the holding distribution per the five-class typology in Section 3.8.
- **Signer-side governance-operation addresses.** Foundation operational signing wallets that cast votes but are distinct from holder-side custody. These do not appear in the holder-side exclusions store; they are registered separately in the sibling canonical store `exclusions_log_signer.csv`.
- **Off-Realms custody multisigs for Solana protocols.** These appear in neither on-Realms voter sets nor Snapshot voter pools, because Solana PCAs structurally separate custody from governance signing.

A naive mirror of the holder-side address list onto the voting side therefore detects almost nothing: across thirteen Snapshot-sourced protocols (12,878 voter rows), holder-side PCA-address-based symmetric exclusion detects zero PCA voters, because Snapshot voter pools (off-chain message signers) are structurally disjoint from the holder-side custody-address taxonomy. The substantive symmetric-exclusion test is therefore the signer-side functional-PCA test below.

## Per-protocol signer-side functional-PCA exclusion results

Four signer-side functional PCAs hold substantial voting weight and are registered in `exclusions_log_signer.csv`. Each was confirmed via blockchain-explorer or vesting-contract verification (Blockscout address-info lookups; Tally delegate labels; Hedgey vesting-redemption traces; public-name-tag and Farcaster cross-reference).

| Protocol | Functional PCA | Voter share | Voting HHI (before exclusion) | Voting HHI (after exclusion) | Direction |
|---|---|---:|---:|---:|---|
| Compound | Compound Foundation operational signer | 25.01 percent | 0.0889 | 0.0468 | reduces |
| Balancer | Balancer DAO multisig (GnosisSafe 1.3.0) | 51.95 percent | 0.3045 | 0.1499 | reduces |
| Gitcoin | Kevin Owocki / Gitcoin Maintainer founder address | 27.93 percent | 0.1792 | 0.1948 | increases |
| WeatherXM | Hedgey-vested WXM insider allocation recipient | 74.04 percent | 0.5561 | 0.1184 | reduces |

**The amplification finding holds across all four confirmed signer-side cases even under symmetric PCA exclusion.** All four protocols retain voting HHI above their post-exclusion holding HHI after the functional PCA is removed, so the directional claim (delegation amplifies governance concentration above holdings) survives symmetric exclusion.

## Case interpretation: signer-side exclusion is a direction-of-effect test, not a mechanical reduction

Signer-side PCA exclusion is a substantive direction-of-effect test rather than a mechanical concentration-reducing adjustment. For three of the four confirmed functional PCAs, exclusion reduces voting HHI as expected (Compound 0.0889 to 0.0468, delta -0.0421; Balancer 0.3045 to 0.1499, delta -0.1546; WeatherXM 0.5561 to 0.1184, delta -0.4377). For Gitcoin, exclusion *increases* voting HHI from 0.1792 to 0.1948 (delta +0.0156): the reverse-direction pattern arises from a smaller-denominator effect, because the excluded PCA held about 28 percent of total weight and the remaining voters become more concentrated relative to each other under the smaller post-exclusion total. When PCA exclusion increases HHI, the finding indicates that PCA concentration was masking a more concentrated underlying distribution among non-PCA voters, which is itself a substantive structural feature of the protocol's governance. The pattern is most extreme in small voter pools and dilutes in larger pools.

## Case interpretation: a refuted candidate cluster

An additional DIMO Foundation candidate cluster (rank-1 plus rank-2 voters; 58.83 percent of combined voting weight) was registered in the initial expansion and subsequently refuted via Polygon Blockscout funding-source verification: neither voter holds substantial DIMO tokens, so the cluster represents active community delegates in a thin ten-voter pool rather than functional PCAs. The refutation is recorded to document that the signer-side test rejects false positives, not only confirms expected ones.

## Methodology continuity note

Four Tally-sourced protocols sweep from the top-1,000 delegate sample to the all-delegates depth as a sampling-robustness companion to the symmetric-exclusion test: AAVE (N = 150,911), COMP (N = 18,627), UNI (N = 48,707), and ARB (N = 437,453). All four HHI shifts are below 0.005 (AAVE 0.0357 to 0.0324; COMP and UNI unchanged; ARB 0.0340 to 0.0320). The top-1,000 sample is empirically robust because PCAs concentrate at the top of the distribution and tail delegates contribute share-squared terms below 1e-4. The three Solana protocols supplying apples-to-apples voting HHI under proper-weight methodology (JUP at 0.00546, HNT bracketed at 0.0261 to 0.0394 under VSR position-state reconstruction, DRIFT at 0.0833) confirm the Solana custody-versus-governance separation, because the respective protocol-controlled addresses do not appear in the voter sets.

## Methodological implications

1. **Asymmetric methodology follows established literature.** The paper's Section 4.5 voting HHI uses the asymmetric approach consistent with Fritsch et al. (2024); this is the literature standard for cross-protocol comparison.

2. **Symmetric methodology preserves the qualitative finding.** Predominant amplification holds across the confirmed signer-side functional-PCA cases under either methodology; the magnitude estimates differ but the directional claim (delegation amplifies above holdings) is robust to methodology choice.

3. **Signer-side functional PCAs, not holder-side addresses, are the operative voting-side construct.** Snapshot voter pools are disjoint from the holder-side custody taxonomy, so the substantive symmetric-exclusion test runs on signer-side governance-operation addresses verified via funding-source and vesting-redemption tracing. Layer-2 funding-source clustering (Blockscout verification on Snapshot; Subscan transfers-received clustering on Polkadot) is the productive cross-surface verification method for this class, and is the recommended standard verification axis for future cross-protocol expansion.

## Replication

The four confirmed signer-side functional PCAs, with per-address verification reasoning and before / after voting HHI, are in the canonical store `data/processed/exclusions_log_signer.csv` in the replication repository. Inputs: Snapshot voter pools per protocol (12-month rolling window); Tally delegate labels and Blockscout address-info lookups for PCA identification; Hedgey vesting-redemption traces for the WeatherXM case.
