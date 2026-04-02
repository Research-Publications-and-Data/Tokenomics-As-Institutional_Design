# Dune Analytics Query Registry

All queries were run with a snapshot cutoff of **2026-04-01**. Queries use the
DuneSQL dialect (Trino/PrestoSQL).

## Query Files

### B2 Governance Concentration (April 2026 snapshot)
| File | Description |
|------|-------------|
| `evm_concentration.sql` | ERC-20 HHI/Gini/Top-N query (template — fill in `{{contract_address}}`, `{{chain_table}}`, `{{decimals}}`, `{{symbol}}`) |
| `evm_holder_list.sql` | ERC-20 top-1000 holder export (used to generate `data/raw/holder_lists/TOKEN_holders.csv`) |
| `solana_concentration.sql` | Solana SPL token HHI query using `solana_utils.latest_balances` |

### DePIN Protocol Analyses (B2 §4–§5, uses Feb–Apr 2026 data)
| File | Dune ID | Paper Reference | Description |
|------|---------|-----------------|-------------|
| `02_helium_s2r.sql` | — | B2 Figure 2 / Table 2 | Helium monthly S2R (burns vs. issuance, May 2023–Feb 2026) |
| `03_dimo_s2r.sql` | — | B2 §5.B | DIMO developer license burn S2R (Polygon, Jan 2024–Feb 2026) |
| `04_helium_who_burns.sql` | — | B2 §5.A | Helium DC burn concentration — "who burns?" |
| `05_defi_benchmarks.sql` | — | B2 Table 2 | DeFi governance HHI benchmarks (6 Ethereum protocols, Feb 2026) |
| `06_geodnet_burns.sql` | 6917159 | B2 §5.C | GEODNET monthly burn transactions + GEOD burned (Solana) |
| `07_geodnet_emissions.sql` | 6923474 | B2 §5.C | GEODNET monthly emissions (Solana) |
| `08_geodnet_burn_concentration.sql` | 6917162 | B2 §5.C | GEODNET burn signer HHI — concentration of burn activity |

Note: Queries 02–05 are templates without saved Dune IDs (run ad hoc during data collection).
Queries 06–08 have saved IDs in the Dune workspace.

## Authoritative Query IDs (April 2026 session)

These IDs correspond to saved queries in the Dune workspace. Use them to re-run
or inspect the exact queries that produced the April 2026 snapshot data.

| Token | Query ID | Notes |
|-------|----------|-------|
| AAVE | 6929860 | ethereum.erc20 evt_transfer |
| ARB | 6929861 | arbitrum (erc20_arbitrum.evt_transfer corrected) |
| BAL | 6929862 | ethereum, raw token only |
| COMP | 6929863 | ethereum |
| CRV | 6929864 | ethereum |
| DIMO | 6929865 | polygon |
| ENS | 6929866 | ethereum |
| ETHFI | 6929867 | ethereum |
| FIL | — | Filfox richlist (see `utils/filfox_richlist.py`) |
| GEOD | 6929868 | polygon |
| GMX | 6929869 | arbitrum |
| GRASS | 6929870 | Solana (Helius DAS API) |
| GRT | 6929871 | ethereum |
| GTC | 6929872 | ethereum |
| HNT | — | Solana (solana_utils.latest_balances) |
| HONEY | — | Solana (solana_utils.latest_balances, top-100 only) |
| HYPE | — | Hypurrscan richlist (Hyperliquid L1) |
| IOTX | 6929873 | ethereum |
| JUP | 6929874 | Solana |
| LDO | 6929875 | ethereum |
| LPT | 6929876 | ethereum |
| META | 6929877 | Solana (Helius DAS API) |
| MKR | 6929878 | ethereum |
| MOR | 6929879 | ethereum |
| MPL | 6929880 | ethereum |
| OP | 6929881 | optimism |
| POKT | — | POKTscan API (see `utils/poktscan_richlist.py`) |
| POL | 6929882 | polygon |
| RENDER | 6929883 | Solana (Helius) + ethereum (merged) |
| RPL | 6929884 | ethereum |
| TEC | 6929885 | xdai/gnosis |
| UNI | 6929886 | ethereum |
| W | 6938147 | Solana (Helius DAS API) |
| WXM | 6929887 | polygon |
| ZRO | 6929888 | ethereum |
| ANYONE | 6929889 | ethereum |
| DRIFT | 6929890 | Solana (Helius DAS API) |
| ATH | 6929891 | ethereum |
| AXL | 6929892 | ethereum |
| SYRUP | 6929893 | ethereum |

## Credit Cost Estimates

- EVM concentration query (1 token, top-1000): ~2–5 Dune credits
- Solana concentration (via solana_utils): ~10–20 Dune credits
- Full session (40 tokens): ~200 credits estimated

## Usage

```bash
# Set API key
export DUNE_API_KEY=your_key_here

# Run all queries (submits and polls for completion)
python analysis/utils/run_dune_queries.py

# Download results to data/raw/holder_lists/
python analysis/utils/fetch_dune_results.py
```
