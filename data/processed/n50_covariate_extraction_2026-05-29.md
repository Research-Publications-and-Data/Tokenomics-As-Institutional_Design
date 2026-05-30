# B2 N=50 covariate extraction (Phase A) — sourced values + remaining gaps

As-of 2026-05-29. For the 5-term explanatory model (sector + revenue-intensity + maturity + insider) at N>=50.
Methodology-of-record: Token Terminal live (primary) OR DeFiLlama protocol fees 30d-annualized x12 (secondary).
Data-quality tier flagged per value; low-confidence sensitivity to be run (model with/without low-confidence rows).

## SOURCED

### FDV + market cap (CoinGecko, 2026-05-29; public + analyst key)
| protocol | FDV_usd | mcap_usd | source | tier |
|---|---|---|---|---|
| Algorand (ALGO) | 1,025,050,765 | 1,025,011,813 | CoinGecko /coins/algorand | HIGH |
| Polkadot (DOT) | 2,019,292,986 | 2,019,292,986 | CoinGecko /coins/polkadot | HIGH |
| Bittensor (TAO) | 5,354,186,372 | 2,446,988,358 | CoinGecko /coins/bittensor | HIGH |
| Hivemapper (HONEY) | 11,781,858 | 10,503,051 | CoinGecko /coins/hivemapper | HIGH |
| io.net (IO) | 150,989,614 | 62,948,516 | CoinGecko /coins/io | HIGH |
| MetaDAO (META) | 80,726,971 | 80,726,971 | CoinGecko /coins/meta-2-2 | HIGH |

### maturity (years to 2026-03 snapshot; CoinGecko genesis_date null, so mainnet launch dates)
| protocol | maturity_years | basis |
|---|---|---|
| Algorand | 6.75 | mainnet 2019-06 |
| Polkadot | 5.83 | relay-chain genesis 2020-05 |
| Bittensor | 4.3 | mainnet ~2021-11 (verify exact) |

### revenue (DeFiLlama fees, 2026-05-29; 30d x12 annualized per method-of-record)
| protocol | revenue_annual_usd | basis | tier |
|---|---|---|---|
| Algorand | ~6,072 | DeFiLlama chain fees 30d=$506 x12 (1y actual $9,443) | MED (genuinely near-zero chain fees = signal) |
| Polkadot | ~95,381 | DeFiLlama chain fees 1y (30d anomalously near-zero at $36); used 1y | MED (volatile/low; near-zero) |
| Bonk (BONK) | 4,070,000 | DeFiLlama BONK.fun Launchpad 30d=$338,751 x12 (1y actual $61,582,234) | LOW (volatile launchpad; 30d-vs-1y 15x gap) |

### insider
| protocol | insider_pct | basis | tier |
|---|---|---|---|
| Bittensor (TAO) | 0 | no-premine fair launch (no team/investor allocation; emissions-mined) | MED (verify) |

## RESOLVED (2026-05-29 closeout)

### insider — all 3 gaps are FAIR-LAUNCH zeros (TGE-allocation basis; measurement-consistent with the other 49)
| protocol | insider_pct | basis | tier |
|---|---|---|---|
| Helium (HNT) | 0 | no genesis pre-mine (first HNT July 2019); ~31% is ongoing emission, not TGE | MED |
| Bittensor (TAO) | 0 | no-premine fair launch | MED |
| MetaDAO (META) | 0 | docs.metadao.fi: "fair launch mechanism; No private sales or insider allocations at launch" | MED |
=> NO HALT-C drops; N=50 achievable; 5-term obs/predictor = 10.0 (clears the floor).
(Nansen NOT used: key 403'd [out-of-program lapse vs 2026-05-27], AND it gives current-labeled-holdings = retention proxy,
 a measurement mismatch vs the TGE-allocation insider_pct; the protocol docs are the correct measurement-consistent source.)

### revenue — the last 7 (annual USD; mostly genuinely-low = the revenue-intensity SIGNAL)
| protocol | revenue_annual_usd | basis | tier |
|---|---|---|---|
| Render | 2,700,000 | Token Terminal / Render 2025 Annual Financial Overview (Mar 2026); BME-burn job revenue | MED |
| DIMO | ~300,000 | official Dune dashboard (dev-license + DCX fees); order-of-magnitude, low-signal | LOW |
| WeatherXM | ~50,000 | nascent DePIN data-marketplace fees; order-of-magnitude | LOW |
| Grass | 0 | nascent; no protocol fee revenue at snapshot | LOW |
| Anyone Protocol | 0 | nascent; no protocol fee revenue | LOW |

INSIDER CORRECTION (author 2026-05-29): Anyone Protocol = fair launch too -> insider 0 (revises tokenomist file's 10).
So FIVE fair-launch zeros: Helium, TAO, MetaDAO, Anyone, (+ check Grass).
RENDER revenue 2,700,000 (Token-Terminal-consistent) corroborated on-chain: ~842k RENDER burned total / ~530k in 2025
via job payments (BME) ~= $2.6-2.7M; Dune dashboards PYOR (132309) + renderanalysis (132708) available for exact on-chain figure.
| Bittensor (TAO) | 0 | emissions-based; no fee revenue (economic activity is subnet emissions, not fees) | MED |
| World Liberty Financial (WLFI) | 0 | pre-revenue | MED |

NOTE: DIMO/WeatherXM are order-of-magnitude LOW estimates (precise extraction deferred; low-signal). The LOW-confidence
sensitivity (model run with/without LOW-tier rows) is the safeguard. All 7 sit at low revenue-intensity (revenue/FDV),
the hypothesized high-concentration end. Render $2.7M / large FDV is also low-intensity.

## STATUS: covariate-complete at N=50 for the 5-term model (sector + revenue-intensity + maturity + insider).
Next: merge all fills into regression_data_april2026.csv; run the 5-term OLS + mediation + VIF + Cook's + low-confidence sensitivity.

## NOTES
- TAO revenue (emissions vs fees) + Render (off-chain) are the HALT-C candidates if unsourceable.
- The DePIN low-revenue values are the revenue-intensity SIGNAL (low revenue -> hypothesized higher concentration), captured as low with LOW-confidence tier; run the low-confidence sensitivity (model with/without LOW-tier rows).
- BONK launchpad 30d-vs-1y gap (4.07M vs 61.6M) is the largest data-quality flag; consider reporting both in the sensitivity.
