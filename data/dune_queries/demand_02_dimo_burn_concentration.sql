-- ============================================================
-- Query: DIMO Token Burn Concentration — Full HHI
-- Paper: Paper 2 ("GeoDePIN: Design Patterns")
-- Section: Exhibit 4 — Demand HHI
-- Chain: Polygon
-- Time Range: Jan 2024 to Apr 2026
-- Dune Query ID: TBD
-- Author: Zach Zukowski
-- Notes:
--   - DIMO token on Polygon: 0xE261D618a959aFfFd53168Cd07D12E37B26761db
--   - Burns to 0x0 = DIMO→DCX conversions (demand purchases)
--   - Each DCX purchase requires burning DIMO, making this
--     a direct proxy for demand-side activity
--   - Developer License NFT: 0x9A9D2E717bB005B240094ba761Ff074d392C7C85
--   - If this returns low row count, demand is very concentrated
-- ============================================================

WITH dimo_burns AS (
    SELECT
        "from" AS buyer,
        SUM(CAST(value AS DOUBLE) / 1e18) AS total_dimo_burned,
        COUNT(*) AS txn_count,
        MIN(evt_block_time) AS first_burn,
        MAX(evt_block_time) AS last_burn
    FROM erc20_polygon.evt_Transfer
    WHERE contract_address = 0xE261D618a959aFfFd53168Cd07D12E37B26761db
      AND "to" = 0x0000000000000000000000000000000000000000
      AND evt_block_time >= TIMESTAMP '2024-01-01'
      AND evt_block_time < TIMESTAMP '2026-04-01'
    GROUP BY "from"
),
totals AS (
    SELECT SUM(total_dimo_burned) AS grand_total FROM dimo_burns
),
shares AS (
    SELECT
        b.buyer,
        b.total_dimo_burned,
        b.txn_count,
        b.first_burn,
        b.last_burn,
        b.total_dimo_burned / t.grand_total AS share
    FROM dimo_burns b
    CROSS JOIN totals t
)
SELECT
    buyer,
    total_dimo_burned,
    txn_count,
    first_burn,
    last_burn,
    ROUND(share * 100, 4) AS pct_of_total,
    ROUND(POWER(share, 2), 8) AS hhi_contribution
FROM shares
ORDER BY total_dimo_burned DESC
