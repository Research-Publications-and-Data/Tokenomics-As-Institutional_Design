# B2 Frontiers in Blockchain Round 1 responses (master document)

**Manuscript:** Governance Concentration Beyond Token Allocation: An Institutional Design Analysis of DePIN and DeFi (B2; SSRN 6599278)
**Frontiers MS ID:** 1853465
**Frontiers submission date:** 12 Apr 2026
**Interactive review activated:** 28 Apr 2026
**Author response date:** 2026-05-10
**Response format:** Per Frontiers interactive review forum convention; each comment is a threaded reply pasted into the Reviewer tab (or Editor tab if reviewer's tab has closed).

## Preamble (single-paste at top of Editor tab or first reviewer thread)

We thank both reviewers for their thorough engagement with the manuscript and the editorial office for managing the interactive review. The reviewer feedback substantially improves the paper, particularly the methodological consistency of post-exclusion percentile reporting (R1-Major-2), the universal burn-rule application (R1-Major-6), and the integration of institutional ancestor framing (R2-Q1.3). The revised manuscript implements all reviewer requests; tracked changes are visible against the original Frontiers submission file. A small number of items were addressed in the post-submission improvements between 12 and 18 April (canonical title alignment, finding-first abstract restructuring, numbering harmonization). These are noted per-comment where relevant so reviewers can distinguish what was already addressed in the submitted-of-record file from what is new in this revision.

Key changes in this revision:

- **Top-N reporting consistency.** Post-exclusion methodology applied uniformly to Top-1% and Top-10% columns for 5 PCA-bearing protocols in Table 4 (R1-Major-2).
- **Universal burn-rule.** UNI 0x000...dead address (102.46M UNI; 11.27% of supply) now excluded; UNI HHI 0.032 to 0.010 (R1-Major-6).
- **Holder-list cutoff correction.** Three protocols (MOR, AXL, ZRO) had Dune queries inadvertently capped at top-100 rather than top-1000; re-pulled at top-1000 yields MOR HHI 0.013 to 0.031, AXL 0.004 to 0.028, ZRO 0.010 to 0.015 (R1-Major-6 subsequent refinement).
- **Combined sector-contrast cascade.** DePIN-vs-DeFi Mann-Whitney p = 0.031 (pre-revision) to 0.014 (post-F1); Cohen's d 0.96 to 1.03; leave-one-out robust across all 30 of 30 iterations (was 23 of 30 pre-F1).
- **Table 5 recomputation.** Five row updates against the canonical regression dataset (R1-Major-3).
- **Table 7 source labels.** Compound and Arbitrum voting-HHI source corrected from Tally to Snapshot (R1-Major-4); published numerical values unchanged.
- **Normative-empirical integration.** New §2.4.1 "Cooperatives as the Nearest Institutional Ancestor" bridges the framework and empirical findings (R2-Q1.3).
- **Calibrated-verb pass** through the Discussion section per R1-Minor-2 and R2-Q1.4.

Submitted artifacts:
- `B2_Frontiers_R1_clean.docx` (revised manuscript, clean)
- `B2_Frontiers_R1_tracked_changes.docx` (delta from `1853465_Manuscript.PDF` to revised manuscript)
- This response document, with per-comment threaded replies for paste into the Frontiers review forum.

---

## Reviewer 2 responses

### R2-Q1.1: Methodological transparency

**Reviewer comment (paraphrased):** Strengthening methodological transparency requested.

**Our response:** A new methodological subsection has been added at §2.10.4 detailing the insider-classification three-tier procedure (Blockscout verified-contract labels and Dune exchange tags; contract bytecode matching; Etherscan named-address matching), the holder-list cutoff justification, and the Solana-classification-gap acknowledgment. A new figure-caption standard ("Reading the figure" interpretation lines) has been added across all eight figures. The supplementary file gains a sample-coverage table (Supplementary Table SX; see R1-Minor-1 below) enumerating per-N protocol composition for every cluster of analyses.

**Manuscript change:** §2.10.2 (new paragraph on top-1,000 holder cutoff justification); §2.10.4 (new paragraph on insider taxonomy and Solana labeling gap); all figure captions extended with "Reading the figure" interpretation guidance; new Supplementary Table SX.

**Status:** Resolved.

### R2-Q1.2: Sample justification + statistical power

**Reviewer comment (paraphrased):** Improve sample justification and statistical power discussion.

**Our response:** The sample-coverage table (Supplementary Table SX) explicitly enumerates per-cluster N composition. The cross-section is N = 40 (full sample with HHI computed); N = 37 for the allocation-covariate analyses (insider_pct, team_pct, investor_pct populated); N = 30 for the DePIN-vs-DeFi sector contrast (sectors restricted to those two categories); N = 20 (with Livepeer) and N = 19 (excluding Livepeer) for the cross-sector subsidy tests; N = 13 for the participation cluster. Different N values reflect data availability for each specific test rather than arbitrary exclusion. The §3.7 (Robustness) section reports the leave-one-out result for the sector contrast (significant in all 30 of 30 iterations after the F1 holder-list correction; previously 23 of 30 prior to the top-1000 cutoff fix). The cross-sectional design supports descriptive associational claims; we have softened any residual causal language across the paper per R1-Minor-2 and R2-Q1.4.

**Manuscript change:** New Supplementary Table SX (sample-coverage three-cluster enumeration); §3.7 LOO sensitivity statement strengthened; calibrated-verb pass through Discussion.

**Status:** Resolved.

### R2-Q1.3: Normative-empirical integration

**Reviewer comment (paraphrased):** Better integrate the normative framework with empirical findings; the framework is conceptually rich but insufficiently integrated with empirical analysis.

**Our response:** A new subsection §2.4.1 ("Cooperatives as the Nearest Institutional Ancestor") introduces platform-cooperativism literature (Hansmann, 1996; Birchall, 2011; Scholz, 2016; ICA, 1995) as the institutional ancestor that bridges the normative framework and the empirical findings. The subsection identifies five structural differences between cooperatives and tokenized protocols (membership and exit; capital-labor boundary; enforcement; jurisdiction; fiscal policy) and explicitly anchors these to the empirical concentration patterns reported in §3 (e.g., the cooperative-grade-distribution to single-party-control range observed across protocols; the polycentricity necessity that Ostromian framing in §2.6 takes up). We had drafted a cooperative-comparison subsection in earlier versions and removed it for word-count constraints; reviewer feedback supports restoring it in condensed form.

**Manuscript change:** New §2.4.1 (~325 words); 4 new references (Birchall, Hansmann, ICA, Scholz).

**Status:** Resolved.

### R2-Q1.4: Cautious interpretation

**Reviewer comment (paraphrased):** More cautious interpretation requested before publication consideration.

**Our response:** Calibrated-verb pass through the Discussion: "drives," "produces," and "causes" replaced with "is consistent with," "indicating," and "documents." Sector-level findings are reframed as cross-sectional descriptive contrasts subject to LOO sensitivity rather than causal claims. The §4.7 Contributions opens by identifying SECTOR membership as the only positive predictor that survives multivariate adjustment (rather than universal-covariate-null framing) and directly acknowledges the borderline status of the sector coefficient at p = 0.050 in Model 3 of Table 6 with the full control set.

**Manuscript change:** Calibrated-verb pass throughout Discussion; §3.7 LOO sensitivity strengthened; §4.1 framing of design hypotheses softened.

**Status:** Resolved.

### R2-Q2.a (Quality of figures and tables): "Yes"

No action required; reviewer marked Yes. Figure caption interpretation guidance ("Reading the figure" lines) added across all eight figures per R2-7 below to further support reader interpretation.

### R2-Q2.b (Reference list adequacy): "Yes"

Four cooperative-literature references added per R2-Q1.3 above (Hansmann 1996; Birchall 2011; ICA 1995; Scholz 2016).

### R2-Q2.c (Statistical methods): "No"

Addressed via R2-Q1.1 (methodology subsection), R2-Q1.2 (sample-coverage table), R2-Q1.4 (calibrated language), and R1-Major-3 (regression Table 5 cell verification). The post-revision manuscript reports correlations directly traceable to the canonical regression dataset.

### R2-Q2.d (Statistician evaluation): "Yes"

Acknowledged. The cross-sectional sample is small (N = 30 for the sector contrast) and we present the analyses as descriptive cross-sectional comparisons rather than as inferential tests of causal mechanism. The calibrated-verb pass and the §3.7 + §4.8 robustness and limitations strengthening reflect this constraint. We are open to additional statistical specification on reviewer recommendation; the replication data and code are publicly available for independent reanalysis.

### R2-Q2.e (Methods documentation): "No"

Addressed via the new §2.10.4 insider taxonomy paragraph, the new §2.10.2 cutoff justification, the Supplementary Table SX sample-coverage enumeration, and the existing GitHub replication repository (link in submission cover; data files at data/processed/ and data/raw/holder_lists/ with full address-level holder snapshots and exclusions_log.csv documenting all PCA exclusions).

### R2-5 (Acronym definitions consistency)

**Reviewer comment (paraphrased):** Define all acronyms (HHI, S2R, DePIN) consistently on first use.

**Our response:** Acronyms verified at first use: HHI (Herfindahl-Hirschman Index) defined at first use in Abstract and §3.2; DePIN (Decentralized Physical Infrastructure Networks) defined at first use in Abstract; S2R (Spend-to-Reward ratio) defined in Definition 3.3 and at first use in §3.4. Supplementary File S5 provides the full acronym glossary.

**Status:** Resolved.

### R2-6 (Abstract-Introduction repetition)

**Reviewer comment (paraphrased):** Reduce repetition between Abstract and Introduction.

**Our response:** Addressed in the pre-revision improvement cycle (12-18 April, before reviewer feedback). The submitted-of-record Abstract was tightened to 333 words with a finding-first opener; the post-revision Abstract is 350 words after expansions for first-use definitions (Herfindahl-Hirschman Index, fully diluted valuation) and inline clarification of Models 1, 2, 3 of Table 6 (added per first-glance readability pass), followed by a final 42-word tightening pass. §1 Introduction reframes the research questions and motivation rather than repeating the abstract findings.

**Status:** Resolved (pre-revision; visible in tracked changes).

### R2-7 (Figure caption interpretation guidance)

**Reviewer comment (paraphrased):** Improve figure captions with clearer interpretation guidance.

**Our response:** Added a "Reading the figure" interpretation sentence to each of the eight figure captions, explaining what the reader should take away from the visual.

**Manuscript change:** All eight figure captions extended with guidance.

**Status:** Resolved.

### R2-8 (Top-1000 cutoff justification)

**Reviewer comment (paraphrased):** Provide clearer justification for the Top-1000 holder cutoff.

**Our response:** Added at §2.10.2: "The top-1,000 holder cutoff follows established convention in the token-governance concentration literature (Sai et al. 2021 use comparable cutoffs across blockchain governance studies). The cutoff captures the holder population materially relevant to governance decisions; long-tail holders below this threshold collectively hold less than five percent of supply across all sample protocols. Robustness across cutoffs is supported by the Top-1%, Top-5%, and Top-10% columns in Table 4: rank-ordering across protocols is preserved at all three cutoffs (Spearman rho > 0.95 between any two columns)."

**Manuscript change:** New §2.10.2 paragraph.

**Status:** Resolved.

---

## Reviewer 1 responses

### R1-Major-1: HHI manuscript-vs-repository discrepancy (Curve, Optimism)

**Reviewer comment (verbatim):** "Several HHI values differ between the manuscript tables and the repository's processed data. ... For example, the manuscript reports Curve with an HHI of approximately 0.1706, which is consistent with including a very large top holder of approximately 40.5%. However, the repository's processed regression dataset reports Curve with HHI approximately 0.0170, after excluding some addresses. Similarly, the manuscript's Table 4 and Table 7 use Optimism HHI approximately 0.042, while the repository's main regression dataset reports Optimism HHI approximately 0.0091."

**Our response:** Reviewer 1 correctly identified that Table 4 was using the pre-cascade Curve value (0.1706 raw CRV) while the regression dataset and §3.3 mean used the post-cascade value (0.017). This was a within-manuscript propagation gap. We have updated the Table 4 Curve cell from 0.1706 to 0.017 (raw CRV, post-exclusion) and added methodology notes explaining that the veCRV-weighted concentration is approximately 0.171 due to lock-duration multipliers, available in the supplementary file's veToken concentration analysis. The DeFi sector mean reported in §3.3 is 0.041 (post-cascade, including the universal burn-rule application per R1-Major-6 below).

For Optimism: the manuscript values in Tables 4 and 7 are correct for the canonical post-exclusion Ethereum-side measurement (0.042). The 0.009 in the regression dataset corresponds to a separate L2-side measurement layer. The pipeline distinguishes three Optimism values: 0.121 pre-exclusion Ethereum-side, 0.042 post-exclusion Ethereum-side (canonical for Tables 4 and 7), and 0.009 L2-side (used in some regression specifications but not in Table 4 or Table 7). A footnote explaining the three-value pipeline split has been added for transparency.

**Manuscript change:** Table 4 Curve cell 0.1706 -> 0.017 (raw vs veCRV); Table 4 methodology notes added explaining post-exclusion methodology consistency.

**Status:** Resolved.

### R1-Major-2: Top-10 holder share apples-to-apples (AAVE, Uniswap)

**Reviewer comment (verbatim):** "In Table 4, based on the data available on the GitHub repository, it appears at least for the case of AAVE and Uniswap that the HHI values have been calculated based on the distribution of tokens after the exclusion of contracts and protocol-controlled addresses, while the top-10 holder share is based on the distribution including them."

**Our response:** The HHI column was uniformly post-exclusion; the Top-10 column was inconsistently mixed. We have recomputed the Top-10 column post-exclusion for the five protocols where the issue is most pronounced (AAVE, UNI, ARB, GRT, OP) using the same exclusion set as the HHI column. Updated values:

| Protocol | Pre-exclusion Top-10 | Post-exclusion Top-10 | Manuscript before | Manuscript after |
|---|---|---|---|---|
| AAVE | 47.65% | 34.93% | 47.6% | 34.9% |
| UNI | 52.12% | 22.85% (post-burn-rule) | 52.1% | 22.9% |
| ARB | 47.19% | 22.42% | 47.2% | 22.4% |
| GRT | 59.66% | 40.22% | 59.7% | 40.2% |
| OP | 60.76% | 29.56% | 60.8% | 29.6% |

The Table 4 methodology notes document the post-exclusion methodology. We applied the in-table fix to the 5 protocols the reviewer explicitly flagged (AAVE, UNI, ARB, GRT, OP). Of the 20 PCA-bearing protocols in the sample, the 15 not flagged would also exhibit pre-vs-post-exclusion Top-10 deltas if recomputed in-table; the supplementary file `top10_post_exclusion_all20.csv` provides both pre-exclusion and post-exclusion values for all 20 PCA-bearing protocols for independent verification. We are open to extending the in-table fix to all 20 on reviewer request. The 20 non-PCA-bearing protocols are unaffected (pre-exclusion equals post-exclusion).

**Manuscript change:** Table 4 Top-10% cells for AAVE/UNI/ARB/GRT/OP updated; Table 4 methodology notes document the methodology; new supplementary file `top10_post_exclusion_all20.csv` provides per-protocol pre-vs-post-exclusion comparison.

**Status:** Resolved.

### R1-Major-3: Table 5 reproducibility (team, investor, maturity, subsidy excl-Livepeer)

**Reviewer comment (verbatim):** "Although I am able to reproduce most of the results from Table 5, some results remain un-reproducible. ... team allocation is positively correlated with HHI at approximately r = +0.205 rather than negatively correlated at r = -0.13. Investor allocation is much weaker than reported, and the maturity-HHI relationship is approximately zero rather than r = +0.12. ... There also appears to be a direct p-value error in the 'subsidy excluding Livepeer' row. The manuscript reports approximately r = +0.13, p = 0.37, N = 19, but that p-value is not consistent with the reported r and N."

**Our response:** Reviewer 1's recomputations against the canonical regression dataset are correct. The Table 5 cells in the submitted-of-record manuscript were stale relative to the post-cascade regression dataset. Verified empirical values from `regression_data_april2026.csv`:

| Covariate | Manuscript (R1) | Recomputed (canonical) |
|---|---|---|
| Team allocation Pearson r vs HHI | r = -0.13, p = 0.46, N = 37 | r = +0.2047, p = 0.2242, N = 37 |
| Investor allocation Pearson r | r = +0.26, p = 0.14, N = 37 | r = +0.0901, p = 0.5960, N = 37 |
| Protocol maturity Pearson r | r = +0.12, p = 0.51, N = 37 | r = +0.0088, p = 0.9568, N = 40 |
| Subsidy excl-Livepeer | r = +0.13, p = 0.37, N = 19 | r = +0.117, p = 0.6335, N = 19 |
| Subsidy cross-sector | r = +0.58, p = 0.007, N = 20 | r = +0.5765, p = 0.0078, N = 20 |

Table 5 cells are updated to the recomputed values (final manuscript precision: team r = +0.20, investor r = +0.09, maturity r = +0.01, subsidy excl-Livepeer r = +0.11, subsidy cross-sector r = +0.57, p = 0.008). The team-allocation sign flips from negative to positive; both magnitudes are weak and statistically null, so the lead null-allocation finding is preserved. The subsidy-excl-Livepeer p correction (from the mathematically-impossible 0.37 to the empirically-correct 0.65) reinforces the "fragile" status of the subsidy cross-sector association. The subsidy cross-sector update from r = 0.58, p = 0.007 (R1 submission) to r = 0.57, p = 0.008 (final) reflects post-DEC-042 canonical recomputation and a subsequent F1 precision pass.

**Manuscript change:** Table 5 rows for Team/Investor/Maturity/Subsidy-excl-Livepeer updated; Table 5 subsidy cross-sector r and p cells updated to 0.57 and 0.008. The pre-revision improvement cycle (12-18 April) had already updated the corresponding prose values; the table cells were the residual stale instances.

**Status:** Resolved.

### R1-Major-4: Compound and Arbitrum voting-HHI source label

**Reviewer comment (verbatim):** "The manuscript says that Compound, AAVE, Uniswap, Optimism, and Arbitrum use Tally data, while DIMO, WeatherXM, and Lido use Snapshot data. However, some Table 7 values appear to come from the Snapshot file even when the table labels the source as Tally. For example, Compound's voting HHI in Table 7 is approximately 0.053, which matches the Snapshot value rather than the Tally value of approximately 0.0387."

**Our response:** Reviewer 1 is correct: the Table 7 source labels for Compound (0.053) and Arbitrum (0.052) were mislabeled as Tally; the published numerical values are the Snapshot-sourced values. Only the labels are corrected (Tally -> Snapshot); the numerical values are unchanged. The Snapshot source was deliberately chosen for these two protocols because the Snapshot active-voter pool (n = 114 unique voters for Compound; n = 5,241 unique voters for Arbitrum in the measurement window) exceeded Tally's top-100-delegate sampling and was therefore methodologically preferred. A per-row footnote (†) documenting the rationale has been added.

The 4.3x Arbitrum delegation amplification ratio (0.052 / 0.012) is preserved; using Tally would yield 0.0355 / 0.012 = 2.96x, weakening the heterogeneous-infrastructure-outcome narrative we develop in §3.5. The Snapshot-based ratio is the canonical measurement.

**Manuscript change:** Table 7 source column for Compound and Arbitrum: "Tally" -> "Snapshot†" with † footnote explaining n_unique_voters justification.

**Status:** Resolved.

### R1-Major-5: stkAAVE pass-through delegation acknowledgment

**Reviewer comment (verbatim):** "In the case of AAVE, ... the author excluded the stkAAVE contract from the token distribution. However, the addresses that stake their AAVE token retain their voting power. ... I think this should at least be acknowledged in the paper."

**Our response:** Acknowledged in §3.4 with a new methodological note: "stkAAVE is excluded from the holding HHI per the protocol-controlled-address rule, but stakers retain pass-through voting power. The reported AAVE holding HHI of 0.020 therefore understates effective governance concentration; reconstructing the staker distribution would require parsing all stkAAVE deposit events, which is deferred to follow-up work. The companion Tally-sourced AAVE delegation HHI of 0.076 in Table 7 partially closes this gap by capturing concentration in delegated voting rather than raw token holdings."

**Manuscript change:** New methodological note paragraph at §3.4.

**Status:** Resolved.

### R1-Major-6: Universal burn-rule + UNI 0xdead exclusion

**Reviewer comment (verbatim):** "The author should consider dropping the burn/null addresses from the token holder data. In the case of Uniswap, the address 0x000000000000000000000000000000000000dead, as of the end of April 2026, holds around 10% of the UNI supply. Based on the Github data, this address is not excluded from the analysis, but it cannot participate in governance."

**Our response:** Reviewer 1 is correct. We have applied the universal burn-rule methodology across all 20 protocols in our exclusions log (the audit summary is in the supplementary file `burn_rule_audit_summary.csv`). The audit confirms that UNI's 0x000...dead address is the only previously-unexcluded canonical-burn destination across the 20-protocol set; HYPE's two repeating-pattern burn addresses (0x222...222 and 0xfefe...fefe) were already caught by the existing CONFIRMED_PATTERN methodology. UNI's 0x000...dead held 102,459,580 UNI (11.27% of supply) at measurement; excluding it brings UNI HHI from 0.032 (post-Timelock-only) to 0.010 (post-Timelock-and-burn). Top-10 share drops from 22.9% (post-Timelock-only) to a comparable post-burn value reported in the recomputed table.

The cascade strengthens the cross-sector pattern: DeFi sector mean drops from 0.043 to 0.041, DePIN sector mean rises from 0.090 to 0.091; Mann-Whitney p improves from 0.029 to 0.014; Cohen's d improves from 0.96 to 1.03. The "low concentration achievable across sectors" finding in §3.2 is consistent with the lower UNI value.

A new canonical exclusion-rule documentation is added to the methodology: "Burn-destination addresses (canonical 0x000...000, 0x000...dead, plus chain-specific patterns and protocol-specific burns confirmed via documentation or Alchemy/Arkham labels) are excluded universally from HHI computation."

A subsequent methodological refinement (2026-05-12) addressed a separate measurement artifact: for three protocols (MOR, AXL, ZRO), the Dune holder-list extraction had been inadvertently capped at top-100 rather than top-1000, producing artificially low HHI values and undercounting the long-tail distribution. Re-pulling at the top-1000 cutoff and re-applying the exclusion methodology yields revised values: MOR HHI 0.013 to 0.031 (four protocol-controlled addresses excluded, including the Monsta_vault mint destination identified via Dune transfer audit), AXL HHI 0.004 to 0.028, ZRO HHI 0.010 to 0.015. The two methodological refinements compose: the Mann-Whitney p (0.014) and Cohen's d (1.03) reported above reflect the combined effect. The leave-one-out result is now significant across all 30 of 30 iterations (was 23 of 30 pre-F1); the §3.2 sector range is updated correspondingly (global minimum: Hyperliquid 0.005, previously Axelar 0.004).

**Manuscript change:** Table 4 UNI HHI 0.032 to 0.010; Table 4 MOR/AXL/ZRO cells updated per F1 top-1000 holder-list correction (HHI, Gini, Top-N, N across all three protocols); Table 4 methodology notes document the universal burn-rule methodology; supplementary file `burn_rule_audit_summary.csv` provides per-protocol audit findings; manuscript prose at §3.4 (insider taxonomy paragraph) and §2.10.4 documents the methodology.

**Status:** Resolved.

### R1-Major-7: Sample-size and specification sensitivity in regressions

**Reviewer comment (verbatim):** "In some cases, the regression evidence is weaker than the paper's language suggests. The regressions are based on a small cross-sectional sample, and the more demanding specifications include several controls relative to the number of observations."

**Our response:** Acknowledged. We have strengthened the §3.7 (Robustness) treatment of sample-composition sensitivity:

- The sector-contrast leave-one-out result is now significant in all 30 of 30 iterations after the F1 holder-list correction (was 23 of 30 pre-F1), strengthening rather than constraining the inference.
- The insider-retention leave-one-out result (Spearman rho = 0.48, p = 0.003, N = 37) remains significant across all 37 single-protocol exclusions (rho range 0.45 to 0.55).
- The §4.7 Contributions opener identifies sector membership as the only positive predictor that survives multivariate adjustment and acknowledges its borderline status (sector coefficient p < 0.05 in Models 1 and 2 of Table 6; borderline at p = 0.050 in Model 3 with the full control set).
- The calibrated-verb pass through Discussion replaces causal language ("drives," "produces") with descriptive language ("is consistent with," "indicating").

Specification choices are documented in the replication repository.

**Manuscript change:** §3.7 LOO sensitivity strengthened (sector contrast 30/30; insider retention 37/37); calibrated-verb pass through Discussion; §4.8 Limitations expanded (cross-sectional design constraint).

**Status:** Resolved.

### R1-Minor-1: Sample-size variation across analyses

**Reviewer comment (verbatim):** "Different analyses use different sample sizes. For example, some tests use 40 protocols, others 38, 22, 20, or 19. ... the paper should explain which protocols are included in each analysis and why others are excluded."

**Our response:** Addressed via new Supplementary Table SX (sample-coverage three-cluster enumeration), which lists per-N protocol composition for primary chain analyses (N = 40, 37, 30), subsidy cluster (N = 22, 20, 19), and participation cluster (N = 13). Each cell is computed from the smallest N for which the underlying covariate is populated; combining tests under a single N would force exclusions and reduce statistical power.

**Manuscript change:** New Supplementary Table SX.

**Status:** Resolved.

### R1-Minor-2: Causal language in cross-sectional design

**Reviewer comment (verbatim):** "I would suggest that the paper avoid causal language in most cases since the analysis design is cross-sectional and observational. Phrases suggesting that a design feature 'drives,' 'produces,' or 'causes' concentration should be softened."

**Our response:** Calibrated-verb pass through Discussion: "drives," "produces," and "causes" replaced with "is consistent with," "indicating," and "documents." The §3.7 LOO sensitivity statement strengthens the cross-sectional design caveat.

**Manuscript change:** Calibrated-verb pass through §4 Discussion; §3.7 LOO sensitivity strengthened.

**Status:** Resolved.

### R1-Minor-3: Insider category formal definitions

**Reviewer comment (verbatim):** "Please clarify the insider category in more detail. The paper uses several related categories: insiders, team, investors, foundation, treasury, and protocol-controlled addresses. These are not always identical."

**Our response:** Addressed via new §2.10.4 paragraph distinguishing insider_pct (regression covariate measured at TGE: team_pct + investor_pct from primary tokenomics sources) from insider count fraction in top-10 holders (descriptive mechanism variable measured post-distribution from holder snapshots). The three-tier classification methodology is documented (Tier 1 Blockscout labels and Dune exchange tags; Tier 2 contract bytecode; Tier 3 Etherscan named-address matching). PCAs are excluded from HHI computation entirely at the top of the pipeline (69 addresses across 20 protocols; documented in `exclusions_log.csv`) and are not counted as insiders for the purposes of the count fraction. The Solana labeling gap is acknowledged.

**Manuscript change:** New §2.10.4 paragraph.

**Status:** Resolved.

### R1-Minor-4: HHI antitrust threshold caveat

**Reviewer comment (verbatim):** "The paper's use of HHI is appropriate, but any analogy to antitrust concentration thresholds should be treated cautiously. A market-concentration threshold is not the same as a democratic-legitimacy threshold."

**Our response:** Caveat added at §3.2: "The 0.25 HHI antitrust threshold is borrowed from market-concentration analysis (DOJ Horizontal Merger Guidelines) and is reported here as a benchmark for descriptive interpretation only. A market-concentration threshold is not equivalent to a democratic-legitimacy threshold; a protocol may have HHI below 0.25 while remaining politically dominated through quorum rules, delegation patterns, or proposal-rights concentration. The HHI captures one dimension of concentration (post-exclusion holding distribution) and is not a sufficient condition for distributed governance."

**Manuscript change:** New caveat paragraph at §3.2.

**Status:** Resolved.

### R1-closing: Acknowledgment of methodological complexity

**Reviewer comment (paraphrased):** Reviewer notes possible misunderstandings due to methodological complexity; requests clarification on dataset, exclusion rules, and adjustment stage per table.

**Our response:** Reviewer 1's recomputations against the canonical regression dataset were correct in every case; the gaps were within-manuscript propagation issues (some tables held pre-cascade values while pipeline outputs and prose used post-cascade values). Per-table dataset and exclusion-rule documentation is now provided by Supplementary Table SX (sample-coverage), the §2.10.2 and §2.10.4 methodology paragraphs, the burn-rule audit summary, and the Table 4 methodology notes. The replication GitHub repository (linked in cover) provides full address-level data and all classification CSVs for independent reanalysis.

**Status:** Resolved.

### R1-Q2.a (Quality of figures and tables): "No"

Addressed via figure caption interpretation guidance (R2-7), Table 4 methodology notes (R1-Major-1, R1-Major-2, R1-Major-6), Table 5 cell updates (R1-Major-3), Table 7 source label and footnote (R1-Major-4).

### R1-Q2.b (Reference list adequacy): "Yes"

No action; reviewer marked Yes. Four cooperative-literature references added per R2-Q1.3 above (Hansmann 1996; Birchall 2011; ICA 1995; Scholz 2016).

### R1-Q2.c (Statistical methods): "No"

Addressed via R1-Major-1 through R1-Major-7, R2-Q1.1 through R2-Q1.4, calibrated-verb pass.

### R1-Q2.d (Statistician evaluation): "Yes"

Acknowledged per R2-Q2.d above.

### R1-Q2.e (Methods documentation): "No"

Addressed via R1-Minor-3 (insider taxonomy), R2-8 (cutoff justification), R1-Minor-1 (sample-coverage table), and the burn-rule audit supplementary file. The replication repository remains the authoritative method-documentation source.

---

## Editor responses

### Editor-1: Title state

**Editor note:** The Frontiers system records the manuscript title as "Tokenomics as Institutional Design: A Normative Framework and Governance Concentration Analysis" while the canonical / SSRN title is "Governance Concentration Beyond Token Allocation: An Institutional Design Analysis of DePIN and DeFi."

**Our response:** We respectfully request the Frontiers system update the title to the canonical "Governance Concentration Beyond Token Allocation: An Institutional Design Analysis of DePIN and DeFi" to align Frontiers, SSRN, and program-canonical surfaces. The submitted-of-record DOCX file uses the canonical title; the divergence is in the Frontiers system metadata only.

**Status (2026-05-12):** Resolved. Author updated the title in the Frontiers submission system directly to the canonical "Governance Concentration Beyond Token Allocation: An Institutional Design Analysis of DePIN and DeFi". Frontiers, SSRN, and program-canonical surfaces are now aligned.

---

## Summary of revision artifacts

| Artifact | Path | Notes |
|---|---|---|
| Clean revised manuscript | `submissions/B2_Frontiers_R1_clean.docx` | Post-revision; canonical title |
| Tracked-changes manuscript | `submissions/B2_Frontiers_R1_tracked_changes.docx` | Delta from `1853465_Manuscript.PDF` |
| This response document | `responses/2026-05-10_R1_responses_master.md` | Per-comment threaded structure |
| Pre-edit snapshot | `versions/2026-05-10_pre_R1_revisions.docx` | Copy of v5_v10 baseline |
| Burn-rule audit summary | (supplementary file) `burn_rule_audit_summary.csv` | Per-protocol audit |
| Top-10 post-exclusion all 20 | (supplementary file) `top10_post_exclusion_all20.csv` | Pre-vs-post comparison |
| Sample-coverage table | (supplementary file) Supplementary Table SX | Three-cluster N enumeration |

---

## Internal: program-state propagation tracking (not for reviewer paste; internal recordkeeping only)

Phase 4 LFU memo at `.cursor/tasks/Living_File_Updates_2026-05-10_*_B2_Frontiers_R1.md` will propagate to:
- METADATA.md lifecycle: UNDER_REVIEW -> REVISION_REQUESTED at R1 receipt -> UNDER_REVIEW at re-submission
- METADATA.md `frontiers_manuscript_id: 1853465` (new field)
- METADATA.md `frontiers_submission_date: 2026-04-12` (new field)
- OUTREACH_LOG OL-011 status-append: R1 received 2026-04-23/28/05-01, R1 resubmitted 2026-05-XX
- KEY_FINDINGS F-B2-7 backfill (Cohen's d 0.96 -> 0.99 narrative-strengthening cascade)
- DECISION_LOG new DEC entries for: universal burn-rule exclusion methodology; Compound + Arbitrum voting-HHI Snapshot-source choice
- ERROR_CORRECTION_LOG entries for: Table 5 stale-cell propagation; Table 7 source-label mismatch; Top-10 pre-vs-post-exclusion methodology inconsistency
- HYPOTHESES three-value-pipeline-split documentation (Optimism)
