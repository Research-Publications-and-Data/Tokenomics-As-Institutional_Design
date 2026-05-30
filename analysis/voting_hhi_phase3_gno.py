#!/usr/bin/env python3
"""
voting_hhi_phase3_gno.py

B2 governance-concentration paper, voting-HHI Phase 3 (N=52 sample additions).
Token: GNO (Gnosis). CONTROL / clean anchor: linear governance (1 GNO = 1 vote),
no escrow, no conviction, no quadratic weighting.

Source: Snapshot GraphQL (keyless) at https://hub.snapshot.org/graphql, space "gnosis.eth".

Measure (S12 voter-pool HHI; matches the existing voting-HHI data of record):
  - Build a per-voter total voting-power (vp) vector summed across the sampled
    closed proposals (recent window).
  - Sort descending; take the TOP 100 (or all if fewer than 100).
  - Normalize shares WITHIN that top-N sample: shares = top_n / top_n.sum().
  - voting_hhi = sum(shares**2).
  - voting_top1_pct = 100*shares[0]; top5 = 100*sum(shares[:5]); top10 = 100*sum(shares[:10]).
  - voting_gini over the top-N vector via the mean-absolute-difference formula
    (positive convention): gini = sum(|v_i - v_j|) / (2 * n * sum(v)).
  - n_unique_voters = total distinct voters in the window (before top-N truncation).
  - n_sampled = min(100, available).

Re-runnability: pulls live, writes the raw per-voter CSV, prints the computed row.
Run with: python3 voting_hhi_phase3_gno.py
"""

import csv
import os
import sys
import time

import numpy as np
import requests

SNAPSHOT_URL = "https://hub.snapshot.org/graphql"
SPACE = "gnosis.eth"
SYMBOL = "GNO"
SOURCE = "snapshot"

# Window: most recent closed proposals created in roughly the last 18 months.
# We pull a generous batch of recent closed proposals and keep those created
# within the window; proposals with zero votes contribute nothing and are skipped.
MAX_PROPOSALS = 60               # recent closed proposals to scan (orderBy created desc)
WINDOW_MONTHS = 18               # keep proposals created within this many months of the newest
VOTES_PAGE = 1000                # Snapshot caps first at 1000 per votes page
SKIP_CAP = 5000                  # Snapshot caps skip near 5000; vp-desc makes the tail negligible

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_OUT = os.path.join(REPO_ROOT, "data", "raw", "voting_hhi_phase3_gno_raw.csv")


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


def gql(query, variables=None, retries=4):
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    last_err = None
    for attempt in range(retries):
        try:
            r = requests.post(
                SNAPSHOT_URL,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=45,
            )
            if r.status_code == 429:
                time.sleep(2 + attempt * 2)
                continue
            r.raise_for_status()
            data = r.json()
            if "errors" in data and data["errors"]:
                raise RuntimeError(f"GraphQL errors: {data['errors']}")
            return data["data"]
        except Exception as e:  # noqa: BLE001
            last_err = e
            time.sleep(1.5 + attempt * 1.5)
    raise RuntimeError(f"GraphQL request failed after {retries} retries: {last_err}")


def fetch_proposals():
    q = """
    query($space: String!, $first: Int!) {
      proposals(
        first: $first,
        where: {space: $space, state: "closed"},
        orderBy: "created",
        orderDirection: desc
      ) {
        id
        title
        created
        votes
        scores_total
        state
      }
    }
    """
    data = gql(q, {"space": SPACE, "first": MAX_PROPOSALS})
    props = data["proposals"] or []
    if not props:
        return []
    newest = max(p["created"] for p in props)
    window_secs = WINDOW_MONTHS * 30 * 24 * 3600
    cutoff = newest - window_secs
    kept = [p for p in props if p["created"] >= cutoff and (p.get("votes") or 0) > 0]
    return kept


def fetch_votes(proposal_id):
    """Page through all votes for one proposal, vp-desc, until exhausted."""
    out = []
    skip = 0
    q = """
    query($proposal: String!, $first: Int!, $skip: Int!) {
      votes(
        first: $first,
        skip: $skip,
        where: {proposal: $proposal},
        orderBy: "vp",
        orderDirection: desc
      ) {
        voter
        vp
      }
    }
    """
    while True:
        if skip >= SKIP_CAP:
            # vp-desc ordering means the remaining tail past the cap is negligible for HHI.
            break
        data = gql(q, {"proposal": proposal_id, "first": VOTES_PAGE, "skip": skip})
        batch = data["votes"] or []
        for v in batch:
            vp = v.get("vp")
            if vp is None:
                continue
            out.append((v["voter"], float(vp)))
        if len(batch) < VOTES_PAGE:
            break
        skip += VOTES_PAGE
    return out


def main():
    proposals = fetch_proposals()
    if not proposals:
        print("NO_DATA: no closed proposals with votes in the window for", SPACE)
        sys.exit(0)

    # Per-proposal unique-voter counts (turnout context) and per-voter vp aggregation.
    voter_vp = {}              # voter -> total vp summed across sampled proposals
    per_proposal_voters = []   # list of (proposal_id, created, unique_voter_count)

    for p in proposals:
        votes = fetch_votes(p["id"])
        seen = set()
        for voter, vp in votes:
            if vp <= 0:
                continue
            voter_vp[voter] = voter_vp.get(voter, 0.0) + vp
            seen.add(voter)
        per_proposal_voters.append((p["id"], p["created"], len(seen)))

    if not voter_vp:
        print("NO_DATA: no positive-vp votes aggregated for", SPACE)
        sys.exit(0)

    # Full voter-pool vector (before top-N truncation).
    items = sorted(voter_vp.items(), key=lambda kv: kv[1], reverse=True)
    n_unique_voters = len(items)

    # S12 top-N method.
    top_items = items[:100]
    n_sampled = len(top_items)
    top_vals = np.array([vp for _, vp in top_items], dtype=float)

    voting_hhi = compute_hhi(top_vals)
    voting_gini = compute_gini(top_vals)

    shares = top_vals / top_vals.sum()
    voting_top1_pct = float(100 * shares[0])
    voting_top5_pct = float(100 * shares[:5].sum())
    voting_top10_pct = float(100 * shares[:10].sum())

    # Write raw per-voter evidence (full pool, with dominance = share of full-pool total).
    full_total = sum(vp for _, vp in items)
    os.makedirs(os.path.dirname(RAW_OUT), exist_ok=True)
    with open(RAW_OUT, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["rank", "voter", "voting_power", "dominance_full_pool", "in_top_n"])
        for i, (voter, vp) in enumerate(items, start=1):
            w.writerow([
                i,
                voter,
                f"{vp:.10f}",
                f"{(vp / full_total):.10f}" if full_total > 0 else "0",
                "1" if i <= n_sampled else "0",
            ])

    # Turnout context.
    per_prop_counts = [c for _, _, c in per_proposal_voters]
    median_voters = int(np.median(per_prop_counts)) if per_prop_counts else 0
    min_voters = min(per_prop_counts) if per_prop_counts else 0
    max_voters = max(per_prop_counts) if per_prop_counts else 0

    print("=" * 60)
    print(f"TOKEN={SYMBOL}  SOURCE={SOURCE}  SPACE={SPACE}")
    print(f"proposals_sampled (closed, votes>0, in-window) = {len(proposals)}")
    print(f"n_unique_voters (full pool) = {n_unique_voters}")
    print(f"n_sampled (top-N) = {n_sampled}")
    print(f"voting_hhi   = {voting_hhi:.6f}")
    print(f"voting_gini  = {voting_gini:.6f}  (positive convention)")
    print(f"voting_top1_pct  = {voting_top1_pct:.4f}")
    print(f"voting_top5_pct  = {voting_top5_pct:.4f}")
    print(f"voting_top10_pct = {voting_top10_pct:.4f}")
    print(f"turnout: per-proposal unique voters min/median/max = "
          f"{min_voters}/{median_voters}/{max_voters}")
    print(f"raw written -> {RAW_OUT}")
    print("=" * 60)

    return {
        "symbol": SYMBOL,
        "source": SOURCE,
        "voting_hhi": voting_hhi,
        "voting_gini": voting_gini,
        "voting_top1_pct": voting_top1_pct,
        "voting_top5_pct": voting_top5_pct,
        "voting_top10_pct": voting_top10_pct,
        "n_unique_voters": n_unique_voters,
        "n_sampled": n_sampled,
    }


if __name__ == "__main__":
    main()
