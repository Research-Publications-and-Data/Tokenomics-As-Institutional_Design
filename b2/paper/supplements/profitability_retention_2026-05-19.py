"""
Profitability-vs-insider-retention cross-sectional analysis (N-expanded).

Tests whether protocol profitability or size correlates with insider position
retention in the current top-10 holder set.

Inputs:
- data/processed/regression_data_april2026.csv: revenue (Token Terminal +
  on-chain fallback), FDV, market-cap, subsidy ratio (TT + on-chain
  fallback), treasury, initial insider allocation %
- data/processed/insider_analysis_results_v3.csv: insider_count_frac and
  insider_balance_frac in current top-10

Sample-expansion strategy (2026-05-19 update):
- Revenue: prefer Token Terminal value; fall back to on-chain revenue when
  TT is missing or zero. Expands revenue sample from N=30 to N=31
  (adds Livepeer).
- Subsidy ratio: prefer Token Terminal value; fall back to on-chain
  subsidy_ratio when TT is missing. Expands subsidy sample from N=15
  to N=22 (adds 7 DePIN protocols).
- Size-only proxies (FDV, market cap, treasury) reported separately as
  they measure size rather than profitability per se; they reach maximum-N
  specifications (36 for FDV, 33 for market cap, 24 for treasury).

Output:
- profitability_retention_2026-05-19.csv: per-protocol joined data
- profitability_retention_summary_2026-05-19.csv: full specification table
"""

import csv
import numpy as np
from pathlib import Path
from scipy import stats as sps


REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
CSV_PATH = REPO_ROOT / "data" / "processed" / "regression_data_april2026.csv"
INSIDER_PATH = REPO_ROOT / "data" / "processed" / "insider_analysis_results_v3.csv"


def _f(x):
    try:
        v = float(x or "nan")
        return v if v == v else float("nan")  # handle nan
    except (ValueError, TypeError):
        return float("nan")


def load_insider():
    out = {}
    with INSIDER_PATH.open() as f:
        for r in csv.DictReader(f):
            v_c = _f(r.get("insider_count_frac"))
            v_b = _f(r.get("insider_balance_frac"))
            if not np.isnan(v_c) and not np.isnan(v_b):
                out[r["token"]] = {
                    "insider_count_frac": v_c,
                    "insider_balance_frac": v_b,
                }
    return out


def main():
    insider = load_insider()
    records = []
    with CSV_PATH.open() as f:
        for r in csv.DictReader(f):
            tok = r["token"]
            ins = insider.get(tok)
            if ins is None:
                continue
            rev_tt = _f(r.get("revenue_annual_usd"))
            rev_oc = _f(r.get("revenue_onchain_usd"))
            # Combined revenue: prefer TT, fall back to on-chain
            if not np.isnan(rev_tt) and rev_tt > 0:
                rev = rev_tt
                rev_source = "TT"
            elif not np.isnan(rev_oc) and rev_oc > 0:
                rev = rev_oc
                rev_source = "on-chain"
            else:
                rev = float("nan")
                rev_source = "none"
            sub_tt = _f(r.get("subsidy_ratio"))
            sub_oc = _f(r.get("subsidy_ratio_onchain"))
            # Note: subsidy_ratio = 0 is meaningful (zero emissions per dollar
            # of revenue; protocols with no protocol-level emissions like
            # MakerDAO Surplus Auction, Arbitrum fixed-supply, Maple buyback).
            # Only treat NaN as missing data.
            if not np.isnan(sub_tt):
                sub = sub_tt
                sub_source = "TT"
            elif not np.isnan(sub_oc):
                sub = sub_oc
                sub_source = "on-chain"
            else:
                sub = float("nan")
                sub_source = "none"
            fdv = _f(r.get("fdv_usd"))
            mcap = _f(r.get("market_cap_usd"))
            treasury = _f(r.get("treasury_usd"))
            insider_pct = _f(r.get("insider_pct"))
            rev_per_fdv = rev / fdv if not np.isnan(rev) and not np.isnan(fdv) and fdv > 0 else float("nan")
            rev_per_mcap = rev / mcap if not np.isnan(rev) and not np.isnan(mcap) and mcap > 0 else float("nan")
            inv_sub = 1 / sub if not np.isnan(sub) and sub > 0 else float("nan")
            records.append({
                "protocol": r["protocol"],
                "token": tok,
                "category": r["category"],
                "revenue": rev,
                "revenue_source": rev_source,
                "log_revenue": np.log(rev) if not np.isnan(rev) and rev > 0 else float("nan"),
                "fdv": fdv,
                "log_fdv": np.log(fdv) if not np.isnan(fdv) and fdv > 0 else float("nan"),
                "market_cap": mcap,
                "log_market_cap": np.log(mcap) if not np.isnan(mcap) and mcap > 0 else float("nan"),
                "treasury": treasury,
                "log_treasury": np.log(treasury) if not np.isnan(treasury) and treasury > 0 else float("nan"),
                "rev_per_fdv": rev_per_fdv,
                "rev_per_mcap": rev_per_mcap,
                "subsidy_ratio": sub,
                "subsidy_source": sub_source,
                "inv_subsidy_ratio": inv_sub,
                "insider_pct_initial": insider_pct,
                "insider_count_frac_top10": ins["insider_count_frac"],
                "insider_balance_frac_top10": ins["insider_balance_frac"],
            })

    print(f"Joined sample with insider classification: N = {len(records)}")

    def corr(x, y, label):
        valid = [(a, b) for a, b in zip(x, y) if not (np.isnan(a) or np.isnan(b))]
        if len(valid) < 4:
            return None
        x_arr = np.array([v[0] for v in valid])
        y_arr = np.array([v[1] for v in valid])
        pr, pp = sps.pearsonr(x_arr, y_arr)
        sr, sp = sps.spearmanr(x_arr, y_arr)
        return {
            "test": label,
            "N": len(valid),
            "pearson_r": float(pr),
            "pearson_p": float(pp),
            "spearman_rho": float(sr),
            "spearman_p": float(sp),
        }

    summary = []
    profitability_proxies = {
        "log(revenue, TT-pref-onchain-fallback)": [r["log_revenue"] for r in records],
        "revenue / FDV": [r["rev_per_fdv"] for r in records],
        "revenue / market_cap": [r["rev_per_mcap"] for r in records],
        "1 / subsidy_ratio (TT-pref-onchain-fallback)": [r["inv_subsidy_ratio"] for r in records],
    }
    size_proxies = {
        "log(FDV)": [r["log_fdv"] for r in records],
        "log(market_cap)": [r["log_market_cap"] for r in records],
        "log(treasury)": [r["log_treasury"] for r in records],
    }
    retention_proxies = {
        "insider_count_frac_top10": [r["insider_count_frac_top10"] for r in records],
        "insider_balance_frac_top10": [r["insider_balance_frac_top10"] for r in records],
    }

    print("\n=== Profitability proxies vs insider retention ===")
    for p_name, p_vals in profitability_proxies.items():
        for r_name, r_vals in retention_proxies.items():
            res = corr(p_vals, r_vals, f"{p_name} vs {r_name}")
            if res:
                summary.append(res)
                sig_p = "*" if res["pearson_p"] < 0.05 else ("." if res["pearson_p"] < 0.10 else " ")
                sig_s = "*" if res["spearman_p"] < 0.05 else ("." if res["spearman_p"] < 0.10 else " ")
                print(f"  {res['test']}:")
                print(f"    N={res['N']}, Pearson r = {res['pearson_r']:+.3f} (p = {res['pearson_p']:.4f}) {sig_p}; Spearman rho = {res['spearman_rho']:+.3f} (p = {res['spearman_p']:.4f}) {sig_s}")

    print("\n=== Size proxies vs insider retention ===")
    for p_name, p_vals in size_proxies.items():
        for r_name, r_vals in retention_proxies.items():
            res = corr(p_vals, r_vals, f"{p_name} vs {r_name}")
            if res:
                summary.append(res)
                sig_p = "*" if res["pearson_p"] < 0.05 else ("." if res["pearson_p"] < 0.10 else " ")
                sig_s = "*" if res["spearman_p"] < 0.05 else ("." if res["spearman_p"] < 0.10 else " ")
                print(f"  {res['test']}:")
                print(f"    N={res['N']}, Pearson r = {res['pearson_r']:+.3f} (p = {res['pearson_p']:.4f}) {sig_p}; Spearman rho = {res['spearman_rho']:+.3f} (p = {res['spearman_p']:.4f}) {sig_s}")

    # Burn-active vs subsidizing subset analysis (subsidy_ratio < 1 vs >= 1)
    # Note: subsidy_ratio = 0 is included as the MAXIMALLY net-deflationary case
    # (zero emissions per dollar of revenue; e.g., MakerDAO MKR Surplus Auction,
    # Arbitrum fixed-supply ARB, Maple Finance SYRUP buyback).
    burn_active = [r for r in records if not np.isnan(r["subsidy_ratio"]) and r["subsidy_ratio"] < 1]
    subsidizing = [r for r in records if not np.isnan(r["subsidy_ratio"]) and r["subsidy_ratio"] >= 1]
    print(f"\n=== Burn-active vs subsidizing subset (Mann-Whitney) ===")
    print(f"Net deflationary (subsidy_ratio < 1): N = {len(burn_active)}")
    for r in sorted(burn_active, key=lambda x: x["subsidy_ratio"]):
        print(f"  {r['protocol']:25s} subsidy={r['subsidy_ratio']:.3f}")
    print(f"Net inflationary (subsidy_ratio >= 1): N = {len(subsidizing)}")
    for retention_field, label in [("insider_count_frac_top10", "insider_count"), ("insider_balance_frac_top10", "insider_balance")]:
        ba = [r[retention_field] for r in burn_active]
        sb = [r[retention_field] for r in subsidizing]
        if len(ba) >= 3 and len(sb) >= 3:
            mw = sps.mannwhitneyu(ba, sb, alternative="two-sided")
            psd = np.sqrt(((len(ba)-1)*np.var(ba, ddof=1) + (len(sb)-1)*np.var(sb, ddof=1)) / (len(ba)+len(sb)-2))
            d = (np.mean(ba) - np.mean(sb)) / psd if psd > 0 else float("nan")
            print(f"  {label}: burn-active mean = {np.mean(ba):.3f} (N={len(ba)}); subsidizing mean = {np.mean(sb):.3f} (N={len(sb)})")
            print(f"    MW U = {mw.statistic:.0f}, p = {mw.pvalue:.4f}, Cohen's d = {d:+.3f}")
            summary.append({
                "test": f"burn-active vs subsidizing on {label} (Mann-Whitney)",
                "N": len(ba) + len(sb),
                "pearson_r": float("nan"),
                "pearson_p": float("nan"),
                "spearman_rho": float(d),  # repurpose for Cohen's d
                "spearman_p": float(mw.pvalue),
            })

    print("\n=== Initial insider_pct vs profitability/size proxies ===")
    initial = [r["insider_pct_initial"] for r in records]
    for p_name, p_vals in {**profitability_proxies, **size_proxies}.items():
        res = corr(initial, p_vals, f"insider_pct_initial vs {p_name}")
        if res:
            summary.append(res)
            sig_p = "*" if res["pearson_p"] < 0.05 else ("." if res["pearson_p"] < 0.10 else " ")
            print(f"  {p_name}: N={res['N']}, Pearson r = {res['pearson_r']:+.3f} (p = {res['pearson_p']:.4f}) {sig_p}")

    # Write per-protocol CSV
    out_path = Path(__file__).parent / "profitability_retention_2026-05-19.csv"
    fieldnames = [
        "protocol", "token", "category",
        "revenue", "revenue_source", "log_revenue",
        "fdv", "log_fdv", "market_cap", "log_market_cap",
        "treasury", "log_treasury",
        "rev_per_fdv", "rev_per_mcap",
        "subsidy_ratio", "subsidy_source", "inv_subsidy_ratio",
        "insider_pct_initial",
        "insider_count_frac_top10", "insider_balance_frac_top10",
    ]
    with out_path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in records:
            row = {}
            for k in fieldnames:
                v = r.get(k)
                if isinstance(v, float) and np.isnan(v):
                    row[k] = ""
                else:
                    row[k] = v
            w.writerow(row)
    print(f"\nWrote: {out_path}")

    summary_path = Path(__file__).parent / "profitability_retention_summary_2026-05-19.csv"
    with summary_path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["test", "N", "pearson_r", "pearson_p", "spearman_rho", "spearman_p"])
        w.writeheader()
        for s in summary:
            w.writerow({k: round(v, 4) if isinstance(v, float) else v for k, v in s.items()})
    print(f"Wrote: {summary_path}")


if __name__ == "__main__":
    main()
