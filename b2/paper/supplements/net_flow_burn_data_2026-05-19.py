"""
Net-flow operationalization: burn-data gathering for 40-protocol cross-section.

Aggregates documented burn mechanisms + annualized burn-USD estimates across
the 40-protocol sample for the net-flow subsidy specification.

Distinguishes:
- True burns (tokens permanently destroyed): Polygon EIP-1559, MakerDAO
  Surplus Auction, Hyperliquid Assistance Fund, Helium BME, Hivemapper BME,
  DIMO BME, GEODNET BME, Render BME, Pokt Shannon, IoTeX Burn-Drop,
  Filecoin FIP-100, LayerZero ZRO fee switch, The Graph query fee burns.
- Buyback-and-redistribute (tokens redistributed, not destroyed):
  Aave $50M/yr to stakers; GMX 27%/30% fees to stakers; Lido $10M/yr
  proposed; EtherFi buyback; Maple SYRUP buyback.

Token prices (USD, 2026-05-19 CoinGecko via WebFetch):
  HNT $0.824 | HONEY $0.0020 | DIMO $0.0103 | GEOD $0.139 | POL $0.090 |
  POKT $0.0106 | RENDER $1.80 | ZRO $1.33 | ETHFI $0.374 | SYRUP $0.210 |
  HYPE $48.08 | MKR $1607.21 | AAVE $88.40 | GMX $6.64 | LDO $0.352 |
  FIL $0.951 | GRT $0.0248 | IOTX $0.00433 | ATH $0.00584 | UNI $3.48 |
  CRV $0.235 | COMP $22.48 | ARB $0.115 | OP $0.128 | RPL $1.72 |
  BAL $0.142 | JUP $0.196 | DRIFT $0.0282 | ENS $6.22 | GRASS $0.299 |
  GTC $0.0961 | TEC $0.130 | W $0.0119 | AXL $0.0606

Output: net_flow_burn_data_2026-05-19.csv
"""

import csv
from pathlib import Path


# Token prices (USD) as of 2026-05-19 (CoinGecko)
PRICES = {
    "AAVE": 88.40, "ATH": 0.00584, "ARB": 0.115, "AXL": 0.0606,
    "BAL": 0.142, "COMP": 22.48, "CRV": 0.235, "DIMO": 0.0103,
    "DRIFT": 0.0282, "ENS": 6.22, "ETHFI": 0.374, "FIL": 0.951,
    "GEOD": 0.139, "GTC": 0.0961, "GMX": 6.64, "GRASS": 0.299,
    "HNT": 0.824, "HONEY": 0.00200, "HYPE": 48.08, "IOTX": 0.00433,
    "JUP": 0.196, "ZRO": 1.33, "LDO": 0.352, "MKR": 1607.21,
    "OP": 0.128, "POKT": 0.0106, "POL": 0.0902, "RENDER": 1.80,
    "RPL": 1.72, "SYRUP": 0.210, "GRT": 0.0248, "TEC": 0.130,
    "UNI": 3.48, "W": 0.0119, "META": None,  # MetaDAO price not on CoinGecko
    "IO": None, "MOR": None, "ANYONE": None,  # missing prices
}


# Burn-and-buyback data per protocol (annualized; USD at 2026-05-19 prices)
# Confidence: HIGH = repo data or specific protocol disclosure;
#             MEDIUM = WebSearch with explicit figure;
#             LOW = estimate or projection;
#             NONE = no burn mechanism documented or zero burns
# Type: true_burn = tokens destroyed; buyback_redist = bought-back-and-redistributed
PROTOCOLS = [
    # token, true_burn_usd_annual, buyback_redist_usd_annual, confidence, source, type_notes
    ("AAVE", 0, 50_000_000, "HIGH", "$50M/yr buyback formalized Oct 2025; weekly $250K-$1.75M to stakers", "buyback_redist"),
    ("ATH", 0, 0, "LOW", "Aethir compute burn rate unknown; minimal documented burns", "none"),
    ("ANYONE", 0, 0, "LOW", "Anyone Protocol burn rate unknown", "none"),
    ("ARB", 0, 0, "HIGH", "Arbitrum no token burns; sequencer fees to DAO treasury", "none"),
    ("AXL", 0, 0, "LOW", "AXL gas burns minimal", "none"),
    ("BAL", 0, 0, "HIGH", "Balancer no BAL burns; veBAL emissions only", "none"),
    ("COMP", 0, 0, "HIGH", "Compound no COMP burn mechanism", "none"),
    ("CRV", 0, 0, "HIGH", "Curve no CRV burns; gauge votes determine emissions", "none"),
    ("DIMO", 2_094_500, 0, "HIGH", "203M DIMO/yr burned in 2025 (data/raw/dimo_burn_concentration.csv) x $0.0103", "true_burn"),
    ("DRIFT", 0, 0, "LOW", "Drift buyback proposed; not yet active", "none"),
    ("ENS", 0, 0, "HIGH", "ENS no token burn; registration fees in ETH not ENS", "none"),
    ("ETHFI", 0, 7_500_000, "MEDIUM", "$50M cap buyback; $7.5M acquired to date; ongoing under $3 price", "buyback_redist"),
    ("FIL", 1_500_000, 0, "MEDIUM", "FIP-100 fee burns active; rough estimate based on protocol revenue $2.9M x ~50% burn rate", "true_burn"),
    ("GEOD", 1_192_310, 0, "HIGH", "8.6M GEOD/yr burned (data/raw/geodnet_monthly_burns.csv) x $0.139", "true_burn"),
    ("GTC", 0, 0, "HIGH", "Gitcoin GTC no burns", "none"),
    ("GMX", 0, 7_780_000, "HIGH", "27% V2 fees + 30% V1 fees buyback-and-distribute; $28.8M revenue x 27% effective", "buyback_redist"),
    ("GRASS", 0, 0, "LOW", "Grass burn rate unknown; protocol still early-stage", "none"),
    ("HNT", 2_157_037, 0, "HIGH", "2.6M HNT/yr burned (data/raw/helium_burn_concentration.csv) x $0.824", "true_burn"),
    ("HONEY", 123_491, 0, "HIGH", "62M HONEY/yr burned (data/raw/hivemapper_burn_concentration.csv) x $0.002", "true_burn"),
    ("HYPE", 500_000_000, 0, "HIGH", "Assistance Fund 97% of $780M fees x ~64% effective burn ratio = ~$500M/yr; $9.22M/week recent rate confirms", "true_burn"),
    ("IOTX", 100_000, 0, "LOW", "IoTeX Burn-Drop active; ioID device-registration burns; estimated ~$100K/yr at current device count", "true_burn"),
    ("JUP", 0, 0, "LOW", "Jupiter buyback proposed; not consistently active", "none"),
    ("ZRO", 5_000_000, 0, "MEDIUM", "ZRO fee switch active Feb 2026; Stargate $1.2M early acquired; ramping toward $100M target", "true_burn"),
    ("LDO", 0, 0, "MEDIUM", "$10M/yr Lido buyback PROPOSED Q1 2026 with conditional activation (ETH>$3K + revenue>$40M); not yet active", "future"),
    ("MKR", 365_000_000, 0, "HIGH", "Sky buyback $1M USDS/day = $365M/yr (Feb 2025 onwards); 75M USDS by Aug 2025 confirms", "true_burn"),
    ("META", 0, 0, "HIGH", "MetaDAO futarchy execution fees, no burns", "none"),
    ("MOR", 0, 0, "HIGH", "Morpheus AI no burn mechanism documented", "none"),
    ("OP", 0, 0, "HIGH", "Optimism no OP burns; sequencer fees to DAO", "none"),
    ("POKT", 9_540, 0, "HIGH", "900K POKT/yr burned (Shannon mint ratio 97.5%; PIP-41 Jan 2026) x $0.0106", "true_burn"),
    ("POL", 90_200_000, 0, "HIGH", "EIP-1559 base fee burns ~1M POL/day = 365M POL/yr x $0.0902", "true_burn"),
    ("RENDER", 1_272_600, 0, "HIGH", "707K RENDER/yr burned (Jan-Sep 2025 annualized from 530K) x $1.80; BME 95% of revenue", "true_burn"),
    ("RPL", 0, 0, "HIGH", "Rocket Pool no RPL burns; 5% RPL inflation per year", "none"),
    ("SYRUP", 0, 2_200_000, "MEDIUM", "Maple Finance ~2% of supply/yr buyback at $0.21 x ~22M SYRUP = ~$4.6M/yr; alternate estimate ~$2.2M/yr at lower buyback frequency; tokens removed from circulation (buyback-treasury, not destroyed)", "buyback_redist"),
    ("GRT", 5_000, 0, "HIGH", "The Graph 1% query fee burn x $457K total query fees 2025 = ~$5K/yr (minimal)", "true_burn"),
    ("TEC", 0, 0, "HIGH", "TEC no burns", "none"),
    ("UNI", 0, 0, "HIGH", "Uniswap UNI fee switch off by default; no active burns", "none"),
    ("W", 0, 0, "HIGH", "Wormhole no W burns", "none"),
    ("IO", 500_000, 0, "LOW", "io.net IO burn for compute purchases; rough estimate $0.5M/yr at current usage", "true_burn"),
    ("WXM", 0, 0, "LOW", "WeatherXM no documented burn mechanism; emission-based rewards only", "none"),
    ("LPT", 0, 0, "HIGH", "Livepeer no LPT burn mechanism; bond-fee rewards distributed to orchestrators/delegators", "none"),
]

PRICES["WXM"] = 0.0110  # WeatherXM (CoinGecko weatherxm-network 2026-05-19)
PRICES["LPT"] = 2.03  # Livepeer (CoinGecko livepeer 2026-05-19)


def main():
    # Build per-protocol burn-data records
    fieldnames = [
        "token", "token_price_usd", "true_burn_usd_annual", "buyback_redist_usd_annual",
        "confidence", "type", "source_notes",
    ]
    rows = []
    for token, true_burn, buyback, conf, source, typ in PROTOCOLS:
        price = PRICES.get(token)
        rows.append({
            "token": token,
            "token_price_usd": price if price is not None else "",
            "true_burn_usd_annual": true_burn,
            "buyback_redist_usd_annual": buyback,
            "confidence": conf,
            "type": typ,
            "source_notes": source,
        })

    out_path = Path(__file__).parent / "net_flow_burn_data_2026-05-19.csv"
    with out_path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"Wrote: {out_path}")
    print(f"Total protocols catalogued: {len(rows)}")
    print()
    print(f"True-burn protocols (true_burn_usd_annual > 0):")
    true_burns = sorted([r for r in rows if r["true_burn_usd_annual"] > 0],
                       key=lambda x: -x["true_burn_usd_annual"])
    for r in true_burns:
        print(f"  {r['token']:8s}: ${r['true_burn_usd_annual']/1e6:>9.2f}M/yr  ({r['confidence']:6s})  {r['source_notes'][:80]}")
    print()
    print(f"Buyback-redistribute protocols:")
    bb = sorted([r for r in rows if r["buyback_redist_usd_annual"] > 0],
               key=lambda x: -x["buyback_redist_usd_annual"])
    for r in bb:
        print(f"  {r['token']:8s}: ${r['buyback_redist_usd_annual']/1e6:>9.2f}M/yr  ({r['confidence']:6s})  {r['source_notes'][:80]}")


if __name__ == "__main__":
    main()
