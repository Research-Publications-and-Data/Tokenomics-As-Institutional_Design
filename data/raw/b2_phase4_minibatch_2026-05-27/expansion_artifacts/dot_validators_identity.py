#!/usr/bin/env python3
"""Re-pull DOT validators with full identity + account-display fields."""
import json, urllib.request, time
from collections import defaultdict

API_KEY = "c8625edf41b845a393ff24fe5d3bb132"
UA = "Mozilla/5.0"
URL = "https://polkadot.api.subscan.io/api/scan/staking/validators"

# Pull only 600 unique (single full pass)
all_validators = []
seen_addr = set()
for page in range(0, 10):
    body = json.dumps({"row": 100, "page": page}).encode()
    req = urllib.request.Request(URL, data=body, headers={
        "Content-Type": "application/json", "User-Agent": UA, "X-API-Key": API_KEY,
    }, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            d = json.load(r)
        if d.get("code") != 0:
            break
        vals = d.get("data", {}).get("list", [])
        new = [v for v in vals if v.get("stash_account_display", {}).get("address") not in seen_addr]
        for v in new:
            seen_addr.add(v["stash_account_display"]["address"])
        all_validators.extend(new)
        print(f"  page {page}: {len(vals)} returned; {len(new)} new; total unique: {len(all_validators)}")
        if len(new) == 0 and page > 3:
            break
        time.sleep(0.4)
    except Exception as e:
        print(f"page {page} err: {e}")
        break

# Extract full identity info
PLANCK = 10**10
parsed = []
for v in all_validators:
    stash = v.get("stash_account_display", {})
    addr = stash.get("address", "")
    identity_obj = stash.get("identity", {})
    if isinstance(identity_obj, dict):
        people = stash.get("people", {})
        display_text = people.get("display", "") or stash.get("display", "")
        is_verified = bool(people.get("identity", False))
        judgments = people.get("judgements", [])
    else:
        display_text = stash.get("display", "")
        is_verified = bool(identity_obj)
        judgments = []
    
    bn = int(v.get("bonded_nominators", "0") or "0")
    bo = int(v.get("bonded_owner", "0") or "0")
    parsed.append({
        "address": addr,
        "display": display_text,
        "is_verified": is_verified,
        "n_judgments": len(judgments) if isinstance(judgments, list) else 0,
        "bonded_total_dot": (bn + bo) / PLANCK,
        "bonded_owner_dot": bo / PLANCK,
        "bonded_nominators_dot": bn / PLANCK,
        "count_nominators": v.get("count_nominators", 0),
    })

parsed.sort(key=lambda x: -x["bonded_total_dot"])

# Identify operator clusters based on display name patterns (case-insensitive substring match)
CEX_PATTERNS = {
    "Binance": ["binance"],
    "Kraken": ["kraken"],
    "Coinbase": ["coinbase"],
    "OKX": ["okx", "okcoin"],
    "Bybit": ["bybit"],
    "KuCoin": ["kucoin"],
    "Gate.io": ["gate.io", "gate_io", "gateio"],
    "Crypto.com": ["crypto.com", "crypto_com", "cdc"],
    "Bitfinex": ["bitfinex"],
    "Huobi": ["huobi"],
    "Gemini": ["gemini"],
    "BitMart": ["bitmart"],
    "MEXC": ["mexc"],
    "Bitvavo": ["bitvavo"],
    "Bitpanda": ["bitpanda"],
    "Bitstamp": ["bitstamp"],
    "Bitget": ["bitget"],
}

INSTITUTIONAL_PATTERNS = {
    "Figment": ["figment"],
    "RockX": ["rockx", "rock_x"],
    "Chainsafe": ["chainsafe", "chain_safe"],
    "Stakefish": ["stakefish", "stake.fish", "🐟"],
    "P2P Validator": ["p2p validator", "p2p.org"],
    "Bison Trails / Coinbase Cloud": ["bison trails", "coinbase cloud"],
    "Kiln": ["kiln"],
    "Anchorage": ["anchorage"],
    "Staked": ["staked.us", "staked "],
    "DSRV": ["dsrv"],
    "InfStones": ["infstones", "inf stones"],
    "Stakin": ["stakin"],
    "Blockdaemon": ["blockdaemon"],
    "Pier Two": ["pier two", "piertwo"],
    "Allnodes": ["allnodes"],
    "DothubValidator": ["dothub"],
    "Polkadotters": ["polkadotters"],
    "Stake.Plus": ["stake.plus", "stakeplus"],
    "Hashed": ["hashed"],
    "Zeeprime": ["zeeprime", "zee_prime"],
    "Brightlystake": ["brightly"],
    "Polkachu": ["polkachu"],
}

FOUNDATION_PATTERNS = {
    "Web3 Foundation": ["w3f", "web3 foundation", "web3foundation"],
    "Parity": ["parity"],
}

def classify(display):
    if not display:
        return "Unverified"
    d = display.lower()
    for entity, patterns in CEX_PATTERNS.items():
        if any(p in d for p in patterns):
            return f"CEX:{entity}"
    for entity, patterns in INSTITUTIONAL_PATTERNS.items():
        if any(p in d for p in patterns):
            return f"Institutional:{entity}"
    for entity, patterns in FOUNDATION_PATTERNS.items():
        if any(p in d for p in patterns):
            return f"Foundation:{entity}"
    return "Independent" if display else "Unverified"

# Classify
for v in parsed:
    v["operator_class"] = classify(v["display"])

# Aggregate by class
class_count = defaultdict(int)
class_stake = defaultdict(float)
for v in parsed:
    class_count[v["operator_class"]] += 1
    class_stake[v["operator_class"]] += v["bonded_total_dot"]

total_stake = sum(v["bonded_total_dot"] for v in parsed)

print(f"\nClassification summary (N={len(parsed)} unique validators):")
print(f"{'class':<35} {'count':>6} {'count_pct':>10} {'stake_dot':>15} {'stake_pct':>10}")
sorted_classes = sorted(class_count.items(), key=lambda x: -class_stake[x[0]])
for cls, c in sorted_classes:
    sp = 100 * class_stake[cls] / total_stake if total_stake else 0
    cp = 100 * c / len(parsed)
    print(f"{cls:<35} {c:>6} {cp:>9.2f}% {class_stake[cls]:>15,.0f} {sp:>9.2f}%")

# Top-by-category
print(f"\nTotal classified entities (CEX + Institutional + Foundation):")
cex_total = sum(c for cls, c in class_count.items() if cls.startswith("CEX:"))
inst_total = sum(c for cls, c in class_count.items() if cls.startswith("Institutional:"))
fdn_total = sum(c for cls, c in class_count.items() if cls.startswith("Foundation:"))
indep_total = class_count.get("Independent", 0)
unverif_total = class_count.get("Unverified", 0)
cex_stake = sum(class_stake[cls] for cls in class_stake if cls.startswith("CEX:"))
inst_stake = sum(class_stake[cls] for cls in class_stake if cls.startswith("Institutional:"))
print(f"  CEX:          {cex_total} validators ({100*cex_total/len(parsed):.2f}%) / {cex_stake:,.0f} DOT ({100*cex_stake/total_stake:.2f}% stake)")
print(f"  Institutional: {inst_total} validators ({100*inst_total/len(parsed):.2f}%) / {inst_stake:,.0f} DOT ({100*inst_stake/total_stake:.2f}% stake)")
print(f"  Foundation:    {fdn_total} validators")
print(f"  Independent:   {indep_total} validators")
print(f"  Unverified:    {unverif_total} validators")

# Top-15 by stake
print(f"\nTop-15 validators by bonded stake (with class):")
for i, v in enumerate(parsed[:15], 1):
    verified = "✓" if v["is_verified"] else " "
    print(f"  #{i:>2}  {verified} {v['display'][:35]:<35} {v['bonded_total_dot']:>10,.0f} DOT  cls={v['operator_class']}")

# Save full data
with open("/tmp/b2_phase4/dot_validators_classified.json", "w") as f:
    json.dump({
        "n_unique": len(parsed),
        "total_bonded_dot": total_stake,
        "class_summary": {cls: {"count": c, "stake_dot": class_stake[cls], "stake_pct": 100*class_stake[cls]/total_stake} for cls, c in sorted_classes},
        "validators": parsed,
    }, f, default=str, indent=2)
