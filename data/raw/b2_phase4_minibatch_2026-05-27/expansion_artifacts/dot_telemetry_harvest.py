#!/usr/bin/env python3
"""Harvest Polkadot Telemetry WebSocket feed to identify validator nodes."""
import asyncio, json, sys
import websockets

# Polkadot mainnet genesis hash (used to subscribe to network on telemetry)
POLKADOT_GENESIS = "0x91b171bb158e2d3848fa23a9f1c25182fb8e20313b2c1eb49219da7a70ce90c3"

# Telemetry feed URL
TELEMETRY_URL = "wss://feed.telemetry.polkadot.io/feed/"
# Backup: TELEMETRY_URL = "wss://feed.telemetry.polkadot.io/feed/0"

HARVEST_SECONDS = 30

async def harvest():
    print(f"Connecting to {TELEMETRY_URL}...")
    try:
        async with websockets.connect(TELEMETRY_URL, max_size=10*1024*1024) as ws:
            # Subscribe to Polkadot network
            await ws.send(f"subscribe:{POLKADOT_GENESIS}")
            print(f"Subscribed to Polkadot genesis {POLKADOT_GENESIS[:16]}...; harvesting for {HARVEST_SECONDS}s")
            
            nodes = {}  # node_id -> {name, version, hardware, network_id, location, ...}
            msg_count = 0
            start = asyncio.get_event_loop().time()
            
            try:
                while True:
                    elapsed = asyncio.get_event_loop().time() - start
                    if elapsed > HARVEST_SECONDS:
                        break
                    timeout = max(0.5, HARVEST_SECONDS - elapsed)
                    msg = await asyncio.wait_for(ws.recv(), timeout=timeout)
                    msg_count += 1
                    
                    # Messages can be binary or text; telemetry uses text JSON array
                    if isinstance(msg, bytes):
                        msg = msg.decode("utf-8", errors="replace")
                    
                    # Telemetry msg format: alternating [action_id, payload, action_id, payload, ...]
                    try:
                        data = json.loads(msg)
                    except json.JSONDecodeError:
                        continue
                    
                    if not isinstance(data, list):
                        continue
                    
                    # Parse pairs
                    for i in range(0, len(data) - 1, 2):
                        action = data[i]
                        payload = data[i + 1] if i + 1 < len(data) else None
                        if payload is None:
                            continue
                        
                        # Action 3 = added_node: [node_id, [name, impl, version, validator_addr, network_id], stats, io, hardware, location, startup_time, hwbench]
                        # Action 4 = removed_node: [node_id]
                        # See https://github.com/paritytech/substrate-telemetry/blob/master/feed/src/types.rs
                        if action == 3 and isinstance(payload, list) and len(payload) >= 2:
                            node_id = payload[0]
                            details = payload[1] if len(payload) > 1 else []
                            location = payload[5] if len(payload) > 5 else None
                            hwbench = payload[7] if len(payload) > 7 else None
                            if isinstance(details, list) and len(details) >= 5:
                                name = details[0]
                                impl = details[1]
                                version = details[2]
                                validator_addr = details[3] if len(details) > 3 else None
                                network_id = details[4] if len(details) > 4 else None
                                nodes[node_id] = {
                                    "name": name,
                                    "impl": impl,
                                    "version": version,
                                    "validator_addr": validator_addr,
                                    "network_id": network_id,
                                    "location": location,
                                    "hwbench": hwbench,
                                }
                        elif action == 0 and isinstance(payload, list):
                            # Feed version info
                            print(f"  Feed action 0 (version): {payload}")
            except asyncio.TimeoutError:
                pass
            
            print(f"\nHarvested {len(nodes)} nodes; {msg_count} messages processed")
            return nodes
    except Exception as e:
        print(f"WebSocket error: {type(e).__name__}: {e}", file=sys.stderr)
        return {}

nodes = asyncio.run(harvest())

# Filter to validators only (validator_addr is not None or empty)
validator_nodes = {nid: n for nid, n in nodes.items() if n.get("validator_addr")}
non_validator_nodes = {nid: n for nid, n in nodes.items() if not n.get("validator_addr")}
print(f"\n  Validators: {len(validator_nodes)}")
print(f"  Non-validator nodes (full/light clients): {len(non_validator_nodes)}")

# Cross-reference with our 600 validators
our_data = json.load(open("/tmp/b2_phase4/dot_validators_classified.json"))
our_addrs = {v["address"]: v for v in our_data["validators"]}

matched = []
for nid, n in validator_nodes.items():
    addr = n.get("validator_addr")
    if addr and addr in our_addrs:
        matched.append({"node_id": nid, "telemetry": n, "our_validator": our_addrs[addr]})

print(f"\nValidators matched to our 600-set: {len(matched)}")
unverified_resolved = [m for m in matched if m["our_validator"]["operator_class"] == "Unverified"]
print(f"  Of which were Unverified (newly resolved via Telemetry): {len(unverified_resolved)}")

# Sample top-by-stake newly resolved
unverified_resolved.sort(key=lambda x: -x["our_validator"]["bonded_total_dot"])
print(f"\nTop-20 newly-resolved via Telemetry (Unverified → telemetry node name):")
for i, m in enumerate(unverified_resolved[:20], 1):
    name = m["telemetry"]["name"][:40]
    impl = m["telemetry"]["impl"]
    loc = m["telemetry"].get("location")
    if isinstance(loc, list) and len(loc) >= 3:
        loc_str = f"{loc[0]:.1f},{loc[1]:.1f} {loc[2]}"
    else:
        loc_str = ""
    stake = m["our_validator"]["bonded_total_dot"]
    print(f"  #{i:>2}  {name:<40}  {stake:>10,.0f} DOT  impl='{impl}' loc='{loc_str}'")

# Save
with open("/tmp/b2_phase4/dot_telemetry_harvest.json", "w") as f:
    json.dump({
        "total_nodes_harvested": len(nodes),
        "validator_nodes": len(validator_nodes),
        "matched_to_our_set": len(matched),
        "newly_resolved_unverified": len(unverified_resolved),
        "matches": matched,
    }, f, default=str, indent=2)

print(f"\nTotal coverage after Telemetry harvest:")
total_resolved = len(matched)
total_unverified = sum(1 for v in our_data["validators"] if v["operator_class"] == "Unverified")
print(f"  Telemetry matched: {len(matched)} of 600 ({100*len(matched)/600:.1f}%)")
print(f"  Newly resolved (from Unverified): {len(unverified_resolved)} of {total_unverified} Unverified ({100*len(unverified_resolved)/total_unverified:.1f}%)")
