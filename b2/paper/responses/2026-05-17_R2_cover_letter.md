# Cover letter: B2 R2 submission

**To:** Editorial Office, Frontiers in Blockchain
**From:** Zach Zukowski (Tokenization Systems; zach@tokenization.systems)
**Re:** Governance Concentration Beyond Token Allocation: An Institutional Design Analysis of DePIN and DeFi (Manuscript ID [TO_BE_FILLED]; SSRN 6599278)
**Date:** 2026-05-17 (R2 submission); 2026-05-19 (revisions incorporated)
**Round:** R2 revision

---

Dear Editor and Reviewers,

I am submitting the R2 revision of "Governance Concentration Beyond Token Allocation: An Institutional Design Analysis of DePIN and DeFi." The revision addresses all four R1 round-2 comments from Reviewer 1, incorporates a substantive new headline finding that emerged from the reproduce-and-sync cycle the reviewer's framing prompted, and includes targeted philosophical-methodological strengthening informed by Reviewer 2's endorsement context.

## Reviewer 1's four issues: addressed

Reviewer 1 identified four classes of manuscript-vs-data-of-record drift. All four are resolved. The accompanying point-by-point response document (`2026-05-17_R2_responses_master.md`) details each fix at the level of granularity raised.

1. **Table 7 holding-HHI inconsistency.** Table 7 fully recomputed using post-exclusion holding HHIs consistent with Table 4. Three protocols (Uniswap, Optimism, Lido) show updated amplification ratios. Two (Uniswap, Optimism) flip from delegation-mediated dispersion to delegation amplification under the corrected exclusion methodology, producing a substantive new finding (described below).

2. **Curve Top-10 column and CRV text disambiguation.** Top-10 column corrected to the post-exclusion value (34.4%). Body-text references to CRV 0.171 disambiguated: raw post-exclusion CRV HHI (0.017) is distinguished from veCRV-weighted voting concentration (0.26, computed directly from Convex contract aggregation of the top-50 historical lockers; a methodological strengthening over the R1 proxy estimate).

3. **Table 5 N = 40 and TT-expanded reproducibility.** Hivemapper, io.net, and Aethir Gini values computed via Helius DAS API and Dune holder lists; all three now appear as full Table 4 rows. Table 5 HHI-Gini correlation reports N = 40 with complete data. TT-expanded subsidy N corrected from a stale count of 22 to 19 (consistent with the canonical regression dataset), confirming the same qualitative null finding.

4. **Figure-vs-text statistical drift.** All manuscript surfaces now align on canonical values from a single regression dataset. Figures regenerated to match the post-cascade canonical state.

## Substantive new finding emerging from R1 corrections

Applying post-exclusion methodology consistently across Table 4 and Table 7 produces a **universal-amplification finding**: delegation amplifies governance concentration across nine of ten protocols in the Table 7 sample (range 1.2x to 11.4x; mean 5.3x), with one structural exception (ENS at 0.57x, reflecting a mature delegate program where holders systematically delegate to a broad community-delegate set). Two protocols previously cited as delegation-dispersion counterexamples (Uniswap, Optimism) join the universal-amplification pattern under the corrected exclusion methodology. The finding strengthens the paper's main thesis that institutional design at the operator and router level governs governance outcomes: magnitude variation within sector is a cleaner empirical signal than direction variation. Section 3.7 adds a PCA-symmetric robustness check confirming the finding holds across all five Tally-sourced protocols even when foundation and aggregation-contract delegates are excluded.

A deep 126-address protocol-controlled-address audit (Section 2.10.10) was completed during the R2 cycle, codifying a five-class PCA typology (burn, foundation / treasury, staking aggregation, bridge / migration, CEX custody) and bringing exclusion documentation to 38 of 40 protocols, with two confirmed non-PCA top holders.

## Substantial R2 enhancements beyond reviewer-flagged issues

The R2 cycle also strengthens the philosophical, methodological, and statistical scaffolding of the paper. The enhancements organize into four clusters.

### Philosophical-methodological framework strengthening

- **Two-layer framing for the five-lens framework** (Section 2.10.1; Table 1): each lens now carries an explicit operational mechanism (what is scored) and a philosophical goal (the normative warrant the tradition supplies). This resolves the R1 Table 1 internal inconsistency where the Pettit row labeled "Contestation" but glossed "freedom from arbitrary power" (the definition of non-domination, not contestation). The two-layer structure is applied consistently across all five lenses.

- **Inter-lens relationships paragraph** (Section 2.9.6): the five lenses are mutually reinforcing rather than orthogonal. This provides the philosophical architecture justifying the Synergy Index's arithmetic-mean aggregation choice.

- **Systematic empirical-philosophical mapping** (Section 4.1): for each major empirical finding, philosophical implications across applicable lenses are made explicit. The universal delegation-amplification finding registers across all five lenses simultaneously.

- **Comparative methodology against existing DAO assessment frameworks** (Section 4.5): the five-lens framework positioned against Aragon DAO Health Index, Snapshot voting analytics, Boardroom, and DAOstar standards along three dimensions: scope, aggregation, comparability.

### Statistical and measurement depth additions

- **Inequality-metric robustness** (Section 3.7): Theil (1967) and Atkinson (1970) indices computed under PCA-symmetric methodology as a robustness check on HHI's value-validity; Hirschman (1964) cited as historical source for HHI; Benjamini-Hochberg false-discovery-rate correction note across the 14 bivariate tests in Table 5.

- **Power-index analysis** (Section 3.7): Shapley-Shubik (1954) and Banzhaf (1965) power indices computed for the five Tally-sourced voting-layer protocols (AAVE, ARB, COMP, OP, UNI) via Monte Carlo permutation. Under simple-majority quorum, Shapley-Shubik concentration-of-power tracks voting-HHI with Pearson r = 0.999. The Banzhaf index reveals an AAVE-specific divergence (Banzhaf top-1 = 33.5 percent vs Shapley-Shubik = 26.7 percent vs voting share = 21.9 percent), identifying AAVE as the per-protocol case where individual-proposal power indices would refine the cross-sectional concentration measure. Quorum-rule variation (0.33 to 0.75 thresholds) shows stable SS-HHI to voting-HHI ratios across the threshold range, tightening the use of HHI as a power-concentration proxy under typical DAO quorum rules.

### Late-cycle robustness extensions (2026-05-19)

- **Synergy Index full-sample 20-cell expansion** (Section 3.7; Supplementary S3 + S3_scoring_tables_20cell_extension_2026-05-19.md): the original Synergy Index was reported on the 12 fully-criterion-scored anchor protocols; the R2 cycle extends per-criterion (20-cell) scoring to all 40 protocols, producing 560 web-verified cells of governance-evidence-backed scoring. Verification sources (governance documentation URLs, proposal-type names, multi-sig structures, voting-mechanism details) are catalogued per protocol. Full-sample Pearson Synergy-vs-HHI correlation r = -0.32 (p = 0.047, statistically significant); arithmetic-vs-geometric Synergy rank agreement Spearman rho = 0.97 across N = 40, addressing the lens-aggregation operationalization-dependency concern at the rank-ordering level. The cross-sector Synergy contrast is not significant (DePIN vs DeFi Mann-Whitney p = 0.28), indicating that the HHI sector-signal does not translate symmetrically to the institutional-design Synergy dimension (a substantively informative asymmetry for the framework's discriminating power).

- **Subsidy multivariate with sector control** (Section 3.4 + Section 3.7): a multivariate OLS specification with subsidy ratio and DePIN sector dummy on the 22-protocol non-zero-subsidy sample (HC3 robust standard errors) demonstrates that the apparent subsidy-HHI relationship is fully absorbed by sector membership once Livepeer is excluded. In Specification 4 (subsidy + DePIN dummy, no Livepeer, N = 21), the subsidy coefficient is strongly non-significant (p = 0.94) while the DePIN sector dummy remains significant (p = 0.007). The Livepeer-driven interpretation in Section 3.4 is substantively reinforced: the apparent cross-sector subsidy-concentration association reflects a single extreme observation combined with sector membership, not a structural relationship between subsidy intensity and governance concentration.

- **Longitudinal panel integration** (Section 3.4 main text; Supplementary S7): the quarterly HHI panel for 14 governance tokens (8 quarters post-token-generation event) was promoted from supplementary-only into Section 3.4 main text. The headline panel finding, that 11 of 14 protocols exhibit monotonic governance HHI decay over 24 months, reinforces the cross-sectional allocation null by adding longitudinal evidence that distributions deconcentrate over time across heterogeneous allocation designs.

- **Operationalization-dependency caveat** (Section 4.8): explicit acknowledgment that the framework's empirical conclusions depend on operationalization choices. The Synergy Index full-sample expansion (above) addresses the lens-aggregation choice question at the rank-ordering level; per-lens operationalization-robustness remains an open empirical question for inter-rater reliability cycles.

### PCA-exclusion universal-audit cycle (2026-05-19)

A user-flagged universal audit of high-HHI protocols for missed Class 1 to Class 5 PCA exclusions surfaced three missed exclusions, all consistent with already-applied typologies. Adding them strengthens the universal-audit consistency of the PCA-exclusion methodology.

- **Aethir Safe multisig 0xfc78 (8-PCA cascade)**: deep verification of the next four unlabeled Aethir top holders identified 0xfc78 as a Safe 1.4.1 multisig matching the same Class 2 typology already applied to 0x3e7e (the previously-documented Aethir Safe multisig). Adding it shifted Aethir HHI from 0.087 to 0.095.

- **IoTeX Genesis-burn precompile slots 0x03 + 0x07**: five precompile slots (0x01, 0x02, 0x04, 0x05, 0x06) were documented as Class 1 exclusions; slots 0x03 and 0x07 had been omitted from the log (oversight) despite Etherscan-verified Burn + Genesis labels and the same receive-only pattern. Adding both shifted IoTeX HHI from 0.189 to 0.081.

- **ENS Cold Wallet 0x690f0581**: Etherscan-labeled "ENS: Cold Wallet" (Safe Singleton 1.3.0 multisig created by nick.eth) holding 4.29M ENS (5.2 percent of post-exclusion supply). Adding it as a Class 2 exclusion shifted ENS HHI from 0.071 to 0.049.

**Cascade through dependent statistics is contained.** DePIN sector mean shifts from 0.077 to 0.071; the DePIN-vs-DeFi Mann-Whitney sector contrast remains significant (p = 0.020 from 0.018; Cohen's d = 0.94 from 0.98, still large effect by Cohen's threshold); LOO 30-of-30 significant-iteration robustness is preserved; the Synergy-HHI Pearson correlation remains statistically significant (r = -0.32, p = 0.047); the Livepeer-driven subsidy interpretation is reinforced (Spec 4 subsidy p = 0.94 absent Livepeer). All headline findings are qualitatively preserved.

### Other R2 additions

- **Falsifiable forward claims and pre-registration intent** (Section 4.9): two specific predictions about subsequent cross-protocol governance trajectories that future panel-data work can test, with explicit pre-registration intent.

- **Data-availability and reproducibility statement** (Section 4.9): explicit listing of replication-repository contents (40-protocol dataset, exclusions log, supplementary data covering Hivemapper / io.net / Aethir holder distributions, veCRV cumulative deposits, Theil and Atkinson supplementary metrics).

- **Abstract accessibility revision**: jargon-dense statistical passages reworked with first-use glosses for Pearson r, Spearman rho, Mann-Whitney, Cohen's d (with explicit small-medium-large thresholds), and ordinary least squares (OLS). The dense OLS-specifications paragraph was rewritten from a multi-clause sentence with nested parentheticals into linear prose. Statistical disclosure is preserved in full; readability is substantially improved for non-statistician audiences.

- **21 new citations** across philosophy (Skinner, Cohen, Habermas, Berlin, Beitz, Pogge, Pettit 2012, Rawls 2001, Brennan & Buchanan, Hardin), mechanism design (Holmstrom, Tirole, North), voting theory (Shapley & Shubik, Banzhaf), DAO political theory (DuPont, Atzori, Schneider), and inequality measurement (Theil, Atkinson, Hirschman).

## Submission package contents

- **B2_Frontiers_R2_clean.docx + B2_Frontiers_R2_clean.pdf**: revised manuscript (clean version).
- **B2_Frontiers_R2_tracked_changes.docx + B2_Frontiers_R2_tracked_changes.pdf**: revised manuscript with tracked changes relative to the R1 baseline.
- **2026-05-17_R2_responses_master.md / .docx / .pdf**: point-by-point response to Reviewer 1 with the universal-audit-cycle section appended.
- **This cover letter**.
- **Supplementary files (S1 through S9)**: methodology and replication materials, including:
  - S1: metric definitions including Synergy Index construction
  - S2: scoring rubric templates with worked examples
  - S3: per-protocol scoring sheets (40 protocols; original 12 fully-criterion-scored, 28 extended via 20-cell verification cycle in S3_scoring_tables_20cell_extension_2026-05-19.md)
  - S5: replication pipeline specification
  - S6: address-by-address exclusion methodology documentation
  - S7: quarterly HHI panel for 14 governance tokens (longitudinal evidence)
  - S8: Token Terminal expansion subsidy sensitivity analysis
  - S9: Theil and Atkinson supplementary metrics
  - Phase 0 R2 supplementary exhibits: holders_ATH_2026-05-17.csv, theil_atkinson_2026-05-17.csv, veCRV_voting_concentration_2026-05-17.csv, phase0_data_collection_results_2026-05-17.md, synergy_index_full_sample_2026-05-19.csv, power_indices_2026-05-19.csv, banzhaf_indices_2026-05-19.csv, power_indices_quorum_variation_2026-05-19.csv, subsidy_multivariate_2026-05-19.csv

## Methodology disclosure

The R2 cycle adopted a single-canonical-regression-dataset-of-record discipline to prevent recurrence of the manuscript-vs-data drift Reviewer 1 surfaced. The Section 2.10.3 methodology note documents this discipline. Snapshot-date discipline is acknowledged: the Table 7 voting HHI values use a March 2026 snapshot consistent with the rest of the dataset; the May 2026 Tally and Snapshot replication shows delegate-pool drift (Compound active-delegate count and Snapshot voter count both shifted) but rank ordering across protocols is the more durable inferential property than absolute magnitude.

The universal-audit cycle described above also adopted a Class 1 to Class 5 PCA typology consistently across the 40-protocol cross-section (documented in `data/processed/exclusions_log.csv`; 133 rows; 40 protocols).

## Conflict of interest

The author is employed by Borderless Capital, a cryptocurrency-focused investment firm. A complete disclosure is provided in the Conflict of Interest statement accompanying this submission. The author may hold or have held positions in some protocols analyzed; the disclosure documents these. There are no co-authors and no other conflicts of interest.

## Acknowledgment

We thank Reviewer 1 for the comprehensive cross-surface audit that identified the manuscript-vs-data-of-record drift and motivated the R2 reproduce-and-sync cycle. The universal-amplification finding documented in Section 3.5 is a direct product of Reviewer 1's R2 framing: applying consistent post-exclusion methodology across Table 4 and Table 7 produces the substantive interpretive change that strengthens the paper's thesis about institutional design at the operator and router level governing governance outcomes. We thank Reviewer 2 for the endorsement of publication.

Sincerely,

Zach Zukowski
Tokenization Systems
zach@tokenization.systems
ORCID: 0009-0006-3642-2450
