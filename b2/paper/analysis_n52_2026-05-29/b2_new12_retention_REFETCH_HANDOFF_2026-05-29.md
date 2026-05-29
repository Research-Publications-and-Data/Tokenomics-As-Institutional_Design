# New-12 retention re-fetch: scoping, de-risking, and pipeline-integration handoff

**As-of:** 2026-05-29. Purpose: re-classify the new-12 post-exclusion top-10 holders insider/not, persist per-protocol `insider_count_frac`, so the retention-spec explanatory model (DePIN + retention + revenue-intensity) is reproducible BY CONSTRUCTION. This memo de-risks the cycle; EXECUTE within the reproduction-pipeline build (`handoff/dispatch/b2_replication_package_reproduction_pipeline_2026-05-29.md`), not ad-hoc.

## DETERMINISTIC PREP DONE (2026-05-29; the fresh session starts here)
The unified, gap-closed exclusion set + correct post-exclusion top-10 for the new-cohort EVM-5 + Solana-4 are built and persisted (no API, no insider-judgment):
- `b2_new12_unified_exclusions_2026-05-29.py` -> `new12_unified_exclusions_2026-05-29.csv` (56 rows: main log + v2-audited + the 3 decided corrections) + `new12_unified_post_exclusion_top10_2026-05-29.json` (the correct survivors to classify).
- Gaps CLOSED in the unified set: ENA Class-3 `0x8be3...` now excluded (top-1 -> orig-rank-2); WLFI DolomiteMargin `0x003ca23...` + LockReleaseTokenPool `0xc785d...` excluded (top-1 -> orig-rank-3); GNO null-burn excluded (top-1 -> orig-rank-7). The 3 corrections are flagged `CORRECTED 2026-05-29` in the CSV (still need backfill into the canonical `exclusions_log.csv` -- a CANONICAL/pipeline task).
- REMAINING for the fresh session: (1) classify the survivors in the JSON insider/not (free-tools-first per the cost plan below); (2) extract DOT/TAO/ALGO exclusions from their per-protocol artifacts (low-confidence ~0); (3) compute `insider_count_frac`, persist, re-run the retention-spec, promote PAPER.md to retention-primary.

## WHY NOT AD-HOC (the decisive finding)
The post-exclusion top-10 (the retention denominator) depends on the COMPLETE PCA-exclusion set, which is scattered AND partially inconsistent across files. Classifying survivors before unifying exclusions yields wrong `insider_count_frac`. Concrete gaps found this cycle:
1. **ENA Class-3 not propagated:** `0x8be3460a480c80728a8c4d7a5d5303c85ba7b3b9` (Ethena Staked ENA) HHI was corrected (0.0467->0.0472) but the EXCLUSION was never added to `exclusions_log.csv` -> it still appears at orig-rank-4 in ENA's "post-exclusion" top-10. Same for WLFI's corrected exclusions (DolomiteMargin, LockReleaseTokenPool).
2. **GNO null/burn `0x000...000` (31.6%)** is excluded in the v2-audited EVM minibatch file (Class 1) but NOT in the main `exclusions_log.csv`.
3. **Scattered sources:** main `exclusions_log.csv` (WLFI/ENA/Solana) + `phase4_evm_minibatch_exclusions_v2_audited_2026-05-27.csv` (FXS/SNX/GNO) + per-protocol (`dot_pca_refined`, `tao_pca.py`, ALGO AlgoNode json). No single unified exclusion set exists.
=> The pipeline must FIRST unify all exclusion sources (closing gaps 1-2), THEN compute post-exclusion top-10, THEN classify.

## CHANNEL-SHIFT IS CONFIRMED IN THE EXCLUSION STRUCTURE (the substantive finding)
The new-cohort insiders are ALREADY classified + excluded as protocol-controlled, which is mechanically WHY retention ~0 for them:
- GNO: co-founder Safes excluded as Class-2 (`0x9d94...` Stefan George; `0xae5fb...` koeppelmann.eth Martin Koppelmann); foundation vesting/treasury Class-2.
- FXS: r1 Fraxtal bridge (Class-4, 48%); veFXS staking (Class-3); Frax Comptroller foundation (Class-2).
- SNX: r1 Synthetix Core (Class-4, 38%); bridge escrow (Class-4); CEX (Class-5).
The identified insiders sit in excluded vehicles -> surviving post-exclusion top-10 are mostly retail/unlabeled -> retention reads ~0. This is observation-firm; it directly supports the channel-shift interpretation.

## CORRECTED post-exclusion top-10 (persisted): `new12_CORRECTED_top10.json`
EVM-5 (FXS/SNX/GNO with v2-audited exclusions; WLFI/ENA with main-log only -- NOTE WLFI/ENA still need gaps 1 closed) + Solana-4 (main-log exclusions) computed. DOT/TAO/ALGO need their per-protocol exclusion sets merged (older L1; retention low-confidence -> flag, do not over-invest).

## CLASSIFICATION PLAN (cost-managed; per author directive 2026-05-29 "other providers first")
Nansen premium-labels = 500 credits each, ~20 calls max from the 10k budget. Order of tools:
1. **FREE first:** Blockscout MCP (`get_address_info`: is_contract, name, public tags) + Etherscan for EVM; Helius (`HELIUS_API_KEY`) account-type/owner for Solana; Subscan/Taostats/AlgoNode for DOT/TAO/ALGO. Resolves contracts, CEX, program-owned, ENS-named.
2. **Nansen MCP `token_current_top_holders`** (one call per token returns labeled holders; far cheaper than per-address premium-labels) for entity labels on the surviving holders -- cross-ref the post-exclusion top-10 addresses. ~12 calls; verify per-call credit cost first.
3. **Reserve premium-labels REST (`/profiler/address/premium-labels`, payload `{"address","chain"}` at body top-level, 500cr)** for ONLY decision-flipping high-share unlabeled EOAs (the ones that move `insider_count_frac`). Budget <=20.
Conservative rule: unlabeled EOA with no fund/team attribution = NOT insider (no imputation). Insider = team/founder/VC/early-investor wallet NOT already PCA-excluded.

## OUTPUT (persist in replication repo, NOT /tmp/prose)
`insider_analysis_results_v3.csv` extended with the new-12 rows (token, full_hhi, insider_count, n_top10, insider_count_frac, non_insider_hhi_approx, per-address classification provenance). Then re-run the retention-spec (sector + retention + revenue-intensity, N~49); report the REPRODUCED DePIN p (not the remembered 0.016). Document residual ambiguity (WLFI SafeProxies; thin Solana labels).

## REPRO SCRIPTS (this cycle, persisted)
`b2_new12_corrected_top10_2026-05-29.py` (unified-exclusion top-10), `b2_new12_post_exclusion_top10_2026-05-29.py` (main-log-only, superseded), `b2_explanatory_model_REPRODUCTION_2026-05-29.py` (the maturity-spec authoritative numbers), `b2_explanatory_model_VERIFIED_NUMBERS_2026-05-29.md`.
