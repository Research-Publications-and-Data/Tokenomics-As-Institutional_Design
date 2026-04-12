# Saved Dune Analytics Query IDs

These queries are saved on the Dune Analytics platform and can be forked or re-run directly at `https://dune.com/queries/{query_id}`.

## Per-protocol HHI queries

| Protocol | Token | Query ID | Chain | Notes |
|---|---|---|---|---|
| Uniswap | UNI | 6937830 | Ethereum | Top-1000 holders, ERC-20 |
| Aave | AAVE | 6937831 | Ethereum | Top-1000 holders, ERC-20 |
| ENS | ENS | 6937833 | Ethereum | Top-1000 holders, ERC-20 |

## Stress event queries (TS- prefix series)

| Query ID Range | Description |
|---|---|
| 6929860-6929892 | Cross-protocol stress event response analysis (12 queries) |

## DePIN-specific queries

| Query ID | Protocol | Description |
|---|---|---|
| 6918150 | Helium | Spend-to-Reward ratio computation |
| 6917159 | GEODNET | Holder distribution |
| 6917162 | GEODNET | Burn trajectory |

## Template queries (in this repository)

| File | Purpose |
|---|---|
| `evm_concentration.sql` | Parameterized EVM governance HHI (replace `{{token_address}}`) |
| `evm_holder_list.sql` | EVM top-1000 holder export |
| `solana_concentration.sql` | Solana SPL governance HHI |
| `01_governance_hhi.sql` | Multi-chain governance concentration (original v1.0) |
| `demand_01-04_*.sql` | Demand-side burn/fee concentration |

## Notes

- All queries use DuneSQL syntax
- Decoded tables use `evt_` prefix columns; spellbook tables use unprefixed columns
- See `../supplements/S5_pipeline_specification.md` for full query documentation
- Solana SPL tokens (HNT, DRIFT, GRASS, W, META, IO, HONEY) use Helius DAS API, not Dune
