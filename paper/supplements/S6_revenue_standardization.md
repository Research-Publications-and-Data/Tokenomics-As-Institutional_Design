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

Subsidy ratio is the strongest concentration predictor in the regression (r = 0.37). These
DeFi values establish the baseline against which DePIN protocols are compared.

| Protocol | Revenue (35mo) | Token Incentives (35mo) | Subsidy Ratio | Holding HHI |
|----------|---------------|------------------------|---------------|-------------|
| MakerDAO | $790.4M | $0.0M | **0.00x** | 0.045 |
| Aave | $254.1M | $149.1M | **0.59x** | 0.020 |
| Compound | $23.0M | $36.5M | **1.59x** | 0.027 |
| Curve | $92.7M | $277.7M | **3.00x** | 0.171 |
| Uniswap | ~$3.0M | $36.5M | **N/A** | 0.032 |

**Formula change (v12):** Prior versions used `incentives / (revenue + incentives)`,
producing percentages that cap at 100%. The paper body uses `incentives / revenue`
(DEC-023 convention), which allows values > 1.0x for subsidy-dominant protocols
(e.g., Livepeer 88.5x). The table above now uses the body convention. Note: the
paper body references Aave at "0.37x," which corresponds to the old formula (37.0%);
under the current formula Aave is 0.59x. This discrepancy should be reconciled in the
body text during the next revision pass.

Source: Token Terminal daily data, February 2023 to January 2026 (1,096 observations per metric).

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
data source documentation.
