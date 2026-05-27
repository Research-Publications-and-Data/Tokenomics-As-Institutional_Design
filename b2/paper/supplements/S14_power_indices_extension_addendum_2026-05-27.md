# Supplementary File S14 Addendum: GMX + ENS Tally Extension (N=13 closure on EVM-side)

**Companion to:** `S14_power_indices_extension.md` (PID 4300 cycle 1, same date 2026-05-27).
**Generated:** 2026-05-27 (PID 4300; B2 R3 omnibus Phase 1 continuation; sister-cycle to S14 initial extension).
**Data source:** Tally GraphQL API delegates endpoint; top-100 by votes per protocol; 200 new rows appended to `data/raw/tally_delegates.csv` (backup at `.pre_gmx_ens_extension_2026-05-27`).

---

## Executive summary

S14 cycle 1 achieved N=11 cross-source observations (5 Tally + 6 Snapshot); 2 Tally protocols (GMX, ENS) and 3 Solana protocols (HNT, DRIFT, JUP) remained for N=13 dispatch-target closure. This addendum closes the GMX + ENS gap via Tally API, extending the cross-source sample to N=13 observations across 9 distinct EVM protocols (10 distinct EVM-side protocols when DIMO is included as Snapshot-only).

**Acceptance test PASS at N=13 cross-source:**
- Pearson r (Share-HHI vs SS-HHI) = **0.9761** (p < 0.001)
- Spearman rho = **0.9835** (p < 0.001)
- Pearson r (Share-HHI vs BZ-HHI) = **0.9738**
- Acceptance threshold > 0.95: **PASS**

**N=13 distinct-protocol target (dispatch original framing):** 10 of 13 EVM-side protocols computed (AAVE, COMP, UNI, ARB, OP, GMX, ENS + DIMO, LDO, WXM); 3 Solana protocols (HNT, DRIFT, JUP) remain for VSR / setvote reconstruction in continuation dispatch.

---

## New findings (GMX + ENS)

### Finding I: GMX moderate SS-share amplification (+2.93pp; NEW)

GMX top-1 delegate exhibits structural pivotal-power amplification:
- Share top-1: 19.50%
- SS top-1: **22.44%** (+2.93pp divergence)
- BZ-HHI: 0.0865 (similar magnitude to SS-HHI 0.0914)

The pattern sits between the high-amplification anchor (AAVE +4.80pp) and the low-amplification cluster (UNI/ARB/OP/COMP/ENS all <1pp). GMX has fewer top delegates with similar weight magnitudes than UNI/ARB/OP, producing more frequent pivotal-permutations for the top-1 delegate.

**Significance for §4.5 framing:** GMX is currently classified DISPERSE in Table 6 (voting-HHI 0.057 vs holding-HHI implicit; 0.87x ratio). The SS-share amplification reveals that GMX's dispersion is REAL at the voting-HHI / Herfindahl axis but the top-1 delegate retains moderate pivotal-power above their share. This is sister to the WXM structural-majority case (S14 Finding B; SS=1.000) but at a much smaller magnitude.

### Finding J: ENS minimal SS-share amplification (+0.29pp; replicates UNI pattern)

ENS top-1 delegate (fireeyesdao.eth) holds 7.67% share with SS top-1 7.96% (+0.29pp divergence; smallest in N=13 sample).

The pattern matches UNI Tally (+0.20pp; top-1 6.99% share / 7.00% SS). Both protocols have broadly-distributed delegate weight at the top such that no single delegate is pivotal in materially more permutations than their share would predict.

**Significance for §4.5 framing:** ENS's DISPERSE classification (Table 6 ratio 0.45x) is reinforced from a sister angle: not just low voting-HHI but low pivotal-power amplification means ENS top delegates have neither concentrated weight nor disproportionate pivotal power. Strongly DISPERSED across both axes.

---

## Full N=13 cross-source results table

| Protocol | Source | N | Share-HHI | SS-HHI | BZ-HHI | SS top-1 | Share top-1 | SS-share pp |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| AAVE | Tally | 100 | 0.0756 | 0.0978 | 0.1268 | 26.71% | 21.91% | +4.80 |
| COMP | Tally | 100 | 0.0387 | 0.0431 | 0.0410 | 12.76% | 11.80% | +0.95 |
| UNI | Tally | 100 | 0.0271 | 0.0279 | 0.0278 | 6.99% | 6.80% | +0.20 |
| ARB | Tally | 100 | 0.0355 | 0.0375 | 0.0383 | 11.36% | 10.40% | +0.95 |
| OP | Tally | 100 | 0.0330 | 0.0347 | 0.0341 | 10.60% | 10.03% | +0.56 |
| **GMX** | Tally | 100 | 0.0768 | **0.0914** | 0.0865 | **22.44%** | 19.50% | **+2.93** |
| **ENS** | Tally | 100 | 0.0283 | 0.0291 | 0.0282 | 7.96% | 7.67% | +0.29 |
| UNI | Snapshot | 100 | 0.0677 | 0.0698 | 0.0701 | 12.78% | 17.20% | +0.82 |
| COMP | Snapshot | 100 | 0.0531 | 0.0606 | 0.0639 | 18.00% | 25.00% | +2.25 |
| LDO | Snapshot | 100 | 0.0880 | 0.0969 | 0.0950 | 20.06% | 11.40% | +2.20 |
| DIMO | Snapshot | 10 | 0.2280 | 0.2326 | 0.2252 | 30.07% | 29.50% | +0.56 |
| WXM | Snapshot | 100 | 0.4861 | **1.0000** | **1.0000** | **100.0%** | 74.00% | **+30.85** |
| ARB | Snapshot | 100 | 0.0523 | 0.0549 | 0.0549 | 12.48% | 9.90% | +1.00 |

(Bold rows: structural-majority WXM + new GMX moderate-amplification finding.)

---

## Updated amplification typology candidate (per Findings I + B replication)

The S14 cycle 1 Finding B (WXM structural-majority) + this addendum's Finding I (GMX moderate amplification) suggest a refined §4.5 amplification typology:

| Class | Pattern | SS-share divergence | Sample example(s) |
|---|---|---:|---|
| **Structural-majority** | Top-1 holds absolute majority of votes; SS=100% mechanically | +30pp+ | WXM (74% share top-1; SS=100%) |
| **Coordinated-amplification** | Top-1 is dominant + second-tier disparate, frequent pivotal-permutations | +3 to +5pp | AAVE (Tally; +4.80), GMX (Tally; +2.93), COMP (Snapshot; +2.25), LDO (Snapshot; +2.20) |
| **Track-share** | Top-1 weight + N voters' weight distribution closely match | +0 to +1pp | UNI, ARB, OP, COMP (Tally), ENS, DIMO, WXM-but-COMP-cross |

Worth surfacing in §4.5 + §4.6.1 as 3-class refinement of the binary amplification-vs-dispersion typology. Current §4.5 prose uses "9 of 13 amplify; 4 disperse" framing; refined typology distinguishes WHICH KIND of amplification + WHICH KIND of dispersion.

---

## Cross-references

- **S14** (cycle 1 same date; N=11 cross-source extension; this addendum closes GMX + ENS gap to N=13)
- **S11** (5-Tally baseline; preserved as historical-of-record)
- **§4.5** Amplification finding (current "predominant" framing; refined typology candidate per this addendum)
- **§4.6.1** Voting-HHI methodology (potential 3-class typology subsection candidate)
- **§5.7 #5** HHI vs pivotal voting power (closed for EVM-side at N=13; 3 Solana protocols remain)
- **§5.8 #4** Coalition-based power indices (closed for EVM-side; Solana remainder)

---

## Pending continuation work

- 3 Solana protocols (HNT, DRIFT, JUP) require VSR position reconstruction or setvote parsing
  for full N=13 distinct-protocol closure
- Quorum-variation extension to 0.33 / 0.40 / 0.50 / 0.60 / 0.67 / 0.75 across full N=13
  (S11 has 5-protocol quorum-variation precedent; identical methodology)

Both deferred to continuation dispatch (`handoff/dispatch/b2_r3_data_collection_omnibus_continuation_2026-05-27.md` Phase 1 remainder spec).

---

## Author note

This addendum integrates author-provided Tally API access enabling on-demand delegate-weight pulls. The Tally API key is treated as ephemeral session secret per security discipline: never committed to git, never logged to repo, used only in `TALLY_API_KEY` environment variable for runtime queries. Future Tally extension cycles (Phase 2 protocols requiring on-chain Governor data; sister Compound/AAVE refresh) can use the same access pattern.

Author: Claude Code session 2026-05-27 (PID 4300); workflow clone `/Users/zach/Tokenization_Systems_Website`; sibling clone `/Users/zach/Tokenomics-As-Institutional_Design`.
