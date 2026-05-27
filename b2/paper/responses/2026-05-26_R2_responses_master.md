# B2 R2 Responses Master (2026-05-26 final)

**Paper:** Governance Concentration Beyond Token Allocation: A 40-Protocol Cross-Sectional Audit of DePIN and DeFi After Protocol-Controlled-Address Exclusion
**Working title (5 words):** Governance Concentration Beyond Token Allocation
**Author:** Zach Zukowski (Tokenization Systems; zach@tokenization.systems)
**Journal:** Frontiers in Blockchain (Manuscript ID 1853465; SSRN 6599278)
**Round:** R2 (response to Reviewer 1 Round 2 feedback)
**Date:** 2026-05-26 (supersedes the 2026-05-17 intermediate-state draft)

---

## Preamble

We thank both reviewers for their continued engagement with the manuscript. Reviewer 2 endorsed publication in R2. The responses below address Reviewer 1's four Round 2 issues at the level of granularity raised. Reviewer 1's general framing -- "reproduce all the tables and figures, and make the text reflect the current data" -- was adopted as a discipline for the entire R2 cycle, which extends beyond the four flagged issues into a comprehensive reproduce-and-sync pass and a structural reframe of the manuscript around its empirical contributions.

The most consequential single result of the R1-to-R2 reproduce-and-sync is a substantive interpretive change in Section 4.5: with corrected post-exclusion holding HHI baselines applied consistently across Table 4 and Table 7, Uniswap and Optimism flip from delegation-mediated dispersion to delegation amplification. Post-2026-05-17 sample expansion via the deep PCA audit cycle further expanded Table 7 from N = 8 to N = 10 (adding GMX and ENS via Tally pulls per the 12-month governance-activity gate). The voting-HHI methodology refresh expanded Snapshot pulls to all proposals in a 12-month rolling window 2025-05-22 to 2026-05-22 and Tally pulls to top-1000 delegates per protocol; the refresh surfaced GMX as a second structural-exception counterexample (1.2x amplification at top-100 sample flipped to 0.87x dispersion at top-1000 sample; sampling-depth artifact resolved). The multi-source PCA-symmetric extension cycle expanded Table 7 from N = 10 to N = 13 by adding three Solana-native protocols (JUP delegated-vote 0.057x; HNT VSR-lockup-weighted 0.35x to 0.53x; DRIFT VSR-lockup-weighted 1.6x). The R2 manuscript now documents a predominant-amplification finding with four structural exceptions: nine of thirteen protocols amplify (range 1.6x DRIFT to 9.9x Compound; mean approximately 4.9x), with ENS at 0.45x (Section 4.5.1 mature-delegate-program counterexample), GMX at 0.87x (Section 4.5.1.1 methodology-sensitive counterexample), HNT at 0.35x to 0.53x (Section 4.5.4 Solana VSR-lockup-weighted), and JUP at 0.057x (Section 4.5.4 Solana delegated-vote with broad-airdrop-user-base; the most-extreme dispersion outlier, 8x more extreme than ENS).

A PCA-symmetric robustness check (Section 4.6) extends the predominant-amplification finding across three independent governance-data sources: Tally all-delegates depth (AAVE N = 150,911; COMP N = 18,627; UNI N = 48,707; ARB N = 437,453; all four sub-0.005 HHI shift versus top-1000 baseline, validating the top-1000 methodology floor); Snapshot signer-side functional-PCA exclusion via a new sibling canonical store registering four confirmed entries (Compound Foundation; Balancer DAO multisig; Kevin Owocki / Gitcoin Maintainer; WXM Hedgey-vested insider); and Solana on-chain governance program parsing for JUP, HNT, and DRIFT. A methodologically substantive finding from the Snapshot signer-side PCA-symmetric recompute: exclusion is not monotonic in the concentration-reduction direction. For three of four Snapshot protocols with confirmed signer-side functional PCAs, exclusion produces the expected concentration reduction; for GTC, signer-side exclusion increases voting HHI from 0.1792 to 0.1948 (smaller-denominator effect). PCA-symmetric exclusion is therefore a substantive direction-of-effect test rather than a mechanical concentration-reduction adjustment.

The manuscript was further reframed during a final 2026-05-26 polish cycle. The R1 framing developed a five-lens philosophical-framework integrated with the empirical results; the R2 manuscript leads with the measurement contributions and routes the philosophical-interpretation thread to a companion paper (Zukowski 2026e). This preserves every R1 statistical finding while making the empirical contribution the spine of the paper.

---

## Issue 1: Table 7 holding-HHI inconsistency (interpretive flip)

### Reviewer comment (verbatim, key points)

> Table 7 still uses the old holding-HHI baselines for some protocols, even though the corresponding HHI values have been revised elsewhere in the paper and repository. ... Using the revised holding-HHI value would make the voting/holding ratio roughly 2.7X rather than 0.84X [for Uniswap]. Optimism's Table 4/processed-data holding HHI is approximately 0.009, while Table 7 still uses 0.042. ... Lido's ratio also appears lower when the revised holding HHI is used. ... I recommend that Table 7 be fully recomputed using the same proper holding-HHI values used in Table 4 and in the regression dataset.

### Response

The reviewer is correct on all three flagged cases. Table 7 has been fully recomputed using post-exclusion holding HHIs consistent with Table 4. The Compound and Arbitrum rows use Snapshot-sourced voting HHIs per the R1 author rationale (larger active-voter pools than Tally top-100 sampling); voting HHI source assignments otherwise reflect the methodology floor established by the post-R1 multi-source PCA-symmetric extension. Holding HHIs are uniformly post-exclusion across Table 7.

**Table 7 current state (N = 13; post-multi-source PCA-symmetric extension):**

| Protocol | Sector | Holding HHI (post-exclusion) | Voting HHI | Ratio | Direction |
|---|---|---:|---:|---:|---|
| DIMO | DePIN | 0.025 | 0.228 | 9.1x | amplifies |
| Lido | DeFi | 0.008 | 0.050 | 6.3x | amplifies |
| WeatherXM | DePIN | 0.148 | 0.556 | 3.8x | amplifies |
| Compound | DeFi | 0.009 | 0.089 | 9.9x | amplifies |
| Aave | DeFi | 0.013 | 0.058 | 4.4x | amplifies |
| Uniswap | DeFi | 0.010 | 0.027 | 2.7x | amplifies (FLIP from R1 0.84x) |
| Arbitrum | Infra | 0.012 | 0.038 | 3.1x | amplifies |
| Optimism | Infra | 0.009 | 0.033 | 3.6x | amplifies (FLIP from R1 0.79x) |
| GMX | DeFi | 0.065 | 0.057 | 0.87x | DISPERSES (Section 4.5.1.1; methodology-sensitive) |
| ENS | Infra | 0.049 | 0.022 | 0.45x | disperses (Section 4.5.1; mature delegate program) |
| DRIFT | DeFi | 0.053 | 0.083 | 1.6x | amplifies (Solana VSR; Section 4.5.4) |
| HNT | DePIN | 0.075 | 0.026 to 0.039 | 0.35x to 0.53x | DISPERSES (Solana VSR; Section 4.5.4) |
| JUP | DeFi | 0.096 | 0.0055 | 0.057x | DISPERSES (Solana delegated-vote; most-extreme outlier; Section 4.5.4) |

Solana rows use on-chain governance program parsing (JUP via Dune `jupiter_solana.govern_call_setvote` per-signer max-weight aggregation; HNT and DRIFT via Helius RPC parsing of SPL Governance VoteRecordV2 accounts). The Aave row reflects the post-R1 all-delegates pull at N = 150,911; the four deeper-N sweeps validate the top-1000 methodology floor (all four sub-0.005 HHI shift versus top-1000 baseline).

**Substantive interpretive consequence.** The flip is not a typo correction: it changes the Section 4.5 finding from the R1 "delegation amplifies unevenly, with two infrastructure protocols showing opposite patterns" to the R2 predominant-amplification framing across nine of thirteen protocols (range 1.6x to 9.9x; mean approximately 4.9x), with four structural exceptions documenting design-tractable dispersion. Section 4.5 opening paragraph, sector-breakdown paragraph, Citizens' House and Dual Governance paragraphs, and the Fritsch et al. extension paragraph have all been rewritten. New subsections Section 4.5.1 (ENS counterexample), Section 4.5.1.1 (GMX counterexample), Section 4.5.4 (within-Solana governance heterogeneity), Section 4.5.4.1 (Drift Foundation proposal-authorship versus vote-weight decoupling), and Section 4.5.5 (cross-protocol institutional-governance-investor pattern as candidate fifth concentration axis) have been added. Abstract and Section 6 conclusion updated to the predominant-amplification framing.

**On Lido.** The reviewer's observation that Lido's ratio "appears lower" with the revised holding HHI is opposite to what our data produces. The R1-corrected Lido holding HHI at this letter's authoring date (Table 4 value 0.013) yielded amplification 6.8x. The post-R1 deep PCA audit refined Lido holding HHI to 0.008 via PCA exclusion of additional Lido DAO addresses identified in the 126-address audit. The voting-HHI methodology refresh expanded the Lido Snapshot pull from sample-bounded (N = 262 across 5 proposals) to comprehensive (N = 333 across all proposals in the 12-month rolling window), yielding voting HHI 0.050 and amplification ratio 6.3x. If the reviewer is computing a different Lido holding HHI from an alternative exclusion list (for example, one that does not exclude the Lido DAO Aragon treasury), we welcome specification of the methodology; the canonical exclusion set is documented in Supplementary File S6 at address granularity.

**On the Uniswap counterexample.** The pre-correction Uniswap result (0.84x) had been cited as evidence that Uniswap's mature delegate program disperses governance power. With the canonical burn-rule exclusion applied (the 0x000...000dead address holding 102.5M UNI, 11.3 percent of supply, structurally unable to participate in governance under any condition), Uniswap joins the predominant-amplification pattern at 2.7x. We document this transition explicitly in Section 4.5 because the prior result was load-bearing in the dispersion-via-mature-delegate-program literature; the corrected analysis reflects the cost of including a wallet that structurally cannot vote in the holding denominator.

**Compound Foundation as PCA at the voting layer.** Phase 0 fact-checking of the Tally API surfaced a substantive methodological finding: the top COMP Tally delegate (21.5 percent of total delegated voting power in the May 2026 pull) is Compound Foundation itself, structurally a protocol-controlled entity. The PCA-symmetric voting-HHI robustness check (Section 4.6) extends the holding-side methodology to the voting layer: PCA exclusion is not monotonic in the concentration-reduction direction (see GTC counterexample above), but predominant amplification holds for the deeper-N Tally sweep across AAVE, COMP, UNI, and ARB at sub-0.005 HHI shift versus the top-1000 baseline.

**Manuscript changes**: Table 7 rows fully recomputed; Table 7 caption updated with explicit post-exclusion methodology note; Section 4.5 opening through Fritsch-extension paragraphs rewritten; new Sections 4.5.1, 4.5.1.1, 4.5.4, 4.5.4.1, 4.5.5; Section 4.6 PCA-symmetric robustness paragraph added; Section 3.3 snapshot-date discipline paragraph added (documents the March 2026 to May 2026 delegate-pool drift; the R2 manuscript uses the March 2026 snapshot consistent with the rest of the dataset for the eight protocols with March 2026 voting data; GMX and ENS additions use May 2026 Tally per Section 4.5 Table 7 footnote ‡); Figure 4 (delegation-adjusted bar chart) regenerated with N = 13 data; abstract finding 4 + Section 1.1 finding 4 + Section 5.6 contribution 4 updated to the predominant-amplification framing.

---

## Issue 2: Curve Top-10 column + CRV text disambiguation

### Reviewer comment (verbatim)

> In Table 4, Curve's HHI has been corrected to the post-exclusion raw-CRV value, but its Top-10 value is still the pre-exclusion one. The repository reports a substantially lower post-exclusion Top-10 value for Curve than the value shown in the table. In several places in the text, CRV is reported as HHI = 0.171, even though Table 4 now reports raw CRV, with HHI = 0.017. If this is supposed to be about veCRV, please mention it explicitly in the text.

### Response

The reviewer is correct on both points. Table 4 Curve Top-10 percentage has been corrected from 60.7 percent (pre-Convex-exclusion) to the post-exclusion value matching the canonical regression dataset. The CRV-versus-veCRV disambiguation has been implemented across all textual surfaces, with the 0.171 proxy replaced by a directly-computed veCRV voting concentration value (0.26).

**Direct veCRV voting concentration computation.** The R1 manuscript used 0.171 as a proxy for veCRV-weighted voting concentration. The 0.171 figure is the raw CRV holding HHI including the Convex veCRV custody position (which holds substantial CRV that has been locked into veCRV). For R2, we compute the actual veCRV-weighted voting concentration directly via Dune analysis of the Curve VotingEscrow Deposit events at 0x5f3b5dfeb7b28cdbd7faba78963ee202a494e2a2. Aggregating cumulative CRV deposits across the top-50 historical veCRV lockers yields HHI 0.26: Convex CRV Locker at 48.0 percent of top-50 deposit-weighted share; Yearn yveCRV at 13.5 percent; Stake DAO sdCRV at 9.5 percent; the remaining 47 lockers each less than 4 percent. The 0.26 direct computation captures the actual gauge-weight voting concentration that veCRV produces and is substantively higher than the 0.171 proxy.

**Disambiguation applied at every textual surface.**

- Table 4 row: HHI = 0.014 (raw post-Convex-exclusion CRV holdings); Top-10 percent = 31.2 (post-exclusion).
- Table 4 caption: HHI for Curve reflects raw CRV holdings after excluding the Convex veCRV custody position; veCRV-weighted voting concentration is approximately 0.26 computed from cumulative CRV deposit volume across the top-50 historical veCRV lockers; methodology discussed in Section 4.5.2.
- Section 4.2 cross-protocol range description: CRV's raw 0.014 places it mid-range; the 0.26 veCRV voting concentration is referenced with explicit methodology cite to Section 4.5.2.
- Section 4.5.2 (vote-escrowed governance subsection; new in R2): Both Curve veCRV (15x amplification relative to raw 0.014) and Balancer veBAL (21x amplification at voting HHI 0.626 against holding 0.030) documented as a distinct extreme-amplification mechanism class separate from delegate-program-based amplification.

The Aethir Table 4 row was also updated: the R1 footnote value reflected the March 2026 cascade snapshot; the R2 direct Dune pull yields HHI 0.095 post-PCA-exclusion (the post-cycle-4 0xfc78 Safe multisig was identified as an additional PCA in the deep PCA audit). Both reflect raw top-1000 holder concentration after PCA exclusion; the cascade-vs-direct drift is documented in Supplementary File S6.

**Manuscript changes**: Table 4 CRV row corrected; Table 4 methodology notes updated with explicit veCRV decomposition (Convex 48 percent, Yearn 14 percent, Stake DAO 9 percent); new Section 4.5.2 "Secondary extension: vote-escrowed governance" documenting both Curve and Balancer ve-token amplification; Supplementary File S6 (address-by-address PCA documentation) updated with Aethir 0xfc78 entry; supplementary exhibit `veCRV_voting_concentration_2026-05-17.csv` ships with the R2 supplementary materials.

---

## Issue 3: Table 5 N = 40 and TT-expanded subsidy reproducibility

### Reviewer comment (verbatim)

> First, the HHI-Gini row reports N = 40, but the current data seem to contain missing Gini values for some protocols. Second, the TT-expanded subsidy analysis is still not straightforwardly reproducible from the repository files. The CSV contains fewer observations than the N reported in the manuscript. In addition, the conclusions drawn appear to be based on the old numbers.

### Response

The reviewer is correct on both sub-issues. Both have been addressed.

**HHI-Gini row N = 40.** Three DePIN protocols (Aethir, Hivemapper, io.net) appeared in the R1 Table 4 footnote with HHI values but were noted as lacking the holder-level Gini and percentile data required for Table 4 reporting. The R1 cycle inconsistently reported N = 40 for the HHI-Gini correlation despite this gap. For R2:

- Hivemapper (HONEY; Solana SPL): pulled via Helius DAS API (90,680 unique holders). HHI 0.018, Gini 0.91, Top-1 percent 5.7, Top-10 percent 31.1. Added as full Table 4 row.
- io.net (IO; Solana SPL): pulled via Helius DAS API (84,861 unique holders). HHI 0.125, Gini 0.94, Top-1 percent 33.5, Top-10 percent 61.2. Added as full Table 4 row.
- Aethir (ATH; Ethereum ERC-20): pulled via Dune top-1008 with eight PCA exclusions. HHI 0.095, Gini 0.94, Top-1 percent 19.7, Top-10 percent 67.6. Added as full Table 4 row.

All three protocols now appear as full Table 4 rows with complete holder-level data; the R2 manuscript reports HHI-Gini correlation at N = 40 with both metrics measured for every protocol (Pearson r = 0.59, p < 0.001; documented in Table 5 and Supplementary File S0).

**TT-expanded subsidy CSV reproducibility.** The reviewer correctly identifies that the R1 manuscript's reported N for the TT-expanded subsidy test does not match the row count of subsidy-ratio-populated observations in the underlying CSV. The R2 audit confirmed that the canonical regression dataset contains 20 protocols with non-null Token Terminal subsidy data at the R2 cycle's authoring date; the canonical subsidy battery uses N = 23 protocols with non-zero subsidy under either Token Terminal or on-chain metrics (and N = 22 when Livepeer is excluded). For R2-current:

- Table 5 "Subsidy ratio (cross-sector)" row: Pearson r = 0.59, p = 0.003, N = 23. Fragile (Livepeer-driven).
- Table 5 "Subsidy ratio (TT expanded)" row: Pearson r = 0.12, p = 0.61, N = 20. Null (robustness check).
- Table 5 "Subsidy ratio (excluding Livepeer)" row: Pearson r = 0.07, p = 0.77, N = 22. Null.
- Spearman rank correlation on the full subsidy sample: rho = 0.20, p = 0.35.
- Section 4.6 Robustness paragraph: the headline subsidy correlation is entirely Livepeer-driven (Livepeer subsidy ratio of 88.5x is a 3.5-sigma outlier on the subsidy axis); excluding Livepeer alone reduces the Pearson correlation to a clean null (r = 0.07).

A new multivariate specification (Section 4.6) with both subsidy ratio and DePIN sector indicator on the 23-protocol non-zero-subsidy sample (HC3 robust standard errors) reinforces the Livepeer-driven interpretation: with all 23 protocols, the DePIN sector indicator is significant (p = 0.016) while subsidy is not (p = 0.36; Adj R-squared = 0.47); excluding Livepeer, the subsidy coefficient is strongly non-significant (p = 0.94) while the DePIN sector indicator is significant (p = 0.007). A convention-invariance robustness check using the on-chain operating-cost subsidy specification reproduces the same null pattern (subsidy p = 0.45; DePIN p = 0.005).

**Raw-OC subsidy refinement.** A focused investigation against the raw on-chain operating-cost computations for the burn-active panel surfaced four canonical-methodology refinements grounded in project-Foundation primary sources (DIMO, Morpheus AI, Filecoin, Helium). Material reclassifications: DIMO moves from net-deflationary subset to subsidy-heavy subset (cycle 3 burn-to-dead aggregation diverged from the DIMO Foundation's canonical revenue methodology by 13.8x token count); Morpheus AI moves from net-deflationary to subsidy-heavy (cycle 3 filters captured cross-chain bridge flows rather than protocol revenue and emissions); Filecoin subsidy ratio refined to 46.05 (Token Terminal emissions undercount of 140 percent due to a vesting-discount filter; cross-validated against Spacescope, Tokenomist, and Coinbase Institutional Tokenomics Review primary sources within 1.8 percent). A verification pass against the remaining thirteen panel protocols produced zero additional canonical-methodology shifts. The cross-protocol pattern is structurally informative: the four protocols requiring methodology refinement are all DePIN-class; the eleven non-DePIN protocols (DeFi blue chips, mid-cap DeFi, L2 / L1 infrastructure) passed direct verification with no methodology shifts. This is offered as a candidate methodology contribution; the structural difference between newer DePIN protocols (cross-chain bridging, custom reward distribution mechanisms) and mature non-DePIN protocols (community-canonical aggregator alignment, methodologically stable Foundation reporting) may concentrate in subsequent B-series papers.

**Manuscript changes**: Table 5 rows updated with current canonical values; Table 4 expanded from 37 to 40 protocols with Hivemapper, io.net, and Aethir as full rows; Section 4.6 subsidy-multivariate paragraph documenting the four specifications; Supplementary File S6 documents the raw-OC methodology refinements per protocol; Supplementary File S8 documents the Token Terminal expansion battery.

---

## Issue 4: Figure-vs-text statistical drift (Figures 2, 3, others)

### Reviewer comment (verbatim, key points)

> Figure 4 visually reports Mann-Whitney p = 0.016, Cohen's d = 0.96, DeFi mean = 0.043, and DePIN mean = 0.090. However, the caption and revised text report p = 0.014, d = 1.03, DeFi mean = 0.041, and DePIN mean = 0.091. Figure 5 has title reporting r = 0.19, p = 0.25, while the caption and abstract report r = 0.18, p = 0.28. The same goes for other figures, too. My general suggestion is to reproduce all the tables and figures, and make the text reflect the current data.

### Response

The reviewer is correct on the specific figures and on the general methodology suggestion. The R2 cycle adopts a "reproduce all tables and figures from canonical regression dataset" discipline. The figure regeneration cycle is complete: all five main-text figures have been regenerated from the canonical regression dataset and the visual statistics now match caption and body-text values exactly.

The figures in the R2 manuscript are renumbered relative to the R1 manuscript. The R1 figure numbering (3, 4, 5, 6, 7, 8) reflected an earlier iteration that included two theory figures (philosophical-framework architecture; conceptual model) at positions 1 and 2; those theory figures were removed during the R2 empirical reframe and the remaining figures were renumbered 1 through 5. The R2 figures are:

- **Figure 1** (HHI bar chart across 40 governance tokens; was R1 Figure 3): Holding HHI ranges 0.005 (Hyperliquid) to 0.199 (Livepeer); DePIN cluster in upper half visible.
- **Figure 2** (DePIN versus DeFi sector boxplot; was R1 Figure 4): Mann-Whitney p = 0.020; Cohen's d = 0.94; N = 15 / 15; visual and caption stats match exactly. The R1 figure visual reported p = 0.016 / d = 0.96 while the caption reported p = 0.014 / d = 1.03; the R2 regenerated figure and caption both report the canonical p = 0.020 / d = 0.94 (the headline values reflect a wider 30-protocol sector contrast under the post-PCA-cycle holder-list refresh and the universal-burn-rule exclusion methodology).
- **Figure 3** (insider allocation scatter; was R1 Figure 5): Pearson r = 0.05, p = 0.76, N = 37 (the headline null). The R1 figure visual reported r = 0.19, p = 0.25 while the caption reported r = 0.18, p = 0.28; the R2 regenerated figure and caption both report the canonical r = 0.05 / p = 0.76 / N = 37 (the R1 manuscript value reflected an earlier pre-canonical-regression dataset state; the headline r dropped to 0.05 after the canonical regression dataset sync established the post-exclusion HHI baseline as the dependent variable and post-PCA-cycle insider allocation as the predictor).
- **Figure 4** (delegation-adjusted bar chart; replaces R1 Figure 6): 13-protocol delegation amplification chart with ratios annotated; visual and caption stats reflect the post-multi-source extension N = 13 sample.
- **Figure 5** (subsidy ratio scatter; was R1 Figure 7): Pearson r = 0.59 inclusive of Livepeer, r = 0.07 excluding Livepeer; N = 23; visual and caption stats match.

**Methodology adopted for R2 onward.** Per the reviewer's general suggestion and to prevent recurrence, the R2 cycle adopts three reinforcing disciplines: (i) a single-canonical-regression-dataset-of-record discipline, with all manuscript surfaces with embedded statistics regenerating from one canonical regression dataset CSV (shipped as Supplementary File S5); (ii) a canonical statistics ledger (Supplementary File S0; new in R2) listing every body-text statistic with its sample size and the reporting convention, providing a single source of truth for body, tables, figures, captions, abstract, and conclusion; (iii) a submission-readiness validation tool (`tools/content-build/submission_readiness_check.py`) that verifies figure-path existence, supplement-reference resolution, output_formats template existence, current_version coherence in METADATA, build-warning-free invocation, figure-caption numbering coherence, and (via a companion `reviewer_trap_lint.py`) prose-side lint for causal-overclaim language and pandoc residue.

**Manuscript changes**: All five main-text figures regenerated from the canonical regression dataset via `tools/content-build/b2_figure6_regen.py` and sister scripts; Section 3.3 documents the figure-regeneration discipline; canonical regression dataset CSV ships as Supplementary File S5; canonical statistics ledger ships as Supplementary File S0; submission-readiness validation tooling ships at `tools/content-build/submission_readiness_check.py` and `tools/content-build/reviewer_trap_lint.py`.

---

## R2 substantive enhancements beyond Reviewer 1 issues

The R2 cycle also includes substantive strengthening that goes beyond the four issues Reviewer 1 raised. These are summarized below for transparency.

**Predominant-amplification thesis with four structural exceptions.** The Issue 1 resolution plus the post-R1 deep PCA audit (Table 7 sample expanded from N = 8 to N = 10 via GMX and ENS Tally additions), the voting-HHI methodology refresh (Snapshot all-proposals plus Tally top-1000), and the multi-source PCA-symmetric extension (Table 7 N = 10 to N = 13 via JUP, HNT, DRIFT Solana additions) produce the R2 headline finding: delegation amplifies governance concentration in nine of thirteen protocols (range 1.6x DRIFT to 9.9x Compound; mean approximately 4.9x), with ENS at 0.45x (Section 4.5.1), GMX at 0.87x (Section 4.5.1.1), HNT at 0.35x to 0.53x (Section 4.5.4), and JUP at 0.057x (Section 4.5.4) as the four structural exceptions.

**Within-Solana governance heterogeneity (Section 4.5.4).** Three Solana-native protocols have on-chain voting HHI computable via proper-weight methodology: JUP at 0.00546 via per-signer max(weight) aggregation (delegated-vote design); HNT at 0.0261 to 0.0394 (sensitivity range under VSR position-state reconstruction; 14.8 percent closed-position rate brackets the bounds); DRIFT at 0.0833 via direct on-chain VoteRecordV2 parsing (VSR lockup-weighted design analogous to HNT). The within-Solana spread (0.005 to 0.083; 15x range) is structurally organized by voting-weight mechanism design as the primary axis: VSR-using protocols (HNT, DRIFT) cluster at EVM-typical voting HHI; delegated-vote JUP is the only Solana protocol exhibiting voting concentration order-of-magnitude below the EVM cross-section median. A categorical claim that Solana governance is less concentrated than EVM governance is not supported by the proper-weight Solana sample; the apparent low-concentration finding from vote-count-proxy methodology on Helium was an artifact superseded by lockup-weight reconstruction.

**Drift Foundation proposal-authorship versus vote-weight decoupling (Section 4.5.4.1).** Drift Protocol exhibits a governance pattern with no close analog in the EVM-protocol cross-section. A single Drift Foundation submitter address (`4CL25...wPiiF` on Solana) proposed 11 of the 13 DRIFT Improvement Proposals over the 12-month window while holding only 0.18 percent of total DRIFT vote weight. Proposal-authorship and vote-weight are structurally decoupled: the Foundation submits proposals, the token-weighted voter pool decides, and the two functions are not co-located in the same address. EVM-protocol top delegates are typically both agenda-setters and vote-weight-holders (Compound Foundation as the Tally top delegate both proposes and votes from a foundation-controlled wallet at 21.5 percent share); the Drift Foundation structure separates these functions explicitly.

**Cross-protocol institutional-governance-investor pattern (Section 4.5.5).** A candidate fifth concentration axis emerges from cross-protocol aggregation. The Snapshot voter-pool extension to 13 protocols aggregated 11,077 unique voter addresses; 1,801 voters (16.3 percent) participate in 2 or more protocols' Snapshot governance. A small institutional-governance-investor class (approximately 10 to 50 addresses) participates in 6 or more protocols' delegate programs simultaneously. The top three institutional cross-protocol delegators collectively exert 17.0 percent combined Snapshot voting power across the L1 DeFi suite: PGov (`0x3fb19771...`; pgov.eth) at 10.16 percent combined summed share across 7 DAOs; Tane Governance at 4.83 percent across 6 DAOs; Arana Digital at 2.04 percent across 6 DAOs. These are professional governance firms whose business model is providing cross-protocol delegation services to token-holders who do not vote directly; the firms aggregate delegated voting power across multiple protocols simultaneously, creating correlated voting patterns invisible to per-protocol Mann-Whitney or Cohen's d analysis. The Tally-side cross-protocol overlap network is identified as a measurement priority for future work.

**Profitability, size, and insider-retention checks (Section 4.6).** Secondary checks sharpen the insider-retention interpretation. Larger protocols by fully diluted valuation have fewer insider wallets in their current top-10 holder set (Pearson r = -0.36, p = 0.032, N = 36; Spearman rho = -0.31, p = 0.063), and the market-capitalization specification has the same direction at borderline significance (Pearson r = -0.34, p = 0.050, N = 33). Balance-retention specifications are not significant, indicating a composition-shift interpretation rather than a retained-balance result. Net-deflationary protocols also show no statistically significant difference in insider retention by count or balance (Mann-Whitney p = 0.57 and p = 0.78 respectively). These checks support the paper's main distinction between launch allocation and current holder composition.

**Empirical-paper reframe (2026-05-26 polish cycle).** The R1 manuscript developed a five-lens philosophical-framework integrated with empirical results; the R2 manuscript leads with the measurement contributions and routes the philosophical-interpretation thread to a companion paper (Zukowski 2026e). The reframing preserves every R1 statistical finding. Key surface changes:

- Title: from the R1 submission title "Governance Concentration Beyond Token Allocation: An Institutional Design Analysis of DePIN and DeFi" to "Governance Concentration Beyond Token Allocation: A 40-Protocol Cross-Sectional Audit of DePIN and DeFi After Protocol-Controlled-Address Exclusion". The lead phrase is preserved exactly for editorial-system continuity; the subtitle is reframed from theory-framing to empirical-audit framing
- Abstract: leads with allocation null, sector contrast, subsidy null, delegation amplification, and the PCA methodology contribution; no philosophical-framework framing
- Section 1.2 (new): one-paragraph bridge to the companion paper Zukowski (2026e) at SSRN registering the Polanyian fourth-fictitious-commodity interpretation; the bridge cites the companion paper rather than developing the argument inline
- Section 5.6 Contributions: four empirical contributions (PCA methodology; allocation null with insider retention contrast; corrected sector contrast; predominant delegation amplification with structural exceptions); no two-layer philosophical-framework contribution
- JEL expansion from seven to nine codes (added C81 Methodology for Collecting Microeconomic Data anchoring the PCA exclusion methodology; added G23 Non-bank Financial Institutions anchoring the DeFi and meta-governance institutional-investor coverage)
- Reference list cleanup: 40 orphan references (residue from the earlier theory-heavy framing) removed from the bibliography; 19 entries migrated to the companion paper's bibliography; Polanyi 1944 preserved as the Tier-1 keeper because Section 1.2 names "Polanyian interpretation" verbatim
- Section 1.1 motivation paragraph order corrected so setup precedes findings teaser; "none explains" softened to "none is sufficient as a standalone explanation" because sector membership, insider retention, and delegate-program design do explain parts of variation
- Section 2.1 opener rewritten gap-first to lead with the three measurement gaps motivating the paper
- Section 4.5 paragraph 2 deduplicated to lead with sector breakdown rather than restating the headline
- Section 5.2 collapsed to a single design-tractability paragraph naming the Anyone Protocol and ENS counterexamples
- Figure 1 relocated from Section 3.2 Methods to Section 4.2 Results adjacent to Table 4
- Section 5.8 split into Section 5.8 Future Research plus a new Section 5.9 Reproducibility and Data Availability
- Headline-statistic repetition reduced from ten mentions of "1.6x to 9.9x; mean approximately 4.9x" to three full and two abbreviated (canonical: abstract, Section 4.5 lead, Section 6 conclusion; abbreviated in Table 7 and Figure 4 captions)
- Associative-language sweep replaced "predicts", "predictor", "predicted by", "drives", "driven by", and "determines" with associative alternatives ("is associated with", "is consistent with", "reflects", "indicator", "covariate") outside the Section 5.8 falsifiable-predictions section
- Section 3.5 Supplemental Instruments stub collapsed; Section 4.6 Additional Concentration Mechanisms stub collapsed with synthesis moved to Section 5.5 Summary
- Stale section cross-references resolved (Section 4.4 misdirect in Table 7 footnote; circular self-reference in Section 4.7 robustness; Section 3.9 / Section 4.7 references updated post-renumber)

**Falsifiable forward claims plus pre-registration intent (Section 5.8).** Four falsifiable predictions operationalized for future panel-data and event-study work: (i) sector persistence (DePIN protocols launching in 2026-2027 will exhibit higher post-distribution holding HHI than DeFi protocols launching in the same period); (ii) delegation amplification universality (any protocol introducing a formal delegate program will produce voting HHI greater than holding HHI within twelve months of launch, with amplification magnitude varying by delegate-program design rather than by sector); (iii) insider-retention persistence (within-protocol panel correlation: protocols whose insider fraction increases will exhibit increased holding HHI); (iv) delegate-program design as moderator (broad-community-delegate distribution design choices yield lower amplification ratios). All four predictions inherit the methodology applied in this paper (PCA-symmetric exclusion via the five-class typology; HHI on post-exclusion top-1,000 holders; Mann-Whitney for two-sample tests; bootstrap 95 percent percentile intervals). Pre-registration commitment: hypothesis specifications, statistical tests, and falsification thresholds will be deposited on the Open Science Framework prior to data collection for any panel-data or event-study extension. Full operationalization detail per prediction in Supplementary File S17.

**Longitudinal panel evidence (Supplementary File S7).** A companion quarterly HHI panel for 14 governance tokens over 8 quarters post-token-generation event documents that 11 of 14 protocols exhibit monotonic governance HHI decay over the 24-month observation window, with the three exceptions reflecting mechanism-specific lock-in: CRV (vote-escrow), COMP (reservoir-drip emissions), and ENS (claim-window distribution). The longitudinal pattern reinforces the cross-sectional finding that initial allocation is not associated with steady-state concentration: distributions tend to deconcentrate over time across heterogeneous allocation designs.

**Data-availability and reproducibility statement (Section 5.9; new).** Explicit statement that the 40-protocol governance concentration dataset, exclusions log (133 protocol-controlled address exclusions across 38 protocols), canonical regression dataset including Token Terminal subsidy ratios and on-chain financial data, Hivemapper / io.net / Aethir holder distributions, veCRV cumulative deposit data underlying the Section 4.5.2 ve-locking analysis, and Theil / Atkinson supplementary metrics are available in the linked replication repository. Replication scripts for each table and figure are provided in Supplementary File S5; the cross-protocol Pearson and Spearman correlations reported across Sections 4.3, 4.4, and 4.6 can be reproduced via the replication scripts using only the linked public-source data.

---

## Acknowledgments

We thank Reviewer 1 for the comprehensive cross-surface audit that surfaced the manuscript-vs-data-of-record drift class in R1 Round 2 and motivated the R2 reproduce-and-sync discipline. The R2 manuscript's predominant-amplification finding with four structural exceptions (Section 4.5; abstract finding 4) is a direct product of Reviewer 1's framing: applying consistent post-exclusion methodology across Table 4 and Table 7 produced a substantive interpretive change. The post-R1 strengthening cycles -- voting-HHI methodology refresh, multi-source PCA-symmetric extension across Tally, Snapshot, and Solana on-chain governance program parsing, raw-OC subsidy refinement, and the empirical-paper reframe in the 2026-05-26 polish cycle -- all extend from the reviewer's general "reproduce all tables and figures and make the text reflect the current data" recommendation operationalized at saturation depth. The submission-readiness validation tooling shipped with this submission (`submission_readiness_check.py` plus `reviewer_trap_lint.py`) is designed to prevent recurrence of the bug classes Reviewer 1 surfaced. We thank Reviewer 2 for the endorsement of publication.
