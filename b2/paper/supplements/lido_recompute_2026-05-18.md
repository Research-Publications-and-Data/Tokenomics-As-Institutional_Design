# Lido Top-1000 Holder Recompute (R2 calibration follow-on)

**Date:** 2026-05-18
**Context:** Post-propagation calibration cycle for B2 R2 manuscript. Lido row in canonical regression CSV used an older 189-row curated holder set (March 31 mtime; ~414K LDO minimum balance threshold); replication-clone holder file (`data/raw/holder_lists/LDO_holders.csv`) was updated to the full top-1000 holder list on May 12 but the canonical CSV's Lido row was never recomputed. Same drift class as the ATH 0.171→0.168→0.153 progression.

## Recomputed values

Source: `data/raw/holder_lists/LDO_holders.csv` (N=1000 holders); `data/processed/exclusions_log.csv` (LDO exclusions: Aragon Agent DAO treasury + 5 Lido vesting multisigs).

| Metric | OLD (189-row curated set) | NEW (top-1000 minus 6 exclusions) |
|---|---|---|
| HHI | 0.0128 | **0.0377** |
| Gini | 0.5186 | **0.8193** |
| Top-1% (top 10 holders) | 7.87% | **35.99%** |
| Top-5% (top 50 holders) | 19.81% | **62.92%** |
| Top-10% (top 100 holders) | 27.71% | **76.60%** |
| N | 189 | **994** (post-exclusion) |
| Total balance (post-exclusion) | 407,996,259 LDO | **626,714,844 LDO** |

## Cascading impact on manuscript

- **Table 4 Lido row:** Updated per above values.
- **Table 7 Lido row:** Holding HHI 0.013 → 0.038; amplification ratio 6.8x → 2.3x.
- **Section 3.3 sector contrast (Fig 4):** DeFi mean 0.041 → 0.043; Mann-Whitney p 0.014 → 0.023; Cohen's d 1.03 → 1.00; LOO robustness preserved (30/30 iterations significant); permutation p 0.009 → 0.006 (more significant under updated baseline).
- **Section 3.5 universal-amplification range:** 1.4x to 6.8x; mean 4.1x → 1.4x to 6.0x; mean 3.3x. DIMO at 6.0x is the new ceiling; Lido at 2.3x sits mid-range.
- **Section 3.5 Lido / Dual Governance paragraph:** Updated to acknowledge that the Dual Governance reform was justified at adoption time by the larger amplification ratio measured from the 189-row curated active-governance subset; under the universal top-1000 methodology applied here, Lido amplification is more moderate (2.3x), but direction (concentration above stake) holds.

## Editorial discipline

Variant B methodology footnote (Section 2.10.2) defines the universal Top-N% convention: Top-1% = top 10 holders share, Top-10% = top 100 holders share, applied to the post-exclusion top-1000 holder sample (with percentile fractions proportionally applied for N < 1000). Lido now uses the same convention as the other 39 rows.

