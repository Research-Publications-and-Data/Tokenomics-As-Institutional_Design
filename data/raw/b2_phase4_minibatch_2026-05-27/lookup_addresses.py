#!/usr/bin/env python3
"""Lookup contract source code names via Etherscan API for PCA classification."""
import json, urllib.request, urllib.parse, time, sys
import os

API_KEY = os.environ["ETHERSCAN_API_KEY"]
BASE = "https://api.etherscan.io/v2/api"

def lookup(addr, chainid=1):
    params = {
        "chainid": chainid,
        "module": "contract",
        "action": "getsourcecode",
        "address": addr,
        "apikey": API_KEY,
    }
    url = BASE + "?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            d = json.load(r)
        if d.get("status") == "1" and d.get("result"):
            res = d["result"][0]
            return {
                "contract_name": res.get("ContractName", ""),
                "compiler": res.get("CompilerVersion", ""),
                "is_proxy": res.get("Proxy", "0") == "1",
                "implementation": res.get("Implementation", ""),
                "license": res.get("LicenseType", ""),
                "abi_present": bool(res.get("ABI") and res.get("ABI") != "Contract source code not verified"),
            }
        return {"error": d.get("message", "unknown")}
    except Exception as e:
        return {"error": str(e)}

PROTOCOLS = {
    "FXS": "/tmp/b2_phase4/fxs_holders.json",
    "SNX": "/tmp/b2_phase4/snx_holders.json",
    "GNO": "/tmp/b2_phase4/gno_holders.json",
}

results = {}
for sym, path in PROTOCOLS.items():
    d = json.load(open(path))
    h = d.get("holders", [])
    print(f"\n=== {sym} top-20 Etherscan lookup ===")
    sym_results = []
    for i, r in enumerate(h[:20], 1):
        addr = r["wallet_address"]
        info = lookup(addr)
        sym_results.append({"rank": i, "address": addr, "balance_raw": r["balance"], "first_acquired": r["first_acquired"], **info})
        name = info.get("contract_name", "")
        err = info.get("error", "")
        flag = "PROXY" if info.get("is_proxy") else ""
        print(f"  #{i:>2}  {addr}  name='{name}' {flag} {err}")
        time.sleep(0.25)  # rate-limit-safe
    results[sym] = sym_results

with open("/tmp/b2_phase4/etherscan_labels.json", "w") as f:
    json.dump(results, f, indent=2)
print("\nWrote /tmp/b2_phase4/etherscan_labels.json")
