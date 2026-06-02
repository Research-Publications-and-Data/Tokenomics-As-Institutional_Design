# S0: Canonical Statistics Ledger

Single source of truth for all statistics cited in the B2 main text. Update this file first when replication outputs change; then sync PAPER.md. This ledger reflects the final-version cross-section (post-exclusion N=52; covariate-complete powered model N=50; balanced sector contrast N=15/15) and the evidence-traced insider classification of record (Section 3.4).

**Snapshot date:** March 2026 (holder lists); Table 6 voting data per protocol notes in Section 3.5. Final-version reconciliation: 2026-05-31 (insider-allocation, subsidy, amplifying-range, and six-scheme values synced to the post-CEX-cascade of-record; see Session Changes 2026-05-31).

---

## Sample sizes

| Analysis | N | Notes |
|---|---:|---|
| Full cross-section (Table 3) | 52 | All protocols with post-exclusion holding HHI |
| Bivariate allocation battery | 37 | Protocols with initial insider allocation data |
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

---

## Session Changes (2026-05-31, CEX-audit cascade)

A 2026 exchange-custody completion audit (Nansen entity labels plus the 2026-05-29 v4 reclassification) excluded an additional 64 centralized-exchange deposit wallets across 21 protocols, on top of the original-layer 133 PCA exclusions across 38 protocols. The two layers are distinct: the original PCA-exclusion methodology figures (133 / 125 / 38 / median inflation 2.3x) are retained as the original layer; the CEX audit is a separate exchange-custody completion layer reflected in the post-exclusion HHIs (see Supplementary File S13).

Headline statistics cascaded as follows:

- Balanced sector contrast (15/15, of record): Mann-Whitney p 0.020 to 0.011; Cohen's d 0.94 to 1.05; DePIN mean HHI 0.071 to 0.067; DeFi mean HHI 0.031 to 0.026; ratio 2.3 to 2.6.
- Balanced-30 robustness: permutation p 0.012 to 0.004; bootstrap mean-difference 95% CI [0.012, 0.069] to [0.016, 0.070]; Cohen's d 95% CI [0.32, 1.68] to [0.55, 1.72].
- Full-frame Mann-Whitney: p 0.0234 to 0.0172; Cohen's d 0.939 to 1.052.
- Powered model (Table 5, Model 4): maturity-spec log-HHI p 0.0197 to 0.0107; untransformed-HHI p 0.030 to 0.019.
- JUP delegation amplification ratio (voting over holding): 0.043x to 0.12x; JUP remains the most-extreme dispersion outlier.

The CEX-retention sensitivity is now load-bearing: retaining all centralized-exchange wallets collapses the balanced-30 contrast to p = 0.184, d = 0.52 (not significant), whereas excluding them yields p = 0.011, d = 1.05. This reverses the prior "CEX not load-bearing" framing.

## Session Changes (2026-05-31, S0-lags-paper reconciliation)

A §5.5-staleness audit (audit-only workflow) found this ledger lagging the CEX-cascaded manuscript on four headline statistics plus the six-scheme range: the manuscript (abstract, Section 4.4, Section 5.5, conclusion) already carried the post-cascade of-record values while this ledger retained pre-cascade snapshots. The drift direction is the inverse of the usual presumption (the summary was current; the of-record ledger lagged). Synced the ledger to the manuscript of-record. All values are deterministic reproductions on the cascaded frame regression_data_april2026.csv, reconciled against the recompute note b2_regression_recompute_finalize_2026-05-31.md:

- Section 1 insider allocation Pearson: r 0.05 to 0.07, p 0.76 to 0.68 (20 of the 37-protocol cohort had CEX-affected HHI; cohort membership unchanged pre/post; recompute r = 0.0704).
- Section 5 subsidy with-Livepeer: r 0.58 to 0.62, p 0.004 to 0.002 (recompute r = 0.6203, N = 23).
- Section 5 subsidy excl-Livepeer: r 0.06 to 0.07, p 0.80 to 0.76 (recompute r = 0.0676, N = 22).
- Section 6 amplifying-ratio floor: 1.6x to 2.5x (Table 6 Gnosis floor; conclusion and Section 4.5 already at 2.5x).
- Section 4 six-scheme insider-classification p-range (Layer 3): keyword-floor 0.0058 to 0.0013, reviewed-safe 0.0090 to 0.0037, classification-of-record 0.0139 to 0.0050, reviewed 0.0148 to 0.0054, baseline 0.0168 to 0.0072, most-permissive 0.0187 to 0.0082; range "0.0058 to 0.0187, all below 0.02" to "0.0013 to 0.0082, all below 0.01" (strengthens; ordering preserved). Cascaded jointly to PAPER Section 4.4.1 and Supplement S22.

Manuscript stale survivors corrected in the same cycle (the prose cascade had missed them): PAPER Table 4 insider-allocation Pearson cell (0.05/0.76 to 0.07/0.68) and subsidy-excl-Livepeer cell (0.06/0.80 to 0.07/0.76).

Surfaced but NOT applied this cycle (outside authorized scope; deterministic, confirmed by the recompute note, recommended for a follow-up): Supplement S22 Section 3 verification list still carries pre-cascade maturity-spec log-HHI p = 0.0197 (of-record 0.0107), untransformed coefficient +0.035 / p = 0.030 (of-record +0.036 / 0.019), full-frame Mann-Whitney p = 0.0234 / d = 0.939 (of-record 0.0172 / 1.052), and balanced-30 p = 0.0202 / d = 0.940 (of-record 0.0114 / 1.048). PAPER line ~2059 subsidy Spearman rho = 0.20 / p = 0.35 recomputes to 0.26 / 0.23 on the cascaded frame (small drift). The submission docx/pdf and response package remain pre-cascade and require rebuild from the synced PAPER.md per the pending finalize handoff.

## Session Changes (2026-05-31, follow-up: S22 Section 3 + subsidy Spearman applied)

Per author direction, the previously-surfaced S22 Section 3 survivors and the PAPER subsidy Spearman were applied (all deterministic; reconciled against reproduce_results_2026-05-29.json and the recompute note):

- Supplement S22 Section 3: maturity-spec log-HHI p 0.0197 to 0.0107; untransformed coefficient +0.035 / p 0.030 to +0.036 / 0.019; full-frame Mann-Whitney p 0.0234 / d 0.939 to 0.0172 / 1.052; balanced-30 p 0.0202 / d 0.940 to 0.0114 / 1.048.
- PAPER Section 4.6 subsidy Spearman: rho 0.20 / p 0.35 to 0.26 / 0.23 (recompute 0.2628 / 0.2256 on the headline N = 23 hybrid sample; the original 0.20 was a pre-N52-expansion value).

HELD (not applied; method not cleanly reproducible): the paired log-transform on the same PAPER sentence (r = 0.27, p = 0.22) recomputes to r = 0.29, p = 0.17 on the current-frame hybrid, but the original 0.27 / 0.22 does not reproduce exactly from the hybrid, on-chain, or TT-only subsidy columns on any frame, so the of-record log-transform definition is unconfirmed; left as-is pending the original subsidy-correlation script. The substantive claim (non-significant under log transformation) is method-invariant.

Confirmed current, no change: PAPER Section 5.6 "133 address exclusions controlled by protocols themselves across 38 protocols" is the original PCA-exclusion layer (retained; the +64 exchange-custody wallets across 21 protocols are a separately-counted exchange-controlled layer per S13, correctly excluded from this protocol-controlled count). Amplifying-ratio floor 2.5x verified against Table 6 (Gnosis 2.5x is the minimum amplifying ratio; Polkadot 25.6x the maximum).

## Session Changes (2026-06-01, ENS + HNT disperser-ratio empirical-upgrade lag corrected)

Audit (site-propagation cross-check) found two more empirical-upgrade survivors in Section 6 disperser ratios: this ledger lagged the manuscript on ENS and HNT amplification ratios, the same lag class flagged in the 2026-05-31 reconciliation note. Drift direction is the inverse of the usual presumption: PAPER.md (Table 6, Section 4.5.4, abstract, intro) carried the post-empirical-upgrade of-record values; this ledger retained the pre-upgrade Cycle-15 values.

Mechanism: the N=40-to-N=52 empirical upgrade recomputed post-exclusion HOLDING HHIs for both protocols while voting HHIs were unchanged, so the amplification ratios (voting HHI over holding HHI) moved:

- ENS: holding HHI 0.049 (Cycle-15) to 0.0463 (current Table 3); voting HHI unchanged at 0.0225 (replication file exhibits/voting_history_50/voting_hhi_full_history.csv; comparison logs delta 0.0). Ratio 0.45x to 0.48x (0.0225 / 0.0463 = 0.486).
- HNT: holding HHI 0.075 (Cycle-15) to 0.099 (current Table 3; S13 post-exclusion); voting HHI unchanged at 0.0261 to 0.0394 (Solana VSR lockup-weight reconstruction, Section 4.5.4). Ratio 0.35x-0.53x to 0.26x-0.39x (0.0261 / 0.099 to 0.0394 / 0.099 = 0.264 to 0.398).

The other three dispersers (GMX 0.87x, JUP 0.12x, LPT 0.27x) already matched and are unchanged. The pre-upgrade values 0.45x / 0.35x-0.53x remain correct in the frozen historical surfaces (responses/2026-05-17_R2_responses_master.md; versions/2026-05-26_pre_empirical_upgrade.md) and were correctly left as historical-of-record. The site page (papers/governance-concentration/index.html) sidestepped both ratios and is unaffected.
