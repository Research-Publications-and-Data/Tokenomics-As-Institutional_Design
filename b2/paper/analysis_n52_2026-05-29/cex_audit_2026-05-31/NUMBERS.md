> **Superseded-in-part (banner added 2026-07-10; the dated 2026-05-31 record below is retained verbatim as audit trail).** Read with these corrections of record: (1) the sector-contrast headline is now the voter-inclusive pass-through frame (Cohen's d = 0.65, Mann-Whitney p = 0.028, N = 15/15), with the uniform staking-aggregation exclusion as robustness (d = 0.75, p = 0.018); (2) the p = 0.011 / d = 1.05 value below is the superseded Spec A inconsistent-staking specification and must never be cited as current; (3) the retain-all-CEX p = 0.184 / d = 0.52 value below is formally error-corrected and NON-reproducible per the 2026-06-01 p0184 reconciliation (of-record replacement: d approximately 0.62 at Mann-Whitney p approximately 0.03 to 0.05 under the most-complete exchange identification); (4) the manuscript publishes no full-frame point p or d (direction only, treatment-sensitive); (5) current LOO / permutation / bootstrap ranges: 30/30 folds significant, per-fold p 0.006 to 0.031 and d 0.68 to 0.92; permutation p = 0.009; bootstrap CIs [0.010, 0.081] and [0.40, 1.52].

# B2 CEX-exclusion audit — authoritative old->new numbers (2026-05-31)

## Headline contrasts (DePIN vs DeFi)
- Balanced-30 (15 gov-DePIN vs 15 gov-DeFi): p 0.020 -> 0.011 ; Cohen's d 0.94 -> 1.05 ; DePIN mean 0.071 -> 0.067 ; DeFi mean 0.031 -> 0.026 ; ratio 2.3 -> 2.6 ; Mann-Whitney U 169 -> 174.
- Full-frame (15 DePIN vs 24 DeFi): p 0.0234 -> 0.0172 ; Cohen's d 0.939 -> 1.052 (PAPER.md rounds to p=0.017, d=1.05).
- 3-class Kruskal-Wallis: p -> 0.0054 (H ~10.4).
- Balanced-30 robustness: LOO p range 0.008-0.034 -> 0.006-0.020 ; LOO d range 0.84-1.10 -> 0.97-1.17 ; permutation p 0.012 -> 0.004 ; bootstrap mean-diff 95% PI [0.012,0.069] -> [0.016,0.070] ; Cohen d 95% CI [0.32,1.68] -> [0.55,1.72] ; DePIN-within-DeFi-range 8 of 15 -> 9 of 15.
- Powered Model 4: maturity-spec DePIN log-HHI p 0.0197 -> 0.0107 (untransformed 0.030 -> 0.019) ; retention-spec primary p 0.0139 -> 0.0050. De-tautology Spearman rho 0.54 (unchanged at 2dp; 0.544). 6-vector insider robustness all significant (p 0.001-0.008).
- NEW finding (Class-5 load-bearing): retaining ALL CEX collapses balanced-30 to p=0.184, d=0.52 (n.s.); excluding gives p=0.011, d=1.05. Reverses prior "CEX not load-bearing" claim.

## JUP (the trigger)
- Holding HHI 0.1260 -> 0.0450 ; top1 30.9% -> 12.0% ; top5 60.0% -> 38.8% ; top10 73.9% -> 58.3% ; Gini 0.98 (unchanged).
- Amplification ratio (voting/holding) 0.043x -> 0.12x. JUP remains most-extreme dispersion outlier.
- JUP no longer the DeFi-governance-token max; new DeFi-gov max is GMX 0.065.

## Per-protocol HHI (frame of-record) old -> new
JUP 0.1260->0.0450 ; DRIFT 0.0568->0.0265 ; HNT 0.0874->0.0988 ; ATH 0.0948->0.1001 ; IO 0.1251->0.0402 ; HONEY 0.0176->0.0204 ; RENDER 0.0268->0.0273 ; ANYONE 0.0128->0.0130 ; GRT 0.0330->0.0214 ; AXL 0.0268->0.0231 ; ENS 0.0494->0.0463 ; COMP 0.0092->0.0086 ; CRV 0.0144->0.0146 ; LDO 0.0077->0.0077 ; MPL_SYRUP 0.0242->0.0237 ; RPL 0.0392->0.0406 ; AAVE 0.0128->0.0128 ; ARB 0.0119->0.0122 ; OP 0.0093->0.0094 ; POL 0.0348->0.0358 ; W 0.0115->0.0119.

## Table 3.5 cells (mean)
EVM DeFi 0.025 (unchanged) ; EVM DePIN 0.083->0.084 ; Solana DeFi 0.044->0.028 ; Solana DePIN 0.058->0.044.
Chain-cohort effect sizes: EVM Cliff -0.69->-0.71, Cohen d -1.40->-1.41 ; Solana Cliff -0.20->-0.43, Cohen d -0.35->-0.79.

## Exclusion accounting
- 64 new Class-5 CEX exclusion entries added across 21 protocols (54 genuinely-new unique addresses; live Nansen entity labels + 2026-05-29 v4 reclass CSV).
- The original-cohort "133 PCA exclusions / 125 unique / 38 protocols / median inflation 2.3x" figures are RETAINED as the original-layer methodology; the CEX audit is documented as a distinct exchange-custody completion layer reflected in the HHIs.

## IO note (data quality)
- IO holder list was truncated (20 rows); repulled 2026-05-31 via Helius DAS (84,881 token accounts -> 84,839 owners -> top-1000). IO frame value 0.1251 was a non-reproducible "R2 calibration rescaling" (per b2_pca_consolidation_GAPFILL). Fresh value with documented vault (Class-2, address 3EpUYHv8) + 23 CEX exclusions = 0.0402. Snapshot-date exception (May 2026 for IO; March 2026 for others) documented.

## Classifier bug (sibling clone)
- File: b2/paper/analysis_n52_2026-05-29/nansen_reclass_2026-05-29/b2_nansen_parse_and_classify_2026-05-29.py line 33.
- Old: EXCHANGE_KW = ['exchange', 'binance', 'coinbase', 'kraken', 'okx', 'gate']
- Missing brands (caused 25 EVM + many Solana misses): upbit, bybit, bithumb, kucoin, bitget, robinhood, backpack, mexc, crypto.com, htx, huobi, coinone, gemini, bitfinex, bitvavo, falconx; plus generic custody terms 'hot wallet', 'internal wallet', 'deposit'.
- Fix: extend EXCHANGE_KW with these brands + generic terms, AND prefer Nansen-entity-label presence over keyword match (label-presence detection). NOTE the 'gate' substring over-matches 'gateway' (a PROTOCOL_KW); guard with word boundary or check PROTOCOL_KW first.

## EM-DASH RULE: zero em-dashes (chr 0x2014) or en-dashes (chr 0x2013) in any authored prose. Use commas/parentheses/colons/periods/semicolons. Preserve source content's dashes only when migrating external author text.
