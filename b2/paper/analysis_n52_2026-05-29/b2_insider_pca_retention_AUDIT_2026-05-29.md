# Audit: insider, PCA-exclusion, and retention calculations (+ gaps)

**As-of:** 2026-05-29. Computational audit of the three B2 calculation families against the
persisted data. Reproduce with `b2_insider_pca_retention_audit_2026-05-29.py`. Reader MUST
re-verify before acting.

## PASS: the calculations are arithmetically correct

| check | result |
|---|---|
| insider_count_frac == insider_count / n_top10 (v3, 39 rows) | OK |
| n_non_insiders == n_top10 - insider_count | OK |
| all_insiders flag consistent (== insider_count==n_top10) | OK |
| insider_balance_frac in [0,1] | OK |
| de-tautology rho(retention, non_insider_hhi_approx) | 0.544, p=0.0009, N=34 (reproduces) |
| new-12 retention vector == provenance insider-count / 10 | OK |
| post-exclusion HHI recompute (raw minus exclusions, renormalized) matches documented | 41/50 |
| column bug: non_insider_hhi_approx == full_hhi for insider_count=0 rows | OK (7/7 clean) |

The `_top10` column bug is real and correctly avoided: `non_insider_hhi_top10` disagrees with
`full_hhi` for 7 insider=0 rows (BAL 0.182 vs 0.0295; IO 0.284 vs 0.111; ARB, CRV, OP, HYPE,
IOTX) where it must equal it. reproduce.py uses `_approx`. CONFIRMED CORRECT.

## GAPS

### G1 (HIGH): the PCA exclusion set is scattered across 6+ sources, not consolidated
9 of 50 protocols' documented HHIs CANNOT be reproduced from the canonical
`data/processed/exclusions_log.csv` because their exclusions live elsewhere:
- **DOT, TAO, ALGO** (3): exclusions in per-protocol artifacts only (ALGO_pca_exclusions.csv in
  the sibling clone, tao_pca.py, dot_pca_refined); ZERO rows in the main log. Recompute gives raw
  HHI (ALGO 0.033 vs doc 0.059; DOT 0.014 vs doc 0.005; TAO 0.014 vs doc 0.007).
- **JUP, DRIFT, HNT, HONEY, IO** (5): the S13 Solana PCA-audit Class-5 exclusions that produced
  the regression HHIs are not in a machine-readable log the recompute can read (recompute is off:
  JUP 0.126 vs doc 0.096; HNT 0.087 vs 0.074; IO 0.079 vs 0.125).
- **WLFI** (1): the corrected exclusions (DolomiteMargin 0x003ca2, LockReleaseTokenPool 0xc785d0)
  are only in the new-12 unified set, NOT in the canonical log (0 rows match). Recompute 0.127 vs
  doc 0.156. (ENA's sENA 0x8be346 Class-3 correction is the same: only in the unified set.)

Exclusion sources currently in play: exclusions_log.csv, exclusions_log_signer.csv,
phase4_evm_minibatch_exclusions_v2_audited, new12_unified_exclusions, ALGO_pca_exclusions.csv,
tao_pca.py, dot_pca_refined, the S13 Solana audit. A full-sample reproduction requires ONE
consolidated machine-readable exclusion log (the Deliverable-1a unification, done only for the
new-12). reproduce.py is honest (it recomputes the new-12 from the unified set and reads the
documented HHI for the rest), but the documented HHIs for these 9 are not independently
reproducible.

### G2 (CLARIFICATION, not an error): gov_conc / v3 hold the FULL HHI, regression holds post-exclusion
Initial read flagged a gov_conc-vs-regression HHI inconsistency; on verification it is NOT one.
`governance_concentration_april2026.csv` `hhi` equals `insider_analysis_results_v3.csv`
`full_hhi` for essentially every protocol (AAVE 0.0202, COMP 0.0289, JUP 0.1166, HNT 0.1024,
LDO 0.0128, ...). That is the FULL holder-HHI (pre-PCA-exclusion). `regression_data` `hhi` is the
POST-PCA-exclusion HHI. They are DIFFERENT metrics by design and are SUPPOSED to differ
(post-exclusion is usually lower, sometimes higher via renormalization). No inconsistency.
The audit CSV's `gov_conc_hhi` column is therefore the full HHI; the `gov_conc_consistent`
column (gov_conc == post-exclusion) is expected False wherever a protocol has PCAs.
Minor real data-quirk: UNI gov_conc `hhi` = 0.0100 does NOT equal v3 `full_hhi` = 0.0322 (the
only protocol where the two full-HHI sources disagree); spot-check which is correct for UNI.

### G3 (LOW): v3 full_hhi may be capture-time stale (the full HHI does not move with PCA audits)
The de-tautology correctly anchors on the FULL HHI (`full_hhi`); that is the design (retention vs
full HHI = the rho~0.48 check; retention vs `non_insider_hhi_approx` = the de-tautology). The full
HHI does not change with the S13 PCA audit (exclusions do not affect it). The only residual is
whether `full_hhi` reflects the latest holder-list captures if those were refreshed after v3; the
headline rho=0.544 reproduces regardless. Low priority.

### G4 (LOW): supply_corrected rows dropped from the de-tautology
AXL, MOR, ZRO have blank `non_insider_hhi_approx` (supply correction left it uncomputable), so
the de-tautology is N=34 not 39. Documented limitation; consider computing their non-insider HHI.

### G5 (LOW): de-tautology sample != regression sample
GTC and TEC are in v3 (and the de-tautology) but not in the current 50-protocol regression frame
(dropped during the cohort revisions). The de-tautology N includes 2 protocols absent from the
headline regression. Consistency note.

### G6 (MEDIUM): original-v3 insider classification is not fully re-auditable
v3's per-address insider determinations were produced via the Tier-2/3 manual review in
`analysis/03_insider_classification.py` (the saved insider_classification.csv has only Tier-1
populated). The DEFINITION matches the new-12 S2 correction (team/investor/founder/foundation/
treasury/multisig), but whether each original protocol was classified identically is not
independently verifiable from persisted data. The new-12-to-original consistency is
definitional, not row-verified.

### G7 (carried): PCA exclusion-incompleteness (leaks) in the new cohort
Surfaced in the re-fetch: Synthetix Treasury, three Ethena Labs EOAs + Proxy, WLFI ecosystem/
multisigs, five pump.fun custody, JITO/Kamino staking + vaults survive into the post-exclusion
top-10 (Class-2/3 that arguably should be excluded). Not insiders, headline-immaterial, but the
new-cohort exclusion set is incomplete relative to current Nansen labels.

### G8 (carried): the S2/S3 co-founder/team boundary is open
GNO co-founder Safes (and PUMP/WLFI team pools) are author-adjudicated as insider (S2 applied to
retention; S3 un-exclusion from the HHI deferred -- it pushes the maturity-spec to 0.0510).

## Recommendations

1. **Consolidate one canonical machine-readable PCA exclusion log** (all 50 protocols: main +
   signer + phase4 + new12-unified + DOT/TAO/ALGO + S13-Solana), with per-row class + source +
   token, so every documented post-exclusion HHI reproduces from raw-minus-log. Single
   highest-value fix (closes G1).
2. **Propagate the WLFI/ENA corrections** (Dolomite, LockRelease, sENA) into exclusions_log.csv
   (part of the consolidation).
3. **Spot-check UNI's full HHI** (gov_conc 0.0100 vs v3 0.0322 disagree) and compute non-insider
   HHI for the supply_corrected rows AXL/MOR/ZRO so the de-tautology covers N=37 not 34.
4. **Optional:** label gov_conc / v3 `full_hhi` explicitly as the pre-exclusion metric to avoid
   future "inconsistency" false-alarms against the post-exclusion regression frame.

All gaps are bookkeeping / reproducibility / consolidation; none is an arithmetic error in the
insider, retention, or de-tautology computations, which all reproduce. Out of scope here: docs/
canonical writes; the consolidation build itself.
