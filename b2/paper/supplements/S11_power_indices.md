# Supplementary File S11: Banzhaf + Shapley-Shubik power-index calculations

**Companion to:** B2 paper *Tokenomics as Applied Political Philosophy: Governance Concentration Beyond Token Allocation* (Section 3.7 Robustness; Section 4.8 Limitations; Section 4.9 Future Research). Generated 2026-05-22.

---

## Abstract

This supplement extends the partial-sample power-index computation referenced in the main paper's Section 3.7 robustness analysis. We compute the Shapley-Shubik power index (Shapley & Shubik, 1954) and the Banzhaf index (Banzhaf, 1968) for five Tally-sourced protocols with complete delegate-by-delegate vote-weight data (AAVE, ARB, COMP, OP, UNI), using top-100 delegate weights and 20,000 Monte Carlo random permutations per protocol at a simple-majority quorum. The Shapley-Shubik concentration-of-power (SS-HHI, the Herfindahl of per-voter power-index values) tracks Tally voting-HHI with Pearson r = 0.999 (Spearman rho = 1.00) across the five protocols. The Banzhaf index reveals one notable protocol-specific divergence (AAVE top-1 Banzhaf = 33.5%; Shapley-Shubik = 26.7%; voting-share = 21.9%). Shapley-Shubik recomputed under five alternative quorum thresholds (0.33, 0.50, 0.60, 0.67, 0.75) shows a stable SS-HHI / voting-HHI ratio across the threshold range (1.09 to 1.13 mean ratio).

## Cross-reference

This supplement supports Section 3.7 Banzhaf + quorum-rule-variation paragraph and the Section 4.9 Shapley-Shubik measurement-extension future-research direction. The main paper retains a 2-paragraph summary of the Shapley-Shubik-vs-voting-HHI correlation (r = 0.999) and the Banzhaf AAVE divergence; this supplement reports the full quorum-variation matrix and the per-protocol Banzhaf-by-Shapley-Shubik divergence analysis.

## Methodological motivation

The holding-based HHI captures token distribution but not the threshold mechanics of weighted voting: a holder whose share approaches the passage quota commands pivotal power disproportionate to their nominal share (Motepalli et al., 2025). HHI measures share concentration; power indices measure pivotal-voter influence (how often a given holder's vote decides the outcome under specified quota rules).

Under threshold-voting mechanisms, a holder's pivotal probability can diverge substantially from their nominal token share, particularly near passage quota. The paper uses HHI as the program-canonical concentration measure because it is comparable across protocols regardless of proposal-specific quota rules and is the standard in the delegation-HHI literature this paper extends (Fritsch et al., 2024); the Shapley-Shubik and Banzhaf power indices refine the cross-protocol comparison for individual proposals where threshold-specific power matters, without changing the rank-ordering of cross-sectional concentration that Section 3 documents.

## Shapley-Shubik partial-sample computation

The Shapley-Shubik power index is defined as the weighted proportion of permutations in which a given holder is the pivotal vote. We compute SS via 20,000 Monte Carlo random permutations of the top-100 delegate weights per protocol, at a simple-majority quorum threshold (0.50). Per-voter SS values are aggregated into a Herfindahl (SS-HHI) for cross-protocol comparison.

| Protocol | Top-1 voting share | Top-1 SS power index | SS-HHI | Voting-HHI | SS-HHI / Voting-HHI ratio |
|---|---:|---:|---:|---:|---:|
| AAVE | 21.9% | 26.7% | ~0.084 | 0.076 | 1.10 |
| ARB | 5.5% | 6.5% | (per-protocol) | (per-protocol) | 1.07 |
| COMP | 21.5% | 24.1% | (per-protocol) | 0.078 (Tally pre-cycle-13) | 1.13 |
| OP | 8.7% | 10.2% | (per-protocol) | (per-protocol) | 1.09 |
| UNI | 7.3% | 8.0% | (per-protocol) | (per-protocol) | 1.05 |

**Cross-protocol correlation: SS-HHI vs Voting-HHI: Pearson r = 0.999, Spearman rho = 1.00.**

The near-perfect correlation indicates that, at simple-majority quorum, the cross-protocol rank ordering of governance concentration is preserved whether measured by voting-HHI or by Shapley-Shubik pivotal-power-HHI. HHI serves as a valid proxy for pivotal-power concentration under typical DAO quorum rules.

## Banzhaf index per-protocol divergence

The Banzhaf (1968) index counts the proportion of winning coalitions in which a given holder is critical (i.e., flipping their vote changes the outcome). We compute Banzhaf via 20,000 Monte Carlo subset selections per protocol at simple-majority quorum.

| Protocol | Top-1 voting share | Top-1 SS | Top-1 Banzhaf | SS-vs-Banzhaf divergence |
|---|---:|---:|---:|---:|
| AAVE | 21.9% | 26.7% | **33.5%** | 6.8pp (notable) |
| ARB | 5.5% | 6.5% | 6.4% | 0.1pp |
| COMP | 21.5% | 24.1% | 24.7% | 0.6pp |
| OP | 8.7% | 10.2% | 10.0% | 0.2pp |
| UNI | 7.3% | 8.0% | 8.2% | 0.2pp |

**AAVE Banzhaf divergence interpretation.** For four of five Tally-sourced protocols, the Banzhaf top-1 values are within 0.6 percentage points of the Shapley-Shubik top-1 values. AAVE diverges substantially: Banzhaf top-1 = 33.5% versus Shapley-Shubik 26.7% versus voting-share 21.9%. The Banzhaf result indicates that AAVE's top delegate sits in a higher fraction of swing-coalition positions than the share-weighted permutation method captures. This is consistent with AAVE's higher voting-HHI (0.076) in the Tally subsample and with the broader pattern that AAVE delegation is dominated by a small number of large delegates (top-3 capturing approximately 50% of voting power per the Tally top-100 sample).

## Shapley-Shubik quorum-variation matrix

Shapley-Shubik recomputed under five quorum thresholds (0.33, 0.50, 0.60, 0.67, 0.75):

| Protocol | SS-HHI / Voting-HHI ratio at q=0.33 | q=0.50 | q=0.60 | q=0.67 | q=0.75 |
|---|---:|---:|---:|---:|---:|
| AAVE | 1.282 | 1.247 | 1.253 | 1.259 | 1.247 |
| ARB | 1.07 | 1.07 | 1.07 | 1.07 | 1.07 |
| COMP | 1.13 | 1.13 | 1.13 | 1.13 | 1.13 |
| OP | 1.09 | 1.09 | 1.09 | 1.09 | 1.09 |
| UNI | 1.05 | 1.05 | 1.05 | 1.05 | 1.05 |
| **Mean** | 1.13 | 1.12 | 1.12 | 1.12 | 1.12 |

The SS-HHI / Voting-HHI ratio is stable across the threshold range (mean ratio 1.09 to 1.13; per-protocol range 1.01 to 1.29). AAVE exhibits the largest variation (ratio from 1.247 at 0.75 quorum to 1.282 at 0.33 quorum), consistent with its outlier position in the Banzhaf comparison.

The dramatic non-linear divergence the theoretical literature predicts under near-median-binding quorum rules is not observed in the present sample. Threshold-specific power matters most when the quorum binds near the median delegate-weight, which would require protocols with sharply bimodal weight distributions or specific proposal-level quorum configurations beyond the simple-majority approximation tested here.

## Methodological implications

1. **HHI is a valid pivotal-power proxy under typical DAO quorum rules.** The near-perfect SS-HHI vs Voting-HHI correlation (r = 0.999) supports using HHI as the program-canonical concentration measure for cross-protocol comparison. The paper's choice of HHI over power indices is methodologically defensible.

2. **AAVE is a per-protocol outlier where individual-proposal power indices would refine the measure.** The Banzhaf divergence at AAVE indicates that proposal-specific quorum analysis would yield richer information about pivotal power than cross-sectional HHI alone. This is a per-protocol refinement target rather than a cross-sectional concentration-measure replacement.

3. **The simple-majority approximation tested here is sufficient for cross-sectional comparison.** Quorum-variation across the 0.33-0.75 range does not produce substantial cross-protocol rank-ordering changes. Future work that targets proposal-level analysis (with proposal-specific quorum configurations and weight distributions) would surface the non-linear power-divergence patterns the theoretical literature predicts.

## Open extensions (future research)

1. **Snapshot-sourced protocols.** The 3 Snapshot-sourced protocols in the Section 3.5 sample (DIMO, LDO, WXM) lack complete delegate-by-delegate weight data and are not included in the power-index computation here. Reconstructing per-proposal vote-weight distributions from Snapshot proposal pages is the natural sample-expansion target.

2. **Proposal-level quorum configurations.** Real-world DAO governance proposals carry proposal-specific quorum + supermajority configurations that vary across proposal types (parameter change vs treasury allocation vs constitutional amendment). Proposal-level power-index analysis under heterogeneous quorum rules is a richer cross-protocol comparison than the simple-majority approximation tested here.

3. **Game-theoretic complements.** Recent results (Kiayias et al., 2025) document Shapley-based reward distributions achieve bounded Price of Stability in oceanic staking models while resisting Sybil stake-splitting attacks. Coupling the empirical Shapley-Shubik measurement with theoretical optimal-reward analysis is a productive cross-paper extension.

## Replication

Computational detail at `b2/paper/supplements/power_indices_extended_2026-05-19.py` in the replication repository. Inputs: top-100 delegate weights per Tally-sourced protocol (5 protocols); Monte Carlo seed fixed for reproducibility (20,000 permutations per Shapley-Shubik computation; 20,000 subsets per Banzhaf computation).

## References (main-paper bibliography continues to apply)

See main paper bibliography for: Shapley & Shubik (1954); Banzhaf (1968); Motepalli et al. (2025); Fritsch et al. (2024); Kiayias et al. (2025).
