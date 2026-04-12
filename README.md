# Tokenomics as Institutional Design: Replication Materials

**Paper:** "Tokenomics as Institutional Design: A Normative Framework and Governance Concentration Analysis"

**Author:** Zach Zukowski, Tokenization Systems

**Contact:** zach@tokenization.systems | ORCID: [0009-0006-3642-2450](https://orcid.org/0009-0006-3642-2450)

**Status:** Submitted to *Frontiers in Blockchain* — Blockchain Economics (April 2026)

---

**Allocation Is Uninformative.** A 40-protocol cross-section documents that initial token allocation design does not predict post-distribution governance concentration (r = 0.19, p = 0.25, N = 37). DePIN protocols exhibit higher concentration than DeFi (Mann-Whitney p = 0.031, Cohen's d = 0.96), though the result is sensitive to sample composition. On-chain subsidy correlates with concentration only through a single outlier (Livepeer); an expanded 22-protocol sample confirms the null.

### Companion paper: Who Burns the Tokens? (B3)

**Demand concentration is an independent failure mode.** A 34-month longitudinal analysis of Helium documents the first empirical observation of burn-to-mint equilibrium threshold crossing (S2R = 1.84). Subscription-based burn models (GEODNET HHI = 0.055, DIMO HHI = 0.063) produce four to five times less demand concentration than carrier-contract models (Helium HHI = 0.27, Livepeer HHI = 0.31).

- Manuscript: `b3/paper/B3_GeoDePIN_Final_v8.docx`
- SSRN: [https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6483619](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6483619)

## Repository Structure

```
├── paper/                          # B2 manuscript
│   └── B2_Final_v20.docx
├── b3/                             # B3 manuscript + data
│   └── paper/
│       └── B3_GeoDePIN_PostSurgery.docx
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
├── paper/supplements/              # Supplementary Files S1-S8
│   └── S7_hhi_panel/                        # Quarterly HHI panel (14 protocols)
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

| Finding | B2 | B3 |
|---------|----|----|
| Allocation null | r = 0.19, p = 0.25, N = 37 | — |
| Sector gap | MW p = 0.031, d = 0.96 | Cited from B2 |
| Insider retention | rho = 0.54, p = 0.001 | — |
| Helium S2R | — | 1.84 (Feb 2026) |
| Demand concentration gap | — | Subscription 4-5x lower than carrier |
| Governance vs demand independence | Conceptual (§6.1) | Empirical (§5.1.2) |

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
5. **Supplementary materials:** S1-S8 in `paper/supplements/`.

See `CODEBOOK.md` for variable definitions.

## Citation

```bibtex
@article{zukowski2026tokenomics,
  title={Tokenomics as Institutional Design: A Normative Framework and
         Governance Concentration Analysis},
  author={Zukowski, Zach},
  year={2026},
  institution={Tokenization Systems}
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
