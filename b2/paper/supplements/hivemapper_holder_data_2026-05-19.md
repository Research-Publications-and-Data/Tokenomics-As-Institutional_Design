# Hivemapper (HONEY) holder data acquisition (2026-05-19)

**Cycle anchor:** dispatch §Open items #2; close 39→40 ceiling on insider-retention specifications.

## State at session close

**Data layer complete.** Top-100 HONEY holders pulled via Dune `solana_utils.latest_balances` (HONEY mint `4vMsoUT2BWatFweudnQM1xedRLfJgJ7hswhcpz4xgBTy`); saved to `data/raw/holder_lists/HONEY_holders.csv`. Top-100 coverage approximately 90.7% of total supply (6.52B HONEY).

**Existing canonical state already includes HONEY HHI.** `data/processed/regression_data_april2026.csv` has HONEY at:

- HHI = 0.017589
- Gini = 0.9144
- Top-1% = 5.69%
- Top-5% = 19.48%
- Top-10% = 31.12%
- n_holders = 1000

The 40-protocol cross-section uses these values; HONEY contributes to Sections 3.3 (sector contrast), 3.4 (allocation null), 3.5 (delegation amplification not applicable; HONEY has no governance delegation), and 3.7 (Synergy Index full-sample).

**Insider-retention specification (Section 3.6) is the limit case.** `data/processed/insider_analysis_results_v3.csv` covers 39 protocols; HONEY is the missing protocol because per-address insider classification of the top-10 post-exclusion holders was not previously executed.

## Top-10 HONEY holders post-exclusion (from top-25 raw)

The Hivemapper Foundation address `ERo2hRAc4L83gW2TrFNKxpKgXh5PaWZHC1tqW9RgKLvN` is excluded per `exclusions_log.csv` (Class 2). The post-exclusion top-10 owners (with HONEY balances):

| Rank | Address | Balance (HONEY) | Share % |
|---:|---|---:|---:|
| 1 | EyBXvV7NfMSTaekeaNiq6hMoXSQQ6rDSXziUH5C6dkQ3 | 459,515,350 | 7.04% |
| 2 | FZ9diFCJoPHaXKM7ik34YYAYHsEJ6oBvy9H74dVzqyjk | 241,665,639 | 3.71% |
| 3 | A6zNJCrSEZprWMMmRgdAiNY1jDmJnW1QfFnXWs6dUU3y | 225,862,595 | 3.46% |
| 4 | 8MgKUjhQ1e38owDu8BR6783Z73r1TQk1YtmB6UbCiwfS | 198,510,802 | 3.04% |
| 5 | EAmeyPtAyFPLccyaEwoyAcYaLLjdhEeDoriDSSTjdT6i | 152,680,458 | 2.34% |
| 6 | D99E2pr78DSVmBcjuDWETY8Nfm9X9ro3Grgc67mzfutA | 144,565,038 | 2.22% |
| 7 | HyW7x3gFHWLFA67a2DZVGeCcLNzuNTSG3yUyq2bSsuvA | 144,357,814 | 2.21% |
| 8 | Fe3XYFYaXEo2LEy4ff1fdvp5TT5pJN5nbusNoSwBcmor | 129,877,731 | 1.99% |
| 9 | FsAA2JoVBLin4CbGk16eCjQM4Etixz9cbT1smJvfC6NQ | 126,115,569 | 1.93% |
| 10 | 3A6s38hSeXDrapWiAR7pRxyaJSiCbGLeKmEZSA9Tix4F | 125,902,272 | 1.93% |

Sum of post-exclusion top-10 shares: 29.87% of supply.

## Remaining work for full N=40 closure

Per-address insider classification requires:

1. Solscan / Solana FM lookup for each owner address (foundation, team, investor, exchange, staking program label)
2. Cross-reference against publicly known Hivemapper team / investor / foundation wallets
3. Transfer-pattern analysis (CEX-like outbound activity; counterparty diversity)
4. Apply five-class PCA typology to decide whether any of these are additional PCA candidates (e.g., undeclared staking contracts, additional foundation multisigs)

A Dune `tokens_solana.transfers` query for outbound activity per-owner was attempted in this session but returned empty (Dune execution issue; potentially needs retry on `large` performance tier or partitioning by quarter).

## Deferred action

Add HONEY row to `data/processed/insider_analysis_results_v4.csv` after classification cycle completes. Re-run insider-retention specifications (Spearman rho; OLS; LOO) at N=40 to verify whether the headline rho = 0.48 (p = 0.003) shifts.

## What ships this cycle

- `data/raw/holder_lists/HONEY_holders.csv` (top-100 owners by balance; canonical format matching other protocols)
- This supplement (gap documentation; transparent reporting of data-layer-complete-but-classification-deferred state)
- No PAPER.md update for Section 3.6 N=40 (insider retention remains N=37 per current canonical state)

The 39→40 closure is partially advanced (data acquisition completed) but not fully closed (classification deferred). The headline insider-retention statistic (Spearman rho = 0.44, p = 0.005, N = 39) is unaffected by this cycle.

End of supplement.
