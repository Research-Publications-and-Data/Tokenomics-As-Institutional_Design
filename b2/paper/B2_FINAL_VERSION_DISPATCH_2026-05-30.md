# B2 final-version dispatch: remaining items to the final paper version

**As-of:** 2026-05-30T04:21:59Z.
**Reader MUST**, before acting on any specific item: run `python3 scripts/claude-code-sync.py` (workflow
clone) and grep current canonical files + this repo's data for every cited identifier; canonical + dataset
state advances across parallel sessions and may have moved past this timestamp.
**Supersedes/extends:** `b2/paper/analysis_n52_2026-05-29/SESSION_HANDOFF_2026-05-29.md` (its "next cycle",
the Nansen re-classification, is now DONE; its 3 open author decisions are folded in below as A5/A3/A6).

## Clone map (this work spans two clones)

- **clone-A `/Users/zach/Tokenomics-As-Institutional_Design`** (this repo): the B2 manuscript
  (`b2/paper/B2_Frontiers_R2_clean.docx` is the current version), response letters
  (`b2/paper/responses/`), data (`data/processed/`, `data/raw/holder_lists/`), `reproduce.py`, and all the
  analysis in `b2/paper/analysis_n52_2026-05-29/`. The final-version docx surgery + data work happens HERE.
- **workflow clone `/Users/zach/Tokenization_Systems_Website`**: `docs/` canonical state (KEY_FINDINGS,
  DATA_REGISTRY, etc.) via the CANONICAL-WRITER lane; `handoff/dispatch/`. Canonical-state propagation of
  the findings happens there (see the two /tmp handoff-backs).

## Where the paper is

Frontiers submission, currently at **R2** (`B2_Frontiers_R2_clean.docx` + `_tracked_changes.docx`, dated
2026-05-27; R2 responses at `responses/2026-05-17_R2_responses_master.md` + `2026-05-26_R2_cover_letter`).
The **final version** (call it R3 / the resubmission) must incorporate the methodology work below. Headline
(DePIN governance concentration) is settled and robust; the remaining work is (a) author decisions on a few
methodology refinements that change published HHIs/insider counts, then (b) applying them and rebuilding the
manuscript + response letter.

## What this session produced (all surfaced, NOTHING applied; frame + v3 untouched)

Three commits in clone-A (`6ab5c64`, `b2a30a8`, `d2b96b1`) under
`b2/paper/analysis_n52_2026-05-29/nansen_reclass_2026-05-29/`:
1. Nansen-grounded insider re-classification of all 45 Nansen-reachable frame protocols (closes audit gaps
   G4/G6/G7). Four classification vectors produced, hardened by on-chain evidence into a fifth:
   - `insider_retention_vector_v4_traced_2026-05-30.csv` is the RECOMMENDED classification of record
     (Nansen labels + Blockscout contract/Safe resolution + Nansen deployer/signer traces).
2. Staking-PCA governance audit (both author directives): staking that retains bloc-voting should not be
   PCA-excluded; team/foundation/insider tokens locked in staking are hidden by wholesale exclusion.
3. Gap-fill + follow-ons A/B/C/D: resolved the decision-flippers with evidence; corrected the
   "any multisig = insider" over-count.

Headline is robust across SIX insider-retention vectors (DePIN p: keyword 0.0062, traced 0.0119, reviewed
0.0274; retention regressor n.s. throughout; maturity anchor 0.0395 reproduces `reproduce.py`). The
methodology refinements do NOT move the finding; they harden auditability and most plausibly strengthen the
insider-concentration story.

## Canonical inputs (read these first)

In `b2/paper/analysis_n52_2026-05-29/nansen_reclass_2026-05-29/`:
- `b2_followon_ABCD_FINDINGS_2026-05-30.md` (the latest synthesis: Safe-trace correction + attribution).
- `b2_gapfill_and_staking_audit_FINDINGS_2026-05-30.md` (the staking audit + gap-fill).
- `b2_nansen_reclass_FINDINGS_2026-05-30.md` (the re-classification + the 6-vector headline).
- Vectors: `insider_retention_vector_v4_traced_2026-05-30.csv` (recommended), plus `_v4_resolved_`,
  `_v4_reviewed_`, `_v4_nansen_` (keyword).
- Per-survivor: `b2_nansen_insider_classification_v4_TRACED_2026-05-30.csv` (the auditable spine).
- Staking: `staking_audit/governance_findings_2026-05-30.json`,
  `staking_audit/directive2_insider_stakers_2026-05-30.json`,
  `staking_audit/followon_B_D_findings_2026-05-30.json`, `staking_audit/safe_deployer_traces_2026-05-30.json`.
- Headline harness: `b2_nansen_v4_headline_impact_2026-05-29.py` (+ `_results_2026-05-29.json`).
Plus: `/tmp/b2_staking_audit_handoff_back_to_canonical_writer_2026-05-30.md` (the canonical-state items, with
the appended follow-on round); `reproduce.py` (repo root); `b2/paper/responses/2026-05-17_R2_responses_master.md`;
`B2_Frontiers_R2_clean.docx`.

---

## SECTION A: author decisions (GATES before the final version)

These change published HHIs/insider counts, so they need an author call. Recommendations given; the headline
survives every option. Resolve A1-A8, then proceed to Section B.

- **A1. Insider classification of record.** Adopt `v4_traced` (the evidence-based vector: multisig = insider
  only if deployer/signer is team-confirmed)? RECOMMENDED yes. Effect vs the un-persisted v3: corrects both
  directions; the traced evidence lowers DIMO 0.4->0.1, GEOD 0.3->0.1, MKR 0.3->0.2, MOR 0.5->0.2,
  WXM 0.4->0.2 (independent whales' Safes were wrongly counted as team) and raises others where Nansen found
  real insiders (UNI a16z, COMP Geoffrey Hayes, ENS Nick Johnson, BAL vested-shareholders).
- **A2. Staking attribution pass.** Apply attribution (add each holder's staked balance back to that holder
  before excluding the staking-contract shell)? RECOMMENDED yes for the material case. Quantified: stkAAVE
  holds 21.67% of AAVE supply, ~20.5% of it Aave team multisigs + founder -> ~4.4-6.3% of AAVE supply is
  insider AAVE currently hidden; ENA ~0.43%; FXS confirmed (Frax-team veFXS locker) but unsized.
- **A3. PCA-strict S2/S3 boundary** (carried from the prior handoff, decision #2). Tighten by excluding the
  surviving foundation/team/multisig as Class-2/3? Prior analysis: tightening STRENGTHENS the headline
  (maturity p 0.0395->0.0140; retention 0.0409->0.0107; MW 0.0364->0.0201) but changes published HHIs (e.g.
  WLFI 0.156->0.066) and re-derives WLFI/ENA/KMNO retention. Note this interacts with A1/A2; decide A1+A2+A3
  together as one coherent "what counts as insider/PCA" policy.
- **A4. Staking-exclusion reconsideration (from the governance audit).** LPT bloc-votes (transcoder
  delegation) -> move into the HHI. CRV/ENA/POL/IOTX/GEOD: staked tokens vote and excluding hides
  concentrated insider stake / creates a ve-token unit mismatch -> reconsider. AAVE/FXS/ETHFI/GNO/GMX/ANYONE/
  MPL_SYRUP: exclusion correct AFTER the A2 attribution pass. Decide which to act on for the final version vs
  footnote as a robustness/limitation.
- **A5. Retention prose lock 0.014-0.016 -> 0.040** (carried, decision #1). The reproduced retention-spec
  DePIN p is 0.0409 (now robust across 6 vectors). Update the claim of record + the R2/R3 response letter to
  report the reproduced 0.040 alongside the maturity-spec 0.0395. RECOMMENDED + low-risk (finding intact).
- **A6. Frame-stale Solana HHIs** (carried, decision #3): refresh JUP/DRIFT/HNT to the log-consistent S13
  values (JUP 0.126, DRIFT 0.057, HNT 0.087); headline-safe.
- **A7. HONEY retention** (N=49 -> 50): the retention-spec drops HONEY for a missing retention vector. v4
  supplies HONEY = 0.0 (Hivemapper distributors/retail). Adopt to lift retention-spec to N=50? Headline-safe.
- **A8. DOT capture-of-record**: the DOT_holders top-1 vs the S16 AssetHub capture vs the frame hhi=0.0052
  diverge; pick the capture of record (DOT retention ~0 either way). Minor; footnote.

---

## SECTION B: executor tasks (once A is decided)

- **B1. Reconcile the frame FIRST.** `data/processed/regression_data_april2026.csv` has carried uncommitted
  parallel-session changes (` M`) since 2026-05-29. Do NOT blind-overwrite. `git diff` it, reconcile the
  parallel changes with the A-decisions, and re-baseline a clean frame. HALT to the author if the parallel
  changes conflict with an A-decision.
- **B2. Apply the chosen vector + recompute.** Swap the retention vector to the A1 choice (v4_traced), apply
  A2/A3 HHI changes if elected, refresh A6 Solana HHIs, fold A7 HONEY. Recompute the HHI table + the
  retention/maturity/MW specs.
- **B3. Update `reproduce.py`** to read the elected vector (currently it reads v3 + new12; point it at the
  v4_traced vector of record) and the reconciled frame. Keep it one-command, no /tmp, no live-API.
- **B4. Re-run `reproduce.py` + the 6-vector headline harness; capture the canonical numbers** for the
  manuscript. Confirm the maturity anchor still reproduces and DePIN stays significant.

---

## SECTION C: build the final paper version (R3 / resubmission)

- **C1. Manuscript docx surgery** (produce `B2_Frontiers_R3_clean.docx` + `_tracked_changes.docx` from the
  R2 docx; use `cryptozach-docx-surgery-patterns`). Update: the HHI table + any changed values; the insider-
  classification description (now Nansen-label-grounded + Blockscout/deployer-verified, with the
  team-confirmed-multisig rule); a methodology paragraph for the staking treatment (attribution +
  bloc-voting + ve-token unit) per the A-decisions; the robustness subsection (the 6-vector retention table
  showing DePIN significant across keyword-floor to traced-evidence); the reproduced retention p (A5).
- **C2. Response letter (R3)** in `b2/paper/responses/`. Lead points: the headline reproduces and is robust
  to the entire insider-classification methodology (6 independent vectors, all significant); the insider
  layer is now source-cited + auditable (Nansen + Blockscout); the staking-attribution refinement
  (and the finding that it strengthens insider concentration); the bare-Safe-vs-team correction. Apply
  reviewer-facing surface discipline (no DEC/KU/F/EC/SHA; no internal-log identifiers).
- **C3. Exhibits/figures**: regenerate any figure whose HHI inputs changed (sector HHI distribution; the
  insider scatter). Cache-bust if any go to the site.
- **C4. Supplement**: add the Nansen-grounded insider classification of record + the staking-PCA audit as a
  supplement (the per-survivor `_TRACED_` CSV + the governance verdicts table); cite the reproducibility
  scripts.
- **C5. Submission-of-record**: stage the exact resubmission files at `b2/paper/` per the existing R1/R2
  naming; commit per the docx-surgery cadence.

---

## Canonical-state lane (parallel, workflow clone; CANONICAL-WRITER)

Independently of the paper, the two /tmp handoff-backs carry KEY_FINDINGS / DATA_REGISTRY / methodology
candidates (the robustness result; the v4_traced classification of record; the staking-attribution finding;
the insider-stakers-in-staking finding). Route via the CANONICAL-WRITER lane in the workflow clone; not on
the final-paper critical path but should land in the same arc.

## HALT conditions

- HALT if the frame reconciliation (B1) surfaces a parallel-session change that conflicts with an A-decision.
- HALT if applying A2/A3 moves the maturity-spec anchor across 0.05 (the prior S3 analysis put full-tighten
  at risk; the elected subset must keep the anchor significant) -> surface the exact spec to the author.
- HALT on any author-decision item in Section A that is not resolved before the corresponding B/C task.

## Acceptance tests (before declaring the final version done)

1. `reproduce.py` runs clean, one command, no /tmp, deterministic; maturity anchor reproduces (~0.0395).
2. The manuscript HHI table matches the reconciled frame exactly (cell-by-cell), and every changed value
   traces to an A-decision + an artifact in `nansen_reclass_2026-05-29/`.
3. The response letter's reported numbers match `reproduce.py` output (report the reproduced number).
4. No em-dashes in newly authored prose; reviewer-facing surfaces carry no internal-log identifiers.
5. Frame + the v4 artifacts are internally consistent (the vector of record == the manuscript's insider
   counts == reproduce.py's input).

## Remaining method limitations (need different data, not more calls)

- veCRV founder/team lock sizing needs a per-address veCRV balance snapshot (the 1Y counterparty flow misses
  the original locks). veCRV voting also concentrates via Convex/vlCVX (a separate bloc).
- A few GRASS survivors churned out of the current top-50 entirely (no current entity to resolve); they read
  as not-insider by the conservative rule.
- ~3,700 Nansen credits remain if the author wants the veCRV balance snapshot or further confirmations.

## Budget + provenance

Nansen spend across the two rounds ~8,000 of 11,700 cr; the bulk ran on free Blockscout + WebSearch. All
analysis scripts in `nansen_reclass_2026-05-29/` are reproducible from persisted inputs (no /tmp, no
live-API except the explicit keyed fetch scripts). Frame + v3 untouched throughout.
