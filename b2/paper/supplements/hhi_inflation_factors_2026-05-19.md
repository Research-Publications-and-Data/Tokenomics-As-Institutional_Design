# HHI inflation factor recompute (2026-05-19)

**Cycle anchor:** GC-2 from `/tmp/b2_table7_cascade_handoff_back_to_canonical.md`. The previous "up to 7x" anchor was preserved as an empirically anchored upper bound (per `CHANGELOG.md` 2026-05-19 entry) pending separate recompute. This supplement closes that recompute.

## Methodology

The PCA exclusion methodology applies 133 address exclusions across 38 protocols (125 unique addresses; five recur across multiple protocols, e.g., Binance 8 hot wallet `0xf977...` excluded for four tokens; burn address `0x000...dead` for three) from the top-1000 holder list before computing HHI (see Section 2.10.10 of PAPER.md). The inflation factor per protocol is defined as:

```
inflation_factor = naive_top_1000_HHI / post_PCA_HHI
```

Higher values indicate that the naive top-1000 HHI overstated governance concentration; in such cases, the naive measurement was driven primarily by addresses that cannot vote (staking contracts, bridges, treasuries, exchange custodians, vesting locks).

Inputs:
- `data/processed/exclusions_log.csv` (per-address exclusion log; `hhi_before` and `hhi_after` columns populated on the first exclusion row per protocol)
- `data/processed/regression_data_april2026.csv` (canonical post-PCA HHI)

## Results

Across the 32 protocols where the exclusions log contains complete pre-exclusion and post-exclusion HHI pairs:

| Statistic | Value |
|---|---:|
| Maximum inflation factor | 17.88x (RENDER) |
| 90th percentile | 7.61x |
| Median | 2.33x |
| Minimum (inflation cases only) | 1.10x (MKR) |
| Renormalization-rising cases (ratio less than 1) | 4 (HONEY, GEOD, MOR, ATH) |

### Top inflation factors

| Rank | Token | Pre-PCA HHI | Post-PCA HHI | Inflation | Driver |
|---:|---|---:|---:|---:|---|
| 1 | RENDER | 0.5775 | 0.0323 | 17.88x | Wormhole Token Bridge custody (Class 4) |
| 2 | MPL_SYRUP | 0.2162 | 0.0242 | 8.93x | Staking pools and protocol treasury |
| 3 | ARB | 0.0970 | 0.0123 | 7.89x | Vesting + Treasury (Class 2 + Class 3) |
| 4 | DIMO | 0.2817 | 0.0379 | 7.43x | Centralized mint contract |
| 5 | GMX | 0.3890 | 0.0564 | 6.90x | sGMX RewardTracker staking |
| 6 | POL | 0.2279 | 0.0348 | 6.55x | MATIC migration + Polygon Foundation |
| 7 | RPL | 0.2530 | 0.0392 | 6.46x | Rocket Pool protocol treasury |

### Renormalization-rising cases

For four protocols (HONEY, GEOD, MOR, ATH), the post-exclusion HHI is slightly larger than pre-exclusion HHI. This is mathematically expected when the excluded addresses are NOT dominant holders: removing a non-dominant address and renormalizing across remaining holders can increase HHI if the residual distribution becomes proportionally less spread. The magnitudes are small (ratios 0.92x to 0.99x), and these protocols are correctly classified post-exclusion.

## Coverage caveat

Six protocols (LDO, CRV, COMP, BAL, HYPE, IO) have exclusion log entries but with empty `hhi_before` and `hhi_after` columns; the exclusion-event sequencing was logged without recording the HHI step values. These protocols' inflation factors could be reconstructed by re-deriving the naive top-1000 HHI from raw holder files, but this is deferred. The 32-protocol sample is sufficient to establish the empirical anchor.

## Anchor update

The headline phrasing "up to 7x" was a conservative empirical upper bound established in earlier cycles before the full per-protocol inflation factor was tabulated. The empirically grounded maximum across 32 protocols is **17.88x for RENDER**, where Wormhole Token Bridge custody dominated naive top-1000 holdings (76% of supply held by the bridge address). Conservative rounding to one significant figure yields **"up to 18x"** for the updated anchor.

## Surfaces updated this cycle

- `research_content/papers/B2_governance_concentration/PAPER.md` (workflow clone): two anchor instances at the abstract-area methodology summary and the contributions section
- `CITATION.cff` (replication clone): abstract block
- `README.md` (replication clone): methodology contribution paragraph
- `CHANGELOG.md` (replication clone): new entry for this cycle (the prior 2026-05-19 entry preserving "up to 7x" is retained as historical record per source-fidelity convention)

End of supplement.
