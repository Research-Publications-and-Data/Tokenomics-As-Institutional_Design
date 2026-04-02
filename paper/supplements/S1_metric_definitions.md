# S1: Metric Definitions

## Governance Concentration Metrics

### Herfindahl-Hirschman Index (HHI)

HHI = sum(s_i^2) for i = 1 to N

where s_i is the share of total token balance held by address i, computed over the top-1,000 non-excluded holders.

Range: 0 (perfectly dispersed) to 1 (single holder). Values above 0.25 indicate high concentration by U.S. antitrust standards (DOJ/FTC Horizontal Merger Guidelines, 2010).

Implementation: `scripts/compute_concentration.py`, function `compute_concentration()`.

### Gini Coefficient

Computed using Brown's formula on the top-1,000 holder shares sorted descending:

G = (2 * sum(s_i * (N + 1 - i))) / (N * sum(s_i)) - (N + 1) / N

where s_i are shares sorted in descending order and i is rank (1-indexed).

Range: 0 (perfect equality) to 1 (maximum inequality).

### Top-N Concentration Ratios

Top-1%: share of total balance held by the single largest holder.
Top-5%: cumulative share of the 5 largest holders.
Top-10%: cumulative share of the 10 largest holders.

### Delegation Amplification Ratio

hhi_ratio = voting_hhi / holding_hhi

where voting_hhi is the HHI of delegated voting power (from Tally or Snapshot) and holding_hhi is the token-holding HHI from the governance concentration cross-section.

Values above 1.0 indicate delegation concentrates governance power beyond holding concentration. Values below 1.0 indicate delegation distributes governance power.

### Synergy Index

Mean of five philosophical lens scores (Kantian publicity, Rawlsian fairness, republican non-domination, Ostromian polycentricity, Hayekian knowledge-use), each scored 0 to 3 per the rubric in Supplementary File S2. The Index is designed to correlate with governance quality but is not a causal claim.

## Share Normalization

For tokens with 1,000 holders in the holder list (Dune query limit), shares are computed as:

s_i = balance_i / sum(balance_j for j = 1 to N)

This normalizes within the observed top-1,000. For tokens with known total supply corrections (ZRO, AXL, MOR, which returned fewer than 100 holders in Dune), the corrected total supply is used as the denominator:

s_i = balance_i / total_supply_corrected

Corrected total supply values are stored in `holder_lists/total_supply_corrections.json`.

## Exclusion Methodology

Two types of address exclusions are applied before HHI computation:

### 1. Exchange Custodian Exclusions

Applied at Dune query time via `labels.addresses` table with `label_type = 'exchange'`. Exchange addresses hold tokens in custody for retail users and do not exercise governance rights as a single entity. The Dune labels database is non-deterministic (labels grow over time); the February 2026 snapshot is authoritative for this paper. Re-runs with March 2026 or later labels are treated as robustness checks only.

### 2. Protocol-Controlled Address Exclusions

17 individually verified addresses across 14 tokens. Each address was identified by manual inspection of the top-10 holders for each token, then verified via Blockscout contract labels, Nansen Profiler API, or on-chain ABI inspection. 11 of 17 (65%) are confirmed by at least 2 independent sources.

Categories of excluded addresses:
- Staking contracts (stkAAVE, sGMX): pass-through custodians where individual holders retain delegation rights; the contract itself never votes.
- Bridge custodians (RENDER Wormhole, GRT BridgeEscrow): tokens locked backing L2 supply; governance rights transfer to L2 holders.
- Vesting locks (ENS TokenLock, Lido GnosisSafe multisigs): time-locked tokens not available for governance participation.
- Protocol treasuries (UNI Timelock, ARB FixedDelegateWallet, OP GnosisSafe, RPL RocketVault): protocol-controlled funds with zero or fixed delegation.
- Migration contracts (Maple MPL-to-SYRUP Migrator, stSYRUP vault): intermediate contracts holding tokens during migration.
- Minting reserves (Livepeer Minter): unminted inflation reserve.

Full list with addresses, identities, verification sources, and before/after HHI impact: `data/exclusions_log.csv`.
Cross-validation documentation: `data/exclusion_crossvalidation.csv`, `data/exclusion_crossvalidation_summary.md`.

## Multi-Chain Token Merging

Two tokens span multiple blockchains:
- RENDER: Ethereum RNDR + Solana RENDER. Merged by concatenating holder lists. Wormhole bridge address excluded to prevent double-counting of bridged tokens.
- Maple: MPL (Ethereum, 18 decimals) + SYRUP (Ethereum, 18 decimals). SYRUP balances divided by 100 to convert to MPL-equivalent (1 MPL = 100 SYRUP migration ratio). Migration contract excluded.

Implementation: `scripts/merge_multichain.py`.

## Solana Token Measurement

Dune's `solana.daily_balances` systematically undercounts SPL token holders. Four tokens were re-collected via Helius DAS API (`getTokenAccounts`):

| Token | Dune holders | Helius holders | Correction factor |
|-------|-------------|----------------|-------------------|
| META  | 29          | 5,067          | 175x              |
| DRIFT | 104         | 27,888         | 268x              |
| GRASS | 291         | 46,607         | 160x              |
| W     | 98          | 99,980         | 1,020x            |

Three remaining Solana tokens (JUP, HNT, RENDER) use Dune-sourced data with 1,000 holders (query limit). Their HHI values are computed from the available top-1,000 and may understate true concentration if the long tail is significant.

## Statistical Tests

All sector comparisons use Welch's t-test (unequal variances assumed) and Cohen's d for effect size. Non-parametric Mann-Whitney U is reported as a robustness check. Correlations use both Pearson r and Spearman rho. No multiple-comparison correction is applied given the exploratory, descriptive nature of the analysis.
