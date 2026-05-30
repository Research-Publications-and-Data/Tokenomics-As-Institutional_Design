#!/usr/bin/env python3
"""
voting_hhi_phase3_snx.py

B2 governance-concentration paper, voting-HHI Phase 3 (N=52 sample additions).
Acquires ONE election-layer voting-concentration row for SNX (Synthetix).

WHAT THIS MEASURES (and why the ELECTION layer):
  Synthetix governance is an ELECTED multi-seat council. Token holders do NOT
  vote on individual SIP/SCCP proposals by token weight; the proposal layer is
  structurally un-concentratable by token weight (an elected, equal-weight
  council decides). The ONLY token-weighted vote is the periodic council
  ELECTION, where per-voter voting power is the quadratically-weighted staked
  SNX "weighted debt". We therefore measure concentration at the ELECTION layer.

  Source: Snapshot GraphQL (keyless), space "synthetix-elections.eth".
  Each election proposal uses the Snapshot strategy "whitelist-weighted-json",
  which loads the per-voter weighted-debt voting power directly into the vote
  vp field. So vp on an election proposal IS the per-voter weighted-debt
  voting power; no further transformation is needed.

MEASURE (S12 voter-pool HHI; matches the existing 13-row data of record):
  - Build a per-voter weighted-debt voting-power vector over the sampled window
    (the most recent council election cycle; a cycle has multiple seats voted in
    the same window, and a given voter casts the SAME vp on each seat, so the
    per-voter vp is the max across that voter's seats in the cycle).
  - Sort descending; take the TOP 100 (or all, if fewer than 100).
  - Normalize shares WITHIN that top-N sample: shares = top_n / top_n.sum().
  - voting_hhi = sum(shares**2).
  - voting_top1/5/10_pct from the cumulative shares.
  - voting_gini over the top-N vector via mean-absolute-difference (positive
    convention), per the exact functions below.
  - n_unique_voters = distinct voters in the window (before top-N truncation).
  - n_sampled = min(100, available).

SAMPLED WINDOW:
  Primary row = the MOST RECENT council election cycle. A SENSITIVITY block also
  reports the prior cycle and the union of the last two cycles. The primary row
  is what gets written to the row dict and printed as the deliverable.

DISCIPLINE:
  - Keyless Snapshot GraphQL; no API key required.
  - Re-runnable: python3 analysis/voting_hhi_phase3_snx.py
  - Writes raw per-voter evidence to data/raw/voting_hhi_phase3_snx_raw.csv
  - Does NOT modify data/raw/voting_hhi.csv (the orchestrator merges).
"""

import csv
import json
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import requests

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
SNAPSHOT_API = "https://hub.snapshot.org/graphql"
ELECTION_SPACE = "synthetix-elections.eth"  # confirmed: name "Synthetix Elections", 4 proposals
TOKEN = "SNX"
SOURCE_LABEL = "snapshot"
HOLDINGS_HHI_OF_RECORD = 0.01707

PROJECT_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_DIR / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)
RAW_CSV = RAW_DIR / "voting_hhi_phase3_snx_raw.csv"


# ---------------------------------------------------------------------------
# Exact measure functions (copied verbatim from the spec; do NOT alter)
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# Snapshot GraphQL helper (keyless; retry with backoff for 429s)
# ---------------------------------------------------------------------------
def snapshot_query(query, variables=None, retries=6):
    for attempt in range(retries):
        try:
            r = requests.post(
                SNAPSHOT_API,
                json={"query": query, "variables": variables or {}},
                timeout=30,
            )
            if r.status_code == 429:
                time.sleep(5 * (attempt + 1))
                continue
            r.raise_for_status()
            data = r.json()
            if "errors" in data:
                print(f"  GraphQL errors: {data['errors']}")
            return data.get("data", {}) or {}
        except Exception as e:  # noqa: BLE001
            if attempt < retries - 1:
                time.sleep(3 * (attempt + 1))
            else:
                print(f"  Request failed after {retries} attempts: {e}")
                return {}
    return {}


def fetch_election_proposals():
    """Return election proposals with an ISO date, newest first."""
    q = """query($space:String!){
      proposals(first:100, where:{space:$space}, orderBy:"created", orderDirection:desc){
        id title type state votes scores_total created
      }
    }"""
    props = snapshot_query(q, {"space": ELECTION_SPACE}).get("proposals", []) or []
    for p in props:
        p["date"] = datetime.fromtimestamp(p["created"], timezone.utc).date().isoformat()
    return props


def fetch_votes(proposal_id):
    """Pull all votes (per-voter weighted-debt vp) for one election proposal."""
    q = """query($proposal:String!, $first:Int!, $skip:Int!){
      votes(first:$first, skip:$skip, where:{proposal:$proposal},
            orderBy:"vp", orderDirection:desc){ voter vp choice created }
    }"""
    out = []
    skip = 0
    while True:
        data = snapshot_query(q, {"proposal": proposal_id, "first": 1000, "skip": skip})
        votes = data.get("votes") or []
        if not votes:
            break
        out.extend(votes)
        if len(votes) < 1000:
            break
        skip += 1000
        time.sleep(0.4)
    return out


# ---------------------------------------------------------------------------
# Build per-voter pools and compute the S12 row
# ---------------------------------------------------------------------------
def build_pool(proposals, raw_rows=None):
    """
    Given a list of election proposals (a cycle, or a union of cycles), build the
    per-voter weighted-debt vp pool. A voter casts the same vp on each seat in a
    cycle; per-voter vp = max across that voter's seats. Optionally append rows
    (voter, proposal, vp) to raw_rows for the evidence CSV.
    """
    pool = {}
    for p in proposals:
        votes = fetch_votes(p["id"])
        for v in votes:
            voter = v["voter"]
            vp = float(v.get("vp") or 0.0)
            if raw_rows is not None:
                raw_rows.append({
                    "voter": voter,
                    "voting_power": vp,
                    "proposal_id": p["id"],
                    "proposal_title": p["title"],
                    "election_date": p["date"],
                    "choice": str(v.get("choice", "")),
                })
            if vp > pool.get(voter, 0.0):
                pool[voter] = vp
        time.sleep(0.4)
    return pool


def s12_row(pool):
    """Compute the S12 top-100 voter-pool HHI row from a per-voter vp pool."""
    vals = sorted([x for x in pool.values() if x > 0], reverse=True)
    n_unique = len(vals)
    if n_unique == 0:
        return None
    top = vals[:100]
    n_sampled = len(top)
    arr = np.array(top, dtype=float)
    shares = arr / arr.sum()
    return {
        "voting_hhi": compute_hhi(top),
        "voting_gini": compute_gini(top),
        "voting_top1_pct": float(100.0 * shares[0]),
        "voting_top5_pct": float(100.0 * shares[:5].sum()),
        "voting_top10_pct": float(100.0 * shares[:10].sum()),
        "n_unique_voters": n_unique,
        "n_sampled_top100": n_sampled,
    }


def group_cycles(proposals):
    """Group election proposals by their election date (each date = one cycle)."""
    cycles = {}
    for p in proposals:
        cycles.setdefault(p["date"], []).append(p)
    # newest first
    return [(d, cycles[d]) for d in sorted(cycles.keys(), reverse=True)]


def main():
    print(f"=== B2 voting-HHI Phase 3: {TOKEN} (election-layer weighted-debt) ===")
    print(f"Space: {ELECTION_SPACE} (keyless Snapshot GraphQL)")

    proposals = fetch_election_proposals()
    # Keep only proposals that actually carry votes (an election has voters).
    proposals = [p for p in proposals if (p.get("votes") or 0) > 0]
    if not proposals:
        print("NO election proposals with votes found. Status: NO_DATA.")
        return

    cycles = group_cycles(proposals)
    print(f"Found {len(proposals)} election proposals across {len(cycles)} cycle(s):")
    for d, ps in cycles:
        seats = ", ".join(p["title"].split(":")[-1].strip() for p in ps)
        print(f"  {d}: {len(ps)} seat(s) [{seats}]  votes={[p['votes'] for p in ps]}")

    # PRIMARY ROW = most recent council election cycle.
    raw_rows = []  # full per-voter, per-seat evidence across ALL cycles we touch
    primary_date, primary_props = cycles[0]
    print(f"\nPRIMARY (most recent election cycle): {primary_date}")
    primary_pool = build_pool(primary_props, raw_rows=raw_rows)
    primary = s12_row(primary_pool)

    # SENSITIVITY = prior cycle + union of last two cycles.
    sensitivity = {}
    if len(cycles) >= 2:
        prior_date, prior_props = cycles[1]
        prior_pool = build_pool(prior_props, raw_rows=raw_rows)
        sensitivity["prior_cycle"] = {"date": prior_date, **(s12_row(prior_pool) or {})}

        union_pool = {}
        for d, ps in cycles[:2]:
            sub = build_pool(ps, raw_rows=None)  # already captured in raw_rows above
            for k, vv in sub.items():
                if vv > union_pool.get(k, 0.0):
                    union_pool[k] = vv
        sensitivity["last_two_union"] = {
            "dates": [cycles[0][0], cycles[1][0]],
            **(s12_row(union_pool) or {}),
        }

    # Write the raw per-voter evidence CSV (the verifier recomputes from this).
    with RAW_CSV.open("w", newline="") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=["voter", "voting_power", "proposal_id",
                        "proposal_title", "election_date", "choice"],
        )
        writer.writeheader()
        for row in raw_rows:
            writer.writerow(row)
    print(f"\nWrote {len(raw_rows)} raw per-voter/per-seat rows -> {RAW_CSV}")

    # Direction vs holdings.
    ratio = (primary["voting_hhi"] / HOLDINGS_HHI_OF_RECORD) if primary and primary["voting_hhi"] else None
    if ratio is None:
        direction = "unknown"
    elif ratio > 1.1:
        direction = "amplify"
    elif ratio < 0.9:
        direction = "disperse"
    else:
        direction = "equivalent"

    print("\n=== PRIMARY ROW (most recent election cycle) ===")
    print(json.dumps({"symbol": TOKEN, "source": SOURCE_LABEL,
                      "election_date": primary_date, **primary}, indent=2))
    print("\n=== SENSITIVITY ===")
    print(json.dumps(sensitivity, indent=2))
    print(f"\nholdings_hhi_of_record = {HOLDINGS_HHI_OF_RECORD}")
    print(f"voting_hhi / holdings_hhi ratio = {ratio:.2f}" if ratio else "ratio = n/a")
    print(f"observed_direction = {direction}")

    return {"symbol": TOKEN, "source": SOURCE_LABEL,
            "election_date": primary_date, **primary,
            "ratio": ratio, "observed_direction": direction,
            "sensitivity": sensitivity}


if __name__ == "__main__":
    main()
