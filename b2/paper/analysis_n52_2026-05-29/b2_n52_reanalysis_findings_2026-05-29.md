# B2 N=52 re-analysis findings (HALT-A determination under the 3-class design)

**As-of:** 2026-05-29 (BULK-EXECUTOR; PID-tree session). Read-only against clone A
`/Users/zach/Tokenomics-As-Institutional_Design/data/processed/regression_data_april2026.csv` (N=46).
Reader MUST re-verify against live canonical state before acting.

Scripts (reproducible): `/tmp/b2_n52_reanalysis.py` (binary baseline) + `/tmp/b2_n52_3class.py` (3-class KW+Dunn).

## Verified inputs
- FXS 0.032411, SNX 0.017075 (S18 EVM minibatch 2026-05-27; per-address CONFIRMED; pre-excl re-derived from raw matches).
- GNO 0.042485 primary (co-founder Safes Class-2 excluded) / 0.076863 sensitivity (Safes kept). Immaterial to headline.
- DOT 0.0052 primary (Binance cluster Class-5 excluded; dot_pca_refined.py README, ground-truthed SubSquare + extrinsic) / 0.0093 sensitivity (Classes 2+3 only) / 0.0090 raw.
- ALGO 0.059096 (ALGO_holding_hhi_2026-04-30.json post-PCA).
- TAO 0.007486 principal-excluded / 0.014 raw. PCA DONE (this cycle): top-1000 cross-referenced vs ground-truthed
  tao_exchange_coldkeys.json; excluded 6 registry-confirmed addresses (12.62% of top-1000): Binance rank-1 (8.86%),
  MEXC, Crypto.com, Gate.io, Taobridge bridge, Binance-2. Renormalized on 994 remaining. Opentensor-foundation +
  subnet-staking-pool long-tail deferred (Substrate CEX-attribution-gap caveat; analog to DOT's 44.4% Class-5 gap).
  Script: /tmp/tao_pca.py.

## Of-record balanced-30 binary (PRESERVED, unchanged): Mann-Whitney p=0.0202, d=0.940. Matches published exactly.

## Three-class KW + Dunn (Holm) -- FINAL PRIMARY (DePIN15 / DeFi18 / L1-11; TAO=0.0075 in L1)
- Group means: DePIN 0.0705 / DeFi 0.0308 / L1 0.0239. L1 heterogeneous (range 0.0052-0.0591).
- Kruskal-Wallis omnibus: H=9.36, p=0.0093, epsilon^2=0.180 (large).
- Dunn post-hoc (Holm):
  - DePIN vs DeFi: p_adj=0.0358 [SIG] (Cohen d=0.99, Cliff delta +0.50) -- HEADLINE SURVIVES the 3-comparison correction.
  - DePIN vs L1: p_adj=0.0137 [SIG].
  - DeFi vs L1: p_adj=0.4355 [n.s.].

## KEY FINDING: the gradient is TWO-TIER, not three-tier.
DePIN >> {DeFi ~= L1}. The hypothesized monotonic DePIN > DeFi > L1 is NOT supported: DeFi and L1 are
statistically indistinguishable (p=0.52), driven by L1's wide internal spread (DOT 0.005 to ALGO 0.059).
Prose must frame as "DePIN significantly more concentrated than both DeFi and L1," NOT "three-tier gradient."

## Robustness caveats (HALT-A relevant; absent from the published balanced-30)
1. LOO-fragile: DePIN-DeFi Dunn p_adj range 0.0137-0.0586 across leave-one-out; dropping Hyperliquid (0.0586),
   Compound/Lido (0.0567), or WeatherXM (0.0565) pushes it past 0.05. The published "robust in 30/30 LOO" claim
   does NOT carry to the 3-class design.
2. TAO-classification-dependent: TAO-as-DePIN (SENS-A) -> DePIN-DeFi p_adj=0.0600 [n.s.]. The headline's survival
   rests on TAO being classified L1. Defensible on architectural grounds (Substrate base-layer L1 like DOT/ALGO),
   but it IS load-bearing -- report the TAO-as-DePIN sensitivity transparently.

## Sensitivities (all preserve the DePIN-DeFi headline except TAO-as-DePIN)
- SENS-A TAO->DePIN: p_adj=0.0600 [n.s.]  <- the one that flips
- SENS-B FIL/POKT excluded (DePIN=13): p_adj=0.0349 [SIG], d=1.037
- SENS-C DOT=0.0093 + GNO=0.0769: p_adj=0.0406 [SIG], d=0.921

## ALGO-sensitivity (author-requested gate on the two-tier framing) -- TWO-TIER ROBUST
ALGO post-PCA 0.059 is driven by ONE eligible holder: rank-1 N2C374IRX7HE (693M ALGO; status Offline,
0 apps, 0 assets; pure cold-storage; LARGER than every excluded Foundation wallet <=210M). Behavioral-signature
classifier (no Algorand explorer labels) left it Class-0 Eligible; it is plausibly an unlabeled CEX/Foundation
that authoritative labels would exclude (which would drop ALGO toward ~0.033). Disclose as a known limitation.
DeFi-vs-L1 Dunn p_adj across ALGO treatments: as-merged 0.059 -> 0.436 ; raw 0.033 -> 0.334 ; ALGO removed -> 0.265.
All >> 0.05: two-tier (DePIN >> {DeFi ~= L1}) is ROBUST; three-tier NOT restored. Lowering ALGO strengthens the
DePIN-L1 contrast (0.014 -> 0.006) and the omnibus (0.0093 -> 0.0054). Headline DePIN-DeFi stable (0.036 -> 0.040).
Merged value kept at 0.059 (documented behavioral-PCA output) with the N2C374 caveat + this sensitivity disclosed.

## Net
The author-chosen 3-class design preserves the DePIN-DeFi headline in the primary specification (p_adj=0.033,
d=0.99) and adds a significant DePIN-vs-L1 result, while honestly refining the gradient hypothesis to two-tier.
The two new caveats (LOO-fragility; TAO-L1 dependency) are the §11a reviewer-credibility items to disclose.
