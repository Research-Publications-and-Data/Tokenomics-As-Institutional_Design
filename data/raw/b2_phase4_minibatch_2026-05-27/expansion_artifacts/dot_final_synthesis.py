#!/usr/bin/env python3
"""Final synthesis: Identity Pallet + W3F TVP + Funding-source + Polkawatch pattern matching."""
import json
from collections import defaultdict

our = json.load(open("/tmp/b2_phase4/dot_validators_classified.json"))
tvp = json.load(open("/tmp/b2_phase4/dot_tvp_crossref.json"))
funding = json.load(open("/tmp/b2_phase4/dot_funding_clusters.json"))
polkawatch = json.load(open("/tmp/b2_phase4/dot_polkawatch_attribution.json"))

validators = our["validators"]
total_stake = our["total_bonded_dot"]

# Build per-validator attribution priority:
# 1. Identity Pallet match to CEX (highest priority - direct CEX attestation)
# 2. Funding-source attribution to known institutional (Blockdaemon, KILN, pos.dog, etc.)
# 3. Polkawatch operator-class attribution (verified by external researcher)
# 4. W3F TVP membership (community-operator vetting)
# 5. Identity Pallet Independent (verified but unclassified)
# 6. Unverified

# Build lookup maps
tvp_attr = {v["address"]: v["tvp_name"] for v in tvp.get("matched_validators", [])}

known_funders_to_display = {
    "14MceVAhD8moRWR3U3vLWBU5R9tqjS": "Blockdaemon",
    "13KJ3t8w1CKMkXCmZ6s3VwdWo4h747": "pos.dog",
    "1nXBtBPt3PV35m7Dfgp32xXgrC9tm1": "KILN",
    "14icei1ZMoG9QtKBFDk4y1eMR756q2": "Iceberg Nodes",
    "16WWmr2Xqgy5fna35GsNHXMU7vDBM1": "ParaNodes.io",
}

funder_attr = {}
for funder in funding["top_funders"]:
    funder_addr = funder["funder"]
    for prefix, display in known_funders_to_display.items():
        if funder_addr.startswith(prefix[:25]):
            for v_addr in funder["validator_addresses"]:
                funder_attr[v_addr] = display

# Polkawatch attribution (address-based)
pw_attr = {}
for op, data in polkawatch.get("by_operator", {}).items():
    cls = data["class"]
    for addr in data["matched_addrs"]:
        pw_attr[addr] = (op, cls)

def best_class(v):
    addr = v["address"]
    display = v["display"] or ""

    # Layer 1: Direct CEX brand match (Identity Pallet)
    if v["operator_class"].startswith("CEX:"):
        return v["operator_class"]
    # Layer 2: Funding-source attribution to known institutional
    if addr in funder_attr:
        return f"FundingSource:{funder_attr[addr]}"
    # Layer 3: Polkawatch attribution
    if addr in pw_attr:
        op, cls = pw_attr[addr]
        return f"Polkawatch_{cls}:{op}"
    # Layer 4: Other Identity Pallet matches
    if v["operator_class"].startswith("Institutional:") or v["operator_class"].startswith("Foundation:"):
        return v["operator_class"]
    # Layer 5: TVP attribution
    if addr in tvp_attr:
        return f"TVP:{tvp_attr[addr]}"
    # Layer 6: Independent
    if v["operator_class"] == "Independent":
        return "Independent"
    # Layer 7: Unverified
    return "Unverified"

# Apply
for v in validators:
    v["best_class_v2"] = best_class(v)

# Aggregate
by_class = defaultdict(lambda: {"n": 0, "stake": 0.0})
for v in validators:
    by_class[v["best_class_v2"]]["n"] += 1
    by_class[v["best_class_v2"]]["stake"] += v["bonded_total_dot"]

# Sort
sorted_classes = sorted(by_class.items(), key=lambda x: -x[1]["stake"])

print(f"=== Final multi-axis attribution (4 axes: Identity + TVP + Funding + Polkawatch) ===\n")
print(f"{'class':<55} {'n':>5} {'stake_dot':>14} {'pct':>7}")

attrs_stake = 0.0
unattr_stake = 0.0
for cls, stats in sorted_classes:
    pct = 100 * stats["stake"] / total_stake
    if cls == "Unverified":
        unattr_stake = stats["stake"]
    else:
        attrs_stake += stats["stake"]
    print(f"  {cls[:53]:<53} {stats['n']:>5} {stats['stake']:>14,.0f} {pct:>6.2f}%")

print(f"\n=== Final cumulative ===")
print(f"  Total bonded:        {total_stake:>14,.0f} DOT")
print(f"  Attributed:          {attrs_stake:>14,.0f} DOT  ({100*attrs_stake/total_stake:.2f}%)")
print(f"  Still unattributed:  {unattr_stake:>14,.0f} DOT  ({100*unattr_stake/total_stake:.2f}%)")

# Top-level type aggregates
cex_stake = sum(s["stake"] for c, s in by_class.items() if c.startswith("CEX:") or c.startswith("Polkawatch_CEX:"))
inst_stake = sum(s["stake"] for c, s in by_class.items() if c.startswith("Institutional:") or c.startswith("FundingSource:") or c.startswith("Polkawatch_Institutional:"))
vc_stake = sum(s["stake"] for c, s in by_class.items() if c.startswith("Polkawatch_Institutional_VC:"))
tvp_stake = sum(s["stake"] for c, s in by_class.items() if c.startswith("TVP:"))
community_stake = sum(s["stake"] for c, s in by_class.items() if c.startswith("Polkawatch_Independent_or_Community:") or c == "Independent")

print(f"\n=== Operator-type aggregates ===")
print(f"  CEX (Identity+Polkawatch verified):              {cex_stake:>14,.0f} ({100*cex_stake/total_stake:.2f}%)")
print(f"  Institutional staking providers (combined):     {inst_stake:>14,.0f} ({100*inst_stake/total_stake:.2f}%)")
print(f"  Institutional VC (Zug/Cypher/Animoca):          {vc_stake:>14,.0f} ({100*vc_stake/total_stake:.2f}%)")
print(f"  TVP community operators:                         {tvp_stake:>14,.0f} ({100*tvp_stake/total_stake:.2f}%)")
print(f"  Polkawatch Independent/Community + verified Indep: {community_stake:>14,.0f} ({100*community_stake/total_stake:.2f}%)")
print(f"  Still Unverified:                                {unattr_stake:>14,.0f} ({100*unattr_stake/total_stake:.2f}%)")

# Save
with open("/tmp/b2_phase4/dot_final_synthesis.json", "w") as f:
    json.dump({
        "axes_executed": ["Identity_Pallet", "W3F_TVP", "Funding_Source_Clustering", "Polkawatch_Pattern_Match"],
        "by_class": {c: s for c, s in sorted_classes},
        "cumulative_attributed_dot": attrs_stake,
        "cumulative_attributed_pct": 100*attrs_stake/total_stake,
        "operator_type_aggregates": {
            "CEX_pct": 100*cex_stake/total_stake,
            "Institutional_pct": 100*inst_stake/total_stake,
            "Institutional_VC_pct": 100*vc_stake/total_stake,
            "TVP_community_pct": 100*tvp_stake/total_stake,
            "Independent_Community_pct": 100*community_stake/total_stake,
            "still_unverified_pct": 100*unattr_stake/total_stake,
        },
        "validators": validators,
    }, f, default=str, indent=2)
