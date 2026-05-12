# Governance Concentration Beyond Token Allocation: Replication Materials

**Paper:** "Governance Concentration Beyond Token Allocation: An Institutional Design Analysis of DePIN and DeFi"

**Author:** Zach Zukowski, Tokenization Systems

**Contact:** zach@tokenization.systems | ORCID: [0009-0006-3642-2450](https://orcid.org/0009-0006-3642-2450)

**Status:** Under review at *Frontiers in Blockchain* — Blockchain Economics (R1 revision submitted May 2026)

**SSRN:** [https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6599278](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6599278)

---

## Summary

A 40-protocol cross-section documents that initial token allocation design does not predict post-distribution governance concentration (r = 0.19, p = 0.25, N = 37). Protocols with generous community distributions exhibit concentration patterns similar to those with heavy insider allocations.

**Supporting findings:**

- **Sector contrast.** DePIN protocols are more concentrated than DeFi protocols (Mann-Whitney p = 0.024, Cohen's d = 0.99); the effect survives multivariate adjustment for protocol age, valuation, and insider allocation (adjusted R² 0.14 to 0.17).
- **Insider retention.** Protocols with more insider wallets in their top-holder sets exhibit higher concentration among non-insider holders (Spearman rho = 0.54, p = 0.001, N = 34), indicating insider-heavy protocols develop concentrated governance ecosystems, not merely concentrated insider positions.
- **Subsidy disconnect.** On-chain subsidy correlates with concentration in levels (r = 0.58, p = 0.008, N = 20) but entirely through Livepeer (88.5x subsidy); excluding Livepeer, the correlation is not significant (r = 0.12, p = 0.63).
- **Delegation amplification.** Voting-power HHI reaches 3 to 6 times holding HHI in DePIN, while infrastructure protocols show heterogeneous outcomes (Optimism 0.79x, Arbitrum 4.3x).
- **Inequality versus concentration.** Token inequality is severe in every protocol (Gini 0.73 to 0.98) while governance concentration varies across two orders of magnitude (HHI 0.004 to 0.199); the moderate correlation between them (r = 0.54) indicates inequality metrics cannot substitute for direct concentration measurement.

**Methodology contribution.** The exclusion methodology identifies 69 addresses controlled by protocols themselves (staking contracts, exchange custodians, vesting locks, and treasuries) that appear on holder lists but cannot vote. Correcting for these changes affected protocols' HHI by up to 5x. Prior studies computing token HHI without this correction measured protocol architecture, not governance concentration.

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
│   │   ├── exclusions_log.csv               # 69 excluded addresses
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
| Allocation null | r = 0.19, p = 0.25 | N = 37 |
| DePIN-DeFi sector gap | Mann-Whitney p = 0.024, Cohen's d = 0.99 | DePIN = 11, DeFi = 19 |
| Insider retention (non-insider HHI correlation) | Spearman rho = 0.54, p = 0.001 | N = 34 |
| Subsidy correlation (Livepeer-driven) | r = 0.58, p = 0.008 (full) / r = 0.12, p = 0.63 (ex-Livepeer) | N = 20 / N = 19 |
| Gini inequality range | 0.73 to 0.98 | N = 40 |
| HHI concentration range | 0.004 to 0.199 | N = 40 |
| Delegation amplification in DePIN | 3x to 6x holding HHI | N = 4 |
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

- **Universal burn-rule exclusion.** Canonical-burn addresses (0x000...000, 0x000...dead, plus chain-specific burn patterns) are now excluded universally from HHI computation. UNI's 0x000...dead address held 102.46M UNI (11.27% of supply) and was the only previously-unexcluded canonical-burn destination in the 20-protocol audit. After also excluding the UNI Timelock (governance treasury, included in the pre-burn-rule baseline), UNI's HHI drops from 0.032 (Timelock-excluded only) to 0.010 (Timelock-and-burn excluded). The recomputed DeFi sector mean drops from 0.043 to 0.041, and the DePIN-vs-DeFi sector contrast strengthens (Mann-Whitney p 0.031 to 0.024; Cohen's d 0.96 to 0.99).
- **Top-N reporting consistency.** For five protocols (AAVE, UNI, ARB, GRT, OP) whose top holders included protocol-controlled addresses, the Top-1% and Top-10% columns in Table 4 are now recomputed using the same exclusion methodology as the HHI column. Pre-exclusion vs post-exclusion values for all 20 protocols with protocol-controlled addresses are provided in `b2/paper/supplements/top10_post_exclusion_all20.csv`.
- **Voting-HHI source labels for Compound and Arbitrum.** Table 7 source labels were corrected from Tally to Snapshot. The published numerical values (Compound 0.053, Arbitrum 0.052) were always Snapshot-derived; only the labels were mislabeled. Snapshot was the chosen source because its active-voter pool (n = 114 unique voters for Compound; n = 5,241 for Arbitrum) exceeded Tally's top-100-delegate sampling.
- **stkAAVE pass-through delegation acknowledgment.** AAVE's stkAAVE staking contract is excluded from the holding HHI per the protocol-controlled-address rule, but stakers retain pass-through voting power. A methodological note added at the manuscript's Section 3.4 acknowledges that the reported AAVE holding HHI (0.020) therefore understates effective governance concentration; reconstructing the staker distribution is deferred to follow-up work.

**Note on `outputs/` directory.** Pre-computed regression outputs in `outputs/` reflect pre-revision pipeline state. The post-revision values are reflected in `data/processed/regression_data_april2026.csv` and `data/processed/governance_concentration_april2026.csv` (manual revisions; see notes columns). The current manuscript is authoritative for reported statistics.

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
