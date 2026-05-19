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
    # 28 protocols added 2026-05-19; lens means recomputed from per-criterion 20-cell scoring
    # (see generate_28_protocol_20cell_scoring.py + S3_scoring_tables_20cell_extension_2026-05-19.md)
    # following web-verification cycle 2026-05-19
    ("Curve", "DeFi", 0.014, [2.00, 0.75, 1.25, 1.50, 2.00],
     "veCRV governance at resources.curve.finance; 2500 veCRV proposal threshold; gauge-vote weekly emissions (Hayek); ve-locking structurally privileges long-lockers (Rawls deficit)"),
    ("Rocket Pool", "DeFi", 0.039, [2.50, 1.50, 1.75, 2.00, 1.00],
     "RPIPs at rpips.rocketpool.net; pDAO + oDAO + GMC tri-body; monthly treasury reports; LEB8 minipool floor mechanism"),
    ("Jupiter", "DeFi", 0.096, [1.50, 0.75, 1.25, 1.00, 1.00],
     "Governance paused June 2025 citing 'breakdown in trust'; resuming 2026 with delegated/council/hybrid model; working group elimination underway"),
    ("Maple Finance", "DeFi", 0.024, [1.75, 1.00, 1.50, 1.00, 1.00],
     "MIPs at community.maple.finance; Governor Timelock Contract (Sept 2025); SYRUP + stSYRUP voting"),
    ("GMX", "DeFi", 0.065, [2.00, 1.00, 1.50, 1.00, 1.50],
     "Active gov.gmx.io proposals; V2 GM tokens (V1 GLP legacy); GMX buyback distribution"),
    ("Drift", "DeFi", 0.053, [1.75, 1.00, 1.50, 1.75, 1.50],
     "Three-branch DAO: Realms (general) + Security Council (upgrades) + Futarchy DAO (grants via MetaDAOProject); DIP-10 community challenge as governance stress test"),
    ("Ether.Fi", "DeFi", 0.042, [1.75, 1.00, 1.00, 1.00, 1.00],
     "Numbered ETHFI DAO proposals at governance.ether.fi; revenue-share + buyback + RWA diversification proposals"),
    ("The Graph", "L1_L2_Infra", 0.033, [2.25, 1.50, 1.75, 2.00, 1.50],
     "GIP process at github.com/graphprotocol/graph-improvement-proposals; 6-of-10 Council multisig representing 5 stakeholder groups; arbitration charter GIP-0009"),
    ("Polygon", "L1_L2_Infra", 0.035, [2.25, 1.25, 1.75, 1.50, 1.00],
     "PIPs at github.com/maticnetwork/Polygon-Improvement-Proposals; 13-member Protocol Council multisig (PIP-77 refreshed); Q1 2026 most proposal-intensive quarter (9 proposals)"),
    ("Hyperliquid", "DeFi", 0.005, [2.00, 1.00, 1.50, 0.00, 2.00],
     "HIPs at hyperliquid.gitbook.io; Q1 2026 validator vote on $1B Assistance Fund sideline; Assistance Fund auto-burns 99% of fees"),
    ("Balancer", "DeFi", 0.029, [2.00, 1.00, 1.50, 1.50, 2.00],
     "BIPs at forum.balancer.fi (BIP-163 governance process); Balancer Maxis multisig; veBAL (80/20 BAL/WETH lock max 1yr); gauge votes weekly"),
    ("IoTeX", "DePIN", 0.189, [1.75, 0.75, 1.00, 1.50, 1.50],
     "IIPs at github.com/iotexproject/iips; only Delegates can create proposals (restriction); IoTeX Hub unified interface April 2026"),
    ("WeatherXM", "DePIN", 0.148, [1.50, 1.00, 1.25, 1.25, 2.00],
     "WIPs at github.com/orgs/weatherxm-network/discussions; WIP-004 SPV multiplier (Feb 2026); Association General Assembly governs"),
    ("Grass", "DePIN", 0.035, [1.50, 1.00, 1.25, 0.50, 1.50],
     "Basic governance forum; decentralized validator committee roadmap H1 2026; bandwidth-quality signals"),
    ("Livepeer", "DePIN", 0.199, [1.50, 1.00, 1.00, 1.00, 2.00],
     "LIPs at github.com/livepeer/LIPs; LIP-Meeting governance archive; Q1 2026 Base rollup migration"),
    ("Filecoin", "DePIN", 0.022, [2.50, 1.25, 2.00, 2.50, 2.00],
     "FIPs at github.com/filecoin-project/FIPs; 7-seat Community Guild (6 stakeholder groups); Constellation Program + veFIL early 2026"),
    ("Render", "DePIN", 0.027, [1.50, 1.00, 1.25, 1.00, 1.50],
     "RNPs at know.rendernetwork.com (NOT RIPs); RNP-023 Salad Network Subnet April 2026 (+60K GPUs); RENDER on Solana via Snapshot"),
    ("Pokt Network", "DePIN", 0.090, [2.25, 1.00, 1.50, 1.50, 1.50],
     "PIP/PEP/PUP triple proposal types + Constitution at github.com/pokt-network/governance; PIP-41 Shannon tokenomics Jan 2026 (97.5% mint ratio)"),
    ("LayerZero", "L1_L2_Infra", 0.014, [1.75, 1.00, 1.50, 1.25, 1.25],
     "Semiannual Protocol Fee-Switch Governance Vote; April 2026 1-of-1 DVN deprecation enforced; 50+ DVNs competitive market"),
    ("Wormhole", "L1_L2_Infra", 0.012, [2.25, 1.00, 1.75, 1.50, 1.00],
     "WIPs at forum.wormhole.com (WIP-1/2/3 all 99%+ approval with 3000+ voters); 19-Guardian set 13/19 supermajority; MultiGov multichain governance"),
    ("Morpheus AI", "DePIN", 0.046, [1.50, 1.00, 1.25, 1.25, 1.50],
     "MRC (Morpheus Request for Comments) + Snapshot voting; Atomic Governance (no central foundation); fair-launch design"),
    ("Axelar", "L1_L2_Infra", 0.027, [2.25, 1.00, 1.50, 1.25, 1.00],
     "Documentation at docs.axelar.dev/learn/evm-governance; 4 formal proposal types; 3-day voting + 33.4% quorum"),
    ("MetaDAO", "DeFi", 0.015, [2.00, 1.00, 2.25, 0.50, 2.50],
     "Futarchy via conditional-on-pass/fail markets; 96 proposals run for 14 organizations since Nov 2023; autocrat program executes; DAO-configurable TWAP sensitivity"),
    ("Gitcoin", "Social_Dead", 0.022, [2.25, 2.25, 1.75, 2.00, 1.50],
     "GIPs + Stewards + 4 named workstreams (Public Goods Funding, Sybil Defenders, Progressive Decentralization, Public Goods Prototyping); GG21 fully community-led ($933K, 11 rounds)"),
    ("Token Engineering Commons", "Social_Dead", 0.028, [2.00, 1.50, 1.50, 1.50, 1.50],
     "Disputable Conviction Voting + Celeste dispute resolution + Tao Voting (technical) + Snapshot (cultural) + Gravity Working Group; TEC Polycentric Governance Framework"),
    ("Aethir", "DePIN", 0.087, [1.50, 0.50, 1.25, 1.00, 1.50],
     "Bicameral Council + Foundation Board governance per Aethir Foundation Bylaws; 4-stage proposal pipeline (Temperature Check + Debate + Implementation Prep + on-chain Decision); 62% team/investor allocation"),
    ("Hivemapper", "DePIN", 0.018, [1.50, 1.50, 1.25, 1.00, 2.50],
     "MIPs at docs.hivemapper.com/welcome/network-governance; MIP-15 (April 2024) 25% burn-reissue + 500K HONEY weekly cap; AI Trainer quality signals"),
    ("io.net", "DePIN", 0.125, [1.00, 1.00, 1.25, 0.50, 1.50],
     "Documentation at docs.iog.net; IDE (Incentive Dynamic Engine) litepaper March 2026; core team retains control during progressive-decentralization transition; DAO planned Q2 2026"),
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
