# Acquisition scope: the 17 protocols not in DefiLlama emissions

**As-of:** 2026-05-29. Scopes emission / incentive / unlock-schedule acquisition for the 17
frame protocols absent from DefiLlama's unlock dataset, so the schedule-method incentive build
and unlock-netting can reach full coverage. Sources gathered VERBATIM in `acquisition_sources/`
(reproducible via the two fetch scripts). Reader MUST re-verify before executing the build.

## Source hierarchy discovered (in priority order)

1. **DefiLlama free CDN** (`defillama-datasets.llama.fi/emissions/<slug>`): 33/50 frame
   protocols (the prior discovery). NOT these 17.
2. **tokenomist.ai/<slug>** (the canonical unlock tracker, formerly TokenUnlocks): curl-able
   verbatim HTML that embeds the allocation + vesting + unlock schedule in the Next.js RSC
   payload. Covers 10 of these 17. Time-phased schedule at `/<slug>/unlock-events`.
3. **CoinGecko Pro `/coins/<id>`** (we have the key): supply metrics + tokenomics description +
   official doc/whitepaper links. Saved for all 17.
4. **Protocol docs** (CoinGecko whitepaper links): schedule parameters (rates, halving, cliffs).
5. **On-chain / Dune**: per-period ACTUAL emissions/burns. Reproducible; we already have DePIN
   burns for DIMO + HONEY (and GEOD/HNT in the DefiLlama set).

SCHEMA NOTE: tokenomist gives allocation% + unlock curve (cumulative), like DefiLlama; per-period
= monthly diff. The "incentives/rewards/inflation" allocation category is the schedule-method
numerator; the "team/investor/strategic" categories are the unlock-netting inputs.

## Per-protocol acquisition (the 17)

| token | sector | tokenomist (verbatim saved) | key incentive/emission split | per-period actuals | priority |
|---|---|---|---|---|---|
| ALGO | L1 | yes (algorand) | Participation Rewards 17.5%, fixed 10B, 2.5B over ~10y to 2030; block rewards 2024+ | Algorand indexer / AlgoNode; Dune | med |
| POL | L1 | yes (polygon-ecosystem-token) | Validator incentives 8.98%/yr + Community treasury 8.98%/yr (the ~2%/yr emission); MATIC migration 82% | PolygonScan emission contract; Dune | med |
| GNO | DeFi | no | fully distributed (max 3M, ~2.64M circ); no ongoing emission | n/a (no emission) | low |
| BONK | DeFi | yes (bonk) | BONK DAO 15.79%, market participants 15.79%, burns ongoing | Solana on-chain burns; Dune | low |
| LPT | DePIN | yes (livepeer) | on-chain inflation (participation-target adjustable), endowment 5%, crowd 63% | Livepeer subgraph / inflation contract; Dune | med |
| RENDER | DePIN | yes (render-token) | Inflation 16.67% (BME), OTOY Treasury 23.3%, Private Sale 18.29% | Solana RENDER program (BME); Dune | high |
| POKT | DePIN | no (slug TBD) | per-relay minting + annual inflation (declining); docs.pokt.network | POKT on-chain mint events; Dune | med |
| IOTX | DePIN | no (slug TBD) | burn-drop emissions; docs.iotex.io / whitepaper PDF | IoTeX on-chain; Dune | med |
| IO | DePIN | yes (io) | Series A 10.15%, Community 10%, network rewards; 800M max | Solana io.net rewards program; docs.io.net/llms.txt | high |
| HONEY | DePIN | yes (hivemapper) | Contributor Rewards 40%; ON-CHAIN BURNS ALREADY GATHERED (hivemapper_burn) | hivemapper_burn_concentration.csv (have) + Solana | covered |
| DIMO | DePIN | no (slug TBD) | issuance/baseline rewards on Polygon; ON-CHAIN BURNS ALREADY GATHERED | dimo_burn_concentration.csv (have) + Polygon | covered |
| WXM | DePIN | yes (weatherxm-network) | Station Rewards 55%, Initial Supporters 30% (4y vest/1y cliff), 10y schedule | Dune dune.com/weatherxm/network-stats (confirmed) | high |
| ANYONE | DePIN | no (docs.anyone.io ?ask= API) | relay/bandwidth rewards; 100M supply | Arbitrum relay-rewards contract; docs.anyone.io | med |
| W | DeFi | yes (wormhole) | Incubation 31%, core/investor vesting; 10B supply | tokenomist unlock-events; on-chain | high |
| WLFI | DeFi | yes (world-liberty-financial) | Community Growth and Incentives 10%, Strategic Partners 5.27%; 100B supply | tokenomist unlock-events; on-chain (recent launch) | high |
| META | DeFi | no (docs.metadao.fi) | MetaDAO futarchy; small (~22.7M supply); little/no incentive emission | docs.metadao.fi; on-chain | low |
| MKR | DeFi | no | fixed ~1M supply; NO emission (Smart Burn Engine buyback/burn); SubDAO farming separate | n/a for emission (burn data on-chain) | low |

## Verbatim sources saved (`acquisition_sources/`)

- `<TOK>_coingecko.json` -- 17 verbatim CoinGecko Pro coin records (supply, links, tokenomics).
- `<TOK>_tokenomist_<slug>.html` -- 10 verbatim tokenomist.ai pages (allocation + unlock data).
- `WXM_docs...md`, `ALGO_emission_websearch...md` -- verbatim WebFetch / WebSearch findings.
- `_coingecko_summary.json` -- extracted supply + homepage/whitepaper links for all 17.
- Fetch scripts: `acquisition_coingecko_coins_fetch_2026-05-29.py`,
  `acquisition_tokenomist_fetch_2026-05-29.py`.

## Recommended acquisition path + effort

- **Highest value, lowest effort (tokenomist + Dune):** RENDER, IO, WXM, W, WLFI (5) -- tokenomist
  unlock-events for the vesting/incentive curve, Dune/on-chain for per-period actuals. The
  schedule-method input is directly assemblable.
- **L1 emission (docs + on-chain):** ALGO, POL -- documented emission policy + on-chain block /
  validator rewards.
- **Already covered (on-chain on hand):** HONEY, DIMO (burns gathered); combine with issuance.
- **DePIN needing on-chain pulls:** LPT, POKT, IOTX, ANYONE -- emission is on-chain (subgraph /
  mint events); route via the Dune skill.
- **No / negligible emission (document and skip):** GNO (distributed), MKR (fixed + burn), META
  (small), BONK (memecoin, burns not emissions).

## Tokenomist slug gaps (7 misses; resolve before fetch)

ANYONE, DIMO, GNO, IOTX, META, MKR, POKT returned no valid tokenomist page on the slug
candidates tried. GNO/MKR/META are low-priority (no/negligible emission). For DIMO/IOTX/POKT/
ANYONE, resolve the slug (tokenomist search) or go straight to on-chain (these are DePIN with
on-chain reward contracts). DIMO + HONEY already have on-chain burns.

## Caveats

tokenomist allocation labels need the same INCENTIVE-vs-INSIDER bucketing as DefiLlama. On-chain
DePIN emissions require per-protocol reward-contract identification (a Dune cycle each).
CoinGecko description tokenomics is prose, not a schedule. Exploratory acquisition scope; the
build is the next cycle.
