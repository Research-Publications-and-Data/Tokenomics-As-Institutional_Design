#!/usr/bin/env python3
"""
B2 Nansen v4-REVIEWED assembly (2026-05-29): ingest the per-token adversarial
review (workflow b2-nansen-insider-review), join to survivor shares, build the
reviewed insider-retention vector, and reconcile v3 vs v4-keyword vs v4-reviewed.

Reads (persisted): the review workflow output (result.reviews), survivors json,
the keyword vector, v3, new12 vector. Writes versioned v4-reviewed outputs.
DOES NOT touch v3 or regression_data_april2026.csv.
"""
import csv, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
A = "/Users/zach/Tokenomics-As-Institutional_Design"
ADIR = os.path.join(A, "b2/paper/analysis_n52_2026-05-29")
OUTFILE = "/private/tmp/claude-501/-Users-zach-Tokenization-Systems-Website/443b94a2-eaac-43c5-8f84-87c7263d42ca/tasks/w1whhdeav.output"


def f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def main():
    reviews = json.load(open(OUTFILE))["result"]["reviews"]
    reviews = {r["frame_token"]: r for r in reviews}
    # ZRO original review was truncated (1 item); override with the clean re-review.
    zro = json.load(open(os.path.join(HERE, "zro_rereview_2026-05-29.json")))
    reviews["ZRO"] = zro
    json.dump(reviews, open(os.path.join(HERE, "b2_nansen_reviews_2026-05-29.json"), "w"), indent=1)

    # guard: every review must cover all 10 survivors (denominator is fixed at 10)
    incomplete = {t: len(r["reviewed"]) for t, r in reviews.items() if len(r["reviewed"]) != 10}
    if incomplete:
        print("WARNING incomplete reviews (expected 10 items):", incomplete)

    survivors = json.load(open(os.path.join(HERE, "survivors_2026-05-29.json")))
    v3 = {r["token"]: f(r.get("insider_count_frac")) for r in csv.DictReader(open(os.path.join(A, "data/processed/insider_analysis_results_v3.csv")))}
    new12 = {r["token"]: f(r["insider_count_frac"]) for r in csv.DictReader(open(os.path.join(ADIR, "new12_retention_vector_2026-05-29.csv")))}
    kwrows = {r["token"]: r for r in csv.DictReader(open(os.path.join(HERE, "insider_retention_vector_v4_nansen_2026-05-29.csv")))}

    NEW9 = ['FXS', 'SNX', 'GNO', 'WLFI', 'ENA', 'PUMP', 'JTO', 'BONK', 'KMNO']

    per_rows = []          # per-survivor reviewed
    vec_rows = []          # reviewed vector
    all_flags = {}
    all_flippers = {}
    notes = {}

    # 35 pulled tokens -> reviewed
    for tok, rv in reviews.items():
        share_by_rank = {s["rank"]: s["share"] for s in survivors[tok]["survivors"]}
        ins_count = 0; ins_share = 0.0; tot_share = 0.0
        for item in rv["reviewed"]:
            rank = int(item["rank"])
            share = share_by_rank.get(rank, 0.0)
            is_ins = bool(item["insider"])
            ins_count += int(is_ins); tot_share += share
            if is_ins:
                ins_share += share
            per_rows.append({"frame_token": tok, "rank": rank, "share": round(share, 4),
                             "nansen_label": item.get("nansen_label", ""),
                             "insider_reviewed": is_ins, "entity_type": item.get("entity_type", ""),
                             "confidence": item.get("confidence", ""), "reason": item.get("reason", "")})
        n = len(survivors[tok]["survivors"])  # fixed denominator (10); robust to truncated reviews
        frac = round(ins_count / n, 4) if n else None
        bal = round(ins_share / tot_share, 4) if tot_share > 0 else 0.0
        vec_rows.append({"token": tok, "insider_count": ins_count, "n_top10": n,
                         "insider_count_frac": frac, "insider_balance_frac": bal,
                         "source": "nansen_v4_reviewed",
                         "n_flags": len(rv.get("flags", [])), "n_flippers": len(rv.get("decision_flippers", []))})
        if rv.get("flags"):
            all_flags[tok] = rv["flags"]
        if rv.get("decision_flippers"):
            all_flippers[tok] = rv["decision_flippers"]
        if rv.get("note"):
            notes[tok] = rv["note"]

    # 9 new-cohort reuse (already author-corrected); GTC skipped
    for tok in NEW9:
        vec_rows.append({"token": tok, "insider_count": int(round(new12[tok] * 10)), "n_top10": 10,
                         "insider_count_frac": new12[tok], "insider_balance_frac": f(kwrows[tok]["insider_balance_frac"]),
                         "source": "new12_provenance_reuse", "n_flags": 0, "n_flippers": 0})

    # write per-survivor reviewed
    with open(os.path.join(HERE, "b2_nansen_insider_classification_v4_REVIEWED_2026-05-29.csv"), "w", newline="") as fp:
        w = csv.DictWriter(fp, fieldnames=list(per_rows[0].keys())); w.writeheader(); w.writerows(per_rows)
    # write reviewed vector
    with open(os.path.join(HERE, "insider_retention_vector_v4_reviewed_2026-05-29.csv"), "w", newline="") as fp:
        w = csv.DictWriter(fp, fieldnames=list(vec_rows[0].keys())); w.writeheader(); w.writerows(vec_rows)

    # reconciliation table v3 vs keyword vs reviewed
    rv_frac = {r["token"]: r["insider_count_frac"] for r in vec_rows}
    kw_frac = {t: f(r["insider_count_frac"]) for t, r in kwrows.items()}
    match = {t: int(r["n_matched_in_nansen"]) for t, r in kwrows.items()}
    recon = []
    for tok in sorted(rv_frac):
        base = new12.get(tok) if tok in new12 else v3.get(tok)
        m = match.get(tok, 10)
        is_reuse = tok in NEW9
        rev = rv_frac[tok]; kw = kw_frac.get(tok)
        if is_reuse:
            cls = "REUSE"
        elif base is None:
            cls = "NEW(no-v3)"
        elif abs(rev - base) < 1e-9:
            cls = "CONFIRM"
        elif m < 5:
            cls = "DIVERGE-LOWMATCH"
        else:
            cls = "DIVERGE-reliable"
        recon.append({"token": tok, "v3": base, "v4_keyword": kw, "v4_reviewed": rev,
                      "match": m, "class": cls,
                      "n_flags": next((r["n_flags"] for r in vec_rows if r["token"] == tok), 0),
                      "n_flippers": next((r["n_flippers"] for r in vec_rows if r["token"] == tok), 0)})
    with open(os.path.join(HERE, "b2_nansen_v4_reconciliation_2026-05-29.csv"), "w", newline="") as fp:
        w = csv.DictWriter(fp, fieldnames=list(recon[0].keys())); w.writeheader(); w.writerows(recon)

    json.dump({"flags_by_token": all_flags, "decision_flippers_by_token": all_flippers, "notes_by_token": notes},
              open(os.path.join(HERE, "b2_nansen_v4_flags_and_flippers_2026-05-29.json"), "w"), indent=1)

    # console summary
    print(f"{'token':10}{'v3':>6}{'kw':>6}{'rev':>6}{'match':>6}{'flag':>5}{'flip':>5}  class")
    print("-" * 72)
    nflip = 0; ndiv = 0
    for r in recon:
        v3s = f"{r['v3']:.1f}" if r['v3'] is not None else "  -"
        kws = f"{r['v4_keyword']:.1f}" if r['v4_keyword'] is not None else "  -"
        print(f"{r['token']:10}{v3s:>6}{kws:>6}{r['v4_reviewed']:>6.1f}{r['match']:>6}{r['n_flags']:>5}{r['n_flippers']:>5}  {r['class']}")
        nflip += r["n_flippers"]
        if r["class"].startswith("DIVERGE"):
            ndiv += 1
    from collections import Counter
    print("\nclass counts:", dict(Counter(r["class"] for r in recon)))
    print(f"tokens still diverging v4-reviewed vs v3: {ndiv} | total decision-flippers: {nflip}")
    print("\nTOKENS WITH DECISION-FLIPPERS:")
    for tok, fl in all_flippers.items():
        for x in fl:
            print(f"  {tok}: {x[:130]}")


if __name__ == "__main__":
    main()
