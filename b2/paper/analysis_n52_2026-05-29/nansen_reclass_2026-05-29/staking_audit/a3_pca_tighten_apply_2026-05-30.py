#!/usr/bin/env python3
"""
A3 PCA-strict tighten APPLY (2026-05-30; ratified, conditional-on-anchor, anchor PASSED).

Excludes the surviving protocol-controlled Class-2/3 addresses (team/foundation multisigs,
protocol contracts, staking pools, custody vaults, proxies, plus the Jump market-maker
deposit) from the holder-HHI of the 5 new-cohort DeFi protocols whose post-exclusion top-10
still carried them. The excluded addresses leave BOTH the HHI and the insider-retention count.

Tighten principle: exclude protocol-controlled Class-2/3 (and MM custody). KEEP genuine
external concentrated holders (VCs / named individuals / corporate-treasury strategic
investors like ALT5 Sigma / Investment Recipients). This is the conservative, consistent
reading (ENA/PUMP/KMNO reproduce the prior RESOLUTION targets 0.045/0.032/0.027 under it).
WLFI sensitivity: keeping ALT5 (a public-company corporate-treasury strategic investor, not a
protocol-controlled address) gives 0.0812; additionally excluding ALT5 would give ~0.066 (the
RESOLUTION estimate). 0.0812 is the conservative choice (higher DeFi HHI, smaller DePIN-DeFi
gap); the headline strengthens either way (maturity-spec DePIN anchor 0.0435 -> 0.0197).

Mutates: data/processed/regression_data_april2026.csv (5 rows: hhi+top1+top5+top10);
b2/paper/analysis_n52_2026-05-29/new12_unified_exclusions_2026-05-29.csv (append tighten rows);
b2/paper/analysis_n52_2026-05-29/new12_retention_vector_2026-05-29.csv (5 rows re-derived).
Writes backups (.pre_a3_tighten). Idempotent guard: refuses to re-append if tighten rows present.
"""
import csv, io, os, json

import os as _os_anchor
_RR = _os_anchor.path.dirname(_os_anchor.path.abspath(__file__))
while _RR != _os_anchor.path.dirname(_RR) and not _os_anchor.path.exists(_os_anchor.path.join(_RR, "reproduce.py")):
    _RR = _os_anchor.path.dirname(_RR)
A = _RR
ADIR = os.path.join(A, "b2/paper/analysis_n52_2026-05-29")
HLD = [os.path.join(A, "data/raw/holder_lists"), "/Users/zach/b2-governance-data/data/raw/holder_lists"]
FRAME = os.path.join(A, "data/processed/regression_data_april2026.csv")
EXCL = os.path.join(ADIR, "new12_unified_exclusions_2026-05-29.csv")
RETV = os.path.join(ADIR, "new12_retention_vector_2026-05-29.csv")

# protocol-controlled Class-2/3 tighten set (pca_class 2 = team/foundation multisig;
# 3 = protocol infra contract/staking/vault/proxy; 5 = MM-deposit custody)
TIGHTEN = {
 "WLFI": [("0xfef30c262676de9af5e5e9ba999cf774000b14b4", 3, "WLFI Ecosystem fund contract"),
          ("0xcc261ab4be137eacf57c19ed97c186b4d88004ca", 5, "Jump Trading (market-maker deposit)"),
          ("0xf0cc01b37086bc122a3d63c615dab379478d2745", 2, "WLFI Multisig (team)"),
          ("0x29de882559194e2be08c182c1860193f8137cbf8", 2, "Ethena Labs WLFI Multisig (team)"),
          ("0x33ccf78a2091979fbc5a7631e6c71e900715ab78", 2, "SafeProxy (team multisig)"),
          ("0x284cf133aa570f29da0961be897dbbb2a37962f8", 2, "SafeProxy (team multisig)")],
 "ENA": [("0x2146aa5807d96e6b2922a149cee870f17347f1d0", 3, "Ethena Labs: Proxy (token/staking proxy)"),
         ("0xa5274a5a4b4bb3b3646475886b41bf6c50edd666", 2, "Ethena (protocol-team EOA)"),
         ("0x7462f0d93260909870487f17a27c336349579557", 2, "Ethena Labs (protocol-team EOA)"),
         ("0xb2af973905f05bc82bf97486b6ab883598d98298", 2, "Ethena Labs (protocol-team EOA)")],
 "PUMP": [("85WTujfJ9meJq5hfjAeb5gftj7n8Q7QTsZJbRqMD5ERS", 5, "pump.fun custody (exchange-class)"),
          ("AvqFxKNrYZNvxsj2oWhLW8det68HzCXBqswshoD2TdT6", 5, "pump.fun custody (exchange-class)"),
          ("96HiV4cGWTJNCjGVff3RTHgPXmpYz7MSrGTAmxNKVWM9", 5, "pump.fun custody (exchange-class)"),
          ("ERRGqu3dh6zYBg7MNAHKL33TyVb7efMmaKxnmdukdNYa", 5, "pump.fun custody (exchange-class)"),
          ("9UcygiamY92yGntGkUkBKi4SdApxkBMZd9QSo6wMC2dN", 5, "pump.fun custody (exchange-class)")],
 "KMNO": [("Ec6MuWtpvFcVyMsp7vipKCg1CMkKrWHZpWPdnJF16G57", 3, "Kamino Staking (Class-3 aggregation)"),
          ("8civ8uAA4RMY8Ho6DmJzgatAqutsRDL4hkmmCXtxZ8ew", 3, "Kamino Custody Vaults (DeFi vault aggregation)"),
          ("4uD7K6KCFfAWoeJVeDKk2V5fuRd8X4Y926cAqeoAhD8N", 3, "Kamino Custody Vaults (DeFi vault aggregation)")],
 "JTO": [("jjCAwuuNpJCNMLAanpwgJZ6cdXzLPXe2GfD6TaDQBXt", 3, "JITO Staking Pool (Class-3 aggregation)")],
}
# external/strategic insiders that SURVIVE the tighten (still counted in retention)
INSIDER = {x.lower() for x in [
 "0x628d3e52e46432ed7ff55efe0eaf67c9ac16aac0", "0x6fcfee4f14eafa723d90ad4b282757c5fe3d92ee",
 "0xd53e50c63b0d549f142a2dcfc454501aaa5b7f3f", "0x99f4176ee457afedffcb1839c7ab7a030a5e4a92",
 "0x1d65d296b6ad7fdbf77d3c9cc44c9b2787f1a341", "0x5ab26169051d0d96217949adb91e86e51a5fda74",
 "0x0249d14d15531065b927f4930562c3814e654b54", "0xcd52e35f7784efc78e835ef6e00be914f48beee6",
 "0xf0cc01b37086bc122a3d63c615dab379478d2745", "0x29de882559194e2be08c182c1860193f8137cbf8",
 "0x33ccf78a2091979fbc5a7631e6c71e900715ab78", "0x284cf133aa570f29da0961be897dbbb2a37962f8",
 "0xa5274a5a4b4bb3b3646475886b41bf6c50edd666", "0x7462f0d93260909870487f17a27c336349579557",
 "0xb2af973905f05bc82bf97486b6ab883598d98298", "0x877b3d5c681c8890d19dbf450306caa3c3d4bba6",
 "0xa55457e0d0652ba47fe1f97873a62b4f9dcae4d1"]} | {
 "4x3uU27N1cfmBx8JerY13ZzdNxgmgQdiZUSFZQHbhe1B", "6EyjmmTYdAEyoLN1eTynuGvQPRq8mR4HKrW9uBqWqi7N",
 "6AapP9rsXMsNTJEMbKUatmzLeYwkZSJWd84c6PLBJNvK"}


def load(tok):
    for d in HLD:
        p = os.path.join(d, f"{tok}_holders.csv")
        if os.path.exists(p):
            return list(csv.DictReader(open(p)))


def cur_excl(tok):
    s = set()
    for r in csv.DictReader(open(os.path.join(A, "data/processed/exclusions_log.csv"))):
        if r["token"].upper() == tok:
            s.add(r["address"].strip().lower())
    for r in csv.DictReader(open(EXCL)):
        if r["token"].upper() == tok:
            s.add(r["address"].strip().lower())
    return s


def recompute(tok):
    rows = load(tok)
    ex = cur_excl(tok)
    tset = {a for a, _, _ in TIGHTEN[tok]} | {a.lower() for a, _, _ in TIGHTEN[tok]}
    surv = sorted([(r["address"].strip(), float(r["balance"])) for r in rows
                   if r["address"].strip().lower() not in ex and r["address"].strip() not in tset
                   and r["address"].strip().lower() not in tset], key=lambda x: -x[1])
    T = sum(b for _, b in surv)
    sh = [b / T for _, b in surv]
    hhi = sum(s * s for s in sh)
    top10 = surv[:10]
    ins = [(a, b) for a, b in top10 if a.lower() in INSIDER or a in INSIDER]
    tot10 = sum(b for _, b in top10)
    icf = len(ins) / 10
    ibf = (sum(b for _, b in ins) / tot10) if tot10 else 0.0
    return {"hhi": round(hhi, 6), "top1": round(100 * sh[0], 6), "top5": round(100 * sum(sh[:5]), 6),
            "top10": round(100 * sum(sh[:10]), 6), "n": len(surv),
            "insider_count": len(ins), "insider_count_frac": round(icf, 4), "insider_balance_frac": round(ibf, 4)}


def main():
    rc = {t: recompute(t) for t in TIGHTEN}
    json.dump(rc, open(os.path.join(os.path.dirname(EXCL), "nansen_reclass_2026-05-29", "staking_audit",
                                    "a3_pca_tighten_results_2026-05-30.json"), "w"), indent=1)
    for t, d in rc.items():
        print(f"{t}: HHI={d['hhi']} top1={d['top1']:.2f} top5={d['top5']:.2f} top10={d['top10']:.2f} "
              f"n={d['n']} ret={d['insider_count_frac']}")

    # ---- 1. FRAME: line-targeted update of cols hhi(5) top1(7) top5(8) top10(9) ----
    open(FRAME + ".pre_a3_tighten", "w").write(open(FRAME).read())
    lines = open(FRAME, newline="").read().split("\n")
    for i, l in enumerate(lines):
        if not l.strip():
            continue
        f = next(csv.reader([l]))
        if len(f) < 10 or f[1] not in rc:
            continue
        d = rc[f[1]]
        f[5] = f"{d['hhi']:.6f}"
        f[7] = f"{d['top1']:.6f}"; f[8] = f"{d['top5']:.6f}"; f[9] = f"{d['top10']:.6f}"
        buf = io.StringIO(); csv.writer(buf, lineterminator="").writerow(f); lines[i] = buf.getvalue()
    open(FRAME, "w", newline="").write("\n".join(lines))

    # ---- 2. EXCLUSIONS: append tighten rows (idempotent guard) ----
    existing = open(EXCL).read()
    if "a3_pca_tighten_2026-05-30" not in existing:
        open(EXCL + ".pre_a3_tighten", "w").write(existing)
        with open(EXCL, "a", newline="") as fh:
            w = csv.writer(fh)
            for tok, addrs in TIGHTEN.items():
                for a, cls, label in addrs:
                    w.writerow([tok, a, cls, label, "a3_pca_tighten_2026-05-30"])

    # ---- 3. RETENTION VECTOR: update the 5 rows ----
    rv = list(csv.DictReader(open(RETV)))
    open(RETV + ".pre_a3_tighten", "w").write(open(RETV).read())
    for r in rv:
        if r["token"] in rc:
            d = rc[r["token"]]
            r["insider_count"] = d["insider_count"]; r["n_top10"] = 10
            r["insider_count_frac"] = d["insider_count_frac"]; r["insider_balance_frac"] = d["insider_balance_frac"]
    with open(RETV, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["token", "insider_count", "n_top10", "insider_count_frac", "insider_balance_frac"])
        w.writeheader(); w.writerows(rv)
    print("\n[applied] frame + new12_unified_exclusions + new12_retention_vector (backups .pre_a3_tighten)")


if __name__ == "__main__":
    main()
