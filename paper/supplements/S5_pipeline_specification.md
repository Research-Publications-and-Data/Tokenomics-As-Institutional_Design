# S5: Data Collection Pipeline Specification

## Overview

The data collection pipeline produces governance concentration metrics for 40 protocols across 8 blockchains using 10 data sources. The pipeline is designed for single-snapshot cross-sectional analysis (March 2026) with reproducibility as a first-class requirement.

## Pipeline Architecture

```
[Data Sources] → [Collection Scripts] → [Raw Data] → [Processing] → [Analysis-Ready Data]

Dune Analytics ──→ run_dune_queries.py ──→ holder_lists/*.csv ──┐
Helius DAS API ──→ update_holder_lists.py ──→ holders_helius_*.csv ──┤
Filfox API ──→ filfox_richlist.py ──→ holders_FIL.csv ──┤
POKTscan API ──→ poktscan_richlist.py ──→ holders_POKT.csv ──┤
                                                              │
                         merge_multichain.py ←────────────────┘
                              │
                     compute_concentration.py
                              │
                     governance_concentration_april2026.csv (Table 4)
                              │
CoinGecko API ──→ refresh_market_data.py ──→ coingecko_market.csv ──┐
Token Terminal ──→ tokenterminal_collect.py ──→ tokenterminal_*.csv ──┤
DeFiLlama API ──→ defillama_fallback.py ──→ defillama_*.csv ──┤
Tokenomist ──→ (manual) ──→ tokenomist_allocations.csv ──┤
DePINScan ──→ (manual) ──→ depinscan_devices.csv ──┤
DeepDAO ──→ (manual) ──→ deepdao_treasury.csv ──┤
                                                    │
                     assemble_regression_data.py ←──┘
                              │
                     regression_data_april2026.csv
                     covariates_merged.csv

Tally API ──→ collect_governance.py ──→ tally_delegates.csv ──┐
Snapshot GQL ──→ collect_governance.py ──→ snapshot_*.csv ──┤
                                                             │
                     (manual computation) ←──────────────────┘
                              │
                     voting_hhi.csv
                     governance_participation.csv (Table 6)
```

## Data Source Specifications

### 1. Dune Analytics

**Access:** Community plan (free tier, 2,500 credits/period)
**API:** `api.dune.com/api/v1/`
**Authentication:** API key in header

**Queries:**
- `queries/evm_concentration.sql`: Parameterized EVM holder query. One execution per token per chain. Uses `erc20_{chain}.evt_Transfer` for cumulative net balances.
- `queries/evm_holder_list.sql`: Top-1000 holder extraction with exchange label exclusion.
- `queries/solana_concentration.sql`: Solana SPL token concentration (limited accuracy; see Helius correction below).

**Tables used:**
- `tokens.balances_daily`: Preferred over transfer-event scans (cheaper, pre-aggregated). Available for Ethereum, Arbitrum, Optimism, Polygon.
- `labels.addresses`: Exchange custodian identification. Non-deterministic; labels grow over time. February 2026 snapshot is authoritative.
- `erc20_{chain}.evt_Transfer`: Fallback for chains without `tokens.balances_daily`.

**Known limitations:**
- Community plan does not access enriched tables (returns "Table does not exist" for premium tables).
- `labels.addresses` is non-deterministic; re-running queries produces HHI drift.
- Solana holder counts are systematically undercounted (see Helius correction).
- Query execution costs credits; query creation (via MCP) is free.

**Script:** `scripts/run_dune_queries.py`, `scripts/fetch_dune_results.py`

### 2. Helius DAS API

**Access:** Free tier (50,000 credits/day)
**API:** `https://mainnet.helius-rpc.com/?api-key={key}`
**Method:** `getTokenAccounts` (Digital Asset Standard)

**Purpose:** Correct Dune's Solana holder undercounting. Enumerates all SPL token accounts for a given mint.

**Tokens corrected:**
| Token | Mint address | Helius holders |
|-------|-------------|----------------|
| META | METAewgxyPbgwsseH8T16a39CQ5VyVxGbpKRnHe4gMQE | 5,067 |
| DRIFT | DriFtupJYLTosbwoN8koMbEYSx54aFAVLddWsbksjwg7d | 27,888 |
| GRASS | Grass7B4RdKfBCjTKgSqnXkqjwiGvQyFbuSCUJr3XXjs | 46,607 |
| W | 85VBFQZC9TZkfaptBWjvUw7YbZjy52A6mjtPGjstQAmQ | 99,980 |

**Script:** `scripts/update_holder_lists.py`

### 3. Filfox API

**Access:** Free, no authentication
**API:** `https://filfox.info/api/v1/`
**Endpoint:** `/rich-list?pageSize=1000`
**Purpose:** Filecoin rich list (native chain, not queryable via Dune)
**Script:** `scripts/filfox_richlist.py`

### 4. POKTscan API

**Access:** Free, no authentication
**API:** `https://poktscan.com/api/`
**Purpose:** Pocket Network rich list (native chain)
**Script:** `scripts/poktscan_richlist.py`

### 5. CoinGecko API

**Access:** Free tier (rate-limited)
**API:** `https://api.coingecko.com/api/v3/`
**Endpoints:** `/coins/{id}` for market cap, FDV, price, circulating supply, total supply
**Script:** `scripts/refresh_market_data.py`
**Output:** `data/coingecko_market.csv`

### 6. Token Terminal API

**Access:** Subscription (unlimited tier)
**API:** `https://api.tokenterminal.com/v2/`
**Endpoints:** `/projects/{id}/metrics` for revenue, fees, token incentives, TVL
**Script:** `scripts/tokenterminal_collect.py`
**Output:** `data/tokenterminal_financials.csv`

### 7. DeFiLlama API

**Access:** Free, no authentication
**API:** `https://api.llama.fi/`
**Endpoints:** `/protocol/{name}` for TVL; `/fees/{name}` for fees/revenue
**Purpose:** Fallback for protocols not covered by Token Terminal; primary source for stablecoin supply data
**Script:** `scripts/defillama_fallback.py`

### 8. Tally API

**Access:** Free tier
**API:** GraphQL at `https://api.tally.xyz/query`
**Purpose:** On-chain governance delegate data for EVM protocols
**Protocols queried:** Compound, Aave, Uniswap, Optimism, Arbitrum (top 100 delegates each)
**Script:** `scripts/collect_governance.py`
**Output:** `data/tally_delegates.csv`

### 9. Snapshot GraphQL

**Access:** Free, no authentication
**API:** `https://hub.snapshot.org/graphql`
**Purpose:** Off-chain governance voting data
**Spaces queried:** DIMO, WeatherXM, Lido, Compound, Aave, MakerDAO, Uniswap, ENS, Arbitrum, Optimism
**Script:** `scripts/collect_governance.py`
**Output:** `data/snapshot_proposals.csv`, `data/snapshot_spaces.csv`, `data/snapshot_votes.csv`

### 10. Manual Sources

**Tokenomist / Protocol Documentation:**
- Token allocation breakdowns compiled from official documentation (whitepapers, token distribution posts, governance forum announcements).
- Each allocation verified against primary source; URL documented in `source_url` column.
- Confidence rating: high (official documentation with percentages), medium (inferred from vesting schedules or multiple sources), unverifiable (MetaDAO, TEC).
- Output: `data/tokenomist_allocations.csv`

**DePINScan / Messari / Protocol Explorers:**
- DePIN active device counts from DePINScan, Messari quarterly reports, and protocol-specific explorers.
- Point-in-time snapshots; measurement differs across implementations.
- Output: `data/depinscan_devices.csv`

**DeepDAO / DeFiLlama:**
- DAO treasury AUM from DeepDAO or DeFiLlama treasury pages.
- DeFi and infrastructure protocols have coverage; DePIN protocols do not (treasury values set to NaN).
- Output: `data/deepdao_treasury.csv`

## Processing Pipeline

### Step 1: Holder List Collection

```bash
# EVM tokens (via Dune)
python scripts/run_dune_queries.py          # Creates/executes Dune queries
python scripts/fetch_dune_results.py        # Downloads results to holder_lists/

# Solana tokens (via Helius)
python scripts/update_holder_lists.py       # Helius getTokenAccounts → holder_lists/

# Native chain tokens
python scripts/filfox_richlist.py           # Filecoin → holder_lists/holders_FIL.csv
python scripts/poktscan_richlist.py         # POKT → holder_lists/holders_POKT.csv
```

### Step 2: Multi-Chain Merge

```bash
python scripts/merge_multichain.py
# RENDER: combines holders_RNDR_ETH.csv + holders_RENDER_SOL.csv
#         excludes Wormhole bridge address to prevent double-counting
# Maple: combines holders_MPL.csv + holders_SYRUP.csv
#        SYRUP balances / 100 for MPL-equivalent
```

### Step 3: Compute Concentration

```bash
python scripts/compute_concentration.py
# Input: holder_lists/*.csv + exclusions from PROTOCOL_EXCLUSIONS dict
# Output: governance_concentration_april2026.csv
# Process:
#   For each token:
#     1. Load holder CSV
#     2. Exclude protocol-controlled addresses (PROTOCOL_EXCLUSIONS)
#     3. Take top 1000 holders
#     4. Compute HHI, Gini, Top-1/5/10, N
#     5. Apply total_supply_corrections.json for ZRO/AXL/MOR
```

### Step 4: Collect Market and Financial Data

```bash
python scripts/refresh_market_data.py       # CoinGecko → coingecko_market.csv
python scripts/tokenterminal_collect.py     # Token Terminal → tokenterminal_financials.csv
python scripts/defillama_fallback.py        # DeFiLlama → defillama_fees_raw.json
```

### Step 5: Assemble Regression Dataset

```bash
python scripts/assemble_regression_data.py
# Merges: governance_concentration + coingecko_market + tokenterminal
#         + tokenomist_allocations + depinscan_devices + deepdao_treasury
# Output: regression_data_april2026.csv (40 × 34)
#         covariates_merged.csv (40 × 46)
```

### Step 6: Collect Voting Data

```bash
python scripts/collect_governance.py
# Tally: top 100 delegates for 5 protocols
# Snapshot: all proposals and votes for 10 spaces
# Output: tally_delegates.csv, snapshot_*.csv, voting_hhi.csv
```

### Step 7: Generate Figures

```bash
python scripts/generate_figure3.py
# Output: figures/figure3_governance_hhi_34protocol.png
# Horizontal bar chart, 40 protocols, colored by category
```

## Verification Checklist

After running the pipeline, verify:

1. `governance_concentration_april2026.csv` has 40 rows
2. All HHI values are between 0 and 1
3. No protocol has N < 50 holders (minimum for inclusion)
4. Exclusions applied: check that excluded addresses do not appear in top-10 for affected tokens
5. Multi-chain merge: RENDER total holders > max(ETH holders, SOL holders)
6. Helius correction: META, DRIFT, GRASS, W have >1000 holders
7. Regression dataset: `regression_ready` column is True for 31/40 protocols
8. Insider correlation: `pearsonr(insider_pct, hhi)` returns r near +0.08, p near 0.64

## Refresh Cadence

This is a single-snapshot analysis (March 2026). For longitudinal extension:

- Holder snapshots: monthly refresh via Dune scheduled queries (requires Team plan)
- Market data: daily refresh via CoinGecko API
- Voting data: quarterly refresh via Tally/Snapshot
- Allocations: annual review (allocation percentages are genesis-fixed)
- Device counts: quarterly review (DePINScan, protocol explorers)

## Credit and Cost Budget

| Source | Cost per refresh | Monthly (30 refreshes) |
|--------|-----------------|----------------------|
| Dune (Community) | ~390 credits | 11,700 credits (exceeds 2,500 plan) |
| Dune (Team) | Same | Covered by plan |
| Helius | ~200K credits | Within free 50K/day |
| All others | Free | Free |

For sustained monitoring, upgrade Dune to Team plan or run queries manually in Dune UI (free, no credit cost).
