# SCOPE: incentive / mining-reward VALUE over time (construction from emission schedules x price)

**As-of:** 2026-05-29. This is a SCOPE / spec memo, not an executed build (per the author's
"scope it as a separate cycle"). It specifies how to construct a time-series of incentive /
mining-reward USD value for the cross-section, from data already on hand. Reader MUST re-verify
against live canonical state before executing.

## Objective

Produce a per-protocol monthly time-series of the USD value of token incentives / mining
rewards (emissions entering circulation), plus a cross-protocol panel, to replace the current
single-point annual incentive figures (`incentives_annual_usd`, present for only 9 of 35
protocols from Token Terminal) with a longitudinal series for all covered coins. This feeds
the subsidy / net-deflation analysis (S2R, subsidy_ratio) with a time dimension and supports
event-study and panel extensions.

## Data on hand (no new acquisition required for the proxy method)

- **CoinGecko daily series, 59 coins** (`/Users/zach/b2-governance-data/data/coingecko/<coin>.csv`;
  approximately 2,016 daily rows each): `date, price_usd, market_cap_usd, volume_usd, OHLC`.
  KEY: implied circulating supply over time = `market_cap_usd / price_usd` (validated:
  DIMO recovers 85.1M -> 497.2M tokens across 2023-04 to 2026-04, 1,095 daily points).
- **Emission-model metadata** (`data/processed/protocol_codebook.csv`): `emission_model`,
  `inflation_rate_annual_pct`, `decay_rule`, `halving_schedule`, `max_supply`, `total_supply`,
  `launch_date`, `vesting_months`, `unlock_schedule_description`.
- **Allocation splits** (`tokenomist_allocations.csv`, `allocation_design_variables.csv`:
  `locked_pct`, `unlocked_pct`, `reserve_pct`, `community_pct`) to separate emissions from
  vesting unlocks where possible.
- **Calibration anchors:** Token Terminal `incentives_annual_usd` (9 coins, annual);
  on-chain DePIN emissions (`geodnet_monthly_emissions.csv`, `helium_burn_concentration.csv`,
  `hivemapper_burn_concentration.csv`).

## Method (recommended: hybrid, calibrated)

1. **Supply-delta value proxy (all 59 coins; validated).** For each month,
   new_supply_t = circ_t - circ_{t-1} (circ = market_cap/price); incentive_value_proxy_t =
   new_supply_t * mid_price_t. This is the fast, universal path.
   - CAVEAT: delta-circulating conflates emissions + scheduled unlocks + burns; it is an
     UPPER-bound proxy for "new supply value," not pure mining rewards.
2. **Schedule method (subset with clean schedules; purer).** For protocols with a defined
   emission/halving schedule in `protocol_codebook` (PoW/PoS-emission and halving-based DePIN),
   compute scheduled per-period emissions directly x price. Use for the DePIN subset where the
   mining-reward concept is well-defined.
3. **Calibrate + reconcile.** Anchor the annual sum of the monthly series to Token Terminal
   `incentives_annual_usd` (9 coins) and to the on-chain DePIN emissions (3 protocols);
   report the proxy-vs-anchor ratio per calibration coin as a quality flag.

## Deliverable

- `incentive_value_monthly_2026-05-29.csv`: protocol, month, implied_circ_supply, new_supply,
  mid_price, incentive_value_usd, method (delta-proxy / schedule), calibration_flag.
- A cross-protocol panel + a findings note (which sectors emit the most value over time; how
  incentive value tracks price cycles; subsidy_ratio with a time dimension).
- Reproduction script; no /tmp, no live-API (reads the persisted CoinGecko series).

## HALT / caveats

- The delta-circulating proxy is NOT pure mining rewards (includes unlocks/burns). Label it
  honestly as "new-supply value" unless the schedule method is used. Do not present the proxy
  as audited emissions.
- CoinGecko circulating-supply implied from market_cap/price inherits CoinGecko's circulating-
  supply methodology (which can step-change on listing/relisting); smooth or flag discontinuities.
- 59-coin CoinGecko coverage vs the 50-protocol regression frame: confirm the join (some frame
  protocols may lack a daily file; some daily files are non-frame coins).

## Effort

Real build, not a quick add. Estimate: the delta-proxy path for all 59 coins + calibration is
roughly one focused cycle; adding the schedule method for the DePIN subset is a second. Route
as a dedicated dispatch (workflow-clone `handoff/dispatch/`) per lane discipline.
