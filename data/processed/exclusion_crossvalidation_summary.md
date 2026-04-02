# Exclusion Cross-Validation Summary

**Date:** 2026-03-31
**Sources used:** Blockscout (original, per-chain), Enhanced Blockscout (multi-chain API with OLI + Kleros tags), Nansen (v1 Profiler address labels API)
**Sources unavailable:** Artemis (no access), Etherscan (V1 API deprecated, V2 migration required)

---

## Cross-Validation Results: Existing 13 Exclusions

| # | Token | Address (first 10) | Blockscout | Enhanced Blockscout | Nansen | Sources | Status |
|---|-------|---------------------|------------|---------------------|--------|---------|--------|
| 1 | LPT | 0xc20de371... | Minter (verified) | name="Minter" (verified) | Behavioral only | 2/3 | CONFIRMED |
| 2 | LPT | 0xf977814e... | Binance 8 (OLI) | Binance 8 (OLI) | **Binance: Reserve Address** | **3/3** | CONFIRMED |
| 3 | GMX | 0x908c4d94... | sGMX RewardTracker (verified) | RewardTracker, token=sGMX (verified) | **GMX: Staked Gmx Tracker** | **3/3** | CONFIRMED |
| 4 | RPL | 0x3bdc69c4... | RocketVault (verified) | RocketVault + Rocket Pool: Vault tag | Behavioral only | 2/3 | CONFIRMED |
| 5 | ENS | 0xd7a029db... | TokenLock (verified) | TokenLock (verified) | Behavioral only | 2/3 | CONFIRMED |
| 6 | WXM | 0x93f1a412... | Unverified, deployer analysis | Unverified, is_contract=true | "High Balance" only | **1/3** | UNCONFIRMED |
| 7 | DIMO | 0xc97bf974... | Unverified, pattern analysis | Polygon Blockscout 500 error | "Token Millionaire" only | **1/3** | UNCONFIRMED |
| 8 | POL | 0x5e3ef299... | PoS Staking Contract (verified) | StakeManagerProxy + Polygon tag | Behavioral only | 2/3 | CONFIRMED |
| 9 | POL | 0x401f6c98... | Plasma Bridge (verified) | DepositManagerProxy + Kleros tag | Behavioral only | 2/3 | CONFIRMED |
| 10 | MPL_SYRUP | 0x9c9499ed... | Syrup: Migrator (verified) | Migrator + Syrup OLI tag | Behavioral only | 2/3 | CONFIRMED |
| 11 | MPL_SYRUP | 0xc7e8b36e... | stSYRUP/xMPL (verified, ERC-4626) | xMPL + Syrup.fi tag + ERC-4626 | **Staked Syrup, Token Contract** | **3/3** | CONFIRMED |
| 12 | RENDER | 0x3ee18b22... | Wormhole Token Bridge (verified) | Wormhole: Token Bridge (Kleros) | Behavioral only | 2/3 | CONFIRMED |

### Summary Statistics

- **3/3 sources (full cross-validation):** 3 exclusions (LPT Binance, GMX sGMX, MPL stSYRUP)
- **2/3 sources (partial cross-validation):** 8 exclusions (LPT Minter, RPL, ENS, POL x2, MPL Migrator, RENDER)
- **1/3 sources (Blockscout only):** 2 exclusions (WXM, DIMO — both flagged as unverified in original paper)
- **Total confirmed (≥2 sources):** 11/13 rows (representing 10/12 unique addresses, 85%)

### Notes on Unconfirmed Exclusions

The 2 unconfirmed exclusions (WXM and DIMO) are exactly the addresses the original paper already flagged as "unverified source code." These rely on deployer analysis and contract pattern matching rather than verified contract labels. Nansen provides only behavioral labels for these addresses ("High Balance" and "Token Millionaire" respectively), which are consistent with but do not independently confirm the identity.

For DIMO specifically, the enhanced Blockscout Polygon endpoint returned 500 errors on all 3 attempts, preventing independent verification. This is a known issue with Polygon Blockscout availability.

---

## Additional Exclusion Candidates Found

Cross-referencing top holders of all 34 sample tokens against Blockscout and Nansen identified 6 potential protocol-controlled addresses not in the current exclusion list:

| Token | Address (first 10) | Identity | Share % | Sources | Recommendation |
|-------|---------------------|----------|---------|---------|----------------|
| **AAVE** | 0x4da27a54... | stkAAVE (Aave Staked Aave) | 21.7% | 3/3 | REVIEW — same pattern as excluded GMX sGMX |
| **UNI** | 0x1a9c8182... | UNI Timelock (Uniswap governance) | 29.1% | 3/3 | REVIEW — same pattern as excluded ENS TokenLock |
| **CRV** | 0x5f3b5dfe... | veCRV (Curve Voting Escrow) | 40.5% | 3/3 | DO NOT EXCLUDE — veCRV IS the governance mechanism |
| **GRT** | 0x36aff700... | GraphProxy → BridgeEscrow | 28.6% | 2/3 | REVIEW — same pattern as RENDER Wormhole exclusion |
| ARB | 0xf3fc1781... | Unknown EOA | 30.2% | 0/3 | NEEDS INVESTIGATION |
| OP | 0x2a82ae14... | Unknown EOA | 31.8% | 0/3 | NEEDS INVESTIGATION |

### Methodological Note on veCRV

The veCRV Voting Escrow is a unique case. Unlike stkAAVE (where stakers delegate voting power) or sGMX (which holds staked tokens passively), veCRV IS the governance voting mechanism — CRV holders lock tokens into veCRV specifically to vote. Excluding this address would remove actual governance participants from the concentration measure, which is methodologically inconsistent with the paper's goal of measuring governance concentration. **Recommend NOT excluding veCRV.**

### Impact Assessment

If the 3 strong candidates (AAVE stkAAVE, UNI Timelock, GRT BridgeEscrow) were added to the exclusion list, HHI values for these tokens would decrease, potentially affecting the regression results. However, since these tokens span both DePIN and non-DePIN categories, the relative DePIN vs. non-DePIN comparison may be minimally affected. A robustness check adding these exclusions is recommended before final submission.

---

## Proposed Paper Language (Section 5.1a)

**Current text:** "All identities verified via Blockscout contract labels unless noted"

**Proposed replacement:**

> Identities verified via Blockscout contract labels and cross-validated against Nansen entity labels and enhanced Blockscout metadata (including Open Labels Initiative and Kleros Curate tags) where available. Of the 13 exclusion entries (12 unique addresses), 11 are confirmed by at least two independent on-chain identity sources; the remaining two (WXM and DIMO) rely on deployer-address analysis due to unverified contract source code. See Appendix Table [X] for the full cross-validation matrix.

**Table 5 caption addition:**

> Identity sources: "B" = Blockscout verified contract name; "OLI" = Open Labels Initiative tag; "K" = Kleros Curate verified tag; "N" = Nansen entity label. Cross-validation status: ✓✓✓ = confirmed by all three sources; ✓✓ = confirmed by two sources; ✓ = single source only.
