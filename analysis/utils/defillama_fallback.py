"""
DefiLlama fallback for protocols missing from Token Terminal.
Uses the defillama MCP-accessible API (same endpoints as the MCP tool).

Fallback priority:
1. DefiLlama fees/revenue endpoint → protocol revenue
2. DefiLlama TVL/protocol endpoint → FDV proxy (market cap from coins)
3. For DePIN without fees: Dune burn/fee queries (document as proxy)

Protocols likely needing fallback:
- ANYONE, GRASS, GEOD (unlikely in TT or DefiLlama)
- TEC (wound down; zero revenue)
- Non-revenue protocols: ENS, GTC (fees but minimal protocol revenue)
"""

import requests
import pandas as pd
import json
from pathlib import Path
from datetime import date, timedelta

PROJECT_DIR = Path(__file__).parent.parent
SNAPSHOT = date(2026, 4, 1)
WINDOW_START = SNAPSHOT - timedelta(days=30)
DEFILLAMA_BASE = "https://api.llama.fi"
DEFILLAMA_FEES = "https://fees.llama.fi"
DEFILLAMA_COINS = "https://coins.llama.fi"

# DefiLlama protocol slug mapping
DEFILLAMA_MAP = {
    "COMP":    "compound-finance",
    "MKR":     "makerdao",
    "AAVE":    "aave",
    "UNI":     "uniswap",
    "CRV":     "curve-dex",
    "RPL":     "rocket-pool",
    "JUP":     "jupiter",
    "MPL_SYRUP": "maple-finance",
    "GMX":     "gmx",
    "DRIFT":   "drift-protocol",
    "ETHFI":   "ether.fi",
    "GRT":     "the-graph",
    "OP":      "optimism",
    "POL":     "polygon",
    "ARB":     "arbitrum",
    "ENS":     "ens",
    "DIMO":    "dimo",
    "IOTX":    "iotex",
    "WXM":     "weatherxm",
    "ANYONE":  None,
    "GRASS":   None,
    "LPT":     "livepeer",
    "HNT":     "helium",
    "GEOD":    None,
    "FIL":     "filecoin",
    "RENDER":  "render",
    "POKT":    "pocket-network",
    "GTC":     "gitcoin",
    "TEC":     None,
}

# CoinGecko IDs for FDV lookup via DefiLlama coins endpoint
COINGECKO_IDS = {
    "COMP":    "compound-governance-token",
    "MKR":     "maker",
    "AAVE":    "aave",
    "UNI":     "uniswap",
    "CRV":     "curve-dao-token",
    "RPL":     "rocket-pool",
    "JUP":     "jupiter-exchange-solana",
    "MPL_SYRUP": "maple",
    "GMX":     "gmx",
    "DRIFT":   "drift-protocol",
    "ETHFI":   "ether-fi",
    "GRT":     "the-graph",
    "OP":      "optimism",
    "POL":     "matic-network",
    "ARB":     "arbitrum",
    "ENS":     "ethereum-name-service",
    "DIMO":    "dimo",
    "IOTX":    "iotex",
    "WXM":     "weatherxm",
    "ANYONE":  "anyone-protocol",
    "GRASS":   "grass",
    "LPT":     "livepeer-token",
    "HNT":     "helium",
    "GEOD":    "geodnet",
    "FIL":     "filecoin",
    "RENDER":  "render-token",
    "POKT":    "pocket-network",
    "GTC":     "gitcoin",
    "TEC":     "token-engineering-commons",
}


def fetch_defillama_protocol_fees(slug: str) -> dict:
    """Get 30d protocol revenue from DefiLlama fees."""
    try:
        url = f"{DEFILLAMA_FEES}/summary/fees/{slug}"
        resp = requests.get(url, timeout=20)
        if resp.status_code == 404:
            return {}
        resp.raise_for_status()
        data = resp.json()

        # data['totalDataChartBreakdown'] or data['total30d'] / data['revenue30d']
        rev_30d = data.get("revenue30d") or data.get("total30d")
        fees_30d = data.get("total30d")

        # Prefer protocol revenue over gross fees
        return {
            "revenue_30d": rev_30d,
            "fees_30d": fees_30d,
        }
    except Exception as e:
        print(f"    DefiLlama fees error for {slug}: {e}")
        return {}


def fetch_coingecko_fdv(token_symbol: str) -> float | None:
    """Get FDV via DefiLlama coins API (uses CoinGecko data)."""
    cg_id = COINGECKO_IDS.get(token_symbol)
    if not cg_id:
        return None
    try:
        url = f"{DEFILLAMA_COINS}/prices/current/coingecko:{cg_id}"
        resp = requests.get(url, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        coin_data = data.get("coins", {}).get(f"coingecko:{cg_id}", {})
        # DefiLlama coins doesn't give FDV directly - use market cap as proxy
        # Will need CoinGecko API for proper FDV
        price = coin_data.get("price")
        return price  # price only; FDV = price * total_supply (get from CoinGecko)
    except Exception as e:
        print(f"    DefiLlama coins error for {token_symbol}: {e}")
        return None


def fetch_coingecko_fdv_direct(cg_id: str, api_key: str = None) -> float | None:
    """Fetch FDV directly from CoinGecko."""
    headers = {"x-cg-demo-api-key": api_key} if api_key else {}
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{cg_id}"
        params = {"localization": "false", "tickers": "false", "community_data": "false"}
        resp = requests.get(url, headers=headers, params=params, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        fdv = data.get("market_data", {}).get("fully_diluted_valuation", {}).get("usd")
        return float(fdv) if fdv else None
    except Exception as e:
        print(f"    CoinGecko error for {cg_id}: {e}")
        return None


def main(symbols_to_fill: list = None):
    """
    Fill missing values from Token Terminal using DefiLlama.
    If symbols_to_fill is None, load from fallback_needed.json.
    """
    if symbols_to_fill is None:
        fallback_path = PROJECT_DIR / "fallback_needed.json"
        if fallback_path.exists():
            with open(fallback_path) as f:
                symbols_to_fill = json.load(f)
        else:
            symbols_to_fill = list(DEFILLAMA_MAP.keys())

    print(f"=== DefiLlama Fallback ({len(symbols_to_fill)} protocols) ===")

    rows = []
    for sym in symbols_to_fill:
        slug = DEFILLAMA_MAP.get(sym)
        print(f"\n  {sym} (slug: {slug or 'N/A'})...")

        rev_annual = None
        fdv = None
        source_notes = []

        if sym == "TEC":
            print("    Wound down protocol → zero revenue")
            rows.append({
                "token": sym,
                "revenue_annual_usd": 0,
                "fdv_usd": None,
                "incentives_annual_usd": 0,
                "subsidy_ratio": None,
                "active_addresses_30d": None,
                "treasury_usd": None,
                "source": "manual",
                "notes": "Protocol wound down; zero revenue by design",
            })
            continue

        if slug:
            fees_data = fetch_defillama_protocol_fees(slug)
            rev_30d = fees_data.get("revenue_30d")
            if rev_30d:
                rev_annual = float(rev_30d) * (365 / 30)
                source_notes.append("DefiLlama-fees")
                print(f"    revenue: ${rev_annual:,.0f}/yr")
            else:
                print(f"    revenue: N/A from DefiLlama")
        else:
            print(f"    No DefiLlama slug → manual/zero")
            source_notes.append("no_source")

        # FDV via CoinGecko
        cg_id = COINGECKO_IDS.get(sym)
        if cg_id:
            fdv = fetch_coingecko_fdv_direct(cg_id)
            if fdv:
                source_notes.append("CoinGecko-FDV")
                print(f"    FDV: ${fdv:,.0f}")
            else:
                print(f"    FDV: N/A")

        source = "+".join(source_notes) if source_notes else "manual"
        rows.append({
            "token": sym,
            "revenue_annual_usd": round(rev_annual, 0) if rev_annual else None,
            "fdv_usd": round(fdv, 0) if fdv else None,
            "incentives_annual_usd": None,  # DePIN token incentives harder to get from DefiLlama
            "subsidy_ratio": None,
            "active_addresses_30d": None,
            "treasury_usd": None,
            "source": source,
            "notes": "DefiLlama fallback" if slug else "No automated source; manual entry required",
        })

    df = pd.DataFrame(rows)
    out = PROJECT_DIR / "covariates_defillama.csv"
    df.to_csv(out, index=False)
    print(f"\nSaved {len(df)} rows → {out}")
    return df


if __name__ == "__main__":
    main()
