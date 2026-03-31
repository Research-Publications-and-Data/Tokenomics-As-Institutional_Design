# Tokenomics as Institutional Design: Replication Package

**Paper:** Zukowski, Z. (2026). "Tokenomics as Institutional Design: Governance Concentration,
Normative Legitimacy, and the Design of Autonomous Economies."
*Working paper, submitted to Frontiers in Blockchain.*

**SSRN:** [per_id 10386216](https://papers.ssrn.com/sol3/cf_dev/AbsByAuth.cfm?per_id=10386216)
**Author:** Zach Zukowski | zach@tokenization.systems | ORCID: 0009-0006-3642-2450

## Key Findings

1. **Exclusion methodology:** Protocol-controlled addresses (staking contracts, bridges,
   vesting locks) inflate naive HHI by 2-20x. 17 exclusions across 14 protocols documented
   in `data/exclusions_log.csv`, 65% cross-validated via Blockscout + Nansen.

2. **Sector invariance:** DePIN mean HHI 0.088 vs DeFi 0.059 (p = 0.20, not significant).
   DePIN vs L1/L2 Infra: 2.45x (p = 0.038, significant).

3. **Allocation null:** Insider allocation does not predict HHI (r = +0.08, p = 0.64, N = 33).
   Post-distribution dynamics dominate initial conditions.

4. **Delegation amplification:** DePIN protocols concentrate governance through delegation
   (DIMO 6.0x, WXM 3.3x), infrastructure protocols distribute (OP 0.79x, ARB 4.3x).

## Repository Structure

```
data/                              # All datasets
  governance_concentration_*.csv   # Primary: 35-protocol HHI/Gini (Table 4)
  exclusions_log.csv               # 17 protocol-controlled address exclusions (Table 5)
  regression_data_*.csv            # Merged regression dataset (35 x 34)
  covariates_merged.csv            # Full covariate dataset (35 x 46)
  tokenomist_allocations.csv       # Token allocations with source URLs
  depinscan_devices.csv            # DePIN active device counts
  governance_participation.csv     # Holding vs voting HHI (Table 6)
  voting_hhi.csv                   # Voting concentration (Tally + Snapshot)
  snapshot_*.csv / tally_*.csv     # Raw governance data
  coingecko_market.csv             # Market data snapshot
  tokenterminal_financials.csv     # Revenue, fees, incentives
  deepdao_treasury.csv             # Treasury AUM (DeFi verified; DePIN NaN)
holder_lists/                      # Top-1000 holder balances per token (41 files)
  holders_helius_*.csv             # Helius-sourced Solana data (4 files, 179K+ rows)
queries/                           # DuneSQL queries
scripts/                           # Python pipeline
figures/                           # Generated figures
```

## Reproduction

```bash
# Reproduce Table 4 (HHI/Gini)
python scripts/compute_concentration.py

# Reproduce regression
python scripts/assemble_regression_data.py

# Reproduce Figure 3
python scripts/generate_figure3.py
```

## Data Sources

Dune Analytics, Helius DAS API, Filfox, POKTscan, Tally, Snapshot,
CoinGecko, Token Terminal, DeFiLlama, Blockscout, Nansen.

## License

CC-BY 4.0
