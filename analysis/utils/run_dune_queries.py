"""
B2 Governance Data: Dune Query Runner
Creates and executes parameterized queries for all EVM + Solana tokens.

Usage:
    export DUNE_API_KEY=your_key_here
    python run_dune_queries.py

Processes tokens in batches by chain to minimize context switching.
Saves holder lists to holder_lists/ and logs query IDs.
"""

import json
import os
import time
import csv
from pathlib import Path

# Try to import dune_client; fall back to raw HTTP if not installed
try:
    from dune_client.client import DuneClient
    from dune_client.query import QueryBase
    HAS_DUNE_CLIENT = True
except ImportError:
    HAS_DUNE_CLIENT = False
    import requests

PROJECT_DIR = Path(__file__).parent.parent
HOLDER_DIR = PROJECT_DIR / "holder_lists"
REGISTRY_PATH = PROJECT_DIR / "token_registry.json"
QUERY_LOG = PROJECT_DIR / "query_log.json"

SNAPSHOT_DATE = "2026-04-01"

# Exchange addresses per chain (top CEX addresses)
EXCHANGE_EXCLUSIONS = {
    "ethereum": [
        "0x28C6c06298d514Db089934071355E5743bf21d60",
        "0x21a31Ee1afC51d94C2eFcCAa2092aD1028285549",
        "0xDFD5293D8e347dFe59E90eFd55b2956a1343963d",
        "0x56Eddb7aa87536c09CCc2793473599fD21A8b17F",
        "0x9696f59E4d72E237BE84fFD425DCaD154Bf96976",
        "0xF977814e90dA44bFA03b6295A0616a897441aceC",
        "0xBE0eB53F46cd790Cd13851d5EFf43D12404d33E8",
        "0x503828976D22510aad0201ac7EC88293211D23Da",
        "0xddfAbCdc4D8FfC6d5beaf154f18B778f892A0740",
        "0x3cD751E6b0078Be393132286c442345e68FF0aA0",
        "0xA9D1e08C7793af67e9d92fe308d5697FB81d3E43",
        "0x77134cbC06cB00b66F4c7e623D5fdBF6777635EC",
        "0xe93381fB4c4F14bDa253907b18faD305D799241a",
        "0x5C985E89DDe482eFE97ea9f1950aD149Eb73829B",
        "0xA7efAe728D2936e78BDA97dc267687568dD593f3",
        "0x6cC5F688a315f3dC28A7781717a9A798a59fDA7b",
        "0x236F233dBf78341d7B88b37e2faBf2CaA5271AeF",
        "0x75e89d5979E4f6Fba9F97c104c2F0AFB3F1dcB88",
        "0x0D0707963952f2fBA59dD06f2b425ace40b492Fe",
        "0x1AB4973a48dc892Cd9971ECE8e01DcC7688f8F23",
        "0x0639556F03714A74a5fEEaF5736a4A64fF70D206",
        "0xd6216fC19DB775Df9774a6E33526131dA7D19a2c",
        "0x2B5634C42055806a59e9107ED44D43c426E58258",
        "0x267be1C1D684F78cb4F6a176C4911b741E4Ffdc0",
        "0xAe2D4617c862309A3d75A0fFB358c7a5009c673F",
        "0x2910543Af39abA0Cd09dBb2D50200b3E800A63D2",
        "0xDA9dfA130Df4dE4673b89022EE50ff26f6EA73Cf",
        "0x0681d8Db095565FE8A346fA0277bFfdE9C0eDBBF",
        "0xf89d7b9c864f589bbF53a82105107622B35EaA40",
    ],
    "polygon": [
        "0xe7804c37c13166fF0b37F5aE0BB07A3aEbb6e245",  # Binance Polygon
        "0xf89d7b9c864f589bbF53a82105107622B35EaA40",  # Bybit
    ],
    "arbitrum": [
        "0xB38e8c17e38363aF6EbdCb3dAE12e0243582891D",  # Binance Arbitrum
        "0xf89d7b9c864f589bbF53a82105107622B35EaA40",  # Bybit
        "0xA7efAe728D2936e78BDA97dc267687568dD593f3",  # OKX
    ],
    "optimism": [
        "0xaCD03D601e5bB1B275Bb94076fF46ED9D753435A",  # Binance Optimism
    ],
    "gnosis": [],  # Minimal CEX presence on Gnosis
    "solana": [
        "5tzFkiKscjHsFKRq1DL8DW2P3RDLEP67475TzqCFMo5E",  # Binance
        "AC5RDfQFmDS1deWZos921JfqscXdByf6BKHAbXh2pVnD",  # Binance 2
        "GJRs4FwHtemZ5ZE9x3FNvJ8TMwitKTh21yxdRPqn7npE",  # Coinbase
        "H8sMJSCQxfKiFTCfDR3DUMLPwcRbM61LGFJ8N4dK3WjS",  # Coinbase Cold
        "2AQdpHJ2JpcEgPiATUXjQxA8QmafFegfQwSLWSprPicm",  # Coinbase 2
        "6VKzED7MCZsxFTc1GzNhML9FDPxGGLHh8EiRBSwkpkG4",  # OKX
    ],
}


def build_evm_query(token: dict) -> str:
    """Build the full SQL for an EVM token holder query."""
    chain = token['chain']
    table = token['dune_table']
    contract = token['contract']
    decimals = token['decimals']
    symbol = token['symbol']

    # Build exchange exclusion clause
    excl_addrs = EXCHANGE_EXCLUSIONS.get(chain, [])
    if excl_addrs:
        excl_list = ",\n        ".join(f"0x{a[2:]}" if not a.startswith("0x0x") else a for a in excl_addrs)
        excl_clause = f"AND address NOT IN (\n        {excl_list}\n      )"
    else:
        excl_clause = ""

    return f"""
-- {symbol} ({token['name']}) on {chain}
-- Snapshot: {SNAPSHOT_DATE}
WITH
transfers_in AS (
    SELECT "to" AS address,
           SUM(CAST(value AS DOUBLE) / POWER(10, {decimals})) AS inflow
    FROM {table}
    WHERE contract_address = 0x{contract[2:]}
      AND evt_block_date <= DATE '{SNAPSHOT_DATE}'
    GROUP BY 1
),
transfers_out AS (
    SELECT "from" AS address,
           SUM(CAST(value AS DOUBLE) / POWER(10, {decimals})) AS outflow
    FROM {table}
    WHERE contract_address = 0x{contract[2:]}
      AND evt_block_date <= DATE '{SNAPSHOT_DATE}'
    GROUP BY 1
),
net_balances AS (
    SELECT COALESCE(i.address, o.address) AS address,
           COALESCE(i.inflow, 0) - COALESCE(o.outflow, 0) AS balance
    FROM transfers_in i
    FULL OUTER JOIN transfers_out o ON i.address = o.address
),
filtered AS (
    SELECT * FROM net_balances
    WHERE balance > 0
      AND address != 0x0000000000000000000000000000000000000000
      {excl_clause}
),
ranked AS (
    SELECT address, balance,
           ROW_NUMBER() OVER (ORDER BY balance DESC) AS rank
    FROM filtered
)
SELECT '{symbol}' AS token,
       CAST(address AS VARCHAR) AS address,
       balance,
       rank,
       balance / SUM(balance) OVER () AS share
FROM ranked
WHERE rank <= 1000
ORDER BY rank
"""


def build_solana_query(token: dict) -> str:
    """Build SQL for Solana SPL token using daily_balances."""
    mint = token['contract']
    decimals = token['decimals']
    symbol = token['symbol']

    excl_addrs = EXCHANGE_EXCLUSIONS.get('solana', [])
    if excl_addrs:
        excl_list = ",\n        ".join(f"'{a}'" for a in excl_addrs)
        excl_clause = f"AND token_balance_owner NOT IN (\n        {excl_list}\n      )"
    else:
        excl_clause = ""

    return f"""
-- {symbol} ({token['name']}) on Solana
-- Snapshot: {SNAPSHOT_DATE}
-- Using solana_utils.daily_balances (partition: month)
WITH daily_bal AS (
    SELECT token_balance_owner AS address,
           token_balance / POWER(10, {decimals}) AS balance
    FROM solana_utils.daily_balances
    WHERE token_mint_address = '{mint}'
      AND day = DATE '{SNAPSHOT_DATE}'
      AND month = DATE '2026-04-01'
      AND token_balance > 0
      {excl_clause}
),
ranked AS (
    SELECT address, balance,
           ROW_NUMBER() OVER (ORDER BY balance DESC) AS rank
    FROM daily_bal
    WHERE balance > 0
)
SELECT '{symbol}' AS token,
       address,
       balance,
       rank,
       balance / SUM(balance) OVER () AS share
FROM ranked
WHERE rank <= 1000
ORDER BY rank
"""


def expand_secondary_queries(registry):
    """
    For tokens with secondary contracts (MPL/SYRUP, RENDER/RNDR),
    generate additional query entries.
    """
    extra = []
    for t in registry:
        if 'contract_secondary' in t and t.get('contract_secondary'):
            if t['symbol'] == 'MPL_SYRUP':
                # Generate SYRUP query separately
                extra.append({
                    'symbol': 'SYRUP',
                    'name': 'Maple Finance (SYRUP)',
                    'category': t['category'],
                    'chain': 'ethereum',
                    'contract': t['contract_secondary'],
                    'decimals': t.get('decimals_secondary', 18),
                    'dune_table': 'erc20_ethereum.evt_transfer',
                    'launch_year': t['launch_year'],
                    'governance_model': t['governance_model'],
                    'distribution_type': t['distribution_type'],
                    'notes': 'SYRUP component for MPL/SYRUP merge',
                })
                # Rename primary to MPL
                t['symbol'] = 'MPL'
            elif t['symbol'] == 'RENDER':
                # Generate RNDR Ethereum query separately
                extra.append({
                    'symbol': 'RNDR_ETH',
                    'name': 'Render (Ethereum RNDR)',
                    'category': t['category'],
                    'chain': 'ethereum',
                    'contract': t['contract_secondary'],
                    'decimals': t.get('decimals_secondary', 18),
                    'dune_table': 'erc20_ethereum.evt_transfer',
                    'launch_year': t['launch_year'],
                    'governance_model': t['governance_model'],
                    'distribution_type': t['distribution_type'],
                    'notes': 'Ethereum RNDR component for RENDER merge',
                })
                # Rename primary to RENDER_SOL
                t['symbol'] = 'RENDER_SOL'
    return registry + extra


def main():
    with open(REGISTRY_PATH) as f:
        registry = json.load(f)

    # Expand secondary contracts into separate queries
    registry = expand_secondary_queries(registry)

    # Group by chain for efficient batching
    by_chain = {}
    for t in registry:
        if t.get('dune_table', 'N/A') == 'N/A':
            continue
        chain = t['chain']
        by_chain.setdefault(chain, []).append(t)

    print("=== B2 Governance Data: Query Plan ===")
    print(f"Snapshot date: {SNAPSHOT_DATE}")
    print(f"Total tokens: {len(registry)}")
    for chain, tokens in sorted(by_chain.items()):
        symbols = [t['symbol'] for t in tokens]
        print(f"  {chain}: {', '.join(symbols)} ({len(tokens)} tokens)")

    # Tokens needing alternative APIs
    alt_api = [t for t in registry if t['dune_table'] == 'N/A']
    if alt_api:
        print(f"  Alternative API: {', '.join(t['symbol'] for t in alt_api)}")

    print("\n=== Generated SQL (paste into Dune) ===\n")

    query_log = []

    for chain, tokens in sorted(by_chain.items()):
        print(f"\n--- {chain.upper()} ---\n")
        for token in tokens:
            if chain == 'solana' or 'solana' in token.get('dune_table', ''):
                sql = build_solana_query(token)
            else:
                sql = build_evm_query(token)

            # Print SQL for manual execution
            print(sql)
            print("-- " + "=" * 60 + "\n")

            query_log.append({
                "symbol": token['symbol'],
                "chain": chain,
                "sql_generated": True,
                "query_id": None,
                "execution_id": None,
                "status": "pending",
            })

    # Save query log
    with open(QUERY_LOG, 'w') as f:
        json.dump(query_log, f, indent=2)
    print(f"\nQuery log saved to {QUERY_LOG}")
    print(f"Total queries to run: {len(query_log)}")
    print("\nNOTE: Run these queries on Dune after April 6, 2026.")
    print("Export results as CSV to holder_lists/holders_<SYMBOL>.csv")
    print("Then run compute_concentration.py to generate final metrics.")


if __name__ == "__main__":
    main()
