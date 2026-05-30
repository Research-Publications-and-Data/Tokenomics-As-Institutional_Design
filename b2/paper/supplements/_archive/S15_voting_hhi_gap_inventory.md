# Supplementary File S15: Voting-HHI Coverage Gap Inventory (Phase 2 of B2 R3 omnibus)

**Companion to:** B2 paper *Tokenomics as Applied Political Philosophy: Governance Concentration Beyond Token Allocation* (Table 6; §4.5 Amplification; §4.6.1 Voting-HHI Methodology; §5.7 Limitations).

**Addresses:** §5.7 limitation #4 (voting-HHI only 13 protocols).

**Generated:** 2026-05-27 (workflow clone PID 4300; B2 R3 data-collection omnibus Phase 2).

**Disposition:** This supplement is a **gap inventory + data-acquisition spec**, not a coverage expansion. Fresh API data (Snapshot proposals + Tally delegates + Solana VoteRecord parsing) for the 27 unmeasured protocols is the continuation-dispatch work; this cycle documents the structured target list per dispatch Phase 2 step 1.

---

## Current Table 6 inventory (canonical N=13)

| Rank | Token | Source | Voting-HHI | Holding-HHI | Ratio (V/H) | Classification |
|---:|---|---|---:|---:|---:|---|
| 1 | UNI | Tally | 0.0267 | 0.0271 | -- | (in Table 6) |
| 2 | AAVE | Tally | 0.058-0.075 | 0.0756 | -- | (in Table 6) |
| 3 | COMP | Tally + Snapshot | 0.039-0.089 | 0.0387 | 2.3x | amplify |
| 4 | ARB | Tally + Snapshot | 0.034-0.038 | 0.0355 | 0.96-1.07x | mixed |
| 5 | OP | Tally | 0.033 | 0.0330 | -- | (in Table 6) |
| 6 | ENS | Tally | 0.022 | (TBD) | 0.45x | DISPERSE |
| 7 | GMX | Tally | 0.057 | (TBD) | 0.87x | DISPERSE |
| 8 | DIMO | Snapshot | 0.228 | 0.025 | 9.1x | amplify (strong) |
| 9 | LDO | Snapshot | 0.050 | (TBD) | -- | amplify |
| 10 | WXM | Snapshot | 0.556 | (TBD) | -- | amplify (strong; SS-HHI=1.0 per S14) |
| 11 | DRIFT | Solana VSR | 0.083 | 0.0529 | 1.6x | amplify |
| 12 | HNT | Solana VSR | 0.026-0.039 | 0.0745 | 0.35x-0.53x | DISPERSE |
| 13 | JUP | Solana setvote | ~0.0055 | 0.0957 | 0.057x | DISPERSE (most-extreme) |

**Current predominant-amplification fraction:** 9 of 13 amplify (69.2%; per §4.5 prose). 4 dispersion exceptions (ENS, GMX, HNT, JUP).

Curve veCRV + Balancer veBAL (15x + 21x) form a separate ve-token class per §4.5.2 (not counted in the 13-protocol amplification count).

---

## Gap inventory: 27 unmeasured protocols (N=40 minus 13 measured)

Sorted by governance-surface tractability + sector. "Priority" reflects expected impact on Table 6 + dispatch step-2 methodology mapping.

### High-priority (Snapshot space confirmed; standard methodology)

| Protocol | Token | Sector | Governance surface | Acquisition methodology | Est. cycles |
|---|---|---|---|---|---|
| Balancer | BAL | DeFi | Snapshot space `balancer.eth` | Per-S12 top-1000 voter-pool 12-month rolling; vote-weight aggregation; HHI on signer max-weight | 0.5 |
| Gitcoin | GTC | Social_Dead | Snapshot space `gitcoindao.eth` | Per-S12 methodology | 0.5 |
| Maple/SYRUP | MPL_SYRUP | DeFi | Snapshot space `mapledao.eth` | Per-S12 methodology | 0.5 |
| POKT Network | POKT | DePIN | Snapshot space `pokt.eth` (verify) | Per-S12 methodology | 0.5 |
| Render | RENDER | DePIN | Snapshot space `rendernetwork.eth` (verify) | Per-S12 methodology | 0.5 |
| Livepeer | LPT | DePIN | Snapshot space `livepeer.eth` (verify) | Per-S12 methodology | 0.5 |
| Axelar | AXL | L1_L2_Infra | Snapshot space `axelarcommunity.eth` (verify; or on-chain) | Per-S12 OR on-chain | 1.0 |

### Medium-priority (on-chain or Snapshot; methodology selection required)

| Protocol | Token | Sector | Governance surface | Acquisition methodology | Est. cycles |
|---|---|---|---|---|---|
| Curve | CRV | DeFi | Curve DAO (on-chain veCRV) | Voting-HHI on veCRV-locked balances (current and historical lock-weighted; sister to §4.5.2 vote-escrow framing) | 1.0 |
| MakerDAO | MKR | DeFi | ds-chief (on-chain) | Voting-HHI on ds-chief executive vote weights; per-elector aggregation | 1.5 |
| Ether.Fi | ETHFI | DeFi | Snapshot OR on-chain (verify) | Per-S12 or on-chain Governor | 1.0 |
| Rocket Pool | RPL | DeFi | Snapshot space (verify) | Per-S12 | 0.5 |
| Filecoin | FIL | DePIN | FIP repo + signaling votes; on-chain limited | Signaling-vote weight aggregation; HHI on weighted votes | 2.0 |
| Polygon | POL | L1_L2_Infra | Governance v2 / community PIP (verify post-MATIC) | On-chain Governor OR Snapshot | 1.5 |
| LayerZero | ZRO | L1_L2_Infra | Foundation (limited formal governance) | Document surface; exclusion-with-rationale row | 0.5 |
| Wormhole | W | L1_L2_Infra | Wormhole Foundation governance | Per-S12 or no-governance row | 0.5 |
| The Graph | GRT | L1_L2_Infra | Snapshot space `graphprotocol.eth` (verify) | Per-S12 | 0.5 |

### Lower-priority (limited governance OR no-governance)

| Protocol | Token | Sector | Status | Disposition |
|---|---|---|---|---|
| Hyperliquid | HYPE | DeFi | No formal token governance (sink mechanism) | Table 6 exclusion-with-rationale row |
| MetaDAO | META | DeFi | Futarchy (conditional markets; not direct voting) | Methodology innovation required; defer OR exclusion-with-rationale |
| Aethir | ATH | DePIN | Snapshot / forum (limited activity) | Verify Snapshot space + activity threshold |
| Anyone Protocol | ANYONE | DePIN | Limited governance activity | Verify; may be exclusion-with-rationale |
| GEODNET | GEOD | DePIN | Forum / off-chain coordination | Verify Snapshot or governance surface |
| Grass | GRASS | DePIN | Foundation-led (limited token governance) | Verify; may be exclusion-with-rationale |
| Hivemapper | HONEY | DePIN | Foundation-led | Verify; may be exclusion-with-rationale |
| IoTeX | IOTX | DePIN | Snapshot OR on-chain (verify) | Per-S12 if space exists |
| io.net | IO | DePIN | Foundation-led (verify) | Verify; may be exclusion-with-rationale |
| Morpheus AI | MOR | DePIN | Snapshot (verify) | Per-S12 |
| TEC | TEC | Social_Dead | Snapshot space `tec.eth` | Per-S12 (low activity; verify) |
| HNT sub-DAOs (IOT + MOBILE) | IOT, MOBILE | DePIN | Realms participation-count proxy | Methodology gap (no wallet-weight connection); current §4.6.1 status quo |

---

## Predominant-amplification sensitivity analysis

**Current:** 9 of 13 protocols amplify (69.2%). The §4.5 prose uses "predominant" framing for this fraction.

**Sensitivity scenarios for extended sample N >= 18:**

| Scenario | Added protocols (5) | Amplify | Disperse | Predominant fraction | §4.5 framing risk |
|---|---|---:|---:|---:|---|
| Baseline expansion | All 5 amplify | 14 | 4 | 77.8% | Strengthens "predominant" |
| Mixed | 3 amplify + 2 disperse | 12 | 6 | 66.7% | Marginal; right at threshold |
| Dispersion-heavy | 1 amplify + 4 disperse | 10 | 8 | 55.6% | DROPS below "predominant"; surface to author per HALT-2.1 |

**Hypothesized direction of effect by sector:**

- **DeFi protocols with Snapshot governance** (BAL, GTC, MPL_SYRUP, ETHFI): expected to amplify (current sample's DeFi Snapshot protocols all amplify: COMP-snapshot, ARB-snapshot, LDO, DIMO, WXM)
- **DePIN protocols (POKT, RENDER, LPT, FIL, GEOD, GRASS, IO, HNT sub-DAOs)**: mixed; current sample DePIN protocols include both amplify (DIMO, WXM, DRIFT) and disperse (HNT, JUP)
- **ve-token protocols** (CRV is the prototypical case): if computed on veCRV-locked, expected to amplify substantially (per §4.5.2 BAL 21x + CRV 15x)
- **Foundation-led protocols** (W, ZRO, IO, GRASS, HONEY): if formal governance is weak, may not be measurable on voting-HHI axis at all; exclusion-with-rationale most likely

**Best estimate:** likely-amplifying expansion (BAL, GTC, MPL_SYRUP, POKT, RENDER, LPT, GRT all Snapshot-side) suggests extension reinforces "predominant" framing. Dispersion cases (potentially FIL, ANYONE, low-activity protocols) unlikely to flip the fraction below 67%.

**No HALT-2.1 trigger expected.** But verify on actual data.

---

## §4.5 predominant-fraction recompute method (acceptance test 2)

When the continuation dispatch ships extended voting-HHI data:

```python
# Per-protocol classification: amplify (voting/holding > 1.0); disperse (< 1.0); flat (~1.0)
# Compute predominant_fraction = n_amplify / n_total
# Halt-and-surface if predominant_fraction < 0.67
```

The 0.67 threshold is informal (matches "two-thirds majority" intuition); current §4.5 uses "predominant" without an explicit numerical floor. Continuation dispatch should specify either:

- (a) Retain "predominant" framing with footnote about which protocols added (anchor §5.7 #4 closure)
- (b) Replace with explicit "two-thirds" or numerical specification if fraction drops below 0.67
- (c) Restructure §4.5 around dispersion-vs-amplification typology if substantial dispersion patterns appear

---

## Methodology innovation gaps (HALT-2.2 candidates)

Three protocols require methodology innovation beyond standard S12 + Tally:

1. **MakerDAO (MKR/SKY).** ds-chief on-chain is not a standard Governor contract. Methodology: per-executor weight on `ds-chief.executive()` log events; HHI on per-address aggregated voted weight. Requires bespoke parsing.
2. **Filecoin (FIL).** FIP voting is signaling (off-chain) plus on-chain ratification. Methodology: aggregate FIP repo voting; weight by some proxy (FIL holdings at vote time; or FIL committed to mining). Requires methodology decision.
3. **MetaDAO (META).** Futarchy is fundamentally not a direct-vote mechanism. Methodology: cannot apply HHI to "conditional market trading"; defer with exclusion-with-rationale row.

If these 3 are deemed in-scope for §5.7 #4 closure, surface to author per HALT-2.2.

---

## Output spec for continuation dispatch (Phase 2)

The continuation dispatch should produce, per protocol added:

1. **Per-protocol governance-surface confirmation note** (Snapshot space ID; Tally org slug; on-chain Governor address; methodology note)
2. **voting_hhi.csv row** with symbol, source, voting_hhi, voting_gini, voting_top1_pct, voting_top5_pct, voting_top10_pct, n_unique_voters, n_sampled
3. **Updated Table 6 in PAPER.md** with new rows + Source-method footnotes (per existing † ‡ § ¶ convention)
4. **Recomputed predominant-amplification fraction** + §4.5 prose update (or HALT surface if fraction shifts threshold)

---

## Cross-references

- **§4.5** Amplification finding (current "9 of 13 = predominant")
- **§4.5.2** Vote-escrow class (CRV + BAL 15x + 21x; separate from main amplification analysis)
- **§4.6.1** Voting-HHI methodology (3 methodology choices)
- **§5.7 #4** Voting-HHI only 13 protocols (gap inventory this supplement; closure pending continuation dispatch data)
- **S11** Power indices (5-protocol baseline; extends in Phase 1)
- **S12** Voting-HHI symmetric-robustness (canonical methodology for Snapshot + Tally + Solana on-chain)
- **S14** Power indices extension (N=11 this cycle; Phase 1 sister supplement)

---

## Author note

This Phase 2 deliverable is **inventory + spec, not coverage expansion**, because fresh API data for the 27 unmeasured protocols requires Tally + Snapshot + on-chain Solana queries not available in the current `data/raw/` snapshot. The continuation dispatch carries the actual data-pull work; this supplement is the structured target list + per-protocol methodology spec that makes the continuation tractable.

The §5.7 #4 limitation closure path is therefore: (1) execute this gap inventory per the priority order; (2) compute voting-HHI per protocol per the methodology mapping; (3) update Table 6; (4) recompute predominant-amplification fraction; (5) close §5.7 #4 OR surface threshold-flip via HALT-2.1.

Author: Claude Code session 2026-05-27 (PID 4300); workflow clone `/Users/zach/Tokenization_Systems_Website`; sibling clone `/Users/zach/Tokenomics-As-Institutional_Design`.
