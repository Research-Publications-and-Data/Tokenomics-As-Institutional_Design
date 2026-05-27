#!/usr/bin/env python3
"""Pull covariates from DeFiLlama API for FXS/SNX/GNO/DOT."""
import json, urllib.request, time

UA = "Mozilla/5.0"

# DeFiLlama has separate endpoints for protocol TVL, token MCap/FDV, etc.
# /protocols returns all protocols list with TVL
# /protocol/<slug> returns detailed protocol-specific data
# coins.llama.fi/prices/current/coingecko:<id> returns token prices

# Map: protocol slug -> CoinGecko ID
PROTOCOLS = {
    "FXS": {"defillama_slug": "frax", "coingecko_id": "frax-share", "name": "Frax Finance"},
    "SNX": {"defillama_slug": "synthetix", "coingecko_id": "havven", "name": "Synthetix"},
    "GNO": {"defillama_slug": "gnosis", "coingecko_id": "gnosis", "name": "Gnosis"},
    "DOT": {"defillama_slug": None, "coingecko_id": "polkadot", "name": "Polkadot"},
}

results = {}
for sym, meta in PROTOCOLS.items():
    print(f"\n=== {sym} ({meta['name']}) ===")
    r = {"symbol": sym}

    # Step 1: DeFiLlama protocol TVL/MCap (where available)
    if meta["defillama_slug"]:
        try:
            url = f"https://api.llama.fi/protocol/{meta['defillama_slug']}"
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=15) as resp:
                d = json.load(resp)
            r["defillama_name"] = d.get("name")
            r["defillama_category"] = d.get("category")
            r["defillama_tvl_current"] = d.get("currentChainTvls", {}).get("Ethereum", 0) or d.get("tvl", [{}])[-1].get("totalLiquidityUSD") if d.get("tvl") else None
            r["defillama_mcap"] = d.get("mcap")
            r["defillama_fdv"] = d.get("fdv")
            r["defillama_chain"] = d.get("chain")
            r["defillama_token_address"] = d.get("address")
            tvl_history = d.get("tvl", [])
            if tvl_history:
                r["defillama_tvl_value"] = tvl_history[-1].get("totalLiquidityUSD")
            print(f"  DeFiLlama TVL: ${r.get('defillama_tvl_value') or 0:,.0f}; mcap=${r.get('defillama_mcap') or 0:,.0f}; fdv=${r.get('defillama_fdv') or 0:,.0f}")
            time.sleep(0.5)
        except Exception as e:
            print(f"  DeFiLlama protocol err: {e}")
            r["defillama_err"] = str(e)

    # Step 2: CoinGecko via DeFiLlama coins (free; aggregated)
    try:
        url = f"https://coins.llama.fi/prices/current/coingecko:{meta['coingecko_id']}"
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=10) as resp:
            d = json.load(resp)
        coin_data = d.get("coins", {}).get(f"coingecko:{meta['coingecko_id']}", {})
        r["price_usd"] = coin_data.get("price")
        r["symbol_confirmed"] = coin_data.get("symbol")
        r["timestamp"] = coin_data.get("timestamp")
        print(f"  Price: ${r.get('price_usd'):.4f} ({r.get('symbol_confirmed')})")
        time.sleep(0.3)
    except Exception as e:
        print(f"  Price err: {e}")

    results[sym] = r

# Pull fees + revenue data from DeFiLlama for each
print("\n=== Pulling fees + revenue data ===")
for sym, meta in PROTOCOLS.items():
    if not meta["defillama_slug"]:
        continue
    try:
        url = f"https://api.llama.fi/summary/fees/{meta['defillama_slug']}?dataType=dailyFees"
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=15) as resp:
            d = json.load(resp)
        results[sym]["fees_total_24h"] = d.get("total24h")
        results[sym]["fees_total_30d"] = d.get("total30d")
        results[sym]["fees_total_1y"] = d.get("total365d")
        print(f"  {sym}: fees 1y=${d.get('total365d') or 0:,.0f}")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"  {sym}: no fees data")
        else:
            print(f"  {sym}: HTTP {e.code}")
    except Exception as e:
        print(f"  {sym}: err {e}")
    time.sleep(0.4)

# Pull revenue separately
for sym, meta in PROTOCOLS.items():
    if not meta["defillama_slug"]:
        continue
    try:
        url = f"https://api.llama.fi/summary/fees/{meta['defillama_slug']}?dataType=dailyRevenue"
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=15) as resp:
            d = json.load(resp)
        results[sym]["rev_total_1y"] = d.get("total365d")
        print(f"  {sym}: rev 1y=${d.get('total365d') or 0:,.0f}")
    except urllib.error.HTTPError as e:
        if e.code != 404:
            print(f"  {sym}: rev HTTP {e.code}")
    except Exception as e:
        print(f"  {sym}: rev err {e}")
    time.sleep(0.4)

with open("/tmp/b2_phase4/covariates_defillama.json", "w") as f:
    json.dump(results, f, default=str, indent=2)

print(f"\n=== Summary ===")
for sym, r in results.items():
    print(f"\n{sym}:")
    for k, v in r.items():
        print(f"  {k}: {v}")
