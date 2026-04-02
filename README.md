# Tokenomics as Institutional Design: Replication Package

**Paper:** Zukowski, Z. (2026). "Tokenomics as Institutional Design: A Normative Framework
and Governance Concentration Analysis." Working Paper, Tokenization Systems.

**Author:** Zach Zukowski | zach@tokenization.systems | ORCID: 0009-0006-3642-2450

**SSRN:** https://papers.ssrn.com/sol3/cf_dev/AbsByAuth.cfm?per_id=10386216

## Abstract

This paper applies institutional economics to blockchain tokenomics, arguing that
governance token distribution functions as a constitutional design problem. Using a
novel dataset of 40 protocols (15 DePIN, 15 DeFi, 10 L1/L2/Infra), we measure
governance concentration via the Herfindahl-Hirschman Index (HHI) after excluding
protocol-controlled addresses (69 exclusions across 17 protocols). Key findings:
(1) initial insider allocation does not predict governance concentration (r = +0.19,
p = 0.25, N = 37); (2) DePIN protocols show higher concentration than DeFi
(Mann-Whitney p = 0.031, d = 1.00); (3) subsidy intensity predicts concentration
cross-sectorally (Pearson r = 0.58, p = 0.007, N = 20). A tautology check confirms
the insider-HHI null is not an artifact of definition: non-insider HHI correlates
with full HHI at ρ = 0.54 (p = 0.001, N = 34), indicating genuine post-distribution
dynamics.

## Data Sources

| Source | Used For | Protocols |
|--------|----------|-----------|
| Dune Analytics | ERC-20 holder distributions (March–April 2026 snapshot) | 34 EVM tokens |
| Helius DAS API | Solana token holders | META, DRIFT, GRASS, W, HONEY |
| Hypurrscan | Hyperliquid L1 token holders | HYPE |
| Filfox | Filecoin on-chain rich list | FIL |
| POKTscan | POKT on-chain balances | POKT |
| Tally | On-chain governance voting power | ARB, GTC, ENS, MKR, RPL |
| Snapshot | Off-chain governance voting power | AAVE, CRV, UNI |
| Token Terminal | Protocol revenue and token emissions | All protocols |
| CoinGecko | Market capitalization and FDV | All protocols |
| DePINScan | Active device counts | DePIN protocols |
| Tokenomist API | Token allocation schedules and vesting | 10 protocols |
| Blockscout / Nansen | Exclusion cross-validation | 17 protocols |

## Key Files

| File | Description | Rows |
|------|-------------|------|
| `data/processed/regression_data_april2026.csv` | Master dataset (40 protocols, 39 columns) | 40 |
| `data/processed/governance_concentration_april2026.csv` | HHI/Gini/Top-N concentration | 40 |
| `data/processed/exclusions_log.csv` | 69 excluded addresses with labels and confidence | 69 |
| `data/processed/insider_classification.csv` | Three-tier classification of 390 top-holder addresses | 390 |
| `data/processed/scoring_sheet.csv` | Normative scores: 14 DePIN protocols × 8 lenses, with evidence links | 112 |
| `data/processed/protocol_codebook.csv` | Comprehensive DePIN protocol metadata (50+ columns) | 14 |
| `paper/supplements/scoring_rubric.csv` | 8-lens scoring rubric with 0–3 anchors (instrument definition) | 8 |
| `outputs/regression_results.json` | All regression statistics cited in the paper | — |
| `outputs/leave_one_out_results.json` | LOO robustness for 3 significant findings | — |
| `outputs/tautology_check_results.json` | Non-insider HHI decomposition | — |
| `outputs/honey_requery_result.json` | HONEY HHI resolution (Dune solana_utils) | — |

## Reproduction

### Requirements

```bash
pip install pandas scipy numpy matplotlib requests
```

### Run order

```bash
# 1. Compute HHI/Gini/Top-N from raw holder lists
python analysis/01_compute_hhi.py

# 2. Classify insider addresses (three-tier methodology)
python analysis/03_insider_classification.py

# 3. Assemble regression dataset from authoritative sources
python analysis/04_assemble_dataset.py

# 4-9. Run all regressions (sector comparison, allocation, subsidy, robustness)
python analysis/05_09_regressions.py

# 10. Delegation analysis (voting vs holding HHI)
python analysis/10_delegation_analysis.py
```

Outputs are written to `outputs/regression_results.json`. The
`outputs/leave_one_out_results.json` and `outputs/tautology_check_results.json`
files were produced by supplementary scripts run during the April 2026 session.

### Environment variables for data collection (not needed for replication)

```bash
export DUNE_API_KEY=...            # Dune Analytics
export TOKEN_TERMINAL_API_KEY=...  # Token Terminal
export TALLY_KEY=...               # Tally governance
```

## Repository Structure

```
paper/                             # Manuscript and supplements
  B2_Final_v12.docx                # Current manuscript (v12)
  B2_Final_v12.pdf                 # PDF render (SSRN upload)
  supplements/
    S1_metric_definitions.md       # Governance metric definitions
    S2_scoring_rubric.md           # Philosophy-to-design scoring rubric (narrative)
    scoring_rubric.csv             # Machine-readable 8-lens rubric with 0–3 anchors
    S3_scoring_tables.md           # Protocol-level scoring tables
    S4_events_table.md             # Governance event log
    S5_pipeline_specification.md   # Full data pipeline spec
    S6_revenue_standardization.md  # Revenue and subsidy ratio standardization
    S7_hhi_panel/                  # Quarterly HHI panel (14 tokens)

data/
  raw/
    holder_lists/                  # Per-token holder CSVs (Dune, Helius, Hypurrscan)
    tokenomist/                    # Tokenomist API responses (10 protocols)
    coingecko_market.csv           # Market data snapshot (April 2026)
    token_terminal_metrics.csv     # Revenue/emissions per protocol
    depinscan_devices.csv          # DePIN active device counts
    snapshot_votes.csv             # Snapshot off-chain votes
    snapshot_proposals.csv         # Snapshot proposal metadata
    voting_hhi.csv                 # Computed voting concentration
    tally_delegates.csv            # Tally on-chain delegation data
    helium_s2r_cleaned.csv         # Helium S2R monthly time series (May 2023–Feb 2026)
    geodnet_monthly_burns.csv      # GEODNET monthly burns (Sep 2024–present)
    geodnet_monthly_emissions.csv  # GEODNET monthly emissions
  processed/
    governance_concentration_april2026.csv   # 40-protocol HHI/Gini/Top-N
    regression_data_april2026.csv            # 40-protocol regression dataset
    exclusions_log.csv                       # 69 excluded addresses
    insider_classification.csv               # 390 classified top-holder addresses
    scoring_sheet.csv                        # 14 DePIN protocols × 8 lens scores (primary)
    protocol_codebook.csv                    # DePIN protocol metadata (50+ columns)
    insider_analysis_results_v3.csv          # V1/V2/V3 + non-insider HHI
    delegation_adjusted_hhi.csv              # Voting vs holding HHI (8 protocols)
    allocation_design_variables.csv          # Tokenomist-derived allocation design
    tokenomist_allocations.csv               # Manual allocation with source URLs
    oaxaca_detailed_decomposition.csv        # Oaxaca-Blinder DePIN/DeFi decomposition
    robustness_all_metrics.csv               # Per-protocol alternative concentration metrics
    additional_exclusion_candidates.csv      # Pending exclusion review
    exclusion_crossvalidation.csv            # Blockscout/Nansen cross-validation results
  dune_queries/
    evm_concentration.sql          # ERC-20 HHI query template
    solana_concentration.sql       # Solana HHI query template
    evm_holder_list.sql            # Holder list export query
    02_helium_s2r.sql              # Helium monthly S2R burns vs issuance
    03_dimo_s2r.sql                # DIMO developer license burn S2R
    04_helium_who_burns.sql        # Helium DC burn concentration
    05_defi_benchmarks.sql         # DeFi governance HHI benchmarks
    06_geodnet_burns.sql           # GEODNET monthly burns (Dune #6917159)
    07_geodnet_emissions.sql       # GEODNET monthly emissions (Dune #6923474)
    08_geodnet_burn_concentration.sql  # GEODNET burn signer HHI (Dune #6917162)

analysis/
  01_compute_hhi.py                # Raw holder lists → HHI/Gini/Top-N
  03_insider_classification.py     # Three-tier insider identification
  04_assemble_dataset.py           # Build regression-ready dataset
  05_09_regressions.py             # All regressions (sector, allocation, subsidy, robustness)
  10_delegation_analysis.py        # Voting vs holding HHI
  full_regression.R                # R replication of OLS results
  oaxaca.R                         # Oaxaca-Blinder decomposition
  utils/                           # Data collection utilities

exhibits/                          # Publication figures
outputs/                           # Authoritative regression outputs
```

## Key Statistics (paper-cited, v12)

| Finding | Statistic | Script |
|---------|-----------|--------|
| Allocation null | r = +0.19, p = 0.25, N = 37 | `05_09_regressions.py` |
| Non-insider HHI tautology check | ρ = 0.54, p = 0.001, N = 34 | `outputs/tautology_check_results.json` |
| DePIN vs DeFi sector comparison | MW p = 0.031, d = 1.00 | `05_09_regressions.py` |
| Subsidy cross-sector | r = 0.58, p = 0.007, N = 20 | `05_09_regressions.py` |
| LOO allocation (39/39 protocols) | All p > 0.05 | `outputs/leave_one_out_results.json` |
| LOO sector (23/30 protocols significant) | DePIN > DeFi holds | `outputs/leave_one_out_results.json` |
| HYPE HHI | 0.0045 | `data/raw/holder_lists/HYPE_holders.csv` |
| HONEY HHI | 0.0175 | `outputs/honey_requery_result.json` |
| HHI-Gini correlation | r = 0.54 | `05_09_regressions.py` |
| Exclusions | 69 addresses, 17 protocols | `data/processed/exclusions_log.csv` |
| Insider-classified addresses | 390 | `data/processed/insider_classification.csv` |

## Known Data Notes

- **subsidy_ratio_onchain** is the authoritative subsidy measure (emissions / revenue,
  both on-chain). The legacy `subsidy_ratio` column uses a different denominator and
  should NOT be used. See `paper/supplements/S6_revenue_standardization.md`.
- **Gini sign convention**: The Dune query returns a negative Gini coefficient due to
  SQL ranking order. Corrected Gini = `-query_gini - 1/n`. Post-exclusion HHI is always
  positive and unaffected.
- **BAL/CRV**: veBAL and veCRV use vote-escrowed mechanics. Raw token HHI is reported,
  not voting power HHI, with a methodology caveat in the paper.
- **HONEY**: Computed from Dune `solana_utils.latest_balances` top-100, rescaled to
  actual supply (6.52B HONEY). HHI = 0.0175 (placeholder was 0.0198, within 5%).

## License

**Code** (`analysis/`): MIT License
**Data and paper** (`data/`, `paper/`): CC BY 4.0

## Citation

```bibtex
@article{zukowski2026tokenomics,
  title={Tokenomics as Institutional Design: A Normative Framework and
         Governance Concentration Analysis},
  author={Zukowski, Zach},
  year={2026},
  note={Working Paper, Tokenization Systems},
  url={https://papers.ssrn.com/sol3/cf_dev/AbsByAuth.cfm?per_id=10386216}
}
```
