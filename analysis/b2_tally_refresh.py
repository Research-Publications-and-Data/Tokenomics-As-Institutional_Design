"""B2 R2 Tally voting HHI refresh: top-1000 delegates per protocol via correct 2-step schema."""
import os
import sys
import time
import json
import csv
import requests
from pathlib import Path

TALLY_API = "https://api.tally.xyz/query"
TALLY_KEY = os.environ.get("TALLY_KEY", "")
if not TALLY_KEY:
    print("[FATAL] TALLY_KEY not set", file=sys.stderr)
    sys.exit(1)

TALLY_SLUGS = {
    "AAVE": "aave",
    "COMP": "compound",
    "UNI":  "uniswap",
    "ARB":  "arbitrum",
    "OP":   "optimism",
    "ENS":  "ens",
    "GMX":  "gmx",
}

HEADERS = {"Content-Type": "application/json", "Api-Key": TALLY_KEY}


def tally_query(query, variables, retries=3):
    for attempt in range(retries):
        try:
            r = requests.post(TALLY_API, headers=HEADERS,
                              json={"query": query, "variables": variables}, timeout=30)
            if r.status_code == 429:
                wait = int(r.headers.get("Retry-After", 10))
                time.sleep(wait)
                continue
            r.raise_for_status()
            data = r.json()
            if "errors" in data:
                print(f"  GraphQL errors: {data['errors'][:2]}", file=sys.stderr)
                return None
            return data.get("data") or {}
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
            else:
                print(f"  request failed: {e}", file=sys.stderr)
                return None


def find_org_id(slug):
    q = """query($slug: String!) {
      organization(input: { slug: $slug }) {
        id slug name proposalsCount delegatesCount tokenOwnersCount
      }
    }"""
    data = tally_query(q, {"slug": slug})
    return data.get("organization") if data else None


def pull_delegates(org_id, target_n=1000):
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
    cursor = None
    delegates = []
    while len(delegates) < target_n:
        page = {"limit": 50}
        if cursor:
            page["afterCursor"] = cursor
        variables = {"input": {
            "filters": {"organizationId": org_id},
            "sort": {"sortBy": "votes", "isDescending": True},
            "page": page,
        }}
        data = tally_query(delegates_q, variables)
        if not data:
            break
        result = data.get("delegates") or {}
        nodes = result.get("nodes") or []
        if not nodes:
            break
        delegates.extend(nodes)
        page_info = result.get("pageInfo") or {}
        cursor = page_info.get("lastCursor")
        if not cursor:
            break
        time.sleep(0.5)
        if len(delegates) >= target_n:
            break
    return delegates[:target_n]


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


def main():
    results = []
    for symbol, slug in TALLY_SLUGS.items():
        print(f"[tally] {symbol} ({slug})... ", end="", flush=True)
        org = find_org_id(slug)
        if not org:
            print("org not found")
            results.append({"symbol": symbol, "source": "tally", "status": "org_not_found"})
            continue
        print(f"org_id={org['id']}, total_delegates={org.get('delegatesCount',0)}", flush=True)
        delegates = pull_delegates(org["id"], target_n=1000)
        print(f"  pulled {len(delegates)} delegates")
        values = []
        for d in delegates:
            try:
                vc = float(d.get("votesCount", 0) or 0)
                if vc > 0:
                    values.append(vc)
            except (ValueError, TypeError):
                pass
        hhi, gini, top1, top5, top10 = compute_hhi(values)
        results.append({
            "symbol": symbol, "source": "tally",
            "n_pulled": len(delegates),
            "n_with_votes": len(values),
            "total_delegates": org.get('delegatesCount', 0),
            "voting_hhi": hhi, "voting_gini": gini,
            "voting_top1_pct": top1, "voting_top5_pct": top5, "voting_top10_pct": top10,
        })
        print(f"  HHI={hhi:.4f}, top1={top1:.1f}%" if hhi else "  no data")

    if results:
        out = Path("/tmp/b2_tally_refresh_results.csv")
        with open(out, "w", newline="") as f:
            keys = set()
            for r in results:
                keys.update(r.keys())
            writer = csv.DictWriter(f, fieldnames=list(keys))
            writer.writeheader()
            writer.writerows(results)
        print(f"\n[WRITTEN] {out}")


if __name__ == "__main__":
    main()
