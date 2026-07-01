"""B2 Romano-Wolf stepdown, sector-member variant B: balanced Mann-Whitney.

Companion to romano_wolf_stepdown.py (variant A). Variant A uses the omnibus
three-class Kruskal-Wallis sector test (H = 10.09, N = 50). This variant B swaps
the sector member for the paper's HEADLINE balanced DePIN-versus-DeFi Mann-Whitney
on the voter-inclusive staking pass-through HHI (Cohen's d = 0.65, Mann-Whitney
p = 0.028, N = 15 DePIN / 15 DeFi), so the family-wise correction can be reported
against the same sector statistic the main text headlines.

The other three members (allocation, insider retention, subsidy) are identical to
variant A and reuse the same frames. The coordinated protocol-key permutation null
(B = 20,000, shared across members, seed 2026) is unchanged in form; only the
sector member's sample (the balanced 30) and statistic (Mann-Whitney U, two-sided
extremity |U - n1 n2 / 2|) differ. The reusable Romano-Wolf core is imported from
variant A so the two variants cannot drift.

Run from exhibits/:  python3 romano_wolf_stepdown_sector_mw.py
Writes romano_wolf_results_sector_mw.json.
"""
import pandas as pd, numpy as np, math, json, warnings
from scipy import stats as ss
from pathlib import Path
from romano_wolf_stepdown import (rw_stepdown, holm, bonferroni, right_tail_p,
                                  minp_stepdown, corr_p, pearson_stat, spearman_stat)
warnings.filterwarnings("ignore")

SEED = 2026
B = 20000
HERE = Path(__file__).resolve().parent
PRICE = HERE / "price_performance_audit" / "b2_price_performance_dataset.csv"
V3 = HERE / "romano_wolf_frames" / "insider_analysis_results_v3.csv"
VEC = HERE.parent / "b2" / "paper" / "analysis_n52_2026-05-29" / "sector_contrast_hhi_vectors_2026-06-02.csv"
SECTOR_BIN = {"DePIN", "DeFi"}
SECTORS = {"DeFi", "DePIN", "L1_L2_Infra"}  # 3-class governance cross-section for the allocation battery (social excluded)


def cohens_d(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    n1, n2 = len(a), len(b)
    sp = math.sqrt(((n1 - 1) * np.var(a, ddof=1) + (n2 - 1) * np.var(b, ddof=1)) / (n1 + n2 - 2))
    return float((a.mean() - b.mean()) / sp)


def mw_U(hhi, cov):
    a = hhi[cov == 'DePIN']; b = hhi[cov == 'DeFi']
    U, p = ss.mannwhitneyu(a, b, alternative='two-sided')
    return float(U), float(p), int(len(a)), int(len(b))


def mw_extremity(U, n1, n2):
    return abs(U - n1 * n2 / 2.0)


# ===================== build master frame (variant A frame + balanced-30 pass-through) =====================
def build_master():
    price = pd.read_csv(PRICE)
    v3 = pd.read_csv(V3)
    vec = pd.read_csv(VEC)

    def subval(row):
        tt = row.get('subsidy_ratio'); oc = row.get('subsidy_ratio_onchain')
        if pd.notna(tt) and tt != 0: return tt
        if pd.notna(oc) and oc != 0: return oc
        return np.nan
    price['_sub'] = price.apply(subval, axis=1)
    price['token'] = price['token'].astype(str).str.upper()
    v3['token'] = v3['token'].astype(str).str.upper()
    vec['token'] = vec['token'].astype(str).str.upper()
    m = price[['token', 'protocol', 'hhi', 'category', 'insider_pct', '_sub']].merge(
        v3[['token', 'full_hhi', 'insider_count_frac']], on='token', how='outer')
    m = m.merge(vec[['token', 'sector', 'hhi_passthrough']].rename(columns={'sector': 'sector_bin'}),
                on='token', how='left')
    return m


# member spec: (name, conc_col, cov_col, kind) -- sector swapped to balanced Mann-Whitney
MEMBERS = [
    ('allocation', 'hhi', 'insider_pct', 'pearson'),
    ('retention', 'full_hhi', 'insider_count_frac', 'spearman'),
    ('subsidy', 'hhi', '_sub', 'pearson'),
    ('sector', 'hhi_passthrough', 'sector_bin', 'mw'),
]


def subsample(master, conc, cov, kind):
    if kind == 'mw':
        s = master[master[conc].notna() & master[cov].isin(SECTOR_BIN)]
    elif cov == 'insider_pct':
        # Allocation battery: the DePIN/DeFi/infrastructure cross-section with insider
        # allocation data (social tokens excluded), matching the manuscript of-record
        # allocation null (N = 50, Pearson r = 0.09). Without this filter the dead social
        # token GTC (Gitcoin) leaks in, giving N = 51 and r = 0.087.
        s = master[master[conc].notna() & master[cov].notna() & master['category'].isin(SECTORS)]
    else:
        s = master[master[conc].notna() & master[cov].notna()]
    return s.reset_index(drop=True)


def observed_stat(s, conc, cov, kind):
    if kind == 'pearson':
        st = pearson_stat(s[conc].values, s[cov].values); return st, corr_p(st, len(s)), len(s)
    if kind == 'spearman':
        st = spearman_stat(s[conc].values, s[cov].values); return st, corr_p(st, len(s)), len(s)
    if kind == 'mw':
        U, p, n1, n2 = mw_U(s[conc].values, s[cov].astype(str).values)
        return U, p, n1 + n2


def perm_stat(s, conc, cov, kind, order):
    c = s[conc].values
    if kind == 'pearson': return pearson_stat(c, s[cov].values[order])
    if kind == 'spearman': return spearman_stat(c, s[cov].values[order])
    if kind == 'mw':
        U, _, n1, n2 = mw_U(c, s[cov].astype(str).values[order])
        return mw_extremity(U, n1, n2)


def obs_extremity(st, s, cov, kind):
    if kind in ('pearson', 'spearman'):
        return abs(st)
    if kind == 'mw':
        c = s[cov].astype(str).values
        n1 = int((c == 'DePIN').sum()); n2 = int((c == 'DeFi').sum())
        return mw_extremity(st, n1, n2)
    return st  # kw (unused in variant B)


def draw_extremity(ps, kind):
    return abs(ps) if kind in ('pearson', 'spearman') else ps  # perm_stat returns extremity for mw


def main():
    rng = np.random.default_rng(SEED)
    master = build_master()
    subs = {nm: subsample(master, c, cv, k) for (nm, c, cv, k) in MEMBERS}
    names = [m[0] for m in MEMBERS]

    obs = {}
    obs_ext = np.zeros(len(MEMBERS))
    for j, (nm, c, cv, k) in enumerate(MEMBERS):
        st, p, n = observed_stat(subs[nm], c, cv, k)
        obs[nm] = {'stat': round(st, 4), 'p_asymptotic': round(p, 4), 'n': int(n)}
        obs_ext[j] = obs_extremity(st, subs[nm], cv, k)
    # sector reporting extras (Cohen's d, U, n1/n2)
    sec = subs['sector']
    sd = cohens_d(sec.loc[sec['sector_bin'] == 'DePIN', 'hhi_passthrough'].values,
                  sec.loc[sec['sector_bin'] == 'DeFi', 'hhi_passthrough'].values)
    obs['sector']['cohens_d'] = round(sd, 4)
    obs['sector']['n1_depin'] = int((sec['sector_bin'] == 'DePIN').sum())
    obs['sector']['n2_defi'] = int((sec['sector_bin'] == 'DeFi').sum())
    obs['sector']['statistic'] = 'mann_whitney_U_passthrough'

    draws_stat = np.zeros((B, len(MEMBERS)))
    tok_index = {t: i for i, t in enumerate(master['token'].values)}
    sub_tokidx = {nm: np.array([tok_index[t] for t in subs[nm]['token'].values]) for nm in names}
    for b in range(B):
        u = rng.random(len(master))
        for j, (nm, c, cv, k) in enumerate(MEMBERS):
            order = np.argsort(u[sub_tokidx[nm]])
            draws_stat[b, j] = draw_extremity(perm_stat(subs[nm], c, cv, k, order), k)

    p_obs = np.array([right_tail_p(draws_stat[:, j], np.array([obs_ext[j]]))[0] for j in range(len(names))])
    q = np.column_stack([right_tail_p(draws_stat[:, j], draws_stat[:, j]) for j in range(len(names))])

    rw = minp_stepdown(p_obs, q)
    bonf = bonferroni(p_obs); hlm = holm(p_obs)

    out = {'meta': {'B': B, 'seed': SEED, 'm_family': len(MEMBERS),
                    'variant': 'B (sector = balanced DePIN-vs-DeFi Mann-Whitney on pass-through HHI, N=15/15)',
                    'permutation': 'coordinated protocol-key u, shared across members',
                    'step_down': 'Westfall-Young minP (each member calibrated vs own permutation null)'},
           'members': {}}
    for j, nm in enumerate(names):
        out['members'][nm] = {
            **obs[nm], 'p_perm_calibrated': round(float(p_obs[j]), 4),
            'p_bonferroni': round(float(bonf[j]), 4), 'p_holm': round(float(hlm[j]), 4),
            'p_romano_wolf_minP': round(float(rw[j]), 4),
            'survives_fwer_0.05': bool(rw[j] < 0.05)}

    g = {
        'retention_rho_0.44_N39': abs(obs['retention']['stat'] - 0.4414) < 0.01 and obs['retention']['n'] == 39,
        'sector_d_0.65_N30': abs(obs['sector']['cohens_d'] - 0.65) < 0.02 and obs['sector']['n'] == 30,
        'sector_mw_p_0.028': abs(obs['sector']['p_asymptotic'] - 0.028) < 0.003,
        'subsidy_r_0.62_N23': abs(obs['subsidy']['stat'] - 0.62) < 0.01 and obs['subsidy']['n'] == 23,
        'allocation_r_0.09_N50': abs(obs['allocation']['stat'] - 0.09) < 0.02 and obs['allocation']['n'] == 50,
    }
    g['sandwich_perm_le_rw'] = bool(np.all(p_obs <= rw + 1e-9))
    g['rw_le_holm'] = bool(np.all(rw <= hlm + 1e-9))
    g['rw_le_bonferroni'] = bool(np.all(rw <= bonf + 1e-9))
    g['rw_monotone'] = bool(np.all(np.diff(rw[np.argsort(p_obs)]) >= -1e-12))
    g['ALL_PASS'] = all(g.values())
    out['acceptance_gate'] = g

    discoveries = ['retention', 'subsidy', 'sector']
    flips = [d for d in discoveries if obs[d]['p_asymptotic'] < 0.05 <= out['members'][d]['p_romano_wolf_minP']]
    out['halt2'] = {'discoveries_that_flip_to_nonsig_under_RW': flips, 'triggered': bool(flips)}

    print(json.dumps(out, indent=1, default=str))
    json.dump(out, open(HERE / "romano_wolf_results_sector_mw.json", "w"), indent=1, default=str)
    print("\nromano_wolf_results_sector_mw.json written; ALL_PASS =", g['ALL_PASS'],
          "; HALT-2 triggered =", out['halt2']['triggered'])


if __name__ == "__main__":
    main()
