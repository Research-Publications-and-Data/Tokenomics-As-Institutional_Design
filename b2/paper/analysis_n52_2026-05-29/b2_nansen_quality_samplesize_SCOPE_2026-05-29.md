# Can more Nansen runs improve data quality + sample size? Scope + answer

**As-of:** 2026-05-29. Answer: YES for data quality on the 44 Nansen-reachable protocols
(directly closes the audit's classification + exclusion gaps); QUALIFIED for sample size (genuine
value because the headline is marginal, but holder-list + covariate capture is the parallel
bottleneck, and 6 protocols are off-Nansen). Reader MUST re-verify before executing.

## Coverage: Nansen reaches 44 of 50 frame protocols

Nansen supports EVM + Solana (+ a few). Of the 50: COVERABLE 44 (ethereum 24, solana 13,
arbitrum 4, polygon 2, optimism 1). NOT coverable 6: FIL (filecoin), POKT (native), HYPE
(hyperliquid L1), ALGO, DOT, TAO. The 6 off-Nansen are exactly the protocols with the hardest
open issues (DOT/TAO/ALGO PCA + capture gaps); Nansen cannot fix those.

## Data-quality gains on the 44 (each is an open audit gap, now Nansen-closable)

Demonstrated this session: `token_current_top_holders` returns authoritative entity labels
(foundation / treasury / multisig / investment-recipient / VC fund / CEX / retail whale) for the
full top-holder set, one call per token. Proven on the new-12 (FXS/SNX/GNO/WLFI/ENA/PUMP/JTO/
BONK/KMNO) and, this turn, ZRO -- whose top-10 resolves completely (LayerZero Future Initiatives
11.15 percent, Foundation 7.31 percent, Strategic Partnerships, 8+ ZRO Multisigs, a ZRO
Investment Recipient, Binance / Coinbase Prime / Upbit CEX, 2 retail Token Millionaires).

- **Closes G4 + G6 (insider classification consistency + auditability).** Re-classify all 44 via
  `token_current_top_holders` to produce ONE machine-readable, source-cited insider classification
  for every protocol (the original 37 + the new 12), replacing the un-persisted Tier-2/3 manual
  determinations. This makes the retention vector fully reproducible and lets the 3 supply-
  corrected non-insider HHIs (AXL/MOR/ZRO) be computed (ZRO is demonstrably resolvable above).
- **Closes G7 (PCA exclusion completeness).** Nansen entity labels authoritatively confirm the
  leaked Class-2/3 survivors (Synthetix Treasury, Ethena-Labs EOAs, WLFI ecosystem/multisigs,
  pump.fun custody, ZRO multisigs), replacing keyword inference with ground-truth labels for a
  complete, verified exclusion set.
- **Resolves decision-flippers.** Premium-labels (reserved) settle the genuinely-ambiguous high-
  share unlabeled EOAs that move a classification.

Off-Nansen residuals stay: DOT/TAO/ALGO (no Nansen coverage; need Subscan/Taostats/AlgoNode +
the AssetHub re-capture), IO's R2 rescaling, FIL/POKT native-chain holder data.

## Sample size: worth expanding, but Nansen is only part of it

The headline is borderline-and-LOO-fragile (per the N=52 reanalysis: dropping one DePIN pushes
the 3-class Dunn p past 0.05; the regression DePIN p sits ~0.04). So MORE protocols genuinely
strengthens the result (more power, less LOO-fragility). But Nansen is only the CLASSIFICATION
step. To add a protocol you also need: the raw top-1000 holder list (Dune / Sim / Helius /
Subscan) and the covariates (revenue, FDV, maturity from Token Terminal / DefiLlama / the
CoinGecko series already gathered). Nansen accelerates the PCA + insider classification for each
new EVM/Solana protocol, not the capture. Realistic expansion: +15 to 30 EVM/Solana governance
tokens -> N approximately 65 to 80, which would materially de-risk the marginal headline. Off-
Nansen chains (Cosmos, Polkadot, Algorand, Filecoin) are the slow lane.

## Cost (Nansen credits)

- **Re-classification of the 44 (closes G4/G6/G7):** ~44 `token_current_top_holders` calls (one
  per token; the cheap bulk-label call) + ~20 to 40 premium-labels (500 cr each, reserved for
  decision-flippers). This is the single highest-value Nansen spend; it makes the entire insider/
  PCA/retention layer reproducible + auditable.
- **Per new protocol (sample-size expansion):** ~1 `token_current_top_holders` + 0 to 5 premium-
  labels for classification, PLUS the non-Nansen capture (Dune/Sim) + covariates.

## Recommendation

1. **Run the 44-protocol re-classification campaign** -- highest value: closes G4/G6/G7, produces
   a consistent machine-readable insider + PCA classification, and makes the retention/de-tautology
   fully reproducible. (Note: it produces a NEW classification that may differ from the un-
   persisted v3 manual one; reconcile + version it, do not silently overwrite.)
2. **Then expand the sample** on EVM/Solana (+15 to 30) to de-risk the marginal headline; Nansen
   handles the classification, Dune/Sim/Token-Terminal handle capture + covariates.
3. **Accept the 6 off-Nansen protocols** stay on their native-explorer lane (DOT/TAO/ALGO/FIL/
   POKT/HYPE).

Exploratory scope; no canonical writes; the campaign is a dedicated cycle (it re-derives the
insider classification of record).
