"""
B2 Governance Concentration: Master Orchestration
Run after April 6, 2026 snapshot date.

Workflow:
1. Run Dune queries (via run_dune_queries.py or Dune UI)
2. Fetch Filfox rich list (FIL)
3. Fetch POKTscan rich list (POKT)
4. Merge multi-chain tokens (MPL/SYRUP, RENDER/RNDR)
5. Compute concentration metrics
6. Generate validation report

Usage:
    cd /Users/zach/b2-governance-data
    python scripts/orchestrate.py
"""

import subprocess
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent
SCRIPTS_DIR = PROJECT_DIR / "scripts"
HOLDER_DIR = PROJECT_DIR / "holder_lists"


def run_script(name):
    print(f"\n{'='*60}")
    print(f"Running: {name}")
    print('='*60)
    result = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / name)],
        cwd=str(PROJECT_DIR),
        capture_output=False,
    )
    if result.returncode != 0:
        print(f"WARNING: {name} exited with code {result.returncode}")
    return result.returncode


def check_holder_files():
    """Check which holder files exist."""
    expected = [
        "COMP", "MKR", "AAVE", "UNI", "CRV", "RPL", "JUP",
        "GMX", "DRIFT", "ETHFI", "GRT", "OP", "POL", "ARB", "ENS",
        "DIMO", "IOTX", "WXM", "ANYONE", "GRASS", "LPT", "HNT", "GEOD",
        "GTC", "TEC",
        # Merged/API tokens
        "FIL", "POKT",
        "MPL_SYRUP", "RENDER",
        # Component files for merge
        "MPL", "SYRUP", "RENDER_SOL", "RNDR_ETH",
    ]

    print(f"\n{'='*60}")
    print("Holder file inventory")
    print('='*60)
    found = 0
    missing = []
    for symbol in expected:
        path = HOLDER_DIR / f"holders_{symbol}.csv"
        if path.exists():
            import pandas as pd
            df = pd.read_csv(path)
            print(f"  OK  holders_{symbol}.csv ({len(df)} rows)")
            found += 1
        else:
            missing.append(symbol)

    print(f"\nFound: {found}, Missing: {len(missing)}")
    if missing:
        print(f"Missing: {', '.join(missing)}")
    return missing


def main():
    print("B2 Governance Concentration Data Collection")
    print("Snapshot date: April 6, 2026")
    print(f"Project dir: {PROJECT_DIR}")

    # Ensure holder_lists dir exists
    HOLDER_DIR.mkdir(exist_ok=True)

    # Step 1: Check what Dune data we already have
    missing = check_holder_files()

    # Step 2: Fetch API-sourced data
    if "FIL" in missing:
        run_script("filfox_richlist.py")

    if "POKT" in missing:
        run_script("poktscan_richlist.py")

    # Step 3: Merge multi-chain tokens
    needs_merge = False
    if "MPL_SYRUP" in missing and ("MPL" not in missing or "SYRUP" not in missing):
        needs_merge = True
    if "RENDER" in missing and ("RENDER_SOL" not in missing or "RNDR_ETH" not in missing):
        needs_merge = True

    if needs_merge:
        run_script("merge_multichain.py")

    # Step 4: Recheck
    missing = check_holder_files()

    # Step 5: Compute concentration metrics
    if len(missing) < 10:  # Allow some missing, compute what we have
        run_script("compute_concentration.py")
    else:
        print(f"\nToo many missing ({len(missing)}). Run Dune queries first.")
        print("Use run_dune_queries.py to generate SQL, execute on Dune,")
        print("download results to holder_lists/holders_<SYMBOL>.csv")


if __name__ == "__main__":
    main()
