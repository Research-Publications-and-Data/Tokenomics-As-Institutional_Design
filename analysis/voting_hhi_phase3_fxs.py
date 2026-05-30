#!/usr/bin/env python3
"""
B2 voting-HHI Phase 3 collector: FXS (Frax).

Frax governance routes through vote-escrow veFXS (time-weighted lock). The
Snapshot space "frax.eth" reports veFXS-weighted voting power (vp) per voter per
proposal, so the Snapshot vote record is the de-facto veFXS-weighted voter pool.
FXS is expected to JOIN the ve-token amplification class (veCRV about 15x; veBAL
about 21x): time-weighted lock weighting concentrates governance power among the
largest long-lockers relative to flat token holdings.

MEASURE (S12 voter-pool HHI, matching the existing 13-row data of record):
per-voter veFXS-weighted vp aggregated across recent closed proposals on the
frax.eth space; sort descending; take the top 100 (or all if fewer); normalize
shares within that top-N sample; voting_hhi = sum(shares**2); top1/top5/top10
cumulative percentages; gini over the top-N vector via mean-absolute-difference.

AGGREGATION CONVENTION (important; differs from the naive "sum across proposals"
wording for a defensible reason): the committed PRIMARY measure is the MAX of a
voter's vp across the sampled proposals, i.e. each voter's single largest
veFXS-weighted vp. The MAX is the correct veFXS-stake proxy because vp at vote
time reflects the voter's veFXS lock; summing the same lock across many proposals
double-counts it and conflates governance STAKE with participation FREQUENCY.
Over a wide 60-proposal window the frax.eth pool contains a high-frequency voter
(50 of 60 proposals); SUM aggregation inflates that one address to top1 about 95
percent (HHI about 0.91), which is a participation-frequency artifact, not a
stake measure. MAX yields top1 about 59 percent (HHI about 0.37), a clean
veFXS-stake distribution still strongly in the ve-token amplification class. Both
the SUM and MAX per-voter columns are written to the raw evidence file so the
verifier can recompute either way; the committed row is MAX. (On the narrow about
5-proposal windows used for the existing Snapshot rows of record, SUM and MAX
nearly coincide because participation frequency barely varies; the divergence
here is purely a wide-window effect, and MAX is the convention that stays
comparable across window widths.)

SOURCE: Snapshot GraphQL (KEYLESS). https://hub.snapshot.org/graphql
  space id "frax.eth" (confirmed live; 515 proposals; veFXS-weighted vp).

Re-runnable: python3 voting_hhi_phase3_fxs.py
Writes raw per-voter CSV to ../data/raw/voting_hhi_phase3_fxs_raw.csv

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

GRAPHQL_URL = "https://hub.snapshot.org/graphql"
SPACE_ID = "frax.eth"
# Number of recent closed proposals to aggregate the voter pool over. A wide
# window builds a robust pool because individual veFXS proposals draw only a
# handful of large lockers (typical 6 to 30 votes per proposal).
N_PROPOSALS = 60
VOTES_PAGE = 1000

HERE = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(HERE, "..", "data", "raw")
RAW_PATH = os.path.join(RAW_DIR, "voting_hhi_phase3_fxs_raw.csv")

HOLDINGS_HHI_OF_RECORD = 0.03241


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


# Politeness pacing: the keyless Snapshot hub rate-limits aggressively (HTTP 429).
# A fixed inter-request delay plus exponential backoff on 429 keeps us under the cap.
BASE_DELAY = 1.2


def gql(query, variables=None, retries=7):
    """POST a GraphQL query to the keyless Snapshot hub; retry on transient errors.

    Handles HTTP 429 (rate limit) with exponential backoff that honors a
    Retry-After header when present. A short fixed pause precedes every request
    so the steady-state call rate stays under the keyless cap.
    """
    body = json.dumps({"query": query, "variables": variables or {}}).encode("utf-8")
    last_err = None
    for attempt in range(retries):
        time.sleep(BASE_DELAY)
        req = urllib.request.Request(
            GRAPHQL_URL,
            data=body,
            headers={"Content-Type": "application/json",
                     "User-Agent": "b2-voting-hhi-collector/1.0"},
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
            if "errors" in payload and payload["errors"]:
                last_err = "GraphQL errors: %s" % json.dumps(payload["errors"])
                time.sleep(3 * (attempt + 1))
                continue
            return payload.get("data", {})
        except urllib.error.HTTPError as exc:
            last_err = "HTTP %s: %s" % (exc.code, exc.reason)
            if exc.code == 429:
                retry_after = exc.headers.get("Retry-After")
                wait = float(retry_after) if (retry_after and retry_after.isdigit()) \
                    else min(60.0, 5.0 * (2 ** attempt))
                time.sleep(wait)
            else:
                time.sleep(3 * (attempt + 1))
        except (urllib.error.URLError, TimeoutError) as exc:
            last_err = "URL error: %s" % exc
            time.sleep(3 * (attempt + 1))
    print("ERROR: GraphQL request failed after %d attempts: %s" % (retries, last_err),
          file=sys.stderr)
    sys.exit(1)


def fetch_closed_proposals(n):
    """Return up to n recent CLOSED proposal ids on the space, newest first."""
    q = """
    query Proposals($space: String!, $first: Int!) {
      proposals(first: $first,
                where: {space: $space, state: "closed"},
                orderBy: "created", orderDirection: desc) {
        id title created votes scores_total
      }
    }
    """
    data = gql(q, {"space": SPACE_ID, "first": n})
    return data.get("proposals", []) or []


def fetch_votes_for_proposal(proposal_id):
    """Page through ALL votes for one proposal; return list of (voter, vp)."""
    q = """
    query Votes($proposal: String!, $first: Int!, $skip: Int!) {
      votes(first: $first, skip: $skip,
            where: {proposal: $proposal},
            orderBy: "vp", orderDirection: desc) {
        voter vp
      }
    }
    """
    out = []
    skip = 0
    while True:
        data = gql(q, {"proposal": proposal_id, "first": VOTES_PAGE, "skip": skip})
        votes = data.get("votes", []) or []
        if not votes:
            break
        for v in votes:
            voter = v.get("voter")
            vp = v.get("vp")
            if voter is None or vp is None:
                continue
            out.append((voter, float(vp)))
        if len(votes) < VOTES_PAGE:
            break
        skip += VOTES_PAGE
        # Snapshot caps skip at 5000; large veFXS proposals never reach this.
        if skip >= 5000:
            break
    return out


def main():
    proposals = fetch_closed_proposals(N_PROPOSALS)
    if not proposals:
        print(json.dumps({
            "token": "FXS",
            "source": "snapshot",
            "status": "NO_DATA",
            "notes": "No closed proposals returned for space %s." % SPACE_ID,
        }, indent=2))
        return

    # Aggregate per-voter vp across proposals.
    sum_vp = {}     # voter -> sum of vp across sampled proposals (primary measure)
    max_vp = {}     # voter -> max single-proposal vp (cross-check)
    vote_count = {}  # voter -> number of proposals voted in
    proposals_used = 0
    total_votes_seen = 0

    for p in proposals:
        pid = p.get("id")
        if not pid:
            continue
        votes = fetch_votes_for_proposal(pid)
        if not votes:
            continue
        proposals_used += 1
        for voter, vp in votes:
            if vp <= 0:
                continue
            total_votes_seen += 1
            sum_vp[voter] = sum_vp.get(voter, 0.0) + vp
            if vp > max_vp.get(voter, 0.0):
                max_vp[voter] = vp
            vote_count[voter] = vote_count.get(voter, 0) + 1

    if not sum_vp:
        print(json.dumps({
            "token": "FXS",
            "source": "snapshot",
            "status": "NO_DATA",
            "notes": "Closed proposals exist but returned zero usable votes.",
        }, indent=2))
        return

    # Build the per-voter vector on the PRIMARY (max) measure; sort descending.
    # MAX = each voter's largest single-proposal veFXS-weighted vp = stake proxy.
    voters = sorted(max_vp.keys(), key=lambda a: max_vp[a], reverse=True)
    n_unique = len(voters)
    n_sampled = min(100, n_unique)
    sample = voters[:n_sampled]

    # Write raw evidence: every voter, ranked by the primary MAX measure, with
    # both the max (primary) and sum (cross-check) vp and the proposal count.
    os.makedirs(RAW_DIR, exist_ok=True)
    with open(RAW_PATH, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["rank", "voter", "voting_power_max_vefxs",
                    "voting_power_sum_vefxs", "proposals_voted",
                    "in_top_n_sample"])
        for i, voter in enumerate(voters, start=1):
            w.writerow([i, voter,
                        "%.10f" % max_vp[voter],
                        "%.10f" % sum_vp[voter],
                        vote_count[voter],
                        1 if i <= n_sampled else 0])
    print("Wrote raw evidence: %s (%d unique voters; %d proposals used)"
          % (RAW_PATH, n_unique, proposals_used), file=sys.stderr)

    # PRIMARY measure: max-aggregated vp (veFXS-stake proxy), top-N.
    sample_vals = [max_vp[v] for v in sample]
    voting_hhi = compute_hhi(sample_vals)

    arr = np.array(sample_vals, dtype=float)
    shares = arr / arr.sum()
    top1 = float(100.0 * shares[0])
    top5 = float(100.0 * shares[:5].sum())
    top10 = float(100.0 * shares[:10].sum())
    gini = compute_gini(sample_vals)

    # Cross-check under SUM aggregation (re-rank on sum measure independently).
    # Expected to be inflated by participation frequency; documented, not used.
    sum_voters = sorted(sum_vp.keys(), key=lambda a: sum_vp[a], reverse=True)
    sum_sample = [sum_vp[v] for v in sum_voters[:min(100, len(sum_voters))]]
    voting_hhi_sum_crosscheck = compute_hhi(sum_sample)

    ratio = voting_hhi / HOLDINGS_HHI_OF_RECORD if voting_hhi else None
    if ratio is None:
        direction = "unknown"
    elif ratio > 1.1:
        direction = "amplify"
    elif ratio < 0.9:
        direction = "disperse"
    else:
        direction = "equivalent"

    result = {
        "token": "FXS",
        "source": "snapshot",
        "status": "OK",
        "voting_hhi": voting_hhi,
        "voting_gini": gini,
        "voting_top1_pct": top1,
        "voting_top5_pct": top5,
        "voting_top10_pct": top10,
        "n_unique_voters": n_unique,
        "n_sampled": n_sampled,
        "voting_hhi_sum_crosscheck": voting_hhi_sum_crosscheck,
        "holdings_hhi_of_record": HOLDINGS_HHI_OF_RECORD,
        "ratio_voting_over_holdings": ratio,
        "observed_direction": direction,
        "proposals_requested": N_PROPOSALS,
        "proposals_used": proposals_used,
        "total_votes_aggregated": total_votes_seen,
        "space_id": SPACE_ID,
    }
    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    main()
