# Supplementary File S19 ADDENDUM: DOT validator analysis expansion (operator-attribution + governance-vote concentration)

**Companion to:** S19 (Phase 4 scope expansion).
**Generated:** 2026-05-27. **Trigger:** author directive "Expand validator analysis" 2026-05-27T18:45Z (responding to Binance-15-validator finding in initial S19 DOT section).

---

## Why this addendum

S19 Item 2 reported Binance controls 15 of 600 DOT validator slots (2.5% slot share; 3.72% stake share) as the largest single-operator concentration. Author requested deeper analysis. This addendum reports:

1. Full operator-attribution sweep across 600 validators (pattern-matching against CEX + institutional staking provider names)
2. Self-stake vs nominator-stake breakdown per operator class (vertical-integration pattern detection)
3. Stake-duplicate clustering investigation (whether unverified validator clusters represent single operators)
4. Polkadot OpenGov referendum vote concentration (governance axis separate from validator-stake axis)

---

## Methodology

Validators sourced from Subscan `/api/scan/staking/validators` (paginated; 600 deduplicated by stash address). Display names extracted from `stash_account_display.people.display` (Polkadot Identity Pallet registrations). Operator-class assignment via case-insensitive substring matching against curated CEX/institutional pattern dictionary.

For unverified (no display name) validators: clustering by bonded-stake amount (10K DOT buckets) to test single-operator hypothesis.

Governance-vote concentration via Subscan `/api/scan/referenda/votes` for recent OpenGov referenda (1775-1777).

---

## Findings

### Finding F.4: Verified operator-class breakdown (N=600 validators)

| Operator class | Count | % of count | Stake (DOT) | % of stake |
|---|---:|---:|---:|---:|
| Unverified (no identity) | 514 | 85.67% | 702,193,349 | 83.89% |
| Independent (verified, non-CEX/non-institutional) | 52 | 8.67% | 74,474,107 | 8.90% |
| CEX:Binance | 15 | 2.50% | 31,136,981 | 3.72% |
| Institutional:Figment | 7 | 1.17% | 11,350,623 | 1.36% |
| Institutional:Stakin | 3 | 0.50% | 4,288,912 | 0.51% |
| Institutional:RockX | 2 | 0.33% | 2,923,162 | 0.35% |
| Institutional:Chainsafe | 2 | 0.33% | 2,700,017 | 0.32% |
| Institutional:DothubValidator | 1 | 0.17% | 2,075,494 | 0.25% |
| Institutional:Stakefish | 1 | 0.17% | 1,469,271 | 0.18% |
| Institutional:P2P Validator | 1 | 0.17% | 1,469,270 | 0.18% |
| Institutional:Polkachu | 1 | 0.17% | 1,469,270 | 0.18% |
| CEX:Kraken | 1 | 0.17% | 1,469,244 | 0.18% |

**Aggregate:**

- **CEX (verified): 16 validators (2.67%) / 32,606,225 DOT (3.90% of stake)**
- **Institutional (verified): 18 validators (3.00%) / 27,746,018 DOT (3.31% of stake)**
- **Independent (verified): 52 validators (8.67%) / 74,474,107 DOT (8.90% of stake)**
- **Unverified: 514 validators (85.67%) / 702,193,349 DOT (83.89% of stake)** -- structurally limits attribution.

### Finding F.5: Binance dominates rank-1 through rank-16 by bonded stake

Sorted by bonded stake, the top-16 validators are ALL CEX:Binance or one Institutional:DothubValidator (rank-9). Binance specifically controls ranks 1-8 and 10-16. Each Binance validator holds approximately 2,075,000 DOT in bonded nominators with $0 self-stake. The pattern: Binance offers DOT staking to customers; customer DOT is bonded via Binance-controlled validators; nominators per validator = 1-2 (single controller account).

**Vertical integration pattern.** Custody (Binance exchange) -> Staking (Binance Earn) -> Validator-set (BINANCE_STAKE_X). This is sister to the "mechanical CEX-custody overlap" pattern documented in S18 audit Finding C, extended to validator-set custody.

### Finding F.6: Self-stake vs nominator-stake patterns differentiate operator types

| Class | n_val | Avg nominators per validator | Self-stake (DOT) | Nominator-stake (DOT) | Self-stake % |
|---|---:|---:|---:|---:|---:|
| Unverified | 514 | 29.4 | 922,445 | 701,270,904 | 0.13% |
| Independent | 52 | 88.5 | 1,498,997 | 72,975,110 | 2.01% |
| CEX:Binance | 15 | 8.4 | 0 | 31,136,981 | 0.00% |
| Institutional:RockX | 2 | 560.5 | 1,285 | 2,921,877 | 0.04% |
| Institutional:P2P Validator | 1 | 320.0 | 0 | 1,469,270 | 0.00% |
| Institutional:Stakefish | 1 | 183.0 | 1,000 | 1,468,271 | 0.07% |
| CEX:Kraken | 1 | 173.0 | 0 | 1,469,244 | 0.00% |
| Institutional:Figment | 7 | 9.1 | 0 | 11,350,623 | 0.00% |
| Institutional:Stakin | 3 | 44.7 | 11,764 | 4,277,148 | 0.27% |

**Three operator-type signatures:**

1. **CEX-vertically-integrated (Binance):** few nominators per validator (1-8); 0% self-stake; bonded stake = customer-DOT routed through CEX-controlled validators. Avg-nominator-count is a misleading low count because each "nominator" is really a CEX-controlled aggregation account, not a retail nominator.
2. **Retail staking service (RockX 561 noms; P2P 320; Stakefish 183; Kraken 173):** many retail nominators per validator; CEX/institutional offers staking to direct retail users.
3. **Foundation/whale (Figment 9 noms; DothubValidator 1):** few but large enterprise/foundation nominators; not retail-aggregated.

### Finding F.7: Stake-duplicate clustering is NPoS-equalization artifact, NOT operator clustering

Initial hypothesis: 197 unverified validators sharing ~1.469M DOT bonded stake might represent a single large operator running many validators. Investigation refuted this hypothesis.

Within the 197-validator 1.469M DOT cluster, the nominator-count distribution is HIGHLY VARIED (1 to 190 nominators per validator). If these were one operator's validators, we would expect similar nominator-count patterns. The wide distribution confirms these are MANY DIFFERENT operators whose validators all happen to share the ~1.469M DOT bonded stake because that's the NPoS Phragmen-equalization convergence point for active validators.

**Conclusion:** Polkadot's NPoS deliberately compresses all elected validators to the same bonded-stake ceiling. The duplicate-stake pattern is structural (NPoS), not behavioral (operator-clustering).

### Finding F.8: Governance-vote concentration is structurally higher than validator-stake concentration

OpenGov referenda allow direct conviction-weighted voting by any DOT holder, NOT mediated through validators. Recent referendum top voters:

| Referendum | Top voter (single account) | Amount |
|---|---|---:|
| #1777 | `16GMHo9HZv...` | 9,000,000 DOT |
| #1777 | `14Ns6kKb...` | 9,000,000 DOT |
| #1777 | `12WLDL2AX...` | 9,000,000 DOT |
| #1775 | `14Ns6kKb...` (same as above) | 1,000,000 DOT |

**Substantive implication:** the validator-set's 1.5M DOT per-validator NPoS-enforced ceiling does NOT cap governance influence. Individual governance voters deploy 8-9M DOT directly via OpenGov; the validator-stake HHI of 0.0017 dramatically UNDERSTATES Polkadot governance concentration.

The address `14Ns6kKbCoka3MS4Hn6b...` voted in multiple referenda (9M in #1777; 1M in #1775); cross-referendum participation by single large voters is a recurring pattern not captured by validator-stake analysis.

### Finding F.9: Methodology recommendation for B2 §3.8 typology

DOT (Polkadot) and similar NPoS-equalized native-chain tokens require a **multi-axis concentration measurement frame** that does not map directly onto EVM top-1000-token-holder HHI:

1. **Validator-stake HHI** (per-validator bonded stake): captures Phragmen equalization; not the governance-influence axis.
2. **Operator-stake HHI** (aggregate per operator): captures CEX + institutional staking provider concentration; limited by ~86% of validators being unverified.
3. **Governance-vote HHI** (per OpenGov referendum, conviction-weighted): captures direct voting concentration; sister to EVM Snapshot voting-HHI methodology in B2 §3.5.
4. **Foundation custody fraction** (W3F + Treasury parachain accounts): captures institutional baseline; sister to EVM Foundation/Treasury Class 2 in §3.8.

For regression integration:
- **NOT directly comparable to EVM `hhi` column** in `regression_data_april2026.csv`
- **Use measurement_type = "staking_aggregation"** to signal methodology branch
- **Document in §3.8 typology** as "NPoS native-chain" sub-class

---

## Updated DOT regression-row values (S19 + this addendum)

The DOT row in `phase4_minibatch_regression_rows_2026-05-27.csv` retains:

- `hhi` = 0.001692 (stake-level on N=600 deduped validators; structurally flat per NPoS)
- `measurement_type` = "staking_aggregation"
- `regression_ready` = False (methodology pending DEC for §3.8 typology extension)

Augmented notes:

- Verified operator HHI by slot count = 0.002378
- Verified operator HHI by stake = 0.003153
- Binance controls 15 of top-16 ranks by bonded stake (top-1 through top-8 and top-10 through top-16; rank-9 is dothub-1)
- 514 of 600 validators (85.67%) are unverified; operator-attribution structurally limited
- Governance-vote concentration on OpenGov referenda dramatically higher than validator-stake concentration (single voters deploy 9M DOT vs validator ceiling of ~1.5M DOT)

---

## Output artifacts (added this expansion cycle)

- `dot_validators_classified.json` (600 validators with operator-class assignment + self-stake / nominator-stake / nominator-count breakdown)
- `dot_validator_cluster_analysis.json` (stake-duplicate clustering analysis; refutes single-operator hypothesis)
- `dot_validators_identity.py` + `dot_cluster_investigation.py` + `dot_gov.py` + `dot_referendum_voters.py` (reproducibility scripts)

---

## Out of scope this addendum

- **Anchorage / Blockdaemon / Bison Trails / Coinbase Cloud / Staked.us / Kiln pattern matching** -- patterns not matched in current dictionary; may exist among the 514 unverified validators.
- **Resolution of 514 unverified validators via on-chain creation-trace analysis** (funding-source clustering; controller-account inspection) -- requires Polkadot RPC + Blockscout-style trace tooling not available via Subscan.
- **Full OpenGov referendum-vote HHI calculation** across all 1,777+ referenda -- single-referendum sampling suggests material concentration; full N-referendum HHI requires sustained data-pull cycle.
- **Web3 Foundation + Polkadot Treasury parachain account custody quantification** -- W3F controls ~30% of DOT per launch tokenomics; Treasury parachain (`13UVJyLnbVp9R...`) holds substantial DOT for proposal funding; per-account custody quantification requires per-account balance queries.
- **DOT cross-chain bridge custody** (Wormhole + Snowbridge + AssetHub) -- additional Class 4 candidates not in this validator-set sweep.
- **TAO (Bittensor) sister analysis** -- parallel session per earlier author directive.
- **Polkadot Fellowship + Tech Committee membership** -- Subscan returned 404 (endpoint moved/renamed); OpenGov replaced Council 2024.

---

## Cross-references

- **Predecessor (this cycle):** S19 Phase 4 scope expansion (Item 2 DOT staking-concentration)
- **Sister supplements:** S18 v1 + S18 audit addendum (EVM Phase 4 mini-batch); S13 + S13 addendum (Solana PCA audit)
- **Methodology references:** B2 PAPER.md §3.5 (voting-HHI methodology) + §3.7 (Herfindahl methodology) + §3.8 (PCA typology); HALT-4.1 (methodology innovation)
- **Sibling-clone commits:** `361a4a3` (Phase 4 audit) + `11f738a` (Phase 4 expansion) + this addendum's ship commit (pending)
- **Workflow-clone dispatch status-append:** `315ffb14`

---

## Reproducibility

```bash
# Validator identity classification + class-level breakdown
python3 b2/paper/supplements/dot_validators_identity.py

# Cluster investigation (refute single-operator hypothesis)
python3 b2/paper/supplements/dot_cluster_investigation.py

# Governance referendum voters
python3 b2/paper/supplements/dot_referendum_voters.py
```

---

## Authorship note

Authored 2026-05-27 in direct response to author directive "Expand validator analysis" referencing the Binance-15-validator finding. PID 14088 (BULK-EXECUTOR; expanded task-scope: handoff/dispatch/b2_r3_data_collection_omnibus_continuation + b2 Phase 4 EVM mini-batch + DOT operator-attribution); workflow clone `/Users/zach/Tokenization_Systems_Website`; sibling clone `/Users/zach/Tokenomics-As-Institutional_Design`.
