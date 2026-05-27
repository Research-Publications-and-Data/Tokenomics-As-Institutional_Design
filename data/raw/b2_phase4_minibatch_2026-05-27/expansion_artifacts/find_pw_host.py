#!/usr/bin/env python3
"""Find Polkawatch's DDP API host."""
import urllib.request, urllib.error

UA = "Mozilla/5.0"
hosts = [
    "polkawatch.app",
    "api.polkawatch.app",
    "data.polkawatch.app",
    "ddp.polkawatch.app",
    "ipfs.polkawatch.app",
    "get.polkawatch.app",
    "stats.polkawatch.app",
    "polkawatch-api.web.app",
    "decentralization.polkawatch.app",
    "open.polkawatch.app",
    "elastic.polkawatch.app",
]
path = "/ddp/operator/overview/0/30.json"

for h in hosts:
    url = f"https://{h}{path}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=8) as r:
            body = r.read()
            print(f"  ✓ {url}  ({len(body)} bytes)")
            print(f"    preview: {body[:300].decode('utf-8', 'replace')}")
            with open(f"/tmp/b2_phase4/pw_{h}_test.json", "wb") as f:
                f.write(body)
            break
    except urllib.error.HTTPError as e:
        body = ""
        try: body = e.read().decode("utf-8")[:60]
        except: pass
        print(f"  HTTP {e.code}: {url}  {body}")
    except Exception as e:
        print(f"  ERR: {url}  {type(e).__name__}: {str(e)[:60]}")
