#!/usr/bin/env python3
"""DISCOVERY GATHER: DefiLlama emissions/unlocks for the B2 cross-section, to enable the
schedule-method incentive build and unlock-netting.

DefiLlama free dataset CDN: https://defillama-datasets.llama.fi/emissions/<slug>
(the per-protocol curve is FREE; the /api/emissions list endpoint is paywalled, but the
free list at .../emissionsProtocolsList gives the slugs). Each curve has:
  documentedData.data[] = per-category series, label + per-point {timestamp, unlocked,
                          rawEmission, burned}
  gecko_id              = for slug validation + joining to our CoinGecko price series.

Category mapping (label -> bucket):
  INCENTIVE  = incentives / farming / emission / reward / staking / liquidity  (schedule-method numerator)
  INSIDER    = team / investor / advisor / insider / private / seed / strategic (unlock-netting)
  OTHER      = airdrop / community / public / ecosystem / foundation / treasury / dao

For each of the 50 frame protocols: resolve + validate a DefiLlama slug (gecko_id must match the
expected CoinGecko id), then extract a COMPACT MONTHLY series: incentive emission tokens
(INCENTIVE rawEmission), insider unlock tokens (INSIDER monthly delta of unlocked), burned.
Writes a readiness inventory + the compact monthly series + a raw-curve cache. Run directly
(uses curl; CoinGecko/DefiLlama CDNs 403 the default urllib User-Agent).
"""
import csv, os, json, subprocess, time, re
from collections import defaultdict
from datetime import datetime, timezone

A = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "defillama_emissions")
os.makedirs(OUT, exist_ok=True)


def norm(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def curl_json(url):
    out = subprocess.run(["curl", "-s", url], capture_output=True, text=True, timeout=90).stdout
    try:
        return json.loads(out)
    except Exception:
        return None


def label_bucket(label):
    l = (label or "").lower()
    if any(k in l for k in ["incentive", "farming", "emission", "reward", "staking", "liquidity", "mining"]):
        return "INCENTIVE"
    if any(k in l for k in ["team", "investor", "advisor", "insider", "private", "seed", "strategic", "founder", "core contributor"]):
        return "INSIDER"
    return "OTHER"


# expected coingecko id per token (coingecko_market + the new-10 map)
EXP = {"SNX": "havven", "GNO": "gnosis", "ENA": "ethena", "WLFI": "world-liberty-financial",
       "JTO": "jito-governance-token", "BONK": "bonk", "KMNO": "kamino", "ALGO": "algorand",
       "DOT": "polkadot", "TAO": "bittensor"}
for r in csv.DictReader(open(os.path.join(A, "data/raw/coingecko_market.csv"))):
    if r.get("coingecko_id"):
        EXP.setdefault(r["token"], r["coingecko_id"])


def main():
    plist = curl_json("https://defillama-datasets.llama.fi/emissionsProtocolsList") or []
    pnorm = {norm(s): s for s in plist}
    frame = [(r["token"], r["protocol"], r["category"]) for r in csv.DictReader(open(os.path.join(A, "data/processed/regression_data_april2026.csv")))
             if r.get("category") in {"DePIN", "DeFi", "L1_L2_Infra"}]

    inv = []
    monthly = []
    for tok, proto, cat in frame:
        # candidate slugs
        cands = []
        for c in (norm(proto), norm(proto.split()[0]), norm(tok)):
            if c in pnorm:
                cands.append(pnorm[c])
        for k, s in pnorm.items():
            if norm(proto.split()[0]) and (norm(proto.split()[0]) in k or k.startswith(norm(tok))):
                cands.append(s)
        cands = list(dict.fromkeys(cands))[:4]
        chosen = None; meta = None
        for slug in cands:
            d = curl_json(f"https://defillama-datasets.llama.fi/emissions/{slug}")
            time.sleep(0.6)
            if not d or "documentedData" not in d:
                continue
            gid = d.get("gecko_id", "")
            ok = (EXP.get(tok) and gid == EXP[tok]) or norm(d.get("name", "")) == norm(proto) or norm(d.get("name", "")).startswith(norm(tok))
            if ok or chosen is None:  # prefer a validated one, else keep first parseable
                chosen, meta = slug, d
                if ok:
                    break
        if not meta:
            inv.append({"token": tok, "sector": cat, "defillama_slug": "", "gecko_id": "", "valid": False,
                        "has_incentives": False, "has_insiders": False, "labels": "", "span": ""})
            continue
        gid = meta.get("gecko_id", "")
        valid = bool(EXP.get(tok) and gid == EXP[tok])
        data = meta.get("documentedData", {}).get("data", [])
        labels = [(s.get("label"), label_bucket(s.get("label"))) for s in data]
        has_inc = any(b == "INCENTIVE" for _, b in labels)
        has_ins = any(b == "INSIDER" for _, b in labels)
        # compact monthly: incentive rawEmission (sum INCENTIVE series), insider unlocked delta, burned
        inc_m = defaultdict(float); ins_cum = defaultdict(float); brn_m = defaultdict(float)
        spans = []
        for s in data:
            b = label_bucket(s.get("label")); pts = s.get("data", [])
            if pts:
                spans += [pts[0]["timestamp"], pts[-1]["timestamp"]]
            for p in pts:
                m = datetime.fromtimestamp(p["timestamp"], tz=timezone.utc).strftime("%Y-%m")
                if b == "INCENTIVE":
                    inc_m[m] += p.get("rawEmission") or 0
                if b == "INSIDER":
                    ins_cum[(s.get("label"), m)] = p.get("unlocked") or 0  # cumulative; delta computed below
                brn_m[m] += p.get("burned") or 0
        # insider monthly unlock = delta of cumulative unlocked per insider series, summed
        ins_m = defaultdict(float)
        per_series = defaultdict(dict)
        for (lab, m), v in ins_cum.items():
            per_series[lab][m] = v
        for lab, mv in per_series.items():
            ms = sorted(mv)
            for i in range(1, len(ms)):
                ins_m[ms[i]] += max(0.0, mv[ms[i]] - mv[ms[i - 1]])
        allm = sorted(set(inc_m) | set(ins_m) | set(brn_m))
        for m in allm:
            monthly.append({"token": tok, "month": m, "incentive_emission_tokens": round(inc_m.get(m, 0), 2),
                            "insider_unlock_tokens": round(ins_m.get(m, 0), 2), "burned_tokens": round(brn_m.get(m, 0), 2)})
        span = (datetime.fromtimestamp(min(spans), tz=timezone.utc).strftime("%Y-%m") + ".." +
                datetime.fromtimestamp(max(spans), tz=timezone.utc).strftime("%Y-%m")) if spans else ""
        inv.append({"token": tok, "sector": cat, "defillama_slug": chosen, "gecko_id": gid, "valid": valid,
                    "has_incentives": has_inc, "has_insiders": has_ins,
                    "labels": "|".join(f"{l}:{b}" for l, b in labels), "span": span})
        print(f"  {tok:8} slug={chosen:22} gid={gid:24} valid={valid} INC={has_inc} INS={has_ins} [{span}]")

    with open(os.path.join(OUT, "defillama_readiness_inventory_2026-05-29.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["token", "sector", "defillama_slug", "gecko_id", "valid", "has_incentives", "has_insiders", "labels", "span"]); w.writeheader(); w.writerows(inv)
    with open(os.path.join(OUT, "defillama_monthly_emissions_unlocks_2026-05-29.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["token", "month", "incentive_emission_tokens", "insider_unlock_tokens", "burned_tokens"]); w.writeheader(); w.writerows(monthly)

    nval = sum(1 for r in inv if r["valid"]); ninc = sum(1 for r in inv if r["has_incentives"]); nins = sum(1 for r in inv if r["has_insiders"])
    print(f"\n=== READINESS: {len(frame)} frame protocols ===")
    print(f"  DefiLlama curve resolved + gecko_id-VALID: {nval}")
    print(f"  with an INCENTIVE (farming/emission) category (schedule-method ready): {ninc}")
    print(f"  with an INSIDER (team/investor/advisor) category (unlock-netting ready): {nins}")
    print(f"  monthly rows gathered: {len(monthly)}")
    print(f"[written] defillama_emissions/defillama_readiness_inventory_2026-05-29.csv + defillama_monthly_emissions_unlocks_2026-05-29.csv")


if __name__ == "__main__":
    main()
