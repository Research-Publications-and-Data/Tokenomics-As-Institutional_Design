# S4: Governance Events Table

Governance events referenced in the paper, organized by type. Each event is linked to the hypothesis or finding it supports. Events are observational; no causal claims are made.

## Structural Governance Events

| Event | Protocol | Date | Type | Description | Paper reference |
|-------|----------|------|------|-------------|----------------|
| EIP-1559 | Ethereum | Aug 2021 | Fee mechanism | Hard-coded fee burn replacing first-price auction; removed ~5.3M ETH by mid-2025 | H3.3 (sinks before faucets); Section 2.2.2 |
| Steem-to-Hive fork | Steem/Hive | Mar 2020 | Hostile takeover + fork | Justin Sun acquired Steem stake; community forked to Hive, exercising ultimate contestability | H3.2 (contestability); Section 3 motivating evidence |
| HIP-147 | Helium | 2024 | Reward reform | Restructured IoT reward distribution; accepted by community including operators whose rewards decreased | H3.1 (publicity); Section 6.1 |
| Helium L1-to-Solana migration | Helium | Apr 2023 | Chain migration | Moved from custom L1 to Solana; governance via veHNT | Table 4 notes |
| SubDAO creation | Helium | 2022-2023 | Governance restructuring | IoT and Mobile subDAOs with independent treasuries and parameters | H3.5 (polycentricity); Helium scoring |
| Endgame restructuring | MakerDAO/Sky | 2023-2026 | Governance restructuring | SubDAO model; rebranding from MakerDAO to Sky Protocol; USDS launch alongside DAI | Section 1; MakerDAO scoring |
| Bitcoin supply cap | Bitcoin | 2009 | Monetary policy | Hard-coded 21M supply cap as maximally public monetary rule | H3.1 (publicity); Section 3 motivating evidence |

## Token Distribution Events

| Event | Protocol | Date | Type | Description | Paper reference |
|-------|----------|------|------|-------------|----------------|
| UNI airdrop | Uniswap | Sep 2020 | Airdrop | 400 UNI to every historical user; 60% community allocation | Section 5.3 (distribution design) |
| ARB airdrop | Arbitrum | Mar 2023 | Airdrop | Large community airdrop; 11.62% to users; 1.13% to DAOs | Table 4; allocation data |
| OP airdrop (multi-season) | Optimism | Jun 2022+ | Airdrop series | Multiple airdrop seasons tied to protocol usage and governance participation | Section 5.3; delegation discussion |
| COMP liquidity mining | Compound | Jun 2020 | Yield farming | COMP distribution through lending/borrowing activity; initiated "DeFi Summer" | Section 5.3 (compression mechanisms) |
| DIMO device mining | DIMO | 2022+ | Device mining | Token rewards for connected vehicle data; hardware-gated distribution | Table 4; DePIN discussion |
| Hyperliquid community allocation | Hyperliquid | Nov 2024 | Airdrop | 31% community airdrop; 0% VC allocation; natural experiment for distribution design | Table 4 notes; natural experiment discussion |

## Delegation and Governance Activity Events

| Event | Protocol | Date | Type | Description | Paper reference |
|-------|----------|------|------|-------------|----------------|
| Optimism delegate programs | Optimism | 2022-2026 | Funded delegation | Compensated delegate programs; reduced voting concentration (hhi_ratio 0.79x) | Section 5.4; Table 6 |
| Arbitrum delegate programs | Arbitrum | 2023-2026 | Funded delegation | Delegate incentive programs; paradoxically high delegation amplification (4.3x) | Section 5.4; Table 6 |
| Lido dual governance | Lido | 2024-2026 | Governance reform | Proposal for stETH holders to participate in governance alongside LDO holders | Lido scoring notes |
| Uniswap fee switch debate | Uniswap | 2022-2026 | Governance dispute | Multi-year debate over activating protocol fee; multiple temperature checks | Uniswap scoring notes |
| Compound Governor Bravo | Compound | 2021 | Governance upgrade | Upgraded from Alpha to Bravo; added proposal threshold, voting delay | Section 5.3 |

## Market and Stress Events (Referenced for Context)

| Event | Date | Type | Protocols affected | Description | Paper reference |
|-------|------|------|-------------------|-------------|----------------|
| SVB bank failure | Mar 2023 | Bank run | Circle (USDC), MakerDAO (DAI) | USDC depegged 13%; DAI contagion via PSM | A1 cross-reference; B2 methodology notes |
| BUSD wind-down | Feb 2023 | Regulatory order | Paxos, Binance | NYDFS ordered Paxos to stop minting BUSD; supply declined $16.6B to $40M | A1, A3 cross-reference |
| FTX collapse | Nov 2022 | Exchange failure | Multiple | Reduced trust in centralized entities; accelerated governance decentralization narrative | Literature review context |
| Terra/LUNA collapse | May 2022 | Algorithmic stablecoin failure | Terra | Algorithmic peg failure; $40B+ value destroyed | Literature review context |

## Measurement Events (Affecting Data Quality)

| Event | Date | Type | Description | Paper reference |
|-------|------|------|-------------|----------------|
| Dune labels update | Feb 2026 | Data source change | labels.addresses table expanded; exchange labels grew; HHI values shifted for re-runs | S1 (measurement notes); Section 4.3 |
| Helius holder correction | Mar 2026 | Data correction | Solana SPL holders recollected via Helius DAS API; META 29→5,067, DRIFT 104→27,888 | Section 4.2; S1 (Solana measurement) |
| Maple MPL-to-SYRUP migration | 2024 | Token migration | MPL holders migrated to SYRUP (100:1 ratio); migration contract excluded from HHI | exclusions_log.csv; S1 (multi-chain merging) |
| RENDER Ethereum-to-Solana migration | 2023 | Token migration | RNDR (ERC-20) migrated to RENDER (SPL); Wormhole bridge excluded | exclusions_log.csv; S1 |

## Hypothesis-Event Mapping

| Hypothesis | Supporting events | Evidence grade |
|------------|-------------------|----------------|
| H3.1 Publicity-Legitimacy | EIP-1559 (transparency produces trust), Bitcoin supply cap, HIP-147 (public process succeeded) | Descriptive |
| H3.2 Contestability-Non-Domination | Steem-to-Hive fork (ultimate contestability), HHI cross-section (concentration data) | Descriptive |
| H3.3 Sinks Before Faucets | EIP-1559 (fee burn as sink), Helium S2R trajectory (B3) | Not directly tested in B2 |
| H3.4 Service over Presence | DePIN device mining events; requires operational data not collected | Indirect |
| H3.5 Polycentric Adaptation | Helium subDAO creation, Optimism two-chamber governance | Indirect |
