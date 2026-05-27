#!/usr/bin/env python3
"""Pull W3F TVP candidates + cross-reference against our 600-validator set."""
import json, urllib.request

UA = "Mozilla/5.0"
URL = "https://raw.githubusercontent.com/w3f/1k-validators-be/master/candidates/polkadot.json"

req = urllib.request.Request(URL, headers={"User-Agent": UA})
with urllib.request.urlopen(req, timeout=15) as r:
    tvp = json.load(r)

candidates = tvp.get("candidates", [])
print(f"TVP candidates total: {len(candidates)}")
print(f"\nSample candidate:")
print(json.dumps(candidates[0], indent=2)[:500])

# Build TVP stash → name map
tvp_by_stash = {c["stash"]: c for c in candidates}

# Load our validator set
our_data = json.load(open("/tmp/b2_phase4/dot_validators_classified.json"))
validators = our_data["validators"]

# Cross-reference
matched_tvp = []
unverified_to_tvp = []
verified_to_tvp = []
for v in validators:
    if v["address"] in tvp_by_stash:
        c = tvp_by_stash[v["address"]]
        matched_tvp.append({**v, "tvp_name": c.get("name", ""), "kyc": c.get("kyc", False), "riot_handle": c.get("riotHandle", "")})
        if v["operator_class"] == "Unverified":
            unverified_to_tvp.append(matched_tvp[-1])
        else:
            verified_to_tvp.append(matched_tvp[-1])

print(f"\n=== TVP membership in our 600-validator set ===")
print(f"  TVP candidates total:                   {len(candidates)}")
print(f"  TVP candidates found in our 600 set:    {len(matched_tvp)}  ({100*len(matched_tvp)/600:.1f}%)")
print(f"  Of which were verified (Identity Pallet): {len(verified_to_tvp)}")
print(f"  Of which were UNVERIFIED (newly resolved): {len(unverified_to_tvp)}")

total_stake_unverif_tvp = sum(v["bonded_total_dot"] for v in unverified_to_tvp)
total_stake = our_data["total_bonded_dot"]
print(f"\n  Newly-resolved (Unverified → TVP) bonded stake: {total_stake_unverif_tvp:,.0f} DOT ({100*total_stake_unverif_tvp/total_stake:.2f}% of total)")

# Sample top-15 of newly resolved
print(f"\nTop-15 newly-resolved (was Unverified, now TVP-attributed):")
unverified_to_tvp.sort(key=lambda x: -x["bonded_total_dot"])
for i, v in enumerate(unverified_to_tvp[:15], 1):
    kyc = "(KYC)" if v["kyc"] else ""
    print(f"  #{i:>2}  {v['tvp_name'][:40]:<40}  {v['bonded_total_dot']:>10,.0f} DOT  {kyc} riot={v['riot_handle']}")

# Save
with open("/tmp/b2_phase4/dot_tvp_crossref.json", "w") as f:
    json.dump({
        "tvp_candidates_total": len(candidates),
        "matched_in_our_set": len(matched_tvp),
        "matched_breakdown": {"verified": len(verified_to_tvp), "newly_resolved": len(unverified_to_tvp)},
        "newly_resolved_stake_dot": total_stake_unverif_tvp,
        "newly_resolved_stake_pct": 100*total_stake_unverif_tvp/total_stake,
        "matched_validators": matched_tvp,
    }, f, default=str, indent=2)

# Updated unverified coverage stats
remaining_unverified = sum(1 for v in validators if v["operator_class"] == "Unverified" and v["address"] not in tvp_by_stash)
remaining_unverified_stake = sum(v["bonded_total_dot"] for v in validators if v["operator_class"] == "Unverified" and v["address"] not in tvp_by_stash)
print(f"\n=== After TVP cross-reference ===")
print(f"  Validators still unattributed: {remaining_unverified} / 600 ({100*remaining_unverified/600:.1f}%)")
print(f"  Stake still unattributed:      {remaining_unverified_stake:,.0f} DOT ({100*remaining_unverified_stake/total_stake:.2f}%)")
