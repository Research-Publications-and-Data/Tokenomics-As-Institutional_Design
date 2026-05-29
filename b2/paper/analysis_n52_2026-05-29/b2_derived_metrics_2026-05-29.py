#!/usr/bin/env python3
"""B2 derived metrics: float-to-FDV and revenue-to-FDV, computed + tested against
governance concentration. Companion to the exchange-vs-PCA-insider supplement.

These are deterministic functions of existing frame columns (market_cap_usd, fdv_usd,
revenue_annual_usd). Written to a COMPANION CSV (derived_metrics_2026-05-29.csv); the
canonical regression frame is left untouched (folding these in as first-class columns is a
CANONICAL-WRITER / author decision). Reads persisted data only; no /tmp, no live-API.

  float_to_fdv     = market_cap_usd / fdv_usd   (circulating value / fully-diluted value;
                     low float = large locked/vesting overhang, an insider-supply proxy)
  revenue_to_fdv   = revenue_annual_usd / fdv_usd      (the paper's revenue-intensity regressor)
  revenue_to_mcap  = revenue_annual_usd / market_cap_usd

Outcome tested: log post-exclusion holding HHI. Correlational, exploratory, N approximately 50.
"""
import csv, os, math, json
import numpy as np
import scipy.stats as ss

A = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
SEC = {"DePIN": "DePIN", "DeFi": "DeFi", "L1_L2_Infra": "L1"}


def f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def build():
    out = []
    for r in csv.DictReader(open(os.path.join(A, "data/processed/regression_data_april2026.csv"))):
        if r.get("category") not in SEC:
            continue
        hhi = f(r["hhi"]); mc = f(r.get("market_cap_usd")); fdv = f(r.get("fdv_usd")); rev = f(r.get("revenue_annual_usd"))
        if hhi is None:
            continue
        float_fdv = (mc / fdv) if (mc and fdv and fdv > 0) else None
        rev_fdv = (rev / fdv) if (rev is not None and fdv and fdv > 0) else None
        rev_mc = (rev / mc) if (rev is not None and mc and mc > 0) else None
        out.append({"protocol": r["protocol"], "token": r["token"], "sector": SEC[r["category"]],
                    "float_to_fdv": float_fdv, "revenue_to_fdv": rev_fdv, "revenue_to_mcap": rev_mc,
                    "hhi": hhi, "log_hhi": math.log(hhi)})
    return out


def corr(D, xk, yk="log_hhi"):
    pr = [(d[xk], d[yk]) for d in D if d[xk] is not None and d[yk] is not None]
    x = np.array([a for a, _ in pr]); y = np.array([b for _, b in pr])
    r, p = ss.pearsonr(x, y); rho, sp = ss.spearmanr(x, y)
    return {"r": round(float(r), 3), "p": round(float(p), 4), "rho": round(float(rho), 3),
            "rho_p": round(float(sp), 4), "N": len(pr), "mean_x": round(float(x.mean()), 4)}


def main():
    D = build()
    res = {"N": len(D)}
    print(f"N protocols = {len(D)}\n")
    # write companion CSV
    cols = ["protocol", "token", "sector", "float_to_fdv", "revenue_to_fdv", "revenue_to_mcap", "hhi"]
    out_csv = os.path.join(os.path.dirname(os.path.abspath(__file__)), "derived_metrics_2026-05-29.csv")
    with open(out_csv, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols); w.writeheader()
        for d in D:
            w.writerow({c: ("" if d.get(c) is None else (round(d[c], 6) if isinstance(d.get(c), float) else d[c])) for c in cols})
    print(f"[written] {os.path.relpath(out_csv, A)}\n")

    print("=== correlations vs log post-exclusion HHI ===")
    res["corr"] = {}
    for xk in ["float_to_fdv", "revenue_to_fdv", "revenue_to_mcap"]:
        v = corr(D, xk); res["corr"][xk] = v
        sig = "*" if v["p"] < 0.05 else ("." if v["p"] < 0.10 else " ")
        print(f"  {xk:16} r={v['r']:+.3f} p={v['p']:.4f}{sig} | rho={v['rho']:+.3f} p={v['rho_p']:.4f}  N={v['N']} mean={v['mean_x']:.3f}")

    print("\n=== regression: log-HHI ~ sector + float_to_fdv ===")
    Df = [d for d in D if d["float_to_fdv"] is not None]
    n = len(Df); y = np.array([d["log_hhi"] for d in Df])
    X = np.column_stack([np.ones(n), [1.0 if d["sector"] == "DePIN" else 0 for d in Df],
                         [1.0 if d["sector"] == "L1" else 0 for d in Df], [d["float_to_fdv"] for d in Df]])
    b, _, _, _ = np.linalg.lstsq(X, y, rcond=None); e = y - X @ b; k = 4
    XtXi = np.linalg.inv(X.T @ X); h = np.diag(X @ XtXi @ X.T)
    cov = XtXi @ (X.T @ np.diag((e ** 2) / ((1 - h) ** 2)) @ X) @ XtXi; se = np.sqrt(np.diag(cov))
    p = [2 * (1 - ss.t.cdf(abs(t), n - k)) for t in b / se]
    res["regression_float"] = {"N": n, "terms": []}
    for nm, bb, pp in zip(["(int)", "DePIN", "L1", "float_to_fdv"], b, p):
        print(f"   {nm:14} b={bb:+.4f} p={pp:.4f}{'*' if pp < 0.05 else ''}")
        res["regression_float"]["terms"].append({"term": nm, "b": round(float(bb), 4), "p": round(float(pp), 4)})

    print("\n=== float-to-FDV by sector (descriptive) ===")
    res["float_by_sector"] = {}
    for s in ("DePIN", "DeFi", "L1"):
        v = [d["float_to_fdv"] for d in D if d["sector"] == s and d["float_to_fdv"] is not None]
        if v:
            res["float_by_sector"][s] = {"mean": round(float(np.mean(v)), 3), "median": round(float(np.median(v)), 3), "N": len(v)}
            print(f"  {s:6} mean float={np.mean(v):.3f} median={np.median(v):.3f} N={len(v)}")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "b2_derived_metrics_results_2026-05-29.json")
    json.dump(res, open(out, "w"), indent=1)
    print(f"\n[written] {os.path.relpath(out, A)}")
    print("[done] no /tmp dependency, no live-API calls.")


if __name__ == "__main__":
    main()
