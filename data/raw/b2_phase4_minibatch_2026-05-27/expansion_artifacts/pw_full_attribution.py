#!/usr/bin/env python3
"""Bulk-fetch Polkawatch per-operator validator-address mapping."""
import urllib.request, urllib.error, json, time, sys

UA = "Mozilla/5.0"
BASE = "https://polkadot-v2-api.polkawatch.app/ddp/operator"

# Get overview first
overview = json.load(open("/tmp/b2_phase4/pw_op_all_30.json"))
operators = overview.get("operatorDistributionDetail", [])
print(f"Total operators in Polkawatch overview: {len(operators)}", flush=True)

# Per-operator validator details
all_mappings = {}  # validator_addr → {"operator_id", "operator_name", ...}
operator_validators = {}  # operator_id → list of validator records

# Cap at 200 (all of them per overview)
for i, op in enumerate(operators, 1):
    op_id = op["Id"]
    op_name = op["ValidationGroup"]
    n_validators = op["Validators"]
    url = f"{BASE}/{op_id}/all/30.json"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=20) as r:
            d = json.load(r)
        nodes = d.get("nodeDistributionDetail", [])
        operator_validators[op_id] = {"name": op_name, "n_polkawatch": n_validators, "validators": nodes}
        for n in nodes:
            v_addr = n["Id"]
            all_mappings[v_addr] = {
                "operator_id": op_id,
                "operator_name": op_name,
                "validator_display": n.get("Validator", ""),
                "LastRegion": n.get("LastRegion", ""),
                "LastCountry": n.get("LastCountry", ""),
                "LastNetwork": n.get("LastNetwork", ""),
                "Nominators": n.get("Nominators", 0),
                "TokenRewards": n.get("TokenRewards", 0),
            }
        if i % 20 == 0 or i == len(operators):
            print(f"  {i}/{len(operators)} operators processed; total validators mapped: {len(all_mappings)}", flush=True)
        time.sleep(0.15)
    except urllib.error.HTTPError as e:
        if i <= 3:
            print(f"  {i}/{len(operators)} HTTP {e.code}: {op_name}")
    except Exception as e:
        if i <= 3:
            print(f"  {i}/{len(operators)} ERR: {op_name}: {e}")

print(f"\nFinal: {len(all_mappings)} validator-stash addresses mapped to operators across {len(operator_validators)} operators")

# Save
with open("/tmp/b2_phase4/pw_full_mapping.json", "w") as f:
    json.dump({
        "operators_total": len(operator_validators),
        "validators_mapped": len(all_mappings),
        "validator_to_operator": all_mappings,
        "operators_to_validators": {k: {"name": v["name"], "n_polkawatch": v["n_polkawatch"], "addresses": [n["Id"] for n in v["validators"]]} for k, v in operator_validators.items()},
    }, f, default=str, indent=2)

# Cross-reference with our 600
our = json.load(open("/tmp/b2_phase4/dot_validators_classified.json"))
our_addrs = {v["address"]: v for v in our["validators"]}
total_stake = our["total_bonded_dot"]

newly_attributed = 0
already_attributed = 0
not_in_our_set = 0

new_attribution_stake = 0.0
for v_addr, mapping in all_mappings.items():
    if v_addr in our_addrs:
        v = our_addrs[v_addr]
        if v["operator_class"] == "Unverified":
            newly_attributed += 1
            new_attribution_stake += v["bonded_total_dot"]
            v["polkawatch_operator"] = mapping["operator_name"]
        else:
            already_attributed += 1
    else:
        not_in_our_set += 1

print(f"\n=== Cross-reference with our 600-validator set ===")
print(f"  Polkawatch-mapped validators total: {len(all_mappings)}")
print(f"    In our 600-set (already verified): {already_attributed}")
print(f"    In our 600-set (was UNVERIFIED, now resolved): {newly_attributed}")
print(f"    Not in our 600-set (Polkawatch tracks but Subscan validators endpoint didn't return): {not_in_our_set}")
print(f"  Newly-attributed stake: {new_attribution_stake:,.0f} DOT ({100*new_attribution_stake/total_stake:.2f}% of total)")

# Updated coverage
total_now_unverif = sum(1 for v in our["validators"] if v["operator_class"] == "Unverified" and "polkawatch_operator" not in v)
total_now_unverif_stake = sum(v["bonded_total_dot"] for v in our["validators"] if v["operator_class"] == "Unverified" and "polkawatch_operator" not in v)
print(f"\nAfter Polkawatch direct attribution:")
print(f"  Remaining unverified: {total_now_unverif} / 600 ({100*total_now_unverif/600:.1f}%)")
print(f"  Remaining unverified stake: {total_now_unverif_stake:,.0f} DOT ({100*total_now_unverif_stake/total_stake:.2f}%)")
