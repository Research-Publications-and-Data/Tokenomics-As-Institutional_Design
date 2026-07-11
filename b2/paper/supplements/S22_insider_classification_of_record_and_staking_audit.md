# Supplementary File S22: Insider Classification of Record and Staking-Attribution Audit

This file is the reviewer-facing index to the insider-classification and staking-attribution materials in the replication package. It documents, in three parts: (1) the evidence-traced per-survivor insider classification that the main text relies on for the insider-retention measure and the six-scheme robustness check; (2) the deployer-and-signer tracing of the seventeen high-share unlabeled Safe holders that resolves the team-confirmed-multisig rule; and (3) the two staking-attribution methodology results (token-level insider-share attribution for the two largest liquid-staking wrappers, and orchestrator-level bloc-voting concentration for Livepeer).

Every numeric value cited here reproduces from the one-command reproduction script and the persisted inputs in the replication repository (no scratch-directory dependency, no live-API calls at reproduction time). Reproduction entry points are listed in Part 4.

---

## Part 1: Insider classification of record (per survivor)

### 1.1 What the classification is

For each protocol, the top ten post-exclusion holders (the survivors of the protocol-controlled-address exclusion methodology) are classified as insider or non-insider. The classification of record uses Nansen entity labels as the primary signal, supplemented by on-chain deployer-and-signer tracing where the label is a bare or generic Safe or multisig with no protocol attribution. An insider is a protocol team, foundation, treasury, named investor or venture fund, vesting or lock contract holding a team or investor allocation, or a multisig demonstrably controlled by the protocol team. Centralized-exchange custody, decentralized-exchange liquidity pools, reward and emission distributor contracts, bridge and migration infrastructure, market makers absent project-seeding evidence, behavioral whale labels (for example "Token Millionaire" or "High Balance"), and bare unlabeled externally-owned accounts are not insiders.

The classification differs from a keyword-only rule in one load-bearing way: a bare Safe or multisig is not automatically counted as insider. It is counted as insider only when deployer-and-signer tracing establishes a protocol-team tie (the team-confirmed-multisig rule). This correction de-counts independent holders' Safes that a keyword rule would over-count, and is what separates the classification of record from the keyword-floor lower bound used in the robustness sweep.

### 1.2 Per-survivor insider count (insiders of ten top-holder survivors)

The table below records, for each protocol with at least one insider survivor, the insider count over the ten survivors and the resolved insider entities with their roles. Eight protocols (Axelar, Curve, Grass, io.net, Jupiter, Optimism, Render, Wormhole) have zero insider survivors under the classification of record and are omitted from the entity column; their top-ten survivors are exchange custody, liquidity pools, distributor or bridge contracts, market makers, or unlabeled retail.

| Protocol | Insiders / 10 | Resolved insider entities (role) | Evidence basis |
|---|---|---|---|
| AAVE | 1 | Aave Ecosystem Reserve (treasury) | Entity label |
| Anyone | 1 | Vesting contract (vesting lock) | Entity label |
| ARB | 1 | Lightspeed Fund (investor) | Entity label |
| ATH (Aethir) | 4 | Aethir (treasury); MerkleVester (vesting); two Aethir Investment Recipients (investor) | Entity label |
| BAL | 1 | Balancer Shareholder (investor) | Entity label |
| COMP | 3 | Compound COMP Multisig (team multisig, signer-traced); Geoffrey Hayes (founder); Sablier Vesting (vesting) | Entity label + signer tracing |
| DIMO | 1 | Team multisig (deployer-and-signer-traced) | Signer tracing |
| DRIFT | 4 | Drift (treasury); Drift Investment Recipient (investor); Drift Foundation (foundation); Drift Custody Vaults (treasury) | Entity label |
| ENS | 2 | Nick Johnson (founder); Gnosis Safe Proxy (multisig) | Entity label |
| ETHFI | 4 | three ETHFI Investment Recipients (investor); ether.fi DAO Treasury (treasury) | Entity label |
| GEOD (Geodnet) | 1 | ParaFi Capital (investor) | Entity label |
| GMX | 4 | two team SafeProxies (deployer-traced); GMX Timelock (treasury); GMX Vester (vesting) | Entity label + deployer tracing |
| GRT | 1 | The Graph Multisig (team multisig) | Entity label |
| HNT (Helium) | 1 | Helium (treasury) | Entity label |
| HONEY (Hivemapper) | 2 | two Hivemapper team wallets (treasury) | Entity label |
| IOTX | 2 | IOTX Investment Recipient (investor); machinefi.eth (team) | Entity label |
| LDO | 4 | Lido DAO Multisig (multisig); KR1 (investor); two Lido treasury wallets (treasury) | Entity label |
| LPT (Livepeer) | 2 | two bare Safe or multisig holders (team-controlled per rule) | Entity label |
| META (MetaDAO) | 4 | MetaDAO (treasury); MetaDAO Custody Vaults (treasury); Investment Recipient (investor); Variant (investor) | Entity label |
| MKR | 2 | two team-controlled multisigs (deployer-and-signer-traced) | Signer tracing |
| MOR (Morpheus) | 2 | two Big Brain Holdings wallets (investor) | Entity label |
| MPL_SYRUP (Maple) | 4 | SYRUP Foundation (treasury); SYRUP Investment Recipient (investor); Framework Ventures (investor); Castle Island Ventures (investor) | Entity label |
| POL | 1 | Polygon MATIC-to-POL Migration (treasury) | Entity label |
| RPL (Rocket Pool) | 1 | RPL Investment Recipient (investor) | Entity label |
| UNI | 3 | two Uniswap Team allocations (team); a16z crypto UNI Tokens (investor) | Entity label |
| WXM (WeatherXM) | 2 | two bare Safe proxies (team-controlled per rule) | Entity label |
| ZRO (LayerZero) | 7 | LayerZero ZRO Multisig and ZRO Multisig (multisig, signer-traced); three LayerZero team addresses; LayerZero Strategic Partnerships (investor-partner allocation); LayerZero Foundation (foundation) | Entity label + signer tracing |

These per-survivor insider counts are the insider-retention regressor used in the powered model and in the six-classification robustness sweep. The full per-holder spine (rank, share, Nansen label, entity type, classification reason, and traced source for all ten survivors of every protocol) is persisted in the replication package as the traced classification table (see Part 4).

### 1.3 Where the classification of record sits among the six schemes

The main text reports that the DePIN sector coefficient stays positive and significant under six independent insider-classification schemes, with two-sided p-values from 0.0013 to 0.0082 (all below 0.01). The six schemes and their reproduced retention-specification DePIN p-values are:

| Scheme (descriptive label) | DePIN p |
|---|---:|
| Keyword-floor lower bound (any treasury or multisig keyword counted insider) | 0.0013 |
| Reliability-gated reviewed (reviewed where the current label reliably matches; prior coding retained elsewhere) | 0.0037 |
| Evidence-traced classification of record (entity labels plus deployer-and-signer tracing) | 0.0050 |
| Adversarially reviewed (full adoption of the reviewed labels) | 0.0054 |
| Original cohort-baseline classification | 0.0072 |
| Gap-filled resolved (most permissive gap-filled variant) | 0.0082 |

The classification of record sits inside this range at 0.0050. Because it corrects the over-count present in keyword-only coding (the team-confirmed-multisig rule de-counts independent holders' Safes), the sector signal is, if anything, sharpest at the keyword floor and remains comfortably significant under the more conservative classification of record. The insider-retention regressor itself is not significant under any of the six schemes (the channel-shift noted in the main text), so the result is carried by the sector channel, not the insider-retention channel, regardless of classification choice.

---

## Part 2: The seventeen high-share bare Safe holders, traced

### 2.1 Why these seventeen

Seventeen survivors across the cross-section carry a bare or generic Safe, GnosisSafeProxy, or "Multisig" Nansen label with no protocol name attached. A keyword-only rule would count all seventeen as insider on the multisig keyword alone. The team-confirmed-multisig rule instead traces each one through its deployer, its first funder, and its current and previous signers, and counts it as insider only when that tracing establishes a protocol-team tie. The result reclassifies six of the seventeen as protocol-team Safes (insider) and eleven as independent holders' Safes (not insider). This is the correction that distinguishes the classification of record from the keyword-floor lower bound.

### 2.2 Verdict table

Six team-confirmed (insider):

| Survivor | Resolved controlling entity | Tracing evidence |
|---|---|---|
| COMP top-holder Safe | Compound Timelock / Compound governance | Signers include the Compound Timelock and a TimelockController; the Safe's own label is the Compound COMP Multisig |
| GMX Safe (first instance) | GMX (gmxresearch.eth) | First funder is gmxresearch.eth, the GMX team and research funding wallet |
| GMX Safe (second instance) | GMX (gmxresearch.eth) | Deployed by gmxresearch.eth, tying the Safe directly to the GMX team |
| MKR DeFi Manager Safe | MakerDAO DeFi Manager | Deployed and signed by an address labeled MakerDAO DeFi Manager |
| ZRO Safe (first instance) | LayerZero (ZRO) Multisig | The Safe itself carries the explicit LayerZero multisig entity label |
| ZRO Safe (second instance) | LayerZero (ZRO Multisig) | The input address carries the dispositive LayerZero ZRO Multisig entity label |

Eleven independent (not insider):

| Survivor | Resolved controlling entity | Tracing evidence |
|---|---|---|
| MKR Safe (independent) | Unlabeled externally-owned-account multisig | All current and previous signers are unlabeled accounts; deployer is an unlabeled account; no MakerDAO or Sky tie |
| DIMO Safe (High Activity) | Unlabeled account (behavioral High Activity label) | Deployed by an unlabeled account; first-funded through a bridge contract; no DIMO team tie |
| DIMO Safe (unlabeled deployer) | Unlabeled deployer account | Deployed by an unlabeled account; first-funded by an unrelated naming-service account; no DIMO tie |
| DIMO Safe (OpenSea handle) | Account with an OpenSea username only | Deployed by an account carrying only a marketplace handle; no DIMO tie |
| GEOD Safe (first instance) | Account with a behavioral Token Millionaire label | Deployed by a generic non-protocol account; no Geodnet tie or protocol signers |
| GEOD Safe (second instance) | Account with a behavioral Token Millionaire label | Deployed by the same generic non-protocol account; no Geodnet tie |
| MOR Safe (first instance) | Unlabeled deployer account | Deployed and first-funded by an unlabeled account; no Morpheus tie, no labeled signers |
| MOR Safe (second instance) | Unlabeled deployer account | Deployed by an unlabeled account; no Morpheus name, no labeled signers |
| MOR Safe (third instance) | Unlabeled deployer account (behavioral High Activity label) | Deployed by an unlabeled account; first-funded by an unlabeled account; no Morpheus tie |
| WXM Safe (first instance) | Account with a behavioral High Activity label | Deployed by an account carrying only a generic behavioral label; no WeatherXM name, no protocol signers |
| WXM Safe (second instance) | Account with a generic Deployer label | Deployed by an account carrying only a generic Deployer label; no WeatherXM tie |

### 2.3 Net effect

The eleven de-counted independent Safes are the difference between a keyword-only insider tally and the classification of record. Their removal is why the keyword-floor scheme reads as a lower bound on the DePIN p-value (0.0013) and the classification of record reads slightly more conservative (0.0050): the keyword rule attributes independent holders' Safes to protocol teams, modestly inflating measured insider retention and tightening the apparent sector contrast. The classification of record reverses that, and the sector result survives the reversal. Two additional protocol-team Safes that are not part of the bare-label seventeen (one MakerDAO Safe confirmed through its own GnosisSafe deployer trace, plus the labeled team Safes carried by entity label) are counted in Part 1 directly.

---

## Part 3: Staking-attribution audit

The holder-concentration measure is computed over current token holders. For protocols with a large liquid-staking wrapper, insider tokens can sit inside the staking contract and become invisible to a holder snapshot, which holds the wrapper, not the underlying insiders. This part documents two attribution exercises and one orchestrator-level governance recomputation. The first two (token-level insider attribution) do not change the frame holding-HHI beyond display precision; the third (staking-pool pass-through, Section 3.4) is load-bearing for the sector-contrast magnitude and is the basis for the consistent-treatment headline in Section 4.6.2.

### 3.1 AAVE and ENA: insider tokens inside the staking wrapper

For AAVE, the staking wrapper (stkAAVE) holds 21.67 percent of AAVE supply (3,005,689 AAVE on the supply base used in the manuscript). Attributing the insider portion of that staked balance back to its underlying insider holders reveals that 4.4 percent of AAVE supply is clearly insider AAVE held inside the wrapper, rising to 6.3 percent of supply when ambiguous insider attributions are included. This insider AAVE is invisible to the holder snapshot, which sees only the wrapper contract. The address-level holding HHI is essentially unchanged when the attribution is performed (0.012790 baseline against 0.012744 attributed, a change below display precision and, if anything, marginally dilutive because attribution redistributes a single large wrapper balance across several smaller insider holders). The finding is the insider share and its visibility, not an HHI movement. This is consistent with the manuscript's argument that holding-HHI understates effective concentration.

For ENA, the equivalent attribution moves a much smaller share: 0.43 percent of ENA supply is insider ENA held inside the staking wrapper, and the address-level holding HHI again moves below display precision and dilutively (0.047164 baseline against 0.046662 attributed). The frame holding-HHI is left at the baseline for both tokens. Both are reported as consistency methodology notes supporting the Section 3.8 staking treatment and the Section 4.4 AAVE methodology paragraph.

### 3.2 LPT: orchestrator-level bloc-voting concentration

Livepeer governance operates a delegated bloc-voting model: delegators bond LPT to orchestrators, who then vote the aggregate bonded stake through the bonding manager. The governance-relevant concentration is therefore the distribution of bonded stake across orchestrators, not the raw token-holder distribution. Computed over the 100 active orchestrators (as of the Arbitrum block recorded in the replication artifact), the orchestrator-level bloc-voting HHI is 0.0535, against a raw post-exclusion token-holder HHI of 0.198868 for the same protocol. The orchestrator-level concentration is roughly 3.7 times lower than the holding concentration (a ratio of about 0.27). Including the inactive-but-bonded orchestrators moves the figure only from 0.0535 to 0.0524, so the result is not an artifact of the active-set cutoff.

This makes Livepeer the most pronounced DePIN governance disperser, at a 0.27 ratio, joining the delegation-disperses exceptions documented for ENS, GMX, Helium, and Jupiter. Helium is the other DePIN-sector disperser, so Livepeer is the most pronounced rather than the only DePIN dispersion exception. The frame holding-HHI for Livepeer is unchanged at 0.198868; the orchestrator-level figure is reported as an additional voting-versus-holding data point in Section 4.5, not as a substitute for the holding measure.

### 3.3 What the staking audit does not change

All three exercises leave the frame holding-HHIs used in the regressions unchanged within display precision. The DePIN-versus-DeFi sector contrast, the multivariate specifications, and the six-classification robustness sweep are all computed on the holder-concentration frame and are unaffected. The staking audit documents that the holder snapshot understates insider visibility for staked protocols (AAVE and ENA) and that delegated bloc-voting can disperse rather than concentrate governance (Livepeer), both of which strengthen, rather than revise, the main-text reading.

---

### 3.4 Per-pool staking decomposition (staking-aggregation contracts as distributed voter pools)

Staking-aggregation contracts pool the stake of many independent governance-eligible holders; treating each as a single holder (which retaining it would do) or excluding it outright both distort the holding-concentration measure. The voter-inclusive treatment in Section 4.6.2 distributes each material staking pool across its measured underlying stakers. The internal staker concentration (HHI among a pool's stakers, as shares of the pool) was measured per pool; the breakpoint at which the headline contrast loses significance is an internal HHI of approximately 0.10.

| Pool | sector | pool share of supply | internal staker-HHI | dominant staker | stakers |
|---|---|---|---|---|---|
| GMX staked tracker | DeFi | 64% | 0.008 | 4.5% | 68,127 |
| Rocket Pool RPL | DeFi | 49% | 0.023 | 9.1% | 1,655 |
| Curve veCRV | DeFi | 40% | 0.278 | 49.5% (Convex) | 8,617 |
| Synthetix V3 SNX | DeFi | 38% | 0.142 | 28.2% | 3,268 |
| stkAAVE | DeFi | 22% | 0.029 | 10.7% (20.5% team excluded) | distributed |
| ether.fi ETHFI | DeFi | 11% | 0.041 | 10.8% | 7,108 |
| IoTeX staking | DePIN | 20% | 0.018 | 5.0% | 1,095 |
| ANyONe staking | DePIN | 13% | 0.025 | 8.6% | 451 |
| Livepeer bonding | DePIN | 1.8% | 0.047 | 17.1% | 3,067 |

The big DeFi staking pools are highly distributed (GMX 68,127 stakers; Rocket Pool 1,655 node operators), with vote-escrowed CRV (49.5 percent Convex-controlled) and Synthetix V3 (top 28 percent) the concentrated exceptions. Distributing the pools to their stakers (excluding only the team/foundation slice, e.g. stkAAVE 20.5 percent) yields the voter-inclusive sector contrast reported in Section 4.6.2 (Cohen's d = 0.65, Mann-Whitney p = 0.028, mean-based permutation borderline at approximately 0.08). The earlier inconsistent-treatment exclusion dropped the DeFi-side pools outright while retaining one DePIN-side pool (Livepeer), the asymmetry that inflated the legacy large effect (Cohen's d = 1.05, reported as superseded, not the headline).

## Part 4: Reproduction and replication-package pointers

All numbers in this file reproduce from the persisted inputs in the replication repository linked in Section 5.9 (github.com/Research-Publications-and-Data/Tokenomics-As-Institutional_Design). Reproduction is deterministic, with no scratch-directory dependency and no live-API calls at reproduction time.

**One-command headline reproduction.** The reproduction script at the repository root regenerates the headline regression results from the raw top-1000 holder lists and the persisted covariate frame:

```
python reproduce.py
```

It reconciles, and this file has reproduced, the following load-bearing numbers:

- maturity-specification DePIN coefficient, log-HHI, p = 0.0107 (exact); same-signed and significant on the untransformed-HHI measure (coefficient +0.036, p = 0.019), so the sector result holds under both the log and the raw concentration measures;
- retention-specification DePIN coefficient under the evidence-traced classification of record, p = 0.0050 (exact);
- full-frame Mann-Whitney DePIN against DeFi reproduces directionally (the manuscript publishes no full-frame point p or d; significance on that frame is sensitive to the staking-aggregation treatment); the balanced-30 recompute at p = 0.0114, d = 1.048 is the superseded S10 Spec A specification (inconsistent staking-aggregation treatment), NOT the of-record headline. Relabel note (2026-07-10): the current headline is the voter-inclusive pass-through frame (MW p = 0.028, Cohen's d = 0.65), with the uniform staking-aggregation exclusion as robustness (p = 0.018, d = 0.75) per Section 4.6.2;
- insider-retention de-tautology on the established-protocol cohort, Spearman rho = 0.544 (the regressor remains not significant at the full sample, the channel-shift).

**Six-classification re-estimation harness.** The harness that re-estimates the retention specification under all six insider-classification schemes, producing the per-scheme DePIN p-values tabulated in Part 1.3, is persisted in the insider-reclassification subdirectory of the replication package, together with the six insider-retention vectors it reads.

**Persisted artifacts cited by this file.** The traced per-survivor classification spine (all ten survivors of every protocol, with rank, share, label, entity type, classification reason, and traced source), the insider-retention vector of record, the seventeen-Safe deployer-and-signer verdicts, the AAVE and ENA staking-attribution recomputation, and the Livepeer orchestrator-level bonded-stake table and HHI computation are all persisted in the insider-reclassification and staking-audit subdirectories of the replication package. The address-by-address exclusion methodology that produces the survivors is documented in Supplementary File S6; the empirical pipeline specification is in Supplementary File S5; the per-scheme classification robustness across the broader specification grid is in Supplementary Files S10 and S12.
