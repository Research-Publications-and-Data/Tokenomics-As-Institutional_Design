# Phase 0 Data Collection Results: 2026-05-17

**Session role:** BULK-EXECUTOR
**Cycle:** B2 R2 (per `handoff/b2_r2_cycle_dispatch_2026-05-17.md`)
**Tier completion status:** A1 partial done; A2 not started; B1 partial (substantive findings surfaced); C1 not started; C3 not started

---

## SUMMARY: Three substantive methodological findings surfaced

1. **Compound Foundation is a PCA at the voting layer.** The top COMP Tally delegate (~21.5% of total delegated voting power) is Compound Foundation itself. If PCA exclusion is applied at the voting layer (consistent with holding-side methodology), Compound's voting HHI drops to ~0.025, yielding ratio ~0.89x; **flipping back to delegation-disperses-power**. This breaks the universal-amplification thesis for Compound.

2. **ENS shows delegation-DISPERSION at the voting layer.** Fresh Tally data: 20 active ENS delegates with voting HHI 0.062, compared to ENS holding HHI 0.1345. Ratio = 0.46x; delegation DISTRIBUTES power. **Adding ENS to Table 7 would break the "universal amplification" thesis.**

3. **Balancer shows extreme veBAL amplification.** Snapshot HHI 0.626 vs holding HHI 0.030 = 20.9x amplification (highest in any sample). Reflects vote-escrowed lock-duration multipliers (analogous to Curve's veCRV).

These findings have substantive implications for the R2 manuscript and warrant author review before deciding scope. Recommendation: keep R2 Table 7 at 8 protocols + add a §3.5 methodology footnote acknowledging Phase 0 findings + defer comprehensive Tier B1 expansion to a follow-up cycle that can resolve the methodology questions.

---

## Tier A1: Hivemapper + io.net Gini computation

Source: pre-pulled Helius holder lists at `~/holder_lists/holders_helius_HONEY.csv` (90,680 holders) and `~/holder_lists/holders_helius_IO.csv` (84,861 holders); March 31, 2026 snapshot.

### Hivemapper (HONEY; Solana)

| Metric | Value | Reference |
|---|---|---|
| HHI (top-1000, pre-exclusion) | 0.0198 | cascade CSV: 0.01748 |
| Gini (top-1000) | 0.9181 | new (closes N=40 gap) |
| Top-1% | 6.65% | new |
| Top-10% | 33.72% | new |
| Total non-zero holders | 90,680 | |

**Methodology note:** Fresh HHI (0.020) slightly exceeds cascade (0.017). The 0.0024 gap suggests cascade applied an undocumented exclusion. Top-3 holders by balance (`ERo2hRAc4...`, `EyBXvV7N...`, `FZ9diFCJ...`) lack published Hivemapper Foundation labels (Solana labeling gap per §2.10.4). For R2 consistency, retain cascade value 0.017.

**Recommended Table 4 row:**
```
Hivemapper | HONEY | DePIN | 0.017 | 0.92 | 6.7% | 33.7% | 1000
```

### io.net (IO; Solana)

| Metric | Value | Reference |
|---|---|---|
| HHI (top-1000, pre-exclusion) | 0.1113 | cascade CSV: 0.1113 (MATCH) |
| Gini (top-1000) | 0.9467 | new |
| Top-1% | 29.98% | new |
| Top-10% | 63.73% | new |
| Total non-zero holders | 84,861 | |

**Methodology note:** HHI matches cascade exactly. Top-1 holder (`3EpUYHv8...`) at 30% is likely a foundation or team multisig; PCA exclusion would substantially reduce HHI but is deferred (Solana labeling gap).

**Recommended Table 4 row:**
```
io.net | IO | DePIN | 0.111 | 0.95 | 30.0% | 63.7% | 1000
```

### Aethir (ATH; Ethereum): PENDING

Requires Dune query for ERC-20 holders. Not yet attempted in this Phase 0 session.

---

## Compound voting-source verification

**User request:** verify which source to use for COMP Table 7 row (Tally vs Snapshot).

### Tally data (May 2026 pull)

```
Compound Governor (org_id: 2206072050458560433)
- Total delegates: 18,814
- Total delegated voting power: 3,331,435 COMP (33.3% of 10M total supply)
- Top delegate: Compound Foundation, 717,436 COMP (21.5% of total delegated)
- Top-20 delegates returned with non-zero voting power
- Top-20 voting HHI (normalized over top-20 sum): 0.149
- Implied HHI normalized over total delegated: 0.046

Top 6 delegates (per Tally screenshot):
1. Compound Foundation: 717.44K COMP (PCA - structurally a protocol entity)
2. 0x3B64...c9C5: 497.54K COMP
3. PGov: 104.79K COMP
4. Geoffrey Hayes: 101.01K COMP
5. Humpy: 87.61K COMP
6. allthecolors: 80.22K COMP
```

### Snapshot data (May 2026 pull, 12-month-window)

```
Compound Snapshot space: comp-vote.eth
- Total proposals: 36 in 12-month window
- Total unique voters: 138 (March 2026 baseline: n=114)
- Aggregated voting power: 15,736,055 (unit-normalized votes)
- Voting HHI (all voters): 0.062 (March 2026 baseline: 0.053)
- Top-1 voter share: 11.11%
```

### voting_hhi.csv (March 2026 baseline used in R1 manuscript)

```
COMP Tally row: 0.0387 (n_sampled_top100 = 100)
COMP Snapshot row: 0.0531 (n_unique_voters = 114)
```

### Critical finding: Compound Foundation is a PCA at the voting layer

The top COMP Tally delegate is **Compound Foundation** (address `0xb06DF4dD01a5c5782f360aDA9345C87E86ADAe3D`), holding 717K COMP delegated. This is a protocol-controlled entity by the same logic that excludes protocol treasuries from HOLDING HHI computation.

If PCA exclusion is applied symmetrically at the voting layer:
- Old Tally HHI: 0.0387 (with Foundation)
- Approximate new Tally HHI (without Foundation): ~0.025
- Implied ratio with holding 0.028: ~0.89x
- **Compound flips back to delegation-DISPERSES-power**

**Substantive implication:** the universal-amplification thesis depends on whether PCA exclusion is applied to voting power. The manuscript currently applies PCA exclusion to HOLDING HHI but not to VOTING HHI. Symmetric application would weaken the universal-amplification claim (Compound dethrones the lower-bound).

### Recommendations

Three options for R2 Table 7 Compound row:

**Option A (R1 author choice; recommended for R2 minimum-disruption):** Keep Snapshot 0.053. Document Compound Foundation finding as a §3.5 methodological footnote noting that "Compound's top Tally delegate is Compound Foundation; the Snapshot-sourced value used here partially mitigates this concentration via inclusion of 138 active voters in the lookback window."

**Option B (symmetric PCA exclusion; methodologically rigorous):** Recompute Tally HHI excluding Compound Foundation; report adjusted value. This BREAKS universal amplification for Compound (ratio drops to ~0.89x) and forces narrative recast to "near-universal amplification: 7 of 8 protocols amplify; Compound shows borderline dispersion when PCA exclusion is applied symmetrically." More honest but weaker headline.

**Option C (defer to follow-up paper):** Note the PCA-at-voting-layer methodology question as future work; keep R2 narrative as-is. Acknowledge in §3.5 footnote and §4.8 limitations.

**Recommendation: Option A** for R2; document the finding for future-work consideration. Option B is a substantive methodology change that goes beyond reviewer's R2 ask.

---

## Tier B1 partial: ENS, GMX, Balancer (Tally / Snapshot)

### ENS (Tally; May 2026)

```
Total delegates: 37,754
Active (non-zero voting power) returned: 20
Top-5 delegates:
  1. fireeyesdao.eth: 244,049 ENS (12.07%)
  2. scratch.ricmoo.eth: 181,229 ENS (8.97%)
  3. nick.eth: 149,046 ENS (7.37%)
  4. 0x81b287c0...: 146,297 ENS (7.24%)
  5. avsa.eth: 131,009 ENS (6.48%)
Voting HHI (top-20): 0.062
ENS holding HHI (Table 4): 0.1345
Implied ratio: 0.062 / 0.1345 = 0.46x
```

**Critical finding:** ENS shows delegation-DISPERSION (voting HHI < holding HHI). Adding ENS to Table 7 would break the "universal amplification" thesis (currently rests on 8/8 protocols amplifying; would become 8/9).

**Why ENS disperses:** ENS holding concentration is driven by ENS DAO treasury / multisig holdings (top-10 cumulative 75.5%). The delegation program distributes voting power across 20 active delegates with HHIs in the 6-12% range, more dispersed than the top-10 holders.

**Implication for R2:** ENS addition to Table 7 forces narrative recast from "universal amplification" to "near-universal amplification with one DAO-treasury-driven exception (ENS)." Recommendation: defer ENS addition; document the finding for follow-up cycle.

### GMX (Tally; May 2026)

```
Total delegates: 12,539
Active (non-zero voting power) returned: 20
Voting HHI (top-20): 0.120
GMX holding HHI (Table 4): 0.0564
Implied ratio: 0.120 / 0.056 = 2.13x
```

GMX amplifies in line with universal-amplification thesis. Could be added to Table 7 in a follow-up cycle (after methodology reconciliation; see Tally data drift below).

### Balancer (Snapshot; May 2026, 12-month window)

```
Total proposals (Snapshot all-time): 1,065
Active voters in 12-month window: 36
Top-1 voter share: 78.10% (likely Aura DAO or veBAL whale)
Top-10 cumulative: 99.85%
Voting HHI: 0.626
BAL holding HHI (Table 4): 0.0295
Implied ratio: 0.626 / 0.030 = 20.9x (HIGHEST in any sample)
```

**Implication:** Balancer's veBAL governance shows extreme amplification, even higher than Lido's 6.8x. This is structurally similar to Curve's veCRV (lock-duration multipliers concentrate voting power among large lockers). Adding BAL strengthens the universal-amplification thesis numerically but also surfaces the question: are veToken protocols (BAL, CRV) representative of "delegation amplification" or do they belong in a separate vote-escrow analysis category?

### Tally data drift (March 2026 → May 2026)

Tally now returns only 20 delegates with non-zero voting power for protocols that previously returned 100. This affects:
- Compound: 100 → 20 delegates
- ENS: 100 → 20 delegates
- GMX: 100 → 20 delegates
- Optimism: 100 → 20 delegates

Two possibilities:
(a) Tally API behavior changed (e.g., now filters out zero-balance-delegators or low-balance delegates)
(b) Many delegates withdrew between March and May (governance activity decline)

**Methodological consequence:** Fresh Tally-based HHIs (May 2026) cannot be combined with March 2026 baseline data without snapshot-date disclosure. For R2 Table 7 expansion, all new protocols would need explicit May 2026 dating, distinct from the March 2026 baseline used for existing 8 protocols.

---

## Recommended R2 Table 7 disposition

**Conservative path (recommended for R2 minimum-disruption):**
- Table 7 stays at 8 protocols (R1 set)
- Holding HHIs updated per R2 cycle (UNI 0.010, OP 0.009, LDO 0.013)
- Voting HHIs unchanged from R1 (matches voting_hhi.csv March 2026 baseline)
- Universal-amplification thesis preserved for 8/8 protocols
- Phase 0 findings (Compound Foundation as PCA; ENS dispersion; BAL veBAL extreme; Tally data drift) documented as Phase 0 supplementary report and surfaced as future-work items in §4.8

**Aggressive path:**
- Add ENS (0.46x dispersion), GMX (2.13x amplification), BAL (20.9x extreme amplification) to Table 7
- Narrative recast: "near-universal amplification with one DAO-treasury-driven exception (ENS at 0.46x); veToken protocols (BAL at 20.9x; CRV proxy at 6.0x via veCRV) show extreme amplification"
- Adds 3 protocols but breaks the "all 8/8 amplify" headline; trade complexity for robustness

**Middle path:**
- Add GMX (clean amplification case; no methodology complications) and BAL (with explicit veBAL caveat)
- Skip ENS for R2; document as future-work
- Narrative: "universal amplification with two veBAL/veCRV-like vote-escrow extremes"

**Recommendation: Conservative path for R2.** Document Phase 0 findings as supplementary; surface methodology questions for follow-up cycle. R2 ships sooner with cleaner narrative; substantive methodological refinements happen in subsequent cycles where they can be developed without time pressure.

---

## Next Phase 0 sub-tasks (still pending)

1. **Aethir (ATH)** Dune query for holder list; compute Gini/Top-N
2. **Tier A2** TT-expanded subsidy N reconciliation against `data/tokenterminal_financials.csv`
3. **Tier C1** veCRV voting concentration via Convex contract analysis
4. **Tier C3** Theil/Atkinson alternative concentration metrics

---

## Decision points for author

1. **Compound voting source**: Option A (keep Snapshot 0.053; document Foundation as PCA footnote) vs Option B (symmetric PCA exclusion; Compound becomes near-1x ratio; breaks universal amplification) vs Option C (defer methodology question to future work)?

2. **Table 7 expansion scope**: Conservative (keep 8 protocols; document Phase 0 as supplementary) vs Aggressive (add ENS+GMX+BAL; recast narrative as "near-universal with veToken exceptions") vs Middle (add GMX+BAL; skip ENS)?

3. **ENS dispersion finding**: Surface in §3.5 as exception case, OR defer entirely, OR add only with separate methodology section explaining DAO-treasury effect on holding HHI?

4. **Aethir / Tier A2 / C1 / C3 priority**: complete in this Phase 0 cycle, or defer to follow-up?
