#!/usr/bin/env python3
"""
A2 staking-attribution HHI recompute (2026-05-30).

Ratified A2: attribute insider-staked tokens (stkAAVE / sENA) back to the underlying
insider holders, excluding only the dispersed-retail "contract shell". Quantifies what
the wholesale staking-contract PCA exclusion HIDES.

KEY EMPIRICAL FINDING: at the ADDRESS level, attribution moves the holding-HHI by < 1%
and DOWNWARD (dilution: adding several separate insider holders grows the denominator
faster than it concentrates). A2's contribution is therefore the insider SHARE/visibility
finding (4.4-6.3% of AAVE supply is insider AAVE invisible under wholesale stkAAVE
exclusion; ~0.43% for ENA), NOT a material holding-HHI change. This is consistent with the
paper's existing argument that the holding-HHI understates effective concentration (which
surfaces in insider share + delegated voting power, not the address-level holding-HHI).

READS ONLY raw holder lists + exclusion logs + directive2 staker shares. Mutates nothing.
Writes a_2 recompute JSON alongside.
"""
import csv, os, json

HERE = os.path.dirname(os.path.abspath(__file__))
import os as _os_anchor
_RR = _os_anchor.path.dirname(_os_anchor.path.abspath(__file__))
while _RR != _os_anchor.path.dirname(_RR) and not _os_anchor.path.exists(_os_anchor.path.join(_RR, "reproduce.py")):
    _RR = _os_anchor.path.dirname(_RR)
A = _RR
HLD = [os.path.join(A, "data/raw/holder_lists"), "/Users/zach/b2-governance-data/data/raw/holder_lists"]


def load(tok):
    for d in HLD:
        p = os.path.join(d, f"{tok}_holders.csv")
        if os.path.exists(p):
            return list(csv.DictReader(open(p)))
    return None


def dist(bals):
    bals = sorted(bals, reverse=True)
    t = sum(bals)
    sh = [b / t for b in bals]
    return {"hhi": round(sum(s * s for s in sh), 6), "top1": round(100 * sh[0], 2),
            "top5": round(100 * sum(sh[:5]), 2), "top10": round(100 * sum(sh[:10]), 2),
            "n": len(bals), "total": round(t, 1)}


def excl_log(tok):
    return {r["address"].strip().lower() for r in csv.DictReader(open(os.path.join(A, "data/processed/exclusions_log.csv"))) if r["token"].upper() == tok}


def excl_new12(tok):
    p = os.path.join(A, "b2/paper/analysis_n52_2026-05-29/new12_unified_exclusions_2026-05-29.csv")
    return {r["address"].strip().lower() for r in csv.DictReader(open(p)) if r["token"].upper() == tok}


out = {"method": "attribute insider staked-token share back as holders; keep retail shell excluded",
       "finding": "address-level holding-HHI effect is < 1% and dilutive (downward); the substantive A2 output is the insider-share visibility finding, not an HHI change"}

# ---- AAVE: stkAAVE contract 0x4da27a... fully excluded; attribute clear insider portion ----
rows = load("AAVE")
ex = excl_log("AAVE")
stk_bal = next(float(r["balance"]) for r in rows if r["address"].strip().lower() == "0x4da27a545c0c5b758a6ba100e3a049001de870f5")
surv = {r["address"].strip().lower(): float(r["balance"]) for r in rows if r["address"].strip().lower() not in ex}
stani = "0xe705b1d26b85c9f9f91a3690079d336295f14f08"  # Aave founder, already a direct AAVE holder
clear = {"aave_multisig_3e312e": 10.72, "aave_multisig_144f28": 5.08, "aave_multisig_507b3f": 2.72, "stani_founder": 1.94}
ambig = {"safeproxy_54a1be": 8.56, "multisig_0efccb": 1.76}

base = dist(list(surv.values()))
pool = dict(surv)
pool[stani] = pool.get(stani, 0.0) + clear["stani_founder"] / 100 * stk_bal
for k in ("aave_multisig_3e312e", "aave_multisig_144f28", "aave_multisig_507b3f"):
    pool[f"__{k}__"] = clear[k] / 100 * stk_bal
clr = dist(list(pool.values()))
pool_amb = dict(pool)
for k, p in ambig.items():
    pool_amb[f"__{k}__"] = p / 100 * stk_bal
amb = dist(list(pool_amb.values()))
out["AAVE"] = {
    "stkAAVE_contract_AAVE": round(stk_bal, 1),
    "insider_AAVE_clear_pct_of_supply": 4.43, "insider_AAVE_with_ambiguous_pct_of_supply": 6.29,
    "clear_insider_share_of_stkAAVE_pct": 20.46,
    "baseline": base, "attributed_clear": clr, "attributed_with_ambiguous": amb,
    "hhi_delta_clear": round(clr["hhi"] - base["hhi"], 6),
    "note": "frame holding-HHI left at the baseline 0.012790 (the clear-attribution recompute 0.012744 is a -0.4% dilutive move, immaterial and below manuscript display precision); A2 reported as insider-visibility methodology"}

# ---- ENA: sENA contract 0x8be3460a... excluded (new12_unified); attribute insider sENA ----
rows = load("ENA")
ex = excl_new12("ENA")
sena_bal = next(float(r["balance"]) for r in rows if r["address"].strip().lower() == "0x8be3460a480c80728a8c4d7a5d5303c85ba7b3b9")
surv = {r["address"].strip().lower(): float(r["balance"]) for r in rows if r["address"].strip().lower() not in ex}
ena_ins = {"ethena_labs": 2.71, "kain_warwick_founder": 2.01, "strobe_ventures": 1.15}
base = dist(list(surv.values()))
pool = dict(surv)
for k, p in ena_ins.items():
    pool[f"__{k}__"] = p / 100 * sena_bal
att = dist(list(pool.values()))
out["ENA"] = {
    "sENA_contract_ENA": round(sena_bal, 1), "insider_ENA_pct_of_supply": 0.43,
    "clear_insider_share_of_sENA_pct": 5.87, "baseline": base, "attributed": att,
    "hhi_delta": round(att["hhi"] - base["hhi"], 6),
    "note": "immaterial (0.43% of supply); frame holding-HHI left at 0.047164 (ENA is in the reproduce.py NEW_COHORT recompute; partial attribution does not fit the address-exclusion model and the effect is below display precision); reported as a consistency methodology note"}

json.dump(out, open(os.path.join(HERE, "a2_attribution_hhi_recompute_2026-05-30.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
