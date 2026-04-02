"""
Fetch holder list results from Dune Analytics and save to holder_lists/.
Uses hardcoded execution IDs from the April 2026 data collection session.

Execution IDs:
- Solana queries use the final corrected run (GROUP BY, no decimal division)
- ARB uses the corrected run (erc20_arbitrum.evt_transfer)
- All others use the original EVM runs
"""

import requests
import pandas as pd
import json
from pathlib import Path
import time

PROJECT_DIR = Path(__file__).parent.parent
HOLDER_DIR = PROJECT_DIR / "holder_lists"
HOLDER_DIR.mkdir(exist_ok=True)

import os
DUNE_API_KEY = os.environ.get("DUNE_API_KEY", "")
DUNE_BASE = "https://api.dune.com/api/v1"
HEADERS = {"X-DUNE-API-KEY": DUNE_API_KEY}

# Symbol → (query_id, execution_id) — use latest correct execution
EXECUTION_MAP = {
    # Solana (final GROUP BY runs, snapshot 2026-03-30, token_balance already decimal-adjusted)
    "JUP":        (6928143, "01KN0C5H4JW4K7QR3BCJ0985GR"),
    "DRIFT":      (6928144, "01KN0C5J3D1BYX3CJHMRPW8DB5"),
    "GRASS":      (6928146, "01KN0C5KMJR31A6FFJ6WND84PW"),
    "HNT":        (6928148, "01KN0C5MRFNQZXFX0PNWRSD066"),
    "RENDER_SOL": (6928149, "01KN0C5NF08HB8E08GYKPJN3JJ"),
    # EVM Ethereum (snapshot 2026-04-01)
    "COMP":       (6928154, "01KN0B71V7MD5EC1Q69SHHSPYA"),
    "MKR":        (6928258, "01KN0B75QSKQM07QNCXVTYQW71"),
    "AAVE":       (6928260, "01KN0B76HJ8BKXNNYS9QV8PPR5"),
    "UNI":        (6928261, "01KN0B7795P0HP6TNPF1SNTKT3"),
    "CRV":        (6928263, "01KN0B7818EQ02EQ4NS0T75DMS"),
    "RPL":        (6928264, "01KN0B78WC947S80FTVGG6AC4M"),
    "MPL":        (6928266, "01KN0B79P87BBGGQ2PH7D8D20W"),
    "SYRUP":      (6928267, "01KN0B7AD4CFA99NZX75BYVGNW"),
    "ETHFI":      (6928268, "01KN0B7B53EAF75B1822MH9EYP"),
    "GRT":        (6928269, "01KN0B7BXYT50XZT7WZJW4DWR4"),
    "POL":        (6928270, "01KN0B7CNXWS1G4MM4PM5GK7QV"),
    "ENS":        (6928273, "01KN0B7EAXVWFWX6MCCJ9R0XJE"),
    "IOTX":       (6928276, "01KN0B7F257RN7AY77Q32G71G9"),
    "ANYONE":     (6928277, "01KN0B7FSF51MTVRC96VM3DTTC"),
    "GTC":        (6928287, "01KN0B7GG041DM9WHB0D7Z4GPV"),
    "RNDR_ETH":   (6928288, "01KN0B7H77SGPC8RMS1K1B4BCC"),
    # EVM Arbitrum
    "ARB":        (6928272, "01KN0BSV0HQHSNTYF3H0WWN91H"),  # fixed run
    "GMX":        (6928289, "01KN0B7HYQD91HDFKR7WKMGM6P"),
    "WXM":        (6928290, "01KN0B7JPQECJCXEW79J0HK6NK"),
    "LPT":        (6928291, "01KN0B7KF5BG3CWHA0MCS0539B"),
    # EVM Polygon
    "DIMO":       (6928293, "01KN0B7M8KMAWZFE4ETDJQZVMV"),
    "GEOD":       (6928294, "01KN0B7N8XS9G04RCVVPQS5EJM"),
    # EVM Optimism
    "OP":         (6928295, "01KN0B7P0FS9J7NDW520805RXB"),
    # EVM Gnosis
    "TEC":        (6928296, "01KN0B7PPHW3B624T99K95XXS3"),
}


def fetch_execution_results(execution_id: str, limit: int = 1000) -> list[dict]:
    """Fetch all rows from a completed Dune execution."""
    url = f"{DUNE_BASE}/execution/{execution_id}/results"
    all_rows = []
    offset = 0

    while True:
        resp = requests.get(url, headers=HEADERS, params={"limit": limit, "offset": offset}, timeout=60)
        resp.raise_for_status()
        data = resp.json()

        state = data.get("state", "")
        if state not in ("QUERY_STATE_COMPLETED", ""):
            print(f"    WARNING: state={state}")
            break

        result = data.get("result", {})
        rows = result.get("rows", [])
        all_rows.extend(rows)

        # Check if there are more pages
        total_row_count = result.get("metadata", {}).get("total_row_count", len(rows))
        if offset + limit >= total_row_count or len(rows) < limit:
            break
        offset += limit
        time.sleep(0.2)  # avoid rate limit

    return all_rows


def main():
    print("=== Fetching Dune Holder Lists ===")

    results_summary = []

    for sym, (query_id, exec_id) in EXECUTION_MAP.items():
        print(f"\n  {sym} (exec: {exec_id[:12]}...)...")

        out_path = HOLDER_DIR / f"holders_{sym}.csv"
        if out_path.exists():
            df_existing = pd.read_csv(out_path)
            print(f"    Already exists ({len(df_existing)} rows), skipping.")
            results_summary.append({"symbol": sym, "n_rows": len(df_existing), "status": "cached"})
            continue

        try:
            rows = fetch_execution_results(exec_id)
            if not rows:
                print(f"    ERROR: No rows returned!")
                results_summary.append({"symbol": sym, "n_rows": 0, "status": "error"})
                continue

            df = pd.DataFrame(rows)
            df.to_csv(out_path, index=False)
            print(f"    Saved {len(df)} rows → {out_path.name}")
            results_summary.append({"symbol": sym, "n_rows": len(df), "status": "ok",
                                     "top1_pct": float(df["share"].iloc[0]) if "share" in df.columns else None})
        except Exception as e:
            print(f"    ERROR: {e}")
            results_summary.append({"symbol": sym, "n_rows": 0, "status": f"error: {e}"})

        time.sleep(0.3)

    print("\n=== Summary ===")
    for r in results_summary:
        top1 = f"  top1={r['top1_pct']:.3f}" if r.get("top1_pct") else ""
        print(f"  {r['symbol']:12s} {r['status']:8s} n={r['n_rows']}{top1}")

    # Update query_log.json
    log = [{"symbol": sym, "query_id": qid, "execution_id": eid, "status": "completed"}
           for sym, (qid, eid) in EXECUTION_MAP.items()]
    with open(PROJECT_DIR / "query_log.json", "w") as f:
        json.dump(log, f, indent=2)
    print(f"\nUpdated query_log.json")


if __name__ == "__main__":
    main()
