"""
POKT Network rich list via POKTscan API.
Native POKT is not an ERC-20; wPOKT on Ethereum is a small fraction of supply.
"""

import requests
import pandas as pd
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent
HOLDER_DIR = PROJECT_DIR / "holder_lists"

# POKTscan API endpoints - verify these before running
# Docs: https://docs.poktscan.com/ or https://poktscan.com/api
POKTSCAN_BASE = "https://api.poktscan.com"


def fetch_poktscan_richlist():
    """
    Fetch POKT holder distribution from POKTscan.
    Try multiple endpoint patterns since API docs may vary.
    """
    # Attempt 1: /accounts endpoint with sort by balance
    endpoints_to_try = [
        "/accounts?sort=balance&order=desc&limit=1000",
        "/v1/accounts?sort=balance&order=desc&limit=1000",
        "/api/v1/richlist?limit=1000",
        "/richlist?limit=1000&page=0",
    ]

    for endpoint in endpoints_to_try:
        url = POKTSCAN_BASE + endpoint
        print(f"  Trying: {url}")
        try:
            resp = requests.get(url, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                print(f"  Success! Response keys: {list(data.keys()) if isinstance(data, dict) else 'list'}")
                return data
            else:
                print(f"  HTTP {resp.status_code}")
        except Exception as e:
            print(f"  Error: {e}")

    # Attempt 2: GraphQL endpoint (POKTscan v2)
    graphql_url = "https://api.poktscan.com/graphql"
    query = """
    query {
        accounts(
            sort: { field: "balance", order: "desc" }
            limit: 1000
        ) {
            items {
                address
                balance
            }
            totalCount
        }
    }
    """
    print(f"  Trying GraphQL: {graphql_url}")
    try:
        resp = requests.post(graphql_url, json={"query": query}, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            print(f"  GraphQL success!")
            return data
        else:
            print(f"  GraphQL HTTP {resp.status_code}: {resp.text[:200]}")
    except Exception as e:
        print(f"  GraphQL error: {e}")

    return None


def parse_poktscan_response(data) -> pd.DataFrame:
    """Parse POKTscan response into holder DataFrame."""
    holders = []

    if isinstance(data, dict):
        # Try common response structures
        items = (
            data.get("data", {}).get("accounts", {}).get("items", [])
            or data.get("accounts", [])
            or data.get("data", [])
            or data.get("richList", [])
            or data.get("items", [])
        )
    elif isinstance(data, list):
        items = data
    else:
        return pd.DataFrame()

    for item in items:
        addr = item.get("address", item.get("id", ""))
        # POKT balances are in uPOKT (1e-6)
        bal_raw = item.get("balance", item.get("staked_balance", 0))
        balance = float(bal_raw) / 1e6  # Convert uPOKT to POKT
        if balance > 0:
            holders.append({"address": addr, "balance": balance})

    return pd.DataFrame(holders)


def main():
    print("Fetching POKT rich list from POKTscan...")
    data = fetch_poktscan_richlist()

    if data is None:
        print("\nFailed to fetch from POKTscan.")
        print("Manual fallback: Visit https://poktscan.com/explore?tab=accounts")
        print("Export top 1000 accounts and save to holder_lists/holders_POKT.csv")
        return

    df = parse_poktscan_response(data)
    print(f"Parsed {len(df)} holders")

    if len(df) > 0:
        df = df.sort_values('balance', ascending=False).reset_index(drop=True)
        outpath = HOLDER_DIR / "holders_POKT.csv"
        df.head(1000).to_csv(outpath, index=False)
        print(f"Saved top {min(1000, len(df))} holders to {outpath}")
        print(f"Top holder: {df.iloc[0]['balance']:,.0f} POKT")
    else:
        print("No holders parsed. Check API response format.")
        print("Manual fallback: Visit https://poktscan.com/explore?tab=accounts")


if __name__ == "__main__":
    main()
