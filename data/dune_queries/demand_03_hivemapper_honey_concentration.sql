-- ============================================================
-- Query: Hivemapper HONEY Burn Concentration — Full HHI
-- Paper: Paper 2 ("GeoDePIN: Design Patterns")
-- Section: Exhibit 4 — Demand HHI
-- Chain: Solana
-- Time Range: Jan 2025 to Mar 2026
-- Dune Query ID: 6942583
-- Author: Zach Zukowski
-- Notes:
--   - HONEY mint: 4vMsoUT2BWatFweudnQM1xedRLfJgJ7hswhcpz4xgBTy  ← VERIFIED
--   - Burns occur when map credits are purchased; 8,319 events, 75.8M HONEY
--   - action = 'burn' confirmed in tokens_solana.transfers
--   - RESULT: HHI = 0.9257 — top signer 3BYkM... = 96.1% (likely PROXY CONTRACT)
--   - Address 3BYkMaBytqQm9L9zJeSp2DNK58of8TgbDJNei2G7aCSX had 3,852 txns;
--     this is almost certainly a relayer/program that aggregates map credit burns
--   - True demand HHI is unknowable without off-chain buyer data from Hivemapper
-- ============================================================

WITH honey_burns AS (
    SELECT
        tx_signer AS signer,
        SUM(amount_display) AS total_honey_burned,
        COUNT(*) AS burn_count,
        MIN(block_time) AS first_burn,
        MAX(block_time) AS last_burn
    FROM tokens_solana.transfers
    WHERE token_mint_address = '4vMsoUT2BWatFweudnQM1xedRLfJgJ7hswhcpz4xgBTy'
      AND action = 'burn'
      AND block_date >= DATE '2025-01-01'
      AND block_date < DATE '2026-04-01'
    GROUP BY tx_signer
),
totals AS (
    SELECT SUM(total_honey_burned) AS grand_total FROM honey_burns
),
shares AS (
    SELECT
        b.signer,
        b.total_honey_burned,
        b.burn_count,
        b.first_burn,
        b.last_burn,
        b.total_honey_burned / t.grand_total AS share
    FROM honey_burns b
    CROSS JOIN totals t
)
SELECT
    signer,
    total_honey_burned,
    burn_count,
    first_burn,
    last_burn,
    ROUND(share * 100, 4) AS pct_of_total,
    ROUND(POWER(share, 2), 8) AS hhi_contribution
FROM shares
ORDER BY total_honey_burned DESC
