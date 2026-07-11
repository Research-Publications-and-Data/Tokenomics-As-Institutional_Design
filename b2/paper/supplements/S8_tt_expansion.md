# Supplementary File S8: Subsidy-ratio robustness (Token Terminal specification and multivariate models)

**Date:** 2026-07-10 (replaces the 2026-04-02 Token Terminal expansion note; the superseded content is retained in Section 5 below)
**Status:** Robustness documentation for the manuscript's subsidy-concentration analysis (primary specification: merged non-zero subsidy cross-section, N = 23, Section 4.4 of the manuscript)

---

## 1. Purpose and manuscript attributions

The manuscript cites this file for three things:

1. **The Token Terminal (TT) robustness specification**: "A robustness check using the Token Terminal subsidy_ratio (N = 20 protocols with non-null Token Terminal revenue and incentives data) is consistent with the null at cross-sector Pearson r = 0.12 (p approximately 0.61)" (manuscript Section 4.6 robustness paragraph, and the Figure 7 caption: "The Token Terminal robustness sample (N = 20, Supplementary File S8) is consistent with the null at r = 0.12").
2. **The multivariate subsidy models with sector controls** ("multivariate subsidy models with sector controls (S8)", manuscript Section 4.6.3): OLS of post-exclusion holding HHI on subsidy ratio plus a DePIN sector indicator, with HC3 robust standard errors, on the 23-protocol non-zero-subsidy sample, with and without Livepeer.
3. **The merged-sample methodology footnote**: the aggregation-by-preference rule that combines TT subsidy_ratio with the on-chain (OC) emission/fee fallback to produce the merged sample (N = 26 across both methodologies at the of-record vintage; N = 23 protocols with non-zero subsidy under either metric).

Sections 2 through 4 document each in turn, with derivation provenance and reproduction status against the committed data. Section 5 retains the superseded 2026-04-02 mixed-regime expansion for the record.

---

## 2. Token Terminal robustness specification (N = 20; r = 0.12, p approximately 0.61)

### 2.1 Membership rule

The TT robustness sample is: **all protocols in the regression frame with a non-null Token Terminal subsidy_ratio (equivalently, non-null TT revenue and incentives data), including protocols whose measured TT subsidy is exactly zero, and a non-null post-exclusion holding HHI.** Subsidy_ratio is defined as annual token incentives divided by annual protocol revenue (incentives_annual_usd / revenue_annual_usd). The statistic is the cross-sector Pearson correlation of subsidy_ratio with post-exclusion holding HHI.

Two rules that look similar do NOT produce this sample:

- Filtering on `revenue_source` containing `token_terminal` gives N = 17 (recomputed this revision: r = 0.1303, p = 0.6181). That filter wrongly drops protocols whose subsidy_ratio is populated but whose revenue figure was sourced elsewhere (in the current frame: Hivemapper `b3_s2r_derived`, io.net `io_net_blog_estimate`, Hyperliquid `public_buyback_data_jan_2026`).
- Dropping the explicit zeros gives N = 17 as well (a different 17). The three zeros in the N = 20 sample (MakerDAO, Maple Finance, Arbitrum) are genuine measured zero-incentive observations and are retained; they are the same three protocols the manuscript's merged-sample footnote describes as "excluded" when moving from the merged N = 26 to the non-zero N = 23.

### 2.2 Result of record and derivation source

- **Of-record values:** N = 20, Pearson r = 0.12, p = 0.608 (reported in the manuscript body as p approximately 0.61).
- **Derivation source:** the values entered the manuscript in workflow-clone commit `46d79ee03` (2026-05-21, "B2 R2 cycle 6 finalization"), whose commit message records the cascade "Token Terminal subsidy_ratio N = 19 to 20; TT body r = 0.097 to 0.12 + p = 0.69 to 0.61; Table 5 TT row r = 0.10 to 0.12 + p = 0.674 to 0.608" as a live recompute from the then-current `data/processed/regression_data_april2026.csv`. No standalone analysis script or results JSON for this leg was committed at the time; the reproduction below closes that gap.

### 2.3 Reproduction status (recomputed this revision)

**The of-record values reproduce exactly from committed data at the of-record vintage.** Applying the Section 2.1 rule to `data/processed/regression_data_april2026.csv` as committed in this repository at commit `83a1649` (2026-05-19, the frame vintage on which the 2026-05-21 finalize cascade was computed) gives:

- N = 20, Pearson r = 0.1222, p = 0.6079

which rounds to the published r = 0.12, p = 0.61 (Table row value 0.608). Recomputed by the S8 author from the committed CSV (scipy pearsonr); membership and per-protocol values below.

**The same rule applied to the CURRENT committed frame gives a larger sample, not N = 20.** The frame has since expanded to the N = 52 cross-section, and TT/fee-based subsidy coverage grew with it. On the current committed dataset (`data/processed/regression_data_april2026.csv`, current head; identical values in the workflow-clone exhibit `exhibits/price_performance_audit/b2_price_performance_dataset.csv`), the rule gives:

- N = 29, Pearson r = 0.1179, p = 0.5425 (recomputed this revision)

The conclusion the manuscript draws from this leg (a cross-sector null; r consistent with approximately 0.12) is unchanged on the expanded sample; the N = 20 / p = 0.61 citation is the of-record vintage statistic, pinned and reproduced above.

### 2.4 N = 20 membership (of-record vintage, commit `83a1649`)

Extracted from the committed vintage CSV; subsidy_ratio is TT incentives/revenue; HHI is the post-exclusion holding HHI as of that vintage (several HHIs were corrected later by the exchange-custody completion audit; the current-frame recompute in Section 2.3 uses the corrected values).

| Protocol | Category | TT subsidy ratio | HHI (vintage) |
|---|---|---:|---:|
| The Graph | Infrastructure | 49.8767 | 0.032983 |
| IoTeX | DePIN | 39.0514 | 0.080958 |
| Filecoin | DePIN | 19.1785 | 0.022086 |
| Pokt Network | DePIN | 7.6362 | 0.089859 |
| Optimism | Infrastructure | 7.5646 | 0.009281 |
| Hivemapper | DePIN | 5.4600 | 0.017589 |
| Uniswap | DeFi | 3.4372 | 0.009784 |
| Polygon | Infrastructure | 2.5879 | 0.034750 |
| Curve | DeFi | 2.2951 | 0.014418 |
| Compound | DeFi | 1.1354 | 0.009223 |
| io.net | DePIN | 0.4000 | 0.125136 |
| Aave | DeFi | 0.3707 | 0.012790 |
| Aethir | DePIN | 0.3550 | 0.094764 |
| Ether.Fi | DeFi | 0.2396 | 0.041725 |
| Lido | DeFi | 0.0761 | 0.007718 |
| GMX | DeFi | 0.0061 | 0.064722 |
| Hyperliquid | DeFi | 0.0010 | 0.005158 |
| MakerDAO | DeFi | 0.0000 | 0.040408 |
| Maple Finance | DeFi | 0.0000 | 0.024243 |
| Arbitrum | Infrastructure | 0.0000 | 0.011914 |

Composition: 10 DeFi, 4 Infrastructure, 6 DePIN. The three explicit zeros (MakerDAO, Maple Finance, Arbitrum) are retained per the membership rule.

---

## 3. Multivariate subsidy models with sector controls

### 3.1 Specification and provenance

OLS of post-exclusion holding HHI on the merged subsidy ratio (TT preferred, OC fallback; Section 4 rule) and a DePIN sector indicator, HC3 heteroskedasticity-robust standard errors, on the 23-protocol non-zero-subsidy sample, estimated with and without Livepeer. Committed script: `b2/paper/supplements/subsidy_multivariate_2026-05-19.py` (input: `data/processed/regression_data_april2026.csv`). Committed results: `b2/paper/supplements/subsidy_multivariate_2026-05-19.csv` (introduced in repository commit `949cfb3`, 2026-05-19; last regenerated against the corrected frame in commit `ce4f527`, 2026-06-03). An OC-preferred field-selection sensitivity companion is committed at `b2/paper/supplements/subsidy_multivariate_oc_sensitivity_2026-05-19.py` (script only; no committed output table).

### 3.2 Results (quoted from the committed results CSV)

| Spec | N | subsidy beta | subsidy t | subsidy p | DePIN beta | DePIN t | DePIN p | Adj R^2 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1. Subsidy only (all) | 23 | 0.001333 | 1.079 | 0.2806 | | | | 0.3554 |
| 2. Subsidy only (no LPT) | 22 | 0.000162 | 0.194 | 0.8465 | | | | -0.0452 |
| 3. Subsidy + DePIN (all) | 23 | 0.001122 | 0.923 | 0.3559 | 0.035044 | 2.173 | 0.0298 | 0.4855 |
| 4. Subsidy + DePIN (no LPT) | 22 | -0.000035 | -0.082 | 0.9345 | 0.034661 | 2.886 | 0.0039 | 0.2542 |

These are the values the manuscript's multivariate paragraph reports: with all 23 protocols the DePIN indicator is significant (p = 0.030) while subsidy is not (p = 0.36; Adj R-squared = 0.49); excluding Livepeer the subsidy coefficient is strongly non-significant (p = 0.93) while the DePIN indicator is significant (p = 0.004).

### 3.3 Reproduction status

**Reproduces exactly from the current committed dataset.** An independent re-estimation for this revision (statsmodels OLS, HC3, same membership rule, run against the current committed `data/processed/regression_data_april2026.csv` and, identically, the workflow-clone `b2_price_performance_dataset.csv`) returns the same coefficients, t statistics, p-values, and adjusted R-squared to all reported digits (Spec 3: subsidy beta 0.001122, p 0.3559; DePIN beta 0.035044, p 0.0298; Adj R^2 0.4855; Spec 4: subsidy beta -0.000035, p 0.9345; DePIN beta 0.034661, p 0.0039; Adj R^2 0.2542).

Interpretation (as in the manuscript): with Livepeer included, neither model assigns the subsidy ratio a significant coefficient once sector is controlled; without Livepeer the subsidy coefficient is indistinguishable from zero while DePIN sector membership remains significant. The apparent subsidy-HHI association is absorbed by sector membership absent the single extreme observation.

---

## 4. Broader merged sample (manuscript Section 4.4 restated)

### 4.1 Aggregation-by-preference rule

The merged cross-section aggregates the two subsidy methodologies by preference: the Token Terminal subsidy_ratio is used where available; the on-chain emission/fee subsidy_ratio_onchain is used as fallback where TT data is unavailable but on-chain data is present. At the of-record vintage this yields N = 26 across both methodologies (20 TT + 6 OC-fallback: DIMO, GEODNET, Helium, Livepeer, Morpheus AI, Render; verified against the committed `83a1649` vintage). The non-zero-under-either-metric sub-sample is N = 23, dropping the three explicit TT zeros (MakerDAO, Maple Finance, Arbitrum). On the current expanded committed frame the same rule yields a union of N = 35 (29 TT + the same 6 OC-fallback) with the identical N = 23 non-zero sub-sample; the twelve zero-subsidy protocols in the current union are the manuscript's N = 35 zero-inclusive robustness sample.

### 4.2 Results (recomputed this revision from the current committed dataset)

All values below are the S8 author's recomputation from `data/processed/regression_data_april2026.csv` (current head; identical from the workflow-clone `b2_price_performance_dataset.csv`), matching the manuscript's Section 4.4 statements:

| Sample | N | Statistic | Value | p | Manuscript statement |
|---|---:|---|---:|---:|---|
| Merged non-zero, with Livepeer | 23 | Pearson r | 0.6203 | 0.0016 | r = 0.62, p = 0.002 |
| Merged non-zero, excluding Livepeer | 22 | Pearson r | 0.0676 | 0.7649 | r = 0.07, p = 0.76 |
| Merged non-zero, with Livepeer | 23 | Spearman rho | 0.2628 | 0.2256 | rho = 0.26, p = 0.23 |
| Zero-inclusive, with Livepeer | 35 | Pearson r | 0.6081 | 0.0001 | r = 0.61, p = 0.0001 |
| Zero-inclusive, excluding Livepeer | 34 | Pearson r | 0.0898 | 0.6134 | r = 0.09, p = 0.61 |
| Zero-inclusive, with Livepeer | 35 | Spearman rho | 0.0916 | 0.6006 | rho = 0.09 |

The merged-sample headline (r = 0.62 with Livepeer; r = 0.07 excluding) and the zero-inclusive extension both reproduce to two decimals. Livepeer (subsidy ratio 88.5x on the on-chain basis, revenue_onchain_usd = 838,701 USD; post-exclusion HHI 0.198868, both from the committed dataset) is the single high-leverage observation driving the inclusive correlation; every specification excluding it is a clean null, and the outlier-robust Spearman statistic is non-significant even with Livepeer retained.

---

## 5. Superseded vintage (retained for the record)

The remainder of this section carries, condensed, the content of the prior S8 ("Token Terminal Expansion, Subsidy-Concentration Analysis", dated 2026-04-02), which documented an older N = 22 mixed-regime expansion. It is retained for the record only; it is NOT the specification the manuscript cites as S8, and several of its values are superseded (flags below).

### 5.1 Superseded sample construction (2026-04-02 vintage)

Subsidy ratios for 13 DeFi and Infrastructure protocols were computed from Token Terminal revenue and incentive data using cumulative 35-month values (February 2023 to January 2026); DePIN subsidy ratios used annualized on-chain burn revenue and mint emissions (Dune Analytics). Two DePIN protocols were excluded from that expanded sample: Livepeer (subsidy ratio 88.5x, the 3.5-sigma outlier) and Render (7.63x, cross-chain measurement complexity). Full cross-sector sample: N = 22 (9 DeFi, 4 Infrastructure, 9 DePIN). Balancer and Hyperliquid were excluded for missing HHI.

**Definitional note (added 2026-07-10):** the 2026-04-02 table's DeFi/Infrastructure "Subsidy Ratio (TT)" column used the bounded incentives share, incentives / (revenue + incentives), not the of-record incentives / revenue ratio (check: Compound 36.5M / (23.0M + 36.5M) = 0.6134, matching the vintage table's 0.614; the of-record frame carries Compound at 1.1354). The two columns are not directly comparable across vintages.

### 5.2 Superseded Table S8-A (protocol-level data, 2026-04-02 vintage, condensed)

| Protocol | Sector | Subsidy ratio (vintage basis) | HHI (vintage) |
|---|---|---:|---:|
| MakerDAO | DeFi | 0.000 | 0.045 |
| Maple | DeFi | 0.000 | 0.024 |
| Jupiter | DeFi | 0.000 | 0.117 |
| Lido | DeFi | 0.115 | 0.019 |
| GMX | DeFi | 0.259 | 0.056 |
| Aave | DeFi | 0.370 | 0.020 |
| Compound | DeFi | 0.614 | 0.028 |
| Curve | DeFi | 0.750 | 0.171 |
| Ether.Fi | DeFi | 0.842 | 0.067 |
| Arbitrum | Infra | 0.000 | 0.012 |
| Optimism | Infra | 0.871 | 0.042 |
| Polygon | Infra | 0.893 | 0.035 |
| The Graph | Infra | 0.982 | 0.036 |
| DIMO | DePIN | 0.330 (on-chain) | 0.038 |
| Helium | DePIN | 1.050 (on-chain) | 0.102 |
| Morpheus AI | DePIN | 1.540 (on-chain) | 0.013 |
| GEODNET | DePIN | 1.610 (on-chain) | 0.133 |
| Hivemapper | DePIN | 5.460 (on-chain) | 0.017 |
| io.net | DePIN | 0.400 (on-chain) | 0.111 |
| Aethir | DePIN | 0.355 (on-chain) | 0.168 |
| Filecoin | DePIN | 21.600 (on-chain) | 0.047 |
| IoTeX | DePIN | 27.800 (on-chain) | 0.106 |

**SUPERSEDED VALUE FLAG (Filecoin):** the 21.6x Filecoin figure above is a stale vintage. The of-record committed dataset carries Filecoin at subsidy_ratio_onchain = 46.05 (the on-chain basis; the value the manuscript cites as the next-highest subsidy ratio in the cross-section after Livepeer) and subsidy_ratio (TT basis) = 19.18. Both verified directly from the committed `b2_price_performance_dataset.csv` / `regression_data_april2026.csv` this revision.

The vintage HHI column also predates the exchange-custody completion audit and subsequent corrections; of-record per-protocol HHIs are in the committed dataset and the S0 canonical statistics ledger.

### 5.3 Superseded Table S8-B (correlations by sector, 2026-04-02 vintage)

| Sample | N | Pearson r | p | Interpretation |
|---|---:|---:|---:|---|
| Full cross-sector | 22 | +0.095 | 0.674 | Null |
| DeFi only | 9 | +0.336 | 0.377 | Null |
| Infrastructure only | 4 | +0.954 | 0.046 | Suggestive (N too small for inference) |
| DePIN only (excl. Livepeer, Render) | 9 | -0.074 | 0.850 | Null |

Spearman rho (full cross-sector) = 0.115, p = 0.610. The vintage notes cautioned that the Infrastructure r = 0.954 at N = 4 is not inferentially meaningful and that the mixed measurement regime (TT accounting metrics for DeFi/Infra; on-chain burn/mint for DePIN) made this an additive robustness check rather than a replacement for the primary on-chain specification. The vintage also recorded: "Aethir revenue: body text updated to $156M (Token Terminal, April 2026) in v14."

The N = 22 mixed-regime expansion result (r = 0.095, p = 0.674) is qualitatively consistent with the of-record TT specification (Section 2) and merged-sample results (Section 4): all are cross-sector nulls once the Livepeer outlier is handled.

---

## 6. Provenance and change note (2026-07-10)

**What changed:** this file previously documented only the 2026-04-02 N = 22 mixed-regime expansion, while the manuscript had moved to citing S8 for the N = 20 TT robustness specification, the multivariate sector-control models, and the merged-sample methodology. This revision re-authors S8 around what the manuscript actually attributes to it and demotes the old content to the superseded-vintage section.

**Grounding of every reported value:**

- Section 2 of-record leg (N = 20, r = 0.12, p = 0.608): no standalone committed analysis script existed for this leg; its documented derivation is the live-recompute record in workflow-clone commit `46d79ee03` (2026-05-21). It is now grounded by direct recomputation in this revision from the committed dataset vintage at repository commit `83a1649` (2026-05-19), reproducing N = 20, r = 0.1222, p = 0.6079 under the stated membership rule.
- Section 2 current-frame values (N = 29, r = 0.1179, p = 0.5425) and the naive-filter contrast (N = 17, r = 0.1303, p = 0.6181): recomputed this revision from the current committed dataset.
- Section 3 model table: quoted from the committed `b2/paper/supplements/subsidy_multivariate_2026-05-19.csv` (regenerated in commit `ce4f527`, 2026-06-03), and independently re-estimated this revision from the current committed dataset with exact agreement.
- Section 4 table: recomputed this revision from the current committed dataset; matches the manuscript's Section 4.4 values to the stated precision.
- Section 5 vintage tables and statistics: quoted from the prior committed S8 (2026-04-02 content); the Compound definitional check (0.6134) recomputed this revision from that table's own revenue/incentives figures.
- Filecoin of-record values (46.05 on-chain; 19.18 TT): read directly from the committed dataset this revision.

**Flagged item (not fully grounded against the current dataset):** the manuscript's parenthetical describing Filecoin (46.05x) as "the next-highest subsidy ratio in the cross-section" after Livepeer is PAPER-sourced. On the current committed dataset, The Graph carries 49.88 in both subsidy columns and IoTeX carries 39.05 on the TT basis, so a naive ranking of the current merged cross-section places The Graph, not Filecoin, second after Livepeer's 88.5x. The Filecoin values themselves (46.05 on-chain; 19.18 TT) are dataset-verified; the ranking phrasing is reported here as the manuscript states it, with this observation recorded for a future editorial pass.

**Reproduction recipe:** load `data/processed/regression_data_april2026.csv` (or the workflow-clone `exhibits/price_performance_audit/b2_price_performance_dataset.csv`); TT leg = Pearson(subsidy_ratio, hhi) over rows with non-null subsidy_ratio and hhi (zeros retained; N = 20 at commit `83a1649`, N = 29 at current head); merged leg = prefer non-null non-zero subsidy_ratio, else non-null non-zero subsidy_ratio_onchain, require non-null hhi (N = 23); multivariate leg = `python3 b2/paper/supplements/subsidy_multivariate_2026-05-19.py`.
