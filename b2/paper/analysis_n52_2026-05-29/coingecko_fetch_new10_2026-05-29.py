#!/usr/bin/env python3
"""Fetch the 10 missing CoinGecko daily series (the new cohort) to bring the B2 regression
frame to full 50/50 CoinGecko coverage. CoinGecko Pro API (pro-api.coingecko.com,
x-cg-pro-api-key). Run via the key wrapper:

    bash scripts/with_api_key.sh coingecko -- python3 coingecko_fetch_new10_2026-05-29.py

Writes <coingecko_id>.csv (date, price_usd, market_cap_usd, volume_usd) into ./coingecko_new10/.
Uses curl (CoinGecko's CDN 403s the default urllib User-Agent). Implied circulating supply
downstream = market_cap_usd / price_usd.
"""
import os, json, csv, subprocess, time
from datetime import datetime, timezone

KEY = os.environ["COINGECKO_API_KEY"]
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "coingecko_new10")
os.makedirs(OUT, exist_ok=True)

# token -> (coingecko_id, protocol). SNX uses the legacy id `havven`.
COINS = {
    "SNX": ("havven", "Synthetix"), "GNO": ("gnosis", "Gnosis"), "ENA": ("ethena", "Ethena"),
    "WLFI": ("world-liberty-financial", "World Liberty Financial"),
    "JTO": ("jito-governance-token", "Jito"), "BONK": ("bonk", "Bonk"),
    "KMNO": ("kamino", "Kamino Finance"), "ALGO": ("algorand", "Algorand"),
    "DOT": ("polkadot", "Polkadot"), "TAO": ("bittensor", "Bittensor"),
}


def fetch(cid):
    url = f"https://pro-api.coingecko.com/api/v3/coins/{cid}/market_chart?vs_currency=usd&days=max&interval=daily"
    out = subprocess.run(["curl", "-s", url, "-H", f"x-cg-pro-api-key: {KEY}",
                          "-H", "accept: application/json"], capture_output=True, text=True, timeout=90).stdout
    return json.loads(out)


def main():
    ok = 0
    for tok, (cid, proto) in COINS.items():
        try:
            d = fetch(cid)
            prices = d.get("prices", [])
            if not prices:
                print(f"  {tok:6} ({cid}) EMPTY/err: {str(d)[:120]}")
                continue
            mc = {t: v for t, v in d.get("market_caps", [])}
            vo = {t: v for t, v in d.get("total_volumes", [])}
            rows = [{"coingecko_id": cid, "protocol": proto,
                     "date": datetime.fromtimestamp(t / 1000, tz=timezone.utc).strftime("%Y-%m-%d"),
                     "price_usd": p, "market_cap_usd": mc.get(t, ""), "volume_usd": vo.get(t, "")}
                    for t, p in prices]
            with open(os.path.join(OUT, f"{cid}.csv"), "w", newline="") as f:
                w = csv.DictWriter(f, fieldnames=["coingecko_id", "protocol", "date", "price_usd", "market_cap_usd", "volume_usd"])
                w.writeheader(); w.writerows(rows)
            ok += 1
            print(f"  {tok:6} ({cid:28}) {len(rows):>5} rows {rows[0]['date']}..{rows[-1]['date']}")
            time.sleep(2.5)
        except Exception as e:
            print(f"  {tok:6} ({cid}) ERROR {e}")
    print(f"\nfetched {ok}/{len(COINS)}")


if __name__ == "__main__":
    main()
