# Supplementary File S12: PCA-symmetric robustness check

**Companion to:** B2 paper *Tokenomics as Applied Political Philosophy: Governance Concentration Beyond Token Allocation* (Section 4.6 Robustness). Generated 2026-05-22.

---

## Abstract

This supplement tests whether the predominant-amplification finding in Section 4.5 of the main paper (delegation amplifies voting concentration above holding concentration in thirteen of eighteen protocols sampled) is robust to applying protocol-controlled-address (PCA) exclusion symmetrically, that is, excluding foundation, treasury, and aggregation-contract delegates from voting HHI as the paper excludes them from holding HHI. The asymmetric approach used in Section 4.5 follows established delegation-HHI literature (Fritsch et al., 2024) by including all delegates with non-zero voting power regardless of whether the delegate is a protocol-controlled entity. The symmetric robustness check tests the alternative methodology.

## Cross-reference

This supplement supports the Section 4.6 PCA-symmetric voting-HHI sensitivity check. Main paper retains a 2-sentence summary inline; this supplement reports the per-protocol exclusion results and the Compound Foundation + stkAAVE staking-aggregation case interpretations.

## Methodological setup

The Table 6 voting HHI in the main paper follows established delegation-HHI literature (Fritsch et al., 2024) by including all delegates with non-zero voting power, regardless of whether the delegate is a protocol-controlled entity. Applying protocol-controlled-address exclusion symmetrically (excluding foundation, treasury, and aggregation-contract delegates from voting HHI as we exclude them from holding HHI) yields a sensitivity-check result.

Among the five Tally-sourced protocols where PCA delegates can be identified from Tally labels (Compound, Aave, Uniswap, Optimism, Arbitrum), three show zero PCA presence in their top-100 delegates because their excluded foundation addresses do not delegate voting power to themselves: Uniswap, Optimism, Arbitrum. The remaining two protocols (Compound, Aave) have a PCA-equivalent delegate in the top-100 sample.

## Per-protocol PCA-symmetric exclusion results

| Protocol | Voting HHI (asymmetric, Table 6) | Top PCA-equivalent delegate | Voting HHI (symmetric exclusion) | Amplification ratio (asymmetric) | Amplification ratio (symmetric) |
|---|---:|---|---:|---:|---:|
| Compound | 0.078 | Compound Foundation (21.5% of total delegated voting power) | 0.052 | 8.7x | 5.8x |
| Aave | 0.076 | stkAAVE staking contract (21.9% of total delegated voting power) | 0.045 | 5.9x | 3.5x |
| Uniswap | 0.045 | (no PCA delegate in top-100; asymmetric ≈ symmetric) | 0.045 | 4.5x | 4.5x |
| Optimism | 0.033 | (no PCA delegate in top-100) | 0.033 | 3.6x | 3.6x |
| Arbitrum | 0.050 | (no PCA delegate in top-100) | 0.050 | 5.5x | 5.5x |

**The predominant-amplification finding holds across all five Tally-sourced protocols even under symmetric PCA exclusion.** All five protocols retain amplification ratios above 1.0 (voting HHI > holding HHI) under either methodology.

## Case interpretation: Compound Foundation

Compound's top Tally delegate is Compound Foundation (21.5% of total delegated voting power in the May 2026 Tally pull at top-100 sampling depth). Applying symmetric exclusion drops Compound's voting HHI from 0.078 to 0.052 and the amplification ratio from 8.7x to 5.8x. The Compound Foundation case is informative because: (a) the Foundation entity is structurally similar to other excluded protocol-controlled addresses (the Foundation does not act on behalf of broad token-holder preferences); (b) Compound's Snapshot-based voting HHI for the same window is 0.089, which is the canonical Table 6 voting HHI for Compound, selected over the Tally-source because Snapshot's broader voter pool (N = 138 unique voters) exceeds Tally's top-100 delegate sampling and partially internalizes the PCA-exclusion logic.

## Case interpretation: Aave stkAAVE staking contract

Aave's top Tally delegate is the stkAAVE staking contract (21.9% of total delegated voting power); this is a passthrough aggregation rather than an institutional PCA. Stakers in stkAAVE vote through the contract, which votes as a single delegate per Tally's data model. The "symmetric exclusion under the broader definition" (treating the staking contract as a PCA) drops Aave's voting HHI from 0.076 to 0.045 and the ratio from 5.9x to 3.5x at the top-100 sample depth. The case is methodologically interesting because the underlying voters are dispersed (the staking contract aggregates many stakers), but the contract-level voting position is concentrated; whether to count the contract as a single delegate or to distribute its voting weight across underlying stakers is a methodology decision.

## Methodology continuity note

The main paper's voting-HHI methodology uses top-1000 Tally delegate sampling per protocol (the Section 3.3 sampling methodology, with robustness in Section 4.6.1). The PCA-symmetric exclusion values reported above are computed at the top-100 delegate sample depth, reported as a pre-refresh sensitivity-check companion to the Section 4.6 robustness analysis.

## Methodological implications

1. **Asymmetric methodology follows established literature.** The paper's Section 4.5 voting-HHI uses the asymmetric approach consistent with Fritsch et al. (2024); this is the literature standard for cross-protocol comparison.

2. **Symmetric methodology preserves the qualitative finding.** Predominant-amplification holds across all five Tally-sourced protocols under either methodology; the magnitude estimates differ but the directional claim (delegation amplifies above holdings) is robust to methodology choice.

3. **Snapshot-based voting HHI internalizes the PCA-exclusion logic naturally.** Snapshot's broader voter pool (N = 138 for Compound) does not concentrate in a Foundation-style delegate the way Tally's top-100 delegate sampling does. The Snapshot-based voting HHIs in Table 6 are therefore closer to the symmetric-exclusion methodology than the Tally-based voting HHIs, and the Table 6 selection of Snapshot over Tally for protocols where Snapshot data is more comprehensive partially closes the symmetric-asymmetric methodology gap.

## Replication

Computational detail and per-protocol stkAAVE / Compound Foundation delegate identification at `b2/paper/supplements/pca_symmetric_robustness_2026-05-22.py` in the replication repository. Inputs: Tally top-100 delegate sample per protocol (May 2026 pull); Tally delegate labels for PCA identification.
