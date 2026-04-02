"""
refresh_market_data.py
Live CoinGecko data refresh for covariates_merged.csv and coingecko_market.csv
Source: CoinGecko MCP API calls, 2026-03-31
"""
import pandas as pd
import numpy as np

# ── Live data from CoinGecko API (2026-03-31) ────────────────────────────────
# Format: coingecko_id -> {price, market_cap, total_supply, circ_supply}
CG_LIVE = {
    "compound-governance-token": {
        "price": 17.62, "market_cap": 170272531, "circ_supply": 9668189.28, "total_supply": 10000000.0,
    },
    # MKR: CG data broken (circ=0) post-Sky migration — keep fdv from prior session, skip market_cap update
    "maker": None,
    "aave": {
        "price": 97.67, "market_cap": 1481437372, "circ_supply": 15185755.57, "total_supply": 16000000.0,
    },
    "uniswap": {
        "price": 3.51, "market_cap": 2223202852, "circ_supply": 633561603.60, "total_supply": 897544420.04,
    },
    "curve-dao-token": {
        "price": 0.217579, "market_cap": 324541384, "circ_supply": 1493385051.0, "total_supply": 2366447157.53,
    },
    "rocket-pool": {
        "price": 1.69, "market_cap": 37570638, "circ_supply": 22283476.40, "total_supply": 22283476.40,
    },
    "jupiter-exchange-solana": {
        "price": 0.153681, "market_cap": 545012815, "circ_supply": 3550835739.32, "total_supply": 6863982434.69,
    },
    "maple": {
        "price": 0.183691, "market_cap": 321109, "circ_supply": 1748089.34, "total_supply": 10000000.0,
    },
    "gmx": {
        "price": 6.27, "market_cap": 65038289, "circ_supply": 10381264.51, "total_supply": 10381264.51,
    },
    "drift-protocol": {
        "price": 0.063874, "market_cap": 37048496, "circ_supply": 581163076.43, "total_supply": 1000000000.0,
    },
    "ether-fi": {
        "price": 0.468971, "market_cap": 369164093, "circ_supply": 787264625.0, "total_supply": 998535999.0,
    },
    # MetaDAO: not found on CoinGecko
    "meta-dao": None,
    "lido-dao": {
        "price": 0.326931, "market_cap": 277578113, "circ_supply": 849264458.59, "total_supply": 1000000000.0,
    },
    "dimo": {
        "price": 0.01543238, "market_cap": 7663204, "circ_supply": 496528414.90, "total_supply": 1000000000.0,
    },
    "iotex": {
        "price": 0.00462874, "market_cap": 43700433, "circ_supply": 9441368661.0, "total_supply": 9441368667.0,
    },
    # WXM: new ID is weatherxm-network (was "weatherxm" which 404'd)
    "weatherxm-network": {
        "price": 0.01594566, "market_cap": 497517, "circ_supply": 31201225.0, "total_supply": 100000000.0,
    },
    # Anyone Protocol: not found on CoinGecko
    "anyone-protocol": None,
    "grass": {
        "price": 0.285511, "market_cap": 161220686, "circ_supply": 564673734.0, "total_supply": 1000000000.0,
    },
    "livepeer": {
        "price": 2.06, "market_cap": 102463381, "circ_supply": 49688954.55, "total_supply": 49688954.55,
    },
    "helium": {
        "price": 1.069, "market_cap": 197286767, "circ_supply": 184571549.07, "total_supply": 184571549.07,
    },
    "geodnet": {
        "price": 0.141392, "market_cap": 60244202, "circ_supply": 426078902.62, "total_supply": 968091567.62,
    },
    "filecoin": {
        "price": 0.82827, "market_cap": 633356445, "circ_supply": 764908287.0, "total_supply": 1957925127.0,
    },
    "render-token": {
        "price": 1.7, "market_cap": 883569990, "circ_supply": 518743261.01, "total_supply": 533503434.29,
    },
    "pocket-network": {
        "price": 0.01237974, "market_cap": 24904074, "circ_supply": 2011680128.05, "total_supply": 2351355446.25,
    },
    # Morpheus AI MOR: not found on CoinGecko (wrong match returned)
    "morpheus-ai": None,
    "the-graph": {
        "price": 0.0237858, "market_cap": 256162157, "circ_supply": 10770371545.86, "total_supply": 10800262816.05,
    },
    "optimism": {
        "price": 0.108045, "market_cap": 228794474, "circ_supply": 2117847344.0, "total_supply": 4294967296.0,
    },
    "polygon-ecosystem-token": {
        "price": 0.091469, "market_cap": 970844394, "circ_supply": 10617468716.20, "total_supply": 10617468716.20,
    },
    "arbitrum": {
        "price": 0.092603, "market_cap": 559249324, "circ_supply": 6040824145.0, "total_supply": 10000000000.0,
    },
    "ethereum-name-service": {
        "price": 5.6, "market_cap": 214780224, "circ_supply": 38380013.53, "total_supply": 100000000.0,
    },
    "layerzero": {
        "price": 1.87, "market_cap": 472000111, "circ_supply": 252331652.65, "total_supply": 1000000000.0,
    },
    "wormhole": {
        "price": 0.01456389, "market_cap": 81449390, "circ_supply": 5609687898.0, "total_supply": 10000000000.0,
    },
    "axelar": {
        "price": 0.04671781, "market_cap": 53362843, "circ_supply": 1144413675.15, "total_supply": 1235693447.99,
    },
    "gitcoin": {
        "price": 0.075937, "market_cap": 6643467, "circ_supply": 87491501.90, "total_supply": 100000000.0,
    },
    # Token Engineering Commons: not found on CoinGecko
    "token-engineering-commons": None,
}

# Map protocol → coingecko_id (correct current IDs)
PROTOCOL_TO_CGID = {
    "Compound": "compound-governance-token",
    "MakerDAO": "maker",
    "Aave": "aave",
    "Uniswap": "uniswap",
    "Curve": "curve-dao-token",
    "Rocket Pool": "rocket-pool",
    "Jupiter": "jupiter-exchange-solana",
    "Maple Finance": "maple",
    "GMX": "gmx",
    "Drift": "drift-protocol",
    "Ether.Fi": "ether-fi",
    "MetaDAO": "meta-dao",
    "Lido": "lido-dao",
    "DIMO": "dimo",
    "IoTeX": "iotex",
    "WeatherXM": "weatherxm-network",   # CORRECTED from "weatherxm"
    "Anyone Protocol": "anyone-protocol",
    "Grass": "grass",
    "Livepeer": "livepeer",
    "Helium": "helium",
    "GEODNET": "geodnet",
    "Filecoin": "filecoin",
    "Render": "render-token",
    "Pokt Network": "pocket-network",
    "Morpheus AI": "morpheus-ai",
    "The Graph": "the-graph",
    "Optimism": "optimism",
    "Polygon": "polygon-ecosystem-token",
    "Arbitrum": "arbitrum",
    "ENS": "ethereum-name-service",
    "LayerZero": "layerzero",
    "Wormhole": "wormhole",
    "Axelar": "axelar",
    "Gitcoin": "gitcoin",
    "Token Engineering Commons": "token-engineering-commons",
}

DATA_DIR = "/Users/zach/b2-governance-data/data"

# ── 1. Update coingecko_market.csv ─────────────────────────────────────────
cg = pd.read_csv(f"{DATA_DIR}/coingecko_market.csv")

for idx, row in cg.iterrows():
    protocol = row["protocol"]
    cgid = PROTOCOL_TO_CGID.get(protocol)
    if cgid is None:
        continue
    data = CG_LIVE.get(cgid)

    # Always update the stored coingecko_id (corrects WXM and others)
    cg.at[idx, "coingecko_id"] = cgid

    if data is None:
        # Known broken / not found — leave existing values
        continue

    fdv = data["price"] * data["total_supply"]

    cg.at[idx, "price_usd"] = data["price"]
    cg.at[idx, "market_cap_usd"] = data["market_cap"]
    cg.at[idx, "fdv_usd"] = fdv
    cg.at[idx, "circulating_supply"] = data["circ_supply"]
    cg.at[idx, "total_supply"] = data["total_supply"]
    if data["total_supply"] > 0:
        cg.at[idx, "circ_to_total_ratio"] = data["circ_supply"] / data["total_supply"]

cg.to_csv(f"{DATA_DIR}/coingecko_market.csv", index=False)
print("✓ coingecko_market.csv updated")

# ── 2. Update covariates_merged.csv ────────────────────────────────────────
df = pd.read_csv(f"{DATA_DIR}/covariates_merged.csv")

for idx, row in df.iterrows():
    protocol = row["protocol"]
    cgid = PROTOCOL_TO_CGID.get(protocol)
    if cgid is None:
        continue
    data = CG_LIVE.get(cgid)
    if data is None:
        continue

    fdv = data["price"] * data["total_supply"]

    df.at[idx, "market_cap_usd"] = data["market_cap"]
    df.at[idx, "fdv_usd"] = fdv
    df.at[idx, "price_usd"] = data["price"]
    df.at[idx, "circulating_supply"] = data["circ_supply"]
    df.at[idx, "total_supply"] = data["total_supply"]
    df.at[idx, "circ_to_total_ratio"] = (
        data["circ_supply"] / data["total_supply"] if data["total_supply"] > 0 else np.nan
    )

# Recompute log_fdv
df["log_fdv"] = df["fdv_usd"].apply(lambda x: np.log(x) if (pd.notna(x) and x > 0) else np.nan)

# Recompute regression_ready: need hhi + fdv + treasury + gini + n_holders + insider_pct
def check_ready(row):
    required = ["hhi", "fdv_usd", "treasury_usd", "gini", "n_holders", "insider_pct"]
    return all(pd.notna(row.get(c)) and row.get(c, 0) > 0 for c in required)

df["regression_ready"] = df.apply(check_ready, axis=1)

df.to_csv(f"{DATA_DIR}/covariates_merged.csv", index=False)
print("✓ covariates_merged.csv updated")

# ── 3. Summary report ──────────────────────────────────────────────────────
print(f"\n=== MARKET DATA COVERAGE (post-refresh) ===")
print(f"market_cap_usd populated: {df['market_cap_usd'].notna().sum()} / {len(df)}")
print(f"fdv_usd populated:        {df['fdv_usd'].notna().sum()} / {len(df)}")
print(f"regression_ready:         {df['regression_ready'].sum()} / {len(df)}")

print(f"\n=== NOTABLE CHANGES ===")
wxm = df[df["token"] == "WXM"].iloc[0]
print(f"WXM market_cap: ${wxm['market_cap_usd']:,.0f}  FDV: ${wxm['fdv_usd']:,.0f}  (was NaN)")
mkr = df[df["token"] == "MKR"].iloc[0]
print(f"MKR market_cap: ${mkr['market_cap_usd']:,.0f}  FDV: ${mkr['fdv_usd']:,.0f}  (CG broken, kept prior)")

print(f"\n=== PROTOCOLS WITH MISSING MARKET DATA ===")
missing = df[df["market_cap_usd"].isna() | (df["market_cap_usd"] == 0)]
for _, r in missing.iterrows():
    print(f"  {r['protocol']:30s} {r['token']:8s}  market_cap={r['market_cap_usd']}")

print(f"\n=== KEY CORRELATIONS (updated) ===")
from scipy import stats
sub = df[df["regression_ready"] == True].copy()
sub["log_holders"] = sub["n_holders"].apply(lambda x: np.log(x) if pd.notna(x) and x > 0 else np.nan)
pairs = [("gini","hhi"), ("n_holders","hhi"), ("insider_pct","hhi"),
         ("log_fdv","hhi"), ("log_revenue","hhi"), ("log_treasury","hhi")]
for x_col, y_col in pairs:
    if x_col in sub.columns:
        xy = sub[[x_col, y_col]].dropna()
        if len(xy) > 5:
            r, p = stats.pearsonr(xy[x_col], xy[y_col])
            sig = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else "ns"
            print(f"  {x_col:20s} vs hhi: r={r:+.3f} p={p:.3f} {sig}  N={len(xy)}")
