#!/usr/bin/env python3
"""B2 Full Revision: Exclusion discovery, HHI recomputation, data update, regression."""

import requests
import time
import json
import pandas as pd
import numpy as np
from scipy import stats
import sys
import os

DUNE_API_KEY = "WsfJ8jH971X4hiuKfwGZLZo3S70ibX4f"
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ── EXCLUSION ADDRESSES ──

EXCLUSIONS = {
    "COMP": {
        "token": "0xc00e94Cb662C3520282E6f5717214004A7f26888",
        "chain": "ethereum",
        "addrs": {
            "0x3d9819210A31b4961b30EF54bE2aeD79B9c9Cd3B": "Comptroller",
            "0x6d903f6003cca6255D85CcA4D3B5E5146dC33925": "Timelock",
            "0xc0Da02939E1441F497fd74F78cE7Decb17B66529": "Governor Bravo",
            "0x2775b1c75658Be0F5a7235755D462ee099aff4E4": "Reservoir",
            "0x91d14789071e5E195FFC9F745348736677De3292": "DComp (354K COMP)",
            "0xc3d688B66703497DAA19211EEdff47f25384cdc3": "Compound USDCv3 Token (100K COMP)",
            "0x3Afdc9BCA9213A35503b077a6072F3D0d5AB0840": "Compound cUSDTv3 Token (100K COMP)",
        },
    },
    "CRV": {
        "token": "0xD533a949740bb3306d119CC777fa900bA034cd52",
        "chain": "ethereum",
        "addrs": {
            "0x5f3b5DfEb7B28CDbD7FAba78963EE202a494e2A2": "veCRV locker (857M CRV)",
            "0xd061D61a4d941c39E5453435B6345Dc261C2fcE0": "CRV Minter",
            "0x2F50D538606Fa9EDD2B11E2446BEb18C9D5846bB": "GaugeController",
            "0xa3A7B6F88361F48403514059F1F16C8E78d60EeC": "Arbitrum L1ERC20Gateway (bridge)",
            "0xafca625321Df8D6A068bDD8F1585d489D2acF11b": "LLAMMA-crvUSDAMM",
            "0x575CCD8e2D300e2377B43478339E364000318E2c": "pre-CRV Liquidity Providers",
            "0x99C9fc46f92E8a1c0deC1b1747d010903E884bE1": "Optimism L1StandardBridge",
            # NEW: discovered from top-30 analysis
            "0xD347Ce96266d99aC67DEbb15b3edD43a9E94B751": "Community Fund vesting (VestingEscrowSimple)",
            "0xc420C9d507D0E038BD76383AaADCAd576ed0073c": "Team/Investor GnosisSafe multisig",
            "0x300d1a01b2C8fc34d5D15071B2611560D7AB9d61": "Investor allocation wallet (64.9M CRV)",
            "0x7cD7dB9D5F402E5a27774BEE9d61aB8F21cC51FD": "Investor allocation wallet (64.8M CRV)",
        },
    },
    "LDO": {
        "token": "0x5A98FcBEA516Cf06857215779Fd812CA3beF1B32",
        "chain": "ethereum",
        "addrs": {
            "0x3e40D73EB977Dc6a537aF587D48316feE66E9C8c": "Aragon Agent (DAO treasury)",
            # NEW: 5 founding-era vesting multisigs
            "0x945755dE7EAc99008c8C57bdA96772d50872168b": "Lido vesting multisig #1 (50M LDO)",
            "0x695C388153bEa0fbE3e1C049c149bAD3bc917740": "Lido vesting multisig #2 (50M LDO)",
            "0xA2dfC431297aee387C05bEEf507E5335E684FbCD": "Lido vesting multisig #3 (45.8M LDO)",
            "0x1597D19659F3DE52ABd475F7D2314DCca29359BD": "Lido vesting multisig #4 (45M LDO)",
            "0xb8d83908AAB38a159F3dA47a59d84dB8e1838712": "Lido vesting multisig #5 (31.1M LDO)",
            # TRP factory individual escrows not in top-30
            # 5M LDO SafeProxies (ranks 25-30) — not excluded: insufficient evidence of DAO control
        },
    },
    "ARB": {
        "token": "0x912CE59144191C1204E64559FE8253a0e49E6548",
        "chain": "arbitrum",
        "addrs": {
            "0xF3FC178157fb3c87548bAA86F9d24BA38E649B58": "FixedDelegateErc20Wallet (existing)",
            # NEW: 5 additional
            "0xCaD7828a19b363A2B44717AFB1786B5196974D8E": "Token Distributor (L2ReverseCustomGateway)",
            "0x15533b77981cDa0F85c4F9a485237DF4285D6844": "ArbitrumFoundationVestingWallet",
            "0x140e4D8d4229D5437EfD6FC1BEeB86Cb2bCF9D98": "DAO Treasury (SafeProxy via UpgradeExecutor)",
            "0xD6c8a4E72584f24bd5517AfeD6c01D21477C17f6": "Security Council (GnosisSafeL2)",
            "0xef297424bbC64B21fB405532b58fe77299f1e1F4": "Upgrade Executor Safe",
            "0xAe8cBcef7DE8664C3fF5BfC58536c183FfA60B51": "Security Council v2 (GnosisSafeL2)",
        },
    },
    "GRT": {
        "token": "0xc944E90C64B2c07662A292be6244BDf05Cda44a7",
        "chain": "ethereum",
        "addrs": {
            "0x36aFF7001294daE4C2ED4fDEfC478a00De77F090": "BridgeEscrow (existing)",
            # NEW: 3 additional
            "0xF55041E37E12cD407ad00CE2910B8269B01263b9": "L1Staking proxy (GraphProxy)",
            "0xa5946A2C7A6C4232224b89a696AE51879bf5aED1": "GraphTokenLockManager",
            "0x32Ec7A59549b9F114c9D7d8b21891d91Ae7F2ca1": "GraphTokenLockSimple (749M GRT vesting)",
        },
    },
    "OP": {
        "token": "0x4200000000000000000000000000000000000042",
        "chain": "optimism",
        "addrs": {
            "0x2A82Ae142b2e62Cb7D10b55E323ACB1Cab663a26": "Foundation GnosisSafe (existing)",
            "0x2501c477D0A35DAd0eAB9F1d4c8972bBa4DE1B18": "Foundation (existing)",
            # NEW: 5 additional
            "0x2501c477D0A35545a387Aa4A3EEe4292A9a8B3F0": "Foundation operating wallet (OLI tagged)",
            "0xAcf32F4e1260636cf1e3066c060C74AD52fE4E9e": "Grants locked (Foundation Safe 2022)",
            "0x19793c7824Be70ec58BB673CA42D2779d12581BE": "Grants unlocked (Foundation Safe 2023)",
            "0x6ba2C3b591Ac4bE15cDA66b305Db4F03E7ff7C9f": "Airdrop distributor (EIP-1167 proxy)",
            "0xADbF24E9968cdF7792E8823110Ae9F104d1B1809": "Foundation safe v2 (created 2025-02)",
        },
    },
}

# ── DUNE SQL TEMPLATE ──

CHAIN_MAP = {"ethereum": "ethereum", "arbitrum": "arbitrum", "optimism": "optimism"}

def build_hhi_query(proto, info):
    chain = CHAIN_MAP[info["chain"]]
    token = info["token"]
    excl_list = ", ".join(f"0x{a[2:]}" for a in info["addrs"].keys())
    decimals = 18
    return f"""
WITH balances AS (
    SELECT b.address AS holder, b.amount / POWER(10, {decimals}) AS balance
    FROM tokens.balances_daily b
    WHERE b.blockchain = '{chain}'
      AND b.token_address = 0x{token[2:]}
      AND b.day = CURRENT_DATE - INTERVAL '1' DAY
      AND b.amount > 0
      AND b.address NOT IN (
          SELECT address FROM labels.addresses
          WHERE blockchain = '{chain}' AND label_type = 'exchange'
      )
      AND b.address NOT IN ({excl_list})
),
ranked AS (
    SELECT *,
        ROW_NUMBER() OVER (ORDER BY balance DESC) AS rank,
        SUM(balance) OVER () AS total_balance
    FROM balances
),
top1000 AS (SELECT * FROM ranked WHERE rank <= 1000)
SELECT '{proto}' AS protocol,
    ROUND(SUM(POWER(balance / total_balance, 2)), 6) AS hhi,
    ROUND(MAX(CASE WHEN rank = 1 THEN balance / total_balance * 100 END), 2) AS top1_pct,
    COUNT(*) AS n_holders
FROM top1000
"""

def execute_dune_sql(sql):
    url = "https://api.dune.com/api/v1/query/sql"
    headers = {"X-Dune-Api-Key": DUNE_API_KEY, "Content-Type": "application/json"}
    resp = requests.post(url, headers=headers, json={"query_sql": sql, "performance": "medium"})
    if not resp.ok:
        print(f"  ERROR submitting: {resp.status_code} {resp.text[:200]}")
        return None
    data = resp.json()
    exec_id = data.get("execution_id")
    if not exec_id:
        print(f"  ERROR: no execution_id in response: {data}")
        return None
    print(f"  Execution ID: {exec_id}")

    # Poll for results
    for i in range(60):
        time.sleep(5)
        status_url = f"https://api.dune.com/api/v1/execution/{exec_id}/status"
        sr = requests.get(status_url, headers={"X-Dune-Api-Key": DUNE_API_KEY})
        if not sr.ok:
            continue
        state = sr.json().get("state", "")
        if state == "QUERY_STATE_COMPLETED":
            results_url = f"https://api.dune.com/api/v1/execution/{exec_id}/results"
            rr = requests.get(results_url, headers={"X-Dune-Api-Key": DUNE_API_KEY})
            if rr.ok:
                rows = rr.json().get("result", {}).get("rows", [])
                return rows
            break
        elif state in ("QUERY_STATE_FAILED", "QUERY_STATE_CANCELLED"):
            print(f"  Query {state}")
            return None
        if i % 6 == 0:
            print(f"  ... polling ({state})")
    print("  TIMEOUT")
    return None

# ── MAIN ──

def main():
    print("=" * 60)
    print("B2 FULL REVISION")
    print("=" * 60)

    # Count total exclusions
    total_excl = sum(len(v["addrs"]) for v in EXCLUSIONS.values())
    print(f"\nTotal exclusion addresses: {total_excl}")

    # ── PART 3: Recompute HHI ──
    print("\n── PART 3: Recomputing HHI for 6 protocols ──")
    recomputed = {}
    for proto, info in EXCLUSIONS.items():
        print(f"\n{proto} ({len(info['addrs'])} exclusions on {info['chain']}):")
        sql = build_hhi_query(proto, info)
        rows = execute_dune_sql(sql)
        if rows and len(rows) > 0:
            row = rows[0]
            recomputed[proto] = {
                "hhi": float(row.get("hhi", 0)),
                "top1_pct": float(row.get("top1_pct", 0)),
                "n_holders": int(row.get("n_holders", 0)),
            }
            print(f"  RESULT: HHI={recomputed[proto]['hhi']:.6f}, top1={recomputed[proto]['top1_pct']}%, n={recomputed[proto]['n_holders']}")
        else:
            print(f"  FAILED - using existing value")

    # ── PART 4: Update Data Files ──
    print("\n── PART 4: Updating data files ──")

    # Map protocol names between EXCLUSIONS keys and CSV protocol names
    PROTO_MAP = {
        "COMP": "Compound",
        "CRV": "Curve",
        "LDO": "Lido",
        "ARB": "Arbitrum",
        "GRT": "The Graph",
        "OP": "Optimism",
    }

    # Expansion protocols
    EXPANSION = {
        "Aethir":    {"hhi": 0.1678, "subsidy": 0.15, "revenue": 166e6, "emissions": 24.9e6, "cat": "DePIN", "chain": "ethereum", "holders": 90700},
        "Hivemapper":{"hhi": 0.0198, "subsidy": 5.46, "revenue": 18e6,  "emissions": 98.4e6, "cat": "DePIN", "chain": "solana",   "holders": 90700},
        "io.net":    {"hhi": 0.1113, "subsidy": 0.56, "revenue": 30e6,  "emissions": 16.8e6, "cat": "DePIN", "chain": "solana",   "holders": 84900},
    }

    # 4a. regression_data_april2026.csv
    reg_path = os.path.join(BASE, "data", "regression_data_april2026.csv")
    reg = pd.read_csv(reg_path)
    print(f"\nLoaded regression_data: {len(reg)} rows")

    # Update recomputed HHI values
    for short, result in recomputed.items():
        full_name = PROTO_MAP.get(short, short)
        mask = reg["protocol"] == full_name
        if mask.any():
            old = reg.loc[mask, "hhi"].values[0]
            reg.loc[mask, "hhi"] = result["hhi"]
            print(f"  {full_name}: HHI {old:.6f} -> {result['hhi']:.6f}")

    # Add 3 expansion protocols
    for name, data in EXPANSION.items():
        if name not in reg["protocol"].values:
            new_row = {
                "protocol": name,
                "token": {"Aethir": "ATH", "Hivemapper": "HONEY", "io.net": "IO"}[name],
                "category": data["cat"],
                "chain": data["chain"],
                "measurement_type": "governance_token",
                "hhi": data["hhi"],
                "n_holders": data["holders"],
                "subsidy_ratio_onchain": data["subsidy"],
                "revenue_onchain_usd": data["revenue"],
                "emissions_onchain_usd": data["emissions"],
                "regression_ready": True,
                "revenue_source_onchain": "Messari + Dune",
            }
            reg = pd.concat([reg, pd.DataFrame([new_row])], ignore_index=True)
            print(f"  Added {name}: HHI={data['hhi']}, subsidy={data['subsidy']}x")

    # Fix Livepeer subsidy
    mask_lp = reg["protocol"] == "Livepeer"
    if mask_lp.any():
        old_sub = reg.loc[mask_lp, "subsidy_ratio_onchain"].values[0]
        reg.loc[mask_lp, "subsidy_ratio_onchain"] = 88.5
        reg.loc[mask_lp, "revenue_onchain_usd"] = 838701
        reg.loc[mask_lp, "emissions_onchain_usd"] = 74200000
        print(f"  Livepeer subsidy: {old_sub} -> 88.5")

    # Fix Helium subsidy
    mask_he = reg["protocol"] == "Helium"
    if mask_he.any():
        old_sub = reg.loc[mask_he, "subsidy_ratio_onchain"].values[0]
        reg.loc[mask_he, "subsidy_ratio_onchain"] = 1.05
        reg.loc[mask_he, "revenue_onchain_usd"] = 17560000
        reg.loc[mask_he, "emissions_onchain_usd"] = 18490000
        print(f"  Helium subsidy: {old_sub} -> 1.05")

    reg.to_csv(reg_path, index=False)
    print(f"  Saved regression_data: {len(reg)} rows")

    # 4b. governance_concentration_april2026.csv
    gov_path = os.path.join(BASE, "data", "governance_concentration_april2026.csv")
    gov = pd.read_csv(gov_path)
    for short, result in recomputed.items():
        full_name = PROTO_MAP.get(short, short)
        mask = gov["protocol"] == full_name
        if mask.any():
            gov.loc[mask, "hhi"] = result["hhi"]
            if "top1_pct" in gov.columns:
                gov.loc[mask, "top1_pct"] = result["top1_pct"]
    for name, data in EXPANSION.items():
        if name not in gov["protocol"].values:
            new_row = {
                "protocol": name,
                "token": {"Aethir": "ATH", "Hivemapper": "HONEY", "io.net": "IO"}[name],
                "category": data["cat"],
                "chain": data["chain"],
                "measurement_type": "governance_token",
                "hhi": data["hhi"],
                "n_holders": data["holders"],
            }
            gov = pd.concat([gov, pd.DataFrame([new_row])], ignore_index=True)
    gov.to_csv(gov_path, index=False)
    print(f"  Saved governance_concentration: {len(gov)} rows")

    # 4c. depin_onchain_financials.csv
    fin_path = os.path.join(BASE, "data", "depin_onchain_financials.csv")
    fin = pd.read_csv(fin_path)

    # Fix Livepeer
    mask_lp_fin = fin["protocol"] == "Livepeer"
    if mask_lp_fin.any():
        fin.loc[mask_lp_fin, "revenue_usd_annual"] = 838701
        fin.loc[mask_lp_fin, "emissions_usd_annual"] = 74200000
        fin.loc[mask_lp_fin, "subsidy_ratio"] = 88.5
        fin.loc[mask_lp_fin, "source"] = "Messari ETH fees + Dune LPT mints"

    # Fix Helium
    mask_he_fin = fin["protocol"] == "Helium"
    if mask_he_fin.any():
        fin.loc[mask_he_fin, "revenue_usd_annual"] = 17560000
        fin.loc[mask_he_fin, "emissions_usd_annual"] = 18490000
        fin.loc[mask_he_fin, "subsidy_ratio"] = 1.05

    # Add expansion
    for name in ["Aethir", "Hivemapper", "io.net"]:
        d = EXPANSION[name]
        if name not in fin["protocol"].values:
            new_row = {
                "protocol": name,
                "revenue_usd_annual": d["revenue"],
                "emissions_usd_annual": d["emissions"],
                "subsidy_ratio": d["subsidy"],
                "source": "Messari + Dune",
                "measurement_window": "Apr2025-Mar2026",
            }
            fin = pd.concat([fin, pd.DataFrame([new_row])], ignore_index=True)
    fin.to_csv(fin_path, index=False)
    print(f"  Saved depin_onchain_financials: {len(fin)} rows")

    # 4d. exclusions_log.csv
    excl_path = os.path.join(BASE, "data", "exclusions_log.csv")
    excl_df = pd.read_csv(excl_path)
    new_excl_rows = []
    for proto_short, info in EXCLUSIONS.items():
        full_name = PROTO_MAP.get(proto_short, proto_short)
        existing_addrs = set(excl_df.loc[excl_df["token"] == proto_short, "address"].str.lower()) if len(excl_df) > 0 else set()
        for addr, identity in info["addrs"].items():
            if addr.lower() not in existing_addrs:
                hhi_after = recomputed.get(proto_short, {}).get("hhi", "")
                new_excl_rows.append({
                    "token": {"Compound": "COMP", "Curve": "CRV", "Lido": "LDO", "Arbitrum": "ARB", "The Graph": "GRT", "Optimism": "OP"}.get(full_name, proto_short),
                    "address": addr,
                    "identity": identity,
                    "exclusion_reason": "Protocol-controlled address: " + identity,
                    "chain": info["chain"].capitalize(),
                    "hhi_before": "",
                    "hhi_after": hhi_after,
                    "source": "Blockscout top-holder analysis + on-chain verification",
                })
    if new_excl_rows:
        excl_df = pd.concat([excl_df, pd.DataFrame(new_excl_rows)], ignore_index=True)
    excl_df.to_csv(excl_path, index=False)
    # Also save to root-level copy
    excl_df.to_csv(os.path.join(BASE, "exclusions_log.csv"), index=False)
    print(f"  Saved exclusions_log: {len(excl_df)} rows ({len(new_excl_rows)} new)")

    # ── PART 5: Recompute Regressions ──
    print("\n── PART 5: Recomputing regressions ──")

    # Reload updated data
    reg = pd.read_csv(reg_path)

    # Filter to protocols with subsidy data
    sub = reg.dropna(subset=["hhi", "subsidy_ratio_onchain"])
    sub = sub[sub["subsidy_ratio_onchain"] > 0].copy()
    print(f"\nSubsidy sample: N={len(sub)}")
    print(sub[["protocol", "category", "hhi", "subsidy_ratio_onchain"]].to_string())

    # Cross-sector Pearson
    r_p, p_p = stats.pearsonr(sub["subsidy_ratio_onchain"], sub["hhi"])
    print(f"\nCross-sector Pearson: r={r_p:.3f}, p={p_p:.3f}, N={len(sub)}")

    # Cross-sector Spearman
    r_s, p_s = stats.spearmanr(sub["subsidy_ratio_onchain"], sub["hhi"])
    print(f"Cross-sector Spearman: rho={r_s:.3f}, p={p_s:.3f}")

    # Log Pearson
    sub_log = sub.copy()
    sub_log["log_sub"] = np.log(sub_log["subsidy_ratio_onchain"])
    r_log, p_log = stats.pearsonr(sub_log["log_sub"], sub_log["hhi"])
    print(f"Cross-sector log Pearson: r={r_log:.3f}, p={p_log:.3f}")

    # Excluding Livepeer
    sub_no_lp = sub[sub["protocol"] != "Livepeer"]
    r_nolp, p_nolp = stats.pearsonr(sub_no_lp["subsidy_ratio_onchain"], sub_no_lp["hhi"])
    print(f"Excluding Livepeer: r={r_nolp:.3f}, p={p_nolp:.3f}, N={len(sub_no_lp)}")

    # Within-DePIN
    depin = sub[sub["category"] == "DePIN"]
    if len(depin) >= 3:
        r_dp, p_dp = stats.pearsonr(depin["subsidy_ratio_onchain"], depin["hhi"])
        r_ds, p_ds = stats.spearmanr(depin["subsidy_ratio_onchain"], depin["hhi"])
        print(f"DePIN Pearson: r={r_dp:.3f}, p={p_dp:.3f}, N={len(depin)}")
        print(f"DePIN Spearman: rho={r_ds:.3f}, p={p_ds:.3f}")

    # Within-DeFi
    defi = sub[sub["category"] == "DeFi"]
    if len(defi) >= 3:
        r_df, p_df = stats.pearsonr(defi["subsidy_ratio_onchain"], defi["hhi"])
        print(f"DeFi Pearson: r={r_df:.3f}, p={p_df:.3f}, N={len(defi)}")

    # Sector test (Mann-Whitney)
    depin_all = reg[reg["category"] == "DePIN"]["hhi"].dropna()
    defi_all = reg[reg["category"] == "DeFi"]["hhi"].dropna()
    u_stat, p_mw = stats.mannwhitneyu(depin_all, defi_all, alternative="two-sided")
    print(f"\nSector test (Mann-Whitney): U={u_stat:.1f}, p={p_mw:.3f}")
    print(f"  DePIN: N={len(depin_all)}, mean={depin_all.mean():.4f}")
    print(f"  DeFi:  N={len(defi_all)}, mean={defi_all.mean():.4f}")

    # ── Summary ──
    print("\n" + "=" * 60)
    print("RESULTS SUMMARY")
    print("=" * 60)
    print(f"Total exclusions: {len(excl_df)} rows")
    print(f"Sample: {len(reg)} protocols")
    print(f"Subsidy N: {len(sub)}")
    print(f"DePIN with subsidy: {len(depin)}")
    print(f"DeFi with subsidy: {len(defi)}")

    # Save regression results for paper patching
    results = {
        "cross_pearson": {"r": round(r_p, 3), "p": round(p_p, 3)},
        "cross_spearman": {"rho": round(r_s, 3), "p": round(p_s, 3)},
        "cross_log": {"r": round(r_log, 3), "p": round(p_log, 3)},
        "excl_livepeer": {"r": round(r_nolp, 3), "p": round(p_nolp, 3)},
        "sector_mw": {"p": round(p_mw, 3)},
        "n_subsidy": len(sub),
        "n_depin_subsidy": len(depin),
        "n_defi_subsidy": len(defi),
        "n_total": len(reg),
    }
    if len(depin) >= 3:
        results["depin_pearson"] = {"r": round(r_dp, 3), "p": round(p_dp, 3)}
        results["depin_spearman"] = {"rho": round(r_ds, 3), "p": round(p_ds, 3)}
    if len(defi) >= 3:
        results["defi_pearson"] = {"r": round(r_df, 3), "p": round(p_df, 3)}

    results_path = os.path.join(BASE, "data", "regression_results.json")
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved regression results to {results_path}")

    # HHI change summary
    print("\n── HHI Changes ──")
    for short, result in recomputed.items():
        full_name = PROTO_MAP.get(short, short)
        print(f"  {full_name}: {result['hhi']:.6f} (top1={result['top1_pct']}%, n={result['n_holders']})")

    print("\nDone. Ready for paper patching.")

if __name__ == "__main__":
    main()
