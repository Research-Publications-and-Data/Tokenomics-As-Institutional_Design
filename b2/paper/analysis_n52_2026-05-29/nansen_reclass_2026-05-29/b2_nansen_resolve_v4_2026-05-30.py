#!/usr/bin/env python3
"""
B2 Nansen v4-RESOLVED (2026-05-30): apply the gap-fill evidence (Blockscout EVM
contract/Safe resolution + Nansen deployer traces) to the v4-reviewed per-survivor
classification, producing the evidence-hardened v4-resolved vector. Then the headline
is re-estimated (5th vector) by the headline-impact script.

Override rule: for any survivor whose key (TOKEN#rank) was gap-fill-resolved to a
DECISIVE entity_class (insider / protocol_contract / exchange / retail), set insider
accordingly; 'ambiguous' (unresolved Solana, etc.) keeps the v4-reviewed call.
Reads only; writes versioned v4-resolved outputs. Frame + v3 untouched.
"""
import csv, json, os
HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    reviewed = list(csv.DictReader(open(os.path.join(HERE, "b2_nansen_insider_classification_v4_REVIEWED_2026-05-29.csv"))))
    gap = json.load(open(os.path.join(HERE, "b2_gapfill_blockscout_resolved_2026-05-30.json")))
    survivors = json.load(open(os.path.join(HERE, "survivors_2026-05-29.json")))

    DECISIVE = {"insider": True, "protocol_contract": False, "exchange": False, "retail": False}
    rows = []
    overrides = []
    for r in reviewed:
        key = f"{r['frame_token']}#{r['rank']}"
        ins = r["insider_reviewed"] == "True"
        src = "v4_reviewed"
        et = r["entity_type"]
        g = gap.get(key)
        if g and g.get("entity_class") in DECISIVE:
            new_ins = DECISIVE[g["entity_class"]]
            if new_ins != ins:
                overrides.append((key, ins, new_ins, g.get("identity", "")[:40]))
            ins = new_ins
            src = "gapfill_resolved"
            et = g.get("entity_class")
        rows.append({**r, "insider_resolved": ins, "resolved_entity": et, "resolved_source": src,
                     "resolved_identity": (g.get("identity", "") if g else "")})

    # write per-survivor resolved
    flds = list(reviewed[0].keys()) + ["insider_resolved", "resolved_entity", "resolved_source", "resolved_identity"]
    with open(os.path.join(HERE, "b2_nansen_insider_classification_v4_RESOLVED_2026-05-30.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=flds); w.writeheader(); w.writerows(rows)

    # recompute vector (resolved). NEW9 reuse + GTC skip handled as before (reviewed had them; reuse keeps v4_reviewed which == new12)
    NEW9 = ['FXS', 'SNX', 'GNO', 'WLFI', 'ENA', 'PUMP', 'JTO', 'BONK', 'KMNO']
    by_tok = {}
    for r in rows:
        by_tok.setdefault(r["frame_token"], []).append(r)
    vec = []
    for tok, rs in by_tok.items():
        n = len(survivors[tok]["survivors"])
        ins_count = sum(1 for r in rs if r["insider_resolved"])
        tot = sum(float(r["share"]) for r in rs)
        ins_share = sum(float(r["share"]) for r in rs if r["insider_resolved"])
        vec.append({"token": tok, "insider_count": ins_count, "n_top10": n,
                    "insider_count_frac": round(ins_count / n, 4) if n else None,
                    "insider_balance_frac": round(ins_share / tot, 4) if tot > 0 else 0.0})
    with open(os.path.join(HERE, "insider_retention_vector_v4_resolved_2026-05-30.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(vec[0].keys())); w.writeheader(); w.writerows(vec)

    print(f"per-survivor overrides applied (gap-fill changed the reviewed call): {len(overrides)}")
    for k, a, b, ident in overrides:
        print(f"  {k:13} {a} -> {b}   {ident}")
    # show tokens whose frac changed vs reviewed
    rev_frac = {r["token"]: float(r["insider_count_frac"]) for r in csv.DictReader(open(os.path.join(HERE, "insider_retention_vector_v4_reviewed_2026-05-29.csv")))}
    print("\ntokens whose insider_count_frac changed v4_reviewed -> v4_resolved:")
    for v in sorted(vec, key=lambda x: x["token"]):
        rv = rev_frac.get(v["token"])
        if rv is not None and abs(rv - v["insider_count_frac"]) > 1e-9:
            print(f"  {v['token']:10} {rv} -> {v['insider_count_frac']}")


if __name__ == "__main__":
    main()
