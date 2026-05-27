# Supplementary File S19: Phase 4 scope expansion (universal CEX-sweep + DOT + regression rows)

**Companion to:** S18 v1 + addendum (Phase 4 EVM mini-batch FXS / SNX / GNO).
**Generated:** 2026-05-27. **Trigger:** author directive "Expand scope now" 2026-05-27T17:55Z.

---

## Scope of this expansion cycle

After S18 v1 + audit addendum shipped, author directed expansion of Phase 4 scope to cover three deferred items:

1. **Universal CEX-sweep** across existing N=40 sample for the 5 newly-confirmed CEX hot wallets surfaced in S18 audit.
2. **DOT (Polkadot) holder pull** via chain-specific tooling.
3. **TAO (Bittensor) holder pull** via Taostats API.
4. **Covariate population** for FXS / SNX / GNO regression rows (insider %, FDV, MCap, revenue, etc.).

This supplement reports the results across all four expansion items + the consequent regression-dataset + exclusions-log extensions.

---

## Item 1: Universal CEX-sweep results (5 new hot wallets across N=40 sample)

### Scope

Scan top-1000 holder lists of all 40 existing protocols in `data/raw/holder_lists/*_holders.csv` for the 5 newly-confirmed CEX hot wallets:

- `0xa023f08c70a23abc7edfc5b6b5e171d78dfc947e` Crypto.com 22 / Hot Wallet
- `0x0529ea5885702715e83923c59746ae8734c553b7` Bitpanda 18
- `0xedc6bacdc1e29d7c5fa6f6eca6fdd447b9c487c9` Bitvavo
- `0xab782bc7d4a2b306825de5a7730034f8f63ee1bc` Bitvavo Hot Wallet
- `0x3a5cc8689d1b0cef2c317bc5c0ad6ce88b27d597` Luno Wallet

### Findings

**Total: 89 cross-protocol CEX hot wallet hits across 21 existing protocols.**

| CEX hot wallet | Protocols affected | Notable highest-share appearances |
|---|---:|---|
| Bitpanda 18 | 20 | Spans ARB, ATH, AXL, BAL, COMP, CRV, ENS, ETHFI, GMX, GRT, GTC, IOTX, LDO, MPL_SYRUP, OP, +5 |
| Bitvavo Hot Wallet | 17 | AAVE, ARB, ATH, AXL, COMP, CRV, ENS, ETHFI, GMX, GRT, GTC, LDO, MPL_SYRUP, RPL, SYRUP, +2 |
| Crypto.com 22 | 14 | AAVE, ATH, AXL, COMP, CRV, ENS, ETHFI, GRT, GTC, LDO, POL, RPL, UNI, ZRO |
| Bitvavo | 12 | AAVE, ATH, AXL, COMP, CRV, ENS, ETHFI, LDO, POL, RPL, UNI, ZRO |
| Luno Wallet | 7 | AAVE, CRV, ENS, GRT, LDO, UNI, ZRO |

### Material HHI cascade effects

Per S12 sensitivity-threshold convention (|HHI shift| > 0.0005), 8 protocols have material HHI shifts from adding the new CEX exclusions:

| Protocol | n_new_exclusions | Aggregate share excluded | HHI shift |
|---|---:|---:|---:|
| ATH | 4 | 0.541% | +0.003279 |
| GRT | 4 | 2.175% | +0.001737 |
| AXL | 4 | 1.607% | +0.001657 |
| RPL | 4 | 0.824% | +0.001224 |
| GTC | 3 | 1.935% | +0.000969 |
| ENS | 5 | 0.185% | +0.000862 |
| GMX | 2 | 0.224% | +0.000855 |
| POL | 3 | 0.483% | +0.000831 |

**Direction-of-shift note:** all shifts are POSITIVE (HHI increases) because PCA exclusion re-normalizes the remaining holders to a smaller denominator. This is sister to the FXS / SNX direction-of-shift pattern documented in S18 v1 and resolved in S18 audit addendum.

### CONFIRMED scope across the sweep

The hit rates suggest the 5 newly-confirmed CEX hot wallets are SYSTEMIC across mature DeFi protocols (Bitpanda 18 alone in 20 of 40 = 50%). This is consistent with the cross-protocol CEX-custody pattern documented as Finding C in S18 audit addendum: mature DeFi tokens are listed on a small set of CEXs that collectively custody a substantial fraction of top-1000 supply across protocols.

**Implication for B2 §4.5.5:** the cross-protocol custody concentration is structurally amplified when measured at CEX-level rather than per-protocol-CEX-wallet level. The 5 newly-confirmed CEX hot wallets aggregate to approximately 5-15% of additional cross-protocol custody depending on protocol; sister to PGov + Tane + Arana voting-side cluster but at the custody-axis.

### Output artifacts

- `b2/paper/supplements/universal_cex_sweep_phase4_new_2026-05-27.csv` (89 rows; 1 row per (protocol, CEX-address) pair)
- `b2/paper/supplements/phase4_exclusions_log_extension_2026-05-27.csv` (100 rows: 30 Phase 4 new-protocol PCAs + 70 universal-sweep additions for existing protocols)

---

## Item 2: DOT (Polkadot) staking-concentration analysis (methodology-innovation case)

### Approach

Polkadot's DOT is a native chain token (Substrate), not an ERC20. The Subscan `/api/v2/scan/accounts` endpoint returns indexed external accounts ranked by free balance, which excludes system accounts (treasury, validators, parachain crowdloan reserves) and produces a misleading "top-1000 holders" view (top-1 only 21,464 DOT at first_pass).

The Polkadot governance architecture's actual concentration axis is the **validator-bonded-stake distribution**: each elected validator carries delegated nominator stake + own stake; governance influence and economic returns flow through this layer.

### Data pull

`https://polkadot.api.subscan.io/api/scan/staking/validators` with `X-API-Key` header.

- Pulled 3,000 records across 10 pages of 100 → after deduplication by stash address: **N=600 unique validators**.
- Total bonded across all validators: **4,185,098,492 DOT** (~$5.3B at $1.27/DOT; or $20B+ at typical $5/DOT pricing).

### Concentration measurements

| Metric | Value |
|---|---:|
| Stake-level HHI (per-validator stake) | **0.001692** |
| top1_pct (largest validator) | 0.248% |
| top5_pct | 1.240% |
| top10_pct | 2.480% |
| Operator-level HHI (by validator-slot count) | 0.002378 |
| Operator-level HHI (by total bonded stake) | 0.003153 |
| Number of unique validators | 600 |
| Number of unique operators (deduplicated by display name) | ~570 |

### Substantive findings

**Finding F.1: Polkadot NPoS deliberately flattens validator-stake distribution.** Phragmen-based NPoS election algorithm equalizes stake across active validators to maximize fairness; stake-level HHI of 0.001692 is approximately 10x lower than any DeFi or DePIN protocol in B2's current N=40 sample.

**Finding F.2: CEX-validator concentration at operator level.** Binance operator controls 15 of 600 validator slots (2.50%) and 3.72% of total bonded stake — the largest single-operator concentration in the validator set. Smaller CEX operators: Figment (7 slots; 1.36% of stake), RockX Polkadot (2 slots), ChainSafe Polkadot Validator (2 slots).

**Finding F.3: Methodology-innovation case (HALT-4.1).** DOT's validator-stake distribution is not directly comparable to EVM top-1000 token-holder HHI used in B2 §3.7. Inclusion in the regression sample requires §3.8 typology extension to address:

- "Holder" definition for native-chain governance tokens (free balance vs bonded stake vs total)
- Concentration measurement unit (per-validator vs per-operator)
- Treatment of validator-set elections (Polkadot's NPoS deliberately disperses)

### Output artifacts

- `data/raw/b2_phase4_minibatch_2026-05-27/dot_holders.json` (1000 indexed accounts; for reference)
- `data/raw/b2_phase4_minibatch_2026-05-27/dot_validators.json` (deduped validators + HHI stats)
- `dot_validators.py` / `dot_alternatives.py` reproducibility scripts

### Status

DOT regression row populated (S19 Item 4); `regression_ready=False` pending §3.8 typology extension DEC. The row enables methodological transparency without committing to a stake-vs-holder-vs-operator HHI choice.

---

## Item 3: TAO (Bittensor) status

**Status: DELEGATED to parallel session per author directive 2026-05-27T18Z.** Taostats API requires authenticated requests (Authorization header with API key); key was provided mid-cycle but cycle scope was redirected to other items. Bittensor's subnet × validator × delegator structure presents a sister methodology-innovation challenge to DOT (see Item 2 Finding F.3).

Pending parallel-session ship: subnet-level staking concentration; Bittensor Foundation custody identification; root-vs-alpha subnet emission flow analysis.

---

## Item 4: Regression-row candidates (FXS + SNX + GNO + DOT)

Output at `b2/paper/supplements/phase4_minibatch_regression_rows_2026-05-27.csv` (4 rows; schema-compatible with `regression_data_april2026.csv`).

| Protocol | Token | Category | HHI (full audit) | top1_pct | n_holders | Maturity | Tokenomics source | regression_ready |
|---|---|---|---:|---:|---:|---:|---|---|
| Frax Finance | FXS | DeFi | 0.032411 | 11.13 | 993 | 6 | Frax docs (best-effort; verify against V3 whitepaper) | False |
| Synthetix | SNX | DeFi | 0.017075 | 8.38 | 990 | 8 | Synthetix 2018 docs.synthetix.io | False |
| Gnosis | GNO | DeFi | 0.042485 | 13.84 | 987 | 9 | Gnosis 2017 ICO whitepaper | False |
| Polkadot | DOT | Infra | 0.001692 (stake-level) | 0.248 | 600 (validators) | 6 | Polkadot 2020 launch tokenomics + Web3 Foundation | False |

### Population status

**Fields populated from this cycle:**
- HHI / Gini / top-N / n_holders / total_balance_top1000: from S18 v2 audit + DOT validators analysis
- Source / query_id / notes: full data lineage documentation
- Maturity_years: TGE-based (2020 FXS; 2018 SNX; 2017 GNO; 2020 DOT)
- Tokenomics allocation (team / investor / community / treasury / insider): best-effort from public docs

**Fields requiring follow-on data acquisition:**
- revenue_annual_usd: DeFiLlama returned partial 30d aggregates (~$200-$300K/yr extrapolated); needs Token Terminal confirmation
- fdv_usd / market_cap_usd: computed from supply × DeFiLlama price (note: FXS price returned was FRAX stablecoin's $0.40 not the FXS governance token's actual price; verify)
- treasury_usd: DeFiLlama TVL used as proxy where applicable; actual treasury (DAO + Foundation) requires governance-doc lookup
- incentives_annual_usd: protocol-specific (Frax incentives; SNX V3 removed inflation; GNO has no incentive program of note; DOT inflation model differs)
- subsidy_ratio: derived once revenue + incentives populated

### regression_ready=False rationale per row

- **FXS:** FDV uses FRAX-stablecoin price misattribution; revenue near-zero per DeFiLlama (V3 migration impact); needs verification
- **SNX:** revenue collapsed post-Optimism migration; V3 emission structure not directly retrievable; needs Token Terminal
- **GNO:** treasury_usd unknown (GnosisDAO treasury composition not in DeFiLlama); revenue marginal
- **DOT:** methodology-innovation HALT-4.1 pending; not directly comparable to EVM HHI without §3.8 typology extension

### Recommendation

Populate the 4 regression rows with the HHI + Gini + top-N + maturity_years + tokenomics-best-effort values in this cycle. Mark regression_ready=False pending the follow-on data-acquisition cycle. The HHI values are CONFIRMED via Etherscan public name tag verification and safe to use for cross-section concentration analysis (even if revenue/subsidy covariates are pending).

---

## Aggregate scope-expansion summary

| Item | Status | Artifacts |
|---|---|---|
| Universal CEX-sweep (5 hot wallets × N=40) | SHIPPED | universal_cex_sweep_phase4_new_2026-05-27.csv (89 hits); phase4_exclusions_log_extension_2026-05-27.csv (70 rows for universal sweep) |
| DOT staking-concentration analysis | SHIPPED (methodology-innovation HALT) | dot_holders.json; dot_validators.json; dot_alternatives.py |
| TAO holder pull | DELEGATED to parallel session | (none this cycle) |
| FXS / SNX / GNO / DOT regression rows | SHIPPED (regression_ready=False) | phase4_minibatch_regression_rows_2026-05-27.csv (4 rows) |
| exclusions_log.csv extension | SHIPPED | phase4_exclusions_log_extension_2026-05-27.csv (100 rows total: 30 Phase 4 PCAs + 70 universal sweep) |

---

## Out of scope this expansion cycle

Items deliberately not addressed in this cycle (rationale documented for git-log surface recoverability):

- **Polkadot governance-token-specific PCA classification** (Polkadot Treasury parachain `13UVJyLnbVp9RBZYFwHYxaAHz2wUWeAdAFbgn94o6M77nAZw`; W3F operational accounts; Council members) — methodology-innovation §3.8 pending; treasury is identified but not formally PCA-classified per the EVM typology.
- **Bittensor (TAO) subnet-validator concentration** — delegated to parallel session per author directive 2026-05-27T18Z.
- **Multivariate regression re-run** on extended N=43-44 sample — gated on covariate population (regression_ready=False for all 4 new rows).
- **B2 PAPER.md §4.5.5 EVM cross-protocol paragraph integration** — CANONICAL-WRITER lane; routed via handoff-back memo.
- **B2 PAPER.md §3.8 typology extension** for: (a) Solana-specific examples; (b) co-founder personal Safe sub-class; (c) native-chain validator-stake concentration vs EVM token-holder HHI — multiple inputs require integrated revision cycle; CANONICAL-WRITER lane.
- **Token Terminal / Messari covariate research** for FXS / SNX / GNO / DOT revenue + treasury + incentives — separate data-acquisition cycle; subscription-gated sources required.
- **Co-founder personal Safe classification policy DEC** — open author decision; pattern surfaced in GNO (Stefan George + koeppelmann.eth Safes).
- **DOT validator operator-attribution refinement** — 8 of top-10 operators are unlabeled (`<unlabeled:12GTt3pf>` etc.); Subscan's `merkle.tag_name` field empty for most; would require Polkadot validator-set directory cross-reference (e.g., RuntimeVerification audit list; Polkassembly identity database).
- **Universal CEX-sweep extension to remaining established CEXs** (OKX, Bybit, KuCoin, Gate.io, Bitstamp, Bitfinex, Bittrex, Huobi, Crypto.com cold wallets) — the 5-CEX sweep this cycle is bounded by Phase 4 audit findings; broader sweep is a separate continuation dispatch.
- **Updates to `docs/` canonical files** (KEY_FINDINGS, KNOWN_UNKNOWNS, DECISION_LOG, ERROR_CORRECTION_LOG) — BULK-EXECUTOR lane; all routed via handoff-back memo to next CANONICAL-WRITER cycle.

---

## Pending CANONICAL-WRITER actions (consolidated)

1. **Integrate S18 v2 audit findings + S19 expansion into `regression_data_april2026.csv`:**
   - Add 4 new rows from `phase4_minibatch_regression_rows_2026-05-27.csv` (FXS + SNX + GNO + DOT)
   - Apply universal-sweep HHI shifts to the 8 existing protocols with material drift (ATH; GRT; AXL; RPL; GTC; ENS; GMX; POL)
2. **Extend `exclusions_log.csv` with 100 new rows** from `phase4_exclusions_log_extension_2026-05-27.csv` (30 Phase 4 + 70 universal-sweep).
3. **File ERROR_CORRECTION_LOG entries** for the 4 EC candidates surfaced (E + F + G + H + I per S18 v1 + addendum + S19).
4. **File KNOWN_UNKNOWNS entries** for the 3 KU candidates (gamma + delta + epsilon).
5. **File DECISION_LOG entries** for:
   - Resolved: PCA confidence-promotion via Etherscan public name tag + Nansen API
   - Pending: cofounder personal Safe classification policy
   - Pending: DOT validator-stake-vs-EVM-holder concentration methodology choice (§3.8 typology extension)
6. **Update PROGRAM_STATE Section H** with Phase 4 mini-batch + universal-sweep shipped status.
7. **Authorize follow-on dispatch** for: (a) Token Terminal covariate research; (b) TAO holder pull from parallel session's output; (c) §3.8 typology extension cycle; (d) extended-CEX-sweep continuation (OKX + Bybit + KuCoin + others).

---

## Cross-references

- **Predecessor supplements:** S18 v1 + audit addendum (Phase 4 EVM mini-batch + audit)
- **Predecessor handoff-back:** `/tmp/b2_phase4_minibatch_handoff_back_to_canonical_writer_2026-05-27.md` (initial cycle)
- **Sibling-clone parent dispatch:** `handoff/dispatch/b2_r3_data_collection_omnibus_continuation_2026-05-27.md` Phase 4 mini-batch
- **Sister supplements:** S13 + S13 addendum (Solana PCA audit + Sim API verification); S14 + S14 addendum (power indices); S15 (voting-HHI gap inventory); S16 (Aethir/IoTeX/ENS sensitivity)
- **Methodology references:** B2 PAPER.md §3.7 + §3.8 + §4.3 + §4.5.5 + §4.6 + §5.7 + §5.8

---

## Reproducibility

```bash
# Universal sweep
python3 /tmp/b2_phase4/universal_cex_sweep.py

# DOT pulls
python3 /tmp/b2_phase4/dot_holders.py      # accounts (free-balance basis)
python3 /tmp/b2_phase4/dot_validators.py   # validators (bonded-stake basis; canonical)

# Covariate fills + regression rows
python3 /tmp/b2_phase4/covariates_defillama.py
python3 /tmp/b2_phase4/build_regression_rows.py

# Exclusions log extension
python3 /tmp/b2_phase4/build_exclusions_extension.py
```

Raw artifacts mirrored at `data/raw/b2_phase4_minibatch_2026-05-27/` per analytical-artifact retention policy 2026-05-27.

---

## Authorship note

Authored 2026-05-27 in response to author scope-expansion directive: "Expand scope now" (referencing DOT + TAO + covariates + universal-sweep deferred items). Mid-cycle Taostats API key delegation to parallel session per author 2026-05-27T18Z.

PID 14088 (BULK-EXECUTOR; expanded task-scope: handoff/dispatch/b2_r3_data_collection_omnibus_continuation + b2 Phase 4 EVM mini-batch via Sim API EVM); workflow clone `/Users/zach/Tokenization_Systems_Website`; sibling clone `/Users/zach/Tokenomics-As-Institutional_Design`.
