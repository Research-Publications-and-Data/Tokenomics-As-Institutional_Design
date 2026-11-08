#!/usr/bin/env python3
"""Decode the call path behind every DIMO null-address burn transfer that is not a
direct `withdraw(uint256)` on the token, and cache the result.

Input : dimo_burn_sender_detail_2026-08-27.json (the committed Dune result set)
Output: dimo_burn_calldata_decode_2026-08-27.json (tx hash -> unwrapped call chain)

The cache is what makes the classification reproducible without a live archive node:
`--check` re-reads the cache and asserts every non-direct transfer has a decoded
terminal function. `--refresh` re-fetches from a public Polygon RPC.

Wrapper selectors unwrapped: Gelato Relay sponsoredCallV2, Gnosis Safe
execTransaction, Gnosis Safe MultiSend, ERC-4337 v0.7 handleOps, and the common
smart-account execute(address,uint256,bytes).
"""
import json, os, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SRC   = os.path.join(HERE, "dimo_burn_sender_detail_2026-08-27.json")
CACHE = os.path.join(HERE, "dimo_burn_calldata_decode_2026-08-27.json")

DIMO_TOKEN = "0xe261d618a959afffd53168cd07d12e37b26761db"
RPCS = ["https://polygon.drpc.org", "https://1rpc.io/matic",
        "https://polygon-bor-rpc.publicnode.com"]
HDR = {"Content-Type": "application/json", "User-Agent": "curl/8.7.1",
       "Accept": "application/json"}

NAMES = {
    "0x2e1a7d4d": "withdraw(uint256)",
    "0x42966c68": "burn(uint256)",
    "0x9dc29fac": "burn(address,uint256)",
    "0xa9059cbb": "transfer(address,uint256)",
    "0x23b872dd": "transferFrom(address,address,uint256)",
    "0x40c10f19": "mint(address,uint256)",
    "0xcf2c52cb": "deposit(address,bytes)",
    "0x6a761202": "execTransaction",
    "0xad718d2a": "sponsoredCallV2",
    "0x8d80ff0a": "multiSend(bytes)",
    "0x765e827f": "handleOps",
    "0xb61d27f6": "execute(address,uint256,bytes)",
}


def rpc(method, params):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method,
                       "params": params}).encode()
    last = None
    for url in RPCS:
        for attempt in range(3):
            try:
                req = urllib.request.Request(url, data=body, headers=HDR)
                with urllib.request.urlopen(req, timeout=30) as r:
                    d = json.load(r)
                if "result" in d:
                    return d["result"]
                last = RuntimeError(d.get("error"))
            except Exception as e:
                last = e
                time.sleep(1.5)
    raise last


def hx(d):
    return d[2:] if d.startswith("0x") else d


def word(a, i):
    return a[i * 64:(i + 1) * 64]


def as_addr(w):
    return "0x" + w[24:]


def as_int(w):
    return int(w, 16) if w else 0


def dynb(a, byte_off):
    p = byte_off * 2
    ln = int(a[p:p + 64], 16)
    return "0x" + a[p + 64:p + 64 + ln * 2]


def parse_multisend(packed):
    """Gnosis MultiSend packs each call as op(1) to(20) value(32) len(32) data(len)."""
    h = hx(packed)
    out, i = [], 0
    while i + 2 + 40 + 64 + 64 <= len(h):
        to = "0x" + h[i + 2:i + 42]
        ln = int(h[i + 106:i + 170], 16)
        data = "0x" + h[i + 170:i + 170 + ln * 2]
        out.append((to, data))
        i += 170 + ln * 2
    return out


def parse_handleops(a):
    """ERC-4337 v0.7 handleOps(PackedUserOperation[],address) -> [(sender, callData)]."""
    ops_off = as_int(word(a, 0)) * 2
    n = int(a[ops_off:ops_off + 64], 16)
    base = ops_off + 64
    res = []
    for k in range(n):
        rel = int(a[base + k * 64:base + (k + 1) * 64], 16) * 2
        s = base + rel
        sender = "0x" + a[s + 24:s + 64]
        cd_off = int(a[s + 3 * 64:s + 4 * 64], 16) * 2
        p = s + cd_off
        ln = int(a[p:p + 64], 16)
        res.append((sender, "0x" + a[p + 64:p + 64 + ln * 2]))
    return res


def unwrap(target, data, depth=0, chain=None):
    chain = chain if chain is not None else []
    sel = data[:10]
    node = {"depth": depth, "target": (target or "").lower(), "selector": sel,
            "fn": NAMES.get(sel, sel)}
    chain.append(node)
    if depth > 6:
        return chain
    a = hx(data)[8:]
    try:
        if sel == "0xad718d2a":
            return unwrap(as_addr(word(a, 0)), dynb(a, as_int(word(a, 1))), depth + 1, chain)
        if sel == "0x6a761202":
            return unwrap(as_addr(word(a, 0)), dynb(a, as_int(word(a, 2))), depth + 1, chain)
        if sel == "0xb61d27f6":
            return unwrap(as_addr(word(a, 0)), dynb(a, as_int(word(a, 2))), depth + 1, chain)
        if sel == "0x8d80ff0a":
            inner = [(to, d2) for to, d2 in parse_multisend(dynb(a, as_int(word(a, 0))))
                     if to.lower() == DIMO_TOKEN]
            burny = [(to, d2) for to, d2 in inner
                     if d2[:10] in ("0x2e1a7d4d", "0x42966c68", "0x9dc29fac")]
            pick = burny or inner
            if pick:
                return unwrap(pick[0][0], pick[0][1], depth + 1, chain)
            node["note"] = "multiSend carried no call to the DIMO token"
            return chain
        if sel == "0x765e827f":
            for sender, cd in parse_handleops(a):
                sub = unwrap(sender, cd, depth + 1, [])
                if sub[-1]["target"] == DIMO_TOKEN:
                    chain.extend(sub)
                    return chain
            node["note"] = "handleOps carried no reachable call to the DIMO token"
            return chain
    except Exception as e:
        node["decode_error"] = str(e)
        return chain
    if sel == "0x2e1a7d4d":
        node["amount"] = as_int(word(a, 0)) / 1e18
    elif sel == "0x42966c68":
        node["amount"] = as_int(word(a, 0)) / 1e18
    elif sel == "0x9dc29fac":
        node["burned_from"] = as_addr(word(a, 0))
        node["amount"] = as_int(word(a, 1)) / 1e18
    return chain


def token_calls_from_trace(txhash):
    """Authoritative tier: every call into the DIMO token in this transaction,
    read from an execution trace rather than inferred from calldata."""
    tr = rpc("debug_traceTransaction", [txhash, {"tracer": "callTracer"}])
    found = []

    def walk(node):
        to = (node.get("to") or "").lower()
        if to == DIMO_TOKEN:
            inp = node.get("input") or "0x"
            found.append({"caller": (node.get("from") or "").lower(),
                          "selector": inp[:10],
                          "fn": NAMES.get(inp[:10], inp[:10]),
                          "type": node.get("type")})
        for c in node.get("calls", []) or []:
            walk(c)

    walk(tr)
    return found


BURN_SELECTORS = ("0x2e1a7d4d", "0x42966c68", "0x9dc29fac")


def targets():
    """Every burn tx hash that is NOT a direct withdraw() on the token."""
    rows = json.load(open(SRC))["result"]["rows"]
    seen, out = set(), []
    for r in rows:
        if r["row_kind"] != "burn":
            continue
        direct = (r["method_id"] == "0x2e1a7d4d"
                  and (r["tx_to"] or "").lower() == DIMO_TOKEN)
        if direct or r["tx_hash"] in seen:
            continue
        seen.add(r["tx_hash"])
        out.append(r["tx_hash"])
    return out


def refresh():
    cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
    todo = [h for h in targets() if h not in cache]
    print(f"[decode] {len(todo)} transaction(s) to fetch "
          f"({len(cache)} already cached)")
    for i, h in enumerate(todo, 1):
        try:
            tx = rpc("eth_getTransactionByHash", [h])
            entry = {"eoa": tx["from"], "to": tx["to"],
                     "chain": unwrap(tx["to"], tx["input"])}
            try:
                tc = token_calls_from_trace(h)
                entry["token_calls"] = tc
                burns = [c for c in tc if c["selector"] in BURN_SELECTORS]
                if burns:
                    entry["burn_selector"] = burns[0]["selector"]
                    entry["burn_fn"] = burns[0]["fn"]
                    entry["burn_caller"] = burns[0]["caller"]
            except Exception as e:
                entry["trace_error"] = str(e)
            cache[h] = entry
        except Exception as e:
            cache[h] = {"error": str(e)}
        if i % 25 == 0:
            print(f"[decode]   {i}/{len(todo)}")
            json.dump(cache, open(CACHE, "w"), indent=1, sort_keys=True)
    json.dump(cache, open(CACHE, "w"), indent=1, sort_keys=True)
    print(f"[decode] cache holds {len(cache)} transaction(s) -> {CACHE}")


def check():
    cache = json.load(open(CACHE))
    need = targets()
    missing = [h for h in need if h not in cache]
    errored = [h for h in need if cache.get(h, {}).get("error")]
    undec = [h for h in need if h in cache and not cache[h].get("burn_selector")]
    print(f"[check] non-direct transactions   : {len(need)}")
    print(f"[check] missing from cache        : {len(missing)}")
    print(f"[check] rpc errors                : {len(errored)}")
    print(f"[check] no burn call found in trace: {len(undec)}")
    for h in undec[:10]:
        print(f"[check]   undecided: {h}")
    return 0 if not missing and not errored and not undec else 1


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(check())
    refresh()
