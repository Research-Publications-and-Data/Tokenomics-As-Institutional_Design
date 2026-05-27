# Cover letter: B2 R2 submission

**To:** Editorial Office, Frontiers in Blockchain
**From:** Zach Zukowski (Tokenization Systems; zach@tokenization.systems)
**Re:** Governance Concentration Beyond Token Allocation: A 40-Protocol Cross-Sectional Audit of DePIN and DeFi After Protocol-Controlled-Address Exclusion (Manuscript ID 1853465; SSRN 6599278)
**Working title (5 words):** Governance Concentration Beyond Token Allocation
**Title note:** The full title revises the R1 submission title "Governance Concentration Beyond Token Allocation: An Institutional Design Analysis of DePIN and DeFi" by preserving the lead phrase exactly and reframing the subtitle from theory-framing ("An Institutional Design Analysis") to empirical-audit framing ("A 40-Protocol Cross-Sectional Audit ... After Protocol-Controlled-Address Exclusion"). The R1 lead-phrase preservation is deliberate: it provides editorial-system continuity (the working title matches the R1 lead phrase exactly), while the new subtitle signals the R2 reframing toward the empirical-measurement contribution. The institutional-design-and-philosophical-interpretation thread has been moved to a companion paper (Zukowski, 2026e), allowing the R2 title and abstract to lead directly with the audit contribution.
**Date:** 2026-05-26
**Round:** R2 revision

---

Dear Editor and Reviewers,

I am submitting the R2 revision of "Governance Concentration Beyond Token Allocation: A 40-Protocol Cross-Sectional Audit of DePIN and DeFi After Protocol-Controlled-Address Exclusion" addressing Reviewer 1's four Round 2 issues and incorporating substantial post-R1 strengthening across data, methodology, and manuscript architecture. Point-by-point responses to all four reviewer issues, plus a narrative of the post-R1 cycles that further refined the manuscript, are documented in the accompanying response document (`2026-05-26_R2_responses_master.md`), which is structured for direct copy-paste into the Frontiers reviewer-response web form.

This R2 submission supersedes the 2026-05-17 R2 draft prepared after the initial R1 response cycle. The 2026-05-17 draft is preserved as an audit-trail artifact; the present 2026-05-26 submission reflects the post-2026-05-17 strengthening cycles (deep PCA audit; voting-HHI methodology refresh; multi-source PCA-symmetric extension; raw-OC subsidy refinement; historical burn empirical refresh) plus an empirical-paper reframe completed during a final polish cycle.

## Manuscript identity change since R1

The manuscript has been reframed around its empirical-measurement contribution. The R1 manuscript developed a five-lens philosophical-framework integrated with empirical results; the R2 manuscript leads with the measurement contributions and routes the philosophical-interpretation thread to a companion paper. This reframing preserves every R1 statistical finding. What is different is the architecture: empirical contributions are now the spine, with normative interpretation moved to a companion paper that develops the Polanyian fourth-fictitious-commodity argument at the depth that thesis warrants.

The R2 manuscript reports four empirical contributions (Section 5.6):

1. **Generalizable PCA exclusion methodology** (Section 3.8) - 133 protocol-controlled-address exclusions across 38 protocols correcting systematic HHI inflation in prior holder-list studies (median inflation factor 2.3x; maximum approximately 18x at RENDER). The five-class typology (burn-destination; foundation/treasury custody; staking-aggregation contracts; bridge custody and migration addresses; centralized exchange custody) generalizes to any cross-protocol governance HHI analysis on ERC-20 or SPL token holders.

2. **Allocation-null with insider-retention contrast** (Section 4.4) - Initial team-and-investor allocation does not explain post-distribution concentration in the 37-protocol allocation subsample (Pearson r = 0.05, p = 0.76); current insider wallet presence among top-10 holders is associated with concentration (Spearman rho = 0.48, p = 0.003, N = 37; the count-based non-insider HHI tautology check at rho = 0.54, p = 0.001, N = 34 supports this as more than an arithmetic artifact).

3. **Corrected sector contrast** (Section 4.3) - DePIN governance concentration exceeds DeFi after PCA correction (Mann-Whitney p = 0.020, Cohen's d = 0.94, N = 15/15; robust in 30/30 leave-one-out iterations; permutation test p = 0.012; bootstrap 95% percentile interval on mean difference [+0.012, +0.069]).

4. **Predominant delegation amplification with four structural exceptions** (Section 4.5) - Voting-HHI exceeds post-exclusion holding HHI in nine of thirteen protocols with sufficient governance data (range 1.6x DRIFT to 9.9x Compound; mean approximately 4.9x). Four protocols disperse voting power below the holding baseline (ENS at 0.45x; GMX at 0.87x; HNT at 0.35x to 0.53x; JUP at 0.057x, the most-extreme dispersion outlier in the cross-section). Curve veCRV and Balancer veBAL form a separate vote-escrowed class with extreme amplification (15x and 21x respectively).

## Submission package contents

- **B2_Post_Polish_Cycle_2026-05-26_clean.docx** - Revised manuscript (clean version; DOCX-only build target with pre-publication conversion handled by Frontiers production pipeline)
- **2026-05-26_R2_responses_master.md** - Point-by-point response to Reviewer 1's R2 issues plus the post-R1 strengthening narrative (markdown source for direct copy-paste into the Frontiers reviewer-response web form)
- **This cover letter** (PDF and DOCX)
- **Supplementary files**: S0 (canonical statistics ledger; new); S1 (metric definitions); S2-S3 (codebook plus optional governance-scoring instruments retained as supplementary, not load-bearing for the empirical analysis); S4 (events table); S5 (empirical pipeline specification including per-iteration LOO data and per-protocol participation values); S6 (source provenance, revenue standardization, address-by-address PCA exclusion documentation); S7 (quarterly HHI panel for 14 governance tokens across 8 quarters); S8 (Token Terminal subsidy expansion analysis with sector-control multivariate models); S9 (Theil and Atkinson concentration metrics robustness check); S10 (PCA classification robustness across Specs A through E); S11 (Shapley-Shubik and Banzhaf power-index calculations); S12 (PCA-symmetric voting-HHI and signer-side functional PCA cases); S15 (Optimism worked example); S16 (Aethir, IoTeX, and ENS sensitivity analyses); S17 (falsifiable predictions and pre-registration specification)

S13 and S14 are not in the R2 package: the prior placeholders for reserved or externally hosted replication artifacts did not point to concrete content, and have been removed from the supplement list to avoid orphan references. Replication code and the full canonical regression dataset continue to be available at the linked GitHub repository.

## Methodology disclosure

The R2 cycle adopted a single-canonical-regression-dataset-of-record discipline to prevent recurrence of the manuscript-vs-data drift Reviewer 1 surfaced in the R1 review. A canonical statistics ledger (Supplementary File S0) lists every body-text statistic with its sample size and the reporting convention; the ledger is the single source of truth that body, tables, figures, captions, abstract, and conclusion reconcile against. Snapshot-date discipline is acknowledged: Table 7 voting-HHI values for the eight protocols sampled at the R1 scope use a March 2026 snapshot consistent with the rest of the dataset; the GMX and ENS additions from the post-R1 sample-expansion cycle use a May 2026 Tally snapshot (documented in Section 4.5 Table 7 footnote as a deliberate methodological exception for sample-expansion protocols). The May 2026 Tally and Snapshot replication confirms delegate-pool drift; rank ordering across protocols is the more durable inferential property than absolute magnitude.

The S0 ledger plus submission-readiness validation tooling (`tools/content-build/submission_readiness_check.py` + `reviewer_trap_lint.py`) reduce the surface area where caption-versus-text drift can recur. These tools verify figure-path existence, supplement-reference resolution, output_formats template existence, current_version coherence in METADATA, build-warning-free invocation, figure-caption numbering coherence, and prose-side lint for causal-overclaim language and pandoc residue.

## Conflict of interest

The author served as Senior Investment Analyst at Borderless Capital, a cryptocurrency-focused investment firm, through February 2026 and retains no decision-making role, carried interest, or position-dependent compensation with the firm. The author may hold small personal positions in some of the protocols analyzed; positions were established outside the research period and are not position-dependent on Borderless Capital. A complete disclosure is provided in the Conflict of Interest statement accompanying this submission. No co-authors or other conflicts of interest.

## Acknowledgment

We thank Reviewer 1 for the comprehensive cross-surface audit in R1 that surfaced the manuscript-vs-data drift class and motivated the R2 reproduce-and-sync discipline. The reproduce-and-sync framing in turn enabled the post-R1 strengthening cycles (deep PCA audit; voting-HHI methodology refresh; multi-source PCA-symmetric extension across Tally, Snapshot, and Solana on-chain governance program parsing) that produced the substantive R2 thesis evolution: the headline finding moved from "delegation amplifies unevenly with two infrastructure protocols showing opposite patterns" to "predominant amplification across nine of thirteen protocols with four structural exceptions documenting design-tractable dispersion." The R2 manuscript's empirical contributions are stronger than the R1 manuscript's because the reviewer's audit framing was applied at saturation depth. We thank Reviewer 2 for the endorsement of publication.

Sincerely,
Zach Zukowski
Tokenization Systems
zach@tokenization.systems
ORCID: 0009-0006-3642-2450
