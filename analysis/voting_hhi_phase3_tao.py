#!/usr/bin/env python3
"""
B2 voting-HHI Phase 3 collector: TAO (Bittensor).

Native Substrate chain (NOT EVM). Governance routes through delegated validator
stake plus an elected stake-weighted Senate (max 12 seats) plus a 3-person
Opentensor Foundation Triumvirate that holds exclusive propose/close rights.

MEASURE (S12 voter-pool HHI, matching the existing 13-row data of record):
validator-stake-HHI over delegated TAO per validator hotkey. The per-validator
"dominance" field from Taostats is the percent share of total network stake; the
validator set is the de-facto voter pool for stake-weighted governance (Senate
seats are allocated by validator stake rank).

SOURCE: Taostats Pro REST API.
  GET https://api.taostats.io/api/validator/latest/v1?limit=75
  header: Authorization: <TAOSTATS_API_KEY>

Because total validators is about 75 (one page at limit=75), the entire voter
pool is captured; top-N truncation at 100 is a no-op here (n_sampled equals the
full validator count, which is below 100).

Re-runnable: python3 voting_hhi_phase3_tao.py
Writes raw per-validator CSV to ../data/raw/voting_hhi_phase3_tao_raw.csv

DISCIPLINE: does not commit; does not modify data/raw/voting_hhi.csv (orchestrator
merges). No em-dashes anywhere.
"""

import csv
import json
import os
import sys
import time
import urllib.request
import urllib.error

import numpy as np

API_URL = "https://api.taostats.io/api/validator/latest/v1"
PAGE_LIMIT = 75

# The taostats edge WAF rejects the default Python-urllib User-Agent with a 403;
# a browser-like User-Agent plus an explicit Accept header returns 200. Verified
# 2026-05-30: same Authorization key works under curl but fails under bare urllib.
REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (research-collector; voting-hhi-phase3)",
    "Accept": "application/json",
}

HERE = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(HERE, "..", "data", "raw")
RAW_PATH = os.path.join(RAW_DIR, "voting_hhi_phase3_tao_raw.csv")

HOLDINGS_HHI_OF_RECORD = 0.00749


def compute_hhi(values):
    v = np.array(values, dtype=float)
    v = v[v > 0]
    if len(v) == 0 or v.sum() == 0:
        return None
    shares = v / v.sum()
    return float(np.sum(shares ** 2))


def compute_gini(values):
    v = np.sort(np.array([x for x in values if x > 0], dtype=float))
    n = len(v)
    if n == 0 or v.sum() == 0:
        return None
    d = np.abs(v[:, None] - v[None, :]).sum()
    return float(d / (2 * n * v.sum()))


def fetch_validators():
    """Pull all validators, paginating if total_items exceeds one page."""
    key = os.environ.get("TAOSTATS_API_KEY")
    if not key:
        print("ERROR: TAOSTATS_API_KEY not set in environment.", file=sys.stderr)
        sys.exit(1)

    headers = dict(REQUEST_HEADERS)
    headers["Authorization"] = key

    rows = []
    page = 1
    while True:
        url = "%s?limit=%d&page=%d" % (API_URL, PAGE_LIMIT, page)
        payload = None
        last_err = None
        for attempt in range(4):
            req = urllib.request.Request(url, headers=headers)
            try:
                with urllib.request.urlopen(req, timeout=60) as resp:
                    payload = json.loads(resp.read().decode("utf-8"))
                break
            except urllib.error.HTTPError as exc:
                last_err = exc
                # Back off on transient 403 / 429; the WAF occasionally rate-limits.
                if exc.code in (403, 429) and attempt < 3:
                    time.sleep(2 * (attempt + 1))
                    continue
                break
        if payload is None:
            code = getattr(last_err, "code", "?")
            reason = getattr(last_err, "reason", "unknown")
            print("ERROR: HTTP %s on page %d: %s" % (code, page, reason),
                  file=sys.stderr)
            sys.exit(1)

        data = payload.get("data", [])
        rows.extend(data)

        pg = payload.get("pagination", {})
        total_pages = pg.get("total_pages", 1)
        if page >= total_pages or not data:
            break
        page += 1

    return rows


def extract(row):
    """Pull hotkey ss58, dominance (percent), and raw stake from one API row."""
    hk = row.get("hotkey", {})
    ss58 = hk.get("ss58") if isinstance(hk, dict) else str(hk)
    name = row.get("name") or ""
    dominance = float(row.get("dominance", 0.0))
    # stake is a raw integer string in RAO (1 TAO = 1e9 RAO); kept raw for shares.
    stake_raw = row.get("stake", "0")
    try:
        stake = float(stake_raw)
    except (TypeError, ValueError):
        stake = 0.0
    nominators = row.get("nominators", 0)
    return {
        "hotkey_ss58": ss58,
        "name": name,
        "dominance_pct": dominance,
        "stake_raw": stake,
        "nominators": nominators,
    }


def main():
    raw_rows = fetch_validators()
    validators = [extract(r) for r in raw_rows]
    # Sort descending by dominance (percent network-stake share).
    validators.sort(key=lambda d: d["dominance_pct"], reverse=True)

    n_unique = len(validators)
    n_sampled = min(100, n_unique)
    sample = validators[:n_sampled]

    # Write the raw evidence file the verifier will independently recompute from.
    os.makedirs(RAW_DIR, exist_ok=True)
    with open(RAW_PATH, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["rank", "hotkey_ss58", "name", "dominance_pct",
                    "stake_raw", "nominators"])
        for i, d in enumerate(validators, start=1):
            w.writerow([i, d["hotkey_ss58"], d["name"],
                        "%.20f" % d["dominance_pct"],
                        "%.0f" % d["stake_raw"], d["nominators"]])
    print("Wrote raw evidence: %s (%d validators)" % (RAW_PATH, n_unique))

    # (a) canonical voting_hhi from dominance percentages.
    dom = [d["dominance_pct"] for d in sample]
    dom_shares = [x / 100.0 for x in dom]
    voting_hhi_dom = float(np.sum(np.array(dom_shares) ** 2))

    # (b) cross-check from raw stake field, normalized within the sample.
    stake_vals = [d["stake_raw"] for d in sample]
    voting_hhi_stake = compute_hhi(stake_vals)

    # Cumulative dominance of top 1 / 5 / 10 validators.
    top1 = sum(dom[:1])
    top5 = sum(dom[:5])
    top10 = sum(dom[:10])

    # Gini over the dominance vector (top-N sample).
    gini = compute_gini(dom)

    # Senate top-12 seat concentration: share of total stake held by top 12.
    senate_top12 = sum(dom[:12])

    ratio = voting_hhi_dom / HOLDINGS_HHI_OF_RECORD
    if ratio > 1.1:
        direction = "amplify"
    elif ratio < 0.9:
        direction = "disperse"
    else:
        direction = "equivalent"

    data_ts = raw_rows[0].get("timestamp") if raw_rows else None

    result = {
        "token": "TAO",
        "source": "taostats",
        "voting_hhi": voting_hhi_dom,
        "voting_hhi_stake_crosscheck": voting_hhi_stake,
        "voting_top1_pct": top1,
        "voting_top5_pct": top5,
        "voting_top10_pct": top10,
        "voting_gini": gini,
        "n_unique_voters": n_unique,
        "n_sampled": n_sampled,
        "senate_top12_stake_pct": senate_top12,
        "holdings_hhi_of_record": HOLDINGS_HHI_OF_RECORD,
        "ratio_voting_over_holdings": ratio,
        "observed_direction": direction,
        "api_snapshot_timestamp": data_ts,
    }
    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    main()
