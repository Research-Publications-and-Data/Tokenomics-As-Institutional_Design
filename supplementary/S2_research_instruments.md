# S2: Research Instruments

## Philosophy-to-Design Scoring Rubric

This rubric translates five normative traditions into observable institutional design criteria scored 0-3 per protocol. The rubric is designed for inter-rater reliability testing (future work) and replication across protocol samples.

### Scoring Scale

| Score | Label | Definition |
|-------|-------|------------|
| 0 | Absent | No observable evidence of the criterion in protocol documentation, governance forums, or on-chain mechanisms |
| 1 | Minimal | Criterion partially addressed; evidence is informal, inconsistent, or not codified in protocol rules |
| 2 | Partial | Criterion substantially addressed; formal mechanisms exist but with documented gaps or untested edge cases |
| 3 | Exemplary | Criterion fully addressed; mechanisms are codified, tested under stress, and publicly documented |

### Scoring Procedure

1. For each protocol, gather evidence from: official documentation (whitepapers, governance docs), governance forums (Discourse, Commonwealth, Snapshot), on-chain governance activity (Tally, Snapshot proposals and votes), and code repositories (parameter governance, access controls).

2. Score each criterion 0-3 using the definitions below. Record the primary evidence source for each score.

3. Compute the lens score as the unweighted mean of its criteria.

4. Compute the Synergy Index as the unweighted mean of all five lens scores.

5. Flag any criterion where evidence is ambiguous or contested. These are excluded from reliability testing.

---

## Lens 1: Kantian Publicity

**Core principle:** Rules must be publicly justifiable. Mechanisms requiring secrecy to function are illegitimate.

| Criterion ID | Criterion | 0 (Absent) | 1 (Minimal) | 2 (Partial) | 3 (Exemplary) |
|-------------|-----------|------------|-------------|-------------|----------------|
| PUB-1 | Rule transparency | No public documentation of tokenomics or governance rules | Whitepaper exists but parameters are undocumented or stale | Current parameters documented; change history partially available | All parameters documented, versioned, and machine-readable; change history complete |
| PUB-2 | Proposal rationale | No governance proposals or rationales published | Proposals exist without rationale or with minimal justification | Proposals include rationale; some lack quantitative impact analysis | Proposals include rationale, impact analysis, and community discussion period |
| PUB-3 | Enforcement transparency | Slashing, bans, or sanctions applied without published criteria | Criteria exist but enforcement is discretionary or inconsistent | Published criteria with documented enforcement; some edge cases unaddressed | Published criteria, consistent enforcement, public audit trail of all actions |
| PUB-4 | Information symmetry | Insiders have material information advantages over token holders | Some information asymmetry; team communications partially public | Most governance-relevant information public; team updates regular | Full information parity; no insider advantage on governance-relevant data |

## Lens 2: Rawlsian Fairness

**Core principle:** Institutional design should protect the least advantaged participants. Inequalities are acceptable only if they benefit the worst-off.

| Criterion ID | Criterion | 0 (Absent) | 1 (Minimal) | 2 (Partial) | 3 (Exemplary) |
|-------------|-----------|------------|-------------|-------------|----------------|
| FAIR-1 | Floor protection | No minimum reward, no protection against exploitation | Minimum participation threshold exists but is not enforced | Enforced minimums; small operators receive baseline rewards | Progressive reward structure; explicit floor guarantees; hardship provisions |
| FAIR-2 | Access equity | Participation requires substantial capital or technical expertise | Lower barriers than competitors; some accessibility features | Multiple participation tiers; documentation for non-technical users | Permissionless entry at minimal cost; accessibility-first design; multilingual docs |
| FAIR-3 | Distribution fairness | Token allocation >70% insiders; no community distribution | Mixed allocation; some community distribution but insider-dominated | Substantial community allocation (>40%); airdrop or mining distribution | Broad distribution design (>60% community); sub-linear scaling; anti-whale mechanisms |
| FAIR-4 | Governance accessibility | Governance participation requires high token threshold | Proposal threshold exists; delegation available but not promoted | Active delegation; funded delegate programs; low proposal thresholds | Compensated delegation; representative structures; governance incentives for small holders |

## Lens 3: Republican Non-Domination (Pettit)

**Core principle:** Freedom from arbitrary interference. No single actor should have the power to unilaterally impose decisions on others.

| Criterion ID | Criterion | 0 (Absent) | 1 (Minimal) | 2 (Partial) | 3 (Exemplary) |
|-------------|-----------|------------|-------------|-------------|----------------|
| NDOM-1 | Contestability | No mechanism to challenge governance decisions | Informal objection process; no binding appeal | Formal contestation mechanism (veto, timelock, optimistic governance) | Multi-stage contestation with independent adjudication; fork as credible exit |
| NDOM-2 | Concentration limit | HHI > 0.25 (single entity can dominate) | HHI 0.15-0.25 (high concentration; domination risk) | HHI 0.05-0.15 (moderate concentration; coalition needed) | HHI < 0.05 (distributed; no single entity dominates) |
| NDOM-3 | Emergency powers | Team/foundation retains unilateral emergency powers with no sunset | Emergency powers exist with informal constraints | Emergency powers with timelock, multisig, or sunset clause | Emergency powers require supermajority approval; automatic sunset; public audit |
| NDOM-4 | Exit rights | No credible exit; token locked or illiquid | Exit possible but penalized (slashing, lockup) | Exit available with reasonable notice period | Unconditional exit; ragequit mechanism; fork-friendly architecture |

## Lens 4: Ostromian Polycentricity

**Core principle:** Distributed decision-making centers with localized authority outperform centralized governance for heterogeneous communities.

| Criterion ID | Criterion | 0 (Absent) | 1 (Minimal) | 2 (Partial) | 3 (Exemplary) |
|-------------|-----------|------------|-------------|-------------|----------------|
| POLY-1 | Decision centers | Single governance body for all decisions | Some informal delegation of authority | Formal sub-governance (subDAOs, committees, working groups) | Multiple autonomous decision centers with independent budgets and authorities |
| POLY-2 | Local adaptation | One-size-fits-all parameters across all contexts | Minor parameter variation by context | Context-specific parameter governance (e.g., per-market, per-region) | Full local governance with bounded autonomy; nested rule-making |
| POLY-3 | Cross-scale coordination | No coordination mechanism between decision centers | Informal coordination; shared communication channels | Formal coordination protocols; resource sharing agreements | Constitutional meta-governance; arbitration mechanisms; shared standards with local implementation |
| POLY-4 | Subsidiarity | All decisions made at top level regardless of scope | Some decisions delegated informally | Formal subsidiarity principle; decisions pushed to lowest competent level | Explicit subsidiarity with escalation rules; local decisions default; central only for externalities |

## Lens 5: Hayekian Knowledge Use

**Core principle:** Decentralized systems should channel dispersed local knowledge through price signals, reputation mechanisms, and competitive discovery processes.

| Criterion ID | Criterion | 0 (Absent) | 1 (Minimal) | 2 (Partial) | 3 (Exemplary) |
|-------------|-----------|------------|-------------|-------------|----------------|
| KNOW-1 | Price signals | No market-based signal for resource allocation | Basic fee mechanism; fixed or administered prices | Dynamic fee mechanism responsive to demand (e.g., congestion pricing) | Multi-dimensional price signals; location-based, quality-based, and time-based pricing |
| KNOW-2 | Local knowledge | Protocol ignores participant-specific information | Some participant input via governance proposals | Structured feedback mechanisms; participant data informs parameters | Automated parameter adjustment from local conditions; oracle-mediated knowledge aggregation |
| KNOW-3 | Competitive discovery | Single implementation; no competition for roles | Limited competition; high barriers to entry for operators | Open competition with published performance metrics | Active market for operator roles; transparent ranking; permissionless entry; reputation systems |
| KNOW-4 | Information aggregation | No mechanism to aggregate distributed information | Governance voting as sole information channel | Prediction markets, signaling mechanisms, or structured deliberation | Futarchy or continuous prediction markets for parameter governance; multi-channel aggregation |

---

## Scoring Sheet Template

For each protocol, complete one row per criterion:

| protocol | lens_id | criterion_id | score | evidence_url | evidence_summary | scorer_initials | date |
|----------|---------|-------------|-------|-------------|------------------|----------------|------|
| [name] | PUB | PUB-1 | [0-3] | [URL] | [brief note] | [initials] | [YYYY-MM-DD] |

Store completed sheets in `supplementary/S3_scoring_tables.csv`.

## Reliability Protocol (Future Work)

1. Select 10% of protocols (minimum 4) for double-coding.
2. Second scorer receives protocol documentation pack but not first scorer's ratings.
3. Compute Cohen's kappa per criterion and per lens.
4. Adjudicate disagreements where kappa < 0.6 via structured discussion.
5. Report final kappa values and adjudication rate in paper.
