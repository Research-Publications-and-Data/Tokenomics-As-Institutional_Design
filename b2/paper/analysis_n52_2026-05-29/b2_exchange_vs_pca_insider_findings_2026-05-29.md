# Exchange-held supply and the PCA-vs-insider distinction: findings

**As-of:** 2026-05-29. Reproduce with `python3 b2_exchange_vs_pca_insider_2026-05-29.py`
(reads persisted data; no /tmp, no live-API). Results JSON:
`b2_exchange_vs_pca_insider_results_2026-05-29.json`. N = 50 protocols (DePIN/DeFi/L1 with a
raw holder list + exclusion records). Correlational, exploratory; outcome = log post-exclusion
holding HHI. Reader MUST re-verify against live canonical state before acting.

## Q1. Exchange-held supply does NOT predict governance concentration

| relationship | Pearson r | p |
|---|---:|---:|
| exchange-held % to log post-exclusion HHI | -0.196 | 0.17 |
| exchange-held % to raw post-exclusion HHI | -0.077 | 0.59 |
| exchange-held % to pre-exclusion top-10 share | -0.205 | 0.15 |
| regression log-HHI ~ sector + exchange% (exchange coefficient) | -1.61 | 0.28 |

Exchange-held supply is a small bucket (mean approximately 4.8% of the top-1000) and is, if
anything, weakly NEGATIVELY associated with concentration, but not significantly. In the
sector-controlled regression the exchange coefficient is not significant and DePIN remains
significant (p = 0.030). Descriptively, the most-concentrated sector (DePIN) has the LOWEST
exchange-held share (3.5%) versus DeFi (5.1%) and L1 (6.1%). Exchange custody behaves as a
liquid-float indicator, orthogonal to (mildly opposed to) deep governance concentration. This
is a third confirmation of the paper's thesis that surface supply-distribution metrics (launch
allocation %, exchange %) do not predict the deep concentration, whereas sector does.

## Q2. PCA and insider are NOT interchangeable; the concentration signal lives in their overlap

The five-class PCA exclusion (burns, foundation/treasury, staking, bridges, CEX) overlaps the
insider bucket (team, founder, investor, foundation, treasury, multisig) ONLY in
foundation/treasury. Decomposing the excluded supply by bucket and correlating each with
log post-exclusion HHI:

| bucket | PCA? | insider? | Pearson r | p | mean share |
|---|:--:|:--:|---:|---:|---:|
| foundation/team % | yes | yes | +0.313 | 0.027 | 0.212 |
| CEX % | yes | no | -0.196 | 0.17 | 0.048 |
| bridge % | yes | no | -0.025 | 0.86 | 0.034 |
| staking % | yes | no | +0.092 | 0.52 | 0.042 |
| total PCA-excluded % | yes | mixed | +0.401 | 0.004 | 0.420 |
| insider_pct ALLOCATION | no | yes (launch %) | +0.233 | 0.10 | 35.3 |

The predictive power of total-PCA-excluded share comes from its foundation/team
(insider-overlapping) component. The pure-infrastructure PCA buckets (CEX, bridge, staking)
are flat or negative.

**Substantive, not a renormalization artifact.** Excluding a large chunk mechanically inflates
the renormalized HHI, so a positive excluded-share to post-exclusion-HHI link could be
mechanical. It is not, for foundation/team: that bucket also tracks PRE-exclusion concentration
(r = +0.30 vs raw top-10 share, p = 0.035), whereas CEX does not (r = -0.21, n.s.); and in a
partial regression the foundation/team share stays significant controlling for all other
excluded share (b = +1.66, p = 0.011; other-excluded b = +1.12, p = 0.082).

## Synthesis (paper-relevant)

A clean three-way contrast emerges:
- insider ALLOCATION % (launch team+investor allocation): null (the paper's headline allocation null);
- exchange-held %: null (this check);
- insider HOLDINGS (foundation/team on-chain control): significant and positive.

PCA and insider differ, and the difference is exactly the composition-shift thesis: what tracks
governance concentration is not how much was ALLOCATED to insiders at launch, nor how much sits
on exchanges, but how much insiders still HOLD and control on-chain. This is a candidate
robustness point for the R1-Major-7 response (the regression-evidence concern), distinguishing
the launch-allocation null from the insider-holdings signal.

## Caveats

N = 50; correlational, not causal. The foundation/team versus infrastructure split is
keyword-classified from the exclusions log (approximate at the margins; e.g. an ambiguous
multisig could fall either way). Exchange-% is share-of-top-1000, not total circulating supply.
The foundation/team to HHI link partly reflects that protocols with larger insider holdings are
simply more concentrated overall (pre and post exclusion); it is not a claim that exclusion
causes concentration. Exploratory supplement, not a primary result.
