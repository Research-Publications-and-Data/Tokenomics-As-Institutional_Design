# Supplementary File S10: PCA-classification 5-spec robustness

**Companion to:** B2 paper *Tokenomics as Applied Political Philosophy: Governance Concentration Beyond Token Allocation* (Section 4.6 Robustness). Generated 2026-05-22.

---

## Abstract

This supplement tests whether the DePIN-versus-DeFi sector contrast documented in Section 4.3 of the main paper is sensitive to the choice of which protocol-controlled-address (PCA) classes are excluded from the holding distribution. Five alternative specifications (Specs A through E) progressively reduce exclusion strictness from the canonical 5-class typology (Section 3.8) to the minimal Class 1 burn-destinations-only exclusion. The direction of the sector contrast (DePIN HHI > DeFi HHI in central tendency) holds under every specification (Cohen's d positive in all five), but statistical significance requires the full 5-class typology: Specs A and B retain conventional significance, while Specs C, D, and E lose significance at progressively reduced exclusion strictness. The PCA exclusion methodology is therefore load-bearing for the inferential claim of statistical significance; the directional claim is robust to specification choice.

## Cross-reference

This supplement supports the Section 4.6.2 PCA-classification robustness paragraph (and the limitations cross-reference in Section 5.7). Main paper retains the 5-spec results table plus a 1-paragraph interpretation summary; this supplement reports the per-specification narrative interpretation and the alternative-classification rationale.

## Five-class typology recap

The canonical 5-class PCA typology codified in Section 3.8 of the main paper distinguishes:

- **Class 1:** Burn destinations (e.g., `0x000...000` and `0x000...000dead` on EVM chains; chain-specific equivalents on Solana).
- **Class 2:** Foundation and treasury custody (e.g., Optimism Foundation GnosisSafe; ENS Cold Wallet; WeatherXM treasury).
- **Class 3:** Staking-aggregation contracts (e.g., stkAAVE staking contract; sGMX RewardTracker).
- **Class 4:** Bridge custody and migration addresses (e.g., Wormhole Token Bridge custody; cross-chain migration contracts).
- **Class 5:** Centralized exchange (CEX) custody (e.g., Binance hot wallets; Coinbase custody addresses).

The full address-by-address documentation is in the exclusions log (`data/processed/exclusions_log.csv`).

## Five-specification robustness test

We recompute the Mann-Whitney rank test on the DePIN-vs-DeFi sector contrast (N = 15 DePIN + 15 DeFi protocols where holder files are available; total N = 30) under five progressively stricter alternative exclusion specifications. Effect sizes are reported as Cohen's d (pooled standard deviation).

| Spec | Description | Addresses excluded | Mann-Whitney p | Cohen's d |
|---|---|---:|---:|---:|
| **A** | Canonical 5-class (Classes 1-5 all excluded) | 125 across 36 protocols | 0.029 | 0.94 |
| **B** | Drop Class 5 (CEX custody retained in holders) | 106 | 0.039 | 0.84 |
| **C** | Drop Class 4 + 5 (CEX + bridge/migration retained) | 98 | 0.115 | 0.60 |
| **D** | Drop Class 3 + 4 + 5 (only Class 1 + 2 excluded) | 86 | 0.610 | 0.17 |
| **E** | Drop Class 2 + 3 + 4 + 5 (only Class 1 burn destinations excluded) | 10 | 0.512 | 0.35 |

## Per-specification narrative interpretation

**Spec A (canonical 5-class; the paper's main specification).** Mann-Whitney p = 0.029, Cohen's d = 0.94. The DePIN-vs-DeFi sector contrast is statistically significant at conventional thresholds with a large effect size. This is the specification used throughout the paper's main results.

**Spec B (drop Class 5; CEX custody retained).** Mann-Whitney p = 0.039, Cohen's d = 0.84. The sector contrast remains statistically significant. Retaining CEX-custody addresses in the holder distribution inflates concentration measures for protocols with high exchange-side custody (notably Aave with the Binance 8 hot wallet at 10.32% of total supply) but does not change the sector contrast direction or significance.

**Spec C (drop Class 4 + 5; CEX custody and bridge/migration retained).** Mann-Whitney p = 0.115, Cohen's d = 0.60. The contrast loses conventional significance at the N = 30 sample size, though the effect size remains medium (d > 0.5). Bridge custody addresses (notably Wormhole Token Bridge for RENDER) account for substantial concentration mass in specific DePIN protocols; retaining them in the holder distribution narrows the DePIN-vs-DeFi gap.

**Spec D (only Class 1 + 2 excluded).** Mann-Whitney p = 0.610, Cohen's d = 0.17. The contrast loses both significance and meaningful effect size. Retaining staking-aggregation contracts (Class 3) in the holder distribution absorbs a substantial fraction of governance-relevant token holdings into single-address custody, which inflates HHI for protocols with prominent staking aggregation (notably stkAAVE at 21.9% of post-PCA-exclusion top-1000 AAVE).

**Spec E (only Class 1 burn destinations excluded).** Mann-Whitney p = 0.512, Cohen's d = 0.35. The contrast is statistically null. Excluding only burn destinations and retaining all other protocol-controlled addresses in the holder distribution preserves a holder distribution that is structurally not governance-relevant (because foundation, treasury, staking-aggregation, bridge, and CEX-custody addresses do not vote in proportion to their token holdings).

## Methodological implications

The progression illustrates two findings:

1. **Direction is robust.** The DePIN HHI > DeFi HHI central-tendency claim holds under every specification (Cohen's d is positive in all five). The directional cross-protocol pattern is not an artifact of specific PCA-exclusion choices.

2. **Significance is load-bearing on the 5-class typology.** Statistical significance of the sector contrast depends on whether staking-aggregation (Class 3) and CEX-custody (Class 5) exclusions are applied. Specs A and B retain conventional significance; Spec C produces a medium-effect-size contrast that fails the 0.05 threshold under N = 30; Specs D and E (very minimal exclusions) absorb so much non-vote-eligible signal into the holding distribution that the sector contrast statistical power is exhausted.

The methodological implication is that the PCA exclusion methodology applied throughout the paper is load-bearing for the inferential claim of statistical significance: applying the consistent 5-class typology documented in Section 3.8 is necessary to identify the sector contrast that the paper reports. Without the 5-class exclusion, the holding distribution includes addresses that structurally cannot vote, and the sector signal is absorbed into the noise of non-vote-eligible token holdings.

## Alternative-classification rationale

The five-class typology was developed by inspection of the 40-protocol cross-section: each class corresponds to an empirically-identifiable category of token-holding address that structurally cannot or does not vote in proportion to its token holdings. The classes are not statistical convenience but operational categories derivable from blockchain-explorer labels (Etherscan, Blockscout, Solscan) and protocol documentation. An alternative classification could:

- Drop Class 5 (CEX custody) on the rationale that exchange custody addresses do vote on behalf of beneficial holders in some governance systems (notably Compound's COMP delegation from Coinbase). This is Spec B; it preserves significance.
- Drop Class 3 (staking aggregation) on the rationale that aggregation contracts pass-through underlying staker voting power. This is Spec D; it loses significance. The pass-through framing is partially correct (stkAAVE does pass through voting power) but stkAAVE votes as a single delegate per Tally's data model, so the aggregation contract's voting-HHI position is preserved at the contract level rather than distributed across underlying stakers.
- Add Class 6 (lending-protocol collateral custody) on the rationale that tokens held as DeFi collateral are not governance-active. This refinement is documented as future-work; the current 40-protocol sample does not have sufficient cross-protocol lending-collateral data to estimate the effect.

The selected 5-class typology balances completeness (capturing the dominant categories of non-vote-eligible token custody) with operational identifiability (each class can be assigned from publicly-available blockchain data with reasonable inter-rater reliability per Section 3.4).

## Replication

The five-specification robustness test was computed via `b2/paper/supplements/pca_classification_robustness_2026-05-22.py` in the replication repository (`Tokenomics-As-Institutional_Design`). Inputs: post-exclusion top-1000 holder files per protocol (per the canonical 5-class exclusion); per-specification exclusion masks are applied to recompute holder HHI per specification before Mann-Whitney test.

## References (main-paper bibliography continues to apply)

See main paper bibliography for full references to: Hirschman (1964), Aramonte et al. (2021), Mann-Whitney rank test methodology, Cohen (1988) effect-size conventions, PCA-exclusion methodology Section 3.8.
