"""B3 Figure 3 v12: GEODNET burn absorption on the CONSTRUCT-CORRECT burn flow.

v11 plotted the Solana SPL burn series (Dune q6917159), which a 2026-06 Blockworks
reconciliation showed predominantly measures Wormhole NTT bridge outflow, not the
Foundation buy-and-burn. This v12 plots the Foundation buy-and-burn measured on the
Polygon burn address 0x...dEaD (Dune 7541498 v2 logic; reproduced from Etherscan v2
to 0.2%), divided by net miner issuance (Console methodology, Dune 7542071).

Real shape: gentle ~9-13% through mid-2025, a ramp from Jul 2025 (28.5%) to a
52.5% peak (Oct 2025), then easing to 21.9% (Feb 2026, the corrected S2R 0.219).
No "collapse" months (those were Solana-bridge artifacts).
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

MONTHS = [
    "Sep\n2024", "Oct\n2024", "Nov\n2024", "Dec\n2024",
    "Jan\n2025", "Feb\n2025", "Mar\n2025", "Apr\n2025", "May\n2025",
    "Jun\n2025", "Jul\n2025", "Aug\n2025", "Sep\n2025", "Oct\n2025",
    "Nov\n2025", "Dec\n2025", "Jan\n2026", "Feb\n2026",
]
# Foundation buy-and-burn to the Polygon dead address (GEOD), monthly.
BURNS = [
    580000, 500000, 570000, 850000,
    710000, 650000, 890000, 1060000, 1250000,
    1440000, 1590000, 2170000, 2210000, 2763000,
    1895000, 1415000, 1395000, 1305000,
]
# Net miner issuance (of-record, Console net-flow methodology), unchanged from v11.
NET_ISSUANCE = [
    5431990, 6108600, 6383043, 7023933,
    7732760, 7123939, 8197685, 10375036, 9816738,
    9885323, 5588138, 6357258, 4854364, 5266613,
    6220896, 6264383, 6465076, 5948674,
]
rate = [100.0 * b / n for b, n in zip(BURNS, NET_ISSUANCE)]

plt.rcParams.update({
    "font.family": "serif", "font.size": 9,
    "axes.spines.top": False, "axes.spines.right": False,
})
fig, ax = plt.subplots(figsize=(7.0, 4.1))
x = range(len(MONTHS))
ax.fill_between(x, rate, color="#aec6e8", alpha=0.45, zorder=1)
ax.plot(x, rate, color="#1a5276", marker="o", markersize=4.5, linewidth=1.6, zorder=3)

# 50% absorption threshold (now actually reached at the Oct 2025 peak)
ax.axhline(50, color="#999999", linestyle="--", linewidth=0.9, zorder=2)
ax.text(0.1, 51.5, "50% absorption threshold", color="#777777", fontsize=7.5, style="italic")

# Annual halving marker (June 30, 2025): between Jun 2025 (idx 9) and Jul 2025 (idx 10)
ax.axvline(9.5, color="#c87f2a", linestyle=":", linewidth=1.1, zorder=2)
ax.text(9.32, 6.0, "Annual halving", color="#c87f2a", fontsize=7.5, style="italic", ha="right")

peak_idx = rate.index(max(rate))  # Oct 2025
ax.annotate(
    f"Peak: {rate[peak_idx]:.1f}%\n(Oct 2025)",
    xy=(peak_idx, rate[peak_idx]), xytext=(peak_idx - 1.7, rate[peak_idx] + 4),
    fontsize=8, color="#1a5276", fontweight="bold", ha="center",
    arrowprops=dict(arrowstyle="-", color="#1a5276", linewidth=0.7),
)
ax.annotate(
    f"{rate[-1]:.1f}%\n(Feb 2026)",
    xy=(len(MONTHS) - 1, rate[-1]), xytext=(len(MONTHS) - 1.15, rate[-1] + 11),
    fontsize=8, color="#1a5276", fontweight="bold", ha="center",
    arrowprops=dict(arrowstyle="-", color="#1a5276", linewidth=0.7),
)

ax.set_ylim(0, 62)
ax.set_xlim(-0.5, len(MONTHS) - 0.4)
ax.set_xticks([0, 2, 4, 6, 8, 10, 12, 14, 16])
ax.set_xticklabels([MONTHS[i] for i in [0, 2, 4, 6, 8, 10, 12, 14, 16]], fontsize=7.5)
ax.set_ylabel("Burn Absorption Rate (% of net issuance)", fontsize=9)
ax.set_xlabel("Date", fontsize=9)
ax.tick_params(axis="y", labelsize=8)

fig.text(
    0.5, 0.005,
    "Source: Dune Analytics. GEODNET Foundation buy-and-burn (Polygon burn address) vs net miner issuance (Console methodology).",
    ha="center", fontsize=6.5, style="italic", color="#666666",
)
fig.tight_layout(rect=(0, 0.03, 1, 1))
fig.savefig("B3_figure3_geodnet_burn_absorption.png", dpi=160)
print("rendered. series:")
for m, r in zip(MONTHS, rate):
    print(" ", m.replace("\n", " "), f"{r:.1f}%")
print("peak:", MONTHS[peak_idx].replace(chr(10), " "), f"{max(rate):.1f}%")
