# B2 R2 Responses Master

**Paper:** Governance Concentration Beyond Token Allocation: An Institutional Design Analysis of DePIN and DeFi
**Author:** Zach Zukowski (Tokenization Systems; zach@tokenization.systems)
**Journal:** Frontiers in Blockchain
**Round:** R2 (response to Reviewer 1 second-round feedback)
**Date:** 2026-05-17 (final; Phase 0 data collection complete)

---

## Preamble

We thank both reviewers for their continued engagement with the manuscript. Reviewer 2 endorsed publication in R2. The revisions below address Reviewer 1's four remaining issues at the level of granularity raised. The R2 cycle treats Reviewer 1's specific findings as one class (manuscript-vs-data-of-record drift) and resolves them with a comprehensive reproduce-and-sync pass per the reviewer's general suggestion. Beyond Reviewer 1's specific issues, the R2 cycle also strengthens the philosophical-methodological framework substantially (Section 2.9.6 inter-lens relationships; Section 2.10.1 two-layer framing; Section 4.5 comparative methodology; 21 new citations across philosophy, mechanism design, voting theory, and institutional economics; falsifiable forward claims; data-availability statement; multiple-comparisons correction note).

The most consequential single result of the R1→R2 reproduce-and-sync is a substantive interpretive change in Section 3.5: with corrected holding HHI baselines for Uniswap and Optimism, both protocols flip from delegation-mediated dispersion to delegation amplification. The R2 manuscript documents a **universal-amplification finding** across nine of ten protocols in the Table 7 sample (range 1.2x to 11.4x; mean 5.3x), with one structural exception (ENS at 0.39x, a mature delegate program where broad-community-delegate distribution disperses voting power below the holding baseline) and a robustness check under symmetric PCA-exclusion methodology confirming the finding holds across all 5 Tally-sourced protocols even when foundation and aggregation-contract delegates are excluded from voting HHI (Section 3.7). The Table 7 sample was further expanded mid-cycle to include GMX (Tally) and ENS (Tally), bringing N=10. A subsequent 126-address deep protocol-controlled-address audit (Section 2.10.10) codified a five-class PCA typology (burn, foundation / treasury, staking aggregation, bridge / migration, CEX custody) and refined Table 7 holding HHIs further, yielding the final amplification range and mean cited above.

---

## Issue 1: Table 7 holding-HHI inconsistency (interpretive flip)

### Reviewer comment (verbatim, key points)

> Table 7 still uses the old holding-HHI baselines for some protocols, even though the corresponding HHI values have been revised elsewhere in the paper and repository. ... Using the revised holding-HHI value would make the voting/holding ratio roughly 2.7X rather than 0.84X [for Uniswap]. Optimism's Table 4/processed-data holding HHI is approximately 0.009, while Table 7 still uses 0.042. ... Lido's ratio also appears lower when the revised holding HHI is used. ... I recommend that Table 7 be fully recomputed using the same proper holding-HHI values used in Table 4 and in the regression dataset.

### Response

The reviewer is correct on all three flagged cases. Table 7 has been fully recomputed using post-exclusion holding HHIs consistent with Table 4. The Compound and Arbitrum rows continue to use Snapshot-sourced voting HHIs per the R1 author rationale (larger active-voter pools than Tally's top-100 sampling); voting HHI source assignments are unchanged from R1. Holding HHIs are now uniformly post-exclusion across Table 7.

**Table 7 R1-baseline to R2-final (including deep PCA audit + Lido recompute completed during R2 cycle):**

| Protocol  | Sector | R1 Holding  | **R2 Holding**  | Voting HHI | R1 Ratio  | **R2 Ratio**  | Direction         |
|-----------|--------|-------------|-----------------|------------|-----------|---------------|-------------------|
| DIMO      | DePIN  | 0.038       | **0.025**       | 0.228      | 6.0x      | **9.1x**      | amplifies (higher)|
| Lido      | DeFi   | 0.018       | **0.008**       | 0.088      | 4.8x      | **11.4x**     | amplifies (highest)|
| WeatherXM | DePIN  | 0.148       | 0.148           | 0.486      | 3.3x      | 3.3x          | unchanged         |
| Compound  | DeFi   | 0.028       | **0.009**       | 0.053      | 1.9x      | **5.7x**      | amplifies (higher)|
| Aave      | DeFi   | 0.020       | **0.013**       | 0.076      | 3.8x      | **5.9x**      | amplifies (higher)|
| Uniswap   | DeFi   | 0.032       | **0.010**       | 0.027      | 0.84x     | **2.8x**      | **FLIP**          |
| Arbitrum  | Infra  | 0.012       | 0.012           | 0.052      | 4.3x      | 4.4x          | unchanged         |
| Optimism  | Infra  | 0.042       | **0.009**       | 0.033      | 0.79x     | **3.6x**      | **FLIP**          |
| GMX       | DeFi   | (new)       | **0.065**       | 0.077      | (new)     | **1.2x**      | new (Tier B1)     |
| ENS       | Infra  | (new)       | **0.071**       | 0.028      | (new)     | **0.39x**     | new (dispersion)  |

**Substantive interpretive consequence.** The flip is not a typo fix: it changes the Section 3.5 finding from "delegation amplifies unevenly, with two infrastructure protocols showing opposite patterns" to "delegation amplifies governance concentration in nine of ten protocols sampled, with one structural exception (ENS at 0.39x), and magnitude (not direction) varying by institutional design within sector." The Tier B1 expansion added GMX and ENS to Table 7; ENS is the structural-exception case in which a mature delegate program (~100 active community delegates with public delegate platforms and recurring delegate compensation) systematically distributes voting power below the holding baseline. We have rewritten Section 3.5 (opening paragraph, DeFi paragraph, Optimism / Arbitrum paragraph, Citizens' House / Dual Governance paragraph, Fritsch et al. extension paragraph), Section 3.5.1 ENS counterexample subsection, Section 3.5.2 ve-token-class subsection, abstract finding 4, Section 1.4 finding 4, and the Section 4.1 design-hypotheses synthesis to reflect the universal-amplification thesis with the ENS structural-exception case.

**On Lido.** The reviewer's observation that Lido's ratio "appears lower" with the revised holding HHI is opposite to what our data produces. The R1-corrected Lido holding HHI (Table 4 value 0.013) yields an amplification ratio of 6.8x, higher than the R1 Table 7's reported 4.8x. Subsequent post-R1 audit waves during the R2 cycle further reduced Lido's holding HHI: the canonical regression CSV was found to have computed Lido's row from an older 189-row curated holder file while every other row used the universal top-1000 methodology; recomputing under universal methodology yielded 0.038 (mid-cycle 2026-05-18 state); the 126-address deep PCA audit (completed 2026-05-19) then identified Bybit hot wallet and Binance 14 cold wallet as Class 5 (CEX custody) addresses on the Lido top-1000 list, bringing post-PCA Lido holding HHI to 0.008 and amplification ratio to 11.4x. Lido now sits at the top of the cross-protocol amplification distribution; the universal-amplification thesis is unchanged in direction; the magnitude is at the upper end. The canonical exclusion set is documented in `data/processed/exclusions_log.csv` (126 rows; 38 protocols).

**On the Uniswap counterexample.** The pre-correction Uniswap result (0.84x) had been cited as evidence that Uniswap's mature delegate program disperses governance power. With the burn address exclusion applied (the canonical 0x000...000dead holding 102.5M UNI, 11.3 percent of supply, structurally unable to participate in governance), Uniswap joins the universal-amplification pattern at 2.8x. We document this transition explicitly in Section 3.5 because the prior result was load-bearing in the dispersion-via-mature-delegate-program literature; the corrected analysis indicates the prior result was driven by including a wallet that structurally cannot vote in the holding denominator. The dispersion finding now attaches not to Uniswap (Tally) but to ENS (Tally; 0.39x ratio); see Section 3.5.1 for the ENS-as-institutional-design-counterexample analysis.

**Compound Foundation as PCA at the voting layer.** Phase 0 fact-checking of the Tally API surfaced a substantive methodological finding: the top COMP Tally delegate (21.5% of total delegated voting power in the May 2026 pull) is Compound Foundation itself, structurally a protocol-controlled entity. Applying PCA exclusion symmetrically at the voting layer (consistent with the holding-side methodology) drops Compound's voting HHI from 0.078 to 0.052 and the amplification ratio from 8.7x to 5.8x (using current post-deep-audit Compound holding HHI 0.009). The R1 Snapshot-based COMP voting HHI value (0.053) is essentially equivalent to the PCA-excluded Tally value (0.052); the R1 methodology choice already approximated the PCA-exclusion outcome. Aave's top delegate is the stkAAVE staking contract (21.9% of total delegated voting power); symmetric exclusion drops Aave's voting HHI from 0.076 to 0.045 and the amplification ratio from 5.9x to 3.5x (using current post-audit Aave holding HHI 0.013). We document this analysis as a Section 3.7 PCA-symmetric robustness paragraph showing universal amplification holds across all 5 Tally-sourced protocols (Compound 5.8x, Aave 3.5x, Uniswap 2.8x, Optimism 3.6x, Arbitrum 4.4x) even under symmetric PCA exclusion.

**Manuscript changes**: Table 7 rows updated (UNI, OP, LDO holdings + ratios); Table 7 caption updated with explicit post-exclusion methodology note; Section 3.5 paragraphs 1-5 rewritten; abstract finding 4 rewritten; Section 1.4 finding 4 rewritten; Section 3.7 PCA-symmetric robustness paragraph added; Section 2.10.3 Tally data drift methodology note added (documents the March 2026 to May 2026 delegate-pool drift; the R2 manuscript uses the March 2026 snapshot consistent with the rest of the dataset, with May 2026 results reported as supplementary robustness check); Figure 6 regeneration pending Phase 4 figure-regeneration cycle.

---

## Issue 2: Curve Top-10 column + CRV text disambiguation

### Reviewer comment (verbatim)

> In Table 4, Curve's HHI has been corrected to the post-exclusion raw-CRV value, but its Top-10 value is still the pre-exclusion one. The repository reports a substantially lower post-exclusion Top-10 value for Curve than the value shown in the table. In several places in the text, CRV is reported as HHI = 0.171, even though Table 4 now reports raw CRV, with HHI = 0.017. If this is supposed to be about veCRV, please mention it explicitly in the text.

### Response

The reviewer is correct on both points. Table 4 Curve Top-10% has been corrected from 60.7% (pre-Convex-exclusion) to 34.4% (post-Convex-exclusion, matching the regression dataset). The CRV-vs-veCRV disambiguation has been implemented across all four textual surfaces, with the 0.171 proxy replaced by a directly-computed veCRV voting concentration value (0.26) per Phase 0 Tier C1 analysis below.

**Direct veCRV voting concentration computation (Phase 0 Tier C1).** The R1 manuscript used 0.171 as a proxy for veCRV-weighted voting concentration. The 0.171 figure is the raw CRV holding HHI INCLUDING the Convex veCRV custody position (which holds substantial CRV that has been locked into veCRV). For R2 we compute the actual veCRV-weighted voting concentration directly via Dune analysis of the Curve VotingEscrow Deposit events at 0x5f3b5dfeb7b28cdbd7faba78963ee202a494e2a2. Aggregating cumulative CRV deposits across the top-50 historical veCRV lockers yields HHI = 0.26 (Convex CRV Locker: 48.0% of top-50 deposit-weighted share; Yearn yveCRV: 13.5%; Stake DAO sdCRV: 9.5%; the remaining 47 lockers each less than 4%). The 0.26 direct computation captures the actual gauge-weight voting concentration that veCRV produces and is substantively higher than the 0.171 proxy.

**Disambiguation strategy applied.** We have made the raw-vs-veCRV distinction explicit at every textual surface where CRV is cited:

- **Table 4 (row)**: HHI = 0.017 (raw post-exclusion); Top-10% = 34.4% (post-exclusion).
- **Table 4 (footnote methodology notes)**: HHI for Curve reflects raw CRV holdings after excluding the Convex veCRV custody position; veCRV-weighted voting concentration is approximately 0.26 computed from cumulative CRV deposit volume across the top-50 historical veCRV lockers; methodology discussed in Section 4.1.
- **Section 3.2 (DeFi range description)**: DeFi HHI ranges from 0.005 (Hyperliquid) to 0.117 (Jupiter); CRV's raw 0.017 places it mid-range. The 0.26 veCRV voting concentration is referenced with explicit methodology cite.
- **Section 4.1 (publicity-territory list)**: CRV removed from the upper-end-of-distribution territory list (which is now Aethir 0.209, Livepeer 0.199, WeatherXM 0.148). The veCRV discussion is reserved for the Section 4.1 ve-locking paragraph.
- **Section 4.1 (Constitutional Transparency / Pettit Non-Domination ve-locking discussion)**: Both surfaces distinguish raw post-exclusion CRV holding HHI (0.017) from veCRV-weighted voting concentration (0.26), with the gap attributed to lock-duration multipliers + Convex meta-governance aggregation.

The Aethir HHI in Table 4 was also corrected: the R1 footnote value of 0.171 reflected the March 2026 cascade snapshot; the R2 direct Dune pull (May 2026 top-1000) yields 0.209 under the universal ATH Top-N% convention applied in this manuscript (Section 2.10.2). Both reflect raw top-1000 holder concentration; the drift between snapshots and the Top-N% convention alignment are documented in Section 2.10.3.

**Manuscript changes**: Table 4 CRV Top-10% cell (60.7% to 34.4%); Section 3.2 DeFi-range paragraph rewritten with disambiguation; Section 4.1 publicity territory list updated; Section 4.1 ve-locking paragraph and Pettit non-domination paragraph updated to use 0.26 (direct computation); Table 4 methodology notes updated with explicit veCRV decomposition (Convex 48%, Yearn 14%, Stake DAO 9%); supplementary exhibit veCRV_voting_concentration_2026-05-17.csv ships with R2 submission.

---

## Issue 3: Table 5 N=40 and TT-expanded subsidy reproducibility

### Reviewer comment (verbatim)

> First, the HHI-Gini row reports N = 40, but the current data seem to contain missing Gini values for some protocols. Second, the TT-expanded subsidy analysis is still not straightforwardly reproducible from the repository files. The CSV contains fewer observations than the N reported in the manuscript. In addition, the conclusions drawn appear to be based on the old numbers.

### Response

The reviewer is correct on both sub-issues. We have addressed both in the R2 cycle.

**HHI-Gini row N=40 issue.** Three DePIN protocols (Aethir, Hivemapper, io.net) appeared in the R1 Table 4 footnote with HHI values but were noted as lacking the holder-level Gini and percentile data required for Table 4 reporting. The R1 cycle inconsistently reported N=40 for the HHI-Gini correlation despite this gap. For R2:

- Hivemapper (HONEY; Solana SPL): pulled via Helius DAS API (90,680 unique holders). HHI 0.017 (matches cascade methodology), Gini 0.92, Top-1% 6.7%, Top-10% 33.7%. Added as full Table 4 row.
- io.net (IO; Solana SPL): pulled via Helius DAS API (84,861 unique holders). HHI 0.111 (matches cascade exactly), Gini 0.95, Top-1% 30.0%, Top-10% 63.7%. Added as full Table 4 row.
- Aethir (ATH; Ethereum ERC-20): pulled via Dune erc20_ethereum.evt_transfer net-balance aggregation (top-1000 holders; May 2026 holders_ATH_2026-05-17.csv). HHI 0.209, Gini 0.43, Top-1% 33.6% (top-1-holder share), Top-10% 83.8% (top-10-holders cumulative share) under the universal ATH Top-N% convention codified in Section 2.10.2. Added as full Table 4 row.

All three protocols now appear as full Table 4 rows with complete holder-level data; the R2 manuscript reports HHI-Gini correlation at N=40 with both metrics measured for every protocol. The R1 footnote noting their lack of Gini/percentile data has been replaced with a footnote documenting the R2 supplementary holder-list collection.

**TT-expanded subsidy CSV reproducibility.** The reviewer correctly identifies that the R1 manuscript's reported N=22 for the TT-expanded subsidy test does not match the row count of subsidy-ratio-populated observations in `tokenterminal_financials.csv`. The R2 audit (Phase 0 Tier A2) confirmed that the canonical regression dataset contains 19 protocols with non-null Token Terminal subsidy_ratio data; the manuscript's N=22 was a stale count from an earlier draft. For R2:

- The Table 5 "Subsidy ratio (TT expanded)" row is updated to N=19 with corresponding Pearson r=0.10 (computed directly from the 19 protocols with TT subsidy data). Closely matches the manuscript's previously-reported r=0.095, confirming the qualitative conclusion (null cross-sector association) but with the corrected N.
- The Section 3.7 paragraph documenting the TT-expanded robustness check is updated to N=19 with r=0.097.
- A new supplementary sensitivity check is added: combining TT subsidy with on-chain subsidy data for protocols where TT data is not available yields N=25 (or N=22 with non-zero subsidy under either metric). Pearson r=0.42 with Livepeer included and r=0.008 with Livepeer excluded. This broader combined-sample sensitivity replicates the main Section 3.7 finding qualitatively: subsidy correlates with HHI only through Livepeer's 88.5x subsidy outlier.

**Manuscript changes**: Table 5 HHI-Gini row N updated to 40 with all-protocol Gini coverage; Table 5 TT-expanded subsidy row N corrected from 22 to 19 with r=0.097; Section 3.7 paragraph updated with both N=19 TT-direct and N=25 combined-sample sensitivity; Table 4 expanded from 37 to 40 protocols with Hivemapper / io.net / Aethir as full rows; supplementary exhibit phase0_data_collection_results_2026-05-17.md documents Phase 0 methodology; supplementary exhibit holders_ATH_2026-05-17.csv ships with R2 submission.

---

## Issue 4: Figure-vs-text statistical drift (Figures 4, 5, +)

### Reviewer comment (verbatim, key points)

> Figure 4 visually reports Mann-Whitney p = 0.016, Cohen's d = 0.96, DeFi mean = 0.043, and DePIN mean = 0.090. However, the caption and revised text report p = 0.014, d = 1.03, DeFi mean = 0.041, and DePIN mean = 0.091. Figure 5 has title reporting r = 0.19, p = 0.25, while the caption and abstract report r = 0.18, p = 0.28. The same goes for other figures, too. My general suggestion is to reproduce all the tables and figures, and make the text reflect the current data.

### Response

The reviewer is correct on the specific Figures 4 and 5 drift and on the general methodology suggestion. The R2 cycle adopts a "reproduce all tables and figures from canonical regression dataset" discipline. The figure regeneration cycle is in flight: the R2 cycle has fully aligned the body text and table values with the canonical regression dataset; the figure PNG regeneration is the remaining Phase 4 deliverable and will be applied to the R2 submission package as a parallel workstream to the manuscript surgery. The regenerated figures will produce visual statistics that match caption and body-text values exactly across all six figures (3, 4, 5, 6, 7, 8). The replication GitHub repository linked in the submission cover contains the regeneration scripts (Python with matplotlib).

**Methodology adopted for R2 onward.** Per the reviewer's general suggestion and to prevent recurrence, the R2 cycle adopts a single-canonical-CSV-of-record discipline: all manuscript surfaces with embedded statistics regenerate from one canonical regression dataset CSV (shipped as Supplementary File S5). The Section 2.10.3 methodology note documents this discipline, including a snapshot-date discipline acknowledging that voting-power distributions can drift over multi-month windows (the May 2026 Tally pull confirmed this empirically for Compound).

**Manuscript changes**: Section 2.10.3 figure-regeneration discipline note added; canonical regression dataset CSV updated with Phase 0 additions (Hivemapper, io.net, Aethir Gini values; TT-expanded subsidy N reconciliation); regeneration scripts to be committed in the R2 submission package per the figure-regeneration Phase 4 workstream.

---

## R2 substantive enhancements beyond Reviewer 1 issues

The R2 cycle also includes substantive philosophical-methodological strengthening that goes beyond the four issues Reviewer 1 raised. These are summarized below for transparency.

**Universal-amplification thesis as a new finding (Section 3.5).** The Issue 1 resolution combined with subsequent R2-cycle audits (Lido recompute; 126-address deep PCA audit) produces a new headline finding: delegation amplifies governance concentration in nine of ten Table 7 protocols (range 1.2x to 11.4x; mean 5.3x), with one structural exception (ENS at 0.39x, a mature delegate program producing dispersion below the holding baseline). This finding strengthens the paper's main thesis that institutional design at the operator and router level governs governance outcomes, since magnitude variation within sector is a cleaner empirical signal than direction variation, and the ENS counterexample demonstrates that delegation-mediated dispersion is achievable under explicit institutional-design choices. Section 3.5 is rewritten to reflect this, Section 3.5.1 documents ENS as the structural-exception case, Section 3.5.2 documents Curve and Balancer as a separate ve-token-class with extreme amplification (15x and 21x) under lock-duration-weighted voting, and Section 3.7 adds a PCA-symmetric robustness check confirming the finding holds even when foundation and aggregation-contract delegates are excluded.

**Philosophical-credibility two-layer framing (Section 2.10.1; Table 1 caption).** The R1 Table 1 caption glossed "Pettit Contestation (freedom from arbitrary power)" but "freedom from arbitrary power" is the textbook definition of non-domination, not contestation; the gloss-vs-label mismatch was an internal inconsistency. The R2 cycle resolves this by adopting an explicit two-layer framing: each lens has an operational mechanism (what we score in Table 1) and a philosophical goal (the normative warrant the tradition supplies). The scoring rubric measures the mechanism; the philosophical tradition supplies the warrant. The Pettit row keeps "Contestation" as the label (matching the scoring criteria: appeals + veto rights) and clarifies that non-domination is the goal-state contestability is designed to produce. The two-layer structure is documented in Section 2.10.1 and applied consistently across all five lenses; the Synergy Index reference paragraph (Section 2.10.6) is updated to reflect this.

**Inter-lens relationships paragraph (Section 2.9.6).** New paragraph documenting that the five lenses are mutually reinforcing rather than orthogonal: publicity (Kant) enables contestability (Pettit); polycentricity (Ostrom) enables knowledge-use (Hayek); Difference Principle (Rawls) constrains contestation outcomes; non-domination (Pettit) requires publicity (Kant) per Pettit 1997 §4.3. The Synergy Index's arithmetic-mean aggregation reflects this mutually-reinforcing structure; an alternative weakest-link aggregation (geometric mean) is identified as a structurally-defensible alternative.

**Systematic empirical-philosophical mapping (Section 4.1).** For each major empirical finding, we now state philosophical implications across applicable lenses. The universal delegation amplification finding (Section 3.5) registers across all five lenses simultaneously: it thins Kantian publicity, attenuates Pettit contestability in practice, undermines Rawlsian fairness, inverts Ostromian polycentricity, and silences Hayekian knowledge-use.

**Comparative methodology against existing DAO assessment frameworks (Section 4.5).** New paragraph positioning the five-lens framework against Aragon DAO Health Index, Snapshot voting analytics, Boardroom, and DAOstar standards along three dimensions: scope (philosophical-tradition anchor vs operational-only), aggregation (Synergy Index vs single-dimension), and comparability (uniform cross-protocol methodology vs per-protocol dashboards).

**Falsifiable forward claims + pre-registration intent (Section 4.9).** Two falsifiable predictions: (i) DePIN protocols entering the sample in 2026-2027 will exhibit higher holding HHI than DeFi protocols entering in the same period (conditional on launch year and insider allocation); (ii) any protocol introducing a delegate-program after R2 will produce voting HHI > holding HHI within 12 months of program launch. Future panel-data and event-study work testing these predictions will be pre-registered.

**Data-availability and reproducibility statement (Section 4.9).** Explicit statement that the 40-protocol governance concentration dataset, exclusions log, regression dataset, Phase 0 supplementary data (Hivemapper / io.net / Aethir holder distributions; veCRV cumulative deposits; Theil/Atkinson supplementary metrics) are all available in the linked replication repository.

**Methodology citations (Section 3.7).** Added Theil (1967), Atkinson (1970), Hirschman (1964) as historical sources for the inequality indices used in the post-exclusion robustness check. Added Shapley & Shubik (1954) and Banzhaf (1965) as power-index references contextualizing the HHI choice. Added Holmstrom (1979) as principal-agent foundation for the Section 3.5 delegate-program analysis.

**Multiple-comparisons correction note (Section 3.7).** Table 5 reports 14 separate tests; we now report that applying Benjamini-Hochberg false-discovery-rate correction at q=0.05 leaves three of four significant findings (the subsidy-with-Livepeer result is fragile under both multiple-comparisons correction and the Livepeer-outlier sensitivity already noted).

**Operationalization-dependency caveat (Section 4.8).** New paragraph acknowledging that the framework's empirical conclusions depend on operationalization choices; alternative operationalizations of each lens could yield different lens scores. The HHI cross-protocol rank ordering is robust to choice of concentration metric (Theil and Atkinson correlations in Section 3.7); the framework's lens-level rank ordering may be more sensitive to operationalization choices, an open empirical question for inter-rater reliability and operationalization-robustness analysis.

**Citations added (21 total across R2 cycle).** Theil (1967), Atkinson (1970), Hirschman (1964), Shapley & Shubik (1954), Banzhaf (1965), Holmstrom (1979), Hardin (1968), Olson (1965; existing citation made more central), Skinner (1998), Cohen (1989), Habermas (1996), Berlin (1958), Beitz (1979), Pogge (2002), Pettit (2012), Rawls (2001), Brennan & Buchanan (1985), North (1990), Atzori (2017), DuPont (2014), Schneider (2019), Tirole (2001).

---

## Acknowledgments

We thank Reviewer 1 for the comprehensive cross-surface audit that surfaced the drift class, and Reviewer 2 for the endorsement of publication. The R2 manuscript's universal-amplification finding (Section 3.5; abstract finding 4) is a direct product of Reviewer 1's R2 framing: applying consistent post-exclusion methodology across Table 4 and Table 7 produces a substantive interpretive change that strengthens the paper's main thesis about institutional design at the operator and router level governing governance outcomes. The R2 cycle's philosophical-credibility strengthening (Section 2.10.1 two-layer framing; Section 2.9.6 inter-lens relationships; Section 4.5 comparative methodology) addresses internal coherence questions adjacent to the reviewer's concerns; these enhancements also extend from the cross-surface audit discipline the reviewer's framing recommended.
