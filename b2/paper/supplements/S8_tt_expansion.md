# Supplementary File S8: Token Terminal Expansion — Subsidy-Concentration Analysis

**Date:** 2026-04-02
**Status:** Robustness check (additive; primary specification is on-chain N=20 in §5.7)

---

## Sample Construction

Subsidy ratios for 13 DeFi and Infrastructure protocols are computed from Token Terminal revenue and incentive data using cumulative 35-month values (February 2023–January 2026). DePIN subsidy ratios use annualized on-chain burn revenue and mint emissions (Dune Analytics) as in the primary analysis (see §4.3). Two DePIN protocols are excluded from this expanded sample: Livepeer (subsidy ratio = 88.5×, 3.5-sigma outlier explicitly driving the primary result) and Render (subsidy ratio = 7.63×, cross-chain measurement complexity from merged Solana RENDER + Ethereum RNDR token). The full cross-sector sample is N = 22 (9 DeFi, 4 Infrastructure, 9 DePIN).

---

## Table S8-A. Protocol-Level Data

| Protocol | Sector | Revenue (USD) | Incentives (USD) | Subsidy Ratio (TT) | HHI |
|---|---|---|---|---|---|
| MakerDAO | DeFi | 790,400,000 | 0 | 0.000 | 0.045 |
| Maple | DeFi | 17,400,000 | 0 | 0.000 | 0.024 |
| Jupiter | DeFi | 850,000 | 0 | 0.000 | 0.117 |
| Lido | DeFi | 263,800,000 | 34,200,000 | 0.115 | 0.019 |
| GMX | DeFi | 112,400,000 | 39,200,000 | 0.259 | 0.056 |
| Aave | DeFi | 254,100,000 | 149,100,000 | 0.370 | 0.020 |
| Compound | DeFi | 23,000,000 | 36,500,000 | 0.614 | 0.028 |
| Curve | DeFi | 92,700,000 | 277,700,000 | 0.750 | 0.171 |
| Ether.Fi | DeFi | 71,000,000 | 379,300,000 | 0.842 | 0.067 |
| Arbitrum | Infra | 133,400,000 | 0 | 0.000 | 0.012 |
| Optimism | Infra | 90,900,000 | 611,300,000 | 0.871 | 0.042 |
| Polygon | Infra | 36,900,000 | 308,900,000 | 0.893 | 0.035 |
| The Graph | Infra | 2,400,000 | 130,900,000 | 0.982 | 0.036 |
| DIMO | DePIN | — | — | 0.330 (on-chain) | 0.038 |
| Helium | DePIN | — | — | 1.050 (on-chain) | 0.102 |
| Morpheus AI | DePIN | — | — | 1.540 (on-chain) | 0.013 |
| GEODNET | DePIN | — | — | 1.610 (on-chain) | 0.133 |
| Hivemapper | DePIN | — | — | 5.460 (on-chain) | 0.017 |
| io.net | DePIN | — | — | 0.400 (on-chain) | 0.111 |
| Aethir | DePIN | — | — | 0.355 (on-chain) | 0.168 |
| Filecoin | DePIN | — | — | 21.600 (on-chain) | 0.047 |
| IoTeX | DePIN | — | — | 27.800 (on-chain) | 0.106 |

*Protocols excluded from regression (HHI missing): Balancer, Hyperliquid. Protocols excluded as outliers: Livepeer (88.5×), Render (7.63×).*

---

## Table S8-B. Subsidy-Concentration Correlations by Sector

| Sample | N | Pearson r | p-value | Interpretation |
|---|---|---|---|---|
| Full cross-sector | 22 | +0.095 | 0.674 | Null |
| DeFi only | 9 | +0.336 | 0.377 | Null |
| Infrastructure only | 4 | +0.954 | 0.046 | Suggestive (N too small) |
| DePIN only (excl. Livepeer, Render) | 9 | −0.074 | 0.850 | Null |

Spearman rho (full cross-sector) = 0.115, p = 0.610.

---

## Notes

**Measurement regime**: DeFi and Infrastructure protocols use TT accounting metrics (protocol revenue, token incentives). DePIN protocols use on-chain burn/mint ratios. This mixed-regime design is the reason this analysis is a robustness check rather than a replacement for the primary on-chain specification (r = 0.58, p = 0.007, N = 20 in §5.7), which uses consistent on-chain methodology for all 20 protocols.

**Aethir revenue**: Body text updated to $156M (Token Terminal, April 2026) in v14.

**Infrastructure caution**: The r = 0.954 correlation among 4 Infrastructure protocols (Arbitrum, Optimism, Polygon, The Graph) is not inferentially meaningful at N = 4; it is reported for completeness.
