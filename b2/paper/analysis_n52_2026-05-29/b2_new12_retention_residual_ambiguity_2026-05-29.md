# New-12 insider-retention re-fetch: residual-ambiguity + provenance log

**As-of:** 2026-05-29. Companion to `new12_retention_vector_2026-05-29.csv` (the persisted
retention vector), `new12_retention_provenance_2026-05-29.json` (per-address classification),
and `b2_new12_retention_classify_2026-05-29.py` (the classifier). Reader MUST re-verify
against live canonical state before acting on any specific value.

## Insider definition (matches the original sample)

Anchored to `analysis/03_insider_classification.py` line 127, which defines insider among
the post-exclusion top-10 survivors as: team, investor, founder, vest, foundation, treasury,
multisig, deployer, grant. This re-fetch applies the SAME definition to the new-12 survivors:
INSIDER = team / founder / co-founder / investor (VC/fund) / Investment Recipient /
foundation / treasury / attributed multisig (Safe) / vesting. NOT insider = CEX/exchange
(including exchange-class custody hot wallets), market-maker, bridge / escrow / staking-pool /
vault aggregation / token-proxy contract, unlabeled EOA / retail whale.

An earlier draft of this re-fetch was too strict (it treated surviving foundation/team/
treasury/multisig addresses as not-insider "exclusion leaks"); that undercounted relative to
the original methodology (which counts them, e.g. DIMO and META at 10/10). Corrected here.

## Scope: HHIs UNCHANGED (this is the S2 boundary)

This reclassifies the LABELS of post-exclusion SURVIVORS only. The PCA-exclusion set and the
published HHIs are untouched. The big foundation/treasury/co-founder addresses already in the
exclusion set stay excluded (they never enter the survivor top-10). Separately re-adjudicating
those (the S3 un-exclusion: GNO co-founder Safes, PUMP team 80B/35B, WLFI Foundation/team) is
an author-owned PCA-methodology decision recorded below, NOT applied here.

## Resolved retention vector (insider_count_frac)

| token | insiders/10 | count_frac | basis (surviving insiders) |
|---|---|---|---|
| WLFI | 7 | 0.70 | Justin Sun + Aqua1 Foundation + ALT5 Sigma Treasury + WLFI Multisig + Ethena-Labs WLFI Multisig + 2 bare SafeProxies |
| ENA | 5 | 0.50 | 3 Ethena Labs protocol-team EOAs + REZ Investment Recipient + ENA Investment Recipient |
| FXS | 3 | 0.30 | Dragonfly Capital (VC) + 2 Frax-protocol-team/treasury EOAs |
| KMNO | 3 | 0.30 | 3 KMNO Investment Recipients |
| SNX | 1 | 0.10 | surviving Synthetix Treasury |
| GNO | 1 | 0.10 | surviving Gnosis Multisig (co-founder Safes stay PCA-excluded under S2) |
| PUMP, JTO, BONK | 0 | 0.00 | survivors are CEX / exchange-class custody / staking-pool / retail whales |
| DOT, TAO, ALGO | 0 | 0.00 | LOW CONFIDENCE: survivors are validators / treasury-residual / unattributed |

Pattern: retention is age-dependent. Newest tokens (WLFI, ENA, KMNO launched 2024) retain
team/foundation/investor allocations in the post-exclusion top-10; mature tokens (FXS, SNX,
GNO at 6 to 9 years) retain little. Consistent with the composition-shift interpretation.

## Headline robustness (the decisive check)

HHIs are unchanged, so the retention values (which rose materially under this correction) do
NOT move the DePIN significance: maturity-spec DePIN p = 0.0395 (exact reproduction), retention-
spec DePIN p = 0.0409 (significant), insider-retention coefficient not significant (p = 0.49,
the channel-shift), balanced-30 Mann-Whitney p = 0.0202 (published, robust). An adversarial
stress-test (4003 retention vectors) could not push the DePIN p to 0.05 with the HHIs fixed.

## Residual ambiguities (lower-confidence calls; flagged for sensitivity)

1. **FXS "Frax" / "Frax Finance" labeled EOAs** (`0x6fcfee4f...`, `0xd53e50c6...`): counted
   insider as foundation/treasury operational holdings. If treated as not-insider, FXS -> 0.10.
2. **WLFI two bare "SafeProxy" addresses** (`0x33ccf78a...`, `0x284cf133...`): counted insider
   per the multisig rule, but unattributed. If dropped, WLFI -> 0.50.
3. **DOT / TAO / ALGO**: low-confidence ~0. DOT also has a capture-provenance gap (clone-A
   `DOT_holders.csv` top-1 = 132.8M = 9.92% vs the S16 AssetHub canonical top-1 = 94.1M =
   6.90%); retention reads near zero under either capture (validators / treasury-residual /
   unattributed survivors).

## S3 (author-owned PCA-methodology decision; NOT applied this cycle)

Un-excluding the named co-founder/team allocation pools from the HHI (treating them as insider
holders rather than Class-2 PCAs) is defensible under the same "team = insider" principle but
changes the PUBLISHED HHIs and is out of this dispatch's scope:
- GNO co-founder Safes (Stefan George `0x9d94ef33...`, Köppelmann `0xae5fb390...`): GNO HHI
  0.042 -> 0.074; GNO retention -> 0.20.
- PUMP team allocation (`8uhb...` 80B, `9pkf...` 35B): PUMP HHI 0.040 -> 0.065.
- WLFI Foundation/team allocation (`0x4af891...`): WLFI HHI 0.156 -> 0.135.
Consequence if applied (S3): the retention-spec primary (0.042) and the balanced-30 Mann-Whitney
(0.045) stay significant, but the maturity-spec robustness anchor goes to 0.0510 (just over
0.05). Un-excluding ALL Class-2 foundation/treasury (S4) collapses the finding (DePIN p 0.19 to
0.37) and is NOT viable: the big foundation/treasury MUST remain PCA-excluded for the paper's
methodology. The original-sample (v3) retention may also understate any protocols whose
co-founder personal Safes were excluded as Class-2; a dedicated cross-sample audit is the right
venue for the S3 boundary.

## Reconciliation to surface (claim of record + response letter; out of this cycle's scope)

The reproduced retention-spec DePIN p is **0.0409**, not the prose-locked 0.014 to 0.016. The
finding holds (DePIN significant in both specs; insider-retention not significant), but the
reproduced value supersedes the prose lock. The claim of record (reframe Section 7) and the R2
response-letter draft should update to the reproduced 0.041 (retention-spec) alongside the
maturity-spec 0.0395.
