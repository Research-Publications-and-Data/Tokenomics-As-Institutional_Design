# S6: Revenue and Subsidy Ratio Standardization

**Applies to:** `data/regression_data_april2026.csv`, `data/covariates_merged.csv`
**Last updated:** 2026-03-31

---

## Metric Definitions

| Metric | Source field | Definition |
|--------|-------------|------------|
| **Protocol revenue** | `revenue` (Token Terminal) | Fees retained by the protocol after paying LPs, lenders, or other service providers |
| **Token incentives** | `token_incentives` (Token Terminal) | Dollar value of tokens distributed to participants (liquidity mining, staking rewards) |
| **Subsidy ratio** | Derived | `token_incentives / revenue` (DEC-023 convention) |

---

## DeFi Protocol Subsidy Ratios (B2 Baseline)

Subsidy ratio correlates with concentration in the primary on-chain specification (r = 0.58, p = 0.007, N = 20), though this result is driven by Livepeer (see §5.7 and Supplementary File S8). These DeFi values establish the baseline against which DePIN protocols are compared.

| Protocol | Revenue (35mo) | Token Incentives (35mo) | Subsidy Ratio | Holding HHI |
|----------|---------------|------------------------|---------------|-------------|
| MakerDAO | $790.4M | $0.0M | **0.00x** | 0.045 |
| Aave | $135.4M | $50.2M | **0.37x** | 0.020 |
| Compound | $23.0M | $36.5M | **1.59x** | 0.027 |
| Curve | $92.7M | $277.7M | **3.00x** | 0.171 |
| Uniswap | ~$3.0M | $36.5M | **N/A** | 0.032 |

**Formula:** All values use `incentives / revenue` (DEC-023 convention), allowing values > 1.0x
for subsidy-dominant protocols (e.g., Livepeer 88.5x). Aave values sourced from regression_data_april2026.csv
(Token Terminal live pull, April 2026: revenue=$135.4M, incentives=$50.2M → ratio=0.37x). An earlier
35-month TT aggregate ($254.1M / $149.1M) was used in v13 and produced 0.59x; v14 reverts to the
regression-period values for internal consistency.

Source: Token Terminal daily data, regression measurement period (Token Terminal live, April 2026 pull).

**Uniswap note:** The fee switch has never been permanently activated. Protocol revenue is
near-zero because all trading fees accrue to liquidity providers. The subsidy ratio is
undefined (near-zero denominator) and Uniswap is excluded from subsidy ratio regressions.

**Mechanism:** Subsidized protocols attract mercenary capital seeking token rewards.
This capital concentrates governance power without long-term alignment, driving the
positive correlation between subsidy ratio and HHI.

---

## Cross-Validation: Token Terminal vs DefiLlama

Six of seven protocols pass the <20% threshold between sources.

| Protocol | TT 30d fees | DL 30d fees | Delta | Status |
|----------|-------------|-------------|-------|--------|
| Tether | $459.1M | $491.0M | −6.5% | PASS |
| Circle | $196.1M | $202.7M | −3.3% | PASS |
| Aave | $42.6M | $46.1M | −7.5% | PASS |
| MakerDAO | $42.8M | $46.7M | −8.2% | PASS |
| Uniswap | $37.1M | $40.6M | −8.6% | PASS |
| Curve | $4.6M | $4.0M | +12.6% | WARN |
| Compound | $1.6M | $1.5M | +6.6% | PASS |

TT systematically runs 5–8% below DL for most protocols, reflecting different reporting
windows or data ingestion lag.

**MakerDAO / Sky fragmentation note:** DefiLlama fragments the MakerDAO/Sky ecosystem
across three separate slugs: Sky Lending ($34.3M/30d), Spark ($12.0M/30d), and sDAI
($0.3M/30d). Researchers using DefiLlama for MakerDAO or Sky must sum all three entries
to obtain the correct aggregate ($46.7M/30d). Using only `sky-lending` or `makerdao`
understates revenue by 27–35%.

---

## Subsidy Ratio Computation (Replication)

```python
import pandas as pd

df = pd.read_csv("data/regression_data_april2026.csv")

# Subsidy ratio: incentives / revenue (DEC-023 convention)
# Protocols with revenue ≈ 0 (Uniswap) are excluded
df["subsidy_ratio"] = df["incentives_annual_usd"] / df["revenue_annual_usd"]

# Flag Uniswap (fee switch inactive, revenue ≈ 0)
df.loc[df["token"] == "UNI", "subsidy_ratio"] = float("nan")
```

For DePIN protocols without Token Terminal coverage, `subsidy_ratio` is derived from
on-chain emission and burn data (Dune Analytics). See `CODEBOOK.md` for per-protocol
data source documentation. Subsidy-to-Revenue ratios for DePIN protocols were computed
from protocol-native burn and emission events using the `compute_s2r.py` script in the
replication package; input files include `helium_s2r_cleaned.csv` (34 months),
`geodnet_monthly_burns.csv`, and `geodnet_monthly_emissions.csv`.

## Subsidy field selection convention (2026-05-19 source-mismatch harmonization)

The regression dataset (`regression_data_april2026.csv`) carries two subsidy fields:

- `subsidy_ratio` (sub_TT): Token Terminal-sourced where available; the TT
  methodology aggregates incentives / revenue with TT-defined revenue scope.
- `subsidy_ratio_onchain` (sub_OC): raw on-chain emit_OC / rev_OC computed
  directly from `emissions_onchain_usd` / `revenue_onchain_usd` fields.

The subsidy multivariate analysis (Section 3.4 / 3.7) uses sub_TT first; falls
back to sub_OC for protocols without TT coverage. All 23 protocols in the
subsidy sample have non-null sub_TT and use the TT value. The sub_OC field is
metadata (replicable from raw on-chain fields) and not used by the regression
when TT is available.

**Convention shift, 2026-05-19.** Prior to this date, the sub_OC field for
Aethir and io.net was set to the TT value rather than computed from raw on-chain
fields (a documentation choice consistent with the regression's TT preference
but inconsistent with the field's name). Per the source-mismatch audit
(`source_mismatch_audit_2026-05-19.md`), sub_OC is now computed from
`emissions_onchain_usd / revenue_onchain_usd` for all protocols where both
fields are populated:

| Protocol | sub_OC (prior; TT-inherited) | sub_OC (current; raw OC) |
|---|---:|---:|
| Aethir | 0.355 | 0.150 |
| io.net | 0.400 | 0.560 |
| Hivemapper | 5.46 | 5.467 (negligible) |

Substantive impact on regression: none. The subsidy multivariate uses sub_TT
for these protocols (TT is non-null), and the analysis is unchanged. The field
correction restores semantic consistency between the field name and its values.

**Cross-source divergence (Category A from the audit).** IoTeX has sub_TT =
39.05 and sub_OC = 27.80; both are internally consistent within their respective
pipelines (TT: $3.4M incentives / $88K revenue; OC: $3.8M emissions / $135K
revenue). IoTeX's sub_OC field is preserved as the raw-OC computation (27.80);
the regression uses sub_TT (39.05) per the script convention. IoTeX is
net-inflationary under both pipelines (subsidy ratio greater than one).

**Burn-active subset classification** (Section 3.7) is preserved under both
conventions for all affected protocols. The headline subsidy multivariate Spec
4 result (subsidy beta = 0.000067, p = 0.88; DePIN dummy beta = 0.038, p = 0.004
under N = 22 without Livepeer) is unchanged by this convention restoration.

## DeFi sector batch raw-OC population (2026-05-19 follow-on cycle)

Per `handoff/dispatch/b2_raw_oc_refresh_workstream_2026-05-19.md` (Task #13 from
DEC-167 multi-cycle workstream), the DeFi sector batch (10 protocols) has been
populated this cycle. Provenance class for the batch: TT-equivalent-documented
(see workflow clone `research_content/papers/B2_governance_concentration/supplements/raw_oc/INDEX.md`
for the full provenance class taxonomy).

The DeFi-batch protocols had `subsidy_ratio_onchain` populated pre-cycle with
TT-aggregator values but `revenue_onchain_usd` and `emissions_onchain_usd`
empty. This cycle populates rev_OC and emit_OC with the TT-aggregated values
cross-walked to TT's underlying on-chain methodology (Token Terminal indexes
the same on-chain fee accrual + emissions events; the "TT-sourced" label
reflects TT as the aggregator surface, not a different data layer). Per-protocol
methodology documentation: see workflow clone `supplements/raw_oc/<protocol>_methodology.md`.

| Protocol | rev_OC (this cycle) | emit_OC (this cycle) | sub_OC | Provenance sub-class |
|---|---:|---:|---:|---|
| COMP | 4,883,808 | 5,545,006 | 1.135 | Dune POC verified |
| MKR | 349,334,678 | 0 | 0.000 | trivial-emissions |
| AAVE | 135,365,014 | 50,181,033 | 0.371 | multi-chain-aggregation |
| UNI | 10,628,912 | 36,533,248 | 3.437 | fee-switch-inactive |
| CRV | 30,717,717 | 70,500,548 | 2.295 | gauge-emissions complex |
| MPL_SYRUP | 13,280,708 | 0 | 0.000 | trivial-emissions |
| GMX | 28,797,066 | 175,054 | 0.006 | Arbitrum + Avalanche |
| ETHFI | 49,226,494 | 11,794,199 | 0.240 | (default) |
| LDO | 80,518,093 | 6,131,082 | 0.076 | Dune POC verified |
| HYPE | 780,000,000 | 0 | 0.001 | on-chain-direct (pre-cycle; Assistance Fund) |

**Substantive impact on regression: none.** The subsidy multivariate uses
sub_TT for all 23 protocols by default; sub_OC sensitivity (per
`subsidy_multivariate_oc_sensitivity_2026-05-19.py`) gives Spec 4 subsidy
p = 0.96 (essentially identical to TT-preferred p = 0.88). The DeFi-batch
population brings rev_OC + emit_OC field replicability (so the field name is
no longer hazardous per DEC-167) without changing the regression result.

**Remaining workstream (deferred to follow-on cycles).** The L1/L2/Infra batch
(GRT, OP, POL, POKT, FIL) and DePIN batch (DIMO, HNT/HONEY-on-Solana,
GEOD, RENDER, MOR) are deferred to subsequent per-sector cycles per the
multi-cycle workstream pattern in DEC-167. These 8 protocols (HNT/HONEY already
documented in `hivemapper_holder_data_2026-05-19.md` for the related HONEY
concentration analysis) retain empty rev_OC + emit_OC fields pending follow-on
extraction; their sub_OC values remain populated with pre-cycle TT-equivalent
values pending convention-aware refresh.

**Full Dune extraction (deferred to per-protocol cycles).** The DeFi-batch
methodology MDs document indicative Dune SQL templates per protocol; full
multi-chain / multi-contract aggregation execution is deferred. Per-protocol
follow-on cycles can execute the templates and replace the rev_OC + emit_OC
values with genuine raw-OC extractions; the methodology MDs anchor each
protocol's TT-vs-OC cross-walk for cross-cycle continuity.
