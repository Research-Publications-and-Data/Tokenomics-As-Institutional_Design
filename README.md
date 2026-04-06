# Tokenization Systems: Governance Concentration Research

Two-paper research program on governance and demand concentration in token economies.

## Papers

### B2: Tokenomics as Institutional Design

**Allocation Is Uninformative.** A 40-protocol cross-section documents that initial token allocation design does not predict post-distribution governance concentration (r = 0.19, p = 0.25, N = 37). DePIN protocols exhibit higher concentration than DeFi (Mann-Whitney p = 0.031, Cohen's d = 0.96), though the result is sensitive to sample composition. On-chain subsidy correlates with concentration only through a single outlier (Livepeer); an expanded 22-protocol sample confirms the null.

- Manuscript: `paper/B2_Final_v20.docx` (15,205 words, 8 figures)
- SSRN: [Pending upload]

### B3: Who Burns the Tokens?

**Demand concentration is an independent failure mode.** A 34-month longitudinal analysis of Helium documents the first empirical observation of burn-to-mint equilibrium threshold crossing (S2R = 1.84). Subscription-based burn models (GEODNET HHI = 0.055, DIMO HHI = 0.063) produce four to five times less demand concentration than carrier-contract models (Helium HHI = 0.27, Livepeer HHI = 0.31). Resource Dependence Theory grounds this finding: if the top two burn addresses ceased purchasing, Helium's S2R would fall from 1.84 to approximately 0.62 within one month.

- Manuscript: `b3/paper/B3_GeoDePIN_PostSurgery.docx` (11,797 words, refs [1]-[44], 3 figures)
- SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6483619

## Repository Structure

```
├── paper/                          # B2 manuscript
│   └── B2_Final_v20.docx
├── b3/                             # B3 manuscript + data
│   └── paper/
│       └── B3_GeoDePIN_PostSurgery.docx
├── data/
│   ├── processed/                  # Master datasets
│   │   ├── regression_data_april2026.csv    # 40 protocols
│   │   ├── exclusions_log.csv               # 69 excluded addresses
│   │   ├── insider_classification.csv       # 390 classifications
│   │   └── scoring_sheet.csv                # 12-protocol scoring
│   └── raw/                        # Source data
│       ├── helium_s2r_cleaned.csv           # 34-month S2R trajectory
│       ├── helium_burn_concentration.csv    # 3,767 burn signers
│       ├── dimo_burn_concentration.csv      # 100 license buyers
│       ├── livepeer_fee_concentration.csv   # 28 broadcasters
│       ├── geodnet_monthly_burns.csv
│       └── geodnet_monthly_emissions.csv
├── exhibits/                       # Publication figures (300 DPI)
├── analysis/                       # Replication scripts
├── outputs/                        # Computed results (JSON)
└── paper/supplements/              # S1-S8
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

1. `pip install pandas scipy numpy matplotlib`
2. Run scripts in `analysis/` (numbered order)
3. Key output: `outputs/regression_results.json`

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
