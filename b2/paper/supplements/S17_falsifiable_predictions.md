# Supplementary File S17: Falsifiable forward predictions with operationalization detail

**Companion to:** B2 paper *Tokenomics as Applied Political Philosophy: Governance Concentration Beyond Token Allocation* (Section 5.8 Future Research). Generated 2026-05-22.

---

## Abstract

This supplement details five falsifiable predictions about subsequent cross-protocol governance trajectories that the B2 cross-sectional design supports. Each prediction comes with an explicit operationalization that future panel-data and event-study work can test. The full operationalization includes data requirements, statistical tests, and explicit falsification thresholds; the main paper retains a brief list of the five predictions, with detail in this supplement.

## Cross-reference

This supplement supports the Section 5.8 falsifiable forward claims subsection. Main paper retains a brief list of the predictions; this supplement reports the full operationalization detail per prediction.

## Methodology inheritance

All five predictions inherit the methodology applied in the main paper:
- PCA-symmetric exclusion via the five-class typology codified in Section 3.8
- HHI computed on the post-exclusion top-1,000 holder distribution
- Mann-Whitney for two-sample tests
- Bootstrap 95% percentile intervals for effect-size robustness

## Pre-registration commitment

The hypothesis specifications, statistical tests, and falsification thresholds below will be deposited as a pre-registration document on the Open Science Framework (OSF) prior to data collection for any panel-data or event-study extension of this cross-sectional analysis. The pre-registration DOI will be incorporated into the replication-repository README and Supplementary File S5 (pipeline specification) on deposit; the commitment is to fix the hypothesis text and analysis plan before the data is collected, addressing the multiple-comparisons concerns inherent in post-hoc cross-sectional descriptive analysis.

---

## Prediction 1 (sector persistence)

**Claim.** If governance concentration tracks sector membership, DePIN protocols launching in 2026 or 2027 will, on average, exhibit higher post-distribution holding HHI than DeFi protocols launching in the same period, conditional on launch year and initial insider allocation similarity.

**Operationalization.** For each protocol in the entry cohort, compute holding HHI at the T+12-month and T+24-month marks under the PCA-symmetric exclusion methodology applied in this paper (per Section 3.8).

**Test.** Mann-Whitney comparing the DePIN-cohort and DeFi-cohort holding HHI distributions.

**Falsification thresholds.** The prediction is falsified if (a) the cohort-level Mann-Whitney p-value exceeds 0.10 across both time points, or (b) the sign of the median difference reverses (DeFi exceeds DePIN).

## Prediction 2 (delegation amplification universality)

**Claim.** Any protocol introducing a formal delegate-program after the snapshot dates used in this analysis (or expanding from informal to formal delegation) will produce voting HHI greater than its holding HHI within twelve months of the program launch, with the amplification magnitude varying by delegate-program design rather than by sector.

**Operationalization.** Compute the protocol's holding HHI under the PCA-symmetric exclusion methodology and its voting HHI using Tally or Snapshot delegate voting power at T+6, T+9, and T+12 months post-launch.

**Falsification thresholds.** The prediction is falsified if (a) any of these post-launch protocols produces voting HHI less than holding HHI at the T+12-month mark (structural-dispersion case in the ENS direction; falsifies the universality claim), or (b) amplification magnitude correlates with sector membership rather than with delegate-program design choices.

## Prediction 3 (insider-retention persistence)

**Claim.** Protocols whose insider fraction of top-10 holders increases between the March 2026 baseline and a subsequent measurement will, on average, exhibit increased holding HHI over the same period; protocols whose insider fraction decreases will exhibit decreased holding HHI.

**Operationalization.** Panel measurement of the insider-fraction-of-top-10-holders variable and holding HHI at quarterly intervals.

**Falsification threshold.** The prediction is falsified if the cross-protocol within-protocol correlation between insider-fraction change and HHI change is not statistically distinguishable from zero (Spearman rho < 0.20 with 95% CI including zero).

## Prediction 4 (delegate-program design as moderator)

**Claim.** Among protocols in Prediction 2's post-launch set, those that adopt broad-community-delegate distribution design choices (recurring delegate compensation; public delegate platforms; active recruitment of long-form policy positions) will exhibit lower amplification ratios than those that do not.

**Operationalization.** Code each post-launch protocol on a binary indicator for broad-community-delegate-distribution design; test whether the indicator predicts amplification ratio.

**Falsification threshold.** Falsified if the design-indicator coefficient does not differ from zero at p < 0.10 in a regression of amplification ratio on design choice, sector dummies, and protocol-age control.

## Prediction 5 (chain-architecture as trajectory moderator)

**Claim.** An age-balanced extended cohort, matching Solana and EVM DeFi protocols on distribution-phase maturity, will discriminate among three outcomes for the chain-architecture trajectory difference observed descriptively in Section 4.3.1. If the matched cohort sustains a higher post-distribution deconcentration rate for EVM than for Solana DeFi protocols at conventional significance, chain ecosystem operates as a trajectory moderator independent of maturity. If the difference attenuates below significance, the descriptive difference is attributable to the maturity imbalance rather than to chain architecture. If the difference inverts, an alternative mechanism is required.

**Operationalization.** Construct an entry-cohort of Solana and EVM DeFi protocols matched on launch-era distribution-phase maturity (so that chain ecosystem is not collinear with protocol age, the confound that holds Section 4.3.1 at the descriptive layer). For each protocol, compute the post-distribution deconcentration rate (holding-HHI change under the Section 3.8 PCA-symmetric exclusion methodology) at the T+12-month and T+24-month marks.

**Test.** Mann-Whitney and Fisher exact tests on the entry-cohort deconcentration rates at T+12 and T+24 months, comparing the EVM and Solana DeFi sub-cohorts on the age-balanced cohort.

**Falsification thresholds.** The prediction is operationalized as a three-outcome discrimination rather than a single null: (a) chain-architecture moderates trajectory (EVM deconcentration rate exceeds Solana at conventional significance on the matched cohort); (b) the descriptive difference is a maturity artifact (the difference attenuates below significance once maturity is balanced); (c) an alternative mechanism is required (the difference inverts). The prediction that chain architecture is a trajectory moderator is falsified under outcomes (b) and (c).

---

## Power-index measurement extension

Beyond the five forward predictions, a parallel extension is to compute the Shapley-Shubik power index (Shapley & Shubik, 1954) and the Banzhaf index (Banzhaf, 1968) for additional protocols beyond the Tally-sourced 5-protocol partial-sample reported in Supplementary File S11. The current partial sample shows Shapley-Shubik HHI tracking voting-HHI with Pearson r = 0.999 across simple-majority quorum (per S11); the extension target is Snapshot-sourced protocols (DIMO, LDO, WXM) where complete delegate-by-delegate weight data must be reconstructed from per-proposal vote-weight distributions. Recent game-theoretic results (Kiayias et al., 2025) indicate that Shapley-based reward distributions achieve bounded Price of Stability (4/3; an efficiency-loss bound on equilibrium outcomes relative to the welfare-optimal allocation) in oceanic staking models while inherently resisting Sybil stake-splitting attacks, indicating that this measurement extension is both theoretically grounded and computationally feasible for the sample sizes in the current dataset.

## Cross-references

- Section 5.8 Future Research (main paper)
- Supplementary File S5 (pipeline specification; replication-repository README and pre-registration DOI integration)
- Supplementary File S11 (power-index calculations for the 5 Tally-sourced protocols)

## References (main-paper bibliography continues to apply)

See main paper bibliography for: Shapley & Shubik (1954); Banzhaf (1968); Kiayias et al. (2025); Fritsch et al. (2024).
