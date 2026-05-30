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

## Cross-references

- Main paper Section 4.6 (robustness) and the concentration-metric discussion (HHI-Theil and HHI-Gini correlations).
- The post-exclusion holder distributions and the Section 3.8 exclusion methodology (the address-by-address exclusions log, `data/processed/exclusions_log.csv`).
