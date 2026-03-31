"""
Generate Figure 3: Horizontal bar chart of governance HHI by protocol.
Sorted by category, then HHI ascending within category.
Dashed vertical lines for category means.
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

matplotlib.use('Agg')

INPUT_CSV = "governance_concentration_april2026.csv"
OUTPUT_PNG = "figure3_governance_hhi_34protocol.png"

# Category display names and colors
CATEGORY_COLORS = {
    'DePIN': '#2196F3',
    'DeFi': '#4CAF50',
    'L1_L2_Infra': '#FF9800',
    'Social_Dead': '#9E9E9E',
}

CATEGORY_LABELS = {
    'DePIN': 'DePIN',
    'DeFi': 'DeFi',
    'L1_L2_Infra': 'L1/L2 Infra',
    'Social_Dead': 'Social/Dead',
}


def generate_figure3():
    df = pd.read_csv(INPUT_CSV)

    # Exclude LDO_raw if present; keep only active protocols
    df = df[~df['token'].str.contains('_raw', na=False)]

    # Sort: category order, then HHI ascending within category
    cat_order = ['DePIN', 'DeFi', 'L1_L2_Infra', 'Social_Dead']
    df['cat_sort'] = df['category'].map({c: i for i, c in enumerate(cat_order)})
    df = df.sort_values(['cat_sort', 'hhi'], ascending=[True, True]).reset_index(drop=True)

    n = len(df)
    print(f"Plotting {n} protocols")

    fig, ax = plt.subplots(figsize=(10, max(8, n * 0.32)))

    y_pos = np.arange(n)
    colors = [CATEGORY_COLORS.get(cat, '#666') for cat in df['category']]

    bars = ax.barh(y_pos, df['hhi'], color=colors, edgecolor='white', linewidth=0.5, height=0.7)

    # Protocol labels on y-axis
    labels = []
    for _, row in df.iterrows():
        label = row['protocol']
        if row['token'] == 'META':
            label += ' †'  # futarchy marker
        labels.append(label)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=8)

    # Category mean vertical lines
    for cat in cat_order:
        cat_data = df[df['category'] == cat]['hhi']
        if len(cat_data) > 0:
            mean_hhi = cat_data.mean()
            ax.axvline(x=mean_hhi, color=CATEGORY_COLORS[cat], linestyle='--',
                       alpha=0.7, linewidth=1.5,
                       label=f'{CATEGORY_LABELS[cat]} mean = {mean_hhi:.3f}')

    # Category group separators
    prev_cat = None
    for i, (_, row) in enumerate(df.iterrows()):
        if prev_cat is not None and row['category'] != prev_cat:
            ax.axhline(y=i - 0.5, color='#ccc', linewidth=0.5, linestyle='-')
        prev_cat = row['category']

    ax.set_xlabel('Herfindahl-Hirschman Index (HHI)', fontsize=11)
    ax.set_title('Governance Token Concentration by Protocol', fontsize=13, fontweight='bold')
    ax.set_xlim(0, max(df['hhi']) * 1.15)

    # Add HHI value labels on bars
    for i, (_, row) in enumerate(df.iterrows()):
        ax.text(row['hhi'] + 0.003, i, f"{row['hhi']:.3f}", va='center', fontsize=7, color='#333')

    ax.legend(loc='lower right', fontsize=8, framealpha=0.9)
    ax.invert_yaxis()

    plt.tight_layout()
    plt.savefig(OUTPUT_PNG, dpi=300, bbox_inches='tight')
    print(f"Saved {OUTPUT_PNG}")
    plt.close()


if __name__ == "__main__":
    generate_figure3()
