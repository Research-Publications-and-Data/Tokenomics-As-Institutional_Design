# Resolution of the remaining audit gaps (G3-G8 + IO/DOT residuals)

**As-of:** 2026-05-29. Closes out every remaining gap from
`b2_insider_pca_retention_AUDIT_2026-05-29.md` and the consolidation residuals. Each is RESOLVED,
DOCUMENTED (provenance recorded), or SURFACED (author decision, with quantified impact). Reader
MUST re-verify. No regression-frame mutation (the live frame has uncommitted parallel changes).

## RESOLVED (verified; no action needed)

### G3 -- UNI full-HHI disagreement, and v3 full_hhi vs raw
- **UNI:** raw full HHI (clone-A holder list) = 0.10084 (the 0x000...dead burn at ~11 percent
  dominates); v3 `full_hhi` = 0.0322 (burn-excluded, the correct "full" metric); post-exclusion
  (regression) = 0.0098. gov_conc `hhi` = 0.0100 is the ANOMALY: for UNI alone it holds the
  post-exclusion value where every other protocol's gov_conc holds the full HHI (== v3
  `full_hhi`). v3's 0.0322 is correct; gov_conc's UNI cell is an isolated data error in a
  non-analysis-of-record file. No impact on the regression or de-tautology.
- **v3 full_hhi is NOT stale:** it is the baseline-adjusted full HHI (canonical-burn / dominant
  protocol contract removed), so it legitimately differs from a raw all-holders recompute for
  protocols with a dominant burn/contract (AAVE, UNI, GMX) and matches for those without (COMP,
  JUP, HNT). Not a capture-staleness gap.

### G5 -- de-tautology sample includes GTC/TEC (not in the regression frame)
Immaterial: de-tautology Spearman rho = 0.544 (p=0.0009, N=34, with GTC/TEC) vs 0.546 (p=0.0012,
N=32, frame-consistent without them). Identical conclusion. The de-tautology is intentionally
anchored to the original v3 sample; the 2 extra protocols do not change it.

## DOCUMENTED (provenance recorded; raw-reproducible from the recorded source)

### IO -- documented HHI 0.1251 (raw-from-clone-A gives 0.0786)
The IO regression HHI is the R2-calibration value (2026-05-18; top-100 rescaled to actual
circulating supply; Gini 0.9467, top-1 30.0 percent, top-10 63.7 percent, per the Phase-0 Tier-A1
memo). The clone-A `IO_holders.csv` is a different (un-rescaled, 84.9k-holder) capture, so a raw
recompute gives 0.0786. Method-of-record: the R2 calibration. To make it raw-reproducible, persist
the rescaled top-100 holder list used for the calibration.

### DOT -- documented HHI 0.0052 (raw-from-clone-A gives 0.0139; S16 AssetHub post-PCA was 0.0093)
The DOT regression HHI is from the AssetHub Subscan capture with the Binance-cluster Class-5
exclusion (`dot_pca_refined`), the "primary" of three documented DOT values (raw 0.0090 /
Classes-2+3-only 0.0093 / Binance-cluster-excluded 0.0052). Clone-A `DOT_holders.csv` is the
relay-chain-residual capture (top-1 132.8M), not AssetHub, so a raw recompute gives 0.0139.
Capture-of-record: AssetHub Subscan. To make it raw-reproducible, persist the AssetHub top-1000 +
the Binance-cluster address list.

## NOT COMPUTABLE FROM PERSISTED DATA (re-derivation required; documented limitation)

### G4 -- non-insider HHI for AXL/MOR/ZRO (supply_corrected rows; de-tautology N=34 not 37)
`non_insider_hhi_approx` is blank for these three. Computing it needs the per-address insider
flags, which are NOT persisted (insider_classification.csv `final_classification` is blank for
AXL/MOR/ZRO; only Tier-1 exchange tags exist). Immaterial to the de-tautology (rho stable ~0.545
at N=32-34). A clean fill requires re-deriving their insider classification (a re-fetch cycle,
like the new-12).

### G6 -- the original 37-protocol insider classification is not row-re-auditable
v3's per-address insider determinations came from the Tier-2/3 manual review in
`analysis/03_insider_classification.py`; the saved `insider_classification.csv` carries only the
Tier-1 (exchange) tags. The insider DEFINITION matches the new-12 S2 correction
(team/investor/founder/foundation/treasury/multisig), but per-protocol row-equality with the
original is not independently verifiable. Full re-audit = re-deriving the original 37 (a separate
cycle); the new-12-to-original consistency is definitional, established here.

## SURFACED (author decision; quantified)

### G7 + G8 -- the foundation/team/multisig boundary (PCA-exclude vs insider-retain)
These are ONE decision. The new-cohort post-exclusion top-10 contains protocol-controlled
Class-2/3 addresses (WLFI Ecosystem + multisigs, ENA Ethena-Labs EOAs, PUMP pump.fun custody,
KMNO staking + vaults, JTO staking). Two self-consistent treatments:
- **Current (S2):** keep them in the HHI and count them as insider retention.
- **PCA-strict (tighten = S3-direction):** exclude them as Class-2/3; they leave the HHI and the
  retention count.

Tightening is the methodology-consistent reading (PCA excludes Class-2/3) AND it STRENGTHENS the
headline:

| spec | current | tightened (leaks excluded) |
|---|---:|---:|
| maturity-spec DePIN p | 0.0395 | 0.0140 |
| retention-spec DePIN p | 0.0409 | 0.0107 |
| balanced-30 Mann-Whitney | 0.0364 | 0.0201 |

It lowers the inflated DeFi HHIs (WLFI 0.156 -> 0.066, PUMP 0.040 -> 0.032, KMNO 0.031 -> 0.027,
ENA 0.047 -> 0.045; SNX/JTO ~flat), widening the DePIN-DeFi gap. The cost is a substantial change
to WLFI's published HHI and a re-derivation of WLFI/ENA/KMNO retention (the excluded addresses
leave the insider count). Author decision: adopt the PCA-strict tightening (stronger, methodology-
consistent, but changes published HHIs + retention) or keep the current set (document the leaks as
a known incompleteness). This is the same boundary as the GNO co-founder S2/S3 question.

## Net

Of the remaining gaps: G3, G5 resolved (no action); IO, DOT documented (provenance + raw-repro
path recorded); G4, G6 are not computable without a re-derivation cycle (data not persisted);
G7/G8 surfaced as a single author decision with the quantified finding that the methodology-
consistent tightening STRENGTHENS the headline (DePIN p 0.040 -> 0.014). No arithmetic errors
remain in the insider, PCA, or retention calculations; the open items are provenance, optional
re-derivation, and the one foundation/team boundary decision.
