"""
B2 R2 figure regeneration (Figures 3 through 8).

Reads canonical R2-corrected regression dataset and embedded R2 Table 7
plus participation values; writes PNG + PDF outputs to ./

Inputs:
  REG_CSV     R2-corrected per-protocol HHI / insider / subsidy table
              (Tokenomics-As-Institutional_Design clone; UNI=0.010 reflects
              universal burn-rule per DEC-146).
  Table 7     Embedded inline (Section 3.5 of PAPER.md; 10 protocols).
  Figure 6    Subset of Table 7: 5 Tally-sourced protocols (Compound,
              Aave, Uniswap, Optimism, Arbitrum) per caption.
  Figure 8    Participation data embedded inline (mirrors
              participation_april2026.csv).

Pre-R2 figure provenance: gen_exhibits_v2.py in ~/b2-governance-data/.
This script is the R2 regeneration entry point; styling intentionally
matches the pre-R2 script so figure visual identity is preserved.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import numpy as np
from scipy import stats

try:
    from adjustText import adjust_text
    HAS_ADJUST_TEXT = True
except ImportError:
    HAS_ADJUST_TEXT = False

REG_CSV = "/Users/zach/Tokenomics-As-Institutional_Design/data/processed/regression_data_april2026.csv"
OUT_DIR = Path(__file__).resolve().parent

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "font.size": 11,
    "axes.titlesize": 13,
    "axes.labelsize": 12,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "axes.spines.top": False,
    "axes.spines.right": False,
})

DEPIN_COLOR = "#2171b5"
DEFI_COLOR = "#cb6d51"
INFRA_COLOR = "#2d6a2e"
SOCIAL_COLOR = "#888888"
OUTLIER_COLOR = "#c0392b"

cat_colors_map = {
    "DeFi": DEFI_COLOR,
    "DePIN": DEPIN_COLOR,
    "L1_L2_Infra": INFRA_COLOR,
    "Social_Dead": SOCIAL_COLOR,
}


def save(fig, name):
    for ext in ("png", "pdf"):
        fig.savefig(OUT_DIR / f"{name}.{ext}", dpi=300, bbox_inches="tight")
    plt.close(fig)


reg = pd.read_csv(REG_CSV)
print(f"reg: N={len(reg)}, categories={reg['category'].value_counts().to_dict()}")
uni_hhi = reg.loc[reg["protocol"] == "Uniswap", "hhi"].values[0]
print(f"UNI HHI = {uni_hhi:.4f}  (R2 expects 0.010 after burn-rule)")


# =============================================================================
# FIGURE 3: HHI bar (all 40 protocols)
# =============================================================================
print("\n-- Fig 3: HHI bar (N=40)")
cat_order = ["DeFi", "DePIN", "L1_L2_Infra", "Social_Dead"]
df3 = reg.sort_values(["category", "hhi"], ascending=[True, True]).reset_index(drop=True)

y_pos, colors, labels, values = [], [], [], []
current_y = 0
for cat in cat_order:
    subset = df3[df3["category"] == cat]
    if len(subset) == 0:
        continue
    for _, row in subset.iterrows():
        y_pos.append(current_y)
        colors.append(cat_colors_map[cat])
        labels.append(row["protocol"])
        values.append(row["hhi"])
        current_y += 1
    current_y += 0.6

fig, ax = plt.subplots(figsize=(12, 14))
ax.barh(y_pos, values, color=colors, height=0.72, edgecolor="white", linewidth=0.3)

x_max = max(values)
for y, v in zip(y_pos, values):
    ax.text(v + x_max * 0.008, y, f"{v:.3f}", va="center", fontsize=8)

ax.set_yticks(y_pos)
ax.set_yticklabels(labels, fontsize=9)
ax.invert_yaxis()
ax.set_xlim(0, max(x_max * 1.18, 0.30))

ax.axvline(x=0.25, color="gray", linestyle="--", linewidth=1, alpha=0.7)
ax.text(0.252, len(y_pos) - 2, "HHI = 0.25\n(mod.\nconcentrated)",
        fontsize=7.5, color="gray", va="top")

ax.set_xlabel("Herfindahl-Hirschman Index (HHI)")

from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor=cat_colors_map[c],
          label=f"{c.replace('_', ' ').replace('Social Dead', 'Social')} (N={len(df3[df3['category']==c])})")
    for c in cat_order if c in df3["category"].values
]
ax.legend(handles=legend_elements, loc="lower right", fontsize=9)

ax.set_title("Governance Concentration (HHI) Across 40 Protocols",
             fontsize=14, fontweight="bold", pad=12)

fig.text(0.5, -0.005,
         "Source: Dune Analytics + Helius DAS API (March 2026). "
         "69 protocol-controlled addresses excluded across 20 protocols.",
         ha="center", fontsize=8, style="italic", color="gray")

save(fig, "fig3_hhi_bar_40protocols")


# =============================================================================
# FIGURE 4: Sector boxplot (DePIN vs DeFi)
# =============================================================================
print("-- Fig 4: Sector boxplot")
defi = reg[reg["category"] == "DeFi"]["hhi"]
depin = reg[reg["category"] == "DePIN"]["hhi"]

stat, p_mw = stats.mannwhitneyu(depin, defi, alternative="two-sided")
d_cohen = (depin.mean() - defi.mean()) / np.sqrt((depin.std()**2 + defi.std()**2) / 2)
print(f"  DeFi:  mean={defi.mean():.4f}, N={len(defi)}")
print(f"  DePIN: mean={depin.mean():.4f}, N={len(depin)}")
print(f"  MW p={p_mw:.4f}, Cohen d={d_cohen:.3f}")

fig, ax = plt.subplots(figsize=(7, 8))
bp = ax.boxplot(
    [defi.values, depin.values], positions=[1, 2], widths=0.5,
    patch_artist=True, showmeans=True,
    meanprops=dict(marker="D", markerfacecolor="white", markeredgecolor="black", markersize=8),
    medianprops=dict(color="black", linewidth=2),
)
bp["boxes"][0].set_facecolor(DEFI_COLOR); bp["boxes"][0].set_alpha(0.4)
bp["boxes"][1].set_facecolor(DEPIN_COLOR); bp["boxes"][1].set_alpha(0.4)

np.random.seed(42)
for data, pos, color in [(defi, 1, DEFI_COLOR), (depin, 2, DEPIN_COLOR)]:
    jitter = np.random.normal(0, 0.04, len(data))
    ax.scatter(pos + jitter, data.values, color=color, alpha=0.6, s=40,
               zorder=3, edgecolors="white", linewidth=0.5)

ax.text(1.35, defi.mean(), f"Mean: {defi.mean():.3f}", va="center", fontsize=10)
ax.text(2.35, depin.mean(), f"Mean: {depin.mean():.3f}", va="center", fontsize=10)

y_top = max(depin.max(), defi.max()) + 0.015
ax.plot([1, 1, 2, 2], [y_top, y_top + 0.005, y_top + 0.005, y_top], "k-", linewidth=1)
ax.text(1.5, y_top - 0.006, f"Mann-Whitney p = {p_mw:.3f}", ha="center", fontsize=10, style="italic")
ax.text(1.5, y_top - 0.012, f"Cohen's d = {d_cohen:.2f}", ha="center", fontsize=10, style="italic")

ax.set_xticks([1, 2])
ax.set_xticklabels([f"DeFi (N={len(defi)})", f"DePIN (N={len(depin)})"], fontsize=11)
ax.set_ylabel("Governance HHI (post-exclusion)")

fig.text(0.5, -0.02,
         "Source: Author calculations. Diamond = mean. "
         "Horizontal line = median. Individual protocols overlaid.",
         ha="center", fontsize=8, style="italic", color="gray")

save(fig, "fig4_sector_boxplot")


# =============================================================================
# FIGURE 5: Insider allocation scatter (N=37)
# =============================================================================
print("-- Fig 5: Allocation scatter")
alloc = reg.dropna(subset=["insider_pct", "hhi"]).copy()
alloc["insider_pct"] = pd.to_numeric(alloc["insider_pct"], errors="coerce")
alloc = alloc.dropna(subset=["insider_pct"])
print(f"  N={len(alloc)}")

fig, ax = plt.subplots(figsize=(12, 8))
for cat in alloc["category"].unique():
    subset = alloc[alloc["category"] == cat]
    ax.scatter(subset["insider_pct"], subset["hhi"],
               color=cat_colors_map.get(cat, SOCIAL_COLOR), s=60, alpha=0.8,
               label=cat.replace("_", " ").replace("Social Dead", "Social"),
               edgecolors="white", linewidth=0.5, zorder=3)

x = alloc["insider_pct"].values
y = alloc["hhi"].values
slope, intercept, r, p, _ = stats.linregress(x, y)

x_line = np.linspace(x.min(), x.max(), 100)
y_line = slope * x_line + intercept
n = len(x)
se_y = np.sqrt(np.sum((y - (slope * x + intercept))**2) / (n - 2))
ci = 1.96 * se_y * np.sqrt(1/n + (x_line - x.mean())**2 / np.sum((x - x.mean())**2))

ax.plot(x_line, y_line, "--", color="gray", linewidth=1.5, alpha=0.8)
ax.fill_between(x_line, y_line - ci, y_line + ci, alpha=0.10, color="gray")

if HAS_ADJUST_TEXT:
    texts = [
        ax.text(row["insider_pct"], row["hhi"], row["protocol"],
                fontsize=7, alpha=0.85,
                color=cat_colors_map.get(row["category"], "gray"))
        for _, row in alloc.iterrows()
    ]
    adjust_text(texts, ax=ax,
                arrowprops=dict(arrowstyle="-", color="gray", lw=0.3),
                force_text=(0.8, 1.0),
                force_points=(0.4, 0.6),
                expand_text=(1.3, 1.5),
                expand_points=(1.5, 1.5))
else:
    for _, row in alloc.iterrows():
        ax.annotate(row["protocol"], (row["insider_pct"], row["hhi"]),
                    fontsize=7, alpha=0.85, xytext=(3, 3),
                    textcoords="offset points",
                    color=cat_colors_map.get(row["category"], "gray"))

ax.set_title(f"Insider Allocation Is Uninformative (r = {r:.2f}, p = {p:.2f}, N = {len(alloc)})",
             fontweight="bold")
ax.set_xlabel("Initial Insider Allocation (percentage points)")
ax.set_ylabel("Governance Token HHI (April 2026)")
ax.legend(title="Category", loc="upper right")

fig.text(0.5, -0.02,
         "Source: Author calculations from Dune Analytics and Token Terminal (March 2026).",
         ha="center", fontsize=8, style="italic", color="gray")

save(fig, "fig5_allocation_scatter")


# =============================================================================
# FIGURE 6: Delegation grouped bars (R2 Table 7 values)
# Tally subset: Compound, Aave, Uniswap, Optimism, Arbitrum
# =============================================================================
print("-- Fig 6: Delegation grouped (R2 values)")
deleg_data = [
    {"protocol": "Compound", "raw_hhi": 0.028, "delegated_hhi": 0.053,
     "category": "DeFi",       "source": "Snapshot"},
    {"protocol": "Aave",     "raw_hhi": 0.020, "delegated_hhi": 0.076,
     "category": "DeFi",       "source": "Tally"},
    {"protocol": "Uniswap",  "raw_hhi": 0.010, "delegated_hhi": 0.027,
     "category": "DeFi",       "source": "Tally"},
    {"protocol": "Arbitrum", "raw_hhi": 0.012, "delegated_hhi": 0.052,
     "category": "L1_L2_Infra", "source": "Snapshot"},
    {"protocol": "Optimism", "raw_hhi": 0.009, "delegated_hhi": 0.033,
     "category": "L1_L2_Infra", "source": "Tally"},
]
deleg = pd.DataFrame(deleg_data)
deleg["ratio"] = deleg["delegated_hhi"] / deleg["raw_hhi"]
deleg = deleg.sort_values("ratio", ascending=True).reset_index(drop=True)
print(deleg[["protocol", "raw_hhi", "delegated_hhi", "ratio"]].to_string(float_format="%.4f"))

fig, ax = plt.subplots(figsize=(10, 6))
y = np.arange(len(deleg))
bh = 0.35
ax.barh(y - bh/2, deleg["raw_hhi"], bh, label="Holding HHI",
        color=DEFI_COLOR, alpha=0.7, edgecolor="white")
ax.barh(y + bh/2, deleg["delegated_hhi"], bh, label="Voting HHI",
        color=DEPIN_COLOR, alpha=0.7, edgecolor="white")

for i, row in deleg.iterrows():
    max_val = max(row["raw_hhi"], row["delegated_hhi"])
    txt = f"{row['ratio']:.2f}x" if row["ratio"] < 1.0 else f"{row['ratio']:.1f}x"
    clr = OUTLIER_COLOR if row["ratio"] > 3 else ("green" if row["ratio"] < 0.9 else "gray")
    ax.text(max_val + 0.003, i, txt, va="center", fontsize=9, fontweight="bold", color=clr)

for i, row in deleg.iterrows():
    ax.text(-0.002, i, row["source"], va="center", ha="right",
            fontsize=7, color="gray", style="italic")

ax.set_yticks(y)
ax.set_yticklabels(deleg["protocol"], fontsize=10)
ax.set_xlabel("HHI")
ax.legend(loc="lower right")
ax.set_xlim(-0.02, deleg["delegated_hhi"].max() * 1.25)

fig.text(0.5, -0.03,
         "Source: Tally (on-chain) and Snapshot (off-chain) governance data. "
         "Ratio > 1.0 = delegation concentrates voting power; < 1.0 = distributes it.",
         ha="center", fontsize=8, style="italic", color="gray")

save(fig, "fig6_delegation_grouped")


# =============================================================================
# FIGURE 7: Subsidy scatter (Livepeer outlier prominent)
# =============================================================================
print("-- Fig 7: Subsidy scatter")
sub = reg.copy()
sub["subsidy_ratio_onchain"] = pd.to_numeric(sub["subsidy_ratio_onchain"], errors="coerce")
sub = sub.dropna(subset=["subsidy_ratio_onchain", "hhi"]).copy()
print(f"  N={len(sub)}")

lpt = sub[sub["protocol"].str.lower() == "livepeer"]
rest = sub[sub["protocol"].str.lower() != "livepeer"]

fig, ax = plt.subplots(figsize=(10, 7))
for cat in rest["category"].unique():
    s = rest[rest["category"] == cat]
    ax.scatter(s["subsidy_ratio_onchain"], s["hhi"],
               color=cat_colors_map.get(cat, SOCIAL_COLOR), s=50, alpha=0.7,
               label=cat.replace("_", " ").replace("Social Dead", "Social"),
               zorder=3, edgecolors="white", linewidth=0.5)

if len(lpt) > 0:
    ax.scatter(lpt["subsidy_ratio_onchain"], lpt["hhi"],
               color=OUTLIER_COLOR, marker="D", s=130, zorder=4,
               edgecolors="black", linewidth=1)
    ax.annotate(
        f"Livepeer\n({lpt['subsidy_ratio_onchain'].values[0]:.1f}x subsidy\nHHI {lpt['hhi'].values[0]:.2f})",
        (lpt["subsidy_ratio_onchain"].values[0], lpt["hhi"].values[0]),
        xytext=(-25, 20), textcoords="offset points",
        fontsize=9, color=OUTLIER_COLOR, fontweight="bold",
        arrowprops=dict(arrowstyle="->", color=OUTLIER_COLOR, lw=1),
    )

x_all = sub["subsidy_ratio_onchain"].values
y_all = sub["hhi"].values
sl_a, ic_a, r_a, p_a, _ = stats.linregress(x_all, y_all)
x_ln_a = np.linspace(0, x_all.max() * 1.04, 100)
ax.plot(x_ln_a, sl_a * x_ln_a + ic_a, "-", color=OUTLIER_COLOR,
        alpha=0.5, linewidth=1.5, label=f"With LPT: r={r_a:.2f}, p={p_a:.3f}")

x_r = rest["subsidy_ratio_onchain"].values
y_r = rest["hhi"].values
sl_r, ic_r, r_r, p_r, _ = stats.linregress(x_r, y_r)
x_ln_r = np.linspace(0, x_r.max() * 1.10, 100)
ax.plot(x_ln_r, sl_r * x_ln_r + ic_r, "--", color="gray",
        alpha=0.7, linewidth=1.5, label=f"Without LPT: r={r_r:.2f}, p={p_r:.3f}")

ax.set_xlabel("Subsidy Ratio (emissions / revenue)")
ax.set_ylabel("Governance HHI (post-exclusion)")
ax.legend(loc="upper left", fontsize=9)

fig.text(0.5, -0.02,
         f"Source: Author calculations from Dune Analytics and Token Terminal (March 2026). N={len(sub)}.",
         ha="center", fontsize=8, style="italic", color="gray")

save(fig, "fig7_subsidy_scatter")


# =============================================================================
# FIGURE 8: HHI vs Participation (N=13)
# Embedded from participation_april2026.csv (b2-governance-data)
# =============================================================================
print("-- Fig 8: HHI vs participation")
part_data = [
    ("Arbitrum",    2530.6, "L1_L2_Infra", 0.012),
    ("Gitcoin",      700.8, "Social_Dead", 0.077),
    ("Uniswap",      232.8, "DeFi",        0.010),
    ("GMX",          197.1, "DeFi",        0.056),
    ("ENS",          124.2, "L1_L2_Infra", 0.135),
    ("Lido",          80.3, "DeFi",        0.013),
    ("Rocket Pool",   64.7, "DeFi",        0.039),
    ("WeatherXM",     51.5, "DePIN",       0.148),
    ("Compound",      23.2, "DeFi",        0.029),
    ("DIMO",           7.5, "DePIN",       0.038),
    ("Balancer",       5.6, "DeFi",        0.030),
    ("Aave",         100.0, "DeFi",        0.020),
    ("Optimism",     100.0, "L1_L2_Infra", 0.009),
]
part = pd.DataFrame(part_data, columns=["protocol", "voters_per_proposal", "category", "hhi"])

fig, ax = plt.subplots(figsize=(11, 7))
for cat in ["DeFi", "DePIN", "L1_L2_Infra", "Social_Dead"]:
    s = part[part["category"] == cat]
    if len(s) == 0:
        continue
    ax.scatter(s["hhi"], s["voters_per_proposal"],
               color=cat_colors_map.get(cat, SOCIAL_COLOR), s=80, alpha=0.8,
               label=cat.replace("_", " ").replace("Social Dead", "Social"),
               zorder=3, edgecolors="white", linewidth=0.5)

for _, row in part.iterrows():
    ax.annotate(row["protocol"], (row["hhi"], row["voters_per_proposal"]),
                xytext=(5, 5), textcoords="offset points", fontsize=8,
                color=cat_colors_map.get(row["category"], "gray"))

x = part["hhi"].values
log_y = np.log10(part["voters_per_proposal"].values)
slope, intercept, r, p, _ = stats.linregress(x, log_y)
x_line = np.linspace(x.min() * 0.7, x.max() * 1.15, 100)
n = len(x)
se_y = np.sqrt(np.sum((log_y - (slope * x + intercept))**2) / (n - 2))
ci = 1.96 * se_y * np.sqrt(1/n + (x_line - x.mean())**2 / np.sum((x - x.mean())**2))

y_lo = np.clip(10**(slope*x_line+intercept-ci), 1.0, None)
y_hi = np.clip(10**(slope*x_line+intercept+ci), None, 1e5)
ax.plot(x_line, 10**(slope*x_line+intercept), "--", color="gray", linewidth=1.5, alpha=0.7)
ax.fill_between(x_line, y_lo, y_hi, alpha=0.08, color="gray")

ax.set_yscale("log")
ax.set_ylim(3, 5000)
ax.set_xlabel("Governance Token HHI")
ax.set_ylabel("Unique Voters per Proposal (log scale)")
ax.set_title(f"Governance Concentration vs Participation (r = {r:.2f}, N = {len(part)})")
ax.legend(title="Category", loc="upper left")

fig.text(0.5, -0.02,
         "Source: Snapshot governance data (12-month lookback, mean voters per proposal). "
         "Aave and Optimism estimated from on-chain Governor / Agora data.",
         ha="center", fontsize=8, style="italic", color="gray")

save(fig, "fig8_participation")

print("\nDone. Outputs in:", OUT_DIR)
