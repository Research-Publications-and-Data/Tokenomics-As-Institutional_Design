# Cover letter: B2 R2 submission

**To:** Editorial Office, Frontiers in Blockchain
**From:** Zach Zukowski (Tokenization Systems; zach@tokenization.systems)
**Re:** Governance Concentration Beyond Token Allocation: A 52-Protocol Cross-Sectional Audit of DePIN and DeFi After Protocol-Controlled-Address Exclusion (Manuscript ID 1853465; SSRN 6599278)
**Working title (5 words):** Governance Concentration Beyond Token Allocation
**Title note:** The full title revises the R1 submission title "Governance Concentration Beyond Token Allocation: An Institutional Design Analysis of DePIN and DeFi" by preserving the lead phrase exactly and reframing the subtitle from theory-framing ("An Institutional Design Analysis") to empirical-audit framing ("A 52-Protocol Cross-Sectional Audit ... After Protocol-Controlled-Address Exclusion"). The R1 lead-phrase preservation is deliberate: it provides editorial-system continuity (the working title matches the R1 lead phrase exactly), while the new subtitle signals the reframing toward the empirical-measurement contribution. The institutional-design-and-philosophical-interpretation thread has been moved to a companion paper (Zukowski, 2026e), allowing the title and abstract to lead directly with the audit contribution.
**Date:** 2026-05-31
**Round:** R2 revision

---

Dear Editor and Reviewers,

I am submitting the R2 revision of "Governance Concentration Beyond Token Allocation: A 52-Protocol Cross-Sectional Audit of DePIN and DeFi After Protocol-Controlled-Address Exclusion" addressing Reviewer 1's four Round 2 issues and incorporating substantial strengthening across data, methodology, and manuscript architecture. Point-by-point responses to all four reviewer issues are documented in the accompanying response document (`2026-05-26_R2_responses_master.md`), which is structured for direct copy-paste into the Frontiers reviewer-response web form.

## Manuscript identity change since R1

The manuscript has been reframed around its empirical-measurement contribution. The R1 manuscript developed a five-lens philosophical framework integrated with empirical results; the revised manuscript leads with the measurement contributions and routes the philosophical-interpretation thread to a companion paper. This reframing preserves every R1 statistical finding. What is different is the architecture: empirical contributions are now the spine, with normative interpretation moved to a companion paper that develops the Polanyian fourth-fictitious-commodity argument at the depth that thesis warrants.

The revised manuscript reports four empirical contributions (Section 5.6):

1. **Generalizable PCA exclusion methodology** (Section 3.8) - 133 protocol-controlled-address exclusions across 38 protocols correcting systematic HHI inflation in prior holder-list studies (median inflation factor 2.3x; maximum approximately 18x at RENDER). The five-class typology (burn-destination; foundation/treasury custody; staking-aggregation contracts; bridge custody and migration addresses; centralized exchange custody) generalizes to any cross-protocol governance HHI analysis on ERC-20 or SPL token holders.

2. **Allocation-null with insider-retention contrast** (Section 4.4) - Initial team-and-investor allocation does not explain post-distribution concentration in the 37-protocol allocation subsample (Pearson r = 0.05, p = 0.76); current insider wallet presence among top-10 holders is associated with concentration (Spearman rho = 0.48, p = 0.003, N = 37; the count-based non-insider HHI tautology check at rho = 0.54, p = 0.001, N = 34 supports this as more than an arithmetic artifact).

3. **Corrected sector contrast** (Section 4.3) - DePIN governance concentration exceeds DeFi after PCA correction (Mann-Whitney p = 0.020, Cohen's d = 0.94, N = 15/15; robust in 30/30 leave-one-out iterations; permutation test p = 0.012; bootstrap 95% percentile interval on mean difference [+0.012, +0.069]).

4. **Predominant delegation amplification with five structural exceptions** (Section 4.5) - Voting-HHI exceeds post-exclusion holding HHI in thirteen of eighteen protocols with sufficient governance data (range 1.6x DRIFT to 25.6x Polkadot; mean approximately 6.8x, median 4.4x). Five protocols disperse voting power below the holding baseline (ENS at 0.45x; GMX at 0.87x; HNT at 0.35x to 0.53x; JUP at 0.057x, the most-extreme dispersion outlier in the cross-section; and LPT at 0.27x, the most pronounced DePIN governance disperser, with Livepeer holding concentration unchanged at the cross-section maximum). Curve veCRV, Balancer veBAL, and Frax veFXS form a separate vote-escrowed class with extreme amplification (15x, 21x, and 11.4x respectively).

## Submission package contents

- **Revised manuscript (clean version)** - the full R2 manuscript incorporating all changes described in the response document
- **2026-05-26_R2_responses_master.md** - Point-by-point response to Reviewer 1's R2 issues (markdown source for direct copy-paste into the Frontiers reviewer-response web form)
- **This cover letter** (PDF and DOCX)
- **Supplementary files**: S0 (statistics ledger); S1 (metric definitions); S2-S3 (codebook plus optional governance-scoring instruments retained as supplementary, not load-bearing for the empirical analysis); S4 (events table); S5 (empirical pipeline specification including per-iteration LOO data and per-protocol participation values); S6 (source provenance and revenue standardization); S7 (quarterly HHI panel for 14 governance tokens across 8 quarters); S8 (Token Terminal subsidy expansion analysis with sector-control multivariate models); S9 (Theil and Atkinson concentration-metric robustness check); S10 (PCA classification robustness across Specs A through E); S11 (Shapley-Shubik and Banzhaf power-index calculations); S12 (PCA-symmetric voting-HHI and signer-side functional PCA cases); S13 (Solana PCA exclusion audit including cross-protocol candidate-address verification); S14 (Shapley-Shubik and Banzhaf power-index full closure across the N=16 cross-source voting sample); S15 (voting-HHI coverage across the N=52 cross-section); S16a (Aethir, IoTeX, and ENS sensitivity analyses); S16b (additional protocols: FXS, SNX, GNO, TAO); S16c (Polkadot governance analysis); S17 (falsifiable predictions and pre-registration specification); S18 (EVM PCA classification with two-layer audit); S19 (Polkadot validator-set five-axis attribution methodology); S20 (Polkadot Subscan delegate-pool analysis); S21 (Class 3 versus Class 5 PCA disambiguation via transaction-pattern signatures); S22 (insider classification and staking-attribution audit); S23 (Q1-to-Q8 governance-HHI trajectory analysis on the 14-protocol panel); S24 (Optimism worked example); S25 (cross-protocol institutional concentration: voter-axis institutional-delegate audit plus holder-axis and validator-set CEX-overlap synthesis)

The address-by-address PCA exclusion log and the full regression dataset are available at the linked GitHub replication repository.

## Methodology disclosure

The revision reconciles all reported statistics against a single source-of-truth regression dataset to prevent recurrence of the manuscript-vs-data drift Reviewer 1 surfaced in the R1 review. A statistics ledger (Supplementary File S0) lists every body-text statistic with its sample size and the reporting convention; the ledger is the single source of truth that body, tables, figures, captions, abstract, and conclusion reconcile against, and all reported statistics are reconciled against it. Snapshot-date discipline is acknowledged: Table 7 voting-HHI values for the eight protocols sampled at the R1 scope use a March 2026 snapshot consistent with the rest of the dataset; the GMX and ENS additions use a May 2026 Tally snapshot (documented in Section 4.5 Table 7 footnote as a deliberate methodological exception for the added protocols). The May 2026 Tally and Snapshot replication confirms delegate-pool drift; rank ordering across protocols is the more durable inferential property than absolute magnitude.

## Conflict of interest

The author served as Senior Investment Analyst at Borderless Capital, a cryptocurrency-focused investment firm, through February 2026 and retains no decision-making role, carried interest, or position-dependent compensation with the firm. The author may hold small personal positions in some of the protocols analyzed; positions were established outside the research period and are not position-dependent on Borderless Capital. A complete disclosure is provided in the Conflict of Interest statement accompanying this submission. No co-authors or other conflicts of interest.

## Acknowledgment

We thank Reviewer 1 for the comprehensive cross-surface audit in R1 that surfaced the manuscript-vs-data drift class and motivated the reproduce-and-sync discipline adopted in this revision. Responding to that audit directly produced the substantive thesis evolution in the revised manuscript: the headline finding moved from "delegation amplifies unevenly with two infrastructure protocols showing opposite patterns" to "predominant amplification across thirteen of eighteen protocols with five structural exceptions documenting design-tractable dispersion." The revised manuscript's empirical contributions are stronger than the R1 manuscript's because the reviewer's audit framing was applied throughout the data, methodology, and architecture. We thank Reviewer 2 for the endorsement of publication.

Sincerely,
Zach Zukowski
Tokenization Systems
zach@tokenization.systems
ORCID: 0009-0006-3642-2450
