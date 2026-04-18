# Supplementary File S7 — Quarterly HHI Panel for 14 Governance Tokens

**Companion to:** Zukowski (2026), "Tokenomics as Institutional Design: A Normative Framework and Governance Concentration Analysis"

**Section reference in main paper:** §4.9 Future Research

**Files in this supplement:**
- `S7_hhi_panel.md` (this document)
- `exhibit_k1_hhi_decay.png` (Exhibit S7, governance HHI trajectories)
- `exhibit_k1_panel_full.csv` (replication data, 14 protocols × 8 quarters)

---

## 1. Purpose

The cross-sectional analysis reported in the main paper documents that initial allocation design does not predict governance concentration (Pearson r = 0.19, p = 0.25, N = 37). This supplementary file extends the cross-section to a quarterly panel for 14 governance tokens with at least eight quarters of post-token-generation event (TGE) holder data, providing longitudinal context for the cross-sectional null.

The panel is descriptive rather than causal. It documents the trajectory of holding-based Herfindahl-Hirschman Index (HHI) values across the eight quarters following each protocol's TGE, allowing the cross-sectional snapshot to be situated within the temporal evolution of governance concentration after token launch.

## 2. Sample

Fourteen governance tokens were selected from the 40-protocol main-paper cross-section based on three inclusion criteria:

1. At least eight quarters of holder data available via Dune Analytics or the Helius DAS API
2. TGE date prior to Q1 2024 (ensuring eight quarters of observation by the March 2026 snapshot)
3. Sufficient holder count throughout the observation window to compute HHI from top-1,000 holders post-exclusion

The fourteen-protocol sample is a subset of the main-paper cross-section and uses identical exclusion methodology (Section 5.1a of the main paper, Supplementary File S6).

## 3. Methodology

For each protocol-quarter, holding-based HHI was computed using the same procedure as the main paper cross-section: top-1,000 holders by balance, protocol-controlled addresses excluded, balance shares squared and summed. Quarter boundaries follow standard calendar quarters (Q1 = Jan-Mar, Q2 = Apr-Jun, Q3 = Jul-Sep, Q4 = Oct-Dec).

Quarter 0 (Q0) is defined as the calendar quarter containing each protocol's TGE. Subsequent quarters are indexed Q1 through Q7. The eight-quarter window provides approximately two years of post-launch observation for each protocol.

## 4. Findings

Eleven of the fourteen protocols exhibit monotonic governance HHI decay across the observation window, indicating that concentration declines over time as initial token allocations distribute through secondary markets, vesting unlocks, and continued issuance.

Three protocols deviate from the monotonic decay pattern, each for a mechanism-specific reason:

- **Curve (CRV)** uses a vote-escrow (veCRV) mechanism that locks tokens in exchange for boosted voting power. The lock-duration multiplier concentrates effective voting power among long-duration lockers, producing a non-monotonic trajectory in the holding-based HHI as the underlying CRV distribution and the veCRV claim distribution evolve on different schedules.
- **Compound (COMP)** distributes tokens through a reservoir-drip mechanism that releases approximately 2,312 COMP per day to suppliers and borrowers proportional to interest accrued. The continuous distribution mechanism produces a slower decay trajectory than allocation-based protocols, with concentration declining steadily but not monotonically as drip rewards offset selling pressure unevenly across quarters.
- **ENS (ENS)** distributes tokens through a one-time claim window for historical ENS users, after which no further claims occur. The claim-window structure produces a step-function in the holding distribution as new claimants enter the holder population, generating a non-monotonic HHI trajectory.

The eleven monotonic-decay protocols span multiple sectors (DePIN, DeFi, infrastructure) and multiple distribution mechanisms (airdrops, liquidity mining, public sale, hybrid). The shared trajectory pattern is consistent with the cross-sectional finding that initial allocation design does not predict steady-state concentration: protocols with very different launch allocations converge toward similar concentration levels through post-distribution market dynamics.

## 5. Caveats

The eight-quarter window captures the early-stage trajectory of each protocol's governance distribution but does not capture longer-term equilibrium dynamics. Several protocols in the sample are still within their initial vesting cliff windows, meaning observed HHI changes partially reflect contractual unlocks rather than market-driven redistribution.

The decay pattern documented here is descriptive across the sample and should not be interpreted as a universal property of governance tokens. Newer protocols with different distribution mechanisms (points-based programs, retroactive airdrops, fee-funded buyback-and-redistribute) may produce different trajectories.

The panel uses calendar quarters rather than calendar months to balance observation density against measurement noise. Higher-frequency observation would be feasible for protocols with daily holder snapshots in Dune but is not currently part of the replication infrastructure.

## 6. Replication

The CSV file `exhibit_k1_panel_full.csv` contains the underlying data with the following schema:

| Column | Description |
|---|---|
| protocol | Protocol ticker (e.g., COMP, CRV, ENS) |
| quarter | Quarter index relative to TGE (Q0 through Q7) |
| calendar_quarter | Calendar quarter (e.g., 2022-Q1) |
| hhi | Herfindahl-Hirschman Index (post-exclusion, top-1000 holders) |
| top10_share | Combined balance share of the top 10 holders |
| n_holders | Total holder count for that protocol-quarter |

The exhibit `exhibit_k1_hhi_decay.png` plots the fourteen HHI trajectories across the eight-quarter window, with the three non-monotonic protocols (Curve, Compound, ENS) highlighted in distinct colors.

Replication of the panel from raw on-chain data requires the Dune Analytics queries and Helius DAS API calls documented in Supplementary File S5 (Empirical Pipeline Specification) and Supplementary File S6 (Data Sources and Exclusion Methodology).

## 7. Cross-references in the main paper

§4.9 Future Research describes longitudinal governance tracking as a research priority and references this supplementary file: "A companion panel analysis of quarterly HHI trajectories for 14 governance tokens (Supplementary File S7) documents that 11 of 14 protocols exhibit monotonic governance HHI decay over 24 months post-token-generation event, with vote-escrow (CRV), reservoir-drip (COMP), and claim-window (ENS) designs as exceptions; this longitudinal pattern is consistent with the cross-sectional allocation null reported in Section 3.4."

The longitudinal pattern complements the cross-sectional null (Pearson r = 0.19, p = 0.25, N = 37) by indicating that the absence of an allocation-concentration relationship in the cross-section is not an artifact of measurement at a single point in time. The same null relationship holds when concentration is observed across multiple quarters of post-launch evolution.
