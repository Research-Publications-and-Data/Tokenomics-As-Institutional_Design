# Supplementary File S13: Solana PCA Classification Audit (Phase 5 of B2 R3 omnibus)

**Companion to:** B2 paper *Tokenomics as Applied Political Philosophy: Governance Concentration Beyond Token Allocation* (§3.8 Five-Class PCA Typology; §4.6.1 Voting-HHI Methodology; §5.7 Limitations).

**Closes:** §5.7 limitation #3 (PCA classification weaker coverage for Solana-native protocols).

**Generated:** 2026-05-27 (workflow clone PID 4300; B2 R3 data-collection omnibus Phase 5).

**Data sources:** existing top-1000 holder snapshots in `data/raw/holder_lists/` (loaded 2026-05-19 cycle); existing exclusions in `data/processed/exclusions_log.csv` (134 rows; 8 Solana rows pre-audit).

**Script:** `solana_pca_audit_2026-05-27.py` (computational reproducibility).

**Output artifacts:**
- `solana_pca_audit_2026-05-27.csv` (per-protocol HHI pre/post-exclusion + shift)
- `solana_pca_candidates_2026-05-27.csv` (top-10 unexcluded holders per Solana protocol; PCA verification queue)

---

## Executive summary

The B2 paper's §5.7 #3 limitation flags PCA classification as "weaker coverage" for Solana-native protocols. This audit produces three findings.

**Finding A (gap closure status).** Existing Solana exclusions cover the rank-1 holder for JUP, DRIFT, HNT, META adequately (HHI shifts -0.021 to -0.048; all within S12 sensitivity threshold and below HALT-5.1 0.05 threshold). GRASS and RENDER (Solana-side) have **zero Solana-side exclusions** despite top-1 holder shares of 16.01% (GRASS) and 18.01% (RENDER_SOL) — these are open PCA verification queues.

**Finding B (data-integrity discrepancies).** Three Solana-side data-integrity issues surfaced:
1. **HONEY exclusion attribution mismatch** — the exclusion log targets address `ERo2...` at rank 4 (3.34% share), but the documented attribution claims "6.48% of top-1000 share consistent with Foundation treasury / mint authority." The HONEY top-1 holder is `EyBXvV7...` at 7.04% share. Either the rank-4 address is correctly the Foundation (and the 6.48% claim was wrong) OR the wrong address was excluded (and the top-1 should be re-audited). Surfaced as EC candidate.
2. **RENDER chain-data inconsistency** — canonical regression dataset labels RENDER's chain as `solana` but the HHI value (0.026753) cannot be reproduced from `RENDER_SOL_holders.csv` (computed HHI 0.07034). The 0.026753 value reproduces from `RENDER_holders.csv` (Ethereum-side). RENDER migrated from Ethereum (RNDR) to Solana per the Render Network Proposal RNP-002; the canonical dataset may be using the pre-migration Ethereum holder snapshot while labeling chain as Solana. Surfaced as EC candidate.
3. **IO holder data missing** — `IO_holders.csv` is absent from `data/raw/holder_lists/` (only `IOTX_holders.csv` is present, which is a different protocol — IoTeX). The canonical regression value for io.net (HHI=0.125136) cannot be reproduced this cycle. Surfaced as gap in data registry.

**Finding C (cross-protocol Solana custody concentration; NEW substantive finding).** Seven unexcluded addresses appear in the top-10 holder lists of 2+ Solana protocols. The most consequential:
- **`u6PJ8DtQuPFnfmwHbGFULQ4u4EgjDiyYKjVEsynXq2w`** holds top-10 positions in 4 protocols (Jupiter 2.34%, Helium 5.97%, Grass 6.61%, Render-Solana 3.70%). Behavioral signature consistent with a single CEX custody address (similar pattern to the already-excluded Binance hot wallet `9WzDXw...` which holds W and IO).
- **`5LZkATrLwHYCQj2YuVbjjgsDZzBk6YfL4pFQRJmtboT2`** is HNT rank-1 unexcluded at 12.43% share AND Wormhole rank-3 at 1.85%. The HNT rank-1 unexcluded position is the single most consequential PCA gap in this audit; if this is exchange custody or a Foundation secondary wallet, HNT HHI would shift materially.
- **`6FEVkH17P9y8Q9aCkDdPcMDjvj7SVxrTETaYEm8f51Jy`** in 3 protocols (Jupiter, Helium, Render-Solana).

This is sister to the §4.5.5 cross-protocol delegate overlap finding (PGov + Tane + Arana on Snapshot + Tally) — voting-axis cross-protocol concentration is paralleled by holder-axis cross-protocol custody concentration on Solana.

---

## Per-protocol HHI audit table

| Protocol | Token | N holders | Existing exclusions | HHI pre | HHI post | Shift | Status |
|---|---|---:|---:|---:|---:|---:|---|
| Jupiter | JUP | 1000 | 1 | 0.11658 | 0.09571 | -0.02087 | OK (matches canonical 0.095708) |
| Drift | DRIFT | 1000 | 1 | 0.10113 | 0.05291 | -0.04822 | OK (matches canonical 0.052914) |
| Helium | HNT | 1000 | 1 | 0.10240 | 0.07446 | -0.02794 | OK (matches canonical 0.074465) |
| Hivemapper | HONEY | 100 | 1 | 0.02248 | 0.02277 | +0.00029 | DISCREPANCY (exclusion at rank 4; canonical 0.017589 from different snapshot) |
| MetaDAO | META | 1000 | 1 | 0.04825 | 0.01518 | -0.03307 | OK (matches canonical 0.015176) |
| io.net | IO | MISSING | 2 | N/A | N/A | N/A | DATA GAP (IO_holders.csv missing) |
| Grass | GRASS | 1000 | 0 | 0.03520 | 0.03520 | 0.00000 | GAP (zero Solana-side exclusions; top-1 share 16.01%) |
| Render (Solana) | RENDER_SOL | 549 | 0 | 0.07034 | 0.07034 | 0.00000 | GAP + CANONICAL MISMATCH (chain label "solana" but canonical 0.026753 uses Ethereum data) |
| Wormhole | W | 1000 | 1 | 0.01493 | 0.01153 | -0.00339 | OK (matches canonical 0.011532) |

**HALT status:** All per-protocol HHI shifts within HALT-5.1 threshold (max shift -0.04822 for DRIFT; threshold 0.05). HALT-5.2 (Solana structural difference) NOT triggered by this audit but pending fresh Foundation/CEX address verification (Finding C cross-protocol custody pattern is suggestive but not yet conclusive).

---

## Candidate PCA addresses (next-cycle verification queue)

Per dispatch Phase 5 step 2, the top-10 unexcluded holders per Solana protocol surface as PCA verification candidates. Full enumeration in `solana_pca_candidates_2026-05-27.csv`. Cross-protocol entities (7 addresses appearing in 2+ protocols' top-10) are highest priority for next-cycle on-chain verification via:
- **Helius DAS API** (token-account decoding; Anchor program inspection)
- **Squads Protocol** (multi-sig membership verification)
- **Realms** (DAO treasury registry)
- **Solscan / SolanaFM** (label aggregation across community sources)
- **Wormhole bridge accounts** (verified bridge custody addresses)

### Cross-protocol candidate PCAs (Finding C; highest verification priority)

| Address | Protocols (rank, share) | Pattern hypothesis |
|---|---|---|
| `u6PJ8DtQuPFnfmwHbGFULQ4u4EgjDiyYKjVEsynXq2w` | JUP r8 2.34%; HNT r4 5.97%; GRASS r2 6.61%; RENDER_SOL r10 3.70% | CEX custody (4-protocol presence; behavioral signature parallels existing Binance hot wallet `9WzDXw...`) |
| `5LZkATrLwHYCQj2YuVbjjgsDZzBk6YfL4pFQRJmtboT2` | HNT r1 12.43%; W r3 1.85% | Foundation secondary OR major CEX custody; **highest-share single-protocol unexcluded** |
| `6FEVkH17P9y8Q9aCkDdPcMDjvj7SVxrTETaYEm8f51Jy` | JUP r10 1.98%; HNT r5 5.24%; RENDER_SOL r2 8.81% | CEX or staking-aggregation; multi-protocol presence |
| `5tzFkiKscXHK5ZXCGbXZxdw7gTjjD1mBwuoFbhUvuAi9` | JUP r5 3.80%; RENDER_SOL r8 4.20%; W r5 1.12% | Bridge custody OR CEX |
| `6LY1JzAFVZsP2a2xKrtU6znQMQ5h4i7tocWdgrkZzkzF` | JUP r4 3.95%; RENDER_SOL r5 6.92% | CEX or LST aggregation |
| `5PAhQiYdLBd6SVdjzBQDxUAEFyDdF5ExNPQfcscnPRj5` | GRASS r3 3.16%; RENDER_SOL r9 4.12% | Cross-DePIN custody candidate |
| `JCNCMFXo5M5qwUPg2Utu1u6YWp3MbygxqBsBeXXJfrw` | DRIFT r6 1.95%; DRIFT r9 1.28% | Same-protocol duplicate (possible misclassification; verify single address) |

### Highest-impact single-protocol candidates

| Protocol | Address | Rank | Share | Hypothesis |
|---|---|---|---|---|
| HNT | `5LZkATrLwHY...` | 1 | 12.43% | See cross-protocol table |
| GRASS | `5Q544fKrFoe...` | 1 | 16.01% | First-time Solana audit; no prior attribution |
| RENDER_SOL | `51PZFsSVorG...` | 1 | 18.01% | First-time Solana audit; no prior attribution |
| HNT | `4UiT93tyCiv...` | 2 | 8.76% | Same-protocol candidate (not in cross-protocol list) |
| HONEY | `EyBXvV7...` | 1 | 7.04% | Top-1 holder; potentially the true Foundation address vs the wrongly-excluded `ERo2...` |

---

## Methodology

### Solana-specific PCA classes (§3.8 typology extension proposal)

Current §3.8 typology has 5 classes (burn destinations; foundation/treasury custody; staking-aggregation; bridge custody/migration; CEX custody). Solana-specific examples to surface in §3.8 if Finding C cross-protocol pattern is confirmed:

- **Class 1 (burn destinations):** Solana System Program `11111111111111111111111111111111`; per-protocol burn vaults
- **Class 2 (foundation/treasury):** Squads Protocol multi-sigs (DRIFT Foundation `9Wiiyvy8...`; HNT Foundation `AguTdjm...`); Realms DAO treasury accounts; protocol-controlled program accounts (META `4viad...`)
- **Class 3 (staking-aggregation):** SPL stake-pool accounts; LST aggregation (Marinade, Jito, BlazeStake); per-protocol VSR position accounts (HNT, DRIFT, JUP veToken positions)
- **Class 4 (bridge custody):** Wormhole `5tzFkiKscX...` (candidate); DeBridge; Allbridge; per-protocol native-to-Solana migration mappers
- **Class 5 (CEX custody):** Binance `9WzDXw...` (excluded); candidate cross-protocol addresses per Finding C

### Sensitivity threshold convention (per S12)

HHI shifts > 0.005 flagged as material; > 0.05 triggers HALT-5.1 (cascade to Table 3, Figure 1, §4.3 sector contrast). All shifts in this audit are within the 0.005-0.05 range or smaller; no HALT-5.1 trigger.

### Computational reproducibility

`solana_pca_audit_2026-05-27.py` provides full reproducibility. To re-run:

```bash
cd /Users/zach/Tokenomics-As-Institutional_Design
python3 b2/paper/supplements/solana_pca_audit_2026-05-27.py
```

Output writes to `b2/paper/supplements/solana_pca_audit_2026-05-27.csv` and `b2/paper/supplements/solana_pca_candidates_2026-05-27.csv`.

---

## §5.7 #3 closure status

The §5.7 limitation #3 framing ("weaker coverage for some Solana-native protocols") is partially addressed by this audit:

- **Closed:** the rank-1 holder per-protocol PCA coverage for JUP, DRIFT, HNT, META is adequate (matches canonical HHI within 0.0001).
- **Open (next-cycle):** GRASS and RENDER (Solana-side) zero-exclusion gaps; 7 cross-protocol candidate addresses pending on-chain verification.
- **EC candidates:** HONEY exclusion attribution mismatch; RENDER chain-data inconsistency; IO holder data missing.

Recommendation: retain §5.7 #3 framing in B2 R3 with status-update language acknowledging this audit's partial closure + the open verification queue. Full closure pending next-cycle on-chain audit (continuation dispatch Phase 5 detail).

---

## §4.6.1 update recommendation

The §4.6.1 Solana proper-weight methodology subsection should extend with:

- **Sister-table to existing EVM PCA examples:** Solana-specific Class 2 (Squads multi-sig); Class 3 (SPL stake pool); Class 4 (Wormhole bridge custody); Class 5 (Binance Solana hot wallet)
- **Methodology footnote:** Solana protocols' VSR vote-weight (HNT 1-4x lockup multiplier; DRIFT VSR; JUP setvote signing) requires per-protocol weighting in voting-HHI computation (S12 reference)
- **Cross-protocol concentration footnote (Finding C):** the 7-address cross-protocol custody pattern is parallel to §4.5.5 cross-protocol delegate overlap; may warrant a new sub-subsection at §4.5.5 ("Cross-protocol concentration on Solana: holder-axis") or §4.6.1 extension

---

## Cross-references

- **§3.8** Five-class PCA typology (current 5 EVM-anchored examples; Solana extension this supplement)
- **§4.5.5** Cross-protocol delegate overlap (Tally-side PGov+Tane+Arana = 8.11% on ARB+COMP+UNI; sister-finding to Finding C cross-protocol holder concentration)
- **§4.6.1** Voting-HHI methodology robustness (current 3 methodology choices; Solana proper-weight extension proposed)
- **§5.7 #3** PCA classification weaker for Solana-native protocols (partial closure status this audit)
- **S11** Power indices (Phase 1 dependency for Solana SS computation; deferred to continuation dispatch)
- **S12** Voting-HHI symmetric-robustness (sensitivity-threshold convention 0.005)
- **EC candidates this session:** HONEY exclusion-attribution; RENDER chain-data; IO holder-data-gap

---

## Author note

This audit is **bounded by session data-access constraints.** Specifically, fresh on-chain queries (Helius DAS API; Squads Protocol; Realms; Solscan label aggregation) are deferred to the continuation dispatch. The 7 cross-protocol candidate addresses (Finding C) require on-chain verification before they can enter `exclusions_log.csv` with confidence. The audit shipped this cycle is the **analytical scaffolding + gap inventory**; the on-chain data collection is the next-cycle work.

Author: Claude Code session 2026-05-27 (PID 4300); workflow clone `/Users/zach/Tokenization_Systems_Website`; sibling clone `/Users/zach/Tokenomics-As-Institutional_Design`.
