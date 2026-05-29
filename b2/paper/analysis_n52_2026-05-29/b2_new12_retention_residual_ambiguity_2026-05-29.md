# New-12 insider-retention re-fetch: residual-ambiguity + provenance log

**As-of:** 2026-05-29. Companion to `new12_retention_vector_2026-05-29.csv` (the persisted
retention vector), `new12_retention_provenance_2026-05-29.json` (per-address classification),
and `b2_new12_retention_classify_2026-05-29.py` (the classifier). Reader MUST re-verify
against live canonical state before acting on any specific value.

## Method (cost-tiered; no premium-labels were needed)

Label sources, free-first then Nansen bulk:
1. Nansen `token_current_top_holders` (one labeled call per token; 2026-05-29) for entity labels.
2. phase4 `etherscan_labels.json` / `nansen_labels.json` (2026-05-27; FXS/SNX/GNO contract status).
3. `exclusions_log.csv` + the phase4 v2-audited set (what is already PCA-excluded).

Classification rule (consistent with the original-sample composition-shift framing):
INSIDER = team / founder / VC / early-investor allocation wallet NOT already PCA-excluded
(named VC or fund, named individual investor, "Investment Recipient"). NOT insider =
protocol-controlled contract / foundation / treasury / staking / custody (Class 2/3 PCA;
flagged if it leaked past exclusion, but still not an insider), CEX, market-maker, and any
unlabeled EOA or retail whale (conservative rule: no imputation).

## Resolved retention vector (insider_count_frac)

| token | insiders/10 | count_frac | basis |
|---|---|---|---|
| WLFI | 3 | 0.30 | Justin Sun + Aqua1 Foundation + ALT5 Sigma Treasury Strategy (strategic investors) |
| KMNO | 3 | 0.30 | three "KMNO Investment Recipient" survivors |
| ENA | 2 | 0.20 | "REZ Investment Recipient" + "ENA Investment Recipient" |
| FXS | 1 | 0.10 | Dragonfly Capital (VC fund) |
| SNX, GNO, PUMP, JTO, BONK | 0 | 0.00 | survivors are CEX / market-maker / retail whales / protocol contracts |
| DOT, TAO, ALGO | 0 | 0.00 | LOW CONFIDENCE: survivors are validators / treasury-residual / unattributed |

Pattern: retention is age-dependent. The newest tokens (WLFI, KMNO, ENA launched 2024)
retain strategic investors in the post-exclusion top-10; the mature tokens (FXS, SNX, GNO
at 6 to 9 years) have shed them. This refines the composition-shift interpretation; it is
immaterial to the headline (see sensitivity below).

## Headline robustness (the decisive check)

The retention-spec DePIN p is robust across the full plausible range of new-12 retention
vectors (all-zero, prose-estimate, high, extreme): DePIN p stays in 0.019 to 0.040, always
under 0.05, and the insider-retention coefficient is not significant in every scenario
(p 0.55 to 0.94). The classification judgment calls below therefore do not move the headline.

## Residual ambiguities (judgment calls; NOT counted as insider in the primary vector)

1. **FXS "Frax" / "Frax Finance" labeled EOAs** (`0x6fcfee4f...`, `0xd53e50c6...`): protocol-team
   vs operational. Treated as protocol (not insider). If counted as insider, FXS -> 0.30.
2. **WLFI "Jump Trading"** (`0xcc261ab4...`): market-maker vs strategic investor. Treated as
   market-maker (not insider). If counted, WLFI -> 0.40.
3. **DOT / TAO / ALGO**: low-confidence ~0. DOT also has a capture-provenance gap (the
   clone-A `DOT_holders.csv` top-1 is 132.8M = 9.92%, vs the S16 AssetHub canonical capture
   top-1 = 94.1M = 6.90%); the retention reads near zero under either capture because the
   survivors are validators / treasury-residual / unattributed.

## Exclusion-incompleteness flags (Class 2/3 leaked past the new-cohort exclusion set)

These are protocol-controlled addresses that survived into the post-exclusion top-10 but are
NOT insiders. They do not affect insider_count_frac and do not move the headline. They are
recorded for a future exclusion-tightening cycle (the new-cohort exclusion set is incomplete
relative to current Nansen entity labels):

- SNX: Synthetix Treasury (`0x99f4176e...`).
- ENA: Ethena Labs Proxy (`0x2146aa58...`) + three "Ethena Labs" protocol EOAs
  (`0xa5274a5a...`, `0x7462f0d9...`, `0xb2af9739...`).
- WLFI: Ecosystem fund (`0xfef30c26...`), Multisig (`0xf0cc01b3...`), Ethena-Labs WLFI
  Multisig (`0x29de8825...`), two SafeProxies.
- PUMP: five "pump.fun" custody addresses surviving in the top-10.
- JTO: JITO Staking Pool (`jjCAwuuN...`).
- KMNO: KMNO Staking (`Ec6MuWtp...`) + two KMNO Custody Vaults.

## Reconciliation to surface (claim of record + response letter; out of this cycle's scope)

The reproduced retention-spec DePIN p is **0.040**, not the prose-locked 0.014 to 0.016.
The finding holds (DePIN significant in both specs; insider-retention not significant = the
channel-shift), but the authoritative reproduced value supersedes the prose lock. The claim
of record (`handoff/dispatch/b2_r3_explanatory_model_reframe_2026-05-29.md` Section 7) and
the R2 response-letter draft should update from 0.014 to 0.016 to the reproduced 0.040. The
maturity-spec reproduces exactly at 0.0395, confirming the model machinery.
