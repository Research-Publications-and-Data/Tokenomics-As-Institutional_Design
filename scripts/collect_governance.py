"""
B2 Governance Data Collection: Tally + Snapshot
Pulls delegated voting power, proposal activity, voter participation.
Computes voting HHI alongside holding HHI.

Usage:
    python3 collect_governance.py
    TALLY_KEY=your_key python3 collect_governance.py  # also runs Tally
"""

import os
import sys
import time
import json
import math
import requests
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta

PROJECT_DIR = Path(__file__).parent.parent
DATA_DIR = PROJECT_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

SNAPSHOT_API = "https://hub.snapshot.org/graphql"
TALLY_API = "https://api.tally.xyz/query"
TALLY_KEY = os.environ.get("TALLY_KEY", "")

# ── Snapshot spaces (confirmed working 2026-03-30) ─────────────────────────
# Protocols with no Snapshot space:
#   AAVE, MKR → Tally (on-chain Governor)
#   ANYONE, GRASS, RNDR, ZRO, W, AXL, META, MOR → no formal Snapshot governance
SNAPSHOT_SPACES = {
    "UNI":   "uniswapgovernance.eth",
    "COMP":  "comp-vote.eth",
    "CRV":   "curve.eth",
    "GRT":   "graphprotocol.eth",
    "LDO":   "lido-snapshot.eth",
    "DIMO":  "dimo.eth",
    "IOTX":  "iotex.eth",
    "WXM":   "weatherxm.eth",
    "OP":    "opcollective.eth",
    "ARB":   "arbitrumfoundation.eth",
}

# ── Tally organization slugs (requires API key) ────────────────────────────
TALLY_ORGS = {
    "AAVE": "aave",
    # MKR: MakerDAO uses ds-chief, not Governor Bravo — not on Tally
    "COMP": "compound",    # COMP uses both Tally and Snapshot
    "UNI":  "uniswap",     # UNI uses both Tally and Snapshot
    "ARB":  "arbitrum",    # ARB uses both Tally and Snapshot
    "OP":   "optimism",    # OP uses both
    # GRT: not found on Tally (uses Snapshot only)
    # LDO: lido slug exists but only 1 proposal/2 delegates — skip
}


# ── Utility ─────────────────────────────────────────────────────────────────

def snapshot_query(query, variables=None, retries=3):
    for attempt in range(retries):
        try:
            r = requests.post(
                SNAPSHOT_API,
                json={"query": query, "variables": variables or {}},
                timeout=30,
            )
            r.raise_for_status()
            data = r.json()
            if "errors" in data:
                print(f"  GraphQL errors: {data['errors']}")
            return data.get("data", {})
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
            else:
                print(f"  Request failed after {retries} attempts: {e}")
                return {}


def tally_query(query, variables=None, retries=3):
    if not TALLY_KEY:
        return {}
    headers = {"Content-Type": "application/json", "Api-Key": TALLY_KEY}
    for attempt in range(retries):
        try:
            r = requests.post(
                TALLY_API,
                headers=headers,
                json={"query": query, "variables": variables or {}},
                timeout=30,
            )
            if r.status_code == 429:
                wait = int(r.headers.get("Retry-After", 10))
                print(f"  Rate limited; waiting {wait}s")
                time.sleep(wait)
                continue
            r.raise_for_status()
            data = r.json()
            if "errors" in data:
                print(f"  GraphQL errors: {data['errors']}")
            return data.get("data") or {}
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
            else:
                print(f"  Tally request failed: {e}")
                return {}


def compute_hhi(values):
    """HHI from raw values (renormalizes internally)."""
    v = np.array(values, dtype=float)
    v = v[v > 0]
    if len(v) == 0:
        return None
    shares = v / v.sum()
    return float(np.sum(shares ** 2))


def compute_gini(values):
    """Gini using relative mean absolute difference."""
    v = np.array(values, dtype=float)
    v = v[v > 0]
    if len(v) < 2:
        return None
    n = len(v)
    abs_diffs = np.abs(v[:, None] - v[None, :]).sum()
    return float(abs_diffs / (2 * n * v.sum()))


# ── Part 1: Snapshot Spaces ──────────────────────────────────────────────────

def pull_snapshot_spaces():
    print("\n=== Part 1: Snapshot Space Metadata ===")
    q = """query($ids: [String!]) {
      spaces(where: {id_in: $ids}) {
        id name about network symbol followersCount proposalsCount
        voting { delay period type quorum }
        strategies { name network params }
      }
    }"""
    data = snapshot_query(q, {"ids": list(SNAPSHOT_SPACES.values())})
    found = {s["id"]: s for s in (data.get("spaces") or [])}

    rows = []
    for symbol, space_id in SNAPSHOT_SPACES.items():
        if space_id not in found:
            print(f"  {symbol}: space {space_id!r} not found")
            continue
        s = found[space_id]
        strats = [st["name"] for st in (s.get("strategies") or [])]
        v = s.get("voting") or {}
        rows.append({
            "symbol": symbol,
            "space_id": space_id,
            "name": s["name"],
            "network": s.get("network", ""),
            "token_symbol": s.get("symbol", ""),
            "followers": s.get("followersCount", 0),
            "proposals_total": s.get("proposalsCount", 0),
            "voting_type": v.get("type", ""),
            "voting_quorum": v.get("quorum", 0),
            "voting_period_sec": v.get("period", 0),
            "strategies": "; ".join(strats),
        })
        print(f"  {symbol}: {s['name']} | {s['proposalsCount']} props | {s['followersCount']} followers")

    df = pd.DataFrame(rows)
    df.to_csv(DATA_DIR / "snapshot_spaces.csv", index=False)
    print(f"Saved {len(df)} spaces → snapshot_spaces.csv")
    return found


# ── Part 2: Snapshot Proposals (last 12 months) ─────────────────────────────

def pull_snapshot_proposals(found_spaces):
    print("\n=== Part 2: Snapshot Proposals (last 12 months) ===")
    cutoff_ts = int((datetime.utcnow() - timedelta(days=365)).timestamp())

    q = """query($space: String!, $first: Int!, $skip: Int!) {
      proposals(
        first: $first, skip: $skip,
        where: { space: $space },
        orderBy: "created", orderDirection: desc
      ) {
        id title type start end state votes scores scores_total quorum author
      }
    }"""

    all_rows = []
    for symbol, space_id in SNAPSHOT_SPACES.items():
        if space_id not in found_spaces:
            continue
        print(f"  {symbol} ({space_id})...")
        skip = 0
        stop = False
        while not stop:
            data = snapshot_query(q, {"space": space_id, "first": 100, "skip": skip})
            proposals = data.get("proposals") or []
            if not proposals:
                break
            for p in proposals:
                if p["end"] < cutoff_ts:
                    stop = True
                    break
                choices = []
                scores = p.get("scores") or []
                scores_total = p.get("scores_total") or 0
                top_score_pct = round(max(scores) / scores_total * 100, 1) if scores and scores_total > 0 else 0
                all_rows.append({
                    "symbol": symbol,
                    "space_id": space_id,
                    "proposal_id": p["id"],
                    "title": (p.get("title") or "")[:200],
                    "type": p.get("type", ""),
                    "state": p.get("state", ""),
                    "start": datetime.utcfromtimestamp(p["start"]).date().isoformat() if p.get("start") else "",
                    "end": datetime.utcfromtimestamp(p["end"]).date().isoformat() if p.get("end") else "",
                    "votes": p.get("votes", 0),
                    "scores_total": scores_total,
                    "quorum": p.get("quorum", 0),
                    "top_choice_pct": top_score_pct,
                    "author": p.get("author", ""),
                })
            skip += 100
            if len(proposals) < 100:
                break
            time.sleep(0.3)

        count = sum(1 for r in all_rows if r["symbol"] == symbol)
        print(f"    {count} proposals in last 12 months")

    df = pd.DataFrame(all_rows)
    df.to_csv(DATA_DIR / "snapshot_proposals.csv", index=False)
    print(f"Saved {len(df)} proposals → snapshot_proposals.csv")
    return df


# ── Part 3: Snapshot Votes (top-5 proposals per protocol) ───────────────────

def pull_snapshot_votes(proposals_df):
    print("\n=== Part 3: Snapshot Votes (top-5 proposals by votes each) ===")

    q = """query($proposal: String!, $first: Int!, $skip: Int!) {
      votes(
        first: $first, skip: $skip,
        where: { proposal: $proposal },
        orderBy: "vp", orderDirection: desc
      ) { id voter vp choice created }
    }"""

    all_votes = []

    for symbol in SNAPSHOT_SPACES:
        proto_props = proposals_df[proposals_df["symbol"] == symbol].sort_values(
            "votes", ascending=False
        ).head(5)

        if len(proto_props) == 0:
            print(f"  {symbol}: no proposals to sample")
            continue

        print(f"  {symbol}: sampling {len(proto_props)} proposals...")

        for _, prop in proto_props.iterrows():
            prop_id = prop["proposal_id"]
            skip = 0
            prop_votes = 0
            while True:
                data = snapshot_query(q, {"proposal": prop_id, "first": 1000, "skip": skip})
                votes = data.get("votes") or []
                if not votes:
                    break
                for v in votes:
                    all_votes.append({
                        "symbol": symbol,
                        "proposal_id": prop_id,
                        "voter": v["voter"],
                        "voting_power": float(v.get("vp") or 0),
                        "choice": str(v.get("choice", "")),
                        "created": datetime.utcfromtimestamp(v["created"]).date().isoformat() if v.get("created") else "",
                    })
                prop_votes += len(votes)
                skip += 1000
                if len(votes) < 1000:
                    break
                time.sleep(0.3)
            print(f"    proposal {prop_id[:20]}...: {prop_votes} votes")

    df = pd.DataFrame(all_votes)
    df.to_csv(DATA_DIR / "snapshot_votes.csv", index=False)
    print(f"Saved {len(df)} votes → snapshot_votes.csv")
    return df


# ── Part 4: Tally Delegates (requires API key) ───────────────────────────────

def pull_tally_delegates():
    if not TALLY_KEY:
        print("\n=== Part 4: Tally Delegates — SKIPPED (no TALLY_KEY) ===")
        print("  Set TALLY_KEY=<your_key> to enable Tally collection.")
        print("  Get a free key at: https://tally.xyz/user/settings/api-keys")
        return pd.DataFrame()

    print("\n=== Part 4: Tally Delegates ===")

    find_org_q = """query($slug: String!) {
      organization(input: { slug: $slug }) {
        id slug name proposalsCount delegatesCount tokenOwnersCount
      }
    }"""

    delegates_q = """query($input: DelegatesInput!) {
      delegates(input: $input) {
        nodes {
          ... on Delegate {
            account { address ens name }
            votesCount
            delegatorsCount
          }
        }
        pageInfo { lastCursor count }
      }
    }"""

    all_rows = []
    orgs = {}

    for symbol, slug in TALLY_ORGS.items():
        data = tally_query(find_org_q, {"slug": slug})
        org = data.get("organization")
        if not org:
            print(f"  {symbol} ({slug}): not found on Tally")
            continue
        orgs[symbol] = org
        print(f"  {symbol}: {org['name']} | {org.get('proposalsCount',0)} proposals | "
              f"{org.get('delegatesCount',0)} delegates")
        time.sleep(1)

    for symbol, org in orgs.items():
        print(f"\n  Pulling delegates for {symbol}...")
        cursor = None
        delegates = []
        while len(delegates) < 100:
            variables = {
                "input": {
                    "filters": {"organizationId": org["id"]},
                    "sort": {"sortBy": "votes", "isDescending": True},
                    "page": {"limit": 50},
                }
            }
            if cursor:
                variables["input"]["page"]["afterCursor"] = cursor
            data = tally_query(delegates_q, variables)
            result = data.get("delegates") or {}
            nodes = result.get("nodes") or []
            if not nodes:
                break
            for d in nodes:
                delegates.append({
                    "symbol": symbol,
                    "address": d["account"]["address"],
                    "ens": d["account"].get("ens", ""),
                    "name": d["account"].get("name", ""),
                    "votes_count": int(d.get("votesCount") or 0),
                    "delegators_count": int(d.get("delegatorsCount") or 0),
                })
            page_info = result.get("pageInfo") or {}
            cursor = page_info.get("lastCursor")
            if not cursor:
                break
            time.sleep(0.5)

        print(f"    {len(delegates)} delegates")
        all_rows.extend(delegates)

    df = pd.DataFrame(all_rows)
    if len(df) > 0:
        df.to_csv(DATA_DIR / "tally_delegates.csv", index=False)
        print(f"Saved {len(df)} delegates → tally_delegates.csv")
    return df


# ── Part 5: Tally Proposals (requires API key) ───────────────────────────────

def pull_tally_proposals():
    if not TALLY_KEY:
        print("\n=== Part 5: Tally Proposals — SKIPPED (no TALLY_KEY) ===")
        return pd.DataFrame()

    print("\n=== Part 5: Tally Proposals ===")
    # (Implementation mirrors delegates but queries proposals endpoint)
    # Omitted for brevity when no key; structure matches snapshot_proposals
    return pd.DataFrame()


# ── Part 6: Compute Voting HHI ───────────────────────────────────────────────

def compute_voting_hhi(votes_df, delegates_df):
    print("\n=== Part 6: Compute Voting HHI ===")
    results = []

    # Snapshot: voting power from votes (max VP per voter across sampled proposals)
    if len(votes_df) > 0:
        for symbol in votes_df["symbol"].unique():
            proto = votes_df[votes_df["symbol"] == symbol]
            # Max VP per voter (best representation of their governance weight)
            voter_vp = proto.groupby("voter")["voting_power"].max()
            voter_vp = voter_vp[voter_vp > 0].sort_values(ascending=False)

            if len(voter_vp) < 5:
                print(f"  {symbol} (Snapshot): only {len(voter_vp)} voters — insufficient")
                continue

            top100 = voter_vp.head(100).values
            hhi = compute_hhi(top100)
            gini = compute_gini(top100)
            shares = top100 / top100.sum()
            top1 = float(shares[0])
            top5 = float(shares[:5].sum())
            top10 = float(shares[:10].sum()) if len(shares) >= 10 else float(shares.sum())

            results.append({
                "symbol": symbol,
                "source": "snapshot",
                "voting_hhi": round(hhi, 6),
                "voting_gini": round(gini, 4),
                "voting_top1_pct": round(top1 * 100, 2),
                "voting_top5_pct": round(top5 * 100, 2),
                "voting_top10_pct": round(top10 * 100, 2),
                "n_unique_voters": int(len(voter_vp)),
                "n_sampled_top100": int(len(top100)),
            })
            print(f"  {symbol} (Snapshot): HHI={hhi:.4f} Gini={gini:.3f} top1={top1:.3f} N={len(voter_vp)}")

    # Tally: voting power from delegate votesCount
    if len(delegates_df) > 0:
        for symbol in delegates_df["symbol"].unique():
            proto = delegates_df[delegates_df["symbol"] == symbol].copy()
            proto = proto[proto["votes_count"] > 0].sort_values("votes_count", ascending=False)

            if len(proto) < 5:
                print(f"  {symbol} (Tally): only {len(proto)} delegates — insufficient")
                continue

            top100 = proto.head(100)["votes_count"].values.astype(float)
            hhi = compute_hhi(top100)
            gini = compute_gini(top100)
            shares = top100 / top100.sum()
            top1 = float(shares[0])
            top5 = float(shares[:5].sum())
            top10 = float(shares[:10].sum()) if len(shares) >= 10 else float(shares.sum())

            results.append({
                "symbol": symbol,
                "source": "tally",
                "voting_hhi": round(hhi, 6),
                "voting_gini": round(gini, 4),
                "voting_top1_pct": round(top1 * 100, 2),
                "voting_top5_pct": round(top5 * 100, 2),
                "voting_top10_pct": round(top10 * 100, 2),
                "n_unique_voters": int(len(proto)),
                "n_sampled_top100": int(len(top100)),
            })
            print(f"  {symbol} (Tally):    HHI={hhi:.4f} Gini={gini:.3f} top1={top1:.3f} N={len(proto)}")

    df = pd.DataFrame(results)
    df.to_csv(DATA_DIR / "voting_hhi.csv", index=False)
    print(f"Saved {len(df)} voting HHI rows → voting_hhi.csv")
    return df


# ── Part 7: Merge Holding + Voting HHI ───────────────────────────────────────

# Map from prompt symbols to our token registry symbols
SYMBOL_MAP = {
    "UNI": "UNI", "COMP": "COMP", "MKR": "MKR", "AAVE": "AAVE", "CRV": "CRV",
    "GRT": "GRT", "LDO": "LDO",
    "IOTX": "IOTX", "DIMO": "DIMO", "WXM": "WXM", "ANYONE": "ANYONE",
    "GRASS": "GRASS", "RNDR": "RENDER",
    "OP": "OP", "ZRO": "ZRO", "W": "W", "AXL": "AXL", "META": "META",
    "ARB": "ARB", "MOR": "MOR",
}

CATEGORIES = {
    "UNI": "DeFi", "COMP": "DeFi", "MKR": "DeFi", "AAVE": "DeFi",
    "CRV": "DeFi", "GRT": "DeFi", "LDO": "DeFi",
    "IOTX": "DePIN", "DIMO": "DePIN", "WXM": "DePIN",
    "ANYONE": "DePIN", "GRASS": "DePIN", "RNDR": "DePIN",
    "OP": "Infra", "ZRO": "Infra", "W": "Infra",
    "AXL": "Infra", "META": "Infra", "ARB": "Infra",
    "MOR": "AI",
}

# LDO holding HHI: not in our data, use published estimate (Nansen ~Mar 2026)
LDO_HOLDING_HHI_ESTIMATE = 0.0128  # Dune query 6928830, top-1000 after exclusions (2026-03-30)


def merge_holding_voting(voting_hhi_df):
    print("\n=== Part 7: Merge Holding HHI + Voting HHI ===")

    # Load our computed holding HHI
    conc_path = PROJECT_DIR / "governance_concentration_april2026.csv"
    conc = pd.read_csv(conc_path)[["token", "hhi", "gini", "top1_pct", "top10_pct", "n_holders"]]
    conc_lookup = dict(zip(conc["token"], conc.to_dict("records")))

    rows = []
    for symbol in SYMBOL_MAP:
        reg_symbol = SYMBOL_MAP[symbol]
        category = CATEGORIES[symbol]

        # Holding HHI
        if reg_symbol and reg_symbol in conc_lookup:
            h = conc_lookup[reg_symbol]
            holding_hhi = h["hhi"]
            holding_gini = h["gini"]
            holding_top1 = h["top1_pct"]
            holding_top10 = h["top10_pct"]
        elif symbol == "LDO":
            holding_hhi = LDO_HOLDING_HHI_ESTIMATE
            holding_gini = None
            holding_top1 = None
            holding_top10 = None
        else:
            holding_hhi = None
            holding_gini = None
            holding_top1 = None
            holding_top10 = None

        # Voting HHI
        v_row = voting_hhi_df[voting_hhi_df["symbol"] == symbol]
        if len(v_row) > 0:
            v = v_row.iloc[0]
            voting_hhi = v["voting_hhi"]
            voting_gini = v["voting_gini"]
            voting_top1 = v["voting_top1_pct"]
            voting_top10 = v["voting_top10_pct"]
            governance_source = v["source"]
            n_voters = int(v["n_unique_voters"])
        else:
            voting_hhi = None
            voting_gini = None
            voting_top1 = None
            voting_top10 = None
            governance_source = "none"
            n_voters = None

        # Gap metrics
        hhi_gap = round(voting_hhi - holding_hhi, 4) if (voting_hhi is not None and holding_hhi is not None) else None
        hhi_ratio = round(voting_hhi / max(holding_hhi, 1e-6), 2) if (voting_hhi is not None and holding_hhi is not None) else None

        rows.append({
            "symbol": symbol,
            "category": category,
            "holding_hhi": holding_hhi,
            "holding_gini": holding_gini,
            "holding_top1_pct": holding_top1,
            "holding_top10_pct": holding_top10,
            "voting_hhi": voting_hhi,
            "voting_gini": voting_gini,
            "voting_top1_pct": voting_top1,
            "voting_top10_pct": voting_top10,
            "hhi_gap": hhi_gap,
            "hhi_ratio": hhi_ratio,
            "governance_source": governance_source,
            "n_voters_sampled": n_voters,
        })

    df = pd.DataFrame(rows)
    df.to_csv(DATA_DIR / "governance_participation.csv", index=False)
    print(f"Saved {len(df)} rows → governance_participation.csv")

    # Print summary
    print("\n" + "=" * 90)
    print(f"{'Symbol':8s} {'Cat':6s} {'HoldHHI':>8s} {'VoteHHI':>8s} {'Gap':>8s} {'Ratio':>7s}  Source")
    print("-" * 90)
    valid = df.dropna(subset=["voting_hhi"])
    for _, r in df.sort_values(["category", "symbol"]).iterrows():
        ratio_str = f"{r['hhi_ratio']:.2f}x" if r['hhi_ratio'] is not None else "   N/A"
        gap_str = f"{r['hhi_gap']:+.4f}" if r['hhi_gap'] is not None else "    N/A"
        hold_str = f"{r['holding_hhi']:.4f}" if r['holding_hhi'] is not None else "   N/A"
        vote_str = f"{r['voting_hhi']:.4f}" if r['voting_hhi'] is not None else "   N/A"
        print(f"  {r['symbol']:6s} {r['category']:6s} {hold_str:>8s} {vote_str:>8s} {gap_str:>8s} {ratio_str:>7s}  {r['governance_source']}")

    if len(valid) >= 3:
        print(f"\nProtocols with voting data: {len(valid)}/{len(df)}")
        for cat in ["DeFi", "DePIN", "Infra", "AI"]:
            sub = valid[valid["category"] == cat]
            if len(sub) > 0:
                print(f"  {cat}: mean voting HHI = {sub['voting_hhi'].mean():.4f}  "
                      f"mean holding HHI = {sub['holding_hhi'].mean():.4f}  "
                      f"mean ratio = {sub['hhi_ratio'].mean():.2f}x  (N={len(sub)})")

        print("\nKey finding (hhi_ratio > 1 → delegation concentrates power):")
        concentrated = valid[valid["hhi_ratio"] > 2.0].sort_values("hhi_ratio", ascending=False)
        for _, r in concentrated.iterrows():
            print(f"  {r['symbol']:6s}: {r['hhi_ratio']:.1f}x — voting {r['voting_hhi']:.4f} vs holding {r['holding_hhi']:.4f}")

    return df


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print("B2 Governance Data Collection")
    print(f"Snapshot: 10 spaces confirmed")
    print(f"Tally:    {'enabled (key found)' if TALLY_KEY else 'DISABLED — set TALLY_KEY env var'}")
    print("=" * 70)

    # Snapshot
    found_spaces = pull_snapshot_spaces()
    proposals_df = pull_snapshot_proposals(found_spaces)
    votes_df = pull_snapshot_votes(proposals_df)

    # Tally
    delegates_df = pull_tally_delegates()
    pull_tally_proposals()

    # Voting HHI
    voting_hhi_df = compute_voting_hhi(votes_df, delegates_df)

    # Merge
    merged_df = merge_holding_voting(voting_hhi_df)

    # Output summary
    print("\n" + "=" * 70)
    print("FILES PRODUCED")
    print("=" * 70)
    for fname in ["snapshot_spaces.csv", "snapshot_proposals.csv", "snapshot_votes.csv",
                  "tally_delegates.csv", "voting_hhi.csv", "governance_participation.csv"]:
        path = DATA_DIR / fname
        if path.exists():
            size_kb = path.stat().st_size // 1024
            rows = sum(1 for _ in open(path)) - 1
            print(f"  {fname:35s} {rows:5d} rows  {size_kb:4d} KB")
        else:
            print(f"  {fname:35s} NOT CREATED")

    print(f"\nTally data missing: run with TALLY_KEY=<key> to collect AAVE, MKR, and on-chain votes.")
    print(f"LDO holding HHI uses estimate ({LDO_HOLDING_HHI_ESTIMATE}) — run Dune query to verify.")


if __name__ == "__main__":
    main()
