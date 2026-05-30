# Dune dashboard gap-fill for the 17 not-in-DefiLlama protocols

**As-of:** 2026-05-29. Addendum to `b2_17_acquisition_SCOPE_2026-05-29.md`: pre-built Dune
dashboards / queries that supply per-period (monthly/daily) emission, reward, inflation,
unlock, or burn token amounts for the 17 gap protocols. Found via the Dune MCP
(searchDuneDashboards / searchDuneQueries) plus a 17-agent fan-out. Structured data:
`acquisition_sources/dune_dashboards_gapfill_2026-05-29.csv` (+ `_full_.json`). Reader MUST
re-verify (re-run the query) before building on any specific dashboard.

## Coverage: 15 of 17 now have a pre-built Dune source

| token | best pre-built Dune source | official / verified | covers (per-period) |
|---|---|---|---|
| RENDER | dune.com/tobiases/render-emission-breakdown ; dune.com/pyor_xyz/render-network ; burn query 5656074 | analyst (PYOR, Tokenomist) | emissions + burns (BME, Solana) |
| IO | dune.com/ionet/ionettokeneconomicactivity ; queries 5180192 (burns) + 5194567 (emission schedule) | OFFICIAL (ionet team) | emissions + unlocks + burns |
| WXM | dune.com/weatherxm/network-stats ; query 6933258 | OFFICIAL + a session-built query (verified) | mints (emissions) + burns, monthly + USD |
| LPT | query 1137991 (livepeer_arbitrum.BondingManager_evt_Reward) ; dune.com/larry/livepeer | verified pre-existing | per-round LPT reward emissions |
| POKT | query 4026824 ; dune.com/frytos/Pocket-Network | community | mint per relay / inflation / burn |
| IOTX | dune.com/iotex_devrel/iotex ; query 6933265 | OFFICIAL team + a session-built query | emissions + burns |
| ANYONE | dune.com/anyoneprotocol/network ; query 6933263 | OFFICIAL + a session-built query | relay-rewards emissions + burns |
| POL | query 5966871 (POL Staking stats: RootChainProxy NewHeaderBlock rewards) | verified pre-existing | validator reward emissions, daily |
| HONEY | dune.com/gabe_hivemapper/hivemapper ; dune.com/pyor_xyz/hivemapper | OFFICIAL + analyst | contributor-reward emissions + burns (also on-chain burns on hand) |
| DIMO | dune.com/dimo_network/dimo ; query 6346970 (weekly baseline issuance) | OFFICIAL team + verified query | baseline issuance, weekly (also on-chain burns on hand) |
| BONK | query 5571873 | community | burns + supply |
| W | dune.com/gjgd/wormhole-tokens | community | token flows (per-period unlocks weak; pair with tokenomist) |
| WLFI | dune.com/smart_ape/wlfi-unlocks-tracker ; dune.com/jtai/world-liberty-financial | analyst | unlocks + emissions + supply |
| MKR | query 6816280 ; 3748833 | community | burns (Smart Burn Engine) + supply -- NO emission |
| META | query 4121914 | community | emissions + burns + supply (small) |
| ALGO | NONE found on Dune | -- | use on-chain block rewards (Algorand indexer / AlgoNode) + the algorand.foundation schedule |
| GNO | NONE found | -- | n/a (fully distributed; no ongoing emission) |

Spot-verified this session via getDuneQuery (SQL inspected, executions completed): WXM 6933258
(WXM mints from 0x0 + burns to 0xdead, monthly + USD), POL 5966871 (NewHeaderBlock validator
rewards, daily + APR), LPT 1137991 (BondingManager Reward events), DIMO 6346970 (weekly baseline
issuance from the rewards contract). All target the correct emission/reward source.

## Combined data path for the schedule-method / unlock-netting build (all 50)

- DefiLlama free CDN: 33 protocols (21 incentive-ready, 29 insider-ready).
- tokenomist.ai verbatim: 10 of these 17 (allocation + unlock curves).
- Dune pre-built dashboards: 15 of these 17 (per-period on-chain emission/reward/burn actuals).
- Net: every frame protocol except ALGO (on-chain) and GNO (no emission) has a per-period
  emission/reward/unlock source identified. The build can proceed without further discovery.

## Process note (transparency + Dune cost-discipline)

The 17-agent fan-out was asked to SEARCH for pre-built dashboards. The autonomous agents (with
full Dune MCP access via ToolSearch) went further and CREATED + EXECUTED three gap-filling
queries (the `TS-B2-DePIN-0X` series: WXM 6933258, IOTX 6933265, ANYONE 6933263 on the team
account), spending Dune credits (period usage 718/4000 at check time; well within quota). These
are useful working artifacts, but it is scope-creep relative to a search-only ask. For future
read-only fan-outs, constrain the agent tool set or instruction to search-only to avoid credit
spend. The session-built queries are flagged above; the rest are pre-existing community/official
dashboards.

## Caveats

Dashboard widgets can be point-in-time KPI tiles rather than downloadable per-period series;
confirm the specific widget yields a monthly/daily token-amount column before building. Re-run
stale queries. Community dashboards are unverified beyond the SQL spot-check above. ALGO and the
on-chain DePIN actuals still need a per-protocol Dune/indexer pull where no hosted series exists.
