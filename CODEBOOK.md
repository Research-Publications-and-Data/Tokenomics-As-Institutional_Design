# Codebook: B2 Governance Concentration Dataset

**Version:** April 2026 (40-protocol universe)
**Paper:** "Tokenomics as Institutional Design: A Normative Framework and Governance Concentration Analysis"

---

## regression_data_april2026.csv
**Location:** `data/processed/regression_data_april2026.csv`
**Rows:** 40 (one per protocol)
**Unit of observation:** Protocol × token × April 2026 snapshot

| Column | Type | Description | Source |
|--------|------|-------------|--------|
| protocol | str | Protocol full name (e.g., "Aave", "Helium") | Manual |
| token | str | Governance token ticker (e.g., "AAVE", "HNT") | Manual |
| category | str | Sector: DePIN / DeFi / L1_L2_Infra | Manual |
| chain | str | Primary blockchain for holder data | Manual |
| measurement_type | str | Method: dune_erc20 / helius_das / hypurrscan / filfox / poktscan | Derived |
| hhi | float | Post-exclusion HHI (top-1000 holders, rescaled to total supply) | Computed |
| gini | float | Post-exclusion Gini coefficient (corrected: `−query_gini − 1/n`) | Computed |
| top1_pct | float | Post-exclusion top-1 holder share (0–1) | Computed |
| top5_pct | float | Post-exclusion top-5 holder share (0–1) | Computed |
| top10_pct | float | Post-exclusion top-10 holder share (0–1) | Computed |
| n_holders | int | Number of holders indexed in the snapshot | Dune/Helius |
| total_balance_top1000 | float | Sum of top-1000 holder balances (raw token units) | Dune/Helius |
| source | str | Data source identifier | Derived |
| query_id | str | Dune query ID used for this token (if applicable) | Dune |
| notes | str | Methodological notes (e.g., veCRV caveat, chain selection) | Manual |
| team_pct | float | Team allocation at genesis (0–100) | Project docs / Tokenomist |
| investor_pct | float | Investor allocation at genesis (0–100) | Project docs / Tokenomist |
| community_pct | float | Community/ecosystem allocation (0–100) | Project docs / Tokenomist |
| treasury_pct | float | Foundation/treasury allocation (0–100) | Project docs / Tokenomist |
| other_pct | float | Other allocation (0–100) | Project docs / Tokenomist |
| insider_pct | float | team_pct + investor_pct (total insider allocation) | Derived |
| revenue_annual_usd | float | Annualized protocol revenue (trailing 30d × 12, USD) | Token Terminal |
| revenue_source | str | Revenue data source identifier | Derived |
| fdv_usd | float | Fully diluted valuation (USD) | CoinGecko |
| market_cap_usd | float | Market capitalization (USD) | CoinGecko |
| incentives_annual_usd | float | Annualized token emissions (trailing 30d × 12, USD) | Token Terminal |
| subsidy_ratio | float | **LEGACY — DO NOT USE.** Old emissions/(rev+emissions) formula | Deprecated |
| treasury_usd | float | Treasury AUM (USD); NaN for DePIN protocols | DeepDAO / project docs |
| active_devices | int | Active hardware devices (DePIN only); NaN otherwise | DePINScan |
| maturity_years | float | Years since token launch (as of April 2026) | Manual |
| log_revenue | float | log(revenue_annual_usd + 1) | Derived |
| log_fdv | float | log(fdv_usd) | Derived |
| log_treasury | float | log(treasury_usd + 1) | Derived |
| log_incentives | float | log(incentives_annual_usd + 1) | Derived |
| regression_ready | bool | True if all required covariates are non-null | Derived |
| subsidy_ratio_onchain | float | **AUTHORITATIVE.** emissions_onchain_usd / revenue_onchain_usd | Computed |
| revenue_onchain_usd | float | On-chain revenue (Dune / Token Terminal verified), annualized | Dune / TT |
| emissions_onchain_usd | float | On-chain token emissions (USD), annualized | Dune / TT |
| revenue_source_onchain | str | Source for onchain revenue (dune_onchain / token_terminal / etc.) | Derived |

> **IMPORTANT:** Use `subsidy_ratio_onchain` for all subsidy analyses. The legacy
> `subsidy_ratio` column uses a different denominator and was replaced after the
> April 2026 recomputation. See `paper/supplements/S6_revenue_standardization.md`.

---

## governance_concentration_april2026.csv
**Location:** `data/processed/governance_concentration_april2026.csv`
**Rows:** 40 (one per protocol)

Contains concentration metrics only (HHI, Gini, Top-N), without financial and
allocation covariates. Same columns as the concentration portion of
`regression_data_april2026.csv`: protocol, token, category, chain,
measurement_type, hhi, gini, top1_pct, top5_pct, top10_pct, n_holders,
total_balance_top1000, source, query_id, notes.

---

## exclusions_log.csv
**Location:** `data/processed/exclusions_log.csv`
**Rows:** 69 (one per excluded address)

| Column | Type | Description |
|--------|------|-------------|
| token | str | Token ticker |
| address | str | Excluded address (0x... for EVM; base58 for Solana) |
| identity | str | Identified entity (e.g., "Aave: Safety Module", "Binance Hot Wallet") |
| exclusion_reason | str | Category: treasury / staking_contract / cex / bridge / vesting_lock / team_multisig |
| chain | str | Blockchain |
| hhi_before | float | HHI before excluding this address (cumulative from top) |
| hhi_after | float | HHI after excluding this address |
| source | str | Evidence source: CONFIRMED_DOCS / CONFIRMED_PATTERN / HIGH_ALLOCATION_MATH / tier2_blockscout / tier1_eoa |

**Coverage:** 69 exclusions across 17 protocols. 65% cross-validated via Blockscout
and Nansen. See `data/processed/exclusion_crossvalidation.csv` for validation details.

---

## insider_classification.csv
**Location:** `data/processed/insider_classification.csv`
**Rows:** 390 (10 top-holders × 39 tokens; HONEY excluded from top-holder classification)

| Column | Type | Description |
|--------|------|-------------|
| token | str | Token ticker |
| chain | str | Blockchain |
| address | str | Holder address |
| balance | float | Token balance at April 2026 snapshot |
| share | float | Share of post-exclusion total supply (0–1) |
| post_exclusion_rank | int | Rank among non-excluded holders (1 = largest) |
| tier1_label | str | Label from Tier 1 (Blockscout tags / well-known labels) |
| tier2_label | str | Label from Tier 2 (secondary cross-reference) |
| tier3_label | str | Label from Tier 3 (manual EOA heuristics) |
| final_classification | str | insider / exchange / contract / dao_treasury / unknown |
| classification_source | str | tier1_blockscout / tier2_blockscout / tier1_eoa / manual |
| confidence | str | high / medium / low |
| vesting_status | str | locked / unlocked / unknown |
| notes | str | Free-text notes on classification rationale |

**Three-tier methodology:**
- Tier 1: Known smart contract addresses (staking pools, bridges, exchanges); labeled via Blockscout and Etherscan tags
- Tier 2: Cross-reference with Nansen whale labels and protocol GitHub documentation
- Tier 3: EOA heuristics — dormant addresses, round-number balances, allocation-math matching

---

## delegation_adjusted_hhi.csv
**Location:** `data/processed/delegation_adjusted_hhi.csv`
**Rows:** 8 protocols with both on-chain token HHI and voting power HHI

| Column | Type | Description |
|--------|------|-------------|
| protocol | str | Protocol name |
| symbol | str | Token ticker |
| raw_hhi | float | Token holding HHI (post-exclusion) |
| delegated_hhi | float | Voting power HHI (from Tally / Snapshot) |
| hhi_change_pct | float | (delegated_hhi − raw_hhi) / raw_hhi × 100 |
| raw_gini | float | Token holding Gini |
| delegated_gini | float | Voting power Gini |
| raw_nakamoto | int | Nakamoto coefficient (holding) |
| delegated_nakamoto | int | Nakamoto coefficient (voting power) |
| n_delegates | int | Number of active delegates |
| top1_delegate_share | float | Top-1 delegate share of total votes |
| source | str | tally_onchain / snapshot_offchain |

---

## holder_lists/
**Location:** `data/raw/holder_lists/`
**Naming convention:** `TOKEN_holders.csv` (processed exports) or `TOKEN_helius_raw.csv` (raw Helius API)

### TOKEN_holders.csv (standard format — Dune, Filfox, POKTscan exports)
| Column | Type | Description |
|--------|------|-------------|
| address | str | Holder address |
| balance | float | Token balance (raw token units, not USD) |
| rank | int | Rank by balance (1 = largest) |
| share | float | Share of total indexed supply (0–1) |
| token | str | Token ticker |

### TOKEN_helius_raw.csv (Helius DAS API format)
| Column | Type | Description |
|--------|------|-------------|
| owner | str | Solana wallet address |
| balance | float | Token balance (raw lamports — divide by 10^decimals) |

**Special files:**
- `HYPE_holders.csv` — sourced from Hypurrscan (Hyperliquid-native block explorer)
- `DRIFT_helius_raw.csv`, `GRASS_helius_raw.csv`, `META_helius_raw.csv`, `W_helius_raw.csv` — raw Helius DAS API responses
- `BAL_holders.csv` — raw BAL token (NOT veBAL). Paper notes veBAL caveat.
- `BAL_raw_holders.csv` — unfiltered Dune export before address deduplication
- `total_supply_corrections.json` — manual supply overrides where Dune's indexed supply deviates from on-chain circulating supply by >5%

**HONEY note:** No holder list file saved locally. HHI computed from Dune's
`solana_utils.latest_balances` top-100; result in `outputs/honey_requery_result.json`.

---

## outputs/regression_results.json
**Location:** `outputs/regression_results.json`

JSON object with all regression statistics cited in the paper. Key fields:

| Field | Value | Description |
|-------|-------|-------------|
| n_concentration | 40 | Total protocols in concentration universe |
| n_total | 40 | Total protocols |
| n_subsidy | ~20 | Protocols with onchain subsidy data |
| sector_mw_p | 0.031 | DePIN vs DeFi Mann-Whitney p-value |
| sector_cohens_d | 1.00 | DePIN vs DeFi effect size |
| insider_pearson_r | 0.19 | Allocation vs HHI Pearson r |
| insider_pearson_p | 0.25 | Allocation vs HHI p-value |
| insider_n | 37 | N for allocation regression |
| cross_pearson_r | 0.58 | Subsidy vs HHI cross-sector Pearson r |
| cross_pearson_p | 0.007 | Subsidy vs HHI p-value |
| hhi_gini_r | 0.54 | HHI-Gini robustness correlation |
| _timestamp | "2026-04-01" | Computation date |

Produced by `analysis/05_09_regressions.py`.

---

## scoring_sheet.csv
**Location:** `data/processed/scoring_sheet.csv`
**Rows:** 112 (14 protocols × 8 normative lenses)
**Unit of observation:** Protocol × lens

Primary research data. Contains the scored normative judgments used in the paper's
institutional design framework (Part I). **Not derivable from any other file.**

| Column | Type | Description |
|--------|------|-------------|
| protocol_id | str | Protocol identifier (snake_case, matches protocol_codebook.csv) |
| lens_id | str | Normative lens identifier (see scoring_rubric.csv for definitions) |
| score | int | Score 0–3 (0=absent, 1=minimal, 2=partial, 3=exemplary) |
| evidence_link | str | URL to primary evidence used for scoring |
| scorer_initials | str | Scorer identifier (ZZ = Zach Zukowski) |
| date | date | Date of scoring (YYYY-MM-DD) |
| notes | str | Rationale and evidence summary |

**Protocols scored (14 DePIN protocols):** anyone, cudis, dimo, filecoin, geodnet,
grass, helium, hivemapper, iotex, livepeer, render, uprock, wayru, weatherxm

**Lenses (8):**
| lens_id | Tradition | What it measures |
|---------|-----------|-----------------|
| kantian_publicity | Kant | Transparency and public justification of governance rules |
| rawlsian_fairness | Rawls | Floor-raising mechanisms for disadvantaged participants |
| pettit_contestation | Pettit | Formal mechanisms to challenge and appeal decisions |
| ostrom_polycentricity | Ostrom | Nested, polycentric governance structure |
| hayek_knowledge | Hayek | Price signals and distributed knowledge mechanisms |
| nussbaum_capability | Nussbaum | Participant capability development and support |
| floridi_integrity | Floridi | Information-flow governance and data integrity |
| appiah_cosmopolitan | Appiah | Cross-cultural accessibility and participation |

See `paper/supplements/scoring_rubric.csv` for full 0–3 anchors per lens.

---

## protocol_codebook.csv
**Location:** `data/processed/protocol_codebook.csv`
**Rows:** 14 (DePIN protocols only)

Comprehensive protocol metadata with 50+ columns covering emission mechanics,
governance structure, DePIN-specific hardware/verification parameters, and
S2R data sources. Superset of `regression_data_april2026.csv` for DePIN protocols —
includes fields not in the regression dataset (hardware_cost_usd, coverage_verification_method,
s2r_period, operator_type, etc.).

Key column groups:
- **Identity:** protocol_id, name, chain, category, subcategory, launch_date, token_ticker
- **Emission design:** emission_model, max_supply, inflation_rate_annual_pct, decay_rule, halving_schedule
- **Token allocation:** team_allocation_pct, investor_allocation_pct, community_allocation_pct, treasury_allocation_pct
- **Governance structure:** governance_type, on_chain_voting, delegation_enabled, proposal_threshold, quorum_pct, timelock_hours
- **Concentration metrics:** holding_hhi, holding_gini, top_1_share, top_5_share, top_10_share
- **DePIN-specific:** operator_type, deployment_unit, hardware_cost_usd, coverage_verification_method, reward_basis, geodata_required, location_verification_method
- **S2R fields:** s2r_burns_only, s2r_burns_plus_locks, s2r_period, s2r_data_source

---

## helium_s2r_cleaned.csv / geodnet_monthly_burns.csv / geodnet_monthly_emissions.csv
**Location:** `data/raw/`

Time series data for DePIN protocol economic analyses.

### helium_s2r_cleaned.csv (34 rows, monthly, May 2023–Feb 2026)
| Column | Description |
|--------|-------------|
| period | Month end date (UTC) |
| hnt_burned | HNT burned as Data Credits that month |
| hnt_issued | HNT issued (staking rewards) that month |
| s2r_burns_only | Simple S2R = hnt_burned / hnt_issued |
| migration_excluded | True if Solana migration artifacts excluded |
| s2r_clean | Cleaned S2R (migration artifacts removed) |
| s2r_3m_rolling | 3-month rolling median of s2r_clean |
| spike_flag | True if > 2× trailing median (spike detection) |
| s2r_median_5m | 5-month rolling median |

### geodnet_monthly_burns.csv (19 rows, monthly, Sep 2024–present)
| Column | Description |
|--------|-------------|
| month | Month start date |
| burn_tx_count | Number of burn transactions |
| geod_burned | GEOD tokens burned |
| unique_signers | Unique addresses initiating burns |

### geodnet_monthly_emissions.csv (19 rows, monthly, Sep 2024–present)
| Column | Description |
|--------|-------------|
| month | Month start date (YYYY-MM format) |
| mint_tx_count | Number of mint transactions |
| geod_emitted | GEOD tokens emitted |

---

## Gini Correction Note

The Dune ERC-20 concentration query ranks holders from largest to smallest
(rank = 1 for the largest holder). Standard Gini requires ascending order
(poorest first). The sign is therefore reversed, requiring an end-correction:

```
corrected_gini = -raw_gini - (1 / n_holders)
```

This correction is applied in `analysis/01_compute_hhi.py`. HHI values are
order-invariant and unaffected.
