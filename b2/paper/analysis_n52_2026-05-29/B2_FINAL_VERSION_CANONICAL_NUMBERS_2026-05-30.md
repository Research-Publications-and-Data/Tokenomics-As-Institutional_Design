# B2 final-version canonical numbers (post A1-A8 data lane)

As-of: 2026-05-30. Produced by the clone-A data-lane execution of the B2 final-version
dispatch (commits B1 d662b41, A6 4bfc0f3, A1/B3 80d7ad5, A2 52b074e, A4 76c7291, A3 5f35687).
Reader MUST re-run `python3 reproduce.py` + the six-vector harness and grep current canonical
files before propagating to the manuscript; state may have advanced.

## Headline specs (final, N=50)

| spec | pre-A-decisions (committed baseline) | FINAL (post A1+A6+A3) |
|---|---:|---:|
| maturity-spec DePIN p (anchor) | 0.0395 | **0.0197** |
| retention-spec DePIN p (v4_traced of record) | 0.0409 (v3) | **0.0139** |
| full-frame Mann-Whitney DePIN vs DeFi | 0.0364 (d 0.807) | **0.0234 (d 0.939)** |
| balanced-30 Mann-Whitney (of record; unchanged) | 0.0202 (d 0.940) | 0.0202 (d 0.940) |
| insider-retention regressor (n.s.; channel-shift) | 0.4884 | 0.4892 |
| de-tautology Spearman rho / OLS p (unchanged) | 0.544 / 0.0024 | 0.544 / 0.0024 |

Six-vector insider-classification robustness (all < 0.02, DePIN significant under every vector):
keyword 0.0058 / reviewed_safe 0.0090 / **v4_traced 0.0139** / reviewed 0.0148 / baseline_v3 0.0168 / resolved 0.0187.

The headline (DePIN governance concentration > DeFi) is robustly STRENGTHENED by the A-decisions.

## Per-protocol frame changes

A6 (Solana holder-HHI refresh; pre to post-S13-exclusion):
- JUP  hhi 0.095708 -> 0.126008 ; top1 25.96/30.94 ; top5 52.06/59.96 ; top10 69.32/73.87
- DRIFT hhi 0.052914 -> 0.056802 ; top1 19.30/20.19 ; top5 39.03/40.84 ; top10 49.10/49.60
- HNT  hhi 0.074465 -> 0.087431 ; top1 16.47/19.34 ; top5 51.47/56.96 ; top10 76.39/78.07

A3 (PCA-strict tighten; exclude surviving protocol-controlled Class-2/3):
- WLFI hhi 0.155738 -> 0.081244 ; top1 28.68/25.90 ; top5 62.73/42.72 ; top10 72.11/53.98 (ret 0.7->0.3)
- ENA  hhi 0.047164 -> 0.042670 ; top1 9.67/15.81 ; top5 41.91/36.87 ; top10 61.38/47.36 (ret 0.5->0.2)
- PUMP hhi 0.040147 -> 0.031642 ; top1 10.03/9.75 ; top5 37.83/34.46 ; top10 56.99/47.85 (ret 0.0)
- KMNO hhi 0.031341 -> 0.026914 ; top1 7.89/7.98 ; top5 31.94/28.61 ; top10 49.22/44.22 (ret 0.3)
- JTO  hhi 0.025881 -> 0.026567 ; top1 9.61/9.88 ; top5 28.52/29.31 ; top10 41.07/41.17 (ret 0.0; ~flat)

WLFI sensitivity: 0.081244 keeps ALT5 Sigma (corporate-treasury strategic investor, not
protocol-controlled); excluding ALT5 too would give ~0.066. 0.081244 is the conservative choice.

## Classification of record (A1)

Insider classification of record = v4_traced (Nansen entity labels + Blockscout/Safe-deployer
traces; team-confirmed-multisig rule). reproduce.py retention regressor = v4_traced (fallback
new12 then v3). The five A1 corrections: DIMO 0.4->0.1, GEOD 0.3->0.1, MKR 0.3->0.2, MOR 0.5->0.2,
WXM 0.4->0.2 (independent whales' Safes de-counted); additions UNI 0.3 (a16z), COMP 0.3, ENS 0.2,
BAL 0.1. A7: HONEY carries a v4_traced retention value (0.2), lifting the retention-spec N 49->50.

## Methodology deliverables (no frame-HHI change)

- A2 (staking attribution): address-level attribution of insider stkAAVE/sENA moves the holding
  HHI < 1% and dilutively (AAVE 0.012790->0.012744; ENA 0.047164->0.046662). Substance = insider
  SHARE/visibility: 4.4-6.3% of AAVE supply is insider AAVE hidden in stkAAVE (ENA 0.43%).
  Consistent with the paper's "holding-HHI understates effective concentration" argument.
  -> Section 3.8 staking-treatment + Section 4.4 AAVE methodology paragraph.
- A4 (LPT orchestrator-level governance HHI): orchestrator bloc-voting HHI = 0.0535 (100 active
  orchestrators; as-of Arbitrum block 468186375 / round 4216), which is 3.7x LOWER than the raw
  holding-HHI 0.198868 (ratio 0.27x). LPT is a DISPERSER (delegation across ~100 orchestrators
  disperses governance), INVERTING the dispatch's A4 concentrate-hypothesis. Frame holding-HHI
  unchanged (0.198868). -> NEW Section 4.5 voting-vs-holding data point (LPT joins ENS/GMX/HNT/JUP
  as a delegation-disperses exception; the first DePIN one).
- A8 (DOT): keep frame holder-HHI 0.0052 (AssetHub post-PCA of record); footnote 0.0139 raw /
  0.0093 AssetHub Class-2+3 / 0.0017 validator-set alternatives.

## Acceptance

reproduce.py: one command, deterministic, no /tmp, no live-API; 9/9 new-cohort HHIs reproduce
from raw; maturity anchor 0.0197 EXACT; retention 0.0139 EXACT; de-tautology unchanged. The
manuscript HHI table must match the reconciled frame cell-by-cell; every changed value traces to
an A-decision + an artifact in nansen_reclass_2026-05-29/.
