#!/usr/bin/env python3
"""Synthesize all attribution sources: Identity Pallet + TVP + Funding-source clustering."""
import json
from collections import defaultdict

our = json.load(open("/tmp/b2_phase4/dot_validators_classified.json"))
tvp = json.load(open("/tmp/b2_phase4/dot_tvp_crossref.json"))
funding = json.load(open("/tmp/b2_phase4/dot_funding_clusters.json"))

validators = our["validators"]
total_stake = our["total_bonded_dot"]

# Build TVP-matched lookup
tvp_attr = {v["address"]: v["tvp_name"] for v in tvp.get("matched_validators", [])}

# Build funding-source attribution lookup (operator name from display)
# Top-funders with confirmed display names
known_funders_by_display = {
    "Blockdaemon": "14MceVAhD8moRWR3U3vLWBU5R9tqjS",
    "pos.dog": "13KJ3t8w1CKMkXCmZ6s3VwdWo4h747",
    "KILN": "1nXBtBPt3PV35m7Dfgp32xXgrC9tm1",
    "🧊 Iceberg Nodes 🧊": "14icei1ZMoG9QtKBFDk4y1eMR756q2",
    "ParaNodes.io": "16WWmr2Xqgy5fna35GsNHXMU7vDBM1",
}

# Match funder addresses to short prefixes
funder_attr = {}
for funder in funding["top_funders"]:
    addr_short = funder["funder"][:30]
    for display, prefix in known_funders_by_display.items():
        if addr_short.startswith(prefix[:25]):
            for v_addr in funder["validator_addresses"]:
                funder_attr[v_addr] = display

# Compute coverage by axis (assign each validator to best-available class)
def best_class(v):
    addr = v["address"]
    # Layer 1: Identity Pallet (already in operator_class)
    if v["operator_class"] != "Unverified":
        return v["operator_class"]
    # Layer 2: TVP matching
    if addr in tvp_attr:
        return f"TVP:{tvp_attr[addr][:30]}"
    # Layer 3: Funding-source
    if addr in funder_attr:
        return f"FundingSource:{funder_attr[addr]}"
    return "Unverified"

# Apply best-class
for v in validators:
    v["best_class"] = best_class(v)

# Aggregate
by_class = defaultdict(lambda: {"n": 0, "stake": 0.0})
for v in validators:
    by_class[v["best_class"]]["n"] += 1
    by_class[v["best_class"]]["stake"] += v["bonded_total_dot"]

# Sort by stake
sorted_classes = sorted(by_class.items(), key=lambda x: -x[1]["stake"])

print(f"=== Multi-axis attribution: cumulative coverage ===")
print(f"{'class':<45} {'n':>6} {'stake_dot':>14} {'stake_pct':>10}")

cumulative_attr_stake = 0.0
unattr_stake = 0.0
for cls, stats in sorted_classes:
    sp = 100 * stats["stake"] / total_stake
    if cls != "Unverified":
        cumulative_attr_stake += stats["stake"]
    else:
        unattr_stake = stats["stake"]
    print(f"  {cls:<43} {stats['n']:>6} {stats['stake']:>14,.0f} {sp:>9.2f}%")

print(f"\n=== Cumulative coverage ===")
print(f"  Total bonded:        {total_stake:>14,.0f} DOT")
print(f"  Attributed:          {cumulative_attr_stake:>14,.0f} DOT  ({100*cumulative_attr_stake/total_stake:.2f}%)")
print(f"  Still unattributed:  {unattr_stake:>14,.0f} DOT  ({100*unattr_stake/total_stake:.2f}%)")

# CEX vs Institutional vs Independent breakdown
cex_stake = sum(s["stake"] for c, s in by_class.items() if c.startswith("CEX:"))
inst_stake = sum(s["stake"] for c, s in by_class.items() if c.startswith("Institutional:"))
fundsrc_inst_stake = sum(s["stake"] for c, s in by_class.items() if c.startswith("FundingSource:") and c not in ("FundingSource:🧊 Iceberg Nodes 🧊",))
tvp_stake = sum(s["stake"] for c, s in by_class.items() if c.startswith("TVP:"))
indep_stake = sum(s["stake"] for c, s in by_class.items() if c == "Independent")
combined_institutional = inst_stake + fundsrc_inst_stake

print(f"\n=== Operator-type aggregates ===")
print(f"  CEX (verified Identity Pallet):     {cex_stake:>14,.0f} ({100*cex_stake/total_stake:.2f}%)")
print(f"  Institutional (Identity Pallet):    {inst_stake:>14,.0f} ({100*inst_stake/total_stake:.2f}%)")
print(f"  Institutional (Funding Source):     {fundsrc_inst_stake:>14,.0f} ({100*fundsrc_inst_stake/total_stake:.2f}%)")
print(f"  TVP-attributed (community ops):     {tvp_stake:>14,.0f} ({100*tvp_stake/total_stake:.2f}%)")
print(f"  Independent (verified non-CEX/inst): {indep_stake:>14,.0f} ({100*indep_stake/total_stake:.2f}%)")
print(f"  Still Unverified:                    {unattr_stake:>14,.0f} ({100*unattr_stake/total_stake:.2f}%)")

# Save
with open("/tmp/b2_phase4/dot_attribution_synthesis.json", "w") as f:
    json.dump({
        "by_class": {c: s for c, s in sorted_classes},
        "cumulative_attributed_dot": cumulative_attr_stake,
        "cumulative_attributed_pct": 100*cumulative_attr_stake/total_stake,
        "operator_type_aggregates": {
            "CEX_verified_pct": 100*cex_stake/total_stake,
            "Institutional_Identity_pct": 100*inst_stake/total_stake,
            "Institutional_FundingSource_pct": 100*fundsrc_inst_stake/total_stake,
            "TVP_attributed_pct": 100*tvp_stake/total_stake,
            "Independent_verified_pct": 100*indep_stake/total_stake,
            "still_unverified_pct": 100*unattr_stake/total_stake,
        },
        "validators_with_best_class": validators,
    }, f, default=str, indent=2)
