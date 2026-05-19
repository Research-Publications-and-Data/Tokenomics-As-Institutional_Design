"""
Synergy Index full-sample expansion: 40 protocols across 5 philosophical lenses.

Anchors: 12 original scores from S3_scoring_tables.md (Uniswap, Compound, Aave,
MakerDAO, Lido, Helium, DIMO, Anyone Protocol, Optimism, Arbitrum, ENS, GEODNET).
Extension: 28 protocols scored 2026-05-19 using governance documentation, on-chain
proposal records, and protocol forum activity, anchored to the original 12.

Scoring scale: 0 = absent, 1 = minimal, 2 = partial, 3 = exemplary. See S2 for
full criterion definitions. Single coder (ZZ); inter-rater reliability deferred
to future work per S2 + Section 4.8.

Output: Synergy Index (arithmetic mean + geometric mean) and HHI correlation.

Run: python3 synergy_index_full_sample_2026-05-19.py
"""

import numpy as np
from scipy import stats
import csv
from pathlib import Path

# All 40 protocols; format: (Protocol, category, HHI, [Pub, Fair, Non-Dom, Poly, Know], evidence)
# Categories: DeFi, DePIN, L1_L2_Infra, Social_Dead
PROTOCOLS = [
    # Original 12 anchors (from S3_scoring_tables.md)
    ("Uniswap", "DeFi", 0.010, [2.00, 1.00, 2.00, 1.00, 1.00], "Original S3 anchor"),
    ("Compound", "DeFi", 0.009, [2.00, 1.25, 2.00, 1.00, 1.00], "Original S3 anchor"),
    ("Aave", "DeFi", 0.013, [2.25, 1.50, 2.00, 1.25, 1.25], "Original S3 anchor"),
    ("MakerDAO", "DeFi", 0.040, [2.00, 0.75, 1.75, 2.00, 1.50], "Original S3 anchor"),
    ("Lido", "DeFi", 0.008, [1.75, 1.25, 1.75, 1.25, 1.00], "Original S3 anchor"),
    ("Helium", "DePIN", 0.074, [2.00, 1.00, 2.00, 2.00, 2.00], "Original S3 anchor"),
    ("DIMO", "DePIN", 0.025, [1.50, 1.25, 1.75, 1.50, 1.50], "Original S3 anchor"),
    ("Anyone Protocol", "DePIN", 0.013, [1.00, 1.00, 1.00, 1.00, 1.00], "Original S3 anchor"),
    ("Optimism", "L1_L2_Infra", 0.009, [2.25, 1.75, 2.25, 2.00, 1.25], "Original S3 anchor"),
    ("Arbitrum", "L1_L2_Infra", 0.012, [2.00, 1.50, 2.00, 1.75, 1.25], "Original S3 anchor"),
    ("ENS", "L1_L2_Infra", 0.071, [1.75, 1.00, 1.75, 1.25, 1.00], "Original S3 anchor"),
    ("GEODNET", "DePIN", 0.060, [2.00, 1.00, 1.00, 1.00, 2.00], "Original S3 anchor (Table 2)"),
    # 28 protocols added 2026-05-19
    ("Curve", "DeFi", 0.014, [2.00, 0.75, 1.50, 1.50, 2.00],
     "Snapshot + on-chain veCRV proposals; gauge committee aggregates weekly demand signals (Hayek); lock-duration weighting structurally privileges long-lockers (Rawls deficit)"),
    ("Rocket Pool", "DeFi", 0.039, [2.25, 1.50, 2.00, 2.00, 1.00],
     "Mature pDAO + oDAO + GMC tri-cameral structure (Ostrom strength); node-operator + minipool floor mechanism"),
    ("Jupiter", "DeFi", 0.096, [1.50, 1.00, 1.00, 1.00, 1.00],
     "JUP Realms governance; LFG launchpad partial floor; less mature contestation infrastructure"),
    ("Maple Finance", "DeFi", 0.024, [1.75, 1.00, 1.50, 1.00, 1.00],
     "Governance forum + on-chain proposals; lender / borrower stake structure"),
    ("GMX", "DeFi", 0.065, [2.00, 1.00, 1.50, 1.00, 1.50],
     "Active Snapshot governance; GLP price-signal mechanism (partial Hayek); broader voter pool"),
    ("Drift", "DeFi", 0.053, [1.50, 1.00, 1.00, 1.00, 1.00],
     "DRIFT Realms; early-stage governance documentation"),
    ("Ether.Fi", "DeFi", 0.042, [1.50, 1.00, 1.00, 1.00, 1.00],
     "Governance forum + on-chain proposals; basic structure"),
    ("The Graph", "L1_L2_Infra", 0.033, [2.00, 1.50, 2.00, 2.00, 1.50],
     "GIP process; indexers + curators + delegators + Council polycentric structure (Ostrom strength); query-fee market signals"),
    ("Polygon", "L1_L2_Infra", 0.035, [2.00, 1.25, 1.50, 1.50, 1.00],
     "PIPs; multi-chain Foundation veto; validator-stake floor"),
    ("Hyperliquid", "DeFi", 0.005, [2.00, 1.00, 1.00, 0.00, 2.00],
     "Foundation-led; Assistance Fund auto-burns trade fees (strong Hayek price-signal coupling); monocentric polycentricity floor"),
    ("Balancer", "DeFi", 0.029, [2.00, 1.00, 1.50, 1.50, 2.00],
     "BIP process; gauge committee + safety multisig + veBAL; gauge votes for liquidity allocation (Hayek mechanism)"),
    ("IoTeX", "DePIN", 0.189, [1.50, 1.00, 1.00, 1.50, 1.50],
     "IIPs; delegate voting; DePIN-specific machine-data signals into reward calculation"),
    ("WeatherXM", "DePIN", 0.148, [1.50, 1.00, 1.00, 1.00, 2.00],
     "WMIPs analog; location-based reward weighting; weather data quality signals (Hayek mechanism)"),
    ("Grass", "DePIN", 0.035, [1.50, 1.00, 1.00, 0.50, 1.50],
     "Basic governance forum; bandwidth quality signals; foundation-led polycentricity floor"),
    ("Livepeer", "DePIN", 0.199, [1.50, 1.00, 1.00, 1.00, 2.00],
     "LIPs + Snapshot; orchestrator-delegator structure; encoding job market signals"),
    ("Filecoin", "DePIN", 0.022, [2.00, 1.25, 2.00, 2.50, 2.00],
     "Mature FIP process; FIL Foundation + Protocol Labs + storage providers + retrieval markets polycentric; storage market price signals (strong Hayek mechanism)"),
    ("Render", "DePIN", 0.027, [1.50, 1.00, 1.00, 1.00, 1.50],
     "RIPs + Snapshot; GPU job pricing signals"),
    ("Pokt Network", "DePIN", 0.090, [2.00, 1.00, 1.50, 1.50, 1.50],
     "PUPs; node operators + portal partners + DAO polycentric; relay-volume signals"),
    ("LayerZero", "L1_L2_Infra", 0.014, [1.50, 1.00, 1.00, 1.00, 1.00],
     "DVN configuration public; operator-centric governance"),
    ("Wormhole", "L1_L2_Infra", 0.012, [1.50, 1.00, 1.00, 1.00, 1.00],
     "WIPs; guardian-set governance"),
    ("Morpheus AI", "DePIN", 0.046, [1.50, 1.00, 1.00, 1.00, 1.50],
     "Morpheus.os governance docs; AI agent quality signals (theoretical)"),
    ("Axelar", "L1_L2_Infra", 0.027, [1.75, 1.00, 1.50, 1.25, 1.00],
     "AIP process; validator-set governance"),
    ("MetaDAO", "DeFi", 0.015, [2.00, 1.00, 2.50, 0.50, 2.50],
     "Futarchy: structural contestability via prediction markets (Pettit strength); explicit Hayek information-aggregation mechanism; single-mechanism polycentricity"),
    ("Gitcoin", "Social_Dead", 0.022, [2.25, 2.00, 1.75, 2.00, 1.50],
     "Mature GIPs + Snapshot + Stewards; quadratic funding (strong Rawls floor-protection by design); QF aggregates dispersed signals"),
    ("Token Engineering Commons", "Social_Dead", 0.028, [1.50, 1.50, 1.50, 1.50, 1.50],
     "Commons Hub conviction voting; working-group polycentric structure (pre-stagnation)"),
    ("Aethir", "DePIN", 0.087, [1.00, 0.50, 1.00, 0.50, 1.50],
     "Limited public governance documentation; heavy team / investor allocation (62%); GPU compute market signals"),
    ("Hivemapper", "DePIN", 0.018, [1.50, 1.50, 1.00, 1.00, 2.50],
     "MIPs; per-driver caps (Rawls fairness mechanism); AI training data quality signals (explicit Hayek mechanism)"),
    ("io.net", "DePIN", 0.125, [1.00, 1.00, 1.00, 0.50, 1.50],
     "Early-stage governance; foundation-led; GPU compute pricing signals"),
]


def main():
    print(f"Total scored: {len(PROTOCOLS)}/40")

    results = []
    for name, cat, hhi, scores, _ in PROTOCOLS:
        arith = float(np.mean(scores))
        s_clipped = [max(v, 0.01) for v in scores]
        geom = float(stats.gmean(s_clipped))
        results.append((name, cat, hhi, arith, geom, scores))

    results_sorted = sorted(results, key=lambda r: -r[3])
    print(f"\n{'Rank':>4s} {'Protocol':27s} {'HHI':>7s} {'Arith':>6s} {'Geom':>6s}  P/F/N/O/K")
    for i, (n, c, h, ar, gm, s) in enumerate(results_sorted, 1):
        sstr = "/".join([f"{x:.2f}" for x in s])
        print(f"{i:>4d} {n:27s} {h:>7.4f} {ar:>6.2f} {gm:>6.2f}  {sstr}")

    arith_vals = np.array([r[3] for r in results])
    geom_vals = np.array([r[4] for r in results])
    hhi_vals = np.array([r[2] for r in results])

    rho_a, p_a = stats.spearmanr(arith_vals, hhi_vals)
    rho_g, p_g = stats.spearmanr(geom_vals, hhi_vals)
    r_a, p_ra = stats.pearsonr(arith_vals, hhi_vals)
    rho_ag, p_ag = stats.spearmanr(arith_vals, geom_vals)

    print(f"\n=== Synergy Index vs HHI (N = 40 full sample) ===")
    print(f"Arithmetic Synergy vs HHI: Spearman rho = {rho_a:.4f} (p = {p_a:.4f}); Pearson r = {r_a:.4f} (p = {p_ra:.4f})")
    print(f"Geometric Synergy vs HHI:  Spearman rho = {rho_g:.4f} (p = {p_g:.4f})")
    print(f"Arith vs Geom rank agreement: Spearman rho = {rho_ag:.4f} (p = {p_ag:.4f})")

    defi = [r[3] for r in results if r[1] == "DeFi"]
    depin = [r[3] for r in results if r[1] == "DePIN"]
    infra = [r[3] for r in results if r[1] == "L1_L2_Infra"]
    social = [r[3] for r in results if r[1] == "Social_Dead"]
    print(f"\nSector mean Synergy: DeFi {np.mean(defi):.2f} (N={len(defi)}); "
          f"DePIN {np.mean(depin):.2f} (N={len(depin)}); "
          f"Infra {np.mean(infra):.2f} (N={len(infra)}); "
          f"Social {np.mean(social):.2f} (N={len(social)})")

    mw = stats.mannwhitneyu(depin, defi, alternative="two-sided")
    print(f"DePIN vs DeFi Synergy: MW U = {mw.statistic:.0f}, p = {mw.pvalue:.4f}")

    out_csv = Path(__file__).parent / "synergy_index_full_sample_2026-05-19.csv"
    with out_csv.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Protocol", "Category", "HHI", "Publicity", "Fairness",
                    "NonDomination", "Polycentricity", "KnowledgeUse",
                    "Synergy_arith", "Synergy_geom", "Evidence"])
        for name, cat, hhi, scores, ev in PROTOCOLS:
            arith = float(np.mean(scores))
            s_clipped = [max(v, 0.01) for v in scores]
            geom = float(stats.gmean(s_clipped))
            w.writerow([name, cat, f"{hhi:.4f}"] +
                       [f"{s:.2f}" for s in scores] +
                       [f"{arith:.4f}", f"{geom:.4f}", ev])
    print(f"\nWrote: {out_csv}")


if __name__ == "__main__":
    main()
