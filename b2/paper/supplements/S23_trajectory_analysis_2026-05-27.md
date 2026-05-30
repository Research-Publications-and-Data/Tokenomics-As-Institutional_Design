# Supplementary File S23: Q1-to-Q8 Governance-HHI Trajectory Analysis (14-protocol panel)

**Companion to:** B2 paper *Tokenomics as Applied Political Philosophy: Governance Concentration Beyond Token Allocation*, Section 3.6 (longitudinal panel discussion) and Sections 5.7 / 5.8 (cross-section-vs-longitudinal limitation; future research).

**Scope:** trajectory analysis on the existing 14-protocol Q1-vs-Q8 panel (Supplementary File S7). The full monthly panel across the complete cross-section is documented as future work in Section 5.8.

**Data source:** `S7_hhi_panel/exhibit_k1_panel_full.csv` (14 protocols by 2 time-points: Q1 = three-months-post-token-generation-event; Q8 = twenty-four-months-post-token-generation-event).

---

## Summary

This trajectory analysis uses the existing 14-protocol Q1-vs-Q8 panel without new data collection. The finding: 12 of 14 protocols (85.7 percent) exhibit monotonic holding-HHI decay from Q1 to Q8; the 2 exceptions (ENS and COMP) have documented institutional mechanisms (claim window for ENS; reservoir drip for COMP). The longitudinal evidence is consistent with the cross-sectional findings; there is no direction-of-effect reversal.

---

## Per-protocol trajectory results

| Protocol | Q1 (3mo) | Q8 (24mo) | Delta | Percent change | Pattern | Mechanism |
|---|---:|---:|---:|---:|---|---|
| AAVE | 0.191 | 0.050 | -0.141 | -73.8% | Decay | -- |
| ARB | 0.016 | 0.008 | -0.008 | -50.0% | Decay | -- |
| BAL | 0.212 | 0.020 | -0.192 | -90.6% | Decay | -- |
| COMP | 0.033 | 0.049 | +0.016 | +48.5% | Exception | Reservoir drip |
| CRV | 0.556 | 0.249 | -0.307 | -55.2% | Structural | vote-escrow lock |
| DIMO | 0.529 | 0.015 | -0.514 | -97.2% | Decay | -- |
| ENS | 0.007 | 0.025 | +0.018 | +257.1% | Exception | claim window |
| GRT | 0.083 | 0.048 | -0.035 | -42.2% | Decay | -- |
| LDO | 0.047 | 0.031 | -0.016 | -34.0% | Decay | -- |
| MKR (MCD) | 0.077 | 0.068 | -0.009 | -11.7% | Decay | -- |
| MKR (TGE) | 0.244 | 0.034 | -0.210 | -86.1% | Decay | -- |
| OP | 0.041 | 0.023 | -0.018 | -43.9% | Decay | -- |
| RPL | 0.486 | 0.107 | -0.379 | -78.0% | Decay | -- |
| UNI | 0.054 | 0.011 | -0.043 | -79.6% | Decay | -- |

**Pattern distribution:**
- Decay: 11 protocols (78.6 percent)
- Exception: 2 protocols (14.3 percent; ENS and COMP)
- Structural: 1 protocol (7.1 percent; CRV)

**Monotonic-decay rate: 12 of 14 = 85.7 percent** (counting MKR-MCD at -11.7 percent as decay; alternatively 11 of 14 = 78.6 percent under a -15 percent decay threshold).

---

## Largest decay magnitudes

The largest absolute holding-HHI reductions in the panel:

1. DIMO: 0.529 to 0.015 (-97.2 percent)
2. BAL: 0.212 to 0.020 (-90.6 percent); the BAL vote-escrow voting-HHI (0.305) reflects vote-escrow concentration, distinct from this holder-HHI decay.
3. MKR (TGE): 0.244 to 0.034 (-86.1 percent)
4. UNI: 0.054 to 0.011 (-79.6 percent)
5. RPL: 0.486 to 0.107 (-78.0 percent)

These reflect the typical post-token-generation concentration-decay pattern as initial allocations vest, airdrop recipients trade, and broader market participants accumulate.

---

## Two holding-HHI-increase exceptions (Q1 to Q8)

### COMP (+48.5 percent; reservoir-drip mechanism)

Compound's COMP distribution uses a reservoir-drip mechanism that distributes COMP to suppliers and borrowers over time at fixed rates. Distribution concentrates among heaviest-utilization addresses (large suppliers and large borrowers) over time rather than dispersing broadly. The HHI increase from 0.033 to 0.049 reflects this convergent-to-power-users distribution mechanism.

### ENS (+257.1 percent; claim-window mechanism)

The ENS airdrop used a one-time claim window (October 2021). The Q1 measurement (three months post-token-generation) captured peak post-airdrop dispersion as recipients claimed and held; subsequent on-chain trades and vesting cliffs concentrated holdings into the 24-month state. The 0.007 to 0.025 shift reflects post-airdrop reconcentration, consistent with the ENS dispersion characterization at the later cross-section snapshot.

---

## Per-sector trajectory (limited by N=14)

| Sector | N | Mean Q1 HHI | Mean Q8 HHI | Mean decay |
|---|---:|---:|---:|---:|
| DeFi (AAVE, BAL, COMP, CRV, LDO, MKR-MCD, MKR-TGE, RPL, UNI) | 9 | 0.211 | 0.069 | -67 percent mean |
| Infrastructure (ARB, GRT, OP) | 3 | 0.047 | 0.026 | -45 percent mean |
| DePIN (DIMO) | 1 | 0.529 | 0.015 | -97 percent |
| Social (ENS) | 1 | 0.007 | 0.025 | +257 percent (exception) |

DeFi protocols show consistent strong decay; infrastructure protocols decay more modestly (lower Q1 baseline); the single DePIN observation (DIMO) shows extreme decay. Per-sector trajectory analysis is limited by the N=14 sample; the full monthly panel across the complete cross-section would enable proper per-sector slope comparison.

---

## Relation to the cross-sectional findings

The 14-protocol panel trajectory analysis is consistent with the cross-sectional results:
- Cross-sectional concentration decay over time (12 of 14 monotonic decay).
- Documented exception mechanisms (reservoir drip; claim window; vote-escrow) explain the non-decay cases.
- The single DePIN observation (DIMO, -97.2 percent) is consistent with the broader DePIN cross-section pattern.

Section 5.7 documents the cross-section-versus-longitudinal limitation; this trajectory analysis is a partial closure on the existing panel. The full monthly panel across the complete cross-section is specified as future work in Section 5.8.

---

## Full-panel methodology specification (future work)

### Target scope

- Complete cross-section by monthly snapshots over twelve months from each protocol's token-generation event.
- Per-snapshot: top-1,000 holder list, PCA-symmetric exclusion (Section 3.8 five-class typology), holding-HHI computation.

### Data sources

- EVM protocols: Dune queries on `tokens_ethereum.balances_daily` or `evms.balances` aggregated at month-end.
- Solana protocols: Helius DAS API plus Dune Solana tables.
- Substrate protocols: TAOSTATS API plus Subscan API.

### Expected outputs

- A monthly panel table (protocol by month by HHI plus covariates).
- Per-sector trajectory-slope estimation.
- An event-study scaffold for governance-reform events (delegation-program launches; vesting-cliff expirations; major governance passages).

---

## Cross-references

- Supplementary File S7 (the 14-protocol Q1-vs-Q8 panel; this trajectory analysis's source).
- Main paper Section 3.6 (longitudinal panel discussion).
- Main paper Sections 5.7 and 5.8 (cross-section-versus-longitudinal limitation; future research).
