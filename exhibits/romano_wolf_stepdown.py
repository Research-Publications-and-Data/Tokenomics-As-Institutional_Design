"""B2 Romano-Wolf stepdown over the bivariate battery.

A step-down Romano-Wolf family-wise correction with a reusable permutation core.

Applies a family-wise correction across the four battery tests the paper reports, under a
single coordinated protocol-permutation null that preserves cross-test dependence:

  allocation : Pearson(insider_pct, hhi)                  [of-record null, r approx 0.09, N approx 50]
  retention  : Spearman(insider_count_frac, full_hhi)     [of-record rho 0.44, p 0.005, N 39]
  subsidy    : Pearson(subsidy, hhi)                      [of-record r 0.62, p 0.002, N 23, LPT-driven]
  sector     : Kruskal-Wallis(hhi by 3-class category)    [of-record H 10.09, p 0.0064, N 50]

Heterogeneous frames: retention uses the v3 frame's own
`full_hhi` (exhibits/romano_wolf_frames/insider_analysis_results_v3.csv); the other
three use the price-dataset `hhi`. A single per-draw protocol key u, shared across
members, coordinates the permutation so a protocol moves consistently in every test.

Step-down form: the p-value-based (Westfall-Young minP) realization of Romano-Wolf. Each
member is calibrated against its OWN permutation null (a right-tail rank), so heterogeneous
statistics (Pearson, Spearman, Kruskal-Wallis) and heavy-tailed small-N members (the
Livepeer-driven subsidy test) are handled on a common [0,1] scale. A max-t studentized form
was rejected because the subsidy member's asymptotic |z| (3.16) inverts its permutation
significance (perm p 0.017): asymptotic studentization mis-calibrates an outlier-driven null.

Run from exhibits/:  python3 romano_wolf_stepdown.py
"""
import pandas as pd, numpy as np, math, json, warnings
from scipy import stats as ss
from pathlib import Path
warnings.filterwarnings("ignore")

SEED = 2026
HERE = Path(__file__).resolve().parent
PRICE = HERE / "price_performance_audit" / "b2_price_performance_dataset.csv"
V3 = HERE / "romano_wolf_frames" / "insider_analysis_results_v3.csv"
B = 20000
SECTORS = {"DeFi", "DePIN", "L1_L2_Infra"}


# ===================== reusable Romano-Wolf step-down core =====================
def rw_stepdown(obs_abs, draws_abs, plus_one=True):
    obs_abs = np.asarray(obs_abs, float); draws_abs = np.asarray(draws_abs, float)
    n, m = draws_abs.shape
    order = np.argsort(-obs_abs); padj = np.empty(m); prev = 0.0
    for k in range(m):
        active = order[k:]
        maxstat = draws_abs[:, active].max(axis=1)
        j = order[k]; count = int((maxstat >= obs_abs[j]).sum())
        p = (1 + count) / (1 + n) if plus_one else count / n
        p = max(p, prev); padj[j] = p; prev = p
    return padj


def bonferroni(praw):
    praw = np.asarray(praw, float); return np.minimum(1.0, praw * len(praw))


def holm(praw):
    praw = np.asarray(praw, float); m = len(praw)
    order = np.argsort(praw); padj = np.empty(m); prev = 0.0
    for k, j in enumerate(order):
        p = min(1.0, (m - k) * praw[j]); p = max(p, prev); padj[j] = p; prev = p
    return padj


# ===================== statistics + minP step-down =====================
def corr_p(stat, n):
    """asymptotic two-sided p for a correlation (reporting only; not the calibration basis)."""
    if n <= 3 or abs(stat) >= 1.0:
        return 0.0 if abs(stat) >= 1.0 else 1.0
    t = stat * math.sqrt((n - 2) / (1 - stat ** 2))
    return float(2 * ss.t.sf(abs(t), n - 2))


def pearson_stat(x, y): return float(ss.pearsonr(x, y)[0])
def spearman_stat(x, y): return float(ss.spearmanr(x, y)[0])


def kw_HP(hhi, cats):
    groups = [hhi[cats == c] for c in np.unique(cats)]
    H, p = ss.kruskal(*groups)
    return float(H), float(p)


def right_tail_p(col, values):
    """Permutation right-tail p of each value against the null sample `col`:
    (1 + #{col >= v}) / (1 + len(col)). Vectorized via searchsorted."""
    sc = np.sort(col); n = len(col)
    ge = n - np.searchsorted(sc, values, side='left')
    return (1 + ge) / (1 + n)


def minp_stepdown(p_obs, q):
    """Westfall-Young minP step-down (the p-value form of Romano-Wolf).
    p_obs : (m,) observed per-member permutation p (calibrated against own null).
    q     : (B, m) per-draw permutation p of each member's resampled statistic.
    Returns (m,) adjusted p, monotone in observed significance, FWER-controlled under
    the dependence captured by the shared permutation."""
    p_obs = np.asarray(p_obs, float); q = np.asarray(q, float)
    B, m = q.shape
    order = np.argsort(p_obs); adj = np.empty(m); prev = 0.0
    for k in range(m):
        active = order[k:]
        minq = q[:, active].min(axis=1)
        j = order[k]; cnt = int((minq <= p_obs[j]).sum())
        p = (1 + cnt) / (1 + B); p = max(p, prev); adj[j] = p; prev = p
    return adj


def extremity(stat, kind):
    """larger = more extreme: |corr| for correlations, H for Kruskal-Wallis."""
    return abs(stat) if kind in ('pearson', 'spearman') else stat


# ===================== build master frame =====================
def build_master():
    price = pd.read_csv(PRICE)
    v3 = pd.read_csv(V3)

    def subval(row):
        tt = row.get('subsidy_ratio'); oc = row.get('subsidy_ratio_onchain')
        if pd.notna(tt) and tt != 0: return tt
        if pd.notna(oc) and oc != 0: return oc
        return np.nan
    price['_sub'] = price.apply(subval, axis=1)
    price['token'] = price['token'].astype(str).str.upper()
    v3['token'] = v3['token'].astype(str).str.upper()
    m = price[['token', 'protocol', 'hhi', 'category', 'insider_pct', '_sub']].merge(
        v3[['token', 'full_hhi', 'insider_count_frac']], on='token', how='outer')
    return m


# member spec: (name, conc_col, cov_col, kind)
MEMBERS = [
    ('allocation', 'hhi', 'insider_pct', 'pearson'),
    ('retention', 'full_hhi', 'insider_count_frac', 'spearman'),
    ('subsidy', 'hhi', '_sub', 'pearson'),
    ('sector', 'hhi', 'category', 'kw'),
]


def subsample(master, conc, cov, kind):
    if kind == 'kw':
        s = master[master[conc].notna() & master[cov].isin(SECTORS) & (master[conc] > 0)]
    elif cov == 'insider_pct':
        # Allocation battery: the DePIN/DeFi/infrastructure cross-section with insider
        # allocation data (social tokens excluded), matching the manuscript of-record
        # allocation null (N = 50, Pearson r = 0.09) and the sector member's own SECTORS
        # restriction. Without this filter the dead social token GTC (Gitcoin) leaks in,
        # giving N = 51 and r = 0.087, a reviewer-facing drift from the manuscript.
        s = master[master[conc].notna() & master[cov].notna() & master['category'].isin(SECTORS)]
    else:
        s = master[master[conc].notna() & master[cov].notna()]
    return s.reset_index(drop=True)


def observed_stat(s, conc, cov, kind):
    if kind == 'pearson':
        st = pearson_stat(s[conc].values, s[cov].values); return st, corr_p(st, len(s)), len(s)
    if kind == 'spearman':
        st = spearman_stat(s[conc].values, s[cov].values); return st, corr_p(st, len(s)), len(s)
    if kind == 'kw':
        H, p = kw_HP(s[conc].values, s[cov].astype(str).values); return H, p, len(s)


def perm_stat(s, conc, cov, kind, order):
    c = s[conc].values
    if kind == 'pearson': return pearson_stat(c, s[cov].values[order])
    if kind == 'spearman': return spearman_stat(c, s[cov].values[order])
    if kind == 'kw':
        H, _ = kw_HP(c, s[cov].astype(str).values[order]); return H


# ===================== main =====================
def main():
    rng = np.random.default_rng(SEED)
    master = build_master()
    subs = {nm: subsample(master, c, cv, k) for (nm, c, cv, k) in MEMBERS}

    names = [m[0] for m in MEMBERS]

    # observed statistics + extremity scalar (|corr| or H) + asymptotic p (reporting only)
    obs = {}
    obs_ext = np.zeros(len(MEMBERS))
    for j, (nm, c, cv, k) in enumerate(MEMBERS):
        st, p, n = observed_stat(subs[nm], c, cv, k)
        obs[nm] = {'stat': round(st, 4), 'p_asymptotic': round(p, 4), 'n': int(n)}
        obs_ext[j] = extremity(st, k)

    # coordinated permutation null -> store the extremity scalar per member
    draws_stat = np.zeros((B, len(MEMBERS)))
    tok_index = {t: i for i, t in enumerate(master['token'].values)}
    sub_tokidx = {nm: np.array([tok_index[t] for t in subs[nm]['token'].values]) for nm in names}
    for b in range(B):
        u = rng.random(len(master))
        for j, (nm, c, cv, k) in enumerate(MEMBERS):
            order = np.argsort(u[sub_tokidx[nm]])
            draws_stat[b, j] = extremity(perm_stat(subs[nm], c, cv, k, order), k)

    # calibrate each member against its OWN permutation null (scale-free right-tail p)
    p_obs = np.array([right_tail_p(draws_stat[:, j], np.array([obs_ext[j]]))[0] for j in range(len(names))])
    q = np.column_stack([right_tail_p(draws_stat[:, j], draws_stat[:, j]) for j in range(len(names))])

    rw = minp_stepdown(p_obs, q)
    bonf = bonferroni(p_obs); hlm = holm(p_obs)

    out = {'meta': {'B': B, 'seed': SEED, 'm_family': len(MEMBERS),
                    'permutation': 'coordinated protocol-key u, shared across members',
                    'step_down': 'Westfall-Young minP (each member calibrated vs own permutation null)'},
           'members': {}}
    for j, nm in enumerate(names):
        out['members'][nm] = {
            **obs[nm], 'p_perm_calibrated': round(float(p_obs[j]), 4),
            'p_bonferroni': round(float(bonf[j]), 4), 'p_holm': round(float(hlm[j]), 4),
            'p_romano_wolf_minP': round(float(rw[j]), 4),
            'survives_fwer_0.05': bool(rw[j] < 0.05)}

    # ---- anchor reproduction gate ----
    g = {
        'retention_rho_0.44_N39': abs(obs['retention']['stat'] - 0.4414) < 0.01 and obs['retention']['n'] == 39,
        'sector_H_10.09_N50': abs(obs['sector']['stat'] - 10.09) < 0.1 and obs['sector']['n'] == 50,
        'subsidy_r_0.62_N23': abs(obs['subsidy']['stat'] - 0.62) < 0.01 and obs['subsidy']['n'] == 23,
        'allocation_r_0.09_N50': abs(obs['allocation']['stat'] - 0.09) < 0.02 and obs['allocation']['n'] == 50,
    }
    # ---- minP sandwich: p_obs <= RW <= Holm(p_obs) <= Bonferroni(p_obs); RW monotone ----
    g['sandwich_perm_le_rw'] = bool(np.all(p_obs <= rw + 1e-9))
    g['rw_le_holm'] = bool(np.all(rw <= hlm + 1e-9))
    g['rw_le_bonferroni'] = bool(np.all(rw <= bonf + 1e-9))
    g['rw_monotone'] = bool(np.all(np.diff(rw[np.argsort(p_obs)]) >= -1e-12))
    g['ALL_PASS'] = all(g.values())
    out['acceptance_gate'] = g

    # ---- HALT-2 watch: did any discovery cross 0.05 under correction? ----
    discoveries = ['retention', 'subsidy', 'sector']
    flips = [d for d in discoveries if obs[d]['p_asymptotic'] < 0.05 <= out['members'][d]['p_romano_wolf_minP']]
    out['halt2'] = {'discoveries_that_flip_to_nonsig_under_RW': flips,
                    'triggered': bool(flips)}

    print(json.dumps(out, indent=1, default=str))
    json.dump(out, open(HERE / "romano_wolf_results.json", "w"), indent=1, default=str)
    print("\nromano_wolf_results.json written; ALL_PASS =", g['ALL_PASS'],
          "; HALT-2 triggered =", out['halt2']['triggered'])


if __name__ == "__main__":
    main()
