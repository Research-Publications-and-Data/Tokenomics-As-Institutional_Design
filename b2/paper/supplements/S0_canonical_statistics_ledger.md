# S0: Canonical Statistics Ledger

Single source of truth for all statistics cited in B2 main text. Update this file first when replication outputs change; then sync PAPER.md.

**Snapshot date:** March 2026 (holder lists); Table 7 voting data per protocol notes in Section 3.5.

---

## Sample sizes

| Analysis | N | Notes |
|---|---:|---|
| Full cross-section (Table 4) | 40 | All protocols with post-exclusion HHI |
| Bivariate allocation battery | 37 | Protocols with initial insider allocation data |
| OLS Model 1 (sector dummies) | 38 | |
| OLS Model 2 (+ age, log FDV) | 36 | |
| OLS Model 3 (+ initial insider %) | 35 | |
| DePIN vs DeFi Mann-Whitney (headline) | 15 / 15 | 30 protocols total in sector contrast |
| DePIN sector indicator (Table 5 row) | 30 | DePIN vs non-DePIN indicator test |
| Insider count fraction vs HHI | 37 | Primary insider retention measure |
| Non-insider HHI tautology check (V1, count) | 34 | Excludes 3 zero-insider protocols |
| Non-insider HHI balance (V2) | 34 | Does not survive (p = 0.060) |
| Subsidy ratio (non-zero either metric) | 23 | Primary subsidy cross-section |
| Subsidy ratio (Table 5 full listing) | 25 | Includes zero-subsidy protocols in battery |
| Delegation amplification (Table 7) | 13 | Protocols with sufficient voting data |
| HHI-Gini correlation | 40 | |

---

## Headline findings (canonical values)

### 1. Allocation null

- **Primary:** Pearson r = 0.05, p = 0.76, N = 37 (initial insider allocation % vs post-exclusion HHI)
- Spearman rho = 0.07, p = 0.69, N = 37
- **Do not cite:** r = 0.18, p = 0.28 (incorrect legacy value; removed from literature section)

### 2. Insider wallet retention (primary)

- Insider count fraction in top-10 vs HHI: Spearman rho = 0.48, p = 0.003, N = 37
- LOO robust: significant in 37/37 iterations (rho range 0.45 to 0.55)

### 3. Non-insider HHI tautology check (secondary)

- Non-insider HHI V1 (count): Spearman rho = 0.54, p = 0.001, N = 34
- Non-insider HHI V2 (balance): Spearman rho = 0.33, p = 0.060, N = 34 (not significant)

### 4. DePIN vs DeFi sector contrast

- Mean HHI: DePIN 0.071 vs DeFi 0.031 (ratio 2.3)
- **Headline test:** Mann-Whitney p = 0.020, Cohen's d = 0.94, N = 15/15
- LOO: significant in 30/30 iterations (p range 0.008 to 0.034; d range 0.84 to 1.10)
- Permutation test (100,000 reassignments): p = 0.012
- Bootstrap 95% CI on mean difference: [+0.012, +0.069] HHI points
- **Table 5 DePIN sector indicator row:** Mann-Whitney p = 0.016, N = 30 (different contrast specification; cite explicitly when using Table 5)
- **OLS DePIN coefficient:** Model 1: 0.045, p = 0.012; Model 2: 0.053, p = 0.036; Model 3: 0.043, p = 0.078
- Adjusted R-squared: 0.173 (M1), 0.190 (M2), 0.151 (M3)

### 5. Subsidy ratio

- **With Livepeer (N = 23):** Pearson r = 0.59, p = 0.003
- **Excluding Livepeer (N = 22):** Pearson r = 0.07, p = 0.77
- Spearman on full subsidy sample: rho = 0.20, p = 0.35
- Token Terminal robustness (N = 20): r = 0.12, p = 0.61
- **Do not mix:** N = 25 appears in Table 5 for broader covariate battery including zero-subsidy protocols

### 6. Delegation amplification

- Sample: **13 protocols** (Table 7); not 10
- Nine amplifying protocols: ratios 1.6x to 9.9x; mean approximately 4.9x
- Four dispersion exceptions: ENS 0.45x; GMX 0.87x; HNT 0.35x to 0.53x; JUP 0.057x
- ve-token class: Curve approximately 15x; Balancer approximately 21x (separate from Table 7)

### 7. PCA exclusion methodology

- 133 address exclusions across 38 protocols (125 unique; 5 recur)
- Median HHI inflation factor: 2.3x; maximum approximately 18x (RENDER)

### 8. Gini vs HHI

- Gini range: 0.52 to 0.99; HHI range: 0.005 to 0.199
- Pearson r = 0.59, p < 0.001, N = 40

---

## Reporting conventions

- Use **associative** language: "is associated with," "is consistent with," not "predicts" or "causes" unless in falsifiable forward-prediction section.
- When citing insider findings: lead with **rho = 0.48, N = 37**; note tautology check as secondary confirmation.
- When citing sector tests: lead with **p = 0.020, d = 0.94** for DePIN vs DeFi headline; note Model 3 p = 0.078 when discussing multivariate attenuation.
- When citing subsidy: always pair Livepeer-inclusive result with exclusion null.
