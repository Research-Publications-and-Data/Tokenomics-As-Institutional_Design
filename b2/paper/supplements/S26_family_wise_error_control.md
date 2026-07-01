# Supplementary File S26: Family-Wise Error Control Across the Four-Test Bivariate Battery

This file documents the joint multiple-comparison correction across the paper's four bivariate association tests and reports the full per-member p-value ladder (raw, permutation-calibrated, Bonferroni, Holm, and Romano-Wolf) under two sector-member specifications. It supports the family-wise-error statement in Section 4.6.5.

Every numeric value here reproduces exactly from the committed reproduction scripts and the persisted input frames in the replication package (no scratch-directory dependency, no live-API calls at reproduction time). Both output-of-record JSON files reproduce byte-identically on re-run; reproduction was reconfirmed 2026-06-30. Reproduction entry points are listed in Part 4.

---

## Part 1: The battery and the correction

The paper reports four bivariate associations between governance concentration (post-exclusion holding HHI) and protocol covariates:

1. Launch insider allocation (Pearson correlation with HHI): the reported null.
2. Current insider retention among top-ten holders (Spearman correlation with HHI): a positive finding.
3. Subsidy dependence (Pearson correlation with HHI, Livepeer-inclusive): a positive but outlier-driven finding.
4. Architectural sector (DePIN versus DeFi and infrastructure): a positive finding.

Because four hypotheses are tested on one cross-section, a reviewer may reasonably ask whether any single significant result is a multiple-testing artifact. We control the family-wise error rate with a step-down Romano-Wolf procedure in its Westfall-Young minP form (Westfall and Young, 1993; Romano and Wolf, 2005), reported alongside Bonferroni and Holm (Holm, 1979) for reference.

The four tests live on heterogeneous frames and subsamples (retention on the insider-analysis frame's own full-HHI column, N = 39; launch allocation, subsidy, and sector on the regression and price frame, N = 51, 23, and 50 respectively). A single per-draw protocol key, shared across all members, coordinates the permutation so that each protocol moves consistently in every test. This preserves the cross-test dependence induced by shared protocols while each member is calibrated against its own permutation null (B = 20,000 permutations, seed 2026). The step-down minP statistic is monotone in the raw ordering; the acceptance gate enforces that ordering (Part 3).

## Part 2: Results

Two specifications differ only in how the sector member is measured. Variant A uses the registered omnibus three-class Kruskal-Wallis sector test (the of-record sector statistic). Variant B uses the abstract's headline balanced DePIN-versus-DeFi Mann-Whitney on the pass-through HHI (N = 15 and 15, Cohen's d = 0.65). All other members are identical across variants.

### Variant A: sector member = three-class Kruskal-Wallis omnibus

| Battery member | Statistic of record | N | Raw p | Perm-calibrated p | Bonferroni p | Holm p | Romano-Wolf minP p | Survives FWER 0.05 |
|---|---|---|---|---|---|---|---|---|
| Launch insider allocation | Pearson r = 0.087 | 51 | 0.5426 | 0.5404 | 1.0000 | 0.5404 | 0.5404 | No |
| Insider retention | Spearman rho = 0.441 | 39 | 0.0049 | 0.0050 | 0.0202 | 0.0182 | 0.0178 | Yes |
| Subsidy dependence | Pearson r = 0.620 | 23 | 0.0016 | 0.0171 | 0.0686 | 0.0343 | 0.0339 | Yes |
| Architectural sector | Kruskal-Wallis H = 10.093 | 50 | 0.0064 | 0.0045 | 0.0182 | 0.0182 | 0.0178 | Yes |

Under variant A, all three positive findings survive the joint family-wise correction at FWER 0.05 (retention and sector at Romano-Wolf p = 0.018, subsidy at p = 0.034), and the allocation null is unaffected (p = 0.54). No discovery flips to non-significance under the correction.

### Variant B: sector member = balanced DePIN-versus-DeFi Mann-Whitney

| Battery member | Statistic of record | N | Raw p | Perm-calibrated p | Bonferroni p | Holm p | Romano-Wolf minP p | Survives FWER 0.05 |
|---|---|---|---|---|---|---|---|---|
| Launch insider allocation | Pearson r = 0.087 | 51 | 0.5426 | 0.5404 | 1.0000 | 0.5404 | 0.5404 | No |
| Insider retention | Spearman rho = 0.441 | 39 | 0.0049 | 0.0050 | 0.0202 | 0.0202 | 0.0193 | Yes |
| Subsidy dependence | Pearson r = 0.620 | 23 | 0.0016 | 0.0171 | 0.0686 | 0.0514 | 0.0485 | Yes |
| Architectural sector | Mann-Whitney, Cohen's d = 0.65 | 30 (15 and 15) | 0.0279 | 0.0260 | 0.1040 | 0.0520 | 0.0510 | No |

Under variant B, insider retention carries the correction cleanly (Romano-Wolf p = 0.019) and the subsidy association is at the family-wise boundary (p = 0.049). The sector contrast, measured by the weaker balanced binary statistic, sits just above the family-wise threshold (Romano-Wolf p = 0.051) and does not clear the joint four-test correction. This is reported honestly: it matches the Section 4.6.2 characterization of the sector contrast as a directionally robust, medium effect whose significance is marginal and test-dependent. The allocation null is again unaffected (p = 0.54).

## Part 3: Interpretation and acceptance gate

Because the four tests use different covariates, the cross-test dependence in the permutation null is weak, so the Romano-Wolf adjustment is only marginally tighter than Holm (for example, retention Romano-Wolf p = 0.0178 versus Holm p = 0.0182 in variant A). The value of the procedure here is an assumption-light joint family-wise statement, not a power gain over Holm.

The substantive reading of the paper is unchanged. Insider retention is the finding that carries a joint four-test family-wise correction cleanly under either sector specification (Romano-Wolf p = 0.018 to 0.019). The architectural sector contrast is corroborated when measured by the of-record omnibus statistic (variant A, p = 0.018) and is a marginal, specification-dependent medium effect under the weaker headline binary (variant B, p = 0.051). The subsidy association, already reported as Livepeer-driven, is significant under the correction but is the weakest member (variant A p = 0.034; variant B p = 0.049, at the boundary). The launch-allocation null is unaffected throughout.

Each reproduction writes a deterministic acceptance gate that must pass before the result is accepted of record. The gate re-checks the battery anchor statistics against their registered values (insider retention rho = 0.44 at N = 39; sector Kruskal-Wallis H = 10.09 at N = 50, or Cohen's d = 0.65 with Mann-Whitney p = 0.028 at N = 15 and 15 for variant B; subsidy r = 0.62 at N = 23; allocation r = 0.09) and enforces the monotone ordering: the permutation-calibrated p is at or below the Romano-Wolf p, which is at or below the Holm p, which is at or below the Bonferroni p. Both variants report ALL_PASS. A HALT-2 guard flags any discovery that flips from significant to non-significant under the correction: none flips under variant A; the sector member flips under variant B, which is the source of the marginal-under-the-headline-statistic statement above and is reported rather than suppressed.

## Part 4: Reproduction entry points

| Artifact | Path (replication package `exhibits/`) | Output of record |
|---|---|---|
| Variant A driver (sector = Kruskal-Wallis) | `romano_wolf_stepdown.py` | `romano_wolf_results.json` |
| Variant B driver (sector = Mann-Whitney) | `romano_wolf_stepdown_sector_mw.py` | `romano_wolf_results_sector_mw.json` |
| Input frame (retention member) | `romano_wolf_frames/insider_analysis_results_v3.csv` (columns `full_hhi`, `insider_count_frac`) | N = 39 |
| Input frame (allocation, subsidy, sector members) | `price_performance_audit/b2_price_performance_dataset.csv` (columns `category`, `hhi`) | N = 50 to 52 |

Both drivers are one-command, seed-fixed (seed 2026, B = 20,000), and free of scratch-directory or live-API dependencies. Each re-run reproduces its output-of-record JSON byte-identically and re-emits the acceptance gate; both were reconfirmed byte-identical on 2026-06-30.

References cited in this file (full citations in the main manuscript reference list): Holm (1979); Romano and Wolf (2005); Westfall and Young (1993).
