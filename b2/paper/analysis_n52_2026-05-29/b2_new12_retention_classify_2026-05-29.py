#!/usr/bin/env python3
"""B2 new-12 insider-RETENTION classification (Deliverable 1b; the re-fetch).

Classifies the unified post-exclusion top-10 survivors (EVM-5 + Solana-4) insider/not
via the cost-tiered multi-tool method, computes per-protocol insider_count_frac +
insider_balance_frac, and persists the new-12 retention vector so the retention-spec
explanatory model is reproducible BY CONSTRUCTION. DOT/TAO/ALGO retention is
low-confidence ~0 (older L1; survivors are validators/treasury-residual/unattributed
after exclusion; conservative rule -> not insider).

CLASSIFICATION RULE (matches the original sample's definition in
analysis/03_insider_classification.py line 127: insider = team, investor, founder, vest,
foundation, treasury, multisig, deployer, grant), applied to the POST-EXCLUSION SURVIVORS:
  INSIDER = team / founder / co-founder / investor (VC/fund) / "Investment Recipient" /
            foundation / treasury / attributed multisig (Safe) / vesting, surviving in the
            post-exclusion top-10.
  NOT INSIDER = CEX / exchange ("custody" hot wallets included, e.g. pump.fun Token Custody
                which Nansen flags exchange-class), market-maker (e.g. Jump Trading,
                Wintermute), bridge / escrow / staking-pool / vault aggregation / token
                proxy contract (Class 3/4 protocol infrastructure), unlabeled EOA / retail
                whale ("High Balance", "Token/ETH Millionaire", "PUMP/BONK Whale", "Yield
                Farmer").
  HHI is UNCHANGED (the PCA exclusion set stays as published; this reclassifies the LABELS
  of surviving addresses only). The big foundation/treasury/co-founder addresses already in
  the exclusion set remain excluded (they never enter the survivor top-10); separately
  re-adjudicating those (the S3 un-exclusion) is an author-owned PCA-methodology decision
  recorded in the residual-ambiguity log, NOT applied here.

LABEL SOURCES (cost-tiered; free-first then Nansen bulk; no premium-labels needed):
  - Nansen token_current_top_holders (one labeled call per token; 2026-05-29) -- primary
    entity labels (CEX, fund, Investment Recipient, protocol contracts).
  - phase4 etherscan_labels.json / nansen_labels.json (2026-05-27; FXS/SNX/GNO contract
    status + first-acquired).
  - data/processed/exclusions_log.csv + phase4 v2-audited (what is already excluded).
Conservative rule applied to every ambiguous unlabeled EOA: NOT insider (no imputation).

READ-ONLY against persisted survivor lists; writes the retention vector + provenance.
"""
import csv, json, os, math
import numpy as np, scipy.stats as ss

import os as _os_anchor
_RR = _os_anchor.path.dirname(_os_anchor.path.abspath(__file__))
while _RR != _os_anchor.path.dirname(_RR) and not _os_anchor.path.exists(_os_anchor.path.join(_RR, "reproduce.py")):
    _RR = _os_anchor.path.dirname(_RR)
A = _RR
ADIR = os.path.join(A, "b2/paper/analysis_n52_2026-05-29")
SURV = json.load(open(os.path.join(ADIR, "new12_unified_post_exclusion_top10_2026-05-29.json")))

# ---- per-address INSIDER set among the post-exclusion survivors (everything else -> NOT insider) ----
# addresses lowercased for EVM; verbatim for Solana. Per the original-methodology rule above:
# team / founder / investor / foundation / treasury / attributed-multisig / Investment-Recipient.
INSIDER = {
 # FXS: VC fund + two Frax-protocol-labeled operational/treasury EOAs (foundation/treasury)
 "0x628d3e52e46432ed7ff55efe0eaf67c9ac16aac0": "Dragonfly Capital: Fund (VC/early-investor)",
 "0x6fcfee4f14eafa723d90ad4b282757c5fe3d92ee": "Frax (protocol-team/treasury operational EOA)",
 "0xd53e50c63b0d549f142a2dcfc454501aaa5b7f3f": "Frax Finance (protocol-team/treasury operational EOA)",
 # SNX: surviving protocol treasury (treasury -> insider per the original definition)
 "0x99f4176ee457afedffcb1839c7ab7a030a5e4a92": "Synthetix: Treasury (treasury)",
 # GNO: surviving attributed multisig (co-founder Safes stay PCA-excluded under S2)
 "0x1d65d296b6ad7fdbf77d3c9cc44c9b2787f1a341": "Gnosis Multisig (multisig)",
 # WLFI: named individual investor + investment foundation + corporate treasury + attributed multisigs/Safes
 "0x5ab26169051d0d96217949adb91e86e51a5fda74": "Justin Sun (named individual strategic investor)",
 "0x0249d14d15531065b927f4930562c3814e654b54": "Aqua1 Foundation (external strategic investor)",
 "0xcd52e35f7784efc78e835ef6e00be914f48beee6": "ALT5 Sigma: Treasury Strategy (corporate strategic-investor treasury)",
 "0xf0cc01b37086bc122a3d63c615dab379478d2745": "WLFI Multisig (multisig)",
 "0x29de882559194e2be08c182c1860193f8137cbf8": "Ethena Labs WLFI Multisig (multisig)",
 "0x33ccf78a2091979fbc5a7631e6c71e900715ab78": "SafeProxy (team multisig; bare attribution, see ambiguity log)",
 "0x284cf133aa570f29da0961be897dbbb2a37962f8": "SafeProxy (team multisig; bare attribution, see ambiguity log)",
 # ENA: Ethena Labs protocol/team EOAs (foundation/team) + strategic-investment recipients
 "0xa5274a5a4b4bb3b3646475886b41bf6c50edd666": "Ethena (protocol-team EOA)",
 "0x7462f0d93260909870487f17a27c336349579557": "Ethena Labs (protocol-team EOA)",
 "0xb2af973905f05bc82bf97486b6ab883598d98298": "Ethena Labs (protocol-team EOA)",
 "0x877b3d5c681c8890d19dbf450306caa3c3d4bba6": "Ethena Labs: REZ Investment Recipient (strategic investor)",
 "0xa55457e0d0652ba47fe1f97873a62b4f9dcae4d1": "ENA Investment Recipient (strategic investor)",
 # KMNO: 3 investment-recipient survivors
 "4x3uU27N1cfmBx8JerY13ZzdNxgmgQdiZUSFZQHbhe1B": "KMNO Investment Recipient (strategic investor)",
 "6EyjmmTYdAEyoLN1eTynuGvQPRq8mR4HKrW9uBqWqi7N": "KMNO Investment Recipient (strategic investor)",
 "6AapP9rsXMsNTJEMbKUatmzLeYwkZSJWd84c6PLBJNvK": "Kamino: KMNO Investment Recipient (strategic investor)",
}

# AMBIGUOUS flags (counted per the rule above, but lower-confidence; recorded for sensitivity).
AMBIGUOUS = {
 "0x6fcfee4f14eafa723d90ad4b282757c5fe3d92ee": "FXS 'Frax' EOA (protocol-team vs operational; counted insider as foundation/treasury)",
 "0xd53e50c63b0d549f142a2dcfc454501aaa5b7f3f": "FXS 'Frax Finance' EOA (counted insider as foundation/treasury)",
 "0x33ccf78a2091979fbc5a7631e6c71e900715ab78": "WLFI bare 'SafeProxy' (multisig rule -> insider; unattributed; WLFI -> 0.5 if both bare Safes dropped)",
 "0x284cf133aa570f29da0961be897dbbb2a37962f8": "WLFI bare 'SafeProxy' (multisig rule -> insider; unattributed)",
}

# NOT-INSIDER protocol/infra survivors recorded explicitly (Nansen exchange-class / aggregation /
# proxy / market-maker). These are NOT insiders per the rule; kept here for provenance clarity.
EXCL_LEAK = {
 "0x2146aa5807d96e6b2922a149cee870f17347f1d0": "ENA Ethena Labs: Proxy (token/staking proxy contract -> not insider)",
 "0xfef30c262676de9af5e5e9ba999cf774000b14b4": "WLFI Ecosystem fund contract (protocol contract -> not insider)",
 "0xcc261ab4be137eacf57c19ed97c186b4d88004ca": "WLFI Jump Trading (market-maker -> not insider)",
 "85WTujfJ9meJq5hfjAeb5gftj7n8Q7QTsZJbRqMD5ERS": "PUMP pump.fun (Nansen exchange-class custody -> not insider)",
 "AvqFxKNrYZNvxsj2oWhLW8det68HzCXBqswshoD2TdT6": "PUMP pump.fun (exchange-class custody -> not insider)",
 "96HiV4cGWTJNCjGVff3RTHgPXmpYz7MSrGTAmxNKVWM9": "PUMP pump.fun (exchange-class custody -> not insider)",
 "ERRGqu3dh6zYBg7MNAHKL33TyVb7efMmaKxnmdukdNYa": "PUMP pump.fun (exchange-class custody -> not insider)",
 "9UcygiamY92yGntGkUkBKi4SdApxkBMZd9QSo6wMC2dN": "PUMP pump.fun (exchange-class custody -> not insider)",
 "jjCAwuuNpJCNMLAanpwgJZ6cdXzLPXe2GfD6TaDQBXt": "JTO JITO Staking Pool (Class-3 aggregation -> not insider)",
 "Ec6MuWtpvFcVyMsp7vipKCg1CMkKrWHZpWPdnJF16G57": "KMNO Kamino Staking (Class-3 aggregation -> not insider)",
 "8civ8uAA4RMY8Ho6DmJzgatAqutsRDL4hkmmCXtxZ8ew": "KMNO Custody Vaults (DeFi vault aggregation -> not insider)",
 "4uD7K6KCFfAWoeJVeDKk2V5fuRd8X4Y926cAqeoAhD8N": "KMNO Custody Vaults (DeFi vault aggregation -> not insider)",
}

def is_insider(addr):
    return addr in INSIDER or addr.lower() in INSIDER

# ---- compute per-protocol retention from the unified post-exclusion top-10 ----
rows_out = []
prov = {}
for tok, d in SURV.items():
    if tok.startswith("_"):
        continue
    top10 = d["top10"]
    n = len(top10)
    shares = [float(t.get("share_orig") or 0.0) for t in top10]
    ins_flags = [is_insider(t["address"]) for t in top10]
    insider_count = sum(ins_flags)
    icf = insider_count / n if n else 0.0
    tot_share = sum(shares)
    ins_share = sum(s for s, f in zip(shares, ins_flags) if f)
    ibf = (ins_share / tot_share) if tot_share > 0 else 0.0
    rows_out.append({"token": tok, "insider_count": insider_count, "n_top10": n,
                     "insider_count_frac": round(icf, 4), "insider_balance_frac": round(ibf, 4)})
    prov[tok] = [{"address": t["address"], "orig_rank": t.get("orig_rank"),
                  "share_orig": t.get("share_orig"),
                  "insider": is_insider(t["address"]),
                  "insider_label": INSIDER.get(t["address"]) or INSIDER.get(t["address"].lower()),
                  "flag": AMBIGUOUS.get(t["address"]) or AMBIGUOUS.get(t["address"].lower())
                          or EXCL_LEAK.get(t["address"]) or EXCL_LEAK.get(t["address"].lower())}
                 for t in top10]

# DOT/TAO/ALGO: low-confidence ~0 (survivors after exclusion are validators / treasury-
# residual / unattributed; conservative rule -> not insider).
for tok in ("DOT", "TAO", "ALGO"):
    rows_out.append({"token": tok, "insider_count": 0, "n_top10": 10,
                     "insider_count_frac": 0.0, "insider_balance_frac": 0.0})
    prov[tok] = [{"note": "low-confidence ~0; post-exclusion survivors are validators/"
                          "treasury-residual/unattributed; conservative rule -> not insider"}]

print("=== new-12 retention vector (insider_count_frac) ===")
for r in sorted(rows_out, key=lambda x: -x["insider_count_frac"]):
    print(f"  {r['token']:5} insiders={r['insider_count']}/{r['n_top10']}  "
          f"count_frac={r['insider_count_frac']:.2f}  balance_frac={r['insider_balance_frac']:.3f}")

# persist the retention vector CSV
out_csv = os.path.join(ADIR, "new12_retention_vector_2026-05-29.csv")
with open(out_csv, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["token", "insider_count", "n_top10",
                                      "insider_count_frac", "insider_balance_frac"])
    w.writeheader(); w.writerows(rows_out)
json.dump(prov, open(os.path.join(ADIR, "new12_retention_provenance_2026-05-29.json"), "w"), indent=1)
print(f"\n[written] new12_retention_vector_2026-05-29.csv ({len(rows_out)} protocols)")
print(f"[written] new12_retention_provenance_2026-05-29.json (per-address classification + flags)")

# ---- confirm the retention-spec + maturity-spec reproduce with this vector ----
C = os.path.join(A, "data/processed/regression_data_april2026.csv")
V3 = os.path.join(A, "data/processed/insider_analysis_results_v3.csv")
SEC = {'DePIN': 'DePIN', 'DeFi': 'DeFi', 'L1_L2_Infra': 'L1'}
def f(x):
    try: return float(x)
    except: return None
v3 = {r['token']: f(r.get('insider_count_frac')) for r in csv.DictReader(open(V3))
      if f(r.get('insider_count_frac')) is not None}
new12 = {r['token']: r['insider_count_frac'] for r in rows_out}

frame = []
for r in csv.DictReader(open(C)):
    if r.get('category') not in SEC: continue
    hhi = f(r['hhi']); rev = f(r.get('revenue_annual_usd')); fdv = f(r.get('fdv_usd')) or f(r.get('market_cap_usd')); mat = f(r.get('maturity_years'))
    if None in (hhi, rev, fdv, mat) or fdv <= 0: continue
    frame.append({'tok': r['token'], 'sec': SEC[r['category']], 'y': math.log(hhi),
                  'ri': math.log10(rev / fdv + 1e-7), 'mat': mat})

def ols_hc3(D, cols):
    n = len(D); y = np.array([d['y'] for d in D])
    X = np.column_stack([np.ones(n)] + [np.array([(1.0 if d['sec'] == c[1] else 0.0) if isinstance(c, tuple) else d[c] for d in D]) for c in cols])
    b, _, _, _ = np.linalg.lstsq(X, y, rcond=None); e = y - X @ b; k = X.shape[1]
    XtXi = np.linalg.inv(X.T @ X); h = np.diag(X @ XtXi @ X.T)
    cov = XtXi @ (X.T @ np.diag((e ** 2) / ((1 - h) ** 2)) @ X) @ XtXi; se = np.sqrt(np.diag(cov)); t = b / se
    p = [2 * (1 - ss.t.cdf(abs(tt), n - k)) for tt in t]
    return b, se, p

bm, _, pm = ols_hc3(frame, [('sec', 'DePIN'), ('sec', 'L1'), 'ri', 'mat'])
print(f"\n[maturity-spec N={len(frame)}] DePIN b={bm[1]:+.4f} p={pm[1]:.4f} | revint p={pm[3]:.4f} | maturity p={pm[4]:.4f}")

Dr = []
for d in frame:
    ret = v3.get(d['tok'], new12.get(d['tok']))
    if ret is None: continue
    dd = dict(d); dd['ret'] = ret; Dr.append(dd)
br, _, pr = ols_hc3(Dr, [('sec', 'DePIN'), ('sec', 'L1'), 'ri', 'ret'])
secs = {s: sum(1 for d in Dr if d['sec'] == s) for s in ('DePIN', 'DeFi', 'L1')}
print(f"[retention-spec N={len(Dr)}] sectors={secs}")
print(f"   DePIN b={br[1]:+.4f} p={pr[1]:.4f}{'*' if pr[1] < 0.05 else ''} | L1 p={pr[2]:.4f} | "
      f"revint p={pr[3]:.4f} | RETENTION b={br[4]:+.4f} p={pr[4]:.4f}{'*' if pr[4] < 0.05 else ''}")
print(f"   obs/predictor = {len(Dr)/4:.1f}")
