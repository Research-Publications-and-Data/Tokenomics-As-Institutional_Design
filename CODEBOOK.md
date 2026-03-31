# Codebook: Variable Definitions

## governance_concentration_april2026.csv

| Variable | Description |
|----------|-------------|
| protocol | Protocol name |
| token | Governance token symbol |
| category | DeFi, DePIN, L1_L2_Infra, Social_Dead |
| hhi | Herfindahl-Hirschman Index; sum of squared shares, top-1000 holders, post-exclusion |
| gini | Gini coefficient; Brown's formula on top-1000 shares |
| top1_pct | Largest single holder share (%) |
| n_holders | Holders in computation (max 1000) |
| distribution_type | airdrop, team_vc, mining |
| governance_model | delegate, token_weighted, futarchy |

## exclusions_log.csv

| Variable | Description |
|----------|-------------|
| token | Token symbol |
| address | Excluded address (full hex) |
| identity | Verified identity |
| exclusion_reason | Why excluded |
| hhi_before / hhi_after | HHI impact |
| source | Verification source (Blockscout, Nansen, ABI) |

## tokenomist_allocations.csv

| Variable | Description |
|----------|-------------|
| insider_pct | team_pct + investor_pct |
| source_url | Primary documentation URL |
| confidence | high, medium, unverifiable |

## Measurement Notes

- HHI: shares renormalized within top-1000. Total supply corrections for ZRO/AXL/MOR.
- Gini: Brown's formula. G = (2 * sum(s_i * (N+1-i))) / (N * sum(s_i)) - (N+1)/N
- Exchange exclusions via Dune labels.addresses (Feb 2026 snapshot; non-deterministic).
- Multi-chain: RENDER (ETH+SOL) and MPL+SYRUP merged by address.
