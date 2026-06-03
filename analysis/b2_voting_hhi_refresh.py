"""B2 R2 voting HHI comprehensive refresh: full 12-month Snapshot proposals + Tally top-1000 delegates.

Per author "Full comprehensive refresh" directive 2026-05-21.

Outputs:
- /tmp/b2_voting_hhi_refresh_results.csv: refreshed N, HHI, Gini, top1/5/10 per protocol-source
- /tmp/b2_voting_hhi_refresh_comparison.md: side-by-side comparison vs current Table 7

Methodology:
- Snapshot protocols (DIMO, WXM, LDO, COMP, UNI, ARB): pull ALL proposals in 12-month rolling window
  from 2025-05-22 to 2026-05-22; aggregate unique voters across all proposals weighted by max
  voting_power per voter; compute voting HHI from voter-weighted shares.
- Tally protocols (AAVE, COMP, UNI, ARB, OP, ENS, GMX): pull top-1000 delegates via pagination;
  compute voting HHI from delegate voting_power shares.
"""
import os
import sys
import time
import json
import csv
import math
import requests
from collections import defaultdict
from pathlib import Path

SNAPSHOT_API = "https://hub.snapshot.org/graphql"
TALLY_API = "https://api.tally.xyz/query"
TALLY_KEY = os.environ.get("TALLY_KEY", "")
if not TALLY_KEY:
    print("[FATAL] TALLY_KEY not set", file=sys.stderr)
    sys.exit(1)

OUT_CSV = Path("/tmp/b2_voting_hhi_refresh_results.csv")
OUT_MD = Path("/tmp/b2_voting_hhi_refresh_comparison.md")

# 12-month rolling window (start = 2025-05-22; end = 2026-05-22)
WINDOW_START = int(time.mktime(time.strptime("2025-05-22", "%Y-%m-%d")))
WINDOW_END = int(time.mktime(time.strptime("2026-05-22", "%Y-%m-%d")))

SNAPSHOT_SPACES = {
    "UNI":   "uniswapgovernance.eth",
    "COMP":  "comp-vote.eth",
    "LDO":   "lido-snapshot.eth",
    "DIMO":  "dimo.eth",
    "WXM":   "weatherxm.eth",
    "ARB":   "arbitrumfoundation.eth",
}

TALLY_SLUGS = {
    "AAVE":     "aave",
    "COMP":     "compound",
    "UNI":      "uniswap",
    "ARB":      "arbitrum",
    "OP":       "optimism",
    "ENS":      "ens",
    "GMX":      "gmx",
}


def compute_hhi(values):
    total = sum(values)
    if total <= 0:
        return None, None, None, None, None
    shares = sorted([v/total for v in values], reverse=True)
    hhi = sum(s*s for s in shares)
    gini = 2 * sum((i + 0.5) * s for i, s in enumerate(reversed(shares))) / len(shares) - 1
    top1 = sum(shares[:1]) * 100
    top5 = sum(shares[:5]) * 100
    top10 = sum(shares[:10]) * 100
    return hhi, gini, top1, top5, top10


def snapshot_pull_proposals(space):
    """Pull all proposals from 12-month rolling window."""
    proposals = []
    skip = 0
    page_size = 100
    while True:
        query = """
        query ($space: String!, $start: Int!, $end: Int!, $skip: Int!) {
            proposals(
                first: 100, skip: $skip,
                where: { space: $space, created_gte: $start, created_lte: $end, state: "closed" },
                orderBy: "created", orderDirection: desc
            ) {
                id
                title
                created
                end
            }
        }
        """
        vars = {"space": space, "start": WINDOW_START, "end": WINDOW_END, "skip": skip}
        r = requests.post(SNAPSHOT_API, json={"query": query, "variables": vars}, timeout=30)
        data = r.json().get("data", {}).get("proposals", [])
        if not data:
            break
        proposals.extend(data)
        if len(data) < page_size:
            break
        skip += page_size
        time.sleep(0.3)
    return proposals


def snapshot_pull_votes(proposal_id):
    """Pull all votes for a single proposal."""
    votes = []
    skip = 0
    page_size = 1000
    while True:
        query = """
        query ($proposal: String!, $skip: Int!) {
            votes(
                first: 1000, skip: $skip,
                where: { proposal: $proposal },
                orderBy: "vp", orderDirection: desc
            ) {
                voter
                vp
                choice
            }
        }
        """
        vars = {"proposal": proposal_id, "skip": skip}
        r = requests.post(SNAPSHOT_API, json={"query": query, "variables": vars}, timeout=30)
        data = r.json().get("data", {}).get("votes", [])
        if not data:
            break
        votes.extend(data)
        if len(data) < page_size:
            break
        skip += page_size
        time.sleep(0.2)
    return votes


def snapshot_refresh(symbol, space):
    """Refresh Snapshot voting HHI for a protocol."""
    print(f"[snapshot] {symbol} ({space})... ", end="", flush=True)
    proposals = snapshot_pull_proposals(space)
    print(f"{len(proposals)} proposals found", flush=True)
    # Aggregate unique voters; use max(vp) per voter across all proposals
    voter_max_vp = {}
    for p in proposals:
        votes = snapshot_pull_votes(p["id"])
        for v in votes:
            voter = v["voter"]
            vp = float(v.get("vp", 0) or 0)
            if vp > 0:
                voter_max_vp[voter] = max(voter_max_vp.get(voter, 0), vp)
        print(f"  proposal {p['id'][:10]}... {len(votes)} votes; running unique voters = {len(voter_max_vp)}", flush=True)
        time.sleep(0.2)
    values = sorted(voter_max_vp.values(), reverse=True)
    hhi, gini, top1, top5, top10 = compute_hhi(values)
    n = len(values)
    return {
        "symbol": symbol,
        "source": "snapshot",
        "n_unique_voters": n,
        "n_proposals": len(proposals),
        "voting_hhi": hhi,
        "voting_gini": gini,
        "voting_top1_pct": top1,
        "voting_top5_pct": top5,
        "voting_top10_pct": top10,
    }


def tally_pull_delegates(slug, target_n=1000):
    """Pull top-N delegates from Tally via pagination."""
    delegates = []
    after = None
    page_size = 100
    while len(delegates) < target_n:
        query = """
        query DelegatesV2($input: DelegatesInput!) {
            delegates(input: $input) {
                nodes {
                    ... on Delegate {
                        id
                        votesCount
                        delegatorsCount
                        account { address ens name }
                    }
                }
                pageInfo { lastCursor }
            }
        }
        """
        input_vars = {"input": {
            "filters": {"organizationSlug": slug},
            "sort": {"isDescending": True, "sortBy": "votes"},
            "page": {"limit": page_size, "afterCursor": after} if after else {"limit": page_size}
        }}
        r = requests.post(TALLY_API, json={"query": query, "variables": input_vars},
                          headers={"Api-Key": TALLY_KEY, "Content-Type": "application/json"}, timeout=30)
        if r.status_code != 200:
            print(f"  [HTTP {r.status_code}] {r.text[:200]}")
            break
        result = r.json()
        if "errors" in result:
            print(f"  [GraphQL errors] {result['errors'][:1]}")
            break
        data = result.get("data", {}).get("delegates", {})
        nodes = data.get("nodes", [])
        if not nodes:
            break
        delegates.extend(nodes)
        page_info = data.get("pageInfo", {})
        after = page_info.get("lastCursor")
        if not after:
            break
        time.sleep(0.3)
        if len(delegates) >= target_n:
            break
    return delegates[:target_n]


def tally_refresh(symbol, slug):
    """Refresh Tally voting HHI for a protocol with top-1000."""
    print(f"[tally] {symbol} ({slug})... ", end="", flush=True)
    delegates = tally_pull_delegates(slug, target_n=1000)
    print(f"{len(delegates)} delegates pulled", flush=True)
    values = []
    for d in delegates:
        try:
            vc = float(d.get("votesCount", 0) or 0)
            if vc > 0:
                values.append(vc)
        except (ValueError, TypeError):
            pass
    hhi, gini, top1, top5, top10 = compute_hhi(values)
    return {
        "symbol": symbol,
        "source": "tally",
        "n_unique_voters": len(values),
        "n_proposals": None,
        "voting_hhi": hhi,
        "voting_gini": gini,
        "voting_top1_pct": top1,
        "voting_top5_pct": top5,
        "voting_top10_pct": top10,
    }


def main():
    results = []
    # Snapshot side
    print("=== Snapshot refresh (all 12-month proposals) ===")
    for symbol, space in SNAPSHOT_SPACES.items():
        try:
            r = snapshot_refresh(symbol, space)
            results.append(r)
            print(f"  RESULT {symbol}: N={r['n_unique_voters']}, HHI={r['voting_hhi']:.4f}, Gini={r['voting_gini']:.4f}")
        except Exception as e:
            print(f"  ERROR {symbol}: {e}")
    print()
    # Tally side
    print("=== Tally refresh (top-1000 delegates) ===")
    for symbol, slug in TALLY_SLUGS.items():
        try:
            r = tally_refresh(symbol, slug)
            results.append(r)
            print(f"  RESULT {symbol}: N={r['n_unique_voters']}, HHI={r['voting_hhi']:.4f}, Gini={r['voting_gini']:.4f}" if r['voting_hhi'] else f"  RESULT {symbol}: NO DATA")
        except Exception as e:
            print(f"  ERROR {symbol}: {e}")
    print()

    # Write CSV
    if results:
        with open(OUT_CSV, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
        print(f"\n[WRITTEN] {OUT_CSV}")


if __name__ == "__main__":
    main()
