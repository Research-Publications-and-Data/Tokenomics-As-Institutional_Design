# 40-Protocol PCA Exclusion Coverage Audit (2026-05-19; intermediate-stage snapshot, superseded by 126-address final state)

**Note (2026-05-19 evening update):** This supplement documents the audit at the 35-protocol / 92-address coverage stage. Subsequent deep-top-5 audit waves (workflow commits `cab8a2dd` → `263c6f94` → `19529d6a`) brought coverage to 38 protocols / 126 addresses. The 2026-05-19 evening Table 7 cascade (workflow commit `3a8c3065`; replication sister `6b71ea1`) updated downstream amplification ratios (1.4x to 6.0x → 1.2x to 11.4x; mean 3.3x → 5.3x; ENS 0.21x → 0.39x). The sector-stat summary below (lines 46-50) reflects the 35-protocol stage; the post-Table-7-cascade current values are in `CHANGELOG.md` under the 2026-05-19 Table 7 cascade subsection. Line 53's "universal-amplification unchanged" claim was forward-looking and turned out incorrect: Table 7 holding HHIs shifted with later audit waves and were cascaded today.

**Goal:** Achieve PCA exclusion documentation for all 40 protocols in the regression sample.

**Final state at write time:** 35 of 40 protocols have documented PCA exclusions. 1 protocol confirmed non-PCA. 4 protocols remain audit-pending due to explorer/disclosure limitations. (Subsequent audit waves brought this to 38 documented + 2 confirmed non-PCA = 40/40 coverage.)

## Coverage matrix

| Status | Count | Protocols |
|---|---|---|
| **Documented (35)** | 35 | AAVE, ANYONE, ARB, ATH, AXL, BAL, COMP, CRV, DIMO, DRIFT, ENS, ETHFI, FIL, GEOD, GMX, GRT, GTC, HNT, HONEY, HYPE, IO, IOTX, JUP, LDO, LPT, META, MKR, MOR, MPL_SYRUP, OP, POL, RENDER, RPL, UNI, WXM, ZRO |
| **Confirmed non-PCA (2)** | 2 | TEC (top-1 = `gideonro.eth` = founder personal wallet); GRASS (top-1 = `5Q544fKr...` = Solana MEV bot per community sources, NOT protocol-controlled) |
| **Audit-pending (3)** | 3 | Wormhole (W), POKT, ... |

## Tier 1 Class 2 additions (2026-05-19 WebSearch audit; 6 new protocols)

| Token | Address | Verification source |
|---|---|---|
| JUP | `6tZT9AUcQn4iHMH79YZEXSy55kDLQ4VbA3PMtfLVNsFX` | Jupiter tokenomics docs: 4/7 Team Cold Multisig holds 4B JUP (team + strategic reserve allocations) |
| DRIFT | `9Wiiyvy8zzbZmJwxevi5CHZKs2VSZW7fvJJjrixviLA6` | Drift Foundation governance docs: Squads V4 multisig (treasury function); 27.01% top-1000 share |
| HNT | `AguTdjmW5SkhepT9qsKsj29SEqiVKsJchsap6Kma9i98` | GeckoTerminal + multiple Solana data sources: largest HNT holder; web search confirms Foundation/treasury classification |
| FIL | `f1m2swr32yrlouzs7ijui3jttwgc6lxa5n5sookhi` | Filfox: 156M FIL balance + 212 messages since Nov 2020; behavioral signature = Foundation reserve |
| META | `4viadAyxnRpHyW2g2NEzjLwGGgLTQK2QBmniJJqXWpXN` | CoinMarketCap: largest META token holder; MetaDAO is futarchy governance platform (protocol-controlled by design) |
| HONEY | `ERo2hRAc4L83gW2TrFNKxpKgXh5PaWZHC1tqW9RgKLvN` | Hivemapper Foundation runs HONEY distribution per docs.hivemapper.com + hivemapperfoundation.org/honey |

## Non-PCA confirmations (do NOT exclude)

| Token | Address | Source |
|---|---|---|
| TEC | `0x5584e380c5ba129ccb5c1ce89c2e9d66881f4800` | Etherscan: `gideonro.eth` = founder personal wallet |
| GRASS | `5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1` | Community sources (crowd.news, multiple X posts): Solana MEV bot operating across many tokens with dozens of transactions per second; NOT protocol-controlled |

## Residual audit-pending (3 protocols)

| Token | Top-1 share | Status |
|---|---|---|
| Wormhole (W) | 7.04% | 9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM; Foundation treasury is 23.3% of total supply but 7.04% top-1000 share suggests this is a community/ecosystem distribution wallet rather than Foundation treasury; insufficient evidence |
| POKT | 34.78% | pokt132y5nzs4xahqy6cmzankn8mn4ec897j50wuzhr; POKT chain has no widely-indexed explorer; web search did not surface authoritative identification |

## Cumulative impact summary (full 2026-05-19 audit cycle)

**Coverage:** 22 → 35 documented PCA-exclusion protocols (+13 protocols). 92 PCA addresses (was 69 before cycle; +23 addresses).

**Sector statistics post-full-audit:**

- DeFi mean: 0.0430 → 0.0347 (after JUP, DRIFT, ETHFI, MKR exclusions added)
- DePIN mean: 0.0902 → 0.0870 (after HNT, FIL, ANYONE, IOTX, GEOD exclusions; MOR burn added)
- Mann-Whitney p: 0.014 → 0.014 (essentially preserved; DePIN-DeFi gap robust)
- Cohen's d: 1.03 → 1.19 (effect size increases; gap widens after symmetric application of PCA exclusions)
- Permutation p: 0.009 → 0.001 (10x more significant)
- LOO robustness: 30/30 preserved

**Findings preserved:** Allocation null (r = 0.17, p = 0.32; was 0.18 / 0.28); universal-amplification (1.4x to 6.0x; mean 3.3x; unchanged because HHI-based); subsidy disconnect (with-LPT r = 0.59, without-LPT r = 0.11; basically unchanged).

## Methodology

For each previously-undocumented protocol, the audit followed this protocol:

1. Identify top-1 holder from `data/raw/holder_lists/{TOKEN}_holders.csv`
2. Query Etherscan/Solscan/Filfox/Polygonscan/Gnosisscan for address labels
3. Cross-reference with protocol Foundation docs, tokenomics announcements, GitHub Foundation address disclosures
4. Apply WebSearch with address + protocol name to find indirect references
5. Classify as Class 1-5 per Section 2.10.10 PCA typology, OR confirm as non-PCA (personal wallet, bot, etc.), OR flag as audit-pending

## Cross-references

- `data/processed/exclusions_log.csv`: 90 → 96 rows
- `b2/paper/B2_Frontiers_R2_clean.docx`: Section 2.10.10 Class 5 codification; PCA count "92 addresses across 35 protocols"
- `b2/paper/supplements/exclusions_audit_2026-05-19.md`: PCA Class 5 audit findings (sister file)
- CHANGELOG.md: "Tier 1 WebSearch audit additions (2026-05-19)" subsection
