"""
Filecoin rich list via Filfox API.
FIL has no meaningful ERC-20 representation; use native Filecoin data.
"""

import requests
import pandas as pd
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent
HOLDER_DIR = PROJECT_DIR / "holder_lists"


def fetch_filfox_richlist(pages=10, page_size=100):
    """
    Filfox rich list API.
    Returns top holders (up to pages * page_size).
    """
    all_holders = []
    for page in range(pages):
        url = "https://filfox.info/api/v1/address/rich-list"
        params = {"pageSize": page_size, "page": page}
        resp = requests.get(url, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        # API returns either 'richList' or 'data' key
        holders_raw = data.get("richList", data.get("data", data.get("totalCount", [])))
        if isinstance(holders_raw, int):
            # Might be nested differently
            holders_raw = data.get("richList", [])

        if not holders_raw:
            print(f"  Page {page}: no data returned")
            break

        for h in holders_raw:
            addr = h.get("address", h.get("id", ""))
            bal_raw = h.get("balance", h.get("totalBalance", "0"))
            # Balance is in attoFIL (1e-18)
            balance = float(bal_raw) / 1e18
            all_holders.append({"address": addr, "balance": balance})

        print(f"  Page {page}: {len(holders_raw)} holders fetched")

        if len(holders_raw) < page_size:
            break

    df = pd.DataFrame(all_holders)
    df = df[df['balance'] > 0].sort_values('balance', ascending=False).reset_index(drop=True)
    return df


def main():
    print("Fetching Filecoin rich list from Filfox...")
    df = fetch_filfox_richlist(pages=10, page_size=100)
    print(f"Total holders fetched: {len(df)}")

    if len(df) > 0:
        outpath = HOLDER_DIR / "holders_FIL.csv"
        df.head(1000).to_csv(outpath, index=False)
        print(f"Saved top {min(1000, len(df))} holders to {outpath}")
        print(f"Top holder balance: {df.iloc[0]['balance']:,.0f} FIL")
        print(f"Top 10 total: {df.head(10)['balance'].sum():,.0f} FIL")


if __name__ == "__main__":
    main()
