#!/usr/bin/env python3
"""B2 supplementary check: does exchange-held supply predict governance concentration,
and is the PCA-exclusion bucket distinct from the insider bucket?

Two questions:
  Q1. Does the share of supply held on centralized exchanges (CEX) predict post-exclusion
      holding HHI? (A surface supply-distribution metric, like launch allocation %.)
  Q2. Is there an empirical difference between the PCA buckets (the 5-class exclusion:
      burns / foundation-treasury / staking / bridges / CEX) and the INSIDER bucket
      (team / founder / investor / foundation / treasury / multisig)? They overlap only in
      foundation/treasury; this asks whether the concentration signal lives in the overlap.

Method: for each protocol with a raw holder list + exclusion records, classify each excluded
address into a bucket (CEX / foundation-team / bridge / staking / burn) by identity-label
keywords, and sum its share of the top-1000 balance. Correlate each bucket-share (and the
launch allocation insider_pct) with log post-exclusion HHI. Disentangle the renormalization
artifact (excluding a large chunk mechanically inflates the renormalized HHI) by also
correlating against PRE-exclusion concentration (raw top-10 share) and by a partial regression
controlling for the non-foundation-team excluded share.

Inputs (persisted; no /tmp, no live-API):
  data/processed/regression_data_april2026.csv          frame (hhi, top_pct, insider_pct, sector)
  data/processed/exclusions_log.csv                     per-address exclusions (identity labels)
  b2/paper/supplements/phase4_evm_minibatch_exclusions_v2_audited_2026-05-27.csv  FXS/SNX/GNO classes
  data/raw/holder_lists/<TOK>_holders.csv (+ sibling clone)   raw balances for share lookup

CAVEATS: N approximately 50; correlational, not causal; the foundation-team vs infrastructure
split is keyword-classified from the exclusions log (approximate at the margins); exchange-%
is share-of-top-1000, not total circulating supply. Exploratory robustness check.
"""
import csv, os, math, json
import numpy as np
import scipy.stats as ss

A = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
SIB = "/Users/zach/b2-governance-data"
HL = [os.path.join(A, "data/raw/holder_lists"), os.path.join(SIB, "data/raw/holder_lists")]
SEC = {"DePIN": "DePIN", "DeFi": "DeFi", "L1_L2_Infra": "L1"}
BAL = ["balance", "amount_algo", "amount", "value"]


def f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def load(tok):
    for d in HL:
        p = os.path.join(d, f"{tok}_holders.csv")
        if os.path.exists(p):
            return list(csv.DictReader(open(p)))
    return None


def shares(rows):
    if not rows:
        return None
    bc = next((c for c in BAL if c in rows[0]), None)
    if bc is None or "address" not in rows[0]:
        return None
    v = [(r["address"].strip().lower(), f(r.get(bc))) for r in rows if f(r.get(bc)) is not None]
    tot = sum(x for _, x in v)
    return {a: (x / tot if tot else 0.0) for a, x in v}


def bucket(r):
    s = (r.get("identity", "") + " " + r.get("exclusion_reason", "") + " " + r.get("label", "")).lower()
    if any(k in s for k in ["binance", "coinbase", "kraken", "okx", "gate", "bybit", "bithumb",
                            "upbit", "exchange", "cex", "bitvavo", "luno", "revolut", "crypto.com",
                            "htx", "kucoin", "mexc", "bitget", "btcturk", "paribu", "etoro"]):
        return "CEX"
    if "burn" in s or "dead" in s or "0x0000000000000000000000000000000000000000" in s:
        return "burn"
    if any(k in s for k in ["bridge", "escrow", "omni", "portal", "gateway", "fraxferry", "ccip", "lockrelease"]):
        return "bridge"
    if any(k in s for k in ["stak", "vefxs", "lgno"]):
        return "staking"
    if any(k in s for k in ["foundation", "treasury", "team", "vest", "multisig", "dao", "founder",
                            "grant", "deployer", "comptroller", "timelock", "governor", "disbursement",
                            "koeppelmann", "george", "reservoir", "locking"]):
        return "foundation/team"
    return "other"


def build():
    exc = {}
    for r in csv.DictReader(open(os.path.join(A, "data/processed/exclusions_log.csv"))):
        exc.setdefault(r["token"], []).append((r["address"].strip().lower(), bucket(r)))
    cls = {"1": "burn", "2": "foundation/team", "3": "staking", "4": "bridge", "5": "CEX"}
    for r in csv.DictReader(open(os.path.join(A, "b2/paper/supplements/phase4_evm_minibatch_exclusions_v2_audited_2026-05-27.csv"))):
        exc.setdefault(r["symbol"], []).append((r["address"].strip().lower(), cls.get(r.get("pca_class", ""), bucket(r))))
    out = []
    for r in csv.DictReader(open(os.path.join(A, "data/processed/regression_data_april2026.csv"))):
        if r.get("category") not in SEC:
            continue
        hhi = f(r["hhi"]); hl = load(r["token"])
        if hhi is None or hl is None:
            continue
        sh = shares(hl)
        if sh is None:
            continue
        ex = exc.get(r["token"], [])
        ks = lambda kk: sum(sh.get(a, 0) for a, k in ex if k == kk)
        out.append({"tok": r["token"], "sec": SEC[r["category"]], "hhi": hhi, "log_hhi": math.log(hhi),
                    "exch": ks("CEX"), "found": ks("foundation/team"), "bridge": ks("bridge"),
                    "stk": ks("staking"), "pca": sum(sh.get(a, 0) for a, k in ex),
                    "insider_pct": f(r.get("insider_pct")), "top10": f(r.get("top10_pct"))})
    return out


def corr(D, xk, yk):
    pr = [(d[xk], d[yk]) for d in D if d[xk] is not None and d[yk] is not None]
    x = np.array([a for a, _ in pr]); y = np.array([b for _, b in pr])
    r, p = ss.pearsonr(x, y); rho, sp = ss.spearmanr(x, y)
    return {"r": round(float(r), 3), "p": round(float(p), 4), "rho": round(float(rho), 3),
            "rho_p": round(float(sp), 4), "N": len(pr), "mean_x": round(float(x.mean()), 4)}


def ols_hc3(D, builders):
    n = len(D); y = np.array([d["log_hhi"] for d in D])
    X = np.column_stack([np.ones(n)] + [np.array([g(d) for d in D]) for _, g in builders])
    b, _, _, _ = np.linalg.lstsq(X, y, rcond=None); e = y - X @ b; k = X.shape[1]
    XtXi = np.linalg.inv(X.T @ X); h = np.diag(X @ XtXi @ X.T)
    cov = XtXi @ (X.T @ np.diag((e ** 2) / ((1 - h) ** 2)) @ X) @ XtXi; se = np.sqrt(np.diag(cov))
    p = [2 * (1 - ss.t.cdf(abs(t), n - k)) for t in b / se]
    return [{"term": nm, "b": round(float(bb), 4), "p": round(float(pp), 4)}
            for nm, bb, pp in zip(["(int)"] + [nm for nm, _ in builders], b, p)], n


def main():
    D = build()
    res = {"N": len(D)}
    print(f"N protocols (holder list + exclusions + hhi) = {len(D)}\n")

    print("=== Q1: exchange-held % vs governance concentration ===")
    res["Q1"] = {"exch_vs_logHHI": corr(D, "exch", "log_hhi"),
                 "exch_vs_rawHHI": corr(D, "exch", "hhi"),
                 "exch_vs_top10": corr(D, "exch", "top10")}
    for k, v in res["Q1"].items():
        print(f"  {k:18} r={v['r']:+.3f} p={v['p']:.4f}  rho={v['rho']:+.3f} p={v['rho_p']:.4f}  N={v['N']} mean={v['mean_x']:.3f}")
    reg1, n1 = ols_hc3(D, [("DePIN", lambda d: 1.0 if d["sec"] == "DePIN" else 0.0),
                           ("L1", lambda d: 1.0 if d["sec"] == "L1" else 0.0),
                           ("exchange%", lambda d: d["exch"])])
    res["Q1"]["regression_logHHI_sector_exchange"] = {"N": n1, "terms": reg1}
    print("  regression log-HHI ~ sector + exchange%:", "  ".join(f"{t['term']}={t['b']:+.3f}(p={t['p']:.3f})" for t in reg1))

    print("\n=== Q2: PCA buckets vs concentration (overlap with insider = foundation/team only) ===")
    res["Q2"] = {b: corr(D, b, "log_hhi") for b in ["found", "exch", "bridge", "stk", "pca", "insider_pct"]}
    labels = {"found": "foundation/team % (PCA AND insider)", "exch": "CEX % (PCA NOT insider)",
              "bridge": "bridge % (PCA NOT insider)", "stk": "staking % (PCA NOT insider)",
              "pca": "total PCA-excluded %", "insider_pct": "insider_pct ALLOCATION (paper null)"}
    for b in ["pca", "found", "exch", "bridge", "stk", "insider_pct"]:
        v = res["Q2"][b]
        print(f"  {labels[b]:42} r={v['r']:+.3f} p={v['p']:.4f}  N={v['N']} mean={v['mean_x']:.3f}")

    print("\n=== disentangle: substantive vs renormalization ===")
    res["disentangle"] = {"found_vs_PRE_top10": corr(D, "found", "top10"),
                          "exch_vs_PRE_top10": corr(D, "exch", "top10")}
    for k, v in res["disentangle"].items():
        print(f"  {k:22} r={v['r']:+.3f} p={v['p']:.4f} N={v['N']}")
    # partial: log-HHI ~ foundation/team% + other-PCA%
    partial, npar = ols_hc3([d for d in D if d["found"] is not None],
                            [("found%", lambda d: d["found"]), ("other_PCA%", lambda d: d["pca"] - d["found"])])
    res["disentangle"]["partial_logHHI_found_otherPCA"] = {"N": npar, "terms": partial}
    print("  partial log-HHI ~ found% + other-PCA%:", "  ".join(f"{t['term']}={t['b']:+.3f}(p={t['p']:.3f})" for t in partial))

    print("\n=== exchange-held % by sector (descriptive) ===")
    res["exch_by_sector"] = {}
    for s in ("DePIN", "DeFi", "L1"):
        v = [d["exch"] for d in D if d["sec"] == s]
        res["exch_by_sector"][s] = {"mean": round(float(np.mean(v)), 4), "median": round(float(np.median(v)), 4), "N": len(v)}
        print(f"  {s:6} mean={np.mean(v):.3f} median={np.median(v):.3f} N={len(v)}")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "b2_exchange_vs_pca_insider_results_2026-05-29.json")
    json.dump(res, open(out, "w"), indent=1)
    print(f"\n[written] {os.path.relpath(out, A)}")
    print("[done] no /tmp dependency, no live-API calls.")


if __name__ == "__main__":
    main()
