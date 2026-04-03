"""
Regenerate all data-driven exhibits for B2 + B3.
Run from ~/b2-governance-data/
"""

import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path

# ── Output directory ─────────────────────────────────────────────────────────
Path('exhibits/updated').mkdir(parents=True, exist_ok=True)

# ── Publication style ─────────────────────────────────────────────────────────
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif'],
    'font.size': 11,
    'axes.titlesize': 13,
    'axes.labelsize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'axes.spines.top': False,
    'axes.spines.right': False,
})

DEPIN_COLOR  = '#2171b5'
DEFI_COLOR   = '#cb6d51'
INFRA_COLOR  = '#2d6a2e'
SOCIAL_COLOR = '#888888'
OUTLIER_COLOR = '#c0392b'
ACCENT       = '#e67e22'

cat_colors_map = {
    'DeFi':        DEFI_COLOR,
    'DePIN':       DEPIN_COLOR,
    'L1_L2_Infra': INFRA_COLOR,
    'Social_Dead': SOCIAL_COLOR,
}


def save(fig, name):
    for ext in ['png', 'pdf']:
        fig.savefig(f'exhibits/updated/{name}.{ext}', dpi=300, bbox_inches='tight')
    print(f'  ✓  {name}')
    plt.close(fig)


# ── Load master data ──────────────────────────────────────────────────────────
reg = pd.read_csv('data/processed/regression_data_april2026.csv')
print(f'regression_data: N={len(reg)}, categories={reg["category"].value_counts().to_dict()}')
print(f'Curve HHI = {reg[reg["protocol"].str.lower()=="curve"]["hhi"].values[0]:.6f}')


# ═══════════════════════════════════════════════════════════════════════════════
# B2 FIGURE 3 — HHI Bar Chart (all 40 protocols)
# ═══════════════════════════════════════════════════════════════════════════════
print('\n── Fig 3: HHI bar chart (N=40)')

cat_order = ['DeFi', 'DePIN', 'L1_L2_Infra', 'Social_Dead']
df = reg.sort_values(['category', 'hhi'], ascending=[True, True]).reset_index(drop=True)

y_pos, colors, labels, values = [], [], [], []
current_y = 0
for cat in cat_order:
    subset = df[df['category'] == cat]
    if len(subset) == 0:
        continue
    for _, row in subset.iterrows():
        y_pos.append(current_y)
        colors.append(cat_colors_map[cat])
        labels.append(row['protocol'])
        values.append(row['hhi'])
        current_y += 1
    current_y += 0.6  # gap between categories

fig, ax = plt.subplots(figsize=(12, 14))
ax.barh(y_pos, values, color=colors, height=0.72, edgecolor='white', linewidth=0.3)

# Value labels — right of bar
x_max = max(values)
for y, v in zip(y_pos, values):
    ax.text(v + x_max * 0.008, y, f'{v:.3f}', va='center', fontsize=8)

ax.set_yticks(y_pos)
ax.set_yticklabels(labels, fontsize=9)
ax.invert_yaxis()
ax.set_xlim(0, x_max * 1.18)

# HHI = 0.25 threshold
ax.axvline(x=0.25, color='gray', linestyle='--', linewidth=1, alpha=0.7)
ax.text(0.252, len(y_pos) - 2, 'HHI = 0.25\n(mod.\nconcentrated)',
        fontsize=7.5, color='gray', va='top')

ax.set_xlabel('Herfindahl-Hirschman Index (HHI)')

from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor=cat_colors_map[c],
          label=f'{c.replace("_", " ")} (N={len(df[df["category"]==c])})')
    for c in cat_order if c in df['category'].values
]
ax.legend(handles=legend_elements, loc='lower right', fontsize=9)

fig.text(0.5, -0.005,
         'Source: Dune Analytics + Helius DAS API (March 2026). '
         '69 protocol-controlled addresses excluded across 20 protocols.',
         ha='center', fontsize=8, style='italic', color='gray')

save(fig, 'fig3_hhi_bar_40protocols')


# ═══════════════════════════════════════════════════════════════════════════════
# B2 FIGURE 4 — Sector Box Plot (DePIN vs DeFi)
# ═══════════════════════════════════════════════════════════════════════════════
print('── Fig 4: Sector boxplot')

defi  = reg[reg['category'] == 'DeFi']['hhi']
depin = reg[reg['category'] == 'DePIN']['hhi']

stat, p_mw = stats.mannwhitneyu(depin, defi, alternative='greater')
d_cohen = (depin.mean() - defi.mean()) / np.sqrt((depin.std()**2 + defi.std()**2) / 2)

print(f'  DeFi:  mean={defi.mean():.4f}, N={len(defi)}')
print(f'  DePIN: mean={depin.mean():.4f}, N={len(depin)}')
print(f'  MW p={p_mw:.4f}, Cohen d={d_cohen:.3f}')

fig, ax = plt.subplots(figsize=(7, 8))

bp = ax.boxplot(
    [defi.values, depin.values], positions=[1, 2], widths=0.5,
    patch_artist=True, showmeans=True,
    meanprops=dict(marker='D', markerfacecolor='white', markeredgecolor='black', markersize=8),
    medianprops=dict(color='black', linewidth=2)
)
bp['boxes'][0].set_facecolor(DEFI_COLOR);  bp['boxes'][0].set_alpha(0.4)
bp['boxes'][1].set_facecolor(DEPIN_COLOR); bp['boxes'][1].set_alpha(0.4)

# Jitter points
np.random.seed(42)
for data, pos, color in [(defi, 1, DEFI_COLOR), (depin, 2, DEPIN_COLOR)]:
    jitter = np.random.normal(0, 0.04, len(data))
    ax.scatter(pos + jitter, data.values, color=color, alpha=0.6, s=40,
               zorder=3, edgecolors='white', linewidth=0.5)

ax.text(1.35, defi.mean(),  f'Mean: {defi.mean():.3f}',  va='center', fontsize=10)
ax.text(2.35, depin.mean(), f'Mean: {depin.mean():.3f}', va='center', fontsize=10)

# Significance bracket
y_top = max(depin.max(), defi.max()) + 0.015
ax.plot([1, 1, 2, 2], [y_top, y_top + 0.005, y_top + 0.005, y_top], 'k-', linewidth=1)
ax.text(1.5, y_top + 0.009, f'Mann-Whitney p = {p_mw:.3f}', ha='center', fontsize=10, style='italic')
ax.text(1.5, y_top + 0.003, f"Cohen's d = {d_cohen:.2f}",   ha='center', fontsize=10, style='italic')

ax.set_xticks([1, 2])
ax.set_xticklabels([f'DeFi (N={len(defi)})', f'DePIN (N={len(depin)})'], fontsize=11)
ax.set_ylabel('Governance HHI (post-exclusion)')

fig.text(0.5, -0.02,
         'Source: Author calculations. Diamond = mean. '
         'Horizontal line = median. Individual protocols overlaid.',
         ha='center', fontsize=8, style='italic', color='gray')

save(fig, 'fig4_sector_boxplot')


# ═══════════════════════════════════════════════════════════════════════════════
# B2 FIGURE 5 — Allocation Scatter (null result)
# Column: insider_pct, already in percentage-point units (0–100)
# ═══════════════════════════════════════════════════════════════════════════════
print('── Fig 5: Allocation scatter')

alloc = reg.dropna(subset=['insider_pct', 'hhi']).copy()
print(f'  N={len(alloc)}')

fig, ax = plt.subplots(figsize=(12, 7))

for cat in alloc['category'].unique():
    subset = alloc[alloc['category'] == cat]
    ax.scatter(subset['insider_pct'], subset['hhi'],
               color=cat_colors_map.get(cat, SOCIAL_COLOR), s=60, alpha=0.8,
               label=cat.replace('_', ' '), edgecolors='white', linewidth=0.5, zorder=3)

x = alloc['insider_pct'].values
y = alloc['hhi'].values
slope, intercept, r, p, se = stats.linregress(x, y)

x_line = np.linspace(x.min(), x.max(), 100)
y_line = slope * x_line + intercept
n = len(x)
se_y = np.sqrt(np.sum((y - (slope * x + intercept))**2) / (n - 2))
ci = 1.96 * se_y * np.sqrt(1/n + (x_line - x.mean())**2 / np.sum((x - x.mean())**2))

ax.plot(x_line, y_line, '--', color='gray', linewidth=1.5, alpha=0.8)
ax.fill_between(x_line, y_line - ci, y_line + ci, alpha=0.10, color='gray')

# Protocol labels — use adjustText if available
try:
    from adjustText import adjust_text
    texts = [
        ax.text(row['insider_pct'], row['hhi'], row['protocol'],
                fontsize=7, alpha=0.85,
                color=cat_colors_map.get(row['category'], 'gray'))
        for _, row in alloc.iterrows()
    ]
    adjust_text(texts, arrowprops=dict(arrowstyle='-', color='gray', lw=0.3))
except ImportError:
    for _, row in alloc.iterrows():
        ax.annotate(row['protocol'], (row['insider_pct'], row['hhi']),
                    fontsize=7, alpha=0.85, xytext=(3, 3), textcoords='offset points',
                    color=cat_colors_map.get(row['category'], 'gray'))

ax.set_title(f'Insider Allocation Is Uninformative (r = {r:.2f}, p = {p:.2f}, N = {len(alloc)})',
             fontweight='bold')
ax.set_xlabel('Initial Insider Allocation (percentage points)')
ax.set_ylabel('Governance Token HHI (April 2026)')
ax.legend(title='Category', loc='upper right')

fig.text(0.5, -0.02,
         'Source: Author calculations from Dune Analytics and Token Terminal (March 2026).',
         ha='center', fontsize=8, style='italic', color='gray')

save(fig, 'fig5_allocation_scatter')


# ═══════════════════════════════════════════════════════════════════════════════
# B2 FIGURE 6 — Delegation Comparison (holding vs voting HHI)
# Data from delegation_adjusted_hhi.csv + computed Snapshot HHIs
# ═══════════════════════════════════════════════════════════════════════════════
print('── Fig 6: Delegation grouped bars')

# Tally protocols from delegation_adjusted_hhi.csv
d_adj = pd.read_csv('data/processed/delegation_adjusted_hhi.csv')

# Snapshot voting HHIs (pre-computed from snapshot_votes.csv)
snapshot_rows = [
    {'protocol': 'DIMO',      'symbol': 'DIMO', 'raw_hhi': 0.037903, 'delegated_hhi': 0.237580,
     'category': 'DePIN',  'source': 'Snapshot'},
    {'protocol': 'WeatherXM', 'symbol': 'WXM',  'raw_hhi': 0.147854, 'delegated_hhi': 0.386122,
     'category': 'DePIN',  'source': 'Snapshot'},
    {'protocol': 'Lido',      'symbol': 'LDO',  'raw_hhi': 0.012817, 'delegated_hhi': 0.094353,
     'category': 'DeFi',   'source': 'Snapshot'},
]

# Category map for tally protocols
cat_map = {'Aave': 'DeFi', 'Compound': 'DeFi', 'Uniswap': 'DeFi',
           'Arbitrum': 'L1_L2_Infra', 'Optimism': 'L1_L2_Infra'}

tally_rows = []
for _, row in d_adj.iterrows():
    tally_rows.append({
        'protocol':     row['protocol'],
        'raw_hhi':      row['raw_hhi'],
        'delegated_hhi': row['delegated_hhi'],
        'category':     cat_map.get(row['protocol'], 'DeFi'),
        'source':       row['source'],
    })

deleg = pd.DataFrame(tally_rows + snapshot_rows)
deleg['ratio'] = deleg['delegated_hhi'] / deleg['raw_hhi']
deleg = deleg.sort_values('ratio', ascending=True).reset_index(drop=True)

print(deleg[['protocol', 'raw_hhi', 'delegated_hhi', 'ratio']].to_string(float_format='%.4f'))

fig, ax = plt.subplots(figsize=(10, 6))
y = np.arange(len(deleg))
bh = 0.35

ax.barh(y - bh/2, deleg['raw_hhi'],      bh, label='Holding HHI', color=DEFI_COLOR,  alpha=0.7, edgecolor='white')
ax.barh(y + bh/2, deleg['delegated_hhi'], bh, label='Voting HHI',  color=DEPIN_COLOR, alpha=0.7, edgecolor='white')

# Ratio annotations
for i, row in deleg.iterrows():
    max_val = max(row['raw_hhi'], row['delegated_hhi'])
    txt = f'{row["ratio"]:.2f}x' if row['ratio'] < 1.0 else f'{row["ratio"]:.1f}x'
    clr = OUTLIER_COLOR if row['ratio'] > 3 else ('green' if row['ratio'] < 0.9 else 'gray')
    ax.text(max_val + 0.008, i, txt, va='center', fontsize=9, fontweight='bold', color=clr)

# Source annotation (Snapshot vs Tally)
for i, row in deleg.iterrows():
    ax.text(-0.003, i, row['source'], va='center', ha='right', fontsize=7, color='gray', style='italic')

ax.set_yticks(y)
ax.set_yticklabels(deleg['protocol'], fontsize=10)
ax.set_xlabel('HHI')
ax.legend(loc='lower right')
ax.set_xlim(-0.05, deleg['delegated_hhi'].max() * 1.25)

fig.text(0.5, -0.03,
         'Source: Tally (on-chain) and Snapshot (off-chain) governance data. '
         'Ratio > 1.0 = delegation concentrates voting power; < 1.0 = distributes it.',
         ha='center', fontsize=8, style='italic', color='gray')

save(fig, 'fig6_delegation_grouped')


# ═══════════════════════════════════════════════════════════════════════════════
# B2 FIGURE 7 — Subsidy Scatter (Livepeer outlier prominent)
# ═══════════════════════════════════════════════════════════════════════════════
print('── Fig 7: Subsidy scatter')

sub = reg.dropna(subset=['subsidy_ratio_onchain', 'hhi']).copy()
print(f'  N={len(sub)}, Livepeer={sub[sub["protocol"].str.lower()=="livepeer"]["subsidy_ratio_onchain"].values}')

lpt  = sub[sub['protocol'].str.lower() == 'livepeer']
rest = sub[sub['protocol'].str.lower() != 'livepeer']

fig, ax = plt.subplots(figsize=(10, 7))

for cat in rest['category'].unique():
    s = rest[rest['category'] == cat]
    ax.scatter(s['subsidy_ratio_onchain'], s['hhi'],
               color=cat_colors_map.get(cat, SOCIAL_COLOR), s=50, alpha=0.7,
               label=cat.replace('_', ' '), zorder=3, edgecolors='white', linewidth=0.5)

# LPT diamond
if len(lpt) > 0:
    ax.scatter(lpt['subsidy_ratio_onchain'], lpt['hhi'],
               color=OUTLIER_COLOR, marker='D', s=130, zorder=4,
               edgecolors='black', linewidth=1)
    ax.annotate(f'Livepeer\n({lpt["subsidy_ratio_onchain"].values[0]:.1f}× subsidy\nHHI {lpt["hhi"].values[0]:.2f})',
                (lpt['subsidy_ratio_onchain'].values[0], lpt['hhi'].values[0]),
                xytext=(-25, 20), textcoords='offset points',
                fontsize=9, color=OUTLIER_COLOR, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=OUTLIER_COLOR, lw=1))

# Regression lines
x_all = sub['subsidy_ratio_onchain'].values;   y_all = sub['hhi'].values
sl_a, ic_a, r_a, p_a, _ = stats.linregress(x_all, y_all)
x_ln_a = np.linspace(0, x_all.max() * 1.04, 100)
ax.plot(x_ln_a, sl_a * x_ln_a + ic_a, '-',  color=OUTLIER_COLOR, alpha=0.5, linewidth=1.5,
        label=f'With LPT: r={r_a:.2f}, p={p_a:.3f}')

x_r = rest['subsidy_ratio_onchain'].values;    y_r = rest['hhi'].values
sl_r, ic_r, r_r, p_r, _ = stats.linregress(x_r, y_r)
x_ln_r = np.linspace(0, x_r.max() * 1.10, 100)
ax.plot(x_ln_r, sl_r * x_ln_r + ic_r, '--', color='gray', alpha=0.7, linewidth=1.5,
        label=f'Without LPT: r={r_r:.2f}, p={p_r:.3f}')

ax.set_xlabel('Subsidy Ratio (emissions / revenue)')
ax.set_ylabel('Governance HHI (post-exclusion)')
ax.legend(loc='upper left', fontsize=9)

fig.text(0.5, -0.02,
         f'Source: Author calculations from Dune Analytics and Token Terminal (March 2026). N={len(sub)}.',
         ha='center', fontsize=8, style='italic', color='gray')

save(fig, 'fig7_subsidy_scatter')


# ═══════════════════════════════════════════════════════════════════════════════
# B2 FIGURE 8 — HHI vs Participation (voters per proposal)
# Uses actual Snapshot + Tally avg voters data
# ═══════════════════════════════════════════════════════════════════════════════
print('── Fig 8: HHI vs participation')

# Avg voters per proposal (from snapshot_proposals.csv + tally_delegates.csv)
# Tally: use n_delegates as proxy for active voter pool; Snapshot: avg votes per proposal
part = pd.DataFrame([
    # Tally protocols — average "votes" field not available directly; use n_delegates
    {'protocol': 'Aave',      'hhi': 0.020202, 'voters_per_proposal': 100,  'category': 'DeFi'},
    {'protocol': 'Compound',  'hhi': 0.028930, 'voters_per_proposal': 23,   'category': 'DeFi'},
    {'protocol': 'Uniswap',   'hhi': 0.032200, 'voters_per_proposal': 237,  'category': 'DeFi'},
    {'protocol': 'Lido',      'hhi': 0.012817, 'voters_per_proposal': 83,   'category': 'DeFi'},
    {'protocol': 'Optimism',  'hhi': 0.009097, 'voters_per_proposal': 100,  'category': 'L1_L2_Infra'},
    {'protocol': 'Arbitrum',  'hhi': 0.011844, 'voters_per_proposal': 2574, 'category': 'L1_L2_Infra'},
    {'protocol': 'DIMO',      'hhi': 0.037903, 'voters_per_proposal': 8,    'category': 'DePIN'},
    {'protocol': 'WeatherXM', 'hhi': 0.147854, 'voters_per_proposal': 52,   'category': 'DePIN'},
])

# Verify vs actual Snapshot avg voters
# Snapshot: ARB=2574, COMP=23, DIMO=7.5→8, LDO=83, UNI=237, WXM=52

fig, ax = plt.subplots(figsize=(10, 7))

for cat in part['category'].unique():
    s = part[part['category'] == cat]
    ax.scatter(s['hhi'], s['voters_per_proposal'],
               color=cat_colors_map.get(cat, SOCIAL_COLOR), s=80, alpha=0.8,
               label=cat.replace('_', ' '), zorder=3, edgecolors='white', linewidth=0.5)

for _, row in part.iterrows():
    ax.annotate(row['protocol'], (row['hhi'], row['voters_per_proposal']),
                xytext=(5, 5), textcoords='offset points', fontsize=9,
                color=cat_colors_map.get(row['category'], 'gray'))

# Log-linear fit
x = part['hhi'].values
log_y = np.log10(part['voters_per_proposal'].values)
slope, intercept, r, p, _ = stats.linregress(x, log_y)
x_line = np.linspace(x.min() * 0.7, x.max() * 1.15, 100)
y_line = 10 ** (slope * x_line + intercept)

n = len(x)
se_y = np.sqrt(np.sum((log_y - (slope * x + intercept))**2) / (n - 2))
ci = 1.96 * se_y * np.sqrt(1/n + (x_line - x.mean())**2 / np.sum((x - x.mean())**2))

ax.plot(x_line, y_line, '--', color='gray', linewidth=1.5, alpha=0.7)
ax.fill_between(x_line, 10**(slope*x_line+intercept-ci), 10**(slope*x_line+intercept+ci),
                alpha=0.08, color='gray')

ax.set_yscale('log')
ax.set_xlabel('Governance Token HHI')
ax.set_ylabel('Unique Voters per Proposal (log scale)')
ax.set_title(f'Governance Concentration vs Participation (r = {r:.2f}, N = {len(part)})')
ax.legend(title='Category', loc='upper left')

fig.text(0.5, -0.02,
         'Source: Tally and Snapshot governance data (12-month lookback). '
         'Tally uses top-100 delegate count; Snapshot uses mean votes per proposal.',
         ha='center', fontsize=8, style='italic', color='gray')

save(fig, 'fig8_participation')


# ═══════════════════════════════════════════════════════════════════════════════
# B3 FIGURE 2 — Helium "Who Burns?" (top-20 burn addresses)
# ═══════════════════════════════════════════════════════════════════════════════
print('── B3 Fig 2: Helium burn concentration')

burn = pd.read_csv('data/raw/helium_burn_concentration.csv')
top20 = burn.head(20).copy()
total_shown_pct = top20['burn_share'].sum() * 100
print(f'  Top-20 cumulative: {total_shown_pct:.1f}%  |  Top-2: {top20["burn_share"].head(2).sum()*100:.1f}%')

fig, ax = plt.subplots(figsize=(12, 8))

colors = []
for i in range(len(top20)):
    if i < 2:  colors.append(OUTLIER_COLOR)
    elif i < 5: colors.append(DEPIN_COLOR)
    else:       colors.append('#a6bddb')

ax.barh(range(len(top20)), top20['burn_share'] * 100, color=colors,
        edgecolor='white', linewidth=0.5)

# Truncated address labels
addr_col = top20.columns[1]  # burn_address
addr_labels = []
for addr in top20[addr_col]:
    s = str(addr)
    addr_labels.append(f'{s[:6]}…{s[-4:]}' if len(s) > 12 else s)

ax.set_yticks(range(len(top20)))
ax.set_yticklabels(addr_labels, fontsize=8.5, fontfamily='monospace')
ax.invert_yaxis()

# Percentage labels on bars
x_lim_max = top20['burn_share'].max() * 100
for i, (_, row) in enumerate(top20.iterrows()):
    pct = row['burn_share'] * 100
    if pct > 4:
        ax.text(pct - 0.8, i, f'{pct:.1f}%', va='center', ha='right',
                fontsize=9, color='white', fontweight='bold')
    else:
        ax.text(pct + 0.4, i, f'{pct:.1f}%', va='center', fontsize=8)

# Cumulative share annotations — on right side
cum = 0.0
for i, (_, row) in enumerate(top20.iterrows()):
    cum += row['burn_share'] * 100
    ax.text(x_lim_max * 1.01, i, f'cum {cum:.1f}%', va='center', ha='left',
            fontsize=7, color='gray', style='italic')

# Bracket lines — inset inside plot area, not outside
top2_pct  = top20['burn_share'].head(2).sum() * 100
top5_pct  = top20['burn_share'].head(5).sum() * 100
ax.axhline(y=1.5, color=OUTLIER_COLOR, linestyle='-',  linewidth=0.7, alpha=0.4, xmax=0.9)
ax.axhline(y=4.5, color=DEPIN_COLOR,   linestyle='--', linewidth=0.7, alpha=0.4, xmax=0.9)

# Side-bar annotations — use figure text with tight layout
ax.text(x_lim_max * 0.62, -0.6, f'Top 2: {top2_pct:.1f}%',
        va='center', fontsize=10, fontweight='bold', color=OUTLIER_COLOR)
ax.text(x_lim_max * 0.62, 3.5,  f'Top 5: {top5_pct:.1f}%',
        va='center', fontsize=10, fontweight='bold', color=DEPIN_COLOR)

ax.set_xlabel('Share of Total DC Burns (%)')
ax.set_xlim(0, x_lim_max * 1.35)

fig.text(0.5, -0.02,
         f'Source: Dune Analytics Q6942532 (Solana, Jan–Mar 2026). '
         f'N = 20 shown (top-20 of {len(burn):,} total burn signers).',
         ha='center', fontsize=8, style='italic', color='gray')

save(fig, 'b3_fig2_who_burns')


# ═══════════════════════════════════════════════════════════════════════════════
# B3 FIGURE 3 — GEODNET Burn Trajectory (from actual CSV data)
# ═══════════════════════════════════════════════════════════════════════════════
print('── B3 Fig 3: GEODNET burn trajectory')

geo_b = pd.read_csv('data/raw/geodnet_monthly_burns.csv')
geo_e = pd.read_csv('data/raw/geodnet_monthly_emissions.csv')

# Normalise month key (burns has full date, emissions may differ)
geo_b['month_key'] = pd.to_datetime(geo_b['month']).dt.to_period('M').astype(str)
geo_e['month_key'] = pd.to_datetime(geo_e['month']).dt.to_period('M').astype(str)

geo = geo_b.merge(geo_e[['month_key', 'geod_emitted']], on='month_key', how='inner')
geo['burn_pct'] = (geo['geod_burned'] / geo['geod_emitted'] * 100).clip(upper=100)
geo['date'] = pd.to_datetime(geo['month'])
geo = geo.sort_values('date').reset_index(drop=True)

print(geo[['date', 'geod_burned', 'geod_emitted', 'burn_pct']].to_string(float_format='%.1f'))

fig, ax = plt.subplots(figsize=(12, 6.5))

ax.plot(geo['date'], geo['burn_pct'], '-o', color='#1a5276',
        linewidth=2, markersize=5, zorder=3)
ax.fill_between(geo['date'], 0, geo['burn_pct'], alpha=0.15, color='#1a5276')

ax.axhline(y=50, color='gray', linestyle='--', linewidth=1, alpha=0.5)
ax.text(geo['date'].iloc[0], 52, '50% absorption threshold',
        fontsize=8, color='gray', style='italic', va='bottom')

# Halving marker (July 2025)
halving = pd.Timestamp('2025-07-01')
if geo['date'].min() <= halving <= geo['date'].max():
    ax.axvline(x=halving, color=ACCENT, linestyle=':', linewidth=1.5, alpha=0.7)
    ax.text(halving, geo['burn_pct'].min() + 2, 'Annual\nhalving',
            ha='center', fontsize=9, color=ACCENT, style='italic')

# Peak annotation
peak_idx = geo['burn_pct'].idxmax()
peak_date = geo.loc[peak_idx, 'date']
peak_val  = geo.loc[peak_idx, 'burn_pct']
ax.annotate(f'Peak: {peak_val:.0f}%\n({peak_date.strftime("%b %Y")})',
            (peak_date, peak_val), xytext=(-60, 15), textcoords='offset points',
            fontsize=9, color='#1a5276', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='#1a5276', lw=1))

# Latest value — offset up to avoid 50% line
last_date = geo['date'].iloc[-1]
last_val  = geo['burn_pct'].iloc[-1]
offset_y  = 25 if abs(last_val - 50) < 10 else 15
ax.annotate(f'{last_val:.0f}%\n({last_date.strftime("%b %Y")})',
            (last_date, last_val), xytext=(12, offset_y), textcoords='offset points',
            fontsize=9, color='#1a5276', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='#1a5276', lw=1))

ax.set_xlabel('Date')
ax.set_ylabel('Burn Absorption Rate (% of emissions)')
ax.set_ylim(0, 105)
ax.xaxis.set_major_formatter(mpl.dates.DateFormatter('%b\n%Y'))

fig.text(0.5, -0.02,
         'Source: Dune Analytics — GEODNET on-chain burn and emissions data (monthly). '
         'Burn rate = token burns as % of gross emissions.',
         ha='center', fontsize=8, style='italic', color='gray')

save(fig, 'b3_fig3_geodnet_trajectory')


# ═══════════════════════════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════════════════════════
print('\n── Verification')
expected = [
    'fig3_hhi_bar_40protocols', 'fig4_sector_boxplot', 'fig5_allocation_scatter',
    'fig6_delegation_grouped', 'fig7_subsidy_scatter', 'fig8_participation',
    'b3_fig2_who_burns', 'b3_fig3_geodnet_trajectory',
]
all_ok = True
for name in expected:
    for ext in ['png', 'pdf']:
        path = Path(f'exhibits/updated/{name}.{ext}')
        status = '✓' if path.exists() else '✗ MISSING'
        if not path.exists():
            all_ok = False
        print(f'  {status}  {path.name}')
print('\nAll exhibits OK' if all_ok else '\nWARNING: some exhibits missing')
