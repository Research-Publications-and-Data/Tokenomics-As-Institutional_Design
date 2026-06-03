# Supplementary File S9: Theil and Atkinson concentration-metric robustness

**Companion to:** B2 paper *Tokenomics as Applied Political Philosophy: Governance Concentration Beyond Token Allocation*, Section 4.6 (robustness) and the metric-choice discussion.

**Question.** Does the cross-protocol rank ordering of governance concentration depend on the choice of concentration measure? The main paper reports the Herfindahl-Hirschman Index (HHI). This supplement recomputes two alternative inequality-and-concentration measures, the Theil index and the Atkinson index (inequality-aversion parameter 0.5), on the same post-exclusion holder distributions, and tests whether the protocol rank ordering is preserved.

---

## Data and method

For each protocol in the post-exclusion concentration-metric cross-section, the top-1,000 holder distribution (after the Section 3.8 five-class protocol-controlled-address exclusion) is used to compute three measures: HHI, the Theil index, and the Atkinson index at inequality-aversion parameter 0.5. Per-protocol values are in `b2/paper/supplements/theil_atkinson_2026-05-17.csv` (columns: `symbol`, `n_post1k`, `n_pca_excluded`, `hhi_post_exclusion`, `gini_post`, `theil_post`, `atkinson_0.5_post`). The cross-section here is N = 45 protocols.

The Theil index is a generalized-entropy inequality measure (sensitive across the full distribution); the Atkinson index encodes explicit inequality aversion. HHI, by contrast, is dominated by top-share squared terms. If the three measures agree on the protocol rank ordering despite weighting the distribution differently, the cross-sectional concentration ranking is robust to metric choice.

---

## Results

Cross-protocol correlation with HHI (N = 45):

| Measure vs HHI | Pearson r | Spearman rho |
|---|---:|---:|
| Theil index | 0.77 | 0.78 |
| Atkinson index (0.5) | 0.41 | 0.64 |

Observed ranges across the cross-section: Theil 0.69 to 6.46; Atkinson(0.5) 0.30 to 0.97.

Rank-stability illustration (the most-concentrated protocols are the same set regardless of measure):

- Top-5 by HHI: MPL, RNDR (Ethereum), HYPE, ATH, AXL.
- Top-5 by Theil: MPL, RNDR (Ethereum), IOTX, ATH, GEOD.
- Top-5 by Atkinson(0.5): MPL, IOTX, RNDR (Ethereum), HNT, JUP.

MPL, RNDR, and ATH appear in the high-concentration tier under every measure; the high-concentration cluster is dominated by the same DePIN and lending protocols regardless of which concentration measure is used.

---

## Interpretation

The Theil index tracks HHI strongly on both the linear (Pearson 0.77) and rank (Spearman 0.78) bases. The Atkinson index, which weights the lower tail of the distribution more heavily, tracks HHI less tightly on the linear basis (Pearson 0.41) but still preserves the protocol rank ordering moderately well (Spearman 0.64), with the same high-concentration protocols at the top.

The correlations are moderate-to-strong rather than perfect because the three measures weight the holder distribution differently: HHI is dominated by top-share squared terms, the Theil index integrates the full generalized-entropy profile, and the Atkinson index is governed by its inequality-aversion parameter. Each therefore carries some independent information about distributional shape while agreeing on the cross-protocol ordering. The bivariate associations reported in the main paper (the sector contrast; the insider-retention significance; the subsidy fragility) rest on the protocol rank ordering, which is preserved under Theil-based and Atkinson-based measurement. Inequality metrics do not substitute for direct concentration measurement, but they confirm that the concentration ranking is not an artifact of the HHI functional form.

---

## Voting-power Gini (within-axis robustness)

The HHI-Gini divergence documented above for holdings also appears, more sharply, on the voting-power axis. The table reports the voting-power Gini alongside the voting HHI for the protocols with sufficient governance data. Snapshot rows are off-chain Snapshot voters over a twelve-month window (top-100 by maximum voting power); tally rows are on-chain top-1,000 delegates by delegated voting weight. Raw values are in `data/raw/voting_hhi.csv`.

| Protocol | Source | Voting HHI | Voting Gini | N voters/delegates |
|---|---|---:|---:|---:|
| UNI  | Snapshot | 0.074 | 0.986 | 1,034 |
| COMP | Snapshot | 0.089 | 0.851 | 138 |
| LDO  | Snapshot | 0.050 | 0.940 | 333 |
| DIMO | Snapshot | 0.228 | 0.595 | 10 |
| WXM  | Snapshot | 0.556 | 0.939 | 73 |
| ARB  | Snapshot | 0.038 | 0.995 | 5,491 |
| AAVE | Tally    | 0.062 | 0.921 | 1,000 |
| COMP | Tally    | 0.109 | 0.980 | 1,000 |
| UNI  | Tally    | 0.027 | 0.956 | 1,000 |
| ARB  | Tally    | 0.034 | 0.948 | 1,000 |
| OP   | Tally    | 0.033 | 0.928 | 1,000 |
| ENS  | Tally    | 0.022 | 0.876 | 1,000 |
| GMX  | Tally    | 0.056 | 0.883 | 1,000 |

Voting-power Gini is near-maximal (median 0.94; only the ten-voter DIMO sample falls below 0.85) and is uncorrelated with voting HHI (Pearson r approximately 0, not significant at this sample size), in contrast to the moderate holding-side HHI-Gini coupling (r = 0.52). A protocol can carry a low, dispersed voting HHI alongside a near-maximal Gini: ENS delegate voting HHI is 0.022 against a Gini of 0.876.

This near-maximal-and-decoupled pattern is expected by construction rather than a substantive finding. Two mechanisms pin the voting Gini high: token-weighted voting power is heavy-tailed, and the truncated top-N sample carries a long thin tail of one-vote participants that the Lorenz curve registers as near-maximal inequality while HHI (top-share squared) registers a non-dominated top. The voting Gini is therefore reported only as a within-axis robustness descriptor, not as a measure comparable across the holding and voting axes: the snapshot voters (top-100), the tally delegates (top-1,000), and the holding Gini's post-exclusion holders (top-1,000) are three different populations at two different depths, and the depth sensitivity is real (the GMX top-100-versus-top-1,000 voting-HHI crossover in Section 4.5.1.1). The practical implication confirms the main-paper stance on a second axis: HHI, not an inequality coefficient, must be the primary voting-concentration measure, and the substitution failure is more severe for voting power than for holdings.

The voting metrics are regenerated by `analysis/b2_voting_hhi_refresh.py` (Snapshot, fixed twelve-month window) and `analysis/b2_tally_refresh.py` (Tally top-1,000 delegates); both compute HHI and Gini over the same top-N share vector via the corrected positive-convention Gini formula.

---

## Cross-references

- Main paper Section 4.6 (robustness) and the concentration-metric discussion (HHI-Theil and HHI-Gini correlations).
- The post-exclusion holder distributions and the Section 3.8 exclusion methodology (the address-by-address exclusions log, `data/processed/exclusions_log.csv`).
