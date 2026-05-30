# Supplementary File S18 ADDENDUM: Phase 4 EVM mini-batch audit (Etherscan + Nansen verification)

**Companion to:** S18 v1 (`S18_phase4_evm_minibatch_2026-05-27.md`).
**Generated:** 2026-05-27. **Trigger:** author directive "Audit confident-only exclusion HHI" 2026-05-27T17Z.
**Authoring discipline:** per CLAUDE.md cross-session-artifact discipline; reader MUST run `python3 scripts/claude-code-sync.py` and grep current canonical files for cited identifiers BEFORE acting on any specific item; canonical state may have advanced since the as-of timestamp.

---

## Why this addendum

S18 v1 reported a counterintuitive HHI direction-of-shift pattern for FXS and SNX where confident-only exclusion HHI EXCEEDED pre-exclusion HHI (0.355 > 0.262 for FXS; 0.229 > 0.164 for SNX). The math was correct but the classification was incomplete: the rank-1 holder of each protocol was TENTATIVE-classified despite being identifiable via Etherscan public name tag verification. This addendum reports the audit findings + reclassifications + corrected HHI values.

The audit also surfaced four new cross-protocol CEX hot wallet identifications (Bitvavo, Luno, Crypto.com, Bitpanda) extending the universal-exclusion candidate set, and one substantive correction to Finding E (was attributed to Societe Generale based on EURCV holdings; actually Bitpanda CEX listing EURCV as tradeable asset).

---

## Audit methodology

Two-layer verification applied to S18 v1 classifications:

1. **Etherscan public name tag retrieval** via WebFetch on `etherscan.io/address/<address>` pages. The "Public Name Tag (viewable by anyone)" field is Etherscan's curated attribution for known entity-controlled addresses.
2. **Nansen Address Labels API** via POST `https://api.nansen.ai/api/v1/profiler/address/labels` with `apiKey` header. Returns Nansen's proprietary entity-classification labels (CEX hot wallets; Foundation-cofounder ENS social tags; behavioral classifications like "ETH Millionaire" / "Token Millionaire").

Confidence promotion criteria for TENTATIVE -> CONFIRMED:

- **Sufficient:** Etherscan public name tag matches PCA pattern (any protocol-identifying label like "Frax Finance: Comptroller", "Synthetix: Synthetix Core", "Fraxtal: Optimism Portal Proxy"); OR Nansen entity label matches known CEX / Foundation pattern.
- **Necessary:** independent verification beyond contract source-code name alone (which is a programmer-chosen template name, not an attribution).

---

## Audited reclassifications

### TENTATIVE -> CONFIRMED promotions (7 addresses)

| Address | Symbol | Original (v1) | Audited (v2) | Verification source |
|---|---|---|---|---|
| `0x36cb65c1967a0fb0eee11569c51c2f2aa1ca6f6d` | FXS #1 (48.28%) | TENTATIVE Class 4 "Frax v3 migration proxy" | **CONFIRMED Class 4** "Fraxtal: Optimism Portal Proxy" | Etherscan public name tag |
| `0xb1748c79709f4ba2dd82834b8c82d4a505003f27` | FXS #12 (0.64%) | TENTATIVE Class 2 "Frax Comptroller" | **CONFIRMED Class 2** "Frax Finance: Comptroller" | Etherscan public name tag |
| `0xffffffaeff0b96ea8e4f94b2253f31abdd875847` | SNX #1 (38.07%) | TENTATIVE Class 4 "SNX V3 Migrator proxy" | **CONFIRMED Class 4** "Synthetix: Synthetix Core" | Etherscan public name tag |
| `0x849d52316331967b6ff1198e5e32a0eb168d039d` | GNO #4 (4.17%) | TENTATIVE Class 2 "GnosisSafeProxy" | **CONFIRMED Class 2** "Gnosis: Active Treasury Management" | Etherscan public name tag |
| `0x4f8ad938eba0cd19155a835f617317a6e788c868` | GNO #8 (0.52%) | TENTATIVE Class 2 "TransparentUpgradeableProxy" | **CONFIRMED Class 3** "Gnosis: LGNO Token" (Locked GNO staking aggregation) | Etherscan public name tag |
| `0xae5fb390e5c4fa1962e39e98dbfb0ed8055ed7a9` | GNO #11 (0.34%) | TENTATIVE Class 2 "PayingProxy" | **CONFIRMED Class 2** "koeppelmann.eth Safe" (Gnosis co-founder personal custody) | Nansen `koeppelmann.eth*` social tag |

### CONFIRMED -> TENTATIVE downgrade (1 address)

| Address | Symbol | Original (v1) | Audited (v2) | Why downgrade |
|---|---|---|---|---|
| `0x9d94ef33e7f8087117f85b3ff7b1d8f27e4053d5` | GNO #6 (1.55%) | CONFIRMED Class 4 "Mintr / migration proxy" | **TENTATIVE Class 2** "Stefan George (Gnosis co-founder) Safe" | Etherscan creator: stefangeorge.eth (Gnosis co-founder); Nansen returns only generic "Proxy" tag; v1 attribution to Mintr was incorrect (mintr.gnosis.io is a different contract). Classification depends on author decision: do co-founder personal Safes count as Class 2 Foundation custody, or as institutional / individual? |

### NEW CONFIRMED additions (5 cross-protocol CEX hot wallets)

| Address | Protocols | Class | Nansen label | Etherscan label |
|---|---|---|---|---|
| `0xa023f08c70a23abc7edfc5b6b5e171d78dfc947e` | SNX #58 + GNO #90 | 5 | Crypto.com / Crypto.com: Hot Wallet / CEX | Crypto.com 22 |
| `0x0529ea5885702715e83923c59746ae8734c553b7` | FXS #38 + SNX #50 | 5 | (no specific label; ETH Millionaire only) | Bitpanda 18 / Beacon Depositor / Exchange |
| `0xedc6bacdc1e29d7c5fa6f6eca6fdd447b9c487c9` | FXS #14 + SNX #100 + GNO #100 | 5 | Bitvavo / CEX / Exchange | (no public tag) |
| `0xab782bc7d4a2b306825de5a7730034f8f63ee1bc` | SNX #57 + GNO #65 | 5 | Bitvavo / Bitvavo: Hot Wallet / CEX | (no public tag) |
| `0x3a5cc8689d1b0cef2c317bc5c0ad6ce88b27d597` | SNX #4 (3.87%) | 5 | Luno / Luno: Wallet / CEX | (no public tag) |

These five are candidate universal exclusions for the existing N=40 sample (parallel to Binance 8 / Coinbase 10 cross-protocol pattern documented in `exclusions_log.csv`). The Bitvavo + Crypto.com + Bitpanda multi-protocol presence parallels the §4.5.5 cross-protocol concentration finding at the CEX-custody axis.

---

## Corrected HHI summary (v2 audited)

| Symbol | HHI pre | HHI confident (v1) | HHI full (v1) | HHI confident (v2 audited) | HHI full (v2 audited) |
|---|---:|---:|---:|---:|---:|
| FXS | 0.261654 | 0.355062 (INCREASED +0.0934) | 0.031609 | **0.032411** (DECREASED -0.229) | **0.032411** (no TENTATIVE) |
| SNX | 0.164252 | 0.229055 (INCREASED +0.0648) | 0.021858 | **0.017075** (DECREASED -0.147) | **0.017075** (no TENTATIVE) |
| GNO | 0.272764 | 0.178622 (DECREASED -0.094) | 0.042080 | **0.076863** (DECREASED -0.196) | **0.042485** (2 TENTATIVE remain) |

**Direction-of-shift resolution.** The S18 v1 counterintuitive INCREASE pattern for FXS + SNX is fully resolved post-audit. Confident-only HHI now reflects proper Class 4 protocol-custody exclusion for both protocols. GNO retains a small CONFIRMED-vs-FULL delta (0.077 vs 0.042) driven by the Stefan George Safe + one unverified GnosisSafeProxy in the TENTATIVE set.

---

## Corrected top-1 shares (post-exclusion)

| Symbol | top-1 share pre | top-1 share confident (v1) | top-1 share confident (v2 audited) |
|---|---:|---:|---:|
| FXS | 48.28% | 59.15% (was rank-1 Fraxtal Portal; misclassified as TENTATIVE) | 11.13% (rank-2 veFXS now also excluded; new rank-1 = rank-3 EOA at 11.13%) |
| SNX | 38.07% | 47.22% (was rank-1 Synthetix Core) | 8.38% (rank-2 SynthetixBridgeEscrow + Binance + Coinbase + Luno excluded) |
| GNO | 38.69% | 40.54% (rank-1 Gnosis: Vesting excluded; rank-2 became Gnosis: Active Treasury) | 22.90% confident / 13.84% full |

---

## Regression-row candidates (corrected)

For integration into `data/processed/regression_data_april2026.csv` (extending N=40 -> N=43):

| symbol | category | chain | hhi (HHI full audited) | top1_pct | top5_pct | top10_pct | n_holders | gini | maturity_years |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| FXS | DeFi | ethereum | 0.032411 | 11.13 | 35.79 | 50.32 | 993 | 0.9095 | 6 |
| SNX | DeFi | ethereum | 0.017075 | 8.38 | 26.16 | 36.50 | 990 | 0.8959 | 8 |
| GNO | DeFi | ethereum | 0.042485 | 13.84 | 36.95 | 51.74 | 987 | 0.9111 | 9 |

**Note on TENTATIVE remainders for GNO:** the Stefan George Safe (1.55%) + unverified GnosisSafeProxy (0.12%) jointly contribute approximately 1.67% of pre-exclusion top-1000. Excluding them yields HHI = 0.0425 (the "full" column above); including them yields HHI = 0.0769 (the "confident" column). The author decision on co-founder-personal-vs-Foundation custody affects this 0.04 HHI delta.

Insider / team / investor / treasury / community / subsidy / FDV covariates remain UNPOPULATED for these 3 rows; they require independent acquisition (Token Terminal + protocol docs + DeFiLlama). The HHI + Gini + top-N columns are populated from this audit.

---

## Universal-exclusion sweep candidates (cross-protocol CEX)

The 5 newly-confirmed CEX hot wallets (Crypto.com 22; Bitpanda 18; Bitvavo; Bitvavo: Hot Wallet; Luno: Wallet) are candidates for **universal exclusion sweep across existing N=40 sample**, parallel to the 2026-05-19 universal exclusion sweep that surfaced Binance 8 / Bithumb 462 / Coinbase 10 cross-protocol holdings.

Recommended universal-sweep procedure (sister to the 2026-05-19 cycle):

1. For each of the 5 new CEX addresses, scan top-1000 holder list of existing N=40 protocols for cross-references.
2. Document hit-rate per protocol (e.g., does Crypto.com 22 appear in any of the existing 40?).
3. Add CONFIRMED Class 5 rows to `exclusions_log.csv` per protocol where the address appears.
4. Recompute affected HHI values; cascade to regression dataset if material.

The universal sweep is in-scope for a separate continuation dispatch (sister to S13 Phase 5 continuation pattern).

---

## Substantive findings (corrected from S18 v1)

### Finding A (corrected): Migration-custody dominates pre-exclusion HHI for FXS and SNX (CONFIRMED post-audit)

For both FXS and SNX, the top-1 holder is a verified protocol-controlled custody contract:

- **FXS top-1 = "Fraxtal: Optimism Portal Proxy"** (52.48% of top-1000): the Frax L2 (Fraxtal) bridge custody, equivalent to Optimism Portal pattern. Acquired 2025-04-29 coincident with Fraxtal launch. Class 4 (bridge custody).
- **SNX top-1 = "Synthetix: Synthetix Core"** (38.07% of top-1000): the V3 protocol-controlled inflation / treasury contract. Acquired 2023-07-07 coincident with V3 launch. Class 4 (V3 protocol-controlled custody; in this case the "Core" naming reflects the Synthetix V3 architecture's central protocol contract).

Pre-exclusion HHIs (FXS 0.262; SNX 0.164) are dominated by these protocol-controlled custody contracts, NOT by retail concentration. Post-exclusion HHIs (FXS 0.032; SNX 0.017) are consistent with B2's mature-DeFi sector pattern.

**Methodology implication:** the v1 "Migration Proxy confidence threshold" question is moot for these two cases (Etherscan public name tag is sufficient); but the general pattern (V3-migration custody at top-1) recurs across mature DeFi protocols and should be documented in B2 §3.8 typology updates.

### Finding B (preserved): GNO Class 1 burn-destination dominance

Unchanged from v1: 31.62% of top-1000 GNO at null address; Genesis-burn-dominant pattern parallel to IOTX. After full audit, GNO also has substantial Foundation custody: Gnosis: Vesting (38.69%) + Gnosis: Active Treasury Management (4.17%) + LGNO staking (0.52%) + 2 co-founder Safes (1.89%) = approximately 45.27% Foundation-aligned custody. Combined with null burn (31.62%) and Omnibridge (14.05%), the protocol-controlled aggregate exceeds 90% of top-1000.

### Finding C (corrected): Cross-protocol EOA pattern is overwhelmingly CEX custody, not institutional funds

S18 v1 reported 10 cross-protocol top-100 holders, with 4 "substantive cross-protocol-class examples." Post-audit:

| Cross-protocol address | Original (v1) classification | Audited (v2) classification |
|---|---|---|
| `0xa023f08c70a23abc7edfc5b6b5e171d78dfc947e` | CEX (Crypto.com institutional) | **CONFIRMED CEX (Crypto.com 22 / Crypto.com: Hot Wallet)** |
| `0xd2dd7b597fd2435b6db61ddf48544fd931e6869f` | Institutional treasury or DeFi book ($385M; ETH+LINK+PAXG+ONDO+AAVE) | **Sophisticated individual / fund** (Nansen: ETH Millionaire only; no entity attribution) |
| `0x0529ea5885702715e83923c59746ae8734c553b7` | TradFi-EUR institutional (Societe Generale EURCV custody) | **CONFIRMED CEX (Bitpanda 18)** — Finding E in v1 INCORRECT; the $14.8M EURCV is Bitpanda listing EURCV as tradeable asset, not SG operational custody |
| `0x7dafba1d69f6c01ae7567ffd7b046ca03b706f83` | Drained wallet (transactional pattern) | **Unchanged; sophisticated transactional wallet** (Nansen: ETH Millionaire only) |
| `0xedc6bacdc1e29d7c5fa6f6eca6fdd447b9c487c9` | (older mixed) | **CONFIRMED CEX (Bitvavo)** |
| `0xab782bc7d4a2b306825de5a7730034f8f63ee1bc` | (SNX+GNO same-day) | **CONFIRMED CEX (Bitvavo: Hot Wallet)** |
| `0xa023f08c70a23abc7edfc5b6b5e171d78dfc947e` | (above) | (above) |

**Revised Finding C narrative:** the EVM cross-protocol top-100 holder pattern is **dominantly CEX-custody overlap** (parallel to S13 Solana Finding F: 6 of 7 candidates classified Class 5 CEX). Of the 10 cross-protocol top-100 addresses in FXS / SNX / GNO:

- 7 are CONFIRMED CEX hot wallets (Binance 8 + Binance 14 + Coinbase 10 + Crypto.com 22 + Bitpanda 18 + Bitvavo + Bitvavo: Hot Wallet).
- 1 is Luno (SNX only at rank-4; not cross-protocol but newly identified CEX).
- 3 are unclassified by Nansen entity-label set (`0xd2dd...` + `0x7dafba...` + `0x7bf3cc...`); behavioral classification per S13 heuristic suggests sophisticated retail / fund / market-maker pattern without specific entity attribution.

The cross-protocol concentration pattern is therefore **mechanical CEX-custody overlap** (Binance lists FXS + SNX; Bitvavo lists FXS + SNX + GNO; Crypto.com lists SNX + GNO; Bitpanda lists FXS + SNX) — paralleling S13 Solana Finding G refinement that "cross-protocol pattern is mechanical CEX-custody overlap, distinct from coordinated single-entity multi-protocol custody."

### Finding D (preserved): Crypto.com 22 newly identified CEX hot wallet

Unchanged from v1; verified post-audit via both Etherscan public name tag ("Crypto.com 22") and Nansen ("Crypto.com" / "Crypto.com: Hot Wallet" / "CEX"). Universal-exclusion candidate.

### Finding E (corrected): Bitpanda 18, NOT Societe Generale; same-day FXS+SNX acquisition

**Finding E in S18 v1 was INCORRECT.** The address `0x0529ea5885702715e83923c59746ae8734c553b7` is Bitpanda (Austrian exchange) per Etherscan public name tag "Bitpanda 18". The $14.8M EURCV (Societe Generale's tokenized euro) holding reflects Bitpanda LISTING EURCV as a tradeable asset on its exchange, not SG operational custody. EURC + EURCV concentration on a Bitpanda hot wallet is consistent with European exchange offering Euro-denominated stablecoin trading pairs.

**Substantive implication:** the originally-hypothesized "first TradFi-affiliated institutional address in B2 cross-section" is retracted. Bitpanda is a standard exchange (not a TradFi institution), and its EUR-stablecoin balances are operational liquidity for exchange customers, not custody on behalf of TradFi clients.

### Finding F (new post-audit): Gnosis co-founder personal Safes surfaced

Two GNO top-20 holders are personal Safes deployed by Gnosis co-founders:

- `0x9d94ef33e7f8087117f85b3ff7b1d8f27e4053d5` (1.55%) created by **stefangeorge.eth** (Stefan George, Gnosis co-founder).
- `0xae5fb390e5c4fa1962e39e98dbfb0ed8055ed7a9` (0.34%) labeled **koeppelmann.eth** (Martin Koppelmann, Gnosis co-founder).

These surface a methodology question for B2 §3.8: do founder-personal Safes count as Class 2 Foundation custody, or as separate "founder allocation" custody?

**Implications:**

- If counted as Class 2 Foundation: post-PCA HHI = 0.0425 (GNO full).
- If retained as non-PCA: post-PCA HHI = 0.0769 (GNO confident).

The 0.034 HHI delta is small relative to GNO's pre-exclusion HHI (0.273) but meaningful in absolute terms (factor-of-1.8 difference). Sister to S11 Aethir cycle's "high-share-Foundation-not-CONFIRMED-PCA" pattern. Recommended for DEC-eligible author decision on `cofounder_personal_custody_classification` rule.

---

## Error-correction candidates (CORRECTED + EXPANDED)

### EC candidate E (preserved): FXS top-1000 cumulative exceeds nominal total supply (108.71 percent)

Unchanged from v1. Methodology-of-record gap; HHI invariant to this issue.

### EC candidate F (RESOLVED): FXS top-1 holder classification confidence

**Status:** RESOLVED in audit. FXS top-1 `0x36cb65c1967a0fb0eee11569c51c2f2aa1ca6f6d` is "Fraxtal: Optimism Portal Proxy" per Etherscan public name tag; CONFIRMED Class 4 (bridge custody).

### EC candidate G (RESOLVED): SNX top-1 holder classification confidence

**Status:** RESOLVED in audit. SNX top-1 `0xffffffaeff0b96ea8e4f94b2253f31abdd875847` is "Synthetix: Synthetix Core" per Etherscan public name tag; CONFIRMED Class 4 (V3 protocol-controlled custody).

### EC candidate H (NEW): S18 v1 Finding E mis-attribution (Bitpanda vs Societe Generale)

**Class:** documentation-defect-in-supplement class (sister to EC-2026-05-20-DEC-179-Memory-Mirror-M2-Documentation-Defects).

**Context.** S18 v1 Finding E asserted `0x0529ea5885702715e83923c59746ae8734c553b7` is a Societe Generale EUR institutional holder based on $14.8M EURCV holdings. Etherscan public name tag and Nansen verification both confirm this is Bitpanda (Austrian exchange) hot wallet 18; the EURCV holding reflects Bitpanda listing EURCV as a tradeable asset.

**Root cause.** Pre-audit classification relied on token-portfolio inference (EURCV holding -> SocGen affiliation) without entity-tag verification.

**Fix.** S18 v2 supersedes v1 Finding E with corrected Bitpanda classification.

**Prevention pattern:** for cross-protocol holder identity attribution, verify via Etherscan public name tag + Nansen Address Labels API BEFORE asserting entity-class attribution based on portfolio-composition inference alone.

### EC candidate I (NEW): S18 v1 GNO #6 mis-attribution (Mintr vs Stefan George Safe)

**Class:** PCA-classification-attribution drift (sister to HONEY EC candidate A).

**Context.** S18 v1 classified GNO #6 `0x9d94ef33e7f8087117f85b3ff7b1d8f27e4053d5` as CONFIRMED Class 4 "Mintr / migration proxy" with documentation reference docs.gnosischain.com. Etherscan creator verification reveals the contract is a Safe deployed by stefangeorge.eth (Gnosis co-founder Stefan George); no public name tag attests to "Mintr" attribution. The actual GNO Mintr migration contract is at a different address (mintr.gnosis.io references a UI, not this contract).

**Fix.** S18 v2 reclassifies to TENTATIVE Class 2 (founder-personal custody pending DEC-eligible author decision on cofounder-personal vs Foundation-operational distinction).

**Prevention pattern:** for protocol-documentation cross-references, verify the documented address matches the audited Etherscan contract before asserting PCA classification.

---

## Updated known-unknown candidates

### KU candidate gamma (preserved): EVM cross-protocol institutional custody pattern empirical breadth

Unchanged from v1.

### KU candidate delta (RESOLVED partially): Crypto.com + Bitpanda + Bitvavo + Luno cross-protocol CEX prevalence

**Resolution.** The 5 newly-confirmed CEX hot wallets (Crypto.com 22; Bitpanda 18; Bitvavo + Bitvavo: Hot Wallet; Luno: Wallet) are NOT one-off appearances; they appear across multiple of FXS / SNX / GNO. Universal-sweep candidate for existing N=40 sample.

**Pending data:** universal-sweep results across existing N=40 sample (separate continuation dispatch).

### KU candidate epsilon (NEW): co-founder personal Safe classification policy

**Question.** Do co-founder personal Safes (verified via deployer ENS / Nansen social tags) count as Class 2 Foundation custody, or as separate founder-allocation custody, in B2 §3.8 typology?

**Significance.** Pattern surfaced in GNO (Stefan George + Martin Koppelmann Safes); likely recurs in other protocols (Vitalik / Ethereum Foundation; Charlie Lee / Litecoin; etc.). DEC-eligible after 2-of-N anchor.

**Pending data:** Phase 4 continuation + universal-sweep cycles to identify additional co-founder Safe instances across existing N=40 sample.

---

## DEC candidates

### DEC candidate (preserved, RESOLVED for this cycle): Migration Proxy PCA confidence threshold

**Resolution.** Etherscan public name tag verification is sufficient (replacing the pre-audit "pattern-criteria-based promotion" framing). For future Phase 4 expansion protocols, the verification chain is:

1. Etherscan public name tag retrieval (WebFetch on address page).
2. Nansen Address Labels API cross-check (POST /api/v1/profiler/address/labels).
3. If either yields PCA-pattern attribution: CONFIRMED.
4. If neither yields attribution: TENTATIVE; further verification (creator-chain trace; protocol-doc cross-reference) required.

### DEC candidate (NEW): Cofounder personal Safe classification policy

Per KU candidate epsilon. Open for author decision.

---

## Acceptance test (Phase 4 mini-batch audit)

- [x] All confident-only HHI direction-of-shift anomalies resolved post-audit.
- [x] Top-1 holder of each protocol verified via Etherscan public name tag.
- [x] Nansen Address Labels API integrated as verification layer.
- [x] Cross-protocol CEX hot wallet identifications expanded (5 new addresses).
- [x] Finding E mis-attribution (Bitpanda vs SocGen) corrected.
- [x] Finding C (cross-protocol pattern) refined: dominantly mechanical CEX-overlap.
- [ ] Universal-sweep across existing N=40 sample (deferred to separate continuation dispatch).
- [ ] Author DEC on cofounder personal Safe classification (deferred).
- [ ] Insider / team / investor / FDV covariates populated for FXS + SNX + GNO regression rows (deferred to data-acquisition cycle).

---

## Reproducibility

```bash
# Step 1: Pull top-1000 holders (Sim API)
mkdir -p /tmp/b2_phase4
dune sim evm token-holders 0x3432B6A60D23Ca0dFCa7761B7ab56459D9C964D0 --chain-id 1 --limit 1000 -o json > /tmp/b2_phase4/fxs_holders.json
dune sim evm token-holders 0xC011a73ee8576Fb46F5E1c5751cA3B9Fe0af2a6F --chain-id 1 --limit 1000 -o json > /tmp/b2_phase4/snx_holders.json
dune sim evm token-holders 0x6810e776880C02933D47DB1b9fc05908e5386b96 --chain-id 1 --limit 1000 -o json > /tmp/b2_phase4/gno_holders.json

# Step 2: Audited classification + HHI pipeline
cd /Users/zach/Tokenomics-As-Institutional_Design
python3 b2/paper/supplements/phase4_evm_minibatch_v2_audited_2026-05-27.py

# Step 3 (optional): Re-run Etherscan + Nansen verification for new addresses
# (Etherscan WebFetch + Nansen POST API; see /tmp/b2_phase4/nansen_labels.py)
```

Outputs at `b2/paper/supplements/phase4_evm_minibatch_v2_audited_*.csv` (3 files).

---

## Cross-references

- **Predecessor (this cycle):** `S18_phase4_evm_minibatch_2026-05-27.md` (v1; superseded by this addendum on Finding E + GNO #6 + direction-of-shift framing)
- **Parent dispatch:** `handoff/dispatch/b2_r3_data_collection_omnibus_continuation_2026-05-27.md` Phase 4 mini-batch
- **Sister supplements:**
  - S13 + S13 addendum (Solana PCA audit; mechanical-CEX-custody refinement Finding G)
  - S14 + S14 addendum (power indices N=11 + WXM structural-majority)
  - S16 (Aethir / IoTeX / ENS sensitivity precedent)
- **Memory anchors:** `feedback_hhi_direction_of_shift_counterintuitive` (sister anchor; direction-of-shift class resolved post-verification); `reference_sim_api_cex_vs_institutional_classification` (heuristic applied; Nansen entity-label verification supersedes for cross-protocol cases)
- **Existing exclusions log:** `data/processed/exclusions_log.csv` (134 rows; this audit proposes 28 CONFIRMED + 2 TENTATIVE row additions; 5 of the CONFIRMED CEX rows are universal-sweep candidates)

---

## Authorship note

Authored 2026-05-27 in direct response to author audit directive: "Audit confident-only exclusion HHI". Etherscan WebFetch + Nansen API verification used as two-layer audit; Nansen API key provided by author 2026-05-27 mid-cycle.

PID 14088 (BULK-EXECUTOR; task-scope b2_phase_4_mini_batch_fxs_snx_gno via Sim API EVM); workflow clone `/Users/zach/Tokenization_Systems_Website`; sibling clone `/Users/zach/Tokenomics-As-Institutional_Design`.
