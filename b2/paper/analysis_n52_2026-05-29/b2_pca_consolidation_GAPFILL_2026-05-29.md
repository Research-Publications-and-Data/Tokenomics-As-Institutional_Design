# Gap-fill: consolidated PCA-exclusion log (closes audit G1)

**As-of:** 2026-05-29. Fills the audit's G1 (scattered PCA exclusions, 9/50 HHIs not reproducible
from a canonical log). Build: `b2_pca_exclusions_consolidate_2026-05-29.py` (reads persisted
sources; no /tmp, no live-API; does NOT touch the regression frame). Reader MUST re-verify.

## What was built

`b2_pca_exclusions_consolidated_2026-05-29.csv` -- ONE machine-readable PCA-exclusion log
(token, address, pca_class, source), **252 rows across 49 tokens**, merging every previously
scattered source: `exclusions_log.csv`, `exclusions_log_signer.csv`, `phase4_evm_minibatch_v2_
audited`, `new12_unified` (the WLFI DolomiteMargin / LockReleaseTokenPool + ENA sENA corrections
that were missing from the canonical log), `ALGO_pca_exclusions` (clone-B), and the TAO coldkey +
bridge registry. `audit_consolidated_hhi_status_2026-05-29.csv` is the per-protocol reproduce
status.

## Result: 45/50 reproduce directly; +3 the log is correct and the FRAME is stale; 2 residual

Recompute post-exclusion HHI from raw-minus-consolidated-log vs the documented regression frame
(tol 2e-3): **45/50 match** (up from 41/50 on the scattered sources). The 5 non-matches resolve:

| token | recompute (consolidated log) | frame doc | disposition |
|---|---:|---:|---|
| JUP | 0.1260 | 0.0957 | FRAME STALE: the log holds the S13 CEX exclusions (already in exclusions_log) that give 0.1260; the frame kept the pre-S13 0.0957. The log is correct. |
| DRIFT | 0.0568 | 0.0529 | FRAME STALE: same; log 0.0568 correct, frame pre-S13. |
| HNT | 0.0874 | 0.0745 | FRAME STALE: same; log 0.0874 correct, frame pre-S13. |
| IO | 0.0786 | 0.1251 | SPECIAL METHOD: the documented IO value is the R2-calibration rescaling (top-100 rescaled to actual supply), not raw-minus-log reproducible. Record the rescaling method or re-derive. |
| DOT | 0.0139 | 0.0052 | SPECIAL METHOD: the documented DOT value is from the AssetHub Subscan capture; clone-A `DOT_holders.csv` is a different capture. Re-capture from AssetHub or record the capture-of-record. |

So the consolidated log correctly handles **48/50** (45 match + 3 where the log gives the right
value and the frame is stale). Only IO and DOT need their per-protocol method recorded to become
raw-reproducible.

## The frame-staleness finding (JUP/DRIFT/HNT) -- refresh is HEADLINE-SAFE

The S13 Solana CEX exclusions (u6PJ8..., 6FEVkH..., 5tzFki..., the documented `hhi_after` per
`solana_pca_proposed_exclusions_2026-05-27.csv`) are ALREADY in `exclusions_log.csv` (13 of 15
present), but the regression frame's `hhi` column was never refreshed to reflect them. Refreshing
JUP 0.0957->0.1260, DRIFT 0.0529->0.0568, HNT 0.0745->0.0874 (and the immaterial GRASS/W/HONEY
deltas) does NOT break the headline:

| spec | current (stale) | refreshed |
|---|---:|---:|
| maturity-spec DePIN p | 0.0395 | 0.0395 |
| retention-spec DePIN p | 0.0409 | 0.0443 * |
| balanced-30 Mann-Whitney | 0.0364 | 0.0390 * |
| DePIN/DeFi HHI gap | 1.93x | 1.89x |

All stay < 0.05 (the S13 CEX exclusions raise DeFi and DePIN roughly proportionally). The refresh
is safe to apply.

## Recommendations (author / CANONICAL-WRITER; NOT applied here)

The live regression frame has uncommitted parallel-session changes (` M` at audit time), and it
is the analysis-of-record, so this cycle did NOT mutate it. Recommended next steps:
1. **Adopt the consolidated log** as the single canonical PCA-exclusion source (replaces the 6+
   scattered files); reproduce.py and any HHI recompute then have one source.
2. **Refresh the 3 stale frame HHIs** (JUP, DRIFT, HNT) to the log-consistent S13 values
   (headline-safe, quantified above), and propagate the WLFI/ENA corrections (already in the
   consolidated log) into the canonical exclusions_log.
3. **Record IO's rescaling method and DOT's AssetHub capture-of-record** so those two become
   raw-reproducible (or re-derive them).

This closes G1 structurally (one consolidated reproducible log) and surfaces the frame refresh +
the 2 special-method residuals for the author, without an unilateral analysis-frame mutation.
