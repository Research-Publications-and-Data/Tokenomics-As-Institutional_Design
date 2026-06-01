# B2 regression recompute (finalize cycle): authoritative cascaded values

**As-of:** 2026-05-31 (post-CEX-exclusion-audit cascade; frame = `data/processed/regression_data_april2026.csv` with CEX-corrected HHI).
**Purpose:** complete the three "data-owner regression recompute" items held open by the outward-facing cascade handoff, by running the persisted regression scripts on the cascaded frame and recording the of-record values. All values below are DETERMINISTIC reproductions (no estimation), reconciled against `reproduce.py` and `reproduce_results_2026-05-29.json`.

Reader MUST re-run the scripts below before acting; the frame may have advanced.

## Scripts run (all read the cascaded `regression_data_april2026.csv`)
- `b2/paper/analysis_n52_2026-05-29/b2_explanatory_model_REPRODUCTION_2026-05-29.py` (Model 4 maturity-spec full panel)
- `b2/paper/supplements/subsidy_multivariate_2026-05-19.py` (subsidy-multivariate TT)
- `b2/paper/supplements/subsidy_multivariate_oc_sensitivity_2026-05-19.py` (subsidy OC sensitivity)
- `b2/paper/supplements/profitability_retention_2026-05-19.py` (profitability/retention)
- `b2/paper/analysis_n52_2026-05-29/nansen_reclass_2026-05-29/b2_nansen_v4_headline_impact_2026-05-29.py` (six-scheme retention-spec)
- `reproduce.py` (master reconciliation)

## LAYER 1: Model 4 Table 5 panel (maturity-spec; log-HHI ~ sector + log(rev-int) + maturity; N=50; HC3)
The published panel was pre-cascade and inconsistent with the (already-cascaded) prose p-values. Recomputed:

| Predictor (DV = log HHI) | OLD coef/se/p | NEW coef/se/p |
|---|---|---|
| DePIN (vs DeFi) | +0.710 / 0.293 / 0.020 | +0.733 / 0.275 / 0.011 |
| L1/L2/Infra (vs DeFi) | -0.372 / 0.328 / 0.263 | -0.353 / 0.307 / 0.256 |
| Log revenue-intensity | -0.003 / 0.078 / 0.966 | -0.010 / 0.077 / 0.894 |
| Protocol maturity (years) | +0.003 / 0.052 / 0.962 | +0.026 / 0.050 / 0.601 |
| Constant | -3.668 / 0.336 / <0.001 | -3.866 / 0.304 / <0.001 |

- adjusted R-squared: 0.14 -> 0.18 (exact 0.183)
- sector-only (M0) DePIN coefficient: +0.71 -> +0.74 (exact +0.7369)
- untransformed-HHI (raw) DePIN coefficient: +0.035 -> +0.036 (exact +0.0357, p = 0.019 unchanged; raw M1 p exact 0.0188)
- maturity-spec DePIN log-HHI p = 0.0107 (EXACT vs of-record; unchanged in prose; matches reproduce.py)

## LAYER 2: subsidy-multivariate (HHI ~ subsidy + DePIN dummy; HC3)
TT-preferred subsidy spec on the cascaded frame:

| Spec | OLD | NEW |
|---|---|---|
| all-23: DePIN dummy p | 0.016 | 0.030 (exact 0.0298) |
| all-23: subsidy p | 0.36 | 0.36 (exact 0.356; unchanged) |
| all-23: Adj R-squared | 0.47 | 0.49 (exact 0.486) |
| excl-Livepeer (N=22): subsidy p | 0.94 | 0.93 (exact 0.9345) |
| excl-Livepeer (N=22): DePIN dummy p | 0.007 | 0.004 (exact 0.0039) |

OC-sensitivity spec (on-chain operating-cost subsidy), excl-Livepeer Spec 4: subsidy p = 0.45 (exact 0.4446), DePIN p = 0.005 (exact 0.0051). These MATCH the response-package values already on record -> NO CHANGE.

Finding direction UNCHANGED: subsidy non-significant under sector control; DePIN significant; apparent subsidy-HHI link is Livepeer-driven and absorbed by sector.

## LAYER 3: six-scheme insider-classification robustness (retention-spec; log-HHI ~ sector + insider-retention + log(rev-int); N=50/49)
Primary (evidence-traced classification of record, v4_traced) cascaded 0.0139 -> 0.0050. Full set recomputed via the v4 headline-impact harness:

| Scheme | OLD p | NEW p |
|---|---|---|
| Keyword-floor lower bound (v4_keyword) | 0.0058 | 0.0013 |
| Reliability-gated reviewed (v4_reviewed_safe) | 0.0090 | 0.0037 |
| Evidence-traced classification of record (v4_traced) | 0.0139 | 0.0050 |
| Adversarially reviewed (v4_reviewed) | 0.0148 | 0.0054 |
| Original cohort-baseline (baseline_v3, N=49) | 0.0168 | 0.0072 |
| Gap-filled resolved (v4_resolved_gapfill) | 0.0187 | 0.0082 |

Range "0.0058 to 0.0187, all below 0.02" -> "0.0013 to 0.0082, all below 0.01" (STRENGTHENS; ordering preserved). Insider-retention regressor itself n.s. under every scheme (channel-shift holds; retention-spec retention p = 0.3283 under v4_traced).

## NO-CHANGE items (documented; not cascade-affected)
- Retention de-tautology: Spearman rho = 0.544 (non-insider HHI, approx column), p = 0.0009, N = 34 -> matches published 0.54; CONFIRMED unchanged.
- Insider-retention vs FULL-HHI ("the published rho ~ 0.48 check"): reproduce.py gives rho = 0.441, p = 0.0049, N = 39. The published manuscript reports rho = 0.48, p = 0.003, N = 37 (the original-sample frozen association, matched to the N=37 insider-allocation sample). v3.csv is NOT touched by the CEX cascade (mtime Apr 11). Difference is a 2-row sample difference (39 vs 37), NOT a cascade effect. Data-owner VERIFIED note marked 0.441 "OK" vs published. AUTHOR DECISION FLAGGED: keep published 0.48/N=37 (frozen original-sample) vs align to replication-script 0.441/N=39. Default this cycle: NO CHANGE (frozen).
- Models 1-3 (Table 5, Models 1-3; N=38/36/35): FROZEN original-sample reference. `analysis/05_09_regressions.py` hard-asserts N=40 (designed not to run on the N=52 frame). Paper structure presents Model 4 as the revision-added powered spec; Models 1-3 are the published small-sample reference. Default: keep frozen.
