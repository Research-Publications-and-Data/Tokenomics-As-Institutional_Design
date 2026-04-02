# Analysis Scripts

## Pipeline Overview

The numbered scripts correspond to the analysis pipeline for B2. Run them in order
from the repo root.

| Script | Description | Input | Output |
|--------|-------------|-------|--------|
| `01_compute_hhi.py` | Compute HHI, Gini, Top-N from raw holder lists | `data/raw/holder_lists/` | `data/processed/governance_concentration_april2026.csv` |
| `03_insider_classification.py` | Three-tier insider identification for top-10 holders | `data/processed/governance_concentration_april2026.csv` | `data/processed/insider_classification.csv` |
| `04_assemble_dataset.py` | Build regression-ready dataset from authoritative sources | `data/processed/*.csv`, `data/raw/*.csv` | `data/processed/regression_data_april2026.csv` |
| `05_09_regressions.py` | All regression analyses (sector comparison, allocation null, subsidy, robustness) | `data/processed/regression_data_april2026.csv` | `outputs/regression_results.json` |
| `10_delegation_analysis.py` | Voting vs holding HHI (Tally + Snapshot) | `data/raw/tally_delegates.csv`, `data/raw/snapshot_votes.csv` | `data/processed/delegation_adjusted_hhi.csv` |

Note: Script `02_apply_exclusions.py` is not a standalone script — exclusions are applied
inline in `01_compute_hhi.py` using `data/processed/exclusions_log.csv` as input.
Scripts `06_subsidy_regression.py`, `07_tautology_check.py`, `08_leave_one_out.py`,
and `09_robustness_metrics.py` are sections within `05_09_regressions.py`.

## R Replication

- `full_regression.R` — OLS regressions using base R; cross-validates Python results
- `oaxaca.R` — Oaxaca-Blinder decomposition of DePIN vs DeFi concentration gap

## utils/

Data collection utilities. These were used to build the dataset and are included for
transparency. They are NOT needed to reproduce the paper statistics from the processed
data files.

| Script | Description |
|--------|-------------|
| `run_dune_queries.py` | Submit and monitor Dune queries (requires `DUNE_API_KEY`) |
| `fetch_dune_results.py` | Download Dune execution results to `data/raw/holder_lists/` |
| `update_holder_lists.py` | Update holder lists for a new snapshot date |
| `refresh_market_data.py` | Refresh CoinGecko market data |
| `tokenterminal_collect.py` | Collect Token Terminal revenue/emissions data |
| `defillama_fallback.py` | DefiLlama fallback for missing Token Terminal data |
| `filfox_richlist.py` | Scrape Filecoin rich list from Filfox |
| `poktscan_richlist.py` | Scrape POKT balance data from POKTscan |
| `collect_fil_pokt.py` | Orchestrate FIL + POKT collection |
| `merge_multichain.py` | Merge multi-chain holder data (RENDER: ETH + SOL) |
| `build_fdv_supplement.py` | Build FDV supplement table |
| `generate_figure3.py` | Generate Figure 3 (governance HHI distribution) |

## Requirements

```
pandas>=2.0
scipy>=1.11
numpy>=1.24
matplotlib>=3.7
requests>=2.28
python-docx>=0.8.11  # only for apply_paper_patches.py utility
```
