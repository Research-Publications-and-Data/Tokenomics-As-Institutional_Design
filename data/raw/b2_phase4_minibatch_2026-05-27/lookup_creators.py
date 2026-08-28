#!/usr/bin/env python3
"""Lookup contract creator + first-tx data for ambiguous proxies."""
import json, urllib.request, urllib.parse, time
import os

API_KEY = os.environ["ETHERSCAN_API_KEY"]
BASE = "https://api.etherscan.io/v2/api"

# Ambiguous proxies needing creator-context verification
TARGETS = [
    ("FXS-1", "0x36cb65c1967a0fb0eee11569c51c2f2aa1ca6f6d"),
    ("FXS-12-multisig", "0xb1748c79709f4ba2dd82834b8c82d4a505003f27"),
    ("SNX-1", "0xffffffaeff0b96ea8e4f94b2253f31abdd875847"),
    ("SNX-16", "0x99f4176ee457afedffcb1839c7ab7a030a5e4a92"),
    ("GNO-1-Disbursement", "0xec83f750adfe0e52a8b0dba6eeb6be5ba0bee535"),
    ("GNO-4-Safe", "0x849d52316331967b6ff1198e5e32a0eb168d039d"),
    ("GNO-5-Disbursement", "0x604e4557e9020841f4e8eb98148de3d3cdea350c"),
    ("GNO-6-Mintr", "0x9d94ef33e7f8087117f85b3ff7b1d8f27e4053d5"),
    ("GNO-8-Safe", "0x4f8ad938eba0cd19155a835f617317a6e788c868"),
    ("GNO-11-Safe", "0xae5fb390e5c4fa1962e39e98dbfb0ed8055ed7a9"),
    ("multi-protocol-d2dd", "0xd2dd7b597fd2435b6db61ddf48544fd931e6869f"),
    ("FXS-3", "0xccfc07b3f23bf293e7363495fa2f9509bf72ecf1"),
    ("SNX-4", "0x3a5cc8689d1b0cef2c317bc5c0ad6ce88b27d597"),
    ("SNX-5", "0x76ec5a0d3632b2133d9f1980903305b62678fbd3"),
]

# 1) Try getcontractcreation (returns creator address + tx hash)
def get_creation(addr):
    params = {"chainid": 1, "module": "contract", "action": "getcontractcreation",
              "contractaddresses": addr, "apikey": API_KEY}
    url = BASE + "?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=10) as r:
        d = json.load(r)
    if d.get("status") == "1" and d.get("result"):
        return d["result"][0]
    return None

# 2) For pure proxies: read implementation slot via eth_getStorageAt
def get_impl(addr):
    # EIP-1967 impl slot
    slot = "0x360894a13ba1a3210667c828492db98dcbf07d44c0b9ad9e8c4d4d6c6d6f"  # not exact
    # Just use the "implementation" from sourcecode result already; this is a fallback
    return None

results = {}
for label, addr in TARGETS:
    try:
        c = get_creation(addr)
        results[label] = {"address": addr, "creation": c}
        creator = c.get("contractCreator") if c else "n/a"
        print(f"  {label}: creator={creator}")
        time.sleep(0.25)
    except Exception as e:
        print(f"  {label}: ERR {e}")

with open("/tmp/b2_phase4/etherscan_creators.json", "w") as f:
    json.dump(results, f, indent=2)
