# Changelog

All notable changes to this replication package. Versions match `CITATION.cff` version field.

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
