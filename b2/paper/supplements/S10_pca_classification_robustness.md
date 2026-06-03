# Supplementary File S10: PCA-classification 5-spec robustness

**Companion to:** B2 paper *Tokenomics as Applied Political Philosophy: Governance Concentration Beyond Token Allocation* (Section 3.8 PCA exclusion methodology; Section 4.6.2 robustness). Generated 2026-05-22; recomputed to the post-CEX-audit frame 2026-06-01 (the earlier pre-audit Spec values are superseded; see Replication).

---

## Abstract

This supplement tests whether the DePIN-versus-DeFi sector contrast documented in Section 4.3 of the main paper is sensitive to the choice of which protocol-controlled-address (PCA) classes are excluded from the holding distribution. Five alternative specifications (Specs A through E) progressively reduce exclusion strictness from the canonical 5-class typology (Section 3.8) to the minimal Class 1 burn-destinations-only exclusion. The direction of the sector contrast (DePIN HHI > DeFi HHI in central tendency) holds under every specification (Cohen's d positive in all five). Statistical significance is sharpest under the full 5-class typology (Spec A: p = 0.011, large effect, Cohen's d = 1.05); under the nearest neighbor (Spec B, retaining CEX custody) the contrast attenuates to a medium effect (Cohen's d approximately 0.62) at the margin of conventional significance, significant under a narrower exchange definition and just non-significant under the most complete entity-label identification (Mann-Whitney p approximately 0.03 to 0.05); Specs C, D, and E lose significance at progressively reduced exclusion strictness. The Spec A large-effect value reflects the of-record exclusion, which applied the staking-aggregation (Class 3) exclusion inconsistently across sectors (DeFi-side staking aggregates excluded, one DePIN-side staking pool retained); applying that exclusion consistently yields a medium effect (Cohen's d = 0.75, Mann-Whitney p = 0.018) that is robustly significant (permutation p = 0.009, all thirty leave-one-out folds), with the direction positive under every specification (Section 4.6.2).

## Cross-reference

This supplement supports Section 4.6.2 PCA-exclusion-strictness robustness paragraph (and the Section 5.7 limitations cross-reference). Main paper retains the 5-spec results table plus a 1-paragraph interpretation summary; this supplement reports the per-specification narrative interpretation and the alternative-classification rationale.

## Five-class typology recap

The canonical 5-class PCA typology codified in Section 3.8 of the main paper distinguishes:

- **Class 1:** Burn destinations (e.g., `0x000...000` and `0x000...000dead` on EVM chains; chain-specific equivalents on Solana).
- **Class 2:** Foundation and treasury custody (e.g., Optimism Foundation GnosisSafe; ENS Cold Wallet; WeatherXM treasury).
- **Class 3:** Staking-aggregation contracts (e.g., stkAAVE staking contract; sGMX RewardTracker).
- **Class 4:** Bridge custody and migration addresses (e.g., Wormhole Token Bridge custody; cross-chain migration contracts).
- **Class 5:** Centralized exchange (CEX) custody (e.g., Binance hot wallets; Coinbase custody addresses).

The full address-by-address documentation is in Supplementary File S6 (exclusions log).

## Five-specification robustness test

We recompute the Mann-Whitney rank test on the DePIN-vs-DeFi sector contrast (N = 15 DePIN + 15 DeFi protocols where holder files are available; total N = 30) under five progressively stricter alternative exclusion specifications. Effect sizes are reported as Cohen's d (pooled standard deviation).

| Spec | Description | Addresses excluded (of 30 holder files) | Mann-Whitney p | Cohen's d |
|---|---|---:|---:|---:|
| **A** | Canonical 5-class (Classes 1-5 all excluded) | 150 | 0.011 | 1.05 |
| **B** | Drop Class 5 (CEX custody retained in holders) | 79 | 0.051 | 0.62 |
| **C** | Drop Class 4 + 5 (CEX + bridge/migration retained) | 74 | 0.135 | 0.40 |
| **D** | Drop Class 3 + 4 + 5 (only Class 1 + 2 excluded) | 65 | 0.648 | 0.16 |
| **E** | Drop Class 2 + 3 + 4 + 5 (only Class 1 burn destinations excluded) | 14 | 0.561 | 0.43 |

Spec B is reported here at the most complete CEX identification (retaining every entity-labeled exchange-custody address); under a narrower exchange definition the same specification is significant (p approximately 0.034, Cohen's d approximately 0.64). The exact retain-CEX p is therefore contingent on exchange-identification breadth across the 0.03 to 0.05 band; the medium effect size (Cohen's d approximately 0.62) is stable across that band.

## Per-specification narrative interpretation

**Spec A (canonical 5-class).** Mann-Whitney p = 0.011, Cohen's d = 1.05. This is the of-record specification, which applied the Class 3 staking-aggregation exclusion inconsistently across sectors; the main text now reports the sector contrast under a consistent staking-aggregation treatment as a medium effect (Cohen's d = 0.75, p = 0.018), robustly significant across permutation, leave-one-out, and the properly-specified multivariate test (Section 4.6.2).

**Spec B (drop Class 5; CEX custody retained).** Mann-Whitney p approximately 0.05, Cohen's d approximately 0.62. Retaining centralized-exchange custody addresses in the holder distribution attenuates the contrast from a large effect to a medium effect at the margin of conventional significance. The exact p is contingent on how completely exchange-deposit wallets are identified by entity label: significant under a narrower exchange definition (p approximately 0.034) and just non-significant under the most complete (p approximately 0.051). Exchange-deposit concentration is sector-similar, so retaining it partially masks the genuine governance-holder difference; complete identification sharpens the contrast rather than being an optional refinement.

**Spec C (drop Class 4 + 5; CEX custody and bridge/migration retained).** Mann-Whitney p = 0.135, Cohen's d = 0.40. The contrast is non-significant at the N = 30 sample size, with a small-to-medium effect size. Bridge custody addresses (notably Wormhole Token Bridge for RENDER) account for substantial concentration mass in specific DePIN protocols; retaining them in addition to CEX custody narrows the DePIN-vs-DeFi gap further.

**Spec D (only Class 1 + 2 excluded).** Mann-Whitney p = 0.648, Cohen's d = 0.16. The contrast loses both significance and meaningful effect size. Retaining staking-aggregation contracts (Class 3) in the holder distribution absorbs a substantial fraction of governance-relevant token holdings into single-address custody, which inflates HHI for protocols with prominent staking aggregation (notably stkAAVE on AAVE and the veCRV vote-escrow locker on CRV).

**Spec E (only Class 1 burn destinations excluded).** Mann-Whitney p = 0.561, Cohen's d = 0.43. The contrast is statistically null. Excluding only burn destinations and retaining all other protocol-controlled addresses in the holder distribution preserves a holder distribution that is structurally not governance-relevant (because foundation, treasury, staking-aggregation, bridge, and CEX-custody addresses do not vote in proportion to their token holdings).

## Methodological implications

The progression illustrates two findings:

1. **Direction is robust.** The DePIN HHI > DeFi HHI central-tendency claim holds under every specification (Cohen's d is positive in all five). The directional cross-protocol pattern is not an artifact of specific PCA-exclusion choices.

2. **Significance strength is load-bearing on the 5-class typology.** The magnitude and significance of the sector contrast depend on whether staking-aggregation (Class 3) and CEX-custody (Class 5) exclusions are applied. Spec A is large and unambiguously significant; Spec B (retaining CEX) attenuates to a medium effect at the margin of significance, significant under a narrow exchange definition and just non-significant under the most complete; Spec C produces a small-to-medium-effect contrast that fails the 0.05 threshold under N = 30; Specs D and E (very minimal exclusions) absorb so much non-vote-eligible signal into the holding distribution that the sector-contrast statistical power is exhausted.

The methodological implication is that consistent and complete PCA exclusion is load-bearing for the magnitude and significance of the sector contrast. Applying the five-class typology consistently across sectors (Section 3.8, Section 4.6.2) yields a medium, robustly-significant effect (Cohen's d = 0.75); the of-record large-effect value reflected an inconsistent staking treatment, and weaker exclusions absorb non-vote-eligible signal into the holding distribution and exhaust the sector-contrast power. Without the 5-class exclusion, the holding distribution includes addresses that structurally cannot vote, and the sector signal is partially absorbed into the noise of non-vote-eligible token holdings.

## Alternative-classification rationale

The five-class typology was developed by inspection of the 52-protocol cross-section: each class corresponds to an empirically-identifiable category of token-holding address that structurally cannot or does not vote in proportion to its token holdings. The classes are not statistical convenience but operational categories derivable from blockchain-explorer labels (Etherscan, Blockscout, Solscan) and protocol documentation. An alternative classification could:

- Drop Class 5 (CEX custody) on the rationale that exchange custody addresses do vote on behalf of beneficial holders in some governance systems (notably Compound's COMP delegation from Coinbase). This is Spec B; it attenuates the contrast to the margin of conventional significance (significant under a narrow exchange definition, just non-significant under the most complete).
- Drop Class 3 (staking aggregation) on the rationale that aggregation contracts pass-through underlying staker voting power. This is Spec D; it loses significance. The pass-through framing is partially correct (stkAAVE does pass through voting power) but stkAAVE votes as a single delegate per Tally's data model, so the aggregation contract's voting-HHI position is preserved at the contract level rather than distributed across underlying stakers.
- Add Class 6 (lending-protocol collateral custody) on the rationale that tokens held as DeFi collateral are not governance-active. This refinement is documented as future-work; the current 52-protocol sample does not have sufficient cross-protocol lending-collateral data to estimate the effect.

The selected 5-class typology balances completeness (capturing the dominant categories of non-vote-eligible token custody) with operational identifiability (each class can be assigned from publicly-available blockchain data with reasonable inter-rater reliability per Section 3.8).

## Replication

The five-specification robustness test was recomputed on the post-CEX-audit frame (2026-06-01) via the of-record CEX-recompute machinery (`b2/paper/analysis_n52_2026-05-29/cex_audit_2026-05-31/b2_full_cex_recompute.py`) plus a per-specification PCA-class re-inclusion sweep (`b2/paper/analysis_n52_2026-05-29/cex_audit_2026-05-31/b2_s10_ofrecord_recompute_2026-06-01.py`) in the replication repository (`Tokenomics-As-Institutional_Design`). Inputs: post-exclusion top-1000 holder files per protocol (per the canonical 5-class exclusion); per-specification masks re-include PCA classes by the 5-class typology before recomputing holder HHI and the Mann-Whitney test. The earlier pre-audit values (computed 2026-05-22 via `pca_classification_robustness_2026-05-22.py`) are superseded by this recompute.

## References (main-paper bibliography continues to apply)

See main paper bibliography for full references to: Hirschman (1964), Aramonte et al. (2021), Mann-Whitney rank test methodology, Cohen (1988) effect-size conventions, PCA-exclusion methodology Section 3.8.
