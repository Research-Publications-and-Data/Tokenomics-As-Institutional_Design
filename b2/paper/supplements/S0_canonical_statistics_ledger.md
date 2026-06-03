# S0: Canonical Statistics Ledger

Single source of truth for all statistics cited in the B2 main text. Update this file first when replication outputs change; then sync PAPER.md. This ledger reflects the final-version cross-section (post-exclusion N=52; covariate-complete powered model N=50; balanced sector contrast N=15/15) and the evidence-traced insider classification of record (Section 3.4).

**Snapshot date:** March 2026 (holder lists); Table 6 voting data per protocol notes in Section 3.5.

---

## Sample sizes

| Analysis | N | Notes |
|---|---:|---|
| Full cross-section (Table 3) | 52 | All protocols with post-exclusion holding HHI |
| Bivariate allocation battery | 50 | Protocols with initial insider allocation data (of-record N=50; r=0.10) |
| Covariate-complete powered model (Table 5, Model 4) | 50 | Sector + revenue intensity + maturity; 12.5 observations per predictor |
| Retention specification (alternative Model 4) | 50 | HONEY carries a classification-of-record retention value (A7) |
| DePIN vs DeFi Mann-Whitney (balanced sector contrast, of record) | 15 / 15 | 30 protocols total |
| Full-frame DePIN vs DeFi Mann-Whitney | varies | All sector-classified DePIN vs DeFi protocols in the cross-section |
| Insider count fraction vs HHI (primary retention) | 37 | Established-protocol cohort |
| Non-insider HHI tautology check | 34 | Excludes 3 zero-insider protocols |
| Subsidy ratio (non-zero either metric) | 23 | Primary subsidy cross-section |
| Subsidy ratio (excluding Livepeer) | 22 | |
| Subsidy ratio (Token Terminal robustness) | 20 | |
| Voting-HHI comparison (Table 6) | 18 | Protocols with sufficient governance data |
| HHI-Gini correlation | 44 | Governance-token-measured post-exclusion sample |
| Median inflation-factor sample | 32 | Protocols with complete pre-exclusion and post-exclusion data |

---

## Headline findings (canonical values)

### 1. Allocation null (covariate sweep)

- **Insider allocation (primary):** Pearson r = 0.07, p = 0.68, N = 37
- Team allocation: r = -0.08, p = 0.62, N = 37
- Investor allocation: r = 0.14, p = 0.39, N = 37
- Protocol maturity: r = 0.02, p = 0.92, N = 38
- Circulating-to-total supply ratio: r = 0.03, p = 0.86, N = 31
- MCap-to-FDV ratio: r = 0.21, p = 0.25, N = 33
- Exclusion-adjusted float specification: r = -0.003, p = 0.99, N = 30
- **Do not cite:** r = 0.18, p = 0.28 (incorrect legacy value; removed from literature section)

### 2. Insider wallet retention (primary)

- Insider count fraction in top-10 vs HHI: Spearman rho = 0.48, p = 0.003, N = 37
- LOO robust: significant in 37/37 iterations

### 3. Non-insider HHI tautology check (secondary)

- Non-insider HHI (count): Spearman rho = 0.544 (reported 0.54), p = 0.001, N = 34; OLS p = 0.0024
- Non-insider HHI (balance variant): not significant (p approximately 0.060)

### 4. DePIN vs DeFi sector contrast

- Mean HHI: DePIN 0.067 vs DeFi 0.026 (ratio approximately 2.6)
- **Headline test (balanced sector contrast, of record):** Mann-Whitney p = 0.011, Cohen's d = 1.05, N = 15/15
- LOO: significant in 30/30 iterations
- Permutation test (100,000 reassignments): p = 0.004
- Bootstrap 95% CI on mean difference: [0.016, 0.070] HHI points; Cohen's d 95% CI [0.55, 1.72]
- **Full-frame Mann-Whitney (all sector-classified DePIN vs DeFi):** p = 0.0172, Cohen's d = 1.052
- **Five-specification PCA robustness (S10):** significance holds under the canonical 5-class typology (Spec A p = 0.029) and Drop-Class-5 (Spec B p = 0.039); direction (Cohen's d positive) holds under all five specs; significance is load-bearing on the full typology
- **Powered model (Table 5, Model 4; N = 50):** DePIN coefficient positive and significant; log-HHI p = 0.0107 (maturity-spec anchor); untransformed-HHI p = 0.019; clears the 12.5-observations-per-predictor floor
- **Six-scheme insider-classification robustness (N = 50):** DePIN sector coefficient positive and significant under all six schemes; two-sided p ranges keyword-floor 0.0013 / reviewed-safe 0.0037 / classification-of-record (v4_traced) 0.0050 / reviewed 0.0054 / baseline 0.0072 / most-permissive 0.0082; all below 0.01. The insider-retention regressor itself is not significant under any scheme. Per-scheme estimates in S22.

### 5. Subsidy ratio

- **With Livepeer (N = 23):** Pearson r = 0.62, p = 0.002
- **Excluding Livepeer (N = 22):** Pearson r = 0.07, p = 0.76
- Livepeer subsidy ratio = 88.5x (3.5-sigma outlier; alone drives the inclusive correlation)
- Token Terminal robustness (N = 20): r = 0.12, p = 0.61
- **Do not mix:** N = 25 appears in Table 5 for the broader covariate battery including zero-subsidy protocols

### 6. Delegation amplification (Table 6)

- Sample: **18 protocols** (Table 6); thirteen amplify
- Amplifying protocols: ratios 2.5x to 25.6x; mean approximately 6.8x, median 4.4x
- **Five dispersion exceptions:** ENS 0.48x; GMX 0.87x; HNT 0.26x to 0.39x; JUP 0.12x (most-extreme dispersion outlier); **LPT 0.27x (the most pronounced DePIN governance disperser; orchestrator bloc-voting HHI 0.0535 vs holding HHI 0.198868, the cross-section maximum)**
- ve-token class (separate from Table 6): Curve approximately 15x; Balancer approximately 21x; Frax approximately 11.4x

### 7. PCA exclusion methodology

- 133 address exclusions across 38 protocols (full cross-section); 125 exclusions across 36 protocols on the balanced sector-contrast subsample
- Median HHI inflation factor 2.3x (across 32 protocols with complete data); maximum approximately 18x (RENDER)
- A 2026 exchange-custody completion audit (Nansen entity labels) excluded an additional 64 centralized-exchange deposit wallets across 21 protocols, reflected in the post-exclusion HHIs; see Supplementary File S13.

### 8. Gini vs HHI

- HHI-Theil Pearson r = 0.77; HHI-Gini Pearson r = 0.58, p < 0.001, N = 44
- Gini range: 0.52 to 0.99; HHI range: 0.005 to 0.199

---

## Reporting conventions

- Use **associative** language: "is associated with," "is consistent with," not "predicts" or "causes" unless in the falsifiable forward-prediction section.
- When citing insider findings: lead with **rho = 0.48, N = 37**; note the tautology check (rho = 0.544) as secondary confirmation.
- When citing sector tests: lead with **p = 0.011, d = 1.05** for the balanced DePIN-vs-DeFi contrast of record; report the powered-model anchor as **log-HHI p = 0.0107 (N = 50)**; note the full-frame Mann-Whitney (p = 0.0172, d = 1.052) when reporting the unbalanced contrast.
- When citing subsidy: always pair the Livepeer-inclusive result with the exclusion null.
- When citing the LPT governance disperser: "most pronounced DePIN governance disperser," not "first"; HNT is also a DePIN disperser.
- Insider classification of record: v4_traced (Section 3.4).
