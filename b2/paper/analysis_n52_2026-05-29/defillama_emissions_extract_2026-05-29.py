#!/usr/bin/env python3
"""Corrected extraction of DefiLlama incentive emissions + insider unlocks (the schedule-method
+ unlock-netting inputs). DISCOVERY FINDING: DefiLlama's `rawEmission` field is CUMULATIVE
(monotonic, equal to `unlocked`); per-period emission = month-over-month DIFF of the cumulative,
NOT the sum. (The initial gather summed it, producing ~5-orders-of-magnitude overcounts.)

Reads the validated slugs from defillama_readiness_inventory_2026-05-29.csv (valid rows), fetches
each curve once (free CDN), and extracts CORRECT monthly per-period tokens:
  incentive_emission_tokens = sum over INCENTIVE-bucket series of monthly delta(cumulative)
  insider_unlock_tokens     = sum over INSIDER-bucket series of monthly delta(cumulative)
  burned_tokens             = monthly delta(cumulative burned)
Overwrites defillama_monthly_emissions_unlocks_2026-05-29.csv with the corrected series. Uses
curl (CDN 403s default urllib UA).
"""
import csv, os, subprocess, json, time, re
from collections import defaultdict
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "defillama_emissions")


def f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def bucket(label):
    l = (label or "").lower()
    if any(k in l for k in ["incentive", "farming", "emission", "reward", "staking", "liquidity", "mining"]):
        return "INCENTIVE"
    if any(k in l for k in ["team", "investor", "advisor", "insider", "private", "seed", "strategic", "founder", "core contributor"]):
        return "INSIDER"
    return "OTHER"


def curl_json(url):
    out = subprocess.run(["curl", "-s", url], capture_output=True, text=True, timeout=90).stdout
    try:
        return json.loads(out)
    except Exception:
        return None


def monthly_delta(series_pts):
    """cumulative -> per-month delta (month-end minus prior month-end)."""
    me = {}
    for p in series_pts:
        m = datetime.fromtimestamp(p["timestamp"], tz=timezone.utc).strftime("%Y-%m")
        me[m] = p  # last wins -> month-end
    ms = sorted(me)
    out = defaultdict(float)
    prev = None
    for m in ms:
        cum = me[m]
        if prev is not None:
            out[m] = max(0.0, (cum["_v"] - prev["_v"]))
        prev = cum
    return out


def main():
    inv = list(csv.DictReader(open(os.path.join(OUT, "defillama_readiness_inventory_2026-05-29.csv"))))
    valid = [r for r in inv if r.get("valid") == "True" and r.get("defillama_slug")]
    monthly = []
    for r in valid:
        tok, slug = r["token"], r["defillama_slug"]
        d = curl_json(f"https://defillama-datasets.llama.fi/emissions/{slug}")
        time.sleep(0.5)
        if not d:
            print(f"  {tok:8} {slug} FETCH FAIL")
            continue
        data = d.get("documentedData", {}).get("data", [])
        inc = defaultdict(float); ins = defaultdict(float); brn = defaultdict(float)
        for s in data:
            b = bucket(s.get("label")); pts = s.get("data", [])
            for p in pts:
                p["_v"] = p.get("rawEmission") or 0
            md_emis = monthly_delta(pts)
            for p in pts:
                p["_v"] = p.get("unlocked") or 0
            md_unl = monthly_delta(pts)
            for p in pts:
                p["_v"] = p.get("burned") or 0
            md_brn = monthly_delta(pts)
            for m, v in md_emis.items():
                if b == "INCENTIVE":
                    inc[m] += v
            for m, v in md_unl.items():
                if b == "INSIDER":
                    ins[m] += v
            for m, v in md_brn.items():
                brn[m] += v
        allm = sorted(set(inc) | set(ins) | set(brn))
        for m in allm:
            monthly.append({"token": tok, "month": m, "incentive_emission_tokens": round(inc.get(m, 0), 2),
                            "insider_unlock_tokens": round(ins.get(m, 0), 2), "burned_tokens": round(brn.get(m, 0), 2)})
        last = allm[-1] if allm else "?"
        print(f"  {tok:8} {slug:22} months={len(allm)} last={last} inc_last={round(inc.get(last,0),1)} ins_last={round(ins.get(last,0),1)}")

    with open(os.path.join(OUT, "defillama_monthly_emissions_unlocks_2026-05-29.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["token", "month", "incentive_emission_tokens", "insider_unlock_tokens", "burned_tokens"]); w.writeheader(); w.writerows(monthly)
    print(f"\n[written] corrected defillama_monthly_emissions_unlocks_2026-05-29.csv ({len(monthly)} rows, {len(valid)} protocols)")


if __name__ == "__main__":
    main()
