# Derived metrics: float-to-FDV and revenue-to-FDV vs governance concentration

**As-of:** 2026-05-29. Reproduce with `python3 b2_derived_metrics_2026-05-29.py` (reads
persisted data; no /tmp, no live-API). Companion CSV: `derived_metrics_2026-05-29.csv`;
results JSON: `b2_derived_metrics_results_2026-05-29.json`. N = 50 (47 with float, where both
market cap and FDV are present). Correlational, exploratory. Outcome = log post-exclusion HHI.

These two metrics are stored in a COMPANION file; the canonical regression frame is left
untouched. Folding `float_to_fdv` / `revenue_to_fdv` in as first-class frame columns is a
CANONICAL-WRITER / author decision.

## Result: both are null

| metric | definition | Pearson r | p |
|---|---|---:|---:|
| float-to-FDV | market_cap_usd / fdv_usd (circulating value / fully-diluted) | +0.027 | 0.86 |
| revenue-to-FDV | revenue_annual_usd / fdv_usd (the revenue-intensity regressor) | -0.002 | 0.99 |
| revenue-to-market-cap | revenue_annual_usd / market_cap_usd | -0.031 | 0.84 |
| regression log-HHI ~ sector + float (float coefficient) | | +0.05 | 0.92 |

Float-to-FDV is also nearly identical across sectors (DePIN 0.72, DeFi 0.71, L1 0.70), so it
carries no sector signal. DePIN stays significant controlling for float (p = 0.009).

## Synthesis (extends the exchange / PCA-insider note)

Five surface supply-distribution and valuation metrics are now confirmed NULL against
governance concentration:
- insider ALLOCATION % (the paper's headline allocation null),
- exchange-held %,
- float-to-FDV (locked / vesting overhang proxy),
- revenue-to-FDV,
- revenue-to-market-cap.

Only two things track concentration: sector (DePIN), and insider HOLDINGS (the foundation/team
on-chain control share, the PCA-and-insider overlap; see
`b2_exchange_vs_pca_insider_findings_2026-05-29.md`). The consistent message reinforces the
paper's thesis: surface tokenomics and valuation ratios do not predict the deep, post-exclusion
governance concentration; only the realized concentration of insider holdings and the sector
do. Candidate robustness paragraph for the R1-Major-7 response.

## Caveats

N = 50 (47 for float); correlational; float-to-FDV uses reported market cap and FDV at a single
snapshot (circulating-supply timing differences across sources add noise). Exploratory.
