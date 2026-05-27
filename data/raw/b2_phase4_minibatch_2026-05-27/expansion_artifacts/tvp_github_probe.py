#!/usr/bin/env python3
"""Find W3F TVP candidate list via GitHub raw."""
import urllib.request, urllib.error, json

UA = "Mozilla/5.0"
candidates = [
    "https://raw.githubusercontent.com/w3f/1k-validators-be/master/candidates/polkadot.json",
    "https://raw.githubusercontent.com/w3f/1k-validators-be/master/candidates/polkadot.yaml",
    "https://raw.githubusercontent.com/w3f/1k-validators-be/master/packages/common/candidates/polkadot.yaml",
    "https://raw.githubusercontent.com/w3f/1k-validators-be/main/candidates/polkadot.yaml",
    "https://raw.githubusercontent.com/w3f/1k-validators-be/main/candidates/polkadot.json",
    # Try via the API to list candidates folder
    "https://api.github.com/repos/w3f/1k-validators-be/contents/candidates",
    "https://api.github.com/repos/w3f/1k-validators-be/contents/packages/common/candidates",
    # Alt repo
    "https://raw.githubusercontent.com/w3f/decentralized-nodes/main/candidates/polkadot.yaml",
    "https://raw.githubusercontent.com/w3f/decentralized-nodes/main/candidates/polkadot.json",
    "https://api.github.com/repos/w3f/decentralized-nodes/contents/",
    # Polkawatch repo (community alternative)
    "https://gitlab.com/api/v4/projects/polkawatch%2Fpolkawatch/repository/files",
]

for url in candidates:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as r:
            body = r.read()
            print(f"  ✓ {url}  ({len(body)} bytes)")
            preview = body[:600].decode("utf-8", errors="replace")
            print(f"    preview: {preview[:400]}")
    except urllib.error.HTTPError as e:
        body = ""
        try: body = e.read().decode("utf-8")[:80]
        except: pass
        print(f"  HTTP {e.code} {url[:90]}  {body[:60]}")
    except Exception as e:
        print(f"  ERR {url[:90]}: {e}")
