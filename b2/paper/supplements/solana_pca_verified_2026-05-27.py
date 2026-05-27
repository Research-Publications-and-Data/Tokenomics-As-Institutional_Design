"""
Phase 5 continuation: integrate Sim API verification results into Solana PCA exclusions.

Per /tmp/b2_r3_omnibus_handoff_back_to_canonical_writer_2026-05-27.md Phase 5 remainder:
on-chain verification of 7 cross-protocol Solana candidate addresses via Sim API.

Verification results (PID 4300 sister-session 2026-05-27):
- 6 of 7 addresses confirmed CEX-hot-wallet behavioral signature (1000+ SPL token balances,
  memecoin dust mix; pattern parallels existing Binance hot wallet 9WzDXw...).
- 1 address (5LZkATrLwHY...) is institutional-investor pattern (63 tokens; only major
  Solana DePIN/DeFi assets; $28M+ concentrated positions). NOT classified as PCA.

Refined exclusions to add (Class 5 CEX custody):
1. u6PJ8DtQuPFnfmwHbGFULQ4u4EgjDiyYKjVEsynXq2w (5197 balances; JUP+HNT+GRASS+RENDER_SOL)
2. 6FEVkH17P9y8Q9aCkDdPcMDjvj7SVxrTETaYEm8f51Jy (1579 balances; JUP+HNT+RENDER_SOL)
3. 5tzFkiKscXHK5ZXCGbXZxdw7gTjjD1mBwuoFbhUvuAi9 (3807 balances; JUP+RENDER_SOL+W)
4. 6LY1JzAFVZsP2a2xKrtU6znQMQ5h4i7tocWdgrkZzkzF (481 balances; $143M USDT + xStocks; JUP+RENDER_SOL)
5. 5PAhQiYdLBd6SVdjzBQDxUAEFyDdF5ExNPQfcscnPRj5 (2547 balances; GRASS+RENDER_SOL)
6. JCNCMFXo5M5qwUPg2Utu1u6YWp3MbygxqBsBeXXJfrw (752 balances; DRIFT same-protocol duplicate)

Output: extended exclusions CSV + recomputed Solana HHIs with new exclusions applied.

Author: Claude Code session 2026-05-27 (PID 4300).
"""

import csv
from pathlib import Path

REPO = Path("/Users/zach/Tokenomics-As-Institutional_Design")
HOLDERS_DIR = REPO / "data/raw/holder_lists"
EXCLUSIONS = REPO / "data/processed/exclusions_log.csv"
OUT_DIR = REPO / "b2/paper/supplements"

# Verified CEX-pattern addresses (Class 5)
VERIFIED_CEX_EXCLUSIONS = [
    {
        "address": "u6PJ8DtQuPFnfmwHbGFULQ4u4EgjDiyYKjVEsynXq2w",
        "identity": "CEX hot wallet on Solana (Class 5; 5197 SPL token balances; memecoin-dust + major-asset mix; behavioral signature parallel to 9WzDXw Binance)",
        "verification": "Sim API svm balances 2026-05-27; 5197 distinct SPL token balances including memecoins (PainPain, CUDIS, DeepepeAI, Anthropic-memecoin) + major assets; behavioral signature consistent with CEX custody (mechanical receipt of all listed-token transfers)",
        "applies_to": ["JUP", "HNT", "GRASS", "RENDER_SOL"],
    },
    {
        "address": "6FEVkH17P9y8Q9aCkDdPcMDjvj7SVxrTETaYEm8f51Jy",
        "identity": "CEX hot wallet on Solana (Class 5; 1579 SPL token balances; memecoin dust + PYUSD stablecoin)",
        "verification": "Sim API svm balances 2026-05-27; 1579 distinct SPL tokens; PYUSD position + extreme memecoin diversity = CEX custody behavioral signature",
        "applies_to": ["JUP", "HNT", "RENDER_SOL"],
    },
    {
        "address": "5tzFkiKscXHK5ZXCGbXZxdw7gTjjD1mBwuoFbhUvuAi9",
        "identity": "CEX hot wallet on Solana (Class 5; 3807 SPL token balances; PENGU + ANIME + memecoin breadth)",
        "verification": "Sim API svm balances 2026-05-27; 3807 distinct SPL tokens; PENGU + ANIME + extreme memecoin diversity = CEX custody behavioral signature",
        "applies_to": ["JUP", "RENDER_SOL", "W"],
    },
    {
        "address": "6LY1JzAFVZsP2a2xKrtU6znQMQ5h4i7tocWdgrkZzkzF",
        "identity": "CEX hot wallet on Solana (Class 5; 481 SPL token balances; major stablecoin custody $143M USDT + $38M USDC + xStocks; high-tier CEX pattern)",
        "verification": "Sim API svm balances 2026-05-27; 481 distinct tokens; $143M USDT + $38M USDC + $42M SOL + $11M RENDER + Backed Finance xStocks (MSTRx, QQQx, CRCLx) holdings = major-CEX-custody pattern (Binance/Coinbase-tier)",
        "applies_to": ["JUP", "RENDER_SOL"],
    },
    {
        "address": "5PAhQiYdLBd6SVdjzBQDxUAEFyDdF5ExNPQfcscnPRj5",
        "identity": "CEX hot wallet on Solana (Class 5; 2547 SPL token balances; extreme memecoin diversity)",
        "verification": "Sim API svm balances 2026-05-27; 2547 distinct tokens; memecoin pattern consistent with CEX hot wallet",
        "applies_to": ["GRASS", "RENDER_SOL"],
    },
    {
        "address": "JCNCMFXo5M5qwUPg2Utu1u6YWp3MbygxqBsBeXXJfrw",
        "identity": "CEX hot wallet on Solana (Class 5; 752 SPL token balances; memecoin pattern; DRIFT same-protocol r6+r9 reflects same-address duplicate token entries in DRIFT holder file)",
        "verification": "Sim API svm balances 2026-05-27; 752 distinct tokens; memecoin diversity consistent with CEX custody",
        "applies_to": ["DRIFT"],
    },
]

# NOT-PCA finding (institutional investor; preserved as genuine holder)
INSTITUTIONAL_INVESTOR = {
    "address": "5LZkATrLwHYCQj2YuVbjjgsDZzBk6YfL4pFQRJmtboT2",
    "classification": "Institutional investor (NOT PCA)",
    "verification": "Sim API svm balances 2026-05-27; only 63 distinct SPL tokens; major Solana DePIN/DeFi only (ZEREBRO $10M + DRIFT $3.5M + HNT $3.1M + PYTH $2.4M + JTO $2.4M + W $2.1M + IO $1.8M); no memecoin dust; behavioral signature consistent with sophisticated multi-token investor or venture-fund custody, not CEX or Foundation",
    "implication": "HNT rank-1 unexcluded holder (12.43% share) is a genuine independent governance holder; HNT HHI should NOT be reduced by excluding this address",
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
            share_raw = row.get("share")
            share = float(share_raw) if share_raw else None
            out.append({"address": addr, "balance": bal, "share": share})
    total = sum(r["balance"] for r in out)
    if total > 0:
        for r in out:
            if r["share"] is None:
                r["share"] = r["balance"] / total
    return out


def load_existing_exclusions(token, chain_filter="solana"):
    excl = set()
    with EXCLUSIONS.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["token"] == token and chain_filter in row.get("chain", "").lower():
                excl.add(row["address"])
    return excl


def compute_hhi(shares):
    return sum(s * s for s in shares)


def normalize_shares(holders, exclude_addrs):
    remaining = [h for h in holders if h["address"] not in exclude_addrs]
    total_bal = sum(h["balance"] for h in remaining)
    if total_bal == 0:
        return []
    return [h["balance"] / total_bal for h in remaining]


def main():
    print("=" * 80)
    print("Phase 5 continuation: Solana PCA verified-exclusions HHI recompute")
    print("=" * 80)

    # Per-token: which new CEX exclusions apply
    token_new_exclusions = {}
    for excl in VERIFIED_CEX_EXCLUSIONS:
        for tok in excl["applies_to"]:
            token_new_exclusions.setdefault(tok, []).append(excl["address"])

    print(f"\n{'Token':<10} {'Existing':<10} {'New':<6} {'N_holders':<10} "
          f"{'HHI_existing':<14} {'HHI_with_new':<14} {'Shift':<10}")
    print("-" * 90)

    results = []
    for token in ["JUP", "HNT", "DRIFT", "GRASS", "RENDER_SOL", "W"]:
        holders = load_holders(token)
        if holders is None:
            print(f"{token:<10} MISSING")
            continue
        existing_excl = load_existing_exclusions(token)
        new_excl = set(token_new_exclusions.get(token, []))
        all_excl = existing_excl | new_excl

        existing_shares = normalize_shares(holders, existing_excl)
        new_shares = normalize_shares(holders, all_excl)
        hhi_existing = compute_hhi(existing_shares)
        hhi_new = compute_hhi(new_shares)
        shift = hhi_new - hhi_existing

        # Find how many new exclusions actually appeared in this token's holder list
        n_new_in_list = sum(1 for a in new_excl if any(h["address"] == a for h in holders))

        print(f"{token:<10} {len(existing_excl):<10} {n_new_in_list:<6} {len(holders):<10} "
              f"{hhi_existing:<14.6f} {hhi_new:<14.6f} {shift:+10.6f}")

        results.append({
            "token": token,
            "n_holders": len(holders),
            "n_existing_exclusions": len(existing_excl),
            "n_new_exclusions_applicable": n_new_in_list,
            "hhi_existing_exclusion": hhi_existing,
            "hhi_with_verified_exclusions": hhi_new,
            "hhi_shift": shift,
        })

    # Write verified CSV
    out_csv = OUT_DIR / "solana_pca_verified_2026-05-27.csv"
    with out_csv.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["token", "n_holders", "n_existing_exclusions", "n_new_exclusions_applicable",
                    "hhi_existing_exclusion", "hhi_with_verified_exclusions", "hhi_shift",
                    "halt_5_1_threshold_0.05"])
        for r in results:
            halt = "TRIGGERED" if abs(r["hhi_shift"]) > 0.05 else "OK"
            w.writerow([r["token"], r["n_holders"], r["n_existing_exclusions"],
                        r["n_new_exclusions_applicable"],
                        f"{r['hhi_existing_exclusion']:.6f}",
                        f"{r['hhi_with_verified_exclusions']:.6f}",
                        f"{r['hhi_shift']:+.6f}", halt])
    print(f"\nWrote: {out_csv}")

    # Write proposed exclusions CSV (for next CANONICAL-WRITER lane integration)
    out_excl = OUT_DIR / "solana_pca_proposed_exclusions_2026-05-27.csv"
    with out_excl.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["token", "address", "identity", "exclusion_reason", "chain",
                    "hhi_before", "hhi_after", "source"])
        # Build per-token-per-address rows
        for excl in VERIFIED_CEX_EXCLUSIONS:
            for tok in excl["applies_to"]:
                # Look up before/after HHI from results
                tok_r = next((r for r in results if r["token"] == tok), None)
                if tok_r is None:
                    continue
                w.writerow([
                    tok, excl["address"], excl["identity"][:80], excl["verification"][:150],
                    "Solana",
                    f"{tok_r['hhi_existing_exclusion']:.6f}",
                    f"{tok_r['hhi_with_verified_exclusions']:.6f}",
                    "Sim API svm balances verification 2026-05-27 (PID 4300)",
                ])
    print(f"Wrote: {out_excl}")

    return results


if __name__ == "__main__":
    main()
