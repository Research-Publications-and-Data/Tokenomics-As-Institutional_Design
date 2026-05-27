"""
Phase 5 of B2 R3 data-collection omnibus: Solana PCA classification audit.

Closes §5.7 limitation #3 (PCA classification weaker coverage for Solana-native protocols).

Inputs (sibling clone /Users/zach/Tokenomics-As-Institutional_Design):
- data/raw/holder_lists/<TOKEN>_holders.csv: top-1000 holder snapshots (varying schemas)
- data/processed/exclusions_log.csv: existing PCA exclusions (134 rows; 8 Solana rows currently)

Outputs:
- b2/paper/supplements/solana_pca_audit_2026-05-27.csv: per-protocol pre/post-exclusion HHI
- b2/paper/supplements/solana_pca_audit_2026-05-27.md: human-readable audit report
- b2/paper/supplements/solana_pca_candidates_2026-05-27.csv: candidate PCA addresses for next-cycle on-chain verification

Methodology:
- For each Solana protocol (9 in N=40 dataset: JUP, DRIFT, HNT, HONEY, META, IO, GRASS, RENDER (Solana), W):
  1. Load top-1000 holder list (normalize schema: address, balance, share)
  2. Apply existing Solana exclusions; recompute holding-HHI
  3. Surface top-10 unexcluded holders for next-cycle PCA verification
  4. Flag data-integrity discrepancies (exclusion addresses that don't match documented attribution)

Per dispatch HALT-5.1: if PCA refinement produces > 0.05 HHI shift, halt and surface.
Per dispatch HALT-5.2: if Solana structural difference revealed, halt and surface.

Author: Claude Code session 2026-05-27 (PID 4300).
"""

import csv
from pathlib import Path
from collections import defaultdict

REPO = Path("/Users/zach/Tokenomics-As-Institutional_Design")
HOLDERS_DIR = REPO / "data/raw/holder_lists"
EXCLUSIONS = REPO / "data/processed/exclusions_log.csv"
OUT_DIR = REPO / "b2/paper/supplements"

# Map B2 protocol -> holder file (token symbol)
SOLANA_PROTOCOLS = {
    "Jupiter": "JUP",
    "Drift": "DRIFT",
    "Helium": "HNT",
    "Hivemapper": "HONEY",
    "MetaDAO": "META",
    "io.net": "IO",
    "Grass": "GRASS",
    "Render (Solana)": "RENDER_SOL",  # SOL-side specifically; RENDER_holders.csv is Ethereum
    "Wormhole": "W",
}


def load_holders(token):
    """Load holder file; normalize schema to (address, balance, share)."""
    path = HOLDERS_DIR / f"{token}_holders.csv"
    if not path.exists():
        return None
    out = []
    with path.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            addr = row.get("address") or row.get("owner")
            bal = float(row.get("balance", 0) or 0)
            # Some files have explicit share; others need to compute from balance
            share_raw = row.get("share")
            share = float(share_raw) if share_raw else None
            out.append({"address": addr, "balance": bal, "share": share})
    # Compute share if missing (treating top-1000 balance sum as denominator)
    total = sum(r["balance"] for r in out)
    if total > 0:
        for r in out:
            if r["share"] is None:
                r["share"] = r["balance"] / total
    return out


def load_exclusions_for_token(token, chain_filter="solana"):
    """Return dict address -> exclusion row for the given token + chain."""
    out = {}
    with EXCLUSIONS.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["token"] != token:
                continue
            if chain_filter and chain_filter not in row.get("chain", "").lower():
                continue
            out[row["address"]] = row
    return out


def compute_hhi(shares):
    """HHI = sum(s_i^2) where s_i is fraction (0-1). Range: 1/n to 1."""
    return sum(s * s for s in shares)


def normalize_shares(holders, exclude_addrs=None):
    """Re-normalize shares after exclusion; returns list of shares summing to 1.0 over remaining holders."""
    if exclude_addrs is None:
        exclude_addrs = set()
    remaining = [h for h in holders if h["address"] not in exclude_addrs]
    total_bal = sum(h["balance"] for h in remaining)
    if total_bal == 0:
        return []
    return [h["balance"] / total_bal for h in remaining]


def audit_protocol(protocol, token):
    """Per-protocol audit: pre/post-exclusion HHI + top-10 unexcluded holders."""
    holders = load_holders(token)
    if holders is None:
        return {"protocol": protocol, "token": token, "status": "MISSING_HOLDER_FILE"}

    exclusions = load_exclusions_for_token(token)

    # Pre-exclusion HHI (top-1000 raw shares as fractions)
    raw_shares = [h["share"] for h in holders]
    raw_total = sum(raw_shares)
    # Compute HHI using share-of-top-1000 (the canonical methodology per S12)
    pre_shares = [s / raw_total for s in raw_shares] if raw_total > 0 else []
    hhi_pre = compute_hhi(pre_shares)

    # Post-existing-exclusion HHI
    excl_addrs = set(exclusions.keys())
    post_shares = normalize_shares(holders, excl_addrs)
    hhi_post = compute_hhi(post_shares)

    # Top-10 unexcluded holders (PCA candidates for next-cycle verification)
    unexcluded = [h for h in holders if h["address"] not in excl_addrs]
    unexcluded.sort(key=lambda h: -h["balance"])
    top10_unexcluded = unexcluded[:10]

    # Discrepancy flag: do excluded addresses appear in top-1000?
    excluded_in_top1000 = []
    for addr in excl_addrs:
        for h in holders:
            if h["address"] == addr:
                excluded_in_top1000.append({
                    "address": addr,
                    "rank": holders.index(h) + 1,
                    "share": h["share"],
                    "identity": exclusions[addr]["identity"][:60],
                })
                break
        else:
            excluded_in_top1000.append({
                "address": addr,
                "rank": "NOT_IN_TOP1000",
                "share": None,
                "identity": exclusions[addr]["identity"][:60],
            })

    return {
        "protocol": protocol,
        "token": token,
        "status": "OK",
        "n_holders": len(holders),
        "n_existing_exclusions": len(excl_addrs),
        "hhi_pre_exclusion": hhi_pre,
        "hhi_post_existing_exclusion": hhi_post,
        "hhi_shift": hhi_post - hhi_pre,
        "top10_unexcluded": top10_unexcluded,
        "excluded_in_top1000": excluded_in_top1000,
    }


def main():
    print("=" * 70)
    print("Phase 5 of B2 R3 data-collection omnibus: Solana PCA audit")
    print("Generated 2026-05-27 (workflow clone PID 4300)")
    print("=" * 70)

    results = []
    for protocol, token in SOLANA_PROTOCOLS.items():
        r = audit_protocol(protocol, token)
        results.append(r)

    # Print summary
    print(f"\n{'Protocol':<18} {'Token':<10} {'N':<6} {'Excl':<6} {'HHI_pre':<10} {'HHI_post':<10} {'Shift':<10}")
    print("-" * 78)
    for r in results:
        if r["status"] != "OK":
            print(f"{r['protocol']:<18} {r['token']:<10} {r['status']}")
            continue
        print(f"{r['protocol']:<18} {r['token']:<10} {r['n_holders']:<6} "
              f"{r['n_existing_exclusions']:<6} {r['hhi_pre_exclusion']:<10.5f} "
              f"{r['hhi_post_existing_exclusion']:<10.5f} {r['hhi_shift']:+10.5f}")

    # Write CSV summary
    out_csv = OUT_DIR / "solana_pca_audit_2026-05-27.csv"
    with out_csv.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["protocol", "token", "status", "n_holders", "n_existing_exclusions",
                    "hhi_pre_exclusion", "hhi_post_existing_exclusion", "hhi_shift"])
        for r in results:
            if r["status"] != "OK":
                w.writerow([r["protocol"], r["token"], r["status"], "", "", "", "", ""])
                continue
            w.writerow([r["protocol"], r["token"], "OK", r["n_holders"],
                        r["n_existing_exclusions"],
                        f"{r['hhi_pre_exclusion']:.6f}",
                        f"{r['hhi_post_existing_exclusion']:.6f}",
                        f"{r['hhi_shift']:+.6f}"])
    print(f"\nWrote: {out_csv}")

    # Write per-protocol candidate PCA file
    candidates_csv = OUT_DIR / "solana_pca_candidates_2026-05-27.csv"
    with candidates_csv.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["protocol", "token", "rank", "address", "balance", "share_top1000_pct",
                    "candidate_class_hypothesis"])
        for r in results:
            if r["status"] != "OK":
                continue
            for i, h in enumerate(r["top10_unexcluded"], 1):
                # Default class hypothesis; refined per-protocol below
                w.writerow([r["protocol"], r["token"], i, h["address"],
                            f"{h['balance']:.2f}", f"{h['share']*100:.4f}",
                            "TBD (next-cycle Helius DAS + Squads + Realms cross-reference)"])
    print(f"Wrote: {candidates_csv}")

    # Discrepancy report
    print("\n=== Existing-exclusion verification ===")
    for r in results:
        if r["status"] != "OK":
            continue
        for e in r["excluded_in_top1000"]:
            rank = e["rank"]
            share = e["share"]
            share_str = f"{share*100:.2f}%" if share is not None else "N/A"
            flag = "OK" if isinstance(rank, int) and rank <= 10 else "FLAG"
            print(f"  [{flag}] {r['token']:>8} rank={str(rank):>15} share={share_str:>8}  "
                  f"{e['address'][:48]:<48}  {e['identity'][:40]}")

    return results


if __name__ == "__main__":
    main()
