#!/usr/bin/env python3
"""
B2 v4-TRACED (2026-05-30): apply the Safe-deployer trace verdicts (follow-on C) to
v4-resolved. Evidence-based multisig rule: a multisig/Safe is INSIDER only if
team_confirmed (deployer/signer is the protocol team); 'independent' (whale/unlabeled
deployer) -> NOT insider. This corrects the keyword rule's over-count of independent
whales' Safes. Produces the most defensible vector. Frame + v3 untouched.
"""
import csv, json, os
HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    resolved = list(csv.DictReader(open(os.path.join(HERE, "b2_nansen_insider_classification_v4_RESOLVED_2026-05-30.csv"))))
    verdicts = json.load(open(os.path.join(HERE, "b2_followon_c_safe_verdicts_2026-05-30.json")))
    # earlier-confirmed team Safes (deployer-traced before the C workflow)
    extra_team = {"MKR#1", "DIMO#1"}
    survivors = json.load(open(os.path.join(HERE, "survivors_2026-05-29.json")))

    overrides = []
    rows = []
    for r in resolved:
        key = f"{r['frame_token']}#{r['rank']}"
        ins = r["insider_resolved"] == "True"
        src = "v4_resolved"
        v = verdicts.get(key)
        if key in extra_team:
            new = True; src = "trace_team_confirmed"
        elif v:
            if v["verdict"] == "team_confirmed":
                new = True; src = "trace_team_confirmed"
            elif v["verdict"] == "independent":
                new = False; src = "trace_independent_not_insider"
            else:
                new = ins; src = "trace_unclear_keep"
        else:
            new = ins
        if v or key in extra_team:
            if new != ins:
                overrides.append((key, ins, new, (v or {}).get("controlling_entity", "deployer=dinc.eth/MakerDAO")))
        rows.append({**r, "insider_traced": new, "traced_source": src})

    flds = list(resolved[0].keys()) + ["insider_traced", "traced_source"]
    with open(os.path.join(HERE, "b2_nansen_insider_classification_v4_TRACED_2026-05-30.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=flds); w.writeheader(); w.writerows(rows)

    by = {}
    for r in rows:
        by.setdefault(r["frame_token"], []).append(r)
    vec = []
    for tok, rs in by.items():
        n = len(survivors[tok]["survivors"])
        ic = sum(1 for r in rs if r["insider_traced"])
        tot = sum(float(r["share"]) for r in rs)
        ish = sum(float(r["share"]) for r in rs if r["insider_traced"])
        vec.append({"token": tok, "insider_count": ic, "n_top10": n,
                    "insider_count_frac": round(ic / n, 4) if n else None,
                    "insider_balance_frac": round(ish / tot, 4) if tot > 0 else 0.0})
    with open(os.path.join(HERE, "insider_retention_vector_v4_traced_2026-05-30.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(vec[0].keys())); w.writeheader(); w.writerows(vec)

    print(f"trace overrides (changed v4_resolved call): {len(overrides)}")
    for k, a, b, ent in overrides:
        print(f"  {k:10} {a} -> {b}   {str(ent)[:40]}")
    res_frac = {r["token"]: float(r["insider_count_frac"]) for r in csv.DictReader(open(os.path.join(HERE, "insider_retention_vector_v4_resolved_2026-05-30.csv")))}
    print("\ntokens whose frac changed v4_resolved -> v4_traced:")
    for v in sorted(vec, key=lambda x: x["token"]):
        rv = res_frac.get(v["token"])
        if rv is not None and abs(rv - v["insider_count_frac"]) > 1e-9:
            print(f"  {v['token']:10} {rv} -> {v['insider_count_frac']}")


if __name__ == "__main__":
    main()
