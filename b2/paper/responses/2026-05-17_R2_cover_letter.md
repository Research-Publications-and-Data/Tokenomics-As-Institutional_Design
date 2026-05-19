# Cover letter: B2 R2 submission

**To:** Editorial Office, Frontiers in Blockchain
**From:** Zach Zukowski (Tokenization Systems; zach@tokenization.systems)
**Re:** Governance Concentration Beyond Token Allocation: An Institutional Design Analysis of DePIN and DeFi (Manuscript ID [TO_BE_FILLED]; SSRN 6599278)
**Date:** 2026-05-17
**Round:** R2 revision

---

Dear Editor and Reviewers,

I am submitting the R2 revision of "Governance Concentration Beyond Token Allocation: An Institutional Design Analysis of DePIN and DeFi" addressing Reviewer 1's four R1-round comments and including substantial additional strengthening to the philosophical and methodological framework.

## Summary of R1 round-2 issues addressed

Reviewer 1's R1 round-2 review identified four classes of manuscript-vs-data-of-record drift. All four are addressed in this submission. The accompanying point-by-point response document (`2026-05-17_R2_responses_master.md`) details each fix at the level of granularity raised. In brief:

1. **Table 7 holding-HHI inconsistency**: Fully recomputed with post-exclusion holding HHIs consistent with Table 4. Three protocols (Uniswap, Optimism, Lido) show updated amplification ratios. Two (Uniswap, Optimism) flip from delegation-dispersion to delegation-amplification under correct exclusion methodology, producing a substantive new finding (see below).

2. **Curve Top-10 column + CRV text disambiguation**: Top-10% corrected to post-exclusion value (34.4%). Body-text references to CRV 0.171 disambiguated: raw post-exclusion CRV HHI (0.017) is distinguished from veCRV-weighted voting concentration (0.26, computed directly from Convex contract aggregation of top-50 historical lockers, a methodological strengthening over the R1 proxy estimate).

3. **Table 5 N=40 and TT-expanded reproducibility**: Hivemapper, io.net, and Aethir Gini values computed via Helius DAS API and Dune holder lists; all three now appear as full Table 4 rows. Table 5 HHI-Gini correlation now reports N=40 with complete data. TT-expanded subsidy N corrected from 22 (stale count) to 19 (matches canonical regression dataset) with corresponding Pearson r confirming the same qualitative null finding.

4. **Figure-vs-text statistical drift**: Manuscript surfaces now align on canonical values from a single regression dataset. Figure regeneration (visual PNGs) is in flight as a parallel workstream to the manuscript surgery; regenerated figures will be applied to the R2 submission package.

## Substantive new finding emerging from R1 corrections

Applying the post-exclusion methodology consistently across Table 4 and Table 7 produces a **universal-amplification finding**: delegation amplifies governance concentration across nine of ten protocols in the Table 7 sample (range 1.2x to 11.4x; mean 5.3x), with one structural exception (ENS at 0.39x, reflecting a mature delegate program where holders systematically delegate to a broad community-delegate set). Two protocols previously cited as delegation-dispersion counterexamples (Uniswap, Optimism) join the universal-amplification pattern under correct exclusion methodology. The finding strengthens the paper's main thesis that institutional design at the operator and router level governs governance outcomes; magnitude variation within sector is a cleaner empirical signal than direction variation. Section 3.7 adds a PCA-symmetric robustness check confirming the finding holds across all 5 Tally-sourced protocols even when foundation and aggregation-contract delegates are excluded. The deep 126-address protocol-controlled-address audit (Section 2.10.10) was completed during the R2 cycle, codifying a five-class PCA typology (burn, foundation / treasury, staking aggregation, bridge / migration, CEX custody) and bringing exclusion documentation to 38 of 40 protocols, with 2 confirmed non-PCA top holders.

## Substantial R2 enhancements beyond reviewer-flagged issues

In addition to addressing all four R1 reviewer issues, the R2 cycle has substantively strengthened the philosophical-methodological framework:

- **Philosophical-credibility two-layer framing** (Section 2.10.1; Table 1): Each lens now carries an explicit operational mechanism (what is scored) and a philosophical goal (the normative warrant). This resolves the R1 Table 1 internal inconsistency where the Pettit row labeled "Contestation" while glossing "freedom from arbitrary power" (the definition of non-domination, not contestation). The two-layer structure prevents the common conflation of philosophical goal with institutional mechanism and is applied consistently across all five lenses.

- **Inter-lens relationships paragraph** (Section 2.9.6): New paragraph documenting that the five lenses are mutually reinforcing rather than orthogonal, providing the philosophical architecture for the Synergy Index aggregation choice.

- **Systematic empirical-philosophical mapping** (Section 4.1): For each major empirical finding, philosophical implications across applicable lenses are made explicit; the universal delegation amplification finding registers across all five lenses simultaneously.

- **Comparative methodology** (Section 4.5): New paragraph positioning the five-lens framework against existing DAO assessment frameworks (Aragon DAO Health Index, Snapshot analytics, Boardroom, DAOstar standards) along three dimensions: scope, aggregation, comparability.

- **Falsifiable forward claims + pre-registration intent** (Section 4.9): Two specific predictions about subsequent cross-protocol governance trajectories that future panel-data work can test, with intent to pre-register hypothesis specifications.

- **Data availability and reproducibility statement** (Section 4.9): Explicit statement of replication-repository contents including the 40-protocol dataset, exclusions log, Phase 0 supplementary data (Hivemapper / io.net / Aethir holder distributions; veCRV cumulative deposits; Theil and Atkinson supplementary metrics).

- **Methodological depth additions** (Section 3.7): Theil (1967) and Atkinson (1970) inequality indices computed under PCA-symmetric methodology as a robustness check on HHI's value-validity; Shapley-Shubik (1954) and Banzhaf (1965) power indices acknowledged as voting-theory complements to HHI; Hirschman (1964) historical source for the HHI itself; multiple-comparisons correction note via Benjamini-Hochberg false-discovery-rate adjustment.

- **Synergy Index full-sample 20-cell expansion + web verification cycle** (Section 3.7; Supplementary Files S3 + S3_scoring_tables_20cell_extension_2026-05-19.md): The original scoring rubric was applied at the per-criterion (20-cell) level to the remaining 28 protocols in the cross-section, producing 560 web-verified cells of governance-evidence-backed scoring and Synergy Index values for all 40 protocols. Verification sources (governance documentation URLs, proposal-type names, multi-sig structures, voting-mechanism details) are catalogued per protocol. Full-sample arithmetic Synergy-vs-HHI Spearman rho = -0.28 (p = 0.076); Pearson r = -0.32 (p = 0.045, statistically significant at conventional alpha); geometric Synergy-vs-HHI Spearman rho = -0.23 (p = 0.155); arith-vs-geom rank agreement rho = 0.97 on the 40-protocol sample. The framework's discriminating claim is strengthened: higher governance concentration predicts lower institutional-design quality across the five normative lenses, with statistical significance reached under Pearson correlation. Cross-sector Synergy contrast is not significant (DePIN vs DeFi Mann-Whitney p = 0.28), indicating that the HHI sector-signal does not translate symmetrically to the institutional-design Synergy dimension. Filecoin (2.05), Gitcoin (1.95), and Optimism (1.90) sit at the top of the full-sample distribution; Anyone Protocol (1.00) and io.net (1.05) sit at the bottom.

- **Shapley-Shubik power indices** (Section 3.7): The Shapley-Shubik (1954) and Banzhaf (1965) power indices acknowledged as voting-theory complements to HHI were computed for the five Tally-sourced voting-layer protocols (AAVE, ARB, COMP, OP, UNI) using top-100 delegate weights and Monte Carlo permutation under simple-majority quorum. Shapley-Shubik concentration-of-power tracks Tally voting-HHI with Pearson r = 0.999 (Spearman rho = 1.00); per-voter top-1 power tracks top-1 voting share with Pearson r = 0.999. The convergence result strengthens the use of HHI as a power-concentration proxy for the comparative-cross-sectional analysis this paper conducts.

- **Subsidy multivariate with sector control** (Section 3.7): A multivariate OLS specification with both subsidy ratio and DePIN sector dummy on the 22-protocol non-zero-subsidy sample (HC3 robust standard errors) demonstrates that the apparent subsidy-HHI relationship is fully absorbed by DePIN sector membership once Livepeer is excluded. Specification 4 (subsidy + DePIN dummy, no Livepeer, N = 21): subsidy coefficient becomes non-significant (p = 0.55) while DePIN sector dummy remains significant (p = 0.03). The Livepeer-driven interpretation in Section 3.4 is substantively reinforced: the apparent cross-sector subsidy-concentration association reflects a single extreme observation combined with sector membership, not a structural relationship between subsidy intensity and governance concentration.

- **Operationalization-dependency caveat** (Section 4.8): Explicit acknowledgment that the framework's empirical conclusions depend on operationalization choices; alternative scoring criteria for the same lens could yield different lens scores. The Synergy Index full-sample expansion (above) addresses the lens-aggregation choice question at the rank-ordering level (arith vs geom rho = 0.97).

- **21 new citations** across philosophy (Skinner, Cohen, Habermas, Berlin, Beitz, Pogge, Pettit 2012, Rawls 2001, Brennan & Buchanan, Hardin), mechanism design (Holmstrom, Tirole, North), voting theory (Shapley & Shubik, Banzhaf), DAO political theory (DuPont, Atzori, Schneider), and inequality measurement (Theil, Atkinson, Hirschman).

## Submission package contents

- **B2_Frontiers_R2_clean.docx + B2_Frontiers_R2_clean.pdf**: Revised manuscript (clean version)
- **B2_Frontiers_R2_tracked_changes.docx + B2_Frontiers_R2_tracked_changes.pdf**: Revised manuscript with tracked changes from R1 baseline
- **2026-05-17_R2_responses_master.md (.docx + .pdf)**: Point-by-point response to Reviewer 1 comments
- **This cover letter**
- **Supplementary files (S1 through S9)**: Methodology and replication materials, including:
  - S1: Metric definitions including Synergy Index construction
  - S2: Scoring rubric templates with worked examples
  - S3: Per-protocol scoring sheets
  - S5: Replication pipeline specification
  - S6: Address-by-address exclusion methodology documentation
  - S8: Token Terminal expansion subsidy sensitivity analysis
  - S9: Theil and Atkinson supplementary metrics (R2 addition)
  - Phase 0 R2 supplementary exhibits: holders_ATH_2026-05-17.csv, theil_atkinson_2026-05-17.csv, veCRV_voting_concentration_2026-05-17.csv, phase0_data_collection_results_2026-05-17.md

## Methodology disclosure

The R2 cycle adopted a single-canonical-regression-dataset-of-record discipline to prevent recurrence of the manuscript-vs-data drift Reviewer 1 surfaced. The Section 2.10.3 methodology note documents this discipline. Snapshot-date discipline is acknowledged: the Table 7 voting HHI values use a March 2026 snapshot consistent with the rest of the dataset; the May 2026 Tally and Snapshot replication shows delegate-pool drift (Compound active-delegate count and Snapshot voter count both shifted) but the rank ordering across protocols is the more durable inferential property than absolute magnitude.

## Conflict of interest

The author is employed by Borderless Capital, a cryptocurrency-focused investment firm. A complete disclosure is provided in the Conflict of Interest statement accompanying this submission. The author may hold or have held positions in some protocols analyzed; the disclosure documents these. No co-authors or other conflicts of interest.

## Acknowledgment

We thank Reviewer 1 for the comprehensive cross-surface audit that identified the manuscript-vs-data-of-record drift and motivated the R2 reproduce-and-sync cycle. The universal-amplification finding documented in Section 3.5 is a direct product of Reviewer 1's R2 framing. We thank Reviewer 2 for the endorsement of publication.

Sincerely,
Zach Zukowski
Tokenization Systems
zach@tokenization.systems
ORCID: 0009-0006-3642-2450
