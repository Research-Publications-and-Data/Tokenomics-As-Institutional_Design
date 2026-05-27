# Supplementary File S16: Phase 4 Mini-Batch Sample Expansion (B2 R3 omnibus)

**Companion to:** B2 paper *Tokenomics as Applied Political Philosophy: Governance Concentration Beyond Token Allocation* (§3.2 holding-HHI cross-section; §3.8 PCA typology; §5.7 #2 + §5.8 #2 sample-expansion limitation + future-research).

**Closes:** §5.7 limitation #2 (small N for regression) + §5.8 future research #2 (sample expansion) PARTIAL via 4-protocol mini-batch extending N=40 to **N=44**.

**Generated:** 2026-05-27 (PID 4300; B2 R3 omnibus Phase 4 mini-batch execution).

**Data sources:**
- Sim API EVM token-holders (Frax FXS, Synthetix SNX, Gnosis GNO; top-500 by balance)
- TAOSTATS API account/latest/v1 (Bittensor TAO; top-1000 by balance_total via 5-page paginated pull at 200/page)

**Output artifacts:**
- `phase4_minibatch_2026-05-27.csv` (per-protocol pre-exclusion metrics)
- `data/raw/holder_lists/FXS_holders.csv` + `SNX_holders.csv` + `GNO_holders.csv` + `TAO_holders.csv` (top-500/1000 holder lists)

---

## Executive summary

Phase 4 of B2 R3 omnibus mini-batch executed: 4 protocols added to N=40 cross-section (3 mature DeFi blue-chips via Sim EVM token-holders + 1 Substrate-native DePIN via TAOSTATS). 5th protocol (Polkadot DOT) deferred to continuation cycle (non-EVM-non-SVM Substrate; requires Subscan API auth).

**N=40 → N=44** (1 protocol from N=45 mini-batch target; 6 from N=50 full Phase 4 target per parent dispatch).

| Protocol | Sector | Chain | N (top) | top-1% | top-10% | HHI (pre-exclusion) | Status |
|---|---|---|---:|---:|---:|---:|---|
| FXS (Frax Share) | DeFi | Ethereum | 500 | 48.86% | 79.97% | 0.268 | PCA-classification pending |
| SNX (Synthetix) | DeFi | Ethereum | 500 | 38.74% | 69.59% | 0.170 | PCA-classification pending |
| GNO (Gnosis) | DeFi | Ethereum | 500 | 38.73% | 95.89% | 0.273 | PCA-classification pending |
| TAO (Bittensor) | DePIN | Bittensor (Substrate) | 1000 | 8.86% | 25.86% | **0.014** | PCA-classification pending; LOWEST PRE-EXCLUSION HHI in 4-protocol batch |
| DOT (Polkadot) | L1 | Polkadot (Substrate) | -- | -- | -- | -- | GAP (Subscan API or substrate node query required) |

**Finding O (TAO low pre-exclusion concentration; NEW).** Bittensor (TAO) exhibits the lowest pre-exclusion HHI in the Phase 4 mini-batch at 0.014; top-1 holder at 8.86% share is comparable to ARB/COMP top-1 share (~10% range) but with shallower tail concentration. The 25.86% top-10 share is also broadly dispersed. This is consistent with Bittensor's validator-subnet architecture where many independent validators stake TAO; no single Foundation/treasury dominates. PCA classification refinement (Foundation; subnet-validator multi-sigs; bridge custody on Bittensor EVM bridge) needed before integration to canonical regression.

**Finding P (EVM DeFi blue-chip high pre-exclusion HHI; expected pattern).** FXS + SNX + GNO show high pre-exclusion HHI (0.17 to 0.27) with top-1 shares 38-49%. This is the characteristic un-cleaned holder pattern for mature DeFi protocols where Foundation/treasury/staking-aggregation dominates raw top-500 (Frax Foundation; SNX staking contracts; Gnosis Foundation). PCA classification needed before HHI canonical-state integration; expected post-exclusion HHI substantially lower (closer to 0.03-0.05 range like AAVE/COMP/UNI cluster).

---

## Per-protocol PCA classification candidates (top holders for next-cycle audit)

### FXS (Frax Share)

Top-1 holder `0x36cb65c1...` at 48.86% share (52.3M FXS; first_acquired 2025-04-29; has_initiated_transfer=false). Behavioral signature consistent with Foundation/treasury OR strategic-investor address. PCA candidate: Class 2 (foundation/treasury custody) — verify via Frax Foundation documentation OR Etherscan label.

Top-2 `0xc8418af6...` at 17.06M FXS (first_acquired 2021-05-06; has_initiated_transfer=false): consistent with early-investor lockup OR vesting contract; PCA candidate Class 2 or Class 3.

### SNX (Synthetix Network Token)

Top-1 at 38.74% share. SNX governance involves SNX staking with multi-signature treasury management; top holder likely Synthetix Foundation OR SNX staking contract. PCA candidate Class 2 or Class 3.

### GNO (Gnosis)

Top-1 at 38.73% share + top-10 at 95.89% (extreme concentration). Gnosis Foundation historically holds substantial GNO treasury; top-1 likely Foundation custody. PCA candidate Class 2.

### TAO (Bittensor)

Top-1 `5Hd2ze5ug8n1bo3UCAcQsf66VNjKqGos8u6apNfzcU86pg4N` at 8.86% share (797,821.79 TAO; rank 1). balance_total includes both balance_free + balance_staked + balance_staked_alpha_as_tao + balance_staked_root; majority of top-holder positions are staked (validator + subnet stakers). PCA candidate Class 3 (staking-aggregation) for accounts where balance_staked >> balance_free (per per-account inspection); Class 2 (Bittensor Foundation) for any identifiable Foundation address.

Top-7 `5FEA1FfUPwT3K4zTsYbQx5X1G9R2ZjYLyFv12xBQxW9QgoCL` shows balance_free=141K + balance_staked=0; unstaked liquid position; likely exchange custody OR liquid-TAO holder.

---

## §3.8 PCA typology extension recommendations (Phase 4 mini-batch insights)

Per §3.8 five-class PCA typology, Phase 4 mini-batch adds candidates for each class:

| Class | Phase 4 candidates |
|---|---|
| Class 1 (burn destinations) | TAO null/burn addresses on Bittensor EVM bridge (if any); Substrate burn addresses |
| Class 2 (Foundation/treasury) | FXS Frax Foundation; SNX Synthetix Foundation; GNO Gnosis Foundation; TAO Bittensor Foundation |
| Class 3 (staking-aggregation) | SNX SNX staking pools; TAO subnet-validator stake-aggregation (extends Class 3 to Substrate-native staking) |
| Class 4 (bridge custody) | FXS/SNX/GNO bridge custody on L2s (Optimism/Arbitrum/Base); TAO bridge custody on Bittensor EVM bridge |
| Class 5 (CEX custody) | All 4 protocols' top-100 holders likely include Binance/Coinbase/Kraken hot wallets |

**Substrate-native staking extension to Class 3 (NEW per TAO addition).** Bittensor's subnet-validator staking architecture extends Class 3 (currently EVM-anchored at SPL stake-pool accounts; Lido stETH staking; Rocket Pool RPL minipools) to Substrate-native validator-stake accounts. Methodology generalizes: any protocol-controlled staking-aggregation account where TAO/ETH/other base tokens are pooled for validator-class governance participation qualifies as Class 3 PCA. TAO is the first Substrate-native PCA candidate in the cross-section; extends the typology empirically.

---

## §4.3 sector-contrast pre-vs-post-extension analysis (PENDING)

Per parent dispatch HALT-4.2: "If expanded sample produces direction-of-effect reversal on any of the headline findings (allocation null, DePIN-DeFi contrast, insider-count significance, subsidy fragility), halt and surface."

Phase 4 mini-batch additions:
- 3 DeFi blue-chips (FXS + SNX + GNO; pre-exclusion HHI 0.17-0.27; expected post-exclusion ~0.03-0.05)
- 1 DePIN (TAO; pre-exclusion 0.014; expected post-exclusion similar magnitude given low pre-exclusion)

After PCA classification + post-exclusion HHI recompute:
- DeFi mean shifts within current range (no direction-of-effect change expected)
- DePIN mean addition (TAO 0.014 post-exclusion) sits in lower-DePIN cluster (sister to W 0.011); does not flip DePIN-vs-DeFi sector contrast

**No HALT-4.2 trigger expected after PCA-cleaned HHI computation.** Continuation cycle should run PCA classification + recompute + multivariate Model 3 with N=44 to confirm.

---

## Continuation work (deferred to next cycle)

1. **PCA classification per protocol** (FXS + SNX + GNO + TAO top-20 holder audit; identify Foundation/treasury/staking-aggregation/CEX custody addresses)
2. **Post-exclusion HHI computation** per protocol (apply identified PCAs to top-N holder list; recompute HHI on remaining non-PCA holders per §3.8 methodology)
3. **Add rows to canonical `regression_data_april2026.csv`** with post-exclusion HHI + covariate values (sector + insider_pct + revenue + subsidy + protocol_maturity_years; per existing N=40 cross-section schema)
4. **Re-run multivariate Model 3** with N=44; verify HALT-4.2 not triggered; document any direction-of-effect shifts
5. **DOT addition** (5th mini-batch protocol): Subscan API key acquisition + top-1000 holder pull + PCA classification; brings to N=45 mini-batch target
6. **Full Phase 4 expansion** to N=50-60 per parent dispatch (LayerZero ZRO; EigenLayer EIGEN; Ondo ONDO; Pendle; Aragon ANT; Snapshot Labs; Tally/Boardroom; Akash; Nosana; Aleo; Avalanche; Aptos; Sui; ICP)

---

## Cross-references

- **B2 PAPER.md §3.2** (Table 3 holding-HHI cross-section; Phase 4 candidate row additions FXS+SNX+GNO+TAO post-PCA-exclusion)
- **B2 PAPER.md §3.8** (Five-class PCA typology; Substrate-native extension Class 3 candidate)
- **B2 PAPER.md §4.3** (DePIN-vs-DeFi sector contrast; HALT-4.2 pending PCA-cleaned recompute)
- **B2 PAPER.md §5.7 #2 + §5.8 #2** (Sample-expansion limitation + future-research; PARTIAL closure this Phase 4 mini-batch)
- **S13 + S13 addendum** (Solana PCA audit + verification; PCA classification methodology reference)
- **S14 + addenda** (Phase 1 power-indices closure N=16)
- **S15 + addenda** (Phase 2 voting-HHI expansion + gap inventory)
- B2 R3 omnibus continuation dispatch (Phase 4 spec for full expansion)
- **NEW memory note candidate**: TAOSTATS API for Substrate-native holder distribution (sister to Sim API reference memory note)

---

## Author note

Phase 4 mini-batch ships 4 of 5 target protocols. Pre-exclusion HHI values are deliberately not integrated into canonical regression_data_april2026.csv this cycle: PCA classification requires per-protocol top-holder audit (Foundation/treasury identification; staking-aggregation contract detection; CEX hot wallet flagging) which is dedicated next-cycle work. Holder lists shipped at `data/raw/holder_lists/` for next-cycle PCA cleanup.

TAOSTATS API + Sim API access enabled this mini-batch. Both APIs treated as ephemeral session secrets per CLAUDE.md security discipline; never committed to git; never logged to repo; used only via inline environment variable / process-args during runtime queries.

Author: Claude Code session 2026-05-27 (PID 4300); workflow clone `/Users/zach/Tokenization_Systems_Website`; sibling clone `/Users/zach/Tokenomics-As-Institutional_Design`.
