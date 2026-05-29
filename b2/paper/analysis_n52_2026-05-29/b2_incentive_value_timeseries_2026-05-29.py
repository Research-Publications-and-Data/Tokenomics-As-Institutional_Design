#!/usr/bin/env python3
"""B2 incentive / new-supply VALUE over time (the part-b build).

Constructs a monthly time-series of token new-supply USD value (an emission/incentive-value
proxy) for the 50-protocol cross-section, from CoinGecko daily price + market-cap series.
KEY identity: implied circulating supply = market_cap / price; monthly new supply = month-end
circ minus prior month-end circ; new-supply value = new_supply * mean monthly price.

Coverage: 40 protocols from the pre-existing 59-coin daily set
(/Users/zach/b2-governance-data/data/coingecko/<id>.csv) + 10 newly fetched (the new cohort)
in ./coingecko_new10/<id>.csv. Full 50/50.

Calibration anchors (annual): Token Terminal incentives_annual_usd (token_terminal_metrics.csv,
9 coins) + on-chain DePIN emissions (geodnet_monthly_emissions.csv). Reported as a ratio per
calibration coin (quality flag), NOT used to rescale.

HONEST LABEL: net new-supply value conflates emissions with scheduled unlocks and is net of
burns. It is an UPPER-bound proxy for emission/incentive value, not audited mining rewards.
Reads persisted data only; no /tmp, no live-API (the CoinGecko fetch is a separate step).

Outputs: incentive_value_monthly_2026-05-29.csv (panel) + incentive_value_annual_2026-05-29.csv
(per-protocol trailing-12-month value, which populates the sparse Token Terminal coverage) +
b2_incentive_value_results_2026-05-29.json.
"""
import csv, os, glob, json, re
from collections import defaultdict

A = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
B = "/Users/zach/b2-governance-data"
HERE = os.path.dirname(os.path.abspath(__file__))
NEW10 = os.path.join(HERE, "coingecko_new10")
EXIST = os.path.join(B, "data/coingecko")
SEC = {"DePIN": "DePIN", "DeFi": "DeFi", "L1_L2_Infra": "L1"}


def f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


# explicit id map for the new 10 + the two fuzzy fixes
ID = {"SNX": "havven", "GNO": "gnosis", "ENA": "ethena", "WLFI": "world-liberty-financial",
      "JTO": "jito-governance-token", "BONK": "bonk", "KMNO": "kamino", "ALGO": "algorand",
      "DOT": "polkadot", "TAO": "bittensor", "MPL_SYRUP": "syrup", "ANYONE": "airtor-protocol"}


def find_daily(tok, proto):
    cand = ID.get(tok)
    for base in (NEW10, EXIST):
        if cand and os.path.exists(os.path.join(base, f"{cand}.csv")):
            return os.path.join(base, f"{cand}.csv")
    # market csv id
    for r in csv.DictReader(open(os.path.join(A, "data/raw/coingecko_market.csv"))):
        if r.get("token") == tok and r.get("coingecko_id"):
            p = os.path.join(EXIST, f"{r['coingecko_id']}.csv")
            if os.path.exists(p):
                return p
    # fuzzy by name
    for p in glob.glob(os.path.join(EXIST, "*.csv")):
        d = os.path.basename(p)[:-4]
        if norm(tok) == norm(d) or norm(d) in norm(proto) or norm(proto).startswith(norm(d)):
            return p
    return None


def monthly_value(path):
    """month -> (circ_end, mean_price). circ = market_cap/price."""
    by = defaultdict(list)
    for r in csv.DictReader(open(path)):
        p = f(r.get("price_usd")); mc = f(r.get("market_cap_usd")); d = r.get("date", "")
        if p and mc and p > 0 and len(d) >= 7:
            by[d[:7]].append((d, mc / p, p))
    months = sorted(by)
    out = []
    for m in months:
        recs = sorted(by[m])
        circ_end = recs[-1][1]
        mean_price = sum(x[2] for x in recs) / len(recs)
        out.append((m, circ_end, mean_price))
    return out


def main():
    frame = [(r["token"], r["protocol"], SEC[r["category"]], f(r.get("fdv_usd")))
             for r in csv.DictReader(open(os.path.join(A, "data/processed/regression_data_april2026.csv")))
             if r.get("category") in SEC]
    tt = {r["token"]: f(r.get("incentives_annual_usd")) for r in csv.DictReader(open(os.path.join(A, "data/raw/token_terminal_metrics.csv")))}

    panel = []          # (token, sector, month, new_supply_value_usd)
    annual = []         # per-protocol trailing-12-month new-supply value
    covered = 0
    for tok, proto, sec, fdv in frame:
        path = find_daily(tok, proto)
        if not path:
            annual.append({"token": tok, "sector": sec, "covered": False, "ttm_newsupply_value_usd": "", "tt_incentives_annual_usd": tt.get(tok)})
            continue
        covered += 1
        mv = monthly_value(path)
        last12_val = 0.0
        for i in range(1, len(mv)):
            (m0, c0, _), (m1, c1, p1) = mv[i - 1], mv[i]
            val = (c1 - c0) * p1
            panel.append({"token": tok, "sector": sec, "month": m1, "new_supply": round(c1 - c0, 2),
                          "mean_price_usd": round(p1, 6), "new_supply_value_usd": round(val, 2)})
        for rec in panel[-12:]:
            if rec["token"] == tok:
                last12_val += rec["new_supply_value_usd"]
        annual.append({"token": tok, "sector": sec, "covered": True,
                       "ttm_newsupply_value_usd": round(last12_val, 2),
                       "tt_incentives_annual_usd": tt.get(tok),
                       "calib_ratio": (round(last12_val / tt[tok], 2) if tt.get(tok) and tt[tok] > 0 else "")})

    # write panel + annual
    with open(os.path.join(HERE, "incentive_value_monthly_2026-05-29.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["token", "sector", "month", "new_supply", "mean_price_usd", "new_supply_value_usd"]); w.writeheader(); w.writerows(panel)
    with open(os.path.join(HERE, "incentive_value_annual_2026-05-29.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["token", "sector", "covered", "ttm_newsupply_value_usd", "tt_incentives_annual_usd", "calib_ratio"]); w.writeheader()
        for r in annual:
            w.writerow({k: r.get(k, "") for k in ["token", "sector", "covered", "ttm_newsupply_value_usd", "tt_incentives_annual_usd", "calib_ratio"]})

    n_tt_before = sum(1 for r in annual if r.get("tt_incentives_annual_usd") not in (None, "", 0, 0.0))
    n_after = sum(1 for r in annual if r.get("covered"))
    print(f"coverage: {covered}/{len(frame)} protocols have a daily series and a constructed incentive-value series")
    print(f"incentive coverage BEFORE (Token Terminal non-zero): {n_tt_before} | AFTER (constructed): {n_after}")
    print(f"panel rows: {len(panel)} monthly observations\n")

    print("=== calibration (constructed trailing-12mo vs Token Terminal annual) ===")
    for r in annual:
        if r.get("calib_ratio") not in ("", None):
            print(f"  {r['token']:10} constructed=${r['ttm_newsupply_value_usd']:>16,.0f}  TT=${r['tt_incentives_annual_usd']:>14,.0f}  ratio={r['calib_ratio']}")

    print("\n=== trailing-12-month new-supply value by sector (sum, descriptive) ===")
    bysec = defaultdict(float); cnt = defaultdict(int)
    for r in annual:
        if r.get("covered") and isinstance(r.get("ttm_newsupply_value_usd"), (int, float)):
            bysec[r["sector"]] += max(0, r["ttm_newsupply_value_usd"]); cnt[r["sector"]] += 1
    for s in ("DePIN", "DeFi", "L1"):
        print(f"  {s:6} sum positive new-supply value (ttm) = ${bysec[s]:>16,.0f}  (N={cnt[s]})")

    res = {"coverage": f"{covered}/{len(frame)}", "incentive_coverage_before_TT": n_tt_before,
           "incentive_coverage_after_constructed": n_after, "panel_rows": len(panel),
           "annual": annual, "by_sector_ttm_positive": {s: round(bysec[s], 2) for s in bysec}}
    json.dump(res, open(os.path.join(HERE, "b2_incentive_value_results_2026-05-29.json"), "w"), indent=1)
    print("\n[written] incentive_value_monthly_2026-05-29.csv + incentive_value_annual_2026-05-29.csv + b2_incentive_value_results_2026-05-29.json")
    print("[done] no /tmp dependency, no live-API in the build (CoinGecko fetch is a separate step).")


if __name__ == "__main__":
    main()
