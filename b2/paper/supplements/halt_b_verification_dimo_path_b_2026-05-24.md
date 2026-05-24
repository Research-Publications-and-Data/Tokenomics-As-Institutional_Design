# HALT-B verification: DIMO Path B canonical methodology (DEC-194; 2026-05-24)

**Cycle:** B2 R3-prep arc Phase A Tier 3 replication-clone cascade per workflow commit `77d1ff5e` (DEC-194 codification) + sibling workflow commit `999ab3a5` (LFU memo + methodology MDs).

**Test:** Spec 4 multivariate regression (HHI ~ subsidy_ratio + DePIN_dummy; excluding Livepeer outlier) with DIMO sub_OC = 5.04 (Path B canonical; supersedes cycle 3 sub_OC = 0.335 dead-burn methodology).

**Acceptance criterion (per DEC-167 convention-invariance):** subsidy_p non-significant (p > 0.05) under sector control; DePIN_p remains highly significant. Headline finding "DePIN sector dummy absorbs the apparent subsidy-HHI association; subsidy coefficient is non-significant under sector control" preserved across the methodology shift.

---

## Pre-DEC-194 baseline (DIMO sub_OC = 0.335; cycle 3 burn-to-dead)

| Specification | Subsidy_p | DePIN_p | Adj R² |
|---|---:|---:|---:|
| TT-preferred Spec 4 (no Livepeer) | 0.9161 | 0.0044 | (prior) |
| OC-sensitivity Spec 4 (no Livepeer) | 0.9300 | 0.0065 | (prior) |

Source: post-DEC-172 GEOD Path B HALT-B verification per `docs/KEY_FINDINGS.md` F-B2-11 cycle 4 status note (workflow clone) + workflow commit `2a8c9a6a` + replication commit `3b5868a`.

## Post-DEC-194 results (DIMO sub_OC = 5.04; Path B Foundation dashboard 159676 protocol-wallet inflow methodology)

Replication-clone CSV refresh: `data/processed/regression_data_april2026.csv` DIMO row updated (rev_OC 7,667,597.7 → 510,045.0; sub_OC 0.335 → 5.04; revenue_source_onchain → `foundation_dashboard_159676_dcx_purchase_wallet_inflow_path_b_2026-05-24`); emit_OC = 2,570,643.27 preserved per Path B canonical (cycle 3 mints-from-null methodology valid).

Pre-Path-B backup: `data/processed/regression_data_april2026.csv.pre_dimo_path_b_2026-05-24`.

### TT-preferred Spec 4 (no Livepeer; N = 22)

```
=== Spec 4: HHI ~ subsidy_ratio + DePIN_dummy (without Livepeer, N = 22) ===
  subsidy beta = 0.000003, t = 0.006, p = 0.9949
  DePIN beta   = 0.038248, t = 2.808, p = 0.0050
  Adj R^2 = 0.259
```

Source: `b2/paper/supplements/subsidy_multivariate_2026-05-19.py` (run 2026-05-24).

### OC-sensitivity Spec 4 (no Livepeer; N = 22)

```
=== Spec 4: HHI ~ subsidy_OC + DePIN (no Livepeer, N = 22) ===
  subsidy beta = -0.000105, t = -0.194, p = 0.8480
  DePIN beta   = 0.038436, t = 3.068, p = 0.0063
  Adj R^2 = 0.261
```

Source: `b2/paper/supplements/subsidy_multivariate_oc_sensitivity_2026-05-19.py` (run 2026-05-24).

## HALT-B comparison table

| Specification | Pre-DEC-194 subsidy_p | Post-DEC-194 subsidy_p | Pre-DEC-194 DePIN_p | Post-DEC-194 DePIN_p | Significance preserved? |
|---|---:|---:|---:|---:|:-:|
| TT-preferred Spec 4 | 0.9161 | 0.9949 | 0.0044 | 0.0050 | YES (subsidy non-significant; DePIN highly significant) |
| OC-sensitivity Spec 4 | 0.9300 | 0.8480 | 0.0065 | 0.0063 | YES (subsidy non-significant; DePIN highly significant) |

### Direction-of-effect analysis

**TT-preferred Spec 4 subsidy_p shifted 0.9161 → 0.9949** (+0.079; subsidy coefficient moved further from significance). Mechanism: DIMO's sub_OC (now 5.04 via Path B) is high, but DIMO's HHI (0.025) is low; this weakens any positive subsidy-HHI relationship in the no-Livepeer subset. The TT-preferred script uses sub_TT first with sub_OC fallback; DIMO has empty sub_TT so it contributes via sub_OC = 5.04.

**OC-sensitivity Spec 4 subsidy_p shifted 0.9300 → 0.8480** (-0.082; subsidy coefficient slightly closer to significance but remains far above conventional thresholds). Mechanism: DIMO joins the subsidy-cluster adjacent to RENDER (9.83) and post-DEC-172 GEODNET (4.51); the cluster has internally varying HHI values which weakens cluster-level concentration signal but does not flip the sector-absorption pattern.

**DePIN_p remained essentially unchanged across both specifications** (TT-preferred: 0.0044 → 0.0050; OC-sensitivity: 0.0065 → 0.0063). The DePIN sector dummy continues to absorb the apparent subsidy-HHI association at the multivariate-headline layer.

## HALT-B verification: PASS

The DIMO sub_OC methodology shift (0.335 → 5.04; 15x change) produces minimal multivariate-headline shift, consistent with DEC-167 convention-invariance preserved across cycles 1-3 (TT p = 0.92 / OC p = 0.93) and post-DEC-172 GEODNET shift (TT p = 0.9161 / OC p = 0.9300).

**Cycle-shift envelope (cross-cycle DEC-167 convention-invariance robustness):**
- Cycles 1-3 baseline: TT-preferred Spec 4 subsidy_p ≈ 0.92; OC-sensitivity Spec 4 subsidy_p ≈ 0.93
- Post-DEC-172 GEODNET Path B: TT 0.9161 / OC 0.9300 (cycle 4)
- Post-DEC-194 DIMO Path B: TT 0.9949 / OC 0.8480 (cycle 5)

Across all three cycles, subsidy_p remains non-significant under sector control (all values p > 0.5). DePIN_p remains highly significant across all three cycles (all values p < 0.01). The convention-invariance prediction (sub_TT preferred default vs sub_OC sensitivity; per DEC-167) holds robustly across two cumulative methodology shifts (GEODNET cycle 4 + DIMO cycle 5).

## Material reclassification (per-protocol layer; not multivariate-headline layer)

DIMO moves from net-deflationary subset (sub_OC = 0.335) to subsidy-heavy subset (sub_OC = 5.04) in the per-protocol classification framework (PAPER.md §3.4). DIMO joins the subsidy-cluster adjacent to RENDER (9.83) and post-DEC-172 GEODNET (4.51).

**N-count cascade (per workflow clone PAPER.md §3.4 cascade applied at workflow commit `77d1ff5e`):**
- Gross-flow burn-active subset: N = 11 → N = 10 (DIMO removed)
- Gross-flow subsidizing subset: N = 14 → N = 15 (DIMO added)
- Net-flow burn-active subset: N = 12 → N = 11 (DIMO removed)

**Insider-retention statistics:** computed on the pre-Path-B panel; flagged for refresh in this Tier 3 cycle (analysis script `b2/paper/supplements/profitability_retention_2026-05-19.py` if rerun). Direction-of-effect prediction per DEC-167 convention-invariance: small effect sizes that do not reach conventional significance under either gross-flow or net-flow definitions; both definitions converge on the substantive null pattern that net-deflationary status does not predict insider position retention.

## Cross-references

- **DEC-194** (workflow clone `docs/DECISION_LOG.md`): DIMO rev_OC + sub_OC Path B canonical selection; six-reason justification parallel to DEC-172 GEODNET pattern.
- **EC-2026-05-24-B2-DIMO-Methodology-Shift-Path-B-Canonical** (workflow clone `docs/ERROR_CORRECTION_LOG.md`): PATTERN; direct-Foundation-measurement-supersedes-alternative-mechanism-burn-to-dead-inference sub-class.
- **F-B2-11** cycle 5 Path B status note (workflow clone `docs/KEY_FINDINGS.md`): DIMO row reclassification.
- **F-B2-12** cycle 5 refinement insight #6 (workflow clone `docs/KEY_FINDINGS.md`): Foundation-dashboard-supersedes-burn-to-dead-inference methodology-of-record extension.
- **3 DIMO KU status-appends + 1 POKT KU PARTIAL** (workflow clone `docs/KNOWN_UNKNOWNS.md`).
- **PAPER.md §3.4 substantive prose cascade** (workflow clone): 3 surfaces (abstract null-pattern reframe + §3.4 enumeration audit-trail + §3.4 paragraph-end DEC-194 cascade note).
- **DIMO_methodology.md §5 Cycle 5 Path B canonical subsection** (workflow clone; sibling workflow commit `999ab3a5`).
- **LFU source memo** (workflow clone `.cursor/tasks/Living_File_Updates_2026-05-24_0714_B2_Phase_A_POKT_DIMO_Findings.md`; 261 lines; HIGH-confidence Path B recommendation).
- **DEC-172 sister-pattern** (GEODNET Path B canonical decision 2026-05-20; precedent methodology-of-record).
- **EC-2026-05-19-B2-GEOD-Methodology-Shift-Path-B-Canonical sister EC** (precedent direct-measurement-supersedes class).
- **Foundation dashboard 159676** (`https://dune.com/dimo_network/dimo-taken-out-of-circulation-and-protocol-revenue`): canonical revenue surface.
- **Foundation Dune queries 4585187 + 4219993**: protocol-wallet inflow methodology SQL.
- **DIP-3 marketplace issuance + token burn framework** (`docs.dimo.org/governance/improvement-proposals/dip3`).
- **Foundation protocol wallet** `0x62b98e019e0d3e4A1Ad8C786202e09017Bd995e1` (GnosisSafeL2 multisig; created 2024-06-21; verified via Blockscout on Polygon chain_id=137).
- **Cycle 3 reference Dune query 7541442** (preserved as audit-trail; superseded by Path B Foundation methodology).
- **Backup files** preserved this cycle: `data/processed/regression_data_april2026.csv.pre_dimo_path_b_2026-05-24` (DIMO row before update).

## Closing notes

HALT-B verification PASS confirms B2 R2 submission package remains finding-stable under the DEC-194 methodology shift. R3 cycle authorized; this Tier 3 cascade completes the workflow + replication clone canonical-state propagation. Frontiers editorial decision return + author-initiated R3 authorization both gates for downstream R3 prep arc Phase B-F (per `/tmp/b2_r3_prep_arc_handoff_back_to_canonical_writer.md`).

**Files this cycle (replication clone):**
- `data/processed/regression_data_april2026.csv` (DIMO row update)
- `data/processed/regression_data_april2026.csv.pre_dimo_path_b_2026-05-24` (backup)
- `b2/paper/supplements/subsidy_multivariate_2026-05-19.csv` (regenerated Spec 1-4 output)
- `b2/paper/supplements/halt_b_verification_dimo_path_b_2026-05-24.md` (this file; verification memo)
- `CHANGELOG.md` (DEC-194 cascade section appended)

Per AUTHOR-DIRECT lane authorization 2026-05-24 ("Execute tier 3. R3 authorized").
