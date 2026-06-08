# Governance Concentration Beyond Token Allocation: Replication Materials

**Paper:** "Governance Concentration Beyond Token Allocation: A Protocol-Address-Corrected Cross-Sectional Audit of 52 DePIN and DeFi Protocols"

**Author:** Zach Zukowski, Tokenization Systems

**Contact:** zach@tokenization.systems | ORCID: [0009-0006-3642-2450](https://orcid.org/0009-0006-3642-2450)

**Status:** Under review at *Frontiers in Blockchain*, Blockchain Economics section (R2 revision submitted May 2026)

**SSRN:** [https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6599278](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6599278)

---

## Summary

A 52-protocol cross-section documents that initial token allocation design does not predict post-distribution governance concentration (insider allocation Pearson r = 0.10, p = 0.49, N = 50). Protocols with generous community distributions exhibit concentration patterns similar to those with heavy insider allocations.

**Supporting findings:**

- **Sector contrast.** DePIN protocols are more concentrated than DeFi protocols, a directionally robust, medium effect (Cohen's d positive across every protocol-controlled-address exclusion specification and all thirty leave-one-out folds). Under the headline voter-inclusive staking pass-through treatment the contrast is medium and rank-significant (Cohen's d = 0.65, Mann-Whitney p = 0.028), with marginal mean-based significance (label-permutation p approximately 0.08) that is the heavy-tail signature of a single concentrated DeFi-side vote-escrow bloc; a uniform staking-aggregation exclusion gives a comparable effect significant on every test (Cohen's d = 0.75, Mann-Whitney p = 0.018, permutation p = 0.009), while an earlier inconsistent-treatment specification (Cohen's d = 1.05) is reported as inflated rather than as the headline. The powered multivariate model keeps the DePIN coefficient positive and significant (+0.87, p = 0.02, N = 44).
- **Insider retention.** Protocols with more insider wallets in their top-holder sets exhibit higher concentration among non-insider holders (Spearman rho = 0.54, p = 0.001, N = 34), indicating insider-heavy protocols develop concentrated governance ecosystems, not merely concentrated insider positions.
- **Subsidy disconnect.** On-chain subsidy correlates with concentration in levels (r = 0.62, p = 0.002, N = 23) but entirely through Livepeer (88.5x subsidy); excluding Livepeer, the correlation collapses to a null (r = 0.07, p = 0.76, N = 22).
- **Delegation amplification.** Voting-power HHI exceeds holding HHI by factors of 2.5x to 25.6x across thirteen of eighteen protocols sampled (mean approximately 6.8x, median 4.4x), with five structural exceptions showing dispersion (ENS 0.48x, GMX 0.87x, HNT 0.26x to 0.39x, JUP 0.12x, and LPT 0.27x), reflecting mature delegate programs where holders systematically delegate to broad community-delegate sets. Three vote-escrowed protocols (Curve, Balancer, Frax) form a distinct class showing extreme amplification (15x, 21x, and 11.4x respectively) under ve-token lock-duration weighting.
- **Inequality versus concentration.** Token inequality is severe in every protocol (Gini 0.52 to 0.99) while governance concentration varies across two orders of magnitude (HHI 0.005 to 0.199); the moderate correlation between them (Pearson r = 0.52, N = 48) indicates inequality metrics cannot substitute for direct concentration measurement.

**Methodology contribution.** The exclusion methodology applies 133 address exclusions across 38 protocols (125 unique addresses; five recur across multiple protocols, including Binance 8 hot wallet across four tokens) controlled by protocols themselves (staking contracts, exchange custodians, vesting locks, and treasuries) that appear on holder lists but cannot vote. Correcting for these changes affected protocols' HHI by up to 18x (RENDER at 17.9x, where Wormhole Token Bridge custody dominated naive top-1000 holdings; median 2.3x across 32 protocols with complete pre-exclusion and post-exclusion HHI logged; see `b2/paper/supplements/hhi_inflation_factors_2026-05-19.md`). Prior studies computing token HHI without this correction measured protocol architecture, not governance concentration.

## Companion paper: Who Burns the Tokens? (B3)

**Demand concentration is an independent failure mode, observable only for direct-burn protocols.** A 34-month longitudinal analysis of Helium documents the first empirical observation of burn-to-mint equilibrium threshold crossing (S2R = 1.84), and there demand is highly concentrated: roughly five purchasers account for about 90% of burns (burn-signer HHI 0.27). On-chain burn-signer concentration is a valid demand-concentration measure only where token holders burn directly (Helium); buy-and-burn (GEODNET, S2R 0.219) and protocol-mediated pooled-burn (DIMO) architectures execute burns through a foundation or treasury, relocating the demand base to off-chain subscriptions and licenses, so their customer concentration is not observable on-chain. (Prior revisions reported GEODNET HHI 0.055 and a four-to-five-times cross-model comparison; both are retired as construct-invalid. See CHANGELOG 1.6.0.)

- Manuscript: `b3/paper/B3_GeoDePIN_Final_v12.docx`
- SSRN: [https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6483619](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6483619)

## Repository Structure

```
├── b2/                             # B2 manuscript + supplements
│   └── paper/
│       ├── B2_Governance_Concentration_Frontiers_Submission.docx
│       └── supplements/                    # Supplementary Files S1-S8
├── b3/                             # B3 manuscript + data
│   └── paper/
│       └── B3_GeoDePIN_Final_v8.docx
├── data/
│   ├── processed/                  # Master datasets
│   │   ├── regression_data_april2026.csv    # 52 protocols, 39 variables
│   │   ├── table6_ols_output.json           # OLS regression output (Table 6)
│   │   ├── exclusions_log.csv               # 133 protocol-controlled address exclusions across 38 protocols (125 unique)
│   │   ├── insider_classification.csv       # 390 classifications
│   │   └── scoring_sheet.csv                # 12-protocol scoring
│   ├── raw/                        # Source data
│   │   ├── holder_lists/                    # Per-protocol top-1000 holders
│   │   ├── helium_s2r_cleaned.csv           # 34-month S2R trajectory
│   │   └── [burn/emission data per protocol]
│   └── dune_queries/               # DuneSQL templates + saved query IDs
├── exhibits/                       # Publication figures (300 DPI)
│   ├── fig1_conceptual_model.png
│   ├── fig2_framework_architecture.png
│   └── updated/fig3-fig8_*.png              # Data-driven figures
├── analysis/                       # Replication scripts
│   ├── full_regression.R                    # OLS Models 1-3 (Table 6)
│   ├── oaxaca.R                             # Oaxaca-Blinder decomposition
│   └── [numbered Python pipeline scripts]
├── outputs/                        # Computed results (JSON)
└── CODEBOOK.md                     # Variable definitions
```

## Data Sources

| Source | Used for |
|--------|----------|
| Dune Analytics | Token holders, DC burns, governance data |
| Helius DAS API | Solana token holders (5 protocols) |
| Blockscout | Contract verification, exclusion methodology |
| Token Terminal | Revenue, incentives, subsidy ratios |
| Tally / Snapshot | Delegation and voting power |
| Blockworks | GEODNET + Helium financial validation |

## Key Statistics

| Finding | Statistic | Sample |
|---|---|---|
| Allocation null (insider allocation Pearson) | r = 0.10, p = 0.49 (Spearman rho = 0.16, p = 0.27); TOST-equivalent to zero within \|r\| = 0.38 (p = 0.02) | N = 50 |
| DePIN-DeFi sector gap (d-triple) | Pass-through headline Cohen's d = 0.65, Mann-Whitney p = 0.028, 30/30 LOO, permutation approximately 0.08; uniform-exclusion robustness d = 0.75, p = 0.018, permutation 0.009; complete-CEX d = 1.05 (inflated, not the headline) | DePIN = 15, DeFi = 15 |
| Insider retention (non-insider HHI correlation) | Spearman rho = 0.54, p = 0.001 | N = 34 |
| Subsidy correlation (Livepeer-driven) | r = 0.62, p = 0.002 (full) / r = 0.07, p = 0.76 (ex-Livepeer; null) | N = 23 / N = 22 |
| Gini inequality range | 0.52 to 0.99 | N = 52 |
| HHI concentration range | 0.005 to 0.199 | N = 52 |
| Delegation amplification (universal, non-ve-token) | 2.5x to 25.6x; mean approximately 6.8x, median 4.4x | N = 18 (13 amplify; 5 dispersers: ENS 0.48x, GMX 0.87x, HNT 0.26x-0.39x, JUP 0.12x, LPT 0.27x) |
| Helium S2R (companion B3) | 1.84 (Feb 2026) | 34-month trajectory |

## Reproduction

### One-command reproduction of the headline regression results

To regenerate the paper's headline numbers from persisted raw, re-fetched, and documented inputs (no `/tmp` dependency, no live-API calls):

```
python reproduce.py
```

`reproduce.py` (repository root) runs the full pipeline and prints a reconciliation table against `b2/paper/analysis_n52_2026-05-29/b2_explanatory_model_VERIFIED_NUMBERS_2026-05-29.md`. It regenerates:

1. **Post-exclusion holder-HHI from raw** for the new cohort (FXS, SNX, GNO, WLFI, ENA, PUMP, JTO, BONK, KMNO): the raw top-1000 holder lists in `data/raw/holder_lists/` minus the unified PCA-exclusion set in `b2/paper/analysis_n52_2026-05-29/new12_unified_exclusions_2026-05-29.csv` reproduce the documented HHIs to within 1e-4 (all nine match exactly), including the corrected ENA and WLFI exclusions.
2. **Retention-spec powered model (elected primary):** log-HHI ~ sector + insider-retention + revenue-intensity, N = 50, HC3 robust SE. The insider-retention vector is the persisted `new12_retention_vector_2026-05-29.csv` (re-fetched, with per-address provenance in `new12_retention_provenance_2026-05-29.json`) joined to the original-sample retention in `insider_analysis_results_v3.csv`. The covariate-complete sample is N = 50; no protocol drops for a missing insider-retention vector. The DePIN sector coefficient is positive and significant (p = 0.005); the insider-retention regressor itself is not significant (the composition-shift result, so the sector channel carries the contrast).
3. **Maturity-spec powered model (robustness anchor):** log-HHI ~ sector + revenue-intensity + maturity, N = 50, HC3 robust SE.
4. **Insider-retention de-tautology** (original sample), reporting both the Spearman rho and the OLS p: the de-tautology (non-insider HHI) Spearman rho = 0.54, N = 34, and the original-sample full-HHI check rho = 0.44, N = 39, both confirming the insider-retention association is more than an arithmetic artifact.
5. **Control null-sweep** and the **sector HHI distribution** plus the DePIN-vs-DeFi contrast.

CODEBOOK hazards a replicator should know (documented so they are not re-hit):

- **De-tautology column:** use `non_insider_hhi_approx`, NOT `non_insider_hhi_top10`. The `_top10` column in `insider_analysis_results_v3.csv` is buggy for insider-count = 0 rows (it does not equal `full_hhi` though it must, for example BAL, IO, ARB); using it yields a spurious rho near 0.27. The `_approx` column is correct.
- **Retention-spec DePIN p:** reproduces at approximately 0.005 (significant) under the evidence-traced insider classification of record, below the earlier pre-audit 0.014 to 0.016 lock. The finding holds in both the retention-spec (DePIN p approximately 0.005) and the maturity-spec (DePIN p approximately 0.011); insider-retention is not significant in either (the composition-shift result).
- **Insider definition (new-12 retention):** matches the original sample (`analysis/03_insider_classification.py`): among post-exclusion top-10 survivors, insider = team / founder / investor (VC/fund) / Investment Recipient / foundation / treasury / attributed multisig / vesting; not insider = CEX / market-maker / staking-pool or vault aggregation / proxy contract / retail whale. This reclassifies survivor labels only; the published HHIs and the PCA-exclusion methodology are unchanged.
- **Covariates** (revenue, FDV, maturity) are sourced documented inputs read as-is; the pipeline does not re-call live APIs, which would not be stable for a replicator.

### Robustness additions (R2 strengthening)

The R2 revision adds a zero-new-data robustness layer, reproducible from committed inputs with no `/tmp` and no live-API dependency:

```
python b2/paper/analysis_n52_2026-05-29/b2_sector_contrast_reproduce_2026-06-02.py
python b2/paper/analysis_n52_2026-05-29/b2_strengthen_compute_2026-06-02.py
```

- **Sector-contrast d-triple** (`b2_sector_contrast_reproduce_2026-06-02.py`, reading `sector_contrast_hhi_vectors_2026-06-02.csv`): the headline voter-inclusive pass-through (Cohen's d = 0.65, Mann-Whitney p = 0.028, 30/30 leave-one-out, mean-based permutation approximately 0.08), the uniform staking-aggregation exclusion robustness check (d = 0.75, p = 0.018, permutation 0.009, bootstrap d interval [0.40, 1.52]), and the inflated complete-CEX treatment (d = 1.05, p = 0.011) all reproduce from the committed per-protocol holding-HHI vectors.
- **Bounded allocation null** (`b2_strengthen_compute_2026-06-02.py`): the allocation null is statistically equivalent to zero within the powered envelope (TOST p = 0.02 within \|r\| = 0.38), and the launch-design block (team, investor, maturity) is jointly uninformative (omnibus F(3,41) = 0.66, p = 0.58, R-squared 4.6 percent).
- **Temporal corroboration (NE-1):** launch insider allocation is uncorrelated with the 24-month governance-HHI endpoint on the quarterly panel (Pearson r = -0.11, N = 13; descriptive, construct-distinct, reported under the no-trajectory-claims scope).
- **Insider-retention triple:** the de-tautology Spearman rho = 0.54, N = 34 carries a bootstrap 95 percent interval [0.21, 0.80], a permutation p = 0.001, all 34 leave-one-out folds positive, and a sector-partial rank correlation of 0.47 (p = 0.005).
- **Model 4 influence:** all 50 leave-one-out refits of the powered specification keep the DePIN coefficient significant (worst-case p = 0.022 in the maturity spec, p = 0.013 in the retention spec), so the sector contrast does not hinge on any single protocol.
- **Retain-CEX robustness:** retaining exchange-deposit wallets in the holding distribution attenuates the contrast toward the margin of conventional significance (Cohen's d approximately 0.62, Mann-Whitney p approximately 0.03 to 0.05), still a medium effect.

### Prerequisites

- **R** (>= 4.2) with packages: `sandwich` (HC3 robust SE), `car`, `lmtest`
- **Python** (>= 3.10): `pip install pandas scipy numpy matplotlib statsmodels`
- **Dune Analytics** account (free tier sufficient)

### Steps

1. **Cross-sectional analysis:** `data/processed/regression_data_april2026.csv` is the analysis-ready dataset (52 protocols, 39 variables).
2. **OLS regression (Table 6):** Run `analysis/full_regression.R`. Pre-computed output: `data/processed/table6_ols_output.json`.
3. **Python pipeline:** Run scripts in `analysis/` (numbered order). Key output: `outputs/regression_results.json`.
4. **Dune queries:** Templates in `data/dune_queries/`. See `saved_query_ids.md` for pre-saved query IDs.
5. **Supplementary materials:** S1-S8 in `b2/paper/supplements/`. May 2026 revision additions: `burn_rule_audit_findings.csv`, `burn_rule_audit_summary.csv`, `top10_post_exclusion_all20.csv`, `uni_burn_cascade.csv`, `sample_coverage_table.md`.

### Reproducibility notes

- **Self-contained core.** `reproduce.py` regenerates the headline numbers from data committed in this repository, with no external dependency. All analysis, figure, and supplement scripts resolve their paths relative to the repository root (no absolute machine paths), so path resolution is clone-independent.
- **Investigation artifacts.** The Polkadot validator-attribution scripts in `data/raw/b2_phase4_minibatch_2026-05-27/expansion_artifacts/` form a chained pipeline that exchanges intermediate outputs through `/tmp`; they are provided as investigation artifacts and are not intended for bare-clone execution. The cited Polkadot concentration values are reproduced by `dot_pca_refined.py`, `dot_cluster_sensitivity.py`, and `b2_n52_merge.py` from committed data.
- **Exploratory artifact (not cited).** `b2/paper/analysis_n52_2026-05-29/b2_incentive_value_timeseries_2026-05-29.py` is exploratory; its CoinGecko price inputs are not committed and it produces no value cited in the paper or supplements. It is included for transparency only.
- **Optional re-pull.** `b2/paper/supplements/power_indices_solana_quorum_variation_2026-05-27.py` reads a JUP voter snapshot regenerable via the Dune query documented in its header; the cited power-index values are also persisted in `power_indices_n14_full_2026-05-27.csv`, so the re-pull is optional for verification.
- **Polkadot Table 3 top-10 share.** The Polkadot descriptive top-10% in Table 3 (21.0%) and the cross-section dataset column (13.00) use different top-share populations; the load-bearing concentration value (HHI 0.0052) is identical in both.

## Round 1 revision (May 2026): methodology updates

Four methodological refinements landed in response to Reviewer 1 and Reviewer 2 comments (reviewer responses archived alongside the manuscript):

- **Universal burn-rule exclusion.** Canonical-burn addresses (0x000...000, 0x000...dead, plus chain-specific burn patterns) are now excluded universally from HHI computation. UNI's 0x000...dead address held 102.46M UNI (11.27% of supply) and was the only previously-unexcluded canonical-burn destination in the 20-protocol audit. After also excluding the UNI Timelock (governance treasury, included in the pre-burn-rule baseline), UNI's HHI drops from 0.032 (Timelock-excluded only) to 0.010 (Timelock-and-burn excluded). The recomputed DeFi sector mean drops from 0.043 to 0.041.
- **Holder-list cutoff correction (F1).** Three protocols (MOR, AXL, ZRO) had Dune holder-list queries inadvertently capped at top-100 rather than top-1000. Re-pulling at top-1000 cutoff yields revised values: MOR HHI 0.013 to 0.031, AXL 0.004 to 0.028, ZRO 0.010 to 0.015. Combined with the burn-rule cascade above, this correction fed into the DePIN-vs-DeFi sector contrast; the contrast was subsequently re-characterized under the consistent staking-treatment analysis introduced in the Round 2 cycle and is now reported under the voter-inclusive pass-through headline summarized above (Cohen's d = 0.65, with the uniform staking-aggregation exclusion at Cohen's d = 0.75), superseding the intermediate R1-cycle effect sizes.
- **Top-N reporting consistency.** For five protocols (AAVE, UNI, ARB, GRT, OP) whose top holders included protocol-controlled addresses, the Top-1% and Top-10% columns in Table 4 are now recomputed using the same exclusion methodology as the HHI column. Pre-exclusion vs post-exclusion values for all 20 protocols with protocol-controlled addresses are provided in `b2/paper/supplements/top10_post_exclusion_all20.csv`.
- **Voting-HHI source labels for Compound and Arbitrum.** Table 7 source labels were corrected from Tally to Snapshot. The published numerical values (Compound 0.053, Arbitrum 0.052) were always Snapshot-derived; only the labels were mislabeled. Snapshot was the chosen source because its active-voter pool (n = 114 unique voters for Compound; n = 5,241 for Arbitrum) exceeded Tally's top-100-delegate sampling.
- **stkAAVE pass-through delegation acknowledgment.** AAVE's stkAAVE staking contract is excluded from the holding HHI per the protocol-controlled-address rule, but stakers retain pass-through voting power. A methodological note added at the manuscript's Section 3.4 acknowledges that the reported AAVE holding HHI (0.020) therefore understates effective governance concentration; reconstructing the staker distribution is deferred to follow-up work.

**Note on `outputs/` directory.** Pre-computed regression outputs in `outputs/` reflect pre-revision pipeline state. The post-revision values are reflected in `data/processed/regression_data_april2026.csv` and `data/processed/governance_concentration_april2026.csv` (manual revisions; see notes columns). The current manuscript is authoritative for reported statistics.

## Round 2 revision (May 2026): scope and substantive changes

The R2 cycle responded to Reviewer 1's R2 round (Reviewer 2 endorsed publication after R1). Five substantive changes landed:

- **Universal delegation amplification thesis (Section 3.5; abstract finding 4).** With post-exclusion holding HHIs applied consistently across Table 4 and Table 7, 9 of 10 protocols in the voting-layer subsample amplify holding concentration in their voting layer (range 1.2x to 11.4x; mean 5.3x), with one structural exception (ENS at 0.39x, a mature delegate program where holders systematically delegate to a broad community-delegate set). Replaces the R1 framing where UNI (0.84x) and OP (0.79x) appeared as delegation-mediated dispersion cases. The flip is driven by methodology consistency: applying the canonical exclusion list (including 0x000...000dead for UNI, the regression-dataset post-exclusion baseline for OP) brings Table 7's holding-side denominators in line with Table 4 and the regression CSV. Subsequent R2-cycle audit waves (Lido recompute under universal top-1000 methodology; deep protocol-controlled-address audit, now 133 address exclusions across 38 protocols, codifying a five-class PCA typology) refined Table 7 holdings further, yielding the final range and mean cited above.
- **Manuscript-vs-data drift remediation (Reviewer 1 Issue 1).** Table 7 holding HHIs recomputed under the full R2-cycle audit chain: UNI 0.032 to 0.010; OP 0.042 to 0.009; LDO 0.018 to 0.008 (post-Lido-recompute + post-Bybit/Binance Class 5 exclusion); Compound 0.028 to 0.009; Aave 0.020 to 0.013; DIMO 0.038 to 0.025; ENS 0.135 to 0.071. Aethir holding HHI 0.171 to 0.209 in Table 4 (R2 direct Dune pull, May 2026 top-1000 under the universal ATH Top-N% convention).
- **PCA-symmetric robustness check (Section 3.7).** Applying protocol-controlled-address exclusion symmetrically at the voting layer confirms universal amplification across all 5 Tally-sourced protocols (using post-deep-audit holding HHIs): Compound 5.8x, Aave 3.5x, Uniswap 2.8x, Optimism 3.6x, Arbitrum 4.4x. The Compound number is load-bearing: the top COMP Tally delegate (~21.5% of delegated voting power) is Compound Foundation itself, and excluding it shifts voting HHI from 0.078 to 0.052.
- **Table 4 expansion.** Hivemapper, io.net, and Aethir added as full rows during the R2 cycle; the cross-section subsequently reached its final 52-protocol frame (Table 3), with the HHI-Gini comparable cohort at N = 48.
- **Table 5 N corrections and multiple-comparisons note.** HHI-Gini correlation reconciled to the final post-exclusion comparable cohort (Pearson r = 0.52, N = 48); the Token-Terminal-expanded subsidy robustness check uses N = 20. Benjamini-Hochberg FDR correction at q = 0.05 applied to the 14 tests reported in Table 5; three of four significant findings survive.

Three Phase 0 findings surfaced during R2 data collection and are deferred to a follow-up cycle (Compound Foundation as PCA at voting layer; ENS delegation-dispersion at 0.46x ratio; Balancer veBAL extreme amplification at 20.9x ratio).

See `CODEBOOK.md` for variable definitions.

## Citation

```bibtex
@article{zukowski2026governance,
  title={Governance Concentration Beyond Token Allocation: A Protocol-Address-Corrected
         Cross-Sectional Audit of 52 DePIN and DeFi Protocols},
  author={Zukowski, Zach},
  year={2026},
  institution={Tokenization Systems},
  note={Under review at Frontiers in Blockchain (Round 2 revision May 2026)}
}

@article{zukowski2026geodnet,
  title={Who Burns the Tokens? Fiscal Sustainability and Demand
         Concentration in GeoDePIN Networks},
  author={Zukowski, Zach},
  year={2026},
  institution={Tokenization Systems}
}
```

Code: MIT. Data and paper: CC-BY-4.0.

zach@tokenization.systems | ORCID: 0009-0006-3642-2450
