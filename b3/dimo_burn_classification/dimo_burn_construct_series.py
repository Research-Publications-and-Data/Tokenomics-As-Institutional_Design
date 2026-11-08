#!/usr/bin/env python3
"""Rebuild the DIMO monthly S2R series with the numerator split by what the burn
actually was, rather than by where the tokens went.

The published series (`dimo_s2r_monthly.csv`, from `data/dune_queries/03_dimo_s2r.sql`)
counts every ERC-20 transfer of DIMO to the null address on Polygon as a burn and
calls the total Developer License demand. Each such transfer is produced by exactly
one of three functions on the token, and they mean different things:

  withdraw(uint256)      permissionless; burns the caller's balance; the Polygon PoS
                         bridge exit path (the token is re-minted on Ethereum)
  burn(uint256)          BURNER_ROLE only; held by DIMO's two Wormhole NTT managers
  burn(address,uint256)  BURNER_ROLE only; held by the DIMO Credit (DCX) token, which
                         burns the buyer's DIMO when credits are purchased

Inputs (both committed beside this file):
  dimo_burn_sender_detail_2026-08-27.json  per-transfer Dune result set
  dimo_burn_calldata_decode_2026-08-27.json  per-transaction call decode + trace

Outputs:
  dimo_burn_classified_monthly.csv   monthly series under each numerator
  dimo_burn_classified_summary.json  totals, sender concentration, role evidence

`--check` asserts the reclassified monthly totals reconcile to the published series
and that the rebuilt CSV is byte-identical to the committed one.
"""
import csv, json, os, sys, collections

HERE = os.path.dirname(os.path.abspath(__file__))
DETAIL = os.path.join(HERE, "dimo_burn_sender_detail_2026-08-27.json")
DECODE = os.path.join(HERE, "dimo_burn_calldata_decode_2026-08-27.json")
PUBLISHED = os.path.join(HERE, "dimo_s2r_monthly.csv")
OUT_CSV = os.path.join(HERE, "dimo_burn_classified_monthly.csv")
OUT_JSON = os.path.join(HERE, "dimo_burn_classified_summary.json")

DIMO_TOKEN = "0xe261d618a959afffd53168cd07d12e37b26761db"

# Classification is by the burn function reached on the token, plus, for the two
# BURNER_ROLE functions, by which role holder called it. Roles read live from the
# token on 2026-08-27 via eth_call hasRole(bytes32,address); see the exhibit note.
NTT_MANAGERS = {
    "0xe0c5e6ae2954a4813a66097adf33efa5470bcde2",  # Wormhole NttManager, DIMO deployer
    "0x6ce25ee2851063966ad299f337217655e911d732",  # Wormhole NttManager, DIMO deployer
}
DCX_TOKEN = "0x7186f9ac35d24c9a4cf1e58a797c04df1b334322"  # DIMO Credit (DCX)

CLASSES = ["pos_bridge_exit", "wormhole_ntt_bridge", "dcx_credit_purchase", "unclassified"]


def classify(row, cache):
    """Return (class, burn_fn) for one null-address transfer."""
    direct = (row["method_id"] == "0x2e1a7d4d"
              and (row["tx_to"] or "").lower() == DIMO_TOKEN)
    if direct:
        return "pos_bridge_exit", "withdraw(uint256)"
    c = cache.get(row["tx_hash"], {})
    sel = c.get("burn_selector")
    caller = (c.get("burn_caller") or "").lower()
    if sel == "0x2e1a7d4d":
        return "pos_bridge_exit", "withdraw(uint256)"
    if sel == "0x42966c68":
        if caller in NTT_MANAGERS:
            return "wormhole_ntt_bridge", "burn(uint256)"
        return "unclassified", "burn(uint256)"
    if sel == "0x9dc29fac":
        if caller == DCX_TOKEN:
            return "dcx_credit_purchase", "burn(address,uint256)"
        return "unclassified", "burn(address,uint256)"
    return "unclassified", sel or "unknown"


def load():
    rows = json.load(open(DETAIL))["result"]["rows"]
    cache = json.load(open(DECODE))
    burns = [r for r in rows if r["row_kind"] == "burn"]
    mints = [r for r in rows if r["row_kind"] == "mint_month_agg"]
    return burns, mints, cache


def hhi(shares):
    t = sum(shares)
    return sum((s / t) ** 2 for s in shares) if t else 0.0


def build():
    burns, mints, cache = load()
    by_month = collections.defaultdict(lambda: collections.defaultdict(float))
    by_class = collections.defaultdict(float)
    n_class = collections.Counter()
    sender_all = collections.defaultdict(float)
    sender_dcx = collections.defaultdict(float)
    dcx_origins = set()

    for r in burns:
        cls, fn = classify(r, cache)
        month = r["block_time"][:7] + "-01"
        by_month[month][cls] += r["amount"]
        by_month[month]["burned_total"] += r["amount"]
        by_class[cls] += r["amount"]
        n_class[cls] += 1
        sender_all[r["counterparty"]] += r["amount"]
        if cls == "dcx_credit_purchase":
            sender_dcx[r["counterparty"]] += r["amount"]
            eoa = cache.get(r["tx_hash"], {}).get("eoa")
            if eoa:
                dcx_origins.add(eoa.lower())

    for r in mints:
        by_month[r["block_time"][:7] + "-01"]["issued"] += r["amount"]

    months = sorted(by_month)
    with open(OUT_CSV, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["month", "burn_pos_bridge_exit", "burn_wormhole_ntt_bridge",
                    "burn_dcx_credit_purchase", "burn_unclassified",
                    "dimo_burned_total", "dimo_issued",
                    "s2r_as_published", "s2r_dcx_credit_only"])
        for mo in months:
            d = by_month[mo]
            iss = d.get("issued", 0.0)
            tot = d.get("burned_total", 0.0)
            dcx = d.get("dcx_credit_purchase", 0.0)
            w.writerow([mo,
                        repr(d.get("pos_bridge_exit", 0.0)),
                        repr(d.get("wormhole_ntt_bridge", 0.0)),
                        repr(dcx),
                        repr(d.get("unclassified", 0.0)),
                        repr(tot), repr(iss),
                        repr(tot / iss) if iss else "",
                        repr(dcx / iss) if iss else ""])

    tot = sum(by_class.values())
    top = sorted(sender_all.items(), key=lambda x: -x[1])
    summary = {
        "as_of": "2026-08-27",
        "window": [months[0], months[-1]],
        "burn_transfers": len(burns),
        "burn_total_dimo": tot,
        "issuance_total_dimo": sum(r["amount"] for r in mints),
        "by_class": {c: {"dimo": by_class.get(c, 0.0),
                         "transfers": n_class.get(c, 0),
                         "share_of_numerator": (by_class.get(c, 0.0) / tot) if tot else 0.0}
                     for c in CLASSES},
        "bridge_share_of_numerator": (
            (by_class.get("pos_bridge_exit", 0.0)
             + by_class.get("wormhole_ntt_bridge", 0.0)) / tot) if tot else 0.0,
        "distinct_null_address_senders": len(sender_all),
        # A credit purchase moves DIMO buyer -> DCX by transferFrom and then DCX burns
        # its OWN holding, so Transfer.from on the null-address leg is always the DCX
        # contract. The buyer count therefore has to come from the transaction origin.
        "distinct_dcx_credit_transfer_from": len(sender_dcx),
        "distinct_dcx_credit_tx_origins": len(dcx_origins),
        "hhi_all_null_address_senders": hhi(list(sender_all.values())),
        "top_sender_share": (top[0][1] / tot) if tot else 0.0,
        "top_sender": top[0][0] if top else None,
        "senders_above_1pct": [
            {"address": a, "dimo": v, "share": v / tot,
             "class_mix": sorted({classify(r, cache)[0] for r in burns
                                  if r["counterparty"] == a})}
            for a, v in top if v / tot > 0.01],
        "dcx_credit_months": sorted({m for m in months
                                     if by_month[m].get("dcx_credit_purchase", 0.0) > 0}),
        "dcx_credit_senders": sorted(sender_dcx),
    }
    json.dump(summary, open(OUT_JSON, "w"), indent=1, sort_keys=True)
    return summary, months, by_month


def check():
    # The committed CSV's bytes are read before build() rewrites it, so the byte-identity this
    # docstring promises is compared, not assumed (promised and not compared until 2026-11-07).
    before = open(OUT_CSV, "rb").read() if os.path.exists(OUT_CSV) else None
    summary, months, by_month = build()
    identical = before is not None and open(OUT_CSV, "rb").read() == before
    pub = {r["month"]: r for r in csv.DictReader(open(PUBLISHED))}
    bad = []
    for mo in months:
        if mo not in pub:
            bad.append((mo, "absent from published series"))
            continue
        for ours, theirs in (("burned_total", "dimo_burned"), ("issued", "dimo_issued")):
            a, b = by_month[mo].get(ours, 0.0), float(pub[mo][theirs])
            if abs(a - b) > max(1e-6, abs(b) * 1e-9):
                bad.append((mo, f"{ours}: reclassified {a!r} vs published {b!r}"))
    missing = set(pub) - set(months)
    for mo in sorted(missing):
        bad.append((mo, "published month absent from reclassified series"))
    unc = summary["by_class"]["unclassified"]["transfers"]
    print(f"[check] months reconciled          : {len(months)}")
    print(f"[check] mismatches vs published    : {len(bad)}")
    print(f"[check] unclassified transfers     : {unc}")
    print(f"[check] rebuilt CSV byte-identical : {identical}")
    for mo, why in bad[:10]:
        print(f"[check]   {mo}: {why}")
    return 0 if not bad and unc == 0 and identical else 1


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(check())
    s, months, _ = build()
    if not (s["burn_transfers"] == 3568 and s["by_class"]["unclassified"]["transfers"] == 0
            and abs(s["bridge_share_of_numerator"] - 0.999871699506005) < 1e-9
            and s["distinct_dcx_credit_tx_origins"] == 40 and check() == 0):
        raise SystemExit("FATAL: DIMO burn construct differs from burn_construct_validation.md (3,568 transfers, 0 unclassified, 99.987 percent bridge share, 40 credit-purchase origins) or fails --check")
    print(json.dumps({k: s[k] for k in                      ("burn_transfers", "burn_total_dimo", "issuance_total_dimo",
                       "bridge_share_of_numerator", "distinct_null_address_senders",
                       "distinct_dcx_credit_transfer_from",
                       "distinct_dcx_credit_tx_origins", "hhi_all_null_address_senders",
                       "top_sender_share", "dcx_credit_months")}, indent=1))
    print(f"wrote {OUT_CSV}")
