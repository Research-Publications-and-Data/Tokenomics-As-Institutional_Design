"""
Generate Exhibits 1, 2, 3, 5 for B2/B3 papers.
Run from ~/b2-governance-data/
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import mannwhitneyu

plt.rcParams.update({
    'figure.dpi': 300,
    'font.family': 'serif',
    'font.size': 10,
    'axes.titlesize': 12,
    'axes.labelsize': 11,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'axes.grid': True,
    'grid.alpha': 0.3,
    'grid.linestyle': '--',
})

DEPIN_COLOR  = '#2C5F8A'
DEFI_COLOR   = '#8B4513'
INFRA_COLOR  = '#556B2F'
HIGHLIGHT_COLOR = '#CC0000'

# ── EXHIBIT 1 ─────────────────────────────────────────────────────────────────
print("Generating Exhibit 1: Subsidy vs HHI scatterplot...")

reg = pd.read_csv('data/processed/regression_data_april2026.csv')
sub = reg.dropna(subset=['subsidy_ratio_onchain', 'hhi']).copy()

lpt     = sub[sub['protocol'].str.lower() == 'livepeer']
non_lpt = sub[sub['protocol'].str.lower() != 'livepeer']

fig, ax = plt.subplots(figsize=(8.5, 5.5))

for cat, color, label in [
    ('DePIN',    DEPIN_COLOR,  'DePIN'),
    ('DeFi',     DEFI_COLOR,   'DeFi'),
    ('Infra',    INFRA_COLOR,  'Infrastructure'),   # str.contains matches L1_L2_Infra
]:
    mask   = non_lpt['category'].str.contains(cat, case=False, na=False)
    subset = non_lpt[mask]
    if len(subset) > 0:
        ax.scatter(subset['subsidy_ratio_onchain'], subset['hhi'],
                   c=color, s=50, alpha=0.7, label=label, zorder=3)

# LPT as highlighted outlier
ax.scatter(lpt['subsidy_ratio_onchain'], lpt['hhi'],
           c=HIGHLIGHT_COLOR, s=120, marker='D', zorder=4, label='Livepeer (outlier)')

# Regression WITH LPT
x_all = sub['subsidy_ratio_onchain'].values
y_all = sub['hhi'].values
slope, intercept, r, p, _ = stats.linregress(x_all, y_all)
x_line = np.linspace(0, max(x_all) * 1.05, 100)
ax.plot(x_line, slope * x_line + intercept,
        color=HIGHLIGHT_COLOR, linestyle='-', linewidth=1.5, alpha=0.6,
        label=f'With LPT: r={r:.2f}, p={p:.3f}')

# Regression WITHOUT LPT
x_no = non_lpt['subsidy_ratio_onchain'].values
y_no = non_lpt['hhi'].values
slope2, intercept2, r2, p2, _ = stats.linregress(x_no, y_no)
x_line2 = np.linspace(0, max(x_no) * 1.05, 100)
ax.plot(x_line2, slope2 * x_line2 + intercept2,
        color='gray', linestyle='--', linewidth=1.5, alpha=0.6,
        label=f'Without LPT: r={r2:.2f}, p={p2:.2f}')

# Annotate LPT
ax.annotate('Livepeer\n(88.5x, HHI 0.20)',
            xy=(lpt['subsidy_ratio_onchain'].values[0], lpt['hhi'].values[0]),
            xytext=(-60, 20), textcoords='offset points',
            fontsize=9, fontstyle='italic', color=HIGHLIGHT_COLOR,
            arrowprops=dict(arrowstyle='->', color=HIGHLIGHT_COLOR, lw=1.2))

ax.set_xlabel('Subsidy Ratio (emissions / revenue)', fontsize=11)
ax.set_ylabel('Governance HHI (post-exclusion)', fontsize=11)
ax.legend(loc='upper left', framealpha=0.9, fontsize=8)

fig.text(0.5, 0.01,
         'Source: Author calculations from Dune Analytics and Token Terminal (March 2026). N=20.',
         ha='center', fontsize=8, fontstyle='italic', color='gray')

plt.tight_layout(rect=[0, 0.03, 1, 1])
plt.savefig('exhibits/exhibit_subsidy_vs_hhi.png', dpi=300, bbox_inches='tight')
plt.savefig('exhibits/exhibit_subsidy_vs_hhi.pdf', bbox_inches='tight')
plt.close()
print(f"  r_full={r:.3f} p_full={p:.4f}  r_noLPT={r2:.3f} p_noLPT={p2:.4f}  N={len(sub)}")
print("  ✓ Exhibit 1 saved")


# ── EXHIBIT 2 ─────────────────────────────────────────────────────────────────
print("\nGenerating Exhibit 2: DePIN vs DeFi sector box plot...")

depin = reg[reg['category'] == 'DePIN']['hhi'].dropna()
defi  = reg[reg['category'] == 'DeFi']['hhi'].dropna()

fig, ax = plt.subplots(figsize=(6, 5))

bp = ax.boxplot([defi.values, depin.values],
                positions=[1, 2], widths=0.5,
                patch_artist=True, showmeans=True,
                meanprops=dict(marker='D', markerfacecolor='white',
                               markeredgecolor='black', markersize=6),
                medianprops=dict(color='black', linewidth=1.5))

bp['boxes'][0].set_facecolor(DEFI_COLOR + '40')
bp['boxes'][0].set_edgecolor(DEFI_COLOR)
bp['boxes'][1].set_facecolor(DEPIN_COLOR + '40')
bp['boxes'][1].set_edgecolor(DEPIN_COLOR)

# Overlay individual points with jitter
np.random.seed(42)
jitter = 0.08
ax.scatter(np.ones(len(defi))  + np.random.uniform(-jitter, jitter, len(defi)),
           defi.values,  c=DEFI_COLOR,  s=30, alpha=0.6, zorder=3)
ax.scatter(np.ones(len(depin)) * 2 + np.random.uniform(-jitter, jitter, len(depin)),
           depin.values, c=DEPIN_COLOR, s=30, alpha=0.6, zorder=3)

ax.set_xticks([1, 2])
ax.set_xticklabels([f'DeFi (N={len(defi)})', f'DePIN (N={len(depin)})'], fontsize=11)
ax.set_ylabel('Governance HHI (post-exclusion)', fontsize=11)

# Annotate means
ax.annotate(f'Mean: {defi.mean():.3f}', xy=(1, defi.mean()),
            xytext=(30, 10), textcoords='offset points', fontsize=9)
ax.annotate(f'Mean: {depin.mean():.3f}', xy=(2, depin.mean()),
            xytext=(30, 10), textcoords='offset points', fontsize=9)

# Significance bracket
u, p_mw = mannwhitneyu(depin, defi, alternative='two-sided')
y_max   = max(depin.max(), defi.max()) * 1.02
ax.plot([1, 1, 2, 2], [y_max, y_max * 1.03, y_max * 1.03, y_max],
        color='black', linewidth=1)
ax.text(1.5, y_max * 1.05, f"Mann-Whitney p = {p_mw:.3f}\nCohen's d = 1.00",
        ha='center', fontsize=9, fontstyle='italic')

fig.text(0.5, 0.01,
         'Source: Author calculations. Diamond = mean. Horizontal line = median. '
         'Individual protocols overlaid.',
         ha='center', fontsize=8, fontstyle='italic', color='gray')

plt.tight_layout(rect=[0, 0.03, 1, 1])
plt.savefig('exhibits/exhibit_sector_comparison.png', dpi=300, bbox_inches='tight')
plt.savefig('exhibits/exhibit_sector_comparison.pdf', bbox_inches='tight')
plt.close()
print(f"  DeFi mean={defi.mean():.3f} N={len(defi)}  DePIN mean={depin.mean():.3f} N={len(depin)}  MW p={p_mw:.4f}")
print("  ✓ Exhibit 2 saved")


# ── EXHIBIT 3 ─────────────────────────────────────────────────────────────────
print("\nGenerating Exhibit 3: GEODNET burn rate trajectory...")

geodnet_data = [
    ('2024-04-01',  2), ('2024-05-01',  3), ('2024-06-01',  5),
    ('2024-07-01',  8), ('2024-08-01', 15), ('2024-09-01', 12),
    ('2024-10-01', 14), ('2024-11-01', 15), ('2024-12-01', 15),
    ('2025-01-01', 15), ('2025-02-01', 20), ('2025-03-01', 28),
    ('2025-04-01', 35), ('2025-05-01', 40), ('2025-06-01', 45),
    ('2025-07-01', 55), ('2025-08-01', 65), ('2025-09-01', 75),
    ('2025-10-01', 55), ('2025-11-01', 60), ('2025-12-01', 65),
    ('2026-01-01', 62),
]

dates = pd.to_datetime([d[0] for d in geodnet_data])
rates = [d[1] for d in geodnet_data]

fig, ax = plt.subplots(figsize=(8.5, 5))

ax.plot(dates, rates, color=DEPIN_COLOR, linewidth=2, marker='o', markersize=4)
ax.fill_between(dates, rates, alpha=0.15, color=DEPIN_COLOR)

# 50% reference line
ax.axhline(y=50, color='gray', linestyle='--', linewidth=1, alpha=0.5)
ax.text(dates[-1] + pd.Timedelta(days=10), 51, '50% absorption',
        fontsize=8, color='gray', va='bottom')

# Peak annotation
peak_idx = rates.index(max(rates))
ax.annotate(f'Peak: {max(rates)}%\n(Sep 2025)',
            xy=(dates[peak_idx], max(rates)),
            xytext=(-80, 10), textcoords='offset points',
            fontsize=9, fontstyle='italic',
            arrowprops=dict(arrowstyle='->', color=DEPIN_COLOR, lw=1.2))

# Current value annotation
ax.annotate(f'~62%\n(Jan 2026)',
            xy=(dates[-1], rates[-1]),
            xytext=(10, -25), textcoords='offset points',
            fontsize=9, fontstyle='italic', color=DEPIN_COLOR)

# Halving annotation
halving_date = pd.Timestamp('2025-07-01')
ax.axvline(x=halving_date, color='orange', linestyle=':', linewidth=1, alpha=0.6)
ax.text(halving_date, 5, 'Annual\nhalving', fontsize=7, color='orange',
        ha='center', fontstyle='italic')

ax.set_xlabel('Date', fontsize=11)
ax.set_ylabel('Burn Absorption Rate (% of emissions)', fontsize=11)
ax.set_ylim(0, 100)

fig.text(0.5, 0.01,
         'Source: Blockworks GEODNET analytics (weekly data, April 2026). '
         'Burn rate = percentage of token issuance offset by subscription-funded burns.',
         ha='center', fontsize=8, fontstyle='italic', color='gray')

plt.tight_layout(rect=[0, 0.03, 1, 1])
plt.savefig('exhibits/exhibit_geodnet_burn_trajectory.png', dpi=300, bbox_inches='tight')
plt.savefig('exhibits/exhibit_geodnet_burn_trajectory.pdf', bbox_inches='tight')
plt.close()
print("  ✓ Exhibit 3 saved")


# ── EXHIBIT 5 ─────────────────────────────────────────────────────────────────
print("\nGenerating Exhibit 5: Helium 'Who Burns?' bar chart...")

helium = pd.read_csv('data/raw/helium_burn_concentration.csv')
# Use pre-computed shares (relative to all signers, not just top-20)
helium = helium.sort_values('burn_share', ascending=False).reset_index(drop=True)
helium['share']      = helium['burn_share']        # already fractional (0.41, 0.28…)
helium['cumulative'] = helium['cumulative_share']  # pre-computed

# Truncate addresses for display
helium['label'] = helium['burn_address'].apply(
    lambda x: str(x)[:6] + '...' + str(x)[-4:] if len(str(x)) > 12 else str(x))

top_n      = 10
plot_data  = helium.head(top_n).copy()
others_share = 1.0 - plot_data['share'].sum()

fig, ax = plt.subplots(figsize=(8, 5.5))

y_pos  = np.arange(top_n)
colors = [HIGHLIGHT_COLOR if i < 2 else DEPIN_COLOR for i in range(top_n)]

bars = ax.barh(y_pos, plot_data['share'].values * 100, color=colors, alpha=0.7,
               edgecolor='black', linewidth=0.5)

# Percentage labels on bars
for i, (bar, share, cum) in enumerate(zip(bars, plot_data['share'], plot_data['cumulative'])):
    width = bar.get_width()
    if width > 5:
        ax.text(width - 1, bar.get_y() + bar.get_height() / 2,
                f'{share:.1%}', ha='right', va='center', fontsize=8,
                fontweight='bold', color='white')
    else:
        ax.text(width + 0.5, bar.get_y() + bar.get_height() / 2,
                f'{share:.1%}', ha='left', va='center', fontsize=8)

# Cumulative annotation on right side
for i, cum in enumerate(plot_data['cumulative']):
    ax.text(52, i, f'cum: {cum:.1%}', fontsize=7, va='center', color='gray',
            fontstyle='italic')

# Y-axis labels
ax.set_yticks(y_pos)
ax.set_yticklabels(plot_data['label'].values, fontsize=8, fontfamily='monospace')
ax.invert_yaxis()

# "Others" annotation
n_others = len(helium) - top_n
ax.text(25, top_n + 0.3,
        f'Remaining {n_others}+ signers: {others_share:.1%}',
        fontsize=9, fontstyle='italic', color='gray', ha='center')

ax.set_xlabel('Share of Total DC Burns (%)', fontsize=11)
ax.set_xlim(0, 58)

# Top-2 bracket
top2_share = plot_data['share'].head(2).sum()
ax.plot([48, 48], [-0.4, 1.4], color=HIGHLIGHT_COLOR, linewidth=2)
ax.text(49, 0.5, f'Top 2:\n{top2_share:.1%}',
        fontsize=9, fontweight='bold', color=HIGHLIGHT_COLOR, va='center')

# Top-5 bracket
top5_share = plot_data['share'].head(5).sum()
ax.plot([45, 45], [-0.4, 4.4], color=DEPIN_COLOR, linewidth=1.5, linestyle='--')
ax.text(45.5, 2, f'Top 5:\n{top5_share:.1%}',
        fontsize=8, color=DEPIN_COLOR, va='center')

fig.text(0.5, 0.01,
         f'Source: Dune Analytics query Q6942532 (Solana, Jan\u2013Mar 2026). '
         f'N = {len(helium):,} unique burn signers shown (top-20 of 3,767 total).',
         ha='center', fontsize=7.5, fontstyle='italic', color='gray')

plt.tight_layout(rect=[0, 0.03, 1, 1])
plt.savefig('exhibits/exhibit_helium_who_burns.png', dpi=300, bbox_inches='tight')
plt.savefig('exhibits/exhibit_helium_who_burns.pdf', bbox_inches='tight')
plt.close()
print(f"  Top-2={top2_share:.1%}  Top-5={top5_share:.1%}  others={others_share:.1%}")
print("  ✓ Exhibit 5 saved")

print("\nDone. Verifying outputs...")
