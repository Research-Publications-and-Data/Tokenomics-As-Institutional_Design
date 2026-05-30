# Supplementary File S24: Optimism worked example (full per-lens narrative)

**Companion to:** B2 paper *Tokenomics as Applied Political Philosophy: Governance Concentration Beyond Token Allocation* (Section 2.10.9 Worked Example: Optimism Protocol Scoring). Generated 2026-05-22.

---

## Abstract

This supplement provides the full per-lens narrative for the Optimism worked-example scoring presented in condensed form in Section 2.10.9 of the main paper. Optimism is chosen as the worked example because its bicameral architecture (Token House plus Citizens' House) exercises multiple lenses simultaneously and because the protocol publishes governance documentation at a level of detail that enables verifiable scoring. The full per-lens narrative reports cited governance documentation, scoring justifications, and operational mechanism observations supporting Optimism's Synergy Index of 2.8 (Kantian Publicity: 3; Rawlsian Fairness: 3; Pettit Contestation: 3; Ostrom Polycentricity: 3; Hayek Knowledge-use: 2).

## Cross-reference

This supplement supports Section 2.10.9 Worked Example. Main paper retains a condensed per-lens scoring summary (per-lens scores plus 1-sentence evidence pointer per dimension) plus the Synergy Index computation; this supplement reports the full per-lens evidence narrative with cited governance documentation and scoring-rationale detail.

---

## Worked example setup

Optimism is a Layer 2 (L2) network on Ethereum implementing a bicameral governance architecture:

- **Token House:** token-weighted upper chamber where OP holders vote on most protocol matters (parameter changes, treasury allocation, governance proposals).
- **Citizens' House:** identity-weighted lower chamber where reputation, not token holdings, determines voting weight; Citizens' House governs Retroactive Public Goods Funding (RetroPGF) rounds and exercises a formal veto power over economic parameters proposed by the Token House.

The bicameral structure exercises multiple philosophical lenses simultaneously, providing a rich worked example for the rubric.

---

## Per-lens scoring narrative

### Kantian Publicity (score: 3, Exemplary)

**Operational mechanism scored:** rules + rationales + procedural transparency for governance proposals.

**Evidence:**
- Optimism publishes governance proposals on Snapshot (off-chain signed voting) and Tally (on-chain transaction voting) with explicit rationales attached to each proposal (Optimism Governance Forum; Optimism, 2024).
- The Citizens' House process includes published deliberation periods during which stakeholders comment publicly on proposed economic parameters; deliberation transcripts are archived in the Optimism Governance Forum.
- Token House proposals require multi-stage review with public commentary periods at each stage; proposal authors must respond to stakeholder feedback before formal voting begins.

**Score justification:** the published-rules-plus-deliberation-plus-justification criterion of Table 1 (Exemplary tier) is satisfied. Proposals are not merely visible but accompanied by rationale and stakeholder commentary. The publicity standard exceeds the Partial tier (rules visible) and the Minimal tier (rules accessible on request).

### Rawlsian Fairness (score: 3, Exemplary)

**Operational mechanism scored:** floor-raising distributional mechanisms protecting the least-advantaged.

**Evidence:**
- Optimism's Retroactive Public Goods Funding (RetroPGF) program explicitly compensates public-goods contributors who would not be captured by token-weighted governance alone. RetroPGF rounds (Round 1-Round 5+) distribute treasury allocations to projects nominated by the broader ecosystem and voted on by the Citizens' House.
- RetroPGF rounds are documented with measured distributional gaps between token-holder-weighted preferences and Citizens'-House-weighted preferences; the gap is structurally informative about whose interests get funded under each weighting rule.
- Combined with the Citizens' House (reputation-weighted, not token-weighted), Optimism operationalizes the floor-raising mechanism Table 1 specifies at the Exemplary tier (systematic equity mechanisms plus measured gaps).

**Score justification:** the systematic-equity-plus-measured-gaps criterion at the Exemplary tier is satisfied. The Difference Principle (Rawls 1971 §13) interpretation of fairness is operationalized through a non-token-weighted distributional mechanism that compensates the structurally less-empowered.

### Pettit Contestation (score: 3, Exemplary)

**Operational mechanism scored:** formal appeals and veto infrastructure protecting from arbitrary interference.

**Evidence:**
- The Citizens' House exercises formal veto power over economic parameters proposed by the Token House, with dynamic veto thresholds that lower the trigger when multiple stakeholder groups align (Optimism, 2024).
- The veto mechanism is the precise independent-arbitration-plus-veto-rights mechanism Table 1 specifies at the Exemplary tier.

**Score justification:** the formal-appeals-plus-veto-infrastructure criterion at the Exemplary tier is satisfied. The two-layer-framing distinction is relevant here: the operational mechanism scored (contestability) is present at exemplary level; the philosophical goal-state Pettit identifies (non-domination) is a separate question that depends on the practical efficacy of veto exercise, which Section 3.5 documents as constrained by Token House delegation amplification (3.6x).

### Ostrom Polycentricity (score: 3, Exemplary)

**Operational mechanism scored:** multiple overlapping decision-centers with local autonomy.

**Evidence:**
- The bicameral architecture (Token House plus Citizens' House) plus the OP Working Group ecosystem instantiates nested governance with local autonomy at the Exemplary tier.
- Distinct decision-centers govern: protocol parameter changes (Token House); economic-parameter veto (Citizens' House); public-goods funding (RetroPGF rounds with broad ecosystem participation); operational coordination across the Superchain (OP Stack governance with cross-chain-coordination working groups).

**Score justification:** the nested-decision-centers-with-local-autonomy criterion at the Exemplary tier is satisfied. Optimism's governance does not concentrate all decision-making in a single body; distinct centers handle distinct decision categories with their own deliberation processes and voting rules.

### Hayek Knowledge-use (score: 2, Partial)

**Operational mechanism scored:** demand-coupled signal mechanisms aggregating dispersed information.

**Evidence:**
- Optimism does not employ DePIN-style demand-coupled emission mechanisms; the OP token does not have demand-coupled signal aggregation that directly maps to Hayek's knowledge-problem framing.
- However, sequencer-revenue split mechanisms (where Optimism Foundation routes a portion of sequencer revenue to the Citizens' House for RetroPGF) and Superchain governance signals (where Superchain participants coordinate on shared-sequencer architecture) provide automated price-signal-like coordination.

**Score justification:** the automated-price-signals criterion at the Partial tier is satisfied; the Exemplary tier (demand-coupled mechanisms with edge feedback) is not because the OP token's emission and value capture do not directly track end-user demand signals. The score is one tier below Exemplary because the price-signal-like coordination is at the Foundation-and-protocol layer rather than at the user-demand-aggregation layer.

---

## Synergy Index aggregation

Per-lens scores: Publicity 3 + Fairness 3 + Contestation 3 + Polycentricity 3 + Knowledge-use 2 = total 14.

**Synergy Index = 14 / 5 = 2.8.** Among the highest scores in the protocol sample.

The Synergy Index aggregates per-dimension Exemplary (3) scores on publicity, fairness, contestability, and polycentricity with a Partial (2) score on knowledge-use; the per-dimension scoring above documents the observable institutional features driving each score.

---

## Two-layer-framing caveat

The Synergy Index measures institutional design intent across normative traditions. It does not capture whether the institutional mechanisms scored at the operational layer actually produce the philosophical goal-states the traditions identify. This is the two-layer framing of the rubric:

- **Layer 1 (philosophical goal-state):** what the tradition aims to secure (e.g., non-domination for Pettit; fairness for Rawls).
- **Layer 2 (operational mechanism):** what is observable in protocol design and scored in Table 1 (e.g., appeals + veto rights as operational measures of contestability).

For Optimism, the operational mechanisms score at Exemplary across four of five lenses (Layer 2), but Section 3.5 of the main paper documents that the goal-state Pettit identifies (non-domination) is partially constrained by Token House delegation amplification (3.6x). The Citizens' House (reputation-weighted) provides a structural accountability layer that operates outside the token-weighted HHI measurement framework, partially addressing this gap; the empirical measurement of whether Citizens' House veto exercises actually constrain Token House outcomes is future work (see Section 4.9).

The two-layer framing also surfaces the Hayek Knowledge-use score: at Layer 2 (operational), Optimism's automated price-signal-like coordination satisfies Partial; at Layer 1 (philosophical goal), whether the price-signal coordination achieves Hayek's epistemic-coordination ideal depends on whether sequencer-revenue routing actually aggregates dispersed information about user demand, which Optimism does not currently measure publicly.

---

## What the worked example illustrates

1. **The framework is tractable.** The five-lens rubric can be applied to a real protocol with publicly-available governance documentation in a reasonable time frame, with scoring decisions traceable to specific cited evidence.

2. **The framework distinguishes operational mechanism from philosophical goal-state.** Optimism scores high on operational mechanisms (Synergy 2.8) but the Section 3.5 voting-power amplification (3.6x) reveals that goal-state achievement is conditional on factors beyond the operational design (delegation outcomes).

3. **Two-layer framing prevents conflation.** Without the two-layer distinction, a high Synergy Index would imply the philosophical goal-states are achieved; the framework's design prevents this conflation by scoring only operational mechanisms while flagging goal-state achievement as a separate empirical question (Section 3.5 voting-HHI evidence; Section 4.1 hypothesis evidence).

4. **Cross-protocol comparability is preserved.** Optimism's score is on the same 0-3 scale as the other 39 protocols in the cross-section (Table 4 + Supplementary File S3), enabling direct cross-protocol Synergy Index comparison.

---

## Cross-references

- Section 2.10.5 Philosophy Scoring Rubric (defines the 0-3 scale and per-criterion anchoring)
- Section 2.10.6 Outcome Variables (defines Synergy Index aggregation as arithmetic mean of five lens scores)
- Section 3.5 Voting Power vs Holding Concentration (documents Optimism's 3.6x Token House delegation amplification)
- Section 4.1 Design Hypotheses (maps Synergy Index scores to hypothesis evidence)
- Supplementary File S2 (full scoring rubric per criterion)
- Supplementary File S3 (full scoring tables for all 40 protocols including Optimism evidence sheet)

## Replication

Optimism scoring sheet at `b2/paper/supplements/S3_scoring_tables.md` (in the replication repository) provides the protocol × criterion scoring matrix with evidence links. Optimism Governance Forum (forum.optimism.io) and Optimism Foundation documentation (optimism.io/foundation) provide the source documentation cited in this supplement.
