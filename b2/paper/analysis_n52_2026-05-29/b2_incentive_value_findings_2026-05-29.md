# Incentive / new-supply value over time: build results (part b) + coverage expansion

**As-of:** 2026-05-29. Build: `b2_incentive_value_timeseries_2026-05-29.py` (reads persisted
CoinGecko daily series; no /tmp, no live-API). Fetch step: `coingecko_fetch_new10_2026-05-29.py`
(the 10 new-cohort daily series, CoinGecko Pro API). Outputs:
`incentive_value_monthly_2026-05-29.csv` (panel), `incentive_value_annual_2026-05-29.csv`,
`b2_incentive_value_results_2026-05-29.json`. Reader MUST re-verify before acting.

## Coverage expansion (the clean win)

- Fetched the 10 missing CoinGecko daily series (the new cohort: SNX via legacy id `havven`,
  GNO, ENA, WLFI, JTO, BONK, KMNO, ALGO, DOT, TAO), saved to `coingecko_new10/`. CoinGecko
  daily coverage of the regression frame goes from 40/50 to **50/50** (49/50 enter the build;
  META is a residual id-mapping ambiguity, `meta-2-2`, left as a documented gap).
- Constructed a monthly new-supply-value series for **49 protocols** (2,266 monthly
  observations). Incentive-VALUE coverage goes from the Token Terminal sparse **9** to a
  constructed **49** (see the honest caveat below on what that value represents).

## HONEST RESULT: the supply-delta proxy measures new-supply value, NOT clean incentives

The calibration is decisive and negative. Constructed trailing-12-month new-supply value vs
Token Terminal annual incentives (the 9 calibration coins):

| coin | constructed ttm | Token Terminal annual | ratio |
|---|---:|---:|---:|
| LPT | $51.0M | $24.6M | 2.1x |
| AAVE | $25.1M | $8.1M | 3.1x |
| OP | $193.6M | $56.6M | 3.4x |
| FIL | $185.5M | $19.7M | 9.4x |
| COMP | $33.0M | $1.2M | 26.9x |
| POL | $445.3M | $9.7M | 46.1x |
| GMX | $3.8M | $0.05M | 70.1x |
| UNI | $215.0M | $0.5M | 400.7x |
| IOTX | -$0.01M | $1.0M | -0.01x |

The ratios (2x to 400x, one negative) show the proxy does NOT isolate liquidity-mining /
incentive emissions. The delta-circulating-supply method captures TOTAL new supply entering
circulation, which for most tokens is dominated by VESTING UNLOCKS, not incentive emissions
(spot-check: UNI 2025-11 had +31.1M new supply worth $203M, a lumpy treasury/vesting unlock,
versus only $0.5M/yr of actual Token Terminal incentives). The negative IOTX (net supply
decline from burns) further shows net new-supply is not gross incentives.

Conclusion: the proxy expands COVERAGE to 49 but the quantity it measures is "net new-supply
value," an upper-bound dominated by unlocks. It is NOT a substitute for incentive / mining-
reward value. It should be reported as new-supply value, never as audited incentives.

## What this means for the original ask

- "Populate more of 9/35": coverage of a NEW-SUPPLY-VALUE series is now 49/50. But clean
  incentive-value coverage remains the Token Terminal 9 plus the on-chain DePIN anchors; the
  proxy does not fill the incentive-specific gap.
- To get PURE incentive / mining-reward value for all coins requires the SCHEDULE method
  (emission_model / inflation_rate / halving_schedule from `protocol_codebook` times price),
  or netting vesting unlocks out of the supply delta via the unlock schedules in
  `allocation_design_variables` / `protocol_codebook`. That is the next-cycle build per the
  scope memo (`b2_incentive_value_timeseries_SCOPE_2026-05-29.md`, method 2), now motivated by
  the calibration evidence here.

## Descriptive (new-supply value by sector, trailing 12 months, positive only)

DeFi $3.91B, L1 $2.30B, DePIN $0.80B. Driven by vesting-unlock magnitude and token count,
not incentive design; interpret with the unlock-dominance caveat.

## Caveats

Net new-supply value conflates emissions, scheduled unlocks, and burns. Implied circulating
supply = market_cap/price inherits CoinGecko's circulating-supply methodology (step-changes on
relisting add noise). Trailing-12-month window. Exploratory; not a primary result.
