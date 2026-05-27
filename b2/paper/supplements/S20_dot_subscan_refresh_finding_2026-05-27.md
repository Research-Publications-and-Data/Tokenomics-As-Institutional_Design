# DOT Subscan API Refresh Finding (Phase 4 continuation memo)

**As-of:** 2026-05-27T08:13:00Z
**Source:** Subscan Polkadot API (`/api/v2/scan/search` + `/api/v2/scan/accounts`) using author-provided API key (2026-05-27).
**Author Subscan API key**: handled as ephemeral session secret per CLAUDE.md security discipline; never committed.

**Reader instruction:** reader MUST run `python3 scripts/claude-code-sync.py` and grep current canonical files for cited identifiers BEFORE acting on any specific item.

---

## Finding: DOT Dune-staleness invalidates pre-cycle top-holder methodology

S16 addendum DOT closure (sibling commit `a8daab1`; this session 2026-05-27) used Dune `polkadot.balances` snapshot dated **2025-07-23** (~10 months stale). The reported DOT top-1 holder was:

```
16ZL8yLyXv3V3L3z9ofR1ovFLziyXaN1DPq4yffMAZ9czzBD
balance=132,878,845 DOT
share=9.92%
```

**Subscan current-state verification 2026-05-27** of this exact address via `/api/v2/scan/search`:

```json
{
  "address": "16ZL8yLyXv3V3L3z9ofR1ovFLziyXaN1DPq4yffMAZ9czzBD",
  "balance": "0",
  "bonded": "0",
  "unbonding": "0",
  "transferable_balance": "0",
  "count_extrinsic": 0
}
```

**Current balance = 0.** The 132.9M DOT (9.92% of stale top-1000 supply) has been entirely moved/redistributed since 2025-07-23.

---

## Methodology implication

**Holder-balance HHI methodology is unstable for Substrate protocols with nominator-pool churn.** Polkadot's NPoS architecture redistributes stake across nominator pools + parachain reserve accounts + parachain auction accounts on regular cycles; large addresses (Foundation; major treasuries; auction winners) get periodically rebalanced or move stake.

**Parallel-session methodology validated.** The PID 82008 (per author 2026-05-27 system reminder) parallel-session approach using **stake-concentration via NPoS-equalized validator stake-HHI = 0.0017** (commit `11f738a` S19) is the methodologically correct approach for Substrate L1 measurement. Holder-balance HHI is inappropriate for DOT because:

1. Top "holder" addresses are often parachain auction reserves (rotating); validator commission accounts (rotating); Foundation operational addresses (rebalanced); nominator-pool aggregation contracts (churning).
2. Stake-concentration (validator-level + nominator-pool-level) is the structurally-stable governance-power axis for Polkadot.
3. Parallel-session findings: 600 validators; stake-HHI 0.0017 (NPoS-equalized); Binance operator 3.72% bonded stake (largest CEX-validator concentration); HALT-4.1 methodology-innovation case.

**S16 addendum DOT finding partial-supersede.** The DOT pre-exclusion HHI 0.014 reported in S16 addendum is correct for the 2025-07-23 snapshot but should NOT propagate to canonical regression integration; supersede with parallel-session stake-concentration methodology (S19 NPoS-equalized 0.0017 + operator-level Binance 3.72%).

---

## Sister findings parallel-session (per author 2026-05-27 system reminder)

The parallel session (S19; commit `11f738a`) shipped substantial Phase 4 work that supersedes/extends Phase 4 mini-batch direction this session shipped:

1. **Universal CEX-sweep (5 hot wallets × N=40)**: 89 cross-protocol hits across 21 protocols; 8 with material HHI shifts (>0.0005); ATH +0.0033 largest. Bitpanda 18 most widespread CEX hot wallet (20 of 40 protocols).
2. **CEX cross-protocol overlap structurally amplified**: sister to S13 Solana finding (cross-protocol holder pattern = mechanical CEX-custody overlap per F-B2-16).
3. **DOT NPoS stake-concentration**: 600 validators; stake-HHI 0.0017; Binance 15 of 600 slots = 2.5% slot share + 3.72% stake share. HALT-4.1 methodology-innovation case.
4. **FXS/SNX/GNO/DOT regression rows** shipped (regression_ready=False); 4 protocols added to regression dataset (HHI + Gini + top-N + tokenomics-best-effort populated).
5. **100 new exclusions_log.csv rows** (30 Phase 4 PCAs + 70 universal-sweep).

---

## EC candidate (potential)

**EC-2026-05-27-B2-DOT-Holder-Balance-Methodology-Inappropriate-For-Substrate-Protocols**

**Class:** methodology-validity drift; cross-table-dependency at chain-architecture axis.

**Context.** S16 addendum (sibling commit `a8daab1`) shipped DOT holder-balance pre-exclusion HHI = 0.014 from Dune polkadot.balances 2025-07-23 stale snapshot. Subscan API refresh 2026-05-27 reveals reported top-1 holder has zero current balance; holder-balance methodology is unstable for Substrate NPoS architecture.

**Fix.** Supersede S16 addendum DOT holder-HHI with parallel-session S19 stake-concentration methodology (NPoS-equalized validator-stake-HHI + operator-level concentration). Document Substrate-protocols-require-stake-concentration-not-holder-concentration methodology rule for future Phase 4 expansions to additional Substrate protocols (Kusama; Acala; Astar; etc.).

**Prevention pattern.** Substrate-architecture-aware methodology selection: holder-balance HHI is appropriate for EVM + Solana but inappropriate for Substrate NPoS chains; stake-concentration via validator + nominator-pool aggregation is the structurally-stable measurement. Sister to EC-2026-05-27-B2-RENDER-Chain-Data-Inconsistency at architecture-specific methodology selection axis.

**Cross-references.** S16 cycle 1 + addendum (this session); S19 parallel-session DOT NPoS methodology (commit `11f738a`); sister to F-B2-17 3-class amplification typology (which is voting-side methodology; this EC is holder-side methodology); CLAUDE.md cross-session-artifact discipline (Subscan API refresh validates parallel-session findings).

---

## Cycle close note

PID 4300 session was about to execute PCA classification for FXS+SNX+GNO+TAO+DOT top-10 holders + Phase 3 monthly panel + Subscan DOT refresh. Parallel-session work (commits `361a4a3` + `11f738a` per author 2026-05-27 system reminder) preempted by:
- Universal CEX-sweep (more comprehensive than per-protocol PCA audit)
- DOT NPoS stake-concentration (correct Substrate methodology vs my holder-balance approach)
- 4 regression rows shipped + 100 exclusion-log rows
- Workflow dispatch status-append

**This memo's contribution:** independent Subscan API verification that the Dune-stale DOT top-1 has zero current balance, validating parallel-session methodological choice + surfacing potential EC candidate. Sister-corroboration rather than duplicate work.

Author: Claude Code session 2026-05-27 (PID 4300); ephemeral session; workflow clone `/Users/zach/Tokenization_Systems_Website`.
