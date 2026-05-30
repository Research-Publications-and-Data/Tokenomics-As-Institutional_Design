# B2 session handoff: reproduction pipeline + retention re-fetch + audit + gap-fills

**As-of:** 2026-05-30T02:27:39Z. **Reader MUST** run `python3 scripts/claude-code-sync.py` and
grep current canonical files for every cited identifier BEFORE acting; canonical + dataset state
advances across parallel sessions and may have moved past this as-of timestamp.
**Clone:** all work landed in clone-A `/Users/zach/Tokenomics-As-Institutional_Design`
(`b2/paper/analysis_n52_2026-05-29/`); 12 local commits this session, none pushed.
**Companion handoff-back:** `/tmp/b2_replication_reproduction_handoff_back_to_canonical_writer_2026-05-29.md`
(the CANONICAL-WRITER / response-letter / docs items).

## What was executed (12 commits, 713db48..a1e61da)

1. **713db48 + f53c248 -- the original dispatch** (`handoff/dispatch/b2_replication_package_
   reproduction_pipeline_2026-05-29.md`). Took over as sole executor from 2 stopped parallel
   sessions. Built `reproduce.py` (repo root; one-command, deterministic, no /tmp/live-API):
   regenerates new-cohort HHIs from raw (9/9 exact), the retention-spec (N=49) + maturity-spec
   (N=50), de-tautology (both stats, column-bug-fixed), reconciled to VERIFIED_NUMBERS. Re-fetched
   the new-12 insider retention (Nansen token_current_top_holders, free-providers-first); f53c248
   corrected the insider definition to the original-methodology rule
   (`analysis/03_insider_classification.py` line 127: team/investor/founder/foundation/treasury/
   multisig) -- the "S2" boundary.
2. **ae354d5, c64e501** -- supplements: exchange-held % null + the PCA-vs-insider decomposition
   (concentration signal lives in the foundation/team overlap); float-to-FDV + revenue-to-FDV null.
3. **52b12e1** -- incentive-value-over-time (part b, proxy method) + CoinGecko coverage 40->50
   (fetched 10 new-cohort daily series). Honest negative: the supply-delta proxy is unlock-
   dominated (2-400x off Token Terminal), NOT clean incentives.
4. **ce91f4d** -- DISCOVERY: DefiLlama free CDN (`defillama-datasets.llama.fi/emissions/<slug>`)
   is the schedule-method + unlock-netting source (33/50; rawEmission is CUMULATIVE -> diff).
5. **fea6287** -- acquisition scope for the 17 not-in-DefiLlama; sources saved VERBATIM
   (`acquisition_sources/`: 17 CoinGecko JSONs + 10 tokenomist.ai HTMLs).
6. **aa657a9** -- pre-built Dune dashboards for the 17 (official handles + verified queries;
   NOTE: the search fan-out's autonomous agents also CREATED 3 queries, see memory
   `workflow-agents-escalate-read-to-write-tools-2026-05-29`).
7. **39edb10** -- AUDIT of insider + PCA + retention calcs.
8. **e9c94e5** -- gap-fill G1: consolidated machine-readable PCA-exclusion log.
9. **519efaf** -- resolution of remaining audit gaps G3-G8.
10. **a1e61da** -- scope: more Nansen runs (44/50 reachable).

## Audit result (the spine; from 39edb10 + 519efaf)

CALCULATIONS ARE ARITHMETICALLY CORRECT: insider_count_frac=count/n, balance in [0,1],
all_insiders, de-tautology rho=0.544 N=34, new-12 vector==provenance, column bug confirmed +
correctly avoided (reproduce.py uses non_insider_hhi_approx, not the buggy _top10). Gaps are all
BOOKKEEPING, not math:
- **G1 (FILLED):** exclusions were scattered across 6+ sources. `b2_pca_exclusions_consolidated_
  2026-05-29.csv` (252 rows/49 tokens) now merges them; recompute reproduces 45/50.
- **JUP/DRIFT/HNT: FRAME STALE** -- the S13 Solana CEX exclusions are already in exclusions_log
  but the regression `hhi` was never refreshed (frame holds the pre-S13 value). The log is
  correct (JUP 0.126, DRIFT 0.057, HNT 0.087). Refresh is HEADLINE-SAFE (maturity 0.0395,
  retention 0.0443, MW 0.0390; all <0.05).
- **IO, DOT: SPECIAL METHOD** -- IO = R2 rescaled top-100 (not raw-reproducible); DOT = AssetHub
  capture differs from clone-A holder list. Provenance documented; need re-capture to reproduce.
- **G3, G5 resolved** (UNI gov_conc cell is an isolated error; v3 full_hhi is baseline-adjusted
  not stale; GTC/TEC immaterial). **G4, G6 not computable** (per-address insider flags not
  persisted; need re-derivation).

## OPEN AUTHOR DECISIONS (surfaced, NOT applied -- frame untouched all session)

1. **Retention-spec DePIN p reproduces at 0.040, NOT the prose-locked 0.014-0.016.** Finding
   holds (both specs significant; retention n.s. = channel-shift). Update the claim of record
   (`handoff/dispatch/b2_r3_explanatory_model_reframe_2026-05-29.md` Section 7) + the R2 response
   letter to 0.040.
2. **S2/S3 + G7/G8 boundary (ONE decision):** foundation/team/multisig surviving addresses --
   keep (S2, current: in HHI + counted as insider retention) vs PCA-strict tighten (exclude as
   Class-2/3). Tightening STRENGTHENS the headline (maturity p 0.0395->0.0140, retention 0.0409->
   0.0107, MW 0.0364->0.0201; lowers inflated DeFi HHIs e.g. WLFI 0.156->0.066) but changes
   published HHIs + re-derives WLFI/ENA/KMNO retention. Same as the GNO co-founder question.
3. **Refresh the 3 frame-stale Solana HHIs** (JUP/DRIFT/HNT) to the log-consistent S13 values
   (headline-safe).
NOTE: `data/processed/regression_data_april2026.csv` had uncommitted parallel-session changes
(` M`) ALL session -- do NOT mutate it; the author/next-session reconciles.

## NEXT CYCLE (interrupted at 99% context): the 44-protocol Nansen re-classification

The high-value campaign that closes G4/G6/G7 (scope: `b2_nansen_quality_samplesize_SCOPE_2026-
05-29.md`). Nansen reaches 44/50 (NOT FIL/POKT/HYPE/ALGO/DOT/TAO). Plan:
1. For each of the 44 (list + chains in the scope memo): get the token contract, run
   `token_current_top_holders` (one cheap call/token), cross-ref the post-exclusion top-10
   survivors against the labels, classify insider + PCA-class per the consistent rule.
2. Contracts: new-12 + ZRO already resolved (ZRO=0x6985884C4392D348587B19cb9eAAf157F13271cd,
   demoed -- its top-10 resolved fully: LayerZero Future Initiatives/Foundation/Multisigs +
   Investment Recipient + CEX + retail). Resolve the other ~32 via known ERC20s + Nansen
   general_search for gaps. Solana mints: JUP/DRIFT/HNT/GRASS/HONEY/IO/RENDER_SOL/PUMP/JTO/BONK/
   KMNO/W/META.
3. Output: ONE machine-readable insider+PCA classification (all 44), recomputed insider_count_frac,
   reconciliation vs v3 (FLAG where it differs -- it may; version it, do NOT silently overwrite
   v3 per the audit's consistency warning), and re-run reproduce.py + the de-tautology.
4. Cost: ~44 token_current_top_holders + ~20-40 premium-labels (500cr) for decision-flippers.
   Free providers (Blockscout MCP / Helius / Etherscan) first per the original REFETCH_HANDOFF.
Then (separate): sample-size expansion (+15-30 EVM/Solana protocols -> N~65-80) to de-risk the
marginal + LOO-fragile headline; bottleneck is holder-list capture (Dune/Sim) + covariates, not
Nansen.

## Key reproducible artifacts (clone-A `b2/paper/analysis_n52_2026-05-29/` + repo-root reproduce.py)

reproduce.py; b2_new12_retention_classify + new12_retention_vector/provenance/residual_ambiguity;
b2_exchange_vs_pca_insider + b2_derived_metrics (+ findings); b2_incentive_value_timeseries (+
coingecko_new10/) + b2_schedule_method_DISCOVERY + defillama_emissions/; b2_17_acquisition_SCOPE +
acquisition_sources/ + b2_17_dune_dashboards_gapfill; b2_insider_pca_retention_AUDIT +
b2_pca_exclusions_consolidated + b2_pca_consolidation_GAPFILL + b2_remaining_gaps_RESOLUTION;
b2_nansen_quality_samplesize_SCOPE. All scripts: no /tmp, no live-API (except the explicit
CoinGecko/DefiLlama/Nansen fetch scripts, which are separate + keyed).
