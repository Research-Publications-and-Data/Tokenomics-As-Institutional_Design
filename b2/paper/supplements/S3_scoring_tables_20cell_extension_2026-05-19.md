# S3 extension: per-criterion 20-cell scoring for 28 protocols (2026-05-19)

This file extends `S3_scoring_tables.md` with full per-criterion (20-cell) scoring for the 28 protocols added 2026-05-19. The 5-lens summary scoring in S3 is recomputed from these per-criterion scores; this file is the authoritative per-criterion record.

**Methodology:** NDOM-2 (concentration limit) follows the original 11 anchors' empirical convention (HHI less than 0.05 -> score 2 'partial' rather than the strict S2 rubric's 3 'exemplary'), reflecting that low holding HHI is consistent with but does not establish exemplary concentration limits absent voting-layer evidence (Section 3.5 documents universal delegation amplification). Other criteria are scored from web-verified governance evidence per the verification cycle 2026-05-19 (URLs, proposal-type names, multi-sig structures, voting-mechanism details cross-referenced against official docs).

**Single coder** (ZZ); **inter-rater reliability** deferred to future cycles per S2 reliability protocol. Evidence as of March to May 2026.

---

## Curve (DeFi, HHI 0.014)

**Verification sources:** resources.curve.finance/governance; docs.curve.finance

| Criterion | Score | Evidence |
|-----------|-------|----------|
| PUB-1 (Rule transparency) | 2 | Governance docs at resources.curve.finance/governance; veCRV mechanics fully documented; gauge weights public on-chain |
| PUB-2 (Proposal rationale) | 2 | On-chain veCRV proposals with rationale; 2,500 veCRV minimum to create proposal |
| PUB-3 (Enforcement transparency) | 2 | Emission gauges enforced on-chain via weekly veCRV votes |
| PUB-4 (Information symmetry) | 2 | Forum communications regular; informational parity moderate |
| FAIR-1 (Floor protection) | 1 | Minimum 1 CRV lock for governance participation; no protected floor beyond |
| FAIR-2 (Access equity) | 1 | veCRV lock duration (1 week to 4 years) economics complex for non-DeFi users |
| FAIR-3 (Distribution fairness) | 0 | 62% community allocation but veCRV lock-time-weighted voting structurally privileges long-lockers |
| FAIR-4 (Governance accessibility) | 1 | 2,500 veCRV proposal threshold; Convex aggregates voting power diluting small holders |
| NDOM-1 (Contestability) | 2 | On-chain governance veto via 30% quorum; emergency DAO multisig |
| NDOM-2 (Concentration limit) | 2 | Post-exclusion HHI 0.014 less than 0.05; anchor convention |
| NDOM-3 (Emergency powers) | 1 | Emergency DAO multisig retains pause powers; sunset unclear |
| NDOM-4 (Exit rights) | 0 | veCRV lock non-redeemable; effective exit only through secondary market (Convex liquid wrapper) |
| POLY-1 (Decision centers) | 2 | DAO + gauge system + sub-ecosystems (Convex meta-governance, Stake DAO sdCRV, yCRV) |
| POLY-2 (Local adaptation) | 2 | Per-pool gauge weights are local; emission curve global |
| POLY-3 (Cross-scale coordination) | 1 | Cross-ecosystem coordination via Convex bribery markets; informal |
| POLY-4 (Subsidiarity) | 1 | Subsidiarity weak; main DAO retains parameter authority |
| KNOW-1 (Price signals) | 3 | Multi-dimensional gauge votes weekly; emission price signals |
| KNOW-2 (Local knowledge) | 2 | Gauge votes aggregate dispersed holder demand preferences |
| KNOW-3 (Competitive discovery) | 2 | Open AMM competition with published TVL; permissionless pool creation |
| KNOW-4 (Information aggregation) | 1 | Convex vlCVX bribery market is implicit vote-prediction market |

**Lens means:** Publicity 2.00; Fairness 0.75; Non-Domination 1.25; Polycentricity 1.50; Knowledge-use 2.00.
**Synergy Index:** arithmetic mean 1.50; geometric mean 1.41.

---

## Rocket Pool (DeFi, HHI 0.039)

**Verification sources:** dao.rocketpool.net; rpips.rocketpool.net

| Criterion | Score | Evidence |
|-----------|-------|----------|
| PUB-1 (Rule transparency) | 3 | Comprehensive docs.rocketpool.net + RPIP repository; all parameters fully on-chain and versioned |
| PUB-2 (Proposal rationale) | 3 | RPIPs (Rocket Pool Improvement Proposals) include rationale and impact analysis; monthly pDAO treasury reports |
| PUB-3 (Enforcement transparency) | 2 | oDAO slashing rules published; sequencer enforcement documented |
| PUB-4 (Information symmetry) | 2 | Team communications regular via Discord and forum |
| FAIR-1 (Floor protection) | 2 | 16 ETH minipool floor; LEB8 (8 ETH) variant lowers entry |
| FAIR-2 (Access equity) | 2 | Node operator setup documented; technical bar moderate but well-documented |
| FAIR-3 (Distribution fairness) | 2 | Community LP distribution + node operator floor; no fixed operator concentration cap |
| FAIR-4 (Governance accessibility) | 0 | pDAO proposal threshold moderate; small-holder voice mostly via delegation |
| NDOM-1 (Contestability) | 3 | pDAO + oDAO bicameral + GMC (Grants Management Committee); RPIP-26 evidences GMC update process |
| NDOM-2 (Concentration limit) | 2 | Post-exclusion HHI 0.039 less than 0.05; anchor convention |
| NDOM-3 (Emergency powers) | 2 | Guardian multisig with timelock; protocol pause requires multisig plus delay |
| NDOM-4 (Exit rights) | 0 | Node operator stake locked while running; exit-fee structure penalizes early withdrawal |
| POLY-1 (Decision centers) | 3 | pDAO + oDAO + GMC + monthly treasury reports formalize tri-body structure |
| POLY-2 (Local adaptation) | 2 | Node operators self-elect commission tiers; minipool-level local choice |
| POLY-3 (Cross-scale coordination) | 2 | Cross-body coordination formal; oDAO can challenge pDAO via veto |
| POLY-4 (Subsidiarity) | 1 | Subsidiarity via minipool-level decisions; main parameters at pDAO |
| KNOW-1 (Price signals) | 1 | Fixed protocol fee; commission market at node-operator level only |
| KNOW-2 (Local knowledge) | 1 | Forum-based feedback; no automated parameter adjustment |
| KNOW-3 (Competitive discovery) | 2 | Open node operator entry; published performance metrics via rocketscan.io |
| KNOW-4 (Information aggregation) | 0 | No prediction markets or structured aggregation |

**Lens means:** Publicity 2.50; Fairness 1.50; Non-Domination 1.75; Polycentricity 2.00; Knowledge-use 1.00.
**Synergy Index:** arithmetic mean 1.75; geometric mean 1.67.

---

## Jupiter (DeFi, HHI 0.096)

**Verification sources:** docs.jup.ag; Coindesk + DLNews 2025 Jupiter pause coverage

| Criterion | Score | Evidence |
|-----------|-------|----------|
| PUB-1 (Rule transparency) | 2 | Documentation at jup.ag/docs; smart contract parameters documented |
| PUB-2 (Proposal rationale) | 1 | Governance paused June 2025; proposals previously carried rationale; pause itself a transparency event |
| PUB-3 (Enforcement transparency) | 1 | Limited enforcement transparency; no formal slashing |
| PUB-4 (Information symmetry) | 2 | Team communications via X regular; governance pause communicated transparently |
| FAIR-1 (Floor protection) | 1 | No formal floor; airdrop tier structure published; Jupuary distribution |
| FAIR-2 (Access equity) | 1 | Solana wallet entry; technical bar low; documentation primarily English |
| FAIR-3 (Distribution fairness) | 1 | LFG launchpad partial floor; allocation skewed insider |
| FAIR-4 (Governance accessibility) | 0 | Governance paused; working group elimination per October 2025 vote restricts small-holder representation |
| NDOM-1 (Contestability) | 1 | Governance was paused 2025 citing 'breakdown in trust'; resuming with delegated/council/hybrid model |
| NDOM-2 (Concentration limit) | 2 | Post-exclusion HHI 0.096 in 0.05 to 0.15 range; anchor convention |
| NDOM-3 (Emergency powers) | 1 | Team retains parameter controls during pause; sunset of pause = 2026 resume |
| NDOM-4 (Exit rights) | 1 | Token freely transferable; no formal exit-from-governance mechanism |
| POLY-1 (Decision centers) | 1 | JUP DAO + working groups (legacy); 2026 plans for councils / committees |
| POLY-2 (Local adaptation) | 1 | Limited local adaptation |
| POLY-3 (Cross-scale coordination) | 1 | Cross-working-group coordination informal; working group elimination underway |
| POLY-4 (Subsidiarity) | 1 | Most meaningful decisions at DAO level |
| KNOW-1 (Price signals) | 1 | Basic swap-fee mechanism; aggregator routing |
| KNOW-2 (Local knowledge) | 1 | Limited structured feedback |
| KNOW-3 (Competitive discovery) | 2 | Permissionless DEX aggregation |
| KNOW-4 (Information aggregation) | 0 | No prediction markets or structured aggregation |

**Lens means:** Publicity 1.50; Fairness 0.75; Non-Domination 1.25; Polycentricity 1.00; Knowledge-use 1.00.
**Synergy Index:** arithmetic mean 1.10; geometric mean 1.07.

---

## Maple Finance (DeFi, HHI 0.024)

**Verification sources:** maple.finance/insights/maple-dao-governance-process; community.maple.finance

| Criterion | Score | Evidence |
|-----------|-------|----------|
| PUB-1 (Rule transparency) | 2 | Documentation at maple.finance; pool parameters public; Discourse forum + Snapshot voting |
| PUB-2 (Proposal rationale) | 2 | MIP (Maple Improvement Proposal) template streamlines submission; standardized rationale required |
| PUB-3 (Enforcement transparency) | 2 | Pool delegate criteria public; default-handling documented; transparency thread on Discourse |
| PUB-4 (Information symmetry) | 1 | Team communications via Twitter; informational asymmetry moderate |
| FAIR-1 (Floor protection) | 1 | Pool minimum caps protect small lenders partially |
| FAIR-2 (Access equity) | 1 | Institutional-focused; non-institutional lender access varies by pool |
| FAIR-3 (Distribution fairness) | 1 | Mixed allocation; community + insider |
| FAIR-4 (Governance accessibility) | 1 | Proposal threshold accessible; SYRUP plus stSYRUP holders can vote |
| NDOM-1 (Contestability) | 2 | Governor Timelock Contract (Sept 2025 upgrade) + Snapshot + Discourse appeals |
| NDOM-2 (Concentration limit) | 2 | Post-exclusion HHI 0.024 less than 0.05; anchor convention |
| NDOM-3 (Emergency powers) | 2 | Governor Timelock for governance execution; security via multisig + delay |
| NDOM-4 (Exit rights) | 0 | Pool delegates can pause withdrawals; exit possible but with potential delay |
| POLY-1 (Decision centers) | 1 | Single DAO; pool delegates operational not governance authority |
| POLY-2 (Local adaptation) | 1 | Per-pool parameter governance limited |
| POLY-3 (Cross-scale coordination) | 1 | Pool delegates coordinate informally |
| POLY-4 (Subsidiarity) | 1 | Centralized governance |
| KNOW-1 (Price signals) | 1 | Pool interest rates set by pool delegate; not market-driven |
| KNOW-2 (Local knowledge) | 1 | Pool delegate performance metrics partial |
| KNOW-3 (Competitive discovery) | 1 | Limited pool-delegate competition |
| KNOW-4 (Information aggregation) | 1 | Governance voting as sole aggregation |

**Lens means:** Publicity 1.75; Fairness 1.00; Non-Domination 1.50; Polycentricity 1.00; Knowledge-use 1.00.
**Synergy Index:** arithmetic mean 1.25; geometric mean 1.21.

---

## GMX (DeFi, HHI 0.065)

**Verification sources:** gov.gmx.io; messari.io/project/gmx/governance

| Criterion | Score | Evidence |
|-----------|-------|----------|
| PUB-1 (Rule transparency) | 2 | Docs at gmxio.gitbook.io; protocol parameters fully public; V2 + V1 architectures documented |
| PUB-2 (Proposal rationale) | 2 | gov.gmx.io active proposals at /c/proposals/5 carry rationale |
| PUB-3 (Enforcement transparency) | 2 | GLP/GM rebalancing on-chain; liquidations transparent |
| PUB-4 (Information symmetry) | 2 | Open communication; team active in forum |
| FAIR-1 (Floor protection) | 1 | GLP redemption available (V1 legacy); GM redemption (V2) |
| FAIR-2 (Access equity) | 1 | Trader entry permissionless; LP entry requires GM/GLP minting |
| FAIR-3 (Distribution fairness) | 1 | esGMX vesting + GMX distribution mixed |
| FAIR-4 (Governance accessibility) | 1 | Proposal threshold moderate; delegation not promoted |
| NDOM-1 (Contestability) | 2 | gov.gmx.io Snapshot voting; informal appeals via forum |
| NDOM-2 (Concentration limit) | 2 | Post-exclusion HHI 0.065 in 0.05 to 0.15 range |
| NDOM-3 (Emergency powers) | 1 | Multisig retains emergency pause |
| NDOM-4 (Exit rights) | 1 | GLP/GM redemption available; GMX staking 30-day cooldown but exits possible |
| POLY-1 (Decision centers) | 1 | GMX DAO; V1 + V2 architecture but unified governance |
| POLY-2 (Local adaptation) | 1 | Per-market (V2) parameter local; emission schedule global |
| POLY-3 (Cross-scale coordination) | 1 | Cross-chain (Arbitrum + Avalanche) coordination informal |
| POLY-4 (Subsidiarity) | 1 | Centralized DAO governance |
| KNOW-1 (Price signals) | 2 | GLP dynamic pricing; Chainlink oracles; pool weights adjust |
| KNOW-2 (Local knowledge) | 2 | Position data informs liquidation parameters |
| KNOW-3 (Competitive discovery) | 1 | Limited competition for keeper roles |
| KNOW-4 (Information aggregation) | 1 | Governance voting as primary aggregation |

**Lens means:** Publicity 2.00; Fairness 1.00; Non-Domination 1.50; Polycentricity 1.00; Knowledge-use 1.50.
**Synergy Index:** arithmetic mean 1.40; geometric mean 1.35.

---

## Drift (DeFi, HHI 0.053)

**Verification sources:** drift.trade/governance; Drift DIP-10 + Foundation 2026 proposals

| Criterion | Score | Evidence |
|-----------|-------|----------|
| PUB-1 (Rule transparency) | 2 | Documentation at docs.drift.trade; multi-branch governance documented; protocol parameters on-chain |
| PUB-2 (Proposal rationale) | 2 | DIPs (Drift Improvement Proposals) with rationale; Realms + Futarchy DAO proposals |
| PUB-3 (Enforcement transparency) | 1 | Liquidation logic public; security council enforcement informal |
| PUB-4 (Information symmetry) | 2 | Team active in Discord; foundation communications regular |
| FAIR-1 (Floor protection) | 1 | No formal floor; insurance fund protects partial defaults |
| FAIR-2 (Access equity) | 1 | Solana wallet entry; documentation primarily English |
| FAIR-3 (Distribution fairness) | 1 | Mixed allocation |
| FAIR-4 (Governance accessibility) | 1 | Realms voting open; Futarchy DAO requires market participation |
| NDOM-1 (Contestability) | 2 | Three-branch contestability: Realms + Security Council + Futarchy DAO; DIP-10 community challenge demonstrated |
| NDOM-2 (Concentration limit) | 2 | Post-exclusion HHI 0.053 in 0.05 to 0.15 range |
| NDOM-3 (Emergency powers) | 1 | Security Council emergency powers; April 2026 exploit + DIP-10 recovery as governance stress test |
| NDOM-4 (Exit rights) | 1 | Position close + cooldown; no formal governance-exit |
| POLY-1 (Decision centers) | 3 | Three-branch DAO: Realms (general) + Security Council (upgrades) + Futarchy DAO (grants via MetaDAOProject) |
| POLY-2 (Local adaptation) | 1 | Per-market parameter governance limited |
| POLY-3 (Cross-scale coordination) | 2 | Cross-branch coordination via Foundation + Security Council elected by Realms |
| POLY-4 (Subsidiarity) | 1 | Subsidiarity weak; main parameters at Realms |
| KNOW-1 (Price signals) | 1 | Basic fee mechanism; dynamic only for liquidations |
| KNOW-2 (Local knowledge) | 1 | Limited structured feedback |
| KNOW-3 (Competitive discovery) | 2 | Permissionless DEX with published performance |
| KNOW-4 (Information aggregation) | 2 | Futarchy DAO branch is structured prediction market aggregation for grants |

**Lens means:** Publicity 1.75; Fairness 1.00; Non-Domination 1.50; Polycentricity 1.75; Knowledge-use 1.50.
**Synergy Index:** arithmetic mean 1.50; geometric mean 1.47.

---

## Ether.Fi (DeFi, HHI 0.042)

**Verification sources:** governance.ether.fi; etherfi.gitbook.io/gov

| Criterion | Score | Evidence |
|-----------|-------|----------|
| PUB-1 (Rule transparency) | 2 | Documentation at etherfi.gitbook.io; ETHFI DAO governance docs public |
| PUB-2 (Proposal rationale) | 2 | Numbered DAO proposals (#1, #3, #6, #8, #9) at governance.ether.fi with rationale + impact analysis |
| PUB-3 (Enforcement transparency) | 1 | Limited enforcement transparency |
| PUB-4 (Information symmetry) | 2 | Team communications regular via Twitter and forum |
| FAIR-1 (Floor protection) | 1 | No formal floor; minimum stake low |
| FAIR-2 (Access equity) | 1 | Restaking participation accessible; technical bar moderate |
| FAIR-3 (Distribution fairness) | 1 | Mixed allocation; community + insider |
| FAIR-4 (Governance accessibility) | 1 | Proposal threshold accessible; ETHFI staker rewards (5% protocol revenue) |
| NDOM-1 (Contestability) | 1 | Basic voting via ETHFI DAO |
| NDOM-2 (Concentration limit) | 2 | Post-exclusion HHI 0.042 less than 0.05; anchor convention |
| NDOM-3 (Emergency powers) | 1 | Foundation retains operational authority over $50M buyback program |
| NDOM-4 (Exit rights) | 0 | Restaked ETH unstaking delay; no formal governance-exit mechanism |
| POLY-1 (Decision centers) | 1 | ETHFI DAO + Foundation + operator; mostly monocentric |
| POLY-2 (Local adaptation) | 1 | Per-validator parameter governance limited |
| POLY-3 (Cross-scale coordination) | 1 | Operator coordination informal |
| POLY-4 (Subsidiarity) | 1 | Centralized governance |
| KNOW-1 (Price signals) | 1 | Basic restaking yield mechanism |
| KNOW-2 (Local knowledge) | 1 | Limited structured feedback |
| KNOW-3 (Competitive discovery) | 1 | Limited operator competition |
| KNOW-4 (Information aggregation) | 1 | Governance voting as sole aggregation |

**Lens means:** Publicity 1.75; Fairness 1.00; Non-Domination 1.00; Polycentricity 1.00; Knowledge-use 1.00.
**Synergy Index:** arithmetic mean 1.15; geometric mean 1.12.

---

## The Graph (L1_L2_Infra, HHI 0.033)

**Verification sources:** thegraph.com/governance; github.com/graphprotocol/graph-improvement-proposals

| Criterion | Score | Evidence |
|-----------|-------|----------|
| PUB-1 (Rule transparency) | 3 | GIPs at github.com/graphprotocol/graph-improvement-proposals; parameters fully versioned; GIP-0001 documents process |
| PUB-2 (Proposal rationale) | 3 | GIPs require rationale + impact analysis + community discussion + arbitration charter (GIP-0009) |
| PUB-3 (Enforcement transparency) | 2 | Curator/indexer slashing on-chain; arbitration charter for disputes |
| PUB-4 (Information symmetry) | 1 | Foundation communications regular; some informational asymmetry on roadmap |
| FAIR-1 (Floor protection) | 2 | Indexer minimum stake floor; curator signal-rebate mechanism |
| FAIR-2 (Access equity) | 1 | Indexer setup requires GRT plus infrastructure; technical bar high |
| FAIR-3 (Distribution fairness) | 2 | Curator + delegator + indexer + initial team multi-role distribution |
| FAIR-4 (Governance accessibility) | 1 | Proposal threshold moderate; Council representation indirect |
| NDOM-1 (Contestability) | 2 | GIP appeals via Council + arbitration charter; community-led GIP-0061 updated process |
| NDOM-2 (Concentration limit) | 2 | Post-exclusion HHI 0.033 less than 0.05; anchor convention |
| NDOM-3 (Emergency powers) | 2 | Graph Council 6-of-10 multisig with documented stakeholder representation |
| NDOM-4 (Exit rights) | 1 | Indexer 28-day unstake; delegator immediate; effective exit possible |
| POLY-1 (Decision centers) | 3 | 5 stakeholder groups represented through Graph Council: Indexers, token holders, initial team, users, technical domain experts |
| POLY-2 (Local adaptation) | 2 | Per-subgraph curator signaling; per-indexer commission tiers |
| POLY-3 (Cross-scale coordination) | 2 | Cross-stakeholder coordination via Graph Council 6-of-10 multisig |
| POLY-4 (Subsidiarity) | 1 | Subsidiarity moderate; subgraph-level decisions local |
| KNOW-1 (Price signals) | 3 | Query-fee market signals; dynamic pricing per indexer; curator signaling |
| KNOW-2 (Local knowledge) | 2 | Curator signaling reveals subgraph demand |
| KNOW-3 (Competitive discovery) | 1 | Indexer competition moderate; high entry barrier |
| KNOW-4 (Information aggregation) | 0 | No prediction markets |

**Lens means:** Publicity 2.25; Fairness 1.50; Non-Domination 1.75; Polycentricity 2.00; Knowledge-use 1.50.
**Synergy Index:** arithmetic mean 1.80; geometric mean 1.78.

---

## Polygon (L1_L2_Infra, HHI 0.035)

**Verification sources:** github.com/maticnetwork/Polygon-Improvement-Proposals; governance.polygon.technology

| Criterion | Score | Evidence |
|-----------|-------|----------|
| PUB-1 (Rule transparency) | 2 | PIPs at github.com/maticnetwork/Polygon-Improvement-Proposals; parameters versioned |
| PUB-2 (Proposal rationale) | 3 | PIPs require rationale + impact; Q1 2026 was most proposal-intensive quarter with 9 proposals across two governance calls |
| PUB-3 (Enforcement transparency) | 2 | Validator slashing on-chain; PIP-78 checkpoint reward adjustments transparent |
| PUB-4 (Information symmetry) | 2 | Foundation communications regular |
| FAIR-1 (Floor protection) | 2 | 1M MATIC validator stake floor; clear minimum requirement |
| FAIR-2 (Access equity) | 1 | Validator setup requires substantial capital and infrastructure |
| FAIR-3 (Distribution fairness) | 1 | Community allocation moderate; insider allocation significant |
| FAIR-4 (Governance accessibility) | 1 | PIP-50 introduces staker signaling framework; small-holder voice via delegate-to-validator |
| NDOM-1 (Contestability) | 2 | Foundation veto + community PIPs + PIP-50 three-stage staker signaling |
| NDOM-2 (Concentration limit) | 2 | Post-exclusion HHI 0.035 less than 0.05; anchor convention |
| NDOM-3 (Emergency powers) | 2 | 13-member Protocol Council multi-sig (PIP-77 refreshed composition) supervises smart contract upgrades |
| NDOM-4 (Exit rights) | 1 | Validator unbonding 80-epoch (~80 minutes); delegator similar |
| POLY-1 (Decision centers) | 2 | PoS chain + zkEVM + AggLayer + Foundation tri-stakeholder; PIP-77 Protocol Council multi-sig |
| POLY-2 (Local adaptation) | 1 | Cross-chain (PoS + zkEVM) parameter divergence limited |
| POLY-3 (Cross-scale coordination) | 2 | Cross-chain coordination via shared validators; AggLayer roadmap formalizes this |
| POLY-4 (Subsidiarity) | 1 | Subsidiarity weak; foundation retains key parameters |
| KNOW-1 (Price signals) | 1 | Gas-fee market dynamic |
| KNOW-2 (Local knowledge) | 1 | Validator behavior informs parameter adjustments; PIP-85 performance-adjusted distribution |
| KNOW-3 (Competitive discovery) | 1 | Validator role competitive but high entry barrier |
| KNOW-4 (Information aggregation) | 1 | Governance voting as sole aggregation |

**Lens means:** Publicity 2.25; Fairness 1.25; Non-Domination 1.75; Polycentricity 1.50; Knowledge-use 1.00.
**Synergy Index:** arithmetic mean 1.55; geometric mean 1.49.

---

## Hyperliquid (DeFi, HHI 0.005)

**Verification sources:** hyperliquid.gitbook.io/hyperliquid-docs/hyperliquid-improvement-proposals-hips; validator vote coverage 2026

| Criterion | Score | Evidence |
|-----------|-------|----------|
| PUB-1 (Rule transparency) | 3 | All protocol parameters on-chain and queryable; HIPs (Hyperliquid Improvement Proposals) at gitbook |
| PUB-2 (Proposal rationale) | 2 | Hyper Foundation publishes HIP proposals; Q1 2026 validator vote on $1B Assistance Fund sideline |
| PUB-3 (Enforcement transparency) | 2 | Liquidation parameters fully public; auction mechanism transparent |
| PUB-4 (Information symmetry) | 1 | Foundation retains operational discretion; team communications via X mostly |
| FAIR-1 (Floor protection) | 1 | No formal protected floor; broad airdrop served as initial floor |
| FAIR-2 (Access equity) | 1 | Trading entry permissionless; provider entry requires capital |
| FAIR-3 (Distribution fairness) | 1 | 31% broad airdrop; foundation retains substantial allocation |
| FAIR-4 (Governance accessibility) | 1 | Validator vote (not token-holder vote) for governance proposals; HYPE holders cannot directly propose |
| NDOM-1 (Contestability) | 2 | Validator vote mechanism (Hyper Foundation initiates HIPs); 2026 $1B Assistance Fund sideline as governance stress test |
| NDOM-2 (Concentration limit) | 2 | Post-exclusion HHI 0.005 strongly less than 0.05; anchor convention |
| NDOM-3 (Emergency powers) | 1 | Foundation retains operational powers; informal constraints |
| NDOM-4 (Exit rights) | 1 | Trader exit immediate via close; token transfer permissionless |
| POLY-1 (Decision centers) | 0 | Foundation-led monocentric; no formal sub-bodies |
| POLY-2 (Local adaptation) | 0 | No local adaptation mechanism |
| POLY-3 (Cross-scale coordination) | 0 | No cross-scale coordination |
| POLY-4 (Subsidiarity) | 0 | All decisions at foundation/validator level |
| KNOW-1 (Price signals) | 3 | Assistance Fund auto-burns 99% of fees; price-signal-coupled HLP redistribution; $1.7M weekly buybacks Jan 2026 |
| KNOW-2 (Local knowledge) | 2 | Trader position data informs HLP rebalancing |
| KNOW-3 (Competitive discovery) | 2 | Permissionless market-maker entry; performance metrics public |
| KNOW-4 (Information aggregation) | 1 | HLP profitability signals but not codified as prediction market |

**Lens means:** Publicity 2.00; Fairness 1.00; Non-Domination 1.50; Polycentricity 0.00; Knowledge-use 2.00.
**Synergy Index:** arithmetic mean 1.30; geometric mean 0.57.

---

## Balancer (DeFi, HHI 0.029)

**Verification sources:** docs.balancer.fi/concepts/governance/process; forum.balancer.fi; bips.dev

| Criterion | Score | Evidence |
|-----------|-------|----------|
| PUB-1 (Rule transparency) | 2 | Documentation at docs.balancer.fi; protocol parameters fully public; BIP-163 defines governance process |
| PUB-2 (Proposal rationale) | 2 | BIP process at forum.balancer.fi requires rationale; bips.dev archives BIPs (BIP-262 L2 Gauge Migration, BIP-877 Kill Stale Gauges) |
| PUB-3 (Enforcement transparency) | 2 | Gauge cap rules published; Balancer Maxis multisig procedures documented |
| PUB-4 (Information symmetry) | 2 | Team communications regular; informational parity moderate |
| FAIR-1 (Floor protection) | 1 | veBAL lock-time-weighted (max 1 year); small holders disadvantaged |
| FAIR-2 (Access equity) | 1 | veBAL lock requires 80/20 BAL/WETH BPT; technical bar moderate |
| FAIR-3 (Distribution fairness) | 1 | Mixed allocation; veBAL lockers privileged over BAL holders |
| FAIR-4 (Governance accessibility) | 1 | Proposal threshold moderate; delegation via veBAL |
| NDOM-1 (Contestability) | 2 | BIP process + Snapshot + veBAL voting; informal appeals via forum |
| NDOM-2 (Concentration limit) | 2 | Post-exclusion HHI 0.029 less than 0.05; anchor convention |
| NDOM-3 (Emergency powers) | 1 | Balancer Maxis multisig retains pause powers; emergency framework via multisig |
| NDOM-4 (Exit rights) | 1 | veBAL non-redeemable lock (1-year max); secondary market via Aura/Hidden Hand |
| POLY-1 (Decision centers) | 2 | Balancer Maxis multisig + DAO + veBAL holders; tri-body operational structure |
| POLY-2 (Local adaptation) | 1 | Per-pool gauge weights are local; emission schedule global |
| POLY-3 (Cross-scale coordination) | 1 | Cross-body coordination informal |
| POLY-4 (Subsidiarity) | 2 | Subsidiarity via gauge-level weight setting |
| KNOW-1 (Price signals) | 3 | Gauge votes weekly determine liquidity emission allocation; explicit Hayek mechanism |
| KNOW-2 (Local knowledge) | 2 | Per-gauge votes reveal LP-level demand |
| KNOW-3 (Competitive discovery) | 2 | Open AMM competition; pool-creator permissionless |
| KNOW-4 (Information aggregation) | 1 | Hidden Hand vote-marketplace is implicit prediction market |

**Lens means:** Publicity 2.00; Fairness 1.00; Non-Domination 1.50; Polycentricity 1.50; Knowledge-use 2.00.
**Synergy Index:** arithmetic mean 1.60; geometric mean 1.55.

---

## IoTeX (DePIN, HHI 0.189)

**Verification sources:** docs.iotex.io/participate/governance/iotex-improvement-proposals; github.com/iotexproject/iips

| Criterion | Score | Evidence |
|-----------|-------|----------|
| PUB-1 (Rule transparency) | 2 | Documentation at docs.iotex.io; IIPs at github.com/iotexproject/iips; protocol parameters versioned |
| PUB-2 (Proposal rationale) | 2 | IIPs require rationale; IIP-50 slashing underperforming delegates as recent example |
| PUB-3 (Enforcement transparency) | 2 | Delegate slashing rules published; IIP-50 codifies enforcement |
| PUB-4 (Information symmetry) | 1 | Team communications via Twitter; some informational asymmetry |
| FAIR-1 (Floor protection) | 1 | Validator staking floor present; rotation excludes smaller validators |
| FAIR-2 (Access equity) | 1 | Delegate setup requires substantial IOTX plus infrastructure |
| FAIR-3 (Distribution fairness) | 1 | Community allocation moderate; insider allocation significant |
| FAIR-4 (Governance accessibility) | 0 | Only Delegates can create proposals (significant restriction); IOTX stakers can vote but not propose |
| NDOM-1 (Contestability) | 1 | Delegate-only proposal creation; basic voting |
| NDOM-2 (Concentration limit) | 1 | Post-exclusion HHI 0.189 in 0.15 to 0.25 range (high concentration) |
| NDOM-3 (Emergency powers) | 1 | Foundation retains protocol-upgrade authority; informal constraints |
| NDOM-4 (Exit rights) | 1 | IOTX staking has cooldown; transfer permissionless |
| POLY-1 (Decision centers) | 2 | Delegate-DAO + foundation + IoTeX Hub (April 2026 unified interface) |
| POLY-2 (Local adaptation) | 1 | Per-machine parameter governance limited |
| POLY-3 (Cross-scale coordination) | 2 | Foundation coordinates between DePIN layer and L1 |
| POLY-4 (Subsidiarity) | 1 | Subsidiarity moderate |
| KNOW-1 (Price signals) | 2 | Dapp gas fee mechanism dynamic |
| KNOW-2 (Local knowledge) | 2 | Machine data signals (DePIN-specific) inform parameters |
| KNOW-3 (Competitive discovery) | 1 | Delegate competition limited (delegate-only proposal creation) |
| KNOW-4 (Information aggregation) | 1 | Governance voting via Snapshot as sole aggregation |

**Lens means:** Publicity 1.75; Fairness 0.75; Non-Domination 1.00; Polycentricity 1.50; Knowledge-use 1.50.
**Synergy Index:** arithmetic mean 1.30; geometric mean 1.24.

---

## WeatherXM (DePIN, HHI 0.148)

**Verification sources:** github.com/orgs/weatherxm-network/discussions (WIP-004)

| Criterion | Score | Evidence |
|-----------|-------|----------|
| PUB-1 (Rule transparency) | 2 | Documentation at docs.weatherxm.com; station and data parameters public |
| PUB-2 (Proposal rationale) | 2 | WIPs (WeatherXM Improvement Proposals) carry rationale; WIP-004 introduces SPV multiplier |
| PUB-3 (Enforcement transparency) | 1 | Station banning criteria informal; enforcement via Quality-of-Data score |
| PUB-4 (Information symmetry) | 1 | Team communications via Twitter and Discord |
| FAIR-1 (Floor protection) | 1 | Per-station reward floor minimal; QoD-weighted |
| FAIR-2 (Access equity) | 1 | Station deployment cost moderate; geographic constraints |
| FAIR-3 (Distribution fairness) | 1 | Community allocation moderate; team allocation significant |
| FAIR-4 (Governance accessibility) | 1 | WIP voting open via WXM token; Association General Assembly governs SPV parameters |
| NDOM-1 (Contestability) | 1 | WIP voting + Association General Assembly; appeals via WIP-004 SPV resubmission |
| NDOM-2 (Concentration limit) | 2 | Post-exclusion HHI 0.148 at upper boundary of 0.05 to 0.15 range; anchor convention |
| NDOM-3 (Emergency powers) | 1 | Foundation retains operational authority |
| NDOM-4 (Exit rights) | 1 | Station decommissioning permissionless; token transfer free |
| POLY-1 (Decision centers) | 1 | Foundation + Association General Assembly; informal regional clusters |
| POLY-2 (Local adaptation) | 2 | Location-based reward weighting; QoD-adjusted local rewards |
| POLY-3 (Cross-scale coordination) | 1 | No formal cross-region coordination |
| POLY-4 (Subsidiarity) | 1 | Centralized governance |
| KNOW-1 (Price signals) | 2 | Location-based reward weighting; quality-based rewards |
| KNOW-2 (Local knowledge) | 3 | Weather data quality signals + SPV photo verification directly into reward calculation |
| KNOW-3 (Competitive discovery) | 2 | Station competition local; entry permissionless |
| KNOW-4 (Information aggregation) | 1 | Governance voting as aggregation channel |

**Lens means:** Publicity 1.50; Fairness 1.00; Non-Domination 1.25; Polycentricity 1.25; Knowledge-use 2.00.
**Synergy Index:** arithmetic mean 1.40; geometric mean 1.36.

---

## Grass (DePIN, HHI 0.035)

**Verification sources:** solanacompass.com/projects/grass (Solana DePIN listing)

| Criterion | Score | Evidence |
|-----------|-------|----------|
| PUB-1 (Rule transparency) | 2 | Documentation at docs.getgrass.io; token allocation 30% community |
| PUB-2 (Proposal rationale) | 1 | Governance forum proposals; rationale variable |
| PUB-3 (Enforcement transparency) | 1 | Limited enforcement transparency |
| PUB-4 (Information symmetry) | 2 | Team communications via Twitter and Discord |
| FAIR-1 (Floor protection) | 1 | Per-user bandwidth reward minimal |
| FAIR-2 (Access equity) | 1 | Browser-extension entry low barrier; geographic constraints |
| FAIR-3 (Distribution fairness) | 1 | Mixed allocation; community 30% (170M tokens incentives + 30M router + 100M initial airdrop) |
| FAIR-4 (Governance accessibility) | 1 | Proposal threshold accessible |
| NDOM-1 (Contestability) | 1 | Basic voting; roadmap targets decentralized validator committee with autonomous slashing H1 2026 |
| NDOM-2 (Concentration limit) | 2 | Post-exclusion HHI 0.035 less than 0.05; anchor convention |
| NDOM-3 (Emergency powers) | 1 | Foundation retains operational authority |
| NDOM-4 (Exit rights) | 1 | User exit immediate; token transfer free |
| POLY-1 (Decision centers) | 1 | Foundation-led; no formal sub-bodies; account-abstraction wallet H1 2026 |
| POLY-2 (Local adaptation) | 0 | No local adaptation |
| POLY-3 (Cross-scale coordination) | 0 | No cross-scale coordination |
| POLY-4 (Subsidiarity) | 1 | Centralized governance |
| KNOW-1 (Price signals) | 2 | Bandwidth quality signals |
| KNOW-2 (Local knowledge) | 2 | User bandwidth data informs AI training datasets |
| KNOW-3 (Competitive discovery) | 1 | Limited operator competition |
| KNOW-4 (Information aggregation) | 1 | Governance voting as aggregation |

**Lens means:** Publicity 1.50; Fairness 1.00; Non-Domination 1.25; Polycentricity 0.50; Knowledge-use 1.50.
**Synergy Index:** arithmetic mean 1.15; geometric mean 1.07.

---

## Livepeer (DePIN, HHI 0.199)

**Verification sources:** github.com/livepeer/LIPs; github.com/livepeer/community-governance/LIP-Meetings

| Criterion | Score | Evidence |
|-----------|-------|----------|
| PUB-1 (Rule transparency) | 2 | Documentation at docs.livepeer.org; LIPs at github.com/livepeer/LIPs |
| PUB-2 (Proposal rationale) | 2 | LIPs (Livepeer Improvement Proposals) require rationale; LIP-73 + LIP-Meeting governance archive |
| PUB-3 (Enforcement transparency) | 1 | Orchestrator slashing rules public; enforcement variable |
| PUB-4 (Information symmetry) | 1 | Team communications via Discord; informational asymmetry moderate |
| FAIR-1 (Floor protection) | 1 | 1 LPT orchestrator minimum stake; effective floor low |
| FAIR-2 (Access equity) | 1 | Orchestrator setup requires GPU + LPT; technical bar moderate |
| FAIR-3 (Distribution fairness) | 1 | Community allocation moderate |
| FAIR-4 (Governance accessibility) | 1 | Proposal threshold accessible; delegation widely used |
| NDOM-1 (Contestability) | 1 | Basic voting via LIP; informal appeals |
| NDOM-2 (Concentration limit) | 1 | Post-exclusion HHI 0.199 in 0.15 to 0.25 range (high concentration) |
| NDOM-3 (Emergency powers) | 1 | Foundation retains protocol-upgrade authority |
| NDOM-4 (Exit rights) | 1 | LPT unbonding 7-round delay; delegator immediate |
| POLY-1 (Decision centers) | 1 | Orchestrator-delegator structure; no formal sub-DAOs; Q1 2026 Base rollup migration |
| POLY-2 (Local adaptation) | 1 | Per-orchestrator commission tier setting |
| POLY-3 (Cross-scale coordination) | 1 | Cross-orchestrator coordination informal |
| POLY-4 (Subsidiarity) | 1 | Centralized governance |
| KNOW-1 (Price signals) | 3 | Encoding job pricing dynamic; per-segment payment; real-time AI pipelines |
| KNOW-2 (Local knowledge) | 2 | Encoding job demand signals into bond reward distribution |
| KNOW-3 (Competitive discovery) | 2 | Open orchestrator competition; published performance metrics |
| KNOW-4 (Information aggregation) | 1 | Bond market is implicit prediction market on orchestrator quality |

**Lens means:** Publicity 1.50; Fairness 1.00; Non-Domination 1.00; Polycentricity 1.00; Knowledge-use 2.00.
**Synergy Index:** arithmetic mean 1.30; geometric mean 1.25.

---

## Filecoin (DePIN, HHI 0.022)

**Verification sources:** github.com/filecoin-project/FIPs; fil.org/governance; Filecoin Community Guild FIP0001v2

| Criterion | Score | Evidence |
|-----------|-------|----------|
| PUB-1 (Rule transparency) | 3 | Comprehensive FIPs at github.com/filecoin-project/FIPs; FIP0001v2 process proposal; parameters versioned |
| PUB-2 (Proposal rationale) | 3 | FIPs require rationale + impact analysis + Filecoin Request for Comments (FRC) community period |
| PUB-3 (Enforcement transparency) | 2 | Storage provider slashing via cryptographic proofs (PoSt/PoRep); enforcement consistent on-chain |
| PUB-4 (Information symmetry) | 2 | FIP discussion community-driven; informational parity moderate |
| FAIR-1 (Floor protection) | 1 | Storage provider initial collateral requirement substantial |
| FAIR-2 (Access equity) | 1 | Storage provider setup requires hardware + collateral + technical expertise |
| FAIR-3 (Distribution fairness) | 2 | Community allocation substantial; storage provider distribution broad |
| FAIR-4 (Governance accessibility) | 1 | FIP proposal threshold via FRC moderate; delegation not formalized |
| NDOM-1 (Contestability) | 3 | FIP appeals + Filecoin Foundation oversight + 7-seat Community Guild (6 stakeholder groups: Token Holders, Storage Providers, Clients, Developers, Ecosystem Partners, Protocol Labs + Filecoin Foundation) |
| NDOM-2 (Concentration limit) | 2 | Post-exclusion HHI 0.022 less than 0.05; anchor convention |
| NDOM-3 (Emergency powers) | 2 | Foundation multisig with FIP-approval timelock; Constellation Program modernizing governance |
| NDOM-4 (Exit rights) | 1 | Storage provider sector termination with penalty; client retrieval immediate |
| POLY-1 (Decision centers) | 3 | FIL Foundation + Protocol Labs + storage providers + clients + developers + ecosystem partners six-stakeholder Community Guild |
| POLY-2 (Local adaptation) | 3 | Per-sector + per-region storage parameters; retrieval markets local |
| POLY-3 (Cross-scale coordination) | 3 | Cross-body coordination via FIP process and FRC consultation; FDS-7 Constellation Program |
| POLY-4 (Subsidiarity) | 1 | Subsidiarity moderate; FIP retains protocol-level changes |
| KNOW-1 (Price signals) | 3 | Storage market dynamic pricing; retrieval market pricing; per-sector parameters |
| KNOW-2 (Local knowledge) | 2 | Storage provider performance data informs reward calculation; veFIL early 2026 FIP under discussion |
| KNOW-3 (Competitive discovery) | 2 | Open storage provider entry; published performance metrics via Filfox/Filscan |
| KNOW-4 (Information aggregation) | 1 | FRC informal aggregation; no formal prediction markets |

**Lens means:** Publicity 2.50; Fairness 1.25; Non-Domination 2.00; Polycentricity 2.50; Knowledge-use 2.00.
**Synergy Index:** arithmetic mean 2.05; geometric mean 1.99.

---

## Render (DePIN, HHI 0.027)

**Verification sources:** know.rendernetwork.com/about-render-network-governance/render-network-proposal-rnp-system; rndr.gitbook.io

| Criterion | Score | Evidence |
|-----------|-------|----------|
| PUB-1 (Rule transparency) | 2 | Documentation at know.rendernetwork.com; Render Foundation governance docs |
| PUB-2 (Proposal rationale) | 2 | RNPs (Render Network Proposals) require rationale; RNP-023 Salad Network Subnet approval April 2026 |
| PUB-3 (Enforcement transparency) | 1 | Operator dispute resolution informal |
| PUB-4 (Information symmetry) | 1 | Team communications via Twitter |
| FAIR-1 (Floor protection) | 1 | Per-job operator reward minimal floor |
| FAIR-2 (Access equity) | 1 | Operator setup requires GPU + RENDER stake; technical bar moderate |
| FAIR-3 (Distribution fairness) | 1 | Community allocation moderate; insider allocation significant |
| FAIR-4 (Governance accessibility) | 1 | Proposal threshold accessible; RENDER holders vote via Snapshot on Solana |
| NDOM-1 (Contestability) | 1 | Basic RNP voting; informal appeals |
| NDOM-2 (Concentration limit) | 2 | Post-exclusion HHI 0.027 less than 0.05; anchor convention |
| NDOM-3 (Emergency powers) | 1 | Foundation retains operational authority |
| NDOM-4 (Exit rights) | 1 | Operator opt-out permissionless |
| POLY-1 (Decision centers) | 1 | Render Network Foundation; no formal sub-bodies |
| POLY-2 (Local adaptation) | 1 | Per-job parameter governance limited |
| POLY-3 (Cross-scale coordination) | 1 | Cross-subnet coordination via RNP (e.g., RNP-023 Salad Network adds ~60K GPUs) |
| POLY-4 (Subsidiarity) | 1 | Centralized governance |
| KNOW-1 (Price signals) | 2 | GPU job dynamic pricing; per-job tier |
| KNOW-2 (Local knowledge) | 2 | Operator performance metrics into reward; H100/H200/A100/MI300 enterprise-grade expansion |
| KNOW-3 (Competitive discovery) | 2 | Permissionless operator entry |
| KNOW-4 (Information aggregation) | 0 | No prediction markets |

**Lens means:** Publicity 1.50; Fairness 1.00; Non-Domination 1.25; Polycentricity 1.00; Knowledge-use 1.50.
**Synergy Index:** arithmetic mean 1.25; geometric mean 1.23.

---

## Pokt Network (DePIN, HHI 0.090)

**Verification sources:** gov.pokt.network; forum.pokt.network/c/proposals/9; github.com/pokt-network/governance

| Criterion | Score | Evidence |
|-----------|-------|----------|
| PUB-1 (Rule transparency) | 3 | Constitution at github.com/pokt-network/governance; PIP/PEP/PUP triple proposal type structure documented; gov.pokt.network |
| PUB-2 (Proposal rationale) | 2 | PUPs (Parameter Update), PIPs (Pocket Improvement), PEPs require rationale; PIP-41 Shannon tokenomics (Jan 2026, 97.5% mint ratio) |
| PUB-3 (Enforcement transparency) | 2 | Node operator slashing rules public; enforcement consistent on-chain |
| PUB-4 (Information symmetry) | 2 | Foundation communications regular via forum |
| FAIR-1 (Floor protection) | 1 | Node staking minimum 15K POKT; floor moderate |
| FAIR-2 (Access equity) | 1 | Node setup requires POKT + infrastructure; technical bar moderate |
| FAIR-3 (Distribution fairness) | 1 | Community allocation moderate |
| FAIR-4 (Governance accessibility) | 1 | Proposal threshold via PUP accessible; POKTDAO off-chain voting open to POKT holders |
| NDOM-1 (Contestability) | 2 | PUP/PIP/PEP voting + DAO + Constitution; 7-day voting period + majority approval requirement |
| NDOM-2 (Concentration limit) | 2 | Post-exclusion HHI 0.090 in 0.05 to 0.15 range |
| NDOM-3 (Emergency powers) | 1 | Foundation retains protocol-upgrade authority |
| NDOM-4 (Exit rights) | 1 | Node unbonding 21-block delay |
| POLY-1 (Decision centers) | 2 | POKTDAO + node operators + portal partners + Foundation tri-stakeholder structure |
| POLY-2 (Local adaptation) | 1 | Per-chain relay parameter governance limited |
| POLY-3 (Cross-scale coordination) | 2 | Portal-partner coordination via DAO; Constitution formalizes |
| POLY-4 (Subsidiarity) | 1 | Subsidiarity moderate |
| KNOW-1 (Price signals) | 2 | Relay-volume pricing; per-chain rates |
| KNOW-2 (Local knowledge) | 2 | Relay-volume signals into reward calculation |
| KNOW-3 (Competitive discovery) | 1 | Node operator competition limited |
| KNOW-4 (Information aggregation) | 1 | Governance voting as aggregation |

**Lens means:** Publicity 2.25; Fairness 1.00; Non-Domination 1.50; Polycentricity 1.50; Knowledge-use 1.50.
**Synergy Index:** arithmetic mean 1.55; geometric mean 1.50.

---

## LayerZero (L1_L2_Infra, HHI 0.014)

**Verification sources:** info.layerzero.foundation; eco.com/support/en/articles/13714024-layerzero-architecture-and-zro-2026-guide

| Criterion | Score | Evidence |
|-----------|-------|----------|
| PUB-1 (Rule transparency) | 2 | Documentation at docs.layerzero.network; DVN configuration public; 50+ DVNs as of April 2026 |
| PUB-2 (Proposal rationale) | 2 | Protocol Fee-Switch Governance Vote every 6 months; April 2026 1-of-1 DVN config deprecation forced via governance |
| PUB-3 (Enforcement transparency) | 2 | DVN slashing rules public; enforcement via fee-switch and migration mandates |
| PUB-4 (Information symmetry) | 1 | Team communications via Twitter; informational asymmetry on Zero L1 roadmap (fall 2026) |
| FAIR-1 (Floor protection) | 1 | No formal floor; DVN selection by application choice |
| FAIR-2 (Access equity) | 1 | DVN operator setup requires infrastructure + reputation |
| FAIR-3 (Distribution fairness) | 1 | Mixed allocation; insider allocation significant |
| FAIR-4 (Governance accessibility) | 1 | ZRO holders vote on protocol parameters; voting is autonomous, on-chain, immutable |
| NDOM-1 (Contestability) | 2 | Semiannual fee-switch governance + ZRO holder votes; April 2026 1-of-1 DVN deprecation as governance enforcement |
| NDOM-2 (Concentration limit) | 2 | Post-exclusion HHI 0.014 less than 0.05; anchor convention |
| NDOM-3 (Emergency powers) | 1 | LayerZero Labs retains operational authority; Zero L1 launch planned fall 2026 |
| NDOM-4 (Exit rights) | 1 | DVN opt-out permissionless |
| POLY-1 (Decision centers) | 2 | DVN diversity (50+ DVNs) + ZRO governance + LayerZero Labs Foundation |
| POLY-2 (Local adaptation) | 1 | Per-chain DVN configuration is application-local |
| POLY-3 (Cross-scale coordination) | 1 | Cross-chain coordination via DVN standards |
| POLY-4 (Subsidiarity) | 1 | Centralized governance |
| KNOW-1 (Price signals) | 1 | Per-chain gas pricing; basic fee mechanism; fee-switch directs fees to ZRO burns since Feb 2026 |
| KNOW-2 (Local knowledge) | 1 | Limited structured feedback |
| KNOW-3 (Competitive discovery) | 2 | Competitive DVN market (50+ providers) for verification services |
| KNOW-4 (Information aggregation) | 1 | No prediction markets |

**Lens means:** Publicity 1.75; Fairness 1.00; Non-Domination 1.50; Polycentricity 1.25; Knowledge-use 1.25.
**Synergy Index:** arithmetic mean 1.35; geometric mean 1.33.

---

## Wormhole (L1_L2_Infra, HHI 0.012)

**Verification sources:** wormhole.com/docs/protocol/security; WIP-1/2/3 votes at forum.wormhole.com

| Criterion | Score | Evidence |
|-----------|-------|----------|
| PUB-1 (Rule transparency) | 2 | Documentation at wormhole.com/docs; 19-Guardian set public; MultiGov multichain governance documented |
| PUB-2 (Proposal rationale) | 3 | WIPs (Wormhole Improvement Proposals) require rationale + impact analysis; WIP-1 (Code of Conduct, 3,428 voters), WIP-2 (Governance Process), WIP-3 (Grants Program) all 99%+ approval |
| PUB-3 (Enforcement transparency) | 2 | Guardian behavior on-chain transparent; supermajority 13/19 required for transfers |
| PUB-4 (Information symmetry) | 2 | Forum.wormhole.com transparent voting records; Tally wrapped 2025 documented activity |
| FAIR-1 (Floor protection) | 1 | No formal floor |
| FAIR-2 (Access equity) | 1 | Guardian operator selection by foundation; not permissionless |
| FAIR-3 (Distribution fairness) | 1 | Mixed allocation |
| FAIR-4 (Governance accessibility) | 1 | WIP proposal threshold moderate; W holders vote on supported chains via MultiGov |
| NDOM-1 (Contestability) | 2 | WIP-2 codifies structured governance process; appeals via forum; 3,000+ voters per recent WIP demonstrates broad contestability |
| NDOM-2 (Concentration limit) | 2 | Post-exclusion HHI 0.012 less than 0.05; anchor convention |
| NDOM-3 (Emergency powers) | 2 | Foundation retains guardian-set rotation authority; 13/19 supermajority for sensitive operations |
| NDOM-4 (Exit rights) | 1 | Token transfer permissionless; W holders can vote on any supported chain via MultiGov |
| POLY-1 (Decision centers) | 2 | 19-Guardian set + W token holders + Foundation + MultiGov multichain governance system |
| POLY-2 (Local adaptation) | 1 | Per-chain VAA verification is application-local |
| POLY-3 (Cross-scale coordination) | 2 | MultiGov enables cross-chain governance; first multichain governance system in industry |
| POLY-4 (Subsidiarity) | 1 | Centralized parameter governance |
| KNOW-1 (Price signals) | 1 | Basic relay fee mechanism |
| KNOW-2 (Local knowledge) | 1 | Limited structured feedback |
| KNOW-3 (Competitive discovery) | 1 | Guardian competition limited; permissioned set of 19 |
| KNOW-4 (Information aggregation) | 1 | No prediction markets |

**Lens means:** Publicity 2.25; Fairness 1.00; Non-Domination 1.75; Polycentricity 1.50; Knowledge-use 1.00.
**Synergy Index:** arithmetic mean 1.50; geometric mean 1.43.

---

## Morpheus AI (DePIN, HHI 0.046)

**Verification sources:** mor.org; github.com/MorpheusAIs/Docs

| Criterion | Score | Evidence |
|-----------|-------|----------|
| PUB-1 (Rule transparency) | 2 | Documentation at mor.org/whitepaper + gitbook.mor.org; MOR token mechanics documented (block reward starts 14,400 MOR/day, declining to 0 at day 5,833) |
| PUB-2 (Proposal rationale) | 2 | MRC (Morpheus Request for Comments) proposal system on GitHub + Snapshot voting; markdown-based proposals |
| PUB-3 (Enforcement transparency) | 1 | Compute provider dispute resolution informal |
| PUB-4 (Information symmetry) | 1 | Team communications via Discord; no central foundation reduces info-asymmetry concerns |
| FAIR-1 (Floor protection) | 1 | Per-agent compute reward minimal floor |
| FAIR-2 (Access equity) | 1 | Compute provider setup requires GPU + technical expertise |
| FAIR-3 (Distribution fairness) | 1 | Atomic governance; no central allocation to insiders; fair-launch design inspired by Bitcoin/Ethereum |
| FAIR-4 (Governance accessibility) | 1 | MRC proposal threshold low; MOR holders vote via Snapshot |
| NDOM-1 (Contestability) | 1 | Basic MRC voting; no formal appeals; atomic governance reduces concentrated decision-power |
| NDOM-2 (Concentration limit) | 2 | Post-exclusion HHI 0.046 less than 0.05; anchor convention |
| NDOM-3 (Emergency powers) | 1 | Atomic governance: no central team/foundation; each contributor category makes independent decisions |
| NDOM-4 (Exit rights) | 1 | MOR transfer permissionless; mining-based emissions |
| POLY-1 (Decision centers) | 2 | Atomic Governance model: no central foundation; multiple contributor categories make independent decisions (Capital + Compute + Code + Community) |
| POLY-2 (Local adaptation) | 1 | Per-category autonomy; limited cross-category mechanism |
| POLY-3 (Cross-scale coordination) | 1 | Cross-contributor-category coordination informal via MRC |
| POLY-4 (Subsidiarity) | 1 | Atomic structure inherently subsidiary by design |
| KNOW-1 (Price signals) | 2 | AI agent compute pricing; per-job dynamic |
| KNOW-2 (Local knowledge) | 2 | AI agent quality signals theoretical; partial implementation |
| KNOW-3 (Competitive discovery) | 1 | Compute provider competition limited |
| KNOW-4 (Information aggregation) | 1 | MRC voting as aggregation |

**Lens means:** Publicity 1.50; Fairness 1.00; Non-Domination 1.25; Polycentricity 1.25; Knowledge-use 1.50.
**Synergy Index:** arithmetic mean 1.30; geometric mean 1.29.

---

## Axelar (L1_L2_Infra, HHI 0.027)

**Verification sources:** docs.axelar.dev/learn/evm-governance; docs.axelar.dev/resources/community/community-pool-proposals

| Criterion | Score | Evidence |
|-----------|-------|----------|
| PUB-1 (Rule transparency) | 3 | Documentation at docs.axelar.dev/learn/evm-governance; 4 formal proposal types (Software Upgrade, Parameter Change, Community Pool Spend, Call Contracts); 3-day voting period + 33.4% quorum |
| PUB-2 (Proposal rationale) | 2 | Proposals require rationale + sufficient deposit; community pool spend proposals documented |
| PUB-3 (Enforcement transparency) | 2 | Validator slashing on-chain; enforcement consistent |
| PUB-4 (Information symmetry) | 2 | Team communications via Twitter and forum; team token vesting completes by 2026 |
| FAIR-1 (Floor protection) | 1 | Validator stake floor present |
| FAIR-2 (Access equity) | 1 | Validator setup requires AXL + infrastructure |
| FAIR-3 (Distribution fairness) | 1 | Mixed allocation; team vesting completes 2026 |
| FAIR-4 (Governance accessibility) | 1 | Proposal threshold moderate; AXL stakers + delegators vote |
| NDOM-1 (Contestability) | 2 | 4 formal proposal types + 3-day voting + 33.4% quorum + appeals via forum |
| NDOM-2 (Concentration limit) | 2 | Post-exclusion HHI 0.027 less than 0.05; anchor convention |
| NDOM-3 (Emergency powers) | 1 | Foundation retains protocol-upgrade authority via Software Upgrade proposal type |
| NDOM-4 (Exit rights) | 1 | Validator unbonding 21-day delay |
| POLY-1 (Decision centers) | 1 | Validator + community + AXL token-governance via Software Upgrade / Parameter Change / Community Pool / Call Contracts |
| POLY-2 (Local adaptation) | 1 | Per-chain validator set configuration; EVM Contract Governance for cross-EVM calls |
| POLY-3 (Cross-scale coordination) | 2 | Cross-chain coordination via validator-set rotation; EVM Contract Governance |
| POLY-4 (Subsidiarity) | 1 | Subsidiarity moderate |
| KNOW-1 (Price signals) | 1 | Per-chain gas pricing; basic |
| KNOW-2 (Local knowledge) | 1 | Limited structured feedback |
| KNOW-3 (Competitive discovery) | 1 | Validator competition limited |
| KNOW-4 (Information aggregation) | 1 | No prediction markets |

**Lens means:** Publicity 2.25; Fairness 1.00; Non-Domination 1.50; Polycentricity 1.25; Knowledge-use 1.00.
**Synergy Index:** arithmetic mean 1.40; geometric mean 1.33.

---

## MetaDAO (DeFi, HHI 0.015)

**Verification sources:** docs.metadao.fi/governance/overview; metadao.fi

| Criterion | Score | Evidence |
|-----------|-------|----------|
| PUB-1 (Rule transparency) | 2 | Documentation at docs.metadao.fi/governance/overview; futarchy mechanism fully public |
| PUB-2 (Proposal rationale) | 2 | Proposals carry rationale; conditional-on-pass/fail market-resolution criteria public; 96 proposals run for 14 organizations since Nov 2023 |
| PUB-3 (Enforcement transparency) | 2 | Conditional-token enforcement on-chain via futarchy market resolution; TWAP sensitivity parameters DAO-configurable |
| PUB-4 (Information symmetry) | 2 | Futarchy markets are publicly observable by design |
| FAIR-1 (Floor protection) | 1 | No formal floor; market-determined outcomes |
| FAIR-2 (Access equity) | 1 | Conditional-token trading accessible but mechanism complex |
| FAIR-3 (Distribution fairness) | 1 | Token-weighted futarchy structurally favors wealth |
| FAIR-4 (Governance accessibility) | 1 | Proposal threshold low but futarchy execution requires market participation |
| NDOM-1 (Contestability) | 3 | Futarchy provides structural contestability via prediction markets; explicit Pettit operationalization (Hanson 2000 putative-mechanism) |
| NDOM-2 (Concentration limit) | 2 | Post-exclusion HHI 0.015 less than 0.05; anchor convention |
| NDOM-3 (Emergency powers) | 2 | Foundation pause-rights limited; autocrat program resolves futarchy automatically; DAO configures market duration + pass/fail price differential + minimum liquidity + TWAP sensitivity |
| NDOM-4 (Exit rights) | 2 | Conditional-token redemption immediate after resolution |
| POLY-1 (Decision centers) | 1 | Single futarchy mechanism; autocrat program executes; no formal sub-bodies |
| POLY-2 (Local adaptation) | 0 | No local adaptation; futarchy resolves globally |
| POLY-3 (Cross-scale coordination) | 0 | No cross-scale coordination mechanism |
| POLY-4 (Subsidiarity) | 1 | Subsidiarity weak; all decisions via futarchy |
| KNOW-1 (Price signals) | 3 | Prediction markets aggregate information by design; conditional pricing |
| KNOW-2 (Local knowledge) | 3 | Futarchy aggregates dispersed participant beliefs |
| KNOW-3 (Competitive discovery) | 2 | Market-maker permissionless; futarchy traders open |
| KNOW-4 (Information aggregation) | 2 | Futarchy is structured prediction market aggregation (Hayek operationalization at scale) |

**Lens means:** Publicity 2.00; Fairness 1.00; Non-Domination 2.25; Polycentricity 0.50; Knowledge-use 2.50.
**Synergy Index:** arithmetic mean 1.65; geometric mean 1.41.

---

## Gitcoin (Social_Dead, HHI 0.022)

**Verification sources:** support.gitcoin.co; gitcoin.co/program; grants.gitcoin.co

| Criterion | Score | Evidence |
|-----------|-------|----------|
| PUB-1 (Rule transparency) | 2 | Documentation at support.gitcoin.co; GTC parameters and QF rounds public; Grants Stack open-source |
| PUB-2 (Proposal rationale) | 3 | GIPs (Gitcoin Improvement Proposals) require rationale + impact analysis + Stewards review; Grants Rounds Governance Briefs to Stewards |
| PUB-3 (Enforcement transparency) | 2 | QF round criteria public; sybil-attack detection documented; Sybil Defenders workstream |
| PUB-4 (Information symmetry) | 2 | Foundation communications regular; GG21 first fully community-led round ($933K, 11 rounds) |
| FAIR-1 (Floor protection) | 3 | Quadratic Funding mathematically protects floor (small donors count more by design) |
| FAIR-2 (Access equity) | 2 | QF round entry permissionless; documentation accessible; multilingual |
| FAIR-3 (Distribution fairness) | 2 | Community allocation substantial; airdrop broad |
| FAIR-4 (Governance accessibility) | 2 | Proposal threshold accessible; 4 workstreams provide engagement paths (Public Goods Funding, Sybil Defenders, Progressive Decentralization, Public Goods Prototyping) |
| NDOM-1 (Contestability) | 2 | GIP appeals + Stewards Program + QF rounds + Foundation; community-led GG21 round |
| NDOM-2 (Concentration limit) | 2 | Post-exclusion HHI 0.022 less than 0.05; anchor convention |
| NDOM-3 (Emergency powers) | 1 | Foundation retains some QF-round administrative authority; Stewards ratify rounds |
| NDOM-4 (Exit rights) | 2 | Token transfer free; QF round opt-out immediate |
| POLY-1 (Decision centers) | 3 | 4 named workstreams + Stewards + community + Foundation; GG21 fully community-led |
| POLY-2 (Local adaptation) | 2 | Per-round QF parameters set locally; per-workstream autonomy |
| POLY-3 (Cross-scale coordination) | 2 | Cross-workstream coordination via Foundation; Stewards bridge |
| POLY-4 (Subsidiarity) | 1 | Subsidiarity via workstream autonomy (limited by stagnation) |
| KNOW-1 (Price signals) | 2 | QF matching dynamic; per-round signal |
| KNOW-2 (Local knowledge) | 2 | Donor preferences aggregate per round |
| KNOW-3 (Competitive discovery) | 1 | Workstream competition limited |
| KNOW-4 (Information aggregation) | 1 | QF aggregates dispersed signals via quadratic formula |

**Lens means:** Publicity 2.25; Fairness 2.25; Non-Domination 1.75; Polycentricity 2.00; Knowledge-use 1.50.
**Synergy Index:** arithmetic mean 1.95; geometric mean 1.93.

---

## Token Engineering Commons (Social_Dead, HHI 0.028)

**Verification sources:** token-engineering-commons.gitbook.io/tec-handbook; forum.tecommons.org

| Criterion | Score | Evidence |
|-----------|-------|----------|
| PUB-1 (Rule transparency) | 2 | Documentation at token-engineering-commons.gitbook.io/tec-handbook; multi-layer governance (Advice + Conviction + Tao + Snapshot) |
| PUB-2 (Proposal rationale) | 2 | Proposals require rationale; Conviction Voting + Snapshot + Tao Voting tracking |
| PUB-3 (Enforcement transparency) | 2 | Disputable Conviction Voting + Celeste dispute resolution protocol enforce community covenant |
| PUB-4 (Information symmetry) | 2 | Forum-based communications; TEC Handbook complete archive |
| FAIR-1 (Floor protection) | 2 | Conviction voting protects small voters by design (vote-streaming over time) |
| FAIR-2 (Access equity) | 1 | Commons Stack tooling moderate accessibility |
| FAIR-3 (Distribution fairness) | 2 | Mixed allocation; community + insider; Hatch initial distribution |
| FAIR-4 (Governance accessibility) | 1 | Proposal threshold low; conviction-voting protects small voters via time-weighted preference |
| NDOM-1 (Contestability) | 2 | Disputable Conviction Voting + Celeste protocol + Tao Voting for technical + Snapshot for cultural; multi-layer contestability |
| NDOM-2 (Concentration limit) | 2 | Post-exclusion HHI 0.028 less than 0.05; anchor convention |
| NDOM-3 (Emergency powers) | 1 | Foundation pause-rights informal |
| NDOM-4 (Exit rights) | 1 | Token transfer free; conviction voting opt-out via stake removal |
| POLY-1 (Decision centers) | 3 | TEC Polycentric Governance Framework: Advice Process + Conviction Voting (financial) + Tao Voting (technical) + Snapshot (cultural) + Gravity Working Group (conflict resolution) |
| POLY-2 (Local adaptation) | 1 | Per-working-group autonomy (limited by stagnation) |
| POLY-3 (Cross-scale coordination) | 1 | Cross-group coordination informal post-stagnation |
| POLY-4 (Subsidiarity) | 1 | Subsidiarity moderate |
| KNOW-1 (Price signals) | 1 | Conviction voting weighted by time |
| KNOW-2 (Local knowledge) | 2 | Time-preferences aggregation explicit via conviction voting |
| KNOW-3 (Competitive discovery) | 1 | Working-group competition limited |
| KNOW-4 (Information aggregation) | 2 | Conviction voting + Dandelion Voting are structured aggregation of time-preferences |

**Lens means:** Publicity 2.00; Fairness 1.50; Non-Domination 1.50; Polycentricity 1.50; Knowledge-use 1.50.
**Synergy Index:** arithmetic mean 1.60; geometric mean 1.59.

---

## Aethir (DePIN, HHI 0.087)

**Verification sources:** docs.aethir.com/aethir-governance/aethir-foundation-bylaws; blog.aethir.com

| Criterion | Score | Evidence |
|-----------|-------|----------|
| PUB-1 (Rule transparency) | 2 | Documentation at docs.aethir.com/aethir-governance; Foundation Bylaws specify quorum + proposal types |
| PUB-2 (Proposal rationale) | 2 | 4-stage proposal process: Temperature Check + Debate + Implementation Preparation + Decision (on-chain vote); veATH-weighted voting |
| PUB-3 (Enforcement transparency) | 1 | GPU provider dispute resolution informal; Council role partially codified |
| PUB-4 (Information symmetry) | 1 | Team communications via Telegram and Twitter; informational asymmetry |
| FAIR-1 (Floor protection) | 1 | Per-GPU reward minimal floor |
| FAIR-2 (Access equity) | 0 | GPU operator setup requires substantial hardware capital |
| FAIR-3 (Distribution fairness) | 0 | Heavy team / investor allocation (62%); minimal community floor |
| FAIR-4 (Governance accessibility) | 1 | veATH staking required for governance; lock duration weighted; proposal pipeline accessible |
| NDOM-1 (Contestability) | 2 | Council + Foundation Board bicameral governance + 4-stage proposal pipeline + on-chain final vote |
| NDOM-2 (Concentration limit) | 2 | Post-exclusion HHI 0.087 in 0.05 to 0.15 range |
| NDOM-3 (Emergency powers) | 1 | Foundation Board retains major-initiative oversight; Council day-to-day operational authority |
| NDOM-4 (Exit rights) | 0 | GPU staking lock with no formal exit mechanism documented |
| POLY-1 (Decision centers) | 2 | Council + Foundation Board bicameral structure with consultative role between stakeholder classes |
| POLY-2 (Local adaptation) | 0 | No local adaptation |
| POLY-3 (Cross-scale coordination) | 1 | Council consults Foundation Board on major initiatives |
| POLY-4 (Subsidiarity) | 1 | Centralized governance |
| KNOW-1 (Price signals) | 2 | GPU compute market dynamic pricing |
| KNOW-2 (Local knowledge) | 2 | Compute job demand signals |
| KNOW-3 (Competitive discovery) | 1 | GPU provider competition limited |
| KNOW-4 (Information aggregation) | 1 | Governance voting as aggregation |

**Lens means:** Publicity 1.50; Fairness 0.50; Non-Domination 1.25; Polycentricity 1.00; Knowledge-use 1.50.
**Synergy Index:** arithmetic mean 1.15; geometric mean 1.07.

---

## Hivemapper (DePIN, HHI 0.018)

**Verification sources:** docs.hivemapper.com/welcome/network-governance

| Criterion | Score | Evidence |
|-----------|-------|----------|
| PUB-1 (Rule transparency) | 2 | Documentation at docs.hivemapper.com/welcome/network-governance; MIP framework documented |
| PUB-2 (Proposal rationale) | 2 | MIPs (Map Improvement Proposals) notice-and-comment rulemaking: Hivemapper Foundation blog -> Discord community input -> finalization; MIP-9 + MIP-15 (April 2024, 25% burn-reissue, 500K HONEY weekly cap) |
| PUB-3 (Enforcement transparency) | 1 | Map data quality enforcement via AI Trainers; criteria partially public |
| PUB-4 (Information symmetry) | 1 | Team communications via Discord; some informational asymmetry |
| FAIR-1 (Floor protection) | 2 | Per-driver caps + AI training data quality scoring (anti-whale by design) |
| FAIR-2 (Access equity) | 2 | Dashcam hardware cost moderate; geographic constraints; permissionless driver entry |
| FAIR-3 (Distribution fairness) | 1 | Community allocation moderate |
| FAIR-4 (Governance accessibility) | 1 | Proposal threshold accessible; Foundation initiates MIPs; community input via Discord |
| NDOM-1 (Contestability) | 1 | MIP notice-and-comment provides voice; no binding token-holder veto |
| NDOM-2 (Concentration limit) | 2 | Post-exclusion HHI 0.018 less than 0.05; anchor convention |
| NDOM-3 (Emergency powers) | 1 | Foundation retains operational authority via MIP-finalization role |
| NDOM-4 (Exit rights) | 1 | Driver opt-out permissionless |
| POLY-1 (Decision centers) | 1 | Hivemapper Foundation + AI Trainers (quality auditors) |
| POLY-2 (Local adaptation) | 1 | Per-region map coverage targets |
| POLY-3 (Cross-scale coordination) | 1 | Cross-region coordination informal |
| POLY-4 (Subsidiarity) | 1 | Centralized governance |
| KNOW-1 (Price signals) | 3 | Per-region map demand pricing; map-data freshness multipliers; MIP-15 weekly consumption rewards cap |
| KNOW-2 (Local knowledge) | 3 | AI training quality signals; explicit Hayek mechanism for data-quality reward weighting |
| KNOW-3 (Competitive discovery) | 2 | Permissionless driver entry |
| KNOW-4 (Information aggregation) | 2 | AI Trainer quality auditing is structured aggregation |

**Lens means:** Publicity 1.50; Fairness 1.50; Non-Domination 1.25; Polycentricity 1.00; Knowledge-use 2.50.
**Synergy Index:** arithmetic mean 1.55; geometric mean 1.48.

---

## io.net (DePIN, HHI 0.125)

**Verification sources:** io.net/documents/ionet_Tokenomics_Litepaper.pdf; docs.iog.net/docs/io-tokenomics

| Criterion | Score | Evidence |
|-----------|-------|----------|
| PUB-1 (Rule transparency) | 1 | Documentation at docs.iog.net partial; IDE (Incentive Dynamic Engine) litepaper March 2026; some parameters undocumented |
| PUB-2 (Proposal rationale) | 1 | Limited public governance; team-driven; IDE proposal consultation window with community comment form |
| PUB-3 (Enforcement transparency) | 1 | Compute provider dispute resolution informal |
| PUB-4 (Information symmetry) | 1 | Team communications via Discord; progressive decentralization roadmap states core team initially retains control |
| FAIR-1 (Floor protection) | 1 | Per-GPU reward minimal floor; IDE introduces sustainability ratio-based auto-adjustment |
| FAIR-2 (Access equity) | 1 | GPU operator setup moderate cost |
| FAIR-3 (Distribution fairness) | 1 | Mixed allocation; insider allocation significant |
| FAIR-4 (Governance accessibility) | 1 | No formal token-holder DAO yet; planned for Q2 2026 implementation |
| NDOM-1 (Contestability) | 1 | Basic governance via community consultation; no formal appeals architecture pre-DAO |
| NDOM-2 (Concentration limit) | 2 | Post-exclusion HHI 0.125 in 0.05 to 0.15 range |
| NDOM-3 (Emergency powers) | 1 | Core team retains control during progressive-decentralization transition |
| NDOM-4 (Exit rights) | 1 | GPU provider opt-out permissionless |
| POLY-1 (Decision centers) | 0 | io.net Foundation monocentric (core team retains control); DAO transition planned |
| POLY-2 (Local adaptation) | 0 | No local adaptation |
| POLY-3 (Cross-scale coordination) | 1 | Cross-provider coordination informal |
| POLY-4 (Subsidiarity) | 1 | Centralized governance |
| KNOW-1 (Price signals) | 2 | GPU compute market dynamic pricing; IDE introduces revenue-based emission/burn auto-adjustment |
| KNOW-2 (Local knowledge) | 2 | Compute job demand signals; sustainability ratio measures revenue vs. payout obligations |
| KNOW-3 (Competitive discovery) | 1 | Provider competition limited |
| KNOW-4 (Information aggregation) | 1 | Governance voting as aggregation (limited pre-DAO) |

**Lens means:** Publicity 1.00; Fairness 1.00; Non-Domination 1.25; Polycentricity 0.50; Knowledge-use 1.50.
**Synergy Index:** arithmetic mean 1.05; geometric mean 0.99.

---
