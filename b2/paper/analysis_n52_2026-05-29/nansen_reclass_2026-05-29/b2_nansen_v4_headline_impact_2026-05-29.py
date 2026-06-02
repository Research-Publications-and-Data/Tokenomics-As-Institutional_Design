#!/usr/bin/env python3
"""
B2 Nansen v4 HEADLINE IMPACT (2026-05-29): re-estimate the retention-spec under
FOUR insider-retention vectors and compare to the v3-based reproduce.py baseline.
The maturity-spec (retention-independent) is the invariant sanity anchor.

Vectors (each: the 45 Nansen-reachable tokens get the named value; the 6-7 off-Nansen
frame tokens keep v3/new12):
  baseline_v3        : v3 / new12 (exactly reproduce.py)
  v4_keyword         : Tier-1 keyword rule on current Nansen labels (lower bound)
  v4_reviewed        : adversarial-reviewed (full adoption)
  v4_reviewed_safe   : reviewed for reliable-match tokens; v3 retained where current-
                       Nansen match < 7/10 (vintage-gap tokens: MKR/GRASS/JUP/W/AAVE)

READS ONLY. Mutates nothing (not v3, not the frame). Output JSON + console table.
"""
import csv, math, os, json
import numpy as np
import scipy.stats as ss

HERE = os.path.dirname(os.path.abspath(__file__))
import os as _os_anchor
_RR = _os_anchor.path.dirname(_os_anchor.path.abspath(__file__))
while _RR != _os_anchor.path.dirname(_RR) and not _os_anchor.path.exists(_os_anchor.path.join(_RR, "reproduce.py")):
    _RR = _os_anchor.path.dirname(_RR)
A = _RR
ADIR = os.path.join(A, "b2/paper/analysis_n52_2026-05-29")
SEC = {"DePIN": "DePIN", "DeFi": "DeFi", "L1_L2_Infra": "L1"}
MATCH_FLOOR = 7


def f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def ols_hc3(D, cols, dv="y"):
    n = len(D)
    y = np.array([d[dv] for d in D])
    X = np.column_stack([np.ones(n)] + [
        np.array([(1.0 if d["sec"] == c[1] else 0.0) if isinstance(c, tuple) else d[c] for d in D]) for c in cols])
    b, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
    e = y - X @ b
    k = X.shape[1]
    XtXi = np.linalg.inv(X.T @ X)
    h = np.diag(X @ XtXi @ X.T)
    cov = XtXi @ (X.T @ np.diag((e ** 2) / ((1 - h) ** 2)) @ X) @ XtXi
    se = np.sqrt(np.diag(cov))
    t = b / se
    p = [2 * (1 - ss.t.cdf(abs(tt), n - k)) for tt in t]
    return b, p


def load():
    v3 = {r["token"]: f(r.get("insider_count_frac")) for r in csv.DictReader(open(os.path.join(A, "data/processed/insider_analysis_results_v3.csv")))}
    v3 = {k: v for k, v in v3.items() if v is not None}
    new12 = {r["token"]: f(r["insider_count_frac"]) for r in csv.DictReader(open(os.path.join(ADIR, "new12_retention_vector_2026-05-29.csv")))}
    kwrows = list(csv.DictReader(open(os.path.join(HERE, "insider_retention_vector_v4_nansen_2026-05-29.csv"))))
    v4kw = {r["token"]: f(r["insider_count_frac"]) for r in kwrows}
    match = {r["token"]: int(r["n_matched_in_nansen"]) for r in kwrows}
    v4rev = {r["token"]: f(r["insider_count_frac"]) for r in csv.DictReader(open(os.path.join(HERE, "insider_retention_vector_v4_reviewed_2026-05-29.csv")))}
    rp = os.path.join(HERE, "insider_retention_vector_v4_resolved_2026-05-30.csv")
    v4res = {r["token"]: f(r["insider_count_frac"]) for r in csv.DictReader(open(rp))} if os.path.exists(rp) else {}
    tp = os.path.join(HERE, "insider_retention_vector_v4_traced_2026-05-30.csv")
    v4trc = {r["token"]: f(r["insider_count_frac"]) for r in csv.DictReader(open(tp))} if os.path.exists(tp) else {}
    return v3, new12, v4kw, v4rev, match, v4res, v4trc


def build(retfn):
    frame = []
    for r in csv.DictReader(open(os.path.join(A, "data/processed/regression_data_april2026.csv"))):
        if r.get("category") not in SEC:
            continue
        hhi = f(r["hhi"]); rev = f(r.get("revenue_annual_usd"))
        fdv = f(r.get("fdv_usd")) or f(r.get("market_cap_usd")); mat = f(r.get("maturity_years"))
        if None in (hhi, rev, fdv, mat) or fdv <= 0:
            continue
        frame.append({"tok": r["token"], "sec": SEC[r["category"]], "hhi": hhi, "y": math.log(hhi),
                      "ri": math.log10(rev / fdv + 1e-7), "mat": mat, "ret": retfn(r["token"])})
    return frame


def retspec(frame):
    Dr = [d for d in frame if d["ret"] is not None]
    b, p = ols_hc3(Dr, [("sec", "DePIN"), ("sec", "L1"), "ri", "ret"])
    return {"N": len(Dr), "depin_b": round(b[1], 4), "depin_p": round(p[1], 4),
            "ret_b": round(b[4], 4), "ret_p": round(p[4], 4)}


def main():
    v3, new12, v4kw, v4rev, match, v4res, v4trc = load()

    def base(t): return new12.get(t, v3.get(t))
    def kw(t): return v4kw[t] if t in v4kw else base(t)
    def rev(t): return v4rev[t] if t in v4rev else base(t)
    def rev_safe(t):
        if t in v4rev and match.get(t, 10) >= MATCH_FLOOR:
            return v4rev[t]
        return base(t)
    def res(t): return v4res[t] if t in v4res else base(t)
    def trc(t): return v4trc[t] if t in v4trc else base(t)

    specs = {
        "baseline_v3": retspec(build(base)),
        "v4_keyword": retspec(build(kw)),
        "v4_reviewed": retspec(build(rev)),
        "v4_reviewed_safe": retspec(build(rev_safe)),
        "v4_resolved_gapfill": retspec(build(res)),
        "v4_traced_evidence": retspec(build(trc)),
    }
    # maturity-spec invariant anchor
    Fm = build(base)
    bm, pm = ols_hc3(Fm, [("sec", "DePIN"), ("sec", "L1"), "ri", "mat"])
    maturity = {"N": len(Fm), "depin_p": round(pm[1], 4), "maturity_p": round(pm[4], 4)}

    out = {"maturity_spec_anchor": maturity, "retention_specs": specs}
    json.dump(out, open(os.path.join(HERE, "b2_nansen_v4_headline_impact_results_2026-05-29.json"), "w"), indent=1)

    print("MATURITY-spec anchor (retention-independent; reproduce.py = 0.0395):"
          f"  DePIN p={maturity['depin_p']}  N={maturity['N']}")
    print("\nRETENTION-spec DePIN coefficient under four insider-retention vectors:")
    print(f"  {'vector':20}{'N':>4}{'DePIN_b':>10}{'DePIN_p':>10}{'sig?':>6}{'ret_p':>9}")
    for name, s in specs.items():
        sig = 'YES' if s["depin_p"] < 0.05 else 'NO'
        print(f"  {name:20}{s['N']:>4}{s['depin_b']:>10}{s['depin_p']:>10}{sig:>6}{s['ret_p']:>9}")
    allsig = all(s["depin_p"] < 0.05 for s in specs.values())
    print("\n  => DePIN significant under ALL four vectors: finding ROBUST to the Nansen re-classification."
          if allsig else
          "\n  => DePIN significance is NOT uniform across vectors -> SURFACE: headline is sensitive to the insider vector.")


if __name__ == "__main__":
    main()
