#!/usr/bin/env python3
"""Polkawatch's 147 operator universe (per author paste 2026-05-27).
Use for pattern-matching against Identity Pallet display names + funding-source displays.
"""
import json, re
from collections import defaultdict

# All 147 Polkawatch operators ranked by rewards (from author paste 2026-05-27)
# Format: (operator_name, n_validators_tracked_polkawatch)
POLKAWATCH_OPERATORS = [
    # Rows 1-50
    ("pos.dog", 38), ("P2P.ORG", 20), ("Jaco", 9), ("Coinbase", 12),
    ("Zug Capital", 11), ("Iceberg Nodes", 8), ("LEGEND", 6), ("ParaNodes.io", 6),
    ("DOZENODES.COM", 5), ("cryptostake.com", 4), ("Meria", 5), ("Novasama", 5),
    ("SAXEMBERG", 3), ("turboflakes.io", 3), ("HODL.FARM", 3), ("Blockseeker.io", 3),
    ("Khastor", 3), ("talisman.xyz", 3), ("GameTheory", 3), ("Staker Space", 4),
    ("EXNESS.COM", 6), ("Polkadotters", 3), ("Coinstudio", 3),
    ("helixstreet.foundation", 3), ("GATOTECH", 3), ("Mile", 3),
    ("ProStakers.com", 2), ("DRAGONSTAKE", 2), ("Staking4All", 3),
    ("YellowFin Tuna", 2), ("HELIKON", 2), ("Joe", 2), ("Swiss Bond", 3),
    ("ValidOrange", 2), ("ECH0.RE", 2), ("PROOF.COMPUTER", 2), ("Kraken01", 2),
    ("BESTVALIDATOR", 2), ("PERMANENCE DAO", 2), ("ITRocket", 2),
    ("HYPERSPEED", 2), ("Chris-Staking", 2), ("openbitlab", 2),
    ("RADIUMBLOCK.COM", 3), ("Zetetic Validator", 2), ("Encointer", 2),
    ("digitalghost.xyz", 2), ("pathrocknetwork", 2), ("HoneyStake.xyz", 2),
    ("deigenvektor.io", 2),
    # Rows 51-100
    ("vonFlandern", 2), ("Zugian Duck", 4), ("NEWDEAL", 2), ("BUENO VALIDATORO", 2),
    ("Eric", 2), ("ValidAndina", 2), ("cedric.AAA", 2), ("ajuna.io", 2),
    ("INFRASTRUCTURE CORPORATION", 3), ("OnFinality.io", 2), ("STEAKCHEF", 2),
    ("hirish", 2), ("VALIDEXIS", 2), ("locozoo", 2), ("luizv", 2),
    ("BRC", 5), ("APERTURE MINING", 2), ("DotSkull", 2), ("ZKV", 2),
    ("COSMOON", 2), ("Stake Magnet", 1), ("GuruStaking", 1), ("anvel", 1),
    ("KUZO STAKE", 1), ("ALFASTAKE", 1), ("ANAMIX", 1), ("VF Validierung", 1),
    ("COSMOTRON", 1), ("GTSTAKING", 1), ("SNZPool", 1), ("WDMASTER", 1),
    ("POLKACHU.COM", 1), ("Sio34", 1), ("HYPERSPHERE", 1), ("Nodeasy", 1),
    ("Stakeworld.io", 1), ("KeepNode", 1), ("Dionysus", 1), ("Amforc", 2),
    ("Titan Nodes", 1), ("CRYPTOBEES.XYZ", 1), ("STAKE HULK", 1),
    ("LuckyFriday.io", 1), ("ROTKO.NET", 1), ("Taichung", 1), ("SubWallet", 2),
    ("Merkletribe", 1), ("P2P STAKING", 1), ("dakkk", 1), ("decentraDOT.com", 1),
    ("StakedTech", 1),
    # Rows 101-147
    ("Blockdaemon", 1), ("Cointelegraph", 1), ("Sik | crifferent.de", 1),
    ("stateless_money", 1), ("Stakebaby", 1), ("General-Beck", 1),
    ("Stampede", 1), ("Figment 7", 1), ("Figment 3", 1), ("Ryabina", 1),
    ("Figment 1", 1), ("Figment 2", 1), ("Luganodes", 1), ("Figment 4", 1),
    ("dotvalidators.com", 1), ("RockX_Polkadot3", 1), ("Figment 5", 1),
    ("Cypher Labs", 1), ("CP287-CLOUDWALK", 1), ("Figment 8", 1),
    ("RockX_Polkadot", 1), ("SenseiNode", 1), ("Animoca Brands", 1),
    ("prematurata", 1), ("ChainSafe-Polkadot-Validator", 1), ("Grimface", 1),
    ("Tesla", 1), ("Hsinchu", 1), ("ALESSIO", 1), ("Bodhi-Validator", 1),
    ("KOLKADOT.COM", 1), ("Current", 1), ("SUNSHINEAUTOSDOT", 1), ("TUXEDO", 2),
    ("INTERWEB", 2), ("Paramito", 1), ("Stake Plus", 1),
    ("PromoTeam Validator", 1), ("POWERSTAKE POLKADOT", 1), ("Uno Staking", 1),
    ("snf dot validator", 1), ("Stake Kat", 1), ("wiggumdot", 1), ("AZIMUT", 1),
    ("PureStake", 1), ("KIRA Staking", 1),
]

# Classification of each operator into CEX / Institutional / Community pools / Independent
OPERATOR_CLASS = {
    # CEX
    "Coinbase": "CEX",
    "Kraken01": "CEX",
    "EXNESS.COM": "CEX",  # Exness is a major broker
    # Institutional staking providers (verified-by-reputation as professional services)
    "pos.dog": "Institutional",
    "P2P.ORG": "Institutional",
    "ParaNodes.io": "Institutional",
    "Iceberg Nodes": "Institutional",
    "Blockdaemon": "Institutional",
    "Figment 1": "Institutional", "Figment 2": "Institutional",
    "Figment 3": "Institutional", "Figment 4": "Institutional",
    "Figment 5": "Institutional", "Figment 7": "Institutional",
    "Figment 8": "Institutional",
    "RockX_Polkadot": "Institutional", "RockX_Polkadot3": "Institutional",
    "ChainSafe-Polkadot-Validator": "Institutional",
    "Luganodes": "Institutional",
    "OnFinality.io": "Institutional",
    "Amforc": "Institutional",
    "PureStake": "Institutional",
    "POLKACHU.COM": "Institutional",
    "SenseiNode": "Institutional",
    "Stakeworld.io": "Institutional",
    "P2P STAKING": "Institutional",
    "INFRASTRUCTURE CORPORATION": "Institutional",
    "RADIUMBLOCK.COM": "Institutional",
    "StakedTech": "Institutional",
    "PROOF.COMPUTER": "Institutional",
    "talisman.xyz": "Institutional",
    "ROTKO.NET": "Institutional",
    "dotvalidators.com": "Institutional",
    "BRC": "Institutional",
    "Animoca Brands": "Institutional_VC",  # Crypto VC fund
    "Zug Capital": "Institutional_VC",  # Crypto VC
    "Cypher Labs": "Institutional_VC",
    "ZKV": "Institutional_VC",
    "Cointelegraph": "Institutional_Media",  # Crypto media company
    "talisman.xyz": "Institutional_Wallet",  # Polkadot wallet
    "SubWallet": "Institutional_Wallet",
    # Community / pool operators (TVP-like)
    # Many small operators tracked by Polkawatch
}

def classify(name):
    return OPERATOR_CLASS.get(name, "Independent_or_Community")

# Build lowercase-tokens for pattern matching against validator displays
def to_pattern(name):
    # Generate alternative patterns: lowercase, strip emoji, strip whitespace/punctuation
    n = name.lower()
    base = re.sub(r'[\s\-_\.]+', '', n)  # Compact version
    return n, base, n.split()[0] if name.split() else n

# Total tracked validators per operator
total_validators = sum(n for _, n in POLKAWATCH_OPERATORS)
print(f"Polkawatch operators: {len(POLKAWATCH_OPERATORS)}")
print(f"Total validators tracked: {total_validators}")
print()

# Cross-reference against our 600
our = json.load(open("/tmp/b2_phase4/dot_validators_classified.json"))
our_validators = our["validators"]
total_stake = our["total_bonded_dot"]

# Build operator → patterns map
operator_patterns = {}
for op, n_val in POLKAWATCH_OPERATORS:
    full, base, first_token = to_pattern(op)
    operator_patterns[op] = {
        "full": full, "base": base, "first_token": first_token,
        "n_validators_polkawatch": n_val,
        "class": classify(op),
    }

# Match our validator displays against Polkawatch patterns
matches = defaultdict(list)  # operator → [our_validators]
for v in our_validators:
    display = (v["display"] or "").lower()
    if not display:
        continue
    display_compact = re.sub(r'[\s\-_\.]+', '', display)

    for op, patterns in operator_patterns.items():
        full_l = patterns["full"]
        base_l = patterns["base"]
        # Substring match on either compact form or full form
        if full_l in display or base_l in display_compact:
            matches[op].append(v)
            break
        # First-token match for short operator names (avoid false positives)
        if len(full_l) >= 5 and full_l == display.split()[0] if display.split() else False:
            matches[op].append(v)
            break

# Report match results
print(f"Polkawatch operators matched in our 600-set: {sum(1 for op, vs in matches.items() if vs)}")
print(f"\nMatched validators per operator (sorted by class):")

by_class = defaultdict(list)
for op, vs in matches.items():
    if vs:
        cls = operator_patterns[op]["class"]
        by_class[cls].append((op, vs))

for cls in sorted(by_class.keys()):
    print(f"\n  [{cls}]:")
    for op, vs in sorted(by_class[cls], key=lambda x: -sum(v["bonded_total_dot"] for v in x[1])):
        stake = sum(v["bonded_total_dot"] for v in vs)
        n_pw = operator_patterns[op]["n_validators_polkawatch"]
        print(f"    {op:<35} matched={len(vs):>2}  (PW tracks {n_pw}) stake={stake:>10,.0f} DOT  ({100*stake/total_stake:.3f}%)")

# Total class-level aggregates
print(f"\n=== Operator-class aggregates (Polkawatch-pattern matches) ===")
for cls in sorted(by_class.keys()):
    ops_in_class = by_class[cls]
    total_validators_cls = sum(len(vs) for _, vs in ops_in_class)
    total_stake_cls = sum(sum(v["bonded_total_dot"] for v in vs) for _, vs in ops_in_class)
    print(f"  {cls:<35} {len(ops_in_class):>3} operators, {total_validators_cls:>3} matched validators, {total_stake_cls:>10,.0f} DOT ({100*total_stake_cls/total_stake:.2f}%)")

# Save full mapping
with open("/tmp/b2_phase4/dot_polkawatch_attribution.json", "w") as f:
    json.dump({
        "polkawatch_operators_total": len(POLKAWATCH_OPERATORS),
        "polkawatch_validators_total": total_validators,
        "matched_operators_count": sum(1 for op, vs in matches.items() if vs),
        "matched_validators_count": sum(len(vs) for vs in matches.values()),
        "by_operator": {op: {"matched_addrs": [v["address"] for v in vs], "matched_count": len(vs), "stake_dot": sum(v["bonded_total_dot"] for v in vs), "class": operator_patterns[op]["class"]} for op, vs in matches.items() if vs},
    }, f, default=str, indent=2)
