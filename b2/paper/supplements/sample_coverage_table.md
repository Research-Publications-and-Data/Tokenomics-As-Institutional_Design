# Sample-coverage table (Supplementary Table SX)

Per-cluster N composition for the cross-sectional analyses in B2.

## Cluster A: Primary chain (governance concentration cross-section)

| N | Definition | Composition |
|---|---|---|
| 40 | Full sample (all protocols with HHI computed) | Aave, Aethir, Anyone Protocol, Arbitrum, Axelar, Balancer, Compound, Curve, DIMO, Drift, ENS, Ether.Fi, Filecoin, GEODNET, GMX, Gitcoin, Grass, Helium, Hivemapper, Hyperliquid, IoTeX, Jupiter, LayerZero, Lido, Livepeer, MakerDAO, Maple Finance, MetaDAO, Morpheus AI, Optimism, Pokt Network, Polygon, Render, Rocket Pool, The Graph, Token Engineering Commons, Uniswap, WeatherXM, Wormhole, io.net |
| 37 | Allocation-covariate subset (insider_pct populated) | Aave, Aethir, Anyone Protocol, Arbitrum, Axelar, Balancer, Compound, Curve, DIMO, Drift, ENS, Ether.Fi, Filecoin, GEODNET, GMX, Gitcoin, Grass, Hivemapper, Hyperliquid, IoTeX, Jupiter, LayerZero, Lido, Livepeer, MakerDAO, Maple Finance, Morpheus AI, Optimism, Pokt Network, Polygon, Render, Rocket Pool, The Graph, Uniswap, WeatherXM, Wormhole, io.net |
| 30 | DePIN-vs-DeFi cross-sector subset (Mann-Whitney; Cohen's d) | Aave, Aethir, Anyone Protocol, Balancer, Compound, Curve, DIMO, Drift, Ether.Fi, Filecoin, GEODNET, GMX, Grass, Helium, Hivemapper, Hyperliquid, IoTeX, Jupiter, Lido, Livepeer, MakerDAO, Maple Finance, MetaDAO, Morpheus AI, Pokt Network, Render, Rocket Pool, Uniswap, WeatherXM, io.net |

## Cluster B: Subsidy (orthogonal)

| N | Definition | Composition |
|---|---|---|
| 20 | Cross-sector subsidy with Livepeer (subsidy_ratio_onchain populated) | Aave, Aethir, Compound, Curve, DIMO, Ether.Fi, Filecoin, GEODNET, GMX, Helium, Hivemapper, IoTeX, Lido, Livepeer, MakerDAO, Maple Finance, Morpheus AI, Render, Uniswap, io.net |
| 19 | Cross-sector subsidy excluding Livepeer (excl-LPT) | Aave, Aethir, Compound, Curve, DIMO, Ether.Fi, Filecoin, GEODNET, GMX, Helium, Hivemapper, IoTeX, Lido, MakerDAO, Maple Finance, Morpheus AI, Render, Uniswap, io.net |
| 9 | DeFi within-sector subsidy | Aave, Compound, Curve, Ether.Fi, GMX, Lido, MakerDAO, Maple Finance, Uniswap |

## Cluster C: Participation (orthogonal)

| N | Definition | Composition |
|---|---|---|
| 13 | Current canonical participation sample (per F-X-12) | Pulled from voter-participation merge; not all in primary regression dataset |

## Cross-cluster note

Different cluster N values reflect data availability for the specific test, not arbitrary exclusions. Every cell is computed from the smallest N for which the underlying covariate is populated.
