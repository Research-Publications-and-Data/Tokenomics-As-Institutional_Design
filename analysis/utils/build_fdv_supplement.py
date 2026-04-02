"""
Supplement TT covariate file with FDV from CoinGecko market cap.
Writes covariates_fdv_supplement.csv with fdv_usd for all 29 protocols.
"""

import pandas as pd
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent

# Market cap as FDV proxy (CoinGecko, ~2026-03-30)
# Sources: CoinGecko simple/price with include_market_cap=true
# Notes: MKR uses DefiLlama initial FDV; WXM/ANYONE not listed

FDV_MAP = {
    # DeFi
    "COMP":     167_939_773,
    "MKR":      156_338_218,    # DefiLlama (CG shows 0 - token migrated to SKY)
    "AAVE":   1_471_909_189,
    "UNI":    2_207_117_641,
    "CRV":      323_291_399,
    "RPL":       37_011_839,
    "JUP":      537_607_094,
    "MPL_SYRUP":     None,      # Maple: MPL market cap negligible; SYRUP CG ID unclear
    "GMX":       64_551_659,
    "DRIFT":     37_589_287,
    "ETHFI":    364_229_750,
    # L1/L2 Infra
    "GRT":      257_044_737,
    "OP":       226_055_742,
    "POL":      971_317_828,
    "ARB":      551_072_641,
    "ENS":      212_982_923,
    # DePIN
    "DIMO":       7_297_170,
    "IOTX":      44_062_499,
    "WXM":           None,      # Not on CoinGecko
    "ANYONE":        None,      # Negligible / not listed
    "GRASS":    160_219_812,
    "LPT":      102_557_900,
    "HNT":      197_705_610,
    "GEOD":      59_840_200,
    "FIL":      627_729_476,
    "RENDER":   880_620_450,
    "POKT":      25_383_980,
    # Social/Dead
    "LDO":    1_400_000_000,    # CoinGecko ~Mar 2026
    "GTC":        6_650_728,
    "TEC":               0,     # Wound down
    # New protocols (added 2026-03-30)
    "ZRO":      480_000_000,    # CoinGecko ~Mar 2026
    "W":         82_000_000,    # CoinGecko ~Mar 2026
    "MOR":        8_600_000,    # CoinGecko ~Mar 2026
    "AXL":       53_000_000,    # CoinGecko ~Mar 2026 (axlAXL bridge token market cap)
    "META":           None,     # MetaDAO META — not listed on CoinGecko
}

rows = [{"token": t, "fdv_usd_cg": v} for t, v in FDV_MAP.items()]
df = pd.DataFrame(rows)

out = PROJECT_DIR / "fdv_supplement.csv"
df.to_csv(out, index=False)
print(f"Saved {len(df)} FDV entries → {out}")
print(f"  Non-null: {df['fdv_usd_cg'].notna().sum()}/29")
