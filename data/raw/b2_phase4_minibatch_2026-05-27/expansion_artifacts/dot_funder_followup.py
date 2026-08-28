#!/usr/bin/env python3
"""Lookup the 2 still-unidentified top funders via transfers (who funded them?)."""
import json, urllib.request, time
import os

API_KEY = os.environ["SUBSCAN_API_KEY"]
UA = "Mozilla/5.0"

# Top unattributed funders
TARGETS = [
    ("14BsHGhfW3HuYRfcsfUo4AXFW4jRV3", "funds 19 validators / 28M DOT"),
    ("15iuYWAyfBkVnLrQJNJ7YZURMXoDXy", "funds 16 / 24M DOT"),
    ("12wvz9PZswHrtqayJGmcRGKNT2znp4", "funds 9 / 15M DOT"),
    ("14Dyrjcj2S8HfgTg32ViuMV3HB7A8v", "funds 9 / 13M DOT"),
    ("1346PqVgQuntdu4UFPbdSviidscuii", "funds 7 / 10M DOT"),
    ("1mndd9E8kssCxXDacCbKw3iwFQwdAB", "funds 5 / 7M DOT"),
    ("1qnJN7FViy3HZaxZK9tGAA71zxHSBe", "funds 5 / 7M DOT"),
    ("12xtAYsRUrmbniiWQqJtECiBQrMn8A", "funds 4 / 6M DOT"),
    ("133FTagMMVnVtSa4YAtYZz5EzbWv8Z", "funds 4 / 6M DOT"),
    ("14upMeWUxkV62eqwc7ZNRTdgN5Lkjy", "funds 3 / 4.5M DOT"),
]

# Use full addresses from clusters
clusters = json.load(open("/tmp/b2_phase4/dot_funding_clusters.json"))
short_to_full = {f["funder"][:30]: f["funder"] for f in clusters["top_funders"]}

for short, ctx in TARGETS:
    full = next((f for k, f in short_to_full.items() if k.startswith(short[:25])), None)
    if not full:
        continue
    # 1: Check incoming transfers (who funded the funder)
    url = "https://polkadot.api.subscan.io/api/v2/scan/transfers"
    body = json.dumps({"address": full, "row": 5, "page": 0, "direction": "received"}).encode()
    req = urllib.request.Request(url, data=body, headers={
        "Content-Type": "application/json", "User-Agent": UA, "X-API-Key": API_KEY,
    }, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            d = json.load(r)
        if d.get("code") == 0:
            transfers = d.get("data", {}).get("transfers", []) or []
            print(f"\n{full[:24]}... ({ctx})")
            for t in transfers[:3]:
                src = t.get("from", "")
                amt = float(t.get("amount", "0") or "0")
                # Check if from has identity
                fd = t.get("from_account_display", {}) or {}
                p = fd.get("people", {}) or {}
                display = p.get("display") or fd.get("display", "")
                print(f"    funded by: {src[:24]}... {amt:>10,.0f} DOT  '{display}'")
        time.sleep(0.3)
    except Exception as e:
        print(f"  err: {e}")
