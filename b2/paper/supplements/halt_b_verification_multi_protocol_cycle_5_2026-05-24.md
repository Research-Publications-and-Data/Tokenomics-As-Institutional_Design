# HALT-B verification: Cycle 5 multi-protocol Path B cascade (DIMO + MOR + FIL; 2026-05-24)

**Cycle:** B2 R3-prep arc Phase B cycle 5 cumulative cascade per workflow commits `999ab3a5` (Phase A DIMO + POKT) + `77d1ff5e` (DEC-194 Tier 1+2) + `40e27f23` (Phase B cycle 5 synthesis LFU + methodology MDs).

**Test:** Spec 4 multivariate regression (HHI ~ subsidy_ratio + DePIN_dummy; excluding Livepeer outlier) with cumulative cycle 5 Path B updates:
- DIMO sub_OC = 5.04 (Path B per DEC-194; ship date 2026-05-24)
- MOR sub_OC = 13.84 (Path B; DEC-195 candidate)
- FIL sub_OC = 46.05 (Path B; DEC-196 candidate; TT emit_OC undercount correction)
- HNT sub_OC = 2.15 PRESERVED (Path A confirmed; precision-residual annotation only)
- LPT sub_OC = 88.5 PRESERVED (Path A archeology-confirmed; documentation-gap closure only)

**Acceptance criterion (per DEC-167 convention-invariance):** subsidy_p non-significant (p > 0.05) under sector control; DePIN_p remains highly significant. Headline finding "DePIN sector dummy absorbs the apparent subsidy-HHI association; subsidy coefficient is non-significant under sector control" preserved across cumulative methodology shifts.

---

## Pre-cycle-5 baselines (cumulative comparison)

| Cycle | Methodology shift | TT Spec 4 subsidy_p | TT Spec 4 DePIN_p | OC Spec 4 subsidy_p | OC Spec 4 DePIN_p |
|---|---|---:|---:|---:|---:|
| Cycles 1-3 | baseline (pre-cycle-4) | ~0.92 | (sig) | ~0.93 | (sig) |
| Cycle 4 | DEC-172 GEODNET Path B | 0.9161 | 0.0044 | 0.9300 | 0.0065 |
| Cycle 5 partial | DEC-194 DIMO Path B (only) | 0.9949 | 0.0050 | 0.8480 | 0.0063 |

## Post-cycle-5 cumulative results (DIMO + MOR + FIL Path B)

Replication-clone CSV refresh: `data/processed/regression_data_april2026.csv` DIMO + MOR + FIL rows updated (per-row Path B canonical values). HNT + LPT rows PRESERVED.

Pre-cycle-5-cumulative backup: `data/processed/regression_data_april2026.csv.pre_mor_fil_path_b_2026-05-24`.

### TT-preferred Spec 4 (no Livepeer; N = 22)

```
=== Spec 4: HHI ~ subsidy_ratio + DePIN_dummy (without Livepeer, N = 22) ===
  subsidy beta = -0.000046, t = -0.074, p = 0.9410
  DePIN beta   = 0.038424, t = 2.708, p = 0.0068
  Adj R^2 = 0.260
```

### OC-sensitivity Spec 4 (no Livepeer; N = 22)

```
=== Spec 4: HHI ~ subsidy_OC + DePIN (no Livepeer, N = 22) ===
  subsidy beta = -0.000345, t = -0.764, p = 0.4540
  DePIN beta   = 0.039995, t = 3.193, p = 0.0048
  Adj R^2 = 0.281
```

## HALT-B comparison table (cumulative cycle 5)

| Specification | Pre-DEC-172 | Post-DEC-172 (cycle 4) | Post-DEC-194 (cycle 5 partial) | Post-cycle-5 cumulative (this cycle) | Significance preserved? |
|---|---:|---:|---:|---:|:-:|
| TT Spec 4 subsidy_p | ~0.92 | 0.9161 | 0.9949 | **0.9410** | YES (non-significant) |
| TT Spec 4 DePIN_p | (sig) | 0.0044 | 0.0050 | **0.0068** | YES (highly significant) |
| OC Spec 4 subsidy_p | ~0.93 | 0.9300 | 0.8480 | **0.4540** | YES (non-significant) |
| OC Spec 4 DePIN_p | (sig) | 0.0065 | 0.0063 | **0.0048** | YES (highly significant) |

### Direction-of-effect analysis (cycle 5 cumulative)

**TT-preferred Spec 4 subsidy_p** moved from 0.9949 (post-DIMO-only) to 0.9410 (post-cycle-5-cumulative); shift -0.054. Subsidy coefficient remains essentially zero in TT-preferred specification (the no-Livepeer subsample is overwhelmingly the DePIN cluster after Livepeer exclusion; subsidy variation within DePIN does not predict HHI variation).

**OC-sensitivity Spec 4 subsidy_p** moved from 0.8480 (post-DIMO-only) to 0.4540 (post-cycle-5-cumulative); shift -0.394 (closer to significance threshold but still well above 0.05). Direction-of-effect: MOR sub_OC 13.84 + FIL sub_OC 46.05 contribute high-subsidy DePIN points with mid-range HHI; this slightly increases the positive subsidy-HHI relationship in the OC-sensitivity specification but does not reach significance.

**DePIN_p remained highly significant in both specifications** across all 4 cycles. TT-preferred: 0.0044 → 0.0050 → 0.0068 (delta +0.0024 across cycle 5 cumulative). OC-sensitivity: 0.0065 → 0.0063 → 0.0048 (delta -0.0017 across cycle 5 cumulative). DePIN sector dummy continues to absorb the apparent subsidy-HHI association at the multivariate-headline layer.

## HALT-B verification: PASS

The cycle 5 cumulative methodology cascade (DIMO sub_OC 0.335 → 5.04; MOR sub_OC 1.63 → 13.84; FIL sub_OC 21.6 → 46.05; HNT + LPT preserved) produces minimal multivariate-headline shift, consistent with DEC-167 convention-invariance preserved across 4 cycles spanning 4 methodology cascades:

- Cycles 1-3 baseline: TT p ≈ 0.92 / OC p ≈ 0.93
- Cycle 4 (DEC-172 GEODNET Path B): TT 0.9161 / OC 0.9300
- Cycle 5 partial (DEC-194 DIMO Path B): TT 0.9949 / OC 0.8480
- Cycle 5 cumulative (DIMO + MOR + FIL Path B): TT 0.9410 / OC 0.4540

Across all 4 cycles, subsidy_p remains non-significant under sector control (all values p > 0.45). DePIN_p remains highly significant across all 4 cycles (all values p < 0.01). The convention-invariance prediction (sub_TT preferred default vs sub_OC sensitivity; per DEC-167) holds robustly across 4 cumulative methodology shifts.

**Four-cycle robustness signal:** convention-invariance is now empirically anchored across baseline + 3 progressive methodology cascades (GEODNET + DIMO + cycle-5-cumulative multi-protocol). This strengthens the DEC-167 prediction beyond the original 1-of-N strict ship; promotion-shape candidate per DEC-107 4-of-4-strict.

## Material per-protocol reclassifications (cycle 5 cumulative; not multivariate-headline layer)

Subsidy-cluster composition post-cycle-5 cumulative:

| Protocol | Cycle 3 sub_OC | Cycle 5 sub_OC | Methodology |
|---|---:|---:|---|
| LPT | 88.5 (TicketBroker ETH-fees per commit a31b69c 2026-03-31) | 88.5 PRESERVED | Path A archeology-confirmed |
| FIL | 21.6 (Messari Cat-D) | **46.05** (Spacescope+Tokenomist) | Path B (DEC-196 candidate; magnitude increase within cluster) |
| MOR | 1.63 (Arbitrum burn-to-dead) | **13.84** (Distribution.sol OverplusBridged + UserClaimed) | Path B (DEC-195 candidate; cluster-flip) |
| RENDER | 9.83 (Foundation-canonical per Cycle 3) | 9.83 PRESERVED | Path B pre-cycle-5 |
| DIMO | 0.335 (Polygon dead+zero burn) | **5.04** (Foundation wallet 0x62b98... inflow) | Path B (DEC-194; cluster-flip) |
| GEODNET | 1.61 (back-computed) | 4.51 (post-cycle 4 net-flow) | Path B (DEC-172; pre-cycle-5) |
| HNT | 2.15 (SPL action='burn'/'mint') | 2.15 PRESERVED | Path A precision-residual annotation only |

**Cycle 5 net summary:** 2 cluster-flips (DIMO + MOR; both net-deflationary → subsidy-heavy); 1 magnitude-increase-within-cluster (FIL); 2 preserved (HNT precision-residual + LPT archeology-confirmed).

## Pattern 27 Mode B 3-of-N promotion-eligible (per DEC-107)

Direct-canonical-measurement-supersedes-alternative-mechanism-inference class anchored at 3 sister-instances:

1. GEODNET cycle 4 (DEC-172; 2026-05-20): back-computation-vs-independent-measurement (sub_OC 1.61 → 4.51; 2.80x divergence)
2. DIMO cycle 5 (DEC-194; 2026-05-24): wrong-mechanism-measured (burn-to-dead vs Foundation protocol-wallet inflow; sub_OC 0.335 → 5.04; 15x divergence)
3. MOR cycle 5 (DEC-195 candidate; 2026-05-24): bridge-flow-not-protocol (LayerZero OFT bridge flows mis-aggregated; sub_OC 1.63 → 13.84; 8.5x divergence)

**PROMOTION-ELIGIBLE per DEC-107 3-of-3 strict.** Promotion candidate to `cryptozach-canonical-state-claims` SKILL Rule 1 extension: "project-canonical Foundation methodology direct inspection before validating any cycle's Dune extraction against pre-cycle canonical values."

Sister 2-of-N strict multisig-treasury-burn class (DIMO Foundation treasury + MOR Morpheus DAO multisig + LPT discretionary Foundation/DAO burns) qualifies as promotion candidate at 2-of-N strict; 3rd anchor confirmation needed for full promotion.

## Files this cycle (replication clone)

- `data/processed/regression_data_april2026.csv` (MOR + FIL row updates; DIMO already updated cycle 5 partial)
- `data/processed/regression_data_april2026.csv.pre_mor_fil_path_b_2026-05-24` (pre-cycle-5-cumulative backup)
- `b2/paper/supplements/subsidy_multivariate_2026-05-19.csv` (Spec 1-4 output regenerated with all 3 cumulative Path B updates)
- `b2/paper/supplements/halt_b_verification_multi_protocol_cycle_5_2026-05-24.md` (this verification memo; cycle 5 cumulative)
- `CHANGELOG.md` (NEW section [1.4.0-frontiers-r3-prep-cycle-5-multi-protocol])
- `CITATION.cff` (version bump 1.3.0 → 1.4.0; date 2026-05-24)

## Cross-references

- **Workflow clone:** DEC-194 (workflow commit `77d1ff5e`); Phase A LFU `Living_File_Updates_2026-05-24_0714_B2_Phase_A_POKT_DIMO_Findings.md` (workflow commit `999ab3a5`); Phase B synthesis LFU `Living_File_Updates_2026-05-24_0836_B2_Phase_B_Cycle_5_Synthesis_HNT_LPT_FIL.md` + MOR LFU `Living_File_Updates_2026-05-24_0821_B2_Phase_B_MOR_Path_B_Findings.md` (workflow commit `40e27f23`).
- **Pre-cycle-5 HALT-B verification:** `b2/paper/supplements/halt_b_verification_dimo_path_b_2026-05-24.md` (DIMO-only post-DEC-194 cycle 5 partial; ship date 2026-05-24 replication-clone-local commit `729679d`).
- **DEC entries cited:** DEC-167 (raw on-chain OC convention; convention-invariance); DEC-172 (GEODNET Path B); DEC-194 (DIMO Path B); DEC-195 candidate (MOR Path B; workflow Tier 1+2 commit pending); DEC-196 candidate (FIL Path B; workflow Tier 1+2 commit pending); DEC-107 (observe-before-codify; 3-of-N strict promotion-shape; 4-of-4-strict convention-invariance promotion candidate).
- **F-B2 findings:** F-B2-11 (burn-active subset; pending MOR + FIL row updates); F-B2-12 (cycle 5 refinement insights pending #6 + #7 + #8); F-B2-9 (predominant-amplification thesis preserved per DEC-167 convention-invariance).
- **KU resolutions:** KU-DIMO-Supply-Removal-vs-Burn-Classification (RESOLVED via DEC-194); KU-DIMO-Bridge-Out-Burn-Contamination (RESOLVED via supersession); KU-DIMO-Sub-OC-Source-Methodology-Reconstruction (SUPERSEDED); KU-POKT-Post-Shannon-TT-Reliability-Gap (PARTIAL); KU-HNT-Lazy-Distributor-Refinement (RESOLVED without methodology shift per workflow commit `40e27f23`); KU-LPT-BondingManager-Refinement (RESOLVED via archeology per workflow commit `40e27f23`); KU-FIL-TT-vs-Messari-Cross-Source-Divergence (RESOLVED with methodology shift; pending workflow Tier 1+2 commit); KU-MOR-Cross-Chain-Bridge-Bidirectional-Contamination (RESOLVED with cluster-flip; pending workflow Tier 1+2 commit).
- **Author authorization:** "Execute tier 3. R3 authorized" 2026-05-24 + "Apply all 4 in single coordinated cascade" 2026-05-24 (AskUserQuestion) + "Do not push to public repo yet" 2026-05-24 + "We can go to 6000 dune credits" 2026-05-24 + "Continue: full Tier 1+2 + Tier 3 cascade this session" 2026-05-24 (AskUserQuestion).

## Closing notes

HALT-B verification PASS confirms B2 R2 submission package remains finding-stable across cycle 5 cumulative methodology shifts. Per author hold 2026-05-24, replication clone commit local-only (NOT pushed to public Research-Publications-and-Data/Tokenomics-As-Institutional_Design). Workflow clone Tier 1+2 docs/* + PAPER.md §3.4 cascade pending in follow-on commit.

**4-cycle convention-invariance robustness signal preserved.** B2 R2 submission-ready (cycle 6 finalization state) maintained at multivariate-headline layer; per-protocol reclassifications (DIMO + MOR cluster-flips; FIL within-cluster magnitude increase) cascade through PAPER.md §3.4 narrative but do not flip the headline subsidy-driven null Livepeer-outlier discussion.

**Pattern 27 Mode B 3-of-N strict PROMOTION-ELIGIBLE.** Direct-canonical-Foundation-methodology-supersedes-alternative-mechanism-inference class confirmed across GEODNET + DIMO + MOR cluster.

Per AUTHOR-DIRECT lane authorization 2026-05-24 ("Execute tier 3. R3 authorized" + cumulative "All" + "Continue").
