"""B2 N=52 three-class sector boxplot (the N=52-cycle headline visual).

Governance-token measurement only (measurement_type == governance_token), three
architectural classes {DePIN, DeFi, L1}; Social_Dead (n=2) excluded from the contrast.
Kruskal-Wallis omnibus + Dunn (Holm) pairwise. Two-tier result: DePIN >> {DeFi ~= L1}.
The published balanced-30 DePIN-vs-DeFi binary (fig4) remains the of-record primary;
this figure is the N=52 extension. Styling matches regenerate_b2_figures.py.
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

REG_CSV = "/Users/zach/Tokenomics-As-Institutional_Design/data/processed/regression_data_april2026.csv"
DEPIN_COLOR, DEFI_COLOR, INFRA_COLOR = "#2171b5", "#cb6d51", "#2d6a2e"

plt.rcParams.update({
    "font.family": "serif", "font.serif": ["Times New Roman", "DejaVu Serif"],
    "font.size": 11, "axes.titlesize": 13, "axes.labelsize": 12,
    "xtick.labelsize": 10, "ytick.labelsize": 10, "legend.fontsize": 10,
    "figure.dpi": 300, "savefig.dpi": 300, "savefig.bbox": "tight",
    "axes.spines.top": False, "axes.spines.right": False,
})

reg = pd.read_csv(REG_CSV)
gov = reg[reg["measurement_type"] == "governance_token"]

# GUARD (load-bearing; the silent-conflation vector): the sector contrast uses
# governance-token measurement ONLY. Holder-measurement tokens (the phase6 additions
# WLFI/ENA/PUMP/JTO/BONK/KMNO) belong in the distribution figure, NEVER the sector
# contrast; mixing them is the measurement-type conflation that weakens the headline.
assert (gov["measurement_type"] == "governance_token").all(), "measurement-type conflation in sector contrast"
assert (reg["measurement_type"] == "holder").any(), "holder-measurement rows must exist (and stay out of the contrast)"

groups = {
    "DePIN": gov[gov["category"] == "DePIN"]["hhi"].values,
    "DeFi":  gov[gov["category"] == "DeFi"]["hhi"].values,
    "L1":    gov[gov["category"] == "L1_L2_Infra"]["hhi"].values,
}
names = list(groups)

# Kruskal-Wallis omnibus + epsilon^2
H, p_kw = stats.kruskal(*groups.values())
N = sum(len(v) for v in groups.values())
eps2 = (H - len(names) + 1) / (N - len(names))

# Dunn post-hoc (Holm) with tie correction
allv = np.concatenate(list(groups.values()))
ranks = stats.rankdata(allv)
_, cnt = np.unique(allv, return_counts=True)
ties = sum(t**3 - t for t in cnt)
sigma2 = (N * (N + 1) / 12) - ties / (12 * (N - 1))
idx = 0; mr = {}; n = {}
for nm in names:
    k = len(groups[nm]); mr[nm] = ranks[idx:idx+k].mean(); n[nm] = k; idx += k
pairs = []
for i in range(len(names)):
    for j in range(i+1, len(names)):
        a, b = names[i], names[j]
        z = (mr[a]-mr[b]) / np.sqrt(sigma2 * (1/n[a] + 1/n[b]))
        pairs.append([f"{a}-{b}", 2*(1-stats.norm.cdf(abs(z)))])
order = sorted(range(len(pairs)), key=lambda k: pairs[k][1]); m = len(pairs)
for rk, k in enumerate(order):
    pairs[k].append(min(1.0, pairs[k][1]*(m-rk)))
padj = {x[0]: x[2] for x in pairs}
print(f"KW H={H:.3f} p={p_kw:.4f} eps2={eps2:.3f}; Dunn(Holm) {padj}")

fig, ax = plt.subplots(figsize=(8.5, 8))
data = [groups["DePIN"], groups["DeFi"], groups["L1"]]
colors = [DEPIN_COLOR, DEFI_COLOR, INFRA_COLOR]
bp = ax.boxplot(data, positions=[1, 2, 3], widths=0.55, patch_artist=True, showmeans=True,
                meanprops=dict(marker="D", markerfacecolor="white", markeredgecolor="black", markersize=8),
                medianprops=dict(color="black", linewidth=2))
for box, c in zip(bp["boxes"], colors):
    box.set_facecolor(c); box.set_alpha(0.4)

np.random.seed(42)
for d, pos, c in zip(data, [1, 2, 3], colors):
    jitter = np.random.normal(0, 0.045, len(d))
    ax.scatter(pos + jitter, d, color=c, alpha=0.6, s=40, zorder=3, edgecolors="white", linewidth=0.5)
for pos, d in zip([1, 2, 3], data):
    ax.text(pos + 0.34, np.mean(d), f"Mean: {np.mean(d):.3f}", va="center", fontsize=9)

ymax = max(v.max() for v in data)
# DePIN-DeFi bracket
y1 = ymax + 0.012
ax.plot([1, 1, 2, 2], [y1, y1+0.005, y1+0.005, y1], "k-", lw=1)
ax.text(1.5, y1+0.007, f"Dunn p = {padj['DePIN-DeFi']:.3f}", ha="center", fontsize=9, style="italic")
# DePIN-L1 bracket (higher)
y2 = ymax + 0.045
ax.plot([1, 1, 3, 3], [y2, y2+0.005, y2+0.005, y2], "k-", lw=1)
ax.text(2.0, y2+0.007, f"Dunn p = {padj['DePIN-L1']:.3f}", ha="center", fontsize=9, style="italic")
# DeFi-L1 n.s. note
ax.text(2.5, np.mean(data[1])+0.01, f"DeFi vs L1: n.s. (p = {padj['DeFi-L1']:.2f})",
        ha="center", fontsize=8.5, style="italic", color="gray")

ax.set_xticks([1, 2, 3])
ax.set_xticklabels([f"DePIN (N={n['DePIN']})", f"DeFi (N={n['DeFi']})", f"L1/Infra (N={n['L1']})"], fontsize=11)
ax.set_ylabel("Governance HHI (post-PCA exclusion)")
ax.set_title(f"Governance Concentration by Architecture (N={N} governance-token-measured, of the 52-protocol cross-section)\n"
             f"Kruskal-Wallis p = {p_kw:.3f}, $\\epsilon^2$ = {eps2:.2f}",
             fontsize=13, fontweight="bold", pad=14)
fig.text(0.5, -0.02,
         "Source: Author calculations. Diamond = mean; horizontal line = median; protocols overlaid. "
         "Governance-token measurement only; Social tokens (n=2) excluded from the contrast. "
         "DePIN is more concentrated than both DeFi and L1; DeFi and L1 are not distinguishable.",
         ha="center", fontsize=8, style="italic", color="gray", wrap=True)

for ext in ("png", "pdf"):
    fig.savefig(f"/Users/zach/Tokenomics-As-Institutional_Design/b2/paper/figures/fig_sector_3class_n52.{ext}",
                dpi=300, bbox_inches="tight")
plt.close(fig)
print("wrote fig_sector_3class_n52.{png,pdf}")
