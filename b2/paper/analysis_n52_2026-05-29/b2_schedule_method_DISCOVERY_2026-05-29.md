# DISCOVERY: data gathered for the schedule-method incentive build + unlock-netting

**As-of:** 2026-05-29. Gathers and characterizes every input needed to build pure incentive /
mining-reward value over time (the schedule method) and to net vesting unlocks out of the
supply-delta proxy (unlock-netting). Reader MUST re-verify before executing the build.

Artifacts (in `defillama_emissions/`):
- `defillama_emissions_gather_2026-05-29.py` (resolve + validate slugs + first extract)
- `defillama_emissions_extract_2026-05-29.py` (CORRECTED per-period extraction; run this)
- `defillama_readiness_inventory_2026-05-29.csv` (per-protocol readiness)
- `defillama_monthly_emissions_unlocks_2026-05-29.csv` (3,614 rows: incentive emission tokens,
  insider unlock tokens, burned tokens, by token-month; 33 protocols)

## The source (the key find): DefiLlama free dataset CDN

`https://defillama-datasets.llama.fi/emissions/<slug>` returns, FREE (the `/api/emissions`
list/per-protocol endpoints are paywalled), the full unlock + emission schedule:
- `documentedData.data[]` = per-CATEGORY series (e.g. "Farming Incentives", "Staking Rewards",
  "team", "investors", "advisors", "community", "airdrop"), each with per-day points
  `{timestamp, unlocked, rawEmission, burned}`.
- `gecko_id` for slug validation + joining to our CoinGecko price series.
- Slug list (free): `.../emissionsProtocolsList` (327 protocols).

SCHEMA GOTCHA (caught + fixed): `rawEmission` is CUMULATIVE (monotonic, equal to `unlocked`).
Per-period emission = month-over-month DIFF of the cumulative, NOT the sum. Summing it
overcounts by ~5 orders of magnitude (the corrected extractor diffs).

Category mapping: INCENTIVE = incentives / farming / emission / reward / staking / liquidity /
mining; INSIDER = team / investor / advisor / insider / private / seed / strategic / founder.

## Readiness (50 frame protocols)

- **DefiLlama unlock curve VALID: 33/50** (slug resolved + gecko_id matched). Slug-resolution
  caveats fixed: POL, W, META, IO, WLFI are NOT in DefiLlama (the fuzzy matcher had grabbed
  polkadot/wombex/metars/iota/worldcoin; removed). ATH/HYPE/BAL/PUMP/FXS/MPL_SYRUP/DOT are
  correct (gecko-id naming differences only).
- **Schedule-method ready (an INCENTIVE category): 21** -- AAVE, AXL, BAL, COMP, DOT, DRIFT,
  ETHFI, FXS, GEOD, GMX, GRASS, GRT, HYPE, KMNO, LDO, MPL_SYRUP, PUMP, RPL, SNX, TAO, UNI.
- **Unlock-netting ready (an INSIDER category): 29** -- ARB, ATH, AXL, BAL, COMP, CRV, DOT,
  DRIFT, ENA, ENS, ETHFI, FIL, FXS, GEOD, GRASS, GRT, HNT, HYPE, JTO, JUP, KMNO, LDO, MPL_SYRUP,
  OP, PUMP, RPL, SNX, UNI, ZRO.
- **On-chain emission/burn already gathered (DePIN, for the not-in-DefiLlama subset):** GEOD
  (geodnet_monthly_emissions), HNT (helium burns), HONEY (hivemapper burns), DIMO (dimo burns).
- **Not in DefiLlama, need on-chain or proxy: 17** -- ALGO, ANYONE, BONK, DIMO, GNO, HONEY, IO,
  IOTX, LPT, META, MKR, POKT, POL, RENDER, W, WLFI, WXM (DIMO + HONEY covered by on-chain burns).

## Validation: the schedule method is the right quantity (and far better than the proxy)

DefiLlama incentive-emission VALUE (incentive tokens x CoinGecko price, trailing 12 calendar
months) vs Token Terminal annual incentives:

| coin | DL incentive value | Token Terminal | ratio |
|---|---:|---:|---:|
| AAVE | $35.2M | $8.1M | 4.3x |
| UNI | $20.0M | $0.5M | 37x |
| GMX | $2.1M | $0.05M | 38x |
| COMP | $0 (no scheduled emit in window) | $1.2M | n/a |

The schedule method calibrates to within single-digits-to-tens of Token Terminal (AAVE 4.3x),
versus 2x to 400x for the supply-delta proxy and ~19,000x for the buggy-cumulative-sum. The
residual 4x to 38x gap is DEFINITIONAL, not a bug: DefiLlama's incentive series is the
SCHEDULED emission allocated to incentive programs (Farming + Staking Rewards), while Token
Terminal counts RECOGNIZED / distributed incentive expense (narrower; e.g. UNI has scheduled
incentive reserves that are not actively distributed). Both are legitimate; they measure
scheduled-allocation vs recognized-expense.

## Recommended build (now fully specified)

1. **Schedule method, 21 protocols:** incentive_value_t = incentive_emission_tokens_t (DefiLlama
   monthly delta) x CoinGecko mean monthly price. This is the clean incentive/mining-reward
   value over time. Label as SCHEDULED incentive emission value (distinct from recognized).
2. **Unlock-netting, 29 protocols:** emission_proxy_t = (delta-circulating - insider_unlock_t)
   x price, to strip vesting unlocks out of the supply-delta proxy where no INCENTIVE category
   exists. Combine with the schedule method where both exist (cross-check).
3. **On-chain fallback:** GEOD/HNT/HONEY/DIMO from the on-chain emission/burn files.
4. **Residual proxy-only:** ALGO, BONK, GNO, IO, META, POL, MKR, IOTX, WXM, ANYONE, LPT,
   RENDER, POKT, W, WLFI -- supply-delta proxy with the new-supply-value caveat, or further
   acquisition (token unlock trackers, protocol docs).

Calibration anchors for the build: Token Terminal annual (9 coins) for recognized-expense
cross-check; the on-chain DePIN emissions for GEOD/HNT/HONEY/DIMO.

## Caveats

DefiLlama schedules are forward-dated (some extend to 2056/2069); use a trailing calendar
window. Incentive vs recognized-expense definitional gap (above). gecko_id join needed for the
USD conversion. Slug list is a point-in-time snapshot (327 protocols). Exploratory discovery,
not a finished build; the build itself is the next cycle, now fully sourced.
