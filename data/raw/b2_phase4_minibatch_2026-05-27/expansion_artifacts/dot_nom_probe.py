#!/usr/bin/env python3
"""Find correct nominators-of-validator endpoint."""
import json, urllib.request

API_KEY = "c8625edf41b845a393ff24fe5d3bb132"
UA = "Mozilla/5.0"

test = "114SUbKCXjmb9czpWTtS3JANSmNRwVa4mmsMrWYpRG1kDH5"  # BINANCE_STAKE_9

variants = [
    # (endpoint, payload, description)
    ("/api/scan/staking/nominators", {"address": test, "row": 50, "page": 0, "is_validator": True}, "is_validator flag"),
    ("/api/scan/staking/nominators", {"validator": test, "row": 50, "page": 0}, "validator key"),
    ("/api/scan/staking/nominators", {"stash": test, "row": 50, "page": 0}, "stash key"),
    ("/api/scan/staking/voter", {"address": test, "row": 50, "page": 0}, "voter endpoint"),
    ("/api/scan/staking/era_validator_history", {"stash": test, "row": 50, "page": 0}, "era history"),
    ("/api/scan/staking/voter_history", {"address": test, "row": 50, "page": 0}, "voter history"),
]

for path, payload, desc in variants:
    body = json.dumps(payload).encode()
    req = urllib.request.Request(f"https://polkadot.api.subscan.io{path}", data=body, headers={
        "Content-Type": "application/json", "User-Agent": UA, "X-API-Key": API_KEY,
    }, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            d = json.load(r)
        code = d.get("code", "?")
        msg = d.get("message", "")[:60]
        if code == 0:
            data = d.get("data", {})
            if isinstance(data, dict):
                count = data.get("count", 0)
                items = data.get("list", [])
                print(f"  ✓ {path} [{desc}]: count={count}, items={len(items)}")
                if items:
                    print(f"    sample[0]: {json.dumps(items[0], default=str)[:250]}")
            else:
                print(f"  ✓ {path} [{desc}]: data type {type(data).__name__}")
        else:
            print(f"  {path} [{desc}]: code={code} '{msg}'")
    except urllib.error.HTTPError as e:
        body = ""
        try: body = e.read().decode("utf-8")[:80]
        except: pass
        print(f"  {path} [{desc}]: HTTP {e.code} {body}")
    except Exception as e:
        print(f"  {path} [{desc}]: err {e}")
