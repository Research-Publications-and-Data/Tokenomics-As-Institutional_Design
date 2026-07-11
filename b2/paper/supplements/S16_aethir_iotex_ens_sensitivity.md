# Supplementary File S16: Aethir / IoTeX / ENS sensitivity analyses (cycle 13 audit-trail)

**Companion to:** B2 paper *Tokenomics as Applied Political Philosophy: Governance Concentration Beyond Token Allocation* (Section 4.8 Limitations). Generated 2026-05-22.

---

## Abstract

This supplement documents per-protocol PCA-exclusion sensitivity analyses surfaced during the 2026-05-19 universal verification audit cycle, addressing protocol-controlled-address (PCA) classification edge cases for Aethir (4 top-holder verifications), IoTeX (Genesis-burn precompile slot completeness audit), and ENS (Cold Wallet exclusion). The audit cycle confirmed one additional Aethir Safe multisig PCA, two missed IoTeX Genesis-burn precompile exclusions, and one missed ENS Cold Wallet exclusion. All three cascade updates preserve direction of effect and statistical significance of the headline DePIN-vs-DeFi sector contrast; the audit-trail detail provides the per-protocol sensitivity-check transparency that Reviewer 1 R2 feedback specifically flagged. 

**Supersession note.** This is a point-in-time record of the 2026-05-19 verification cycle (cycle 13). The per-protocol PCA-exclusion edge cases documented below (Aethir Safe multisig, IoTeX Genesis-burn precompiles, ENS Cold Wallet) remain of-record. The downstream sector and per-protocol HHIs reported here as cycle-13 cascade effects (the DePIN-vs-DeFi sector mean and Mann-Whitney significance; the ENS and L1/L2 per-protocol HHIs) were subsequently updated by the 2026-05-31 exchange-custody completion cascade and the 2026-06-01 disperser-ratio empirical upgrade; of-record values are in Section 4.3, Table 3, and Supplementary File S0.

## Cross-reference

This supplement supports Section 4.8 Limitations (Cross-referenced limitations discussed in other sections subsection). Main paper retains a headline-summary in §4.8; this supplement reports the per-protocol sensitivity detail.

## Aethir holding HHI sensitivity (4 top-holder verifications)

The Aethir holding HHI was revised in the R2 cascade via a supplementary verification cycle (2026-05-19) of the next four unlabeled top holders. Etherscan address analysis identified one confirmed additional PCA and three indeterminate candidates pending inter-rater reliability review.

**Confirmed additional PCA exclusion: 0xfc78...**

0xfc78... is a Safe 1.4.1 smart account (multisig) holding 1.01 billion ATH (2.4 percent of supply) with nine Exec Transaction calls, matching the same Class 2 typology already applied to 0x3e7e... (the previously-documented Aethir Safe multisig). Adding 0xfc78... to the canonical exclusion set raised the documented PCA count from 7 to 8 and shifted Aethir HHI from 0.087 to 0.095 (top-1 share 18.32 percent to 19.74 percent; Gini 0.945 to 0.943; N 993 to 992).

**Aethir-only sub-cascade effects (small):**

- DePIN sector mean: 0.077 → 0.078
- DePIN-vs-DeFi Mann-Whitney p-value: 0.018 (unchanged)
- Cohen's d: 0.99 (up from 0.98)
- LOO 30 of 30 significant-iteration result: preserved
- Permutation-test p-value: remains less than 0.01

**Three additional top holders verified but not excluded from canonical methodology:**

1. **0x33548...** — exhibits a distribution-wallet pattern (13 small-amount transfers; EOA without Etherscan label). Flagged as Class 1 candidate pending inter-rater reliability cycle.

2. **0x5a4a...** — a 21-day-old EOA funded by a single source with 100 percent ATH portfolio. Flagged as a possible strategic-allocation recipient pending inter-rater reliability cycle.

3. **0xaf8d...** — a 1.7-year-old EOA with 286 transactions. Deeper transfer-pattern analysis (2026-05-19) shows systematic outflows to the ATH token contract itself (regular 3 to 10 million ATH transfers every 1 to 3 days over the most recent 45-day window; no CEX-counterparty outflows visible). The token-contract-recipient pattern is consistent with treasury, vesting unlock, or staking-pool interactions rather than EOA hodling or market-maker behavior, elevating 0xaf8d... from indeterminate to a likely Class 1 or Class 4 candidate; the formal classification remains pending inter-rater reliability review.

**Sensitivity scenarios:**

- If 0x33548... is also classified as a PCA: Aethir HHI shifts to 0.104.
- If 0xaf8d... is reclassified: Aethir HHI shifts downward to 0.028 (indeterminate is a downward-leverage exclusion).
- All sensitivity scenarios preserve Aethir's rank ordering within the DePIN sector and the DePIN-vs-DeFi sector contrast direction.

The 8-PCA value of 0.095 was the canonical value at this cycle, pending inter-rater reliability review of the three remaining candidates. Vintage note (2026-07-10): after the Supplementary File S13 exchange-custody completion audit, the of-record Table 3 Aethir value is 0.1001 (0.100 in the Figure 1 caption); 0.095 is retained here as the cycle-13 point-in-time 8-PCA value.

## IoTeX Genesis-burn precompile slot completeness audit

The same 2026-05-19 universal verification cycle identified two additional missed IoTeX exclusions: Genesis-burn precompile slots 0x03 (1B IOTX, 10 percent) and 0x07 (748M IOTX, 7.5 percent; both Etherscan-verified Burn+Genesis labels). These had been omitted from the exclusion log despite matching the same Class 1 typology already applied to slots 0x01, 0x02, 0x04, 0x05, and 0x06.

**Cascade effects:**

- IoTeX HHI: 0.189 → 0.081 (substantial shift; the missed exclusions accounted for ~17.5% of supply at the protocol level)
- DePIN sector mean: 0.078 → 0.071 at this cycle; of-record 0.067 after the subsequent 2026-05-31 exchange-custody completion cascade (Section 4.3; Supplementary File S0)
- DePIN-vs-DeFi Mann-Whitney significance: p = 0.020 (preserved) at this cycle. Of-record now (2026-07-10 repoint): the headline is the voter-inclusive pass-through frame, MW p = 0.028 / Cohen's d = 0.65, with the uniform staking-aggregation exclusion as robustness (p = 0.018 / d = 0.75); the p = 0.011 / d = 1.05 previously cited here is the superseded S10 Spec A inconsistent-staking estimate (Section 4.3, Section 4.6.2; Supplementary Files S0 and S10)
- LOO 30 of 30 significant-iteration robustness: preserved

The cascade strengthens the universal-audit consistency of the PCA-exclusion methodology by closing a log omission surfaced during the user-flagged 2026-05-19 audit cycle.

## ENS Cold Wallet exclusion

ENS Cold Wallet 0x690f0581 (4.29M ENS, 5.2 percent of supply) is an Etherscan-labeled Safe Singleton 1.3.0 multisig created by nick.eth (the protocol founder). Adding it as a Class 2 exclusion (foundation-controlled multisig custody) shifted ENS HHI from 0.071 to 0.049, with the L1/L2/Infrastructure sector mean shifting from 0.027 to 0.024.

The cascade strengthens the universal-audit consistency of the PCA-exclusion methodology by closing a log omission surfaced during the audit cycle.

## Audit-cycle methodological implications

Both cascade updates (IoTeX precompile slots; ENS Cold Wallet) strengthen the universal-audit consistency of the PCA-exclusion methodology by closing log omissions surfaced during the user-flagged 2026-05-19 audit cycle. The audit cycle was triggered by a manual review of the highest-holding addresses across all 40 protocols, specifically looking for Etherscan-labeled or Blockscout-verified PCA candidates that may have been omitted from the canonical exclusion log.

The audit-cycle pattern (manual review of top-N addresses; cross-check against Etherscan + Blockscout labels; verify against protocol documentation) is documented as a methodological discipline for future replication and extension work. The 5-class PCA typology is well-defined; the audit-cycle discipline is necessary because protocol-controlled-address identification is partly judgment-based (Class 1 burn destinations are mechanical; Classes 2-5 require inspection of address provenance, deployer identity, and transaction patterns).

## Replication

Audit-cycle output captured at `b2/paper/supplements/exclusions_log_v2_2026-05-19.csv` in the replication repository. The 2026-05-19 audit-cycle additions are marked with `audit_cycle: 2026-05-19` column tags for traceability. The four remaining inter-rater-reliability-pending Aethir candidates (0x33548, 0x5a4a, 0xaf8d) are tagged `irr_pending: true` for future audit-cycle review.

## References (main-paper bibliography continues to apply)

PCA exclusion methodology codified in main paper Section 2.10.10; cycle 13 audit-cycle anchor in main paper Section 4.8 limitations subsection.
