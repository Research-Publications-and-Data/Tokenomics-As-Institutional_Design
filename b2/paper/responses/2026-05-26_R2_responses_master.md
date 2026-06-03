# B2 R2 Responses Master

**Paper:** Auditing Governance Concentration Beyond Token Allocation: A Live-Governance Study of 52 Token Protocols
**Working title (5 words):** Governance Concentration Beyond Token Allocation
**Author:** Zach Zukowski (Tokenization Systems; zach@tokenization.systems)
**Journal:** Frontiers in Blockchain (Manuscript ID 1853465; SSRN 6599278)
**Round:** R2 (response to Reviewer 1 Round 2 feedback)
**Date:** 2026-06-03

---

## Preamble

We thank both reviewers for their continued engagement with the manuscript. Reviewer 2 endorsed publication in R2. The responses below address Reviewer 1's four Round 2 issues at the level of granularity raised. Reviewer 1's general framing ("reproduce all the tables and figures, and make the text reflect the current data") was adopted as a discipline for the entire revision, which extends beyond the four flagged issues into a comprehensive reproduce-and-sync pass and a structural reframe of the manuscript around its empirical contributions.

The most consequential single result of the reproduce-and-sync is a substantive interpretive change in Section 4.5: with corrected post-exclusion holding HHI baselines applied consistently across the holding-concentration table and the delegation table, Uniswap and Optimism flip from delegation-mediated dispersion to delegation amplification. The revised paper documents a predominant-amplification finding with structural exceptions: of the eighteen protocols with computable voting concentration, thirteen amplify and five disperse. The dispersers are ENS (Section 4.5.1, mature delegate program), GMX (Section 4.5.1.1, methodology-sensitive counterexample), Helium (Section 4.5.4, Solana VSR-lockup-weighted), Jupiter (Section 4.5.4, Solana delegated-vote with broad-airdrop user base; the most-extreme dispersion outlier), and Livepeer (Section 4.5, the most pronounced DePIN governance disperser).

A PCA-symmetric robustness check (Section 4.6) extends the predominant-amplification finding across three independent governance-data sources: Tally all-delegates depth (AAVE N = 150,911; COMP N = 18,627; UNI N = 48,707; ARB N = 437,453; all four sub-0.005 HHI shift versus the top-1000 baseline, validating the top-1000 methodology floor); Snapshot signer-side functional-PCA exclusion registering four confirmed entries (Compound Foundation; Balancer DAO multisig; Kevin Owocki / Gitcoin Maintainer; WXM Hedgey-vested insider); and Solana on-chain governance program parsing for Jupiter, Helium, and Drift. A methodologically substantive finding from the Snapshot signer-side PCA-symmetric recompute: exclusion is not monotonic in the concentration-reduction direction. For three of four Snapshot protocols with confirmed signer-side functional PCAs, exclusion produces the expected concentration reduction; for GTC, signer-side exclusion increases voting HHI from 0.1792 to 0.1948 (smaller-denominator effect). PCA-symmetric exclusion is therefore a substantive direction-of-effect test rather than a mechanical concentration-reduction adjustment.

The manuscript was also reframed around its empirical contributions, and the revision adds substantial strengthening across data, methodology, and architecture. To avoid duplicating the cover letter, those substantial changes are described there and detailed in the revised manuscript; the point-by-point responses below focus on Reviewer 1's four issues.

---

## Issue 1: Table 7 holding-HHI inconsistency (interpretive flip)

### Reviewer comment (verbatim, key points)

> Table 7 still uses the old holding-HHI baselines for some protocols, even though the corresponding HHI values have been revised elsewhere in the paper and repository. ... Using the revised holding-HHI value would make the voting/holding ratio roughly 2.7X rather than 0.84X [for Uniswap]. Optimism's Table 4/processed-data holding HHI is approximately 0.009, while Table 7 still uses 0.042. ... Lido's ratio also appears lower when the revised holding HHI is used. ... I recommend that Table 7 be fully recomputed using the same proper holding-HHI values used in Table 4 and in the regression dataset.

### Response

The reviewer is correct on all three flagged cases. The delegation table has been fully recomputed using post-exclusion holding HHIs consistent with the current holding-concentration table and regression dataset. The Compound and Arbitrum rows use Snapshot-sourced voting HHIs per the R1 author rationale (larger active-voter pools than Tally top-100 sampling); the remaining voting-HHI source assignments reflect the methodology floor of all-proposal Snapshot pulls and top-1000-delegate Tally pulls. Holding HHIs are uniformly post-exclusion across the table.

The revised delegation table (Table 6) reports eighteen protocols. Relative to R1 it adds the protocols for which on-chain voting concentration is computable on a proper-weight basis, including three Solana-native protocols (Jupiter via per-signer max-weight aggregation on delegated votes; Drift via SPL Governance VoteRecordV2 parsing and Helium via Voter Stake Registry position-state reconstruction, both VSR-lockup-weighted), and it corrects the holding-HHI baselines for the carried-over rows. Of the eighteen, thirteen amplify (voting HHI greater than holding HHI) and five disperse. The amplification range runs from 2.5x (Gnosis) to 25.6x (Polkadot), with mean approximately 6.8x and median 4.4x. The thirteen-protocol core of the amplifying group includes DIMO, Lido, WeatherXM, Compound, Aave, Uniswap, Arbitrum, Optimism, and Drift; the five dispersers are ENS (0.48x), GMX (0.87x), Helium (0.26x to 0.39x), Jupiter (0.12x, the most-extreme outlier), and Livepeer (0.27x).

**Selected post-exclusion rows (illustrative; full table in the manuscript):**

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
| ENS | Infra | 0.046 | 0.022 | 0.48x | disperses (Section 4.5.1; mature delegate program) |
| Drift | DeFi | 0.026 | 0.083 | 3.1x | amplifies (Solana VSR; Section 4.5.4) |
| Helium | DePIN | 0.099 | 0.026 to 0.039 | 0.26x to 0.39x | DISPERSES (Solana VSR; Section 4.5.4) |
| Jupiter | DeFi | 0.045 | 0.0055 | 0.12x | DISPERSES (Solana delegated-vote; most-extreme outlier; Section 4.5.4) |

Solana rows use on-chain governance program parsing (Jupiter via Dune `jupiter_solana.govern_call_setvote` per-signer max-weight aggregation; Drift via Helius RPC parsing of SPL Governance VoteRecordV2 accounts and Helium via Helius RPC reconstruction of Voter Stake Registry position-state, both VSR-lockup-weighted). The Aave row reflects an all-delegates pull at N = 150,911; the four deeper-N sweeps validate the top-1000 methodology floor (all four sub-0.005 HHI shift versus the top-1000 baseline).

**Substantive interpretive consequence.** The flip is not a typo correction: it changes the Section 4.5 finding from the R1 "delegation amplifies unevenly, with two infrastructure protocols showing opposite patterns" to the revised predominant-amplification framing, in which thirteen of eighteen protocols amplify, with five structural exceptions documenting design-tractable dispersion. The Section 4.5 opening paragraph, sector-breakdown paragraph, Citizens' House and Dual Governance paragraphs, and the Fritsch et al. extension paragraph have all been rewritten. New subsections Section 4.5.1 (ENS counterexample), Section 4.5.1.1 (GMX counterexample), Section 4.5.4 (within-Solana governance heterogeneity), Section 4.5.4.1 (Drift Foundation proposal-authorship versus vote-weight decoupling), and Section 4.5.5 (cross-protocol institutional-governance-investor pattern as candidate fifth concentration axis) have been added. The abstract and the Section 6 conclusion are updated to the predominant-amplification framing.

**On Lido.** The reviewer's observation that Lido's ratio "appears lower" with the revised holding HHI is opposite to what our data produces. Applying PCA exclusion of the full set of Lido DAO addresses yields a Lido holding HHI of 0.008. The Snapshot voting pull, taken across all proposals in the analysis window (N = 333), yields voting HHI 0.050 and an amplification ratio of 6.3x. If the reviewer is computing a different Lido holding HHI from an alternative exclusion list (for example, one that does not exclude the Lido DAO Aragon treasury), we welcome specification of the methodology; the exclusion set is documented in Supplementary File S6 at address granularity.

**On the Uniswap counterexample.** The pre-correction Uniswap result (0.84x) had been cited as evidence that Uniswap's mature delegate program disperses governance power. With the burn-rule exclusion applied (the 0x000...000dead address holding 102.5M UNI, 11.3 percent of supply, structurally unable to participate in governance under any condition), Uniswap joins the predominant-amplification pattern at 2.7x. We document this transition explicitly in Section 4.5 because the prior result was load-bearing in the dispersion-via-mature-delegate-program literature; the corrected analysis reflects the cost of including a wallet that structurally cannot vote in the holding denominator.

**Compound Foundation as PCA at the voting layer.** Fact-checking of the Tally API surfaced a substantive methodological finding: the top COMP Tally delegate (21.5 percent of total delegated voting power in the May 2026 pull) is Compound Foundation itself, structurally a protocol-controlled entity. The PCA-symmetric voting-HHI robustness check (Section 4.6) extends the holding-side methodology to the voting layer: PCA exclusion is not monotonic in the concentration-reduction direction (see the GTC counterexample above), but predominant amplification holds for the deeper-N Tally sweep across AAVE, COMP, UNI, and ARB at sub-0.005 HHI shift versus the top-1000 baseline.

**Manuscript changes**: Delegation table rows fully recomputed; table caption updated with explicit post-exclusion methodology note; Section 4.5 opening through Fritsch-extension paragraphs rewritten; new Sections 4.5.1, 4.5.1.1, 4.5.4, 4.5.4.1, 4.5.5; Section 4.6 PCA-symmetric robustness paragraph added; Section 3.3 snapshot-date discipline paragraph added (documents the March 2026 to May 2026 delegate-pool drift; the revised manuscript uses the March 2026 snapshot consistent with the rest of the dataset for the protocols with March 2026 voting data; the GMX and ENS additions use May 2026 Tally per the delegation-table footnote); Figure 4 (delegation-adjusted bar chart) regenerated with the eighteen-protocol data; abstract, Section 1.1, and Section 5.6 updated to the predominant-amplification framing.

---

## Issue 2: Curve Top-10 column + CRV text disambiguation

### Reviewer comment (verbatim)

> In Table 4, Curve's HHI has been corrected to the post-exclusion raw-CRV value, but its Top-10 value is still the pre-exclusion one. The repository reports a substantially lower post-exclusion Top-10 value for Curve than the value shown in the table. In several places in the text, CRV is reported as HHI = 0.171, even though Table 4 now reports raw CRV, with HHI = 0.017. If this is supposed to be about veCRV, please mention it explicitly in the text.

### Response

The reviewer is correct on both points. Table 4 Curve Top-10 percentage has been corrected from 60.7 percent (pre-Convex-exclusion) to the post-exclusion value matching the regression dataset. The CRV-versus-veCRV disambiguation has been implemented across all textual surfaces, with the 0.171 proxy replaced by a directly computed veCRV voting concentration value (0.26).

**Direct veCRV voting concentration computation.** The R1 manuscript used 0.171 as a proxy for veCRV-weighted voting concentration. The 0.171 figure is the raw CRV holding HHI including the Convex veCRV custody position (which holds substantial CRV that has been locked into veCRV). The revised paper computes the actual veCRV-weighted voting concentration directly via Dune analysis of the Curve VotingEscrow Deposit events at 0x5f3b5dfeb7b28cdbd7faba78963ee202a494e2a2. Aggregating cumulative CRV deposits across the top-50 historical veCRV lockers yields HHI 0.26: Convex CRV Locker at 48.0 percent of top-50 deposit-weighted share; Yearn yveCRV at 13.5 percent; Stake DAO sdCRV at 9.5 percent; the remaining 47 lockers each less than 4 percent. The 0.26 direct computation captures the actual gauge-weight voting concentration that veCRV produces and is substantively higher than the 0.171 proxy.

**Disambiguation applied at every textual surface.**

- Table 3 row: HHI = 0.014 (raw post-Convex-exclusion CRV holdings); Top-10 percent = 31.2 (post-exclusion).
- Table 3 caption: HHI for Curve reflects raw CRV holdings after excluding the Convex veCRV custody position; veCRV-weighted voting concentration is approximately 0.26 computed from cumulative CRV deposit volume across the top-50 historical veCRV lockers; methodology discussed in Section 4.5.2.
- Section 4.2 cross-protocol range description: CRV's raw 0.014 places it mid-range; the 0.26 veCRV voting concentration is referenced with explicit methodology cite to Section 4.5.2.
- Section 4.5.2 (vote-escrowed governance subsection; new in R2): Both Curve veCRV (15x amplification relative to raw 0.014) and Balancer veBAL (21x amplification at voting HHI 0.626 against holding 0.030) documented as a distinct extreme-amplification mechanism class separate from delegate-program-based amplification.

The Aethir Table 3 row was also updated. The R1 footnote value reflected an earlier snapshot; the revised direct Dune pull yields HHI 0.095 post-PCA-exclusion (the 0xfc78 Safe multisig was identified as an additional PCA). Both reflect raw top-1000 holder concentration after PCA exclusion; the difference between the earlier and the direct pulls is documented in Supplementary File S6.

**Manuscript changes**: Table 3 CRV row corrected; Table 3 methodology notes updated with explicit veCRV decomposition (Convex 48 percent, Yearn 14 percent, Stake DAO 9 percent); new Section 4.5.2 "Secondary extension: vote-escrowed governance" documenting both Curve and Balancer ve-token amplification; Supplementary File S6 (address-by-address PCA documentation) updated with the Aethir 0xfc78 entry; a supplementary exhibit reporting the veCRV voting-concentration computation ships with the supplementary materials.

---

## Issue 3: Table 5 N = 40 and TT-expanded subsidy reproducibility

### Reviewer comment (verbatim)

> First, the HHI-Gini row reports N = 40, but the current data seem to contain missing Gini values for some protocols. Second, the TT-expanded subsidy analysis is still not straightforwardly reproducible from the repository files. The CSV contains fewer observations than the N reported in the manuscript. In addition, the conclusions drawn appear to be based on the old numbers.

### Response

The reviewer is correct on both sub-issues. Both have been addressed.

**HHI-Gini row N = 40.** Three DePIN protocols (Aethir, Hivemapper, io.net) appeared in the R1 Table 4 footnote with HHI values but were noted as lacking the holder-level Gini and percentile data required for Table 4 reporting. The R1 manuscript inconsistently reported N = 40 for the HHI-Gini correlation despite this gap. The revised paper resolves the gap by pulling full holder-level data for all three:

- Hivemapper (HONEY; Solana SPL): pulled via Helius DAS API (90,680 unique holders). HHI 0.018, Gini 0.91, Top-1 percent 5.7, Top-10 percent 31.1. Added as a full Table 3 row.
- io.net (IO; Solana SPL): pulled via Helius DAS API (84,861 unique holders). HHI 0.125, Gini 0.94, Top-1 percent 33.5, Top-10 percent 61.2. Added as a full Table 3 row.
- Aethir (ATH; Ethereum ERC-20): pulled via Dune top-1008 with eight PCA exclusions. HHI 0.095, Gini 0.94, Top-1 percent 19.7, Top-10 percent 67.6. Added as a full Table 3 row.

All three protocols now appear as full cross-section rows (Table 3) with complete holder-level data. The revised manuscript reports the HHI-Gini correlation on the N = 48 post-exclusion comparable cohort, the frame for which holder-level Gini is directly comparable (Pearson r = 0.52, p < 0.001; Table 4 and Supplementary File S0); the comparable cohort grew from 40 to 48 as the cross-section reached its final 52-protocol frame.

**TT-expanded subsidy CSV reproducibility.** The reviewer correctly identifies that the R1 manuscript's reported N for the TT-expanded subsidy test does not match the row count of subsidy-ratio-populated observations in the underlying CSV. In the revised paper the subsidy battery is reported on a single regression dataset: the dataset contains 20 protocols with non-null Token Terminal subsidy data, while the headline subsidy battery uses N = 23 protocols with non-zero subsidy under either Token Terminal or on-chain metrics (and N = 22 when Livepeer is excluded). The revised values are:

- Table 5 "Subsidy ratio (cross-sector)" row: Pearson r = 0.62, p = 0.002, N = 23. Fragile (Livepeer-driven).
- Table 5 "Subsidy ratio (TT expanded)" row: Pearson r = 0.12, p = 0.61, N = 20. Null (robustness check).
- Table 5 "Subsidy ratio (excluding Livepeer)" row: Pearson r = 0.07, p = 0.76, N = 22. Null.
- Spearman rank correlation on the full subsidy sample: rho = 0.26, p = 0.23.
- Section 4.6 Robustness paragraph: the headline subsidy correlation is entirely Livepeer-driven (Livepeer subsidy ratio of 88.5x is a 3.5-sigma outlier on the subsidy axis); excluding Livepeer alone reduces the Pearson correlation to a clean null (r = 0.07).

**Sample-size robustness of the subsidy fragility.** Because the apparent association is carried by a single high-leverage observation, a natural question is whether a larger subsidy sample would resolve it rather than confirm it. Relaxing the non-zero-subsidy filter to include the twelve protocols with a genuine measured zero subsidy (revenue present, token incentives equal to zero: mature, buyback-only, or no-fee-accrual tokens, for which a zero is a substantive economic observation rather than a missing value) yields N = 35. The Livepeer-inclusive Pearson correlation is essentially unchanged at r = 0.61 (p = 0.0001), and excluding Livepeer it again collapses to a clean null at r = 0.09 (p = 0.61, N = 34); the outlier-robust Spearman correlation is non-significant at both sample sizes even with Livepeer retained (rho = 0.26 at N = 23, rho = 0.09 at N = 35). Adding twelve protocols, a 52 percent increase in the sample, moves the Livepeer-inclusive coefficient by only 0.01 and leaves the Livepeer-excluded association null, so the larger cross-section confirms rather than rescues the fragility (Section 4.6).

A new multivariate specification (Section 4.6) with both subsidy ratio and DePIN sector indicator on the 23-protocol non-zero-subsidy sample (HC3 robust standard errors) reinforces the Livepeer-driven interpretation: with all 23 protocols, the DePIN sector indicator is significant (p = 0.030) while subsidy is not (p = 0.36; Adj R-squared = 0.49); excluding Livepeer, the subsidy coefficient is strongly non-significant (p = 0.93) while the DePIN sector indicator is significant (p = 0.004).

**On-chain operating-cost subsidy methodology.** A focused investigation against the raw on-chain operating-cost computations for the burn-active panel surfaced four methodology refinements grounded in project-Foundation primary sources (DIMO, Morpheus AI, Filecoin, Helium). Material reclassifications: DIMO moves from the net-deflationary subset to the subsidy-heavy subset (an earlier burn-to-dead aggregation diverged from the DIMO Foundation's revenue methodology by 13.8x token count); Morpheus AI moves from net-deflationary to subsidy-heavy (an earlier filter captured cross-chain bridge flows rather than protocol revenue and emissions); Filecoin subsidy ratio refined to 46.05 (Token Terminal emissions undercount of 140 percent due to a vesting-discount filter; cross-validated against Spacescope, Tokenomist, and the Coinbase Institutional Tokenomics Review primary sources within 1.8 percent). A verification pass against the remaining thirteen panel protocols produced zero additional methodology shifts. The cross-protocol pattern is structurally informative: the four protocols requiring methodology refinement are all DePIN-class; the eleven non-DePIN protocols (DeFi blue chips, mid-cap DeFi, L2 / L1 infrastructure) passed direct verification with no methodology shifts. This is offered as a candidate methodology contribution; the structural difference between newer DePIN protocols (cross-chain bridging, custom reward distribution mechanisms) and mature non-DePIN protocols (community-aggregator alignment, methodologically stable Foundation reporting) may motivate further work in subsequent B-series papers.

**Manuscript changes**: Table 5 rows updated to current values; the cross-section (Table 3) reaches its final N = 52 frame, with Hivemapper, io.net, and Aethir among the full rows; Section 4.6 subsidy-multivariate paragraph documenting the four specifications; Supplementary File S6 documents the on-chain operating-cost methodology per protocol; Supplementary File S8 documents the Token Terminal expansion battery; Section 4.6 reports the N = 35 sample-size-robustness extension that relaxes the non-zero-subsidy filter and shows the fragility persists at the larger sample.

---

## Issue 4: Figure-vs-text statistical drift (Figures 2, 3, others)

### Reviewer comment (verbatim, key points)

> Figure 4 visually reports Mann-Whitney p = 0.016, Cohen's d = 0.96, DeFi mean = 0.043, and DePIN mean = 0.090. However, the caption and revised text report p = 0.014, d = 1.03, DeFi mean = 0.041, and DePIN mean = 0.091. Figure 5 has title reporting r = 0.19, p = 0.25, while the caption and abstract report r = 0.18, p = 0.28. The same goes for other figures, too. My general suggestion is to reproduce all the tables and figures, and make the text reflect the current data.

### Response

The reviewer is correct on the specific figures and on the general methodology suggestion. The revised paper adopts a "reproduce all tables and figures from one regression dataset" discipline. All main-text figures have been regenerated from the regression dataset and the visual statistics now match caption and body-text values exactly.

The figures in the revised manuscript are renumbered relative to R1. The R1 figure numbering (3, 4, 5, 6, 7, 8) reflected an earlier iteration that included two theory figures (philosophical-framework architecture; conceptual model) at positions 1 and 2; those theory figures were removed during the empirical reframe and the remaining figures were renumbered (with a supplementary 2b panel for the three-class sector contrast), and a multi-year voting-HHI trajectory robustness exhibit was added in this revision (Figure 5, below). The revised manuscript carries seven numbered figures; they are:

- **Figure 1** (HHI bar chart across 52 governance tokens; was R1 Figure 3): Holding HHI ranges 0.005 (Hyperliquid) to 0.199 (Livepeer); the DePIN cluster in the upper half is visible.
- **Figure 2** (DePIN versus DeFi sector boxplot; was R1 Figure 4): the figure displays the of-record post-exclusion HHI distribution by sector (DePIN mean 0.067 versus DeFi 0.026, N = 15 / 15) and reports the headline sector test under the voter-inclusive staking pass-through treatment (Mann-Whitney p = 0.028, Cohen's d = 0.65), with the uniform staking-aggregation exclusion noted as the robustness check (Cohen's d = 0.75); visual and caption stats match. The figure-versus-caption drift the reviewer identified for this figure is resolved: the revised figure and caption are reconciled to the pass-through headline.
- **Figure 2b** (three-class sector boxplot; new): DePIN versus DeFi versus L1/infrastructure across the N = 44 governance-token frame (Kruskal-Wallis), confirming the sector effect generalizes beyond the balanced 15/15 contrast.
- **Figure 3** (insider allocation scatter; was R1 Figure 5): the figure plots the original insider-allocation cohort (Pearson r = 0.07, p = 0.68, N = 37) and the caption notes that the null holds on the current N = 50 frame at r = 0.09, p = 0.55. The figure-versus-caption drift the reviewer identified is resolved; the revised figure and caption both report r = 0.07 / p = 0.68 / N = 37 for the cohort scatter. The lead allocation null is the current-frame result (r = 0.09, p = 0.55, N = 50), reported in the abstract and Section 4.4.
- **Figure 4** (delegation-adjusted bar chart; replaces R1 Figure 6): eighteen-protocol delegation amplification chart (thirteen amplify, five disperse) with ratios annotated; visual and caption stats reflect the eighteen-protocol voting-HHI sample.
- **Figure 5** (multi-year voting-HHI trajectories; new robustness exhibit): per-period voting HHI (log scale) for the three protocols with a true per-period governance series (Algorand across fifteen governance periods, GEODNET across nine GIPs, Helium across its proposal history), showing that voting concentration is stable across multi-year windows of normal participation; the two annotated late-period excursions (the Algorand GP15 uptick after the post-GP14 end of rewards-eligible commitment, and the Helium post-HIP-141 turnout collapse from the 200-to-1,024-voter range to 5-to-10 voters) are low-turnout artifacts rather than concentration drift. Reproducible one-command from committed series files.
- **Figure 6** (leave-one-out sector-contrast forest; new): computed under the uniform staking-aggregation exclusion (the robustness-check treatment, Cohen's d = 0.75); all 30 leave-one-out iterations remain significant (per-iteration p range 0.006 to 0.031) and the Cohen's d point estimates span 0.68 to 0.92.
- **Figure 7** (subsidy ratio scatter; was R1 Figure 7): Pearson r = 0.62 inclusive of Livepeer, r = 0.07 excluding Livepeer; N = 23; visual and caption stats match.

**Reproducibility commitment.** Per the reviewer's general suggestion and to prevent recurrence, the revised paper regenerates every body-text statistic, table, and figure from a single regression dataset (shipped as Supplementary File S5) and ships a statistics ledger (Supplementary File S0; new in R2) listing every body-text statistic with its sample size and reporting convention, providing one source of truth for body, tables, figures, captions, abstract, and conclusion.

**Manuscript changes**: All main-text figures regenerated from the regression dataset; Supplementary File S5 documents the empirical pipeline and figure-regeneration discipline; the regression dataset CSV ships with the replication materials; the statistics ledger ships as Supplementary File S0.

---

## Changes beyond the four issues

The revision includes substantial strengthening beyond Reviewer 1's four issues, spanning data, methodology, and manuscript architecture. To avoid duplicating the cover letter, the narrative of these changes lives there (the four empirical contributions, the zero-new-data robustness layer, the empirical-paper reframe, the reference additions, and the single-source-of-truth methodology discipline); we do not re-narrate them here. For the reviewer's navigation, the additional changes and their locations in the revised manuscript are:

- Predominant-amplification thesis with five structural exceptions (Section 4.5): thirteen of eighteen protocols amplify (range 2.5x to 25.6x), a substantive interpretive change produced by resolving Issue 1.
- Within-Solana governance heterogeneity (Section 4.5.4) and the Drift Foundation proposal-authorship versus vote-weight decoupling (Section 4.5.4.1).
- Cross-protocol institutional-governance-investor pattern as a candidate fifth concentration axis (Section 4.5.5).
- Insider classification re-derived from primary on-chain evidence rather than keyword-coded, robust across six independent classification schemes (Sections 3.4, 4.6.4; Supplementary File S22).
- Staking-attribution recovery of a hidden insider share (Section 4.4) and the Livepeer orchestrator-level governance dispersion result (Section 4.5).
- Multivariate sector coefficient significant under both the raw and the log measures (Sections 4.4, 4.6.4).
- Profitability, size, and insider-retention secondary checks (Section 4.6).
- Five falsifiable forward predictions with pre-registration intent (Section 5.8; Supplementary File S17).
- Longitudinal panel evidence and full-history voting robustness (Supplementary Files S7 and S23; Table 6b; Figure 5).
- Data-availability and reproducibility statement (Section 5.9).

---

## Acknowledgments

We thank Reviewer 1 for the comprehensive cross-surface audit that surfaced the manuscript-versus-data drift in R1 Round 2 and motivated the R2 reproduce-and-sync discipline. The revised manuscript's predominant-amplification finding with structural exceptions (Section 4.5; abstract finding 4) is a direct product of Reviewer 1's framing: applying consistent post-exclusion methodology across Table 4 and the delegation table produced a substantive interpretive change. The broader strengthening of the voting layer (proper-weight Snapshot, Tally, and Solana on-chain governance parsing), the on-chain operating-cost subsidy methodology, and the empirical-paper reframe all extend from the reviewer's general "reproduce all tables and figures and make the text reflect the current data" recommendation. We thank Reviewer 2 for the endorsement of publication.
