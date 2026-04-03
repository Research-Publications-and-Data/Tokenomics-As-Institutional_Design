# Tokenomics as Institutional Design: Replication Package

## Paper

Zukowski, Z. (2026). "Tokenomics as Institutional Design: A Normative Framework and Governance Concentration Analysis." Working Paper.

SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=PENDING

## Abstract

Governance concentration in token economies is not predicted by initial allocation design. A 40-protocol cross-section spanning DePIN, DeFi, infrastructure, and social token categories documents that the percentage of tokens allocated to team and investors at launch is uninformative about post-distribution governance concentration (r = 0.19, p = 0.25, N = 37). Protocols with more insider wallets among their top holders exhibit higher concentration even among their non-insider holders (Spearman rho = 0.54, p = 0.001, N = 34). DePIN protocols exhibit higher concentration than DeFi protocols (Mann-Whitney p = 0.031, Cohen's d = 0.96), a suggestive result sensitive to sample composition (23/30 LOO iterations). On-chain subsidy intensity correlates with concentration in levels (Pearson r = 0.58, p = 0.007, N = 20) but is driven entirely by Livepeer; an expanded 22-protocol sample confirms the null (r = 0.095, p = 0.674).

## Companion Paper

- **B3** (vertical, case studies): [GeoDePIN](https://github.com/Research-Publications-and-Data/geodnet-depin-analysis) — taxonomy, S2R trajectories, demand concentration, unit economics

## Data Sources

| Source | Coverage | Used for |
|--------|----------|----------|
| Dune Analytics | ERC-20 token holders (March 2026) | Governance concentration (HHI, Gini) |
| Helius DAS API | Solana token holders | META, DRIFT, GRASS, W, HONEY |
| Blockscout | Contract verification | Exclusion methodology (69 addresses, 20 protocols) |
| Token Terminal | Protocol revenue/incentives | Subsidy ratios, TT expansion (S8) |
| Tally / Snapshot | Governance voting power | Delegation analysis (8 protocols) |
| Blockworks | GEODNET + Helium financials | S2R validation, burn trajectories |

## Key Files

| File | Description |
|------|-------------|
| `paper/B2_Final_v17.docx` | Current manuscript (15,205 words, 8 figures) |
| `data/processed/regression_data_april2026.csv` | Master dataset (40 protocols) |
| `data/processed/exclusions_log.csv` | 69 excluded addresses with Blockscout labels |
| `data/processed/insider_classification.csv` | 390 top-holder classifications |
| `data/raw/helium_burn_concentration.csv` | Helium DC burn concentration (3,767 signers) |
| `data/raw/dimo_burn_concentration.csv` | DIMO license burn concentration (100 buyers) |
| `data/raw/livepeer_fee_concentration.csv` | Livepeer fee concentration (28 broadcasters) |
| `exhibits/` | Publication-quality figures (300 DPI PNG + PDF) |
| `paper/supplements/S1-S8` | Full supplement suite |

## Reproduction

1. Install: `pip install pandas scipy numpy matplotlib`
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
  journal={Working Paper},
  institution={Tokenization Systems}
}
```

Code: MIT. Data and paper: CC-BY-4.0.

zach@tokenization.systems | ORCID: 0009-0006-3642-2450
