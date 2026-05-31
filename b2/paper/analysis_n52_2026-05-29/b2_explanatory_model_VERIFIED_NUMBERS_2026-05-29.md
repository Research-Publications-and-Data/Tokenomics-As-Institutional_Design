# B2 explanatory model: VERIFIED authoritative numbers (cascade-time reproduction)

> **Superseded-in-part 2026-05-31 (CEX-exclusion audit).** The 2026-05-31 full 52-protocol exchange-custody audit (64 additional Nansen-labeled CEX wallets excluded across 21 protocols; see `EC-2026-05-31-B2-JUP-Retained-CEX-Upbit-Backpack-Plus-Full-52-Protocol-Exchange-Custody-Audit`) advanced the frame, so the model anchors below are superseded: maturity-spec DePIN p 0.0197 to 0.0107; retention-spec DePIN p 0.0139 to 0.0050; full-frame Mann-Whitney 0.0234 to 0.0172 (Cohen d 0.939 to 1.052); balanced-30 0.020 to 0.011 (d 0.94 to 1.05). All STRENGTHEN. De-tautology Spearman rho 0.544 unchanged. The post-audit of-record values are in `reproduce.py` reconcile() and the apply script `b2_apply_cex_audit_2026-05-31.py`.

**As-of:** 2026-05-29. Reproduced READ-ONLY from persisted clone-A data after the original
/tmp run scripts evaporated (artifact-retention gap). Script:
`b2/paper/analysis_n52_2026-05-29/b2_explanatory_model_REPRODUCTION_2026-05-29.py`.
This file is the authoritative number source for the PAPER.md Table 5 cascade + the response letter.

## REPRODUCIBLE NOW (persisted data; HC3 robust SE; matches Table 5 spec)

### Powered model: log-HHI ~ sector(DePIN,L1; DeFi=ref) + log(revenue-intensity) + maturity
- N = 50 governance-token protocols (15 DePIN, 24 DeFi, 11 L1). obs/predictor = 12.5 (clears the >=10 floor; published Model 3 was 35/~5-7).
- DePIN beta = +0.651, p = 0.0395 (SIGNIFICANT). M0 (sector only) DePIN = +0.669; M1 controlled = +0.651 => 3% attenuation = NO attenuation.
- revenue-intensity p = 0.832 (NULL); maturity p = 0.862 (NULL). VIF < 1.1 (rev-int 1.08, maturity 1.00).
- raw-HHI DV (comparable to published Models 1-3 coefficient scale): DePIN beta = +0.0304, p = 0.0855; M0 +0.0340.

### Retention de-tautology (original sample; insider_analysis_results_v3.csv)
- retention vs FULL-HHI: Spearman rho = 0.441, p = 0.0049, N = 39 (the published rho~0.48 check; OK).
- retention vs NON-INSIDER-HHI (the de-tautology), correct column `non_insider_hhi_approx`:
  **Spearman rho = 0.544, p = 0.0009, N = 34**; Pearson r = 0.497, p = 0.0028; OLS raw beta = +0.195, p = 0.0028; OLS log-DV beta = +3.34, p = 0.0009. **DE-TAUTOLOGY SURVIVES** (retention is not a mechanical artifact of insiders being IN the HHI).

### COLUMN-CHOICE WARNING (corrected this cycle)
`non_insider_hhi_top10` in v3 is BUGGY: for 7 insider_count=0 rows (ARB, CRV, OP, HYPE, BAL, IO; IOTX OK) it does NOT equal full_hhi though it must (BAL top10=0.182 vs full=0.0295; IO top10=0.284 vs full=0.111). Using it gives a spurious rho=0.265 p=0.113. **Use `non_insider_hhi_approx`** (insider=0 -> equals full_hhi, as required). A first reproduction used the wrong column and momentarily contradicted the lock; the lock was right.

## NOT REPRODUCIBLE (artifact-retention gap, flagged)
The exact model in the locked claim, **log-HHI ~ sector + insider-RETENTION + revenue-intensity (N=49, DePIN p=0.016, retention n.s. p=0.91)**, cannot be reproduced from persisted data: the new-12 retention frame (FXS/SNX/GNO/WLFI/ENA/PUMP/JTO/BONK/KMNO/DOT/TAO/ALGO insider_count_frac) was assembled at run-time and evaporated with the /tmp script. v3.csv covers only the original ~38 (AAVE..IO).
- Re-derivable: the new-12 post-exclusion top-10 holder lists ARE persisted (data/raw/holder_lists/); the session's Nansen/Blockscout/Helius insider classifications are in the LFU prose (FXS ~0.3; SNX/GNO/WLFI/ENA ~0; PUMP/JTO/BONK/KMNO ~0-0.1; DOT/TAO/ALGO ~0/low). A re-derivation cycle would re-establish insider_count_frac for the 12 and reproduce the retention-spec exactly.
- Headline does NOT depend on it: DePIN robust (p=0.040) reproduces without the retention term; retention's "doesn't generalize to the new cohort" is the channel-shift observation (verified this session: new-cohort insiders sit in PCA-excluded vehicles, so post-exclusion-top-10 retention ~0 by construction).

## RECONCILIATIONS for the response letter (author flagged "verify before sending")
| letter value | reproducible value | note |
|---|---|---|
| obs/pred 35/7.0 -> 49/12.2 | 35/~5-7 -> **50/12.5** | improvement holds; exact revised figure is spec-dependent (49 retention-spec vs 50 maturity-spec) |
| DePIN p = 0.016 (no attenuation) | **p = 0.040** (maturity spec) / 0.016 (retention spec, needs re-derivation) | both significant, both no-attenuation; the headline ("strengthens under the demanded spec") holds |
| retention de-tautologized (original sample) | rho = 0.54, p < 0.001 | CONFIRMED |
| revenue-intensity / maturity / allocation null | p = 0.83 / 0.86 / (Model 3) | CONFIRMED |
