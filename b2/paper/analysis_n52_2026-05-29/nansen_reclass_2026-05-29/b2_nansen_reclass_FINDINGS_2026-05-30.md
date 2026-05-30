# B2 Nansen 45-protocol insider re-classification: findings

**As-of:** 2026-05-30T03:25:04Z. **Clone:** clone-A `/Users/zach/Tokenomics-As-Institutional_Design`
(`b2/paper/analysis_n52_2026-05-29/nansen_reclass_2026-05-29/`). Nothing pushed.
**Reader MUST** run `python3 scripts/claude-code-sync.py` and grep current canonical files for any
cited identifier before acting; canonical + dataset state advances across parallel sessions.

## What this cycle did

Executed the high-value Nansen campaign scoped in `b2_nansen_quality_samplesize_SCOPE_2026-05-29.md`:
re-classify every Nansen-reachable B2 frame protocol's post-exclusion top-10 survivors against current
Nansen entity labels, to close the audit's classification + exclusion-auditability gaps (G4 / G6 / G7)
and to test whether the headline is sensitive to the insider-classification methodology.

Coverage: 45 of the 52 frame protocols are Nansen-reachable. 7 are off-Nansen (native/unsupported
chains: HYPE, FIL, POKT, ALGO, DOT, TAO, TEC) and keep their existing classification.

Pipeline (all reproducible; scripts in this directory):
1. `b2_nansen_contract_map_2026-05-29.json` token contracts (15 from CoinGecko platforms, 30 via Nansen
   `general_search`; MPL_SYRUP split MPL + SYRUP).
2. `survivors_2026-05-29.json` post-exclusion top-10 survivors per token, recomputed from raw holder
   lists minus the right exclusion set (new12_unified for the 9 new-cohort, exclusions_log for the rest).
   Validated: ENA / WLFI / PUMP top-shares reproduce the prior session's provenance to 6 decimals.
3. `nansen_raw/<TOKEN>.md` raw Nansen top-holder pulls (`token_current_top_holders`).
4. `b2_nansen_insider_classification_v4_2026-05-29.csv` Tier-1 keyword classification (the original
   `analysis/03_insider_classification.py` line-127 rule) joined to the Nansen labels.
5. `b2_nansen_insider_classification_v4_REVIEWED_2026-05-29.csv` adversarial per-token review (35 reasoning
   agents) that adjudicates each survivor against its actual entity label with an expanded ruleset.
6. `b2_nansen_v4_reconciliation_2026-05-29.csv` reconciliation of v3 vs keyword vs reviewed.
7. `b2_nansen_v4_headline_impact_*` the four-way retention-spec re-estimation.

## Credit usage

~9,900 Nansen credits (150/pull). Optimized from the naive ~13,800: 30 tokens at top-50 (2 pages, before
the credit-reduction directive), 6 final tokens at top-25 (1 page), the 9 new-cohort reused from the prior
session's provenance at zero cost, GTC skipped (out-of-frame Social_Dead). The per-pull price (150) is
Nansen-fixed; all reduction was call-count. No premium-label (500cr) spend; decision-flippers surfaced
below instead of auto-resolved.

## HEADLINE RESULT (load-bearing): the finding is ROBUST

The DePIN governance-concentration coefficient is significant (p < 0.05) under every insider-retention
vector. The harness reproduces `reproduce.py` exactly (baseline DePIN p 0.0409; maturity anchor 0.0395),
which validates it.

| retention vector | N | DePIN b | DePIN p | significant | retention p |
|---|---|---|---|---|---|
| baseline_v3 | 49 | +0.691 | 0.0409 | YES | 0.49 |
| v4_keyword (Tier-1 floor) | 50 | +0.788 | 0.0062 | YES | 0.084 |
| v4_reviewed (full) | 50 | +0.667 | 0.0274 | YES | 0.31 |
| v4_reviewed_safe (v3 retained where match < 7/10) | 50 | +0.697 | 0.0168 | YES | 0.18 |

The insider-retention regressor is NOT significant under any vector: the channel-shift finding (DePIN
sector effect real; insider-RETENTION not the channel) holds throughout. Despite 28 tokens diverging from
v3 and 46 flagged judgment calls, none move the headline. v4 also fills HONEY's previously-missing
retention vector, lifting the retention-spec from N=49 to N=50.

## Classification reconciliation (the substantive finding)

v4-reviewed diverges from v3 on 28 of 36 pulled tokens (13 up, 15 down), confirms 6, reuses 9
(new-cohort), and is unreliable on 2 (low match, see vintage gap). The divergence is real and two-sided:

- The Tier-1 keyword rule (v3's automated layer) is a LOWER BOUND. It misses entities the review caught:
  Safe / SafeProxy / Gnosis Safe (= multisig), "Custody Vaults" / "Token Vault" (= team treasury), named
  VC funds (a16z on UNI, Variant, ParaFi, Lightspeed, KR1), and named founders (Nick Johnson on ENS,
  Geoffrey Hayes on COMP, Nikolai Mushegian on MKR).
- v3 OVER-counts in places. HNT v3=0.5 but its survivors are all exchanges (Bybit, Crypto.com, Binance US,
  Kraken) plus HNT distributors and retail (v4 = 0.1). DIMO v3=1.0 and META v3=1.0 both include bare /
  retail survivors (v4 = 0.3 / 0.4).

Biggest movers (v3 -> reviewed): DIMO 1.0->0.3, META 1.0->0.4, MPL_SYRUP 0.1->0.6, HNT 0.5->0.1,
JUP 0.4->0.0, ZRO 0.3->0.7, ANYONE 0.4->0.1, LDO 0.1->0.4.

## Vintage gap (a methodological caveat to record)

Current Nansen top-holders are a May-30 snapshot; the holder lists are an April capture. For tokens with
sticky top holders the match is high (most tokens 8-10/10 survivors found in the current Nansen top set).
Two tokens churned: MKR (0/10 survivors in the current Nansen top-50) and GRASS (1/10). For these, v4 is
unreliable and v3 is retained (the `v4_reviewed_safe` vector). This is the right reliability discipline:
v4 is a current-Nansen re-classification, accurate where the cap table is stable, weak where it churned.

## Decision-flippers (46; surfaced, not resolved)

Full list in `b2_nansen_v4_flags_and_flippers_2026-05-29.json`. Recurring ambiguity classes:
- Bare unattributed Safe / SafeProxy / Multisig (DIMO, GMX, LPT, MOR, WXM, ENS): counted insider on the
  "any multisig = team-controlled" rule but could be a third-party holder's Safe. Each moves frac by 0.1.
- "Custody Vaults" / "Token Vault" (DRIFT, META, MPL_SYRUP, RENDER, JUP, GEOD): team custody vs DeFi
  user-deposit vaults. MPL_SYRUP rank-1 "SYRUP Custody Vaults" (6.95%) is the single largest such call.
- Named-entity identification (ARB / Lightspeed, COMP / Geoffrey Hayes, UNI / a16z, LDO / KR1): rests on
  recognizing the entity, not on the literal label.
- DePIN reward distributors (ANYONE Relay Rewards): team-provisioned emission pools vs distributor
  contracts; the rule puts them non-insider, but it is a boundary call.
- ZRO bare "LayerZero [0x...]" tags (ranks 2/8/10): protocol-team-controlled per Nansen entity tag but
  possibly operational (relayer/executor); swings ZRO between 0.4 and 0.7.

These are author calls. None changes the headline (robust under all vectors). Premium Nansen labels (500cr)
would resolve some; not spent this cycle.

## De-tautology

v3 de-tautology of-record (reproduce.py STAGE 8): Spearman rho 0.544, p 0.0009, N=34. The v4 de-tautology
was NOT computed this cycle: verification showed v3's `non_insider_hhi_approx` is not
`full_hhi - insider_hhi_contribution` (max abs err 0.145), so the naive reconstruction is the wrong
formula. A valid v4 de-tautology needs v3's exact non-insider-HHI methodology; flagged as a follow-on in
`b2_nansen_v4_detautology_2026-05-29.json`. The headline does not depend on it.

## Open author decisions (none applied; frame + v3 untouched)

1. Whether to adopt the v4-reviewed insider vector as the classification of record (recommended:
   `v4_reviewed_safe`, which retains v3 for the two vintage-gap tokens). The headline is robust either way;
   this is about the auditability + source-citation of the retention vector, not the result.
2. The 46 decision-flippers (above): which ambiguity calls to lock, and whether to spend premium Nansen
   labels to resolve the high-share ones (MPL_SYRUP custody vault, GEOD token vault, the bare Safes).
3. The v4 de-tautology follow-on (recompute under v3's non-insider-HHI method).

## Out of scope this cycle

- No writes to `data/processed/regression_data_april2026.csv` (it carried uncommitted parallel-session
  changes all session) or to `insider_analysis_results_v3.csv`. v4 is versioned alongside, never over it.
- No PCA-exclusion-set changes (G7 confirmation via labels is recorded in the per-survivor entity_type
  field; tightening exclusions changes published HHIs and is an author decision).
- The 7 off-Nansen protocols stay on their native-explorer lane.
