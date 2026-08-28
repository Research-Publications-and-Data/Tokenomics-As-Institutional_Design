#!/usr/bin/env python3
"""Query Nansen Address Labels API with browser-like User-Agent (Cloudflare WAF requires it)."""
import json, urllib.request, time
import os

KEY = os.environ["NANSEN_API_KEY"]
URL = "https://api.nansen.ai/api/v1/profiler/address/labels"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"

ADDRS = [
    ("0xd2dd7b597fd2435b6db61ddf48544fd931e6869f", "3-protocol; 2025-09-21 cluster; $385M"),
    ("0x7dafba1d69f6c01ae7567ffd7b046ca03b706f83", "3-protocol; 2025-09-20 cluster; drained wallet"),
    ("0xedc6bacdc1e29d7c5fa6f6eca6fdd447b9c487c9", "3-protocol; older mixed"),
    ("0xab782bc7d4a2b306825de5a7730034f8f63ee1bc", "2-protocol SNX+GNO 2024-01-04 same-day"),
    ("0x7bf3cc3130d0efee990b0905540f982571e9205c", "2-protocol SNX+GNO 2025-11-09"),
    ("0xa023f08c70a23abc7edfc5b6b5e171d78dfc947e", "Crypto.com 22 per Etherscan"),
    ("0x0529ea5885702715e83923c59746ae8734c553b7", "Bitpanda 18 per Etherscan"),
    ("0xccfc07b3f23bf293e7363495fa2f9509bf72ecf1", "FXS rank-3 EOA (3.89%)"),
    ("0x3a5cc8689d1b0cef2c317bc5c0ad6ce88b27d597", "SNX rank-4 (3.87%)"),
    ("0x76ec5a0d3632b2133d9f1980903305b62678fbd3", "SNX rank-5 (3.23%)"),
    ("0xae5fb390e5c4fa1962e39e98dbfb0ed8055ed7a9", "GNO rank-11 PayingProxy"),
    ("0x445cc6c3d51eb0a63395a613a0960c7922bca0d6", "GNO rank-7 (0.70%)"),
    ("0xf977814e90da44bfa03b6295a0616a897441acec", "VALIDATION Binance 8"),
    ("0x9d94ef33e7f8087117f85b3ff7b1d8f27e4053d5", "GNO rank-6 Stefan-George Safe"),
]

results = []
for addr, ctx in ADDRS:
    body = json.dumps({"address": addr, "chain": "ethereum"}).encode()
    req = urllib.request.Request(URL, data=body, headers={
        "apiKey": KEY,
        "Content-Type": "application/json",
        "User-Agent": UA,
        "Accept": "application/json",
    }, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            d = json.load(r)
        # Try to extract labels
        labels = d.get("data", []) if isinstance(d, dict) else []
        if not labels and isinstance(d, dict):
            labels = d.get("labels", [])
        # Format
        if isinstance(labels, list):
            label_summary = [(x.get("label") or x.get("name"), x.get("category", "")) for x in labels[:10] if isinstance(x, dict)]
        else:
            label_summary = [str(labels)[:200]]
        print(f"  {addr}")
        print(f"    [{ctx}]")
        print(f"    labels: {label_summary}")
        results.append({"address": addr, "context": ctx, "labels": label_summary, "raw": d})
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")[:200] if hasattr(e, "read") else ""
        print(f"  {addr}: HTTP {e.code}  {body[:100]}")
    except Exception as e:
        print(f"  {addr}: ERR {type(e).__name__}: {e}")
    time.sleep(0.5)

with open("/tmp/b2_phase4/nansen_labels.json", "w") as f:
    json.dump(results, f, indent=2, default=str)
print(f"\nSaved {len(results)} results")
