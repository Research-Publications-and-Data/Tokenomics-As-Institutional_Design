"""
Token Terminal Financial Covariates Collection
Snapshot date: 2026-04-01

Collects per-protocol:
  - revenue_annual_usd       (trailing 30d annualized; protocol revenue only)
  - fdv_usd                  (fully diluted valuation)
  - incentives_annual_usd    (trailing 30d token emissions, annualized)
  - subsidy_ratio            (incentives / (revenue + incentives))
  - active_addresses_30d     (secondary)
  - treasury_usd             (secondary)

Fallback to DefiLlama for missing protocols (called from defillama_fallback.py).
"""

import requests
import json
import pandas as pd
from pathlib import Path
from datetime import date, timedelta

PROJECT_DIR = Path(__file__).parent.parent
import os
API_KEY = os.environ.get("TOKEN_TERMINAL_API_KEY", "")
BASE_URL = "https://api.tokenterminal.com/v2"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}
SNAPSHOT = date(2026, 4, 1)
WINDOW_START = SNAPSHOT - timedelta(days=30)  # trailing 30d

# Token Terminal project slug mapping (best-known slugs; verified by /projects lookup)
PROJECT_MAP = {
    "COMP":    "compound",
    "MKR":     "makerdao",
    "AAVE":    "aave",
    "UNI":     "uniswap",
    "CRV":     "curve-finance",
    "RPL":     "rocket-pool",
    "JUP":     "jupiter-exchange",
    "MPL_SYRUP": "maple-finance",
    "GMX":     "gmx",
    "DRIFT":   "drift",
    "ETHFI":   "ether-fi",
    "GRT":     "the-graph",
    "OP":      "optimism",
    "POL":     "polygon",
    "ARB":     "arbitrum",
    "ENS":     "ethereum-name-service",
    "DIMO":    "dimo",
    "IOTX":    "iotex",
    "WXM":     "weatherxm",
    "ANYONE":  None,   # unlikely; flag for DefiLlama fallback
    "GRASS":   None,   # unlikely
    "LPT":     "livepeer",
    "HNT":     "helium",
    "GEOD":    None,   # unlikely
    "FIL":     "filecoin",
    "RENDER":  "render-network",
    "POKT":    "pocket-network",
    "GTC":     "gitcoin",
    "TEC":     None,   # wound down; report zero revenue
}


def get(endpoint, params=None):
    url = BASE_URL + endpoint
    resp = requests.get(url, headers=HEADERS, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def discover_projects():
    """Fetch all Token Terminal projects and build a slug→id map."""
    data = get("/projects")
    projects = {}
    for p in data:
        slug = p.get("project_id") or p.get("slug") or p.get("id", "")
        name = p.get("name", "")
        projects[slug] = name
    return projects


def get_project_metrics(project_id: str) -> dict:
    """
    Fetch trailing 30d financials for a project.
    Returns dict with revenue, fdv, incentives, active_addresses, treasury.
    """
    result = {
        "revenue_30d_sum": None,
        "fdv_usd": None,
        "incentives_30d_sum": None,
        "active_addresses_30d": None,
        "treasury_usd": None,
    }

    # Try /projects/{id}/metrics endpoint (standard TT API)
    try:
        data = get(f"/projects/{project_id}/metrics", params={
            "metric_ids": "revenue,fees,token_incentives,fdv,active_addresses,treasury",
            "start": str(WINDOW_START),
            "end": str(SNAPSHOT),
            "granularity": "daily",
        })

        # Parse response - TT returns list of daily rows
        rows = data if isinstance(data, list) else data.get("data", data.get("metrics", []))
        if rows:
            df = pd.DataFrame(rows)
            df.columns = [c.lower().replace(" ", "_") for c in df.columns]

            # Revenue: sum over window
            for col in ("revenue", "protocol_revenue", "fees"):
                if col in df.columns:
                    result["revenue_30d_sum"] = pd.to_numeric(df[col], errors="coerce").sum()
                    break

            # Token incentives: sum over window
            for col in ("token_incentives", "token_incentive_emissions_usd", "incentives"):
                if col in df.columns:
                    result["incentives_30d_sum"] = pd.to_numeric(df[col], errors="coerce").sum()
                    break

            # FDV: last available value
            for col in ("fdv", "fully_diluted_valuation", "market_cap_fully_diluted"):
                if col in df.columns:
                    vals = pd.to_numeric(df[col], errors="coerce").dropna()
                    if len(vals):
                        result["fdv_usd"] = vals.iloc[-1]
                    break

            # Active addresses
            for col in ("active_addresses", "dau", "daily_active_addresses"):
                if col in df.columns:
                    result["active_addresses_30d"] = pd.to_numeric(df[col], errors="coerce").mean()
                    break

            # Treasury
            for col in ("treasury", "treasury_usd", "treasury_balance"):
                if col in df.columns:
                    vals = pd.to_numeric(df[col], errors="coerce").dropna()
                    if len(vals):
                        result["treasury_usd"] = vals.iloc[-1]
                    break

    except Exception as e:
        print(f"    Metrics endpoint failed for {project_id}: {e}")

    # Try /projects/{id} for FDV / snapshot values if metrics missing
    if result["fdv_usd"] is None:
        try:
            snap = get(f"/projects/{project_id}")
            for key in ("fdv", "fully_diluted_valuation", "market_cap_fully_diluted"):
                val = snap.get(key) or (snap.get("metrics", {}) or {}).get(key)
                if val:
                    result["fdv_usd"] = float(val)
                    break
        except Exception as e:
            print(f"    Snapshot endpoint failed for {project_id}: {e}")

    return result


def annualize(val_30d):
    """Convert 30-day sum to annualized value."""
    if val_30d is None:
        return None
    return val_30d * (365 / 30)


def main():
    print("=== Token Terminal Financial Covariates ===")
    print(f"Snapshot: {SNAPSHOT}")
    print(f"Window: {WINDOW_START} → {SNAPSHOT}")

    # Discover available projects
    print("\nDiscovering Token Terminal projects...")
    try:
        all_projects = discover_projects()
        print(f"  Found {len(all_projects)} projects")
        # Check coverage for our protocols
        for sym, slug in PROJECT_MAP.items():
            if slug and slug not in all_projects:
                print(f"  WARNING: {sym} → '{slug}' not found in project list")
    except Exception as e:
        print(f"  WARNING: Could not discover projects: {e}")
        all_projects = {}

    rows = []
    needs_fallback = []

    for sym, slug in PROJECT_MAP.items():
        print(f"\n  {sym} ({slug or 'N/A'})...")

        if slug is None:
            print(f"    No TT slug → fallback")
            rows.append({
                "token": sym, "tt_project_id": None,
                "revenue_annual_usd": None, "fdv_usd": None,
                "incentives_annual_usd": None, "subsidy_ratio": None,
                "active_addresses_30d": None, "treasury_usd": None,
                "source": "fallback_needed", "notes": "No Token Terminal coverage",
            })
            needs_fallback.append(sym)
            continue

        if slug not in all_projects and all_projects:
            print(f"    Slug '{slug}' not in project list → trying anyway...")

        metrics = get_project_metrics(slug)

        rev = annualize(metrics["revenue_30d_sum"])
        inc = annualize(metrics["incentives_30d_sum"])

        # Subsidy ratio = incentives / (revenue + incentives), bounded [0,1]
        if inc is not None and rev is not None and (rev + inc) > 0:
            sub_ratio = round(inc / (rev + inc), 4)
        elif inc is not None and inc > 0 and (rev is None or rev == 0):
            sub_ratio = 1.0
        else:
            sub_ratio = None

        has_data = any(v is not None for v in [rev, metrics["fdv_usd"], inc])
        if not has_data:
            print(f"    No data returned → fallback")
            needs_fallback.append(sym)
            source = "fallback_needed"
        else:
            source = "token_terminal"

        rows.append({
            "token": sym,
            "tt_project_id": slug,
            "revenue_annual_usd": round(rev, 0) if rev else None,
            "fdv_usd": round(metrics["fdv_usd"], 0) if metrics["fdv_usd"] else None,
            "incentives_annual_usd": round(inc, 0) if inc else None,
            "subsidy_ratio": sub_ratio,
            "active_addresses_30d": round(metrics["active_addresses_30d"], 0) if metrics["active_addresses_30d"] else None,
            "treasury_usd": round(metrics["treasury_usd"], 0) if metrics["treasury_usd"] else None,
            "source": source,
            "notes": "",
        })

        # Print summary
        print(f"    revenue: ${rev:,.0f}/yr" if rev else "    revenue: N/A")
        print(f"    FDV: ${metrics['fdv_usd']:,.0f}" if metrics["fdv_usd"] else "    FDV: N/A")
        print(f"    incentives: ${inc:,.0f}/yr" if inc else "    incentives: N/A")
        print(f"    subsidy_ratio: {sub_ratio}" if sub_ratio else "    subsidy_ratio: N/A")

    df = pd.DataFrame(rows)
    out = PROJECT_DIR / "covariates_tokenterminal.csv"
    df.to_csv(out, index=False)
    print(f"\nSaved {len(df)} rows → {out}")

    if needs_fallback:
        print(f"\nNeeds DefiLlama fallback ({len(needs_fallback)}): {', '.join(needs_fallback)}")
        with open(PROJECT_DIR / "fallback_needed.json", "w") as f:
            json.dump(needs_fallback, f)

    return df, needs_fallback


if __name__ == "__main__":
    main()
