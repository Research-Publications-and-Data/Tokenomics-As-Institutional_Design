# B2 CEX-exclusion reconciliation audit: handoff-back

**As-of:** 2026-05-31T (UTC; generated this session)
**Session:** Claude Code PID 52097, mixed-role CANONICAL-WRITER+BULK-EXECUTOR
**Dispatch executed:** `handoff/dispatch/b2_cex_exclusion_reconciliation_audit_2026-05-31.md`
**Reader instruction:** run `python3 scripts/claude-code-sync.py` and re-grep cited files before acting; canonical state may have advanced.

## Commits landed
- Workflow paper + supplements: `fa1b094f` (pushed to origin CryptoZach/Claude1).
- Workflow docs (EC + F-B2-16 + DEC-203 + ledger): `e242309c` (pushed).
- Sibling data lane: `0ef796e` (LOCAL ONLY in Tokenomics-As-Institutional_Design; NOT pushed; public push gated on author authorization per standing B2 hold).

## What was done (author-approved full scope 2026-05-31)
Full 52-protocol Nansen-entity-label exchange-custody audit. Excluded **64 Class-5 CEX deposit wallets across 21 protocols** (54 unique new addresses), correcting a two-layer detection blind spot (a 500-token behavioral heuristic plus a six-term brand-keyword classifier missing Upbit/Backpack/Bybit/Bithumb/KuCoin/Bitget/Robinhood/MEXC and others).

### Per-protocol HHI deltas (frame of-record)
JUP 0.126008 to 0.044977; DRIFT 0.0568 to 0.0265; IO 0.1251 to 0.0402; HNT 0.0874 to 0.0988 (rises; mid-share CEX renormalization); ATH 0.0948 to 0.1001; GRT 0.0330 to 0.0214; AXL 0.0268 to 0.0231; ENS 0.0494 to 0.0463; plus small moves at AAVE/COMP/CRV/LDO/MPL_SYRUP/RPL/RENDER/HONEY/ANYONE/W/ARB/OP/POL.

### Headline (all STRENGTHEN)
- Balanced-30 (the published headline): Mann-Whitney p 0.020 to **0.011**, Cohen's d 0.94 to **1.05**, ratio 2.3 to **2.6**, U 169 to 174. DePIN mean 0.071 to 0.067; DeFi mean 0.031 to 0.026.
- Full-frame: p 0.0234 to **0.0172**, d 0.939 to **1.052**.
- 3-class Kruskal-Wallis: p **0.0054**.
- Powered Model 4: maturity-spec DePIN log-HHI p 0.0197 to **0.0107** (untransformed 0.030 to 0.019); retention-spec primary p 0.0139 to **0.0050**.
- Robustness: LOO p 0.006 to 0.020; permutation p 0.004; bootstrap mean-diff PI [0.016, 0.070], d CI [0.55, 1.72]; DePIN-within-DeFi-range 9 of 15.

### NEW downstream finding (notable)
With the complete CEX identification, **Class-5 exclusion is now load-bearing**: retaining all CEX collapses the balanced-30 to p=0.184 (d=0.52, not significant) vs excluding at p=0.011 (d=1.05). This REVERSES the prior line-2150 "CEX exclusion not load-bearing" claim (an artifact of the incomplete CEX set) and strengthens the paper's central methodological thesis. PAPER.md line-2150 rewritten accordingly.

### HALT decisions surfaced (author approved)
- HALT-2 (headline change) + HALT-4 (magnitude, 133 to ~197 effective exclusions): surfaced with a scope-sensitivity table; author chose FULL 52-protocol audit + update the published headline + include borderline addresses + repull IO.
- HALT-1 (borderline): 5LZkATrL was live-confirmed by Nansen as "Bybit: Hot Wallet" (resolving the prior institutional-vs-CEX ambiguity); included. Gem2VAyp (JUP Bybit, v4-only) included; headline robust to dropping both (C vs C-minus: p 0.006 vs 0.007).

### IO data-quality resolution
IO's frame value 0.1251 was a **non-reproducible "R2 calibration rescaling"** (per b2_pca_consolidation_GAPFILL; no holder list reproduced it) and its working holder list was truncated to 20 rows. Repulled 2026-05-31 via Helius DAS (84,881 token accounts to 84,839 owners, top-1000); excluded the protocol-controlled custody vault (Class 2, already logged) + 23 Nansen-labeled CEX wallets to 0.0402. Snapshot-date exception: IO is now a May-2026 snapshot; the rest of the cross-section is March 2026 (documented).

## Residual items for follow-on (NOT done this cycle)
1. **AT9 docx/pdf rebuild.** The submission-of-record docx + true redline were NOT rebuilt this cycle (the manuscript HHIs changed across Table 3/6, contrasts, captions, abstract). This is the remaining outward-facing step; flagged RESOLVED-pending in the EC. Recommend a dedicated docx-surgery / build cycle.
2. **Figure 1 + Figure 2 regeneration.** The Figure 1 HHI bar (io.net dropped from the high cluster to 0.040; Aethir/Helium rose) and Figure 2 boxplot reflect the new frame; the underlying images (`media/fig3_hhi_bar_40protocols.png`, `media/fig4_sector_boxplot.png`, `media/fig_sector_3class_n52.png`) were NOT regenerated. Captions are updated; images need a figure-pipeline run.
3. **F-B2-16 duplication in KEY_FINDINGS.md.** The F-B2-16 main entry is duplicated (two near-identical blocks). I appended the 2026-05-31 status to the second (more complete) block and flagged it. Recommend a de-duplication pass.
4. **Models 1-3 (PAPER.md Section 4.3, "Model 3 p=0.078").** Left unchanged: these are the published original-sample (N~37) controlled regressions (a frozen historical reference; the live pipeline only powers Model 4). The stale 40-protocol script (analysis/05_09_regressions.py) errors. Verify whether Models 1-3 should be recomputed on the new frame or remain the original-sample reference.
5. **S6 per-source provenance expansion.** Section 3.3 was already the 6-stream version (parallel-session landed); I refined it (dropped unsubstantiated Arkham/Alchemy). The dispatch's "expand S6" is unresolved: S6 is actually revenue-standardization; the real provenance file is S5 (itself stale, 10-source, predates the N=52 expansion). Author decision needed on whether to repurpose S6, expand S5, or create a new provenance supplement.
6. **Class-3-drop sensitivity (S10).** The prior line-2150 "0.60 to 0.17" Class-3-drop magnitude was removed (reworded to qualitative + point to S10) because its baseline changed with the larger Class-5 set; the exact recompute needs the S10 class-tagged sweep.

## Reproducibility artifacts
- Apply script (committed, sibling): `b2/paper/analysis_n52_2026-05-29/b2_apply_cex_audit_2026-05-31.py` (idempotent; .pre_cex_audit backups).
- IO repull (committed, sibling): `b2/paper/analysis_n52_2026-05-29/b2_io_helius_repull_2026-05-31.py`.
- `reproduce.py` reconciles 49 of 50 protocols within tol 2e-3 (lone residual: pre-existing DOT AssetHub-Subscan special-method gap, unrelated).
- Robustness recompute (LOO/permutation/bootstrap) script preserved at sibling `b2/paper/analysis_n52_2026-05-29/b2_balanced30_robustness_2026-05-31.py`.

---

# Companion section: R2 editorial polish (Claude Code PID 17254, BULK-EXECUTOR)

**As-of:** 2026-05-31T10:56:32Z. **Pushed:** all editorial commits below are on `origin/main` (CryptoZach/Claude1); workflow HEAD `e242309c` at close. Authored in PARALLEL with the CEX-audit session above; the two sessions both edited PAPER.md.

## What this companion session shipped (manuscript prose / figures / supplements; no data-of-record changes)
- **Title (spelled-out):** "Governance Concentration Beyond Token Allocation: A Protocol-Address-Corrected Cross-Sectional Audit of 52 DePIN and DeFi Protocols" (chosen over "PCA-Corrected" to avoid the Principal-Component-Analysis collision for the econometrics audience). Cascaded to METADATA, README, cover letter, responses-master.
- **Conceptual-lineage citation orphans removed** (Cohen-1989, De-Filippi-2018, Bebchuk-Hirst); Polanyi-1944 cited at the Polanyian-interpretation mention. (Filippi et al. 2024 IS still cited at line ~588; only the 2018 entry was the orphan.)
- **Title-page date** April -> May 2026 (data-snapshot March-2026 + Token-Terminal/Blockworks April-2026 access dates preserved).
- **Section 3.3 Data Sources** expanded to 6 streams / 20 named sources (dropped unsubstantiated Arkham/Alchemy on the companion-session refinement; see CEX-audit residual #5 re: S5/S6 provenance, still author-open).
- **Supplements S10 / S12 / S21 sanitized** (stale section-refs, 40->52 framing, "eight of ten"->"thirteen of eighteen"; S21 heavy workflow-artifact removal: commit SHAs, DEC/KU/Pattern/SKILL IDs, clone paths, forward-planning section, HALT conditions).
- **Figure 4** (`media/exhibit_delegation_adjusted.png`): reorganized to grouped-by-category (DeFi/DePIN/Infra, ratio-ascending within).
- **Figure 6** (`media/fig7_subsidy_scatter.png`): excluding-Livepeer regression line now DRAWN (audit confirmed r=0.0561=canonical 0.06; the code comment's stale "0.027" removed) and extended across the full x-range (Livepeer is the rightmost point at 88.5x).
- **Flow / caption fixes:** §1.4.3 cross-ref + Solana-clause broadening; §2.6.2 disclaimer relocation; §2.7/3.1 four-vs-three decouple; Figure 3 caption "Initial insider allocation"; 9-item refinement batch (dead §2.8 ref, "Phase 3" build-label leak strip, S25 added to §6 index, Table 2 pointer, §1.1 dedup, etc.).

## CRITICAL coordination hazard (read before the build cycle)
The CEX-audit residual #1 (AT9 docx/pdf rebuild) and #2 (Figure 1 + Figure 2 regen) are now COUPLED with this companion session's edits. My earlier in-session docx rebuild (`submissions/B2_Frontiers_R2_clean.{docx,pdf}`) is STALE: it predates the CEX-audit numeric cascade (new Table 3/6 HHIs, p=0.011/d=1.05, io.net 0.040, Aethir/Helium rises). The FINAL build cycle must rebuild from the CURRENT PAPER.md so it captures BOTH (a) this session's title/citations/§3.3/captions/flow polish AND (b) the CEX-audit session's HHI cascade. Do not rebuild off either session's intermediate state alone. Likewise regenerate Figures 1 + 2 (CEX-audit residual #2) in the same cycle; Figures 4 and 6 are already current from this session.

## HELD items (author authorization required; do NOT proceed)
- **Public clone-A push** (irreversible): `/Users/zach/Tokenomics-As-Institutional_Design` (origin = Research-Publications-and-Data, PUBLIC replication repo) is ahead and NOT pushed. Standing directive "push everything except paper": the manuscript docx is excluded from the public push. Push command: `git -C /Users/zach/Tokenomics-As-Institutional_Design push origin main`.
- **True-redline tracked-changes:** the committed `B2_Frontiers_R2_tracked_changes.docx` is additions-only (no reliable headless redline tool here). Recommend author runs Word Compare: `submissions/B2_Frontiers_R1_clean.docx` vs the final rebuilt R2 docx.

## Provenance note
Orphan-cleanup commit `65c29089` also absorbed session 85783's intro enhancement via the shared working tree; a git note records this. Propagate the notes ref if needed: `git push origin refs/notes/commits`.

---

## Routed-items addendum (CEX-cascade session, commit 0f2060a8)

The 3 refinement-scan items routed into this session via the dispatch addendum (19f9740b) are DONE in commit `0f2060a8` (pushed):

1. **Aethir staleness — resolved toward 0.100, NOT the routed 0.095 (drift-direction inversion; flag for author).** The routed item assumed Aethir was a stale non-CEX row and said "correct to 0.095." The EVM audit falsifies that premise: Aethir has 3 confirmed Ethereum CEX wallets (Upbit Internal 2.58B, Bybit 657M, Bithumb 371M holdings, all Nansen-labeled), and excluding them (consistent with every other protocol) legitimately RAISED ATH 0.0948 to 0.1001. The routed-item author likely hit the HHI-direction gotcha (expected CEX exclusion to lower HHI, saw 0.1001 > 0.095, flagged it as stale). Aethir is now consistent at 0.100 across Table 3 row, Table 3 caption, Figure 1 caption, and the 4.4 subsidy trio. **If the author has Aethir-specific context that says 0.095 is correct (e.g. those CEX labels are disputed), say so and I will revert Aethir to 0.095 and exempt it from CEX exclusion.**
2. **Section 4.3 vs 4.6 permutation/bootstrap:** the contradiction was already gone (4.6 had no conflicting numbers post-cascade); collapsed 4.3's standalone LOO/permutation/bootstrap battery to a one-clause pointer and placed the single canonical battery (new post-CEX values) in 4.6.
3. **Intro/4.4 subsidy-trio duplication:** Intro trimmed to a value-free summary clause; full trio kept in 4.4 with recomputed HHIs (io.net 0.125 to 0.040; Aethir 0.095 to 0.100; Aave 0.013 unchanged).

Note: a parallel companion session (PID 17254) did the OTHER refinement-scan items (title, citations, date, supplements S10/S12/S21) and closed at e242309c; lanes did not collide (my routed edits all matched count==1, confirming the companion had not touched those regions).
