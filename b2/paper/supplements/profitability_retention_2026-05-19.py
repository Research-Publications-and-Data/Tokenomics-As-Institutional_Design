"""
Profitability-vs-insider-retention cross-sectional analysis.

Tests whether protocol profitability (revenue, revenue/FDV, revenue/market-cap,
net-profit-per-emission) correlates with insider position retention (count
and balance fractions of insider-classified wallets remaining in the current
top-10 holder set).

Inputs:
- data/processed/regression_data_april2026.csv: revenue, FDV, market-cap,
  subsidy ratio, initial insider allocation %
- data/processed/insider_analysis_results_v3.csv: insider_count_frac and
  insider_balance_frac in current top-10

Output:
- profitability_retention_2026-05-19.csv: per-protocol joined data + summary
  statistics
"""

import csv
import numpy as np
from pathlib import Path
from scipy import stats as sps


REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
CSV_PATH = REPO_ROOT / "data" / "processed" / "regression_data_april2026.csv"
INSIDER_PATH = REPO_ROOT / "data" / "processed" / "insider_analysis_results_v3.csv"


def load_insider():
    out = {}
    with INSIDER_PATH.open() as f:
        for r in csv.DictReader(f):
            try:
                out[r["token"]] = {
                    "insider_count_frac": float(r["insider_count_frac"]),
                    "insider_balance_frac": float(r["insider_balance_frac"]),
                }
            except (ValueError, KeyError):
                pass
    return out


def main():
    insider = load_insider()
    records = []
    with CSV_PATH.open() as f:
        for r in csv.DictReader(f):
            try:
                rev = float(r.get("revenue_annual_usd", "") or "nan")
                fdv = float(r.get("fdv_usd", "") or "nan")
                mcap = float(r.get("market_cap_usd", "") or "nan")
                sub = float(r.get("subsidy_ratio", "") or "nan")
                insider_pct = float(r.get("insider_pct", "") or "nan")
            except (ValueError, KeyError):
                continue
            if np.isnan(rev) or rev == 0:
                continue
            tok = r["token"]
            ins = insider.get(tok)
            if ins is None:
                continue
            rev_per_fdv = rev / fdv if not np.isnan(fdv) and fdv > 0 else float("nan")
            rev_per_mcap = rev / mcap if not np.isnan(mcap) and mcap > 0 else float("nan")
            inv_sub = 1 / sub if not np.isnan(sub) and sub > 0 else float("nan")
            records.append({
                "protocol": r["protocol"],
                "token": tok,
                "category": r["category"],
                "revenue": rev,
                "log_revenue": np.log(rev),
                "fdv": fdv,
                "market_cap": mcap,
                "rev_per_fdv": rev_per_fdv,
                "rev_per_mcap": rev_per_mcap,
                "subsidy_ratio": sub,
                "inv_subsidy_ratio": inv_sub,
                "insider_pct_initial": insider_pct,
                "insider_count_frac_top10": ins["insider_count_frac"],
                "insider_balance_frac_top10": ins["insider_balance_frac"],
            })

    print(f"Joined sample (profitability + insider retention): N = {len(records)}")

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
    profitability = {
        "log(revenue)": [r["log_revenue"] for r in records],
        "revenue / FDV": [r["rev_per_fdv"] for r in records],
        "revenue / market_cap": [r["rev_per_mcap"] for r in records],
        "1 / subsidy_ratio (net-profit-per-emission)": [r["inv_subsidy_ratio"] for r in records],
    }
    retention = {
        "insider_count_frac_top10": [r["insider_count_frac_top10"] for r in records],
        "insider_balance_frac_top10": [r["insider_balance_frac_top10"] for r in records],
    }

    print()
    for p_name, p_vals in profitability.items():
        for r_name, r_vals in retention.items():
            res = corr(p_vals, r_vals, f"{p_name} vs {r_name}")
            if res:
                summary.append(res)
                sig = "*" if res["pearson_p"] < 0.05 else ("." if res["pearson_p"] < 0.10 else " ")
                sig_s = "*" if res["spearman_p"] < 0.05 else ("." if res["spearman_p"] < 0.10 else " ")
                print(f"  {res['test']}: N={res['N']}")
                print(f"    Pearson r = {res['pearson_r']:+.3f} (p = {res['pearson_p']:.4f}) {sig}")
                print(f"    Spearman rho = {res['spearman_rho']:+.3f} (p = {res['spearman_p']:.4f}) {sig_s}")

    # Initial insider_pct vs profitability (auxiliary)
    print("\n  Initial insider_pct vs profitability:")
    initial = [r["insider_pct_initial"] for r in records]
    for p_name, p_vals in profitability.items():
        res = corr(initial, p_vals, f"insider_pct_initial vs {p_name}")
        if res:
            sig = "*" if res["pearson_p"] < 0.05 else ("." if res["pearson_p"] < 0.10 else " ")
            print(f"    {p_name}: N={res['N']}, Pearson r = {res['pearson_r']:+.3f} (p = {res['pearson_p']:.4f}) {sig}")

    # Write per-protocol CSV
    out_path = Path(__file__).parent / "profitability_retention_2026-05-19.csv"
    fieldnames = [
        "protocol", "token", "category", "revenue", "log_revenue", "fdv", "market_cap",
        "rev_per_fdv", "rev_per_mcap", "subsidy_ratio", "inv_subsidy_ratio",
        "insider_pct_initial", "insider_count_frac_top10", "insider_balance_frac_top10",
    ]
    with out_path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in records:
            row = {k: ("" if isinstance(r.get(k), float) and np.isnan(r.get(k)) else r.get(k)) for k in fieldnames}
            w.writerow(row)
    print(f"\nWrote: {out_path}")

    # Write summary statistics CSV
    summary_path = Path(__file__).parent / "profitability_retention_summary_2026-05-19.csv"
    with summary_path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["test", "N", "pearson_r", "pearson_p", "spearman_rho", "spearman_p"])
        w.writeheader()
        for s in summary:
            w.writerow({k: round(v, 4) if isinstance(v, float) else v for k, v in s.items()})
    print(f"Wrote: {summary_path}")


if __name__ == "__main__":
    main()
