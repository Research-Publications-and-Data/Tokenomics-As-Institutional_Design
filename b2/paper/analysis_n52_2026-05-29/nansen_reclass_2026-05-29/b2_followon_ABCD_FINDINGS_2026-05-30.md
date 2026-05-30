# B2 follow-ons A/B/C/D: findings

**As-of:** 2026-05-30T04:15:00Z. **Clone:** clone-A. Nothing pushed. Frame + v3 untouched.
**Reader MUST** run `python3 scripts/claude-code-sync.py` + grep canonical before acting.

Executed all four follow-ons from the staking-audit handoff, per author direction to spend the Nansen
budget. The big result: the deeper evidence both HARDENS the classification and corrects it in BOTH
directions, and the headline stays robust across the now-six-vector range. Recommended classification of
record is now `v4_traced` (the most evidence-based).

## Follow-on C: Safe team-ownership traces (the most consequential)

Traced 17 high-share bare Safes via Nansen deployer/signer relations. The "any multisig = insider" keyword
heuristic OVERCOUNTS: only 6 of 17 are protocol-team Safes; 11 are independent whales' Safes.
- TEAM-CONFIRMED (insider): COMP#5 (Compound Timelock signers), GMX#4/#7 (gmxresearch.eth = GMX team),
  MKR#5 (MakerDAO DeFi Manager), ZRO#1/#5 (LayerZero multisig); plus the earlier MKR#1 (MakerDAO Delegator)
  and DIMO#1 (dinc.eth).
- INDEPENDENT (NOT insider): DIMO#2/#4/#8 (deployed by an OpenSea-handle / unlabeled EOAs), GEOD#5/#6
  (deployed by a "Token Millionaire" retail whale), MKR#3, MOR#3/#4/#5, WXM#3/#5 (unlabeled/generic
  deployer EOAs).

Evidence-based correction (`insider_retention_vector_v4_traced_2026-05-30.csv`): DIMO 0.4->0.1, GEOD
0.3->0.1, MKR 0.3->0.2, MOR 0.5->0.2, WXM 0.4->0.2. Four of the five lowered tokens are DePIN; the keyword
rule had inflated DePIN insider-retention by counting independent whales' Safes as team.

## Follow-on A: Solana survivor resolution

Deeper top-holder pages (ranks 25-75) + entity counterparty traces resolved/characterized the ambiguous
Solana survivors. ALL are exchange / custody / retail, NONE are hidden insiders:
- HNT#8 = HNT Custody Vaults; JUP#7 = Bitget; JUP#8 = OKX; JUP#5 / HNT#10 = retail.
- GRASS#1 (16%): "excessively high trade activity" (CEX/market-maker hot-wallet signature); W#1 (6.5%)
  funded by Upbit; DRIFT#2 (5.5%) routes to Coinbase.
Conclusion: the conservative not-insider rule held on Solana; no insider undercounting. (Several GRASS
survivors churned out of the current top-50 entirely; they are not current entities.)

## Follow-on B: ve-token lock tracing

- veFXS: the top FXS locker is "Frax Finance: fraxcetacean.eth" (3.5M FXS) = a Frax team/protocol address.
  CONFIRMS insider FXS locked in vote-escrow (validates the high insider-staking-risk verdict for FXS).
- veCRV: the dominant counterparty is Convex Finance Voter Proxy (1.8M CRV) = a meta-governance bloc
  aggregator; veCRV voting concentrates partly via Convex/vlCVX. LIMITATION: founder (Egorov) + original
  team/investor locks predate the 1-year counterparty window and are not surfaced by flow analysis; a
  balance-based veCRV snapshot or long-window lock-event pull is needed to size them.

## Follow-on D: staking attribution pass (quantified)

Quantifying the insider stake hidden inside the PCA-excluded staking contracts:
- AAVE: stkAAVE holds 21.67% of AAVE supply; ~20.5% of stkAAVE is Aave team multisigs + founder Stani
  Kulechov -> ~4.4% of AAVE supply (up to 6.3% incl the 8.6% bare Safe) is insider AAVE HIDDEN by the
  wholesale stkAAVE exclusion. Attributing it back materially raises AAVE measured insider concentration.
- ENA: sENA holds 7.27% of ENA supply; ~5.9% insider (Ethena Labs + Kain Warwick + Strobe) -> ~0.43% of
  ENA supply insider-staked (smaller).
This confirms the attribution recommendation: add staked balances back to holders before excluding the
contract shell, so insider stake is not erased. AAVE is the material case.

## Headline: robust across all six vectors

| vector | DePIN p | sig | ret p |
|---|---|---|---|
| baseline_v3 | 0.0409 | YES | 0.49 |
| v4_keyword | 0.0062 | YES | 0.084 |
| v4_reviewed | 0.0274 | YES | 0.31 |
| v4_reviewed_safe | 0.0168 | YES | 0.18 |
| v4_resolved_gapfill | 0.0245 | YES | 0.24 |
| v4_traced_evidence | 0.0119 | YES | 0.24 |

DePIN significant under every vector; retention regressor n.s. throughout (channel-shift holds). The traced
evidence actually STRENGTHENS the DePIN coefficient (lowering independent-whale Safes sharpens the sector
signal). Maturity anchor 0.0395 reproduces reproduce.py.

## Recommended classification of record + remaining items

- Adopt `v4_traced` (Safe-trace-corrected) as the insider classification of record; it is the most
  evidence-based and supersedes v4_resolved on the 5 corrected tokens.
- AUTHOR DECISIONS still open: the staking ATTRIBUTION pass (AAVE material at ~4-6% hidden insider; ENA/FXS
  smaller); LPT bloc-voting -> in-HHI; CRV/ENA/POL/IOTX/GEOD staking-exclusion reconsideration; ve-token
  unit mismatch. None changes the headline.
- Remaining method limitations (need different data, not more of the same calls): veCRV founder/team locks
  (balance snapshot or long-window lock events); the fully-churned GRASS survivors (no current entity).

## Credit usage

This follow-on round: ~40 Nansen calls (~6,000 cr) on top of the ~2,000 from the prior round = ~8,000 cr of
the budget; the rest ran on free Blockscout/WebSearch. Comfortably within budget.
