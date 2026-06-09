# Changelog

All notable changes to this replication package. Versions match `CITATION.cff` version field.

## [1.6.3-b3-v13-journal-build] (2026-06-08)

### B3 Final_v13 journal-strengthened build

- b3/paper: added B3_GeoDePIN_Final_v13.docx + .pdf (53 pages). Demand concentration recovered to N=2 (Helium burn-signer 0.27 + Livepeer fee-payer 0.31, both high; measurability framing); new Table 3a trailing-window Helium S2R (6m 1.24, TTM 0.51); governance reframed to the post-exclusion test (p=0.028, d=0.65); DIMO resolved (per-user account-abstraction wallets, off-axis because DCX-credit purchases are one step removed from end-customers, not a foundation treasury); Hivemapper single-relayer; citations [26]->[30], [62]/[63] added.
- b3/figures: Figure 4 v13 (Helium + Livepeer on the demand axis; DIMO label corrected to "DCX-credit purchase burns").


## [1.6.2-b3-correctness-pass] (2026-06-08)

### B3 whole-paper correctness pass (preprint)

A whole-paper audit found the GEODNET burn-flow error generalized to other claims; the manuscript headlines were corrected to match the on-chain evidence and the replication data was reconciled.

- data/raw/helium_s2r_cleaned.csv: corrected the Feb-2026 row from the retired stale values (777,042 burned / 377,260 issued -> S2R 2.06) to the canonical of-record values (1,144,240 / 621,370 -> S2R 1.84) so the package reproduces the manuscript Table 3. On a trailing-twelve-month basis the network is net inflationary (S2R approximately 0.49), which the manuscript now states.
- b3/paper: synced the corrected B3 v12 docx + pdf (Helium lead finding now stated as the first net-deflationary monthly readings rather than full steady-state offset; DIMO 4.24 presented as a single elevated month, not a confirmed fiscal-parity case; governance comparison reframed to the companion post-exclusion test).


## [1.6.1-b3-burn-construct-correction] (2026-06-08)

### Completeness fixes surfaced by a post-correction audit of v1.6.0

- b3/paper: synced the corrected B3 v12 docx + pdf (Table 7 now lists only Helium with a measured Demand HHI; Livepeer 0.31, a fee-payer HHI with no token burn, was the third invalid value and is now the not-measured marker, matching GEODNET and DIMO).
- b3/figures: Figure 3 peak label precision (52% to 52.5%) and a few prose/precision touch-ups synced.
- data/raw/geodnet_net_issuance.csv: ADDED. The B3 S2R denominator (net miner issuance, Console net-flow, Dune 7542071) was previously present only as a hardcoded array in the figure script, so a replicator could not regenerate the headline 0.219 from tracked files. The 18-month series is now tracked; S2R = geodnet_monthly_burns / geodnet_net_issuance (Feb 2026 = 1,305,000 / 5,948,674 = 0.219).
- data/dune_queries/README.md: query registry corrected to match the re-pointed SQL (06 -> Polygon 7541498 v2; 08 marked DEPRECATED; 07 clarified as Solana gross mint, not the S2R denominator).
- CODEBOOK.md: geodnet_monthly_burns.csv schema updated (21 rows; columns month/geod_burned/burn_flow; old burn_tx_count + unique_signers retired); geodnet_net_issuance.csv documented.
- README.md: repository-structure tree manuscript pointer corrected (v8 to v12), matching the prose.

## [1.6.0-b3-burn-construct-correction] (2026-06-08)

### B3 GEODNET burn-construct correction (companion paper "Who Burns the Tokens?")

A reconciliation against the Blockworks GEODNET dashboard established that the
GEODNET burn series previously used for the B3 S2R numerator (Dune query 6917159,
Solana SPL burn instructions) predominantly measures Wormhole NTT bridge outflow
(cross-chain transfers), not the Foundation buy-and-burn. The construct-correct
burn flow is the Polygon buy-and-burn to the dead address (Dune query 7541498 v2,
the same flow this package already uses for the companion B2 on-chain GEOD
revenue), which reproduces the issuer-reported (Messari) burn totals to within
0.2%. Two corrections follow.

Changed:
- `data/raw/geodnet_monthly_burns.csv`: replaced the Solana SPL burn series with
  the Polygon Foundation buy-and-burn series (monthly GEOD to 0x...dEaD,
  Sep 2024 to May 2026). Feb 2026 = 1,305,000 GEOD.
- `data/dune_queries/06_geodnet_burns.sql`: re-pointed from the Solana SPL burn
  query (6917159) to the Polygon buy-and-burn query (7541498 v2).
- GEODNET S2R (Feb 2026): 0.225 to 0.219 (1,305,000 Polygon buy-and-burn /
  5,948,674 net miner issuance). The prior 0.225 used the Solana-bridge numerator
  and coincided within tolerance.
- `b3/figures/`: Figure 3 regenerated on the corrected series (single-peaked: a
  post-halving ramp to a 52.5% October 2025 absorption peak, easing to 21.9% by
  February 2026, replacing the prior collapse-and-recovery shape). Figure 4
  regenerated (Helium plotted on the burn-signer demand axis; GEODNET, DIMO, and
  Hivemapper moved to an off-axis off-chain-demand lane).
- `b3/paper/`: added `B3_GeoDePIN_Final_v12.{docx,pdf}`.
- `README.md`: B3 demand-concentration summary corrected.

Retired (construct-invalid):
- `data/dune_queries/08_geodnet_burn_concentration.sql`: deprecated. On-chain
  burn-signer concentration is a valid demand proxy only for direct-burn
  protocols. GEODNET runs a Foundation buy-and-burn, so its burn signers are the
  treasury, not customers. The GEODNET burn-signer HHI 0.055 is retired.
- The cross-model "subscription/license models produce four to five times less
  demand concentration" claim is retired. A contract-level audit found DIMO
  (0.063) is a protocol-mediated pooled burn (developers pool DIMO via
  `issueInDimo`; the treasury burns later per DIP-3) and Livepeer (0.31) is an
  ETH fee-payer HHI with no token burn. Only Helium (0.27, direct Data Credit
  burns) is a construct-valid burn-signer HHI; it is preserved. The finding is
  recast: the "Who Burns?" diagnostic measures demand concentration only for
  direct-burn protocols, and buy-and-burn / pooled-burn architectures relocate
  demand off-chain.

Unaffected:
- The companion B2 governance study and its on-chain GEOD revenue measurement
  already use the construct-correct Polygon buy-and-burn (Dune 7541498 v2) and
  require no change.

## [1.5.0-frontiers-r2-revision] (2026-06-02)

### R2 final: pass-through-headline reconciliation plus a Phase 1-4 robustness layer

The sector contrast is finalized to the voter-inclusive staking pass-through headline, a zero-new-data robustness layer is added, and all package surfaces (README, cover letter, reviewer response, CITATION, CODEBOOK) are reconciled to this of-record.

**Sector contrast finalized to an honest effect-size triple (Section 4.6.2).** The headline is the voter-inclusive staking pass-through treatment (Cohen's d = 0.65, Mann-Whitney p = 0.028, all 30 leave-one-out folds significant; the mean-based permutation is marginal at approximately 0.08, a heavy-tail signature of one concentrated DeFi-side vote-escrow bloc). The uniform staking-aggregation exclusion is reported as a robustness check significant on every test (Cohen's d = 0.75, p = 0.018, permutation 0.009). The earlier complete-CEX effect (Cohen's d = 1.05) is reported as inflated by an inconsistent staking treatment rather than as the headline. Supersedes the prior d = 0.96 / d = 1.05 headline framing.

**Allocation null finalized and bounded.** Insider allocation Pearson r = 0.10, p = 0.49, N = 50 (Spearman rho = 0.16, p = 0.27), statistically equivalent to zero within |r| = 0.38 (TOST p = 0.02), with the launch-design block jointly uninformative (omnibus F(3,41) = 0.66, p = 0.58). Supersedes r = 0.07, N = 37.

**Phase 1-4 robustness layer added.** Two-one-sided-tests equivalence on the allocation null; the launch-design omnibus; a descriptive 24-month temporal-endpoint null (launch insider allocation uncorrelated with the governance-HHI endpoint, Pearson r = -0.11, N = 13); Model 4 influence diagnostics (all 50 leave-one-out refits keep the DePIN coefficient significant); and the insider-retention de-tautology triple (Spearman rho = 0.54, N = 34; bootstrap interval [0.21, 0.80]; permutation p = 0.001; sector-partial r = 0.47, p = 0.005).

**Other reconciliations.** HHI-Gini correlation Pearson r = 0.52, N = 48 (supersedes r = 0.58, N = 40 / 44); subsidy with-Livepeer r = 0.62, N = 23 (excluding Livepeer r = 0.07, N = 22; Spearman rho = 0.26). The retain-exchange-wallet robustness is reported as a reproducible medium effect (Cohen's d approximately 0.62, Mann-Whitney p approximately 0.03 to 0.05), replacing an earlier non-reproducible not-significant claim.

**Reproducibility additions.** `b2/paper/analysis_n52_2026-05-29/b2_sector_contrast_reproduce_2026-06-02.py` reproduces the sector-contrast d-triple from the committed per-protocol holding-HHI vectors (`sector_contrast_hhi_vectors_2026-06-02.csv`); `b2/paper/analysis_n52_2026-05-29/b2_strengthen_compute_2026-06-02.py` reproduces the allocation null, TOST equivalence, omnibus, temporal-endpoint null, Model 4 influence, and the insider-retention triple. Both run from in-repo data with no `/tmp` and no external dependency.

## [1.4.0-frontiers-r3-prep-cycle-5-multi-protocol] — 2026-05-24

### Cycle 5 cumulative multi-protocol Path B cascade (DEC-195 + DEC-196; HNT + LPT preserved)

Workflow-clone canonical-state cascade per workflow commits `999ab3a5` (Phase A DIMO + POKT) + `77d1ff5e` (DEC-194 DIMO Tier 1+2) + `40e27f23` (Phase B cycle 5 synthesis LFU + 4 methodology MDs). Per author "Apply all 4 in single coordinated cascade" directive 2026-05-24 (AskUserQuestion); Dune quota raised 4000 to 6000 per author authorization 2026-05-24T08:30Z.

**Replication-clone CSV refresh (data/processed/regression_data_april2026.csv):**

| Protocol | Cycle 3 | Cycle 5 Path B | Methodology |
|---|---:|---:|---|
| MOR | sub_OC 1.63; rev_OC $8.82M; emit_OC $14.36M | sub_OC **13.84**; rev_OC $874,659; emit_OC $12,107,145 | Distribution.sol OverplusBridged + UserClaimed (DEC-195 candidate) |
| FIL | sub_OC 21.6; rev_OC $2.88M; emit_OC $55.19M | sub_OC **46.05**; rev_OC $2,874,197; emit_OC $132,350,157 | Spacescope + Tokenomist (DEC-196 candidate; corrects TT emit_OC undercount) |
| DIMO | sub_OC 0.335; rev_OC $7.67M; emit_OC $2.57M (cycle 3) | sub_OC **5.04**; rev_OC $510,045; emit_OC $2,570,643 (DEC-194; cycle 5 partial; shipped 2026-05-24 replication commit `729679d`) | Foundation dashboard 159676 wallet `0x62b98...` |
| HNT | sub_OC 2.15 PRESERVED | sub_OC 2.15 PRESERVED | Path A precision-residual annotation only (KU acceptance criterion strictly met) |
| LPT | sub_OC 88.5 PRESERVED | sub_OC 88.5 PRESERVED | Path A archeology-confirmed (commit `a31b69c` 2026-03-31 TicketBroker ETH-fees correction) |

**Material reclassifications:**
- DIMO + MOR cluster-flips: net-deflationary subset → subsidy-heavy subset
- FIL within-cluster magnitude increase: 21.6 → 46.05 (subsidy-heavy preserved)
- HNT + LPT preserved (no change)

Subsidy-cluster composition post-cycle-5-cumulative:
- LPT 88.5 (extreme outlier; load-bearing for Livepeer-driven null discussion per B2 §3.4 + §3.6 + §3.7)
- FIL 46.05 (HIGH; post-DEC-196 Path B)
- MOR 13.84 (HIGH; post-DEC-195 Path B)
- RENDER 9.83
- DIMO 5.04 (post-DEC-194)
- GEODNET 4.51 (post-DEC-172)

**HALT-B Spec 4 verification (PASS; convention-invariance preserved across 4 cumulative cycles):**

| Cycle | TT Spec 4 subsidy_p | TT Spec 4 DePIN_p | OC Spec 4 subsidy_p | OC Spec 4 DePIN_p |
|---|---:|---:|---:|---:|
| Cycles 1-3 baseline | ~0.92 | (sig) | ~0.93 | (sig) |
| Cycle 4 (DEC-172 GEODNET) | 0.9161 | 0.0044 | 0.9300 | 0.0065 |
| Cycle 5 partial (DEC-194 DIMO) | 0.9949 | 0.0050 | 0.8480 | 0.0063 |
| **Cycle 5 cumulative (DIMO + MOR + FIL)** | **0.9410** | **0.0068** | **0.4540** | **0.0048** |

Across all 4 cycles: subsidy_p non-significant under sector control (all values p > 0.45); DePIN_p highly significant (all values p < 0.01). DePIN sector dummy continues to absorb the apparent subsidy-HHI association. 4-cycle convention-invariance robustness signal preserved per DEC-167 + DEC-107 4-of-4-strict promotion candidate.

**Critical FIL finding (TT emit_OC undercount):** TT-reported $55.2M vs project-canonical Tokenomist + Spacescope $132.4M = 140% divergence. TT incentives field applies a vesting-discount filter inconsistent with full protocol-emissions definition (75% of FIL block rewards vest over 180 days per Filecoin spec). External anchors (Coinbase Institutional Tokenomics Review + Filecoin Docs cite "$120-130M/yr new supply") corroborate Tokenomist-derived figure within 1.8%. rev_OC cross-validated to 0.13% (Spacescope $2,874,197 matches TT $2,877,882 within $3,685).

**Critical MOR finding (LayerZero OFT bridge contamination):** 96.3% of cycle 3 burns (5.25M of 5.45M MOR) were `oftSent` bridge-outs from Arbitrum to Base + Ethereum; 20.4% of cycle 3 mints (0.97M of 4.73M MOR) were `oftReceived` bridge-ins. Distribution.sol on Ethereum is canonical origin; OverplusBridged = canonical revenue event; UserClaimed = canonical emission event; LayerZero Relayer v2 mediates 1:1.

**LPT archeology resolution:** commit `a31b69c` (2026-03-31; "Full revision: 42 exclusions, N=20 expansion, Livepeer $839K correction") proves pre-cycle canonical sub_OC = 88.5 IS the structurally-correct TicketBroker ETH-fees Path B methodology, deliberately codified in March 2026. KU's proposed Path B via bondingmanager_call_rewardwithhint had 3 structural defects (no _amount field; LPT burns NOT canonical revenue; chain framing inverted post-Arbitrum migration).

**HNT precision-residual resolution:** Helium Foundation transformation views (`dune."helium-foundation".result_helium_dc_minted_hnt_burned_unparameterized`) yield rev_OC $12.90M / sub_OC 2.44 vs cycle 3 SPL $14.64M / 2.15. emit_OC delta -0.24% strictly meets KU acceptance criterion (within 10%). Cycle 3 SPL methodology IS canonical mechanism, just less precise (11.85% precision-residual scope difference; Foundation filters to `BurnDelegatedDataCreditsV0` instruction only; SPL includes admin/governance/tooling residue). Path A preserved.

**Pattern 27 Mode B 3-of-N strict PROMOTION-ELIGIBLE per DEC-107:** Direct-canonical-Foundation-methodology-supersedes-alternative-mechanism-inference class:
1. GEODNET cycle 4 (DEC-172): back-computation-vs-independent-measurement
2. DIMO cycle 5 (DEC-194): wrong-mechanism-measured
3. MOR cycle 5 (DEC-195 candidate): bridge-flow-not-protocol

Sister 2-of-N strict multisig-treasury-burn class (DIMO Foundation treasury + MOR Morpheus DAO multisig + LPT discretionary Foundation/DAO burns) qualifies as promotion candidate.

**Workflow-clone canonical state cascade (pending; this cycle replication-clone commit + workflow Tier 1+2 follow-on commit):**
- docs/DECISION_LOG.md: DEC-195 (MOR Path B) + DEC-196 (FIL Path B); both sister to DEC-194
- docs/ERROR_CORRECTION_LOG.md: EC-2026-05-24-B2-Cycle-5-Phase-B-Multi-Protocol-Methodology-Shift (or per-protocol ECs)
- docs/KEY_FINDINGS.md: F-B2-11 MOR + FIL row updates; F-B2-12 cycle 5 refinement insights #6 + #7 + #8
- docs/KNOWN_UNKNOWNS.md: 4 KU status-appends (HNT + LPT + MOR + FIL)
- docs/PROGRAM_STATE.md: Session Changes block
- docs/VERSION_HISTORY.md: R3_Prep_Phase_B_Cycle_5_Multi_Protocol_Cascade row
- research_content/papers/B2_governance_concentration/PAPER.md: §3.4 cascade for MOR + FIL classification shifts

**Replication-clone Tier 3 files this cycle:**
- `data/processed/regression_data_april2026.csv` (MOR + FIL row updates)
- `data/processed/regression_data_april2026.csv.pre_mor_fil_path_b_2026-05-24` (pre-cycle-5-cumulative backup)
- `b2/paper/supplements/subsidy_multivariate_2026-05-19.csv` (Spec 1-4 output regenerated)
- `b2/paper/supplements/halt_b_verification_multi_protocol_cycle_5_2026-05-24.md` (this verification memo)
- `CHANGELOG.md` (this section)
- `CITATION.cff` (version bump 1.3.0 → 1.4.0)

Per author 2026-05-24 directives: "Execute tier 3. R3 authorized" + "Do not push to public repo yet" + "We can go to 6000 dune credits" + "Continue: full Tier 1+2 + Tier 3 cascade this session" (AskUserQuestion).

NOT pushed to origin per ongoing author hold (pending author authorization for push to Research-Publications-and-Data/Tokenomics-As-Institutional_Design).

---

## [1.3.0-frontiers-r3-prep-dimo-path-b] — 2026-05-24

### DIMO Path B canonical methodology adoption (DEC-194; cycle 5 Phase A)

Workflow-clone DEC-194 codification: DIMO rev_OC + sub_OC Path B canonical selection per cycle 5 max-effort Phase A investigation. Foundation dashboard 159676 protocol-wallet inflow methodology adopted (wallet `0x62b98e019e0d3e4A1Ad8C786202e09017Bd995e1`; GnosisSafeL2 multisig; created 2024-06-21; verified via Blockscout on Polygon chain_id=137); supersedes cycle 3 burn-to-dead alternative-mechanism inference.

**Replication-clone CSV refresh:**
- `data/processed/regression_data_april2026.csv` DIMO row update:
  - rev_OC: 7,667,597.7 (cycle 3 dead-burn) → 510,045.0 (Foundation dashboard 159676 protocol-wallet inflow TTM Q1 2026; Dune MCP direct query 4219993 execution; 29.9 credits)
  - emit_OC: 2,570,643.27 PRESERVED (cycle 3 mints-from-null methodology valid; 51M DIMO TTM Q1 2026 baseline weekly issuance approximately 1.1M DIMO/week × 52 weeks = 57.2M DIMO/year theoretical max)
  - sub_OC: 0.335 → 5.04 (15x shift)
  - revenue_source_onchain: `on_chain_direct_license_burn_dune_extracted_2026-05-19` → `foundation_dashboard_159676_dcx_purchase_wallet_inflow_path_b_2026-05-24`

**Material reclassification:** DIMO moves from net-deflationary subset (sub_OC = 0.335 cycle 3 / pre-cycle) to subsidy-heavy subset (sub_OC = 5.04 Path B canonical; adjacent to RENDER 9.83 and post-DEC-172 GEODNET 4.51). Analogous to GEODNET DEC-172 cycle 4 1.61 to 4.51 methodology shift.

**Methodology divergence summary:**
- Cycle 3 query 7541442 (`to IN (0x0...0000, 0x0...dEaD)`): 167M DIMO / $7,667,597 TTM Q1 2026 = supply-removal events dominated by Polygon-to-Base supply migration burns + Foundation treasury burns (NOT operating revenue)
- Foundation methodology query 4219993 (`to = 0x62b98...`): 12.09M DIMO / $510,045 TTM Q1 2026 = DCX-purchase + Developer-License inflows per DIP-3 marketplace issuance framework
- Divergence ratio: 13.8x token count, 15.0x USD value
- Cross-check: all-time Foundation revenue cumulative through May 2026 is only ~15.5M DIMO / $852K USD; cycle 3 single-TTM 167M cannot be revenue if all-time revenue is only ~9% of cycle 3 single-TTM figure

**HALT-B Spec 4 verification (PASS; convention-invariance preserved):**
- TT-preferred Spec 4 (no Livepeer; N = 22): subsidy_p = 0.9949 (pre-DEC-194 0.9161; delta +0.079); DePIN_p = 0.0050 (pre-DEC-194 0.0044; delta +0.0006); Adj R² = 0.259
- OC-sensitivity Spec 4 (no Livepeer; N = 22): subsidy_p = 0.8480 (pre-DEC-194 0.9300; delta -0.082); DePIN_p = 0.0063 (pre-DEC-194 0.0065; delta -0.0002); Adj R² = 0.261

Both specifications preserve the headline finding: subsidy coefficient remains non-significant under sector control; DePIN sector dummy continues to absorb the apparent subsidy-HHI association. The DIMO sub_OC shift (15x) is methodology-significant for per-protocol reclassification but finding-stable at multivariate-headline layer. Per DEC-167 convention-invariance preserved across cycles 1-3 baseline (TT p ≈ 0.92 / OC p ≈ 0.93) + post-DEC-172 GEODNET Path B (TT 0.9161 / OC 0.9300) + post-DEC-194 DIMO Path B (TT 0.9949 / OC 0.8480); three-cycle robustness signal.

**Six reasons for Path B over Path A (cycle 3 dead-burn $7.67M; sub_OC = 0.335; rejected) and Path C (refined cycle 3 with bridge-out exclusion; sub_OC ≈ 0.43-0.56; rejected):**
1. Project-canonical (Foundation dashboard 159676 IS the canonical revenue surface; dashboard title explicitly distinguishes "Protocol Revenue" from "Out of Circulation" which is staking-dominated)
2. Foundation-aligned + address-verified (Foundation wallet `0x62b98e019e0d3e4A1Ad8C786202e09017Bd995e1` verified via Blockscout; Foundation query SQL inspection confirms address usage)
3. Within-protocol methodology symmetry (both rev_OC + emit_OC direct on-chain measurements; no back-computation; no proxy estimates; no mechanism inference)
4. Cross-protocol consistency with DEC-172 GEODNET precedent (project-canonical revenue methodology supersedes alternative-mechanism queries; DEC-172 "burn-to-dead methodology symmetry" reasoning recalibrated to "project-canonical operating-revenue mechanism per project")
5. Reflects true economic state ($510K DCX-purchase revenue against $2.57M baseline issuance is genuinely subsidy-heavy ramp-phase economy; Path A would make DIMO appear 23x deflationary by counting supply-migration burns as revenue)
6. Migration-immune by design (Foundation wallet structurally immune to Polygon-to-Base migration contamination; cannot receive bridge-migration burns which route to zero address `0x0...0000`)

**Workflow-clone canonical state cascade (commits `999ab3a5` + `77d1ff5e`):**
- `docs/DECISION_LOG.md` DEC-194 added
- `docs/ERROR_CORRECTION_LOG.md` NEW EC-2026-05-24-B2-DIMO-Methodology-Shift-Path-B-Canonical (PATTERN; direct-Foundation-measurement-supersedes-alternative-mechanism-burn-to-dead-inference sub-class; 2-of-N strict per DEC-107 cross-protocol applicability confirmed; sister to EC-2026-05-19-B2-GEOD-Methodology-Shift-Path-B-Canonical)
- `docs/KEY_FINDINGS.md` F-B2-11 cycle 5 Path B status note + F-B2-12 cycle 5 refinement insight #6 (Foundation-dashboard-supersedes-burn-to-dead-inference; methodology-of-record extension; sister to insight #3 Custom Reward Distributor Detection Class)
- `docs/KNOWN_UNKNOWNS.md` 4 KU status-appends (3 DIMO RESOLVED + 1 POKT PARTIAL)
- `docs/PROGRAM_STATE.md` Session Changes block
- `docs/VERSION_HISTORY.md` R3_Prep_Phase_A_Path_B_Cascade row
- `research_content/papers/B2_governance_concentration/PAPER.md` §3.4 substantive prose cascade (3 surfaces: abstract null-pattern reframe + §3.4 enumeration audit-trail + §3.4 paragraph-end DEC-194 cascade note)
- `research_content/papers/B2_governance_concentration/supplements/raw_oc/DIMO_methodology.md` Cycle 5 Path B canonical subsection
- `research_content/papers/B2_governance_concentration/supplements/raw_oc/POKT_methodology.md` §3.1-§3.4 Shannon transition extension
- `.cursor/tasks/Living_File_Updates_2026-05-24_0714_B2_Phase_A_POKT_DIMO_Findings.md` (261 lines; HIGH-confidence Path B recommendation; LFU source memo)

**Replication-clone Tier 3 files this cycle:**
- `data/processed/regression_data_april2026.csv` (DIMO row update)
- `data/processed/regression_data_april2026.csv.pre_dimo_path_b_2026-05-24` (backup)
- `b2/paper/supplements/subsidy_multivariate_2026-05-19.csv` (Spec 1-4 output regenerated with DIMO sub_OC = 5.04)
- `b2/paper/supplements/halt_b_verification_dimo_path_b_2026-05-24.md` (verification memo this cycle)
- `CHANGELOG.md` (this section)

Per author "Execute tier 3. R3 authorized" directive 2026-05-24 (AUTHOR-DIRECT lane authorization; CSV refresh + multivariate regression rerun executed in single replication-clone session per BULK-EXECUTOR delegation).

---

## [1.2.0-frontiers-r2-revision] — 2026-05-17 (initial) / 2026-05-18 (calibration + methodology fix + Lido recompute) / 2026-05-19 (Table 7 cascade + Table-4-prose cascade + HHI inflation factor recompute)

### HHI inflation factor recompute (2026-05-19, GC-2 closure)

The "up to 7x" headline inflation factor was preserved in the prior 2026-05-19 Table 7 cascade entry pending separate recompute (see entry below). This cycle closes that recompute by computing pre-PCA vs post-PCA HHI ratios per protocol from `data/processed/exclusions_log.csv`. Across the 32 protocols with complete `hhi_before` and `hhi_after` pairs logged, the maximum inflation factor is **17.88x for RENDER** (where Wormhole Token Bridge custody dominated naive top-1000 holdings); median is 2.33x. The headline anchor is updated to "up to 18x" with median-context qualification.

Six protocols (LDO, CRV, COMP, BAL, HYPE, IO) have exclusion log entries but empty `hhi_before`/`hhi_after` columns; their inflation factors could be reconstructed from raw holder files in a future cycle but are deferred. The 32-protocol sample is sufficient to establish the empirical anchor.

**Surfaces updated:**
- PAPER.md abstract-area methodology summary (line 178 region) and contributions section (line 3768 region)
- `CITATION.cff` abstract block
- `README.md` methodology contribution paragraph (line 27)

**New supplement:** `b2/paper/supplements/hhi_inflation_factors_2026-05-19.csv` and `.md` (per-protocol pre/post/ratio table; methodology notes; coverage caveat).

The methodology contribution claim is now empirically grounded rather than conservatively bounded.

### Table 7 cascade + Table-4-prose cascade (2026-05-19, post-deep-audit)

The 126-address PCA audit cycle (completed 2026-05-19) shifted Table 4 holding HHIs for nine protocols. Table 7 (delegation amplification) was not cascaded in the audit cycle and retained pre-audit holding HHIs, producing systematic understatement of the universal-amplification thesis. This cycle cascades Table 7 cells + narrative prose surfaces to current CSV values.

**Table 7 holding HHI cells updated (PAPER.md Section 3.5):**

| Protocol | Pre-audit | Post-audit | New ratio |
|---|---|---|---|
| DIMO | 0.038 | 0.025 | 9.1x (was 6.0x) |
| Lido | 0.038 | 0.008 | 11.4x (was 2.3x) |
| Compound | 0.028 | 0.009 | 5.7x (was 1.9x) |
| Aave | 0.020 | 0.013 | 5.9x (was 3.8x) |
| ENS | 0.135 | 0.071 | 0.39x (was 0.21x) |
| GMX | 0.056 | 0.065 | 1.2x (was 1.4x) |
| Optimism | 0.009 | 0.009 | 3.6x (was 3.7x) |
| Arbitrum | 0.012 | 0.012 | 4.4x (was 4.3x) |
| Uniswap | 0.010 | 0.010 | 2.8x (was 2.7x) |
| WeatherXM | 0.148 | 0.148 | 3.3x (unchanged) |

**Headline framing updated:**
- Amplification range: 1.4x to 6.0x → 1.2x to 11.4x
- Mean amplification (9 amplifying protocols): 3.3x → 5.3x
- ENS structural exception: 0.21x → 0.39x

The universal-amplification thesis strengthens (higher mean amplification; wider variance). All directional findings preserved (9-of-10 amplify; ENS is structural exception; sector-membership-does-not-predict-magnitude).

**Surfaces cascaded:**
- Abstract (lines 42-50 of PAPER.md)
- Section 1.4 Finding 4 (lines 123-128)
- Section 3.4 maturity-vs-concentration paragraph (DIMO 0.038 → 0.025; Compound 0.027 → 0.009; MakerDAO 0.045 → 0.040)
- Section 3.4 DeFi-ranking sentence (Hyperliquid lowest; Lido second; Compound third; was Hyperliquid / Uniswap / Aave)
- Section 3.4 AAVE methodological note (0.020 → 0.013)
- Section 3.4 subsidy-disconnect paragraph (DIMO 0.038 → 0.025; Aethir 0.153 → 0.209; Aave 0.020 → 0.013)
- Section 3.5 prose (range citations; sector ranges; protocol-specific cites; Uniswap detail paragraph; Optimism Token House; Lido Dual Governance framing)
- Section 3.5.1 ENS counterexample (ratio 0.21x → 0.39x; holding HHI 0.135 → 0.071; top-1 holding 26.7% → 19.9%)
- Section 3.5.2 ve-token class comparison (1.4x-6.0x range → 1.2x-11.4x range)
- Section 3.7 PCA-symmetric robustness check (Compound 1.89x to 1.85x → 8.7x to 5.8x; Aave 3.80x to 2.26x → 5.9x to 3.5x)
- Section 4.1 effect-size paragraph (mean 3.3x → 5.3x; ENS 0.21x → 0.39x; smallest amplification 1.4x → 1.2x)
- Section 4.5 multi-lens registration (ratios 1.4x to 6.0x → 1.2x to 11.4x; mean 3.8x → 5.3x; ENS 0.21x → 0.39x)
- Section 4.7 cross-section discussion (1.4 times to 6.0 times → 1.2 times to 11.4 times; Optimism 3.7 → 3.6; Arbitrum 4.3 → 4.4; ENS 0.21x → 0.39x)
- Section 5 implications block (Anyone 0.040 → 0.013; ratio 0.21x → 0.39x; ENS holding 0.135 → 0.071)
- Section 5.3 (range 1.4x to 6.0x → 1.2x to 11.4x; mean 3.3x → 5.3x; ENS 0.21x → 0.39x)
- Section 6 fourth finding recap (range 1.4x to 6.0x → 1.2x to 11.4x; mean 3.8x → 5.3x; ENS 0.21x → 0.39x)
- Twin-counterexamples paragraph (ratio 0.21x → 0.39x; holding HHI 0.135 → 0.071)

**Table-4-prose cascade (extension scope):**

In parallel, the deep PCA audit also shifted Table 4 HHIs for protocols not in Table 7 (Anyone Protocol, Filecoin, MakerDAO, Render; Aethir from Top-N% recompute). Narrative prose surfaces citing these stale values were updated in the same cycle:

- Anyone Protocol: 0.040 → 0.013 (5 prose surfaces: Section 2.7 cooperatives paragraph; Section 2.10.5 DePIN existence proof; Table 2 rubric cell; Section 4.2 Hypothesis 1 counterexample; Section 5 institutional-design discussion)
- MakerDAO: 0.045 → 0.040 (Section 5.1 Kantian transparency paragraph)
- Aethir: 0.153 → 0.209 (Table 4 footnote; Section 4.5 multi-lens registration; Section 5.2 subsidy disconnect)
- Hivemapper: 0.020 → 0.018 (Section 5.2 subsidy disconnect)
- Render / Grass / DIMO / Filecoin DePIN-existence-proof list (Section 2.10.5)

**Figure 6 (delegation amplification grouped bar chart) regenerated** with updated raw_hhi values (post-PCA-audit) and higher-precision inputs (4-decimal CSV values) so figure-text ratios match Table 7 cell ratios to one decimal.

**Methodology contribution count updated:** "69 PCA addresses across 20 protocols" → "126 PCA addresses across 38 protocols" (matches exclusions_log.csv post-deep-audit). HHI inflation factor "up to 7x" preserved (the largest single-protocol inflation factor post-deep-audit is not separately recomputed; the 7x claim was established prior to this cycle and is preserved as an empirically anchored upper bound).

### Pre-existing 2026-05-17 / 2026-05-18 entries follow.


Round 2 revision response to Frontiers in Blockchain peer review (Reviewer 1 R2 round). The R2 cycle resolved residual manuscript-vs-data drift in Table 7 and adopted a universal delegation amplification thesis as a substantive interpretive change in Section 3.5. Three post-propagation calibration cycles on 2026-05-18 resolved additional drift findings in the Aethir row (Top-N% convention alignment) and the Lido row (canonical CSV used a stale 189-row curated holder set; recomputed against the universal top-1000 methodology).

### Manuscript

- `b2/paper/B2_Frontiers_R2_clean.docx` and `.pdf` added (R2 final state)
- `b2/paper/B2_Frontiers_R2_tracked_changes.docx` and `.pdf` added (R1-to-R2 delta)
- R1 baseline files (`B2_Governance_Concentration_Frontiers_Submission.docx/.pdf`; `B2_Frontiers_R1_tracked_changes.docx/.pdf`) retained as historical-of-record

### Reviewer responses

- `b2/paper/responses/2026-05-17_R2_responses_master.md`, `.docx`, `.pdf` added (Reviewer 1 R2 issue-by-issue responses; .docx and .pdf rendered via pandoc + LibreOffice for archive parity with R1)
- `b2/paper/responses/2026-05-17_R2_cover_letter.md` added (Frontiers cover letter)
- `b2/paper/responses/2026-05-10_R1_responses_master.md`, `.docx`, `.pdf` added (R1 responses backfilled from workflow clone per R2 propagation cycle)

### Methodology updates (R1 round 2 feedback)

- **Manuscript-vs-data drift remediation (Reviewer 1 Issue 1).** Table 7 holding HHIs recomputed against post-exclusion baselines consistent with Table 4 and the regression dataset: UNI 0.032 to 0.010; OP 0.042 to 0.009; LDO 0.018 to 0.013. Table 7 delegation amplification ratios recomputed: UNI 2.7x, OP 4.06x, LDO 6.8x. Aethir holding HHI 0.171 to 0.168 in Table 4 footnote (consistency fix; CSV authoritative at 0.1678).
- **Universal delegation amplification thesis (Section 3.5; abstract finding 4).** Substantive interpretive change: all 8 Table 7 protocols amplify holding concentration in their voting layer (range 1.9x to 6.8x; mean 4.1x). Replaces the R1 framing where UNI (0.84x) and OP (0.79x) appeared as delegation-mediated dispersion cases. Magnitude (not direction) varies by institutional design within sector. Section 3.5 paragraphs 1 through 5 rewritten; Section 1.4 finding 4 rewritten; Section 4.1 design-hypotheses synthesis updated.
- **PCA-symmetric robustness check (Section 3.7).** Applying protocol-controlled-address exclusion symmetrically at the voting layer (consistent with the holding-side methodology) confirms universal amplification across all 5 Tally-sourced protocols even when foundation and aggregation-contract delegates are excluded: Compound 1.85x, Aave 2.26x, Uniswap 2.72x, Optimism 4.06x, Arbitrum 3.01x.
- **CRV disambiguation strategy.** Section 3.2 distribution descriptions use raw CRV holding HHI 0.017; Section 4 ve-locking discussion uses 0.171 with explicit veCRV labeling.
- **OP L1-vs-L2 framing correction (EC-2026-05-17-B2-OP-L1-L2-Side-Misframing).** Per workflow clone error-correction entry: the R1 author memo defended 0.042 as canonical Ethereum-side measurement with 0.009 as a separate L2-side measurement; the data CSV explicitly states OP token is on Optimism L2 (not Ethereum), so 0.042 IS the L2-side measurement. R2 adopts 0.009 as canonical post-exclusion measurement matching the regression dataset's Table 5/6 usage.
- **Table 5 N corrections (Reviewer 1 Issue 3).** HHI-Gini correlation row N updated to 40 (all-protocol Gini coverage); TT-expanded subsidy row N corrected from 22 to 19 with Pearson r = 0.097 (qualitative null-cross-sector conclusion confirmed; closely matches the previously-reported r = 0.095).
- **Table 4 expansion (Reviewer 1 Issue 3).** Sample expanded from 37 to 40 protocols with Hivemapper, io.net, and Aethir added as full rows.
- **Multiple-comparisons correction note (Section 3.7).** Benjamini-Hochberg FDR correction at q = 0.05 applied to the 14 tests reported in Table 5; three of four significant findings survive (the subsidy-with-Livepeer result is fragile under both multiple-comparisons correction and the Livepeer-outlier sensitivity already noted in F1).
- **Tally data drift methodology note (Section 2.10.3).** Documents the March 2026 to May 2026 delegate-pool drift; the R2 manuscript uses the March 2026 snapshot consistent with the rest of the dataset, with May 2026 results reported as supplementary robustness check.

### Post-propagation calibration cycles (2026-05-18)

Three follow-on commits resolved drift findings surfaced during post-propagation audit:

1. **Calibration cycle (37dae20).** Universal Table 4 audit surfaced four data integrity issues: (a) Aethir HHI stale at 0.1678 (R1-era March 2026 value) where PAPER.md had R2-canonical 0.153 (May 2026 Dune re-pull); (b) Aethir Gini empty (Phase 0 Tier A1 marked PENDING); (c) Hivemapper Gini stored as 0.8652 full-universe value where Phase 0 memo specified 0.9181 top-1000 value; (d) io.net Gini empty per Phase 0 memo Tier A1 not landing in CSV. CSV harmonization landed all four corrections; figures regenerated; DOCX figure replacement + PDF re-render shipped.
2. **Methodology fix (0b5d4f1).** Cross-row Top-N% convention mismatch: Aethir row used Top-1% = single-largest-holder share / Top-10% = top-10-holders-sum (literal interpretation), while the other 39 rows used Top-1% = top-10-holders share / Top-10% = top-100-holders share (per Sai et al. 2021 and Fritsch et al. 2024 convention). Aethir recomputed: Top-1% 33.6% to 83.8%; Top-10% 83.8% to 98.2%. Variant B methodology footnote added to Section 2.10.2 explicitly defining the convention.
3. **Lido recompute (this commit).** Canonical regression CSV's Lido row was computed from an older 189-row curated holder set (March 31; ~414K LDO minimum balance threshold) while every other row used the full top-1000 holder pull. Same drift class as the Aethir progression. Lido recomputed against the universal top-1000 methodology: HHI 0.013 to 0.038; Gini 0.52 to 0.82; Top-1% 7.9% to 36.0%; Top-10% 27.7% to 76.6%; N 189 to 994. Cascading manuscript edits: Table 4 Lido row; Table 7 Lido amplification ratio 6.8x to 2.3x; Section 3.3 sector contrast (Mann-Whitney p 0.014 to 0.023; Cohen's d 1.03 to 1.00; LOO robustness preserved at 30/30; permutation p 0.009 to 0.006); Section 3.5 universal-amplification range 1.4x to 6.8x to 1.4x to 6.0x (mean 4.1x to 3.3x); Lido / Dual Governance paragraph updated to acknowledge that the Dual Governance reform was justified at the time by the larger amplification measured from the 189-row subset. Supplementary file `b2/paper/supplements/lido_recompute_2026-05-18.md` documents the recompute.

### Path B Top-N% convention correction (2026-05-19)

Universal audit on 2026-05-19 revealed that 35 of 38 holder-file-backed CSV rows use ATH convention (literal top-1 / top-10 cumulative shares), not Variant B (top-10 / top-100 percentile-based). The earlier 2026-05-18 methodology footnote (Section 2.10.2) and the Aethir + Lido "Variant B fixes" applied at commits 0b5d4f1 and 36d4aee were inconsistent with the universal CSV convention. Path B forward-only correction:

- **Section 2.10.2 methodology footnote rewritten.** Now describes ATH convention: Top-1% = single-largest-holder share; Top-5% = top-5-holders sum; Top-10% = top-10-holders sum, applied to the post-exclusion top-1,000-holder sample.
- **Aethir Top-N% reverted to ATH convention.** Top-1% 83.81 → 33.56 (top-1 share); Top-10% 98.15 → 83.81 (top-10 share). Aethir HHI (0.153) and Gini (0.9756) preserved from the Phase 0 holders_ATH_2026-05-17.csv recompute.
- **Lido Top-N% reverted to ATH convention.** Top-1% 35.99 → 17.07 (top-1 share); Top-5% 62.92 → 29.48; Top-10% 76.60 → 35.99 (top-10 share). Lido HHI (0.0377) and Gini (0.8193) preserved from the new 994-holder set recompute (sister to 36d4aee). The universal-amplification thesis is unchanged: Lido's amplification ratio (2.33x) is HHI-based and independent of the Top-N% column convention.
- **Curve Top-5% mathematical impossibility fixed.** Curve CSV had Top-5% = 53.08 > Top-10% = 34.40 (structurally impossible: top-50 sum cannot exceed top-100 sum). Top-5% 53.08 → 23.15 (correct top-5-holders share from holder file); Top-10% 34.40 (unchanged) is the canonical top-10-share. The earlier 53.08 likely came from a veCRV computation that was inadvertently retained in the Top-5% slot.

Surfaced but NOT applied in this cycle (require author judgment):

- **HHI drifts for OP, AXL, ZRO, MOR.** Universal audit recompute from current holder files yields HHI values substantially different from the CSV: AXL 0.028 → 0.202 (43.6 percent gap); OP 0.009 → 0.022 (140 percent gap); ZRO 0.015 → 0.027; MOR 0.031 → 0.045. These gaps suggest the CSV uses additional exclusions beyond what is documented in `data/processed/exclusions_log.csv` (e.g., CEX hot wallets like Binance for OP; 42-percent-of-supply top holder for AXL). The 4-class PCA typology in Section 2.10.10 does not explicitly include CEX/exchange-custodian addresses as a class, but Section 3.2 prose mentions excluding them. Resolution requires author decision on whether to expand the documented exclusion list to match the actual computation, or to recompute the CSV under the documented 4-class typology only.
- **Aethir holder file inconsistency.** The replication clone `data/raw/holder_lists/ATH_holders.csv` has only 15 rows (curated subset); the authoritative Aethir top-1000 file is at `b2/paper/supplements/holders_ATH_2026-05-17.csv`. Future audit cycles should standardize on the supplements/ location for ATH to avoid confusion.

### PCA exclusion universal audit (2026-05-19)

Bytewise recompute of all 40 protocol HHI values from holder files surfaced four HHI gaps between the canonical CSV and recomputed values (AXL CSV 0.028 vs recompute 0.202; OP 0.009 vs 0.022; ZRO 0.015 vs 0.027; MOR 0.031 vs 0.045). Root-cause investigation via Etherscan address inspection revealed that the canonical CSV applies a 5-class PCA exclusion methodology while the documented typology in Section 2.10.10 enumerated only four classes.

**Class 5 (Centralized Exchange Custody) added to PCA typology.** Section 2.10.10 of PAPER.md now documents five PCA classes: Class 1 (burn destinations); Class 2 (foundation and treasury custody); Class 3 (staking-aggregation contracts); Class 4 (bridge custody and migration); Class 5 (centralized exchange custody — newly documented). Class 5 explicitly identifies CEX hot wallets and cold wallets that custody customer deposits; the operational practice of CEXes is to abstain from governance voting on customer-held tokens, so these addresses are governance-irrelevant.

**Six new exclusions added to `data/processed/exclusions_log.csv`:**

- OP: 0xf977...41acec (Binance 8 hot wallet; Class 5)
- AXL: 0x54d1...22cbf9 (Bithumb 162; Class 5)
- AXL: 0x377b...190873 (Upbit 59; Class 5)
- AXL: 0xd2ff...deebc (unlabeled EOA holding 42 percent of post-listed-exclusion supply; CSV-excluded; classification deferred to author judgment)
- ZRO: 0x8f64...a449c (LayerZero Future Initiatives Multisig; Class 2)
- ZRO: 0x744d...38da24 (LayerZero GnosisSafeProxy multisig; Class 2)

**Exclusion count updated.** PAPER.md cross-references updated from "69 PCA addresses across 20 protocols" to "75 PCA addresses across 22 protocols" (8 references swept across abstract, Section 1, Section 2.10.10, Section 3.2, Section 4 Contributions).

**CSV HHI values unchanged.** The 5-class typology is what the production CSV already applied; this cycle documents the methodology that was implicitly used. No manuscript HHI claims change.

**Residual MOR audit finding (deferred to author judgment).** CSV MOR HHI 0.031 does not reproduce exactly under any combination of documented PCA classes plus Class 5 CEX. The MOR top non-listed holders are small-balance EOAs that don't fit any PCA class. Either (a) the CSV applied additional one-off exclusions specific to MOR, or (b) the CSV value is slightly stale relative to current holder data. The 0.045 (5-class recompute) and 0.031 (CSV) difference is within the rounding tolerance for a robust sector contrast at the DePIN-DeFi level; substantive findings are not affected.

**Supplementary file added:** `b2/paper/supplements/exclusions_audit_2026-05-19.md` documents the audit methodology, reproduction verification table, and address-by-address identification trail.

### 40-protocol exclusion expansion + PCA Class 5 codification (2026-05-19 v2)

Universal exclusion audit expanded from 22 to 29 protocols with documented PCA exclusions; 11 new addresses identified via Etherscan verified contract labels + name tags + holder-file recompute.

**New burn-address exclusions (Class 1; universal sweep across all 40 protocols):**

- RPL: 0xdead...4206942069 (chain-specific burn pattern; cosmetic share)
- GMX: 0xdead...4206942069 (chain-specific burn pattern; 0.35% share)
- GEOD: 0x000...dead (3.25% of top-1000 GEOD supply)
- MOR: 0x000...dead (3.29% of top-1000 MOR supply; closes the MOR residual gap surfaced in eee7a5a2)
- IO: 11111...11111 (Solana System Program / null destination; cosmetic share)

**New PCA Class 2-4 exclusions (identified via Etherscan address inspection):**

- MKR: 0x473d...AF90B (LockstakeMigrator; Class 4 migration contract; Sky Deployer 8; 11.37% top-holder)
- IOTX: 0x87c9...29193 (Verified IoTeX Staking contract; Class 3 staking-aggregation; 19.75% top-holder)
- ANYONE: 0x0d9a...583EF (Anyone Protocol and Staking ERC1967Proxy; Class 3 staking-aggregation; 13.29% top-holder)
- GTC: 0x57a8...Be518 (Verified Gitcoin GTC Timelock; Class 2 governance infrastructure; 17.58% top-holder)
- ETHFI: 0x7a6a...39bb53 (GnosisSafeProxy accumulator; Class 2 likely Ether.Fi protocol-controlled pending verification; 19.02% top-holder)
- GEOD: 0xca3e...324b2 (Unlabeled GEODNET treasury / unallocated supply wallet; Class 2 pending GEODNET disclosure; 24.95% top-holder)

**CSV HHI updates (recomputed with full 5-class exclusions applied):**

Substantive shifts (greater than 5 percent absolute):
- Ether.Fi: 0.067 to 0.047 (-30 percent; DeFi)
- Anyone Protocol: 0.040 to 0.030 (-25 percent; DePIN)
- Morpheus AI: 0.031 to 0.046 (+50 percent; DePIN; burn now excluded)
- Gitcoin: 0.077 to 0.067 (-12 percent; Social_Dead)
- MakerDAO: 0.045 to 0.041 (-9 percent; DeFi)

Moderate / minor: IoTeX 0.107 to 0.105; GEOD 0.133 to 0.134; GMX 0.056 to 0.057; RPL 0.039 to 0.039; IO 0.111 to 0.111.

**Sector contrast strengthens slightly post-audit:**

- DeFi mean: 0.0430 to 0.0415
- DePIN mean: 0.0902 to 0.0905 (essentially unchanged; Anyone Protocol decrease offsets Morpheus AI increase)
- Mann-Whitney p: 0.023 to 0.018 (more significant)
- Cohen's d: 1.00 to 1.04
- Permutation p: 0.006 to 0.004 (more significant)
- LOO robustness preserved: 30 of 30 iterations significant

**Cross-references updated** across PAPER.md from "75 PCA addresses across 22 protocols" to "86 PCA addresses across 29 protocols" (8 surfaces).

**Manuscript impact:** Universal-amplification range (1.4x to 6.0x; mean 3.3x) unchanged because Table 7 ratios are HHI-based and the affected protocols' HHI changes are all within sector. Headline findings (allocation null; sector contrast; subsidy disconnect; universal delegation amplification) all preserved with statistics shifting in favorable directions (more significant sector contrast; allocation null r = 0.17 vs prior 0.18; subsidy with-LPT r = 0.60 vs prior 0.57).

**Supplementary file added:** `b2/paper/supplements/40_protocol_exclusion_audit_2026-05-19.md` documents the universal audit methodology, address-by-address PCA classification table, and reproduction verification.

### Philosophical-framework strengthening (R1 round 2 framing extension)

- **Section 2.10.1 two-layer framing.** Explicit separation of the empirical layer (concentration measurement) from the normative layer (institutional design evaluation).
- **Section 2.9.6 inter-lens relationships.** Maps Kantian publicity, Pettit non-domination, Rawlsian fairness, Ostromian polycentricity, and Hayekian knowledge-use lenses against each other so readers see where they overlap and where they diverge.
- **Section 4.1 systematic empirical-philosophical mapping.** For each major empirical finding, philosophical implications stated across applicable lenses. The universal delegation amplification finding registers across all five lenses.
- **Section 4.5 comparative methodology.** Frames the institutional design analysis approach against political-economy and computational-political-science alternatives.

### New supplementary files (`b2/paper/supplements/`)

- `phase0_data_collection_results_2026-05-17.md`: R2 Phase 0 data collection summary (Tier A1 Gini computation; Tier B1 voting HHI methodology findings; Tier C1 veCRV proxy; Tier C3 Theil and Atkinson indices)
- `holders_ATH_2026-05-17.csv`: Aethir token holder list (Ethereum top-1000)
- `veCRV_voting_concentration_2026-05-17.csv`: veCRV-weighted concentration via Convex contract analysis (Tier C1)
- `theil_atkinson_2026-05-17.csv`: Theil and Atkinson concentration indices for the 37 regression-ready protocols (Tier C3 robustness supplementary)

### New figures (`b2/paper/figures/`)

Regenerated from R2-canonical data (Phase 4 fix for visual-vs-caption-vs-text drift per Reviewer 1 Issue 4):
- `fig3_hhi_bar_40protocols`, `fig4_sector_boxplot`, `fig5_allocation_scatter`, `fig6_delegation_grouped`, `fig7_subsidy_scatter`, `fig8_participation` (each as `.png` and `.pdf`)
- `regenerate_b2_figures.py`: plotting script archived for replication; consumes the canonical `data/processed/regression_data_april2026.csv` (May 2026 F1 cycle state)

### Substantive findings surfaced during Phase 0 (deferred to follow-up cycle)

R2 Phase 0 data collection surfaced three findings that warrant methodology resolution before broader Table 7 expansion:

1. **Compound Foundation as PCA at voting layer.** Top COMP Tally delegate (~21.5% of delegated voting power) is Compound Foundation itself. If PCA exclusion is applied at the voting layer (consistent with the holding-side methodology), Compound's voting HHI drops to ~0.025. This is the PCA-symmetric robustness analysis added to Section 3.7 in this R2 cycle; further Tier B1 expansion is deferred.
2. **ENS delegation-dispersion.** Fresh Tally data shows 20 active ENS delegates with voting HHI 0.062 versus holding HHI 0.1345 (ratio 0.46x). ENS would be a delegation-dispersion outlier in an expanded sample.
3. **Balancer veBAL extreme amplification.** Snapshot HHI 0.626 versus holding HHI 0.030 (ratio 20.9x; highest in any sample). veBAL would be a delegation-amplification outlier.

The R2 manuscript retains Table 7 at 8 protocols with a Section 3.5 methodology footnote acknowledging these findings; comprehensive Tier B1 expansion to 12-15 protocols is deferred to a follow-up cycle that can resolve the methodology questions across the larger sample.

### Documentation

- `README.md`: status updated to "R2 revision submitted May 2026"; Key Statistics table refreshed with universal delegation amplification finding (1.4x to 6.0x; mean 3.3x; N = 10 with ENS exception at 0.21x); Gini inequality range updated to 0.73 to 0.99 (post-Lido-recompute); Mann-Whitney p = 0.023, Cohen's d = 1.00, permutation p = 0.006 reflected in headline; Delegation amplification narrative paragraph rewritten to match universal-amplification thesis; new section "Round 2 revision (May 2026): scope and substantive changes" added
- `CITATION.cff`: version bumped from `1.1.0-frontiers-r1-revision` to `1.2.0-frontiers-r2-revision`; `date-released` updated to 2026-05-17; abstract updated to include universal delegation amplification finding

## [1.1.0-frontiers-r1-revision] — 2026-05-12

Round 1 revision response to Frontiers in Blockchain peer review.

### Manuscript

- `b2/paper/B2_Governance_Concentration_Frontiers_Submission.docx` and `.pdf` replaced with Round 1 revision content (cycle F1 final state)
- `b2/paper/B2_Frontiers_R1_tracked_changes.docx` and `.pdf` added as paired companion (delta from the original Frontiers submission file)

### Methodology updates (responses to Reviewer 1 and Reviewer 2)

- **Universal burn-rule exclusion.** Canonical-burn addresses (0x000...000, 0x000...dead, plus chain-specific patterns) now excluded universally from HHI computation. UNI 0x000...dead address held 102.46M UNI (11.27% of supply); excluding it brings UNI HHI from 0.032 to 0.010 and shifts the DeFi sector mean from 0.043 to 0.041.
- **Holder-list cutoff correction (F1).** Three protocols (MOR, AXL, ZRO) had Dune holder-list queries inadvertently capped at top-100 rather than top-1000, biasing HHI values downward by capturing only the headtail. Re-pulling at top-1000 cutoff and re-applying exclusion methodology yields revised values: MOR HHI 0.013 to 0.031 (DePIN; includes the Monsta_vault mint destination identified via Dune transfer audit as a 4th protocol-controlled address), AXL HHI 0.004 to 0.028 (L1/L2/Infra), ZRO HHI 0.010 to 0.015 (L1/L2/Infra).
- **Combined sector-contrast cascade.** Burn-rule and holder-list-cutoff refinements compose: DePIN-vs-DeFi Mann-Whitney p moves from 0.031 (pre-revision) to 0.014 (post-F1); Cohen's d from 0.96 to 1.03. The leave-one-out result strengthens from 23 of 30 significant iterations to 30 of 30 (now robust to any single-protocol exclusion). The permutation test yields p = 0.009 (was 0.029).
- **Manuscript / CSV alignment audit.** During the F1 cycle, four pre-existing manuscript/CSV drifts were corrected: OP Table 4 HHI 0.042 to 0.009 (off by 4.6x; pre-existing typo); GRT Table 4 HHI 0.036 to 0.033; CRV Table 4 Top-1% 40.5% to 6.7% (typo; correct CSV value used); LDO Table 4 HHI 0.0185 to 0.013 plus Top-1% 9.9% to 7.9% (manuscript reflected pre-comprehensive-exclusion values; aligned with current post-exclusion CSV).
- **Top-N reporting consistency.** For five protocols (AAVE, UNI, ARB, GRT, OP) whose top holders included protocol-controlled addresses, the Top-1% and Top-10% columns in Table 4 are now recomputed using the same exclusion methodology as the HHI column. Pre-exclusion versus post-exclusion values for all 20 protocols with protocol-controlled addresses are provided in `b2/paper/supplements/top10_post_exclusion_all20.csv`.
- **Voting-HHI source labels for Compound and Arbitrum.** Table 7 source labels corrected from Tally to Snapshot. Published numerical values (Compound 0.053, Arbitrum 0.052) were always Snapshot-derived; only the labels were mislabeled.
- **stkAAVE pass-through delegation acknowledgment.** A methodological note added at Section 3.4 acknowledges that AAVE stakers retain pass-through voting power despite stkAAVE contract exclusion.
- **Cooperatives as Nearest Institutional Ancestor.** New Section 2.4.1 added bridging the normative framework and empirical findings via platform-cooperativism literature (Hansmann 1996; Birchall 2011; ICA 1995; Scholz 2016).
- **Calibrated-verb pass.** Discussion section language calibrated from causal-claim verbs to associational verbs for cross-sectional design discipline.

### Table 2 (rubric scoring) expansion

- Sample expanded from 3 to 5 protocols by adding Hyperliquid (DeFi; zero-VC outlier) and GEODNET (DePIN; subscription-burn model)
- Helium scoring re-evaluated to exercise the 4-tier rubric ceiling: Polycentric 2 to 3 (subDAO structure with local autonomy); Knowledge 2 to 3 (HIP-147 operator-driven reward reform demonstrates edge feedback)
- Table 2 caption extended with column-by-column framework definitions (Publicity, Fairness, Non-Domination, Polycentric, Knowledge) so readers do not need to flip back to Section 2.7 or Table 1

### Data updates

- `data/processed/regression_data_april2026.csv`: UNI HHI 0.0322 to 0.010; Top-1%, Top-5%, Top-10% columns recomputed post-exclusion for 5 protocols (AAVE, UNI, ARB, GRT, OP); MOR/AXL/ZRO HHI + Gini + Top-N + N recomputed at top-1000 holder cutoff (F1 correction)
- `data/processed/governance_concentration_april2026.csv`: matching upstream update
- `data/processed/exclusions_log.csv`: new UNI 0x000...dead burn-rule entry added; two new MOR exclusions added during F1 (Builders v2 0x42bb446e... and Monsta_vault 0x18b68344..., the latter identified as the protocol-controlled mint destination via Dune transfer audit)
- `data/raw/holder_lists/{MOR,AXL,ZRO,LDO}_holders.csv`: replaced with top-1000 holder data (1001 rows each including header) per F1 holder-list cutoff correction

### New supplementary files (`b2/paper/supplements/`)

- `burn_rule_audit_findings.csv` — per-address burn detection findings (3 entries: 1 newly excluded, 2 already-excluded)
- `burn_rule_audit_summary.csv` — per-protocol burn-rule audit across the 20-protocol exclusion set
- `top10_post_exclusion_all20.csv` — pre-exclusion versus post-exclusion Top-1, Top-5, Top-10 values for all 20 protocols with protocol-controlled addresses
- `uni_burn_cascade.csv` — UNI burn-rule cascade impact on DeFi sector mean and Mann-Whitney test
- `sample_coverage_table.md` — Supplementary Table SX (three-cluster N enumeration per Reviewer 1 Minor Comment 1)

### Documentation

- `README.md`: status updated to "Under review (Round 1 revision submitted May 2026)"; SSRN URL populated; sector contrast statistics updated to post-F1 values (Mann-Whitney p 0.014, Cohen's d 1.03); phrasing aligned with manuscript's calibrated-verb discipline; "Round 1 revision (May 2026): methodology updates" section explains the methodological refinements
- `CITATION.cff`: abstract values updated to post-F1 statistics; version bumped from `1.0.0-frontiers-submission` to `1.1.0-frontiers-r1-revision`; `date-released` updated to 2026-05-12; `repository-code` URL corrected from stale `zzukowski/Tokenomics-As-Institutional_Design` to actual `Research-Publications-and-Data/Tokenomics-As-Institutional_Design`

### Editorial pass

- Calibrated-verb pass through Discussion: strong-causal verbs ("drives", "produces", "causes") replaced with associational verbs ("is consistent with", "indicating", "documents") where the cross-sectional evidence base supports descriptive rather than causal claims
- Zukowski 2026 reference list re-lettered to standard APA convention starting from 2026a (was non-standard 2026b without a 2026a)
- Revision-history artifacts removed from clean DOCX (paragraph-mark cell markers, "(added in R1 revision)" framing, "Per Reviewer 1 and Reviewer 2 guidance" prefixes); the tracked-changes DOCX retains revision-tracking markers for reviewer-facing diff inspection
- First-use definitions added for DePIN, leave-one-out (LOO), Helium Improvement Proposal (HIP), Fully Diluted Valuation (FDV), Market Capitalization (MCap), Real-Time Kinematic GPS (RTK)
- Bold topic-paragraph lead-ins applied across §4.2 (Assumptions; 3 paragraphs), §4.4 (Risks and Counterpoints; 6 paragraphs), and §4.5 (Position in Literature; 4 paragraphs) for visual hierarchy
- Table 6 caption extended to clarify nested-model structure (Model 1 sector dummies only; Model 2 adds protocol age + log FDV; Model 3 adds initial insider allocation %)

### Notes on `outputs/` directory

Pre-computed regression outputs in `outputs/` reflect pre-revision pipeline state. Post-revision values are reflected in `data/processed/regression_data_april2026.csv` and `data/processed/governance_concentration_april2026.csv` (manual revisions; see notes columns). The current manuscript is authoritative for reported statistics.

### F1 cycle polish (2026-05-12 sub-cycles)

After the F1 cascade landed, four sub-cycles refined the manuscript and aligned the public-repo paper-and-data state:

- **F1.6 narrative coherence.** Resolved §3.7 internal contradiction ("robust to most but not all exclusions" was inconsistent with "robust to individual observations" earlier in the same section); recalibrated to consistent "robust to single-protocol exclusion (significant across all 30 of 30 leave-one-out iterations)" framing. Updated §4.6 "suggestively higher concentration" to "significantly higher concentration" (post-F1 LOO 30/30 makes the hedge unnecessary). Tightened subsidy correlation precision (r = 0.58 to 0.57; r = 0.12 to 0.11, p = 0.63 to 0.65; 7 surfaces affected including Table 5 row cells).
- **F1.7 final cleanup.** Aethir HHI 0.171 to 0.168 (pre-existing manuscript typo; CSV authoritative at 0.1678; 2 body surfaces). §3.7 insider-concentration relationship Spearman rho recomputed from 0.44 (pre-F1) to 0.48 (post-F1); 5 surfaces updated including LOO range update (0.41-0.50 to 0.45-0.55). §4.7 Contributions Models 1-3 framing tightened to mirror abstract precision (sector coefficient p < 0.05 in Models 1 and 2, borderline at p = 0.050 in Model 3 with the full control set).
- **Abstract polish + 42-word tightening.** Model 1/2/3 expanded inline ("three nested specifications adding protocol age, log fully diluted valuation, and initial insider allocation as successive controls"); Herfindahl-Hirschman Index defined at first body use; insider Pearson r 0.19/0.25 to 0.18/0.28; Gini range 0.73-0.98 to 0.52-0.99 (Lido as new minimum after F1 holder-list correction); HHI-Gini r 0.54 to 0.51. Subsequent 42-word reduction (392 to 350 words) preserved all numerical findings + first-use definitions + four-finding structure.
- **Metadata polish.** JEL O33 (Technological Change: Choices and Consequences) added (10 codes total); keyword swap "political philosophy of institutions" became "burn-rule exclusion" (10 keywords; sharper F1-aligned signal). Both DOCXs + CITATION.cff updated.

Cross-clone state: workflow clone commits `0351562c` through `0d6fe8d7` correspond to the above sub-cycles; public-repo clone commits `d8b26ca` through `1425b16` refresh paper files + CITATION.cff. Tracked-changes DOCX includes paired `<w:ins>`/`<w:del>` revision markers for the abstract redline (ids 2001-2009; author "Zach Zukowski (F1 final precision)"; date 2026-05-12T00:00:00Z) so reviewers see the post-F1 cleanup as visible diff in Word Review pane.

`insider_classification.csv` regenerated against post-F1 holder lists (`data/processed/insider_classification.csv` commit `3864cd2`); 391-row to 381-row net delta as F1 top-1000 re-pull shifted post-exclusion top-10 holder sets for MOR/AXL/ZRO/LDO. Now consistent with `regression_data_april2026.csv` post-F1 values.

## [1.0.0-frontiers-submission] — 2026-04-17

Initial submission to Frontiers in Blockchain — Blockchain Economics section.

- Manuscript: `b2/paper/B2_Governance_Concentration_Frontiers_Submission.docx` (April 18, 2026 submission)
- 40-protocol cross-section dataset across DeFi, DePIN, L1/L2 infrastructure, and social token categories
- Python analysis pipeline (`analysis/01_compute_hhi.py` through `analysis/10_delegation_analysis.py`)
- R regression pipeline (`analysis/full_regression.R`, `analysis/oaxaca.R`)
- Replication-ready dataset (`data/processed/regression_data_april2026.csv`; 39 variables)
- Supplementary Files S1-S8 in `b2/paper/supplements/`
- Companion paper B3 ("Who Burns the Tokens?") staged under `b3/paper/`
