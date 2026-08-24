# S0: Canonical Statistics Ledger

Single source of truth for all statistics cited in the B2 main text. Update this file first when replication outputs change; then sync PAPER.md. This ledger reflects the final-version cross-section (post-exclusion N=52; covariate-complete powered model N=50; balanced sector contrast N=15/15) and the evidence-traced insider classification of record (Section 3.4). Reconciled 2026-06-03 to the DEC-209 of-record (PAPER.md): the allocation battery moved to the N=50 fuller sample, the sector headline is the voter-inclusive pass-through treatment (Cohen's d = 0.65, not the prior d = 1.05), HHI-Gini is r = 0.52 (N = 48), and insider retention is rho = 0.44 (N = 39). A follow-up 2026-06-03 pass corrected the S10 five-specification PCA-robustness row to the 2026-06-01 post-CEX-audit recompute (Spec A p = 0.011, d = 1.05 as the superseded inconsistent-staking spec; Spec B at the margin), which the initial reconciliation had left at the stale pre-audit Spec A p = 0.029 / Spec B p = 0.039 values. A further 2026-06-03 pass applied the insider-allocation re-code under the documented token-generation-event (TGE) convention (Anyone 0 to 10, Gnosis 0 to 95.82, Aave 0 to 18.75; Helium footnoted at zero TGE allocation, its roughly 34 percent cumulative HNT emission share to HST holders reported as an ongoing emission share rather than re-coded): the allocation null is unchanged in status (Pearson r = 0.09, p = 0.55; Spearman rho = 0.19, p = 0.18; TOST p = 0.02), team allocation is r = -0.03, the joint launch-design block is F(3, 41) = 0.60, p = 0.62 (4.2 percent), and the temporal-endpoint corroboration is r = -0.14 (N = 13). Prior r = 0.10 / -0.02 / -0.11 and the 4.6 percent block values are superseded. Prior values are superseded, not historical-of-record.

**Snapshot date:** holder lists collected March to May 2026 (a March 2026 baseline cohort, extended with cohort-expansion snapshots through May 2026 as the set grew to 52; per Section 3.3); Table 8 voting data per protocol notes in Section 3.5.

**Table-number note (2026-07-10):** table cross-references in this ledger follow the 2026-06-30 production renumbering (sequential Tables 1 to 10); the pre-renumber labels this ledger previously carried (Table 5 Model 4; Table 6; the old Table 7 per-period table) were corrected to Tables 7, 8, and 10 on this date.

---

## Sample sizes

| Analysis | N | Notes |
|---|---:|---|
| Full cross-section (Table 3) | 52 | All protocols with post-exclusion holding HHI |
| Bivariate allocation battery | 50 | Protocols with initial insider allocation data (of-record N=50; r=0.09) |
| Covariate-complete powered model (Table 7, the powered specification) | 50 | Sector + revenue intensity + maturity; 12.5 observations per predictor |
| Retention specification (alternative Model 4) | 50 | HONEY carries a classification-of-record retention value (A7) |
| DePIN vs DeFi Mann-Whitney (balanced sector contrast, of record) | 15 / 15 | 30 protocols total |
| Full-frame DePIN vs DeFi Mann-Whitney | varies | All sector-classified DePIN vs DeFi protocols in the cross-section |
| Insider count fraction vs HHI (primary retention) | 39 | Established-protocol cohort |
| Non-insider HHI tautology check | 34 | Excludes 3 zero-insider protocols |
| Subsidy ratio (non-zero either metric) | 23 | Primary subsidy cross-section |
| Subsidy ratio (excluding Livepeer) | 22 | |
| Subsidy ratio (Token Terminal robustness) | 20 | |
| Voting-HHI comparison (Table 8) | 18 | Protocols with sufficient governance data |
| HHI-Gini correlation | 48 | Governance-token-measured post-exclusion sample |
| Median inflation-factor sample | 32 | Protocols with complete pre-exclusion and post-exclusion data |

---

## Headline findings (canonical values)

### 1. Allocation null (covariate sweep)

- **Insider allocation (primary):** Pearson r = 0.09, p = 0.55, N = 50 (Spearman rho = 0.19, p = 0.18; TOST equivalent to zero within the powered |r| = 0.38 envelope, p = 0.02)
- Team allocation: r = -0.03, p = 0.87, N = 45
- Investor allocation: r = 0.19, p = 0.21, N = 45
- Protocol maturity: r = 0.10, p = 0.49, N = 50
- Circulating-to-total supply ratio: r = 0.03, p = 0.86, N = 31
- MCap-to-FDV ratio: r = 0.21, p = 0.25, N = 33
- Exclusion-adjusted float specification: r = -0.003, p = 0.99, N = 30
- Joint launch-design block (team + investor + maturity): F(3, 41) = 0.60, p = 0.62, explains 4.2 percent of HHI variance
- **Do not cite:** r = 0.18, p = 0.28 (incorrect legacy value; removed from literature section)

### 2. Insider wallet retention (primary)

- Insider count fraction in top-10 vs HHI: Spearman rho = 0.44, p = 0.005, N = 39
- LOO robust: significant in 39/39 iterations
- Within-sector partial rank correlation (controls for architectural sector): r = 0.47, p = 0.005, N = 34

### 3. Non-insider HHI tautology check (secondary)

- Non-insider HHI (count): Spearman rho = 0.544 (reported 0.54), p = 0.001, N = 34; OLS p = 0.0024
- Non-insider HHI (balance variant): not significant (p approximately 0.060)

### 4. DePIN vs DeFi sector contrast

- Mean HHI: DePIN 0.067 vs DeFi 0.026 (ratio approximately 2.6)
- **Headline test (balanced sector contrast, of record; voter-inclusive staking pass-through treatment):** Mann-Whitney p = 0.028, Cohen's d = 0.65, N = 15/15; marginal mean-based label-permutation p approximately 0.08 (heavy-tail signature of a single DeFi-side vote-escrow bloc, so the rank-based Mann-Whitney is the primary inference)
- **Uniform staking-aggregation exclusion (robustness check):** Mann-Whitney p = 0.018 (U = 174), Cohen's d = 0.75; significant on every test
- **Prior inconsistent-treatment specification (reframed, NOT the headline):** Mann-Whitney p = 0.011, Cohen's d = 1.05, reported as inflated by an inconsistent cross-sector staking treatment
- LOO (uniform-exclusion robustness): significant in 30/30 iterations; per-iteration p 0.006 to 0.031, Cohen's d 0.68 to 0.92
- Permutation test (100,000 reassignments, uniform exclusion): p = 0.009
- Bootstrap (10,000 resamples, uniform exclusion): 95% mean-difference CI [0.010, 0.081] HHI points; Cohen's d 95% CI [0.40, 1.52], strictly excluding zero
- **Full-frame (15 DePIN vs all 24 DeFi):** directionally consistent; significance is sensitive to the staking-aggregation treatment (Section 4.6.2)
- **Five-specification PCA robustness (S10; recomputed 2026-06-01 post-CEX-audit):** direction (Cohen's d positive) holds under all five specifications. Spec A (canonical 5-class) is the prior inconsistent-treatment specification at Mann-Whitney p = 0.011, Cohen's d = 1.05 (reframed-inflated, not the headline; the of-record significant value is the consistent staking-aggregation treatment, d = 0.75, p = 0.018); Spec B (drop Class 5, CEX custody retained) attenuates to a medium effect (Cohen's d approximately 0.62) at the margin of conventional significance (Mann-Whitney p approximately 0.05, just non-significant under the most complete exchange identification, significant under a narrower definition at p approximately 0.034); Specs C through E lose significance at progressively reduced strictness. Significance is load-bearing on the full 5-class typology
- **Powered model (Table 7; N = 50):** DePIN coefficient positive and significant; log-HHI p = 0.0107 (maturity-spec anchor); untransformed-HHI p = 0.019; clears the 12.5-observations-per-predictor floor
- **Six-scheme insider-classification robustness (N = 50):** DePIN sector coefficient positive and significant under all six schemes; two-sided p ranges keyword-floor 0.0013 / reviewed-safe 0.0037 / classification-of-record (v4_traced) 0.0050 / reviewed 0.0054 / baseline 0.0072 / most-permissive 0.0082; all below 0.01. The insider-retention regressor itself is not significant under any scheme. Per-scheme estimates in S22.

### 5. Subsidy ratio

- **With Livepeer (N = 23):** Pearson r = 0.62, p = 0.002
- **Excluding Livepeer (N = 22):** Pearson r = 0.07, p = 0.76
- Livepeer subsidy ratio = 88.5x (3.5-sigma outlier; alone drives the inclusive correlation)
- Token Terminal robustness (N = 20): r = 0.12, p = 0.61
- **Do not mix:** N = 25 appears in Table 5 for the broader covariate battery including zero-subsidy protocols

### 6. Delegation amplification (Table 8)

- Sample: **18 protocols** (Table 8); thirteen amplify
- Amplifying protocols: ratios 2.5x to 25.6x; mean approximately 6.8x, median 4.4x
- **Five dispersion exceptions:** ENS 0.48x; GMX 0.87x; HNT 0.26x to 0.39x; JUP 0.12x (most-extreme dispersion outlier); **LPT 0.27x (the most pronounced DePIN governance disperser; orchestrator bloc-voting HHI 0.0535 vs holding HHI 0.198868, the cross-section maximum)**
- ve-token class (separate from Table 8): Curve approximately 15x; Balancer approximately 21x; Frax approximately 11.4x

### 7. PCA exclusion methodology

- 133 address exclusions across 38 protocols (full cross-section); 125 exclusions across 36 protocols on the balanced sector-contrast subsample
- Median HHI inflation factor 2.3x (across 32 protocols with complete data); maximum approximately 18x (RENDER)
- A 2026 exchange-custody completion audit (Nansen entity labels) excluded an additional 64 centralized-exchange deposit wallets across 21 protocols, reflected in the post-exclusion HHIs; see Supplementary File S13.

### 8. Gini vs HHI

- HHI-Theil Pearson r = 0.77; HHI-Gini Pearson r = 0.52, p < 0.001, N = 48
  - **Provenance footnote (added 2026-06-27; pending a post-audit Theil recompute):** the two legs differ in provenance. The **HHI-Gini r = 0.52 (N = 48)** leg is reviewer-citable: it reproduces from the of-record per-token metrics in `exhibits/price_performance_audit/b2_price_performance_dataset.csv` (recomputed Pearson r = 0.507 over the N = 50 non-null pairs, about 0.52 at the governance-token-measured N = 48 cut; independent auto-verify b0d461e8 recomputed r = 0.5066). The **HHI-Theil r = 0.77** leg is provisional and pre-audit: it is the internal correlation of the pre-audit `exhibits/theil_atkinson_2026-05-17.csv` exhibit (recomputed r = 0.770 over its N = 45 rows, on the exhibit's own stale HHI column), and it was NOT re-derived in the 2026-06-03 reconciliation that updated HHI-Gini. No post-audit per-token Theil is committed anywhere: the `theil_post` values in both that exhibit and `b2_price_performance_dataset.csv` are the same stale pre-audit values (they match token-for-token for 39 of 40), and joining those stale Theil values to the of-record HHIs gives r = 0.59 (N = 40), not 0.77, so the 0.77 holds only within the stale exhibit's own (pre-audit) HHI column. A faithful post-audit HHI-Theil recompute needs the March-to-May post-exclusion holder distributions, which are not retained (the per-token `*_holders.csv` files are gone; a fresh re-pull would be a different-date snapshot under a re-derived exclusion classification, not a reproduction). The N = 48 above is the HHI-Gini sample; the HHI-Theil N is 45. Until a post-audit Theil recompute, cite the HHI-Theil leg as the pre-audit exhibit value (N = 45) or rely on the HHI-Gini leg, which reproduces. The qualitative rank-stability and metric-non-substitutability conclusion is unaffected (it rests on the HHI-Gini reproduction and the near-zero voting-axis inequality-metric correlation). Cross-references: KEY_FINDINGS F-B2-36 reproducibility note and DATA_REGISTRY (both 2026-06-27); the full recipe and the missing-distributions search are in the B2 theil_atkinson exhibit-regen handoff-back. PAPER.md still carries the unqualified 0.77 / N = 48 (manuscript-of-record, under review): amending the manuscript headline is held for the author plus the recompute. **Status (2026-07-10): author adopted option (b), footnote-pending-recompute.** The PAPER.md Section 4.6.3 rank-stability sentence now carries per-leg provenance (Theil = pre-audit exhibit value at N = 45; Gini legs stated from the of-record data) and the paragraph gained a provenance note; the unqualified 0.77 / N = 48 no longer appears in the living manuscript (the in-press Frontiers record is unchanged until the next version). Same-session independent recompute confirmed every leg from the committed CSVs: exhibit-internal r(HHI,Theil) = 0.7697 (N = 45); of-record r(HHI,Gini) = 0.5066 (N = 50), 0.517 on the 44-token governance cut, and 0.49 to 0.52 across all 1,225 possible N = 48 two-token cuts (85 of them land within 0.0015 of the previously-cited 0.516, so no unique committed N = 48 sample exists); stale-join r = 0.5932 (N = 40, dataset theil_post) and 0.4417 (N = 41, exhibit join); theil_post identical 39-of-40 between exhibit and dataset (ATH the surviving-distribution recompute); the largest stale-HHI input moves are HYPE -97.7 percent and CRV -91.4 percent, both later-corrected values. The post-audit Theil recompute remains queued behind the holder-distribution re-pull.
- Gini range: 0.65 to 0.98; HHI range: 0.005 to 0.199

### 9. Per-period voting-HHI trajectories (Section 4.5.4.2; Table 10; Figure 5)

- **ALGO** (15 governance periods, commitment-weight HHI): min 0.0096, median 0.0129, max 0.0357. The GP15 value (0.0357) is a post-rewards regime artifact (post-GP14 commitment-volume drop), not concentration drift.
- **GEOD** (9 GIPs, veNFT vote-weight HHI): min 0.0853, median 0.1708, max 0.3216. The 0.3216 peak is GIP-1 (37 voters); no monotonic trend.
- **HNT** (46 substantive proposals, per-proposal HHI, voters >= 5): pre-HIP-141 (n=38) min 0.0367, median 0.0877, max 0.3332; post-HIP-141 (n=8) min 0.4329, median 0.6997, max 0.8655; combined-46 median 0.1014. The post-141 rise is a turnout-collapse artifact (participation fell from the 200-to-1,024-voter range to 5-to-10 voters; Spearman rho between voter count and HHI = -0.73, p < 1e-8), not concentration drift.
- **DRIFT**: no dated per-period series (on-chain corpus keyed by proposal address without timestamps); 10 substantive proposals show a cross-sectional per-proposal HHI median of 0.266 (range 0.089 to 0.522). Reported cross-sectionally, not as a trajectory.
- Source series (in-repo, `b2/paper/analysis_n52_2026-05-29/voting_timeseries/`): `ALGO_voting_hhi_series.json`, `GEOD_voting_hhi_series.json`, `HNT_per_proposal_turnout.csv`, `DRIFT_full_corpus_onchain.json`. Generator: `b2/paper/analysis_n52_2026-05-29/voting_timeseries/b2_voting_timeseries_reproduce_2026-06-03.py` (self-contained: reads the committed files in that directory, no live API). Plotted in Figure 5; summarized in Table 7.

---

## Reporting conventions

- Use **associative** language: "is associated with," "is consistent with," not "predicts" or "causes" unless in the falsifiable forward-prediction section.
- When citing insider findings: lead with **rho = 0.44, N = 39**; note the tautology check (rho = 0.544) as secondary confirmation.
- When citing sector tests: lead with **Cohen's d = 0.65, Mann-Whitney p = 0.028** for the balanced DePIN-vs-DeFi contrast under the voter-inclusive staking pass-through treatment of record; report the uniform staking-aggregation exclusion (**d = 0.75, p = 0.018**) as the robustness check and the prior inconsistent-treatment **d = 1.05** as reframed-inflated, not the headline; report the powered-model anchor as **log-HHI p = 0.0107 (N = 50)**.
- When citing subsidy: always pair the Livepeer-inclusive result with the exclusion null.
- When citing the LPT governance disperser: "most pronounced DePIN governance disperser," not "first"; HNT is also a DePIN disperser.
- Insider classification of record: v4_traced (Section 3.4).
