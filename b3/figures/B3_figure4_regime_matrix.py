"""B3 Figure 4 v18: burn-architecture observability and S2R.

v18 (DIMO erratum, AUTHOR-CARD b3-dimo-s2r-refuted-published-v17-carries-it): DIMO removed
(its null-address flow is 99.987 percent bridge exits; exhibits/dimo_s2r/burn_construct_validation.md);
Hivemapper re-placed at its reported S2R 0.183 (it was drawn at 0.02); y-axis rescaled.

The Final_v10/v11 Figure 4 plotted GEODNET (0.055) and DIMO (0.063) on a
demand-concentration (burn-signer HHI) axis and drew a "4-5x gap" between a
subscription/license cluster and a carrier/enterprise cluster. A 2026-06
reconciliation established that on-chain burn-signer HHI is a valid demand-
concentration measure only for DIRECT-burn protocols, where each customer signs
their own burn. Among the protocols studied only Helium meets that condition.
GEODNET runs a Foundation buy-and-burn, so its on-chain burn signer is a treasury,
not customers; its demand base is off-chain and not measurable from burn data.
The reconciliation then read DIMO as a protocol-mediated pooled burn; v18 retires
that reading (see the v18 note above: its null-address flow is bridge exits).
Hivemapper's burns route through
a single proxy relayer contract (96.1% of burns), so it is likewise off-axis.

This figure plots the one construct-valid burn-signer point (Helium) on the
demand axis and places the off-chain / not-measurable protocols in a shaded
off-axis lane at left, positioned by S2R only. The "4-5x gap" claim is retired.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

plt.rcParams.update({
    "font.family": "serif", "font.size": 9,
    "axes.spines.top": False, "axes.spines.right": False,
})
fig, ax = plt.subplots(figsize=(7.3, 5.12))

# Off-axis lane (left): demand off-chain / not measurable via burn signers
LANE_HI = 0.055
ax.axvspan(-0.02, LANE_HI, color="#eef0f2", zorder=0)
ax.axvspan(LANE_HI, 0.46, color="#fbf7ef", zorder=0)
ax.axhline(1.0, color="#888888", linestyle="--", linewidth=0.9, zorder=1)
ax.text(0.115, 1.04, "S2R = 1.0 (fiscal parity)", fontsize=7.5, style="italic", color="#666666")

ax.text(0.0175, 2.24, "Demand off-chain\n(not measurable via burns)", color="#666666",
        fontsize=7.5, style="italic", ha="center")
ax.text(0.29, 2.24, "Demand observable on-chain\n(direct-payment)", color="#666666",
        fontsize=7.5, style="italic", ha="center")

blue, orange, grey = "#1f77b4", "#c64600", "#8a8a8a"

# Off-axis lane markers (positioned by S2R only; x is nominal within the lane)
ax.scatter([0.030], [0.219], s=110, facecolors="none", edgecolors=blue, linewidths=1.6, zorder=5)  # GEODNET
ax.scatter([0.040], [0.183], s=120, color=grey, marker="x", zorder=5)                               # Hivemapper (S2R 0.183)

# Construct-valid burn-signer point
ax.scatter([0.27], [1.84], s=130, color=orange, marker="D", zorder=5)                               # Helium (direct-burn)
ax.scatter([0.31], [0.0], s=120, color=orange, marker="s", zorder=5)                                # Livepeer (direct-fee; S2R ~0)

def label(x, y, tx, ty, text, edge):
    ax.annotate(text, xy=(x, y), xytext=(tx, ty), fontsize=7,
                bbox=dict(boxstyle="round,pad=0.32", facecolor="white", edgecolor=edge, linewidth=0.8),
                arrowprops=dict(arrowstyle="-", color="#555555", linewidth=0.6))

label(0.030, 0.219, 0.072, 1.25, "GEODNET\n(Foundation buy-and-burn;\ndemand off-chain)", blue)
label(0.040, 0.183, 0.090, 0.62, "Hivemapper\n(single credit-purchase relayer;\nnot measurable)", grey)
label(0.27, 1.84, 0.310, 1.40, "Helium\n(direct DC burns;\nHHI 0.27, top-2: 70.1%)", orange)
label(0.31, 0.0, 0.350, 0.60, "Livepeer\n(direct fee payments;\nfee-payer HHI 0.31, top-2: 75%)", orange)

handles = [
    Line2D([0], [0], marker="D", color="w", markerfacecolor=orange, markersize=8,
           label="Direct-burn (demand on-chain)"),
    Line2D([0], [0], marker="s", color="w", markerfacecolor=orange, markersize=8,
           label="Direct-fee (demand on-chain)"),
    Line2D([0], [0], marker="o", color="w", markerfacecolor="none", markeredgecolor=blue,
           markersize=9, label="Foundation buy-and-burn (demand off-chain)"),
    Line2D([0], [0], marker="x", color="w", markeredgecolor=grey, markerfacecolor=grey,
           markersize=9, label="Single-relayer burns (not measurable)"),
]
ax.legend(handles=handles, loc="lower left", bbox_to_anchor=(0.26, 0.02),
          fontsize=7, framealpha=0.95)

ax.set_xlim(-0.02, 0.46)
ax.set_ylim(-0.25, 2.45)
ax.set_xlabel("Demand Concentration (direct-payer HHI; valid only for direct-payment protocols)", fontsize=9)
ax.set_ylabel("S2R (burns / emissions)", fontsize=9)
ax.tick_params(labelsize=8)

fig.text(
    0.5, 0.012,
    "Direct-payer HHI is a valid demand-concentration measure only where customers pay the protocol directly on-chain (Helium burns, Livepeer fees).\n"
    "Buy-and-burn (GEODNET) and single-relayer (Hivemapper) architectures place demand off-chain and off-axis here.\n"
    "DIMO is not plotted: its null-address flow is almost entirely bridge transfers.",
    ha="center", fontsize=6, style="italic", color="#666666",
)
fig.tight_layout(rect=(0, 0.05, 1, 1))
fig.savefig("research_content/papers/B3_who_burns_the_tokens/exhibits/B3_figure4_regime_matrix.png", dpi=160)
print("Figure 4 v18 regenerated (Helium direct-burn + Livepeer direct-fee on-axis; GEODNET/Hivemapper off-axis lane; DIMO removed per the burn-construct validation).")
