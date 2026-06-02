"""
B2 R2 figure regeneration (Figures 3 through 9).

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
  Figure 9    LOO sensitivity forest + bootstrap CI for DePIN-vs-DeFi
              contrast (N=30); computed inline from REG_CSV with fixed
              numpy seed for reproducibility (seed=42).

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

import os as _os_anchor
_RR = _os_anchor.path.dirname(_os_anchor.path.abspath(__file__))
while _RR != _os_anchor.path.dirname(_RR) and not _os_anchor.path.exists(_os_anchor.path.join(_RR, "reproduce.py")):
    _RR = _os_anchor.path.dirname(_RR)
REG_CSV = (_RR + "/data/processed/regression_data_april2026.csv")
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

ax.set_title("Governance Concentration (HHI) Across 52 Protocols",
             fontsize=14, fontweight="bold", pad=12)

fig.text(0.5, -0.005,
         "Source: Dune Analytics + Helius DAS API (March 2026). "
         "133 protocol-controlled addresses excluded across 38 protocols.",
         ha="center", fontsize=8, style="italic", color="gray")

save(fig, "fig3_hhi_bar_40protocols")


# =============================================================================
# FIGURE 4: Sector boxplot (DePIN vs DeFi)
# =============================================================================
print("-- Fig 4: Sector boxplot")
# OF-RECORD BALANCED-30 (15 DePIN + 15 DeFi-governance_token). The caption stats
# (DePIN mean 0.071, DeFi 0.031, Mann-Whitney p=0.020, Cohen's d=0.94, 30/30 LOO)
# reproduce ONLY against the pre-N52 HHI snapshot: the live REG_CSV refreshed Jupiter
# and Drift and grew DeFi-governance_token from 15 to 18 in the N=52 expansion, so
# computing on live data silently yields d=0.889. Read the frozen snapshot when present;
# the assert fails loud (never silently unbalances) if the of-record 15/15 is unavailable.
import os as _os
_PRE_N52 = REG_CSV + ".pre_n52_merge_2026-05-29"
_bal_src = pd.read_csv(_PRE_N52) if _os.path.exists(_PRE_N52) else reg
_bal = _bal_src[(_bal_src["category"] == "DePIN") |
                ((_bal_src["category"] == "DeFi") & (_bal_src["measurement_type"] == "governance_token"))]
defi = _bal[_bal["category"] == "DeFi"]["hhi"]
depin = _bal[_bal["category"] == "DePIN"]["hhi"]
assert len(depin) == 15 and len(defi) == 15, (
    f"fig4 of-record balanced-30 needs 15 DePIN + 15 DeFi(governance_token); got "
    f"{len(depin)}/{len(defi)}. The N=52 expansion grew DeFi-gt to 18; re-cut requires "
    f"the pre-N52 snapshot ({_PRE_N52}). Committed fig4_sector_boxplot.* is the frozen "
    f"of-record artifact (p=0.020, d=0.94). Aborting rather than emit an unbalanced figure.")

stat, p_mw = stats.mannwhitneyu(depin, defi, alternative="two-sided")
# pooled-SD Cohen's d (df-weighted; matches reproduce.py canonical full-frame d).
# The prior simple-average pooling sqrt((s1^2+s2^2)/2) diverged from canonical at unbalanced N.
_pn1, _pn2 = len(depin), len(defi)
_psd = np.sqrt(((_pn1 - 1) * depin.var(ddof=1) + (_pn2 - 1) * defi.var(ddof=1)) / (_pn1 + _pn2 - 2))
d_cohen = (depin.mean() - defi.mean()) / _psd
print(f"  DeFi:  mean={defi.mean():.4f}, N={len(defi)}")
print(f"  DePIN: mean={depin.mean():.4f}, N={len(depin)}")
print(f"  MW p={p_mw:.4f}, Cohen d={d_cohen:.3f}")

fig, ax = plt.subplots(figsize=(7, 8))
bp = ax.boxplot(
    [defi.values, depin.values], positions=[1, 2], widths=0.5,
    patch_artist=True, showmeans=True, showfliers=False,
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
ax.text(1.5, y_top - 0.006, f"Mann-Whitney p = {p_mw:.3f} (balanced 30)", ha="center", fontsize=10, style="italic")
ax.text(1.5, y_top - 0.012, f"Cohen's d = {d_cohen:.2f}", ha="center", fontsize=10, style="italic")

ax.set_xticks([1, 2])
ax.set_xticklabels([f"DeFi (N={len(defi)})", f"DePIN (N={len(depin)})"], fontsize=11)
ax.set_ylabel("Governance HHI (post-exclusion)")

ax.set_title("DePIN Governance More Concentrated Than DeFi After PCA Correction",
             fontsize=13, fontweight="bold", pad=12)

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

# Per-protocol manual label positioning (replaces adjustText after iterative
# attempts confirmed automatic collision-avoidance leaves residual overlap in
# the dense insider_pct 30-60 / HHI 0.005-0.05 cluster). Each protocol has
# an explicit (dx, dy) offset in points + ha/va alignment chosen to avoid
# label-on-dot overlap and label-on-label collision.
fig, ax = plt.subplots(figsize=(13, 8))

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

# Per-protocol label position map: dx, dy in points (positive = right/up); ha + va alignment.
# Manual positioning iteratively refined to avoid overlap with dots and other labels.
# Defaults to (0, 8, center, bottom) = label centered ABOVE dot.
LABEL_OFFSETS = {
    "Compound":              (0, -10, "center", "top"),
    "MakerDAO":              (9, 3, "left", "center"),
    "Aave":                  (-10, 12, "left", "center"),
    "Uniswap":               (19, -10, "right", "top"),
    "Curve":                 (-10, 0, "right", "center"),
    "Rocket Pool":           (-9, -2, "right", "bottom"),
    "Jupiter":               (0, 9, "center", "bottom"),
    "Maple Finance":         (0, 9, "center", "bottom"),
    "GMX":                   (0, 9, "center", "bottom"),
    "Drift":                 (0, 9, "center", "bottom"),
    "Ether.Fi":              (-42, -1, "left", "bottom"),
    "The Graph":             (11, 3, "left", "top"),
    "Optimism":              (-6, 5, "right", "top"),
    "Polygon":               (-4, 7, "left", "bottom"),
    "Arbitrum":              (-20, -9, "left", "top"),
    "ENS":                   (0, 9, "center", "bottom"),
    "DIMO":                  (11, 9, "right", "bottom"),
    "IoTeX":                 (0, 9, "center", "bottom"),
    "WeatherXM":             (0, 9, "center", "bottom"),
    "Anyone Protocol":       (-34, 12, "left", "center"),
    "Grass":                 (4, 6, "left", "bottom"),
    "Livepeer":              (0, 9, "center", "bottom"),
    "GEODNET":               (0, 9, "center", "bottom"),
    "Filecoin":              (11, 7, "right", "bottom"),
    "Render":                (0, -10, "center", "top"),
    "Pokt Network":          (29, 13, "right", "center"),
    "LayerZero":             (0, 9, "center", "bottom"),
    "Wormhole":              (0, -10, "center", "top"),
    "Morpheus AI":           (-29, 13, "left", "center"),
    "Axelar":                (0, -10, "center", "top"),
    "Lido":                  (-9, -9, "left", "top"),
    "Gitcoin":               (-12, 7, "left", "bottom"),
    "Aethir":                (-14, 12, "left", "center"),
    "Hivemapper":            (8, -5, "left", "bottom"),
    "io.net":                (0, 9, "center", "bottom"),
    "Hyperliquid":           (0, -10, "center", "top"),
    "Balancer":              (0, 9, "center", "bottom"),
}
DEFAULT_OFFSET = (0, 9, "center", "bottom")


# =============================================================================
# FIG 7 LABEL OFFSETS (per-protocol label positions for subsidy scatter)
# Edit positions via interactive_fig7_editor.py (drag + drop tool)
# =============================================================================
FIG7_LABEL_OFFSETS = {
    "Compound":              (27, -17, "center", "bottom"),
    "MakerDAO":              (-6, 34, "center", "bottom"),
    "Aave":                  (-20, 12, "center", "bottom"),
    "Uniswap":               (24, 4, "center", "bottom"),
    "Curve":                 (-7, 6, "center", "bottom"),
    "Maple Finance":         (31, 6, "center", "bottom"),
    "GMX":                   (0, 9, "center", "bottom"),
    "Ether.Fi":              (13, 21, "center", "bottom"),
    "The Graph":             (0, 9, "center", "bottom"),
    "Optimism":              (33, -4, "center", "bottom"),
    "Polygon":               (35, 4, "center", "bottom"),
    "DIMO":                  (-18, 9, "center", "bottom"),
    "IoTeX":                 (0, 9, "center", "bottom"),
    "Helium":                (0, 9, "center", "bottom"),
    "GEODNET":               (12, 13, "center", "bottom"),
    "Filecoin":              (0, 9, "center", "bottom"),
    "Render":                (0, 9, "center", "bottom"),
    "Pokt Network":          (0, 9, "center", "bottom"),
    "Morpheus AI":           (26, -11, "left", "center"),
    "Lido":                  (-19, 4, "center", "bottom"),
    "Aethir":                (0, 9, "center", "bottom"),
    "Hivemapper":            (6, 7, "center", "bottom"),
    "io.net":                (0, 9, "center", "bottom"),
    "Hyperliquid":           (-7, -19, "center", "bottom"),
}
FIG7_DEFAULT_OFFSET = (0, 9, "center", "bottom")


# =============================================================================
# FIG 8 LABEL OFFSETS (per-protocol label positions for HHI vs participation)
# Edit positions via interactive_fig8_editor.py (drag + drop tool)
# =============================================================================
FIG8_LABEL_OFFSETS = {
    "Arbitrum":              (5, 5, "left", "bottom"),
    "Gitcoin":               (5, 6, "left", "bottom"),
    "Uniswap":               (3, 9, "left", "bottom"),
    "GMX":                   (-8, 9, "left", "bottom"),
    "ENS":                   (-3, 10, "left", "bottom"),
    "Lido":                  (-6, -23, "left", "bottom"),
    "Rocket Pool":           (-28, -22, "left", "bottom"),
    "WeatherXM":             (0, -18, "left", "bottom"),
    "Compound":              (-25, -22, "left", "bottom"),
    "DIMO":                  (-14, 12, "left", "bottom"),
    "Balancer":              (5, 5, "left", "bottom"),
    "Aave":                  (26, 15, "left", "top"),
    "Optimism":              (-23, 12, "left", "bottom"),
}
FIG8_DEFAULT_OFFSET = (5, 5, "left", "bottom")

for _, row in alloc.iterrows():
    dx, dy, ha, va = LABEL_OFFSETS.get(row["protocol"], DEFAULT_OFFSET)
    ax.annotate(row["protocol"],
                xy=(row["insider_pct"], row["hhi"]),
                xytext=(dx, dy),
                textcoords="offset points",
                fontsize=7.5, alpha=0.95, fontweight="bold",
                color=cat_colors_map.get(row["category"], "gray"),
                ha=ha, va=va,
                zorder=5)

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
    {"protocol": "Compound", "raw_hhi": 0.009223, "delegated_hhi": 0.053,
     "category": "DeFi",       "source": "Snapshot"},
    {"protocol": "Aave",     "raw_hhi": 0.012790, "delegated_hhi": 0.076,
     "category": "DeFi",       "source": "Tally"},
    {"protocol": "Uniswap",  "raw_hhi": 0.009784, "delegated_hhi": 0.027,
     "category": "DeFi",       "source": "Tally"},
    {"protocol": "Arbitrum", "raw_hhi": 0.011914, "delegated_hhi": 0.052,
     "category": "L1_L2_Infra", "source": "Snapshot"},
    {"protocol": "Optimism", "raw_hhi": 0.009281, "delegated_hhi": 0.033,
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
# FIGURE 7: Subsidy scatter (Livepeer outlier prominent + per-protocol labels)
# =============================================================================
print("-- Fig 7: Subsidy scatter")
from adjustText import adjust_text

sub = reg.copy()
# Canonical subsidy metric per PAPER.md Section 4.4 footnote: Token Terminal
# subsidy_ratio where available, on-chain subsidy_ratio_onchain as fallback; the
# "either-metric > 0" sub-sample is N=23. A prior version plotted on-chain alone,
# which mispositioned the four TT-sourced protocols whose on-chain value differs
# (Filecoin 46.05 vs TT 19.18; IoTeX 27.80 vs TT 39.05; Aethir; io.net) and fit the
# regression to r=0.51 rather than the canonical hybrid r=0.58. Overwriting the
# plotted column with the hybrid keeps the downstream plotting code unchanged.
sub["subsidy_ratio"] = pd.to_numeric(sub["subsidy_ratio"], errors="coerce")
sub["subsidy_ratio_onchain"] = pd.to_numeric(sub["subsidy_ratio_onchain"], errors="coerce")
sub["subsidy_ratio_onchain"] = sub["subsidy_ratio"].where(sub["subsidy_ratio"].notna(), sub["subsidy_ratio_onchain"])
sub = sub.dropna(subset=["subsidy_ratio_onchain", "hhi"]).copy()
sub = sub[sub["subsidy_ratio_onchain"] > 0].copy()
print(f"  N={len(sub)}")

lpt = sub[sub["protocol"].str.lower() == "livepeer"]
rest = sub[sub["protocol"].str.lower() != "livepeer"]

fig, ax = plt.subplots(figsize=(11, 7.5))
for cat in rest["category"].unique():
    s = rest[rest["category"] == cat]
    ax.scatter(s["subsidy_ratio_onchain"], s["hhi"],
               color=cat_colors_map.get(cat, SOCIAL_COLOR), s=50, alpha=0.75,
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

# With LPT regression line (canonical hybrid metric gives r=0.58; slope captures the Livepeer-driven correlation)
x_all = sub["subsidy_ratio_onchain"].values
y_all = sub["hhi"].values
sl_a, ic_a, r_a, p_a, _ = stats.linregress(x_all, y_all)
x_ln_a = np.linspace(0, x_all.max() * 1.04, 100)
ax.plot(x_ln_a, sl_a * x_ln_a + ic_a, "-", color=OUTLIER_COLOR,
        alpha=0.5, linewidth=1.5, label=f"With LPT: r={r_a:.2f}, p={p_a:.3f} (Livepeer-driven)")

# Without LPT: compute r + p for legend; DO NOT draw the line.
# Rationale: r=0.027 produces a near-flat regression line that visually
# misleads readers into expecting a relationship; absence-of-line communicates
# the null finding more honestly. Legend conveys the exact stat.
x_r = rest["subsidy_ratio_onchain"].values
y_r = rest["hhi"].values
_, _, r_r, p_r, _ = stats.linregress(x_r, y_r)
from matplotlib.lines import Line2D
null_handle = Line2D([0], [0], color="none", label=f"Without LPT: r={r_r:.2f}, p={p_r:.3f} (no significant correlation; line omitted)")

# Per-protocol labels via FIG7_LABEL_OFFSETS dict (edit positions with interactive_fig7_editor.py)
# Labels color-coded by category (matches dot colors); leader lines connect label to dot
for _, row in rest.iterrows():
    dx, dy, ha, va = FIG7_LABEL_OFFSETS.get(row["protocol"], FIG7_DEFAULT_OFFSET)
    label_color = cat_colors_map.get(row["category"], "#444444")
    ax.annotate(row["protocol"],
                xy=(row["subsidy_ratio_onchain"], row["hhi"]),
                xytext=(dx, dy),
                textcoords="offset points",
                fontsize=7.5, fontweight="bold",
                color=label_color,
                ha=ha, va=va,
                zorder=5,
                arrowprops=dict(arrowstyle="-", color=label_color,
                                 lw=0.4, alpha=0.5, shrinkA=2, shrinkB=4))

ax.set_xlabel("Subsidy Ratio (emissions / revenue)")
ax.set_ylabel("Governance HHI (post-exclusion)")

ax.set_title("Subsidy-Concentration Association Driven Entirely by Livepeer Outlier",
             fontsize=13, fontweight="bold", pad=12)

# Custom legend with null-correlation handle
handles, labels = ax.get_legend_handles_labels()
handles.append(null_handle)
labels.append(null_handle.get_label())
ax.legend(handles=handles, labels=labels, loc="upper left", fontsize=9)

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
    ("Gitcoin",      700.8, "Social_Dead", 0.022),
    ("Uniswap",      232.8, "DeFi",        0.010),
    ("GMX",          197.1, "DeFi",        0.065),
    ("ENS",          124.2, "L1_L2_Infra", 0.071),
    ("Lido",          80.3, "DeFi",        0.008),
    ("Rocket Pool",   64.7, "DeFi",        0.039),
    ("WeatherXM",     51.5, "DePIN",       0.148),
    ("Compound",      23.2, "DeFi",        0.009),
    ("DIMO",           7.5, "DePIN",       0.025),
    ("Balancer",       5.6, "DeFi",        0.029),
    ("Aave",         100.0, "DeFi",        0.013),
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

# Per-protocol labels via FIG8_LABEL_OFFSETS dict (edit positions with interactive_fig8_editor.py)
# Labels color-coded by category; leader lines connect label to dot
for _, row in part.iterrows():
    dx, dy, ha, va = FIG8_LABEL_OFFSETS.get(row["protocol"], FIG8_DEFAULT_OFFSET)
    label_color = cat_colors_map.get(row["category"], "gray")
    ax.annotate(row["protocol"],
                xy=(row["hhi"], row["voters_per_proposal"]),
                xytext=(dx, dy), textcoords="offset points",
                fontsize=8, fontweight="bold",
                color=label_color,
                ha=ha, va=va,
                arrowprops=dict(arrowstyle="-", color=label_color,
                                 lw=0.5, alpha=0.6, shrinkA=2, shrinkB=4))

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
ax.legend(title="Category", loc="upper right")

fig.text(0.5, -0.02,
         "Source: Snapshot governance data (12-month lookback, mean voters per proposal). "
         "Aave and Optimism estimated from on-chain Governor / Agora data.",
         ha="center", fontsize=8, style="italic", color="gray")

save(fig, "fig8_participation")


# =============================================================================
# FIGURE 9: LOO sensitivity forest + bootstrap CI (DePIN vs DeFi; N=30)
# =============================================================================
print("-- Fig 9: LOO forest + bootstrap CI")

# OF-RECORD BALANCED-30 LOO (15 DePIN + 15 DeFi-governance_token); reproduces d=0.94,
# 30/30 LOO significant ONLY against the pre-N52 snapshot (live REG_CSV drifted + grew
# DeFi-gt to 18). Fail loud rather than silently produce an N=39 forest.
import os as _os9
_PRE_N52_9 = REG_CSV + ".pre_n52_merge_2026-05-29"
_src9 = pd.read_csv(_PRE_N52_9) if _os9.path.exists(_PRE_N52_9) else reg
sect = _src9[(_src9["category"] == "DePIN") |
             ((_src9["category"] == "DeFi") & (_src9["measurement_type"] == "governance_token"))].copy()
assert len(sect) == 30 and (sect["category"] == "DePIN").sum() == 15, (
    f"fig9 of-record balanced-30 LOO needs N=30 (15 DePIN + 15 DeFi-gt); got {len(sect)}. "
    f"Re-cut requires the pre-N52 snapshot ({_PRE_N52_9}).")
defi9 = sect[sect["category"] == "DeFi"]["hhi"].values
depin9 = sect[sect["category"] == "DePIN"]["hhi"].values

def cohen_d(a, b):
    return (a.mean() - b.mean()) / np.sqrt((a.std(ddof=1)**2 + b.std(ddof=1)**2) / 2)

d_headline = cohen_d(depin9, defi9)
_, p_headline = stats.mannwhitneyu(depin9, defi9, alternative="two-sided")
print(f"  Headline: d={d_headline:.3f}, p={p_headline:.4f}")

loo_rows = []
for proto in sect["protocol"].values:
    s2 = sect[sect["protocol"] != proto]
    a = s2[s2["category"] == "DePIN"]["hhi"].values
    b = s2[s2["category"] == "DeFi"]["hhi"].values
    _, pv = stats.mannwhitneyu(a, b, alternative="two-sided")
    loo_rows.append({
        "drop": proto,
        "cat": sect[sect["protocol"] == proto]["category"].values[0],
        "d": cohen_d(a, b),
        "p": pv,
    })
loo = pd.DataFrame(loo_rows).sort_values("d", ascending=False).reset_index(drop=True)
print(f"  LOO d range: {loo['d'].min():.3f} to {loo['d'].max():.3f}")
print(f"  LOO p range: {loo['p'].min():.4f} to {loo['p'].max():.4f}")

rng = np.random.default_rng(42)
boot_ds = []
for _ in range(10000):
    a_b = rng.choice(depin9, size=len(depin9), replace=True)
    b_b = rng.choice(defi9, size=len(defi9), replace=True)
    if a_b.std(ddof=1) == 0 or b_b.std(ddof=1) == 0:
        continue
    boot_ds.append(cohen_d(a_b, b_b))
ci_lo, ci_hi = np.percentile(boot_ds, [2.5, 97.5])
print(f"  Bootstrap 95% CI: [{ci_lo:.3f}, {ci_hi:.3f}]")

fig, (axL, axR) = plt.subplots(
    1, 2, figsize=(14, 8),
    gridspec_kw={"width_ratios": [3.2, 1]},
)

y_pos = np.arange(len(loo))
bar_colors = [DEFI_COLOR if c == "DeFi" else DEPIN_COLOR for c in loo["cat"]]
axL.barh(y_pos, loo["d"], color=bar_colors, alpha=0.75, edgecolor="white",
         height=0.72, linewidth=0.4)

axL.invert_yaxis()
axL.set_yticks(y_pos)
axL.set_yticklabels([f"Drop {p} ({c})" for p, c in zip(loo["drop"], loo["cat"])],
                    fontsize=9)
axL.set_xlabel("Cohen's d (DePIN vs DeFi)")
axL.set_title("Leave-one-out sensitivity: drop each protocol and recompute",
              fontsize=12, fontweight="bold")

x_min = max(0.80, loo["d"].min() - 0.06)
x_max = max(1.32, loo["d"].max() + 0.05)
axL.set_xlim(x_min, x_max)

axL.axvline(x=d_headline, color="black", linestyle="--", linewidth=1.0,
            alpha=0.25, label=f"Main result (d = {d_headline:.2f})", zorder=1)
axL.axvline(x=0.80, color="gray", linestyle=":", linewidth=1.0,
            alpha=0.25, label="Cohen's large effect (d = 0.80)", zorder=1)

for yi, (_, row) in zip(y_pos, loo.iterrows()):
    x_text = row["d"] + (x_max - x_min) * 0.012
    axL.text(x_text, yi, f"p = {row['p']:.3f}",
             va="center", fontsize=8, color="#444")

from matplotlib.patches import Patch
from matplotlib.lines import Line2D
loo_legend = [
    Patch(facecolor=DEFI_COLOR, alpha=0.75, label="DeFi protocol dropped"),
    Patch(facecolor=DEPIN_COLOR, alpha=0.75, label="DePIN protocol dropped"),
    Line2D([0], [0], color="black", linestyle="--", linewidth=1.0, alpha=0.5,
           label=f"Main result (d = {d_headline:.2f})"),
    Line2D([0], [0], color="gray", linestyle=":", linewidth=1.0, alpha=0.5,
           label="Cohen's large effect (d = 0.80)"),
]
axL.legend(handles=loo_legend, loc="lower right", fontsize=8, framealpha=0.92)

axR.errorbar(
    [0], [d_headline],
    yerr=[[d_headline - ci_lo], [ci_hi - d_headline]],
    fmt="o", color="black", markersize=8, linewidth=1.6, capsize=8, capthick=1.6,
    zorder=3,
)
axR.set_xlim(-0.6, 0.6)
axR.set_ylim(0.0, 2.0)
axR.set_xticks([])
axR.set_ylabel("Cohen's d")
axR.set_title("Bootstrap 95% CI", fontsize=12, fontweight="bold")

axR.axhline(y=0.80, color="gray", linestyle=":", linewidth=1.0, alpha=0.5, zorder=1)
axR.axhline(y=0.50, color="gray", linestyle=":", linewidth=1.0, alpha=0.5, zorder=1)
axR.text(0.58, 0.80 + 0.035, "Large (0.8)", fontsize=8, color="gray",
         ha="right", va="bottom", style="italic")
axR.text(0.58, 0.50 + 0.035, "Medium (0.5)", fontsize=8, color="gray",
         ha="right", va="bottom", style="italic")

axR.text(0.16, d_headline, f"d = {d_headline:.2f}",
         ha="left", va="center", fontsize=10, fontweight="bold")
axR.text(0.16, ci_hi, f"{ci_hi:.2f}", ha="left", va="center",
         fontsize=8, color="gray")
axR.text(0.16, ci_lo, f"{ci_lo:.2f}", ha="left", va="center",
         fontsize=8, color="gray")

axR.spines["top"].set_visible(False)
axR.spines["right"].set_visible(False)
axR.spines["bottom"].set_visible(False)

save(fig, "fig9_loo_forest")

print("\nDone. Outputs in:", OUT_DIR)
