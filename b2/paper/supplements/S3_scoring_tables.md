# S3: Scoring Tables

Protocol-by-criterion scores for all 40 protocols in the cross-section. Twelve protocols (Uniswap, Compound, Aave, MakerDAO, Lido, Helium, DIMO, Anyone Protocol, Optimism, Arbitrum, ENS, GEODNET) carry full 20-cell criterion-by-criterion evidence tables (240 cells); the remaining 28 protocols carry 5-lens summary scores with evidence notes per lens, added 2026-05-19 to enable full-sample Synergy Index analysis. Wayru carries 5-lens abbreviated scores as a degenerate-case reference. Scores assigned by a single coder (ZZ); inter-rater reliability testing specified as future work. Evidence gathered from governance documentation, on-chain proposal records, and protocol forum activity as of March to May 2026.

Scoring scale: 0 = absent, 1 = minimal, 2 = partial, 3 = exemplary. See S2 for full criterion definitions. Synergy Index reported as arithmetic mean (paper-canonical) and geometric mean (weakest-link robustness check); arith vs geom rank-order Spearman rho = 0.98 across the full 40-protocol sample.

Reproducibility: see `synergy_index_full_sample_2026-05-19.py` and `synergy_index_full_sample_2026-05-19.csv` in this directory.

## Summary Table (all 40 protocols, sorted by Synergy descending)

| Protocol | Category | HHI | Publicity | Fairness | Non-Dom. | Polycentric | Knowledge | Syn. (arith) | Syn. (geom) |
|----------|----------|-----|-----------|----------|----------|-------------|-----------|--------------|-------------|
| Filecoin | DePIN | 0.022 | 2.00 | 1.25 | 2.00 | 2.50 | 2.00 | 1.95 | 1.90 |
| Optimism | L1_L2_Infra | 0.009 | 2.25 | 1.75 | 2.25 | 2.00 | 1.25 | 1.90 | 1.86 |
| Gitcoin | Social_Dead | 0.022 | 2.25 | 2.00 | 1.75 | 2.00 | 1.50 | 1.90 | 1.88 |
| Helium | DePIN | 0.074 | 2.00 | 1.00 | 2.00 | 2.00 | 2.00 | 1.80 | 1.74 |
| The Graph | L1_L2_Infra | 0.033 | 2.00 | 1.50 | 2.00 | 2.00 | 1.50 | 1.80 | 1.78 |
| Rocket Pool | DeFi | 0.039 | 2.25 | 1.50 | 2.00 | 2.00 | 1.00 | 1.75 | 1.68 |
| Arbitrum | L1_L2_Infra | 0.012 | 2.00 | 1.50 | 2.00 | 1.75 | 1.25 | 1.70 | 1.67 |
| MetaDAO | DeFi | 0.015 | 2.00 | 1.00 | 2.50 | 0.50 | 2.50 | 1.70 | 1.44 |
| Aave | DeFi | 0.013 | 2.25 | 1.50 | 2.00 | 1.25 | 1.25 | 1.65 | 1.60 |
| MakerDAO | DeFi | 0.040 | 2.00 | 0.75 | 1.75 | 2.00 | 1.50 | 1.60 | 1.51 |
| Balancer | DeFi | 0.029 | 2.00 | 1.00 | 1.50 | 1.50 | 2.00 | 1.60 | 1.55 |
| Curve | DeFi | 0.014 | 2.00 | 0.75 | 1.50 | 1.50 | 2.00 | 1.55 | 1.47 |
| DIMO | DePIN | 0.025 | 1.50 | 1.25 | 1.75 | 1.50 | 1.50 | 1.50 | 1.49 |
| Pokt Network | DePIN | 0.090 | 2.00 | 1.00 | 1.50 | 1.50 | 1.50 | 1.50 | 1.47 |
| Token Engineering Commons | Social_Dead | 0.028 | 1.50 | 1.50 | 1.50 | 1.50 | 1.50 | 1.50 | 1.50 |
| Hivemapper | DePIN | 0.018 | 1.50 | 1.50 | 1.00 | 1.00 | 2.50 | 1.50 | 1.41 |
| Compound | DeFi | 0.009 | 2.00 | 1.25 | 2.00 | 1.00 | 1.00 | 1.45 | 1.38 |
| Polygon | L1_L2_Infra | 0.035 | 2.00 | 1.25 | 1.50 | 1.50 | 1.00 | 1.45 | 1.41 |
| Uniswap | DeFi | 0.010 | 2.00 | 1.00 | 2.00 | 1.00 | 1.00 | 1.40 | 1.32 |
| Lido | DeFi | 0.008 | 1.75 | 1.25 | 1.75 | 1.25 | 1.00 | 1.40 | 1.37 |
| GEODNET | DePIN | 0.060 | 2.00 | 1.00 | 1.00 | 1.00 | 2.00 | 1.40 | 1.32 |
| GMX | DeFi | 0.065 | 2.00 | 1.00 | 1.50 | 1.00 | 1.50 | 1.40 | 1.35 |
| ENS | L1_L2_Infra | 0.071 | 1.75 | 1.00 | 1.75 | 1.25 | 1.00 | 1.35 | 1.31 |
| IoTeX | DePIN | 0.189 | 1.50 | 1.00 | 1.00 | 1.50 | 1.50 | 1.30 | 1.28 |
| WeatherXM | DePIN | 0.148 | 1.50 | 1.00 | 1.00 | 1.00 | 2.00 | 1.30 | 1.25 |
| Livepeer | DePIN | 0.199 | 1.50 | 1.00 | 1.00 | 1.00 | 2.00 | 1.30 | 1.25 |
| Axelar | L1_L2_Infra | 0.027 | 1.75 | 1.00 | 1.50 | 1.25 | 1.00 | 1.30 | 1.27 |
| Maple Finance | DeFi | 0.024 | 1.75 | 1.00 | 1.50 | 1.00 | 1.00 | 1.25 | 1.21 |
| Hyperliquid | DeFi | 0.005 | 2.00 | 1.00 | 1.00 | 0.00 | 2.00 | 1.20 | 0.53 |
| Render | DePIN | 0.027 | 1.50 | 1.00 | 1.00 | 1.00 | 1.50 | 1.20 | 1.18 |
| Morpheus AI | DePIN | 0.046 | 1.50 | 1.00 | 1.00 | 1.00 | 1.50 | 1.20 | 1.18 |
| Jupiter | DeFi | 0.096 | 1.50 | 1.00 | 1.00 | 1.00 | 1.00 | 1.10 | 1.08 |
| Drift | DeFi | 0.053 | 1.50 | 1.00 | 1.00 | 1.00 | 1.00 | 1.10 | 1.08 |
| Ether.Fi | DeFi | 0.042 | 1.50 | 1.00 | 1.00 | 1.00 | 1.00 | 1.10 | 1.08 |
| Grass | DePIN | 0.035 | 1.50 | 1.00 | 1.00 | 0.50 | 1.50 | 1.10 | 1.02 |
| LayerZero | L1_L2_Infra | 0.014 | 1.50 | 1.00 | 1.00 | 1.00 | 1.00 | 1.10 | 1.08 |
| Wormhole | L1_L2_Infra | 0.012 | 1.50 | 1.00 | 1.00 | 1.00 | 1.00 | 1.10 | 1.08 |
| Anyone Protocol | DePIN | 0.013 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| io.net | DePIN | 0.125 | 1.00 | 1.00 | 1.00 | 0.50 | 1.50 | 1.00 | 0.94 |
| Aethir | DePIN | 0.087 | 1.00 | 0.50 | 1.00 | 0.50 | 1.50 | 0.90 | 0.82 |
| Wayru (degenerate reference) | DePIN | N/A | 1.00 | 1.00 | 0.00 | 0.00 | 1.00 | 0.60 | 0.01 |

## Full-sample correlations (N = 40)

- **Synergy (arith) vs HHI:** Spearman rho = -0.250 (p = 0.120); Pearson r = -0.272 (p = 0.090). Direction: higher concentration weakly predicts lower institutional-design quality across the five lenses.
- **Synergy (geom) vs HHI:** Spearman rho = -0.198 (p = 0.221). Weakest-link aggregation preserves the negative direction at attenuated magnitude.
- **Arith vs geom Synergy:** Spearman rho = 0.980 (p < 0.001) on rank ordering. Operationalization-of-aggregation choice does not materially change protocol rank ordering across the 40-protocol sample, addressing one operationalization-dependency concern raised in Section 4.8.
- **Sector mean Synergy:** DeFi 1.42 (N = 15); DePIN 1.33 (N = 15); L1_L2_Infra 1.46 (N = 8); Social_Dead 1.70 (N = 2). DePIN-vs-DeFi Synergy contrast: Mann-Whitney U = 87, p = 0.298 (not significant; sector signal in HHI does not translate symmetrically to Synergy Index, indicating that the five-lens framework captures dimensions orthogonal to raw holding concentration).

---

## 1. Uniswap (DeFi, HHI 0.032)

| Criterion | Score | Evidence |
|-----------|-------|----------|
| PUB-1 Rule transparency | 2 | Governance docs at docs.uniswap.org; GovernorBravo parameters on-chain; fee tier parameters public |
| PUB-2 Proposal rationale | 2 | gov.uniswap.org requires rationale; Temperature Check, Consensus Check, and On-Chain Vote stages enforce deliberation |
| PUB-3 Enforcement transparency | 2 | No slashing mechanism; enforcement limited to parameter governance; 2-day Timelock provides transparency window |
| PUB-4 Information symmetry | 2 | Team blog updates; Uniswap Labs strategy partially opaque; fee switch deliberations extended over years |
| FAIR-1 Floor protection | 1 | No minimum for LPs; impermanent loss unmitigated; small LPs earn proportionally but bear full IL risk |
| FAIR-2 Access equity | 1 | Permissionless LP entry; but 2.5M UNI (~$20M) required to submit on-chain proposal; high barrier |
| FAIR-3 Distribution fairness | 1 | 60% community allocation at genesis; but 26.5% (264.6M UNI) locked in Timelock treasury with zero voting power (delegates() returns 0x0) |
| FAIR-4 Governance accessibility | 1 | Delegation available; 126 active delegates (Tally, March 2026); voting HHI 0.068 (2.1x amplification); top delegates dominate |
| NDOM-1 Contestability | 2 | 2-day Timelock; quorum 40M UNI; SushiSwap fork (2020) demonstrated credible exit |
| NDOM-2 Concentration limit | 2 | Post-exclusion HHI 0.032; moderate; voting HHI 0.068 indicates delegate concentration beyond holdings |
| NDOM-3 Emergency powers | 2 | Labs retains front-end control; no on-chain emergency override; Foundation operational discretion informal |
| NDOM-4 Exit rights | 2 | Liquid UNI; no lockup; governance exit by selling or abstaining; LP withdrawal permissionless |
| POLY-1 Decision centers | 1 | Single GovernorBravo; no formal subDAOs or working groups with independent authority |
| POLY-2 Local adaptation | 1 | Four fee tiers per pool (0.01%, 0.05%, 0.30%, 1.00%); governance parameters global |
| POLY-3 Cross-scale coordination | 1 | Multi-chain deployments (Ethereum, Arbitrum, Polygon, Optimism, Base); governance remains Ethereum-only |
| POLY-4 Subsidiarity | 1 | All governance decisions through single proposal pipeline; no delegation of authority by domain |
| KNOW-1 Price signals | 1 | AMM concentrated liquidity pricing; no protocol-level congestion pricing; fee switch debate unresolved since 2022 |
| KNOW-2 Local knowledge | 1 | Governance forum as sole structured feedback; no oracle-mediated parameter adjustment |
| KNOW-3 Competitive discovery | 1 | Permissionless LP entry; DEX aggregator competition for routing; no operator role competition |
| KNOW-4 Information aggregation | 1 | Token-weighted voting only; no prediction markets, futarchy, or conviction voting |

---

## 2. Compound (DeFi, HHI 0.009)

| Criterion | Score | Evidence |
|-----------|-------|----------|
| PUB-1 Rule transparency | 2 | Compound III parameters documented; interest rate models published in code; GovernorBravo on-chain |
| PUB-2 Proposal rationale | 2 | comp.xyz governance forum; proposals require description; multi-step process (review, voting, timelock) |
| PUB-3 Enforcement transparency | 2 | Liquidation parameters public and deterministic; no discretionary enforcement |
| PUB-4 Information symmetry | 2 | Compound Labs updates; risk parameters set by governance; Gauntlet risk reports public |
| FAIR-1 Floor protection | 1 | No minimum deposit; small depositors earn proportional yield; liquidation risk borne equally |
| FAIR-2 Access equity | 1 | Permissionless deposit/borrow; 65,000 COMP (~$3.5M) required to propose; high threshold |
| FAIR-3 Distribution fairness | 2 | COMP distributed through usage (liquidity mining 2020-2023); compressed concentration over time from 50% insider genesis |
| FAIR-4 Governance accessibility | 1 | Active delegation; 100 delegates (Tally); voting HHI 0.053 (1.9x amplification); moderate concentration |
| NDOM-1 Contestability | 2 | 2-day Timelock; quorum requirements; GovernorBravo upgrade from Alpha added protections |
| NDOM-2 Concentration limit | 2 | HHI 0.028 (low); no single entity dominates; consistent with distributed governance |
| NDOM-3 Emergency powers | 2 | Guardian multisig can pause markets; scope documented in governance docs |
| NDOM-4 Exit rights | 2 | Liquid COMP; permissionless deposit/withdrawal; no lock-in beyond utilization-based borrowing limits |
| POLY-1 Decision centers | 1 | Single GovernorBravo; no subDAOs; Compound Labs handles development |
| POLY-2 Local adaptation | 1 | Per-market parameters (collateral factor, interest rate model) governed globally |
| POLY-3 Cross-scale coordination | 1 | Multi-chain Compound III deployments; governance remains Ethereum-only |
| POLY-4 Subsidiarity | 1 | All parameters governed through single proposal pipeline |
| KNOW-1 Price signals | 1 | Interest rate curves as capital allocation signals; utilization-based dynamic pricing |
| KNOW-2 Local knowledge | 1 | Gauntlet risk modeling as structured input; implementation centralized |
| KNOW-3 Competitive discovery | 1 | Market competition (vs Aave, Morpho); no internal operator-role competition |
| KNOW-4 Information aggregation | 1 | Token-weighted voting; Gauntlet as oracle-like risk input; no prediction markets |

---

## 3. Aave (DeFi, HHI 0.013)

| Criterion | Score | Evidence |
|-----------|-------|----------|
| PUB-1 Rule transparency | 3 | AIP process comprehensive; V3 risk parameters documented per market per chain; governance.aave.com |
| PUB-2 Proposal rationale | 2 | AIPs require motivation and specification; Snapshot pre-vote + on-chain execution |
| PUB-3 Enforcement transparency | 2 | Liquidation mechanics deterministic and documented; no discretionary enforcement |
| PUB-4 Information symmetry | 2 | Aave Companies publishes updates; Gauntlet and Chaos Labs risk reports public; GHO operations transparent |
| FAIR-1 Floor protection | 2 | Safety Module staking earns rewards at any amount; stkAAVE provides shortfall insurance |
| FAIR-2 Access equity | 1 | Permissionless deposit/borrow; 80,000 AAVE (~$12M) for proposition power; delegation lowers effective barrier |
| FAIR-3 Distribution fairness | 2 | 0% insider at AAVE genesis (LEND-to-AAVE migration); Safety Module and ecosystem reserve distribute over time |
| FAIR-4 Governance accessibility | 2 | Active delegation; stkAAVE holders retain governance through staking contract; voting HHI 0.076 (3.8x amplification) |
| NDOM-1 Contestability | 2 | Guardian multisig with published scope; cross-chain governance bridge (a.DI); Timelock delays |
| NDOM-2 Concentration limit | 2 | Post-exclusion HHI 0.020 (low); stkAAVE exclusion was critical correction (21.7% removed) |
| NDOM-3 Emergency powers | 2 | Guardian can pause markets; cannot change core parameters unilaterally; scope defined in AIP |
| NDOM-4 Exit rights | 2 | Liquid AAVE; stkAAVE 10-day cooldown; permissionless deposit withdrawal |
| POLY-1 Decision centers | 1 | Single governance process; risk service providers advisory but no independent authority |
| POLY-2 Local adaptation | 2 | Per-market risk parameters (LTV, liquidation threshold) per chain deployment; V3 e-mode adds context settings |
| POLY-3 Cross-scale coordination | 1 | Multi-chain via a.DI bridge; governance originates on Ethereum |
| POLY-4 Subsidiarity | 1 | Risk providers advise; DAO decides all parameters centrally |
| KNOW-1 Price signals | 2 | Interest rate curves; GHO stablecoin rate as monetary policy signal; utilization-based dynamic pricing |
| KNOW-2 Local knowledge | 1 | Gauntlet and Chaos Labs modeling; structured input but centralized implementation |
| KNOW-3 Competitive discovery | 1 | Lending market competition (Compound, Morpho, Spark); no internal operator competition |
| KNOW-4 Information aggregation | 1 | Token-weighted voting; risk providers as oracle-like input; no prediction markets |

---

## 4. MakerDAO (DeFi, HHI 0.045)

| Criterion | Score | Evidence |
|-----------|-------|----------|
| PUB-1 Rule transparency | 2 | Extensive MIP process; parameters documented at vote.makerdao.com; governance portal comprehensive |
| PUB-2 Proposal rationale | 2 | MIPs require motivation, specification, and community discussion; forum.makerdao.com has deep deliberation culture |
| PUB-3 Enforcement transparency | 2 | Vault liquidation deterministic; oracle price feeds public; Emergency Shutdown documented |
| PUB-4 Information symmetry | 2 | Recognized Delegates publish reasoning; RWA collateral introduces off-chain asymmetry (institutional vaults less transparent) |
| FAIR-1 Floor protection | 1 | No minimum vault size; gas costs disproportionately affect small positions; no hardship provisions |
| FAIR-2 Access equity | 1 | Permissionless vault creation; but 100% insider genesis means all governance power originated with founders/investors |
| FAIR-3 Distribution fairness | 0 | 100% insider at genesis (84.5% team, 15.5% investors); zero community distribution mechanism; secondary market is sole path to MKR |
| FAIR-4 Governance accessibility | 1 | Delegation available; Recognized Delegates compensated; but all governance power traces to original insider allocation |
| NDOM-1 Contestability | 2 | Emergency Shutdown as ultimate contestability (any MKR holder can trigger if threshold met); executive vote delay |
| NDOM-2 Concentration limit | 2 | HHI 0.045 (moderate); Top-1 holder 11.4%; no single entity unilateral control |
| NDOM-3 Emergency powers | 1 | Emergency Shutdown is nuclear (shuts entire system); no graduated response; Endgame introduces granular controls |
| NDOM-4 Exit rights | 2 | Liquid MKR; vault withdrawal permissionless; DAI redeemable through PSM |
| POLY-1 Decision centers | 2 | Core Units (2021-2023) with independent budgets; Endgame SubDAOs (2024+) formalize multi-center governance |
| POLY-2 Local adaptation | 2 | Per-collateral risk parameters; RWA vaults have distinct processes; PSM parameters separate from lending |
| POLY-3 Cross-scale coordination | 2 | Core Unit coordination; budget allocation across units; SubDAO shared L1 with independent operations |
| POLY-4 Subsidiarity | 2 | Core Units handled domain decisions; Endgame pushes operational authority to SubDAOs |
| KNOW-1 Price signals | 2 | DSR as monetary policy signal; PSM spreads as arbitrage signal; stability fees as collateral risk pricing |
| KNOW-2 Local knowledge | 2 | Oracle network aggregates prices; RWA partners contribute off-chain credit assessment |
| KNOW-3 Competitive discovery | 1 | Vault strategies compete for yield; oracle providers compete for slots; governance remains token-weighted |
| KNOW-4 Information aggregation | 1 | Token-weighted voting; Recognized Delegates as intermediaries; no prediction markets |

---

## 5. Lido (DeFi, HHI 0.018)

| Criterion | Score | Evidence |
|-----------|-------|----------|
| PUB-1 Rule transparency | 2 | Governance docs published; EasyTrack for routine governance; staking parameters public |
| PUB-2 Proposal rationale | 2 | LIP process; Snapshot proposals with rationale; Research forum active |
| PUB-3 Enforcement transparency | 1 | Node operator performance monitoring public; but operator selection criteria partially opaque |
| PUB-4 Information symmetry | 2 | Financial reports; validator dashboards public; some treasury strategy opacity |
| FAIR-1 Floor protection | 2 | stETH rebasing provides proportional rewards at any amount; democratizes staking access |
| FAIR-2 Access equity | 1 | stETH minting permissionless; but node operator entry restricted (curated ~30 operators); LDO required for governance |
| FAIR-3 Distribution fairness | 1 | Team and investors hold significant LDO; community distribution through incentives but insider-weighted genesis |
| FAIR-4 Governance accessibility | 1 | Delegation on Snapshot; EasyTrack lowers operational barrier; strategic decisions controlled by large LDO holders |
| NDOM-1 Contestability | 1 | Dual governance (stETH holders participate) proposed but not yet live as of March 2026; current governance LDO-only |
| NDOM-2 Concentration limit | 2 | HHI 0.018 (very low token concentration); but only 189 holders and voting HHI 0.088 (4.8x amplification) |
| NDOM-3 Emergency powers | 2 | EasyTrack for routine operations; DAO multisig for emergency pauses; scope documented |
| NDOM-4 Exit rights | 2 | stETH liquid/tradeable; LDO liquid; staked ETH withdrawal available post-Shanghai |
| POLY-1 Decision centers | 1 | Single DAO; LNOSG has limited scope; committees exist without independent budgets |
| POLY-2 Local adaptation | 2 | Per-module parameters; Community Staking Module adds permissionless operator tier |
| POLY-3 Cross-scale coordination | 1 | Multi-chain wstETH; governance single-chain |
| POLY-4 Subsidiarity | 1 | EasyTrack for routine motions; strategic decisions DAO-level; limited authority delegation |
| KNOW-1 Price signals | 1 | stETH/ETH peg as market signal; no dynamic fee or congestion pricing |
| KNOW-2 Local knowledge | 1 | Validator performance metrics public; operator selection not market-based |
| KNOW-3 Competitive discovery | 1 | Curated operator set; CSM adds permissionless tier but nascent |
| KNOW-4 Information aggregation | 1 | Token-weighted LDO voting; validator performance as implicit signal |

---

## 6. Helium (DePIN, HHI 0.102)

| Criterion | Score | Evidence |
|-----------|-------|----------|
| PUB-1 Rule transparency | 2 | HIP process documented at docs.helium.com; chain variables public; subDAO specs published |
| PUB-2 Proposal rationale | 2 | HIPs require motivation, stakeholders, and technical specification; HIP-147 exemplary |
| PUB-3 Enforcement transparency | 2 | Denylist process documented; validator slashing parameters published; removal criteria public |
| PUB-4 Information symmetry | 2 | Foundation quarterly reports; subDAO metrics on Explorer; coverage maps public |
| FAIR-1 Floor protection | 1 | No minimum reward guarantee; small operators face high variance; PoC rewards location-dependent |
| FAIR-2 Access equity | 1 | Hardware $300-$2,000; technical setup non-trivial; Mobile requires expensive radios |
| FAIR-3 Distribution fairness | 1 | Mining distributes to operators; but early/dense locations accumulated disproportionately |
| FAIR-4 Governance accessibility | 1 | veHNT delegation available; HIP voting requires staked HNT; delegation mechanics complex |
| NDOM-1 Contestability | 2 | HIP rejection demonstrated; HIP-147 community override (operators accepted reward cuts through legitimate process) |
| NDOM-2 Concentration limit | 2 | HHI 0.102 (moderate-high); burn HHI 0.27 (top-5 burners ≈ 90%; top-2 = 70%); concentrated usage |
| NDOM-3 Emergency powers | 2 | Foundation operational authority; Helium Council provides checks; no unilateral override |
| NDOM-4 Exit rights | 2 | Liquid HNT; hotspot resale market; hardware transferable; no governance lock-in |
| POLY-1 Decision centers | 2 | SubDAO structure (IoT, Mobile) with independent treasuries and emission schedules |
| POLY-2 Local adaptation | 2 | Per-subDAO reward curves; IoT and Mobile different economics; location multipliers |
| POLY-3 Cross-scale coordination | 2 | Cross-subDAO HNT emission; shared L1 (Solana) with independent subDAO L2 operations |
| POLY-4 Subsidiarity | 2 | SubDAO-level parameters; HNT-level cross-cutting policy; veHNT determines subDAO allocation |
| KNOW-1 Price signals | 2 | Data Credits as demand signal; location-based coverage rewards; congestion multipliers |
| KNOW-2 Local knowledge | 2 | Proof-of-coverage transmits local network quality; hotspot proximity detection; coverage maps |
| KNOW-3 Competitive discovery | 2 | Permissionless hotspot deployment; geographic competition for DC revenue; multiple hardware makers |
| KNOW-4 Information aggregation | 2 | Coverage verification oracles; PoC as distributed quality measurement; challenge mechanism |

---

## 7. DIMO (DePIN, HHI 0.025)

| Criterion | Score | Evidence |
|-----------|-------|----------|
| PUB-1 Rule transparency | 2 | DIP process at docs.dimo.zone; token parameters published; device requirements documented |
| PUB-2 Proposal rationale | 1 | DIPs exist but less formalized than mature protocols; early-stage documentation |
| PUB-3 Enforcement transparency | 2 | Device registration requirements published; data quality thresholds documented |
| PUB-4 Information symmetry | 1 | Foundation strategy partially opaque; data marketplace economics emerging; partnerships not fully public |
| FAIR-1 Floor protection | 1 | Device mining proportional to data contribution; no minimum guarantee; hardware investment required |
| FAIR-2 Access equity | 2 | OBD-II dongle $50-$100 (lower than most DePIN hardware); broad vehicle compatibility |
| FAIR-3 Distribution fairness | 1 | Device mining distributes to operators; Foundation holds significant share |
| FAIR-4 Governance accessibility | 1 | Snapshot voting; only 10 voters in recent rounds; Foundation likely controls outcomes |
| NDOM-1 Contestability | 1 | Snapshot with low participation; no formal contestation mechanism beyond voting |
| NDOM-2 Concentration limit | 2 | Holding HHI 0.038 (low); voting HHI 0.228 (6.0x amplification, 10 voters) |
| NDOM-3 Emergency powers | 2 | Foundation multisig; standard for early-stage; scope informally bounded |
| NDOM-4 Exit rights | 2 | Liquid DIMO token; device resaleable; no lock-in beyond hardware |
| POLY-1 Decision centers | 2 | Node structure; marketplace governance emerging; data validation separate from token governance |
| POLY-2 Local adaptation | 1 | Global reward parameters; no geographic differentiation |
| POLY-3 Cross-scale coordination | 1 | Single-chain governance (Polygon) |
| POLY-4 Subsidiarity | 2 | Device-level validation separated from token governance; marketplace operations delegated |
| KNOW-1 Price signals | 2 | Data marketplace pricing emerging; vehicle data differentiated by type and geography |
| KNOW-2 Local knowledge | 1 | Vehicle telemetry as input; reward function does not yet differentiate by data quality |
| KNOW-3 Competitive discovery | 2 | Multiple device manufacturers; open hardware spec; quality competition |
| KNOW-4 Information aggregation | 1 | Token-weighted Snapshot (10 voters); no structured aggregation |

---

## 8. Anyone Protocol (DePIN, HHI 0.013)

| Criterion | Score | Evidence |
|-----------|-------|----------|
| PUB-1 Rule transparency | 1 | Basic documentation; token parameters published; governance process not formalized |
| PUB-2 Proposal rationale | 1 | No formal proposal process; community Discord as primary communication |
| PUB-3 Enforcement transparency | 1 | Node requirements documented; no slashing or enforcement history; early stage |
| PUB-4 Information symmetry | 1 | Team communications limited to blog and Discord; no governance reports |
| FAIR-1 Floor protection | 1 | Relay operation has minimum bandwidth requirements; no minimum reward guarantee |
| FAIR-2 Access equity | 1 | Node operation requires technical skill and bandwidth; lower hardware cost than most DePIN |
| FAIR-3 Distribution fairness | 1 | Community distribution through node operation; allocation split not fully transparent |
| FAIR-4 Governance accessibility | 1 | Token-weighted; no delegation infrastructure; participation data unavailable |
| NDOM-1 Contestability | 1 | No formal contestation mechanism; governance informal; early-stage |
| NDOM-2 Concentration limit | 1 | Holding HHI 0.040 (low, encouraging); but governance mechanisms underdeveloped to use it |
| NDOM-3 Emergency powers | 1 | Team retains operational control; no published scope or constraints |
| NDOM-4 Exit rights | 1 | Liquid ANYONE token; node shutdown permissionless; limited DEX liquidity |
| POLY-1 Decision centers | 1 | Single body (effectively team/foundation); no subDAOs |
| POLY-2 Local adaptation | 1 | Global parameters; no geographic or context-specific governance |
| POLY-3 Cross-scale coordination | 1 | Single-chain; no coordination needed |
| POLY-4 Subsidiarity | 1 | All decisions centralized at team level |
| KNOW-1 Price signals | 1 | Bandwidth contribution as implicit signal; no dynamic pricing |
| KNOW-2 Local knowledge | 1 | Relay nodes contribute local information; not structured into governance |
| KNOW-3 Competitive discovery | 1 | Permissionless relay entry; 6,000 nodes; no formal quality ranking |
| KNOW-4 Information aggregation | 1 | No structured aggregation; governance minimal |

Note: Anyone scores uniformly at 1 due to early-stage maturity, not poor design intent. The low HHI (0.040) reflects deliberate distribution design; institutional governance infrastructure is nascent.

---

## 9. Optimism (Infrastructure, HHI 0.042)

| Criterion | Score | Evidence |
|-----------|-------|----------|
| PUB-1 Rule transparency | 3 | Optimism Collective constitution published; governance framework at community.optimism.io; Operating Manual versioned |
| PUB-2 Proposal rationale | 2 | Mission Requests and Intent frameworks require detailed rationale; Delegate Approvals structured |
| PUB-3 Enforcement transparency | 2 | Code of Conduct published; enforcement through Token House and Citizens' House |
| PUB-4 Information symmetry | 2 | Regular governance updates; Foundation reports; some opacity around Superchain strategy |
| FAIR-1 Floor protection | 2 | RetroPGF distributes to public goods ($300M+ distributed); impact-assessed, not merit-weighted |
| FAIR-2 Access equity | 2 | Delegation accessible; Citizens' House expanding beyond tokens; soulbound citizenship |
| FAIR-3 Distribution fairness | 1 | 64% nominally community; Foundation treasury controls substantial share; initial airdrop broad (248,699 addresses) |
| FAIR-4 Governance accessibility | 2 | Compensated delegation; active recruitment; low threshold; voting guides published |
| NDOM-1 Contestability | 3 | Two-chamber governance (Token House + Citizens' House); veto between chambers; constitutional limits |
| NDOM-2 Concentration limit | 2 | Post-exclusion holding HHI 0.042; voting HHI 0.033 (0.79x ratio, healthiest in sample) |
| NDOM-3 Emergency powers | 2 | Security Council 9-of-12 multisig; published scope; sunset and rotation provisions |
| NDOM-4 Exit rights | 2 | Liquid OP; bridge to L1 (7-day delay); no governance lock-in |
| POLY-1 Decision centers | 2 | Two chambers; working groups; grants councils with independent budgets |
| POLY-2 Local adaptation | 2 | Superchain enables per-chain governance (emerging); Law of Chains framework |
| POLY-3 Cross-scale coordination | 2 | Superchain coordination; shared OP Stack with member chain autonomy |
| POLY-4 Subsidiarity | 2 | Working groups handle domain governance; grants councils allocate; chambers have defined scope |
| KNOW-1 Price signals | 1 | L1 data availability fee; sequencer revenue as demand signal; no OP congestion pricing |
| KNOW-2 Local knowledge | 1 | Proposals; RetroPGF as retrospective impact assessment; Delegate Approvals |
| KNOW-3 Competitive discovery | 2 | Permissionless Superchain deployment; sequencer competition planned |
| KNOW-4 Information aggregation | 1 | Token-weighted Token House; Citizens' House adds non-token signal; RetroPGF as partial measurement |

---

## 10. Arbitrum (Infrastructure, HHI 0.012)

| Criterion | Score | Evidence |
|-----------|-------|----------|
| PUB-1 Rule transparency | 2 | Constitution published; AIP process documented; governance.arbitrum.io |
| PUB-2 Proposal rationale | 2 | AIPs require abstract, motivation, specification; Snapshot temperature check before on-chain |
| PUB-3 Enforcement transparency | 2 | Security Council actions logged; no discretionary user enforcement; sequencer transparent |
| PUB-4 Information symmetry | 2 | Offchain Labs technical updates; Foundation quarterly reports; some Orbit strategy opacity |
| FAIR-1 Floor protection | 1 | No minimum for L2 usage; gas fees lower than L1; sequencer revenue accrues to DAO |
| FAIR-2 Access equity | 2 | Large airdrop (11.62% users, 1.13% DAOs); funded delegate programs; lower proposal threshold |
| FAIR-3 Distribution fairness | 1 | 44% insider; 56% community (including DAO treasury); airdrop broadest L2 distribution at launch |
| FAIR-4 Governance accessibility | 2 | Compensated delegation; active ecosystem; 100 Tally delegates; voting HHI 0.052 (4.3x amplification) |
| NDOM-1 Contestability | 2 | Constitutional governance with amendment process; Security Council defined emergency scope; optimistic model |
| NDOM-2 Concentration limit | 2 | Post-exclusion HHI 0.012 (lowest Infra); FixedDelegateWallet exclusion removed 30% share |
| NDOM-3 Emergency powers | 2 | Security Council 9-of-12; published scope; can perform emergency upgrades; sunset provisions |
| NDOM-4 Exit rights | 2 | Liquid ARB; bridge to L1 (7-day); Orbit exit to own L3 |
| POLY-1 Decision centers | 2 | DAO; Security Council; grants programs (LTIPP, Backfund, STIP); working groups |
| POLY-2 Local adaptation | 1 | Orbit chains customize; Arbitrum One governance global |
| POLY-3 Cross-scale coordination | 2 | Orbit L3 coordination; DAO for L2; grants coordinate ecosystem |
| POLY-4 Subsidiarity | 2 | Grants delegate allocation; Security Council handles emergency; working groups for domains |
| KNOW-1 Price signals | 1 | Sequencer fee as demand signal; gas pricing follows L1 model; no ARB pricing |
| KNOW-2 Local knowledge | 1 | Proposals; delegate commentary; no oracle-mediated adjustment |
| KNOW-3 Competitive discovery | 2 | Orbit competitive L3 deployment; sequencer decentralization planned |
| KNOW-4 Information aggregation | 1 | Token-weighted voting; delegate reasoning published; no prediction markets |

---

## 11. ENS (Infrastructure, HHI 0.071)

| Criterion | Score | Evidence |
|-----------|-------|----------|
| PUB-1 Rule transparency | 2 | ENS Constitution published; EP process documented; governance.ens.domains |
| PUB-2 Proposal rationale | 2 | EPs require motivation and specification; social + executable proposal stages |
| PUB-3 Enforcement transparency | 1 | Name registration deterministic; governance of root key holders and DNS integration partially opaque |
| PUB-4 Information symmetry | 2 | ENS Labs updates; treasury reports; community calls |
| FAIR-1 Floor protection | 1 | Name costs scale with length; short names expensive ($640+/year for 3-char); no subsidy |
| FAIR-2 Access equity | 1 | Registration permissionless; governance requires ENS tokens; airdrop limited to early registrants |
| FAIR-3 Distribution fairness | 1 | Airdrop to early registrants; 50% community but concentrated among early adopters who registered many names |
| FAIR-4 Governance accessibility | 1 | Delegation available; but Top-1 holder controls 26.7% (highest concentration in sample after exclusions) |
| NDOM-1 Contestability | 2 | Constitution limits DAO scope; veto for constitutional violations; root key multisig backstop |
| NDOM-2 Concentration limit | 1 | HHI 0.135 (high); Top-1 26.7%; Top-10 controls 75.5%; most concentrated Infra protocol |
| NDOM-3 Emergency powers | 2 | Root key holder multisig for DNS emergencies; scope limited by Constitution; membership public |
| NDOM-4 Exit rights | 2 | Liquid ENS; names transferable; no lock-in beyond renewal fees |
| POLY-1 Decision centers | 1 | Working groups (Meta-Governance, Ecosystem, Public Goods, DAO Tooling) with budgets |
| POLY-2 Local adaptation | 1 | Single namespace; no geographic governance; pricing uniform by length |
| POLY-3 Cross-scale coordination | 2 | DNS integration requires ICANN coordination; multi-chain resolution emerging |
| POLY-4 Subsidiarity | 1 | Working groups operational; strategic decisions DAO-level; limited delegation |
| KNOW-1 Price signals | 1 | Registration pricing as demand signal; premium auctions for short names; administrative pricing |
| KNOW-2 Local knowledge | 1 | Registration data reveals naming demand; not structured into governance |
| KNOW-3 Competitive discovery | 1 | Near-monopoly on Ethereum naming; limited competition (Unstoppable Domains, SpaceID) |
| KNOW-4 Information aggregation | 1 | Token-weighted voting; delegate platforms; no structured aggregation |

---

## Scoring Notes and Caveats

1. **Single coder.** All scores assigned by ZZ. Inter-rater reliability testing with a second independent scorer is specified as future work (S2, Reliability Protocol).

2. **Snapshot date.** Evidence as of March 2026. Governance evolves; scores may not reflect post-snapshot changes (e.g., Lido dual governance launch, MakerDAO Endgame completion).

3. **Floor effects.** Anyone Protocol scores 1 on all criteria because it is early-stage, not because of poor design. The rubric does not distinguish "absent by choice" from "absent due to immaturity."

4. **HHI in NDOM-2.** Scores use post-exclusion holding HHI from Table 4. Voting HHI (Table 6) referenced in evidence but does not set the score directly, as voting data covers only 8 of 11 protocols.

5. **Synergy Index range.** 1.00 (Anyone) to 1.90 (Optimism). Compressed because no protocol scores 0 on any full lens and no protocol scores 3 on more than one criterion. The Index is ordinal; 1.90 is not "twice as legitimate" as 1.00.

6. **Helium Knowledge score.** Only protocol scoring 2 on all four Knowledge criteria, reflecting proof-of-coverage, location pricing, competitive hardware deployment, and oracle verification. Consistent with Hayekian emphasis on distributed knowledge through sensing and pricing.

7. **MakerDAO FAIR-3 = 0.** Only zero score in the dataset. 100% insider genesis with no community distribution mechanism. Does not determine governance quality: HHI 0.045 (moderate) shows secondary markets partially decompressed initial concentration over 9 years.

8. **Optimism highest Synergy (1.90).** Driven by two-chamber governance (only protocol with 3 on any criterion: NDOM-1 and PUB-1), compensated delegation, RetroPGF, and constitutional structure. Also the only protocol where delegation distributes rather than concentrates power (0.79x ratio).

9. **Post-exclusion HHI shifts.** AAVE (0.059 to 0.020), UNI (0.101 to 0.032), ARB (0.097 to 0.012) shifted substantially after excluding stkAAVE, Timelock, and FixedDelegateWallet respectively. NDOM-2 scores reflect post-exclusion values; the exclusions themselves are documented in S1.

10. **Wayru abbreviated scoring.** Wayru (DePIN, mesh WiFi) was scored using the 8-criterion philosophical-lens rubric rather than the full 20-criterion criterion-set used for the other 11 protocols. The abbreviated scheme assigns one score per lens (Kantian, Rawlsian, Pettitian, Ostromian, Hayekian, Nussbaum, Floridi, Appiah) rather than 4 per lens. Synergy Index = 0.62 (mean of 8 scores). Holding HHI was not computable for Wayru as it was not included in the primary regression dataset (N/A in Table 4).

---

## 12. Wayru (DePIN, HHI N/A)

*Scored using abbreviated 8-lens philosophical rubric (one score per lens). Protocol is a mesh WiFi DePIN network. HHI not computed (not in primary regression sample).*

| Lens | Score | Evidence |
|------|-------|----------|
| Kantian Publicity | 1 | Basic governance documentation; rules partially transparent but not fully on-chain |
| Rawlsian Fairness | 1 | Node operator access minimal but non-zero; hardware cost accessible; no floor protection |
| Pettit Non-Domination | 0 | No formal contestation mechanism; governance centralized at team/foundation level |
| Ostrom Polycentricity | 0 | Single governance body; no subDAOs, no local adaptation by geography |
| Hayek Knowledge | 1 | Bandwidth and coverage pricing as implicit demand signal; not structured into governance |
| Nussbaum Capability | 0 | No minimum capability thresholds; governance inaccessible to small operators |
| Floridi Integrity | 0 | Limited data integrity verification; network quality measurement nascent |
| Appiah Cosmopolitan | 2 | Explicit global mission (internet access for underserved communities); cross-border deployment design |

**Synergy Index:** 5/8 = **0.62**

Note: Wayru scores reflect early-stage maturity (network launch 2022 to 2023), not poor design intent. The Appiah Cosmopolitan score of 2 is the highest single-lens score and reflects the protocol's stated mission. The zero scores on Non-Domination and Polycentricity are consistent with early-stage DePIN protocols (cf. Anyone Protocol).

---

## 13 to 40. Extended-sample 5-lens scoring (added 2026-05-19)

The original 11 protocols above carry full 20-cell criterion-by-criterion scoring tables (240 cells); GEODNET appears in the summary table at the top of this document with abbreviated 5-lens scores carried from Table 2 of the main manuscript. The 28 protocols documented in this section were scored 2026-05-19 to expand the Synergy Index sample to the full 40-protocol cross-section, addressing the partial-coverage limitation noted in Section 4.8 of the main manuscript. Scoring uses the same 5-lens (Publicity / Fairness / Non-Domination / Polycentricity / Knowledge-use) summary protocol applied to GEODNET and Wayru, with one score per lens (0 to 3) anchored to the 11 fully-scored protocols. Evidence is summarized per lens rather than per criterion; full per-criterion scoring is reserved for future inter-rater reliability cycles.

The scoring methodology for the extended sample follows the same evidence-discipline as the original 11: governance documentation, on-chain proposal records, protocol forum activity, and published treasury / multisig configurations. Evidence-of-record per protocol is summarized below; the structured per-criterion expansion is future work.

### Curve (DeFi, HHI 0.014)

| Lens | Score | Evidence |
|------|-------|----------|
| Publicity | 2.00 | Snapshot + on-chain veCRV proposals; mature governance documentation |
| Fairness | 0.75 | veCRV lock-duration weighting structurally privileges long-lockers; floor mechanisms weak |
| Non-Domination | 1.50 | DAO appeals via 30%-quorum but ve-locking dilutes broad participation |
| Polycentricity | 1.50 | Gauge committee + emission committee + sub-DAOs (yCRV, sdCRV ecosystem) |
| Knowledge-use | 2.00 | Gauge votes aggregate weekly demand signals (high gauge votes -> high emissions) |

**Synergy Index:** arith 1.55, geom 1.47.

### Rocket Pool (DeFi, HHI 0.039)

| Lens | Score | Evidence |
|------|-------|----------|
| Publicity | 2.25 | Active forum + mandatory proposal rationales + on-chain pDAO |
| Fairness | 1.50 | Minipool floor (16 ETH min); node operator caps |
| Non-Domination | 2.00 | pDAO veto + oDAO oversight + GMC (security council) |
| Polycentricity | 2.00 | pDAO (token holders) + oDAO (node operators) + GMC tri-cameral structure |
| Knowledge-use | 1.00 | Basic on-chain gauge mechanisms |

**Synergy Index:** arith 1.75, geom 1.68.

### Jupiter (DeFi, HHI 0.096)

| Lens | Score | Evidence |
|------|-------|----------|
| Publicity | 1.50 | JUP Realms; public proposals; less mature documentation |
| Fairness | 1.00 | LFG launchpad partial floor; allocation skewed insider |
| Non-Domination | 1.00 | Basic voting; no formal appeals architecture |
| Polycentricity | 1.00 | JUP DAO + team; mostly monocentric |
| Knowledge-use | 1.00 | Basic price signals |

**Synergy Index:** arith 1.10, geom 1.08.

### Maple Finance (DeFi, HHI 0.024)

| Lens | Score | Evidence |
|------|-------|----------|
| Publicity | 1.75 | Governance forum; proposals on-chain |
| Fairness | 1.00 | Lender / borrower distinct stakes; no strong floor |
| Non-Domination | 1.50 | GovernorBravo + delegate program; appeals off-chain |
| Polycentricity | 1.00 | Mostly monocentric |
| Knowledge-use | 1.00 | Basic |

**Synergy Index:** arith 1.25, geom 1.21.

### GMX (DeFi, HHI 0.065)

| Lens | Score | Evidence |
|------|-------|----------|
| Publicity | 2.00 | Active forum + Snapshot + on-chain |
| Fairness | 1.00 | Basic |
| Non-Domination | 1.50 | Snapshot-based with broader voter pool |
| Polycentricity | 1.00 | GMX DAO; mostly monocentric |
| Knowledge-use | 1.50 | GLP price signals + dynamic pricing |

**Synergy Index:** arith 1.40, geom 1.35.

### Drift (DeFi, HHI 0.053)

| Lens | Score | Evidence |
|------|-------|----------|
| Publicity | 1.50 | DRIFT Realms; less mature |
| Fairness | 1.00 | Basic |
| Non-Domination | 1.00 | Basic voting |
| Polycentricity | 1.00 | Monocentric |
| Knowledge-use | 1.00 | Basic |

**Synergy Index:** arith 1.10, geom 1.08.

### Ether.Fi (DeFi, HHI 0.042)

| Lens | Score | Evidence |
|------|-------|----------|
| Publicity | 1.50 | Governance forum; proposals on-chain |
| Fairness | 1.00 | Basic |
| Non-Domination | 1.00 | Basic |
| Polycentricity | 1.00 | Monocentric (ETHFI + operator) |
| Knowledge-use | 1.00 | Basic |

**Synergy Index:** arith 1.10, geom 1.08.

### The Graph (L1_L2_Infra, HHI 0.033)

| Lens | Score | Evidence |
|------|-------|----------|
| Publicity | 2.00 | GIP process; public proposals |
| Fairness | 1.50 | GRT staking lowers indexer entry threshold |
| Non-Domination | 2.00 | Council veto + on-chain governance |
| Polycentricity | 2.00 | Indexers + curators + delegators + Council |
| Knowledge-use | 1.50 | Query-fee market signals |

**Synergy Index:** arith 1.80, geom 1.78.

### Polygon (L1_L2_Infra, HHI 0.035)

| Lens | Score | Evidence |
|------|-------|----------|
| Publicity | 2.00 | PIPs + on-chain Polygon Improvement Proposals |
| Fairness | 1.25 | Validator floor (1M MATIC stake) |
| Non-Domination | 1.50 | Foundation veto + community PIPs |
| Polycentricity | 1.50 | PoS chain governance + zkEVM + Foundation |
| Knowledge-use | 1.00 | Basic |

**Synergy Index:** arith 1.45, geom 1.41.

### Hyperliquid (DeFi, HHI 0.005)

| Lens | Score | Evidence |
|------|-------|----------|
| Publicity | 2.00 | Public discussion forum + on-chain governance docs |
| Fairness | 1.00 | Broad airdrop; no post-distribution floor |
| Non-Domination | 1.00 | Basic |
| Polycentricity | 0.00 | Foundation-led; no formal sub-bodies |
| Knowledge-use | 2.00 | Assistance Fund auto-burns trade fees (price-signal-coupled buyback mechanism) |

**Synergy Index:** arith 1.20, geom 0.53. Note: zero on Polycentricity drives geometric mean below 1.0, illustrating weakest-link aggregation sensitivity (see Section 4.8 operationalization-dependency paragraph).

### Balancer (DeFi, HHI 0.029)

| Lens | Score | Evidence |
|------|-------|----------|
| Publicity | 2.00 | BIP process + forum + Snapshot |
| Fairness | 1.00 | veBAL holders + LP holders; basic floor |
| Non-Domination | 1.50 | BAL / veBAL governance + multi-stakeholder |
| Polycentricity | 1.50 | Gauge committee + safety multisig + DAO |
| Knowledge-use | 2.00 | Gauge votes for liquidity allocation (Hayek mechanism) |

**Synergy Index:** arith 1.60, geom 1.55.

### IoTeX (DePIN, HHI 0.189)

| Lens | Score | Evidence |
|------|-------|----------|
| Publicity | 1.50 | Governance documentation public + IIPs |
| Fairness | 1.00 | Validator staking floor; no strong fairness mechanism |
| Non-Domination | 1.00 | Delegate voting; weak appeals |
| Polycentricity | 1.50 | Delegates + foundation; some decentralization |
| Knowledge-use | 1.50 | Dapp gas + machine-data signals (DePIN-specific) |

**Synergy Index:** arith 1.30, geom 1.28.

### WeatherXM (DePIN, HHI 0.148)

| Lens | Score | Evidence |
|------|-------|----------|
| Publicity | 1.50 | WMIPs analog; weather network documentation |
| Fairness | 1.00 | Operator rewards with location-based weighting |
| Non-Domination | 1.00 | Basic |
| Polycentricity | 1.00 | Mostly monocentric foundation |
| Knowledge-use | 2.00 | Weather data quality signals into reward calculation (Hayek mechanism) |

**Synergy Index:** arith 1.30, geom 1.25.

### Grass (DePIN, HHI 0.035)

| Lens | Score | Evidence |
|------|-------|----------|
| Publicity | 1.50 | Basic governance forum |
| Fairness | 1.00 | Basic |
| Non-Domination | 1.00 | Basic |
| Polycentricity | 0.50 | Mostly monocentric |
| Knowledge-use | 1.50 | Bandwidth quality signals |

**Synergy Index:** arith 1.10, geom 1.02.

### Livepeer (DePIN, HHI 0.199)

| Lens | Score | Evidence |
|------|-------|----------|
| Publicity | 1.50 | LIPs + Snapshot proposals |
| Fairness | 1.00 | Orchestrator stake floor (1 LPT min) |
| Non-Domination | 1.00 | Basic |
| Polycentricity | 1.00 | Orchestrator-delegator structure |
| Knowledge-use | 2.00 | Encoding job market signals into bond reward distribution |

**Synergy Index:** arith 1.30, geom 1.25.

### Filecoin (DePIN, HHI 0.022)

| Lens | Score | Evidence |
|------|-------|----------|
| Publicity | 2.00 | Mature FIPs (Filecoin Improvement Proposals); formal process |
| Fairness | 1.25 | Storage provider entry barrier moderate |
| Non-Domination | 2.00 | FIP appeals + Filecoin Foundation oversight + community |
| Polycentricity | 2.50 | FIL Foundation + Protocol Labs + storage providers + community + retrieval markets |
| Knowledge-use | 2.00 | Storage market signals; demand-based compensation |

**Synergy Index:** arith 1.95, geom 1.90. Top of full-sample distribution.

### Render (DePIN, HHI 0.027)

| Lens | Score | Evidence |
|------|-------|----------|
| Publicity | 1.50 | RIPs + Snapshot |
| Fairness | 1.00 | Basic |
| Non-Domination | 1.00 | Basic delegate voting |
| Polycentricity | 1.00 | Mostly monocentric |
| Knowledge-use | 1.50 | GPU job pricing signals |

**Synergy Index:** arith 1.20, geom 1.18.

### Pokt Network (DePIN, HHI 0.090)

| Lens | Score | Evidence |
|------|-------|----------|
| Publicity | 2.00 | PUPs (Pokt Improvement Proposals) |
| Fairness | 1.00 | Node staking floor moderate |
| Non-Domination | 1.50 | PUP voting + DAO |
| Polycentricity | 1.50 | Node operators + portal partners + DAO |
| Knowledge-use | 1.50 | Relay-volume signals |

**Synergy Index:** arith 1.50, geom 1.47.

### LayerZero (L1_L2_Infra, HHI 0.014)

| Lens | Score | Evidence |
|------|-------|----------|
| Publicity | 1.50 | DVN configuration public; less mature governance |
| Fairness | 1.00 | Basic |
| Non-Domination | 1.00 | Basic |
| Polycentricity | 1.00 | DVN diversity but operator-centric |
| Knowledge-use | 1.00 | Basic |

**Synergy Index:** arith 1.10, geom 1.08.

### Wormhole (L1_L2_Infra, HHI 0.012)

| Lens | Score | Evidence |
|------|-------|----------|
| Publicity | 1.50 | Wormhole Improvement Proposals |
| Fairness | 1.00 | Basic |
| Non-Domination | 1.00 | Basic |
| Polycentricity | 1.00 | Guardian set governance |
| Knowledge-use | 1.00 | Basic |

**Synergy Index:** arith 1.10, geom 1.08.

### Morpheus AI (DePIN, HHI 0.046)

| Lens | Score | Evidence |
|------|-------|----------|
| Publicity | 1.50 | Morpheus.os governance docs |
| Fairness | 1.00 | Basic |
| Non-Domination | 1.00 | Basic |
| Polycentricity | 1.00 | Monocentric |
| Knowledge-use | 1.50 | AI agent quality signals (theoretical operationalization) |

**Synergy Index:** arith 1.20, geom 1.18.

### Axelar (L1_L2_Infra, HHI 0.027)

| Lens | Score | Evidence |
|------|-------|----------|
| Publicity | 1.75 | AIP process |
| Fairness | 1.00 | Basic |
| Non-Domination | 1.50 | Validator-set governance with checks |
| Polycentricity | 1.25 | Validator + community + AXL token-governance |
| Knowledge-use | 1.00 | Basic |

**Synergy Index:** arith 1.30, geom 1.27.

### MetaDAO (DeFi, HHI 0.015)

| Lens | Score | Evidence |
|------|-------|----------|
| Publicity | 2.00 | Futarchy is publicly observable by design |
| Fairness | 1.00 | Futarchy weights wealth heavily |
| Non-Domination | 2.50 | Futarchy provides structural contestability (market-based decisions); explicit Pettit operationalization |
| Polycentricity | 0.50 | Single-mechanism futarchy; no formal sub-bodies |
| Knowledge-use | 2.50 | Prediction markets aggregate information by design (strong Hayek mechanism) |

**Synergy Index:** arith 1.70, geom 1.44. Note: low Polycentricity drives substantial arith-geom divergence; geometric-mean penalty highlights the single-mechanism design tradeoff.

### Gitcoin (Social_Dead, HHI 0.022)

| Lens | Score | Evidence |
|------|-------|----------|
| Publicity | 2.25 | Mature GIPs + Snapshot + governance forum |
| Fairness | 2.00 | Quadratic funding for public goods (Rawls floor-protection by design) |
| Non-Domination | 1.75 | Multiple QF rounds + DAO + Foundation |
| Polycentricity | 2.00 | Workstreams + Stewards + community |
| Knowledge-use | 1.50 | QF aggregates dispersed signals |

**Synergy Index:** arith 1.90, geom 1.88. Top of full-sample distribution alongside Filecoin and Optimism.

### Token Engineering Commons (Social_Dead, HHI 0.028)

| Lens | Score | Evidence |
|------|-------|----------|
| Publicity | 1.50 | Commons Hub governance documentation |
| Fairness | 1.50 | Conviction voting for floor protection |
| Non-Domination | 1.50 | Conviction voting structure |
| Polycentricity | 1.50 | Working groups (active pre-stagnation) |
| Knowledge-use | 1.50 | Conviction-voting aggregates time-preferences |

**Synergy Index:** arith 1.50, geom 1.50. Note: stagnation does not alter design-intent scoring; the protocol scored against its institutional architecture rather than current operating activity.

### Aethir (DePIN, HHI 0.087)

| Lens | Score | Evidence |
|------|-------|----------|
| Publicity | 1.00 | Limited public governance documentation |
| Fairness | 0.50 | Heavy team / investor allocation (62%); no community floor mechanism |
| Non-Domination | 1.00 | Basic |
| Polycentricity | 0.50 | Aethir Foundation monocentric |
| Knowledge-use | 1.50 | GPU compute market signals |

**Synergy Index:** arith 0.90, geom 0.82. Bottom of full-sample distribution.

### Hivemapper (DePIN, HHI 0.018)

| Lens | Score | Evidence |
|------|-------|----------|
| Publicity | 1.50 | MIPs (Mapper Improvement Proposals) |
| Fairness | 1.50 | Per-driver caps + AI training data quality scoring |
| Non-Domination | 1.00 | Basic |
| Polycentricity | 1.00 | Mostly monocentric |
| Knowledge-use | 2.50 | AI training quality signals are explicit knowledge-aggregation (strong Hayek mechanism) |

**Synergy Index:** arith 1.50, geom 1.41.

### io.net (DePIN, HHI 0.125)

| Lens | Score | Evidence |
|------|-------|----------|
| Publicity | 1.00 | Early-stage governance documentation |
| Fairness | 1.00 | Basic |
| Non-Domination | 1.00 | Basic |
| Polycentricity | 0.50 | Foundation-led |
| Knowledge-use | 1.50 | GPU compute pricing signals |

**Synergy Index:** arith 1.00, geom 0.94.

---

## Extended-sample scoring caveats (2026-05-19 addition)

The 28-protocol extension above carries the following methodological caveats specific to this expansion cycle (in addition to the original single-coder and snapshot-date caveats in the "Scoring Notes and Caveats" section above):

1. **Five-lens summary rather than 20-cell criterion-by-criterion.** The extension scores one cell per lens rather than four cells per lens. This is a deliberate methodological choice to enable full-sample Synergy Index analysis without overcommitting evidence-collection effort before inter-rater reliability is established. Full per-criterion expansion of the 28 protocols is reserved for future cycles, ideally concurrent with the inter-rater reliability cycle specified in Section 4.8 and S2.

2. **Snapshot-date drift since 2026-03-15.** Evidence for the 28 newly-scored protocols was gathered May 2026. Several protocols' governance architectures have evolved since the original 12 protocols' March 2026 snapshot. Where structural governance changes occurred (e.g., Curve's veCRV ecosystem maturation, Filecoin's FIP process formalization), the May 2026 state is scored; this snapshot heterogeneity is documented for inter-rater reliability cycles to account for.

3. **Conservative scoring anchored to original 12.** New-protocol scores are anchored to the original 11 fully-scored protocols (plus GEODNET from Table 2) as reference. Protocols with mature governance documentation but limited evidence of community contestation were scored conservatively in the Non-Domination dimension; protocols with single-mechanism polycentricity (Hyperliquid foundation-led; MetaDAO futarchy) were scored on the unaltered 0 to 3 scale, allowing zero scores where appropriate.

4. **Sector representation: balanced.** The expansion brings DeFi to N = 15 and DePIN to N = 15 with Infra at N = 8 and Social-dead at N = 2; sector means become DeFi 1.42 / DePIN 1.33 / Infra 1.46 / Social 1.70 (no significant cross-sector Synergy difference at p < 0.05, confirming that the HHI sector-signal does not extend symmetrically to the institutional-design Synergy dimension).
