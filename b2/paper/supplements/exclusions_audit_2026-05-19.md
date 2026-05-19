# PCA Exclusion Universal Audit (2026-05-19)

**Date:** 2026-05-19
**Trigger:** Deep audit cycle following Path B Top-N% convention correction. Bytewise recompute of all 40 protocol HHI values from holder files surfaced four HHI drifts between the canonical CSV and recomputed values: AXL (0.028 vs 0.202), OP (0.009 vs 0.022), ZRO (0.015 vs 0.027), MOR (0.031 vs 0.045). Root-cause investigation revealed that the canonical CSV applies a 5-class PCA exclusion methodology while the documented typology (Section 2.10.10) only enumerated four classes.

## Identified Class-5 (Centralized Exchange Custody) exclusions

Six addresses identified via Etherscan name tags + universal audit recompute. With these exclusions added, CSV HHI values reproduce exactly for OP, AXL, and ZRO.

| Token | Address | Identification | Source |
|---|---|---|---|
| OP | 0xf977...41acec | Binance 8 hot wallet | Etherscan + audit recompute (CSV 0.0091 reproduces) |
| AXL | 0x54d1...22cbf9 | Bithumb 162 | Etherscan name tag (hildobby) |
| AXL | 0x377b...190873 | Upbit 59 | Etherscan name tag (hildobby) |
| AXL | 0xd2ff...deebc | Unlabeled EOA (113M AXL = 42% post-listed-exclusion supply) | Audit recompute; CSV-excluded; **classification deferred to author judgment** |
| ZRO | 0x8f64...a449c | LayerZero Future Initiatives Multisig | Etherscan name tag (Safe Singleton 1.3.0; 106M ZRO) |
| ZRO | 0x744d...38da24 | GnosisSafeProxy holding 69.5M ZRO | Etherscan (likely LayerZero protocol-controlled based on architecture + holding size) |

## Reproduction verification

| Protocol | CSV HHI | Recompute (listed-only) | Recompute (listed + Class 5) | Match |
|---|---|---|---|---|
| OP | 0.009 | 0.022 | **0.009** | ✓ |
| AXL | 0.028 | 0.202 | **0.028** | ✓ |
| ZRO | 0.015 | 0.027 | **0.014** | ✓ (close; within rounding) |
| MOR | 0.031 | 0.045 | 0.045 | ⚠ unresolved (see below) |

## Unresolved findings

**MOR residual gap.** CSV HHI 0.031 does not reproduce with any CEX-class addition. The MOR top non-listed holders are small-balance EOAs (~$1M each) that don't fit Class 5. The CSV may have applied additional exclusions beyond the 5-class typology, or the CSV value may itself be slightly stale. Author judgment recommended.

**AXL 0xd2ff... ambiguity.** Etherscan shows this address as an unlabeled EOA with 99.99 percent AXL allocation and active daily token transfers. Behavior is consistent with either (a) an Axelar Foundation operational wallet that Etherscan has not labeled (Class 2), (b) a vesting / distribution proxy (Class 4), or (c) a large institutional position (no PCA class applies; CSV would be over-excluding). Production CSV treats it as excluded. Future Axelar Foundation disclosure should confirm; for now, this address is retained in the exclusion log with classification note "deferred to author judgment."

## Methodology update

PAPER.md Section 2.10.10 PCA typology updated to add **Class 5: Centralized Exchange Custody**. Cross-references to "four-class typology" updated to "five-class typology"; address-count claim updated from "69 addresses across 20 protocols" to "75 addresses across 22 protocols" (the existing 69 from documented 4-class methodology plus the 6 newly documented Class-5 / Class-2 entries identified in this audit).

## Cross-references

- `data/processed/exclusions_log.csv`: 6 new rows appended (OP Binance; AXL Bithumb + Upbit + d2ff...; ZRO LayerZero multisigs).
- `b2/paper/B2_Frontiers_R2_clean.docx` (sister to workflow `cd924b4f` then this audit): Section 2.10.10 Class 5 addition; multiple "four-class" / "69 addresses" references updated.
- CHANGELOG.md `[1.2.0-frontiers-r2-revision]`: new subsection "PCA exclusion universal audit (2026-05-19)" documenting the discovery.
