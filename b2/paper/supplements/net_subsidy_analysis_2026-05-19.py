"""
Net-flow subsidy analysis: net_subsidy = (gross_emissions - true_burns) / revenue.

Joins:
- data/processed/regression_data_april2026.csv: gross revenue + emissions + subsidy
- b2/paper/supplements/net_flow_burn_data_2026-05-19.csv: documented burn USD
- data/processed/insider_analysis_results_v3.csv: insider top-10 retention

Computes:
1. Net subsidy ratio = (gross_emissions - true_burns_usd) / revenue
   - Strict definition: true_burn only (tokens destroyed)
   - Permissive definition: true_burn + buyback_redistribute
2. Net-deflationary classification: net_subsidy < 1
3. Re-runs Mann-Whitney insider retention contrast under net-flow definition

Outputs:
- net_subsidy_analysis_2026-05-19.csv: per-protocol net subsidy values
- printed summary including new MW test
"""

import csv
import numpy as np
from pathlib import Path
from scipy import stats as sps


REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent


def load_burn_data():
    out = {}
    path = Path(__file__).parent / "net_flow_burn_data_2026-05-19.csv"
    with path.open() as f:
        for r in csv.DictReader(f):
            tok = r["token"]
            try:
                tb = float(r["true_burn_usd_annual"] or 0)
                bb = float(r["buyback_redist_usd_annual"] or 0)
            except ValueError:
                tb = 0
                bb = 0
            out[tok] = {
                "true_burn_usd_annual": tb,
                "buyback_redist_usd_annual": bb,
                "confidence": r["confidence"],
                "type": r["type"],
            }
    return out


def load_insider():
    out = {}
    path = REPO_ROOT / "data" / "processed" / "insider_analysis_results_v3.csv"
    with path.open() as f:
        for r in csv.DictReader(f):
            try:
                out[r["token"]] = {
                    "count": float(r["insider_count_frac"]),
                    "balance": float(r["insider_balance_frac"]),
                }
            except (ValueError, KeyError):
                pass
    return out


def _f(v):
    try:
        x = float(v or "nan")
        return x if x == x else float("nan")
    except (ValueError, TypeError):
        return float("nan")


def main():
    burns = load_burn_data()
    insider = load_insider()

    path = REPO_ROOT / "data" / "processed" / "regression_data_april2026.csv"
    records = []
    with path.open() as f:
        for r in csv.DictReader(f):
            tok = r["token"]
            rev_tt = _f(r.get("revenue_annual_usd"))
            rev_oc = _f(r.get("revenue_onchain_usd"))
            inc_tt = _f(r.get("incentives_annual_usd"))
            emit_oc = _f(r.get("emissions_onchain_usd"))
            # Revenue: prefer TT
            rev = rev_tt if not np.isnan(rev_tt) and rev_tt > 0 else (rev_oc if not np.isnan(rev_oc) and rev_oc > 0 else float("nan"))
            # Emissions: prefer TT
            emit = inc_tt if not np.isnan(inc_tt) else (emit_oc if not np.isnan(emit_oc) else float("nan"))
            sub_tt = _f(r.get("subsidy_ratio"))
            sub_oc = _f(r.get("subsidy_ratio_onchain"))
            sub_gross = sub_tt if not np.isnan(sub_tt) else (sub_oc if not np.isnan(sub_oc) else float("nan"))
            b = burns.get(tok, {})
            true_burn = b.get("true_burn_usd_annual", 0)
            buyback = b.get("buyback_redist_usd_annual", 0)
            ins = insider.get(tok)
            # Net subsidy: take gross_subsidy as truth, subtract burns/revenue ratio.
            # net_sub = max(0, gross_sub - burns_usd/revenue_usd)
            # When revenue or gross_subsidy missing, fall through to NaN.
            if not np.isnan(sub_gross) and not np.isnan(rev) and rev > 0:
                burn_ratio = true_burn / rev
                buyback_ratio = buyback / rev
                net_sub_strict = max(0, sub_gross - burn_ratio)
                net_sub_permissive = max(0, sub_gross - burn_ratio - buyback_ratio)
                net_emit_strict = net_sub_strict * rev
                net_emit_permissive = net_sub_permissive * rev
            elif not np.isnan(sub_gross) and (true_burn == 0):
                # Gross-subsidy known but revenue NaN; without burns, net = gross
                net_sub_strict = sub_gross
                net_sub_permissive = max(0, sub_gross)  # buyback adjustment requires revenue
                net_emit_strict = float("nan")
                net_emit_permissive = float("nan")
            else:
                net_sub_strict = float("nan")
                net_sub_permissive = float("nan")
                net_emit_strict = float("nan")
                net_emit_permissive = float("nan")
            records.append({
                "protocol": r["protocol"],
                "token": tok,
                "category": r["category"],
                "revenue_usd": rev,
                "gross_emissions_usd": emit,
                "true_burn_usd": true_burn,
                "buyback_redist_usd": buyback,
                "gross_subsidy": sub_gross,
                "net_subsidy_strict": net_sub_strict,
                "net_subsidy_permissive": net_sub_permissive,
                "net_emissions_strict": net_emit_strict,
                "net_emissions_permissive": net_emit_permissive,
                "insider_count_top10": ins["count"] if ins else float("nan"),
                "insider_balance_top10": ins["balance"] if ins else float("nan"),
                "confidence": b.get("confidence", ""),
            })

    # Print summary
    n_with_net = sum(1 for r in records if not np.isnan(r["net_subsidy_strict"]))
    print(f"Total protocols: {len(records)}; with net-subsidy data: N = {n_with_net}")
    print()

    # Net-deflationary classification under strict (true burns only)
    burn_active_strict = [r for r in records if not np.isnan(r["net_subsidy_strict"]) and r["net_subsidy_strict"] < 1]
    burn_active_permissive = [r for r in records if not np.isnan(r["net_subsidy_permissive"]) and r["net_subsidy_permissive"] < 1]
    subsidizing_strict = [r for r in records if not np.isnan(r["net_subsidy_strict"]) and r["net_subsidy_strict"] >= 1]
    subsidizing_permissive = [r for r in records if not np.isnan(r["net_subsidy_permissive"]) and r["net_subsidy_permissive"] >= 1]

    print(f"=== Net-deflationary classification (STRICT: true_burns only) ===")
    print(f"Net-deflationary (net_subsidy < 1): N = {len(burn_active_strict)}")
    for r in sorted(burn_active_strict, key=lambda x: x["net_subsidy_strict"]):
        print(f"  {r['protocol']:25s} ({r['category']:12s}) net_sub={r['net_subsidy_strict']:.3f}; gross_sub={r['gross_subsidy']:.3f}; burns=${r['true_burn_usd']/1e6:.1f}M")
    print(f"\nNet-inflationary: N = {len(subsidizing_strict)}")
    for r in sorted(subsidizing_strict, key=lambda x: -x["net_subsidy_strict"])[:10]:
        print(f"  {r['protocol']:25s} ({r['category']:12s}) net_sub={r['net_subsidy_strict']:.2f}; gross_sub={r['gross_subsidy']:.2f}; burns=${r['true_burn_usd']/1e6:.2f}M")

    print(f"\n=== Net-deflationary classification (PERMISSIVE: true_burns + buybacks) ===")
    print(f"Net-deflationary (net_subsidy < 1): N = {len(burn_active_permissive)}")

    # Note protocols where status FLIPPED under net-flow definition vs gross-flow
    flipped = []
    for r in records:
        gs = r["gross_subsidy"]
        ns = r["net_subsidy_strict"]
        if np.isnan(gs) or np.isnan(ns):
            continue
        gross_class = "deflationary" if gs < 1 else "inflationary"
        net_class = "deflationary" if ns < 1 else "inflationary"
        if gross_class != net_class:
            flipped.append((r["protocol"], gs, ns, r["true_burn_usd"]))
    if flipped:
        print(f"\n=== Protocols whose classification FLIPPED under net-flow definition ===")
        for proto, gs, ns, tb in flipped:
            arrow = "inflationary -> deflationary" if gs >= 1 and ns < 1 else "deflationary -> inflationary"
            print(f"  {proto:25s}: gross={gs:.2f}, net={ns:.3f}; burns=${tb/1e6:.1f}M ({arrow})")
    else:
        print("\n  No flip cases (all protocols retain gross-flow classification under strict net-flow).")

    # Mann-Whitney insider retention
    print(f"\n=== Mann-Whitney burn-active vs subsidizing (STRICT net-flow) ===")
    ba = [r for r in burn_active_strict if not np.isnan(r["insider_count_top10"])]
    sb = [r for r in subsidizing_strict if not np.isnan(r["insider_count_top10"])]
    for fld, label in [("insider_count_top10", "insider_count"), ("insider_balance_top10", "insider_balance")]:
        ba_v = [r[fld] for r in ba]
        sb_v = [r[fld] for r in sb]
        if len(ba_v) >= 3 and len(sb_v) >= 3:
            mw = sps.mannwhitneyu(ba_v, sb_v, alternative="two-sided")
            psd = np.sqrt(((len(ba_v)-1)*np.var(ba_v, ddof=1) + (len(sb_v)-1)*np.var(sb_v, ddof=1)) / (len(ba_v)+len(sb_v)-2))
            d = (np.mean(ba_v) - np.mean(sb_v)) / psd if psd > 0 else float("nan")
            print(f"  {label}: burn-active {np.mean(ba_v):.3f} (N={len(ba_v)}); subsidizing {np.mean(sb_v):.3f} (N={len(sb_v)})")
            print(f"    MW p = {mw.pvalue:.4f}; Cohen's d = {d:+.3f}")

    # Write CSV
    fieldnames = [
        "protocol", "token", "category", "revenue_usd", "gross_emissions_usd",
        "true_burn_usd", "buyback_redist_usd", "gross_subsidy",
        "net_subsidy_strict", "net_subsidy_permissive",
        "net_emissions_strict", "net_emissions_permissive",
        "insider_count_top10", "insider_balance_top10", "confidence",
    ]
    out_path = Path(__file__).parent / "net_subsidy_analysis_2026-05-19.csv"
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


if __name__ == "__main__":
    main()
