"""
Quick collection script for FIL (Filfox) and POKT (POKTscan).
Fixes endpoint URLs discovered during testing.
"""

import requests
import pandas as pd
import json
from pathlib import Path
import time

PROJECT_DIR = Path(__file__).parent.parent
HOLDER_DIR = PROJECT_DIR / "holder_lists"
HOLDER_DIR.mkdir(exist_ok=True)


# ─── Filecoin (Filfox) ───────────────────────────────────────────────────────

def fetch_fil():
    print("=== Filecoin (Filfox) ===")
    all_holders = []
    for page in range(10):
        url = "https://filfox.info/api/v1/rich-list"
        resp = requests.get(url, params={"pageSize": 100, "page": page}, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        items = data.get("richList", [])
        if not items:
            break
        for h in items:
            bal_raw = h.get("balance", "0")
            balance = float(bal_raw) / 1e18  # attoFIL → FIL
            all_holders.append({"address": h.get("address", ""), "balance": balance})
        print(f"  Page {page}: {len(items)} holders")
        if len(items) < 100:
            break
        time.sleep(0.2)

    df = pd.DataFrame(all_holders)
    df = df[df["balance"] > 0].sort_values("balance", ascending=False).reset_index(drop=True)
    df["rank"] = range(1, len(df) + 1)
    total = df["balance"].sum()
    df["share"] = df["balance"] / total
    df.insert(0, "token", "FIL")
    out = HOLDER_DIR / "holders_FIL.csv"
    df.head(1000).to_csv(out, index=False)
    print(f"Saved {min(1000, len(df))} rows → {out.name}")
    print(f"Top holder: {df.iloc[0]['balance']:,.0f} FIL ({df.iloc[0]['share']:.3f})")
    return df


# ─── POKT Network (POKTscan GraphQL) ─────────────────────────────────────────

def fetch_pokt():
    print("\n=== POKT Network (POKTscan) ===")
    url = "https://api.poktscan.com/graphql"

    # Probe schema first
    introspect = '{ __schema { queryType { fields { name args { name } } } } }'
    resp = requests.post(url, json={"query": introspect}, timeout=30)
    if resp.status_code == 200:
        schema = resp.json()
        fields = schema.get("data", {}).get("__schema", {}).get("queryType", {}).get("fields", [])
        print("  Query fields:", [f["name"] for f in fields[:20]])

    # Try known POKTscan query patterns
    queries = [
        # Pattern 1: accounts with pagination/ordering
        """{ accounts(page: { pageSize: 1000, pageNumber: 1 }, sort: { property: "balance", direction: -1 }) { pageInfo { totalCount } results { address stakedTokens } } }""",
        # Pattern 2: richlist query
        """{ getTopAccounts(page: 1, pageSize: 1000) { totalCount accounts { address balance } } }""",
        # Pattern 3: simple accounts
        """{ accounts(first: 1000) { address balance } }""",
        # Pattern 4: poktAddresses
        """{ poktAddresses(orderBy: balance, orderDirection: desc, first: 1000) { id balance } }""",
    ]

    for q in queries:
        try:
            r = requests.post(url, json={"query": q}, timeout=30)
            data = r.json()
            if "errors" in data:
                print(f"  Query failed: {data['errors'][0]['message'][:80]}")
                continue
            print(f"  Query succeeded! Keys: {list(data.get('data', {}).keys())}")
            return data
        except Exception as e:
            print(f"  Error: {e}")
            continue

    # Last resort: try poktscan REST endpoint
    print("  Trying REST endpoints...")
    rest_endpoints = [
        "https://api.poktscan.com/v1/accounts?page=1&per_page=1000&sort=balance&order=desc",
        "https://poktscan.com/api/accounts?limit=1000",
        "https://api.poktscan.com/accounts/richlist",
    ]
    for endpoint in rest_endpoints:
        try:
            r = requests.get(endpoint, timeout=30)
            if r.status_code == 200:
                print(f"  REST success at {endpoint}")
                return r.json()
            else:
                print(f"  {r.status_code}: {endpoint}")
        except Exception as e:
            print(f"  Error at {endpoint}: {e}")

    return None


def parse_pokt(data) -> pd.DataFrame:
    if not data:
        return pd.DataFrame()
    holders = []
    # Try multiple schemas
    d = data.get("data", data) if isinstance(data, dict) else {}
    candidates = [
        d.get("accounts", {}).get("results", []),
        d.get("accounts", []),
        d.get("getTopAccounts", {}).get("accounts", []),
        d.get("poktAddresses", []),
        data if isinstance(data, list) else [],
    ]
    items = next((c for c in candidates if c), [])
    for item in items:
        addr = item.get("address", item.get("id", ""))
        bal = (item.get("balance") or item.get("stakedTokens") or item.get("amount") or 0)
        try:
            # POKT balances may be in uPOKT (1e-6) or POKT depending on endpoint
            bal_float = float(bal)
            if bal_float > 1e9:  # likely uPOKT
                bal_float /= 1e6
            if bal_float > 0:
                holders.append({"address": addr, "balance": bal_float})
        except (ValueError, TypeError):
            pass
    return pd.DataFrame(holders)


def main():
    # FIL
    try:
        fetch_fil()
    except Exception as e:
        print(f"FIL failed: {e}")

    # POKT
    data = fetch_pokt()
    df = parse_pokt(data)
    if len(df) > 0:
        df = df.sort_values("balance", ascending=False).reset_index(drop=True)
        df["rank"] = range(1, len(df) + 1)
        df["share"] = df["balance"] / df["balance"].sum()
        df.insert(0, "token", "POKT")
        out = HOLDER_DIR / "holders_POKT.csv"
        df.head(1000).to_csv(out, index=False)
        print(f"\nSaved {min(1000, len(df))} POKT rows → {out.name}")
        print(f"Top holder: {df.iloc[0]['balance']:,.0f} POKT ({df.iloc[0]['share']:.3f})")
    else:
        print("\nPOKT: No data. Manual download required.")
        print("Visit: https://poktscan.com/explore?tab=accounts")


if __name__ == "__main__":
    main()
