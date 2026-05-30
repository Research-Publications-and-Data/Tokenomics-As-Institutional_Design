#!/usr/bin/env python3
"""
voting_hhi_phase3_dot.py

B2 governance-concentration paper, voting-HHI Phase 3 (N=52 sample additions).
Acquires ONE conviction-weighted realized-vote concentration row for DOT
(Polkadot OpenGov / Gov2) from the Subscan API and computes the S12 voter-pool
HHI metric (top-100 pooled across a sample of recent DECIDED referenda).

Measure (matches the existing 13-row data of record for comparability):
  - For each sampled DECIDED referendum, page all votes.
  - Each vote exposes: voter account, locked amount (Planck), conviction multiplier,
    aye/nay/abstain status, and a Subscan precomputed weighted field "votes" that
    equals amount x conviction_multiplier. We use the Subscan "votes" field as the
    conviction-weighted weight, and we independently recompute amount x multiplier
    to confirm agreement (divergence is reported).
  - Effective voter attribution: when a vote carries a non-null delegate_account,
    the deciding power is exercised BY the delegate (the account.address is the
    delegator). We attribute the weight to the delegate (the entity actually
    wielding the power); direct votes attribute to account.address. This captures
    the delegation-concentration amplification mechanism and mirrors the Tally
    delegate-aggregation method used by the other comparable rows. The raw file
    also records a self-attributed weight for independent re-derivation.
  - POOLED canonical row: aggregate each effective voter's total conviction-weighted
    weight across the sampled referenda, sort descending, take TOP 100, normalize
    WITHIN the top-N sample, then compute HHI, top1/5/10 pct, and Gini (positive
    convention via the standard mean-absolute-difference formula).
  - Per-referendum conviction-weighted HHI is computed as a diagnostic (median + range).

Conviction multipliers per OpenGov: {0 -> 0.1x, 1 -> 1x, 2 -> 2x, 3 -> 3x,
4 -> 4x, 5 -> 5x, 6 -> 6x}. NOTE: Subscan returns the conviction field already as
the multiplier string itself ("0.1", "1", ... "6"), so the printed multiplier is
the conviction field value directly.

DOT has 10 decimals (1 DOT = 1e10 Planck).

Run: python3 analysis/voting_hhi_phase3_dot.py
Requires: env var SUBSCAN_API_KEY (auto-loaded in the author shell).

Writes:
  data/raw/voting_hhi_phase3_dot_raw.csv          (per-effective-voter pooled weights)
  data/raw/voting_hhi_phase3_dot_per_referendum.csv (per-referendum diagnostic)
"""

import os
import sys
import json
import time
import urllib.request
import urllib.error
import numpy as np

# ----------------------------------------------------------------------------
# Canonical metric helpers (copied verbatim from the dispatch spec).
# ----------------------------------------------------------------------------

def compute_hhi(values):
    v = np.array(values, dtype=float); v = v[v > 0]
    if len(v) == 0 or v.sum() == 0:
        return None
    shares = v / v.sum(); return float(np.sum(shares ** 2))


def compute_gini(values):
    v = np.sort(np.array([x for x in values if x > 0], dtype=float)); n = len(v)
    if n == 0 or v.sum() == 0:
        return None
    d = np.abs(v[:, None] - v[None, :]).sum(); return float(d / (2 * n * v.sum()))


# ----------------------------------------------------------------------------
# Subscan API plumbing.
# ----------------------------------------------------------------------------

SUBSCAN_BASE = "https://polkadot.api.subscan.io/api/scan/"
DOT_DECIMALS = 1e10

# Statuses that count as DECIDED (a final on-chain outcome was reached).
# Subscan label set observed live: Executed, Rejected, Timeout, ExecutedFailed.
# We also accept the canonical OpenGov terminal labels in case the label surface
# shifts (Approved, Confirmed, NotPassed, TimedOut). Excluded as NOT decided:
# Submitted, Decision (deciding), Cancelled, Killed.
DECIDED_STATUSES = {
    "Executed", "ExecutedFailed", "Rejected", "Timeout", "TimedOut",
    "Approved", "Confirmed", "NotPassed",
}
EXCLUDED_STATUSES = {"Submitted", "Decision", "Deciding", "Cancelled", "Killed"}

# Conviction-multiplier table (kept for the independent amount x multiplier check).
# Subscan returns the conviction field already AS the multiplier, but we map the
# raw OpenGov conviction index here defensively in case a "0".."6" index surfaces.
CONVICTION_MULT = {
    "0": 0.1, "1": 1.0, "2": 2.0, "3": 3.0,
    "4": 4.0, "5": 5.0, "6": 6.0,
    "0.1": 0.1,  # Subscan-style direct multiplier
}

N_REFERENDA_TARGET = 20          # sample size of recent DECIDED referenda
VOTES_PAGE_ROWS = 100
SLEEP_BETWEEN_CALLS = 0.20       # politeness; Subscan rate budget


def _api_key():
    key = os.environ.get("SUBSCAN_API_KEY")
    if not key:
        sys.stderr.write("ERROR: SUBSCAN_API_KEY not set in environment.\n")
        sys.exit(2)
    return key


def post(path, body, key, retries=4):
    url = SUBSCAN_BASE + path
    data = json.dumps(body).encode()
    headers = {"X-API-Key": key, "Content-Type": "application/json"}
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, data=data, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as resp:
                d = json.load(resp)
            if d.get("code") != 0:
                last = RuntimeError("API code %s: %s" % (d.get("code"), d.get("message")))
                time.sleep(1.0 + attempt)
                continue
            return d
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as e:
            last = e
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError("post failed for %s: %s" % (path, last))


def fetch_recent_referenda(key, want_decided):
    """Return a list of decided-referendum dicts (most recent first), enough to
    yield want_decided decided entries."""
    decided = []
    page = 0
    while len(decided) < want_decided and page < 8:
        d = post("referenda/referendums", {"row": 100, "page": page}, key)
        lst = (d.get("data") or {}).get("list") or []
        if not lst:
            break
        for r in lst:
            st = r.get("status")
            if st in DECIDED_STATUSES:
                decided.append(r)
            # statuses not in DECIDED and not explicitly excluded are skipped silently
        page += 1
        time.sleep(SLEEP_BETWEEN_CALLS)
    return decided[:want_decided]


def fetch_all_votes(referendum_index, key):
    """Page through all votes for a referendum. Returns list of vote dicts."""
    out = []
    page = 0
    while True:
        d = post(
            "referenda/votes",
            {"referendum_index": referendum_index, "row": VOTES_PAGE_ROWS, "page": page},
            key,
        )
        data = d.get("data") or {}
        lst = data.get("list") or []
        out.extend(lst)
        count = data.get("count") or 0
        page += 1
        if len(out) >= count or not lst:
            break
        if page > 60:  # hard safety cap
            break
        time.sleep(SLEEP_BETWEEN_CALLS)
    return out


def _addr(node):
    """Extract an address string from an account-or-delegate node (dict or str)."""
    if node is None:
        return None
    if isinstance(node, dict):
        return node.get("address")
    return str(node)


def vote_weight(v):
    """Conviction-weighted weight in DOT for a single vote row.
    Primary: Subscan precomputed "votes" field (amount x conviction_multiplier).
    Returns (weight_dot, recomputed_dot, conviction_str, status)."""
    amount_planck = float(v.get("amount") or 0)
    conv = str(v.get("conviction"))
    mult = CONVICTION_MULT.get(conv)
    if mult is None:
        # conviction already a multiplier-looking float string not in table
        try:
            mult = float(conv)
        except ValueError:
            mult = 1.0
    subscan_votes_planck = float(v.get("votes") or 0)
    weight_dot = subscan_votes_planck / DOT_DECIMALS
    recomputed_dot = (amount_planck * mult) / DOT_DECIMALS
    return weight_dot, recomputed_dot, conv, v.get("status")


def main():
    key = _api_key()

    print("Fetching recent referenda and filtering to DECIDED ...", file=sys.stderr)
    referenda = fetch_recent_referenda(key, N_REFERENDA_TARGET)
    if not referenda:
        sys.stderr.write("NO DECIDED REFERENDA FOUND.\n")
        # still write empty outputs so the run is reproducible
        sys.exit(3)
    print("Sampled %d decided referenda: %s"
          % (len(referenda), [r["referendum_index"] for r in referenda]), file=sys.stderr)

    # Pooled effective-voter weights (canonical) and self-attributed weights (diagnostic).
    pooled_effective = {}   # effective_voter_addr -> total conviction-weighted DOT
    pooled_self = {}        # account_addr        -> total conviction-weighted DOT
    voter_meta = {}         # effective_voter_addr -> {"is_delegate": bool, "display": str}

    per_ref_rows = []       # diagnostic: one row per referendum
    raw_vote_records = []   # full vote-level evidence (for the raw csv)

    total_recompute_divergence = 0
    total_votes_seen = 0

    for r in referenda:
        idx = r["referendum_index"]
        status = r.get("status")
        track = r.get("origins") or r.get("call_module")
        votes = fetch_all_votes(idx, key)
        per_voter_ref = {}  # effective voter -> weight within this referendum

        for v in votes:
            total_votes_seen += 1
            w_dot, recomp_dot, conv, vstatus = vote_weight(v)
            if w_dot <= 0:
                continue
            if abs(w_dot - recomp_dot) > max(1e-6, 0.001 * w_dot):
                total_recompute_divergence += 1

            self_addr = _addr(v.get("account"))
            deleg_node = v.get("delegate_account")
            deleg_addr = _addr(deleg_node)
            effective = deleg_addr if deleg_addr else self_addr
            if effective is None:
                continue

            pooled_effective[effective] = pooled_effective.get(effective, 0.0) + w_dot
            if self_addr:
                pooled_self[self_addr] = pooled_self.get(self_addr, 0.0) + w_dot
            per_voter_ref[effective] = per_voter_ref.get(effective, 0.0) + w_dot

            if effective not in voter_meta:
                disp = ""
                node = deleg_node if deleg_addr else v.get("account")
                if isinstance(node, dict):
                    ppl = node.get("people") or {}
                    disp = (ppl.get("display") or "") if isinstance(ppl, dict) else ""
                voter_meta[effective] = {"is_delegate": bool(deleg_addr), "display": disp}

            raw_vote_records.append({
                "referendum_index": idx,
                "ref_status": status,
                "track": track,
                "effective_voter": effective,
                "self_account": self_addr or "",
                "delegate_account": deleg_addr or "",
                "is_delegated": 1 if deleg_addr else 0,
                "amount_dot": float(v.get("amount") or 0) / DOT_DECIMALS,
                "conviction": conv,
                "vote_status": vstatus or "",
                "weight_dot_subscan": w_dot,
                "weight_dot_recomputed": recomp_dot,
            })

        # per-referendum conviction-weighted HHI diagnostic (effective-voter basis)
        ref_vals = list(per_voter_ref.values())
        ref_hhi = compute_hhi(ref_vals)
        per_ref_rows.append({
            "referendum_index": idx,
            "status": status,
            "track": track,
            "n_effective_voters": len(per_voter_ref),
            "n_vote_rows": len(votes),
            "ref_conviction_weighted_hhi": ref_hhi,
            "total_weight_dot": sum(ref_vals),
        })
        print("  ref %s [%s] track=%s: %d vote-rows, %d effective voters, HHI=%s"
              % (idx, status, track, len(votes), len(per_voter_ref),
                 ("%.5f" % ref_hhi) if ref_hhi is not None else "NA"),
              file=sys.stderr)

    # ------------------------------------------------------------------
    # POOLED canonical row: top-100 of effective-voter pooled weights.
    # ------------------------------------------------------------------
    items = sorted(pooled_effective.items(), key=lambda kv: kv[1], reverse=True)
    n_unique_voters = len(items)
    top = items[:100]
    n_sampled = len(top)
    top_weights = [w for _, w in top]

    voting_hhi = compute_hhi(top_weights)
    voting_gini = compute_gini(top_weights)

    arr = np.array(top_weights, dtype=float)
    arr = arr[arr > 0]
    arr_sorted = np.sort(arr)[::-1]
    tot = arr_sorted.sum()
    shares = arr_sorted / tot if tot > 0 else arr_sorted
    voting_top1_pct = float(100 * shares[0]) if len(shares) >= 1 else None
    voting_top5_pct = float(100 * shares[:5].sum()) if len(shares) >= 1 else None
    voting_top10_pct = float(100 * shares[:10].sum()) if len(shares) >= 1 else None

    # per-referendum diagnostic stats
    ref_hhis = [row["ref_conviction_weighted_hhi"] for row in per_ref_rows
                if row["ref_conviction_weighted_hhi"] is not None]
    ref_hhi_median = float(np.median(ref_hhis)) if ref_hhis else None
    ref_hhi_min = float(np.min(ref_hhis)) if ref_hhis else None
    ref_hhi_max = float(np.max(ref_hhis)) if ref_hhis else None

    # ------------------------------------------------------------------
    # Write raw evidence files (committed paths; no /tmp dependency).
    # ------------------------------------------------------------------
    here = os.path.dirname(os.path.abspath(__file__))
    repo = os.path.dirname(here)
    raw_dir = os.path.join(repo, "data", "raw")
    os.makedirs(raw_dir, exist_ok=True)

    # 1) Canonical per-effective-voter POOLED weights (the verifier re-runs HHI on this).
    pooled_csv = os.path.join(raw_dir, "voting_hhi_phase3_dot_raw.csv")
    with open(pooled_csv, "w") as f:
        f.write("rank,effective_voter,is_delegate,display,pooled_conviction_weighted_dot,"
                "self_attributed_pooled_dot,in_top100\n")
        for rank, (addr, w) in enumerate(items, start=1):
            meta = voter_meta.get(addr, {})
            disp = (meta.get("display") or "").replace(",", " ").replace("\n", " ")
            self_w = pooled_self.get(addr, "")
            f.write("%d,%s,%d,%s,%.6f,%s,%d\n" % (
                rank, addr, 1 if meta.get("is_delegate") else 0, disp,
                w, ("%.6f" % self_w) if self_w != "" else "",
                1 if rank <= 100 else 0,
            ))

    # 2) Per-referendum diagnostic.
    perref_csv = os.path.join(raw_dir, "voting_hhi_phase3_dot_per_referendum.csv")
    with open(perref_csv, "w") as f:
        f.write("referendum_index,status,track,n_effective_voters,n_vote_rows,"
                "ref_conviction_weighted_hhi,total_weight_dot\n")
        for row in per_ref_rows:
            f.write("%s,%s,%s,%d,%d,%s,%.6f\n" % (
                row["referendum_index"], row["status"], row["track"],
                row["n_effective_voters"], row["n_vote_rows"],
                ("%.6f" % row["ref_conviction_weighted_hhi"])
                if row["ref_conviction_weighted_hhi"] is not None else "",
                row["total_weight_dot"],
            ))

    # 3) Full vote-level evidence (optional deep audit).
    votelevel_csv = os.path.join(raw_dir, "voting_hhi_phase3_dot_votes.csv")
    with open(votelevel_csv, "w") as f:
        cols = ["referendum_index", "ref_status", "track", "effective_voter",
                "self_account", "delegate_account", "is_delegated", "amount_dot",
                "conviction", "vote_status", "weight_dot_subscan", "weight_dot_recomputed"]
        f.write(",".join(cols) + "\n")
        for rec in raw_vote_records:
            f.write(",".join(str(rec[c]) for c in cols) + "\n")

    # ------------------------------------------------------------------
    # Emit the computed row as JSON to stdout for the orchestrator.
    # ------------------------------------------------------------------
    holdings_hhi_of_record = 0.0052
    holdings_hhi_alt = 0.01392
    ratio_documented = (voting_hhi / holdings_hhi_of_record) if voting_hhi else None
    ratio_alt = (voting_hhi / holdings_hhi_alt) if voting_hhi else None
    if ratio_documented is None:
        direction = "unknown"
    elif ratio_documented > 1.1:
        direction = "amplify"
    elif ratio_documented < 0.9:
        direction = "disperse"
    else:
        direction = "equivalent"

    result = {
        "symbol": "DOT",
        "source": "subscan",
        "voting_hhi": voting_hhi,
        "voting_gini": voting_gini,
        "voting_top1_pct": voting_top1_pct,
        "voting_top5_pct": voting_top5_pct,
        "voting_top10_pct": voting_top10_pct,
        "n_unique_voters": n_unique_voters,
        "n_sampled": n_sampled,
        "n_referenda_sampled": len(referenda),
        "referenda_indices": [r["referendum_index"] for r in referenda],
        "per_ref_hhi_median": ref_hhi_median,
        "per_ref_hhi_min": ref_hhi_min,
        "per_ref_hhi_max": ref_hhi_max,
        "total_vote_rows_seen": total_votes_seen,
        "recompute_divergences": total_recompute_divergence,
        "holdings_hhi_of_record": holdings_hhi_of_record,
        "ratio_vs_documented_0.0052": ratio_documented,
        "ratio_vs_alt_0.01392": ratio_alt,
        "observed_direction": direction,
        "raw_csv": pooled_csv,
        "per_referendum_csv": perref_csv,
        "vote_level_csv": votelevel_csv,
    }
    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    main()
