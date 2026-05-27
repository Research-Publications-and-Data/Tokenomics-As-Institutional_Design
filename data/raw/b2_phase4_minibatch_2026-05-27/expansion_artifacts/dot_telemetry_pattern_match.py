#!/usr/bin/env python3
"""Cross-match telemetry NODE NAMES against our validator set (operators may run multiple validators)."""
import json, re

t = json.load(open("/tmp/b2_phase4/dot_telemetry_harvest.json"))
our = json.load(open("/tmp/b2_phase4/dot_validators_classified.json"))

# Build telemetry node-name dict (only those with validator_addr indicating they're acting as validators)
tel_names = {}
for m in t.get("matches", []):
    tel_names[m["telemetry"]["name"]] = m

# Re-extract all telemetry nodes from saved data (need to re-run since matches was 0)
# Use a quick re-pull
import asyncio, websockets

POLKADOT = "0x91b171bb158e2d3848fa23a9f1c25182fb8e20313b2c1eb49219da7a70ce90c3"

async def harvest_short():
    nodes = []
    async with websockets.connect("wss://feed.telemetry.polkadot.io/feed/", max_size=10*1024*1024) as ws:
        await ws.send(f"subscribe:{POLKADOT}")
        start = asyncio.get_event_loop().time()
        while asyncio.get_event_loop().time() - start < 15:
            try:
                msg = await asyncio.wait_for(ws.recv(), timeout=3)
                if isinstance(msg, bytes): msg = msg.decode("utf-8", "replace")
                data = json.loads(msg)
                if not isinstance(data, list): continue
                for i in range(0, len(data) - 1, 2):
                    action = data[i]
                    payload = data[i+1]
                    if action == 3 and isinstance(payload, list) and len(payload) >= 2:
                        details = payload[1] if len(payload) > 1 else []
                        if isinstance(details, list) and len(details) >= 4:
                            name = details[0]
                            validator_addr = details[3]
                            network_id = details[4] if len(details) > 4 else None
                            location = payload[5] if len(payload) > 5 else None
                            nodes.append({
                                "name": name,
                                "validator_addr": validator_addr,
                                "is_validator": bool(validator_addr and validator_addr != "<unknown>"),
                                "network_id": network_id,
                                "location": location,
                            })
            except asyncio.TimeoutError:
                continue
    return nodes

nodes = asyncio.run(harvest_short())
print(f"Telemetry nodes harvested: {len(nodes)}")
validators = [n for n in nodes if n["is_validator"]]
print(f"Telemetry validator nodes: {len(validators)}")

# Build telemetry name → addresses map (one name may have multiple addresses if operator runs multiple)
from collections import defaultdict
name_to_addrs = defaultdict(set)
addr_to_name = {}
for n in validators:
    name_to_addrs[n["name"]].add(n["validator_addr"])
    addr_to_name[n["validator_addr"]] = n["name"]

print(f"\nUnique telemetry validator names: {len(name_to_addrs)}")

# Build operator-clusters from telemetry: same operator likely uses same name-prefix
# E.g., "Meria 02" / "Meria 03" → operator "Meria"
def operator_prefix(name):
    # Strip trailing numbers, dashes, special chars
    n = re.sub(r'[\s\-_]+\d+$', '', name.strip())  # "Meria 02" -> "Meria"
    n = re.sub(r'[\s\-_]+v\d+(\.\d+)*$', '', n, flags=re.I)
    return n.strip().lower()

tel_operators = defaultdict(list)
for name, addrs in name_to_addrs.items():
    op = operator_prefix(name)
    tel_operators[op].extend([(name, a) for a in addrs])

# Direct address match
our_addrs = set(v["address"] for v in our["validators"])
our_by_addr = {v["address"]: v for v in our["validators"]}

direct_matches = []
for n in validators:
    if n["validator_addr"] in our_addrs:
        direct_matches.append({"telemetry": n, "our": our_by_addr[n["validator_addr"]]})

print(f"\nDirect address matches (telemetry validator_addr ∈ our 600-set): {len(direct_matches)}")
for m in direct_matches[:10]:
    o = m["our"]
    t_node = m["telemetry"]
    print(f"  '{t_node['name'][:30]}' → our address={o['address'][:20]}... stake={o['bonded_total_dot']:,.0f} prev_class={o['operator_class']}")

# Pattern-match: telemetry operator-prefix → our validator display
# For each operator with >=2 telemetry validators, check if any of those validators (or any with same prefix) match
print(f"\nMulti-validator operators detected in telemetry (>=2 validators with same prefix):")
multi_ops = {op: v for op, v in tel_operators.items() if len(set(a for _, a in v)) >= 2}
print(f"Total multi-validator operators in telemetry: {len(multi_ops)}")
sorted_ops = sorted(multi_ops.items(), key=lambda x: -len(set(a for _, a in x[1])))
for op, validators_list in sorted_ops[:20]:
    addrs = set(a for _, a in validators_list)
    names = sorted(set(n for n, _ in validators_list))
    # Check how many of these addresses are in our 600-set
    in_ours = sum(1 for a in addrs if a in our_addrs)
    # Check if any our validator has matching display prefix
    our_match_count = sum(1 for v in our["validators"] if (v["display"] or "").lower().startswith(op[:10]))
    print(f"  operator='{op:<30}' tel_validators={len(addrs):>3} in_our_set={in_ours} our_disp_prefix_match={our_match_count}")

# Save
with open("/tmp/b2_phase4/dot_telemetry_match.json", "w") as f:
    json.dump({
        "telemetry_validators_total": len(validators),
        "unique_telemetry_names": len(name_to_addrs),
        "direct_address_matches": len(direct_matches),
        "multi_validator_operators_in_telemetry": len(multi_ops),
        "operators_with_multiple_validators": [
            {"operator": op, "n_validators_telemetry": len(set(a for _, a in v)), "addresses": sorted(set(a for _, a in v))}
            for op, v in sorted_ops if len(set(a for _, a in v)) >= 2
        ],
    }, f, default=str, indent=2)
