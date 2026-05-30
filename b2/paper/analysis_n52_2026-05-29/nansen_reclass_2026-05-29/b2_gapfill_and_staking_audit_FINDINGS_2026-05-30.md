# B2 gap-fill resolution + staking-PCA governance audit: findings

**As-of:** 2026-05-30T04:10:00Z. **Clone:** clone-A `/Users/zach/Tokenomics-As-Institutional_Design`
(`b2/paper/analysis_n52_2026-05-29/nansen_reclass_2026-05-29/`). Nothing pushed. Frame + v3 untouched;
all of this routes to the author because changing exclusions moves published HHIs.
**Reader MUST** run `python3 scripts/claude-code-sync.py` and grep current canonical files before acting.

This cycle used the 11,700-credit Nansen budget plus free tools (Blockscout, WebSearch) to (1) resolve the
gap-fill decision-flippers and (2) audit the staking/vote-escrow PCA exclusions per two author directives:
"staked GEOD can vote in governance, so it should not be PCA-excluded; audit others" and "check for
PCA/Team/Foundation/Insider holdings locked in staking." Nansen spend this cycle: ~2,000 credits
(~13 calls: 6 staked-token holder pulls, 3 address traces, 4 EOA-search probes); the bulk of the work ran
on free Blockscout + WebSearch. ~9,700 credits remain for optional deeper follow-ons (Solana resolution,
ve-token lock tracing, more Safe-deployer confirmations).

## Part 1: gap-fill resolution (decision-flippers)

60 high-share / ambiguous survivors were resolved with on-chain evidence: free Blockscout
`get_address_info` for the 37 EVM targets (contract type, Safe status, proxy implementation, deployer) plus
targeted Nansen `address_related_addresses` traces for the highest-share Safes. Results in
`b2_gapfill_blockscout_resolved_2026-05-30.json` + `b2_nansen_insider_classification_v4_RESOLVED_2026-05-30.csv`.

Key resolutions (evidence-backed):
- **MKR vintage gap SOLVED (was 0/10 match).** MKR ranks 1, 3, 5 are Gnosis Safe multisigs; rank 1 (11.3%)
  is deployed by "MakerDAO: Delegator" and signs the MakerDAO / Sky multisig cluster (confirmed team).
  Ranks 7 = MakerDAO Flapper (protocol module); rest are retail EOAs. MKR insider 0.0 -> 0.3.
- **Protocol contracts confirmed NOT insider:** MOR rank 1 = "Morpheus Builders staking pool";
  WXM rank 1 (8.81%) = WXM reward distributor (ERC1967Proxy impl=RewardPool); MPL_SYRUP ranks 1+3 = SYRUP
  Custody-Vault aggregations; RENDER rank 4 = RENDER Custody Vaults; AAVE rank 4 = LEND-to-AAVE migrator.
- **Insiders confirmed:** DIMO multisigs (rank 1 deployed by dinc.eth = DIMO team); BAL rank 3 = "Balancer
  Vested Shareholders"; ATH / ZRO bare project-tags = team wallets; MOR Safes.
- **Exchange confirmed:** MPL_SYRUP rank 2 = FalconX; RENDER rank 2 = KuCoin; RPL rank 3 = Coinbase Prime;
  HONEY rank 6 = Hivemapper Deposit.

Nine reviewed calls changed under the evidence (v4_reviewed -> v4_resolved):
MKR 0.0->0.3, DIMO 0.3->0.4, MOR 0.4->0.5, HONEY 0.3->0.2, MPL_SYRUP 0.6->0.4, RENDER 0.1->0.0.
Residual unresolved: the Solana ambiguous survivors (GRASS / JUP / W / HNT) stay unlabeled (Blockscout is
EVM-only; Nansen Solana traces give only weak first-funder signal).

**Headline still robust** under the evidence-hardened vector (now 5 vectors tested):
v4_resolved_gapfill DePIN p = 0.0245 (significant); retention regressor n.s. (0.237). Maturity anchor 0.0395
and baseline 0.0409 reproduce reproduce.py exactly.

## Part 2: staking-PCA governance audit (directive 1)

For each excluded staking / vote-escrow aggregation, a cited WebSearch audit answered: do staked tokens
vote? is voting dispersed (per-staker custody) or bloc (contract/operator/validator)? Full findings in
`staking_audit/governance_findings_2026-05-30.json`.

| verdict | protocols | rationale |
|---|---|---|
| EXCLUSION QUESTIONABLE (should be IN HHI) | LPT | Livepeer bonding delegates stake to transcoders who vote the bloc -> genuine concentration, not custody |
| NEEDS AUTHOR DECISION | CRV, ENA, POL, IOTX, GEOD | staked tokens vote; excluding the contract from a raw-token HHI hides concentrated insider stake and/or creates a unit mismatch (the governance unit is the ve/staked token, not the raw token); high insider-staking risk |
| EXCLUSION CORRECT (with attribution caveat) | AAVE, FXS, ETHFI, GNO, GMX, ANYONE, MPL_SYRUP | voting dispersed per-staker (verified e.g. in Aave GovernanceStrategy code: power attaches to the staker's own address); the contract is custody. BUT see the attribution gap below |

GEOD (the author's example) lands in NEEDS-DECISION with high insider risk, confirming the instinct: GEOD
staking carries governance and the exclusion should be reconsidered.

## Part 3: insider holdings locked in staking (directive 2)

Pulling the holder lists of the liquid staked tokens shows insider/team/founder tokens ARE locked inside
PCA-excluded staking contracts (`staking_audit/directive2_insider_stakers_2026-05-30.json`):
- **stkAAVE** (excluded from the AAVE HHI): ~20% of staked AAVE is held by Aave team multisigs (10.7% +
  5.1% + 2.7%) plus founder Stani Kulechov (1.9%), plus an 8.6% bare Safe. The AAVE-team-controlled MKR-style
  Safe pattern recurs.
- **sENA** (excluded from the ENA HHI): Ethena Labs (2.7%), founder Kain Warwick (2.0%), and Strobe Ventures
  (VC, 1.2%) are stakers; the bulk is Ethena protocol contracts (LP-staking + distributors).
- Method limit: sETHFI / stSYRUP / veFXS / veCRV returned no Nansen token-holder data (non-transferable
  ve-tokens / unindexed); confirming their insider-staking needs lock-event / deposit tracing (follow-on).

## The synthesized methodology finding (the load-bearing recommendation)

The two directives converge on a single refinement. The current method (exclude the staking contract,
compute the HHI on the raw token only) is right that a dispersed-custody staking contract is not one
governance actor, but it has two side effects:

1. **Insider stake vanishes.** Because the HHI counts only raw-token balances and excludes the staking
   contract, an insider who STAKES disappears from both the HHI and the insider count. Confirmed for AAVE
   (team + founder in stkAAVE) and ENA (team + founder + VC in sENA). The fix is ATTRIBUTION: add each
   holder's staked balance back to that holder's own address (stkAAVE -> the staker; sENA -> the staker),
   then exclude only the contract shell. This keeps dispersion correct while restoring insider visibility.
2. **Bloc-voting staking is real concentration.** Where the staking operator/validator/transcoder votes the
   aggregate (LPT; delegated-PoS-style), the contract should stay IN the HHI, not be excluded.
3. **Unit mismatch for ve-tokens.** For CRV/FXS the governance unit is veCRV/veFXS (per-locker), not raw
   CRV/FXS; a raw-token HHI both mis-measures and hides founder/team locks (e.g. Egorov's veCRV).

Recommended treatment, per protocol class:
- Dispersed staking, no insiders staked -> exclude (current behavior fine): mostly the "exclusion correct"
  row, after an attribution pass confirms no insider stake.
- Dispersed staking WITH insider stakers -> exclude the shell but re-attribute the insider-staked portion to
  the insider holders (AAVE, ENA, and likely FXS given high risk).
- Bloc-voting staking -> keep in HHI (LPT; re-examine GEOD/IOTX/POL delegation mechanics).

## Materiality and what is NOT changed

The headline (DePIN sector concentration) is robust under all five insider-retention vectors, so none of
this overturns the finding. The staking-attribution refinement most plausibly STRENGTHENS the insider-
concentration thesis (insiders are more concentrated than the raw HHI shows). But it changes published HHIs
and insider counts, so it is an author decision. This cycle changed no exclusions, no HHIs, and no v3/frame
values; it produced the evidence + the per-protocol recommendations.

## Open author decisions

1. Adopt the attribution pass (add staked balances back to holders; restore insider stake) for AAVE / ENA
   (confirmed) and audit FXS / ETHFI / GNO / GMX similarly.
2. Reclassify the bloc-voting staking (LPT, and re-examine GEOD/IOTX/POL) as in-HHI concentration.
3. Resolve the ve-token unit mismatch (CRV/FXS): measure concentration on veToken, not raw token.
4. Optional: spend remaining Nansen budget (~9,700 cr) on Solana survivor resolution, ve-token lock tracing,
   and Safe-deployer confirmation for the remaining high-share multisigs.
