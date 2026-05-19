# 40-Protocol PCA Exclusion Coverage Audit (2026-05-19)

**Goal:** Achieve PCA exclusion documentation for all 40 protocols in the regression sample.

**Status:** 29 of 40 protocols have documented exclusions (was 22 before the 2026-05-19 expansion cycle).

## Coverage matrix

| Status | Count | Protocols |
|---|---|---|
| **Documented (29)** | 29 | AAVE, ANYONE, ARB, ATH, AXL, BAL, COMP, CRV, DIMO, ENS, ETHFI, GEOD, GMX, GRT, GTC, HYPE, IO, IOTX, LDO, LPT, MKR, MOR, MPL_SYRUP, OP, POL, RENDER, RPL, UNI, WXM, ZRO |
| **Audit-pending (9)** | 9 | JUP, DRIFT, GRASS, HNT, FIL, POKT, W, META, HONEY |
| **Non-PCA confirmed (1)** | 1 | TEC (top-1 holder is `gideonro.eth` = founder personal wallet; not PCA per Etherscan label inspection) |
| **No exclusions needed (1)** | 1 | TEC (as above; founder wallet stays in distribution per methodology) |

## Audit-pending protocols (9)

These protocols have plausible PCA-class top holders identified, but lack authoritative verification needed to apply exclusions silently. Each candidate requires either protocol-team disclosure or on-chain behavioral analysis to confirm PCA classification.

| Protocol | Token | Chain | Top-1 share | Top-1 address | Verification status |
|---|---|---|---|---|---|
| Jupiter | JUP | Solana | 25.07% | `6tZT9AUcQn4iHMH79YZEXSy55kDLQ4VbA3PMtfLVNsFX` | Solscan WebFetch blocked (HTTP 403); Solana labels not in indexed search |
| Drift | DRIFT | Solana | 27.01% | `9Wiiyvy8zzbZmJwxevi5CHZKs2VSZW7fvJJjrixviLA6` | Web search indicates Drift Foundation exists but does not authoritatively label this address |
| Grass | GRASS | Solana | 16.01% | `5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1` | Solscan blocked |
| Helium | HNT | Solana | 24.48% | `AguTdjmW5SkhepT9qsKsj29SEqiVKsJchsap6Kma9i98` | GeckoTerminal sources indicate this is the largest HNT holder; web search suggests it "likely serves as a treasury or distribution address for the Helium Foundation or ecosystem"; HHI impact -27 percent if excluded as Class 2 |
| Filecoin | FIL | filecoin_native | 18.01% | `f1m2swr32yrlouzs7ijui3jttwgc6lxa5n5sookhi` | Filfox shows 156M FIL balance + 212 messages since Nov 2020; behavioral signature consistent with Foundation/treasury holding; HHI impact -54 percent if excluded as Class 2 |
| Pokt Network | POKT | pokt_native | 34.78% | `pokt132y5nzs4xahqy6cmzankn8mn4ec897j50wuzhr` | POKT chain has no widely-indexed explorer for WebFetch; protocol-team verification needed |
| Wormhole | W | Solana | 7.04% | `9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM` | Solscan blocked; lower share (7%) means HHI impact would be modest |
| MetaDAO | META | Solana | 19.61% | `4viadAyxnRpHyW2g2NEzjLwGGgLTQK2QBmniJJqXWpXN` | Solscan blocked |
| Hivemapper | HONEY | Solana | 6.48% | `ERo2hRAc4L83gW2TrFNKxpKgXh5PaWZHC1tqW9RgKLvN` | Solscan blocked; lower share means modest HHI impact |

## Path forward

To push to 40/40 documented coverage, one of:

1. **Author protocol-team verification.** For each protocol, consult official treasury / Foundation address disclosures (Helium Foundation docs; Filecoin Foundation public addresses; POKT Foundation announcements; Jupiter, Drift, Grass, MetaDAO, Hivemapper, Wormhole Foundation discord/docs). This is the highest-fidelity verification path.

2. **Helius DAS API behavioral analysis.** For Solana protocols, query Helius API for each top-1 address: transaction count, age, distribution patterns. Behavioral signatures (large balance + low activity + early funding from protocol mint = Foundation/treasury) can substitute for labels in many cases.

3. **Accept circumstantial-evidence additions with caveats.** Add Helium and Filecoin to exclusions log with "Class 2 likely; protocol-team verification pending" labels (same convention used for AXL d2ff and ETHFI Safe). This pushes coverage to 31/40 but introduces HHI shifts based on circumstantial evidence.

## Recommendation

Author judgment required. Option 1 (protocol-team verification) is highest-fidelity but requires per-protocol disclosure research. Option 2 (Helius behavioral) is medium-cost and reasonably defensible. Option 3 (circumstantial) is fastest but accepts methodological uncertainty.

## What this cycle delivered

The 2026-05-19 expansion cycle pushed coverage from 22 to 29 protocols (+7 protocols, +11 addresses) via:
- Universal Class 1 burn sweep across all 40 protocols (5 new burn destinations: RPL, GMX, GEOD, MOR, IO)
- Etherscan-verified Class 2-4 identifications: MKR LockstakeMigrator (Class 4); IOTX Staking (Class 3); ANYONE Protocol Staking (Class 3); GTC Timelock (Class 2); ETHFI Safe (Class 2); GEOD treasury (Class 2)
- Class 5 (CEX custody) codified in Section 2.10.10

Total exclusions: 90 addresses across 29 protocols (was 79 across 23 before this cycle).

## Cross-references

- `data/processed/exclusions_log.csv`: 79 to 90 rows
- `b2/paper/B2_Frontiers_R2_clean.docx` (workflow commit 8f25b397; replication b410d09): "75 PCA addresses across 22 protocols" updated to "86 PCA addresses across 29 protocols"
- Section 2.10.10 (PCA typology): Class 5 (CEX custody) codified in commit eee7a5a2 / 93cc32e
- `b2/paper/supplements/exclusions_audit_2026-05-19.md`: PCA Class 5 audit findings
