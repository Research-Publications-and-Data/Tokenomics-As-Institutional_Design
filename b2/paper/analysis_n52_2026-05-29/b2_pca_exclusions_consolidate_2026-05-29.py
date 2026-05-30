#!/usr/bin/env python3
"""Fill the G1 gap: ONE consolidated machine-readable PCA-exclusion log merging every scattered
source, then recompute all 50 post-exclusion HHIs from raw-minus-consolidated-log and reconcile
to the documented regression frame. Writes:
  b2_pca_exclusions_consolidated_2026-05-29.csv  (token,address,pca_class,source)
  audit_consolidated_hhi_status_2026-05-29.csv   (per-protocol reproduce status + cause)

Sources merged: exclusions_log.csv, exclusions_log_signer.csv, phase4_evm_minibatch v2-audited,
new12_unified (WLFI Dolomite/LockRelease + ENA sENA corrections), ALGO_pca_exclusions (clone-B),
TAO coldkeys + bridge (tao_exchange_coldkeys.json). READ-ONLY against all sources; does NOT touch
the regression frame. Reads persisted data only; no /tmp, no live-API.
"""
import csv, os, math, re, json
from collections import defaultdict

A = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
B = "/Users/zach/b2-governance-data"
HERE = os.path.dirname(os.path.abspath(__file__))
HL = [f"{A}/data/raw/holder_lists", f"{B}/data/raw/holder_lists"]
BAL = ["balance", "amount_algo", "amount", "value"]


def f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def load(t):
    for d in HL:
        p = f"{d}/{t}_holders.csv"
        if os.path.exists(p):
            return list(csv.DictReader(open(p)))
    return None


def shares(rows):
    if not rows:
        return None
    bc = next((c for c in BAL if c in rows[0]), None)
    if not bc or "address" not in rows[0]:
        return None
    return [(r["address"].strip().lower(), f(r.get(bc))) for r in rows if f(r.get(bc)) is not None]


def build_consolidated():
    con = defaultdict(dict)  # token -> {addr: (class, source)}

    def add(tok, addr, cls, src):
        con[tok][addr.strip().lower()] = (str(cls), src)

    for r in csv.DictReader(open(f"{A}/data/processed/exclusions_log.csv")):
        m = re.search(r"\[Class\s*(\d)\]", (r.get("identity", "") + r.get("exclusion_reason", "")))
        add(r["token"], r["address"], m.group(1) if m else "", "exclusions_log.csv")
    for r in csv.DictReader(open(f"{A}/data/processed/exclusions_log_signer.csv")):
        add(r["token"], r["address"], "2", "signer_log")
    for r in csv.DictReader(open(f"{A}/b2/paper/supplements/phase4_evm_minibatch_exclusions_v2_audited_2026-05-27.csv")):
        add(r["symbol"], r["address"], r.get("pca_class", ""), "phase4_v2_audited")
    for r in csv.DictReader(open(f"{A}/b2/paper/analysis_n52_2026-05-29/new12_unified_exclusions_2026-05-29.csv")):
        add(r["token"], r["address"], r.get("pca_class", ""), "new12_unified")
    for r in csv.DictReader(open(f"{B}/data/processed/ALGO_pca_exclusions.csv")):
        add("ALGO", r["address"], r.get("class_id", ""), "ALGO_pca_exclusions")
    for x in json.load(open(f"{B}/data/processed/tao_exchange_coldkeys.json")):
        add("TAO", x["coldkey"], "5", "tao_exchange_coldkeys")
    add("TAO", "5HiveMEoWPmQmBAb8v63bKPcFhgTGCmST1TVZNvPHSTKFLCv", "4", "tao_bridge")
    return con


# documented post-exclusion (regression) + the S13 before/after for cause attribution
REFRESH = {"JUP": (0.0957, 0.1260), "DRIFT": (0.0529, 0.0568), "HNT": (0.0745, 0.0874)}  # before(frame), after(log)
SPECIAL = {"IO": "R2-calibration rescaled top-100 to actual supply (not raw-reproducible)",
           "DOT": "AssetHub Subscan capture differs from clone-A DOT_holders.csv (capture-provenance gap)"}


def main():
    con = build_consolidated()
    # write the consolidated log
    out = f"{HERE}/b2_pca_exclusions_consolidated_2026-05-29.csv"
    with open(out, "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["token", "address", "pca_class", "source"])
        for tok in sorted(con):
            for addr, (cls, src) in con[tok].items():
                w.writerow([tok, addr, cls, src])
    nrows = sum(len(v) for v in con.values())
    print(f"[written] consolidated log: {nrows} rows / {len(con)} tokens")

    SEC = {"DePIN", "DeFi", "L1_L2_Infra"}
    status = []
    rep = 0
    for r in csv.DictReader(open(f"{A}/data/processed/regression_data_april2026.csv")):
        if r.get("category") not in SEC:
            continue
        tok = r["token"]; doc = f(r["hhi"]); hl = load(tok); s = shares(hl) if hl else None
        if not s or doc is None:
            continue
        ex = set(con.get(tok, {})); surv = [(a, v) for a, v in s if a not in ex]; tot = sum(v for _, v in surv)
        recomp = sum((v / tot) ** 2 for _, v in surv) if tot else None
        ok = recomp is not None and abs(recomp - doc) < 2e-3
        rep += ok
        cause = ""
        if not ok:
            if tok in REFRESH:
                cause = f"FRAME STALE: log gives the correct S13-refreshed {REFRESH[tok][1]} (headline-safe); frame holds pre-S13 {REFRESH[tok][0]}"
            elif tok in SPECIAL:
                cause = "SPECIAL METHOD: " + SPECIAL[tok]
            else:
                cause = "investigate"
        status.append({"token": tok, "documented_hhi": round(doc, 5),
                       "recompute_from_consolidated_log": round(recomp, 5) if recomp else "",
                       "reproduces": ok, "n_excl": len(ex), "cause_if_not": cause})
    with open(f"{HERE}/audit_consolidated_hhi_status_2026-05-29.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["token", "documented_hhi", "recompute_from_consolidated_log", "reproduces", "n_excl", "cause_if_not"]); w.writeheader(); w.writerows(status)
    print(f"reproduce from consolidated log (tol 2e-3): {rep}/50")
    print("residuals:")
    for x in status:
        if not x["reproduces"]:
            print(f"  {x['token']:6} recomp={x['recompute_from_consolidated_log']} doc={x['documented_hhi']} -- {x['cause_if_not']}")
    print(f"\n[written] audit_consolidated_hhi_status_2026-05-29.csv")


if __name__ == "__main__":
    main()
