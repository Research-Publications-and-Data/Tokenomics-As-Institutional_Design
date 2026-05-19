# Governance Concentration Beyond Token Allocation: Replication Materials

**Paper:** "Governance Concentration Beyond Token Allocation: An Institutional Design Analysis of DePIN and DeFi"

**Author:** Zach Zukowski, Tokenization Systems

**Contact:** zach@tokenization.systems | ORCID: [0009-0006-3642-2450](https://orcid.org/0009-0006-3642-2450)

**Status:** Under review at *Frontiers in Blockchain* — Blockchain Economics (R2 revision submitted May 2026)

**SSRN:** [https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6599278](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6599278)

---

## Summary

A 40-protocol cross-section documents that initial token allocation design does not predict post-distribution governance concentration (r = 0.17, p = 0.32, N = 37). Protocols with generous community distributions exhibit concentration patterns similar to those with heavy insider allocations.

**Supporting findings:**

- **Sector contrast.** DePIN protocols are more concentrated than DeFi protocols (Mann-Whitney p = 0.018, Cohen's d = 1.04; robust across all 30 leave-one-out iterations; permutation p = 0.004); the effect survives multivariate adjustment for protocol age, log fully diluted valuation, and insider allocation across three nested OLS specifications (adjusted R² 0.14 to 0.17).
- **Insider retention.** Protocols with more insider wallets in their top-holder sets exhibit higher concentration among non-insider holders (Spearman rho = 0.54, p = 0.001, N = 34), indicating insider-heavy protocols develop concentrated governance ecosystems, not merely concentrated insider positions.
- **Subsidy disconnect.** On-chain subsidy correlates with concentration in levels (r = 0.58, p = 0.008, N = 20) but entirely through Livepeer (88.5x subsidy); excluding Livepeer, the correlation is not significant (r = 0.12, p = 0.63).
- **Delegation amplification.** Voting-power HHI exceeds holding HHI by factors of 1.4x to 6.0x across nine of ten protocols sampled (mean 3.3x), with one structural exception (ENS at 0.21x, reflecting a mature delegate program where holders systematically delegate to a broad community-delegate set). Two vote-escrowed protocols (Curve, Balancer) form a distinct class showing extreme amplification (15x and 21x) under ve-token lock-duration weighting.
- **Inequality versus concentration.** Token inequality is severe in every protocol (Gini 0.73 to 0.98) while governance concentration varies across two orders of magnitude (HHI 0.004 to 0.199); the moderate correlation between them (r = 0.54) indicates inequality metrics cannot substitute for direct concentration measurement.

**Methodology contribution.** The exclusion methodology identifies 86 addresses controlled by protocols themselves (staking contracts, exchange custodians, vesting locks, and treasuries) that appear on holder lists but cannot vote. Correcting for these changes affected protocols' HHI by up to 5x. Prior studies computing token HHI without this correction measured protocol architecture, not governance concentration.

## Companion paper: Who Burns the Tokens? (B3)

**Demand concentration is an independent failure mode.** A 34-month longitudinal analysis of Helium documents the first empirical observation of burn-to-mint equilibrium threshold crossing (S2R = 1.84). Subscription-based burn models (GEODNET HHI = 0.055, DIMO HHI = 0.063) produce four to five times less demand concentration than carrier-contract models (Helium HHI = 0.27, Livepeer HHI = 0.31).

- Manuscript: `b3/paper/B3_GeoDePIN_Final_v8.docx`
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
│   │   ├── regression_data_april2026.csv    # 40 protocols, 39 variables
│   │   ├── table6_ols_output.json           # OLS regression output (Table 6)
│   │   ├── exclusions_log.csv               # 86 excluded addresses across 29 protocols
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
| Allocation null | r = 0.17, p = 0.32 | N = 37 |
| DePIN-DeFi sector gap | Mann-Whitney p = 0.018, Cohen's d = 1.04; 30/30 LOO robust; permutation p = 0.004 | DePIN = 15, DeFi = 15 |
| Insider retention (non-insider HHI correlation) | Spearman rho = 0.54, p = 0.001 | N = 34 |
| Subsidy correlation (Livepeer-driven) | r = 0.57, p = 0.008 (full) / r = 0.11, p = 0.65 (ex-Livepeer) | N = 20 / N = 19 |
| Gini inequality range | 0.73 to 0.99 | N = 40 |
| HHI concentration range | 0.005 to 0.199 | N = 40 |
| Delegation amplification (universal, non-ve-token) | 1.4x to 6.0x; mean 3.3x | N = 10 (9 amplify; ENS 0.21x exception) |
| Helium S2R (companion B3) | 1.84 (Feb 2026) | 34-month trajectory |

## Reproduction

### Prerequisites

- **R** (>= 4.2) with packages: `sandwich` (HC3 robust SE), `car`, `lmtest`
- **Python** (>= 3.10): `pip install pandas scipy numpy matplotlib statsmodels`
- **Dune Analytics** account (free tier sufficient)

### Steps

1. **Cross-sectional analysis:** `data/processed/regression_data_april2026.csv` is the analysis-ready dataset (40 protocols, 39 variables).
2. **OLS regression (Table 6):** Run `analysis/full_regression.R`. Pre-computed output: `data/processed/table6_ols_output.json`.
3. **Python pipeline:** Run scripts in `analysis/` (numbered order). Key output: `outputs/regression_results.json`.
4. **Dune queries:** Templates in `data/dune_queries/`. See `saved_query_ids.md` for pre-saved query IDs.
5. **Supplementary materials:** S1-S8 in `b2/paper/supplements/`. May 2026 revision additions: `burn_rule_audit_findings.csv`, `burn_rule_audit_summary.csv`, `top10_post_exclusion_all20.csv`, `uni_burn_cascade.csv`, `sample_coverage_table.md`.

## Round 1 revision (May 2026): methodology updates

Four methodological refinements landed in response to Reviewer 1 and Reviewer 2 comments (reviewer responses archived alongside the manuscript):

- **Universal burn-rule exclusion.** Canonical-burn addresses (0x000...000, 0x000...dead, plus chain-specific burn patterns) are now excluded universally from HHI computation. UNI's 0x000...dead address held 102.46M UNI (11.27% of supply) and was the only previously-unexcluded canonical-burn destination in the 20-protocol audit. After also excluding the UNI Timelock (governance treasury, included in the pre-burn-rule baseline), UNI's HHI drops from 0.032 (Timelock-excluded only) to 0.010 (Timelock-and-burn excluded). The recomputed DeFi sector mean drops from 0.043 to 0.041.
- **Holder-list cutoff correction (F1).** Three protocols (MOR, AXL, ZRO) had Dune holder-list queries inadvertently capped at top-100 rather than top-1000. Re-pulling at top-1000 cutoff yields revised values: MOR HHI 0.013 to 0.031, AXL 0.004 to 0.028, ZRO 0.010 to 0.015. Combined with the burn-rule cascade above, the DePIN-vs-DeFi sector contrast strengthens from pre-revision Mann-Whitney p = 0.031, Cohen's d = 0.96 to post-F1 Mann-Whitney p = 0.014, Cohen's d = 1.03 (robust across all 30 leave-one-out iterations).
- **Top-N reporting consistency.** For five protocols (AAVE, UNI, ARB, GRT, OP) whose top holders included protocol-controlled addresses, the Top-1% and Top-10% columns in Table 4 are now recomputed using the same exclusion methodology as the HHI column. Pre-exclusion vs post-exclusion values for all 20 protocols with protocol-controlled addresses are provided in `b2/paper/supplements/top10_post_exclusion_all20.csv`.
- **Voting-HHI source labels for Compound and Arbitrum.** Table 7 source labels were corrected from Tally to Snapshot. The published numerical values (Compound 0.053, Arbitrum 0.052) were always Snapshot-derived; only the labels were mislabeled. Snapshot was the chosen source because its active-voter pool (n = 114 unique voters for Compound; n = 5,241 for Arbitrum) exceeded Tally's top-100-delegate sampling.
- **stkAAVE pass-through delegation acknowledgment.** AAVE's stkAAVE staking contract is excluded from the holding HHI per the protocol-controlled-address rule, but stakers retain pass-through voting power. A methodological note added at the manuscript's Section 3.4 acknowledges that the reported AAVE holding HHI (0.020) therefore understates effective governance concentration; reconstructing the staker distribution is deferred to follow-up work.

**Note on `outputs/` directory.** Pre-computed regression outputs in `outputs/` reflect pre-revision pipeline state. The post-revision values are reflected in `data/processed/regression_data_april2026.csv` and `data/processed/governance_concentration_april2026.csv` (manual revisions; see notes columns). The current manuscript is authoritative for reported statistics.

## Round 2 revision (May 2026): scope and substantive changes

The R2 cycle responded to Reviewer 1's R2 round (Reviewer 2 endorsed publication after R1). Five substantive changes landed:

- **Universal delegation amplification thesis (Section 3.5; abstract finding 4).** With post-exclusion holding HHIs applied consistently across Table 4 and Table 7, all 8 protocols in the voting-layer subsample amplify holding concentration in their voting layer (range 1.9x to 6.8x; mean 4.1x). Replaces the R1 framing where UNI (0.84x) and OP (0.79x) appeared as delegation-mediated dispersion cases. The flip is driven by methodology consistency: applying the canonical exclusion list (including 0x000...000dead for UNI, the regression-dataset post-exclusion baseline for OP) brings Table 7's holding-side denominators in line with Table 4 and the regression CSV.
- **Manuscript-vs-data drift remediation (Reviewer 1 Issue 1).** Table 7 holding HHIs recomputed: UNI 0.032 to 0.010; OP 0.042 to 0.009; LDO 0.018 to 0.013. Aethir holding HHI 0.171 to 0.168 in Table 4 footnote (CSV authoritative at 0.1678).
- **PCA-symmetric robustness check (Section 3.7).** Applying protocol-controlled-address exclusion symmetrically at the voting layer confirms universal amplification across all 5 Tally-sourced protocols: Compound 1.85x, Aave 2.26x, Uniswap 2.72x, Optimism 4.06x, Arbitrum 3.01x. The Compound number is load-bearing: the top COMP Tally delegate (~21.5% of delegated voting power) is Compound Foundation itself, and excluding it shifts voting HHI from 0.078 to 0.052.
- **Table 4 expansion to 40 protocols.** Hivemapper, io.net, and Aethir added as full rows (R1 had 37; R2 has 40 with full statistics).
- **Table 5 N corrections and multiple-comparisons note.** HHI-Gini correlation N corrected to 40; TT-expanded subsidy N corrected from 22 to 19 with Pearson r = 0.097. Benjamini-Hochberg FDR correction at q = 0.05 applied to the 14 tests reported in Table 5; three of four significant findings survive.

Three Phase 0 findings surfaced during R2 data collection and are deferred to a follow-up cycle (Compound Foundation as PCA at voting layer; ENS delegation-dispersion at 0.46x ratio; Balancer veBAL extreme amplification at 20.9x ratio).

See `CODEBOOK.md` for variable definitions.

## Citation

```bibtex
@article{zukowski2026governance,
  title={Governance Concentration Beyond Token Allocation: An Institutional
         Design Analysis of DePIN and DeFi},
  author={Zukowski, Zach},
  year={2026},
  institution={Tokenization Systems},
  note={Under review at Frontiers in Blockchain (Round 1 revision May 2026)}
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
